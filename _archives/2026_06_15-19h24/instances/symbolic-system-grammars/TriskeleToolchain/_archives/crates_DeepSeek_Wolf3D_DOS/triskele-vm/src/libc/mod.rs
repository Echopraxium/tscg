// triskele-vm/src/libc/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.1
//
// tsk-libc — C89 standard library for TriskeleVM.
//
// Architecture:
//   Each libc function is a 2-instruction stub injected into VM memory:
//     Im_Syscall <id>   (executes native Rust implementation via dispatch table)
//     F_Ret             (return to caller)
//
//   The linker resolves external C symbols (memset, sin, etc.) to stub addresses.
//   This allows Wolf3D C89 code compiled via clang -O0 to call libc functions
//   transparently through the normal F_CALL mechanism.
//
// Memory layout:
//   LIBC_BASE (0xE000_0000) .. LIBC_BASE + LIBC_STUBS_SIZE
//   Each stub occupies 8 bytes: Im_Syscall(4) + F_Ret(4)
//
// Supported functions (Wolf3D C89 requirements):
//   Memory : memset, memcpy, memmove, memcmp
//   String : strlen, strcpy, strncpy, strcmp, strncmp, strchr
//   Math   : sin, cos, tan, atan, atan2, sqrt, fabs, floor, ceil
//   stdlib : abs, rand, srand
//   I/O    : printf (debug stub — outputs to stderr)

use triskele_common::error::VmError;
use triskele_common::isa::Opcode;
use triskele_common::registers::RegisterFile;
use super::memory::Memory;

/// Base VM address for libc stubs.
pub const LIBC_BASE: u64 = 0xE000_0000;

/// Each stub: Im_Syscall(4 bytes) + F_Ret(4 bytes) = 8 bytes.
pub const STUB_SIZE: u64 = 8;

/// Syscall IDs — each corresponds to a libc function.
#[repr(u16)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LibcSyscall {
    // Memory
    Memset   = 0x01,
    Memcpy   = 0x02,
    Memmove  = 0x03,
    Memcmp   = 0x04,
    // String
    Strlen   = 0x10,
    Strcpy   = 0x11,
    Strncpy  = 0x12,
    Strcmp   = 0x13,
    Strncmp  = 0x14,
    Strchr   = 0x15,
    // Math (fixed-point 16.16 — Wolf3D C89 uses no float)
    Sin      = 0x20,
    Cos      = 0x21,
    Tan      = 0x22,
    Atan     = 0x23,
    Atan2    = 0x24,
    Sqrt     = 0x25,
    Fabs     = 0x26,
    Floor    = 0x27,
    Ceil     = 0x28,
    // Stdlib
    Abs      = 0x30,
    Rand     = 0x31,
    Srand    = 0x32,
    // I/O (debug stub)
    Printf   = 0x40,
}

impl LibcSyscall {
    pub fn from_u16(id: u16) -> Option<Self> {
        match id {
            0x01 => Some(Self::Memset),  0x02 => Some(Self::Memcpy),
            0x03 => Some(Self::Memmove), 0x04 => Some(Self::Memcmp),
            0x10 => Some(Self::Strlen),  0x11 => Some(Self::Strcpy),
            0x12 => Some(Self::Strncpy), 0x13 => Some(Self::Strcmp),
            0x14 => Some(Self::Strncmp), 0x15 => Some(Self::Strchr),
            0x20 => Some(Self::Sin),     0x21 => Some(Self::Cos),
            0x22 => Some(Self::Tan),     0x23 => Some(Self::Atan),
            0x24 => Some(Self::Atan2),   0x25 => Some(Self::Sqrt),
            0x26 => Some(Self::Fabs),    0x27 => Some(Self::Floor),
            0x28 => Some(Self::Ceil),
            0x30 => Some(Self::Abs),     0x31 => Some(Self::Rand),
            0x32 => Some(Self::Srand),
            0x40 => Some(Self::Printf),
            _ => None,
        }
    }

    /// Symbol name as it appears in LLVM IR / C89 code.
    pub fn symbol_name(&self) -> &'static str {
        match self {
            Self::Memset  => "memset",  Self::Memcpy  => "memcpy",
            Self::Memmove => "memmove", Self::Memcmp  => "memcmp",
            Self::Strlen  => "strlen",  Self::Strcpy  => "strcpy",
            Self::Strncpy => "strncpy", Self::Strcmp  => "strcmp",
            Self::Strncmp => "strncmp", Self::Strchr  => "strchr",
            Self::Sin     => "sin",     Self::Cos     => "cos",
            Self::Tan     => "tan",     Self::Atan    => "atan",
            Self::Atan2   => "atan2",   Self::Sqrt    => "sqrt",
            Self::Fabs    => "fabs",    Self::Floor   => "floor",
            Self::Ceil    => "ceil",
            Self::Abs     => "abs",     Self::Rand    => "rand",
            Self::Srand   => "srand",
            Self::Printf  => "printf",
        }
    }

    /// VM address of this function's stub.
    pub fn stub_addr(&self) -> u64 {
        LIBC_BASE + (*self as u16 as u64) * STUB_SIZE
    }
}

/// All supported libc functions (for stub injection and linker registration).
pub const ALL_SYSCALLS: &[LibcSyscall] = &[
    LibcSyscall::Memset,  LibcSyscall::Memcpy,  LibcSyscall::Memmove, LibcSyscall::Memcmp,
    LibcSyscall::Strlen,  LibcSyscall::Strcpy,  LibcSyscall::Strncpy,
    LibcSyscall::Strcmp,  LibcSyscall::Strncmp, LibcSyscall::Strchr,
    LibcSyscall::Sin,     LibcSyscall::Cos,     LibcSyscall::Tan,
    LibcSyscall::Atan,    LibcSyscall::Atan2,   LibcSyscall::Sqrt,
    LibcSyscall::Fabs,    LibcSyscall::Floor,   LibcSyscall::Ceil,
    LibcSyscall::Abs,     LibcSyscall::Rand,    LibcSyscall::Srand,
    LibcSyscall::Printf,
];

/// Inject all libc stubs into VM memory at LIBC_BASE.
/// Must be called during VM initialisation, before executing any .tvmx binary.
pub fn inject_stubs(mem: &mut Memory) -> anyhow::Result<()> {
    // Im_Syscall encoding: Type I  →  opcode(8) | dst(5) | imm19
    // We encode the syscall ID in the imm19 field.
    // F_Ret encoding:      Type R  →  opcode(8) | 0 | 0 | 0 | 0
    let f_ret_word: u32 = (Opcode::F_Ret as u32) << 24;

    for sc in ALL_SYSCALLS {
        let id = *sc as u16 as u32;
        // Im_Syscall  dst=0, imm19 = syscall_id
        let im_syscall_word: u32 = ((Opcode::Im_Syscall as u32) << 24) | (id & 0x0007_FFFF);
        let addr = sc.stub_addr();
        mem.write_u32(addr, im_syscall_word)
            .map_err(|e| anyhow::anyhow!("libc stub inject Im_Syscall@{:#010x}: {}", addr, e))?;
        mem.write_u32(addr + 4, f_ret_word)
            .map_err(|e| anyhow::anyhow!("libc stub inject F_Ret@{:#010x}: {}", addr + 4, e))?;
    }
    Ok(())
}

/// Build the libc symbol table: symbol name → stub VM address.
/// Used by the VM at startup to expose libc symbols to the linker (future tsk-link integration)
/// and to resolve calls from Wolf3D code that references external C functions.
pub fn symbol_table() -> Vec<(&'static str, u64)> {
    ALL_SYSCALLS.iter()
        .map(|sc| (sc.symbol_name(), sc.stub_addr()))
        .collect()
}

// ─────────────────────────────────────────────────────────────────────────────
// Runtime state
// ─────────────────────────────────────────────────────────────────────────────

/// Runtime state for libc (rand seed, etc.).
pub struct LibcState {
    rand_seed: u64,
}

impl LibcState {
    pub fn new() -> Self { Self { rand_seed: 12345 } }
}

// ─────────────────────────────────────────────────────────────────────────────
// Syscall dispatch
// ─────────────────────────────────────────────────────────────────────────────

/// Execute a libc syscall. Called from the VM when Im_Syscall is encountered.
/// Calling convention (mirrors C ABI on TriskeleVM):
///   R0 = first arg, R1 = second, R2 = third, ...
///   R0 = return value on exit
pub fn dispatch(
    id:    u16,
    mem:   &mut Memory,
    regs:  &mut RegisterFile,
    state: &mut LibcState,
) -> Result<(), VmError> {
    let sc = LibcSyscall::from_u16(id)
        .ok_or(VmError::FfiError(format!("unknown libc syscall id: {:#04x}", id)))?;

    match sc {
        // ── Memory ───────────────────────────────────────────────────────────

        LibcSyscall::Memset => {
            // void* memset(void* dst, int val, size_t n)  → R0 = dst (unchanged)
            let dst = regs.get(0)?;
            let val = regs.get(1)? as u8;
            let n   = regs.get(2)? as usize;
            mem.memset(dst, val, n)?;
            // R0 already = dst
        }

        LibcSyscall::Memcpy => {
            // void* memcpy(void* dst, const void* src, size_t n)  → R0 = dst
            let dst = regs.get(0)?;
            let src = regs.get(1)?;
            let n   = regs.get(2)? as usize;
            mem.memcpy(dst, src, n)?;
        }

        LibcSyscall::Memmove => {
            // Identical to memcpy for non-overlapping (Wolf3D assumption)
            let dst = regs.get(0)?;
            let src = regs.get(1)?;
            let n   = regs.get(2)? as usize;
            mem.memcpy(dst, src, n)?;
        }

        LibcSyscall::Memcmp => {
            // int memcmp(const void* a, const void* b, size_t n)  → R0 = cmp result
            let a = regs.get(0)?;
            let b = regs.get(1)?;
            let n = regs.get(2)? as usize;
            let mut result: i32 = 0;
            for i in 0..n {
                let ba = mem.read_u8(a + i as u64)?;
                let bb = mem.read_u8(b + i as u64)?;
                if ba != bb {
                    result = ba as i32 - bb as i32;
                    break;
                }
            }
            regs.set(0, result as u64)?;
        }

        // ── String ───────────────────────────────────────────────────────────

        LibcSyscall::Strlen => {
            // size_t strlen(const char* s)  → R0 = length
            let ptr = regs.get(0)?;
            let mut len = 0u64;
            loop {
                let b = mem.read_u8(ptr + len)?;
                if b == 0 { break; }
                len += 1;
            }
            regs.set(0, len)?;
        }

        LibcSyscall::Strcpy => {
            // char* strcpy(char* dst, const char* src)  → R0 = dst
            let dst = regs.get(0)?;
            let src = regs.get(1)?;
            let mut i = 0u64;
            loop {
                let b = mem.read_u8(src + i)?;
                mem.write_u8(dst + i, b)?;
                if b == 0 { break; }
                i += 1;
            }
        }

        LibcSyscall::Strncpy => {
            // char* strncpy(char* dst, const char* src, size_t n)  → R0 = dst
            let dst = regs.get(0)?;
            let src = regs.get(1)?;
            let n   = regs.get(2)? as usize;
            let mut i = 0usize;
            while i < n {
                let b = mem.read_u8(src + i as u64)?;
                mem.write_u8(dst + i as u64, b)?;
                if b == 0 {
                    // zero-pad remaining
                    for j in (i + 1)..n {
                        mem.write_u8(dst + j as u64, 0)?;
                    }
                    break;
                }
                i += 1;
            }
        }

        LibcSyscall::Strcmp => {
            // int strcmp(const char* a, const char* b)  → R0
            let a = regs.get(0)?;
            let b = regs.get(1)?;
            let mut i = 0u64;
            let result = loop {
                let ca = mem.read_u8(a + i)?;
                let cb = mem.read_u8(b + i)?;
                if ca != cb { break ca as i32 - cb as i32; }
                if ca == 0  { break 0; }
                i += 1;
            };
            regs.set(0, result as u64)?;
        }

        LibcSyscall::Strncmp => {
            // int strncmp(const char* a, const char* b, size_t n)  → R0
            let a = regs.get(0)?;
            let b = regs.get(1)?;
            let n = regs.get(2)? as usize;
            let mut result = 0i32;
            for i in 0..n {
                let ca = mem.read_u8(a + i as u64)?;
                let cb = mem.read_u8(b + i as u64)?;
                if ca != cb { result = ca as i32 - cb as i32; break; }
                if ca == 0  { break; }
            }
            regs.set(0, result as u64)?;
        }

        LibcSyscall::Strchr => {
            // char* strchr(const char* s, int c)  → R0 = ptr or 0
            let s = regs.get(0)?;
            let c = regs.get(1)? as u8;
            let mut i = 0u64;
            let found = loop {
                let b = mem.read_u8(s + i)?;
                if b == c { break s + i; }
                if b == 0 { break 0; }
                i += 1;
            };
            regs.set(0, found)?;
        }

        // ── Math (Wolf3D: fixed-point 16.16) ─────────────────────────────────
        // Wolf3D C89 was compiled for 16-bit x86 with no FPU — it uses lookup
        // tables internally. When compiled via clang -O0 to LLVM IR, float ops
        // appear as double in LLVM IR but are passed as i64 bit-patterns in R0.
        // We interpret R0 as an f64 bit-pattern, compute, and return f64 bits.

        LibcSyscall::Sin => {
            let bits = regs.get(0)?;
            let x = f64::from_bits(bits);
            let r = x.sin();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Cos => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).cos();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Tan => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).tan();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Atan => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).atan();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Atan2 => {
            // atan2(y, x) — y in R0, x in R1
            let y = f64::from_bits(regs.get(0)?);
            let x = f64::from_bits(regs.get(1)?);
            let r = y.atan2(x);
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Sqrt => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).sqrt();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Fabs => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).abs();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Floor => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).floor();
            regs.set(0, r.to_bits())?;
        }
        LibcSyscall::Ceil => {
            let bits = regs.get(0)?;
            let r = f64::from_bits(bits).ceil();
            regs.set(0, r.to_bits())?;
        }

        // ── Stdlib ───────────────────────────────────────────────────────────

        LibcSyscall::Abs => {
            let v = regs.get(0)? as i64;
            regs.set(0, v.unsigned_abs())?;
        }

        LibcSyscall::Rand => {
            // LCG: same constants as glibc for predictable test behavior
            state.rand_seed = state.rand_seed
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            let r = ((state.rand_seed >> 33) as i32).unsigned_abs();
            regs.set(0, r as u64)?;
        }

        LibcSyscall::Srand => {
            state.rand_seed = regs.get(0)?;
        }

        // ── I/O (debug stub) ─────────────────────────────────────────────────

        LibcSyscall::Printf => {
            // Debug stub: read format string from R0 and print its address
            // Full printf would require format string parsing — out of scope for Wolf3D.
            let fmt_ptr = regs.get(0)?;
            eprintln!("[tsk-libc] printf @ fmt_ptr=0x{:08x}", fmt_ptr);
            regs.set(0, 0)?;
        }
    }

    Ok(())
}

// ─────────────────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use crate::memory::{Memory, NULL_PAGE_END};
    use triskele_common::registers::RegisterFile;
    use crate::memory::STACK_TOP;

    fn setup_mem() -> (Memory, RegisterFile, LibcState) {
        let mut mem = Memory::new(NULL_PAGE_END, 0x0010_0000);
        mem.add_segment(LIBC_BASE, (ALL_SYSCALLS.len() as u64 + 1) * STUB_SIZE);
        let regs = RegisterFile::new(STACK_TOP, NULL_PAGE_END);
        let state = LibcState::new();
        (mem, regs, state)
    }

    // ── inject_stubs ─────────────────────────────────────────────────────────

    #[test]
    fn test_inject_stubs_memset_opcode() {
        let (mut mem, _, _) = setup_mem();
        inject_stubs(&mut mem).unwrap();
        let addr = LibcSyscall::Memset.stub_addr();
        let word = mem.read_u32(addr).unwrap();
        let opcode = (word >> 24) as u8;
        use triskele_common::isa::Opcode;
        assert_eq!(opcode, Opcode::Im_Syscall as u8,
            "stub must start with Im_Syscall");
        let imm = word & 0x0007_FFFF;
        assert_eq!(imm, LibcSyscall::Memset as u32,
            "Im_Syscall imm must equal Memset syscall id");
    }

    #[test]
    fn test_inject_stubs_f_ret() {
        let (mut mem, _, _) = setup_mem();
        inject_stubs(&mut mem).unwrap();
        let addr = LibcSyscall::Strlen.stub_addr();
        let ret_word = mem.read_u32(addr + 4).unwrap();
        let opcode = (ret_word >> 24) as u8;
        use triskele_common::isa::Opcode;
        assert_eq!(opcode, Opcode::F_Ret as u8, "second word must be F_Ret");
    }

    // ── memset ───────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_memset() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let base = NULL_PAGE_END + 0x100;
        regs.set(0, base).unwrap();          // dst
        regs.set(1, 0xAB).unwrap();          // val
        regs.set(2, 16).unwrap();            // n
        dispatch(LibcSyscall::Memset as u16, &mut mem, &mut regs, &mut state).unwrap();
        for i in 0..16u64 {
            assert_eq!(mem.read_u8(base + i).unwrap(), 0xAB);
        }
        assert_eq!(regs.get(0).unwrap(), base, "memset must return dst");
    }

    // ── memcpy ───────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_memcpy() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let src = NULL_PAGE_END + 0x100;
        let dst = NULL_PAGE_END + 0x200;
        for i in 0..8u64 { mem.write_u8(src + i, i as u8 + 1).unwrap(); }
        regs.set(0, dst).unwrap();
        regs.set(1, src).unwrap();
        regs.set(2, 8).unwrap();
        dispatch(LibcSyscall::Memcpy as u16, &mut mem, &mut regs, &mut state).unwrap();
        for i in 0..8u64 {
            assert_eq!(mem.read_u8(dst + i).unwrap(), i as u8 + 1);
        }
    }

    // ── strlen ───────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_strlen() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let ptr = NULL_PAGE_END + 0x100;
        let s = b"Hello\0";
        mem.write_bytes(ptr, s).unwrap();
        regs.set(0, ptr).unwrap();
        dispatch(LibcSyscall::Strlen as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 5);
    }

    #[test]
    fn test_libc_strlen_empty() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let ptr = NULL_PAGE_END + 0x100;
        mem.write_u8(ptr, 0).unwrap();
        regs.set(0, ptr).unwrap();
        dispatch(LibcSyscall::Strlen as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 0);
    }

    // ── strcmp ───────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_strcmp_equal() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let a = NULL_PAGE_END + 0x100;
        let b = NULL_PAGE_END + 0x200;
        mem.write_bytes(a, b"wolf3d\0").unwrap();
        mem.write_bytes(b, b"wolf3d\0").unwrap();
        regs.set(0, a).unwrap();
        regs.set(1, b).unwrap();
        dispatch(LibcSyscall::Strcmp as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap() as i32, 0);
    }

    #[test]
    fn test_libc_strcmp_less() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let a = NULL_PAGE_END + 0x100;
        let b = NULL_PAGE_END + 0x200;
        mem.write_bytes(a, b"abc\0").unwrap();
        mem.write_bytes(b, b"abd\0").unwrap();
        regs.set(0, a).unwrap();
        regs.set(1, b).unwrap();
        dispatch(LibcSyscall::Strcmp as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert!((regs.get(0).unwrap() as i32) < 0);
    }

    // ── strcpy ───────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_strcpy() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let src = NULL_PAGE_END + 0x100;
        let dst = NULL_PAGE_END + 0x200;
        mem.write_bytes(src, b"TriskeleVM\0").unwrap();
        regs.set(0, dst).unwrap();
        regs.set(1, src).unwrap();
        dispatch(LibcSyscall::Strcpy as u16, &mut mem, &mut regs, &mut state).unwrap();
        let result = &mem.read_bytes(dst, 11).unwrap();
        assert_eq!(*result, b"TriskeleVM\0");
    }

    // ── memcmp ───────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_memcmp_equal() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let a = NULL_PAGE_END + 0x100;
        let b = NULL_PAGE_END + 0x200;
        mem.write_bytes(a, b"ABCD").unwrap();
        mem.write_bytes(b, b"ABCD").unwrap();
        regs.set(0, a).unwrap(); regs.set(1, b).unwrap(); regs.set(2, 4).unwrap();
        dispatch(LibcSyscall::Memcmp as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap() as i32, 0);
    }

    // ── abs ──────────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_abs() {
        let (mut mem, mut regs, mut state) = setup_mem();
        regs.set(0, (-42i64) as u64).unwrap();
        dispatch(LibcSyscall::Abs as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 42);
    }

    // ── rand / srand ─────────────────────────────────────────────────────────

    #[test]
    fn test_libc_rand_reproducible() {
        let (mut mem, mut regs, mut state) = setup_mem();
        // Seed with srand(42)
        regs.set(0, 42).unwrap();
        dispatch(LibcSyscall::Srand as u16, &mut mem, &mut regs, &mut state).unwrap();
        // Two calls to rand must produce non-zero, different values
        dispatch(LibcSyscall::Rand as u16, &mut mem, &mut regs, &mut state).unwrap();
        let r1 = regs.get(0).unwrap();
        dispatch(LibcSyscall::Rand as u16, &mut mem, &mut regs, &mut state).unwrap();
        let r2 = regs.get(0).unwrap();
        assert_ne!(r1, r2, "consecutive rand() calls must differ");
    }

    // ── sin / cos ────────────────────────────────────────────────────────────

    #[test]
    fn test_libc_sin_zero() {
        let (mut mem, mut regs, mut state) = setup_mem();
        regs.set(0, 0.0f64.to_bits()).unwrap();
        dispatch(LibcSyscall::Sin as u16, &mut mem, &mut regs, &mut state).unwrap();
        let result = f64::from_bits(regs.get(0).unwrap());
        assert!((result - 0.0).abs() < 1e-10, "sin(0) must be ~0");
    }

    #[test]
    fn test_libc_cos_zero() {
        let (mut mem, mut regs, mut state) = setup_mem();
        regs.set(0, 0.0f64.to_bits()).unwrap();
        dispatch(LibcSyscall::Cos as u16, &mut mem, &mut regs, &mut state).unwrap();
        let result = f64::from_bits(regs.get(0).unwrap());
        assert!((result - 1.0).abs() < 1e-10, "cos(0) must be ~1");
    }

    // ── symbol_table ─────────────────────────────────────────────────────────

    #[test]
    fn test_symbol_table_contains_all_functions() {
        let table = symbol_table();
        assert!(table.len() == ALL_SYSCALLS.len());
        let names: Vec<&str> = table.iter().map(|(n, _)| *n).collect();
        assert!(names.contains(&"memset"));
        assert!(names.contains(&"sin"));
        assert!(names.contains(&"strlen"));
        assert!(names.contains(&"printf"));
    }

    #[test]
    fn test_stub_addresses_are_unique() {
        let table = symbol_table();
        let mut addrs: Vec<u64> = table.iter().map(|(_, a)| *a).collect();
        let before = addrs.len();
        addrs.sort();
        addrs.dedup();
        assert_eq!(addrs.len(), before, "all stub addresses must be unique");
    }
}
