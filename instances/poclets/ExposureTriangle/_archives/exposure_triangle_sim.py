"""
exposure_triangle_sim.py
========================
TSCG Poclet Simulation – Exposure Triangle (Pygame)
Author: Echopraxium with the collaboration of Claude AI

Shows 'photo_sample.jpg' (same folder as this script) with live photo
effects driven by the three exposure parameters:

  ISO         → Brightness boost + grain / noise overlay
  Aperture    → Vignette darkening at image edges (shallow DoF indicator)
  Shutter     → Brightness + horizontal motion-blur (camera-shake sim)

ASFID / REVOI scores are loaded from M0_ExposureTriangle.jsonld.
The triangle diagram shows the current EV balance state.

Requirements:
    pip install pygame numpy

Run:
    python exposure_triangle_sim.py
    python exposure_triangle_sim.py path/to/M0_ExposureTriangle.jsonld
"""

import sys
import math
import json
from pathlib import Path

import numpy as np
import pygame

# ─────────────────────────────────────────────────────────────────────────────
# Window / FPS
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H  = 1200, 720
FPS                  = 30          # photo effects cached; 30 fps sufficient
POCLET_PATH_OVERRIDE = sys.argv[1] if len(sys.argv) > 1 else None

# ─────────────────────────────────────────────────────────────────────────────
# Palette
# ─────────────────────────────────────────────────────────────────────────────
BG_COLOR        = (12,  12,  18)
PANEL_COLOR     = (22,  22,  32)
BORDER_COLOR    = (55,  55,  75)
TEXT_COLOR      = (220, 220, 230)
DIM_COLOR       = (130, 130, 150)
GOLD            = (255, 200,  50)
REVOI_COLOR     = (120, 180, 255)
GREEN           = (80,  200, 120)
RED             = (220,  60,  60)
BLUE_DARK       = (80,  120, 255)
SLIDER_BG       = (38,  38,  52)

# Per-parameter accent colors
ISO_COLOR  = ( 80, 210, 210)   # teal
APT_COLOR  = (255, 175,  45)   # amber
SHT_COLOR  = (200, 110, 255)   # violet

# ─────────────────────────────────────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────────────────────────────────────
LEFT_W    = 300
RIGHT_W   = 220
MID_W     = WINDOW_W - LEFT_W - RIGHT_W    # 680
PANEL_PAD = 12

IMG_DISPLAY_W = 658
IMG_DISPLAY_H = 438

# ─────────────────────────────────────────────────────────────────────────────
# Physical parameter ranges
# ─────────────────────────────────────────────────────────────────────────────
ISO_MIN, ISO_MAX = 100.0, 6400.0
F_MIN,   F_MAX   = 1.4,   22.0
T_MIN,   T_MAX   = 1.0 / 4000.0, 2.0   # seconds

# "Correct" baseline for photo_sample.jpg
BASELINE_ISO = 400.0
BASELINE_F   = 5.6
BASELINE_T   = 1.0 / 250.0

# ─────────────────────────────────────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def ev_offset(iso, f_num, t_sec):
    """Signed EV offset from neutral baseline (+ = overexposed, − = under)."""
    return (math.log2(iso   / BASELINE_ISO)
          + 2.0 * math.log2(BASELINE_F / f_num)   # wide = more light
          + math.log2(t_sec / BASELINE_T))


def iso_from_slider(v):
    """v ∈ [0,1] → ISO (log scale 100–6400)."""
    return ISO_MIN * ((ISO_MAX / ISO_MIN) ** v)


def fnum_from_slider(v):
    """v ∈ [0,1] → f-number (f/1.4 wide open … f/22 narrow)."""
    return F_MIN * ((F_MAX / F_MIN) ** v)


def t_from_slider(v):
    """v ∈ [0,1] → shutter time in seconds (1/4000 s … 2 s)."""
    return T_MIN * ((T_MAX / T_MIN) ** v)


def fmt_iso(iso):
    return f"ISO {int(round(iso))}"


def fmt_fnum(f):
    return f"f/{f:.1f}"


def fmt_shutter(t):
    if t >= 1.0:
        return f"{t:.1f} s"
    elif t >= 0.1:
        return f"1/{int(round(1/t))} s"
    else:
        return f"1/{int(round(1/t))} s"


# ─────────────────────────────────────────────────────────────────────────────
# Photo effects  (numpy pixel manipulation)
# ─────────────────────────────────────────────────────────────────────────────
def build_exposure_surface(base_arr, iso, f_num, t_sec):
    """
    Apply exposure effects to base_arr (numpy W×H×3 uint8).
    Returns a pygame.Surface.

    Order of operations (physically motivated):
      1. Vignette   – wide aperture → edge darkening (DoF)
      2. Motion blur – slow shutter → horizontal kernel blur
      3. Brightness  – overall EV scaling
      4. Noise grain – ISO amplification artefact
    """
    W, H = base_arr.shape[0], base_arr.shape[1]
    arr = base_arr.astype(np.float32)

    # ── 1. Vignette (shallow DoF indicator) ─────────────────────────────────
    if f_num < 4.0:
        strength = (4.0 - f_num) / 4.0 * 0.72     # 0 @ f/4 … 0.72 @ f/1.4
        x = np.arange(W, dtype=np.float32).reshape(W, 1)
        y = np.arange(H, dtype=np.float32).reshape(1, H)
        r = np.sqrt(((x - W * 0.5) / (W * 0.5)) ** 2
                  + ((y - H * 0.5) / (H * 0.5)) ** 2)
        vignette = np.clip(1.0 - strength * r, 0.1, 1.0)[:, :, np.newaxis]
        arr *= vignette

    # ── 2. Motion blur (slow shutter = camera shake) ─────────────────────────
    blur_stops = math.log2(max(t_sec / 0.02, 1.0))    # onset at 1/50 s
    blur_px    = int(clamp(blur_stops * 7.0, 0.0, 40.0))
    if blur_px > 1:
        ks  = blur_px
        pad = np.pad(arr, ((ks // 2, ks - ks // 2), (0, 0), (0, 0)),
                     mode='edge')
        cs  = np.cumsum(pad, axis=0, dtype=np.float32)
        arr = (cs[ks:] - cs[:-ks]) / ks
        arr = arr[:W, :H]   # trim to original size

    # ── 3. Brightness (EV offset) ────────────────────────────────────────────
    ev  = ev_offset(iso, f_num, t_sec)
    brt = clamp(2.0 ** (ev * 0.80), 0.05, 7.0)
    arr *= brt

    # ── 4. Grain / noise (ISO) ───────────────────────────────────────────────
    iso_stops = math.log2(iso / ISO_MIN)            # 0 @ ISO 100 … 6 @ ISO 6400
    noise_amp = iso_stops / math.log2(ISO_MAX / ISO_MIN) * 58.0
    if noise_amp > 1.0:
        noise = np.random.default_rng().integers(
            -int(noise_amp), int(noise_amp) + 1,
            size=arr.shape, dtype=np.int16
        ).astype(np.float32)
        arr += noise

    arr = np.clip(arr, 0, 255).astype(np.uint8)

    surf = pygame.Surface((W, H))
    pygame.surfarray.blit_array(surf, arr)
    return surf


# ─────────────────────────────────────────────────────────────────────────────
# Slider widget
# ─────────────────────────────────────────────────────────────────────────────
class Slider:
    """Normalised slider: value ∈ [0.0, 1.0]."""

    def __init__(self, x, y, w, h, init_val, label, color):
        self.rect      = pygame.Rect(x, y, w, h)
        self.value     = float(clamp(init_val))
        self.label     = label
        self.color     = color
        self.dragging  = False
        self.handle_r  = 10

    @property
    def handle_x(self):
        return int(self.rect.x + self.value * self.rect.w)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if math.hypot(event.pos[0] - self.handle_x,
                          event.pos[1] - self.rect.centery) < self.handle_r + 5:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.value = clamp(
                (event.pos[0] - self.rect.x) / max(self.rect.w, 1)
            )

    def draw(self, surf, val_str, font_sm, font_xs):
        cy = self.rect.centery
        # Track
        pygame.draw.rect(surf, SLIDER_BG,
                         (self.rect.x, cy - 3, self.rect.w, 6), border_radius=3)
        # Fill
        fw = int(self.value * self.rect.w)
        if fw > 0:
            pygame.draw.rect(surf, self.color,
                             (self.rect.x, cy - 3, fw, 6), border_radius=3)
        # Handle
        pygame.draw.circle(surf, self.color, (self.handle_x, cy), self.handle_r)
        pygame.draw.circle(surf, TEXT_COLOR, (self.handle_x, cy), self.handle_r, 1)
        # Labels
        lbl = font_sm.render(self.label, True, TEXT_COLOR)
        val = font_sm.render(val_str, True, self.color)
        surf.blit(lbl, (self.rect.x, self.rect.y - 22))
        surf.blit(val, (self.rect.right - val.get_width(), self.rect.y - 22))


# ─────────────────────────────────────────────────────────────────────────────
# Drawing helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_bar(surf, x, y, w, h, val, color):
    pygame.draw.rect(surf, SLIDER_BG, (x, y, w, h), border_radius=3)
    fw = int(clamp(val) * w)
    if fw > 0:
        pygame.draw.rect(surf, color, (x, y, fw, h), border_radius=3)


def draw_panel(surf, rect, title, font_md):
    pygame.draw.rect(surf, PANEL_COLOR, rect, border_radius=8)
    pygame.draw.rect(surf, BORDER_COLOR, rect, 1, border_radius=8)
    y = rect.y + PANEL_PAD
    if title:
        t = font_md.render(title, True, GOLD)
        surf.blit(t, (rect.x + PANEL_PAD, y))
        y += t.get_height() + 4
    return y


def draw_asfid_panel(surf, rect, asfid, base, font_md, font_sm, font_xs):
    y = draw_panel(surf, rect, "ASFID  (Eagle Eye · Territory)", font_md)
    x = rect.x + PANEL_PAD
    bw = rect.w - PANEL_PAD * 2 - 36
    dims = [("A", asfid[0], base[0], (255, 180,  60)),
            ("S", asfid[1], base[1], (100, 200, 255)),
            ("F", asfid[2], base[2], ( 60, 200, 160)),
            ("I", asfid[3], base[3], (200, 130, 255)),
            ("D", asfid[4], base[4], (255, 100, 100))]
    for d, val, bval, col in dims:
        surf.blit(font_sm.render(d, True, col), (x, y + 1))
        draw_bar(surf, x + 22, y, bw, 14, val, col)
        # Base marker (poclet reference)
        bx = x + 22 + int(bval * bw)
        pygame.draw.line(surf, (200, 200, 200), (bx, y), (bx, y + 14), 1)
        surf.blit(font_xs.render(f"{val:.2f}", True, col),
                  (x + 22 + bw + 4, y))
        y += 22


def draw_revoi_panel(surf, rect, revoi, font_md, font_sm, font_xs):
    y = draw_panel(surf, rect, "REVOI  (Sphinx Eye · Map)", font_md)
    x = rect.x + PANEL_PAD
    bw = rect.w - PANEL_PAD * 2 - 36
    dims = [("R", revoi[0], (100, 180, 255)),
            ("E", revoi[1], (180, 255, 120)),
            ("V", revoi[2], (255, 220,  80)),
            ("O", revoi[3], (255, 130, 200)),
            ("I", revoi[4], (130, 220, 255))]
    for d, val, col in dims:
        surf.blit(font_sm.render(d, True, col), (x, y + 1))
        draw_bar(surf, x + 22, y, bw, 14, val, col)
        surf.blit(font_xs.render(f"{val:.2f}", True, col),
                  (x + 22 + bw + 4, y))
        y += 22
    mean = sum(v for _, v, _ in dims) / 5.0
    surf.blit(font_xs.render(f"mean = {mean:.2f}", True, REVOI_COLOR), (x, y + 2))


def draw_status_panel(surf, rect, ev, iso, f_num, t_sec, font_md, font_sm, font_xs):
    y = draw_panel(surf, rect, "Status", font_md)
    x = rect.x + PANEL_PAD

    # EV state
    if abs(ev) < 0.5:
        ev_col, ev_txt = GREEN, "✓ Correct exposure"
    elif ev > 0:
        ev_col, ev_txt = RED,      f"↑ Over  {ev:+.1f} EV"
    else:
        ev_col, ev_txt = BLUE_DARK, f"↓ Under {ev:+.1f} EV"
    s = font_sm.render(ev_txt, True, ev_col)
    surf.blit(s, (x, y)); y += s.get_height() + 8

    # Trade-off warnings
    tof_lbl = font_xs.render("Active trade-offs:", True, GOLD)
    surf.blit(tof_lbl, (x, y)); y += tof_lbl.get_height() + 4

    warnings = []
    if iso >= 1600:
        warnings.append(("Grain / noise (high ISO)", ISO_COLOR))
    if f_num <= 2.8:
        warnings.append(("Shallow DoF (wide aperture)", APT_COLOR))
    if f_num >= 11:
        warnings.append(("Diffraction softening (f/11+)", APT_COLOR))
    if t_sec >= 1.0 / 60:
        warnings.append(("Camera shake risk", SHT_COLOR))
    if t_sec >= 1.0 / 30:
        warnings.append(("Need tripod (≥ 1/30 s)", SHT_COLOR))

    for txt, col in warnings:
        ws = font_xs.render(f"  ⚠ {txt}", True, col)
        surf.blit(ws, (x, y)); y += ws.get_height() + 2
    if not warnings:
        ns = font_xs.render("  None significant", True, DIM_COLOR)
        surf.blit(ns, (x, y)); y += ns.get_height() + 2

    y += 8
    # Fixed info
    for txt in ("ΔΘ (Map–Territory) ≈ 0.32",
                "Metaconcepts: 22 / 72  (30%)"):
        surf.blit(font_xs.render(txt, True, DIM_COLOR), (x, y))
        y += font_xs.get_height() + 3

    # Balance formula reminder
    y += 6
    f1 = font_xs.render("Balance:  log₂(ISO) + log₂(1/f²)", True, (100, 140, 200))
    f2 = font_xs.render("        + log₂(T)  =  const",       True, (100, 140, 200))
    surf.blit(f1, (x, y)); surf.blit(f2, (x, y + font_xs.get_height() + 1))


# ─────────────────────────────────────────────────────────────────────────────
# Exposure Triangle diagram
# ─────────────────────────────────────────────────────────────────────────────
def draw_exposure_triangle(surf, cx, cy, size, iso, f_num, t_sec, ev, font_sm, font_xs):
    """
    Equilateral triangle:
      Top       → ISO   (teal)
      Bottom-L  → Aperture (amber)
      Bottom-R  → Shutter  (violet)

    Interior filled with exposure-state colour:
      Underexposed (ev < 0): dark indigo
      Correct (ev ≈ 0):      amber-gold
      Overexposed (ev > 0):  blown white
    Edges always retain their parameter color.
    """
    h = size * math.sqrt(3) / 2
    pts = [
        (cx,            cy - h * 2 / 3),   # top    ISO
        (cx - size / 2, cy + h / 3),        # BL     Aperture
        (cx + size / 2, cy + h / 3),        # BR     Shutter
    ]

    # ── Fill color (EV state) ─────────────────────────────────────────────
    t = clamp((ev + 3.0) / 6.0)      # map ev ∈ [-3, +3] → t ∈ [0, 1]
    if t < 0.5:
        f = t / 0.5
        fill_col = (int(25  + f * (255 - 25)),
                    int(30  + f * (175 - 30)),
                    int(110 + f * (20  - 110)))
    else:
        f = (t - 0.5) / 0.5
        fill_col = (255,
                    int(175 + f * (255 - 175)),
                    int(20  + f * (255 - 20)))

    fill_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(fill_surf, (*fill_col, 155), pts)
    surf.blit(fill_surf, (0, 0))

    # ── Edges (blended between adjacent vertex colors) ────────────────────
    vcols = [ISO_COLOR, APT_COLOR, SHT_COLOR]
    for i in range(3):
        j   = (i + 1) % 3
        c1, c2 = vcols[i], vcols[j]
        ecol = tuple((c1[k] + c2[k]) // 2 for k in range(3))
        for gw in range(6, 0, -2):
            pygame.draw.line(surf, ecol, pts[i], pts[j], gw)
        pygame.draw.line(surf, ecol, pts[i], pts[j], 2)

    # ── Vertex dots + value labels ─────────────────────────────────────────
    val_labels = [fmt_iso(iso), fmt_fnum(f_num), fmt_shutter(t_sec)]
    nudge      = [(0, -1.25), (-1.1, 1.0), (1.1, 1.0)]   # outward nudge per vertex
    for i, (px, py) in enumerate(pts):
        pygame.draw.circle(surf, vcols[i], (int(px), int(py)), 8)
        pygame.draw.circle(surf, TEXT_COLOR, (int(px), int(py)), 8, 1)
        lsf = font_xs.render(val_labels[i], True, vcols[i])
        nx, ny = nudge[i]
        surf.blit(lsf, (int(px + nx * 24) - lsf.get_width() // 2,
                        int(py + ny * 18) - lsf.get_height() // 2))

    # ── Center EV label ───────────────────────────────────────────────────
    if abs(ev) < 0.5:
        ev_col = GREEN
        ev_txt = "EV ±0"
    else:
        ev_col = RED if ev > 0 else BLUE_DARK
        ev_txt = f"EV {ev:+.1f}"

    brightness = fill_col[0] * 0.299 + fill_col[1] * 0.587 + fill_col[2] * 0.114
    txt_col = (20, 20, 20) if brightness > 155 else TEXT_COLOR

    ev_s = font_sm.render(ev_txt, True, ev_col)
    surf.blit(ev_s, (cx - ev_s.get_width() // 2, cy - ev_s.get_height() // 2))


# ─────────────────────────────────────────────────────────────────────────────
# Poclet JSON-LD loader
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    'label':  'Exposure Triangle (Photography)',
    'domain': 'Photography',
    'asfid':  [0.80, 0.85, 0.95, 0.75, 0.60],
    'revoi':  [0.95, 0.85, 0.95, 0.95, 0.90],
}


def load_poclet(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        node = data.get('@graph', [{}])[0]

        territory = node.get('m0:territorySpace', {})
        a = territory.get('asfidState', {})
        asfid = [float(a.get(k, d))
                 for k, d in zip('ASFID', _DEFAULTS['asfid'])]

        revoi_raw = node.get('m0:revoiAnalysis', {}).get('revoiState', {})
        revoi = [float(revoi_raw.get(k, d))
                 for k, d in zip('REVOI', _DEFAULTS['revoi'])]

        return {
            'label':  node.get('rdfs:label', _DEFAULTS['label']),
            'domain': node.get('m0:domain',  _DEFAULTS['domain']),
            'asfid':  asfid,
            'revoi':  revoi,
        }
    except Exception as ex:
        print(f"[TSCG] Cannot parse poclet: {ex} — using built-in defaults")
        return _DEFAULTS.copy()


def find_file(name, extra_dirs=()):
    """Search for a file next to this script, cwd, and extra_dirs."""
    candidates = [
        Path(__file__).parent / name,
        Path.cwd() / name,
        *[Path(d) / name for d in extra_dirs],
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def find_poclet_path():
    if POCLET_PATH_OVERRIDE:
        return Path(POCLET_PATH_OVERRIDE)
    # Walk up to repo root
    cur = Path(__file__).resolve().parent
    for _ in range(8):
        candidate = (cur / "instances" / "poclets"
                        / "exposure_triangle" / "M0_ExposureTriangle.jsonld")
        if candidate.exists():
            return candidate
        nxt = cur.parent
        if nxt == cur:
            break
        cur = nxt
    return find_file("M0_ExposureTriangle.jsonld")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # ── Load poclet ──────────────────────────────────────────────────────────
    poclet_path = find_poclet_path()
    if poclet_path:
        print(f"[TSCG] Poclet  : {poclet_path}")
        poclet = load_poclet(poclet_path)
    else:
        print("[TSCG] M0_ExposureTriangle.jsonld not found — using defaults")
        poclet = _DEFAULTS.copy()
    print(f"[TSCG] Label   : {poclet['label']}")
    print(f"[TSCG] ASFID   : {poclet['asfid']}")
    print(f"[TSCG] REVOI   : {poclet['revoi']}")

    # ── Load photo ───────────────────────────────────────────────────────────
    photo_path = find_file("photo_sample.jpg")
    if photo_path:
        print(f"[TSCG] Photo   : {photo_path}")
    else:
        print("[TSCG] photo_sample.jpg not found — using gradient placeholder")

    # ── Pygame ───────────────────────────────────────────────────────────────
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(f"TSCG Simulation · {poclet['label']}")
    clock  = pygame.time.Clock()

    font_lg = pygame.font.SysFont("segoeui", 20, bold=True)
    font_md = pygame.font.SysFont("segoeui", 15, bold=True)
    font_sm = pygame.font.SysFont("segoeui", 13)
    font_xs = pygame.font.SysFont("segoeui", 11)

    # ── Build base image array ───────────────────────────────────────────────
    if photo_path:
        raw    = pygame.image.load(str(photo_path)).convert()
        img_sf = pygame.transform.scale(raw, (IMG_DISPLAY_W, IMG_DISPLAY_H))
    else:
        # Gradient placeholder
        img_sf = pygame.Surface((IMG_DISPLAY_W, IMG_DISPLAY_H))
        for xi in range(IMG_DISPLAY_W):
            g = int(xi / IMG_DISPLAY_W * 200) + 20
            pygame.draw.line(img_sf, (g, g, g), (xi, 0), (xi, IMG_DISPLAY_H))
    base_arr = pygame.surfarray.array3d(img_sf).copy()  # W×H×3 uint8

    # ── Sliders  (initial positions = baseline exposure) ─────────────────────
    iso_init = math.log(BASELINE_ISO / ISO_MIN) / math.log(ISO_MAX / ISO_MIN)
    apt_init = math.log(BASELINE_F   / F_MIN)   / math.log(F_MAX   / F_MIN)
    sht_init = math.log(BASELINE_T   / T_MIN)   / math.log(T_MAX   / T_MIN)

    sw = LEFT_W - PANEL_PAD * 4
    sliders = {
        'iso':      Slider(PANEL_PAD * 2, 120, sw, 20, iso_init,
                           "ISO Sensitivity",  ISO_COLOR),
        'aperture': Slider(PANEL_PAD * 2, 210, sw, 20, apt_init,
                           "Aperture (f-stop)", APT_COLOR),
        'shutter':  Slider(PANEL_PAD * 2, 300, sw, 20, sht_init,
                           "Shutter Speed",    SHT_COLOR),
    }

    # Effect cache
    processed_surf = None
    prev_sv        = (-1.0, -1.0, -1.0)

    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            for s in sliders.values():
                s.handle_event(event)

        # Physical values
        iso   = iso_from_slider(sliders['iso'].value)
        f_num = fnum_from_slider(sliders['aperture'].value)
        t_sec = t_from_slider(sliders['shutter'].value)
        ev    = ev_offset(iso, f_num, t_sec)

        # Recompute image only on slider change
        sv = (round(sliders['iso'].value, 3),
              round(sliders['aperture'].value, 3),
              round(sliders['shutter'].value, 3))
        if sv != prev_sv:
            processed_surf = build_exposure_surface(base_arr, iso, f_num, t_sec)
            prev_sv = sv

        # Dynamic ASFID modulation around poclet base values
        base_a   = poclet['asfid']
        iso_frac = (iso   - ISO_MIN) / (ISO_MAX - ISO_MIN)
        apt_frac = 1.0 - (f_num - F_MIN)  / (F_MAX  - F_MIN)   # wide = 1
        sht_frac = (t_sec - T_MIN) / (T_MAX  - T_MIN)
        ev_frac  = clamp(1.0 - abs(ev) / 5.0)                   # best at ev≈0
        asfid_live = [
            clamp(base_a[0] * (0.4 + 0.6 * ev_frac)),           # A: peaks at correct EV
            clamp(base_a[1] * (0.5 + 0.5 * apt_frac)),          # S: aperture structure
            clamp(base_a[2] * (0.2 + 0.8 * apt_frac)),          # F: photon flux ~ aperture
            clamp(base_a[3] * (0.3 + 0.7 * iso_frac)),          # I: signal gain
            clamp(base_a[4] * (0.1 + 0.9 * sht_frac)),          # D: temporal dynamics
        ]

        # ── Draw ─────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # ── Left panel ───────────────────────────────────────────────────────
        pygame.draw.rect(screen, PANEL_COLOR, (0, 0, LEFT_W, WINDOW_H))
        pygame.draw.line(screen, BORDER_COLOR, (LEFT_W, 0), (LEFT_W, WINDOW_H))

        # Title
        title_s = font_lg.render("📷 " + poclet['label'].split("(")[0].strip(),
                                  True, GOLD)
        screen.blit(title_s, (PANEL_PAD + 4, PANEL_PAD + 4))
        dom_s = font_xs.render(f"Domain: {poclet['domain']}", True, DIM_COLOR)
        screen.blit(dom_s, (PANEL_PAD + 4,
                             PANEL_PAD + 4 + title_s.get_height() + 2))

        sep_y = PANEL_PAD + title_s.get_height() + dom_s.get_height() + 20
        pygame.draw.line(screen, BORDER_COLOR,
                         (PANEL_PAD, sep_y), (LEFT_W - PANEL_PAD, sep_y))
        ctrl_s = font_md.render("Parameter Controls", True, TEXT_COLOR)
        screen.blit(ctrl_s, (PANEL_PAD + 4, sep_y + 6))

        sliders['iso'].draw(screen,      fmt_iso(iso),    font_sm, font_xs)
        sliders['aperture'].draw(screen, fmt_fnum(f_num), font_sm, font_xs)
        sliders['shutter'].draw(screen,  fmt_shutter(t_sec), font_sm, font_xs)

        # ── EV bar ───────────────────────────────────────────────────────────
        ev_y = sliders['shutter'].rect.bottom + 24
        pygame.draw.line(screen, BORDER_COLOR,
                         (PANEL_PAD, ev_y - 8), (LEFT_W - PANEL_PAD, ev_y - 8))
        screen.blit(font_md.render("Exposure Value", True, TEXT_COLOR),
                    (PANEL_PAD + 4, ev_y))
        ev_y += font_md.get_height() + 8

        bar_x = PANEL_PAD + 4
        bar_w = LEFT_W - PANEL_PAD * 2 - 8
        bar_h = 14
        pygame.draw.rect(screen, SLIDER_BG,
                         (bar_x, ev_y, bar_w, bar_h), border_radius=3)
        cx_bar = bar_x + bar_w // 2
        pygame.draw.line(screen, (80, 80, 100),
                         (cx_bar, ev_y - 2), (cx_bar, ev_y + bar_h + 2), 1)
        ev_t = clamp((ev + 4.0) / 8.0)
        fill_x = int(bar_x + ev_t * bar_w)
        if ev > 0.1:
            fw = fill_x - cx_bar
            if fw > 0:
                pygame.draw.rect(screen, RED,
                                 (cx_bar, ev_y, fw, bar_h), border_radius=3)
        elif ev < -0.1:
            fw = cx_bar - fill_x
            if fw > 0:
                pygame.draw.rect(screen, BLUE_DARK,
                                 (fill_x, ev_y, fw, bar_h), border_radius=3)
        else:
            pygame.draw.rect(screen, GREEN,
                             (cx_bar - 3, ev_y, 6, bar_h), border_radius=2)

        ev_col = (GREEN if abs(ev) < 0.5 else (GOLD if abs(ev) < 2 else RED))
        ev_val_s = font_xs.render(f"EV {ev:+.2f}", True, ev_col)
        screen.blit(ev_val_s,
                    (cx_bar - ev_val_s.get_width() // 2, ev_y + bar_h + 3))
        screen.blit(font_xs.render("Under", True, BLUE_DARK),
                    (bar_x, ev_y + bar_h + 3))
        screen.blit(font_xs.render("Over",  True, RED),
                    (bar_x + bar_w - font_xs.size("Over")[0], ev_y + bar_h + 3))

        bl_y = ev_y + bar_h + 22
        screen.blit(
            font_xs.render(
                f"Baseline: ISO{int(BASELINE_ISO)} · f/{BASELINE_F} · 1/250s",
                True, DIM_COLOR),
            (PANEL_PAD + 4, bl_y))

        # ── Center panel ─────────────────────────────────────────────────────
        mid_x = LEFT_W
        pygame.draw.rect(screen, (16, 16, 24),
                         (mid_x, 0, MID_W, WINDOW_H))

        ct = font_md.render("Territory Simulation  ·  Live Photo Effects",
                             True, DIM_COLOR)
        screen.blit(ct, (mid_x + MID_W // 2 - ct.get_width() // 2, 7))

        # Photo
        img_x = mid_x + (MID_W - IMG_DISPLAY_W) // 2
        img_y = 28
        if processed_surf:
            screen.blit(processed_surf, (img_x, img_y))
        pygame.draw.rect(screen, BORDER_COLOR,
                         (img_x - 1, img_y - 1,
                          IMG_DISPLAY_W + 2, IMG_DISPLAY_H + 2), 1)

        # Effects legend strip
        eff_y = img_y + IMG_DISPLAY_H + 5
        iso_stops = math.log2(iso / ISO_MIN)
        noise_pct = iso_stops / math.log2(ISO_MAX / ISO_MIN) * 100
        blur_stops = math.log2(max(t_sec / 0.02, 1.0))
        blur_pct  = clamp(blur_stops / 5.0) * 100
        vig_pct   = max(0.0, (4.0 - f_num) / 4.0 * 100) if f_num < 4.0 else 0.0

        legends = [
            (f"Grain: {noise_pct:.0f}%",         ISO_COLOR),
            (f"Motion blur: {blur_pct:.0f}%",    SHT_COLOR),
            (f"Vignette (DoF): {vig_pct:.0f}%",  APT_COLOR),
        ]
        lx = img_x
        for txt, col in legends:
            ls = font_xs.render(txt, True, col)
            screen.blit(ls, (lx, eff_y))
            lx += ls.get_width() + 28

        # Exposure triangle diagram
        tri_cx = mid_x + MID_W // 2
        tri_cy = eff_y + 96
        draw_exposure_triangle(screen, tri_cx, tri_cy, 115,
                               iso, f_num, t_sec, ev, font_sm, font_xs)

        # Source label
        src_s = font_xs.render("Source: M0_ExposureTriangle.jsonld", True, (50, 50, 70))
        screen.blit(src_s, (mid_x + 6, WINDOW_H - 16))

        # ── Right panel ───────────────────────────────────────────────────────
        rp_x = LEFT_W + MID_W
        pygame.draw.rect(screen, PANEL_COLOR, (rp_x, 0, RIGHT_W, WINDOW_H))
        pygame.draw.line(screen, BORDER_COLOR, (rp_x, 0), (rp_x, WINDOW_H))

        asfid_rect  = pygame.Rect(rp_x + 2,  4, RIGHT_W - 4, 172)
        revoi_rect  = pygame.Rect(rp_x + 2,  asfid_rect.bottom + 4, RIGHT_W - 4, 165)
        status_rect = pygame.Rect(rp_x + 2,  revoi_rect.bottom + 4,
                                   RIGHT_W - 4, WINDOW_H - revoi_rect.bottom - 8)

        draw_asfid_panel(screen, asfid_rect, asfid_live,
                          poclet['asfid'], font_md, font_sm, font_xs)
        draw_revoi_panel(screen, revoi_rect, poclet['revoi'],
                          font_md, font_sm, font_xs)
        draw_status_panel(screen, status_rect, ev,
                           iso, f_num, t_sec, font_md, font_sm, font_xs)

        # FPS
        fps_s = font_xs.render(f"FPS: {int(clock.get_fps())}", True, (45, 45, 65))
        screen.blit(fps_s, (LEFT_W + 4, WINDOW_H - 16))

        pygame.display.flip()

    pygame.quit()
    print("[TSCG] Simulation ended.")


if __name__ == "__main__":
    main()
