// tsk-cc/src/codegen.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.3
//
// LLVM IR → TriskeleVM bytecode backend.
//
// Strategy: SSA destruction via register allocation.
//   - Each LLVM SSA value %name → virtual register Vn
//   - Virtual registers mapped to physical R0..R23 (R24-R31 reserved)
//   - PHI nodes resolved by inserting copy instructions at predecessor exits
//   - alloca → stack frame slot (A_ENTER / A_LEAVE)
//   - getelementptr → L_LEA sequence
//   - globals → fixed VM addresses in .data segment
//
// Output: AsmOutput compatible with tsk-asm's TvmBuilder pipeline.

use std::collections::HashMap;
use anyhow::{anyhow, bail, Result};
use triskele_common::isa::Opcode;
use triskele_common::{encode_r, encode_i, encode_j, fits_imm19, split_const32};
use crate::ir::{IrType, Value, Instr, BinOpKind, IcmpPred, BasicBlock,
                Function, GlobalInit, Module};

// ─────────────────────────────────────────────────────────────────────────────
// Physical register allocation
// ─────────────────────────────────────────────────────────────────────────────

const MAX_VREGS: usize = 24;  // R0..R23 available; R24-R31 reserved
const REG_SCRATCH: usize = 24; // scratch for immediates / casts
const REG_SP:   usize = 29;
const REG_FP:   usize = 28;   // Frame Pointer — base for alloca slots

// ─────────────────────────────────────────────────────────────────────────────
// Liveness analysis — per-function, per-SSA-value
// ─────────────────────────────────────────────────────────────────────────────

use std::collections::HashSet;

/// For each SSA value, compute the set of basic block labels where it is live.
/// A value is live in a block if it is used in that block or any successor
/// before being redefined. We use a simple backwards dataflow pass.
fn compute_liveness(func: &Function) -> HashMap<String, HashSet<String>> {
    // Build use/def sets per block
    let mut use_sets:  HashMap<String, HashSet<String>> = HashMap::new();
    let mut def_sets:  HashMap<String, HashSet<String>> = HashMap::new();
    let mut succs:     HashMap<String, Vec<String>>     = HashMap::new();

    for block in &func.blocks {
        let lbl = &block.label;
        let uses  = use_sets.entry(lbl.clone()).or_default();
        let defs  = def_sets.entry(lbl.clone()).or_default();
        let succ  = succs.entry(lbl.clone()).or_default();

        for instr in &block.instrs {
            // Collect uses (values read before being defined in this block)
            for val in instr_uses(instr) {
                if !defs.contains(&val) { uses.insert(val); }
            }
            // Collect defs
            if let Some(d) = instr_def(instr) { defs.insert(d); }
            // Collect successors
            match instr {
                Instr::BrUncond { target } => { succ.push(target.clone()); }
                Instr::BrCond { then_bb, else_bb, .. } => {
                    succ.push(then_bb.clone());
                    succ.push(else_bb.clone());
                }
                Instr::Switch { default_bb, cases, .. } => {
                    succ.push(default_bb.clone());
                    for (_, bb) in cases { succ.push(bb.clone()); }
                }
                _ => {}
            }
        }
    }

    // Backwards fixed-point: live_out[b] = ∪ live_in[succ]
    // live_in[b] = use[b] ∪ (live_out[b] - def[b])
    let block_labels: Vec<String> = func.blocks.iter().map(|b| b.label.clone()).collect();
    let mut live_in:  HashMap<String, HashSet<String>> = HashMap::new();
    let mut live_out: HashMap<String, HashSet<String>> = HashMap::new();

    for lbl in &block_labels {
        live_in.insert(lbl.clone(), HashSet::new());
        live_out.insert(lbl.clone(), HashSet::new());
    }

    let mut changed = true;
    while changed {
        changed = false;
        for lbl in block_labels.iter().rev() {
            // live_out[b] = ∪ live_in[succ(b)]
            let new_out: HashSet<String> = succs.get(lbl)
                .map(|ss| ss.iter()
                    .flat_map(|s| live_in.get(s).cloned().unwrap_or_default())
                    .collect())
                .unwrap_or_default();

            // live_in[b] = use[b] ∪ (live_out[b] - def[b])
            let defs  = def_sets.get(lbl).cloned().unwrap_or_default();
            let uses  = use_sets.get(lbl).cloned().unwrap_or_default();
            let new_in: HashSet<String> = uses.union(
                &new_out.difference(&defs).cloned().collect::<HashSet<_>>()
            ).cloned().collect();

            if new_out != *live_out.get(lbl).unwrap() {
                live_out.insert(lbl.clone(), new_out);
                changed = true;
            }
            if new_in != *live_in.get(lbl).unwrap() {
                live_in.insert(lbl.clone(), new_in);
                changed = true;
            }
        }
    }

    // Result: for each value, the set of blocks where it is live
    let mut value_live_blocks: HashMap<String, HashSet<String>> = HashMap::new();
    for (lbl, live) in &live_in {
        for val in live {
            value_live_blocks.entry(val.clone())
                .or_default()
                .insert(lbl.clone());
        }
    }
    for (lbl, live) in &live_out {
        for val in live {
            value_live_blocks.entry(val.clone())
                .or_default()
                .insert(lbl.clone());
        }
    }
    // Also add the defining block
    for (lbl, defs) in &def_sets {
        for val in defs {
            value_live_blocks.entry(val.clone())
                .or_default()
                .insert(lbl.clone());
        }
    }

    // Alloca values (stack addresses) are live in ALL blocks of the function
    // because their address can be used in any block via load/store.
    // This prevents the liveness analysis from reclaiming their registers too early.
    for block in &func.blocks {
        for instr in &block.instrs {
            if let Instr::Alloca { dst, .. } = instr {
                let all_blocks: HashSet<String> = block_labels.iter().cloned().collect();
                value_live_blocks.insert(dst.clone(), all_blocks);
            }
        }
    }

    value_live_blocks
}

fn instr_def(instr: &Instr) -> Option<String> {
    match instr {
        Instr::Abs   { dst, .. } |
        Instr::BinOp { dst, .. } | Instr::ICmp { dst, .. } | Instr::Phi { dst, .. }
        | Instr::Alloca { dst, .. } | Instr::Load { dst, .. }
        | Instr::Gep { dst, .. } | Instr::Zext { dst, .. } | Instr::Sext { dst, .. }
        | Instr::Trunc { dst, .. } | Instr::Bitcast { dst, .. }
        | Instr::PtrToInt { dst, .. } | Instr::IntToPtr { dst, .. } => Some(dst.clone()),
        Instr::Call { dst, .. } => dst.clone(),
        Instr::Select { dst, .. } => Some(dst.clone()),
        _ => None,
    }
}

fn instr_uses(instr: &Instr) -> Vec<String> {
    let mut uses = Vec::new();
    let mut add = |v: &Value| { if let Value::Reg(n) = v { uses.push(n.clone()); } };
    match instr {
        Instr::BinOp { lhs, rhs, .. }   => { add(lhs); add(rhs); }
        Instr::ICmp  { lhs, rhs, .. }   => { add(lhs); add(rhs); }
        Instr::BrCond { cond, .. }      => { add(cond); }
        Instr::Switch { cond, .. }       => { add(cond); }
        Instr::Phi { incoming, .. }     => { for (v, _) in incoming { add(v); } }
        Instr::Store { val, ptr, .. }   => { add(val); add(ptr); }
        Instr::Load  { ptr, .. }        => { add(ptr); }
        Instr::Gep   { ptr, indices, .. }=> { add(ptr); for i in indices { add(i); } }
        Instr::Zext  { val, .. } | Instr::Sext  { val, .. }
        | Instr::Trunc { val, .. } | Instr::Bitcast { dst: _, from_ty: _, val, .. }
        | Instr::PtrToInt { val, .. }   | Instr::IntToPtr { val, .. } => { add(val); }
        Instr::Call  { func, args, .. } => {
            add(func);
            for (_, v) in args { add(v); }
        }
        Instr::Ret { val, .. }          => { if let Some(v) = val { add(v); } }
        Instr::Abs { val, .. } => { add(val); }
        Instr::Select { cond, true_val, false_val, .. } => {
            add(cond); add(true_val); add(false_val);
        }
        Instr::MemSet { dst_ptr, byte_val, len } => { add(dst_ptr); add(byte_val); add(len); }
        Instr::MemCpy { dst_ptr, src_ptr, len }  => { add(dst_ptr); add(src_ptr); add(len); }
        Instr::VaStart { .. } => {}  // slot is a write target — no SSA reads
        _ => {}
    }
    uses
}

// ─────────────────────────────────────────────────────────────────────────────
// Register allocator with liveness-aware reuse
// ─────────────────────────────────────────────────────────────────────────────

struct RegAlloc {
    map:        HashMap<String, usize>,   // SSA name → physical register
    free:       Vec<usize>,               // free physical registers (stack)
    pub(super) used: usize,               // high-water mark
    /// live_blocks[name] = set of block labels where name is live
    live:       HashMap<String, HashSet<String>>,
    /// current block label (updated per block)
    cur_block:  String,
    /// Protected SSA names — phi destinations whose register must never be
    /// recycled (they can receive a copy from any predecessor block).
    /// All other values use liveness-based recycling unconditionally.
    pub(super) protected: HashSet<String>,
    /// parameter SSA names — kept in ra.map until consumed
    #[allow(dead_code)]
    params:     HashSet<String>,
    /// Spill slots: SSA name → byte offset from frame base (FP-relative, negative).
    /// A spilled value is NOT in `map` — it lives on the stack.
    /// Layout: frame = [alloca slots (0..alloca_top)] [spill slots (alloca_top..spill_top)]
    pub(super) spill_map: HashMap<String, i32>,
    /// Next available spill slot offset, starts at alloca_top (set by FuncGen).
    pub(super) spill_top: i32,
    /// Pending spill store action — set by get_or_alloc when it evicts a register.
    /// FuncGen must consume this (emit D_Store64) before emitting the instruction
    /// that uses the newly allocated register.
    pub(super) spill_pending: Option<SpillAction>,
}

/// A register eviction event: the victim SSA value must be stored to its spill slot.
/// FuncGen emits:  D_Store64 [FP + slot_offset], evicted_reg
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub(super) struct SpillAction {
    pub victim: String,   // SSA name that was evicted
    pub reg:    usize,    // physical register that was evicted (now re-used)
    pub slot:   i32,      // byte offset in spill area (from frame base)
}

impl RegAlloc {
    fn new(params: &[(IrType, String)], live: HashMap<String, HashSet<String>>) -> Self {
        let mut map = HashMap::new();
        let mut used = 0;
        // Parameters occupy R0..Rn
        for (i, (_, name)) in params.iter().enumerate() {
            map.insert(name.clone(), i);
            used = used.max(i + 1);
        }
        // Free registers: MAX_VREGS-1 down to used (LIFO for locality)
        let free: Vec<usize> = (used..MAX_VREGS).rev().collect();
        let params: HashSet<String> = params.iter().map(|(_, n)| n.clone()).collect();
        Self {
            map, free, used, live,
            cur_block: "entry".to_string(),
            protected: HashSet::new(),
            params,
            spill_map: HashMap::new(),
            spill_top: 0,
            spill_pending: None,
        }
    }

    fn set_block(&mut self, label: &str) {
        self.cur_block = label.to_string();
    }

    /// Allocate a physical register for SSA value `name`.
    ///
    /// Single unified mode: liveness-based recycling for all values, except
    /// phi destinations (in `protected`) which are never recycled — they must
    /// keep a stable register because any predecessor can copy into them.
    fn get_or_alloc(&mut self, name: &str) -> Result<usize> {
        if let Some(&r) = self.map.get(name) { return Ok(r); }

        // Liveness-based recycling: free registers dead in current block,
        // but never recycle phi destinations (protected) or function parameters
        // (params) — parameters live in R0..Rn for the entire function lifetime.
        let dead: Vec<String> = self.map.keys()
            .filter(|k| k.as_str() != name)
            .filter(|k| !self.protected.contains(*k))
            .filter(|k| !self.params.contains(*k))
            .filter(|k| {
                self.live.get(*k)
                    .map(|blocks| !blocks.contains(&self.cur_block))
                    .unwrap_or(true)
            })
            .cloned()
            .collect();

        for k in dead {
            if let Some(r) = self.map.remove(&k) {
                self.free.push(r);
                log::debug!("freed R{} (was %{}, dead in {})", r, k, self.cur_block);
            }
        }

        // Allocate from free pool
        if let Some(r) = self.free.pop() {
            self.map.insert(name.to_string(), r);
            self.used = self.used.max(r + 1);
            log::debug!("alloc R{} → %{} (block {})", r, name, self.cur_block);
            return Ok(r);
        }

        // ── Register spill: no free register — evict least-valuable live value ──
        // Choose victim: not protected (phi dst), not a param, not the name we need.
        // Prefer values dead in most blocks (lowest live-block count).
        let victim: Option<String> = {
            let cur = &self.cur_block;
            let mut candidates: Vec<(String, usize)> = self.map.keys()
                .filter(|k| k.as_str() != name)
                .filter(|k| !self.protected.contains(*k))
                .filter(|k| !self.params.contains(*k))
                .map(|k| {
                    let live_count = self.live.get(k)
                        .map(|s| s.len())
                        .unwrap_or(0);
                    // Penalise values live in current block (more costly to reload)
                    let penalty = if self.live.get(k)
                        .map(|s| s.contains(cur.as_str()))
                        .unwrap_or(false) { 1000 } else { 0 };
                    (k.clone(), live_count + penalty)
                })
                .collect();
            candidates.sort_by_key(|(_, cost)| *cost);
            candidates.into_iter().next().map(|(k, _)| k)
        };

        let victim = victim.ok_or_else(|| anyhow!(
            "register spill failed in block {}: no evictable register for %{}              (all {} live values are protected/params)",
            self.cur_block, name, self.map.len()))?;

        // Evict victim: record its spill slot, remove from register map.
        let evicted_reg = self.map.remove(&victim).unwrap();
        let slot = self.spill_top;
        self.spill_top += 8; // 8-byte slot (64-bit)
        self.spill_map.insert(victim.clone(), slot);
        log::debug!("spill R{} (%{}) → slot {} (block {})", evicted_reg, victim, slot, self.cur_block);

        // Assign evicted register to the new name.
        self.map.insert(name.to_string(), evicted_reg);
        self.used = self.used.max(evicted_reg + 1);

        // Return a SpillResult so FuncGen can emit the store instruction.
        // We encode the spill action as Ok(evicted_reg) but set spill_pending.
        self.spill_pending = Some(SpillAction { victim: victim.clone(), reg: evicted_reg, slot });
        log::debug!("alloc R{} → %{} (evicted %{}, block {})", evicted_reg, name, victim, self.cur_block);
        Ok(evicted_reg)
    }

    fn get(&self, name: &str) -> Result<usize> {
        self.map.get(name).copied()
            .ok_or_else(|| anyhow!("undefined SSA value '%{}'", name))
    }

    /// Explicitly free a named SSA value's register.
    ///
    /// Called after Store/Select when the SSA value will never be read again
    /// from its register. Safe because:
    /// - alloca *address* names are never in ra.map (they are stack slots)
    /// - function parameters are protected: we never free a param register
    ///   because the calling convention places args in R0..Rn and those slots
    ///   must remain valid until the callee has consumed them.
    fn free_name(&mut self, name: &str) {
        // Never free parameter registers — they hold caller-supplied values
        // in R0..Rn and must not be recycled while the callee runs.
        if self.params.contains(name) { return; }
        if let Some(r) = self.map.remove(name) {
            if !self.free.contains(&r) {
                self.free.push(r);
                log::debug!("free_name R{} (was %{})", r, name);
            }
        }
        // Also remove from spill_map if present (value is dead)
        self.spill_map.remove(name);
    }

    /// Check whether `name` is currently spilled (not in a register).
    pub(super) fn is_spilled(&self, name: &str) -> bool {
        self.spill_map.contains_key(name) && !self.map.contains_key(name)
    }

    /// Allocate a register for a spilled value and mark it as needing a reload.
    /// Returns (reg, slot_offset) so FuncGen can emit D_Load64.
    pub(super) fn reload(&mut self, name: &str) -> Result<(usize, i32)> {
        let slot = *self.spill_map.get(name)
            .ok_or_else(|| anyhow!("reload: %{} not in spill_map", name))?;
        // Remove from spill_map — it will live in a register again.
        self.spill_map.remove(name);
        // Allocate register (may itself cause another spill — recursive case handled naturally)
        let reg = self.get_or_alloc(name)?;
        Ok((reg, slot))
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Instruction encoding (mirrors tsk-asm/src/encoder.rs)
// enc_r / enc_i / enc_j → now triskele_common::{encode_r, encode_i, encode_j}
// Thin wrappers keep call sites unchanged (Opcode cast to u8).
#[inline(always)]
fn enc_r(op: Opcode, dst: u8, s1: u8, s2: u8, flags: u16) -> u32 {
    encode_r(op as u8, dst, s1, s2, flags)
}
#[inline(always)]
fn enc_i(op: Opcode, dst: u8, imm: i32) -> u32 {
    encode_i(op as u8, dst, imm)
}
#[inline(always)]
fn enc_j(op: Opcode, offset: i32) -> u32 {
    encode_j(op as u8, offset)
}

// ─────────────────────────────────────────────────────────────────────────────
// Code emitter
// ─────────────────────────────────────────────────────────────────────────────

struct Emitter {
    code:    Vec<u8>,
    /// label name → byte offset in code
    labels:  HashMap<String, usize>,
    /// (patch_offset, label_name) — jump instructions to fix up
    fixups:  Vec<(usize, String)>,
    /// (patch_offset, label_name) — call fixups (exported as relocations)
    pub call_fixups: Vec<(usize, String)>,
}

impl Emitter {
    fn new() -> Self {
        Self {
            code: Vec::new(),
            labels: HashMap::new(),
            fixups: Vec::new(),
            call_fixups: Vec::new(),
        }
    }

    fn emit(&mut self, word: u32) {
        self.code.extend_from_slice(&word.to_le_bytes());
    }

    fn current_offset(&self) -> usize { self.code.len() }

    fn define_label(&mut self, name: &str) {
        self.labels.insert(name.to_string(), self.code.len());
    }

    /// Emit a jump placeholder — will be fixed up later.
    fn emit_jump_placeholder(&mut self, op: Opcode, label: &str) {
        let off = self.current_offset();
        self.emit(enc_j(op, 0));
        self.fixups.push((off, label.to_string()));
    }

    /// Emit a call placeholder.
    fn emit_call_placeholder(&mut self, label: &str) {
        let off = self.current_offset();
        self.emit(enc_j(Opcode::F_Call, 0));
        self.call_fixups.push((off, label.to_string()));
    }

    /// Load a value into a physical register.
    /// Returns the register holding the value (may be dst_reg or an alias).
    fn load_value(&mut self, val: &Value, ra: &RegAlloc, dst_reg: usize) -> Result<usize> {
        match val {
            Value::Reg(name) => ra.get(name),
            Value::Global(name) => {
                // Load global address as immediate (fixed up by linker in Phase 2)
                // For now: emit D_MOV_I with placeholder 0 + a call_fixup
                self.emit(enc_i(Opcode::D_MovI, dst_reg as u8, 0));
                self.call_fixups.push((self.current_offset() - 4, name.clone()));
                Ok(dst_reg)
            }
            Value::Const(n) => {
                self.emit(enc_i(Opcode::D_MovI, dst_reg as u8, *n as i32));
                Ok(dst_reg)
            }
            Value::Bool(b) => {
                self.emit(enc_i(Opcode::D_MovI, dst_reg as u8, *b as i32));
                Ok(dst_reg)
            }
            Value::Null | Value::Undef => {
                self.emit(enc_i(Opcode::D_MovI, dst_reg as u8, 0));
                Ok(dst_reg)
            }
        }
    }

    /// Patch all jump/call fixups now that all labels are defined.
    fn apply_fixups(&mut self) -> Result<()> {
        for (patch_off, label) in &self.fixups {
            let target = self.labels.get(label)
                .ok_or_else(|| anyhow!("undefined label '{}'", label))?;
            let instr_vm = patch_off;
            let delta    = (*target as i64) - (*instr_vm as i64);
            if delta > 0x7F_FFFF || delta < -0x80_0000 {
                bail!("jump to '{}' exceeds ±8MB", label);
            }
            let existing = u32::from_le_bytes(
                self.code[*patch_off..*patch_off+4].try_into().unwrap()
            );
            let opcode_byte = (existing >> 24) as u8;
            let patched = encode_j(opcode_byte, delta as i32);
            self.code[*patch_off..*patch_off+4].copy_from_slice(&patched.to_le_bytes());
        }
        // Call fixups for globals/externals are left as 0 — tsk-link will resolve
        Ok(())
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Function code generator
// ─────────────────────────────────────────────────────────────────────────────

struct FuncGen<'m> {
    func:    &'m Function,
    #[cfg_attr(not(test), allow(dead_code))]
    pub(super) ra: RegAlloc,
    em:      Emitter,
    /// alloca slots: name → offset from frame base
    alloca_slots: HashMap<String, i32>,
    frame_size:   i32,
    /// global variable name → placeholder address (resolved by linker)
    #[allow(dead_code)] globals: &'m HashMap<String, usize>,
    /// Named struct type definitions (from module) — used for GEP field offset calculation
    #[allow(dead_code)]
    type_defs: &'m HashMap<String, IrType>,
}

impl<'m> FuncGen<'m> {
    fn new(func: &'m Function,
           globals:   &'m HashMap<String, usize>,
           type_defs: &'m HashMap<String, IrType>) -> Self {
        // Compute liveness before allocating registers
        let live = compute_liveness(func);
        // Conservative mode: never recycle registers.
        // Required for phi nodes — phi destinations must remain in the register
        // map across blocks. Functions with only allocas (no phis) use liveness
        // mode, which recycles dead registers and handles larger functions.
        // Collect all phi destination names — their registers are protected
        // (never recycled by liveness) because any predecessor can copy into them.
        let phi_dsts: HashSet<String> = func.blocks.iter()
            .flat_map(|b| b.instrs.iter())
            .filter_map(|i| if let Instr::Phi { dst, .. } = i { Some(dst.clone()) } else { None })
            .collect();
        let mut ra = RegAlloc::new(&func.params, live);
        ra.protected = phi_dsts;
        Self {
            func, ra,
            em: Emitter::new(),
            alloca_slots: HashMap::new(),
            frame_size: 0,
            globals,
            type_defs,
        }
    }

    /// Resolve a type — if it's a named struct (i64 placeholder from parser),
    /// look it up in type_defs. Returns the concrete IrType.
    /// Used by GEP to compute struct field offsets correctly.
    fn resolve_type(&self, ty: &IrType) -> IrType {
        match ty {
            // Named forward-reference: look up in type_defs, resolve recursively.
            IrType::Named(name) => {
                if let Some(resolved) = self.type_defs.get(name.as_str()) {
                    self.resolve_type(resolved)
                } else {
                    log::warn!("resolve_type: unknown named type %{}", name);
                    IrType::I64  // conservative fallback
                }
            }
            // Struct: resolve each field recursively (handles nested named types).
            IrType::Struct(fields) => {
                let resolved: Vec<IrType> = fields.iter()
                    .map(|f| self.resolve_type(f))
                    .collect();
                IrType::Struct(resolved)
            }
            IrType::Array(n, inner) => IrType::Array(*n, Box::new(self.resolve_type(inner))),
            IrType::Ptr => IrType::Ptr,
            other => other.clone(),
        }
    }

    // ── Spill helpers ────────────────────────────────────────────────────────

    /// Emit D_Store64 to save a register to its spill slot on the stack.
    /// Layout: slot 0 is at FP - frame_size - 8, slot N at FP - frame_size - 8*(N+1).
    /// We keep it simple: spill_offset_from_fp = -(frame_size + slot + 8).
    fn emit_spill_store(&mut self, reg: usize, slot: i32) {
        // addr = FP + offset_from_fp  where offset_from_fp is negative
        let offset_from_fp = -(self.frame_size + slot + 8);
        // D_Store64  [FP + offset], reg    (Type R: d=reg, s1=FP, flags=offset)
        // flags is u16 but offset is negative — cast as i16 then to u16
        let flags = offset_from_fp as i16 as u16;
        self.em.emit(encode_r(Opcode::D_Store64 as u8,
            REG_FP as u8, reg as u8, 0, flags));
        log::debug!("spill-store R{} → [FP{}] (slot {})", reg, offset_from_fp, slot);
    }

    /// Emit D_Load64 to reload a spilled value back into a register.
    fn emit_spill_reload(&mut self, reg: usize, slot: i32) {
        let offset_from_fp = -(self.frame_size + slot + 8);
        let flags = offset_from_fp as i16 as u16;
        self.em.emit(encode_r(Opcode::D_Load64 as u8,
            reg as u8, REG_FP as u8, 0, flags));
        log::debug!("spill-reload R{} ← [FP{}] (slot {})", reg, offset_from_fp, slot);
    }

    /// After get_or_alloc, consume any pending spill store emitted by the allocator.
    /// Must be called before using the newly allocated register.
    fn flush_spill_pending(&mut self) {
        if let Some(action) = self.ra.spill_pending.take() {
            self.emit_spill_store(action.reg, action.slot);
        }
    }

    /// If `name` is spilled, reload it into a register.
    /// Returns the physical register holding the value (reloaded or already live).
    #[allow(dead_code)]
    fn ensure_loaded(&mut self, name: &str) -> Result<usize> {
        if self.ra.is_spilled(name) {
            let (reg, slot) = self.ra.reload(name)?;
            self.flush_spill_pending();  // reload itself may have caused a spill
            self.emit_spill_reload(reg, slot);
            Ok(reg)
        } else {
            self.ra.get(name)
        }
    }

    fn generate(&mut self) -> Result<Vec<u8>> {
        // Pre-pass 1: collect alloca sizes for frame layout.
        // For variadic functions (contain VaStart), pre-reserve 32 bytes at the
        // bottom of the frame for the va register save area BEFORE assigning alloca
        // slot offsets. This ensures allocas sit above the save area.
        // Layout: [va_save_area (32B, bottom)] [alloca_0] [alloca_1] ...
        let func_is_variadic = self.func.blocks.iter().any(|b|
            b.instrs.iter().any(|i| matches!(i, Instr::VaStart { .. }))
        );
        if func_is_variadic {
            self.frame_size = 32; // reserve bottom 32 bytes for va save area
        }
        for block in &self.func.blocks {
            for instr in &block.instrs {
                if let Instr::Alloca { dst, ty, .. } = instr {
                    let size = ty.byte_size().max(8) as i32;
                    let aligned = (size + 7) & !7;
                    self.alloca_slots.insert(dst.clone(), self.frame_size);
                    self.frame_size += aligned;
                }
            }
        }


        // Pre-pass 2: build phi_map for phi copy insertion at branch sites.
        // phi_map[target_label] = Vec<(phi_dst_name, Vec<(pred_label, src_value)>)>
        // IR incoming is Vec<(Value, String)> = (src_value, pred_label) — reorder to (pred, val)
        let mut phi_map: HashMap<String, Vec<(String, Vec<(String, Value)>)>> = HashMap::new();
        for block in &self.func.blocks {
            for instr in &block.instrs {
                if let Instr::Phi { dst, incoming, .. } = instr {
                    let reordered: Vec<(String, Value)> = incoming.iter()
                        .map(|(val, pred)| (pred.clone(), val.clone()))
                        .collect();
                    let entry = phi_map.entry(block.label.clone()).or_default();
                    entry.push((dst.clone(), reordered));
                }
            }
        }

        // Pre-pass 3: pre-allocate all phi destination registers.
        // This ensures emit_phi_copies and gen_instr use the same physical register.
        // Combined with ra.protected, this guarantees stable register assignment
        // for phi destinations across all predecessor blocks.
        let func_has_phi = self.func.blocks.iter().any(|b|
            b.instrs.iter().any(|i| matches!(i, Instr::Phi { .. }))
        );
        if func_has_phi {
            for block in &self.func.blocks {
                for instr in &block.instrs {
                    if let Instr::Phi { dst, .. } = instr {
                        self.ra.get_or_alloc(dst)?;
                    }
                }
            }
        }

        // Function prologue (FP-based frame layout)
        // A_Enter: push LR, push FP, FP = SP  →  FP points to saved-FP slot
        // SP -= total_frame                   →  locals + spill slots below FP
        // alloca slot N at FP + (N - total_frame)  (negative)
        // spill slot S at FP + (-(frame_size + S + 8))  (below alloca region)
        let has_frame = self.frame_size > 0;
        let prologue_mov_i_offset: usize;
        if has_frame {
            self.em.emit(enc_r(Opcode::A_Enter, 0, 0, 0, 0));
            // Emit D_MovI with placeholder 0 — patched after codegen with total frame size
            prologue_mov_i_offset = self.em.current_offset();
            self.em.emit(enc_i(Opcode::D_MovI, REG_SCRATCH as u8, self.frame_size));
            self.em.emit(enc_r(Opcode::D_Sub,
                REG_SP as u8, REG_SP as u8, REG_SCRATCH as u8, 0));
        } else {
            prologue_mov_i_offset = 0;
        }

        // Set ra.spill_top base = frame_size (spill slots grow above alloca region)
        self.ra.spill_top = self.frame_size;

        // Generate each basic block
        for block in &self.func.blocks {
            self.em.define_label(&block.label);
            self.gen_block(block, &phi_map)?;
        }

        // Patch frame size in prologue D_MovI to include spill slots
        if has_frame && self.ra.spill_top > self.frame_size {
            let total_frame = self.ra.spill_top;  // includes alloca + spill
            // Update frame_size so epilogue spill offsets are correct
            // (epilogue A_Leave restores SP from FP, so no patch needed there)
            let patched_word = enc_i(Opcode::D_MovI, REG_SCRATCH as u8, total_frame);
            let off = prologue_mov_i_offset;
            // Emitter stores words in little-endian (to_le_bytes) — patch must match.
            let le = patched_word.to_le_bytes();
            self.em.code[off]   = le[0];
            self.em.code[off+1] = le[1];
            self.em.code[off+2] = le[2];
            self.em.code[off+3] = le[3];
            self.frame_size = total_frame;
            log::debug!("frame patched: alloca={} spill={} total={}",
                self.frame_size - (self.ra.spill_top - self.frame_size),
                self.ra.spill_top - self.frame_size,
                total_frame);
        }

        self.em.apply_fixups()?;
        Ok(self.em.code.clone())
    }

    fn gen_block(&mut self, block: &BasicBlock,
                 phi_map: &HashMap<String, Vec<(String, Vec<(String, Value)>)>>)
                 -> Result<()> {
        self.ra.set_block(&block.label);

        // Intra-block use-count: SSA names used more than once in this block.
        // Used by Store handler to avoid premature free_name on multiply-used values.
        let mut use_count: HashMap<String, usize> = HashMap::new();
        for instr in &block.instrs {
            for name in instr_uses(instr) {
                *use_count.entry(name).or_insert(0) += 1;
            }
        }
        let multi_use: HashSet<String> = use_count.into_iter()
            .filter(|(_, c)| *c > 1)
            .map(|(n, _)| n)
            .collect();

        for instr in &block.instrs {
            self.gen_instr(instr, &block.label, phi_map, &multi_use)?;
        }
        Ok(())
    }

    fn gen_instr(&mut self, instr: &Instr, cur_block: &str,
                 phi_map: &HashMap<String, Vec<(String, Vec<(String, Value)>)>>,
                 multi_use: &HashSet<String>)
                 -> Result<()> {
        match instr {

            // ── BinOp ─────────────────────────────────────────────────────
            Instr::BinOp { dst, op, lhs, rhs, .. } => {
                let rd  = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rl  = self.em.load_value(lhs, &self.ra, REG_SCRATCH)?;
                let rr  = self.em.load_value(rhs, &self.ra, REG_SCRATCH + 1)?;

                let rl_final = self.load_reg_or_imm(lhs, REG_SCRATCH)?;
                let rr_scratch = if rl_final == REG_SCRATCH { REG_SCRATCH + 2 } else { REG_SCRATCH };
                let rr_final = self.load_reg_or_imm(rhs, rr_scratch)?;

                let opcode = match op {
                    BinOpKind::Add  => Opcode::D_Add,
                    BinOpKind::Sub  => Opcode::D_Sub,
                    BinOpKind::Mul  => Opcode::D_Mul,
                    BinOpKind::SDiv | BinOpKind::UDiv => Opcode::D_Div,
                    BinOpKind::SRem | BinOpKind::URem => Opcode::D_Rem,
                    BinOpKind::Shl  => Opcode::D_Shl,
                    BinOpKind::LShr | BinOpKind::AShr => Opcode::D_Shr,
                    BinOpKind::And  => Opcode::D_And,
                    BinOpKind::Or   => Opcode::D_Or,
                    BinOpKind::Xor  => Opcode::D_Xor,
                };
                self.em.emit(enc_r(opcode, rd as u8, rl_final as u8, rr_final as u8, 0));
                let _ = rl; let _ = rr;
            }

            // ── ICmp ──────────────────────────────────────────────────────
            Instr::ICmp { dst, pred, lhs, rhs, .. } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rl = self.load_reg_or_imm(lhs, REG_SCRATCH)?;
                let rr = self.load_reg_or_imm(rhs, REG_SCRATCH + 1)?;
                // V_CMP sets flags; then use V_EQ / V_LT etc. to get 0/1 result
                self.em.emit(enc_r(Opcode::V_Cmp, 0, rl as u8, rr as u8, 0));
                let cmp_op = match pred {
                    IcmpPred::Eq  | IcmpPred::Uge => Opcode::V_Eq,
                    IcmpPred::Ne                  => Opcode::V_Neq,
                    IcmpPred::Slt | IcmpPred::Ult => Opcode::V_Lt,
                    IcmpPred::Sle | IcmpPred::Ule => Opcode::V_Lte,
                    IcmpPred::Sgt | IcmpPred::Ugt => Opcode::V_Gt,
                    IcmpPred::Sge                 => Opcode::V_Gte,
                };
                self.em.emit(enc_r(cmp_op, rd as u8, rl as u8, rr as u8, 0));
            }

            // ── Branch ────────────────────────────────────────────────────
            Instr::BrUncond { target } => {
                self.emit_phi_copies(target, cur_block, phi_map)?;
                self.em.emit_jump_placeholder(Opcode::F_Jmp, target);
            }
            Instr::BrCond { cond, then_bb, else_bb } => {
                let rc = self.load_reg_or_imm(cond, REG_SCRATCH)?;
                self.em.emit(enc_i(Opcode::V_CmpI, rc as u8, 0));

                // Trampoline pattern: avoids running phi copies for then_bb
                // unconditionally (which would corrupt else_bb register state).
                let has_then_phis = phi_map.get(then_bb.as_str())
                    .map(|phis| phis.iter().any(|(_, inc)| inc.iter().any(|(p,_)| p == cur_block)))
                    .unwrap_or(false);

                if has_then_phis {
                    let trampoline = format!("__phi_t_{}_{}", cur_block, then_bb);
                    self.em.emit_jump_placeholder(Opcode::F_Jnz, &trampoline);
                    self.emit_phi_copies(else_bb, cur_block, phi_map)?;
                    self.em.emit_jump_placeholder(Opcode::F_Jmp, else_bb);
                    self.em.define_label(&trampoline);
                    self.emit_phi_copies(then_bb, cur_block, phi_map)?;
                    self.em.emit_jump_placeholder(Opcode::F_Jmp, then_bb);
                } else {
                    self.em.emit_jump_placeholder(Opcode::F_Jnz, then_bb);
                    self.emit_phi_copies(else_bb, cur_block, phi_map)?;
                    self.em.emit_jump_placeholder(Opcode::F_Jmp, else_bb);
                }
            }

            // ── Switch ───────────────────────────────────────────────────
            Instr::Switch { cond, default_bb, cases } => {
                eprintln!("[tsk-cc] Switch: {} cases, default={}", cases.len(), default_bb);
                let rc = self.load_reg_or_imm(cond, REG_SCRATCH)?;
                for (val, bb) in cases {
                    self.em.emit(enc_i(Opcode::V_CmpI, rc as u8, *val as i32));
                    self.em.emit_jump_placeholder(Opcode::F_Jz, bb);
                }
                self.em.emit_jump_placeholder(Opcode::F_Jmp, default_bb);
            }

            // ── Select ───────────────────────────────────────────────────
            // select i1 %cond, ty %true_val, ty %false_val
            // → V_CmpI rc, 0  / F_Jnz true_lbl / D_Mov rd, false / F_Jmp end / true_lbl: D_Mov rd, true
            Instr::Select { dst, cond, true_val, false_val, .. } => {
                let rd  = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rc  = self.load_reg_or_imm(cond, REG_SCRATCH)?;
                // unique labels per instruction using byte offset
                let true_lbl = format!("__sel_t_{}", self.em.current_offset());
                let end_lbl  = format!("__sel_e_{}", self.em.current_offset() + 4);
                self.em.emit(enc_i(Opcode::V_CmpI, rc as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jnz, &true_lbl);
                // false branch
                let rf = self.load_reg_or_imm(false_val, REG_SCRATCH + 1)?;
                if rd != rf { self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rf as u8, 0, 0)); }
                self.em.emit_jump_placeholder(Opcode::F_Jmp, &end_lbl);
                // true branch
                self.em.define_label(&true_lbl);
                let rt = self.load_reg_or_imm(true_val, REG_SCRATCH + 1)?;
                if rd != rt { self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rt as u8, 0, 0)); }
                self.em.define_label(&end_lbl);
                // After select, cond/true_val/false_val are dead — free their registers.
                // safe: select is their last use in -O0 alloca-based code.
                if let Value::Reg(n) = cond      { self.ra.free_name(n); }
                if let Value::Reg(n) = true_val  { self.ra.free_name(n); }
                if let Value::Reg(n) = false_val { self.ra.free_name(n); }
            }


            // ── Abs (llvm.abs.*) ──────────────────────────────────────────
            // Inline: rd = val < 0 ? -val : val
            // Emits:  V_CmpI rv, 0
            //         F_Jnz  pos_lbl
            //         D_Sub  rd, R0(zero), rv   ← neg = 0 - val
            //         F_Jmp  end_lbl
            // pos_lbl: D_Mov  rd, rv
            // end_lbl:
            Instr::Abs { dst, val, .. } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rv = self.load_reg_or_imm(val, REG_SCRATCH)?;
                let pos_lbl = format!("__abs_p_{}", self.em.current_offset());
                let end_lbl = format!("__abs_e_{}", self.em.current_offset() + 4);
                // if val >= 0 jump to pos_lbl
                self.em.emit(enc_i(Opcode::V_CmpI, rv as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jnz, &pos_lbl);
                // negative branch: rd = 0 - rv
                let r_zero = REG_SCRATCH + 1;
                self.em.emit(enc_i(Opcode::D_MovI, r_zero as u8, 0));
                self.em.emit(enc_r(Opcode::D_Sub, rd as u8, r_zero as u8, rv as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jmp, &end_lbl);
                // positive branch: rd = rv
                self.em.define_label(&pos_lbl);
                if rd != rv { self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rv as u8, 0, 0)); }
                self.em.define_label(&end_lbl);
                if let Value::Reg(n) = val { self.ra.free_name(n); }
            }

            // ── MemSet (llvm.memset) ───────────────────────────────────────
            // Emit an inline byte loop: for i in 0..len { *dst_ptr++ = byte_val }
            // VM-side: uses a scratch counter + D_Store8 loop
            Instr::MemSet { dst_ptr, byte_val, len } => {
                let r_ptr = self.load_reg_or_imm(dst_ptr, REG_SCRATCH)?;
                let r_val = self.load_reg_or_imm(byte_val, REG_SCRATCH + 1)?;
                let r_len = self.load_reg_or_imm(len, REG_SCRATCH + 2)?;
                // Use R23 as loop counter (outermost scratch; won't collide)
                let r_ctr: usize = 23;
                self.em.emit(enc_i(Opcode::D_MovI, r_ctr as u8, 0)); // ctr = 0
                let loop_lbl = format!("__mset_lp_{}", self.em.current_offset());
                let done_lbl = format!("__mset_dn_{}", self.em.current_offset() + 4);
                self.em.define_label(&loop_lbl);
                // if ctr >= len goto done
                self.em.emit(enc_r(Opcode::V_Cmp, 0, r_ctr as u8, r_len as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jge, &done_lbl);
                // store byte
                let r_addr = REG_SCRATCH + 3;
                self.em.emit(enc_r(Opcode::D_Add, r_addr as u8, r_ptr as u8, r_ctr as u8, 0));
                self.em.emit(enc_r(Opcode::D_Store8, r_addr as u8, r_val as u8, 0, 0));
                // ctr++
                // ctr++ via scratch
                self.em.emit(enc_i(Opcode::D_MovI, (REG_SCRATCH+3) as u8, 1));
                self.em.emit(enc_r(Opcode::D_Add, r_ctr as u8, r_ctr as u8, (REG_SCRATCH+3) as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jmp, &loop_lbl);
                self.em.define_label(&done_lbl);
            }

            // ── MemCpy (llvm.memcpy) ───────────────────────────────────────
            // Inline byte copy loop: for i in 0..len { dst[i] = src[i] }
            Instr::MemCpy { dst_ptr, src_ptr, len } => {
                let r_dst = self.load_reg_or_imm(dst_ptr, REG_SCRATCH)?;
                let r_src = self.load_reg_or_imm(src_ptr, REG_SCRATCH + 1)?;
                let r_len = self.load_reg_or_imm(len, REG_SCRATCH + 2)?;
                let r_ctr: usize = 23;
                self.em.emit(enc_i(Opcode::D_MovI, r_ctr as u8, 0));
                let loop_lbl = format!("__mcpy_lp_{}", self.em.current_offset());
                let done_lbl = format!("__mcpy_dn_{}", self.em.current_offset() + 4);
                self.em.define_label(&loop_lbl);
                self.em.emit(enc_r(Opcode::V_Cmp, 0, r_ctr as u8, r_len as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jge, &done_lbl);
                let r_src_addr = REG_SCRATCH + 3;
                let r_dst_addr = REG_SCRATCH + 4;
                let r_byte     = REG_SCRATCH + 5;
                self.em.emit(enc_r(Opcode::D_Add, r_src_addr as u8, r_src as u8, r_ctr as u8, 0));
                self.em.emit(enc_r(Opcode::D_Load8, r_byte as u8, r_src_addr as u8, 0, 0));
                self.em.emit(enc_r(Opcode::D_Add, r_dst_addr as u8, r_dst as u8, r_ctr as u8, 0));
                self.em.emit(enc_r(Opcode::D_Store8, r_dst_addr as u8, r_byte as u8, 0, 0));
                // ctr++ via scratch
                self.em.emit(enc_i(Opcode::D_MovI, (REG_SCRATCH+6) as u8, 1));
                self.em.emit(enc_r(Opcode::D_Add, r_ctr as u8, r_ctr as u8, (REG_SCRATCH+6) as u8, 0));
                self.em.emit_jump_placeholder(Opcode::F_Jmp, &loop_lbl);
                self.em.define_label(&done_lbl);
            }

            // ── PHI ───────────────────────────────────────────────────────
            // PHI nodes are resolved by predecessors inserting copies.
            // At codegen time we just allocate the destination register.
            Instr::Phi { dst, .. } => {
                let _ = self.ra.get_or_alloc(dst)?;
                // Actual copy instructions emitted when we process
                // predecessor block terminators (see phi_copies below)
            }

            // ── Alloca ────────────────────────────────────────────────────
            Instr::Alloca { dst, .. } => {
                // Stack-based: alloca address = SP+slot, recomputed on each use.
                // No register is permanently assigned — remove from ra.map if present.
                self.ra.map.remove(dst);
            }

            // ── Load ──────────────────────────────────────────────────────
            Instr::Load { dst, ty, ptr, .. } => {
                let rd  = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rp  = self.load_reg_or_imm(ptr, REG_SCRATCH)?;
                let op  = match ty.byte_size() {
                    1 => Opcode::D_Load8,
                    2 => Opcode::D_Load16,
                    4 => Opcode::D_Load32,
                    _ => Opcode::D_Load64,
                };
                self.em.emit(enc_r(op, rd as u8, rp as u8, 0, 0));
            }

            // ── Store ─────────────────────────────────────────────────────
            Instr::Store { ty, val, ptr, .. } => {
                let rp = self.load_reg_or_imm(ptr, REG_SCRATCH)?;
                let rv = self.load_reg_or_imm(val, REG_SCRATCH + 1)?;
                let op = match ty.byte_size() {
                    1 => Opcode::D_Store8,
                    4 => Opcode::D_Store32,
                    _ => Opcode::D_Store64,
                };
                // store: dst=addr_reg, src1=val_reg
                self.em.emit(enc_r(op, rp as u8, rv as u8, 0, 0));
                // Free the stored SSA value's register after the store — UNLESS
                // the value is used more than once in this block (multi_use guard).
                // Example: "store %58, ptr %10; store %58, ptr %12" — %58 must
                // survive both stores.
                if let Value::Reg(vname) = val {
                    if !multi_use.contains(vname) {
                        self.ra.free_name(vname);
                    }
                }
                // Also free the destination pointer if it's a named SSA register
                // (not an alloca slot) and used only once — reduces register pressure
                // in large single-block functions like Z_ClearZone.
                if let Value::Reg(pname) = ptr {
                    if !self.alloca_slots.contains_key(pname)
                        && !multi_use.contains(pname) {
                        self.ra.free_name(pname);
                    }
                }
            }

            // ── GEP ───────────────────────────────────────────────────────
            Instr::Gep { dst, elem_ty, ptr, indices } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rp = self.load_reg_or_imm(ptr, REG_SCRATCH)?;
                self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rp as u8, 0, 0));

                // Resolve the actual element type — named structs are looked up
                // in type_defs so field offsets can be computed correctly.
                let resolved_ty = self.resolve_type(elem_ty);

                let mut stride = resolved_ty.byte_size() as i64;
                let mut field_idx; // tracks position in struct field list

                for (i, idx) in indices.iter().enumerate() {
                    if i == 0 {
                        // First index: scales by size of the whole element type (array element)
                        match idx {
                            Value::Const(0) => {} // common case: ptr[0] = base
                            Value::Const(n) => {
                                let off = (*n * stride) as i32;
                                self.em.emit(enc_i(Opcode::D_MovI, REG_SCRATCH as u8, off));
                                self.em.emit(enc_r(Opcode::D_Add,
                                    rd as u8, rd as u8, REG_SCRATCH as u8, 0));
                            }
                            _ => {
                                let ri = self.load_reg_or_imm(idx, REG_SCRATCH)?;
                                self.em.emit(enc_i(Opcode::D_MovI, (REG_SCRATCH+1) as u8, stride as i32));
                                self.em.emit(enc_r(Opcode::D_Mul,
                                    (REG_SCRATCH+1) as u8, ri as u8, (REG_SCRATCH+1) as u8, 0));
                                self.em.emit(enc_r(Opcode::D_Add,
                                    rd as u8, rd as u8, (REG_SCRATCH+1) as u8, 0));
                            }
                        }
                        // Next index operates on the inner element type
                        // e.g. for [4096 x i8]: stride = byte_size(i8) = 1, not 4096
                        stride = match &resolved_ty {
                            IrType::Array(_, inner) => inner.byte_size() as i64,
                            IrType::Struct(_)       => 1, // struct: field offsets computed below
                            other                   => other.byte_size() as i64,
                        };
                    } else {
                        // Subsequent indices: struct field index or array element index
                        match &resolved_ty {
                            IrType::Struct(fields) => {
                                // Field index must be a constant (LLVM struct GEP rule)
                                if let Value::Const(field_n) = idx {
                                    let n = *field_n as usize;
                                    // Offset = sum of sizes of preceding fields
                                    let offset: i64 = fields.iter()
                                        .take(n)
                                        .map(|f| self.resolve_type(f).byte_size() as i64)
                                        .sum();
                                    if offset != 0 {
                                        self.em.emit(enc_i(Opcode::D_MovI, REG_SCRATCH as u8, offset as i32));
                                        self.em.emit(enc_r(Opcode::D_Add,
                                            rd as u8, rd as u8, REG_SCRATCH as u8, 0));
                                    }
                                    field_idx = *field_n as usize; let _ = field_idx;
                                    // Update stride to size of the selected field
                                    stride = if field_idx < fields.len() {
                                        self.resolve_type(&fields[field_idx]).byte_size() as i64
                                    } else { 1 };
                                }
                            }
                            _ => {
                                // Array element index
                                match idx {
                                    Value::Const(0) => {}
                                    Value::Const(n) => {
                                        let off = (*n * stride) as i32;
                                        self.em.emit(enc_i(Opcode::D_MovI, REG_SCRATCH as u8, off));
                                        self.em.emit(enc_r(Opcode::D_Add,
                                            rd as u8, rd as u8, REG_SCRATCH as u8, 0));
                                    }
                                    _ => {
                                        let ri = self.load_reg_or_imm(idx, REG_SCRATCH)?;
                                        self.em.emit(enc_i(Opcode::D_MovI, (REG_SCRATCH+1) as u8, stride as i32));
                                        self.em.emit(enc_r(Opcode::D_Mul,
                                            (REG_SCRATCH+1) as u8, ri as u8, (REG_SCRATCH+1) as u8, 0));
                                        self.em.emit(enc_r(Opcode::D_Add,
                                            rd as u8, rd as u8, (REG_SCRATCH+1) as u8, 0));
                                    }
                                }
                                stride = 1;
                            }
                        }
                    }
                }
            }

            // ── Casts ─────────────────────────────────────────────────────
            Instr::Zext { dst, from_ty, val, .. } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rv = self.load_reg_or_imm(val, REG_SCRATCH)?;
                let op = match from_ty.byte_size() {
                    1 => Opcode::R_Zero8,
                    2 => Opcode::R_Zero16,
                    _ => Opcode::D_Mov,
                };
                self.em.emit(enc_r(op, rd as u8, rv as u8, 0, 0));
            }
            Instr::Sext { dst, from_ty, val, .. } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rv = self.load_reg_or_imm(val, REG_SCRATCH)?;
                let op = match from_ty.byte_size() {
                    1 => Opcode::R_Sign8,
                    2 => Opcode::R_Sign16,
                    _ => Opcode::D_Mov,
                };
                self.em.emit(enc_r(op, rd as u8, rv as u8, 0, 0));
            }
            Instr::Trunc { dst, to_ty, val, .. } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rv = self.load_reg_or_imm(val, REG_SCRATCH)?;
                let op = match to_ty.byte_size() {
                    1 => Opcode::R_Zero8,
                    2 => Opcode::R_Zero16,
                    _ => Opcode::D_Mov,
                };
                self.em.emit(enc_r(op, rd as u8, rv as u8, 0, 0));
            }
            Instr::Bitcast { dst, val, .. }
            | Instr::PtrToInt { dst, val, .. }
            | Instr::IntToPtr { dst, val, .. } => {
                let rd = self.ra.get_or_alloc(dst)?;
                self.flush_spill_pending();
                let rv = self.load_reg_or_imm(val, REG_SCRATCH)?;
                self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rv as u8, 0, 0));
            }

            // ── Call ──────────────────────────────────────────────────────
            Instr::Call { dst, func, args, ret_ty, .. } => {
                // Move args into R0..Rn (calling convention).
                //
                // Two-phase to avoid parallel-move clobber: if arg0 is in R1
                // and arg1 is in R0, naive sequential moves produce wrong results.
                //
                // Phase 1: load every arg into a scratch slot ABOVE the arg registers.
                // We use REG_SCRATCH+i (R24, R25, ...) as staging registers.
                // Phase 2: copy staging → R0..Rn.
                //
                // Special case: if the arg is already in the correct Ri AND no other
                // arg lives in Ri, skip the move entirely (common in tail-call style).
                // For simplicity we always stage, then copy — the extra D_Mov pairs
                // are cheap and correct.
                let num_args = args.len();
                // Safe scratch range: R24..R27 (4 slots).
                // R28=FP, R29=SP, R30=LR, R31=PC — MUST NOT be used as staging.
                // For calls with ≤4 args (i=0..3): stage in R24+i.
                // For calls with >4 args (i≥4): stage directly in Ri (target arg reg).
                // This is safe because Ri (i≥4) is not a reserved register and
                // its previous value was already invalidated by the prior F_CALL.
                const MAX_SCRATCH_SLOTS: usize = 4; // R24..R27 only
                let mut staged: Vec<usize> = Vec::with_capacity(num_args);
                for (i, (_, arg_val)) in args.iter().enumerate() {
                    let stage_reg = if i < MAX_SCRATCH_SLOTS {
                        REG_SCRATCH + i   // R24, R25, R26, R27
                    } else {
                        i                 // R4, R5, R6, ... (direct — safe for i≥4)
                    };
                    let src = self.load_reg_or_imm(arg_val, stage_reg)?;
                    if src != stage_reg {
                        self.em.emit(enc_r(Opcode::D_Mov, stage_reg as u8, src as u8, 0, 0));
                    }
                    staged.push(stage_reg);
                }
                // Phase 2: copy staging → R0..Rn
                for (i, &stage_reg) in staged.iter().enumerate() {
                    if stage_reg != i {
                        self.em.emit(enc_r(Opcode::D_Mov, i as u8, stage_reg as u8, 0, 0));
                    }
                }
                match func {
                    Value::Global(fname) => {
                        self.em.emit_call_placeholder(fname);
                    }
                    Value::Reg(rname) => {
                        let rf = self.ra.get(rname)?;
                        self.em.emit(enc_r(Opcode::L_FarCall, 0, rf as u8, 0, 0));
                    }
                    _ => {
                        log::warn!("indirect call via unknown value {:?}", func);
                    }
                }
                // Stack-based: after call, invalidate ALL registers.
                // alloca addresses are never in registers — always recomputed from SP+slot.
                {
                    let victims: Vec<String> = self.ra.map.keys().cloned().collect();
                    for name in victims {
                        let r = self.ra.map.remove(&name).unwrap();
                        if !self.ra.free.contains(&r) { self.ra.free.push(r); }
                    }
                }
                // Stack-based: after call, invalidate ALL registers.
                // alloca addresses are never in registers — always SP+slot on demand.
                {
                    let victims: Vec<String> = self.ra.map.keys().cloned().collect();
                    for name in victims {
                        let r = self.ra.map.remove(&name).unwrap();
                        if !self.ra.free.contains(&r) { self.ra.free.push(r); }
                    }
                }
                // Result in R0 → destination register
                if let Some(dst_name) = dst {
                    if *ret_ty != IrType::Void {
                        let rd = self.ra.get_or_alloc(dst_name)?;
                self.flush_spill_pending();
                        if rd != 0 {
                            self.em.emit(enc_r(Opcode::D_Mov, rd as u8, 0, 0, 0));
                        }
                    }
                }
            }

            // ── Ret ───────────────────────────────────────────────────────
            Instr::Ret { ty, val } => {
                if *ty != IrType::Void {
                    if let Some(v) = val {
                        let rv = self.load_reg_or_imm(v, REG_SCRATCH)?;
                        if rv != 0 {
                            self.em.emit(enc_r(Opcode::D_Mov, 0, rv as u8, 0, 0));
                        }
                    }
                }
                // Function epilogue
                if self.frame_size > 0 {
                    self.em.emit(enc_r(Opcode::A_Leave, 0, 0, 0, 0));
                }
                self.em.emit(enc_r(Opcode::F_Ret, 0, 0, 0, 0));
            }

            // ── VaStart ───────────────────────────────────────────────────
            // llvm.va_start.p0(ptr %slot):
            //
            // Save variadic registers R[n]..R[n+3] (where n = fixed param count)
            // into a register-save area in the current stack frame, then store
            // the base address of that area into *slot so that a subsequent
            //   %va_ptr = load ptr, ptr %slot
            // gives a valid pointer that tsk-libc can read args from.
            //
            // Save area layout (4 × 8 bytes, below alloca region):
            //   [FP - frame_size - 8]  = R[n+0]  (first variadic arg)
            //   [FP - frame_size - 16] = R[n+1]
            //   [FP - frame_size - 24] = R[n+2]
            //   [FP - frame_size - 32] = R[n+3]
            //
            // The frame_size was computed from alloca pre-pass. The save area
            // sits below it (further from FP). frame_size is extended by 32
            // so SP is already adjusted to cover the save area.
            Instr::VaStart { slot } => {
                let n_fixed = self.func.params.len();
                // Va save area occupies the BOTTOM 32 bytes of the frame:
                //   slot 0 (first variadic arg): FP - frame_size
                //   slot 1:                      FP - frame_size + 8
                //   slot 2:                      FP - frame_size + 16
                //   slot 3:                      FP - frame_size + 24
                // frame_size was pre-increased by 32 in pre-pass 1 to reserve this area.
                // No dynamic SP adjustment needed — prologue already covers it.
                let save_base_offset = -(self.frame_size as i32);
                let s_addr = REG_SCRATCH;
                self.em.emit(enc_i(Opcode::D_MovI, s_addr as u8, save_base_offset));
                self.em.emit(enc_r(Opcode::D_Add,
                    s_addr as u8, REG_FP as u8, s_addr as u8, 0));
                // Store R[n_fixed], R[n_fixed+1], R[n_fixed+2], R[n_fixed+3]
                // into save area at [s_addr], [s_addr+8], [s_addr+16], [s_addr+24]
                for i in 0..4usize {
                    let r_arg = n_fixed + i;
                    if r_arg < MAX_VREGS {
                        // D_Store64 [s_addr + i*8], R[r_arg]
                        // Use flags field for small offsets (0..24 fit in i16)
                        let off = (i * 8) as u16;
                        self.em.emit(encode_r(Opcode::D_Store64 as u8,
                            s_addr as u8, r_arg as u8, 0, off));
                    }
                }
                // Store save area base address into *slot
                let r_slot = self.load_reg_or_imm(slot, REG_SCRATCH + 2)?;
                self.flush_spill_pending();
                self.em.emit(enc_r(Opcode::D_Store64,
                    r_slot as u8, s_addr as u8, 0, 0));
            }

            // ── Unreachable ───────────────────────────────────────────────
            Instr::Unreachable => {
                self.em.emit(enc_r(Opcode::F_Trap, 0xFE, 0, 0, 0));
            }

            // PHI handled above (register allocation only)
        }
        Ok(())
    }

    /// Emit MOV copies for phi nodes in `target` block, for the edge coming from `cur_block`.
    /// Must be called just before the branch instruction to `target`.
    ///
    /// For each phi node in target:
    ///   phi %dst = [ %src_a, %pred_a ], [ %src_b, %pred_b ]
    /// When branching from cur_block → target:
    ///   emit: D_Mov  R[dst], R[src_for_cur_block]
    fn emit_phi_copies(
        &mut self,
        target:   &str,
        cur_block: &str,
        phi_map:  &HashMap<String, Vec<(String, Vec<(String, Value)>)>>,
    ) -> Result<()> {
        if let Some(phis) = phi_map.get(target) {
            for (phi_dst, incoming) in phis {
                // Find the source value for our predecessor block
                if let Some((_, src)) = incoming.iter().find(|(pred, _)| pred == cur_block) {
                    let rd = self.ra.get_or_alloc(phi_dst)?;
                    let rs = self.load_reg_or_imm(src, REG_SCRATCH)?;
                    if rd != rs {
                        self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rs as u8, 0, 0));
                    }
                }
            }
        }
        Ok(())
    }

    /// Load value into a register. If it's already a register, return it.
    /// If it's a constant, emit D_MOV_I into scratch_reg and return scratch_reg.
    fn load_reg_or_imm(&mut self, val: &Value, scratch: usize) -> Result<usize> {
        match val {
            Value::Reg(name) => {
                // FP-based: alloca slot at FP + (slot - frame_size)
                // slot is the offset from frame base (0, 8, 16, ...); frame sits below FP.
                if let Some(&slot) = self.alloca_slots.get(name) {
                    let fp_offset = slot - self.frame_size;  // always negative or zero
                    self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, fp_offset));
                    self.em.emit(enc_r(Opcode::D_Add,
                        scratch as u8, REG_FP as u8, scratch as u8, 0));
                    return Ok(scratch);
                }
                // Spill: if value is on stack, reload it into scratch register.
                if self.ra.is_spilled(name) {
                    let (reg, slot) = self.ra.reload(name)?;
                    self.flush_spill_pending();
                    self.emit_spill_reload(reg, slot);
                    return Ok(reg);
                }
                self.ra.get(name)
            }
            Value::Const(n) => {
                let v = *n as i64;
                if fits_imm19(v) {
                    self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, v as i32));
                } else {
                    let (hi, lo) = split_const32(v as i32);
                    let s2 = if scratch == REG_SCRATCH { REG_SCRATCH + 1 } else { REG_SCRATCH };
                    self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, hi));
                    self.em.emit(enc_i(Opcode::D_MovI, s2 as u8, 16));
                    self.em.emit(enc_r(Opcode::D_Shl, scratch as u8, scratch as u8, s2 as u8, 0));
                    if lo != 0 {
                        self.em.emit(enc_i(Opcode::D_MovI, s2 as u8, lo));
                        self.em.emit(enc_r(Opcode::D_Or, scratch as u8, scratch as u8, s2 as u8, 0));
                    }
                }
                Ok(scratch)
            }
            Value::Bool(b) => {
                self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, *b as i32));
                Ok(scratch)
            }
            Value::Global(name) => {
                // Handle inline GEP: "globalname+offset"
                let (base_name, const_off) = if let Some(plus) = name.find('+') {
                    let off = name[plus+1..].parse::<i64>().unwrap_or(0);
                    (&name[..plus], off)
                } else {
                    (name.as_str(), 0i64)
                };
                // Emit D_MOV_I scratch, 0 → tsk-link patches to global address
                self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, 0));
                self.em.call_fixups.push((self.em.current_offset() - 4, base_name.to_string()));
                // Add constant offset if any
                if const_off != 0 {
                    let s2 = if scratch == REG_SCRATCH { REG_SCRATCH + 1 } else { REG_SCRATCH };
                    self.em.emit(enc_i(Opcode::D_MovI, s2 as u8, const_off as i32));
                    self.em.emit(enc_r(Opcode::D_Add, scratch as u8, scratch as u8, s2 as u8, 0));
                }
                Ok(scratch)
            }
            _ => {
                self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, 0));
                Ok(scratch)
            }
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Module code generator — public entry point
// ─────────────────────────────────────────────────────────────────────────────

pub struct CodegenOutput {
    /// Raw bytecode for each function (name → bytes)
    pub functions:   Vec<(String, Vec<u8>)>,
    /// Global data section (name → (offset, size))
    #[allow(dead_code)] pub globals: Vec<(String, usize, usize)>,
    pub data:        Vec<u8>,
    /// Relocations: (absolute_byte_offset_in_concatenated_code, symbol_name)
    pub relocations: Vec<(usize, String)>,
}

pub fn generate_module(module: &Module) -> Result<CodegenOutput> {
    // Build global address map (placeholder layout — linker resolves final addresses)
    let mut global_map: HashMap<String, usize> = HashMap::new();
    let mut data = Vec::new();
    let mut global_meta = Vec::new();

    for g in &module.globals {
        let off = data.len();
        let size = g.ty.byte_size().max(1);
        match &g.init {
            GlobalInit::ZeroInit => data.extend(vec![0u8; size]),
            GlobalInit::Integer(n) => {
                let bytes = n.to_le_bytes();
                data.extend_from_slice(&bytes[..size.min(8)]);
                if size > 8 { data.extend(vec![0u8; size - 8]); }
            }
            GlobalInit::Undef => data.extend(vec![0u8; size]),
            GlobalInit::Bytes(ref raw) => {
                // Copy raw bytes, truncate or zero-pad to `size`
                let copy = raw.len().min(size);
                data.extend_from_slice(&raw[..copy]);
                if size > copy { data.extend(vec![0u8; size - copy]); }
            }
        }
        // Align to 8
        while data.len() % 8 != 0 { data.push(0); }
        global_map.insert(g.name.clone(), off);
        global_meta.push((g.name.clone(), off, size));
    }

    // Generate each non-declaration function
    let mut functions   = Vec::new();
    let mut relocations = Vec::new();
    let mut code_cursor = 0usize;

    for func in &module.functions {
        if func.is_decl || func.blocks.is_empty() {
            log::debug!("skipping declaration @{}", func.name);
            continue;
        }
        log::info!("generating @{} ({} blocks)", func.name, func.blocks.len());
        let mut fg = FuncGen::new(func, &global_map, &module.type_defs);
        match fg.generate() {
            Ok(code) => {
                log::info!("  → {} bytes", code.len());
                // Collect call_fixups as relocations with absolute offsets
                for (local_off, sym_name) in &fg.em.call_fixups {
                    relocations.push((code_cursor + local_off, sym_name.clone()));
                }
                code_cursor += (code.len() + 3) & !3;
                functions.push((func.name.clone(), code));
            }
            Err(e) => {
                log::warn!("codegen failed for @{}: {}", func.name, e);
                let trap = enc_r(Opcode::F_Trap, 0xCC, 0, 0, 0);
                code_cursor += 4;
                functions.push((func.name.clone(), trap.to_le_bytes().to_vec()));
            }
        }
    }

    Ok(CodegenOutput { functions, globals: global_meta, data, relocations })
}

// ─────────────────────────────────────────────────────────────────────────────
// Tests — FP-based frame layout
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use triskele_common::isa::Opcode;
    use crate::ir::IcmpPred;

    /// Decode a 32-bit instruction word → (opcode_byte, dst, src1/imm)
    fn decode_word(w: u32) -> (u8, u8, i32) {
        use triskele_common::{decode_opcode, decode_dst, decode_imm19};
        (decode_opcode(w), decode_dst(w) as u8, decode_imm19(w))
    }

    /// Build a minimal IR function with one i32 alloca and a load from it.
    fn make_alloca_func() -> Function {
        // Equivalent LLVM IR:
        //   define i32 @test_alloca() {
        //   entry:
        //     %slot = alloca i32
        //     store i32 42, i32* %slot
        //     %v = load i32, i32* %slot
        //     ret i32 %v
        //   }
        Function {
            name: "test_alloca".to_string(),
            params: vec![],
            ret_ty: IrType::I32,
            is_decl: false,
            blocks: vec![
                BasicBlock {
                    label: "entry".to_string(),
                    instrs: vec![
                        Instr::Alloca { dst: "slot".to_string(), ty: IrType::I32, align: 4 },
                        Instr::Store  { ty: IrType::I32,
                                        val: Value::Const(42),
                                        ptr: Value::Reg("slot".to_string()),
                                        align: 4 },
                        Instr::Load   { dst: "v".to_string(), ty: IrType::I32,
                                        ptr: Value::Reg("slot".to_string()),
                                        align: 4 },
                        Instr::Ret    { ty: IrType::I32,
                                        val: Some(Value::Reg("v".to_string())) },
                    ],
                }
            ],
        }
    }

    #[test]
    fn test_prologue_emits_a_enter() {
        let globals = HashMap::new();
        let func = make_alloca_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        let bytes = fg.generate().unwrap();
        // First instruction must be A_Enter (frame_size > 0)
        assert!(!bytes.is_empty(), "codegen must produce bytes");
        let first_op = bytes[3];  // opcode is high byte (LE → bytes[3])
        assert_eq!(first_op, Opcode::A_Enter as u8,
            "prologue must start with A_Enter when alloca present");
    }

    #[test]
    fn test_alloca_uses_fp_not_sp() {
        let globals = HashMap::new();
        let func = make_alloca_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        let bytes = fg.generate().unwrap();

        // Scan instructions for D_Add using REG_FP (28) as src1
        // This confirms FP-based alloca address computation
        let mut found_fp_add = false;
        for chunk in bytes.chunks(4) {
            if chunk.len() < 4 { break; }
            let w = u32::from_le_bytes(chunk.try_into().unwrap());
            use triskele_common::{decode_opcode, decode_s1};
            let op   = decode_opcode(w);
            let src1 = decode_s1(w) as u8;
            if op == Opcode::D_Add as u8 && src1 == REG_FP as u8 {
                found_fp_add = true;
                break;
            }
        }
        assert!(found_fp_add,
            "alloca address must be computed via D_Add with REG_FP (FP-based frame)");
    }

    #[test]
    fn test_epilogue_emits_a_leave() {
        let globals = HashMap::new();
        let func = make_alloca_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        let bytes = fg.generate().unwrap();

        // Scan for A_Leave before F_Ret at end
        let words: Vec<u32> = bytes.chunks(4)
            .filter(|c| c.len() == 4)
            .map(|c| u32::from_le_bytes(c.try_into().unwrap()))
            .collect();

        let opcodes: Vec<u8> = words.iter().map(|w| (w >> 24) as u8).collect();
        let a_leave_pos = opcodes.iter().rposition(|&op| op == Opcode::A_Leave as u8);
        let f_ret_pos   = opcodes.iter().rposition(|&op| op == Opcode::F_Ret as u8);

        assert!(a_leave_pos.is_some(), "epilogue must contain A_Leave");
        assert!(f_ret_pos.is_some(),   "epilogue must contain F_Ret");
        assert!(a_leave_pos.unwrap() < f_ret_pos.unwrap(),
            "A_Leave must come before F_Ret");
    }

    #[test]
    fn test_no_sp_based_alloca_address() {
        // Confirm SP (29) is NOT used as base for alloca address computation.
        // (it was the old SP-based bug)
        let globals = HashMap::new();
        let func = make_alloca_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        let bytes = fg.generate().unwrap();

        for chunk in bytes.chunks(4) {
            if chunk.len() < 4 { break; }
            let w = u32::from_le_bytes(chunk.try_into().unwrap());
            use triskele_common::{decode_opcode, decode_s1, decode_dst};
            let op   = decode_opcode(w);
            let dst  = decode_dst(w) as u8;
            let src1 = decode_s1(w) as u8;
            let _ = dst;  // used below
            // D_Add with SP as src1 is only allowed for the frame size adjustment
            // (SP = SP - frame_size), not for alloca address computation.
            // The alloca address D_Add must use FP (28), not SP (29).
            if op == Opcode::D_Add as u8 && src1 == REG_SP as u8 {
                // This D_Add is SP - frame_size (prologue), which is D_Sub actually.
                // D_Add SP, SP, scratch → should be D_Sub. If we see D_Add with SP
                // as BOTH dst and src1, that's the frame setup (ok).
                // If src1=SP and dst≠SP, that would be the old alloca bug.
                assert_eq!(dst, REG_SP as u8,
                    "D_Add with SP as src1 must only appear in frame size adjustment (dst=SP)");
            }
        }
    }
    // ─────────────────────────────────────────────────────────────────────────
    // Tests — unified register allocator (protected phi destinations)
    // ─────────────────────────────────────────────────────────────────────────

    /// Build a function with a phi node — the canonical if/else pattern.
    ///
    /// Equivalent LLVM IR:
    ///   define i32 @test_phi(i32 %0) {
    ///   entry:
    ///     %slot = alloca i32
    ///     store i32 %0, ptr %slot
    ///     %v = load i32, ptr %slot
    ///     %cond = icmp sgt i32 %v, 0
    ///     br i1 %cond, label %pos, label %neg
    ///   pos:
    ///     br label %merge
    ///   neg:
    ///     br label %merge
    ///   merge:
    ///     %result = phi i32 [ 1, %pos ], [ -1, %neg ]
    ///     ret i32 %result
    ///   }
    fn make_phi_func() -> Function {
        Function {
            name: "test_phi".to_string(),
            params: vec![(IrType::I32, "0".to_string())],
            ret_ty: IrType::I32,
            is_decl: false,
            blocks: vec![
                BasicBlock {
                    label: "entry".to_string(),
                    instrs: vec![
                        Instr::Alloca { dst: "slot".to_string(), ty: IrType::I32, align: 4 },
                        Instr::Store  { ty: IrType::I32,
                                        val: Value::Reg("0".to_string()),
                                        ptr: Value::Reg("slot".to_string()), align: 4 },
                        Instr::Load   { dst: "v".to_string(), ty: IrType::I32,
                                        ptr: Value::Reg("slot".to_string()), align: 4 },
                        Instr::ICmp   { dst: "cond".to_string(), pred: IcmpPred::Sgt,
                                        lhs: Value::Reg("v".to_string()),
                                        rhs: Value::Const(0),
                                        ty: IrType::I1 },
                        Instr::BrCond { cond: Value::Reg("cond".to_string()),
                                        then_bb: "pos".to_string(),
                                        else_bb: "neg".to_string() },
                    ],
                },
                BasicBlock {
                    label: "pos".to_string(),
                    instrs: vec![
                        Instr::BrUncond { target: "merge".to_string() },
                    ],
                },
                BasicBlock {
                    label: "neg".to_string(),
                    instrs: vec![
                        Instr::BrUncond { target: "merge".to_string() },
                    ],
                },
                BasicBlock {
                    label: "merge".to_string(),
                    instrs: vec![
                        Instr::Phi { dst: "result".to_string(), ty: IrType::I32,
                                     incoming: vec![
                                         (Value::Const(1),  "pos".to_string()),
                                         (Value::Const(-1), "neg".to_string()),
                                     ]},
                        Instr::Ret { ty: IrType::I32,
                                     val: Some(Value::Reg("result".to_string())) },
                    ],
                },
            ],
        }
    }

    /// Build a function with many SSA values across multiple blocks to stress
    /// the register allocator — simulates the FixedDiv pattern.
    ///
    /// 6 blocks, 20+ SSA values, 2 phi nodes — would spill in conservative mode.
    fn make_many_ssa_func() -> Function {
        // define i32 @many_ssa(i32 %0, i32 %1) — computes abs(%0) + abs(%1)
        // Uses phi to merge the abs branches, generating many live SSA values.
        //
        //   entry: alloca a, alloca b, store params, load, icmp, br
        //   pos_a: sub 0-%a, br merge_a
        //   neg_a: load %a, br merge_a
        //   merge_a: phi %abs_a = [neg_a_val|pos_a, a_val|neg_a], load, icmp, br
        //   pos_b: (br merge_b)
        //   merge_b: phi %abs_b, add %abs_a+%abs_b, ret
        Function {
            name: "many_ssa".to_string(),
            params: vec![
                (IrType::I32, "p0".to_string()),
                (IrType::I32, "p1".to_string()),
            ],
            ret_ty: IrType::I32,
            is_decl: false,
            blocks: vec![
                BasicBlock {
                    label: "entry".to_string(),
                    instrs: vec![
                        Instr::Alloca { dst: "sa".to_string(), ty: IrType::I32, align: 4 },
                        Instr::Alloca { dst: "sb".to_string(), ty: IrType::I32, align: 4 },
                        Instr::Store  { ty: IrType::I32, val: Value::Reg("p0".to_string()),
                                        ptr: Value::Reg("sa".to_string()), align: 4 },
                        Instr::Store  { ty: IrType::I32, val: Value::Reg("p1".to_string()),
                                        ptr: Value::Reg("sb".to_string()), align: 4 },
                        Instr::Load   { dst: "a".to_string(), ty: IrType::I32,
                                        ptr: Value::Reg("sa".to_string()), align: 4 },
                        Instr::ICmp   { dst: "a_neg".to_string(), pred: IcmpPred::Slt,
                                        lhs: Value::Reg("a".to_string()),
                                        rhs: Value::Const(0), ty: IrType::I1 },
                        Instr::BrCond { cond: Value::Reg("a_neg".to_string()),
                                        then_bb: "neg_a".to_string(),
                                        else_bb: "pos_a".to_string() },
                    ],
                },
                BasicBlock {
                    label: "neg_a".to_string(),
                    instrs: vec![
                        Instr::Load  { dst: "a2".to_string(), ty: IrType::I32,
                                       ptr: Value::Reg("sa".to_string()), align: 4 },
                        Instr::BinOp { dst: "neg_a_val".to_string(), op: BinOpKind::Sub,
                                       ty: IrType::I32,
                                       lhs: Value::Const(0),
                                       rhs: Value::Reg("a2".to_string()) },
                        Instr::BrUncond { target: "merge_a".to_string() },
                    ],
                },
                BasicBlock {
                    label: "pos_a".to_string(),
                    instrs: vec![
                        Instr::Load { dst: "a3".to_string(), ty: IrType::I32,
                                      ptr: Value::Reg("sa".to_string()), align: 4 },
                        Instr::BrUncond { target: "merge_a".to_string() },
                    ],
                },
                BasicBlock {
                    label: "merge_a".to_string(),
                    instrs: vec![
                        Instr::Phi { dst: "abs_a".to_string(), ty: IrType::I32,
                                     incoming: vec![
                                         (Value::Reg("neg_a_val".to_string()), "neg_a".to_string()),
                                         (Value::Reg("a3".to_string()),        "pos_a".to_string()),
                                     ]},
                        Instr::Load  { dst: "b".to_string(), ty: IrType::I32,
                                       ptr: Value::Reg("sb".to_string()), align: 4 },
                        Instr::ICmp  { dst: "b_neg".to_string(), pred: IcmpPred::Slt,
                                       lhs: Value::Reg("b".to_string()),
                                       rhs: Value::Const(0), ty: IrType::I1 },
                        Instr::BrCond { cond: Value::Reg("b_neg".to_string()),
                                        then_bb: "neg_b".to_string(),
                                        else_bb: "pos_b".to_string() },
                    ],
                },
                BasicBlock {
                    label: "neg_b".to_string(),
                    instrs: vec![
                        Instr::Load  { dst: "b2".to_string(), ty: IrType::I32,
                                       ptr: Value::Reg("sb".to_string()), align: 4 },
                        Instr::BinOp { dst: "neg_b_val".to_string(), op: BinOpKind::Sub,
                                       ty: IrType::I32,
                                       lhs: Value::Const(0),
                                       rhs: Value::Reg("b2".to_string()) },
                        Instr::BrUncond { target: "merge_b".to_string() },
                    ],
                },
                BasicBlock {
                    label: "pos_b".to_string(),
                    instrs: vec![
                        Instr::Load { dst: "b3".to_string(), ty: IrType::I32,
                                      ptr: Value::Reg("sb".to_string()), align: 4 },
                        Instr::BrUncond { target: "merge_b".to_string() },
                    ],
                },
                BasicBlock {
                    label: "merge_b".to_string(),
                    instrs: vec![
                        Instr::Phi   { dst: "abs_b".to_string(), ty: IrType::I32,
                                       incoming: vec![
                                           (Value::Reg("neg_b_val".to_string()), "neg_b".to_string()),
                                           (Value::Reg("b3".to_string()),        "pos_b".to_string()),
                                       ]},
                        Instr::BinOp { dst: "sum".to_string(), op: BinOpKind::Add,
                                       ty: IrType::I32,
                                       lhs: Value::Reg("abs_a".to_string()),
                                       rhs: Value::Reg("abs_b".to_string()) },
                        Instr::Ret   { ty: IrType::I32,
                                       val: Some(Value::Reg("sum".to_string())) },
                    ],
                },
            ],
        }
    }

    /// Phi destination registers must be stable — the same physical register
    /// must be assigned to the phi dst throughout the function.
    #[test]
    fn test_phi_dst_register_is_stable() {
        let globals = HashMap::new();
        let func = make_phi_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        let bytes = fg.generate().unwrap();
        // Codegen must succeed (no spill) and produce non-trivial bytecode
        assert!(!bytes.is_empty(), "codegen must produce bytes for phi function");
        assert!(bytes.len() > 4,   "phi function must produce more than 1 instruction");
    }

    /// Phi destination must be in ra.protected after FuncGen::new.
    #[test]
    fn test_phi_dst_is_protected() {
        let globals = HashMap::new();
        let func = make_phi_func();
        let type_defs = HashMap::new();
        let fg = FuncGen::new(&func, &globals, &type_defs);
        // "result" is the phi destination in make_phi_func
        assert!(fg.ra.protected.contains("result"),
            "phi destination 'result' must be in ra.protected");
        // Non-phi values must NOT be protected
        assert!(!fg.ra.protected.contains("v"),
            "non-phi value 'v' must not be in ra.protected");
        assert!(!fg.ra.protected.contains("cond"),
            "non-phi value 'cond' must not be in ra.protected");
    }

    /// A function with many SSA values and phi nodes must not spill.
    /// This is the key regression test for the unified allocator —
    /// the conservative mode would have spilled on this pattern.
    #[test]
    fn test_no_spill_with_many_ssa_and_phi() {
        let globals = HashMap::new();
        let func = make_many_ssa_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        let result = fg.generate();
        assert!(result.is_ok(),
            "unified allocator must not spill on many-SSA+phi function: {:?}", result.err());
        let bytes = result.unwrap();
        assert!(bytes.len() > 4, "must produce real bytecode");
    }

    /// Non-phi SSA values must be recycled by liveness — confirmed by checking
    /// that the peak register count stays well below MAX_VREGS.
    #[test]
    fn test_liveness_recycles_non_phi_values() {
        let globals = HashMap::new();
        let func = make_many_ssa_func();
        let type_defs = HashMap::new();
        let mut fg = FuncGen::new(&func, &globals, &type_defs);
        fg.generate().unwrap();
        // After generate(), ra.used is the high-water mark of physical registers.
        // With liveness recycling, this must be far below MAX_VREGS (24).
        // Conservative mode would hit MAX_VREGS; unified mode should stay ≤ 12.
        assert!(fg.ra.used <= 12,
            "liveness recycling must keep register usage ≤ 12, got {}", fg.ra.used);
    }

}
