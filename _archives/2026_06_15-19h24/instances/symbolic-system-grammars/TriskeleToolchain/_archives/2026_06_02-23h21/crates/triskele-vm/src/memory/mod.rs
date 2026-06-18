// triskele-vm/src/memory/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Linear 64-bit address space. All VM memory operations go through here.
// Memory map:
//   0x00000000  NULL page (unmapped — null ptr protection)
//   0x00001000  .code section (entry point)
//   0x...       .rodata, .data, .bss (follows code)
//   0x70000000  Stack top (grows downward, 1MB default)
//   0x80000000  Heap base (grows upward, 4MB default)
//   0xF0000000  VM internal (FFI dispatch tables)

pub mod stack;
pub mod heap;
pub mod arena;

use triskele_common::error::VmError;

pub const NULL_PAGE_END:  u64 = 0x0000_1000;   // first valid address
pub const STACK_TOP:      u64 = 0x7000_0000;
pub const STACK_SIZE:     u64 = 0x0010_0000;   // 1MB
pub const HEAP_BASE:      u64 = 0x8000_0000;
pub const HEAP_SIZE:      u64 = 0x0040_0000;   // 4MB
pub const VM_INTERNAL:    u64 = 0xF000_0000;

/// Linear byte-addressed memory.
/// Backed by a single Vec<u8>; addresses are mapped by subtracting base offset.
pub struct Memory {
    data: Vec<u8>,
    base: u64,      // VM address of data[0]
    size: u64,
}

impl Memory {
    /// Create a zeroed memory region covering [base, base+size).
    pub fn new(base: u64, size: u64) -> Self {
        Self {
            data: vec![0u8; size as usize],
            base,
            size,
        }
    }

    // ── Bounds check ────────────────────────────────────────────────────────

    #[inline]
    fn check(&self, addr: u64, n: usize) -> Result<usize, VmError> {
        if addr < self.base || addr < NULL_PAGE_END {
            return Err(VmError::MemoryFault { addr, size: n });
        }
        let offset = (addr - self.base) as usize;
        if offset.checked_add(n).map_or(true, |end| end > self.data.len()) {
            return Err(VmError::MemoryFault { addr, size: n });
        }
        Ok(offset)
    }

    // ── Read ────────────────────────────────────────────────────────────────

    pub fn read_u8(&self, addr: u64) -> Result<u8, VmError> {
        let off = self.check(addr, 1)?;
        Ok(self.data[off])
    }

    pub fn read_u16(&self, addr: u64) -> Result<u16, VmError> {
        let off = self.check(addr, 2)?;
        Ok(u16::from_le_bytes(self.data[off..off+2].try_into().unwrap()))
    }

    pub fn read_u32(&self, addr: u64) -> Result<u32, VmError> {
        let off = self.check(addr, 4)?;
        Ok(u32::from_le_bytes(self.data[off..off+4].try_into().unwrap()))
    }

    pub fn read_u64(&self, addr: u64) -> Result<u64, VmError> {
        let off = self.check(addr, 8)?;
        Ok(u64::from_le_bytes(self.data[off..off+8].try_into().unwrap()))
    }

    pub fn read_bytes(&self, addr: u64, n: usize) -> Result<&[u8], VmError> {
        let off = self.check(addr, n)?;
        Ok(&self.data[off..off+n])
    }

    // ── Write ────────────────────────────────────────────────────────────────

    pub fn write_u8(&mut self, addr: u64, v: u8) -> Result<(), VmError> {
        let off = self.check(addr, 1)?;
        self.data[off] = v;
        Ok(())
    }

    pub fn write_u16(&mut self, addr: u64, v: u16) -> Result<(), VmError> {
        let off = self.check(addr, 2)?;
        self.data[off..off+2].copy_from_slice(&v.to_le_bytes());
        Ok(())
    }

    pub fn write_u32(&mut self, addr: u64, v: u32) -> Result<(), VmError> {
        let off = self.check(addr, 4)?;
        self.data[off..off+4].copy_from_slice(&v.to_le_bytes());
        Ok(())
    }

    pub fn write_u64(&mut self, addr: u64, v: u64) -> Result<(), VmError> {
        let off = self.check(addr, 8)?;
        self.data[off..off+8].copy_from_slice(&v.to_le_bytes());
        Ok(())
    }

    pub fn write_bytes(&mut self, addr: u64, bytes: &[u8]) -> Result<(), VmError> {
        let off = self.check(addr, bytes.len())?;
        self.data[off..off+bytes.len()].copy_from_slice(bytes);
        Ok(())
    }

    // ── Bulk operations (D_MEMCPY / D_MEMSET) ───────────────────────────────

    /// D_MEMCPY — copy n bytes from src to dst (within this memory).
    pub fn memcpy(&mut self, dst: u64, src: u64, n: usize) -> Result<(), VmError> {
        let src_off = self.check(src, n)?;
        let dst_off = self.check(dst, n)?;
        self.data.copy_within(src_off..src_off+n, dst_off);
        Ok(())
    }

    /// D_MEMSET — fill n bytes at dst with value.
    pub fn memset(&mut self, dst: u64, val: u8, n: usize) -> Result<(), VmError> {
        let off = self.check(dst, n)?;
        self.data[off..off+n].fill(val);
        Ok(())
    }

    // ── Section loading ──────────────────────────────────────────────────────

    /// Load a .tvm section into this memory region at `load_addr`.
    pub fn load_section(&mut self, load_addr: u64, data: &[u8]) -> Result<(), VmError> {
        self.write_bytes(load_addr, data)
    }

    // ── Accessors ────────────────────────────────────────────────────────────

    pub fn base(&self) -> u64  { self.base }
    pub fn size(&self) -> u64  { self.size }
    pub fn top(&self)  -> u64  { self.base + self.size }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_write_u32() {
        let mut mem = Memory::new(NULL_PAGE_END, 0x1000);
        mem.write_u32(NULL_PAGE_END, 0xDEAD_BEEF).unwrap();
        assert_eq!(mem.read_u32(NULL_PAGE_END).unwrap(), 0xDEAD_BEEF);
    }

    #[test]
    fn test_null_page_protection() {
        let mem = Memory::new(NULL_PAGE_END, 0x1000);
        assert!(mem.read_u8(0x0000_0000).is_err());
        assert!(mem.read_u8(0x0000_0FFF).is_err());
    }

    #[test]
    fn test_memset_memcpy() {
        let mut mem = Memory::new(NULL_PAGE_END, 0x1000);
        let base = NULL_PAGE_END;
        mem.memset(base, 0xAB, 8).unwrap();
        mem.memcpy(base + 8, base, 8).unwrap();
        for i in 0..16 {
            assert_eq!(mem.read_u8(base + i).unwrap(), 0xAB);
        }
    }
}
