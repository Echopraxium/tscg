// triskele-vm/src/main.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0

use clap::Parser;
use std::path::PathBuf;
use std::process;
use triskele_common::tvm::{TvmFile, SectionType};
use triskele_vm::memory::{Memory, NULL_PAGE_END, HEAP_BASE, HEAP_SIZE};

#[derive(Parser, Debug)]
#[clap(name = "tskvm", version = "0.3.0", about = "TriskeleVM — Triskele bytecode interpreter")]
struct Args {
    program: PathBuf,
    #[clap(long)] debug: bool,
    #[clap(long)] trace: bool,
    #[clap(long, value_name = "WxH")] sdl: Option<String>,
    #[clap(long, default_value = "TriskeleVM")] title: String,

}

fn main() {
    env_logger::init();
    let args = Args::parse();



    let tvm = match TvmFile::load_from_file(args.program.to_str().unwrap()) {
        Ok(t) => t,
        Err(e) => { eprintln!("[tskvm] error: {}", e); process::exit(1); }
    };

    let total = HEAP_BASE + HEAP_SIZE - NULL_PAGE_END;
    let mut mem = Memory::new(NULL_PAGE_END, total);

    // Add libc segment at 0xE000_0000 (tsk-libc stubs injected by build_cpu)
    use triskele_vm::libc::{LIBC_BASE, ALL_SYSCALLS, STUB_SIZE};
    // Taille = (max_syscall_id + 1) * STUB_SIZE  — les adresses sont LIBC_BASE + id * STUB_SIZE
    let max_id = ALL_SYSCALLS.iter().map(|sc| *sc as u64).max().unwrap_or(0);
    let libc_size = (max_id + 2) * STUB_SIZE;  // +2 pour marge
    mem.add_segment(LIBC_BASE, libc_size);
    let mut load_ptr = NULL_PAGE_END;

    if let Some(rodata) = tvm.find_section(SectionType::Rodata) {
        if !rodata.data.is_empty() {
            mem.write_bytes(load_ptr, &rodata.data).expect("rodata");
            load_ptr += ((rodata.data.len() as u64) + 3) & !3;
        }
    }

    let code = match tvm.find_section(SectionType::Code) {
        Some(s) => s,
        None => { eprintln!("[tskvm] no .code section"); process::exit(1); }
    };
    mem.write_bytes(load_ptr, &code.data).expect("code");

    // Also load Data section (globals like @tilemap) after code
    let mut data_ptr = load_ptr + ((code.data.len() as u64 + 7) & !7);
    if let Some(data_sec) = tvm.find_section(SectionType::Data) {
        if !data_sec.data.is_empty() {
            mem.write_bytes(data_ptr, &data_sec.data).expect("data");
            data_ptr += data_sec.data.len() as u64;
        }
    }

    // Prepend a call stub so F_RET has a valid return address:
    //   F_CALL  → entry function
    //   Im_EXIT → exit with R0
    // Stub is placed just before the code section (at load_ptr - 8).
    // entry_pc points to this stub; the real entry is called from it.
    use triskele_common::isa::Opcode;
    let real_entry = load_ptr + tvm.entry_offset() as u64;
    // Stub layout at stub_base:
    //   [0] F_CALL +8           (jump forward 8 = call real_entry which is 8 bytes ahead)
    //   [4] Im_EXIT             (exit with code in R0)
    // stub_base = real_entry - 8  but we need space before code.
    // Simpler: append stub after code+data and set entry_pc to stub.
    let stub_base = data_ptr;
    let stub_base = (stub_base + 3) & !3;  // align to 4

    // F_CALL offset: target = stub_base + offset, target = real_entry
    // offset = real_entry - stub_base
    let call_offset = real_entry as i64 - stub_base as i64;
    let f_call = ((Opcode::F_Call as u32) << 24)
        | ((call_offset as u32) & 0x00FF_FFFF);
    let im_exit = (Opcode::Im_Exit as u32) << 24;

    mem.write_u32(stub_base,     f_call).expect("stub F_CALL");
    mem.write_u32(stub_base + 4, im_exit).expect("stub Im_EXIT");

    let entry_pc = stub_base;

    // Build CPU — attach SDL2 if requested
    let cpu = triskele_vm::build_cpu(mem, entry_pc, args.debug, args.trace, args.sdl.as_deref(), &args.title);

    let mut cpu = match cpu {
        Ok(c) => c,
        Err(e) => { eprintln!("[tskvm] init error: {}", e); process::exit(1); }
    };

    match cpu.run() {
        Ok(code) => { if args.debug { eprintln!("[tskvm] exit {}", code); } process::exit(code); }
        Err(e)   => { eprintln!("[tskvm] error: {}", e); if args.debug { cpu.regs.dump(); } process::exit(1); }
    }
}
