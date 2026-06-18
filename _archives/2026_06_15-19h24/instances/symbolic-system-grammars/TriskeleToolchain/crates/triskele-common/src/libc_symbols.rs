// triskele-common/src/libc_symbols.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11
//
// tsk-libc symbol table — shared between tsk-link (symbol resolution) and
// triskele-vm (stub injection).
//
// Address layout:  LIBC_BASE + syscall_id * STUB_SIZE
//   LIBC_BASE  = 0xE000_0000
//   STUB_SIZE  = 8  (2 instructions: Im_Syscall(id) + F_Ret)
//
// IDs MUST stay in sync with LibcSyscall enum in triskele-vm/libc/mod.rs.

pub const LIBC_BASE:  u64 = 0xE000_0000;
pub const STUB_SIZE:  u64 = 8;

/// One entry in the libc symbol table.
pub struct LibcSym {
    pub name: &'static str,
    pub id:   u16,
}

impl LibcSym {
    pub const fn stub_addr(&self) -> u64 {
        LIBC_BASE + self.id as u64 * STUB_SIZE
    }
}

/// Complete table of all tsk-libc symbols.
/// Must stay in sync with LibcSyscall enum in triskele-vm/libc/mod.rs.
pub const LIBC_SYMBOLS: &[LibcSym] = &[
    // ── Memory ──────────────────────────────────────────────────
    LibcSym { name: "memset",        id: 0x01 },
    LibcSym { name: "memcpy",        id: 0x02 },
    LibcSym { name: "memmove",       id: 0x03 },
    LibcSym { name: "memcmp",        id: 0x04 },
    // ── String ──────────────────────────────────────────────────
    LibcSym { name: "strlen",        id: 0x10 },
    LibcSym { name: "strcpy",        id: 0x11 },
    LibcSym { name: "strncpy",       id: 0x12 },
    LibcSym { name: "strcmp",        id: 0x13 },
    LibcSym { name: "strncmp",       id: 0x14 },
    LibcSym { name: "strchr",        id: 0x15 },
    LibcSym { name: "strrchr",       id: 0x16 },
    LibcSym { name: "strstr",        id: 0x17 },
    LibcSym { name: "strdup",        id: 0x18 },
    LibcSym { name: "strcasecmp",    id: 0x19 },
    LibcSym { name: "strncasecmp",   id: 0x1A },
    // MSVC aliases — clang on Windows emits _stricmp / _strnicmp
    LibcSym { name: "_stricmp",      id: 0x19 },  // alias for strcasecmp
    LibcSym { name: "_strnicmp",     id: 0x1A },  // alias for strncasecmp
    LibcSym { name: "strlcat",       id: 0x1B },
    LibcSym { name: "strlcpy",       id: 0x1C },
    // ── Stdlib ──────────────────────────────────────────────────
    LibcSym { name: "abs",           id: 0x30 },
    LibcSym { name: "rand",          id: 0x31 },
    LibcSym { name: "srand",         id: 0x32 },
    LibcSym { name: "malloc",        id: 0x33 },
    LibcSym { name: "free",          id: 0x34 },
    LibcSym { name: "exit",          id: 0x35 },
    LibcSym { name: "atoi",          id: 0x36 },
    LibcSym { name: "strtol",        id: 0x37 },
    // ── I/O ─────────────────────────────────────────────────────
    LibcSym { name: "printf",        id: 0x40 },
    LibcSym { name: "fprintf",       id: 0x41 },
    LibcSym { name: "vfprintf",      id: 0x42 },
    LibcSym { name: "sprintf",       id: 0x43 },
    LibcSym { name: "puts",          id: 0x44 },
    LibcSym { name: "vsprintf",      id: 0x45 },
    LibcSym { name: "snprintf",      id: 0x46 },
    LibcSym { name: "vsnprintf",     id: 0x47 },
    // ── Ctype ────────────────────────────────────────────────────
    LibcSym { name: "toupper",       id: 0x50 },
    LibcSym { name: "tolower",       id: 0x51 },
    LibcSym { name: "isspace",       id: 0x52 },
    LibcSym { name: "isdigit",       id: 0x53 },
    LibcSym { name: "isalpha",       id: 0x54 },
    LibcSym { name: "isprint",       id: 0x55 },
    // ── File I/O ─────────────────────────────────────────────────
    LibcSym { name: "fopen",         id: 0x60 },
    LibcSym { name: "fclose",        id: 0x61 },
    LibcSym { name: "fread",         id: 0x62 },
    LibcSym { name: "fwrite",        id: 0x63 },
    LibcSym { name: "fseek",         id: 0x64 },
    LibcSym { name: "ftell",         id: 0x65 },
    LibcSym { name: "feof",          id: 0x66 },
    LibcSym { name: "fflush",        id: 0x67 },
    // ── String utils (Doom m_config.c) ───────────────────────────────────
    LibcSym { name: "strerror",      id: 0x68 },
    LibcSym { name: "sscanf",        id: 0x69 },
    // ── stdlib extra ─────────────────────────────────────────────────────
    LibcSym { name: "calloc",        id: 0x6A },
];

/// Look up a symbol by name. Returns its stub address if found.
pub fn libc_sym_addr(name: &str) -> Option<u64> {
    LIBC_SYMBOLS.iter()
        .find(|s| s.name == name)
        .map(|s| s.stub_addr())
}
