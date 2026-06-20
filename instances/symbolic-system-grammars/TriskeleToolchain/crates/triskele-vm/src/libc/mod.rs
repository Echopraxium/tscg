// triskele-vm/src/libc/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11
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
//   I/O    : printf (%d %i %u %x %X %p %s %c %% — Wolf3D/Doom patterns)
//            snprintf, vsnprintf, sscanf
//   Ctype  : toupper, tolower, isspace, isdigit, isalpha, isprint
//   File   : fopen, fclose, fread, fwrite, fseek, ftell, feof, fflush
//   StrExt : strrchr, strstr, strdup, strcasecmp, strncasecmp, strlcat, strlcpy
//            strerror
//   Stdlib+: atoi, strtol

use triskele_common::error::VmError;
use triskele_common::isa::Opcode;
use triskele_common::registers::RegisterFile;
use std::io::{Read, Write, Seek, SeekFrom};
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
    Strchr       = 0x15,
    Strrchr      = 0x16,
    Strstr       = 0x17,
    Strdup       = 0x18,
    Strcasecmp   = 0x19,
    Strncasecmp  = 0x1A,
    Strlcat      = 0x1B,
    Strlcpy      = 0x1C,
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
    Malloc   = 0x33,
    Free     = 0x34,
    Exit     = 0x35,
    Atoi     = 0x36,
    Strtol   = 0x37,
    // I/O
    Printf   = 0x40,
    Fprintf  = 0x41,
    Vfprintf = 0x42,
    Sprintf  = 0x43,
    Puts     = 0x44,
    Vsprintf   = 0x45,
    Snprintf   = 0x46,
    Vsnprintf  = 0x47,
    // Ctype
    Toupper  = 0x50,
    Tolower  = 0x51,
    Isspace  = 0x52,
    Isdigit  = 0x53,
    Isalpha  = 0x54,
    Isprint  = 0x55,
    // File I/O
    Fopen    = 0x60,
    Fclose   = 0x61,
    Fread    = 0x62,
    Fwrite   = 0x63,
    Fseek    = 0x64,
    Ftell    = 0x65,
    Feof     = 0x66,
    Fflush   = 0x67,
    // String utils (Doom m_config.c and others)
    Strerror = 0x68,
    Sscanf   = 0x69,
    // stdlib extra
    Calloc   = 0x6A,
}

impl LibcSyscall {
    pub fn from_u16(id: u16) -> Option<Self> {
        match id {
            0x01 => Some(Self::Memset),  0x02 => Some(Self::Memcpy),
            0x03 => Some(Self::Memmove), 0x04 => Some(Self::Memcmp),
            0x10 => Some(Self::Strlen),  0x11 => Some(Self::Strcpy),
            0x12 => Some(Self::Strncpy), 0x13 => Some(Self::Strcmp),
            0x14 => Some(Self::Strncmp), 0x15 => Some(Self::Strchr),
            0x16 => Some(Self::Strrchr),     0x17 => Some(Self::Strstr),
            0x18 => Some(Self::Strdup),      0x19 => Some(Self::Strcasecmp),
            0x1A => Some(Self::Strncasecmp), 0x1B => Some(Self::Strlcat),
            0x1C => Some(Self::Strlcpy),
            0x20 => Some(Self::Sin),     0x21 => Some(Self::Cos),
            0x22 => Some(Self::Tan),     0x23 => Some(Self::Atan),
            0x24 => Some(Self::Atan2),   0x25 => Some(Self::Sqrt),
            0x26 => Some(Self::Fabs),    0x27 => Some(Self::Floor),
            0x28 => Some(Self::Ceil),
            0x30 => Some(Self::Abs),     0x31 => Some(Self::Rand),
            0x32 => Some(Self::Srand),   0x33 => Some(Self::Malloc),
            0x34 => Some(Self::Free),    0x35 => Some(Self::Exit),
            0x36 => Some(Self::Atoi),    0x37 => Some(Self::Strtol),
            0x40 => Some(Self::Printf),  0x41 => Some(Self::Fprintf),
            0x42 => Some(Self::Vfprintf),0x43 => Some(Self::Sprintf),
            0x44 => Some(Self::Puts),    0x45 => Some(Self::Vsprintf),
            0x46 => Some(Self::Snprintf),  0x47 => Some(Self::Vsnprintf),
            0x50 => Some(Self::Toupper),   0x51 => Some(Self::Tolower),
            0x52 => Some(Self::Isspace),   0x53 => Some(Self::Isdigit),
            0x54 => Some(Self::Isalpha),   0x55 => Some(Self::Isprint),
            0x60 => Some(Self::Fopen),     0x61 => Some(Self::Fclose),
            0x62 => Some(Self::Fread),     0x63 => Some(Self::Fwrite),
            0x64 => Some(Self::Fseek),     0x65 => Some(Self::Ftell),
            0x66 => Some(Self::Feof),      0x67 => Some(Self::Fflush),
            0x68 => Some(Self::Strerror),  0x69 => Some(Self::Sscanf),
            0x6A => Some(Self::Calloc),
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
            Self::Strrchr     => "strrchr",
            Self::Strstr      => "strstr",
            Self::Strdup      => "strdup",
            Self::Strcasecmp  => "strcasecmp",
            Self::Strncasecmp => "strncasecmp",
            Self::Strlcat     => "strlcat",
            Self::Strlcpy     => "strlcpy",
            Self::Sin     => "sin",     Self::Cos     => "cos",
            Self::Tan     => "tan",     Self::Atan    => "atan",
            Self::Atan2   => "atan2",   Self::Sqrt    => "sqrt",
            Self::Fabs    => "fabs",    Self::Floor   => "floor",
            Self::Ceil    => "ceil",
            Self::Abs     => "abs",     Self::Rand    => "rand",
            Self::Srand   => "srand",   Self::Malloc  => "malloc",
            Self::Free    => "free",    Self::Exit    => "exit",
            Self::Atoi    => "atoi",    Self::Strtol  => "strtol",
            Self::Printf  => "printf",  Self::Fprintf => "fprintf",
            Self::Vfprintf=> "vfprintf",Self::Sprintf => "sprintf",
            Self::Puts     => "puts",      Self::Vsprintf  => "vsprintf",
            Self::Snprintf  => "snprintf",  Self::Vsnprintf => "vsnprintf",
            Self::Toupper   => "toupper",   Self::Tolower   => "tolower",
            Self::Isspace   => "isspace",   Self::Isdigit   => "isdigit",
            Self::Isalpha   => "isalpha",   Self::Isprint   => "isprint",
            Self::Fopen     => "fopen",     Self::Fclose    => "fclose",
            Self::Fread     => "fread",     Self::Fwrite    => "fwrite",
            Self::Fseek     => "fseek",     Self::Ftell     => "ftell",
            Self::Feof      => "feof",      Self::Fflush    => "fflush",
            Self::Strerror  => "strerror",  Self::Sscanf    => "sscanf",
            Self::Calloc    => "calloc",
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
    LibcSyscall::Strrchr, LibcSyscall::Strstr,  LibcSyscall::Strdup,
    LibcSyscall::Strcasecmp, LibcSyscall::Strncasecmp,
    LibcSyscall::Strlcat, LibcSyscall::Strlcpy,
    LibcSyscall::Sin,     LibcSyscall::Cos,     LibcSyscall::Tan,
    LibcSyscall::Atan,    LibcSyscall::Atan2,   LibcSyscall::Sqrt,
    LibcSyscall::Fabs,    LibcSyscall::Floor,   LibcSyscall::Ceil,
    LibcSyscall::Abs,     LibcSyscall::Rand,    LibcSyscall::Srand,
    LibcSyscall::Malloc,  LibcSyscall::Free,    LibcSyscall::Exit,
    LibcSyscall::Atoi,    LibcSyscall::Strtol,
    LibcSyscall::Printf,  LibcSyscall::Fprintf, LibcSyscall::Vfprintf,
    LibcSyscall::Sprintf,  LibcSyscall::Puts,     LibcSyscall::Vsprintf,
    LibcSyscall::Snprintf, LibcSyscall::Vsnprintf,
    LibcSyscall::Toupper,  LibcSyscall::Tolower,
    LibcSyscall::Isspace,  LibcSyscall::Isdigit,  LibcSyscall::Isalpha, LibcSyscall::Isprint,
    LibcSyscall::Fopen,    LibcSyscall::Fclose,
    LibcSyscall::Fread,    LibcSyscall::Fwrite,
    LibcSyscall::Fseek,    LibcSyscall::Ftell,    LibcSyscall::Feof,    LibcSyscall::Fflush,
    LibcSyscall::Strerror, LibcSyscall::Sscanf,
    LibcSyscall::Calloc,
];

/// Inject all libc stubs into VM memory at LIBC_BASE.
/// Must be called during VM initialisation, before executing any .tvmx binary.
pub fn inject_stubs(mem: &mut Memory) -> anyhow::Result<()> {
    // Im_Syscall encoding: Type I  →  opcode(8) | dst(5) | imm19
    // We encode the syscall ID in the imm19 field.
    // Highest discriminant: 0x6A (Calloc) → segment size = (0x6B) * STUB_SIZE
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

/// Runtime state for libc (rand seed, heap bump allocator, etc.).
/// File handle table entry — native only (no std::fs in WASM).
#[cfg(feature = "native")]
#[derive(Debug)]
pub struct FileHandle {
    /// Host-side file (using std::fs::File).
    pub file: std::fs::File,
    /// End-of-file flag.
    pub eof:  bool,
}

/// Maximum number of simultaneously open file descriptors.
pub const MAX_FILE_HANDLES: usize = 32;

pub struct LibcState {
    rand_seed:  u64,
    /// Bump-pointer heap for malloc — grows from HEAP_BASE upward.
    heap_bump:  u64,
    /// Heap ceiling (exclusive).
    heap_ceil:  u64,
    /// Open file handles — native only (no std::fs in WASM).
    #[cfg(feature = "native")]
    pub file_handles: Vec<Option<FileHandle>>,
}

/// VM address base for FILE* pointers (must not overlap any real VM memory).
pub const FILE_HANDLE_BASE: u64 = 0xF000_0000;

impl LibcState {
    pub fn new() -> Self {
        use super::memory::{HEAP_BASE, HEAP_SIZE};
        Self {
            rand_seed: 12345,
            heap_bump: HEAP_BASE,
            heap_ceil: HEAP_BASE + HEAP_SIZE,
            #[cfg(feature = "native")]
            file_handles: {
                let mut handles = Vec::with_capacity(MAX_FILE_HANDLES);
                for _ in 0..MAX_FILE_HANDLES { handles.push(None); }
                handles
            },
        }
    }

    /// Allocate a new file handle slot. Returns VM FILE* address, or 0 on failure.
    #[cfg(feature = "native")]
    pub fn alloc_handle(&mut self, fh: FileHandle) -> u64 {
        for (i, slot) in self.file_handles.iter_mut().enumerate() {
            if slot.is_none() {
                *slot = Some(fh);
                return FILE_HANDLE_BASE + i as u64;
            }
        }
        0 // too many open files
    }

    /// Resolve VM FILE* to mutable handle reference.
    #[cfg(feature = "native")]
    pub fn get_handle_mut(&mut self, vm_fp: u64) -> Option<&mut FileHandle> {
        let idx = vm_fp.checked_sub(FILE_HANDLE_BASE)? as usize;
        self.file_handles.get_mut(idx)?.as_mut()
    }

    /// Close and free a handle by VM FILE*.
    #[cfg(feature = "native")]
    pub fn free_handle(&mut self, vm_fp: u64) -> bool {
        let idx = match vm_fp.checked_sub(FILE_HANDLE_BASE) {
            Some(i) => i as usize,
            None    => return false,
        };
        if let Some(slot) = self.file_handles.get_mut(idx) {
            if slot.is_some() {
                *slot = None;
                return true;
            }
        }
        false
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Printf formatting helper
// ─────────────────────────────────────────────────────────────────────────────

/// Shared printf-family formatter.
///
/// Reads a null-terminated format string from VM memory at `fmt_ptr`,
/// substitutes up to 4 positional arguments from `args`, and returns
/// the formatted string.
///
/// Supported specifiers (Wolf3D / Doom C89 patterns):
///   %d %i %u %x %X %p %s %c %%
///   width/precision/flags are NOT supported (not needed for target code).
fn format_printf(fmt_ptr: u64, args: &[u64], mem: &Memory) -> Result<String, VmError> {
    let mut out = String::new();
    let mut arg_idx = 0usize;
    let mut i = 0u64;

    loop {
        let b = mem.read_u8(fmt_ptr + i)
            .map_err(|_| VmError::FfiError(format!(
                "printf: format string read fault at 0x{:x}", fmt_ptr + i)))?;
        if b == 0 { break; }
        i += 1;

        if b != b'%' {
            out.push(b as char);
            continue;
        }

        // Peek at next char — skip flags/width/precision for simplicity
        let spec = mem.read_u8(fmt_ptr + i)
            .map_err(|_| VmError::FfiError("printf: truncated format specifier".to_string()))?;
        i += 1;

        let arg = if arg_idx < args.len() { args[arg_idx] } else { 0 };
        match spec {
            b'd' | b'i' => { out.push_str(&(arg as i64).to_string()); arg_idx += 1; }
            b'u'        => { out.push_str(&arg.to_string());           arg_idx += 1; }
            b'x'        => { out.push_str(&format!("{:x}", arg));      arg_idx += 1; }
            b'X'        => { out.push_str(&format!("{:X}", arg));      arg_idx += 1; }
            b'p'        => { out.push_str(&format!("0x{:08x}", arg));  arg_idx += 1; }
            b'c'        => { out.push((arg as u8) as char);            arg_idx += 1; }
            b's' => {
                let str_ptr = arg;
                let mut si = 0u64;
                loop {
                    let sb = mem.read_u8(str_ptr + si)
                        .map_err(|_| VmError::FfiError(format!(
                            "printf: %s read fault at 0x{:x}", str_ptr + si)))?;
                    if sb == 0 { break; }
                    out.push(sb as char);
                    si += 1;
                }
                arg_idx += 1;
            }
            b'%' => { out.push('%'); }
            other => { out.push('%'); out.push(other as char); }
        }
    }
    Ok(out)
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

        // ── Heap ─────────────────────────────────────────────────────────

        LibcSyscall::Malloc => {
            // void* malloc(size_t size)  → R0 = ptr or 0
            // Bump allocator: align to 8, fail if out of heap space.
            let size = regs.get(0)? as usize;
            if size == 0 {
                regs.set(0, 0)?;
            } else {
                let aligned = (size + 7) & !7;
                let ptr = state.heap_bump;
                if ptr + aligned as u64 > state.heap_ceil {
                    regs.set(0, 0)?; // OOM
                } else {
                    state.heap_bump += aligned as u64;
                    // Zero-initialise (C malloc does NOT zero, but helps catch bugs)
                    mem.memset(ptr, 0, aligned)?;
                    regs.set(0, ptr)?;
                }
            }
        }

        LibcSyscall::Free => {
            // void free(void* ptr)  — no-op for bump allocator
            // Wolf3D/Doom use Z_Malloc as primary allocator; libc free is rare.
            // R0 = ptr (ignored)
        }

        LibcSyscall::Exit => {
            // void exit(int status) — clean VM halt.
            // Use Halted (not Trap) so run() returns Ok(code) → process::exit(code).
            let code = regs.get(0)? as i32;
            return Err(VmError::Halted(code));
        }

        // ── I/O ─────────────────────────────────────────────────────────────

        LibcSyscall::Printf => {
            // int printf(const char* fmt, ...)  — R0=fmt, R1..R4=args
            let fmt_ptr = regs.get(0)?;
            let args = [regs.get(1)?, regs.get(2)?, regs.get(3)?, regs.get(4)?];
            let out = format_printf(fmt_ptr, &args, mem)?;
            let char_count = out.len();
            eprint!("{}", out);  // output to stderr (VM debug channel)
            regs.set(0, char_count as u64)?;
        }

        LibcSyscall::Fprintf => {
            // int fprintf(FILE* stream, const char* fmt, ...)
            // R0 = FILE* (ignored — all output to stderr), R1 = fmt_ptr, R2..R5 = args
            // Reuse printf logic with shifted argument registers.
            let fmt_ptr = regs.get(1)?;
            let args = [regs.get(2)?, regs.get(3)?, regs.get(4)?, regs.get(5)?];
            let out = format_printf(fmt_ptr, &args, mem)?;
            let char_count = out.len();
            eprint!("{}", out);
            regs.set(0, char_count as u64)?;
        }

        LibcSyscall::Vfprintf => {
            // int vfprintf(FILE* stream, const char* fmt, va_list ap)
            // Called via _vfprintf_l redirect: R0=FILE*, R1=fmt_ptr, R2=va_ptr
            // va_ptr is a pointer into VM memory containing packed 8-byte args.
            // We read up to 4 args from memory at va_ptr.
            // If va_ptr is 0 (from VaStart NULL), fall back to R3..R6 as args.
            let fmt_ptr = regs.get(1)?;
            let va_ptr  = regs.get(2)?;
            let args = if va_ptr != 0 {
                let mut a = [0u64; 4];
                for i in 0..4usize {
                    a[i] = mem.read_u64(va_ptr + i as u64 * 8).unwrap_or(0);
                }
                a
            } else {
                // va_ptr=0 (VaStart wrote NULL): read args from caller registers R3..R6
                [regs.get(3).unwrap_or(0), regs.get(4).unwrap_or(0),
                 regs.get(5).unwrap_or(0), regs.get(6).unwrap_or(0)]
            };
            let out = format_printf(fmt_ptr, &args, mem)?;
            let char_count = out.len();
            eprint!("{}", out);
            regs.set(0, char_count as u64)?;
        }

        LibcSyscall::Sprintf => {
            // int sprintf(char* buf, const char* fmt, ...)
            // R0 = buf, R1 = fmt_ptr, R2..R5 = args
            let buf_ptr = regs.get(0)?;
            let fmt_ptr = regs.get(1)?;
            let args = [regs.get(2)?, regs.get(3)?, regs.get(4)?, regs.get(5)?];
            let out = format_printf(fmt_ptr, &args, mem)?;
            let bytes = out.as_bytes();
            mem.write_bytes(buf_ptr, bytes)?;
            mem.write_u8(buf_ptr + bytes.len() as u64, 0)?;
            regs.set(0, bytes.len() as u64)?;
        }

        LibcSyscall::Vsprintf => {
            // int vsprintf(char* buf, const char* fmt, va_ptr)
            // R0=buf, R1=fmt_ptr, R2=va_ptr (from _vsprintf_l redirect)
            // If va_ptr != 0, read args from memory. Else fall back to R3..R6.
            let buf_ptr = regs.get(0)?;
            let fmt_ptr = regs.get(1)?;
            let va_ptr  = regs.get(2)?;
            let args = if va_ptr != 0 {
                let mut a = [0u64; 4];
                for i in 0..4usize {
                    a[i] = mem.read_u64(va_ptr + i as u64 * 8).unwrap_or(0);
                }
                a
            } else {
                [regs.get(3).unwrap_or(0), regs.get(4).unwrap_or(0),
                 regs.get(5).unwrap_or(0), regs.get(6).unwrap_or(0)]
            };
            let out = format_printf(fmt_ptr, &args, mem)?;
            let bytes = out.as_bytes();
            mem.write_bytes(buf_ptr, bytes)?;
            mem.write_u8(buf_ptr + bytes.len() as u64, 0)?;
            regs.set(0, bytes.len() as u64)?;
        }


        // ── String extensions ─────────────────────────────────────────────

        LibcSyscall::Strrchr => {
            // char* strrchr(const char* s, int c)  → R0 = last ptr or 0
            let s = regs.get(0)?;
            let c = regs.get(1)? as u8;
            let mut i = 0u64;
            let mut last_found = 0u64;
            loop {
                let b = mem.read_u8(s + i)?;
                if b == c { last_found = s + i; }
                if b == 0 { break; }
                i += 1;
            }
            regs.set(0, last_found)?;
        }

        LibcSyscall::Strstr => {
            // char* strstr(const char* haystack, const char* needle) → R0 = ptr or 0
            let hay = regs.get(0)?;
            let ndl = regs.get(1)?;
            // Read needle into Vec<u8>
            let mut needle_bytes = Vec::new();
            let mut ni = 0u64;
            loop {
                let b = mem.read_u8(ndl + ni)?;
                if b == 0 { break; }
                needle_bytes.push(b);
                ni += 1;
            }
            if needle_bytes.is_empty() {
                regs.set(0, hay)?;
            } else {
                let nlen = needle_bytes.len();
                let mut i = 0u64;
                let found = loop {
                    // Check if haystack ends before needle fits
                    let first = match mem.read_u8(hay + i) { Ok(b) if b != 0 => b, _ => break 0 };
                    if first == needle_bytes[0] {
                        let mut matched = true;
                        for j in 0..nlen {
                            let b = mem.read_u8(hay + i + j as u64).unwrap_or(0);
                            if b != needle_bytes[j] { matched = false; break; }
                        }
                        if matched { break hay + i; }
                    } else if first == 0 { break 0; }
                    i += 1;
                };
                regs.set(0, found)?;
            }
        }

        LibcSyscall::Strdup => {
            // char* strdup(const char* s)  → R0 = new heap ptr or 0
            let src_ptr = regs.get(0)?;
            // Measure length
            let mut len = 0u64;
            loop {
                let b = mem.read_u8(src_ptr + len)?;
                if b == 0 { break; }
                len += 1;
            }
            let size = len + 1; // include NUL
            let aligned = (size as usize + 7) & !7;
            let ptr = state.heap_bump;
            if ptr + aligned as u64 > state.heap_ceil {
                regs.set(0, 0)?; // OOM
            } else {
                state.heap_bump += aligned as u64;
                // Copy bytes
                for i in 0..=len {
                    let b = mem.read_u8(src_ptr + i)?;
                    mem.write_u8(ptr + i, b)?;
                }
                regs.set(0, ptr)?;
            }
        }

        LibcSyscall::Strcasecmp => {
            // int strcasecmp(const char* a, const char* b)  → R0
            let a = regs.get(0)?;
            let b = regs.get(1)?;
            let mut i = 0u64;
            let result = loop {
                let ca = mem.read_u8(a + i)?.to_ascii_lowercase();
                let cb = mem.read_u8(b + i)?.to_ascii_lowercase();
                if ca != cb { break ca as i32 - cb as i32; }
                if ca == 0  { break 0; }
                i += 1;
            };
            regs.set(0, result as u64)?;
        }

        LibcSyscall::Strncasecmp => {
            // int strncasecmp(const char* a, const char* b, size_t n)  → R0
            let a = regs.get(0)?;
            let b = regs.get(1)?;
            let n = regs.get(2)? as usize;
            let mut result = 0i32;
            for i in 0..n {
                let ca = mem.read_u8(a + i as u64)?.to_ascii_lowercase();
                let cb = mem.read_u8(b + i as u64)?.to_ascii_lowercase();
                if ca != cb { result = ca as i32 - cb as i32; break; }
                if ca == 0  { break; }
            }
            regs.set(0, result as u64)?;
        }

        LibcSyscall::Strlcat => {
            // size_t strlcat(char* dst, const char* src, size_t dstsize) → R0 = total len
            let dst  = regs.get(0)?;
            let src  = regs.get(1)?;
            let size = regs.get(2)? as usize;
            // Find end of dst
            let mut dlen = 0usize;
            while dlen < size {
                if mem.read_u8(dst + dlen as u64)? == 0 { break; }
                dlen += 1;
            }
            // Measure src length
            let mut slen = 0usize;
            loop {
                if mem.read_u8(src + slen as u64)? == 0 { break; }
                slen += 1;
            }
            // Append as many bytes as fit
            let avail = if size > dlen + 1 { size - dlen - 1 } else { 0 };
            let copy  = slen.min(avail);
            for i in 0..copy {
                let b = mem.read_u8(src + i as u64)?;
                mem.write_u8(dst + dlen as u64 + i as u64, b)?;
            }
            if size > 0 {
                mem.write_u8(dst + (dlen + copy) as u64, 0)?;
            }
            regs.set(0, (dlen + slen) as u64)?;
        }

        LibcSyscall::Strlcpy => {
            // size_t strlcpy(char* dst, const char* src, size_t dstsize) → R0 = src len
            let dst  = regs.get(0)?;
            let src  = regs.get(1)?;
            let size = regs.get(2)? as usize;
            let mut slen = 0usize;
            loop {
                if mem.read_u8(src + slen as u64)? == 0 { break; }
                slen += 1;
            }
            if size > 0 {
                let copy = slen.min(size - 1);
                for i in 0..copy {
                    let b = mem.read_u8(src + i as u64)?;
                    mem.write_u8(dst + i as u64, b)?;
                }
                mem.write_u8(dst + copy as u64, 0)?;
            }
            regs.set(0, slen as u64)?;
        }

        // ── Stdlib extensions ──────────────────────────────────────────────

        LibcSyscall::Atoi => {
            // int atoi(const char* s)  → R0 = integer value
            let ptr = regs.get(0)?;
            let mut i = 0u64;
            // Skip whitespace
            loop {
                let b = mem.read_u8(ptr + i)?;
                if b == b' ' || b == b'\t' || b == b'\n' || b == b'\r' { i += 1; } else { break; }
            }
            let mut neg = false;
            let b = mem.read_u8(ptr + i)?;
            if b == b'-' { neg = true; i += 1; }
            else if b == b'+' { i += 1; }
            let mut val = 0i64;
            loop {
                let b = mem.read_u8(ptr + i)?;
                if b < b'0' || b > b'9' { break; }
                val = val.wrapping_mul(10).wrapping_add((b - b'0') as i64);
                i += 1;
            }
            if neg { val = -val; }
            regs.set(0, val as u64)?;
        }

        LibcSyscall::Strtol => {
            // long strtol(const char* s, char** endptr, int base)  → R0 = value
            // R0=s, R1=endptr (0 = ignored), R2=base (0 or 10 or 16)
            let ptr    = regs.get(0)?;
            let endptr = regs.get(1)?;
            let base   = regs.get(2)? as u32;
            let mut i = 0u64;
            // Skip whitespace
            loop {
                let b = mem.read_u8(ptr + i)?;
                if b == b' ' || b == b'\t' || b == b'\n' || b == b'\r' { i += 1; } else { break; }
            }
            let mut neg = false;
            let b = mem.read_u8(ptr + i)?;
            if b == b'-' { neg = true; i += 1; }
            else if b == b'+' { i += 1; }
            // Auto-detect base
            let actual_base: u64 = if base == 0 {
                let b0 = mem.read_u8(ptr + i)?;
                if b0 == b'0' {
                    let b1 = mem.read_u8(ptr + i + 1).unwrap_or(0);
                    if b1 == b'x' || b1 == b'X' { i += 2; 16 } else { 8 }
                } else { 10 }
            } else if base == 16 {
                let b0 = mem.read_u8(ptr + i)?;
                if b0 == b'0' {
                    let b1 = mem.read_u8(ptr + i + 1).unwrap_or(0);
                    if b1 == b'x' || b1 == b'X' { i += 2; }
                }
                16
            } else { base as u64 };
            let mut val = 0i64;
            loop {
                let b = mem.read_u8(ptr + i)?;
                let digit = match b {
                    b'0'..=b'9' => (b - b'0') as u64,
                    b'a'..=b'f' => (b - b'a' + 10) as u64,
                    b'A'..=b'F' => (b - b'A' + 10) as u64,
                    _ => break,
                };
                if digit >= actual_base { break; }
                val = val.wrapping_mul(actual_base as i64).wrapping_add(digit as i64);
                i += 1;
            }
            if neg { val = -val; }
            if endptr != 0 {
                mem.write_u64(endptr, ptr + i)?;
            }
            regs.set(0, val as u64)?;
        }

        // ── Ctype ──────────────────────────────────────────────────────────

        LibcSyscall::Toupper => {
            let c = regs.get(0)? as u8;
            regs.set(0, c.to_ascii_uppercase() as u64)?;
        }
        LibcSyscall::Tolower => {
            let c = regs.get(0)? as u8;
            regs.set(0, c.to_ascii_lowercase() as u64)?;
        }
        LibcSyscall::Isspace => {
            let c = regs.get(0)? as u8;
            regs.set(0, if c == b' ' || c == b'\t' || c == b'\n' || c == b'\r' || c == 0x0C || c == 0x0B { 1 } else { 0 })?;
        }
        LibcSyscall::Isdigit => {
            let c = regs.get(0)? as u8;
            regs.set(0, if c >= b'0' && c <= b'9' { 1 } else { 0 })?;
        }
        LibcSyscall::Isalpha => {
            let c = regs.get(0)? as u8;
            regs.set(0, if c.is_ascii_alphabetic() { 1 } else { 0 })?;
        }
        LibcSyscall::Isprint => {
            let c = regs.get(0)? as u8;
            regs.set(0, if c >= 0x20 && c < 0x7F { 1 } else { 0 })?;
        }

        // ── File I/O — native only (no std::fs in WASM) ───────────────────
        // In WASM builds these syscalls are unreachable (tsk-libc.tvml is not
        // linked, so no program can call them). If somehow reached, return
        // an error rather than failing to compile.

        LibcSyscall::Fopen => {
            #[cfg(feature = "native")]
            {
            // FILE* fopen(const char* path, const char* mode) → R0 = vm_fp or 0
            let path_ptr = regs.get(0)?;
            let mode_ptr = regs.get(1)?;
            let mut path_bytes = Vec::new();
            let mut i = 0u64;
            loop {
                if i > 4096 {
                    regs.set(0, 0)?;
                    return Ok(());
                }
                let b = mem.read_u8(path_ptr + i)?;
                if b == 0 { break; }
                path_bytes.push(b);
                i += 1;
            }
            let path_str = String::from_utf8_lossy(&path_bytes).to_string();
            let mode0 = mem.read_u8(mode_ptr)?;
            let vm_fp = match mode0 {
                b'r' => {
                    match std::fs::File::open(&path_str) {
                        Ok(f) => state.alloc_handle(FileHandle { file: f, eof: false }),
                        Err(_) => 0,
                    }
                }
                b'w' | b'a' => {
                    let mut opts = std::fs::OpenOptions::new();
                    opts.write(true).create(true);
                    if mode0 == b'a' { opts.append(true); } else { opts.truncate(true); }
                    match opts.open(&path_str) {
                        Ok(f) => state.alloc_handle(FileHandle { file: f, eof: false }),
                        Err(_) => 0,
                    }
                }
                _ => 0,
            };
            regs.set(0, vm_fp)?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, 0)?; } // fopen returns NULL in WASM
        }

        LibcSyscall::Fclose => {
            #[cfg(feature = "native")]
            {
            let vm_fp = regs.get(0)?;
            let ok = state.free_handle(vm_fp);
            regs.set(0, if ok { 0 } else { u64::MAX })?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, u64::MAX)?; }
        }

        LibcSyscall::Fread => {
            #[cfg(feature = "native")]
            {
            let dst_ptr = regs.get(0)?;
            let item_sz = regs.get(1)? as usize;
            let count   = regs.get(2)? as usize;
            let vm_fp   = regs.get(3)?;
            let total   = item_sz * count;
            let mut buf = vec![0u8; total];
            let n_read = if let Some(fh) = state.get_handle_mut(vm_fp) {
                let mut off = 0usize;
                loop {
                    if off >= total { break; }
                    match fh.file.read(&mut buf[off..]) {
                        Ok(0) => { fh.eof = true; break; }
                        Ok(n) => { off += n; }
                        Err(_) => { break; }
                    }
                }
                off
            } else { 0 };
            mem.write_bytes(dst_ptr, &buf[..n_read])?;
            regs.set(0, (if item_sz > 0 { n_read / item_sz } else { 0 }) as u64)?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, 0)?; }
        }

        LibcSyscall::Fwrite => {
            #[cfg(feature = "native")]
            {
            let src_ptr = regs.get(0)?;
            let item_sz = regs.get(1)? as usize;
            let count   = regs.get(2)? as usize;
            let vm_fp   = regs.get(3)?;
            let total   = item_sz * count;
            let buf     = mem.read_bytes(src_ptr, total)?;
            let n_written = if let Some(fh) = state.get_handle_mut(vm_fp) {
                match fh.file.write(&buf) {
                    Ok(n)  => n,
                    Err(_) => 0,
                }
            } else { 0 };
            regs.set(0, (if item_sz > 0 { n_written / item_sz } else { 0 }) as u64)?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, 0)?; }
        }

        LibcSyscall::Fseek => {
            #[cfg(feature = "native")]
            {
            let vm_fp  = regs.get(0)?;
            let offset = regs.get(1)? as i64;
            let whence = regs.get(2)?;
            let seek_from = match whence {
                0 => SeekFrom::Start(offset as u64),
                1 => SeekFrom::Current(offset),
                2 => SeekFrom::End(offset),
                _ => { regs.set(0, u64::MAX)?; return Ok(()); }
            };
            let result = if let Some(fh) = state.get_handle_mut(vm_fp) {
                fh.eof = false;
                match fh.file.seek(seek_from) { Ok(_) => 0u64, Err(_) => u64::MAX }
            } else { u64::MAX };
            regs.set(0, result)?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, u64::MAX)?; }
        }

        LibcSyscall::Ftell => {
            #[cfg(feature = "native")]
            {
            let vm_fp = regs.get(0)?;
            let pos = if let Some(fh) = state.get_handle_mut(vm_fp) {
                match fh.file.stream_position() { Ok(p) => p, Err(_) => u64::MAX }
            } else { u64::MAX };
            regs.set(0, pos)?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, u64::MAX)?; }
        }

        LibcSyscall::Feof => {
            #[cfg(feature = "native")]
            {
            let vm_fp = regs.get(0)?;
            let eof = if let Some(fh) = state.get_handle_mut(vm_fp) { fh.eof } else { true };
            regs.set(0, if eof { 1 } else { 0 })?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, 1)?; }
        }

        LibcSyscall::Fflush => {
            #[cfg(feature = "native")]
            {
            let vm_fp = regs.get(0)?;
            let result = if vm_fp == 0 {
                0u64
            } else if let Some(fh) = state.get_handle_mut(vm_fp) {
                match fh.file.flush() { Ok(_) => 0, Err(_) => u64::MAX }
            } else { u64::MAX };
            regs.set(0, result)?;
            }
            #[cfg(not(feature = "native"))]
            { regs.set(0, 0)?; }
        }

        // ── strerror ──────────────────────────────────────────────────────

        LibcSyscall::Strerror => {
            // char* strerror(int errnum) → R0 = ptr to static error string
            // We write the string into a fixed scratch area in the VM libc segment.
            // Convention: use LIBC_BASE + 0x800 as a 256-byte scratch buffer for
            // static strings returned by strerror.
            let errnum = regs.get(0)? as i32;
            let msg = match errnum {
                0  => "Success",
                1  => "Operation not permitted",
                2  => "No such file or directory",
                4  => "Interrupted system call",
                5  => "Input/output error",
                9  => "Bad file descriptor",
                11 => "Resource temporarily unavailable",
                12 => "Cannot allocate memory",
                13 => "Permission denied",
                17 => "File exists",
                20 => "Not a directory",
                21 => "Is a directory",
                22 => "Invalid argument",
                24 => "Too many open files",
                28 => "No space left on device",
                32 => "Broken pipe",
                _  => "Unknown error",
            };
            let scratch = LIBC_BASE + 0x800;
            let bytes = msg.as_bytes();
            for (i, &b) in bytes.iter().enumerate() {
                mem.write_u8(scratch + i as u64, b)
                    .map_err(|e| VmError::FfiError(format!("strerror: write fault: {}", e)))?;
            }
            mem.write_u8(scratch + bytes.len() as u64, 0)
                .map_err(|e| VmError::FfiError(format!("strerror: null term fault: {}", e)))?;
            regs.set(0, scratch)?;
        }

        // ── sscanf ────────────────────────────────────────────────────────

        LibcSyscall::Sscanf => {
            // int sscanf(const char* str, const char* fmt, ...)
            // R0=str_ptr, R1=fmt_ptr, R2..R5=output pointers (up to 4)
            // Supported: %d %i %u %x %s %c
            // Returns number of items successfully assigned.
            let str_ptr = regs.get(0)?;
            let fmt_ptr = regs.get(1)?;
            let out_ptrs = [regs.get(2)?, regs.get(3)?, regs.get(4)?, regs.get(5)?];

            // Read input string
            let mut input = String::new();
            let mut si = 0u64;
            loop {
                let b = mem.read_u8(str_ptr + si).unwrap_or(0);
                if b == 0 { break; }
                input.push(b as char);
                si += 1;
            }

            // Read format string
            let mut fmt = String::new();
            let mut fi = 0u64;
            loop {
                let b = mem.read_u8(fmt_ptr + fi).unwrap_or(0);
                if b == 0 { break; }
                fmt.push(b as char);
                fi += 1;
            }

            // Simple single-pass parser: split on whitespace, match specifiers
            let mut items_assigned: u64 = 0;
            let mut arg_idx = 0usize;
            let input_tokens: Vec<&str> = input.split_whitespace().collect();
            let mut tok_idx = 0usize;
            let mut fci = fmt.chars().peekable();

            while let Some(fc) = fci.next() {
                if fc != '%' { continue; }
                let spec = match fci.next() { Some(c) => c, None => break };
                if tok_idx >= input_tokens.len() { break; }
                let tok = input_tokens[tok_idx];
                tok_idx += 1;

                if arg_idx >= out_ptrs.len() { break; }
                let out_ptr = out_ptrs[arg_idx];
                arg_idx += 1;

                match spec {
                    'd' | 'i' => {
                        if let Ok(v) = tok.parse::<i32>() {
                            mem.write_u32(out_ptr, v as u32)
                                .map_err(|e| VmError::FfiError(format!("sscanf: write fault: {}", e)))?;
                            items_assigned += 1;
                        }
                    }
                    'u' => {
                        if let Ok(v) = tok.parse::<u32>() {
                            mem.write_u32(out_ptr, v)
                                .map_err(|e| VmError::FfiError(format!("sscanf: write fault: {}", e)))?;
                            items_assigned += 1;
                        }
                    }
                    'x' | 'X' => {
                        let trimmed = tok.trim_start_matches("0x").trim_start_matches("0X");
                        if let Ok(v) = u32::from_str_radix(trimmed, 16) {
                            mem.write_u32(out_ptr, v)
                                .map_err(|e| VmError::FfiError(format!("sscanf: write fault: {}", e)))?;
                            items_assigned += 1;
                        }
                    }
                    's' => {
                        let bytes = tok.as_bytes();
                        for (i, &b) in bytes.iter().enumerate() {
                            mem.write_u8(out_ptr + i as u64, b)
                                .map_err(|e| VmError::FfiError(format!("sscanf: write fault: {}", e)))?;
                        }
                        mem.write_u8(out_ptr + bytes.len() as u64, 0)
                            .map_err(|e| VmError::FfiError(format!("sscanf: null term fault: {}", e)))?;
                        items_assigned += 1;
                    }
                    'c' => {
                        if let Some(b) = tok.bytes().next() {
                            mem.write_u8(out_ptr, b)
                                .map_err(|e| VmError::FfiError(format!("sscanf: write fault: {}", e)))?;
                            items_assigned += 1;
                        }
                    }
                    _ => { /* unsupported specifier — skip */ }
                }
            }
            regs.set(0, items_assigned)?;
        }

        // ── calloc ────────────────────────────────────────────────────────

        LibcSyscall::Calloc => {
            // void* calloc(size_t nmemb, size_t size) → R0 = ptr or 0
            // Equivalent to malloc(nmemb * size) + memset(ptr, 0, nmemb * size)
            let nmemb = regs.get(0)?;
            let size  = regs.get(1)?;
            let total = nmemb.saturating_mul(size);
            let ptr = if total == 0 {
                0u64
            } else {
                let p = state.heap_bump;
                // Align to 8 bytes
                let p_aligned = (p + 7) & !7;
                let next = p_aligned + total;
                if next > state.heap_ceil {
                    0u64
                } else {
                    state.heap_bump = next;
                    // Zero-initialise (calloc guarantee)
                    for i in 0..total {
                        mem.write_u8(p_aligned + i, 0)
                            .map_err(|e| VmError::FfiError(format!("calloc: zero-init fault: {}", e)))?;
                    }
                    p_aligned
                }
            };
            regs.set(0, ptr)?;
        }

        // ── snprintf / vsnprintf ───────────────────────────────────────────

        LibcSyscall::Snprintf => {
            // int snprintf(char* buf, size_t n, const char* fmt, ...)
            // R0=buf, R1=n, R2=fmt, R3..R6=args
            let buf_ptr = regs.get(0)?;
            let max_n   = regs.get(1)? as usize;
            let fmt_ptr = regs.get(2)?;
            let args = [regs.get(3)?, regs.get(4)?, regs.get(5)?, regs.get(6)?];
            let out = format_printf(fmt_ptr, &args, mem)?;
            let bytes = out.as_bytes();
            if max_n > 0 {
                let copy = bytes.len().min(max_n - 1);
                mem.write_bytes(buf_ptr, &bytes[..copy])?;
                mem.write_u8(buf_ptr + copy as u64, 0)?;
            }
            regs.set(0, bytes.len() as u64)?; // returns full length (as if unbounded)
        }

        LibcSyscall::Vsnprintf => {
            // int vsnprintf(char* buf, size_t n, const char* fmt, va_ptr)
            // R0=buf, R1=n, R2=fmt, R3=va_ptr
            let buf_ptr = regs.get(0)?;
            let max_n   = regs.get(1)? as usize;
            let fmt_ptr = regs.get(2)?;
            let va_ptr  = regs.get(3)?;
            let args = if va_ptr != 0 {
                let mut a = [0u64; 4];
                for i in 0..4usize { a[i] = mem.read_u64(va_ptr + i as u64 * 8).unwrap_or(0); }
                a
            } else {
                [regs.get(4).unwrap_or(0), regs.get(5).unwrap_or(0),
                 regs.get(6).unwrap_or(0), regs.get(7).unwrap_or(0)]
            };
            let out = format_printf(fmt_ptr, &args, mem)?;
            let bytes = out.as_bytes();
            if max_n > 0 {
                let copy = bytes.len().min(max_n - 1);
                mem.write_bytes(buf_ptr, &bytes[..copy])?;
                mem.write_u8(buf_ptr + copy as u64, 0)?;
            }
            regs.set(0, bytes.len() as u64)?;
        }

        LibcSyscall::Puts => {
            // int puts(const char* s)  — writes s + '\n' to stdout
            // R0 = str_ptr
            let ptr = regs.get(0)?;
            let mut s = String::new();
            let mut i = 0u64;
            loop {
                let b = mem.read_u8(ptr + i)?;
                if b == 0 { break; }
                s.push(b as char);
                i += 1;
            }
            s.push('\n');
            eprint!("{}", s);
            regs.set(0, s.len() as u64)?;
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
        // Segment must cover the highest discriminant (0x45=Vsprintf)
        mem.add_segment(LIBC_BASE, (0x6B_u64) * STUB_SIZE);  // highest = 0x6A (Calloc)
        let regs = RegisterFile::new(STACK_TOP, NULL_PAGE_END);
        let state = LibcState::new();
        (mem, regs, state)
    }

    /// Setup with a heap segment for malloc/free tests.
    fn setup_mem_with_heap() -> (Memory, RegisterFile, LibcState) {
        use crate::memory::{HEAP_BASE, HEAP_SIZE};
        // Main segment (code/stack area)
        let mut mem = Memory::new(NULL_PAGE_END, 0x0010_0000);
        // Heap segment
        mem.add_segment(HEAP_BASE, HEAP_SIZE);
        // Libc stubs segment
        mem.add_segment(LIBC_BASE, (0x6B_u64) * STUB_SIZE);  // highest = 0x6A (Calloc)
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

    // ── printf ───────────────────────────────────────────────────────────────

    fn write_cstr(mem: &mut Memory, ptr: u64, s: &[u8]) {
        for (i, &b) in s.iter().enumerate() {
            mem.write_u8(ptr + i as u64, b).unwrap();
        }
        mem.write_u8(ptr + s.len() as u64, 0).unwrap();
    }

    #[test]
    fn test_printf_percent_d() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"val=%d");
        regs.set(0, fmt).unwrap();
        regs.set(1, 42u64).unwrap();
        dispatch(LibcSyscall::Printf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 6, "printf returns char count");  // "val=42" = 6 chars
    }

    #[test]
    fn test_printf_percent_s() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt = NULL_PAGE_END + 0x100;
        let msg = NULL_PAGE_END + 0x200;
        write_cstr(&mut mem, fmt, b"err=%s!");
        write_cstr(&mut mem, msg, b"oops");
        regs.set(0, fmt).unwrap();
        regs.set(1, msg).unwrap();
        dispatch(LibcSyscall::Printf as u16, &mut mem, &mut regs, &mut state).unwrap();
        // "err=oops!" = 9 chars
        assert_eq!(regs.get(0).unwrap(), 9);
    }

    #[test]
    fn test_printf_percent_x() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"0x%x");
        regs.set(0, fmt).unwrap();
        regs.set(1, 0xFF).unwrap();
        dispatch(LibcSyscall::Printf as u16, &mut mem, &mut regs, &mut state).unwrap();
        // "0xff" = 4 chars
        assert_eq!(regs.get(0).unwrap(), 4);
    }

    #[test]
    fn test_printf_percent_percent() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"100%%");
        regs.set(0, fmt).unwrap();
        dispatch(LibcSyscall::Printf as u16, &mut mem, &mut regs, &mut state).unwrap();
        // "100%" = 4 chars
        assert_eq!(regs.get(0).unwrap(), 4);
    }

    #[test]
    fn test_printf_no_args() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"hello
");
        regs.set(0, fmt).unwrap();
        dispatch(LibcSyscall::Printf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 6);
    }

    #[test]
    fn test_printf_negative_int() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"%d");
        regs.set(0, fmt).unwrap();
        regs.set(1, (-7i64) as u64).unwrap();
        dispatch(LibcSyscall::Printf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 2); // "-7" = 2 chars
    }

    // ── sprintf ──────────────────────────────────────────────────────────────

    /// Helper: read null-terminated string from VM memory.
    fn read_cstr(mem: &Memory, ptr: u64) -> String {
        let mut s = String::new();
        let mut i = 0u64;
        loop {
            let b = mem.read_u8(ptr + i).unwrap_or(0);
            if b == 0 { break; }
            s.push(b as char);
            i += 1;
            if i > 256 { break; } // safety
        }
        s
    }

    #[test]
    fn test_sprintf_percent_d() {
        // sprintf(buf, "%d", 99)  → buf contains "99\0", returns 2
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x200;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"%d");
        regs.set(0, buf).unwrap();   // buf
        regs.set(1, fmt).unwrap();   // fmt
        regs.set(2, 99u64).unwrap(); // arg
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 2, "sprintf returns char count");
        assert_eq!(read_cstr(&mem, buf), "99", "sprintf writes '99'");
        assert_eq!(mem.read_u8(buf + 2).unwrap(), 0, "null terminator present");
    }

    #[test]
    fn test_sprintf_percent_s() {
        // sprintf(buf, "%s", "hello")  → buf contains "hello\0"
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x300;
        let fmt = NULL_PAGE_END + 0x100;
        let arg = NULL_PAGE_END + 0x200;
        write_cstr(&mut mem, fmt, b"%s");
        write_cstr(&mut mem, arg, b"hello");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, arg).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "hello");
    }

    #[test]
    fn test_sprintf_multi_args() {
        // sprintf(buf, "%d+%d=%d", 1, 2, 3)  → "1+2=3"
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x300;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"%d+%d=%d");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, 1u64).unwrap();
        regs.set(3, 2u64).unwrap();
        regs.set(4, 3u64).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "1+2=3");
        assert_eq!(regs.get(0).unwrap(), 5, "sprintf returns char count");
    }

    #[test]
    fn test_sprintf_writes_to_correct_address() {
        // Verify that Sprintf writes to R0 (buf), not to the format string
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x400;
        let fmt = NULL_PAGE_END + 0x100;
        // Poison buf with 0xFF to make sure sprintf overwrites it
        for i in 0..8u64 { mem.write_u8(buf + i, 0xFF).unwrap(); }
        write_cstr(&mut mem, fmt, b"%d");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, 42u64).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(mem.read_u8(buf).unwrap(), b'4', "buf[0] must be '4'");
        assert_eq!(mem.read_u8(buf + 1).unwrap(), b'2', "buf[1] must be '2'");
        assert_eq!(mem.read_u8(buf + 2).unwrap(), 0,   "buf[2] must be null");
        assert_eq!(mem.read_u8(buf + 3).unwrap(), 0xFF, "buf[3] must be untouched");
    }

    #[test]
    fn test_sprintf_negative_int() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x300;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"%d");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, (-42i64) as u64).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "-42");
    }

    #[test]
    fn test_sprintf_hex() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x300;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"0x%x");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, 0xDEADu64).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "0xdead");
    }

    // ── vsprintf (va_ptr path) ────────────────────────────────────────────────

    #[test]
    fn test_vsprintf_from_va_ptr() {
        // vsprintf(buf, "%d %s", va_ptr) where va_ptr points to [42, ptr_to_"ok"]
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf    = NULL_PAGE_END + 0x400;
        let fmt    = NULL_PAGE_END + 0x100;
        let va_area= NULL_PAGE_END + 0x200;
        let str_ok = NULL_PAGE_END + 0x300;
        write_cstr(&mut mem, fmt, b"%d %s");
        write_cstr(&mut mem, str_ok, b"ok");
        // va_area: [arg0=42 (8 bytes), arg1=ptr_to_"ok" (8 bytes)]
        mem.write_u64(va_area,     42u64).unwrap();
        mem.write_u64(va_area + 8, str_ok).unwrap();
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, va_area).unwrap();  // va_ptr != 0 → read from memory
        dispatch(LibcSyscall::Vsprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "42 ok");
    }

    #[test]
    fn test_vsprintf_va_ptr_zero_fallback() {
        // When va_ptr == 0, Vsprintf falls back to R3..R6
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x400;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"val=%d");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, 0u64).unwrap();   // va_ptr = 0 → fallback
        regs.set(3, 7u64).unwrap();   // first fallback arg
        dispatch(LibcSyscall::Vsprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "val=7");
    }

    // ── vfprintf (va_ptr path) ────────────────────────────────────────────────

    #[test]
    fn test_vfprintf_returns_char_count() {
        // vfprintf(file, "%d", va_ptr) returns count
        let (mut mem, mut regs, mut state) = setup_mem();
        let fmt    = NULL_PAGE_END + 0x100;
        let va_area= NULL_PAGE_END + 0x200;
        write_cstr(&mut mem, fmt, b"n=%d");
        mem.write_u64(va_area, 99u64).unwrap();
        regs.set(0, 0u64).unwrap();    // file (ignored)
        regs.set(1, fmt).unwrap();
        regs.set(2, va_area).unwrap();
        dispatch(LibcSyscall::Vfprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 4, "vfprintf: 'n=99' = 4 chars");
    }

    // ── malloc / free ─────────────────────────────────────────────────────────

    #[test]
    fn test_malloc_returns_nonzero() {
        let (mut mem, mut regs, mut state) = setup_mem_with_heap();
        regs.set(0, 64u64).unwrap();   // size
        dispatch(LibcSyscall::Malloc as u16, &mut mem, &mut regs, &mut state).unwrap();
        let ptr = regs.get(0).unwrap();
        assert_ne!(ptr, 0, "malloc must return non-null for size > 0");
        assert!(ptr >= crate::memory::HEAP_BASE, "malloc returns heap address");
    }

    #[test]
    fn test_malloc_zero_fills() {
        let (mut mem, mut regs, mut state) = setup_mem_with_heap();
        regs.set(0, 16u64).unwrap();
        dispatch(LibcSyscall::Malloc as u16, &mut mem, &mut regs, &mut state).unwrap();
        let ptr = regs.get(0).unwrap();
        for i in 0..16u64 {
            assert_eq!(mem.read_u8(ptr + i).unwrap(), 0,
                "malloc must zero-fill (byte {i} at 0x{ptr:X}+{i})");
        }
    }

    #[test]
    fn test_malloc_size_zero_returns_null() {
        let (mut mem, mut regs, mut state) = setup_mem_with_heap();
        regs.set(0, 0u64).unwrap();
        dispatch(LibcSyscall::Malloc as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 0, "malloc(0) must return null");
    }

    #[test]
    fn test_malloc_two_calls_give_different_ptrs() {
        let (mut mem, mut regs, mut state) = setup_mem_with_heap();
        regs.set(0, 32u64).unwrap();
        dispatch(LibcSyscall::Malloc as u16, &mut mem, &mut regs, &mut state).unwrap();
        let p1 = regs.get(0).unwrap();
        regs.set(0, 32u64).unwrap();
        dispatch(LibcSyscall::Malloc as u16, &mut mem, &mut regs, &mut state).unwrap();
        let p2 = regs.get(0).unwrap();
        assert_ne!(p1, p2, "two malloc calls must return different pointers");
        assert!(p2 >= p1 + 32, "allocations must not overlap");
    }

    #[test]
    fn test_free_is_noop() {
        // free() is a no-op (bump allocator) — should not crash
        let (mut mem, mut regs, mut state) = setup_mem();
        regs.set(0, 0x1234u64).unwrap();
        dispatch(LibcSyscall::Free as u16, &mut mem, &mut regs, &mut state).unwrap();
        // No assertion needed — just ensure it doesn't panic
    }

    // ── puts ──────────────────────────────────────────────────────────────────

    #[test]
    fn test_puts_returns_length_plus_newline() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let ptr = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, ptr, b"hi");
        regs.set(0, ptr).unwrap();
        dispatch(LibcSyscall::Puts as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 3, "puts('hi') = 3 (2 chars + newline)");
    }

    // ── format_printf edge cases ──────────────────────────────────────────────

    #[test]
    fn test_format_printf_empty_string() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x300;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(regs.get(0).unwrap(), 0);
        assert_eq!(mem.read_u8(buf).unwrap(), 0, "empty fmt → just null terminator");
    }

    #[test]
    fn test_format_printf_percent_p() {
        let (mut mem, mut regs, mut state) = setup_mem();
        let buf = NULL_PAGE_END + 0x300;
        let fmt = NULL_PAGE_END + 0x100;
        write_cstr(&mut mem, fmt, b"%p");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, 0x1234u64).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        let result = read_cstr(&mem, buf);
        assert!(result.starts_with("0x"), "%%p must start with 0x: got '{result}'");
        assert!(result.contains("1234"), "%%p must contain address: got '{result}'");
    }

    #[test]
    fn test_sprintf_does_not_clobber_adjacent_memory() {
        // Verify sprintf writes ONLY to buf, not to nearby addresses
        let (mut mem, mut regs, mut state) = setup_mem();
        let guard_before = NULL_PAGE_END + 0x0F8;
        let buf          = NULL_PAGE_END + 0x100;  // 8 bytes after guard
        let guard_after  = NULL_PAGE_END + 0x110;  // 16 bytes after buf
        let fmt          = NULL_PAGE_END + 0x200;
        // Poison guards
        for i in 0..8u64 {
            mem.write_u8(guard_before + i, 0xCC).unwrap();
            mem.write_u8(guard_after  + i, 0xCC).unwrap();
        }
        write_cstr(&mut mem, fmt, b"%d");
        regs.set(0, buf).unwrap();
        regs.set(1, fmt).unwrap();
        regs.set(2, 42u64).unwrap();
        dispatch(LibcSyscall::Sprintf as u16, &mut mem, &mut regs, &mut state).unwrap();
        assert_eq!(read_cstr(&mem, buf), "42");
        // Guards must be untouched
        for i in 0..8u64 {
            assert_eq!(mem.read_u8(guard_before + i).unwrap(), 0xCC,
                "guard before buf clobbered at byte {i}");
            assert_eq!(mem.read_u8(guard_after  + i).unwrap(), 0xCC,
                "guard after buf clobbered at byte {i}");
        }
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
