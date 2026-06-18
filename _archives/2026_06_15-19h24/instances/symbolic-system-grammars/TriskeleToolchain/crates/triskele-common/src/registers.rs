// triskele-common/src/registers.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Register file: 32 × 64-bit registers (R0–R31)
// Aliases: FP=R28, SP=R29, LR=R30, PC=R31

use crate::error::VmError;

// ─────────────────────────────────────────────────────────────────────────────
// Register aliases
// ─────────────────────────────────────────────────────────────────────────────
pub const REG_FP: usize = 28;  // Frame Pointer
pub const REG_SP: usize = 29;  // Stack Pointer
pub const REG_LR: usize = 30;  // Link Register
pub const REG_PC: usize = 31;  // Program Counter

pub const NUM_REGS: usize = 32;

// ─────────────────────────────────────────────────────────────────────────────
// Flags
// ─────────────────────────────────────────────────────────────────────────────

/// CPU flags — set by V_CMP, V_TEST, D_ADD, D_SUB, etc.
#[derive(Debug, Clone, Copy, Default)]
pub struct Flags {
    pub zero:     bool,  // result == 0
    pub negative: bool,  // result < 0 (signed)
    pub overflow: bool,  // signed overflow
    pub carry:    bool,  // unsigned carry/borrow
}

impl Flags {
    pub fn new() -> Self {
        Self::default()
    }

    /// Update flags from a 64-bit signed result.
    pub fn update_i64(&mut self, result: i64, overflow: bool, carry: bool) {
        self.zero     = result == 0;
        self.negative = result < 0;
        self.overflow = overflow;
        self.carry    = carry;
    }

    /// Update flags from a 64-bit unsigned result.
    pub fn update_u64(&mut self, result: u64, carry: bool) {
        self.zero     = result == 0;
        self.negative = (result as i64) < 0;
        self.overflow = false;
        self.carry    = carry;
    }

    /// Clear all flags.
    pub fn clear(&mut self) {
        *self = Self::default();
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// RegisterFile
// ─────────────────────────────────────────────────────────────────────────────

/// 32 × 64-bit general-purpose register file.
///
/// Calling convention:
///   R0–R7   : args / return values (caller-saved)
///   R8–R15  : temporaries (caller-saved)
///   R16–R23 : local variables (callee-saved)
///   R24–R27 : VM internal / reserved
///   R28 FP  : Frame Pointer (callee-saved)
///   R29 SP  : Stack Pointer (callee-saved)
///   R30 LR  : Link Register (caller-saved)
///   R31 PC  : Program Counter (special)
#[derive(Debug, Clone)]
pub struct RegisterFile {
    regs:  [u64; NUM_REGS],
    pub flags: Flags,
}

impl RegisterFile {
    /// Create a new register file.
    /// `stack_top` : initial SP value (Stack Pointer).
    /// `entry`     : initial PC value (entry point).
    pub fn new(stack_top: u64, entry: u64) -> Self {
        let mut regs = [0u64; NUM_REGS];
        regs[REG_SP] = stack_top;
        regs[REG_PC] = entry;
        Self { regs, flags: Flags::new() }
    }

    // ── General access ────────────────────────────────────────────────────────

    #[inline]
    pub fn get(&self, reg: usize) -> Result<u64, VmError> {
        if reg < NUM_REGS {
            Ok(self.regs[reg])
        } else {
            Err(VmError::InvalidRegister(reg))
        }
    }

    #[inline]
    pub fn set(&mut self, reg: usize, val: u64) -> Result<(), VmError> {
        if reg < NUM_REGS {
            self.regs[reg] = val;
            Ok(())
        } else {
            Err(VmError::InvalidRegister(reg))
        }
    }

    // ── Named alias access (infallible — indices are compile-time constants) ──

    #[inline] pub fn sp(&self) -> u64      { self.regs[REG_SP] }
    #[inline] pub fn fp(&self) -> u64      { self.regs[REG_FP] }
    #[inline] pub fn lr(&self) -> u64      { self.regs[REG_LR] }
    #[inline] pub fn pc(&self) -> u64      { self.regs[REG_PC] }

    #[inline] pub fn set_sp(&mut self, v: u64) { self.regs[REG_SP] = v; }
    #[inline] pub fn set_fp(&mut self, v: u64) { self.regs[REG_FP] = v; }
    #[inline] pub fn set_lr(&mut self, v: u64) { self.regs[REG_LR] = v; }
    #[inline] pub fn set_pc(&mut self, v: u64) { self.regs[REG_PC] = v; }

    /// Advance PC by 4 bytes (one instruction).
    #[inline]
    pub fn inc_pc(&mut self) {
        self.regs[REG_PC] = self.regs[REG_PC].wrapping_add(4);
    }

    /// Advance PC by a signed byte offset (Type J / branch).
    #[inline]
    pub fn offset_pc(&mut self, offset: i64) {
        self.regs[REG_PC] = self.regs[REG_PC].wrapping_add(offset as u64);
    }

    // ── Flags helpers ─────────────────────────────────────────────────────────

    /// Update flags after signed 64-bit addition.
    pub fn update_flags_add(&mut self, a: u64, b: u64, result: u64) {
        let (_, carry) = a.overflowing_add(b);
        let sa = a as i64;
        let sb = b as i64;
        let sr = result as i64;
        let overflow = (sa > 0 && sb > 0 && sr < 0) || (sa < 0 && sb < 0 && sr >= 0);
        self.flags.update_i64(sr, overflow, carry);
    }

    /// Update flags after signed 64-bit subtraction.
    pub fn update_flags_sub(&mut self, a: u64, b: u64, result: u64) {
        let (_, borrow) = a.overflowing_sub(b);
        let sa = a as i64;
        let sb = b as i64;
        let sr = result as i64;
        let overflow = (sa > 0 && sb < 0 && sr < 0) || (sa < 0 && sb > 0 && sr >= 0);
        self.flags.update_i64(sr, overflow, borrow);
    }

    /// Update flags from a comparison (a - b) without storing result.
    pub fn update_flags_cmp(&mut self, a: u64, b: u64) {
        let result = a.wrapping_sub(b);
        self.update_flags_sub(a, b, result);
    }

    // ── Debug ─────────────────────────────────────────────────────────────────

    /// Dump all registers (implements O_DUMP_REG).
    pub fn dump(&self) {
        let names = [
            "R0 ", "R1 ", "R2 ", "R3 ", "R4 ", "R5 ", "R6 ", "R7 ",
            "R8 ", "R9 ", "R10", "R11", "R12", "R13", "R14", "R15",
            "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23",
            "R24", "R25", "R26", "R27", "FP ", "SP ", "LR ", "PC ",
        ];
        for row in 0..8 {
            let mut line = String::new();
            for col in 0..4 {
                let i = row * 4 + col;
                line.push_str(&format!("  {}={:#018x}", names[i], self.regs[i]));
            }
            eprintln!("{}", line);
        }
        eprintln!(
            "  FLAGS: Z={} N={} O={} C={}",
            self.flags.zero as u8,
            self.flags.negative as u8,
            self.flags.overflow as u8,
            self.flags.carry as u8
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_register_file_init() {
        let rf = RegisterFile::new(0x7000_0000, 0x0000_1000);
        assert_eq!(rf.sp(), 0x7000_0000);
        assert_eq!(rf.pc(), 0x0000_1000);
        assert_eq!(rf.get(0).unwrap(), 0);
    }

    #[test]
    fn test_flags_add_overflow() {
        let mut rf = RegisterFile::new(0x7000_0000, 0);
        let a = i64::MAX as u64;
        let b = 1u64;
        let result = a.wrapping_add(b);
        rf.update_flags_add(a, b, result);
        assert!(rf.flags.overflow);
        assert!(rf.flags.negative);
    }

    #[test]
    fn test_inc_pc() {
        let mut rf = RegisterFile::new(0, 0x1000);
        rf.inc_pc();
        assert_eq!(rf.pc(), 0x1004);
    }
}
