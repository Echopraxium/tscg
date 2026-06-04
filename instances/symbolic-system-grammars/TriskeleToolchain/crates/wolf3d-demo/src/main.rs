// wolf3d-demo/src/main.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
//
// Wolf3D E1M1 raycaster — standalone SDL2 demo.
// No dependency on triskele-vm; pure Rust + SDL2.
//
// Controls:
//   W / Up    — move forward
//   S / Down  — move backward
//   A         — strafe left
//   D         — strafe right
//   Left      — rotate left
//   Right     — rotate right
//   ESC       — quit
//
// ISA grounding (future .tasm port):
//   A_   framebuffer = memory attractor (RGBA pixel array)
//   F_   ray loop = F_LOOP over 320 columns
//   D_   D_FixMul (fixed 16.16), D_Store32 (pixel write)
//   R_   R_F2Fix / R_Fix2F (type conversions)
//   It_  wall-hit flag = informational state change
//   Im_  Im_FB_BLIT, Im_KEY_QUERY, Im_INPUT_RD
//   T_   T_FRAME_SYN 35fps

mod map;

use map::{MAP_W, MAP_H, E1M1, is_wall, tile, wall_color,
          PLAYER_START_X, PLAYER_START_Y, PLAYER_START_ANGLE};
use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::pixels::PixelFormatEnum;

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────

const FB_W: u32 = 320;
const FB_H: u32 = 200;
const SCALE: u32 = 3;          // window = 960×600 for visibility
const TARGET_FPS: u32 = 35;

const FOV:      f32 = std::f32::consts::PI / 3.0;  // 60°
const MOVE_SPD: f32 = 0.05;
const ROT_SPD:  f32 = 0.04;

const COLOR_CEILING: (u8, u8, u8) = (0x38, 0x38, 0x38);
const COLOR_FLOOR:   (u8, u8, u8) = (0x70, 0x70, 0x70);

// ─────────────────────────────────────────────────────────────────────────────
// PlayerState
// ─────────────────────────────────────────────────────────────────────────────

struct Player { x: f32, y: f32, angle: f32 }

impl Player {
    fn new() -> Self {
        Self { x: PLAYER_START_X, y: PLAYER_START_Y, angle: PLAYER_START_ANGLE }
    }

    fn try_move(&mut self, dx: f32, dy: f32) {
        if !is_wall(&E1M1, (self.x + dx) as i32, self.y as i32) { self.x += dx; }
        if !is_wall(&E1M1, self.x as i32, (self.y + dy) as i32) { self.y += dy; }
    }

    fn rotate(&mut self, da: f32) {
        self.angle = (self.angle + da).rem_euclid(2.0 * std::f32::consts::PI);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Keyboard state
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Default)]
struct Keys {
    w: bool, a: bool, s: bool, d: bool,
    left: bool, right: bool,
    quit: bool,
}

// ─────────────────────────────────────────────────────────────────────────────
// DDA raycaster — single column
// ─────────────────────────────────────────────────────────────────────────────

struct Hit { dist: f32, tile: u8, ns: bool }

fn cast_ray(px: f32, py: f32, ray_angle: f32, player_angle: f32) -> Hit {
    let ca = ray_angle.cos();
    let sa = ray_angle.sin();

    let step_x: i32 = if ca > 0.0 { 1 } else { -1 };
    let step_y: i32 = if sa > 0.0 { 1 } else { -1 };

    let mut mx = px as i32;
    let mut my = py as i32;

    let dx = if ca.abs() < 1e-10 { f32::MAX } else { (1.0 / ca).abs() };
    let dy = if sa.abs() < 1e-10 { f32::MAX } else { (1.0 / sa).abs() };

    let mut sx = if ca < 0.0 { (px - mx as f32) * dx } else { (mx as f32 + 1.0 - px) * dx };
    let mut sy = if sa < 0.0 { (py - my as f32) * dy } else { (my as f32 + 1.0 - py) * dy };

    let mut ns = false;
    loop {
        if sx < sy { sx += dx; mx += step_x; ns = false; }
        else        { sy += dy; my += step_y; ns = true;  }

        if mx < 0 || my < 0 || mx >= MAP_W as i32 || my >= MAP_H as i32 {
            return Hit { dist: 64.0, tile: 1, ns };
        }
        let t = tile(&E1M1, mx, my);
        if t != 0 {
            // Perpendicular wall distance (removes fisheye via projection plane)
            let perp = if !ns {
                (mx as f32 - px + (1.0 - step_x as f32) / 2.0) / ca
            } else {
                (my as f32 - py + (1.0 - step_y as f32) / 2.0) / sa
            };
            // Anti-fisheye correction: cos of ray deviation from view centre
            let corrected = (perp * (ray_angle - player_angle).cos()).abs().max(0.0001);
            return Hit { dist: corrected, tile: t, ns };
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Render one frame into pixels[]  (RGBA row-major)
// ─────────────────────────────────────────────────────────────────────────────

fn render(pixels: &mut [u8], player: &Player) {
    let w = FB_W as usize;
    let h = FB_H as usize;
    let half_h   = h as f32 / 2.0;
    let proj_dist = (w as f32 / 2.0) / (FOV / 2.0).tan();

    // Ceiling + floor
    let (cr, cg, cb) = COLOR_CEILING;
    let (fr, fg, fb) = COLOR_FLOOR;
    for y in 0..h {
        let (r, g, b) = if y < h / 2 { (cr, cg, cb) } else { (fr, fg, fb) };
        for x in 0..w {
            let off = (y * w + x) * 4;
            pixels[off]     = r;
            pixels[off + 1] = g;
            pixels[off + 2] = b;
            pixels[off + 3] = 0xFF;
        }
    }

    // Walls — one DDA ray per column
    for col in 0..w {
        let frac      = col as f32 / w as f32 - 0.5;
        let ray_angle = player.angle + frac * FOV;
        let hit       = cast_ray(player.x, player.y, ray_angle, player.angle);

        let wall_h  = ((proj_dist / hit.dist) as usize).min(h);
        let y0      = (half_h - wall_h as f32 / 2.0).max(0.0) as usize;
        let y1      = (half_h + wall_h as f32 / 2.0).min(h as f32 - 1.0) as usize;

        let (wr, wg, wb) = wall_color(hit.tile, hit.ns);
        let shade        = (1.0 - (hit.dist / 20.0).min(1.0)) * 0.85 + 0.15;
        let wr = (wr as f32 * shade) as u8;
        let wg = (wg as f32 * shade) as u8;
        let wb = (wb as f32 * shade) as u8;

        for y in y0..=y1 {
            let off = (y * w + col) * 4;
            pixels[off]     = wr;
            pixels[off + 1] = wg;
            pixels[off + 2] = wb;
            pixels[off + 3] = 0xFF;
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────────────────────

fn main() -> anyhow::Result<()> {
    let sdl     = sdl2::init().map_err(|e| anyhow::anyhow!("{}", e))?;
    let video   = sdl.video().map_err(|e| anyhow::anyhow!("{}", e))?;
    let window  = video
        .window("TriskeleVM — Wolf3D E1M1 Demo", FB_W * SCALE, FB_H * SCALE)
        .position_centered()
        .build()?;
    let mut canvas = window.into_canvas().accelerated().build()
        .map_err(|e| anyhow::anyhow!("{}", e))?;
    let tc = canvas.texture_creator();
    let mut texture = tc
        .create_texture_streaming(PixelFormatEnum::RGBA32, FB_W, FB_H)
        .map_err(|e| anyhow::anyhow!("{}", e))?;

    let mut pixels = vec![0u8; (FB_W * FB_H * 4) as usize];
    let mut player = Player::new();
    let mut keys   = Keys::default();
    let mut pump   = sdl.event_pump().map_err(|e| anyhow::anyhow!("{}", e))?;

    let frame_dur = std::time::Duration::from_micros(1_000_000 / TARGET_FPS as u64);

    eprintln!("[wolf3d-demo] W/S=forward/back  A/D=strafe  ←/→=rotate  ESC=quit");
    eprintln!("[wolf3d-demo] Spawn: ({:.1}, {:.1})  angle: {:.2} rad", player.x, player.y, player.angle);

    'game: loop {
        let t0 = std::time::Instant::now();

        // ── Im_INPUT_RD — poll events ─────────────────────────────────────
        for event in pump.poll_iter() {
            match event {
                Event::Quit { .. } => break 'game,
                Event::KeyDown { keycode: Some(kc), .. } => match kc {
                    Keycode::Escape => break 'game,
                    Keycode::W      => keys.w     = true,
                    Keycode::A      => keys.a     = true,
                    Keycode::S      => keys.s     = true,
                    Keycode::D      => keys.d     = true,
                    Keycode::Left   => keys.left  = true,
                    Keycode::Right  => keys.right = true,
                    _ => {}
                },
                Event::KeyUp { keycode: Some(kc), .. } => match kc {
                    Keycode::W      => keys.w     = false,
                    Keycode::A      => keys.a     = false,
                    Keycode::S      => keys.s     = false,
                    Keycode::D      => keys.d     = false,
                    Keycode::Left   => keys.left  = false,
                    Keycode::Right  => keys.right = false,
                    _ => {}
                },
                _ => {}
            }
        }

        // ── Im_KEY_QUERY × 6 — apply movement ────────────────────────────
        if keys.left  { player.rotate(-ROT_SPD); }
        if keys.right { player.rotate( ROT_SPD); }

        if keys.w {
            let dx = player.angle.cos() * MOVE_SPD;
            let dy = player.angle.sin() * MOVE_SPD;
            player.try_move(dx, dy);
        }
        if keys.s {
            let dx = -player.angle.cos() * MOVE_SPD;
            let dy = -player.angle.sin() * MOVE_SPD;
            player.try_move(dx, dy);
        }
        if keys.a {
            let perp = player.angle - std::f32::consts::FRAC_PI_2;
            player.try_move(perp.cos() * MOVE_SPD, perp.sin() * MOVE_SPD);
        }
        if keys.d {
            let perp = player.angle + std::f32::consts::FRAC_PI_2;
            player.try_move(perp.cos() * MOVE_SPD, perp.sin() * MOVE_SPD);
        }

        // ── F_LOOP — DDA raycaster (320 columns) ─────────────────────────
        render(&mut pixels, &player);

        // ── Im_FB_BLIT — push framebuffer to SDL2 window ─────────────────
        texture.with_lock(None, |buf, _| buf.copy_from_slice(&pixels))
            .map_err(|e| anyhow::anyhow!("{}", e))?;
        canvas.copy(&texture, None, None)
            .map_err(|e| anyhow::anyhow!("{}", e))?;
        canvas.present();

        // ── T_FRAME_SYN 35 — cap to 35fps ────────────────────────────────
        let elapsed = t0.elapsed();
        if elapsed < frame_dur {
            std::thread::sleep(frame_dur - elapsed);
        }
    }

    eprintln!("[wolf3d-demo] Quit.");
    Ok(())
}
