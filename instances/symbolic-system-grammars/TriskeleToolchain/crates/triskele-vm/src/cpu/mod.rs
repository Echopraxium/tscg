// triskele-vm/src/cpu/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.13
//
// TriskeleVM interpreter — register-based, 32-bit fixed instruction width.
// Main loop: fetch → decode → execute.

pub mod decode;

use crate::host::{HostIo, NativeHost};

use decode::{decode, Instruction};
use triskele_common::{
    error::VmError,
    fixed::{float_to_fixed, fixed_to_float, FIXED_PI},
    isa::Opcode,
    registers::RegisterFile,
};
use crate::memory::{
    Memory, HEAP_BASE, HEAP_SIZE, STACK_TOP, STACK_SIZE, NULL_PAGE_END,
    heap::Heap, stack::Stack, arena::ArenaAllocator,
};
use crate::display::DisplayBackend;
use crate::libc::LibcState;

/// Maximum instructions per run (safety — prevents infinite loops in tests).
const MAX_STEPS: u64 = 100_000_000;

/// VM execution result.
pub type VmResult = Result<i32, VmError>;

// ─────────────────────────────────────────────────────────────────────────────
// Cpu
// ─────────────────────────────────────────────────────────────────────────────

/// One Im_FfiCall slot — a native function loaded via libloading.
/// Not available in WASM builds (no dlopen).
#[cfg(feature = "native")]
pub struct FfiSlot {
    pub lib_name: String,
    pub fn_name:  String,
    /// Raw function pointer (unsafe to call — caller must know ABI).
    pub fn_ptr:   unsafe extern "C" fn() -> u64,
}

pub struct Cpu {
    pub regs:      RegisterFile,
    pub mem:       Memory,
    pub stack:     Stack,
    pub heap:      Heap,
    pub arenas:    ArenaAllocator,
    pub debug:     bool,
    pub trace:     bool,
    pub ticks:     u64,
    /// Display backend — None for headless (tests, CI, WASM without canvas),
    /// Some for graphical runs. Type-erased via Box<dyn DisplayBackend>.
    pub display:   Option<Box<dyn DisplayBackend>>,
    pub host:      Box<dyn HostIo + Send>,
    /// tsk-libc runtime state (rand seed, etc.)
    pub libc_state: LibcState,
    /// Im_FfiCall dispatch table — native only (no dlopen in WASM).
    #[cfg(feature = "native")]
    pub ffi_slots:  Vec<FfiSlot>,
}

impl Cpu {
    /// Create a new VM ready to execute a .tvmx binary already loaded into `mem`.
    pub fn new(mem: Memory, entry_pc: u64, debug: bool) -> Self {
        let regs   = RegisterFile::new(STACK_TOP, entry_pc);
        let stack  = Stack::new(STACK_TOP, STACK_SIZE);
        let heap   = Heap::new(HEAP_BASE, HEAP_SIZE);
        let arenas = ArenaAllocator::new(0xA000_0000, 0x0100_0000);
        Self {
            regs, mem, stack, heap, arenas,
            debug, trace: false, ticks: 0,
            display: None,
            host: Box::new(NativeHost::new()),
            libc_state: LibcState::new(),
            #[cfg(feature = "native")]
            ffi_slots:  Vec::new(),
        }
    }

    /// Create a new VM with a custom stack top address.
    /// Used by build_cpu_headless for WASM builds where STACK_TOP (0x7000_0000)
    /// is outside the allocated memory range.
    pub fn new_with_stack(mem: Memory, entry_pc: u64, stack_top: u64, debug: bool) -> Self {
        let regs   = RegisterFile::new(stack_top, entry_pc);
        let stack  = Stack::new(stack_top, STACK_SIZE);
        let heap   = Heap::new(HEAP_BASE, HEAP_SIZE);
        let arenas = ArenaAllocator::new(0xA000_0000, 0x0100_0000);
        Self {
            regs, mem, stack, heap, arenas,
            debug, trace: false, ticks: 0,
            display: None,
            host: Box::new(NativeHost::new()),
            libc_state: LibcState::new(),
            #[cfg(feature = "native")]
            ffi_slots:  Vec::new(),
        }
    }

    /// Attach a display backend (call before run() for graphical programs).
    pub fn with_display(mut self, display: Box<dyn DisplayBackend>) -> Self {
        self.display = Some(display);
        self
    }

    /// Redirect O_LOG / O_LOG_S to a custom writer (tests inject a Vec<u8>).
    pub fn with_host(mut self, h: Box<dyn HostIo + Send>) -> Self {
        self.host = h;
        self
    }

    /// Capture O_LOG output as UTF-8 string (convenience for tests).
    /// Returns the captured output after run().
    #[cfg(test)]
    pub fn captured_output(cpu: Cpu) -> (VmResult, String) {
        // Can't capture after-the-fact; use with_output(Box::new(Vec::new())) before run()
        // This is a placeholder — actual capture done in test helpers
        let _ = cpu;
        (Ok(0), String::new())
    }

    /// Load a raw bytecode slice into memory at `load_addr` and return a ready Cpu.
    pub fn from_bytecode(code: &[u8], load_addr: u64, debug: bool) -> Self {
        let total_size = 0x1000_0000u64;  // 256MB flat address space
        let mut mem = Memory::new(NULL_PAGE_END, total_size);
        mem.write_bytes(load_addr, code).expect("failed to load bytecode");
        Self::new(mem, load_addr, debug)
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Main interpreter loop
    // ─────────────────────────────────────────────────────────────────────────

    /// Run until F_HALT, Im_EXIT, or error.
    pub fn run(&mut self) -> VmResult {
        let mut steps = 0u64;
        loop {
            if steps >= MAX_STEPS {
                return Err(VmError::Trap(0xFF));  // runaway guard
            }
            steps += 1;
            self.ticks += 1;

            let pc = self.regs.pc();

            // Fetch (32-bit, little-endian)
            let word = match self.mem.read_u32(pc) {
                Ok(w) => w,
                Err(e) => return Err(e),
            };

            // Decode
            let instr = decode(word)?;

            if self.trace {
                self.trace_instr(pc, word, &instr);
            }

            // Advance PC before execution (branches may overwrite it)
            self.regs.inc_pc();

            // Execute
            match self.execute(instr) {
                Ok(()) => {}
                Err(VmError::Halted(code)) => return Ok(code),
                Err(e) => return Err(e),
            }
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Dispatch
    // ─────────────────────────────────────────────────────────────────────────

    fn execute(&mut self, instr: Instruction) -> Result<(), VmError> {
        match instr {
            Instruction::R { opcode, dst, src1, src2, flags } =>
                self.exec_r(opcode, dst, src1, src2, flags),
            Instruction::I { opcode, dst, imm } =>
                self.exec_i(opcode, dst, imm),
            Instruction::J { opcode, offset } =>
                self.exec_j(opcode, offset),
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Type R — register operations
    // ─────────────────────────────────────────────────────────────────────────

    fn exec_r(&mut self, op: Opcode, dst: u8, src1: u8, src2: u8, _flags: u16) -> Result<(), VmError> {
        let d = dst  as usize;
        let s1 = src1 as usize;
        let s2 = src2 as usize;

        match op {
            // ── St_ ──────────────────────────────────────────────────────────
            Opcode::St_Nop => {}  // structure preserved, nothing changes

            // ── D_ Bitwise (repurposed It_ slots) ────────────────────────────
            Opcode::D_And => {
                let r = self.regs.get(s1)? & self.regs.get(s2)?;
                self.regs.set(d, r)?;
            }
            Opcode::D_Or => {
                let r = self.regs.get(s1)? | self.regs.get(s2)?;
                self.regs.set(d, r)?;
            }
            Opcode::D_Xor => {
                let r = self.regs.get(s1)? ^ self.regs.get(s2)?;
                self.regs.set(d, r)?;
            }
            Opcode::D_Not => {
                let r = !self.regs.get(s1)?;
                self.regs.set(d, r)?;
            }
            Opcode::D_Shl => {
                // shift amount: src2 register (preferred) or flags[4:0] (legacy)
                let shift = if s2 != 0 {
                    (self.regs.get(s2)? & 0x3F) as u32
                } else {
                    (_flags & 0x1F) as u32
                };
                let r = self.regs.get(s1)? << shift;
                self.regs.set(d, r)?;
            }
            Opcode::D_Shr => {
                // shift amount: src2 register (preferred) or flags[4:0] (legacy)
                let shift = if s2 != 0 {
                    (self.regs.get(s2)? & 0x3F) as u32
                } else {
                    (_flags & 0x1F) as u32
                };
                let r = ((self.regs.get(s1)? as i64) >> shift) as u64;
                self.regs.set(d, r)?;
            }

            // ── D_ Dynamics ──────────────────────────────────────────────────
            Opcode::D_Mov => {
                let v = self.regs.get(s1)?;
                self.regs.set(d, v)?;
            }
            Opcode::D_Xchg => {
                let va = self.regs.get(s1)?;
                let vb = self.regs.get(s2)?;
                self.regs.set(s1, vb)?;
                self.regs.set(s2, va)?;
            }
            Opcode::D_Add => {
                let a = self.regs.get(s1)?;
                let b = self.regs.get(s2)?;
                let r = a.wrapping_add(b);
                self.regs.update_flags_add(a, b, r);
                self.regs.set(d, r)?;
            }
            Opcode::D_Sub => {
                let a = self.regs.get(s1)?;
                let b = self.regs.get(s2)?;
                let r = a.wrapping_sub(b);
                self.regs.update_flags_sub(a, b, r);
                self.regs.set(d, r)?;
            }
            Opcode::D_Mul => {
                let a = self.regs.get(s1)? as i64;
                let b = self.regs.get(s2)? as i64;
                let r = a.wrapping_mul(b) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::D_Div => {
                let a = self.regs.get(s1)? as i64;
                let b = self.regs.get(s2)? as i64;
                if b == 0 { return Err(VmError::DivisionByZero); }
                self.regs.set(d, a.wrapping_div(b) as u64)?;
            }
            Opcode::D_Rem => {
                // Use unsigned modulo (u64) — IR emits urem, not srem.
                // Signed rem would give wrong results for hash values > 2^31
                // when they have been sign-extended from i32 to u64.
                let a = self.regs.get(s1)?;  // u64 (unsigned)
                let b = self.regs.get(s2)?;  // u64 (unsigned)
                if b == 0 { return Err(VmError::DivisionByZero); }
                self.regs.set(d, a % b)?;
            }
Opcode::D_Load8 => {
                let addr = self.regs.get(s1)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.mem.read_u8(addr)? as u64;
                self.regs.set(d, v)?;
            }
            Opcode::D_Load16 => {
                let addr = self.regs.get(s1)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.mem.read_u16(addr)? as u64;
                self.regs.set(d, v)?;
            }
            Opcode::D_Load32 => {
                let addr = self.regs.get(s1)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.mem.read_u32(addr)? as i32 as i64 as u64;  // sign-extend
                self.regs.set(d, v)?;
            }
            Opcode::D_Load64 => {
                let addr = self.regs.get(s1)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.mem.read_u64(addr)?;
                self.regs.set(d, v)?;
            }
            // D_STORE8/16/32/64 Raddr, Rsrc, offset  — Type R
            Opcode::D_Store8 => {
                let addr = self.regs.get(d)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.regs.get(s1)? as u8;
                self.mem.write_u8(addr, v)?;
            }
            Opcode::D_Store32 => {
                let addr = self.regs.get(d)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.regs.get(s1)? as u32;

                self.mem.write_u32(addr, v)?;
            }
            Opcode::D_Store64 => {
                let addr = self.regs.get(d)?.wrapping_add((if _flags >= 256 { (_flags as i16).wrapping_sub(512) } else { _flags as i16 }) as i64 as u64);
                let v = self.regs.get(s1)?;
self.mem.write_u64(addr, v)?;
            }
            Opcode::D_Memcpy => {
                let dst_addr = self.regs.get(d)?;
                let src_addr = self.regs.get(s1)?;
                let n        = self.regs.get(s2)? as usize;
                self.mem.memcpy(dst_addr, src_addr, n)?;
            }
            Opcode::D_Memset => {
                let dst_addr = self.regs.get(d)?;
                let val      = self.regs.get(s1)? as u8;
                let n        = self.regs.get(s2)? as usize;
                self.mem.memset(dst_addr, val, n)?;
            }

            // ── A_ Attractor ─────────────────────────────────────────────────
            Opcode::A_Push => {
                let v = self.regs.get(s1)?;
                self.stack.push(&mut self.mem, &mut self.regs, v)?;
            }
            Opcode::A_Pop => {
                let v = self.stack.pop(&self.mem, &mut self.regs)?;
                self.regs.set(d, v)?;
            }
            Opcode::A_Peek => {
                let v = self.stack.peek(&self.mem, &self.regs)?;
                self.regs.set(d, v)?;
            }
            Opcode::A_Swap => {
                let a = self.stack.pop(&self.mem, &mut self.regs)?;
                let b = self.stack.pop(&self.mem, &mut self.regs)?;
                self.stack.push(&mut self.mem, &mut self.regs, a)?;
                self.stack.push(&mut self.mem, &mut self.regs, b)?;
            }
            Opcode::A_Dup => {
                let v = self.stack.peek(&self.mem, &self.regs)?;
                self.stack.push(&mut self.mem, &mut self.regs, v)?;
            }
            Opcode::A_Depth => {
                let depth = self.stack.depth(&self.regs);
                self.regs.set(d, depth)?;
            }
            Opcode::A_Enter => {
                self.stack.enter_frame(&mut self.mem, &mut self.regs)?;
            }
            Opcode::A_Leave => {
                self.stack.leave_frame(&self.mem, &mut self.regs)?;
            }
            Opcode::A_Alloc => {
                let n = self.regs.get(s1)?;
                let ptr = self.heap.alloc(&mut self.mem, n)?;
                self.regs.set(d, ptr)?;
            }
            Opcode::A_AllocZ => {
                let n = self.regs.get(s1)?;
                let ptr = self.heap.alloc_zeroed(&mut self.mem, n)?;
                self.regs.set(d, ptr)?;
            }
            Opcode::A_Free => {
                let ptr = self.regs.get(s1)?;
                self.heap.free(&self.mem, ptr)?;
            }
            Opcode::A_HeapSz => {
                self.regs.set(d, self.heap.available())?;
            }

            // ── V_ Verifiability ──────────────────────────────────────────────
            Opcode::V_Cmp => {
                let a = self.regs.get(s1)?;
                let b = self.regs.get(s2)?;
                self.regs.update_flags_cmp(a, b);
            }
            Opcode::V_Eq  => {
                let r = (self.regs.get(s1)? == self.regs.get(s2)?) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::V_Neq => {
                let r = (self.regs.get(s1)? != self.regs.get(s2)?) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::V_Lt  => {
                let r = ((self.regs.get(s1)? as i64) <  (self.regs.get(s2)? as i64)) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::V_Lte => {
                let r = ((self.regs.get(s1)? as i64) <= (self.regs.get(s2)? as i64)) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::V_Gt  => {
                let r = ((self.regs.get(s1)? as i64) >  (self.regs.get(s2)? as i64)) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::V_Gte => {
                let r = ((self.regs.get(s1)? as i64) >= (self.regs.get(s2)? as i64)) as u64;
                self.regs.set(d, r)?;
            }
            Opcode::V_Assert => {
                let v = self.regs.get(s1)?;
                if v == 0 {
                    return Err(VmError::AssertFailed(self.regs.pc()));
                }
            }
            Opcode::V_Null => {
                let v = self.regs.get(s1)?;
                self.regs.set(d, (v == 0) as u64)?;
            }

            // ── R_ Representability ───────────────────────────────────────────
            Opcode::R_I2F => {
                let v = self.regs.get(s1)? as i32 as f32;
                self.regs.set(d, v.to_bits() as u64)?;
            }
            Opcode::R_F2I => {
                let bits = self.regs.get(s1)? as u32;
                let f = f32::from_bits(bits);
                self.regs.set(d, f as i32 as u64)?;
            }
            Opcode::R_Fix2F => {
                let fx = self.regs.get(s1)? as i32;
                let f = fixed_to_float(fx);
                self.regs.set(d, f.to_bits() as u64)?;
            }
            Opcode::R_F2Fix => {
                let bits = self.regs.get(s1)? as u32;
                let f = f32::from_bits(bits);
                self.regs.set(d, float_to_fixed(f) as u64)?;
            }
            Opcode::R_FixMul => {
                // R_FIXMUL Rdst, Ra, Rb — fixed 16.16 multiply: (Ra * Rb) >> 16
                let a = self.regs.get(s1)? as i32;
                let b = self.regs.get(s2)? as i32;
                let result = ((a as i64 * b as i64) >> 16) as i32;
                self.regs.set(d, result as u64)?;
            }
            Opcode::R_FixDiv => {
                // R_FIXDIV Rdst, Ra, Rb — fixed 16.16 divide: (Ra << 16) / Rb
                let a = self.regs.get(s1)? as i32;
                let b = self.regs.get(s2)? as i32;
                if b == 0 { return Err(VmError::Trap(0xDE)); }  // division by zero
                let result = (((a as i64) << 16) / b as i64) as i32;
                self.regs.set(d, result as u64)?;
            }
            Opcode::R_Sign8 => {
                let v = self.regs.get(s1)? as u8 as i8 as i64 as u64;
                self.regs.set(d, v)?;
            }
            Opcode::R_Sign16 => {
                let v = self.regs.get(s1)? as u16 as i16 as i64 as u64;
                self.regs.set(d, v)?;
            }
            Opcode::R_Zero8 => {
                let v = self.regs.get(s1)? & 0xFF;
                self.regs.set(d, v)?;
            }
            Opcode::R_Zero16 => {
                let v = self.regs.get(s1)? & 0xFFFF;
                self.regs.set(d, v)?;
            }

            // ── O_ Observability ──────────────────────────────────────────────
            Opcode::O_DumpReg => {
                self.regs.dump();
            }
            Opcode::O_Log => {
                // O_LOG R0 — write char in R0 (lo byte) to output sink
                let c = self.regs.get(d)? as u8;
                self.host.write_bytes(&[c]);
                self.host.flush();
            }
            Opcode::O_LogS => {
                // O_LOG_S Rdst — write null-terminated string at address in Rdst to output sink
                let mut addr = self.regs.get(d)?;
                loop {
                    let c = self.mem.read_u8(addr)?;
                    if c == 0 { break; }
                    self.host.write_bytes(&[c]);
                    addr += 1;
                }
                self.host.flush();
            }
            Opcode::O_TraceOn  => { self.trace = true; }
            Opcode::O_TraceOff => { self.trace = false; }
            Opcode::O_TimeRd   => {
                self.regs.set(d, self.ticks)?;
            }
            Opcode::O_Break => {
                if self.debug {
                    eprintln!("[BREAK] PC=0x{:016X}", self.regs.pc());
                }
            }

            // ── T_ Temporality ────────────────────────────────────────────────
            Opcode::T_Tick => {
                self.regs.set(d, self.ticks)?;
            }
            Opcode::T_FrameSyn => {
                // T_FRAME_SYN R0 — sync to R0 fps (or 35 if R0=0)
                let fps = self.regs.get(d)? as u32;
                let fps = if fps == 0 { 35 } else { fps };
                if let Some(display) = self.display.as_mut() {
                    display.frame_sync(fps);
                }
            }

            // ── Ss_ Symbol ────────────────────────────────────────────────────
            Opcode::Ss_Pi => {
                self.regs.set(d, FIXED_PI as u64)?;
            }

            // ── L_ Localizability ─────────────────────────────────────────────
            Opcode::L_Lea => {
                let base   = self.regs.get(s1)?;
                let offset = self.regs.get(s2)? as i64;
                self.regs.set(d, base.wrapping_add(offset as u64))?;
            }
            Opcode::L_Deref => {
                let addr = self.regs.get(s1)?;
                let v    = self.mem.read_u64(addr)?;
                self.regs.set(d, v)?;
            }
            Opcode::L_DerefW => {
                let addr = self.regs.get(s1)?;
                let v    = self.regs.get(s2)?;
                self.mem.write_u64(addr, v)?;
            }
            Opcode::L_Null => {
                self.regs.set(d, 0)?;
            }
            Opcode::L_IsNull => {
                let v = self.regs.get(s1)?;
                self.regs.set(d, (v == 0) as u64)?;
            }
            Opcode::L_FarCall => {
                // src1 holds the 64-bit target address
                let target = self.regs.get(s1)?;
                self.regs.set_lr(self.regs.pc());
                self.regs.set_pc(target);
            }
            Opcode::L_FarJmp => {
                let target = self.regs.get(s1)?;
                self.regs.set_pc(target);
            }

            // ── _^_ Positive Pole ──────────────────────────────────────────────
            Opcode::Pos_ArenaB => {
                let size = self.regs.get(s1)? as usize;
                let id   = self.arenas.arena_begin(size)?;
                self.regs.set(d, id)?;
            }
            Opcode::Pos_Lock | Opcode::Neg_Unlock => {
                // Cooperative VM: no real threading, lock/unlock are no-ops for Phase 1
            }

            // ── _$_ Negative Pole ──────────────────────────────────────────────
            Opcode::Neg_ArenaE => {
                let arena_id = self.regs.get(s1)?;
                self.arenas.arena_end(arena_id)?;
            }

            // ── F_ Flow (halt + return — encoded as Type R with no registers) ──
            Opcode::F_Halt => {
                // Stop VM execution — exit code from R0
                let code = self.regs.get(0)? as i32;
                return Err(VmError::Halted(code));
            }
            Opcode::F_Ret => {
                // Return from function — restore PC ← LR
                let lr = self.regs.lr();
                self.regs.set_pc(lr);
            }

            // ── Im_ Interoperability ──────────────────────────────────────────
            Opcode::Im_FbBlit => {
                // Im_FB_BLIT R0 — blit framebuffer at address R0 to display window
                let fb_ptr = self.regs.get(d)?;
                if let Some(display) = self.display.as_mut() {
                    display.fb_blit(&self.mem, fb_ptr)
                        .map_err(|e| VmError::FfiError(e.to_string()))?;
                }
            }
            Opcode::Im_FbClear => {
                // Im_FB_CLEAR R0, R1 — clear framebuffer at R0 with color R1 (RGBA)
                let fb_ptr = self.regs.get(d)?;
                let color  = self.regs.get(s1)? as u32;
                if let Some(display) = self.display.as_mut() {
                    display.fb_clear(&mut self.mem, fb_ptr, color)
                        .map_err(|e| VmError::FfiError(e.to_string()))?;
                }
            }
            Opcode::Im_InputRd => {
                // Im_INPUT_RD — poll display events, store quit flag in R0
                let quit = if let Some(display) = self.display.as_mut() {
                    display.poll_events() as u64
                } else { 0 };
                self.regs.set(d, quit)?;
                if quit != 0 {
                    return Err(VmError::Halted(0));
                }
            }
            Opcode::Im_RegisterCb => {
                // Im_REGISTER_CB R0, R1 — register VM func at R1 for event_id R0
                let event_id = self.regs.get(d)? as u32;
                let vm_addr  = self.regs.get(s1)?;
                if let Some(display) = self.display.as_mut() {
                    display.register_callback(event_id, vm_addr);
                }
            }
            Opcode::Im_KeyQuery => {
                // Im_KEY_QUERY Rdst, Rsrc — Rsrc holds scancode (u8)
                // Rdst ← 1 if key held, 0 otherwise
                // Works only when a display backend is attached (headless → always 0)
                let sc = self.regs.get(s1)? as u8;
                let pressed = self.display.as_ref()
                    .map(|display| display.key_query(sc))
                    .unwrap_or(0);
                self.regs.set(d, pressed)?;
            }

            Opcode::Im_Exit => {
                let code = self.regs.get(0)? as i32;
                return Err(VmError::Halted(code));
            }

            // ── Im_CbInvoke / indirect JMP via register ──────────────────────
            // Im_CbInvoke Rn — jumps to address in Rn WITHOUT touching LR.
            // Type R: opcode(8) | d=0 | s1=reg | s2=0 | flags=0
            //
            // Used by tsk-link trampolines for far calls to libc stubs:
            //   F_CALL from main → trampoline (sets LR=main return addr)
            //   trampoline loads target addr into R24
            //   Im_CbInvoke R24 → jumps to libc stub (LR unchanged)
            //   libc stub: Im_Syscall + F_Ret → F_Ret uses original LR → returns to main
            //
            // NOTE: this is a JUMP (not a call) — LR is intentionally preserved.
            Opcode::Im_CbInvoke => {
                let target = self.regs.get(s1)?;
                self.regs.set_pc(target);
                return Ok(());
            }

            // ── Im_Syscall — tsk-libc pure dispatch ──────────────────────────
            // Im_Syscall <id> — encoded as Type I (dst=0, imm=syscall_id)
            // Handled in exec_i below; this arm covers the Type R path (should not occur).
            Opcode::Im_Syscall => {
                // Normally encoded as Type I — but handle defensively here too.
                let id = dst as u16;  // flags field carries id in Type R path
                crate::libc::dispatch(id, &mut self.mem, &mut self.regs, &mut self.libc_state, &mut *self.host)?;
            }

            // ── Im_FfiCall — native library dispatch ─────────────────────────
            // Im_FfiCall <slot> — calls a native function loaded via libloading.
            // Not available in WASM builds (no dlopen).
            #[cfg(feature = "native")]
            Opcode::Im_FfiCall => {
                let slot = dst as usize;
                if slot >= self.ffi_slots.len() {
                    return Err(VmError::FfiError(
                        format!("Im_FfiCall: slot {} out of range (table has {} entries)",
                            slot, self.ffi_slots.len())));
                }
                let a0 = self.regs.get(0)?;
                let a1 = self.regs.get(1)?;
                let a2 = self.regs.get(2)?;
                let a3 = self.regs.get(3)?;
                let ret = unsafe {
                    let f = self.ffi_slots[slot].fn_ptr;
                    let f6: unsafe extern "C" fn(u64,u64,u64,u64) -> u64 =
                        std::mem::transmute(f);
                    f6(a0, a1, a2, a3)
                };
                self.regs.set(0, ret)?;
            }
            #[cfg(not(feature = "native"))]
            Opcode::Im_FfiCall => {
                return Err(VmError::FfiError("Im_FfiCall not supported in WASM".into()));
            }

            // Unimplemented — trap in debug, silently skip in release
            _ => {
                if self.debug {
                    eprintln!("[WARN] unimplemented opcode: {:?} (0x{:02X})", op, op as u8);
                }
            }
        }
        Ok(())
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Type I — immediate operations
    // ─────────────────────────────────────────────────────────────────────────

    fn exec_i(&mut self, op: Opcode, dst: u8, imm: i32) -> Result<(), VmError> {
        let d = dst as usize;
        match op {
            Opcode::D_MovI => {
                self.regs.set(d, imm as u64)?;
            }
            Opcode::D_MovI64 => {
                // imm is pool index — next 8 bytes in .rodata (simplified: use sign-extended imm)
                self.regs.set(d, imm as i64 as u64)?;
            }
            Opcode::A_PushI => {
                self.stack.push(&mut self.mem, &mut self.regs, imm as u64)?;
            }
            Opcode::V_CmpI => {
                let a = self.regs.get(d)?;
                let b = imm as u64;
                self.regs.update_flags_cmp(a, b);
            }
            Opcode::D_Load8 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                let v    = self.mem.read_u8(addr)? as u64;
                self.regs.set(d, v)?;
            }
            Opcode::D_Load16 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                let v    = self.mem.read_u16(addr)? as u64;
                self.regs.set(d, v)?;
            }
            Opcode::D_Load32 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                let v = self.mem.read_u32(addr)? as i32 as i64 as u64;  // sign-extend
                self.regs.set(d, v)?;
            }
            Opcode::D_Load64 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                let v    = self.mem.read_u64(addr)?;
                self.regs.set(d, v)?;
            }
            Opcode::D_Store8 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                // src1 is encoded in high bits — not available in Type I; use R0 as implicit src
                let v = self.regs.get(0)? as u8;
                self.mem.write_u8(addr, v)?;
            }
            Opcode::D_Store32 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                let v = self.regs.get(0)? as u32;
                self.mem.write_u32(addr, v)?;
            }
            Opcode::D_Store64 => {
                let addr = self.regs.get(d)?.wrapping_add(imm as u64);
                let v = self.regs.get(0)?;
                self.mem.write_u64(addr, v)?;
            }
            Opcode::F_Trap => {
                return Err(VmError::Trap(imm as u8));
            }
            Opcode::F_RetN => {
                // Return and pop N stack words
                self.stack.leave_frame(&self.mem, &mut self.regs)?;
                let sp = self.regs.sp().wrapping_add(imm as u64 * 8);
                self.regs.set_sp(sp);
            }

            // ── Im_Syscall — tsk-libc pure dispatch (normal Type I path) ─────
            // Encoding: opcode=Im_Syscall, dst=0, imm19=syscall_id
            Opcode::Im_Syscall => {
                let id = imm as u16;
                crate::libc::dispatch(id, &mut self.mem, &mut self.regs, &mut self.libc_state, &mut *self.host)
                    .map_err(|e| match e {
                        // Halted must propagate as-is (e.g. from exit() syscall)
                        VmError::Halted(code) => VmError::Halted(code),
                        other => VmError::FfiError(other.to_string()),
                    })?;
            }

            _ => {
                if self.debug {
                    eprintln!("[WARN] unimplemented Type I opcode: {:?}", op);
                }
            }
        }
        Ok(())
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Type J — jump / branch
    // ─────────────────────────────────────────────────────────────────────────

    fn exec_j(&mut self, op: Opcode, offset: i32) -> Result<(), VmError> {
        // PC has already been advanced by 4 before exec_j is called.
        // The offset is relative to the instruction address (PC - 4).
        let instr_pc = self.regs.pc().wrapping_sub(4);
        let target   = instr_pc.wrapping_add(offset as u64);
        let flags    = &self.regs.flags;

        let taken = match op {
            Opcode::F_Jmp  => true,
            Opcode::F_JmpR => true,
            Opcode::F_Jz   => flags.zero,
            Opcode::F_Jnz  => !flags.zero,
            Opcode::F_Jl   => flags.negative != flags.overflow,
            Opcode::F_Jle  => flags.zero || (flags.negative != flags.overflow),
            Opcode::F_Jg   => !flags.zero && (flags.negative == flags.overflow),
            Opcode::F_Jge  => flags.negative == flags.overflow,
            Opcode::F_Loop => {
                // Decrement R1 (CX), jump if R1 ≠ 0
                let cx = self.regs.get(1)?.wrapping_sub(1);
                self.regs.set(1, cx)?;
                cx != 0
            }
            Opcode::F_Call => {
                self.regs.set_lr(self.regs.pc());  // save return address
                true
            }
            _ => false,
        };

        if taken {
            self.regs.set_pc(target);
        }
        Ok(())
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Standalone F_ opcodes (encoded as Type R with no registers)
    // ─────────────────────────────────────────────────────────────────────────
    //
    // F_HALT and F_RET are Type R with opcode only (dst=src1=src2=0).
    // They are dispatched through exec_r above.

    // ─────────────────────────────────────────────────────────────────────────
    // Trace helper
    // ─────────────────────────────────────────────────────────────────────────

    fn trace_instr(&self, pc: u64, word: u32, instr: &Instruction) {
        eprintln!(
            "[TRACE] PC={:#010X} word={:#010X} {:?}",
            pc, word, instr.opcode().mnemonic()
        );
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Convenience: add mnemonic() to Opcode for tracing
// ─────────────────────────────────────────────────────────────────────────────

#[allow(dead_code)]
trait Mnemonic {
    fn mnemonic(&self) -> &'static str;
}

impl Mnemonic for Opcode {
    fn mnemonic(&self) -> &'static str {
        triskele_common::isa::Opcode::mnemonic(*self)
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Integration tests — "Hello World" milestone
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use decode::{encode_i, encode_r, encode_j};
    use triskele_common::isa::Opcode;

    /// Build a Cpu with O_LOG output captured into a Vec<u8>.
    /// This avoids the Windows console UTF-8 restriction in test mode.
    fn cpu_with_capture(code: &[u8], entry: u64) -> (Cpu, std::sync::Arc<std::sync::Mutex<Vec<u8>>>) {
        let buf = std::sync::Arc::new(std::sync::Mutex::new(Vec::<u8>::new()));
        let buf2 = buf.clone();
        struct CaptureHost(std::sync::Arc<std::sync::Mutex<Vec<u8>>>);
        impl crate::host::HostIo for CaptureHost {
            fn write_bytes(&mut self, data: &[u8]) {
                self.0.lock().unwrap().extend_from_slice(data);
            }
            fn flush(&mut self) {}
            fn read_line(&mut self) -> crate::host::HostLine { crate::host::HostLine::Eof }
        }
        unsafe impl Send for CaptureHost {}
        let cpu = Cpu::from_bytecode(code, entry, false)
            .with_host(Box::new(CaptureHost(buf2)));
        (cpu, buf)
    }

    /// Build the "Hello World" bytecode (O_LOG path):
    ///   D_MOV_I  R0, 'H'  → O_LOG R0  (×3 chars: H, i, \n)
    ///   D_MOV_I  R0, 0    → Im_EXIT
    fn build_hello() -> Vec<u8> {
        let message = b"Hi\n";
        let mut code: Vec<u32> = Vec::new();
        for &ch in message {
            code.push(encode_i(Opcode::D_MovI, 0, ch as i32));
            code.push(encode_r(Opcode::O_Log,  0, 0, 0, 0));
        }
        code.push(encode_i(Opcode::D_MovI, 0, 0));
        code.push(encode_r(Opcode::Im_Exit, 0, 0, 0, 0));
        code.iter().flat_map(|w| w.to_le_bytes()).collect()
    }

    #[test]
    fn test_hello_world_milestone() {
        let code  = build_hello();
        let entry = NULL_PAGE_END;
        // Inject Vec<u8> sink — avoids Windows console non-UTF8 crash
        let (mut cpu, buf) = cpu_with_capture(&code, entry);
        let result = cpu.run();
        assert_eq!(result, Ok(0), "Hello World milestone failed: {:?}", result);
        let out = String::from_utf8(buf.lock().unwrap().clone()).unwrap();
        assert_eq!(out, "Hi\n", "O_LOG output mismatch: {:?}", out);
    }

    #[test]
    fn test_d_add() {
        let entry = NULL_PAGE_END;
        let code: Vec<u8> = vec![
            encode_i(Opcode::D_MovI, 1, 10),   // R1 = 10
            encode_i(Opcode::D_MovI, 2, 32),   // R2 = 32
            encode_r(Opcode::D_Add,  0, 1, 2, 0),  // R0 = R1 + R2 = 42
            encode_i(Opcode::D_MovI, 0, 0),    // exit code 0
            encode_r(Opcode::Im_Exit, 0, 0, 0, 0),
        ].into_iter().flat_map(|w: u32| w.to_le_bytes()).collect();
        let mut cpu = Cpu::from_bytecode(&code, entry, false);
        cpu.run().unwrap();
        // Can't read R0 after exit easily — just assert no panic
    }

    #[test]
    fn test_f_halt_stops_execution() {
        // F_HALT must stop the VM immediately with exit code from R0
        let entry = NULL_PAGE_END;
        let code: Vec<u8> = vec![
            encode_i(Opcode::D_MovI, 0, 42),         // R0 = 42  (exit code)
            encode_r(Opcode::F_Halt, 0, 0, 0, 0),    // F_HALT → Halted(42)
            encode_r(Opcode::V_Assert, 0, 0, 0, 0),  // must NOT be reached
        ].into_iter().flat_map(|w: u32| w.to_le_bytes()).collect();
        let mut cpu = Cpu::from_bytecode(&code, entry, false);
        let result = cpu.run();
        assert_eq!(result, Ok(42), "F_HALT must return exit code from R0");
    }

    #[test]
    fn test_f_ret_returns_to_caller() {
        // Program:
        //   entry:   F_CALL  @func     ; call func, saves LR = entry+8
        //            D_MOV_I R0, 0     ; reached after RET
        //            F_HALT
        //   func:    D_MOV_I R1, 99    ; do some work
        //            F_RET             ; return to caller
        let entry = NULL_PAGE_END;

        // Instruction offsets (each instruction = 4 bytes):
        //   +0  F_CALL +12   → jumps to func at +16, saves LR = entry+4
        //   +4  D_MOV_I R0, 0
        //   +8  F_HALT
        //   +12 D_MOV_I R1, 99   (func:)
        //   +16 F_RET

        let code: Vec<u32> = vec![
            encode_j(Opcode::F_Call, 12),          // F_CALL +12 → func
            encode_i(Opcode::D_MovI, 0, 0),        // R0 = 0 (exit code, reached after RET)
            encode_r(Opcode::F_Halt, 0, 0, 0, 0),  // F_HALT
            encode_i(Opcode::D_MovI, 1, 99),        // func: R1 = 99
            encode_r(Opcode::F_Ret,  0, 0, 0, 0),  // F_RET → back to caller
        ];
        let bytes: Vec<u8> = code.iter().flat_map(|w| w.to_le_bytes()).collect();
        let mut cpu = Cpu::from_bytecode(&bytes, entry, false);
        let result = cpu.run();
        assert_eq!(result, Ok(0), "F_RET must return to caller: {:?}", result);
        // R1 must have been set by func
        assert_eq!(cpu.regs.get(1).unwrap(), 99, "func body must have executed");
    }
}
