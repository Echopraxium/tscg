"""
complex_chemical_synapse_sim.py  v1.0
======================================
TSCG Poclet Simulation -- Complex Chemical Synapse (5-Pole Model)
Author: Echopraxium with the collaboration of Claude AI

Animated real-time simulation of the 5-pole synaptic transmission cycle:
  Synthesis --> Storage --> Release --> Reception --> Termination

Features:
  - Animated synaptic signal diagram: NT cleft concentration + Postsynaptic Potential (PSP)
  - Synapse cross-section schematic with animated vesicles, Ca2+ channels, and receptors
  - Live ASFID bars (Eagle Eye / Territory) -- dynamic with transmission phase
  - Static REVOI bars (Sphinx Eye / Map)
  - Parameter sliders: Frequency (Hz), Ca2+ Level, Reuptake Rate
  - Clickable pole table to jump to any phase
  - Live readouts: NT_cleft, PSP amplitude, vesicle pool fill level
  - Playback controls: pause/play button + speed multiplier buttons
  - Step-by-step mode: arrow keys advance/rewind by 5 deg (Shift = 30 deg)
  - Speed via keyboard: < / > keys cycle through speed steps

Keyboard shortcuts:
  SPACE       -- pause / resume
  <- / ->     -- step -5 / +5 degrees (only while paused)
  Shift+<-/-> -- step -30 / +30 degrees (only while paused)
  , / .       -- decrease / increase sim speed
  ESC         -- quit

Requirements:  pip install pygame
Run:
    python complex_chemical_synapse_sim.py
    python complex_chemical_synapse_sim.py path/to/M0_ComplexChemicalSynapse.jsonld
"""

import sys, math, json, random
from pathlib import Path
from enum import Enum, auto
import pygame

# ─────────────────────────────────────────────────────────────────────────────
# Window / layout constants
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H  = 1260, 740
FPS                  = 60
POCLET_OVERRIDE      = sys.argv[1] if len(sys.argv) > 1 else None

LEFT_W   = 300
RIGHT_W  = 230
MID_W    = WINDOW_W - LEFT_W - RIGHT_W   # 730
PAD      = 12

# ─────────────────────────────────────────────────────────────────────────────
# Colour palette
# ─────────────────────────────────────────────────────────────────────────────
BG          = (12,  12,  18)
PANEL_BG    = (22,  22,  32)
BORDER      = (55,  55,  75)
TEXT        = (220, 220, 230)
DIM         = (130, 130, 150)
GOLD        = (255, 200,  50)
GREEN_OK    = ( 80, 200, 120)
RED_WARN    = (220,  60,  60)
SLIDER_BG   = ( 38,  38,  52)
REVOI_COL   = (120, 180, 255)

# Pole colours
C_SYNTH  = ( 40, 200,  80)   # green      — Pole 1 Synthesis
C_STORE  = (220, 190,  50)   # amber      — Pole 2 Storage
C_REL    = (255,  85,  55)   # red-orange — Pole 3 Release
C_RECEP  = ( 65, 160, 255)   # blue       — Pole 4 Reception
C_TERM   = (180,  80, 230)   # purple     — Pole 5 Termination

POLE_COLORS = [C_SYNTH, C_STORE, C_REL, C_RECEP, C_TERM]

# Slider accent colours
FREQ_COL    = ( 80, 210, 210)
CA_COL      = (255, 175,  45)
REUP_COL    = (200, 110, 255)

# Playback
SPEED_COL   = (160, 220,  80)
SPEED_STEPS = [0.002, 0.005, 0.008, 0.025, 0.05, 0.25]
STEP_FINE   = 15.0    # ~1/24 cycle — clearly visible
STEP_COARSE = 60.0    # one full pole boundary

# ─────────────────────────────────────────────────────────────────────────────
# FSM — Simulation states
# ─────────────────────────────────────────────────────────────────────────────
class SimState(Enum):
    PLAYING = auto()
    PAUSED  = auto()

# ─────────────────────────────────────────────────────────────────────────────
# Pole definitions  (label, color, phase_start, phase_end, short_note)
# ─────────────────────────────────────────────────────────────────────────────
POLES = [
    ("Synthesis",    C_SYNTH, 0,   72,  "NT molecules produced"),
    ("Storage",      C_STORE, 72,  144, "NT loaded into vesicles"),
    ("Release",      C_REL,   144, 216, "Ca2+ triggers exocytosis"),
    ("Reception",    C_RECEP, 216, 288, "NT binds postsynaptic receptors"),
    ("Termination",  C_TERM,  288, 360, "Reuptake + degradation"),
]

# ─────────────────────────────────────────────────────────────────────────────
# Physics constants
# ─────────────────────────────────────────────────────────────────────────────
FREQ_MIN,  FREQ_MAX  = 1.0,   100.0   # Hz
CA_MIN,    CA_MAX    = 0.1,   1.0     # Ca2+ level (normalised)
REUP_MIN,  REUP_MAX  = 0.1,   1.0    # reuptake rate (normalised)


def phase_to_pole_idx(phase_deg):
    """Return pole index 0-4 for given phase angle 0-360."""
    p = phase_deg % 360.0
    if p <  72: return 0   # Synthesis
    if p < 144: return 1   # Storage
    if p < 216: return 2   # Release
    if p < 288: return 3   # Reception
    return 4               # Termination


def synapse_signals(phase_deg, ca, reuptake):
    """
    Compute NT cleft concentration and PSP at given phase angle.

    NT_cleft(theta):
      - [0, 144]   : residual from previous cycle decaying from 1.0 to ~0
      - [144, 216] : release — rises sinusoidally to peak at ~198 deg, scaled by Ca
      - [216, 360] : exponential decay scaled by reuptake rate

    PSP(theta):
      - [0, 216]   : near-baseline (leakage from previous cycle)
      - [216, 288] : rises to peak — proportional to Ca, EPSP-like
      - [288, 360] : decays back to baseline
    """
    theta = phase_deg % 360.0

    # ── NT cleft concentration ──────────────────────────────────────────
    if theta < 144:
        # Residual from previous cycle (exponential tail from theta=288..360 → 0..144)
        prev_theta = theta + (360 - 288)  # 0..144 maps to 72..216 of previous decay
        nt = ca * math.exp(-reuptake * 5.0 * (prev_theta / 144.0))
    elif theta < 216:
        # Release phase: sinusoidal rise to peak at ~195 deg, then slight decline
        frac = (theta - 144.0) / 72.0      # 0→1 over release phase
        # Peak at frac=0.7 (theta ~195 deg): use sin²(pi*frac) modulated
        nt = ca * math.sin(math.pi * frac) ** 1.2
    else:
        # Termination: exponential decay from peak
        frac = (theta - 216.0) / 144.0    # 0→1 over termination phase
        nt = ca * math.exp(-reuptake * 4.5 * frac)

    # ── Postsynaptic Potential ──────────────────────────────────────────
    if theta < 216:
        # Small residual PSP from previous cycle
        psp_prev_frac = theta / 216.0
        psp = 0.15 * ca * (1.0 - psp_prev_frac) * math.exp(-2.0 * psp_prev_frac)
    elif theta < 288:
        # EPSP build-up: rapid rise, reflects NT_cleft with slight delay
        frac = (theta - 216.0) / 72.0
        psp = 0.9 * ca * math.sin(math.pi * frac * 0.8 + 0.1) ** 0.7
    else:
        # PSP decay (slower than NT clearance — membrane time constant)
        frac = (theta - 288.0) / 72.0
        psp = 0.9 * ca * math.exp(-2.0 * frac)

    nt  = max(0.0, min(1.0, nt))
    psp = max(0.0, min(1.0, psp))
    return nt, psp


def vesicle_pool(phase_deg):
    """Vesicle pool fill level 0..1 — depletes during Release, refills during Synthesis."""
    theta = phase_deg % 360.0
    if theta < 72:    # Synthesis: refilling
        return 0.3 + 0.7 * (theta / 72.0)
    elif theta < 144:  # Storage: full
        return 1.0
    elif theta < 216:  # Release: depletion
        frac = (theta - 144.0) / 72.0
        return 1.0 - 0.7 * math.sin(math.pi * frac * 0.7)
    else:              # Post-release: partially depleted, slowly refilling
        frac = (theta - 216.0) / 144.0
        return 0.3 + 0.3 * frac
    return 0.3


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


# ─────────────────────────────────────────────────────────────────────────────
# Slider widget
# ─────────────────────────────────────────────────────────────────────────────
class Slider:
    def __init__(self, x, y, w, vmin, vmax, init, label, unit, color):
        self.rect  = pygame.Rect(x, y, w, 20)
        self.vmin, self.vmax = float(vmin), float(vmax)
        self.value = float(init)
        self.label, self.unit, self.color = label, unit, color
        self.dragging = False

    @property
    def ratio(self): return (self.value - self.vmin) / (self.vmax - self.vmin)
    @property
    def hx(self):    return int(self.rect.x + self.ratio * self.rect.w)

    def handle_event(self, e):
        cy = self.rect.centery
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if math.hypot(e.pos[0] - self.hx, e.pos[1] - cy) < 15:
                self.dragging = True
        elif e.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            r = (e.pos[0] - self.rect.x) / max(self.rect.w, 1)
            self.value = clamp(self.vmin + r * (self.vmax - self.vmin),
                               self.vmin, self.vmax)

    def draw(self, surf, font_sm, val_str=None):
        cy = self.rect.centery
        if val_str is None:
            val_str = f"{self.value:.2f} {self.unit}"
        pygame.draw.rect(surf, SLIDER_BG, (self.rect.x, cy - 3, self.rect.w, 6),
                         border_radius=3)
        fw = int(self.ratio * self.rect.w)
        if fw > 0:
            pygame.draw.rect(surf, self.color, (self.rect.x, cy - 3, fw, 6),
                             border_radius=3)
        pygame.draw.circle(surf, self.color, (self.hx, cy), 10)
        pygame.draw.circle(surf, TEXT,       (self.hx, cy), 10, 1)
        surf.blit(font_sm.render(self.label, True, TEXT),
                  (self.rect.x, self.rect.y - 20))
        v = font_sm.render(val_str, True, self.color)
        surf.blit(v, (self.rect.right - v.get_width(), self.rect.y - 20))


# ─────────────────────────────────────────────────────────────────────────────
# Pole table  (clickable, like stroke table)
# ─────────────────────────────────────────────────────────────────────────────
def draw_pole_table(surf, x, y, w, active_idx, hover_label, font_sm, font_xs):
    row_h = 34
    gap   = 3
    rects = []
    for idx, (lbl, col, _s, _e, note) in enumerate(POLES):
        is_active = (idx == active_idx)
        is_hover  = (hover_label == lbl)
        row_rect  = pygame.Rect(x, y, w, row_h)
        rects.append((row_rect, idx))

        bg_a   = 70 if is_active else (38 if is_hover else 18)
        bord_a = 220 if is_active else (140 if is_hover else 45)
        bg = pygame.Surface((w, row_h), pygame.SRCALPHA)
        bg.fill((*col, bg_a))
        pygame.draw.rect(bg, (*col, bord_a), (0, 0, w, row_h), 2, border_radius=5)
        surf.blit(bg, (x, y))

        bcol = col if (is_active or is_hover) else tuple(c // 4 for c in col)
        pygame.draw.rect(surf, bcol, (x + 5, y + 6, 6, row_h - 12), border_radius=3)

        if is_hover and not is_active:
            hint = font_xs.render(">> click to jump", True, (*col, 200))
            surf.blit(hint, (x + w - hint.get_width() - 6, y + row_h - 14))

        tcol = TEXT if (is_active or is_hover) else DIM
        surf.blit(font_sm.render(f"{idx+1}. {lbl}", True, bcol), (x + 16, y + 2))
        surf.blit(font_xs.render(note, True, tcol), (x + 16, y + 19))

        y += row_h + gap
    return rects


# ─────────────────────────────────────────────────────────────────────────────
# Bar + panel helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_bar(surf, x, y, w, h, val, col):
    pygame.draw.rect(surf, SLIDER_BG, (x, y, w, h), border_radius=3)
    fw = int(clamp(val) * w)
    if fw > 0:
        pygame.draw.rect(surf, col, (x, y, fw, h), border_radius=3)


def draw_panel_bg(surf, rect, title, font_md):
    pygame.draw.rect(surf, PANEL_BG, rect, border_radius=8)
    pygame.draw.rect(surf, BORDER,   rect, 1, border_radius=8)
    y = rect.y + PAD
    if title:
        t = font_md.render(title, True, GOLD)
        surf.blit(t, (rect.x + PAD, y))
        y += t.get_height() + 4
    return y


def draw_asfid(surf, rect, live, base, font_md, font_sm, font_xs):
    y  = draw_panel_bg(surf, rect, "ASFID  (Eagle Eye · Territory)", font_md)
    x  = rect.x + PAD
    bw = rect.w - PAD * 2 - 38
    dim_cols = [(255,180,60),(100,200,255),(60,200,160),(200,130,255),(255,100,100)]
    for d, lv, bv, col in zip("ASFID", live, base, dim_cols):
        surf.blit(font_sm.render(d, True, col), (x, y + 1))
        draw_bar(surf, x + 22, y, bw, 14, lv, col)
        bx = x + 22 + int(bv * bw)
        pygame.draw.line(surf, (200, 200, 200), (bx, y), (bx, y + 14), 1)
        surf.blit(font_xs.render(f"{lv:.2f}", True, col), (x + 22 + bw + 4, y))
        y += 22


def draw_revoi(surf, rect, revoi, font_md, font_sm, font_xs):
    y    = draw_panel_bg(surf, rect, "REVOI  (Sphinx Eye · Map)", font_md)
    x    = rect.x + PAD
    bw   = rect.w - PAD * 2 - 38
    cols = [(100,180,255),(180,255,120),(255,220,80),(255,130,200),(130,220,255)]
    for d, v, col in zip("REVOI", revoi, cols):
        surf.blit(font_sm.render(d, True, col), (x, y + 1))
        draw_bar(surf, x + 22, y, bw, 14, v, col)
        surf.blit(font_xs.render(f"{v:.2f}", True, col), (x + 22 + bw + 4, y))
        y += 22
    surf.blit(font_xs.render(f"mean = {sum(revoi)/5:.2f}", True, REVOI_COL),
              (x, y + 2))


def draw_status(surf, rect, pole_label, pole_col, val_lines, font_md, font_sm, font_xs):
    y = draw_panel_bg(surf, rect, "Status", font_md)
    x = rect.x + PAD
    surf.blit(font_sm.render("Domain: Neurobiology", True, GOLD), (x, y)); y += 16
    surf.blit(font_sm.render(f"Pole: {pole_label}", True, pole_col), (x, y)); y += 18
    for lbl, col in val_lines:
        surf.blit(font_sm.render(lbl, True, col), (x, y)); y += 15
    y += 4
    for eq in ["NT_cleft ~ Ca*sin(pi*frac)^1.2", "PSP ~ 0.9*Ca*exp(-2*frac)"]:
        surf.blit(font_xs.render(eq, True, DIM), (x, y)); y += 13
    y += 4
    surf.blit(font_xs.render("Metaconcepts: 22 | DT=0.240", True, DIM), (x, y))


# ─────────────────────────────────────────────────────────────────────────────
# Synapse schematic  (cross-section, left panel)
# ─────────────────────────────────────────────────────────────────────────────
def draw_synapse(surf, cx, cy, phase_deg, pole_idx, ca, reuptake, ves_pool_val,
                 nt_val, psp_val, font_xs):
    """
    Draw a simplified synapse cross-section:
      - Presynaptic terminal (top box)
      - Vesicles (animated dots inside presynaptic)
      - Ca2+ channels (bottom edge of presynaptic)
      - Synaptic cleft (gap, with NT dots floating)
      - Postsynaptic membrane (bottom box, glow proportional to PSP)
      - Receptors on postsynaptic surface
    """
    pole_col = POLE_COLORS[pole_idx]

    pre_w, pre_h = 70, 55
    cleft_h      = 22
    post_h       = 28
    wall_t       = 4

    pre_x  = cx - pre_w // 2
    pre_y  = cy - pre_h - cleft_h // 2
    post_x = cx - pre_w // 2
    post_y = cy + cleft_h // 2

    # ── Presynaptic terminal background ──────────────────────────────────
    pre_surf = pygame.Surface((pre_w, pre_h), pygame.SRCALPHA)
    pre_surf.fill((*pole_col, 20 if pole_idx > 1 else 30))
    surf.blit(pre_surf, (pre_x, pre_y))
    pygame.draw.rect(surf, (70, 80, 100), (pre_x, pre_y, pre_w, pre_h), 2, border_radius=5)

    # ── Vesicles inside presynaptic ───────────────────────────────────────
    n_ves    = int(8 * ves_pool_val) + 1
    ves_cols = [
        (255, 220,  80),  # full vesicle
        (200, 170,  50),
    ]
    for vi in range(min(n_ves, 9)):
        row, col_v = divmod(vi, 3)
        vx = pre_x + 12 + col_v * 18
        vy = pre_y + 10 + row * 16
        vc = ves_cols[vi % 2]
        radius = 6

        # During release: vesicles near bottom edge drift downward
        if pole_idx == 2:
            release_frac = ((phase_deg % 360) - 144.0) / 72.0
            drift = int(release_frac * 12) if row == 2 else 0
            vy += drift
        pygame.draw.circle(surf, vc, (vx, vy), radius)
        pygame.draw.circle(surf, (240, 200, 100), (vx, vy), radius, 1)

    # Vesicle pool label
    surf.blit(font_xs.render(f"Pool:{int(ves_pool_val*100)}%", True, (200,180,80)),
              (pre_x + 2, pre_y + 2))

    # ── Ca2+ channel dots on presynaptic membrane (bottom edge) ──────────
    ca_vis = int(ca * 5)
    for ci in range(5):
        cax = pre_x + 10 + ci * 12
        cay = pre_y + pre_h - 2
        col_ca = (255, 160, 40) if (pole_idx == 2 and ci < ca_vis) else (80, 80, 110)
        pygame.draw.circle(surf, col_ca, (cax, cay), 5)

    # ── Synaptic cleft ────────────────────────────────────────────────────
    cleft_rect = pygame.Rect(pre_x, cy - cleft_h // 2, pre_w, cleft_h)
    cs = pygame.Surface((pre_w, cleft_h), pygame.SRCALPHA)
    cs.fill((20, 20, 40, 80))
    surf.blit(cs, (pre_x, cy - cleft_h // 2))

    # NT molecules drifting in cleft (during/after release)
    if nt_val > 0.05:
        n_dots = int(nt_val * 14)
        random.seed(int(phase_deg * 3.7))
        for _ in range(n_dots):
            dx = random.randint(pre_x + 4, pre_x + pre_w - 4)
            dy = random.randint(cy - cleft_h // 2 + 3, cy + cleft_h // 2 - 3)
            alpha = int(100 + nt_val * 155)
            nt_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(nt_surf, (*C_REL, alpha), (3, 3), 3)
            surf.blit(nt_surf, (dx - 3, dy - 3))

    # Cleft label
    surf.blit(font_xs.render("cleft", True, DIM),
              (pre_x + pre_w + 3, cy - 5))

    # ── Postsynaptic membrane ─────────────────────────────────────────────
    # Glow based on PSP
    if psp_val > 0.05:
        glow_s = pygame.Surface((pre_w, post_h + 8), pygame.SRCALPHA)
        glow_s.fill((*C_RECEP, int(psp_val * 60)))
        surf.blit(glow_s, (post_x, post_y - 4))

    pygame.draw.rect(surf, (50, 60, 90),
                     (post_x, post_y, pre_w, post_h), border_radius=4)
    pygame.draw.rect(surf, (80, 100, 150),
                     (post_x, post_y, pre_w, post_h), 2, border_radius=4)

    # Receptor bumps on postsynaptic surface
    n_rec = 5
    for ri in range(n_rec):
        rx = post_x + 8 + ri * 13
        ry = post_y + 2
        # Occupied receptors glow blue during reception
        occupied = (pole_idx == 3 and nt_val > 0.2 and ri < int(nt_val * n_rec + 1))
        rcol = C_RECEP if occupied else (60, 70, 100)
        pygame.draw.rect(surf, rcol, (rx, ry, 8, 10), border_radius=3)
        if occupied:
            pygame.draw.rect(surf, (130, 200, 255), (rx, ry, 8, 10), 1, border_radius=3)

    # PSP amplitude indicator
    psp_bar_w = int(psp_val * (pre_w - 4))
    pygame.draw.rect(surf, SLIDER_BG, (post_x + 2, post_y + 14, pre_w - 4, 8),
                     border_radius=3)
    if psp_bar_w > 0:
        pygame.draw.rect(surf, C_RECEP, (post_x + 2, post_y + 14, psp_bar_w, 8),
                         border_radius=3)
    surf.blit(font_xs.render(f"PSP:{psp_val:.2f}", True, C_RECEP),
              (post_x + 2, post_y + 24))


# ─────────────────────────────────────────────────────────────────────────────
# Signal diagram  (centre panel) — NT_cleft and PSP vs phase angle
# ─────────────────────────────────────────────────────────────────────────────
def px_from_val(val, rect):
    """Map normalised value 0..1 to y pixel (1 at top, 0 at bottom)."""
    return rect.bottom - int(clamp(val) * rect.h)


def phase_to_px(phase_deg, rect):
    """Map phase 0..360 to x pixel."""
    return rect.x + int((phase_deg / 360.0) * rect.w)


def draw_signal_axes(surf, rect, font_xs):
    """Draw background, grid, and axis labels for signal diagram."""
    pygame.draw.rect(surf, (14, 14, 22), rect)
    pygame.draw.rect(surf, BORDER, rect, 1)

    # Shaded pole bands
    band_alpha = 25
    for idx, (_, col, ps, pe, _) in enumerate(POLES):
        bx  = rect.x + int(ps / 360 * rect.w)
        bw  = int((pe - ps) / 360 * rect.w)
        bs  = pygame.Surface((bw, rect.h), pygame.SRCALPHA)
        bs.fill((*col, band_alpha))
        surf.blit(bs, (bx, rect.y))
        # Pole boundary line
        pygame.draw.line(surf, (*col, 60), (bx, rect.y), (bx, rect.bottom), 1)
        # Pole label at top
        lbl = font_xs.render(POLES[idx][0][:4], True, (*col, 180))
        surf.blit(lbl, (bx + 3, rect.y + 2))

    # Horizontal grid lines at 0.25, 0.5, 0.75
    for val in [0.25, 0.5, 0.75]:
        gy = px_from_val(val, rect)
        pygame.draw.line(surf, (30, 30, 42), (rect.x, gy), (rect.right, gy))
        surf.blit(font_xs.render(f"{val:.2f}", True, DIM), (rect.x - 30, gy - 5))

    # Axis labels
    surf.blit(font_xs.render("Amplitude", True, (120, 150, 110)),
              (rect.x - 28, rect.y - 12))
    surf.blit(font_xs.render("Phase (deg)", True, (140, 130, 80)),
              (rect.x + rect.w // 2 - 30, rect.bottom + 16))
    for deg in [0, 72, 144, 216, 288, 360]:
        px = phase_to_px(deg, rect)
        surf.blit(font_xs.render(f"{deg}", True, DIM), (px - 8, rect.bottom + 3))


def draw_signal_curves(surf, rect, ca, reuptake, font_xs):
    """Draw NT_cleft and PSP curves over 0–360 degrees."""
    N = 360
    nt_pts, psp_pts = [], []
    for i in range(N + 1):
        theta = i * 360.0 / N
        nt, psp = synapse_signals(theta, ca, reuptake)
        nt_pts.append( (phase_to_px(theta, rect), px_from_val(nt,  rect)) )
        psp_pts.append((phase_to_px(theta, rect), px_from_val(psp, rect)) )

    if len(nt_pts)  > 1: pygame.draw.lines(surf, C_REL,    False, nt_pts,  2)
    if len(psp_pts) > 1: pygame.draw.lines(surf, C_RECEP,  False, psp_pts, 2)

    return nt_pts, psp_pts


def draw_qpoint(surf, qx, qy, col, label, rect, font_xs):
    """Draw Q-point (animated marker) with crosshairs and halo."""
    pygame.draw.line(surf, (*col, 50), (rect.x, qy), (rect.right, qy), 1)
    pygame.draw.line(surf, (*col, 50), (qx, rect.y), (qx, rect.bottom), 1)
    for r in [13, 9, 6]:
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*col, 28 + r*8), (r, r), r)
        surf.blit(s, (qx - r, qy - r))
    pygame.draw.circle(surf, col,  (qx, qy), 7)
    pygame.draw.circle(surf, TEXT, (qx, qy), 7, 1)
    lbl = font_xs.render(label, True, col)
    surf.blit(lbl, (min(qx + 10, rect.right - lbl.get_width() - 2),
                    max(qy - 17, rect.y + 2)))


# ─────────────────────────────────────────────────────────────────────────────
# Playback controls  (identical structure to four_stroke_engine_sim)
# ─────────────────────────────────────────────────────────────────────────────
def draw_playback_controls(surf, x, y, w, paused, speed_idx, font_sm, font_xs):
    rects    = {}
    mx_now, my_now = pygame.mouse.get_pos()

    def _draw_transport_btn(bx, by, bw, bh, key, icon, is_active_btn):
        rect = pygame.Rect(bx, by, bw, bh)
        rects[key] = rect
        hovered = rect.collidepoint(mx_now, my_now)
        bg_col  = (55, 90, 55) if is_active_btn else (35, 35, 55)
        brd_col = SPEED_COL    if is_active_btn else (100, 100, 140)
        if hovered:
            bg_col = tuple(min(255, c + 20) for c in bg_col)
        pygame.draw.rect(surf, bg_col,  rect, border_radius=5)
        pygame.draw.rect(surf, brd_col, rect, 1, border_radius=5)
        cx_ = bx + bw // 2
        cy_ = by + bh // 2
        ic  = SPEED_COL if is_active_btn else (200, 200, 220)
        _draw_icon(surf, cx_, cy_, icon, ic)

    def _tri_r(cx, cy, w2, h2): return [(cx-w2,cy-h2),(cx-w2,cy+h2),(cx+w2,cy)]
    def _tri_l(cx, cy, w2, h2): return [(cx+w2,cy-h2),(cx+w2,cy+h2),(cx-w2,cy)]

    def _draw_icon(surf, cx, cy, icon, col):
        tw, th, g = 5, 6, 4
        if icon == "play":
            pygame.draw.polygon(surf, col, _tri_r(cx, cy, tw, th))
        elif icon == "pause":
            pygame.draw.rect(surf, col, (cx-6, cy-th, 4, th*2))
            pygame.draw.rect(surf, col, (cx+2, cy-th, 4, th*2))
        elif icon == "fwd":
            pygame.draw.polygon(surf, col, _tri_r(cx-g, cy, tw-1, th))
            pygame.draw.polygon(surf, col, _tri_r(cx+g, cy, tw-1, th))
        elif icon == "back":
            pygame.draw.polygon(surf, col, _tri_l(cx+g, cy, tw-1, th))
            pygame.draw.polygon(surf, col, _tri_l(cx-g, cy, tw-1, th))
        elif icon == "step_fwd":
            pygame.draw.polygon(surf, col, _tri_r(cx-2, cy, tw-1, th))
            pygame.draw.rect(surf, col, (cx+tw+1, cy-th, 3, th*2))
        elif icon == "step_back":
            pygame.draw.rect(surf, col, (cx-tw-4, cy-th, 3, th*2))
            pygame.draw.polygon(surf, col, _tri_l(cx+2, cy, tw-1, th))

    btn_defs = [
        ("step_back_coarse", "back",      False),
        ("step_back_fine",   "step_back", False),
        ("play_pause",       "play" if paused else "pause", True),
        ("step_fwd_fine",    "step_fwd",  False),
        ("step_fwd_coarse",  "fwd",       False),
    ]
    btn_w, btn_h = 38, 28
    gap          = 5
    total_w      = len(btn_defs) * btn_w + (len(btn_defs) - 1) * gap
    bx           = x + (w - total_w) // 2

    for key, icon, is_active in btn_defs:
        _draw_transport_btn(bx, y, btn_w, btn_h, key, icon, is_active)
        bx += btn_w + gap

    label_row = ["-30°", "-5°", "PLAY" if paused else "PAUS", "+5°", "+30°"]
    bx2 = x + (w - total_w) // 2
    for lbl in label_row:
        t = font_xs.render(lbl, True, (70, 70, 90))
        surf.blit(t, (bx2 + btn_w//2 - t.get_width()//2, y + btn_h + 1))
        bx2 += btn_w + gap

    hint_y = y + btn_h + 13
    hint = font_xs.render(
        "arrows=step 5 deg  Shift+arrows=30 deg  (when paused)", True, (55, 55, 72))
    surf.blit(hint, (x + (w - hint.get_width()) // 2, hint_y))

    spd_labels = ["x0.02", "x0.05", "x0.1", "x0.2", "x0.5", "x1"]
    spd_w, spd_h = 38, 20
    spd_gap      = 3
    total_sw     = len(spd_labels) * spd_w + (len(spd_labels) - 1) * spd_gap
    sx           = x + (w - total_sw) // 2
    spd_y        = hint_y + 14

    for i, lbl in enumerate(spd_labels):
        rect   = pygame.Rect(sx, spd_y, spd_w, spd_h)
        rects[f"speed_{i}"] = rect
        active = (i == speed_idx)
        hov    = rect.collidepoint(mx_now, my_now)
        bg_col  = (40, 80, 40)  if active else ((30, 30, 50) if not hov else (38, 38, 60))
        brd_col = SPEED_COL     if active else (60, 60, 90)
        txt_col = SPEED_COL     if active else (TEXT if hov else DIM)
        pygame.draw.rect(surf, bg_col,  rect, border_radius=4)
        pygame.draw.rect(surf, brd_col, rect, 1, border_radius=4)
        t = font_xs.render(lbl, True, txt_col)
        surf.blit(t, (sx + spd_w//2 - t.get_width()//2,
                      spd_y + spd_h//2 - t.get_height()//2))
        sx += spd_w + spd_gap

    spd_hint = font_xs.render(
        f"Speed: {SPEED_STEPS[speed_idx]}x   ( , / . keys to change )",
        True, (55, 55, 72))
    surf.blit(spd_hint, (x + (w - spd_hint.get_width()) // 2, spd_y + spd_h + 3))
    return rects


# ─────────────────────────────────────────────────────────────────────────────
# Poclet loader  (reads ASFID/REVOI scores from .jsonld if present)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    'label':  'Complex Chemical Synapse',
    'domain': 'Neurobiology',
    'asfid':  [0.65, 0.75, 0.90, 0.70, 0.80],
    'revoi':  [0.90, 0.80, 0.90, 0.85, 0.90],
    'gap':    0.240,
}


def load_poclet(path):
    try:
        data = json.load(open(path, 'r', encoding='utf-8'))
        node = data.get('@graph', [{}])[0]
        asfid_raw = node.get('m0:asfidScores', {})
        revoi_raw = node.get('m0:revoiScores',  {})
        asfid = [float(asfid_raw.get(k, d)) for k, d in zip('ASFID', DEFAULTS['asfid'])]
        revoi = [float(revoi_raw.get(k, d)) for k, d in zip('REVOI', DEFAULTS['revoi'])]
        return {
            'label':  node.get('dcterms:title', DEFAULTS['label']),
            'domain': node.get('m0:domain',     DEFAULTS['domain']),
            'asfid':  asfid,
            'revoi':  revoi,
            'gap':    float(node.get('m0:epistemicGap', DEFAULTS['gap'])),
        }
    except Exception as ex:
        print(f"[TSCG] poclet load failed: {ex}  — using defaults")
        return DEFAULTS.copy()


def find_poclet():
    if POCLET_OVERRIDE:
        return Path(POCLET_OVERRIDE)
    cur = Path(__file__).resolve().parent
    for _ in range(8):
        c = cur / "system-models" / "poclets" / "complex_chemical_synapse" \
            / "M0_ComplexChemicalSynapse.jsonld"
        if c.exists():
            return c
        loc = cur / "M0_ComplexChemicalSynapse.jsonld"
        if loc.exists():
            return loc
        p = cur.parent
        if p == cur:
            break
        cur = p
    return None


# ─────────────────────────────────────────────────────────────────────────────
# FSM helpers
# ─────────────────────────────────────────────────────────────────────────────
def compute_playback_rects():
    """Compute button rects once from layout constants — positions never change."""
    rects = {}
    x  = PAD
    w  = LEFT_W - PAD * 2
    # Transport buttons
    btn_keys = ['step_back_coarse', 'step_back_fine', 'play_pause',
                'step_fwd_fine',    'step_fwd_coarse']
    btn_w, btn_h = 38, 28
    gap     = 5
    total_w = len(btn_keys) * btn_w + (len(btn_keys) - 1) * gap
    bx      = x + (w - total_w) // 2
    ctrl_y  = WINDOW_H - 108
    for key in btn_keys:
        rects[key] = pygame.Rect(bx, ctrl_y, btn_w, btn_h)
        bx += btn_w + gap
    # Speed buttons
    spd_w, spd_h = 38, 20
    spd_gap = 3
    total_sw = len(SPEED_STEPS) * spd_w + (len(SPEED_STEPS) - 1) * spd_gap
    sx       = x + (w - total_sw) // 2
    spd_y    = ctrl_y + btn_h + 13 + 14      # hint_y + 14
    for i in range(len(SPEED_STEPS)):
        rects[f"speed_{i}"] = pygame.Rect(sx, spd_y, spd_w, spd_h)
        sx += spd_w + spd_gap
    return rects


def fsm_transition(state, evt, phase_deg, speed_idx):
    """Pure FSM: (state, event) → (new_state, new_phase, new_speed_idx)."""
    s, p, si = state, phase_deg, speed_idx
    if   evt == 'toggle_play':       s = SimState.PLAYING if s == SimState.PAUSED else SimState.PAUSED
    elif evt == 'step_fwd_fine':     s, p = SimState.PAUSED, (p + STEP_FINE)   % 360.0
    elif evt == 'step_fwd_coarse':   s, p = SimState.PAUSED, (p + STEP_COARSE) % 360.0
    elif evt == 'step_back_fine':    s, p = SimState.PAUSED, (p - STEP_FINE)   % 360.0
    elif evt == 'step_back_coarse':  s, p = SimState.PAUSED, (p - STEP_COARSE) % 360.0
    elif evt == 'speed_dec':         si = max(0, si - 1)
    elif evt == 'speed_inc':         si = min(len(SPEED_STEPS) - 1, si + 1)
    elif evt and evt.startswith('speed_'): si = int(evt.split('_')[1])
    return s, p, si


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pp     = find_poclet()
    poclet = load_poclet(pp) if pp else DEFAULTS.copy()
    print(f"[TSCG] {poclet['label']}  |  domain: {poclet['domain']}"
          f"  |  delta_Theta = {poclet['gap']:.3f}")

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(
        "TSCG · Complex Chemical Synapse — 5-Pole Synaptic Transmission Simulation")
    clock = pygame.time.Clock()

    font_lg = pygame.font.SysFont("segoeui", 19, bold=True)
    font_md = pygame.font.SysFont("segoeui", 14, bold=True)
    font_sm = pygame.font.SysFont("segoeui", 13)
    font_xs = pygame.font.SysFont("segoeui", 11)

    sw = LEFT_W - PAD * 4
    s_freq = Slider(PAD*2,  88, sw, FREQ_MIN, FREQ_MAX, 20.0, "Frequency (Hz)",   "Hz",  FREQ_COL)
    s_ca   = Slider(PAD*2, 164, sw, CA_MIN,   CA_MAX,   0.7,  "Ca2+ Level",       "",    CA_COL)
    s_reup = Slider(PAD*2, 240, sw, REUP_MIN, REUP_MAX, 0.5,  "Reuptake Rate",    "",    REUP_COL)

    # ── FSM state (computed once — rects never change position) ──────────
    phase_deg  = 0.0
    sim_state  = SimState.PLAYING
    speed_idx  = 2       # default nominal speed
    hover_lbl  = ""
    pole_rects = []

    POLE_JUMPS   = [0.0, 72.0, 144.0, 216.0, 288.0]
    pb_rects     = compute_playback_rects()   # stable rects, computed once

    # ── Main loop ─────────────────────────────────────────────────────────
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # ── 1. COLLECT EVENTS → produce FSM event tokens ─────────────────
        fsm_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    fsm_events.append('toggle_play')
                elif sim_state == SimState.PAUSED:
                    shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
                    if event.key == pygame.K_RIGHT:
                        fsm_events.append('step_fwd_coarse' if shift else 'step_fwd_fine')
                    elif event.key == pygame.K_LEFT:
                        fsm_events.append('step_back_coarse' if shift else 'step_back_fine')
                if event.key in (pygame.K_COMMA, pygame.K_LESS):
                    fsm_events.append('speed_dec')
                if event.key in (pygame.K_PERIOD, pygame.K_GREATER):
                    fsm_events.append('speed_inc')

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Pole table jump (handled outside FSM — direct phase set)
                for r_rect, idx in pole_rects:
                    if r_rect.collidepoint(mx, my):
                        phase_deg = POLE_JUMPS[idx]
                        break
                # Playback transport — exactly ONE button per click
                _btn_map = [
                    ('play_pause',       'toggle_play'),
                    ('step_back_fine',   'step_back_fine'),
                    ('step_fwd_fine',    'step_fwd_fine'),
                    ('step_back_coarse', 'step_back_coarse'),
                    ('step_fwd_coarse',  'step_fwd_coarse'),
                ]
                for key, evt in _btn_map:
                    if pb_rects[key].collidepoint(mx, my):
                        fsm_events.append(evt)
                        break   # ← only one button per click, always
                # Speed buttons
                for i in range(len(SPEED_STEPS)):
                    if pb_rects[f"speed_{i}"].collidepoint(mx, my):
                        fsm_events.append(f"speed_{i}")
                        break

            for s in [s_freq, s_ca, s_reup]:
                s.handle_event(event)

        # ── 2. FSM TRANSITIONS (apply all tokens in order) ────────────────
        for evt in fsm_events:
            sim_state, phase_deg, speed_idx = fsm_transition(
                sim_state, evt, phase_deg, speed_idx)

        # ── 3. PHASE ADVANCE (only in PLAYING state) ─────────────────────
        if sim_state == SimState.PLAYING:
            freq_val   = s_freq.value
            deg_s      = 360.0 * freq_val
            phase_deg  = (phase_deg + deg_s * dt * SPEED_STEPS[speed_idx]) % 360.0

        # ── 4. COMPUTE FRAME VALUES ────────────────────────────────────────
        paused      = (sim_state == SimState.PAUSED)   # for draw helpers
        pole_idx    = phase_to_pole_idx(phase_deg)
        pole_lbl    = POLES[pole_idx][0]
        pole_col    = POLES[pole_idx][1]
        freq_val    = s_freq.value
        ca_val      = s_ca.value
        reup_val    = s_reup.value

        nt_val,  psp_val  = synapse_signals(phase_deg, ca_val, reup_val)
        ves_val           = vesicle_pool(phase_deg)

        # ── Dynamic ASFID ──────────────────────────────────────────────────
        ba = poclet['asfid']
        a_fac  = {0: 0.85, 1: 0.65, 2: 0.40, 3: 0.70, 4: 0.90}.get(pole_idx, 0.65)
        a_live = clamp(ba[0] * a_fac)
        s_fac  = {0: 0.75, 1: 1.00, 2: 0.70, 3: 0.80, 4: 0.85}.get(pole_idx, 0.80)
        s_live = clamp(ba[1] * s_fac)
        f_fac  = {0: 0.40, 1: 0.30, 2: 1.00, 3: 0.70, 4: 0.90}.get(pole_idx, 0.55)
        f_live = clamp(ba[2] * f_fac)
        i_fac  = {0: 0.40, 1: 0.35, 2: 0.65, 3: 1.00, 4: 0.60}.get(pole_idx, 0.50)
        i_live = clamp(ba[3] * i_fac)
        d_fac  = {0: 0.55, 1: 0.45, 2: 1.00, 3: 0.80, 4: 0.70}.get(pole_idx, 0.60)
        d_fac  = d_fac * (0.3 + 0.7 * (freq_val - FREQ_MIN) / (FREQ_MAX - FREQ_MIN))
        d_live = clamp(ba[4] * d_fac)
        asfid_live = [a_live, s_live, f_live, i_live, d_live]

        # ── Hover detection ────────────────────────────────────────────────
        mx_now, my_now = pygame.mouse.get_pos()
        hover_lbl = ""
        for r_rect, idx in pole_rects:
            if r_rect.collidepoint(mx_now, my_now):
                hover_lbl = POLES[idx][0]
                break
        any_pb_hover = any(r.collidepoint(mx_now, my_now) for r in pb_rects.values())
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if (hover_lbl or any_pb_hover)
            else pygame.SYSTEM_CURSOR_ARROW)

        # ─────────────────────────────────────────────────────────────────
        # DRAW
        # ─────────────────────────────────────────────────────────────────
        screen.fill(BG)

        # ── LEFT PANEL ───────────────────────────────────────────────────
        pygame.draw.rect(screen, PANEL_BG, (0, 0, LEFT_W, WINDOW_H))
        pygame.draw.line(screen, BORDER, (LEFT_W, 0), (LEFT_W, WINDOW_H))

        t = font_lg.render("Chemical Synapse", True, GOLD)
        screen.blit(t, (PAD + 4, PAD + 4))
        screen.blit(font_xs.render(
            f"Domain: {poclet['domain']}  |  DT={poclet['gap']:.3f}",
            True, DIM), (PAD + 4, PAD + 4 + t.get_height() + 2))

        sep = PAD + t.get_height() + 16
        pygame.draw.line(screen, BORDER, (PAD, sep), (LEFT_W - PAD, sep))
        screen.blit(font_md.render("Parameter Controls", True, TEXT), (PAD + 4, sep + 5))

        s_freq.draw(screen, font_sm, f"{s_freq.value:.1f} Hz")
        s_ca.draw(  screen, font_sm, f"Ca2+ = {s_ca.value:.2f}")
        s_reup.draw(screen, font_sm, f"Reup = {s_reup.value:.2f}")

        # Synapse schematic
        syn_cx = LEFT_W // 2
        syn_cy = s_reup.rect.bottom + 90
        draw_synapse(screen, syn_cx, syn_cy, phase_deg, pole_idx,
                     ca_val, reup_val, ves_val, nt_val, psp_val, font_xs)

        # Phase indicator bar
        ph_y = syn_cy + 80
        screen.blit(font_xs.render(f"Phase: {phase_deg%360:.0f}°", True, DIM),
                    (PAD + 4, ph_y))
        pygame.draw.rect(screen, SLIDER_BG, (PAD + 4, ph_y + 14, LEFT_W - PAD*3, 6),
                         border_radius=3)
        fw2 = int((phase_deg % 360) / 360.0 * (LEFT_W - PAD*3))
        if fw2 > 0:
            pygame.draw.rect(screen, pole_col,
                             (PAD + 4, ph_y + 14, fw2, 6), border_radius=3)

        # Pole table
        mt_y = ph_y + 36
        pygame.draw.line(screen, BORDER, (PAD, mt_y - 22), (LEFT_W - PAD, mt_y - 22))
        screen.blit(font_md.render("Poles", True, TEXT), (PAD + 4, mt_y - 18))
        hint_s = font_xs.render("<- click to jump", True, (100, 140, 100))
        screen.blit(hint_s, (LEFT_W - hint_s.get_width() - PAD, mt_y - 16))
        pole_rects = draw_pole_table(screen, PAD + 2, mt_y, LEFT_W - PAD*2 - 4,
                                     pole_idx, hover_lbl, font_sm, font_xs)

        # Playback controls (draw only — pb_rects already computed at startup)
        ctrl_y = WINDOW_H - 108
        pygame.draw.line(screen, BORDER, (PAD, ctrl_y - 6), (LEFT_W - PAD, ctrl_y - 6))
        draw_playback_controls(
            screen, PAD, ctrl_y, LEFT_W - PAD * 2,
            paused, speed_idx, font_sm, font_xs)

        # ── CENTRE PANEL ─────────────────────────────────────────────────
        pygame.draw.rect(screen, (16, 16, 24), (LEFT_W, 0, MID_W, WINDOW_H))

        tc = font_lg.render(
            f"Synaptic Signal Diagram   [{pole_lbl}  {phase_deg%360:.0f}°]",
            True, pole_col)
        screen.blit(tc, (LEFT_W + 10, 8))
        sub = (f"freq = {freq_val:.1f} Hz   Ca2+ = {ca_val:.2f}"
               f"   Reuptake = {reup_val:.2f}   Ves.Pool = {ves_val:.0%}")
        screen.blit(font_sm.render(sub, True, GOLD), (LEFT_W + 10, 34))

        # Signal plot area
        IV_L, IV_T, IV_R, IV_B = 52, 60, 18, 70
        pr = pygame.Rect(LEFT_W + IV_L, IV_T,
                         MID_W - IV_L - IV_R, WINDOW_H - IV_T - IV_B)

        draw_signal_axes(screen, pr, font_xs)
        nt_pts, psp_pts = draw_signal_curves(screen, pr, ca_val, reup_val, font_xs)

        # Q-point on NT curve
        q_idx = int(phase_deg / 360.0 * len(nt_pts))
        q_idx = min(q_idx, len(nt_pts) - 1)
        qx_nt, qy_nt = nt_pts[q_idx]
        draw_qpoint(screen, qx_nt, qy_nt, C_REL,
                    f"NT={nt_val:.2f}", pr, font_xs)

        # Q-point on PSP curve
        qx_psp, qy_psp = psp_pts[q_idx]
        draw_qpoint(screen, qx_psp, qy_psp, C_RECEP,
                    f"PSP={psp_val:.2f}", pr, font_xs)

        # Legend
        lx, ly = LEFT_W + IV_L, pr.bottom + 3
        for lbl2, col2 in [("NT cleft", C_REL), ("PSP amplitude", C_RECEP)]:
            s2 = font_xs.render(f"--- {lbl2}", True, col2)
            screen.blit(s2, (lx, ly))
            lx += s2.get_width() + 30
        # Pole colour legend
        lx, ly2 = LEFT_W + IV_L, pr.bottom + 16
        for (lbl3, col3, *_) in POLES:
            s3 = font_xs.render(f"| {lbl3[:4]}", True, col3)
            screen.blit(s3, (lx, ly2))
            lx += s3.get_width() + 8

        # NT level bar
        eff_y = pr.bottom + 34
        eff_w = pr.w
        screen.blit(font_xs.render(
            f"NT cleft: {nt_val:.3f}  |  PSP: {psp_val:.3f}  |  Vesicle pool: {ves_val:.0%}",
            True, (160, 200, 140)), (LEFT_W + IV_L, eff_y))
        for bary, bval, bcol in [(eff_y+14, nt_val, C_REL), (eff_y+24, psp_val, C_RECEP)]:
            pygame.draw.rect(screen, SLIDER_BG, (LEFT_W+IV_L, bary, eff_w, 7), border_radius=3)
            bfw = int(bval * eff_w)
            if bfw > 0:
                pygame.draw.rect(screen, bcol, (LEFT_W+IV_L, bary, bfw, 7), border_radius=3)

        screen.blit(font_xs.render(
            "Source: M0_ComplexChemicalSynapse.jsonld", True, (50, 50, 70)),
            (LEFT_W + 6, WINDOW_H - 14))

        # ── RIGHT PANEL ───────────────────────────────────────────────────
        rp = LEFT_W + MID_W
        pygame.draw.rect(screen, PANEL_BG, (rp, 0, RIGHT_W, WINDOW_H))
        pygame.draw.line(screen, BORDER, (rp, 0), (rp, WINDOW_H))

        ar = pygame.Rect(rp + 2, 4,               RIGHT_W - 4, 168)
        rr = pygame.Rect(rp + 2, ar.bottom + 4,   RIGHT_W - 4, 163)
        sr = pygame.Rect(rp + 2, rr.bottom + 4,   RIGHT_W - 4,
                         WINDOW_H - rr.bottom - 8)

        draw_asfid(screen, ar, asfid_live, poclet['asfid'],
                   font_md, font_sm, font_xs)
        draw_revoi(screen, rr, poclet['revoi'], font_md, font_sm, font_xs)

        val_lines = [
            (f"Freq   = {freq_val:.1f} Hz",           FREQ_COL),
            (f"Ca2+   = {ca_val:.2f}",                CA_COL),
            (f"Reup   = {reup_val:.2f}",              REUP_COL),
            (f"NT_cleft = {nt_val:.3f}",              C_REL),
            (f"PSP    = {psp_val:.3f}",               C_RECEP),
            (f"VesPool = {ves_val:.0%}",              C_STORE),
        ]
        draw_status(screen, sr, pole_lbl, pole_col, val_lines,
                    font_md, font_sm, font_xs)

        screen.blit(font_xs.render(f"FPS:{int(clock.get_fps())}", True, (45, 45, 65)),
                    (LEFT_W + 4, WINDOW_H - 40))
        pygame.display.flip()

    pygame.quit()
    print("[TSCG] Simulation ended.")


if __name__ == "__main__":
    main()
