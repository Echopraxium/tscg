// triskele-vm-wasm/src/lib.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.14
//
// WASM host for TriskeleVM — interactive stdin via Web Worker + SharedArrayBuffer.
//
// Architecture (see ADR-WASM-001/002/003 in docs/adr/):
//
//   Main thread                      VM Worker
//   ─────────────────────────        ────────────────────────────────────
//   create_stdin_sab()               worker.js loads this .wasm
//   new Worker("worker.js")    →     worker_entry(tvmx_bytes, sab)
//   hub: routes postMessage   ←      SabHost::flush_to_main() / post_need_input()
//   writes SAB + notify       →      SabHost::read_line() blocks on Atomics.wait
//   <input> row on "needInput"
//
// Public WASM entry points:
//   create_stdin_sab()            — creates the SAB (main thread only)
//   run_tvmx(bytes)               — non-interactive one-shot (patch-1 preserved)
//   worker_entry(bytes, sab)      — called by worker.js; blocks on SAB stdin

use wasm_bindgen::prelude::*;
use std::sync::{Arc, Mutex};
use js_sys::{Int32Array, Uint8Array, SharedArrayBuffer};
use triskele_vm::{HostIo, HostLine, build_cpu_headless, load_tvmx};
use triskele_common::{tvm::TvmFile, error::VmError};
use triskele_vm::DisplayBackend;

// ─────────────────────────────────────────────────────────────────────────────
// Console helpers
// ─────────────────────────────────────────────────────────────────────────────

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
    #[wasm_bindgen(js_namespace = console)]
    fn error(s: &str);
}

macro_rules! console_log {
    ($($t:tt)*) => (log(&format_args!($($t)*).to_string()))
}

// ─────────────────────────────────────────────────────────────────────────────
// WasmBackend — no-op DisplayBackend (headless)
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
// ArcHost — non-interactive HostIo for run_tvmx
// ─────────────────────────────────────────────────────────────────────────────

struct ArcHost(Arc<Mutex<Vec<u8>>>);

impl HostIo for ArcHost {
    fn write_bytes(&mut self, data: &[u8]) {
        self.0.lock().unwrap().extend_from_slice(data);
    }
    fn flush(&mut self) {}
    fn read_line(&mut self) -> HostLine { HostLine::Eof }
}

unsafe impl Send for ArcHost {}

// ─────────────────────────────────────────────────────────────────────────────
// SAB layout  (ADR-WASM-002)
//   [0..4)      Int32  version = 1     (index 0)
//   [4..8)      Int32  flag            (index 1)  0=waiting 1=ready 2=EOF
//   [8..12)     Int32  len             (index 2)
//   [12..4108)  bytes  data (4096 B)
// ─────────────────────────────────────────────────────────────────────────────

const SAB_IDX_VERSION:      i32 = 0;
const SAB_IDX_FLAG:         i32 = 1;
const SAB_IDX_LEN:          i32 = 2;
const SAB_DATA_BYTE_OFFSET: u32 = 12;
const SAB_DATA_SIZE:        u32 = 4096;
pub const SAB_TOTAL_SIZE:   u32 = SAB_DATA_BYTE_OFFSET + SAB_DATA_SIZE;

const FLAG_VM_WAITING: i32 = 0;
const FLAG_LINE_READY: i32 = 1;
const FLAG_EOF:        i32 = 2;

// ─────────────────────────────────────────────────────────────────────────────
// postMessage helpers
// ─────────────────────────────────────────────────────────────────────────────

fn make_msg(type_str: &str) -> js_sys::Object {
    let obj = js_sys::Object::new();
    js_sys::Reflect::set(&obj, &"type".into(), &type_str.into()).ok();
    obj
}

fn post_to_main(msg: &js_sys::Object) {
    if let Ok(scope) = js_sys::global()
        .dyn_into::<web_sys::DedicatedWorkerGlobalScope>()
    {
        scope.post_message(msg).ok();
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// SabHost — interactive HostIo (worker side)
// ─────────────────────────────────────────────────────────────────────────────

struct SabHost {
    flag_arr: Int32Array,
    data_arr: Uint8Array,
    out_buf:  Vec<u8>,
}

impl SabHost {
    fn new(sab: &SharedArrayBuffer) -> Self {
        Self {
            flag_arr: Int32Array::new(sab),
            data_arr: Uint8Array::new_with_byte_offset_and_length(
                sab, SAB_DATA_BYTE_OFFSET, SAB_DATA_SIZE,
            ),
            out_buf: Vec::new(),
        }
    }

    fn flush_to_main(&mut self) {
        if self.out_buf.is_empty() { return; }
        let text = String::from_utf8_lossy(&self.out_buf).into_owned();
        self.out_buf.clear();
        let msg = make_msg("output");
        js_sys::Reflect::set(&msg, &"text".into(), &text.into()).ok();
        post_to_main(&msg);
    }
}

impl HostIo for SabHost {
    fn write_bytes(&mut self, data: &[u8]) {
        self.out_buf.extend_from_slice(data);
    }

    fn flush(&mut self) {
        // Flush accumulated output to the main thread immediately.
        // Called before each read_line() (via flush_to_main) and after run()
        // to ensure no output is lost when the VM halts without a final read.
        self.flush_to_main();
    }

    fn read_line(&mut self) -> HostLine {
        // 1. Send pending output to main thread before showing the prompt.
        self.flush_to_main();

        // 2. Tell main thread to show the <input> row.
        post_to_main(&make_msg("needInput"));

        // 3. Block this worker thread until main thread delivers a line.
        //    Atomics.wait() is allowed on worker threads (ADR-WASM-001).
        let _ = js_sys::Atomics::wait(
            &self.flag_arr,
            SAB_IDX_FLAG as u32,
            FLAG_VM_WAITING,   // wait while flag == 0
        );

        // 4. Read flag value.
        let flag = js_sys::Atomics::load(&self.flag_arr, SAB_IDX_FLAG as u32)
            .unwrap_or(FLAG_EOF);

        // 5. Reset flag to 0 so main thread can deliver the next line.
        let _ = js_sys::Atomics::store(
            &self.flag_arr, SAB_IDX_FLAG as u32, FLAG_VM_WAITING,
        );

        if flag == FLAG_EOF {
            return HostLine::Eof;
        }

        // 6. Read the line bytes from the SAB data region.
        let len = js_sys::Atomics::load(&self.flag_arr, SAB_IDX_LEN as u32)
            .unwrap_or(0) as usize;
        let len = len.min(SAB_DATA_SIZE as usize);
        let mut bytes = vec![0u8; len];
        self.data_arr.copy_to(&mut bytes[..len]);

        HostLine::Line(String::from_utf8_lossy(&bytes).into_owned())
    }
}

// SAFETY: WASM workers are single-threaded. js_sys typed arrays are not
// Send in general, but within a single worker thread this is safe.
unsafe impl Send for SabHost {}

// ─────────────────────────────────────────────────────────────────────────────
// Public API
// ─────────────────────────────────────────────────────────────────────────────

/// Create the stdin SAB — call this on the main thread, then transfer to the
/// worker via postMessage.
#[wasm_bindgen]
pub fn create_stdin_sab() -> SharedArrayBuffer {
    let sab = SharedArrayBuffer::new(SAB_TOTAL_SIZE);
    let arr = Int32Array::new(&sab);
    arr.set_index(SAB_IDX_VERSION as u32, 1);
    arr.set_index(SAB_IDX_FLAG    as u32, FLAG_VM_WAITING);
    sab
}

/// Non-interactive one-shot run — stdin = EOF (patch-1 behaviour preserved).
#[wasm_bindgen]
pub fn run_tvmx(tvmx_bytes: &[u8]) -> String {
    console_log!("[TriskeleVM WASM] run_tvmx: {} bytes", tvmx_bytes.len());

    let tvm = match TvmFile::load_from_bytes(tvmx_bytes) {
        Ok(t)  => t,
        Err(e) => return format!("Error loading .tvmx: {}", e),
    };
    let (mem, entry_pc, stack_top) = match load_tvmx(&tvm, Some(8 * 1024 * 1024)) {
        Ok(r)  => r,
        Err(e) => return format!("Error loading sections: {}", e),
    };
    let mut cpu = match build_cpu_headless(mem, entry_pc, stack_top, false) {
        Ok(c)  => c,
        Err(e) => return format!("Error building CPU: {}", e),
    };
    cpu.display = Some(Box::new(WasmBackend));

    let buf: Arc<Mutex<Vec<u8>>> = Arc::new(Mutex::new(Vec::new()));
    cpu.host = Box::new(ArcHost(Arc::clone(&buf)));

    let exit_code = match cpu.run() {
        Ok(code)                   => code,
        Err(VmError::Halted(code)) => code,
        Err(e) => {
            let msg = format!("VM error: {}", e);
            console_log!("{}", msg);
            return msg;
        }
    };

    let output = {
        let raw = buf.lock().unwrap();
        String::from_utf8_lossy(&raw).to_string()
    };
    console_log!("[TriskeleVM WASM] run_tvmx exit={}", exit_code);
    format!("Exit: {}\n{}", exit_code, output)
}

/// Interactive VM worker entry point — called by worker.js.
/// Receives the .tvmx bytes and the stdin SAB.
/// Sends postMessage events to the main thread hub:
///   { type: "output",   text: "…" }
///   { type: "needInput" }
///   { type: "halted",   exitCode: N }
#[wasm_bindgen]
pub fn worker_entry(tvmx_bytes: &[u8], sab: SharedArrayBuffer) {
    console_log!("[TriskeleVM worker] starting, {} bytes", tvmx_bytes.len());

    let tvm = match TvmFile::load_from_bytes(tvmx_bytes) {
        Ok(t)  => t,
        Err(e) => { error(&format!("[worker] load error: {}", e)); return; }
    };
    let (mem, entry_pc, stack_top) = match load_tvmx(&tvm, Some(8 * 1024 * 1024)) {
        Ok(r)  => r,
        Err(e) => { error(&format!("[worker] section error: {}", e)); return; }
    };
    let mut cpu = match build_cpu_headless(mem, entry_pc, stack_top, false) {
        Ok(c)  => c,
        Err(e) => { error(&format!("[worker] cpu error: {}", e)); return; }
    };
    cpu.display = Some(Box::new(WasmBackend));

    // Move SabHost into cpu.host. From here, cpu.run() drives I/O through it:
    // write_bytes() accumulates output; read_line() blocks via Atomics.wait.
    // This mirrors std::io::{stdin,stdout} on native (ADR-WASM-001).
    cpu.host = Box::new(SabHost::new(&sab));

    let exit_code = match cpu.run() {
        Ok(code)                   => code,
        Err(VmError::Halted(code)) => code,
        Err(e) => {
            error(&format!("[worker] VM error: {}", e));
            let msg = make_msg("halted");
            js_sys::Reflect::set(&msg, &"exitCode".into(), &(-1f64).into()).ok();
            post_to_main(&msg);
            return;
        }
    };

    // M2b flush fix: SabHost::flush() now calls flush_to_main(), so any output
    // buffered after the last read_line() (or all output if there was no fgets)
    // is sent to the main thread before the halted event.
    cpu.host.flush();
    {
        let msg = make_msg("halted");
        js_sys::Reflect::set(&msg, &"exitCode".into(), &(exit_code as f64).into()).ok();
        post_to_main(&msg);
    }
    console_log!("[TriskeleVM worker] done, exit={}", exit_code);
}
