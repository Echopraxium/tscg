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
				Instr::Switch { cond, default_bb, cases } => {
					let rc = self.load_reg_or_imm(cond, REG_SCRATCH)?;
					// Emit V_CmpI + F_JZ for each case
					for (val, bb) in cases {
						self.em.emit(enc_i(Opcode::V_CmpI, rc as u8, *val as i32));
						self.em.emit_branch_placeholder("F_JZ", bb);
					}
					// Default: unconditional jump
					self.em.emit_branch_placeholder("F_JMP", default_bb);
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
        Instr::BinOp { dst, .. } | Instr::ICmp { dst, .. } | Instr::Phi { dst, .. }
        | Instr::Alloca { dst, .. } | Instr::Load { dst, .. }
        | Instr::Gep { dst, .. } | Instr::Zext { dst, .. } | Instr::Sext { dst, .. }
        | Instr::Trunc { dst, .. } | Instr::Bitcast { dst, .. }
        | Instr::PtrToInt { dst, .. } | Instr::IntToPtr { dst, .. } => Some(dst.clone()),
        Instr::Call { dst, .. } => dst.clone(),
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
    used:       usize,                    // high-water mark
    /// live_blocks[name] = set of block labels where name is live
    live:       HashMap<String, HashSet<String>>,
    /// current block label (updated per block)
    cur_block:  String,
    /// conservative mode: disable register reuse (enabled when function has alloca)
    has_alloca: bool,
    /// parameter SSA names — kept in ra.map until consumed
    #[allow(dead_code)]
    params:     HashSet<String>,
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
        Self { map, free, used, live, cur_block: "entry".to_string(), has_alloca: false, params }
    }

    fn set_block(&mut self, label: &str) {
        self.cur_block = label.to_string();
    }

    /// Allocate a physical register for SSA value `name`.
    ///
    /// Two modes:
    /// - Conservative (has_alloca=true): never recycle — safe for -O0 code
    ///   where alloca addresses must remain valid throughout the function.
    /// - Liveness-based (has_alloca=false): recycle dead registers — used for
    ///   -O1+ code where alloca has been optimized away into SSA registers.
    fn get_or_alloc(&mut self, name: &str) -> Result<usize> {
        if let Some(&r) = self.map.get(name) { return Ok(r); }

        if !self.has_alloca {
            // Liveness-based reuse: free registers dead in current block
            let dead: Vec<String> = self.map.keys()
                .filter(|k| k.as_str() != name)
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
        }
        // Conservative mode: never recycle — all registers stay allocated

        // Allocate from free pool
        if let Some(r) = self.free.pop() {
            self.map.insert(name.to_string(), r);
            self.used = self.used.max(r + 1);
            log::debug!("alloc R{} → %{} (block {})", r, name, self.cur_block);
            return Ok(r);
        }

        bail!("register spill in block {}: no free register for %{}                (live values: {}, mode={})",
            self.cur_block, name,
            self.map.keys().cloned().collect::<Vec<_>>().join(", "),
            if self.has_alloca { "conservative" } else { "liveness" });
    }

    fn get(&self, name: &str) -> Result<usize> {
        self.map.get(name).copied()
            .ok_or_else(|| anyhow!("undefined SSA value '%{}'", name))
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Instruction encoding (mirrors tsk-asm/src/encoder.rs)
// ─────────────────────────────────────────────────────────────────────────────

fn enc_r(op: Opcode, dst: u8, s1: u8, s2: u8, flags: u16) -> u32 {
    ((op as u32) << 24) | ((dst as u32) << 19) | ((s1 as u32) << 14)
        | ((s2 as u32) << 9) | (flags as u32 & 0x1FF)
}

fn enc_i(op: Opcode, dst: u8, imm: i32) -> u32 {
    ((op as u32) << 24) | ((dst as u32) << 19) | (imm as u32 & 0x0007_FFFF)
}

fn enc_j(op: Opcode, offset: i32) -> u32 {
    ((op as u32) << 24) | (offset as u32 & 0x00FF_FFFF)
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
            let patched = ((opcode_byte as u32) << 24) | ((delta as u32) & 0x00FF_FFFF);
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
    ra:      RegAlloc,
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
        let has_alloca = func.blocks.iter().any(|b|
            b.instrs.iter().any(|i| matches!(i, Instr::Alloca { .. }))
        );
        let mut ra = RegAlloc::new(&func.params, live);
        ra.has_alloca = false;
        let _ = has_alloca;
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
        // Named structs appear as LocalReg references in LLVM IR.
        // The parser stores them in type_defs keyed by "struct.foo".
        // When GEP has elem_ty = i64 (opaque fallback), we can't do better.
        // But when elem_ty was already resolved to IrType::Struct, we use it directly.
        match ty {
            IrType::Struct(_) => ty.clone(),
            IrType::Array(n, inner) => IrType::Array(*n, Box::new(self.resolve_type(inner))),
            IrType::Ptr => IrType::Ptr,
            other => other.clone(),
        }
    }

    fn generate(&mut self) -> Result<Vec<u8>> {
        // Pre-pass 1: collect alloca sizes for frame layout
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

        // Function prologue (FP-based frame layout)
        // A_Enter: push LR, push FP, FP = SP  →  FP points to saved-FP slot
        // SP -= frame_size                    →  locals live at FP-frame_size..FP-1
        // alloca slot N is accessed as: FP + (N - frame_size)  (negative offset)
        if self.frame_size > 0 {
            self.em.emit(enc_r(Opcode::A_Enter, 0, 0, 0, 0));
            self.em.emit(enc_i(Opcode::D_MovI, REG_SCRATCH as u8, self.frame_size));
            self.em.emit(enc_r(Opcode::D_Sub,
                REG_SP as u8, REG_SP as u8, REG_SCRATCH as u8, 0));
        }

        // Generate each basic block
        for block in &self.func.blocks {
            self.em.define_label(&block.label);
            self.gen_block(block, &phi_map)?;
        }

        self.em.apply_fixups()?;
        Ok(self.em.code.clone())
    }

    fn gen_block(&mut self, block: &BasicBlock,
                 phi_map: &HashMap<String, Vec<(String, Vec<(String, Value)>)>>)
                 -> Result<()> {
        self.ra.set_block(&block.label);
        for instr in &block.instrs {
            self.gen_instr(instr, &block.label, phi_map)?;
        }
        Ok(())
    }

    fn gen_instr(&mut self, instr: &Instr, cur_block: &str,
                 phi_map: &HashMap<String, Vec<(String, Vec<(String, Value)>)>>)
                 -> Result<()> {
        match instr {

            // ── BinOp ─────────────────────────────────────────────────────
            Instr::BinOp { dst, op, lhs, rhs, .. } => {
                let rd  = self.ra.get_or_alloc(dst)?;
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
                // Phi copies for then branch — emit before conditional jump
                // (copies are safe: cond register not overwritten by copies)
                self.emit_phi_copies(then_bb, cur_block, phi_map)?;
                self.em.emit_jump_placeholder(Opcode::F_Jnz, then_bb);
                // Phi copies for else branch
                self.emit_phi_copies(else_bb, cur_block, phi_map)?;
                self.em.emit_jump_placeholder(Opcode::F_Jmp, else_bb);
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
            }

            // ── GEP ───────────────────────────────────────────────────────
            Instr::Gep { dst, elem_ty, ptr, indices } => {
                let rd = self.ra.get_or_alloc(dst)?;
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
                let rv = self.load_reg_or_imm(val, REG_SCRATCH)?;
                self.em.emit(enc_r(Opcode::D_Mov, rd as u8, rv as u8, 0, 0));
            }

            // ── Call ──────────────────────────────────────────────────────
            Instr::Call { dst, func, args, ret_ty, .. } => {
                // Move args into R0..Rn (calling convention)
                for (i, (_, arg_val)) in args.iter().enumerate() {
                    let ra_reg = self.load_reg_or_imm(arg_val, REG_SCRATCH)?;
                    if ra_reg != i {
                        self.em.emit(enc_r(Opcode::D_Mov, i as u8, ra_reg as u8, 0, 0));
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
                self.ra.get(name)
            }
            Value::Const(n) => {
                let v = *n as i64;
                if v >= -262144 && v <= 262143 {
                    self.em.emit(enc_i(Opcode::D_MovI, scratch as u8, v as i32));
                } else {
                    let lo = (v as i32) & 0xFFFF;
                    let hi = ((v as i32) >> 16) & 0xFFFF;
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

    /// Decode a 32-bit instruction word → (opcode_byte, dst, src1/imm)
    fn decode_word(w: u32) -> (u8, u8, i32) {
        let op  = (w >> 24) as u8;
        let dst = ((w >> 19) & 0x1F) as u8;
        let imm = ((w & 0x0007_FFFF) as i32) << 13 >> 13;  // sign-extend 19→32
        (op, dst, imm)
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
        use crate::ir::*;
        Function {
            name: "test_alloca".to_string(),
            params: vec![],
            ret_ty: IrType::I32,
            blocks: vec![
                BasicBlock {
                    label: "entry".to_string(),
                    instrs: vec![
                        Instr::Alloca { dst: "slot".to_string(), ty: IrType::I32, num: 1 },
                        Instr::Store  { ty: IrType::I32,
                                        val: Value::Const(42),
                                        ptr: Value::Reg("slot".to_string()) },
                        Instr::Load   { dst: "v".to_string(), ty: IrType::I32,
                                        ptr: Value::Reg("slot".to_string()) },
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
        let mut fg = FuncGen::new(&func, &globals, &HashMap::new());
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
        let mut fg = FuncGen::new(&func, &globals, &HashMap::new());
        let bytes = fg.generate().unwrap();

        // Scan instructions for D_Add using REG_FP (28) as src1
        // This confirms FP-based alloca address computation
        let mut found_fp_add = false;
        for chunk in bytes.chunks(4) {
            if chunk.len() < 4 { break; }
            let w = u32::from_le_bytes(chunk.try_into().unwrap());
            let op = (w >> 24) as u8;
            let src1 = ((w >> 9) & 0x1F) as u8;
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
        let mut fg = FuncGen::new(&func, &globals, &HashMap::new());
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
        let mut fg = FuncGen::new(&func, &globals, &HashMap::new());
        let bytes = fg.generate().unwrap();

        for chunk in bytes.chunks(4) {
            if chunk.len() < 4 { break; }
            let w = u32::from_le_bytes(chunk.try_into().unwrap());
            let op   = (w >> 24) as u8;
            let src1 = ((w >> 9) & 0x1F) as u8;
            // D_Add with SP as src1 is only allowed for the frame size adjustment
            // (SP = SP - frame_size), not for alloca address computation.
            // The alloca address D_Add must use FP (28), not SP (29).
            if op == Opcode::D_Add as u8 && src1 == REG_SP as u8 {
                // This D_Add is SP - frame_size (prologue), which is D_Sub actually.
                // D_Add SP, SP, scratch → should be D_Sub. If we see D_Add with SP
                // as BOTH dst and src1, that's the frame setup (ok).
                // If src1=SP and dst≠SP, that would be the old alloca bug.
                let dst = ((w >> 19) & 0x1F) as u8;
                assert_eq!(dst, REG_SP as u8,
                    "D_Add with SP as src1 must only appear in frame size adjustment (dst=SP)");
            }
        }
    }
}
