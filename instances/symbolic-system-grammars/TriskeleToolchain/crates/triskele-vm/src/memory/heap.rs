// triskele-vm/src/memory/heap.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Heap — A_ Attractor (dynamic memory well).
// Simple free-list allocator. Phase 2 will add reference counting GC.

use super::Memory;
use triskele_common::error::VmError;

const ALIGN: u64 = 8;     // 8-byte alignment for all allocations
const HEADER: u64 = 8;    // block header size (stores allocation size)

pub struct Heap {
    base:      u64,
    size:      u64,
    cursor:    u64,        // bump pointer (simple Phase 1 allocator)
    free_list: Vec<(u64, u64)>,  // (address, size) of freed blocks
}

impl Heap {
    pub fn new(base: u64, size: u64) -> Self {
        Self {
            base,
            size,
            cursor: base,
            free_list: Vec::new(),
        }
    }

    /// A_ALLOC — allocate `n` bytes → VM address.
    pub fn alloc(&mut self, mem: &mut Memory, n: u64) -> Result<u64, VmError> {
        let aligned = align_up(n + HEADER, ALIGN);

        // Try free list first
        if let Some(idx) = self.free_list.iter().position(|(_, sz)| *sz >= aligned) {
            let (addr, _) = self.free_list.swap_remove(idx);
            mem.write_u64(addr, n)?;
            return Ok(addr + HEADER);
        }

        // Bump allocate
        let addr = self.cursor;
        if addr + aligned > self.base + self.size {
            return Err(VmError::OutOfMemory(n as usize));
        }
        mem.write_u64(addr, n)?;  // header: stores user size
        self.cursor += aligned;
        Ok(addr + HEADER)
    }

    /// A_ALLOC_Z — allocate `n` zeroed bytes → VM address.
    pub fn alloc_zeroed(&mut self, mem: &mut Memory, n: u64) -> Result<u64, VmError> {
        let ptr = self.alloc(mem, n)?;
        mem.memset(ptr, 0, n as usize)?;
        Ok(ptr)
    }

    /// A_FREE — free a block.
    pub fn free(&mut self, mem: &Memory, ptr: u64) -> Result<(), VmError> {
        if ptr < self.base + HEADER || ptr > self.base + self.size {
            return Err(VmError::MemoryFault { addr: ptr, size: 0 });
        }
        let header_addr = ptr - HEADER;
        let user_size = mem.read_u64(header_addr)?;
        let block_size = align_up(user_size + HEADER, ALIGN);
        self.free_list.push((header_addr, block_size));
        Ok(())
    }

    /// A_REALLOC — resize an existing block (naïve: alloc+copy+free).
    pub fn realloc(&mut self, mem: &mut Memory, ptr: u64, new_size: u64) -> Result<u64, VmError> {
        let old_size = mem.read_u64(ptr - HEADER)?;
        let new_ptr = self.alloc(mem, new_size)?;
        let copy_size = old_size.min(new_size) as usize;
        // Manual byte copy to avoid borrow conflict
        for i in 0..copy_size {
            let byte = mem.read_u8(ptr + i as u64)?;
            mem.write_u8(new_ptr + i as u64, byte)?;
        }
        self.free(mem, ptr)?;
        Ok(new_ptr)
    }

    /// Available heap space in bytes.
    pub fn available(&self) -> u64 {
        self.base + self.size - self.cursor
    }

    pub fn base(&self) -> u64 { self.base }
    pub fn size(&self) -> u64 { self.size }
}

#[inline]
fn align_up(n: u64, align: u64) -> u64 {
    (n + align - 1) & !(align - 1)
}

#[cfg(test)]
mod tests {
    use super::*;
    use super::super::{Memory, NULL_PAGE_END, HEAP_BASE, HEAP_SIZE};

    fn setup() -> (Memory, Heap) {
        let total_size = HEAP_BASE + HEAP_SIZE - NULL_PAGE_END;
        let mem = Memory::new(NULL_PAGE_END, total_size);
        let heap = Heap::new(HEAP_BASE, HEAP_SIZE);
        (mem, heap)
    }

    #[test]
    fn test_alloc_free() {
        let (mut mem, mut heap) = setup();
        let ptr = heap.alloc(&mut mem, 64).unwrap();
        assert!(ptr >= HEAP_BASE);
        heap.free(&mem, ptr).unwrap();
    }

    #[test]
    fn test_alloc_zeroed() {
        let (mut mem, mut heap) = setup();
        let ptr = heap.alloc_zeroed(&mut mem, 32).unwrap();
        for i in 0..32 {
            assert_eq!(mem.read_u8(ptr + i).unwrap(), 0);
        }
    }

    #[test]
    fn test_out_of_memory() {
        let (mut mem, mut heap) = setup();
        let result = heap.alloc(&mut mem, HEAP_SIZE + 1);
        assert!(result.is_err());
    }
}
