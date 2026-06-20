// triskele-vm/src/lib.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11

pub mod cpu;
pub mod memory;
pub mod display;
pub mod io;
pub mod libc;

#[cfg(feature = "native")]
pub mod ffi;
#[cfg(feature = "native")]
pub mod wolf3d;

pub use cpu::Cpu;
pub use memory::Memory;
pub use display::DisplayBackend;

#[cfg(feature = "native")]
pub use ffi::sdl2::Sdl2Context;

/// Factory: create a Cpu, inject tsk-libc stubs, optionally attach SDL2.
/// Only available on native builds (SDL2 not available in WASM).
#[cfg(feature = "native")]
pub fn build_cpu(
    mut mem:   Memory,
    entry_pc:  u64,
    debug:     bool,
    trace:     bool,
    sdl_dim:   Option<&str>,
    title:     &str,
) -> anyhow::Result<Cpu> {
    libc::inject_stubs(&mut mem)?;

    let mut cpu = Cpu::new(mem, entry_pc, debug);
    cpu.trace = trace;

    if let Some(dim) = sdl_dim {
        let (w, h) = parse_dim(dim);
        let sdl = Sdl2Context::init(title, w, h)?;
        cpu.display = Some(Box::new(sdl));
    }

    Ok(cpu)
}

/// Load a .tvmx binary into a freshly-allocated Memory, return (Memory, entry_pc, stack_top).
/// Available on all targets (native and WASM) — no SDL2 or std::fs dependency.
/// `mem_size`: override total memory size. Pass None for native default (~2 GB),
/// or Some(small) for WASM (e.g. 8*1024*1024 = 8 MB) to avoid OOM.
pub fn load_tvmx(tvm: &triskele_common::tvm::TvmFile, mem_size: Option<u64>)
    -> anyhow::Result<(Memory, u64, u64)>
{
    use triskele_common::tvm::SectionType;
    use triskele_common::isa::Opcode;
    use crate::memory::{NULL_PAGE_END, HEAP_BASE, HEAP_SIZE, STACK_TOP, STACK_SIZE};
    use crate::libc::{LIBC_BASE, ALL_SYSCALLS, STUB_SIZE};

    let total = mem_size.unwrap_or(HEAP_BASE + HEAP_SIZE - NULL_PAGE_END);

    // Stack top: either the native STACK_TOP (0x7000_0000) if it fits,
    // or 3/4 of the total memory (leaving 1/4 for heap above the code).
    let actual_stack_top = if STACK_TOP < NULL_PAGE_END + total {
        STACK_TOP
    } else {
        NULL_PAGE_END + (total * 3 / 4)
    };

    let mut mem = Memory::new(NULL_PAGE_END, total);

    let max_id = ALL_SYSCALLS.iter().map(|sc| *sc as u64).max().unwrap_or(0);
    let libc_size = (max_id + 2) * STUB_SIZE;
    mem.add_segment(LIBC_BASE, libc_size);

    let mut load_ptr = NULL_PAGE_END;

    if let Some(rodata) = tvm.find_section(SectionType::Rodata) {
        if !rodata.data.is_empty() {
            mem.write_bytes(load_ptr, &rodata.data)
                .map_err(|e| anyhow::anyhow!("{}", e))?;
            load_ptr += ((rodata.data.len() as u64) + 3) & !3;
        }
    }

    let code = tvm.find_section(SectionType::Code)
        .ok_or_else(|| anyhow::anyhow!("no .code section"))?;
    mem.write_bytes(load_ptr, &code.data)
        .map_err(|e| anyhow::anyhow!("{}", e))?;

    let mut data_ptr = load_ptr + ((code.data.len() as u64 + 3) & !3);
    if let Some(data_sec) = tvm.find_section(SectionType::Data) {
        if !data_sec.data.is_empty() {
            mem.write_bytes(data_ptr, &data_sec.data)
                .map_err(|e| anyhow::anyhow!("{}", e))?;
            data_ptr += data_sec.data.len() as u64;
        }
    }

    // Entry stub: F_CALL → real_entry, Im_EXIT
    let real_entry = load_ptr + tvm.entry_offset() as u64;
    let stub_base  = (data_ptr + 3) & !3;
    let call_offset = real_entry as i64 - stub_base as i64;
    let f_call  = ((Opcode::F_Call  as u32) << 24) | ((call_offset as u32) & 0x00FF_FFFF);
    let im_exit = (Opcode::Im_Exit  as u32) << 24;
    mem.write_u32(stub_base,     f_call).map_err(|e| anyhow::anyhow!("{}", e))?;
    mem.write_u32(stub_base + 4, im_exit).map_err(|e| anyhow::anyhow!("{}", e))?;

    Ok((mem, stub_base, actual_stack_top))
}

/// Factory for headless builds (WASM, tests) — no SDL2, no std::fs.
/// Available on all targets.
/// `stack_top`: initial stack pointer. Use STACK_TOP constant for native,
/// or the value returned by load_tvmx() for WASM (adapted to memory size).
pub fn build_cpu_headless(
    mut mem:   Memory,
    entry_pc:  u64,
    stack_top: u64,
    debug:     bool,
) -> anyhow::Result<Cpu> {
    libc::inject_stubs(&mut mem)?;
    let cpu = Cpu::new_with_stack(mem, entry_pc, stack_top, debug);
    Ok(cpu)
}

#[cfg(feature = "native")]
fn parse_dim(s: &str) -> (u32, u32) {
    if let Some((w, h)) = s.split_once('x').or_else(|| s.split_once('X')) {
        (w.parse().unwrap_or(320), h.parse().unwrap_or(200))
    } else { (320, 200) }
}
