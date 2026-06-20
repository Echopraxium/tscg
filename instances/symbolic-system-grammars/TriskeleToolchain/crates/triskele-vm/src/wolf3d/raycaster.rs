// triskele-vm/src/wolf3d/raycaster.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
//
// Wolf3D-style raycaster.
// Algorithm: DDA (Digital Differential Analysis) — same as original Wolf3D.
// Anti-fisheye correction: multiply wall distance by cos(ray_angle − player_angle).
// Arithmetic: f32 (converted to fixed 16.16 by D_FixMul paths in bytecode Phase 2).
//
// ISA grounding:
//   A_  : framebuffer as memory attractor (stack of RGBA pixels)
//   F_  : ray loop = F_Loop construct
//   D_  : pixel writes = D_Store32 in bytecode
//   It_ : wall hit flag = informational state change
//   R_  : f32↔fixed = R_F2Fix / R_Fix2F in bytecode
//   T_  : T_FRAME_SYN (35fps) handled by Sdl2Context::frame_sync
//   Im_ : Im_FB_BLIT — push framebuffer to SDL2 window

use super::map::{MAP_W, MAP_H, E1M1, is_wall, tile, wall_color};

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────

pub const FB_W: u32 = 320;
pub const FB_H: u32 = 200;
const FOV:     f32  = std::f32::consts::PI / 3.0;  // 60°
const HALF_FOV: f32 = FOV / 2.0;
const MOVE_SPEED: f32 = 0.05;
const ROT_SPEED:  f32 = 0.04;

// Ceiling and floor colours (Wolf3D E1M1 style)
const COLOR_CEILING: (u8, u8, u8) = (0x38, 0x38, 0x38);
const COLOR_FLOOR:   (u8, u8, u8) = (0x70, 0x70, 0x70);

// ─────────────────────────────────────────────────────────────────────────────
// PlayerState — D_ category: mutable world state
// ─────────────────────────────────────────────────────────────────────────────

pub struct PlayerState {
    pub x:     f32,
    pub y:     f32,
    pub angle: f32,  // radians, 0 = East, positive = CCW
}

impl PlayerState {
    pub fn new(x: f32, y: f32, angle: f32) -> Self {
        Self { x, y, angle }
    }

    /// Try to move by (dx, dy); reject if wall collision.
    pub fn try_move(&mut self, dx: f32, dy: f32) {
        let nx = self.x + dx;
        let ny = self.y + dy;
        if !is_wall(&E1M1, nx as i32, self.y as i32) {
            self.x = nx;
        }
        if !is_wall(&E1M1, self.x as i32, ny as i32) {
            self.y = ny;
        }
    }

    pub fn rotate(&mut self, da: f32) {
        self.angle = (self.angle + da).rem_euclid(2.0 * std::f32::consts::PI);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Framebuffer — A_ attractor: RGBA pixel array
// ─────────────────────────────────────────────────────────────────────────────

pub struct Framebuffer {
    pub pixels: Vec<u8>,   // RGBA, row-major
    pub w: u32,
    pub h: u32,
}

impl Framebuffer {
    pub fn new(w: u32, h: u32) -> Self {
        Self {
            pixels: vec![0u8; (w * h * 4) as usize],
            w,
            h,
        }
    }

    #[inline]
    pub fn set_pixel(&mut self, x: u32, y: u32, r: u8, g: u8, b: u8) {
        if x >= self.w || y >= self.h { return; }
        let off = ((y * self.w + x) * 4) as usize;
        self.pixels[off    ] = r;
        self.pixels[off + 1] = g;
        self.pixels[off + 2] = b;
        self.pixels[off + 3] = 0xFF;
    }

    /// Draw a vertical stripe from y0 to y1 (inclusive) with given colour.
    pub fn vline(&mut self, x: u32, y0: u32, y1: u32, r: u8, g: u8, b: u8) {
        let y0 = y0.min(self.h - 1);
        let y1 = y1.min(self.h - 1);
        for y in y0..=y1 {
            self.set_pixel(x, y, r, g, b);
        }
    }

    /// Fill entire framebuffer with ceiling (top half) and floor (bottom half).
    pub fn clear_scene(&mut self) {
        let half = self.h / 2;
        let (cr, cg, cb) = COLOR_CEILING;
        let (fr, fg, fb) = COLOR_FLOOR;
        for y in 0..self.h {
            let (r, g, b) = if y < half { (cr, cg, cb) } else { (fr, fg, fb) };
            for x in 0..self.w {
                self.set_pixel(x, y, r, g, b);
            }
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// DDA Ray — It_ informational state per ray
// ─────────────────────────────────────────────────────────────────────────────

struct RayHit {
    dist:       f32,   // corrected wall distance (no fisheye)
    tile:       u8,    // wall tile index
    north_south: bool, // N/S face hit (for shading)
}

/// Cast a single ray from (px, py) at angle `ray_angle`.
/// Uses DDA — the same algorithm as id Software's original Wolf3D.
fn cast_ray(px: f32, py: f32, ray_angle: f32, player_angle: f32) -> RayHit {
    let cos_a = ray_angle.cos();
    let sin_a = ray_angle.sin();

    // DDA: grid step direction
    let step_x: i32 = if cos_a > 0.0 { 1 } else { -1 };
    let step_y: i32 = if sin_a > 0.0 { 1 } else { -1 };

    // Initial cell
    let mut map_x = px as i32;
    let mut map_y = py as i32;

    // t-delta: distance to travel in ray direction for one full cell step
    let delta_x = if cos_a.abs() < 1e-10 { f32::MAX } else { (1.0 / cos_a).abs() };
    let delta_y = if sin_a.abs() < 1e-10 { f32::MAX } else { (1.0 / sin_a).abs() };

    // Initial side distances
    let mut side_x = if cos_a < 0.0 {
        (px - map_x as f32) * delta_x
    } else {
        (map_x as f32 + 1.0 - px) * delta_x
    };
    let mut side_y = if sin_a < 0.0 {
        (py - map_y as f32) * delta_y
    } else {
        (map_y as f32 + 1.0 - py) * delta_y
    };

    // March
    let mut north_south;
    loop {
        if side_x < side_y {
            side_x    += delta_x;
            map_x     += step_x;
            north_south = false;
        } else {
            side_y    += delta_y;
            map_y     += step_y;
            north_south = true;
        }

        if map_x < 0 || map_y < 0
            || map_x >= MAP_W as i32
            || map_y >= MAP_H as i32
        {
            return RayHit { dist: 64.0, tile: 1, north_south };
        }

        let t = tile(&E1M1, map_x, map_y);
        if t != 0 {
            // Perpendicular wall distance (removes fisheye via projection)
            let perp_dist = if !north_south {
                (map_x as f32 - px + (1.0 - step_x as f32) / 2.0) / cos_a
            } else {
                (map_y as f32 - py + (1.0 - step_y as f32) / 2.0) / sin_a
            };

            // Anti-fisheye: multiply by cos(deviation from view centre)
            let deviation = ray_angle - player_angle;
            let corrected = perp_dist * deviation.cos();

            return RayHit {
                dist: corrected.abs().max(0.0001),
                tile: t,
                north_south,
            };
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// render_frame — F_ loop over all columns (F_LOOP construct in bytecode)
// ─────────────────────────────────────────────────────────────────────────────

/// Render one complete frame into `fb`.
pub fn render_frame(fb: &mut Framebuffer, player: &PlayerState) {
    fb.clear_scene();

    let half_w   = fb.w as f32 / 2.0;
    let half_h   = fb.h as f32 / 2.0;
    let proj_dist = half_w / HALF_FOV.tan();   // projection plane distance

    for col in 0..fb.w {
        // Ray angle for this column (left = player_angle - FOV/2, right = + FOV/2)
        let ray_frac   = col as f32 / fb.w as f32 - 0.5;   // -0.5 .. +0.5
        let ray_angle  = player.angle + ray_frac * FOV;

        let hit = cast_ray(player.x, player.y, ray_angle, player.angle);

        // Wall height on screen
        let wall_h = ((proj_dist / hit.dist) as u32).min(fb.h);

        let y0 = (half_h - wall_h as f32 / 2.0).max(0.0) as u32;
        let y1 = (half_h + wall_h as f32 / 2.0).min(fb.h as f32 - 1.0) as u32;

        let (r, g, b) = wall_color(hit.tile, hit.north_south);

        // Distance shading: darker = farther (Wolf3D style)
        let shade = (1.0 - (hit.dist / 20.0).min(1.0)) * 0.85 + 0.15;
        let r = (r as f32 * shade) as u8;
        let g = (g as f32 * shade) as u8;
        let b = (b as f32 * shade) as u8;

        fb.vline(col, y0, y1, r, g, b);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// process_input — D_ dynamics: player state mutation from keyboard
// Uses Im_KeyQuery scancode constants from ffi::sdl2::scancode
// ─────────────────────────────────────────────────────────────────────────────

use crate::display::DisplayBackend;
use crate::ffi::sdl2::scancode;

pub fn process_input(player: &mut PlayerState, display: &dyn DisplayBackend) {
    // Forward / Backward — WASD + arrow keys
    let forward_back = {
        let fwd = display.key_query(scancode::W) != 0
               || display.key_query(scancode::UP) != 0;
        let back = display.key_query(scancode::S) != 0
                || display.key_query(scancode::DOWN) != 0;
        if fwd { 1.0f32 } else if back { -1.0f32 } else { 0.0f32 }
    };

    // Strafe — A / D
    let strafe = {
        let left  = display.key_query(scancode::A) != 0;
        let right = display.key_query(scancode::D) != 0;
        if right { 1.0f32 } else if left { -1.0f32 } else { 0.0f32 }
    };

    // Rotation — Left / Right arrows
    let rot = {
        let left  = display.key_query(scancode::LEFT) != 0;
        let right = display.key_query(scancode::RIGHT) != 0;
        if right { 1.0f32 } else if left { -1.0f32 } else { 0.0f32 }
    };

    // Apply rotation first, then movement
    if rot.abs() > 0.0 {
        player.rotate(rot * ROT_SPEED);
    }

    if forward_back.abs() > 0.0 {
        let dx = player.angle.cos() * MOVE_SPEED * forward_back;
        let dy = player.angle.sin() * MOVE_SPEED * forward_back;
        player.try_move(dx, dy);
    }

    if strafe.abs() > 0.0 {
        // Strafe = move perpendicular to view direction
        let perp = player.angle + std::f32::consts::PI / 2.0;
        let dx = perp.cos() * MOVE_SPEED * strafe;
        let dy = perp.sin() * MOVE_SPEED * strafe;
        player.try_move(dx, dy);
    }
}
