// triskele-vm/src/memory/stack.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Stack — A_ Attractor (LIFO memory well).
// Grows downward from STACK_TOP.
// Frame layout:
//   [SP+0]   saved LR
//   [SP+8]   saved FP
//   [SP+16…] local variables

use super::Memory;
use triskele_common::error::VmError;
use triskele_common::registers::RegisterFile;

pub struct Stack {
    base: u64,   // lowest valid address (stack cannot go below this)
    top:  u64,   // initial SP value (highest address)
}

impl Stack {
    pub fn new(top: u64, size: u64) -> Self {
        Self { base: top - size, top }
    }

    /// A_PUSH — push a 64-bit value onto the stack.
    pub fn push(&self, mem: &mut Memory, regs: &mut RegisterFile, val: u64) -> Result<(), VmError> {
        let sp = regs.sp().wrapping_sub(8);
        if sp < self.base {
            return Err(VmError::StackOverflow(sp));
        }
        mem.write_u64(sp, val)?;
        regs.set_sp(sp);
        Ok(())
    }

    /// A_POP — pop a 64-bit value from the stack.
    pub fn pop(&self, mem: &Memory, regs: &mut RegisterFile) -> Result<u64, VmError> {
        let sp = regs.sp();
        if sp >= self.top {
            return Err(VmError::StackUnderflow);
        }
        let val = mem.read_u64(sp)?;
        regs.set_sp(sp.wrapping_add(8));
        Ok(val)
    }

    /// A_PEEK — read top without popping.
    pub fn peek(&self, mem: &Memory, regs: &RegisterFile) -> Result<u64, VmError> {
        let sp = regs.sp();
        if sp >= self.top {
            return Err(VmError::StackUnderflow);
        }
        mem.read_u64(sp)
    }

    /// A_ENTER — procedure prologue.
    /// Saves LR and FP, then sets FP = SP.
    pub fn enter_frame(&self, mem: &mut Memory, regs: &mut RegisterFile) -> Result<(), VmError> {
        let lr = regs.lr();
        let fp = regs.fp();
        self.push(mem, regs, lr)?;
        self.push(mem, regs, fp)?;
        regs.set_fp(regs.sp());
        Ok(())
    }

    /// A_LEAVE — procedure epilogue.
    /// Restores FP and LR from the frame.
    pub fn leave_frame(&self, mem: &Memory, regs: &mut RegisterFile) -> Result<(), VmError> {
        regs.set_sp(regs.fp());
        let fp = self.pop(mem, regs)?;
        let lr = self.pop(mem, regs)?;
        regs.set_fp(fp);
        regs.set_lr(lr);
        Ok(())
    }

    /// Stack depth in 64-bit words.
    pub fn depth(&self, regs: &RegisterFile) -> u64 {
        (self.top - regs.sp()) / 8
    }

    pub fn base(&self) -> u64 { self.base }
    pub fn top(&self)  -> u64 { self.top  }
}

#[cfg(test)]
mod tests {
    use super::*;
    use super::super::{Memory, NULL_PAGE_END, STACK_TOP, STACK_SIZE};
    use triskele_common::registers::RegisterFile;

    fn setup() -> (Memory, RegisterFile, Stack) {
        let total = STACK_TOP + STACK_SIZE;
        let mem = Memory::new(NULL_PAGE_END, total - NULL_PAGE_END);
        let regs = RegisterFile::new(STACK_TOP, NULL_PAGE_END);
        let stack = Stack::new(STACK_TOP, STACK_SIZE);
        (mem, regs, stack)
    }

    #[test]
    fn test_push_pop() {
        let (mut mem, mut regs, stack) = setup();
        stack.push(&mut mem, &mut regs, 0xDEAD_BEEF_CAFE_1234).unwrap();
        let v = stack.pop(&mem, &mut regs).unwrap();
        assert_eq!(v, 0xDEAD_BEEF_CAFE_1234);
    }

    #[test]
    fn test_enter_leave_frame() {
        let (mut mem, mut regs, stack) = setup();
        regs.set_lr(0x1234);
        regs.set_fp(0x5678);
        let sp_before = regs.sp();
        stack.enter_frame(&mut mem, &mut regs).unwrap();
        assert_ne!(regs.sp(), sp_before);
        stack.leave_frame(&mem, &mut regs).unwrap();
        assert_eq!(regs.sp(), sp_before);
        assert_eq!(regs.lr(), 0x1234);
        assert_eq!(regs.fp(), 0x5678);
    }
}
