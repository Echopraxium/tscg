// triskele-vm/src/lib.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.1

pub mod cpu;
pub mod memory;
pub mod ffi;
pub mod io;
pub mod libc;

pub use cpu::Cpu;
pub use memory::Memory;
pub use ffi::sdl2::Sdl2Context;

/// Factory: create a Cpu, inject tsk-libc stubs, optionally attach SDL2.
pub fn build_cpu(
    mut mem:   Memory,
    entry_pc:  u64,
    debug:     bool,
    trace:     bool,
    sdl_dim:   Option<&str>,
    title:     &str,
) -> anyhow::Result<Cpu> {
    // Inject tsk-libc stubs into the libc segment (0xE000_0000)
    libc::inject_stubs(&mut mem)?;

    let mut cpu = Cpu::new(mem, entry_pc, debug);
    cpu.trace = trace;

    if let Some(dim) = sdl_dim {
        let (w, h) = parse_dim(dim);
        let sdl = Sdl2Context::init(title, w, h)?;
        cpu.sdl = Some(sdl);
    }

    Ok(cpu)
}

fn parse_dim(s: &str) -> (u32, u32) {
    if let Some((w, h)) = s.split_once('x').or_else(|| s.split_once('X')) {
        (w.parse().unwrap_or(320), h.parse().unwrap_or(200))
    } else { (320, 200) }
}
