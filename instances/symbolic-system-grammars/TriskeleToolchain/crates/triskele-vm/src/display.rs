// triskele-vm/src/display.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11
//
// DisplayBackend trait — backend-agnostic display/input interface for TriskeleVM.
//
// Rationale (TODO-3, Handover v0.3.22 §3):
// Previously, `Cpu.sdl: Option<Sdl2Context>` coupled the interpreter core
// directly to SDL2's concrete type. This trait replaces that field with
// `Cpu.display: Option<Box<dyn DisplayBackend>>`, letting the interpreter
// core (CPU, memory, libc) remain unchanged across display backends, while
// the concrete implementation lives in a separately-composable type:
//   - `Sdl2Context` (native Windows/Linux) — existing 276-line module,
//     adapted to implement this trait.
//   - Future: a WASM backend that talks to a <canvas> via wasm-bindgen
//     (`ImageData`/`putImageData`, `requestAnimationFrame`, DOM keyboard
//     events) — additive, zero surgery on the interpreter core.
//
// Trait design notes:
//   - `fb_blit`/`fb_clear` operate on VM Memory (same as the opcodes they
//     implement: Im_FbBlit, Im_FbClear) — the backend reads/writes pixels via
//     the VM's memory bus.
//   - `fb_blit_pixels` is the "direct" variant (used by Wolf3D's Phase-1 loop
//     which owns its own Framebuffer, bypassing VM Memory). This replaces the
//     `canvas()` accessor that previously broke encapsulation by exposing
//     SDL2's raw `Canvas<Window>` to wolf3d/mod.rs.
//   - `key_query` takes a `u8` scancode matching the constants in
//     `ffi::sdl2::scancode` — these are Wolf3D/DOOM scancodes, kept as plain
//     u8 to avoid a dependency on SDL2 types in the trait itself.
//   - All methods take `&mut self` for consistency (poll_events and frame_sync
//     inherently need mutability; making the rest consistent avoids awkward
//     partial-borrow issues at call sites).

use crate::memory::Memory;

/// Backend-agnostic display and input interface.
///
/// Implemented by `Sdl2Context` for native (Windows/Linux) builds.
/// Future implementations: WASM canvas backend, headless test backend.
pub trait DisplayBackend {
    // ── Framebuffer ────────────────────────────────────────────────────────

    /// Im_FbBlit — blit the VM framebuffer at `fb_ptr` in `mem` to the display.
    /// `fb_ptr` points to a contiguous RGBA32 pixel buffer of `fb_w × fb_h × 4`
    /// bytes in VM address space.
    fn fb_blit(&mut self, mem: &Memory, fb_ptr: u64) -> anyhow::Result<()>;

    /// Direct pixel blit — takes a raw RGBA32 slice (no VM Memory indirection).
    /// Used by the Wolf3D Phase-1 loop which owns its own `Framebuffer` directly.
    /// Replaces the `canvas()` accessor that previously broke encapsulation.
    fn fb_blit_pixels(&mut self, pixels: &[u8], width: u32, height: u32)
        -> anyhow::Result<()>;

    /// Im_FbClear — fill the VM framebuffer at `fb_ptr` in `mem` with `color`
    /// (RGBA32, packed as `0xRRGGBBAA`).
    fn fb_clear(&mut self, mem: &mut Memory, fb_ptr: u64, color: u32)
        -> anyhow::Result<()>;

    // ── Input ──────────────────────────────────────────────────────────────

    /// Im_InputRd — drain the event queue; returns `true` if a quit event was
    /// received (window close, ESC key, etc.).
    fn poll_events(&mut self) -> bool;

    /// Im_RegisterCb — register a VM function address to be called for a given
    /// event type (see `ffi::sdl2::event_id`).
    fn register_callback(&mut self, event_id: u32, vm_addr: u64);

    /// Im_KeyQuery — return `1` if the key identified by `scancode` is currently
    /// held, `0` otherwise. Scancodes match `ffi::sdl2::scancode` constants.
    fn key_query(&self, scancode: u8) -> u64;

    // ── Timing ─────────────────────────────────────────────────────────────

    /// T_FrameSyn — sleep as needed to maintain `target_fps` frames per second.
    fn frame_sync(&mut self, target_fps: u32);

    // ── Dimensions ─────────────────────────────────────────────────────────

    /// Framebuffer width in pixels (as configured at init time).
    fn width(&self) -> u32;

    /// Framebuffer height in pixels (as configured at init time).
    fn height(&self) -> u32;
}
