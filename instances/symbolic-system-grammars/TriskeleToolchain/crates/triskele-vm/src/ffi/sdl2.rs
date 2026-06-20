// triskele-vm/src/ffi/sdl2.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11
//
// SDL2 binding for TriskeleVM.
// Implements:
//   Im_FbBlit    (0x92) — blit VM framebuffer → SDL2 window
//   Im_FbClear   (0x93) — clear framebuffer
//   Im_InputRd   (0x94) — read keyboard state
//   Im_RegisterCb(0x99) — register VM callback for SDL2 event
//   T_FrameSyn   (0xA6) — synchronize to target FPS (Wolf3D: 35fps)
//
// Version 0.3.11 (TODO-3, Handover v0.3.22 §3): implements DisplayBackend
// trait instead of being referenced by concrete type from cpu/mod.rs and
// wolf3d/mod.rs. The canvas() accessor is removed; the wolf3d direct blit
// path now goes through fb_blit_pixels() instead.

use std::collections::HashMap;
use std::time::{Duration, Instant};
use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::pixels::PixelFormatEnum;
use sdl2::render::Canvas;
use sdl2::video::Window;
use crate::memory::Memory;
use crate::display::DisplayBackend;

// ─────────────────────────────────────────────────────────────────────────────
// SDL2 event IDs (used by Im_RegisterCb)
// ─────────────────────────────────────────────────────────────────────────────

pub mod event_id {
    pub const QUIT:       u32 = 0x01;
    pub const KEY_DOWN:   u32 = 0x02;
    pub const KEY_UP:     u32 = 0x03;
    pub const MOUSE_MOVE: u32 = 0x04;
    pub const MOUSE_BTN:  u32 = 0x05;
}

// ─────────────────────────────────────────────────────────────────────────────
// Keyboard state — 256 keys
// ─────────────────────────────────────────────────────────────────────────────

pub struct KeyboardState {
    pub keys: [bool; 256],
    pub quit: bool,
}

impl KeyboardState {
    pub fn new() -> Self {
        Self { keys: [false; 256], quit: false }
    }

    pub fn is_pressed(&self, scancode: u8) -> bool {
        self.keys[scancode as usize]
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Sdl2Context — owns the SDL2 window, renderer, and event pump
// ─────────────────────────────────────────────────────────────────────────────

pub struct Sdl2Context {
    sdl:         sdl2::Sdl,
    canvas:      Canvas<Window>,
    pub kbd:     KeyboardState,
    callbacks:   HashMap<u32, u64>,   // event_id → VM function address
    frame_timer: Instant,
    pub fb_w:    u32,
    pub fb_h:    u32,
}

impl Sdl2Context {
    /// Initialize SDL2 window.
    /// title : window title
    /// w, h  : framebuffer dimensions (Wolf3D: 320×200)
    pub fn init(title: &str, w: u32, h: u32) -> anyhow::Result<Self> {
        let sdl = sdl2::init()
            .map_err(|e| anyhow::anyhow!("SDL2 init failed: {}", e))?;

        let video = sdl.video()
            .map_err(|e| anyhow::anyhow!("SDL2 video init failed: {}", e))?;

        // Scale up for visibility — Wolf3D 320×200 would be tiny
        let scale = if w <= 320 { 3u32 } else { 1u32 };
        let win_w = w * scale;
        let win_h = h * scale;

        let window = video.window(title, win_w, win_h)
            .position_centered()
            .build()
            .map_err(|e| anyhow::anyhow!("SDL2 window creation failed: {}", e))?;

        let canvas = window.into_canvas()
            .accelerated()
            .present_vsync()
            .build()
            .map_err(|e| anyhow::anyhow!("SDL2 canvas creation failed: {}", e))?;

        Ok(Self {
            sdl,
            canvas,
            kbd:         KeyboardState::new(),
            callbacks:   HashMap::new(),
            frame_timer: Instant::now(),
            fb_w: w,
            fb_h: h,
        })
    }

    pub fn get_callback(&self, event_id: u32) -> Option<u64> {
        self.callbacks.get(&event_id).copied()
    }

    pub fn is_quit(&self) -> bool { self.kbd.quit }
}

// ─────────────────────────────────────────────────────────────────────────────
// DisplayBackend implementation for Sdl2Context
// ─────────────────────────────────────────────────────────────────────────────

impl DisplayBackend for Sdl2Context {
    // ── Framebuffer ────────────────────────────────────────────────────────

    /// Im_FbBlit (0x92) — blit VM framebuffer → SDL2 window
    fn fb_blit(&mut self, mem: &Memory, fb_ptr: u64) -> anyhow::Result<()> {
        let w = self.fb_w;
        let h = self.fb_h;
        let size = (w * h * 4) as usize;
        let data = mem.read_bytes(fb_ptr, size)?;

        let texture_creator = self.canvas.texture_creator();
        let mut texture = texture_creator
            .create_texture_streaming(PixelFormatEnum::RGBA32, w, h)
            .map_err(|e| anyhow::anyhow!("texture creation failed: {}", e))?;

        texture.with_lock(None, |buf, _pitch| {
            buf.copy_from_slice(data);
        }).map_err(|e| anyhow::anyhow!("texture lock failed: {}", e))?;

        self.canvas.copy(&texture, None, None)
            .map_err(|e| anyhow::anyhow!("canvas copy failed: {}", e))?;

        self.canvas.present();
        Ok(())
    }

    /// Direct pixel blit — used by Wolf3D Phase-1 loop (owns its own Framebuffer).
    /// Replaces the canvas() accessor that previously broke encapsulation.
    fn fb_blit_pixels(&mut self, pixels: &[u8], width: u32, height: u32)
        -> anyhow::Result<()>
    {
        let texture_creator = self.canvas.texture_creator();
        let mut texture = texture_creator
            .create_texture_streaming(PixelFormatEnum::RGBA32, width, height)
            .map_err(|e| anyhow::anyhow!("texture: {}", e))?;

        texture.with_lock(None, |buf, _| {
            buf.copy_from_slice(pixels);
        }).map_err(|e| anyhow::anyhow!("tex lock: {}", e))?;

        self.canvas.copy(&texture, None, None)
            .map_err(|e| anyhow::anyhow!("copy: {}", e))?;
        self.canvas.present();
        Ok(())
    }

    /// Im_FbClear (0x93) — fill framebuffer with solid color
    fn fb_clear(&mut self, mem: &mut Memory, fb_ptr: u64, color: u32)
        -> anyhow::Result<()>
    {
        let size = (self.fb_w * self.fb_h) as usize;
        let r = ((color >> 24) & 0xFF) as u8;
        let g = ((color >> 16) & 0xFF) as u8;
        let b = ((color >>  8) & 0xFF) as u8;
        let a = ( color        & 0xFF) as u8;
        for i in 0..size {
            let off = fb_ptr + (i as u64) * 4;
            mem.write_u8(off,     r)?;
            mem.write_u8(off + 1, g)?;
            mem.write_u8(off + 2, b)?;
            mem.write_u8(off + 3, a)?;
        }
        Ok(())
    }

    // ── Input ──────────────────────────────────────────────────────────────

    /// Im_InputRd (0x94) — poll SDL2 events, update keyboard state.
    /// Returns true if quit was requested.
    fn poll_events(&mut self) -> bool {
        let mut event_pump = match self.sdl.event_pump() {
            Ok(p) => p,
            Err(_) => return false,
        };

        for event in event_pump.poll_iter() {
            match event {
                Event::Quit { .. } => {
                    self.kbd.quit = true;
                }
                Event::KeyDown { keycode: Some(kc), .. } => {
                    if let Some(sc) = keycode_to_scancode(kc) {
                        self.kbd.keys[sc as usize] = true;
                    }
                    if kc == Keycode::Escape {
                        self.kbd.quit = true;
                    }
                }
                Event::KeyUp { keycode: Some(kc), .. } => {
                    if let Some(sc) = keycode_to_scancode(kc) {
                        self.kbd.keys[sc as usize] = false;
                    }
                }
                _ => {}
            }
        }
        self.kbd.quit
    }

    /// Im_RegisterCb (0x99) — register VM function for SDL2 event.
    fn register_callback(&mut self, event_id: u32, vm_addr: u64) {
        self.callbacks.insert(event_id, vm_addr);
    }

    /// Im_KeyQuery (0x9A) — test single key by scancode.
    fn key_query(&self, sc: u8) -> u64 {
        self.kbd.is_pressed(sc) as u64
    }

    // ── Timing ─────────────────────────────────────────────────────────────

    /// T_FrameSyn (0xA6) — sleep to maintain target FPS.
    fn frame_sync(&mut self, target_fps: u32) {
        let frame_dur = Duration::from_micros(1_000_000 / target_fps as u64);
        let elapsed = self.frame_timer.elapsed();
        if elapsed < frame_dur {
            std::thread::sleep(frame_dur - elapsed);
        }
        self.frame_timer = Instant::now();
    }

    // ── Dimensions ─────────────────────────────────────────────────────────

    fn width(&self)  -> u32 { self.fb_w }
    fn height(&self) -> u32 { self.fb_h }
}

// ─────────────────────────────────────────────────────────────────────────────
// Keyboard scancodes (Wolf3D / DOOM compatible)
// ─────────────────────────────────────────────────────────────────────────────

pub mod scancode {
    pub const W:     u8 = 0x11;
    pub const A:     u8 = 0x1E;
    pub const S:     u8 = 0x1F;
    pub const D:     u8 = 0x20;
    pub const LEFT:  u8 = 0x4B;
    pub const RIGHT: u8 = 0x4D;
    pub const UP:    u8 = 0x48;
    pub const DOWN:  u8 = 0x50;
    pub const ESC:   u8 = 0x01;
    pub const SPACE: u8 = 0x39;
    pub const ENTER: u8 = 0x1C;
}

fn keycode_to_scancode(kc: Keycode) -> Option<u8> {
    match kc {
        Keycode::W      => Some(scancode::W),
        Keycode::A      => Some(scancode::A),
        Keycode::S      => Some(scancode::S),
        Keycode::D      => Some(scancode::D),
        Keycode::Left   => Some(scancode::LEFT),
        Keycode::Right  => Some(scancode::RIGHT),
        Keycode::Up     => Some(scancode::UP),
        Keycode::Down   => Some(scancode::DOWN),
        Keycode::Escape => Some(scancode::ESC),
        Keycode::Space  => Some(scancode::SPACE),
        Keycode::Return => Some(scancode::ENTER),
        _ => None,
    }
}

