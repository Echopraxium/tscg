"""
four_stroke_engine_sim.py  v1.1
================================
TSCG Poclet Simulation -- Four-Stroke Internal Combustion Engine (Otto Cycle)
Author: Echopraxium with the collaboration of Claude AI

Animated real-time simulation of the four-stroke thermodynamic cycle:
  Intake --> Compression --> Power (Combustion) --> Exhaust

Features:
  - Animated P-V diagram (Otto cycle) with moving Q-point
  - Cylinder cross-section schematic with animated piston and valves
  - Live ASFID bars (Eagle Eye / Territory) -- dynamic with crank angle
  - Static REVOI bars (Sphinx Eye / Map)
  - Parameter sliders: RPM, Compression Ratio (r), Load (heat input)
  - Clickable stroke table to jump to any phase
  - Live readouts: efficiency, P/V/T, power output
  - Playback controls: pause/play button + speed multiplier buttons (x0.1 to x5)
  - Step-by-step mode: arrow keys advance/rewind by 5 deg (Shift = 30 deg)
  - Speed via keyboard: < / > keys cycle through speed steps

Keyboard shortcuts:
  SPACE       -- pause / resume
  <- / ->     -- step -5 / +5 degrees (only while paused)
  Shift+<-/-> -- step -30 / +30 degrees (only while paused)
  , / .       -- decrease / increase sim speed (same as clicking speed buttons)
  ESC         -- quit

Requirements:  pip install pygame
Run:
    python four_stroke_engine_sim.py
    python four_stroke_engine_sim.py path/to/M0_FourStrokeEngine.jsonld
"""

import sys, math, json
from pathlib import Path
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

# Stroke colours
C_INTAKE     = ( 60, 180, 255)   # blue
C_COMPRESS   = (255, 200,  50)   # gold
C_POWER      = (255,  80,  60)   # red-orange  (combustion!)
C_EXHAUST    = (140, 200, 120)   # green

STROKE_COLORS = [C_INTAKE, C_COMPRESS, C_POWER, C_EXHAUST]

# Slider accent colours
RPM_COL  = ( 80, 210, 210)
R_COL    = (255, 175,  45)
LOAD_COL = (200, 110, 255)

# Playback controls
SPEED_COL   = (160, 220,  80)   # active speed button
SPEED_STEPS = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0]   # simulation speed multipliers (÷7 vs v1.0)
STEP_FINE   = 5.0    # degrees per arrow-key press
STEP_COARSE = 30.0   # degrees per Shift+arrow press

# ─────────────────────────────────────────────────────────────────────────────
# Stroke definitions
# ─────────────────────────────────────────────────────────────────────────────
STROKES = [
    # (label, color, crank_start_deg, crank_end_deg, intake_valve, exhaust_valve, note)
    ("Intake",      C_INTAKE,   0,   180, True,  False, "Air-fuel in, piston down"),
    ("Compression", C_COMPRESS, 180, 360, False, False, "Adiabatic: PV^gamma = const"),
    ("Power",       C_POWER,    360, 540, False, False, "Combustion -> work output"),
    ("Exhaust",     C_EXHAUST,  540, 720, False, True,  "Burnt gas out, piston up"),
]

# ─────────────────────────────────────────────────────────────────────────────
# Physics constants
# ─────────────────────────────────────────────────────────────────────────────
GAMMA   = 1.4      # heat capacity ratio (air)
P_ATM   = 1.0      # normalised atmospheric pressure
T_AMB   = 300.0    # ambient temperature (K)

RPM_MIN, RPM_MAX     = 600.0,  6000.0
R_MIN,   R_MAX       = 6.0,    14.0
LOAD_MIN, LOAD_MAX   = 0.1,    1.0    # 0.1=idle, 1.0=WOT


def otto_states(r, load):
    """
    Compute the 4 key thermodynamic state points of the Otto cycle.
    Returns dict with P1..P4, V1..V2 (V2=V_min, V1=V_max), T1..T4, eta.
    All pressures normalised to P_atm=1, volumes normalised to V_max=1.
    """
    V1 = 1.0          # V_max (normalised)
    V2 = V1 / r       # V_min
    P1 = P_ATM
    T1 = T_AMB

    # 1 -> 2  Isentropic compression
    P2 = P1 * (r ** GAMMA)
    T2 = T1 * (r ** (GAMMA - 1))

    # 2 -> 3  Isochoric heat addition (combustion)
    # pressure ratio from heat input; Q_in proportional to load
    q_ratio = 1.0 + load * 2.5      # at load=1.0: P3/P2 = 3.5
    P3 = P2 * q_ratio
    T3 = T2 * q_ratio

    # 3 -> 4  Isentropic expansion
    P4 = P3 * ((V2 / V1) ** GAMMA)
    T4 = T3 * (V2 / V1) ** (GAMMA - 1)

    eta = 1.0 - 1.0 / (r ** (GAMMA - 1))   # ideal Otto efficiency

    return dict(P1=P1, P2=P2, P3=P3, P4=P4,
                V1=V1, V2=V2,
                T1=T1, T2=T2, T3=T3, T4=T4,
                eta=eta, r=r, load=load)


def crank_to_stroke_idx(crank_deg):
    """Return stroke index 0-3 for given crank angle 0-720."""
    c = crank_deg % 720.0
    if c < 180:   return 0   # Intake
    if c < 360:   return 1   # Compression
    if c < 540:   return 2   # Power
    return 3                  # Exhaust


def piston_pos(crank_deg):
    """Normalised piston position: 0=TDC, 1=BDC  (ideal slider-crank)."""
    theta = math.radians(crank_deg)
    return 0.5 * (1.0 - math.cos(theta))


def current_pv(crank_deg, st):
    """
    Return (V, P) normalised at current crank angle.
    Uses the Otto cycle model for each phase.
    """
    c     = crank_deg % 720.0
    pos   = piston_pos(c)
    V_cur = st['V2'] + pos * (st['V1'] - st['V2'])

    if c < 180:                            # Intake: P = P_atm
        P_cur = P_ATM
    elif c < 360:                          # Compression: adiabatic
        P_cur = st['P1'] * ((st['V1'] / V_cur) ** GAMMA)
    elif c < 540:                          # Power: adiabatic expansion from P3
        if c == 360:
            P_cur = st['P3']
        else:
            P_cur = st['P3'] * ((st['V2'] / V_cur) ** GAMMA)
    else:                                  # Exhaust: P = P_atm
        P_cur = P_ATM

    return V_cur, P_cur


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


# ─────────────────────────────────────────────────────────────────────────────
# Slider widget  (identical to transistor_sim pattern)
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
# Stroke mode table  (clickable)
# ─────────────────────────────────────────────────────────────────────────────
def draw_stroke_table(surf, x, y, w, active_idx, hover_label, font_sm, font_xs):
    row_h = 38
    gap   = 3
    rects = []
    for idx, (lbl, col, _s, _e, iv, ev, note) in enumerate(STROKES):
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
        pygame.draw.rect(surf, bcol, (x + 5, y + 8, 6, row_h - 16), border_radius=3)

        if is_hover and not is_active:
            hint = font_xs.render(">> click to jump", True, (*col, 200))
            surf.blit(hint, (x + w - hint.get_width() - 6, y + row_h - 14))

        tcol = TEXT if (is_active or is_hover) else DIM
        # Valve status indicators
        iv_col = (60, 220, 100) if iv else (80, 40, 40)
        ev_col = (60, 220, 100) if ev else (80, 40, 40)
        surf.blit(font_sm.render(f"{idx+1}. {lbl}", True, bcol), (x + 16, y + 3))
        surf.blit(font_xs.render(note, True, tcol), (x + 16, y + 21))
        surf.blit(font_xs.render("IN", True, iv_col), (x + w - 46, y + 5))
        surf.blit(font_xs.render("EX", True, ev_col), (x + w - 24, y + 5))

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


def draw_status(surf, rect, stroke_label, stroke_col, val_lines, font_md, font_sm, font_xs):
    y = draw_panel_bg(surf, rect, "Status", font_md)
    x = rect.x + PAD
    surf.blit(font_sm.render("Domain: Thermodynamics", True, GOLD), (x, y)); y += 16
    surf.blit(font_sm.render(f"Stroke: {stroke_label}", True, stroke_col),  (x, y)); y += 18
    for lbl, col in val_lines:
        surf.blit(font_sm.render(lbl, True, col), (x, y)); y += 15
    y += 4
    for eq in ["eta = 1 - 1/r^(g-1)", "PV^g = const (adiab.)"]:
        surf.blit(font_xs.render(eq, True, DIM), (x, y)); y += 13
    y += 4
    surf.blit(font_xs.render("Metaconcepts: 20 | DT=0.132", True, DIM), (x, y))


# ─────────────────────────────────────────────────────────────────────────────
# Cylinder cross-section schematic
# ─────────────────────────────────────────────────────────────────────────────
def draw_cylinder(surf, cx, cy, crank_deg, stroke_idx, font_xs):
    """Draw a simplified cylinder cross-section with animated piston."""
    cw, ch = 50, 80
    wall_t  = 5

    # Cylinder walls
    wall_col = (80, 90, 110)
    pygame.draw.rect(surf, wall_col,
                     (cx - cw//2 - wall_t, cy - ch//2, wall_t, ch))       # left wall
    pygame.draw.rect(surf, wall_col,
                     (cx + cw//2,          cy - ch//2, wall_t, ch))       # right wall
    pygame.draw.rect(surf, wall_col,
                     (cx - cw//2 - wall_t, cy - ch//2, cw + wall_t*2, wall_t))  # head

    # Piston position
    pos     = piston_pos(crank_deg % 720.0)
    pist_y  = cy - ch//2 + wall_t + int(pos * (ch - wall_t - 12))
    col     = STROKE_COLORS[stroke_idx]

    # Gas fill (above piston)
    if pist_y > cy - ch//2 + wall_t + 2:
        gas_rect = pygame.Rect(cx - cw//2, cy - ch//2 + wall_t,
                               cw, pist_y - (cy - ch//2 + wall_t))
        gas_surf = pygame.Surface((gas_rect.w, gas_rect.h), pygame.SRCALPHA)
        gas_surf.fill((*col, 35))
        surf.blit(gas_surf, (gas_rect.x, gas_rect.y))

    # Piston block
    pygame.draw.rect(surf, col,
                     (cx - cw//2 + 2, pist_y, cw - 4, 12), border_radius=3)
    pygame.draw.rect(surf, TEXT,
                     (cx - cw//2 + 2, pist_y, cw - 4, 12), 1, border_radius=3)

    # Connecting rod (line to crankshaft)
    crank_r = 14
    crank_cy = cy + ch//2 + crank_r + 8
    theta    = math.radians(crank_deg % 720.0)
    crank_px = int(cx + crank_r * math.sin(theta))
    crank_py = int(crank_cy - crank_r * math.cos(theta))
    pygame.draw.line(surf, (100, 100, 140), (cx, pist_y + 12), (crank_px, crank_py), 2)

    # Crankshaft circle
    pygame.draw.circle(surf, (60, 60, 90), (cx, crank_cy), crank_r, 2)
    pygame.draw.circle(surf, col, (crank_px, crank_py), 4)

    # Valve indicators (top corners of cylinder head)
    iv_open = STROKES[stroke_idx][4]
    ev_open = STROKES[stroke_idx][5]
    iv_col = (60, 220, 100) if iv_open else (100, 40, 40)
    ev_col = (60, 220, 100) if ev_open else (100, 40, 40)
    pygame.draw.circle(surf, iv_col, (cx - cw//2 + 8, cy - ch//2 + 4), 5)
    pygame.draw.circle(surf, ev_col, (cx + cw//2 - 8, cy - ch//2 + 4), 5)

    surf.blit(font_xs.render("IN", True, iv_col), (cx - cw//2 + 3, cy - ch//2 - 12))
    surf.blit(font_xs.render("EX", True, ev_col), (cx + cw//2 - 16, cy - ch//2 - 12))

    # Spark plug (centre top) - flashes during power stroke at TDC
    if stroke_idx == 2:
        sp_col = (255, 255, 100)
        pygame.draw.line(surf, sp_col,
                         (cx, cy - ch//2), (cx, cy - ch//2 + wall_t + 6), 2)
        if pos < 0.1:   # near TDC -> spark flash
            for rad in [12, 8, 5]:
                s = pygame.Surface((rad*2, rad*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 100, 20 + rad*8), (rad, rad), rad)
                surf.blit(s, (cx - rad, cy - ch//2 + 2 - rad))
    else:
        pygame.draw.line(surf, (80, 80, 80),
                         (cx, cy - ch//2), (cx, cy - ch//2 + wall_t + 6), 2)

    # Stroke label
    surf.blit(font_xs.render(STROKES[stroke_idx][0], True, col),
              (cx - 24, crank_cy + crank_r + 6))


# ─────────────────────────────────────────────────────────────────────────────
# P-V Diagram
# ─────────────────────────────────────────────────────────────────────────────
def pv_px(V, P, V_max, P_max, pr):
    px = pr.x + int(V / V_max * pr.w)
    py = pr.bottom - int(clamp(P / P_max) * pr.h)
    return px, py


def draw_pv_axes(surf, pr, V_max, P_max, font_xs):
    pygame.draw.rect(surf, (18, 18, 26), pr)
    pygame.draw.rect(surf, BORDER, pr, 1)
    for i in range(1, 5):
        gx = pr.x + int(i / 5 * pr.w)
        pygame.draw.line(surf, (30, 30, 42), (gx, pr.y), (gx, pr.bottom))
        gy = pr.y + int((1 - i/5) * pr.h)
        pygame.draw.line(surf, (30, 30, 42), (pr.x, gy), (pr.right, gy))
    for i in range(5):
        v = V_max * i / 4
        px = pr.x + int(i / 4 * pr.w)
        surf.blit(font_xs.render(f"{v:.2f}", True, DIM), (px - 10, pr.bottom + 3))
    for i in range(5):
        p = P_max * i / 4
        py = pr.bottom - int(i / 4 * pr.h)
        surf.blit(font_xs.render(f"{p:.1f}", True, DIM), (pr.x - 30, py - 5))
    surf.blit(font_xs.render("Volume (V_max=1)", True, (180, 150, 80)),
              (pr.x + pr.w//2 - 40, pr.bottom + 17))
    surf.blit(font_xs.render("P/P_atm", True, (80, 180, 140)),
              (pr.x - 28, pr.y - 14))


def draw_pv_cycle(surf, pr, st, font_xs):
    """Draw all 4 Otto cycle curves + label the state points."""
    N     = 200
    V1, V2 = st['V1'], st['V2']
    P_max = st['P3'] * 1.15

    draw_pv_axes(surf, pr, V1, P_max, font_xs)

    def ppx(V, P): return pv_px(V, P, V1, P_max, pr)

    # 1 -> 2  Compression (V1 to V2)
    pts12 = [ppx(V1 - (V1-V2)*k/N,
                 st['P1'] * ((V1 / max(V1 - (V1-V2)*k/N, 1e-9)) ** GAMMA))
             for k in range(N+1)]
    pygame.draw.lines(surf, C_COMPRESS, False, pts12, 2)

    # 2 -> 3  Isochoric heat addition (vertical line at V2)
    p23 = [ppx(V2, st['P2'] + (st['P3']-st['P2'])*k/N) for k in range(N+1)]
    pygame.draw.lines(surf, C_POWER, False, p23, 2)

    # 3 -> 4  Expansion (V2 to V1)
    pts34 = [ppx(V2 + (V1-V2)*k/N,
                 st['P3'] * ((V2 / max(V2 + (V1-V2)*k/N, 1e-9)) ** GAMMA))
             for k in range(N+1)]
    pygame.draw.lines(surf, C_POWER, False, pts34, 2)

    # 4 -> 1  Isochoric heat rejection (vertical line at V1)
    p41 = [ppx(V1, st['P4'] + (st['P1']-st['P4'])*k/N) for k in range(N+1)]
    pygame.draw.lines(surf, C_COMPRESS, False, p41, 2)

    # Intake / Exhaust strokes (atmospheric pressure line)
    x_atm_l, y_atm = ppx(V2, P_ATM)
    x_atm_r, _     = ppx(V1, P_ATM)
    pygame.draw.line(surf, C_INTAKE,  (x_atm_l, y_atm), (x_atm_r, y_atm), 1)
    pygame.draw.line(surf, C_EXHAUST, (x_atm_r, y_atm), (x_atm_l, y_atm), 1)

    # State point labels
    for label, V, P in [("1", V1, st['P1']), ("2", V2, st['P2']),
                         ("3", V2, st['P3']), ("4", V1, st['P4'])]:
        lx, ly = ppx(V, P)
        pygame.draw.circle(surf, TEXT, (lx, ly), 4)
        surf.blit(font_xs.render(label, True, GOLD), (lx + 6, ly - 8))

    return P_max


def draw_qpoint(surf, qx, qy, col, label, pr, font_xs):
    """Draw Q-point with halo (same as transistor_sim)."""
    pygame.draw.line(surf, (*col, 60), (pr.x, qy), (pr.right, qy), 1)
    pygame.draw.line(surf, (*col, 60), (qx, pr.y), (qx, pr.bottom), 1)
    for r in [13, 9, 6]:
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*col, 30 + r*8), (r, r), r)
        surf.blit(s, (qx - r, qy - r))
    pygame.draw.circle(surf, col,  (qx, qy), 7)
    pygame.draw.circle(surf, TEXT, (qx, qy), 7, 1)
    lbl = font_xs.render(label, True, col)
    surf.blit(lbl, (min(qx + 10, pr.right - lbl.get_width() - 2),
                    max(qy - 17, pr.y + 2)))


# ─────────────────────────────────────────────────────────────────────────────
# Playback control bar
# ─────────────────────────────────────────────────────────────────────────────
def draw_playback_controls(surf, x, y, w, paused, speed_idx, font_sm, font_xs):
    """
    Draw two rows of playback controls using pygame primitives (no Unicode).

    Row 1 (transport):  |◀◀|  |◀|  |▶/⏸|  |▶|  |▶▶|
    Row 2 (speed):      x0.02 x0.05 x0.1 x0.2 x0.5 x1

    Returns dict of clickable rects.
    """
    rects = {}
    mx_now, my_now = pygame.mouse.get_pos()

    # ── helper: draw one transport button ────────────────────────────────
    def _draw_transport_btn(bx, by, bw, bh, key, icon, is_active_btn):
        rect    = pygame.Rect(bx, by, bw, bh)
        rects[key] = rect
        hovered = rect.collidepoint(mx_now, my_now)

        bg_col  = (55, 90, 55) if is_active_btn else (35, 35, 55)
        brd_col = SPEED_COL    if is_active_btn else (100, 100, 140)
        if hovered:
            bg_col = tuple(min(255, c + 20) for c in bg_col)

        pygame.draw.rect(surf, bg_col,  rect, border_radius=5)
        pygame.draw.rect(surf, brd_col, rect, 1, border_radius=5)

        # icon drawn relative to button centre
        cx_ = bx + bw // 2
        cy_ = by + bh // 2
        ic  = SPEED_COL if is_active_btn else (200, 200, 220)
        _draw_transport_icon(surf, cx_, cy_, icon, ic)

    def _tri_right(cx, cy, w2, h2):
        """Right-pointing filled triangle."""
        return [(cx - w2, cy - h2), (cx - w2, cy + h2), (cx + w2, cy)]

    def _tri_left(cx, cy, w2, h2):
        """Left-pointing filled triangle."""
        return [(cx + w2, cy - h2), (cx + w2, cy + h2), (cx - w2, cy)]

    def _draw_transport_icon(surf, cx, cy, icon, col):
        tw, th = 5, 6   # triangle half-size
        gap2   = 4      # gap between double arrows
        if icon == "play":          # ▶
            pygame.draw.polygon(surf, col, _tri_right(cx, cy, tw, th))
        elif icon == "pause":       # ⏸  two vertical bars
            pygame.draw.rect(surf, col, (cx - 6, cy - th, 4, th * 2))
            pygame.draw.rect(surf, col, (cx + 2, cy - th, 4, th * 2))
        elif icon == "fwd":         # ▶▶
            pygame.draw.polygon(surf, col, _tri_right(cx - gap2, cy, tw - 1, th))
            pygame.draw.polygon(surf, col, _tri_right(cx + gap2, cy, tw - 1, th))
        elif icon == "back":        # ◀◀
            pygame.draw.polygon(surf, col, _tri_left(cx + gap2, cy, tw - 1, th))
            pygame.draw.polygon(surf, col, _tri_left(cx - gap2, cy, tw - 1, th))
        elif icon == "step_fwd":    # ▶|  (triangle + bar)
            pygame.draw.polygon(surf, col, _tri_right(cx - 2, cy, tw - 1, th))
            pygame.draw.rect(surf, col, (cx + tw + 1, cy - th, 3, th * 2))
        elif icon == "step_back":   # |◀  (bar + triangle)
            pygame.draw.rect(surf, col, (cx - tw - 4, cy - th, 3, th * 2))
            pygame.draw.polygon(surf, col, _tri_left(cx + 2, cy, tw - 1, th))

    # ── Row 1 : transport ────────────────────────────────────────────────
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

    # Labels under buttons (tiny, ASCII-safe)
    label_row = ["-30°", "-5°", "PLAY" if paused else "PAUS", "+5°", "+30°"]
    bx2 = x + (w - total_w) // 2
    for lbl in label_row:
        t = font_xs.render(lbl, True, (70, 70, 90))
        surf.blit(t, (bx2 + btn_w // 2 - t.get_width() // 2, y + btn_h + 1))
        bx2 += btn_w + gap

    hint_y = y + btn_h + 13
    hint   = font_xs.render(
        "arrows=step 5 deg  Shift+arrows=30 deg  (when paused)", True, (55, 55, 72))
    surf.blit(hint, (x + (w - hint.get_width()) // 2, hint_y))

    # ── Row 2 : speed buttons ─────────────────────────────────────────────
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

        bg_col  = (40, 80, 40) if active else ((30, 30, 50) if not hov else (38, 38, 60))
        brd_col = SPEED_COL    if active else (60, 60, 90)
        txt_col = SPEED_COL    if active else (TEXT if hov else DIM)

        pygame.draw.rect(surf, bg_col,  rect, border_radius=4)
        pygame.draw.rect(surf, brd_col, rect, 1, border_radius=4)

        t = font_xs.render(lbl, True, txt_col)
        surf.blit(t, (sx + spd_w // 2 - t.get_width() // 2,
                      spd_y + spd_h // 2 - t.get_height() // 2))
        sx += spd_w + spd_gap

    spd_hint = font_xs.render(
        f"Speed: {SPEED_STEPS[speed_idx]}x   ( , / . keys to change )",
        True, (55, 55, 72))
    surf.blit(spd_hint, (x + (w - spd_hint.get_width()) // 2, spd_y + spd_h + 3))

    return rects


# ─────────────────────────────────────────────────────────────────────────────
# Poclet loader
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    'label':  'Four-Stroke Engine',
    'domain': 'Thermodynamics',
    'asfid':  [0.85, 0.90, 0.95, 0.80, 0.85],
    'revoi':  [0.90, 0.85, 0.90, 0.90, 0.85],
    'gap':    0.132,
}


def load_poclet(path):
    try:
        data = json.load(open(path, 'r', encoding='utf-8'))
        node = data.get('@graph', [{}])[0]
        asfid = [float(node.get('m0:asfidScores', {}).get(k, d))
                 for k, d in zip('ASFID', DEFAULTS['asfid'])]
        revoi = [float(node.get('m0:revoiScores', {}).get(k, d))
                 for k, d in zip('REVOI', DEFAULTS['revoi'])]
        return {
            'label':  node.get('rdfs:label', DEFAULTS['label']),
            'domain': node.get('m0:domain',  DEFAULTS['domain']),
            'asfid':  asfid,
            'revoi':  revoi,
            'gap':    float(node.get('m0:epistemicGap', DEFAULTS['gap'])),
        }
    except Exception as ex:
        print(f"[TSCG] poclet load failed: {ex}")
        return DEFAULTS.copy()


def find_poclet():
    if POCLET_OVERRIDE:
        return Path(POCLET_OVERRIDE)
    cur = Path(__file__).resolve().parent
    for _ in range(8):
        c = cur / "system-models" / "poclets" / "four_stroke_engine" / "M0_FourStrokeEngine.jsonld"
        if c.exists():
            return c
        p = cur.parent
        if p == cur:
            break
        cur = p
    loc = Path(__file__).parent / "M0_FourStrokeEngine.jsonld"
    return loc if loc.exists() else None


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
    pygame.display.set_caption("TSCG · Four-Stroke Engine — Otto Cycle Simulation")
    clock  = pygame.time.Clock()

    font_lg = pygame.font.SysFont("segoeui", 19, bold=True)
    font_md = pygame.font.SysFont("segoeui", 14, bold=True)
    font_sm = pygame.font.SysFont("segoeui", 13)
    font_xs = pygame.font.SysFont("segoeui", 11)

    sw = LEFT_W - PAD * 4
    s_rpm  = Slider(PAD*2,  88, sw, RPM_MIN,  RPM_MAX,  2000.0, "Engine Speed (RPM)", "rpm", RPM_COL)
    s_r    = Slider(PAD*2, 164, sw, R_MIN,    R_MAX,      10.0, "Compression Ratio (r)", "", R_COL)
    s_load = Slider(PAD*2, 240, sw, LOAD_MIN, LOAD_MAX,    0.7, "Load (heat input)",   "", LOAD_COL)

    # Animation state
    crank_deg  = 0.0          # 0–720 (full 4-stroke cycle)
    paused     = False
    speed_idx  = 2            # index into SPEED_STEPS (default = 0.1×)
    hover_lbl  = ""
    stroke_rects   = []
    playback_rects = {}       # filled each frame by draw_playback_controls

    # Stroke preset crank angles (TDC of each stroke)
    STROKE_JUMPS = [0.0, 180.0, 360.0, 540.0]

    def apply_stroke_preset(idx):
        nonlocal crank_deg
        crank_deg = STROKE_JUMPS[idx]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0   # seconds

        # Advance crank angle based on RPM × speed multiplier
        if not paused:
            rpm     = s_rpm.value
            speed_mult = SPEED_STEPS[speed_idx]
            deg_s   = rpm * 360.0 / 60.0   # degrees per second for ONE revolution
            # 4-stroke = 2 revolutions = 720 degrees per cycle
            crank_deg = (crank_deg + deg_s * dt * 2.0 * speed_mult) % 720.0

        stroke_idx  = crank_to_stroke_idx(crank_deg)
        stroke_lbl  = STROKES[stroke_idx][0]
        stroke_col  = STROKES[stroke_idx][1]
        r_val       = s_r.value
        load_val    = s_load.value

        # Compute Otto cycle states
        st  = otto_states(r_val, load_val)
        V_c, P_c = current_pv(crank_deg, st)

        # ── Dynamic ASFID ──────────────────────────────────────────────────
        ba   = poclet['asfid']
        pos  = piston_pos(crank_deg % 720.0)
        is_power = (stroke_idx == 2)
        is_inex  = (stroke_idx in (0, 3))

        # A: strongest during power stroke (energy extraction)
        a_live = clamp(ba[0] * (0.3 + 0.7 * (1.0 if is_power else 0.4)))
        # S: constant (geometry)
        s_live = ba[1]
        # F: strongest during intake/exhaust (actual mass flow)
        f_fac  = abs(math.sin(math.radians(crank_deg)))
        f_live = clamp(ba[2] * (0.1 + 0.9 * (f_fac if is_inex else 0.2)))
        # I: strongest near TDC/BDC transitions (timing info)
        near_tdc = max(0.0, 1.0 - min(crank_deg % 180, 180 - crank_deg % 180) / 30.0)
        i_live = clamp(ba[3] * (0.3 + 0.7 * near_tdc))
        # D: proportional to RPM
        d_live = clamp(ba[4] * (0.2 + 0.8 * (s_rpm.value - RPM_MIN) / (RPM_MAX - RPM_MIN)))
        asfid_live = [a_live, s_live, f_live, i_live, d_live]

        # ── Hover detection ────────────────────────────────────────────────
        mx_now, my_now = pygame.mouse.get_pos()
        hover_lbl = ""
        for r_rect, idx in stroke_rects:
            if r_rect.collidepoint(mx_now, my_now):
                hover_lbl = STROKES[idx][0]
                break
        # Use hand cursor over stroke rows OR any playback button
        any_pb_hover = any(r.collidepoint(mx_now, my_now)
                           for r in playback_rects.values())
        if hover_lbl or any_pb_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # ── Events ────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── Keyboard ──
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # SPACE → toggle pause
                if event.key == pygame.K_SPACE:
                    paused = not paused

                # Arrow keys → step when paused
                if paused:
                    shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
                    step  = STEP_COARSE if shift else STEP_FINE
                    if event.key == pygame.K_LEFT:
                        crank_deg = (crank_deg - step) % 720.0
                    if event.key == pygame.K_RIGHT:
                        crank_deg = (crank_deg + step) % 720.0

                # , / . → speed down / up
                if event.key in (pygame.K_COMMA, pygame.K_LESS):
                    speed_idx = max(0, speed_idx - 1)
                if event.key in (pygame.K_PERIOD, pygame.K_GREATER):
                    speed_idx = min(len(SPEED_STEPS) - 1, speed_idx + 1)

            # ── Mouse clicks ──
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Stroke table → jump
                for r_rect, idx in stroke_rects:
                    if r_rect.collidepoint(mx, my):
                        apply_stroke_preset(idx)
                        break

                # Playback buttons
                if playback_rects.get('play_pause') and \
                   playback_rects['play_pause'].collidepoint(mx, my):
                    paused = not paused

                if playback_rects.get('step_back_fine') and \
                   playback_rects['step_back_fine'].collidepoint(mx, my):
                    paused = True
                    crank_deg = (crank_deg - STEP_FINE) % 720.0

                if playback_rects.get('step_fwd_fine') and \
                   playback_rects['step_fwd_fine'].collidepoint(mx, my):
                    paused = True
                    crank_deg = (crank_deg + STEP_FINE) % 720.0

                if playback_rects.get('step_back_coarse') and \
                   playback_rects['step_back_coarse'].collidepoint(mx, my):
                    paused = True
                    crank_deg = (crank_deg - STEP_COARSE) % 720.0

                if playback_rects.get('step_fwd_coarse') and \
                   playback_rects['step_fwd_coarse'].collidepoint(mx, my):
                    paused = True
                    crank_deg = (crank_deg + STEP_COARSE) % 720.0

                # Speed buttons
                for i in range(len(SPEED_STEPS)):
                    key = f"speed_{i}"
                    if playback_rects.get(key) and \
                       playback_rects[key].collidepoint(mx, my):
                        speed_idx = i

            for s in [s_rpm, s_r, s_load]:
                s.handle_event(event)

        # ── DRAW ──────────────────────────────────────────────────────────
        screen.fill(BG)

        # ── LEFT PANEL ───────────────────────────────────────────────────
        pygame.draw.rect(screen, PANEL_BG, (0, 0, LEFT_W, WINDOW_H))
        pygame.draw.line(screen, BORDER, (LEFT_W, 0), (LEFT_W, WINDOW_H))

        t = font_lg.render("Piston Engine", True, GOLD)
        screen.blit(t, (PAD + 4, PAD + 4))
        screen.blit(font_xs.render(
            f"Domain: {poclet['domain']}  |  DT={poclet['gap']:.3f}",
            True, DIM), (PAD + 4, PAD + 4 + t.get_height() + 2))

        sep = PAD + t.get_height() + 16
        pygame.draw.line(screen, BORDER, (PAD, sep), (LEFT_W - PAD, sep))
        screen.blit(font_md.render("Parameter Controls", True, TEXT), (PAD + 4, sep + 5))

        s_rpm.draw(screen,  font_sm, f"{s_rpm.value:.0f} rpm")
        s_r.draw(screen,    font_sm, f"r = {s_r.value:.1f}:1")
        s_load.draw(screen, font_sm, f"{int(s_load.value*100)}% load")

        # Cylinder schematic
        cyl_cy = s_load.rect.bottom + 80
        draw_cylinder(screen, LEFT_W // 2, cyl_cy, crank_deg, stroke_idx, font_xs)

        # Crank angle indicator
        crank_pct = (crank_deg % 720) / 720.0
        ca_y = cyl_cy + 105
        screen.blit(font_xs.render(f"Crank: {crank_deg%720:.0f}°", True, DIM),
                    (PAD + 4, ca_y))
        pygame.draw.rect(screen, SLIDER_BG, (PAD + 4, ca_y + 14, LEFT_W - PAD*3, 6),
                         border_radius=3)
        fw2 = int(crank_pct * (LEFT_W - PAD*3))
        if fw2 > 0:
            pygame.draw.rect(screen, stroke_col,
                             (PAD + 4, ca_y + 14, fw2, 6), border_radius=3)

        # Stroke table
        mt_y = ca_y + 36
        pygame.draw.line(screen, BORDER, (PAD, mt_y - 22), (LEFT_W - PAD, mt_y - 22))
        screen.blit(font_md.render("Strokes", True, TEXT), (PAD + 4, mt_y - 18))
        hint_s = font_xs.render("<- click to jump", True, (100, 140, 100))
        screen.blit(hint_s, (LEFT_W - hint_s.get_width() - PAD, mt_y - 16))
        stroke_rects = draw_stroke_table(screen, PAD + 2, mt_y, LEFT_W - PAD*2 - 4,
                                          stroke_idx, hover_lbl, font_sm, font_xs)

        # Playback controls (bottom of left panel)
        ctrl_y = WINDOW_H - 105   # enough space for 2 rows + hints
        pygame.draw.line(screen, BORDER, (PAD, ctrl_y - 6), (LEFT_W - PAD, ctrl_y - 6))
        playback_rects = draw_playback_controls(
            screen, PAD, ctrl_y, LEFT_W - PAD * 2,
            paused, speed_idx, font_sm, font_xs)

        # ── CENTRE PANEL ─────────────────────────────────────────────────
        pygame.draw.rect(screen, (16, 16, 24), (LEFT_W, 0, MID_W, WINDOW_H))

        # Title bar
        tc = font_lg.render(f"Otto Cycle P-V Diagram   [{stroke_lbl}]",
                             True, stroke_col)
        screen.blit(tc, (LEFT_W + 10, 8))
        eta_txt = f"eta_ideal = {st['eta']*100:.1f}%   r = {r_val:.1f}:1   " \
                  f"load = {int(load_val*100)}%"
        screen.blit(font_sm.render(eta_txt, True, GOLD), (LEFT_W + 10, 34))

        # P-V plot area
        IV_L, IV_T, IV_R, IV_B = 52, 60, 18, 52
        pr = pygame.Rect(LEFT_W + IV_L, IV_T,
                         MID_W - IV_L - IV_R, WINDOW_H - IV_T - IV_B)

        P_max = draw_pv_cycle(screen, pr, st, font_xs)

        # Q-point
        qx, qy = pv_px(V_c, P_c, st['V1'], P_max, pr)
        draw_qpoint(screen, qx, qy, stroke_col,
                    f"({V_c:.2f}, {P_c:.1f})", pr, font_xs)

        # Stroke colour legend
        lx = LEFT_W + IV_L
        ly = pr.bottom + 3
        for lbl2, col2, *_ in STROKES:
            s2 = font_xs.render(f"● {lbl2}", True, col2)
            screen.blit(s2, (lx, ly))
            lx += s2.get_width() + 18

        # Efficiency bar (visual)
        eff_y = pr.bottom + 24
        eff_w = pr.w
        screen.blit(font_xs.render(
            f"Ideal efficiency: {st['eta']*100:.1f}%  |  Real ~{st['eta']*0.45*100:.0f}% (accounting for losses)",
            True, (160, 200, 140)), (LEFT_W + IV_L, eff_y))
        pygame.draw.rect(screen, SLIDER_BG, (LEFT_W + IV_L, eff_y + 14, eff_w, 8),
                         border_radius=4)
        eff_fw = int(st['eta'] * eff_w)
        if eff_fw > 0:
            pygame.draw.rect(screen, GREEN_OK,
                             (LEFT_W + IV_L, eff_y + 14, eff_fw, 8), border_radius=4)
        # Reality bar (estimate)
        real_fw = int(st['eta'] * 0.45 * eff_w)
        pygame.draw.rect(screen, (255, 140, 40),
                         (LEFT_W + IV_L, eff_y + 24, real_fw, 4), border_radius=2)
        screen.blit(font_xs.render("  ideal (green)  |  real estimate (orange)",
                    True, DIM), (LEFT_W + IV_L, eff_y + 30))

        # Source file hint
        screen.blit(font_xs.render("Source: M0_FourStrokeEngine.jsonld", True, (50, 50, 70)),
                    (LEFT_W + 6, WINDOW_H - 14))

        # ── RIGHT PANEL ───────────────────────────────────────────────────
        rp = LEFT_W + MID_W
        pygame.draw.rect(screen, PANEL_BG, (rp, 0, RIGHT_W, WINDOW_H))
        pygame.draw.line(screen, BORDER, (rp, 0), (rp, WINDOW_H))

        ar = pygame.Rect(rp + 2, 4,              RIGHT_W - 4, 163)
        rr = pygame.Rect(rp + 2, ar.bottom + 4,  RIGHT_W - 4, 158)
        sr = pygame.Rect(rp + 2, rr.bottom + 4,  RIGHT_W - 4,
                         WINDOW_H - rr.bottom - 8)

        draw_asfid(screen, ar, asfid_live, poclet['asfid'],
                   font_md, font_sm, font_xs)
        draw_revoi(screen, rr, poclet['revoi'], font_md, font_sm, font_xs)

        val_lines = [
            (f"RPM   = {s_rpm.value:.0f}",        RPM_COL),
            (f"r     = {r_val:.1f}:1",             R_COL),
            (f"P_cur = {P_c:.2f} P_atm",          stroke_col),
            (f"V_cur = {V_c:.3f} V_max",           stroke_col),
            (f"P_max = {st['P3']:.1f} P_atm",      C_POWER),
            (f"eta   = {st['eta']*100:.1f}%",       GREEN_OK),
        ]
        draw_status(screen, sr, stroke_lbl, stroke_col, val_lines,
                    font_md, font_sm, font_xs)

        screen.blit(font_xs.render(f"FPS:{int(clock.get_fps())}", True, (45, 45, 65)),
                    (LEFT_W + 4, WINDOW_H - 40))
        pygame.display.flip()

    pygame.quit()
    print("[TSCG] Simulation ended.")


if __name__ == "__main__":
    main()
