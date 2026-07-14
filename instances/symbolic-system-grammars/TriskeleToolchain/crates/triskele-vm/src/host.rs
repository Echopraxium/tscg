// triskele-vm/src/host.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.13
//
// HostIo — the host I/O boundary (HAL) for TriskeleVM.
//
// Output is synchronous. Input BLOCKS until a line is available:
//   - native: std::io::stdin() (blocks the process thread)
//   - WASM worker: Atomics.wait on a SharedArrayBuffer (implemented in the
//     triskele-vm-wasm crate, NOT here — the core stays platform-agnostic)
//
// The core (cpu, libc) reaches stdin/stdout ONLY through this trait; each
// backend supplies its own implementation. See ADR-WASM-001/002.

use std::io::Write;

/// One unit of host input.
pub enum HostLine {
    /// A line of input, WITHOUT trailing newline.
    Line(String),
    /// End of input — fgets returns NULL, getchar returns EOF.
    Eof,
}

/// Host I/O boundary. Output is synchronous; input blocks.
pub trait HostIo {
    /// Write bytes to host stdout (printf / puts / O_LOG).
    fn write_bytes(&mut self, bytes: &[u8]);
    /// Flush host stdout.
    fn flush(&mut self);
    /// Read one line, BLOCKING until available. Returns Eof when input is closed.
    fn read_line(&mut self) -> HostLine;
}

/// Native host: stdout via std::io, stdin (blocking) for input.
pub struct NativeHost {
    out: std::io::Stdout,
}

impl NativeHost {
    pub fn new() -> Self { Self { out: std::io::stdout() } }
}

impl Default for NativeHost {
    fn default() -> Self { Self::new() }
}

impl HostIo for NativeHost {
    fn write_bytes(&mut self, bytes: &[u8]) { let _ = self.out.write_all(bytes); }
    fn flush(&mut self) { let _ = self.out.flush(); }
    fn read_line(&mut self) -> HostLine {
        let mut s = String::new();
        match std::io::stdin().read_line(&mut s) {
            Ok(0)  => HostLine::Eof,              // EOF (Ctrl-D / closed stream)
            Ok(_)  => {
                while s.ends_with('\n') || s.ends_with('\r') { s.pop(); }
                HostLine::Line(s)
            }
            Err(_) => HostLine::Eof,
        }
    }
}

/// Null host: discards output, reports EOF. Safe default and test sink.
pub struct NullHost;

impl HostIo for NullHost {
    fn write_bytes(&mut self, _bytes: &[u8]) {}
    fn flush(&mut self) {}
    fn read_line(&mut self) -> HostLine { HostLine::Eof }
}
