// triskele-vm/src/memory/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.1
//
// Multi-segment 64-bit address space.
// Memory map:
//   0x00000000  NULL page (unmapped — null ptr protection)
//   0x00001000  .code / .rodata / .data (loaded from .tvmx)
//   0x70000000  Stack top (grows downward, 1MB)
//   0x80000000  Heap base (grows upward, 4MB)
//   0xE0000000  tsk-libc stubs (injected by VM at startup)
//   0xF0000000  VM internal (FFI dispatch tables)
//
// Implementation: two independent segments — main (code/stack/heap) and
// aux (libc stubs + future VM-internal pages). The check() method routes
// accesses to the appropriate segment transparently.

pub mod stack;
pub mod heap;
pub mod arena;

use triskele_common::error::VmError;

pub const NULL_PAGE_END:  u64 = 0x0000_1000;
pub const STACK_TOP:      u64 = 0x7000_0000;
pub const STACK_SIZE:     u64 = 0x0010_0000;   // 1 MB
pub const HEAP_BASE:      u64 = 0x8000_0000;
pub const HEAP_SIZE:      u64 = 0x0040_0000;   // 4 MB
pub const VM_INTERNAL:    u64 = 0xF000_0000;

/// One contiguous memory segment.
struct Segment {
    base: u64,
    data: Vec<u8>,
}

impl Segment {
    fn new(base: u64, size: usize) -> Self {
        Self { base, data: vec![0u8; size] }
    }

    #[inline]
    fn covers(&self, addr: u64, n: usize) -> bool {
        addr >= self.base
            && addr.saturating_sub(self.base)
                .checked_add(n as u64)
                .map_or(false, |end| end <= self.data.len() as u64)
    }

    #[inline]
    fn offset(&self, addr: u64) -> usize {
        (addr - self.base) as usize
    }
}

/// Multi-segment VM memory.
/// Segments are kept in a small Vec; lookup is O(segments) — acceptable since
/// we have at most 2-3 segments in practice.
pub struct Memory {
    segments: Vec<Segment>,
}

impl Memory {
    /// Create a single-segment memory (backwards-compatible with v0.2.0).
    pub fn new(base: u64, size: u64) -> Self {
        Self { segments: vec![Segment::new(base, size as usize)] }
    }

    /// Add an auxiliary segment (e.g. tsk-libc region at 0xE000_0000).
    pub fn add_segment(&mut self, base: u64, size: u64) {
        self.segments.push(Segment::new(base, size as usize));
    }

    // ── Internal routing ─────────────────────────────────────────────────────

    #[inline]
    fn seg_check(&self, addr: u64, n: usize) -> Result<(&Segment, usize), VmError> {
        if addr < NULL_PAGE_END {
            return Err(VmError::MemoryFault { addr, size: n });
        }
        for seg in &self.segments {
            if seg.covers(addr, n) {
                return Ok((seg, seg.offset(addr)));
            }
        }
        Err(VmError::MemoryFault { addr, size: n })
    }

    #[inline]
    fn seg_check_mut(&mut self, addr: u64, n: usize) -> Result<(&mut Segment, usize), VmError> {
        if addr < NULL_PAGE_END {
            return Err(VmError::MemoryFault { addr, size: n });
        }
        for seg in &mut self.segments {
            if seg.covers(addr, n) {
                let off = seg.offset(addr);
                return Ok((seg, off));
            }
        }
        Err(VmError::MemoryFault { addr, size: n })
    }

    // ── Read ─────────────────────────────────────────────────────────────────

    pub fn read_u8(&self, addr: u64) -> Result<u8, VmError> {
        let (seg, off) = self.seg_check(addr, 1)?;
        Ok(seg.data[off])
    }

    pub fn read_u16(&self, addr: u64) -> Result<u16, VmError> {
        let (seg, off) = self.seg_check(addr, 2)?;
        Ok(u16::from_le_bytes(seg.data[off..off+2].try_into().unwrap()))
    }

    pub fn read_u32(&self, addr: u64) -> Result<u32, VmError> {
        let (seg, off) = self.seg_check(addr, 4)?;
        Ok(u32::from_le_bytes(seg.data[off..off+4].try_into().unwrap()))
    }

    pub fn read_u64(&self, addr: u64) -> Result<u64, VmError> {
        let (seg, off) = self.seg_check(addr, 8)?;
        Ok(u64::from_le_bytes(seg.data[off..off+8].try_into().unwrap()))
    }

    pub fn read_bytes(&self, addr: u64, n: usize) -> Result<&[u8], VmError> {
        let (seg, off) = self.seg_check(addr, n)?;
        Ok(&seg.data[off..off+n])
    }

    // ── Write ────────────────────────────────────────────────────────────────

    pub fn write_u8(&mut self, addr: u64, v: u8) -> Result<(), VmError> {
        let (seg, off) = self.seg_check_mut(addr, 1)?;
        seg.data[off] = v;
        Ok(())
    }

    pub fn write_u16(&mut self, addr: u64, v: u16) -> Result<(), VmError> {
        let (seg, off) = self.seg_check_mut(addr, 2)?;
        seg.data[off..off+2].copy_from_slice(&v.to_le_bytes());
        Ok(())
    }

    pub fn write_u32(&mut self, addr: u64, v: u32) -> Result<(), VmError> {
        let (seg, off) = self.seg_check_mut(addr, 4)?;
        seg.data[off..off+4].copy_from_slice(&v.to_le_bytes());
        Ok(())
    }

    pub fn write_u64(&mut self, addr: u64, v: u64) -> Result<(), VmError> {
        let (seg, off) = self.seg_check_mut(addr, 8)?;
        seg.data[off..off+8].copy_from_slice(&v.to_le_bytes());
        Ok(())
    }

    pub fn write_bytes(&mut self, addr: u64, bytes: &[u8]) -> Result<(), VmError> {
        let n = bytes.len();
        let (seg, off) = self.seg_check_mut(addr, n)?;
        seg.data[off..off+n].copy_from_slice(bytes);
        Ok(())
    }

    // ── Bulk (D_MEMCPY / D_MEMSET / libc) ───────────────────────────────────

    pub fn memset(&mut self, dst: u64, val: u8, n: usize) -> Result<(), VmError> {
        let (seg, off) = self.seg_check_mut(dst, n)?;
        seg.data[off..off+n].fill(val);
        Ok(())
    }

    /// Cross-segment-safe memcpy: reads src bytes first, then writes to dst.
    pub fn memcpy(&mut self, dst: u64, src: u64, n: usize) -> Result<(), VmError> {
        // Read source into temporary buffer (handles same-or-different segment)
        let tmp: Vec<u8> = {
            let (seg, off) = self.seg_check(src, n)?;
            seg.data[off..off+n].to_vec()
        };
        let (dseg, doff) = self.seg_check_mut(dst, n)?;
        dseg.data[doff..doff+n].copy_from_slice(&tmp);
        Ok(())
    }

    // ── Accessors ────────────────────────────────────────────────────────────

    /// Base address of the primary (first) segment.
    pub fn base(&self) -> u64 { self.segments[0].base }

    /// Size of the primary segment.
    pub fn size(&self) -> u64 { self.segments[0].data.len() as u64 }

    /// Top address of the primary segment.
    pub fn top(&self)  -> u64 { self.base() + self.size() }
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

    #[test]
    fn test_aux_segment() {
        let mut mem = Memory::new(NULL_PAGE_END, 0x1000);
        // Aux segment at 0xE000_0000 (libc region)
        mem.add_segment(0xE000_0000, 0x1000);
        mem.write_u32(0xE000_0000, 0xCAFE_BABE).unwrap();
        assert_eq!(mem.read_u32(0xE000_0000).unwrap(), 0xCAFE_BABE);
        // Primary segment is still accessible
        mem.write_u32(NULL_PAGE_END, 0x1234_5678).unwrap();
        assert_eq!(mem.read_u32(NULL_PAGE_END).unwrap(), 0x1234_5678);
    }
}
