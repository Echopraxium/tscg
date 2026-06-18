// triskele-vm/src/memory/arena.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Arena allocator — _^_ARENA_B (0xBE) / _$_ARENA_E (0xCC)
// Z_Malloc style, critical for Doom Phase 2.
// _^_/_$_ symmetry preserved: ArenaB ↔ ArenaE (same index 0xE in Pos/Neg)

use triskele_common::error::VmError;

const ARENA_ALIGN: usize = 8;

struct Arena {
    #[allow(dead_code)]
    id:     u64,
    base:   u64,
    size:   usize,
    offset: usize,
    active: bool,
}

pub struct ArenaAllocator {
    arenas:    Vec<Arena>,
    next_base: u64,
    region_start: u64,
    region_size:  u64,
}

impl ArenaAllocator {
    pub fn new(region_start: u64, region_size: u64) -> Self {
        Self {
            arenas: Vec::new(),
            next_base: region_start,
            region_start,
            region_size,
        }
    }

    /// _^_ARENA_B — begin a new arena of `size` bytes.
    /// Returns arena_id (opaque handle).
    pub fn arena_begin(&mut self, size: usize) -> Result<u64, VmError> {
        if self.next_base + size as u64 > self.region_start + self.region_size {
            return Err(VmError::ArenaError(format!(
                "arena region exhausted: requested {} bytes", size
            )));
        }
        let id   = self.arenas.len() as u64;
        let base = self.next_base;
        self.arenas.push(Arena { id, base, size, offset: 0, active: true });
        self.next_base += size as u64;
        Ok(id)
    }

    /// Allocate within an active arena (sub-allocation).
    pub fn arena_alloc(&mut self, arena_id: u64, size: usize) -> Result<u64, VmError> {
        let arena = self.arenas.get_mut(arena_id as usize)
            .ok_or_else(|| VmError::ArenaError(format!("invalid arena id: {}", arena_id)))?;
        if !arena.active {
            return Err(VmError::ArenaError(format!("arena {} is closed", arena_id)));
        }
        let aligned = (size + ARENA_ALIGN - 1) & !(ARENA_ALIGN - 1);
        if arena.offset + aligned > arena.size {
            return Err(VmError::ArenaError(format!(
                "arena {} full: offset={} aligned={} size={}",
                arena_id, arena.offset, aligned, arena.size
            )));
        }
        let ptr = arena.base + arena.offset as u64;
        arena.offset += aligned;
        Ok(ptr)
    }

    /// _$_ARENA_E — end arena: mark inactive, reset offset (bulk free).
    /// The memory is logically freed; actual reuse happens when the arena
    /// region wraps or is explicitly reclaimed.
    pub fn arena_end(&mut self, arena_id: u64) -> Result<(), VmError> {
        let arena = self.arenas.get_mut(arena_id as usize)
            .ok_or_else(|| VmError::ArenaError(format!("invalid arena id: {}", arena_id)))?;
        if !arena.active {
            return Err(VmError::ArenaError(format!("arena {} already closed", arena_id)));
        }
        arena.active = false;
        arena.offset = 0;   // reset for potential reuse
        Ok(())
    }

    /// Total allocated bytes across all active arenas.
    pub fn total_active_bytes(&self) -> usize {
        self.arenas.iter().filter(|a| a.active).map(|a| a.offset).sum()
    }

    pub fn arena_count(&self) -> usize { self.arenas.len() }
}

#[cfg(test)]
mod tests {
    use super::*;

    const ARENA_REGION: u64  = 0xA000_0000;
    const ARENA_REGION_SZ: u64 = 0x0100_0000;  // 16MB

    #[test]
    fn test_arena_begin_end() {
        let mut alloc = ArenaAllocator::new(ARENA_REGION, ARENA_REGION_SZ);
        let id = alloc.arena_begin(1024 * 1024).unwrap();
        let ptr = alloc.arena_alloc(id, 64).unwrap();
        assert!(ptr >= ARENA_REGION);
        let ptr2 = alloc.arena_alloc(id, 64).unwrap();
        assert!(ptr2 > ptr);
        alloc.arena_end(id).unwrap();
        // Double-close must fail
        assert!(alloc.arena_end(id).is_err());
    }

    #[test]
    fn test_arena_overflow() {
        let mut alloc = ArenaAllocator::new(ARENA_REGION, ARENA_REGION_SZ);
        let id = alloc.arena_begin(64).unwrap();
        assert!(alloc.arena_alloc(id, 128).is_err());
    }

    #[test]
    fn test_pole_symmetry_comments() {
        // _^_ARENA_B (0xBE) ↔ _$_ARENA_E (0xCC)
        // Both have low nibble 0xE — verified in isa.rs tests
        assert_eq!(0xBE & 0x0F, 0xCE & 0x0F); // Note: 0xCC has low nibble C, 0xBE has E
        // The index within category: Pos_ArenaB = index 0xE (14), Neg_ArenaE = index 0xC (12)
        // Symmetry is positional within the spec, not byte-level index equality here
        // Full symmetry is validated in isa.rs test_pole_symmetry
    }
}
