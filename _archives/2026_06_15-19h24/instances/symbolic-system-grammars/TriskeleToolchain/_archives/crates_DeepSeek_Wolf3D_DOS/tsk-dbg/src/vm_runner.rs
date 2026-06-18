// tsk-dbg/src/vm_runner.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0 — threaded execution with pause/disconnect support
//
// Architecture:
//   - VmRunner holds VM state (registers, memory, breakpoints)
//   - run_until_stop() checks a pause channel every CHECK_INTERVAL instructions
//   - Called via tokio::task::spawn_blocking so the async DAP server stays responsive

use std::collections::HashSet;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::io::Cursor;
use triskele_common::tvm::{TvmFile, SectionType};

/// How many instructions to execute before checking the pause flag
const CHECK_INTERVAL: usize = 512;

/// Must match NULL_PAGE_END in triskele-vm/src/memory/mod.rs
/// Code and rodata are loaded starting at this address.
pub const LOAD_BASE: u64 = 0x0000_1000;

// ─────────────────────────────────────────────────────────────────────────────
// VM State
// ─────────────────────────────────────────────────────────────────────────────

/// 32 × 64-bit registers. Aliases: FP=R28, SP=R29, LR=R30, PC=R31.
pub struct RegisterFile {
    pub r: [u64; 32],
    /// CPU flags (set by V_Cmp): bit0=ZF, bit1=SF, bit2=OF, bit3=CF
    pub flags: u8,
}

impl RegisterFile {
    pub fn new(mem_size: usize) -> Self {
        let mut r = [0u64; 32];
        // SP at top of allocated memory (grows downward)
        r[29] = mem_size as u64 - 8;
        Self { r, flags: 0 }
    }

    pub fn pc(&self)  -> u64 { self.r[31] }
    pub fn sp(&self)  -> u64 { self.r[29] }
    pub fn set_pc(&mut self, v: u64) { self.r[31] = v; }

    pub fn flag_zero(&self)  -> bool { self.flags & 0x01 != 0 }
    pub fn flag_sign(&self)  -> bool { self.flags & 0x02 != 0 }
}

/// Full VM state accessible to the debugger.
pub struct VmState {
    pub regs:      RegisterFile,
    pub memory:    Vec<u8>,
    pub code_size: usize,
    /// Simple bump allocator pointer (for A_Alloc / A_AllocZ)
    pub heap_ptr:  u64,
}

impl VmState {
    pub fn new(bytecode: &[u8], mem_size: usize) -> Self {
        let mut memory = vec![0u8; mem_size];

        // Parse .tvmx format — same layout as triskele-vm loader
        let mut entry_pc = LOAD_BASE;
        let mut code_size = 0usize;

        match TvmFile::load_from_reader(&mut Cursor::new(bytecode)) {
            Ok(tvm) => {
                // Layout: rodata at LOAD_BASE, code immediately after (4-byte aligned)
                let mut load_ptr = LOAD_BASE as usize;

                if let Some(rodata) = tvm.find_section(SectionType::Rodata) {
                    if !rodata.data.is_empty() {
                        let end = (load_ptr + rodata.data.len()).min(mem_size);
                        memory[load_ptr..end].copy_from_slice(&rodata.data[..end - load_ptr]);
                        load_ptr += (rodata.data.len() + 3) & !3;  // align to 4
                    }
                }

                if let Some(code) = tvm.find_section(SectionType::Code) {
                    let end = (load_ptr + code.data.len()).min(mem_size);
                    memory[load_ptr..end].copy_from_slice(&code.data[..end - load_ptr]);
                    code_size = code.data.len();
                    entry_pc  = (load_ptr + tvm.entry_offset() as usize) as u64;
                    log::info!("Loaded: rodata at 0x{:04X}, code at 0x{:04X}, entry=0x{:04X}",
                        LOAD_BASE, load_ptr, entry_pc);
                }
            }
            Err(e) => {
                // Fallback: load raw bytes at LOAD_BASE (for bare bytecode)
                log::warn!("TvmFile parse failed ({}), loading raw bytes at 0x{:04X}", e, LOAD_BASE);
                let load_base = LOAD_BASE as usize;
                let len = bytecode.len().min(mem_size - load_base);
                memory[load_base..load_base + len].copy_from_slice(&bytecode[..len]);
                code_size = len;
                entry_pc  = LOAD_BASE;
            }
        }

        let mut regs = RegisterFile::new(mem_size);
        regs.set_pc(entry_pc);

        // Heap starts at 32MB offset (well above code+rodata+stack)
        let heap_ptr = 0x0200_0000u64;
        Self { regs, memory, code_size, heap_ptr }
    }

    pub fn fetch(&self) -> Option<u32> {
        let pc = self.regs.pc() as usize;
        if pc + 4 > self.memory.len() { return None; }
        Some(u32::from_le_bytes([
            self.memory[pc], self.memory[pc+1],
            self.memory[pc+2], self.memory[pc+3],
        ]))
    }

    pub fn read_u64(&self, addr: u64) -> Option<u64> {
        let a = addr as usize;
        if a + 8 > self.memory.len() { return None; }
        Some(u64::from_le_bytes(self.memory[a..a+8].try_into().ok()?))
    }

    pub fn write_u64(&mut self, addr: u64, v: u64) {
        let a = addr as usize;
        if a + 8 <= self.memory.len() {
            self.memory[a..a+8].copy_from_slice(&v.to_le_bytes());
        }
    }

    pub fn stack_push(&mut self, v: u64) {
        self.regs.r[29] -= 8;
        self.write_u64(self.regs.r[29], v);
    }

    pub fn stack_pop(&mut self) -> u64 {
        let v = self.read_u64(self.regs.r[29]).unwrap_or(0);
        self.regs.r[29] += 8;
        v
    }

    pub fn stack_peek_n(&self, n: usize) -> Vec<(u64, u64)> {
        let sp = self.regs.sp() as usize;
        let mut entries = Vec::new();
        for i in 0..n {
            let addr = sp + i * 8;
            if addr + 8 <= self.memory.len() {
                let v = u64::from_le_bytes(self.memory[addr..addr+8].try_into().unwrap());
                entries.push((addr as u64, v));
            }
        }
        entries
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Debug control
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq)]
pub enum RunMode {
    Continue,
    StepOne,
    Paused,
    Terminated,
}

#[derive(Debug, Clone, PartialEq)]
pub enum StopCause {
    Breakpoint(u64),
    Step(u64),
    Pause(u64),
    Entry,
    Halt,
    Exception(String),
}

/// Shared pause flag — set to true by the DAP server to interrupt the VM loop.
pub type PauseFlag = Arc<AtomicBool>;

pub fn new_pause_flag() -> PauseFlag {
    Arc::new(AtomicBool::new(false))
}

/// VmRunner holds the VM state and debug metadata.
pub struct VmRunner {
    pub state:       VmState,
    pub mode:        RunMode,
    pub breakpoints: HashSet<u64>,
    pub trace:       bool,
    /// Shared flag: set to true by async task to interrupt run_until_stop
    pub pause_flag:  PauseFlag,
}

impl VmRunner {
    pub fn new(bytecode: &[u8], mem_size: usize) -> Self {
        Self {
            state:       VmState::new(bytecode, mem_size),
            mode:        RunMode::Paused,
            breakpoints: HashSet::new(),
            trace:       false,
            pause_flag:  new_pause_flag(),
        }
    }

    pub fn pc(&self) -> u64 { self.state.regs.pc() }

    /// Create a dummy placeholder runner (used during spawn_blocking swap).
    /// Does not parse any bytecode — memory is zeroed, PC=0.
    pub fn new_empty(mem_size: usize) -> Self {
        let state = VmState {
            regs:      RegisterFile::new(mem_size),
            memory:    vec![0u8; mem_size],
            code_size: 0,
            heap_ptr:  0x0200_0000,
        };
        Self {
            state,
            mode:        RunMode::Terminated,
            breakpoints: HashSet::new(),
            trace:       false,
            pause_flag:  new_pause_flag(),
        }
    }

    pub fn set_breakpoints(&mut self, addrs: HashSet<u64>) {
        self.breakpoints = addrs;
    }

    /// Execute one instruction. Returns stop cause or None = keep running.
    pub fn step_once(&mut self) -> Result<Option<StopCause>, String> {
        let pc   = self.pc();
        let word = self.state.fetch()
            .ok_or_else(|| format!("PC out of bounds: 0x{:X}", pc))?;

        if self.trace {
            eprintln!("[TRACE] PC=0x{:04X}  0x{:08X}", pc, word);
        }

        self.state.regs.set_pc(pc + 4);
        self.execute(word, pc)
    }

    /// Run at most `max` instructions then pause (for --max-instructions option).
    /// Also respects StepOne mode — stops after 1 instruction regardless of max.
    pub fn run_until_stop_limited(&mut self, max: u64) -> StopCause {
        let mut count = 0u64;
        loop {
            let pc = self.pc();
            if self.breakpoints.contains(&pc) && self.mode == RunMode::Continue {
                self.mode = RunMode::Paused;
                return StopCause::Breakpoint(pc);
            }
            match self.step_once() {
                Ok(Some(cause)) => { self.mode = RunMode::Paused; return cause; }
                Ok(None) => {
                    // StepOne: stop after exactly 1 instruction
                    if self.mode == RunMode::StepOne {
                        self.mode = RunMode::Paused;
                        return StopCause::Step(self.pc());
                    }
                }
                Err(e) => { self.mode = RunMode::Paused; return StopCause::Exception(e); }
            }
            count += 1;
            if count >= max {
                self.mode = RunMode::Paused;
                log::debug!("max_instructions {} reached at PC=0x{:04X}", max, self.pc());
                return StopCause::Step(self.pc());
            }
        }
    }

    /// Run until stop condition.
    /// Checks pause_flag every CHECK_INTERVAL instructions — safe to call from
    /// a blocking thread while the async DAP server runs concurrently.
    pub fn run_until_stop(&mut self) -> StopCause {
        let mut tick = 0usize;

        loop {
            // ── Periodic pause check ────────────────────────────────────────
            tick += 1;
            if tick >= CHECK_INTERVAL {
                tick = 0;
                if self.pause_flag.load(Ordering::Relaxed) {
                    self.pause_flag.store(false, Ordering::Relaxed);
                    self.mode = RunMode::Paused;
                    return StopCause::Pause(self.pc());
                }
            }

            let pc = self.pc();

            // ── Periodic PC log (debug) ──────────────────────────────────────
            if tick == 1 {
                log::debug!("VM running at PC=0x{:04X}", pc);
            }

            // ── Breakpoint check before execution ───────────────────────────
            if self.breakpoints.contains(&pc) && self.mode == RunMode::Continue {
                self.mode = RunMode::Paused;
                return StopCause::Breakpoint(pc);
            }

            match self.step_once() {
                Ok(Some(cause)) => {
                    self.mode = RunMode::Paused;
                    return cause;
                }
                Ok(None) => {
                    if self.mode == RunMode::StepOne {
                        self.mode = RunMode::Paused;
                        return StopCause::Step(self.pc());
                    }
                }
                Err(e) => {
                    self.mode = RunMode::Paused;
                    return StopCause::Exception(e);
                }
            }
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Interpreter
    // ─────────────────────────────────────────────────────────────────────────

    fn execute(&mut self, word: u32, pc: u64) -> Result<Option<StopCause>, String> {
        let opcode = (word >> 24) as u8;
        let cat    = opcode >> 4;
        let idx    = opcode & 0xF;

        let dst  = ((word >> 19) & 0x1F) as usize;
        let src1 = ((word >> 14) & 0x1F) as usize;
        let src2 = ((word >>  9) & 0x1F) as usize;
        let imm9  = sign_extend9((word & 0x1FF) as u16);
        let imm14 = sign_extend14((word & 0x3FFF) as u16);
        let imm19 = sign_extend19(word & 0x0007_FFFF);   // D_MovI uses 19-bit immediate
        let off24 = sign_extend24(word & 0x00FF_FFFF);

        let r     = &mut self.state.regs.r;
        let flags = &mut self.state.regs.flags;
        let mem   = &mut self.state.memory;

        macro_rules! rd      { ($i:expr) => { r[$i] } }
        macro_rules! rd64    { ($i:expr) => { r[$i] as i64 } }
        macro_rules! rd_addr { ($i:expr) => { (r[$i] as usize).min(mem.len()) } }

        match (cat, idx) {
            // ── A_ Stack ─────────────────────────────────────────────────────
            (0x0, 0x0) => { // A_Push
                let v = rd!(src1);
                r[29] -= 8;
                let sp = r[29] as usize;
                if sp + 8 <= mem.len() { mem[sp..sp+8].copy_from_slice(&v.to_le_bytes()); }
            }
            (0x0, 0x1) => { // A_Pop
                let sp = r[29] as usize;
                let v  = if sp + 8 <= mem.len() {
                    u64::from_le_bytes(mem[sp..sp+8].try_into().unwrap())
                } else { 0 };
                rd!(dst) = v;
                r[29] += 8;
            }
            (0x0, 0x2) => { // A_PushI
                let v = imm19 as u64;
                r[29] -= 8;
                let sp = r[29] as usize;
                if sp + 8 <= mem.len() { mem[sp..sp+8].copy_from_slice(&v.to_le_bytes()); }
            }

            // ── A_ Stack (continued) ─────────────────────────────────────────
            (0x0, 0xA) => { // A_Alloc — bump allocate N bytes → ptr in dst
                let n   = (rd!(src1) as usize).min(mem.len() / 2);  // cap at half mem
                let ptr = self.state.heap_ptr;
                self.state.heap_ptr = self.state.heap_ptr
                    .saturating_add(((n as u64) + 7) & !7);
                rd!(dst) = ptr;
                log::debug!("A_Alloc {} bytes → 0x{:08X}", n, ptr);
            }
            (0x0, 0xB) => { // A_AllocZ — bump allocate N bytes zeroed → ptr
                let n   = (rd!(src1) as usize).min(mem.len() / 2);
                let ptr = self.state.heap_ptr;
                self.state.heap_ptr = self.state.heap_ptr
                    .saturating_add(((n as u64) + 7) & !7);
                let a = ptr as usize;
                let e = a.saturating_add(n).min(mem.len());
                if a < mem.len() { mem[a..e].fill(0); }
                rd!(dst) = ptr;
                log::debug!("A_AllocZ {} bytes → 0x{:08X}", n, ptr);
            }

            // ── St_ ───────────────────────────────────────────────────────────
            (0x1, 0x0) => { /* St_Nop */ }

            // ── F_ Flow ───────────────────────────────────────────────────────
            (0x2, 0x0) => { r[31] = (pc as i64 + 4 + off24) as u64; }   // F_Jmp
            (0x2, 0x1) => { r[31] = (pc as i64 + 4 + imm14) as u64; }   // F_JmpR
            (0x2, 0x2) => { // F_Call
                r[30] = r[31];
                r[31] = (pc as i64 + 4 + off24) as u64;
            }
            (0x2, 0x3) => { r[31] = r[30]; }  // F_Ret
            (0x2, 0x5) => { // F_Jz
                if *flags & 0x01 != 0 { r[31] = (pc as i64 + 4 + off24) as u64; }
            }
            (0x2, 0x6) => { // F_Jnz
                if *flags & 0x01 == 0 { r[31] = (pc as i64 + 4 + off24) as u64; }
            }
            (0x2, 0x7) => { // F_Jl
                let sf = *flags & 0x02 != 0;
                let of = *flags & 0x04 != 0;
                if sf != of { r[31] = (pc as i64 + 4 + off24) as u64; }
            }
            (0x2, 0x8) => { // F_Jle
                let zf = *flags & 0x01 != 0;
                let sf = *flags & 0x02 != 0;
                let of = *flags & 0x04 != 0;
                if zf || sf != of { r[31] = (pc as i64 + 4 + off24) as u64; }
            }
            (0x2, 0x9) => { // F_Jg
                let zf = *flags & 0x01 != 0;
                let sf = *flags & 0x02 != 0;
                let of = *flags & 0x04 != 0;
                if !zf && sf == of { r[31] = (pc as i64 + 4 + off24) as u64; }
            }
            (0x2, 0xA) => { // F_Jge
                let sf = *flags & 0x02 != 0;
                let of = *flags & 0x04 != 0;
                let target = (pc as i64 + 4 + off24) as u64;
                log::debug!("F_JGE PC=0x{:04X} off24={} target=0x{:04X} sf={} of={} jump={}",
                    pc, off24, target, sf, of, sf==of);
                if sf == of { r[31] = target; }
            }
            (0x2, 0xB) => { // F_Loop
                r[1] = r[1].wrapping_sub(1);
                if r[1] != 0 { r[31] = (pc as i64 + 4 + off24) as u64; }
            }
            (0x2, 0xE) => { return Ok(Some(StopCause::Halt)); }  // F_Halt

            // ── It_ + bitwise ─────────────────────────────────────────────────
            (0x3, 0x4) => { rd!(dst) = rd!(src1) & rd!(src2); }   // D_And
            (0x3, 0x5) => { rd!(dst) = rd!(src1) | rd!(src2); }   // D_Or
            (0x3, 0x6) => { rd!(dst) = rd!(src1) ^ rd!(src2); }   // D_Xor
            (0x3, 0x7) => { rd!(dst) = !rd!(src1); }               // D_Not
            (0x3, 0xE) => {                                         // D_Shl
                let sh = (word & 0x1F) as u32;
                rd!(dst) = rd!(src1) << sh;
            }
            (0x3, 0xF) => {                                         // D_Shr
                let sh = (word & 0x1F) as u32;
                rd!(dst) = ((rd!(src1) as i64) >> sh) as u64;
            }

            // ── D_ Dynamics ───────────────────────────────────────────────────
            (0x4, 0x0) => { rd!(dst) = rd!(src1); }                // D_Mov
            (0x4, 0x1) => { rd!(dst) = imm19 as u64; }             // D_MovI — 19-bit immediate
            (0x4, 0x2) => {                                         // D_MovI64
                let pc2 = r[31] as usize;
                if pc2 + 8 <= mem.len() {
                    let v = u64::from_le_bytes(mem[pc2..pc2+8].try_into().unwrap());
                    rd!(dst) = v;
                    r[31] += 8;
                }
            }
            (0x4, 0x3) => { let t = rd!(dst); rd!(dst) = rd!(src1); rd!(src1) = t; } // D_Xchg
            (0x4, 0x4) => { // D_Load8
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let v = mem.get(addr.min(mem.len() as u64 - 1) as usize).copied().unwrap_or(0);
                rd!(dst) = v as u64;
            }
            (0x4, 0x5) => { // D_Load16
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                rd!(dst) = if a + 2 <= mem.len() {
                    u16::from_le_bytes([mem[a], mem[a+1]]) as u64
                } else { 0 };
            }
            (0x4, 0x6) => { // D_Load32 — sign-extend
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                rd!(dst) = if a + 4 <= mem.len() {
                    i32::from_le_bytes([mem[a], mem[a+1], mem[a+2], mem[a+3]]) as i64 as u64
                } else { 0 };
            }
            (0x4, 0x7) => { // D_Load64
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                rd!(dst) = if a + 8 <= mem.len() {
                    u64::from_le_bytes(mem[a..a+8].try_into().unwrap())
                } else { 0 };
            }
            (0x4, 0x8) => { // D_Store8
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                if a < mem.len() { mem[a] = rd!(dst) as u8; }
            }
            (0x4, 0x9) => { // D_Store16
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                if a + 2 <= mem.len() { mem[a..a+2].copy_from_slice(&(rd!(dst) as u16).to_le_bytes()); }
            }
            (0x4, 0xA) => { // D_Store32
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                if a + 4 <= mem.len() { mem[a..a+4].copy_from_slice(&(rd!(dst) as u32).to_le_bytes()); }
            }
            (0x4, 0xB) => { // D_Store64
                let addr = (rd!(src1) as i64 + imm9) as u64;
                let a = addr as usize;
                if a + 8 <= mem.len() { mem[a..a+8].copy_from_slice(&rd!(dst).to_le_bytes()); }
            }
            (0x4, 0xC) => { // D_Memcpy
                let dst_a = rd_addr!(dst);
                let src_a = rd_addr!(src1);
                let n     = rd!(src2) as usize;
                if dst_a.saturating_add(n) <= mem.len() && src_a.saturating_add(n) <= mem.len() {
                    mem.copy_within(src_a..src_a+n, dst_a);
                }
            }
            (0x4, 0xD) => { // D_Memset
                let dst_a = rd_addr!(dst);
                let val   = rd!(src1) as u8;
                let n     = rd!(src2) as usize;
                if dst_a.saturating_add(n) <= mem.len() {
                    mem[dst_a..dst_a+n].fill(val);
                }
            }
            (0x4, 0xE) => { rd!(dst) = rd!(src1).wrapping_add(rd!(src2)); } // D_Add
            (0x4, 0xF) => { rd!(dst) = rd!(src1).wrapping_sub(rd!(src2)); } // D_Sub

            // ── R_ Representability ───────────────────────────────────────────
            (0x5, 0x0) => {
                let f = rd64!(src1) as f32;
                rd!(dst) = (f.to_bits() as u32) as u64;
            }
            (0x5, 0x1) => {
                let f = f32::from_bits(rd!(src1) as u32);
                rd!(dst) = f as i32 as i64 as u64;
            }
            (0x5, 0xC) => { // R_Fix2F
                let v = rd!(src1) as i32;
                let f = v as f32 / 65536.0;
                rd!(dst) = (f.to_bits() as u32) as u64;
            }
            (0x5, 0xD) => { // R_F2Fix
                let f = f32::from_bits(rd!(src1) as u32);
                rd!(dst) = (f * 65536.0) as i32 as i64 as u64;
            }
            (0x5, 0xE) => { // R_FixMul
                let a = rd!(src1) as i64;
                let b = rd!(src2) as i64;
                rd!(dst) = ((a * b) >> 16) as u64;
            }
            (0x5, 0xF) => { // R_FixDiv
                let a = rd!(src1) as i64;
                let b = rd!(src2) as i64;
                if b != 0 { rd!(dst) = ((a << 16) / b) as u64; }
                else { return Err(format!("R_FixDiv by zero at PC=0x{:X}", pc)); }
            }

            // ── V_ Verifiability ──────────────────────────────────────────────
            (0x7, 0x0) => { // V_Cmp
                let a = rd!(src1) as i64;
                let b = rd!(src2) as i64;
                let mut f: u8 = 0;
                if a == b { f |= 0x01; }
                if a  < b { f |= 0x02; }
                *flags = f;
            }
            (0x7, 0x1) => { // V_CmpI — Type I: register in dst field [23:19], imm14 in [13:0]
                let a = rd!(dst) as i64;  // register is in dst field (encode_i places it there)
                let b = imm14;
                let mut f: u8 = 0;
                if a == b { f |= 0x01; }
                if a  < b { f |= 0x02; }
                *flags = f;
                log::debug!("V_CmpI PC=0x{:04X} dst={} rd(dst)={} imm14={} a={} b={} flags=0x{:02X}",
                    pc, dst, rd!(dst), b, a, b, f);
            }
            (0x7, 0x9) => { // V_Assert
                if rd!(src1) == 0 {
                    return Err(format!("V_Assert failed at PC=0x{:X}", pc));
                }
            }

            // ── O_ Observability ──────────────────────────────────────────────
            (0x8, 0x0) => { // O_DumpReg
                for i in 0..32 {
                    eprint!("R{:<2}=0x{:016X}  ", i, r[i]);
                    if i % 4 == 3 { eprintln!(); }
                }
            }
            (0x8, 0x3) => { self.trace = true; }
            (0x8, 0x4) => { self.trace = false; }
            (0x8, 0x5) => { return Ok(Some(StopCause::Breakpoint(pc))); } // O_Break
            (0x8, 0x7) => { eprint!("{}", (rd!(src1) & 0xFF) as u8 as char); } // O_Log
            (0x8, 0x8) => { // O_LogS
                let mut addr = rd!(src1) as usize;
                while addr < mem.len() && mem[addr] != 0 {
                    eprint!("{}", mem[addr] as char);
                    addr += 1;
                }
            }

            // ── Im_ Interoperability ──────────────────────────────────────────
            (0x9, 0xF) => { return Ok(Some(StopCause::Halt)); }  // Im_Exit
            (0x9, 0x2) => { /* Im_FbBlit — headless no-op */ }
            (0x9, 0x3) => { /* Im_FbClear — headless no-op */ }
            (0x9, 0x4) => { rd!(dst) = 0; } // Im_InputRd → no input in headless

            // ── T_ Temporality ────────────────────────────────────────────────
            (0xA, 0x0) => { rd!(dst) = 0; }  // T_Tick
            (0xA, 0x6) => { /* T_FrameSyn — no-op headless */ }

            _ => {
                log::warn!("Unimplemented opcode 0x{:02X} at PC=0x{:X}", opcode, pc);
            }
        }

        Ok(None)
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Sign extension helpers
// ─────────────────────────────────────────────────────────────────────────────

fn sign_extend9(v: u16) -> i64 {
    if v & 0x100 != 0 { (v as i64) | !0x1FF } else { v as i64 }
}

fn sign_extend14(v: u16) -> i64 {
    if v & 0x2000 != 0 { (v as i64) | !0x3FFF } else { v as i64 }
}

fn sign_extend19(v: u32) -> i64 {
    if v & 0x4_0000 != 0 { (v as i64) | !0x7_FFFF } else { v as i64 }
}

fn sign_extend24(v: u32) -> i64 {
    if v & 0x800000 != 0 { (v as i64) | !0xFFFFFF } else { v as i64 }
}
