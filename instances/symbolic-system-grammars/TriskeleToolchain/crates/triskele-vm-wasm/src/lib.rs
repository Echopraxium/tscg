// triskele-vm-wasm/src/lib.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11
//
// WASM entry point for TriskeleVM — Hello World spike.
// Validates: VM compiles to wasm32, DisplayBackend implementable without SDL2,
// printf() output routed to the browser console and returned to JS.

use wasm_bindgen::prelude::*;
use std::io::Write;
use std::sync::{Arc, Mutex};
use triskele_vm::{Cpu, DisplayBackend, build_cpu_headless, load_tvmx};
use triskele_common::{tvm::TvmFile, error::VmError};

// ─────────────────────────────────────────────────────────────────────────────
// Console helper
// ─────────────────────────────────────────────────────────────────────────────

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

macro_rules! console_log {
    ($($t:tt)*) => (log(&format_args!($($t)*).to_string()))
}

// ─────────────────────────────────────────────────────────────────────────────
// WasmBackend — DisplayBackend with no-op display, console.log for debugging
// ─────────────────────────────────────────────────────────────────────────────

struct WasmBackend;

impl DisplayBackend for WasmBackend {
    fn fb_blit(&mut self, _mem: &triskele_vm::Memory, _fb_ptr: u64)
        -> anyhow::Result<()> { Ok(()) }
    fn fb_blit_pixels(&mut self, _pixels: &[u8], _w: u32, _h: u32)
        -> anyhow::Result<()> { Ok(()) }
    fn fb_clear(&mut self, _mem: &mut triskele_vm::Memory, _fb_ptr: u64, _color: u32)
        -> anyhow::Result<()> { Ok(()) }
    fn poll_events(&mut self) -> bool { false }
    fn register_callback(&mut self, _id: u32, _addr: u64) {}
    fn key_query(&self, _sc: u8) -> u64 { 0 }
    fn frame_sync(&mut self, _fps: u32) {}
    fn width(&self)  -> u32 { 320 }
    fn height(&self) -> u32 { 200 }
}

// ─────────────────────────────────────────────────────────────────────────────
// Output writer — Arc<Mutex<Vec<u8>>> so we can recover after cpu.run()
// ─────────────────────────────────────────────────────────────────────────────

struct ArcWriter(Arc<Mutex<Vec<u8>>>);

impl Write for ArcWriter {
    fn write(&mut self, data: &[u8]) -> std::io::Result<usize> {
        self.0.lock().unwrap().extend_from_slice(data);
        Ok(data.len())
    }
    fn flush(&mut self) -> std::io::Result<()> { Ok(()) }
}

// SAFETY: WASM is single-threaded; Arc<Mutex> is technically Send already,
// but the inner Vec<u8> definitely is — this is fine.
unsafe impl Send for ArcWriter {}

// ─────────────────────────────────────────────────────────────────────────────
// Public API
// ─────────────────────────────────────────────────────────────────────────────

/// Run a .tvmx binary (passed as Uint8Array from JS).
/// Returns the captured stdout output (printf etc.) as a String.
#[wasm_bindgen]
pub fn run_tvmx(tvmx_bytes: &[u8]) -> String {
    console_log!("[TriskeleVM WASM] run_tvmx: {} bytes", tvmx_bytes.len());

    // 1. Parse .tvmx
    let tvm = match TvmFile::load_from_bytes(tvmx_bytes) {
        Ok(t)  => t,
        Err(e) => return format!("Error loading .tvmx: {}", e),
    };

    // 2. Load into memory + get entry PC + adapted stack top
    // Use 8 MB — enough for Hello World, avoids OOM in WASM
    // (native default is ~2 GB which crashes the WASM runtime)
    let (mem, entry_pc, stack_top) = match load_tvmx(&tvm, Some(8 * 1024 * 1024)) {
        Ok(r)  => r,
        Err(e) => return format!("Error loading sections: {}", e),
    };

    // 3. Build headless CPU (no SDL2), with adapted stack pointer
    let mut cpu = match build_cpu_headless(mem, entry_pc, stack_top, false) {
        Ok(c)  => c,
        Err(e) => return format!("Error building CPU: {}", e),
    };

    // 4. Attach no-op display backend
    cpu.display = Some(Box::new(WasmBackend));

    // 5. Capture stdout into a shared buffer
    let buf: Arc<Mutex<Vec<u8>>> = Arc::new(Mutex::new(Vec::new()));
    cpu.output = Box::new(ArcWriter(Arc::clone(&buf)));

    // 6. Run
    let exit_code = match cpu.run() {
        Ok(code)                   => code,
        Err(VmError::Halted(code)) => code,
        Err(e) => {
            let msg = format!("VM error: {}", e);
            console_log!("{}", msg);
            return msg;
        }
    };

    // 7. Return captured output + exit code
    let output = {
        let raw = buf.lock().unwrap();
        String::from_utf8_lossy(&raw).to_string()
    };

    console_log!("[TriskeleVM WASM] exit={} output={:?}", exit_code, output);
    format!("Exit: {}\n{}", exit_code, output)
}
