// triskele-vm/src/wolf3d/mod.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.11
//
// Wolf3D standalone demo entry point for TriskeleVM.
// Invoked via: tskvm --wolf3d
//
// Version 0.3.11 (TODO-3): uses DisplayBackend trait instead of Sdl2Context
// concrete type. The sdl_fb_blit_direct() method now calls fb_blit_pixels()
// on the trait, removing the canvas() encapsulation breach.
//
// ISA mapping (Rust → future bytecode):
//   Pos_ArenaB  : framebuffer allocation
//   F_Loop      : main game loop (Im_InputRd + render_frame + Im_FbBlit + T_FrameSyn)
//   Im_InputRd  : quit detection
//   Im_KeyQuery : per-key state (WASD + arrows)
//   Im_FbBlit   : flush framebuffer to display window
//   T_FrameSyn  : 35fps cap

pub mod map;
pub mod raycaster;

use raycaster::{Framebuffer, PlayerState, render_frame, process_input, FB_W, FB_H};
use map::{PLAYER_START_X, PLAYER_START_Y, PLAYER_START_ANGLE};
use crate::display::DisplayBackend;
use crate::ffi::sdl2::Sdl2Context;

// ─────────────────────────────────────────────────────────────────────────────
// Wolf3DDemo — owns the entire game state
// ─────────────────────────────────────────────────────────────────────────────

pub struct Wolf3DDemo {
    display: Box<dyn DisplayBackend>,
    fb:      Framebuffer,
    player:  PlayerState,
}

impl Wolf3DDemo {
    /// Initialize demo: display window + framebuffer + player.
    pub fn init() -> anyhow::Result<Self> {
        let sdl = Sdl2Context::init(
            "TriskeleVM — Wolf3D E1M1 (Phase 1 Raycaster)",
            FB_W, FB_H,
        )?;
        let fb     = Framebuffer::new(FB_W, FB_H);
        let player = PlayerState::new(PLAYER_START_X, PLAYER_START_Y, PLAYER_START_ANGLE);
        Ok(Self { display: Box::new(sdl), fb, player })
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
            // Im_INPUT_RD — poll display events, update keyboard state
            let quit = self.display.poll_events();
            if quit { break; }

            // Im_KEY_QUERY × 6 — WASD + Left/Right
            process_input(&mut self.player, self.display.as_ref());

            // F_LOOP body — DDA raycaster over all 320 columns
            render_frame(&mut self.fb, &self.player);

            // Im_FB_BLIT — push RGBA framebuffer to display window
            self.display.fb_blit_pixels(&self.fb.pixels, FB_W, FB_H)?;

            // T_FRAME_SYN 35 — sleep to maintain 35fps
            self.display.frame_sync(35);
        }

        eprintln!("[Wolf3D] Quit.");
        Ok(())
    }
}
