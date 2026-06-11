// tsk-lib-dos-gen/src/main.rs
// Génère la bibliothèque tsk-lib-dos.tvml contenant des stubs pour les fonctions DOS.

use clap::Parser;
use std::path::PathBuf;
use anyhow::Result;
use triskele_common::tvm::{TvmBuilder, SectionType, file_flags};
use triskele_common::isa::Opcode;

struct DosFn {
    name: &'static str,
    syscall_id: u16,
}

const DOS_FUNCTIONS: &[DosFn] = &[
    DosFn { name: "sound",      syscall_id: 0x80 },
    DosFn { name: "nosound",    syscall_id: 0x81 },
    DosFn { name: "delay",      syscall_id: 0x82 },
    DosFn { name: "kbhit",      syscall_id: 0x83 },
    DosFn { name: "getch",      syscall_id: 0x84 },
    DosFn { name: "intr",       syscall_id: 0x85 },
    DosFn { name: "set_video_mode", syscall_id: 0x86 },
];

const STUB_BYTES: u32 = 8;  // Im_Syscall + F_Ret

fn enc_i(op: Opcode, dst: u8, imm: i32) -> u32 {
    ((op as u32) << 24) | ((dst as u32 & 0x1F) << 19) | (imm as u32 & 0x0007_FFFF)
}

fn enc_r_nop(op: Opcode) -> u32 {
    (op as u32) << 24
}

#[derive(Parser, Debug)]
#[clap(name = "tsk-lib-dos-gen", version = "0.1.0", about = "Generate tsk-lib-dos.tvml")]
struct Args {
    #[clap(short, long, default_value = "tsk-lib-dos.tvml")]
    output: PathBuf,
    #[clap(long)]
    dump: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let mut code = Vec::new();
    let mut symtab = Vec::new();

    for (idx, func) in DOS_FUNCTIONS.iter().enumerate() {
        let offset = (idx as u32) * STUB_BYTES;
        code.extend_from_slice(&enc_i(Opcode::Im_Syscall, 0, func.syscall_id as i32).to_le_bytes());
        code.extend_from_slice(&enc_r_nop(Opcode::F_Ret).to_le_bytes());

        symtab.extend_from_slice(func.name.as_bytes());
        symtab.push(0);
        symtab.extend_from_slice(&offset.to_le_bytes());

        if args.dump {
            println!("  {:#04x} {:16} offset {:#04x}", func.syscall_id, func.name, offset);
        }
    }

    let tvml = TvmBuilder::new()
        .with_flags(file_flags::IS_LIBRARY | file_flags::HAS_SYMBOL_TABLE)
        .add_section(SectionType::Code, 0x02, code)
        .add_section(SectionType::Symtab, 0x00, symtab)
        .build();

    std::fs::write(&args.output, &tvml)?;
    println!("Generated {} functions -> {} bytes -> {}", DOS_FUNCTIONS.len(), tvml.len(), args.output.display());
    Ok(())
}