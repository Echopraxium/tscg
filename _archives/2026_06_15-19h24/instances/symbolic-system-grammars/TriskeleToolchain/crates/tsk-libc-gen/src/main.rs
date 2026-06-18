// tsk-libc-gen/src/main.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.1
//
// Generates tsk-libc.tvml — pure TriskeleVM library for C89 standard functions.
//
// Usage:
//   cargo run -p tsk-libc-gen -- -o lib/tsk-libc.tvml
//
// Output format: .tvml with flags IS_LIBRARY
//   .code    — Im_Syscall <id> + F_Ret stubs for each libc function
//   .symtab  — "memset" → stub_addr, "sin" → stub_addr, ...
//
// The stub addresses are relative to the .code section base.
// tsk-link resolves calls to @memset, @sin etc. from these symbols.

use clap::Parser;
use std::path::PathBuf;
use anyhow::Result;
use triskele_common::tvm::{TvmBuilder, SectionType, file_flags};
use triskele_common::isa::Opcode;

// ── Libc function table ───────────────────────────────────────────────────────

/// One libc function entry.
struct LibcFn {
    /// C symbol name (as in LLVM IR: @memset, @sin, ...)
    name:       &'static str,
    /// Syscall dispatch ID — must match LibcSyscall in triskele-vm/src/libc/mod.rs
    syscall_id: u16,
}

/// Complete list of supported libc functions.
/// IDs must stay in sync with triskele_vm::libc::LibcSyscall.
const LIBC_FUNCTIONS: &[LibcFn] = &[
    // Memory
    LibcFn { name: "memset",  syscall_id: 0x01 },
    LibcFn { name: "memcpy",  syscall_id: 0x02 },
    LibcFn { name: "memmove", syscall_id: 0x03 },
    LibcFn { name: "memcmp",  syscall_id: 0x04 },
    // String
    LibcFn { name: "strlen",  syscall_id: 0x10 },
    LibcFn { name: "strcpy",  syscall_id: 0x11 },
    LibcFn { name: "strncpy", syscall_id: 0x12 },
    LibcFn { name: "strcmp",  syscall_id: 0x13 },
    LibcFn { name: "strncmp", syscall_id: 0x14 },
    LibcFn { name: "strchr",  syscall_id: 0x15 },
    // Math
    LibcFn { name: "sin",     syscall_id: 0x20 },
    LibcFn { name: "cos",     syscall_id: 0x21 },
    LibcFn { name: "tan",     syscall_id: 0x22 },
    LibcFn { name: "atan",    syscall_id: 0x23 },
    LibcFn { name: "atan2",   syscall_id: 0x24 },
    LibcFn { name: "sqrt",    syscall_id: 0x25 },
    LibcFn { name: "fabs",    syscall_id: 0x26 },
    LibcFn { name: "floor",   syscall_id: 0x27 },
    LibcFn { name: "ceil",    syscall_id: 0x28 },
    // Stdlib
    LibcFn { name: "abs",     syscall_id: 0x30 },
    LibcFn { name: "rand",    syscall_id: 0x31 },
    LibcFn { name: "srand",   syscall_id: 0x32 },
    // I/O (debug stub)
    LibcFn { name: "printf",  syscall_id: 0x40 },
];

// ── Stub size ─────────────────────────────────────────────────────────────────

/// Each stub: Im_Syscall(4) + F_Ret(4) = 8 bytes.
const STUB_BYTES: u32 = 8;

// ── CLI ───────────────────────────────────────────────────────────────────────

#[derive(Parser, Debug)]
#[clap(
    name    = "tsk-libc-gen",
    version = "0.3.1",
    about   = "Generate tsk-libc.tvml — C89 standard library for TriskeleVM"
)]
struct Args {
    #[clap(short, long, default_value = "tsk-libc.tvml")]
    output: PathBuf,

    #[clap(long, help = "Print symbol table to stdout")]
    dump: bool,
}

// ── Instruction encoding (mirrors triskele-common) ───────────────────────────

/// Encode Type I instruction: opcode(8) | dst(5) | imm19(19)
fn enc_i(op: Opcode, dst: u8, imm: i32) -> u32 {
    ((op as u32) << 24)
        | ((dst as u32 & 0x1F) << 19)
        | (imm as u32 & 0x0007_FFFF)
}

/// Encode Type R instruction (no-arg variant for F_Ret)
fn enc_r_nop(op: Opcode) -> u32 {
    (op as u32) << 24
}

// ── Main ──────────────────────────────────────────────────────────────────────

fn main() -> Result<()> {
    let args = Args::parse();

    // ── 1. Generate .code section (stubs) ────────────────────────────────────
    let mut code: Vec<u8> = Vec::new();
    let mut symtab: Vec<u8> = Vec::new();   // null-terminated name + u32 offset pairs

    for (idx, func) in LIBC_FUNCTIONS.iter().enumerate() {
        let offset = (idx as u32) * STUB_BYTES;

        // Stub:  Im_Syscall <syscall_id>   (Type I, dst=0, imm=syscall_id)
        let im_syscall = enc_i(Opcode::Im_Syscall, 0, func.syscall_id as i32);
        code.extend_from_slice(&im_syscall.to_le_bytes());

        // Stub:  F_Ret                     (Type R, no operands)
        let f_ret = enc_r_nop(Opcode::F_Ret);
        code.extend_from_slice(&f_ret.to_le_bytes());

        // Symbol table entry: null-terminated name + u32 LE offset
        symtab.extend_from_slice(func.name.as_bytes());
        symtab.push(0);
        symtab.extend_from_slice(&offset.to_le_bytes());

        if args.dump {
            println!("  [{:#06x}] {:12} → offset +{:#06x}  Im_Syscall({:#06x}) + F_Ret",
                func.syscall_id, func.name, offset, func.syscall_id);
        }
    }

    // ── 2. Build .tvml file ───────────────────────────────────────────────────
    let tvml = TvmBuilder::new()
        .with_flags(file_flags::IS_LIBRARY | file_flags::HAS_SYMBOL_TABLE)
        .add_section(SectionType::Code,   0x02, code)    // 0x02 = EXECUTABLE
        .add_section(SectionType::Symtab, 0x00, symtab)
        .build();

    std::fs::write(&args.output, &tvml)?;

    println!(
        "[tsk-libc-gen] {} functions → {} bytes → {}",
        LIBC_FUNCTIONS.len(),
        tvml.len(),
        args.output.display()
    );

    Ok(())
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use triskele_common::tvm::{TvmFile, SectionType, file_flags};

    fn generate_tvml() -> Vec<u8> {
        let mut code: Vec<u8> = Vec::new();
        let mut symtab: Vec<u8> = Vec::new();
        for (idx, func) in LIBC_FUNCTIONS.iter().enumerate() {
            let offset = (idx as u32) * STUB_BYTES;
            code.extend_from_slice(&enc_i(Opcode::Im_Syscall, 0, func.syscall_id as i32).to_le_bytes());
            code.extend_from_slice(&enc_r_nop(Opcode::F_Ret).to_le_bytes());
            symtab.extend_from_slice(func.name.as_bytes());
            symtab.push(0);
            symtab.extend_from_slice(&offset.to_le_bytes());
        }
        TvmBuilder::new()
            .with_flags(file_flags::IS_LIBRARY | file_flags::HAS_SYMBOL_TABLE)
            .add_section(SectionType::Code,   0x02, code)
            .add_section(SectionType::Symtab, 0x00, symtab)
            .build()
    }

    #[test]
    fn test_tvml_is_library() {
        let tvml = generate_tvml();
        let tvm = TvmFile::load_from_bytes(&tvml).unwrap();
        assert!(tvm.is_library(), ".tvml must have IS_LIBRARY flag");
        assert!(!tvm.is_native(), ".tvml pure must NOT have IS_NATIVE flag");
    }

    #[test]
    fn test_code_section_present() {
        let tvml = generate_tvml();
        let tvm = TvmFile::load_from_bytes(&tvml).unwrap();
        let code = tvm.find_section(SectionType::Code).expect(".code section missing");
        // Each function = 2 instructions × 4 bytes
        assert_eq!(code.data.len(), LIBC_FUNCTIONS.len() * STUB_BYTES as usize);
    }

    #[test]
    fn test_symtab_contains_memset() {
        let tvml = generate_tvml();
        let tvm = TvmFile::load_from_bytes(&tvml).unwrap();
        let sym = tvm.find_section(SectionType::Symtab).expect("symtab missing");
        // Check "memset\0" appears in the raw symtab bytes
        let symtab_str = sym.data.windows(7)
            .any(|w| w == b"memset\0");
        assert!(symtab_str, "symtab must contain 'memset'");
    }

    #[test]
    fn test_stub_encoding_memset() {
        // memset is index 0 → offset 0
        // Im_Syscall(0x90), dst=0, imm=0x01 (memset syscall id)
        let tvml = generate_tvml();
        let tvm = TvmFile::load_from_bytes(&tvml).unwrap();
        let code = tvm.find_section(SectionType::Code).unwrap();
        let word = u32::from_le_bytes(code.data[0..4].try_into().unwrap());
        let opcode_byte = (word >> 24) as u8;
        let imm = word & 0x0007_FFFF;
        assert_eq!(opcode_byte, Opcode::Im_Syscall as u8,
            "first instruction must be Im_Syscall");
        assert_eq!(imm, 0x01, "memset syscall id must be 0x01");
    }

    #[test]
    fn test_stub_f_ret_after_syscall() {
        // Second word of stub must be F_Ret
        let tvml = generate_tvml();
        let tvm = TvmFile::load_from_bytes(&tvml).unwrap();
        let code = tvm.find_section(SectionType::Code).unwrap();
        let word = u32::from_le_bytes(code.data[4..8].try_into().unwrap());
        let opcode_byte = (word >> 24) as u8;
        assert_eq!(opcode_byte, Opcode::F_Ret as u8,
            "second instruction of every stub must be F_Ret");
    }

    #[test]
    fn test_all_functions_have_unique_ids() {
        let mut ids: Vec<u16> = LIBC_FUNCTIONS.iter().map(|f| f.syscall_id).collect();
        let before = ids.len();
        ids.sort();
        ids.dedup();
        assert_eq!(ids.len(), before, "all syscall IDs must be unique");
    }

    #[test]
    fn test_all_functions_have_unique_names() {
        let mut names: Vec<&str> = LIBC_FUNCTIONS.iter().map(|f| f.name).collect();
        let before = names.len();
        names.sort();
        names.dedup();
        assert_eq!(names.len(), before, "all function names must be unique");
    }
}
