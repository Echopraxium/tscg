// triskele-vm/src/wolf3d/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
//
// Wolf3D standalone demo entry point for TriskeleVM.
// Invoked via: tskvm --wolf3d
//
// ISA mapping (Rust → future bytecode):
//   Pos_ArenaB  : framebuffer allocation
//   F_Loop      : main game loop (Im_InputRd + render_frame + Im_FbBlit + T_FrameSyn)
//   Im_InputRd  : quit detection
//   Im_KeyQuery : per-key state (WASD + arrows)
//   Im_FbBlit   : flush framebuffer to SDL2 window
//   T_FrameSyn  : 35fps cap

pub mod map;
pub mod raycaster;

use raycaster::{Framebuffer, PlayerState, render_frame, process_input, FB_W, FB_H};
use map::{PLAYER_START_X, PLAYER_START_Y, PLAYER_START_ANGLE};
use crate::ffi::sdl2::Sdl2Context;

// ─────────────────────────────────────────────────────────────────────────────
// Wolf3DDemo — owns the entire game state
// ─────────────────────────────────────────────────────────────────────────────

pub struct Wolf3DDemo {
    sdl:    Sdl2Context,
    fb:     Framebuffer,
    player: PlayerState,
}

impl Wolf3DDemo {
    /// Initialize demo: SDL2 window + framebuffer + player.
    pub fn init() -> anyhow::Result<Self> {
        let sdl = Sdl2Context::init(
            "TriskeleVM — Wolf3D E1M1 (Phase 1 Raycaster)",
            FB_W, FB_H,
        )?;
        let fb     = Framebuffer::new(FB_W, FB_H);
        let player = PlayerState::new(PLAYER_START_X, PLAYER_START_Y, PLAYER_START_ANGLE);
        Ok(Self { sdl, fb, player })
    }

    // ─────────────────────────────────────────────────────────────────────────
    // run() — main game loop
    //
    // Loop body maps to future .tsk bytecode:
    //   Im_INPUT_RD → quit?
    //   Im_KEY_QUERY × 6 → movement / rotation
    //   [raycaster] → render_frame → fills FB
    //   Im_FB_BLIT → present
    //   T_FRAME_SYN 35 → cap fps
    // ─────────────────────────────────────────────────────────────────────────

    pub fn run(&mut self) -> anyhow::Result<()> {
        eprintln!("[Wolf3D] Starting — WASD to move, arrows to rotate, ESC to quit");
        eprintln!("[Wolf3D] Map: E1M1 16×16-per-sector — 320×200 @ 35fps");

        loop {
            // Im_INPUT_RD — poll SDL2 events, update keyboard state
            let quit = self.sdl.poll_events();
            if quit { break; }

            // Im_KEY_QUERY × 6 — WASD + Left/Right
            process_input(&mut self.player, &self.sdl);

            // F_LOOP body — DDA raycaster over all 320 columns
            render_frame(&mut self.fb, &self.player);

            // Im_FB_BLIT — push RGBA framebuffer to SDL2 window
            // The Sdl2Context::fb_blit expects a &Memory; we borrow pixels directly.
            self.sdl_fb_blit_direct()?;

            // T_FRAME_SYN 35 — sleep to maintain 35fps
            self.sdl.frame_sync(35);
        }

        eprintln!("[Wolf3D] Quit.");
        Ok(())
    }

    /// Direct pixel blit (bypasses VM Memory indirection — Phase 1 only).
    /// In Phase 2 this becomes Im_FB_BLIT via the VM memory bus.
    fn sdl_fb_blit_direct(&mut self) -> anyhow::Result<()> {
        use sdl2::pixels::PixelFormatEnum;

        let w = FB_W;
        let h = FB_H;
        let tc = self.sdl.canvas().texture_creator();
        let mut tex = tc
            .create_texture_streaming(PixelFormatEnum::RGBA32, w, h)
            .map_err(|e| anyhow::anyhow!("texture: {}", e))?;

        tex.with_lock(None, |buf, _| {
            buf.copy_from_slice(&self.fb.pixels);
        }).map_err(|e| anyhow::anyhow!("tex lock: {}", e))?;

        self.sdl.canvas().copy(&tex, None, None)
            .map_err(|e| anyhow::anyhow!("copy: {}", e))?;
        self.sdl.canvas().present();
        Ok(())
    }
}
