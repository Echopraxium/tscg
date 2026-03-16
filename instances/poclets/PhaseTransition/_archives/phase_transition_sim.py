"""
phase_transition_sim.py
=======================
TSCG Poclet Simulation — Phase Transition (Solid / Liquid / Gas)
Author: Echopraxium with the collaboration of Claude AI
Version: 1.3.0  (2026-02-26)

Driven by the M0_PhaseTransition poclet.

Physics:
  - Ideal Gas Law:        pV = nRT
  - Clausius-Clapeyron:   ln(P2/P1) = (ΔHvap/R) * (1/T1 - 1/T2)
  - Gibbs Phase Rule:     F = C - P + 2

Particle animations:
  - GAS    : Langevin / Brownian dynamics (random kicks + soft damping)
  - LIQUID : Divergence-free stream-function field (incompressible turbulence)
  - SOLID  : Lattice vibrations with amplitude proportional to T/T_melt

Seven reference substances:
  Methanol, Water, Gallium, Sulfur, Iodine, Camphor, Dichloromethane

Layout (1440 x 820):
  LEFT   (370 px) : Substance selector + State buttons [S][L][G] + T/P sliders
  CENTER (530 px) : 3-layer phase visualisation (equal heights, click to switch)
  RIGHT  (540 px) : Properties — ideal gas law, Clausius-Clapeyron, ASFID/REVOI

Controls:
  Substance tabs       — select reference substance
  [SOLID][LIQUID][GAS] — snap T,P to canonical values
  T slider             — temperature -200 to 2500 °C
  P slider             — pressure 0.001 to 100 atm (log scale)
  ESC                  — quit

Requirements:
  pip install pygame

Run:
  python phase_transition_sim.py
"""

import math
import random
import pygame

# ---------------------------------------------------------------------------
# Window & layout
# ---------------------------------------------------------------------------
WIN_W, WIN_H = 1440, 820
FPS          = 60

LEFT_W  = 370
RIGHT_W = 540
MID_W   = WIN_W - LEFT_W - RIGHT_W   # 530

LEFT_X  = 0
MID_X   = LEFT_W
RIGHT_X = LEFT_W + MID_W

PAD = 10

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
BG        = ( 12,  14,  22)
PANEL     = ( 22,  24,  36)
PANEL2    = ( 30,  32,  46)
BORDER    = ( 55,  60,  90)
TEXT      = (220, 225, 240)
DIM       = (120, 125, 150)
GOLD      = (255, 205,  55)
GREEN     = ( 80, 215, 120)
RED_C     = (225,  65,  65)
ACCENT    = ( 80, 160, 255)
SLIDER_BG = ( 38,  40,  58)
SLIDER_FG = ( 80, 155, 240)

COL_SOLID  = ( 55,  65, 110)
COL_LIQUID = ( 25,  85, 175)
COL_GAS    = ( 35, 115, 150)

HL_SOLID   = ( 90, 110, 200)
HL_LIQUID  = ( 50, 140, 240)
HL_GAS     = ( 90, 200, 230)

# ---------------------------------------------------------------------------
# Physics constants
# ---------------------------------------------------------------------------
R_GAS  = 8.314
ATM_PA = 101_325.0

# ---------------------------------------------------------------------------
# Reference substances
# ---------------------------------------------------------------------------
SUBSTANCES = {
    "Methanol": {
        "formula": "CH3OH", "molar_mass": 32.04,
        "mp_K": 175.60, "bp_K": 337.75,
        "dHvap": 35_200, "dHfus": 3_215,
        "Tc_K": 512.60, "Pc_atm": 79.8,
        "Ttp_K": 175.60, "Ttp_Pa": 0.18,
        "mp_slope": 0.01,
        "color": (180, 200, 255),
        "note": "Highly toxic; excellent cryogenic antifreeze",
        "hazard": "TOXIC: blindness/death",
    },
    "Water": {
        "formula": "H2O", "molar_mass": 18.015,
        "mp_K": 273.15, "bp_K": 373.15,
        "dHvap": 40_700, "dHfus": 6_010,
        "Tc_K": 647.10, "Pc_atm": 217.7,
        "Ttp_K": 273.16, "Ttp_Pa": 611.7,
        "mp_slope": -0.0075,
        "color": ( 40, 130, 230),
        "note": "Anomalous: density max 4C; negative dTm/dP",
        "hazard": "",
    },
    "Gallium": {
        "formula": "Ga", "molar_mass": 69.72,
        "mp_K": 302.91, "bp_K": 2676.0,
        "dHvap": 256_000, "dHfus": 5_590,
        "Tc_K": 7620.0, "Pc_atm": 2239.0,
        "Ttp_K": 302.91, "Ttp_Pa": 40_000,
        "mp_slope": 0.008,
        "color": (190, 190, 215),
        "note": "Melts in hand (29.76C); widest liquid range: 2373 K",
        "hazard": "",
    },
    "Sulfur": {
        "formula": "S8", "molar_mass": 256.48,
        "mp_K": 385.95, "bp_K": 717.75,
        "dHvap": 45_000, "dHfus": 1_727,
        "Tc_K": 1314.0, "Pc_atm": 201.7,
        "Ttp_K": 385.95, "Ttp_Pa": 6_000,
        "mp_slope": 0.035,
        "color": (230, 210,  30),
        "note": "Viscosity max at ~160C (S8 rings polymerise)",
        "hazard": "",
    },
    "Iodine": {
        "formula": "I2", "molar_mass": 253.81,
        "mp_K": 386.85, "bp_K": 457.55,
        "dHvap": 41_800, "dHfus": 15_520,
        "Tc_K": 819.0, "Pc_atm": 116.5,
        "Ttp_K": 386.65, "Ttp_Pa": 11_657,
        "mp_slope": 0.03,
        "color": (130,  60, 160),
        "note": "Visible violet sublimation at 1 atm; Ptp=0.115 atm",
        "hazard": "",
    },
    "Camphor": {
        "formula": "C10H16O", "molar_mass": 152.23,
        "mp_K": 448.15, "bp_K": 477.15,
        "dHvap": 59_000, "dHfus": 6_800,
        "Tc_K": 701.0, "Pc_atm": 29.0,
        "Ttp_K": 451.55, "Ttp_Pa": 40_000,
        "mp_slope": 0.025,
        "color": (245, 245, 210),
        "note": "Strong sublimation; narrow 29C liquid range; aromatic",
        "hazard": "",
    },
    "Dichloromethane": {
        "formula": "CH2Cl2", "molar_mass": 84.93,
        "mp_K": 176.45, "bp_K": 312.75,
        "dHvap": 28_600, "dHfus": 4_600,
        "Tc_K": 510.0, "Pc_atm": 60.4,
        "Ttp_K": 176.45, "Ttp_Pa": 22.2,
        "mp_slope": 0.012,
        "color": (140, 225, 205),
        "note": "Very low bp (39.6C); dense chlorinated lab solvent",
        "hazard": "Suspected carcinogen",
    },
}

SUBSTANCE_KEYS = list(SUBSTANCES.keys())

# ---------------------------------------------------------------------------
# Phase physics
# ---------------------------------------------------------------------------

def boiling_point_at_P(sub, P_atm):
    """Clausius-Clapeyron: T_b(P)."""
    P_Pa = max(P_atm * ATM_PA, 1.0)
    T_b0 = sub["bp_K"]
    dHv  = sub["dHvap"]
    try:
        return max(1.0 / (1.0 / T_b0 - R_GAS / dHv * math.log(P_Pa / ATM_PA)), 0.1)
    except (ValueError, ZeroDivisionError):
        return T_b0

def melting_point_at_P(sub, P_atm):
    return sub["mp_K"] + sub.get("mp_slope", 0.01) * (P_atm - 1.0)

def determine_phase(sub, T_K, P_atm):
    """Return 'solid' | 'liquid' | 'gas'."""
    T_m = melting_point_at_P(sub, P_atm)
    if T_K < T_m:
        return "solid"
    Ptp = sub["Ttp_Pa"] / ATM_PA
    if P_atm < Ptp:          # below triple-point pressure: no liquid
        return "gas"
    T_b = boiling_point_at_P(sub, P_atm)
    if T_K < T_b:
        return "liquid"
    return "gas"

def ideal_gas_volume_L(n, T_K, P_atm):
    return (n * R_GAS * max(T_K, 1.0)) / (max(P_atm * ATM_PA, 1e-3)) * 1000.0

def is_sublimating(sub, P_atm):
    return P_atm < sub["Ttp_Pa"] / ATM_PA

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def phase_particle_color(phase, sub_col):
    base = {"solid": HL_SOLID, "liquid": HL_LIQUID, "gas": HL_GAS}[phase]
    return lerp_color(base, sub_col, 0.45)

# ---------------------------------------------------------------------------
# Particle systems
# ---------------------------------------------------------------------------

class ParticleSystem:
    """
    Phase-specific particle animations:

    SOLID  — particles sit on a crystal lattice and vibrate around their rest
             positions.  Amplitude is proportional to T_K / T_melt, giving
             visible quivering near the melting point and near-stillness at low T.
             Each particle has independent random phase offsets on x and y so the
             lattice never oscillates in unison.

    LIQUID — particles advect through a time-varying, analytically divergence-free
             velocity field derived from a stream-function sum:
               psi(x,y,t) = sum_k  A_k * sin(fx_k*x + ox_k*t + ph_x_k)
                                       * sin(fy_k*y + oy_k*t + ph_y_k)
               vx =  d_psi/dy   (divergence-free by construction -> incompressible)
               vy = -d_psi/dx
             Three overlapping modes with different spatial frequencies and drift
             speeds produce organic turbulent / vortex-like swirling flow.

    GAS    — Langevin / Brownian dynamics:
               v(t+dt) = v(t) * (1 - damping) + noise_kick
             Each frame a random kick is added in a random direction and the
             velocity is softly damped so it stays statistically near a target
             speed.  The result is the characteristic jittery random walk of
             gas molecules with no preferred direction and frequent course changes.
    """

    COUNTS = {"solid": 56, "liquid": 42, "gas": 28}

    # ── Stream-function modes for liquid (incompressible turbulence) ─────────
    # Each mode: (amplitude, freq_x, freq_y, omega_x, omega_y)
    # Frequencies are in radians per pixel; omegas in radians per second.
    # 3 modes with different vortex scales:
    #   large slow roll  +  medium eddy  +  small fast swirl
    # Amplitudes tuned to ~0.3-0.6 px/frame (half solid vibration speed).
    # Spatial frequencies chosen so vortex size fits the ~200px panel height.
    _STREAM_MODES = [
        (0.55, 0.018, 0.015,  0.18, -0.14),   # large roll   (~350 px wavelength)
        (0.40, 0.042, 0.035, -0.28,  0.22),   # medium eddy  (~150 px wavelength)
        (0.25, 0.080, 0.065,  0.40, -0.32),   # small swirl  ( ~80 px wavelength)
    ]

    # ── Brownian parameters for gas ──────────────────────────────────────────
    _GAS_DAMPING     = 0.04    # fraction of speed removed each frame
    _GAS_KICK_SIGMA  = 0.55    # std-dev of random velocity kick per frame
    _GAS_TARGET_SPD  = 2.2     # soft target speed (pixels/frame)

    def __init__(self, phase, rect, color):
        self.phase = phase
        self.rect  = rect
        self.color = color
        self.pts   = []
        self._init()

    # ── Initialisation ───────────────────────────────────────────────────────

    def _init(self):
        r  = self.rect
        n  = self.COUNTS[self.phase]
        self.pts = []

        if self.phase == "solid":
            # Place on a regular grid; give each particle two independent phase
            # offsets so x- and y-vibrations are decorrelated.
            cols = 10
            rows = max(1, n // cols)
            cw = (r.width  - 20) / cols
            ch = (r.height - 12) / max(rows, 1)
            for row in range(rows):
                for col in range(cols):
                    ox = r.left + 10 + col * cw + cw / 2
                    oy = r.top  +  6 + row * ch + ch / 2
                    self.pts.append({
                        "orig": [ox, oy],
                        "pos":  [ox, oy],
                        # independent phases for x and y
                        "phi_x": random.uniform(0.0, 6.28),
                        "phi_y": random.uniform(0.0, 6.28),
                        # slightly different angular frequencies (1–2 % spread)
                        "wx": random.uniform(4.8, 5.6),
                        "wy": random.uniform(4.4, 5.2),
                    })

        elif self.phase == "liquid":
            # Seed positions randomly; velocities will be overridden by the
            # stream-function field each frame, but we store them for drawing.
            for _ in range(n):
                x = random.uniform(r.left + 6, r.right  - 6)
                y = random.uniform(r.top  + 6, r.bottom - 6)
                self.pts.append({
                    "pos": [x, y],
                    "vx": 0.0, "vy": 0.0,
                })

        elif self.phase == "gas":
            for _ in range(n):
                x   = random.uniform(r.left + 6, r.right  - 6)
                y   = random.uniform(r.top  + 6, r.bottom - 6)
                ang = random.uniform(0.0, 6.28)
                spd = self._GAS_TARGET_SPD * random.uniform(0.6, 1.4)
                self.pts.append({
                    "pos": [x, y],
                    "vx": spd * math.cos(ang),
                    "vy": spd * math.sin(ang),
                })

    def resize(self, new_rect):
        if self.rect != new_rect:
            self.rect = new_rect
            self._init()

    # ── Stream-function velocity field ───────────────────────────────────────

    def _stream_vel(self, x, y, t):
        """Return (vx, vy) from the curl of the stream function at (x, y, t).
        Analytically divergence-free: represents incompressible 2-D flow."""
        vx = vy = 0.0
        for A, fx, fy, ox, oy in self._STREAM_MODES:
            sx = math.sin(fx * x + ox * t)
            cx = math.cos(fx * x + ox * t)
            sy = math.sin(fy * y + oy * t)
            cy = math.cos(fy * y + oy * t)
            #  d(psi)/dy =  A * sx * fy * cy
            # -d(psi)/dx = -A * fx * cx * sy
            vx += A * sx * fy * cy
            vy -= A * fx * cx * sy
        return vx, vy

    # ── Update ───────────────────────────────────────────────────────────────

    def update(self, t, T_K=300.0, T_melt=273.15):
        r = self.rect

        # ── SOLID: vibration amplitude proportional to T/T_melt ──────────
        if self.phase == "solid":
            # amp in [0.3, 4.5] pixels: near-zero at 0 K, ~4 px near melting
            T_ratio = max(0.0, T_K) / max(T_melt, 1.0)
            # Max amplitude ~1.8 px at melting point; near-zero at 0 K
            amp = max(0.15, min(1.8, T_ratio * 1.7))
            for p in self.pts:
                p["pos"][0] = p["orig"][0] + amp * math.sin(t * p["wx"] + p["phi_x"])
                p["pos"][1] = p["orig"][1] + amp * math.cos(t * p["wy"] + p["phi_y"])

        # ── LIQUID: advect through divergence-free velocity field ─────────
        # VEL_SCALE converts the raw stream-function velocity (~0.01 px/frame)
        # to a perceptible ~0.5-0.8 px/frame.  Still visibly slower than gas.
        elif self.phase == "liquid":
            VEL_SCALE = 55.0
            for p in self.pts:
                lx = p["pos"][0] - r.left
                ly = p["pos"][1] - r.top
                vx, vy = self._stream_vel(lx, ly, t)
                vx *= VEL_SCALE
                vy *= VEL_SCALE

                p["vx"] = vx
                p["vy"] = vy
                p["pos"][0] += vx
                p["pos"][1] += vy

                # Wrap at boundaries (periodic-like) for continuous flow
                if p["pos"][0] < r.left  + 4: p["pos"][0] = r.right  - 5
                if p["pos"][0] > r.right - 4: p["pos"][0] = r.left   + 5
                if p["pos"][1] < r.top   + 4: p["pos"][1] = r.bottom - 5
                if p["pos"][1] > r.bottom- 4: p["pos"][1] = r.top    + 5

        # ── GAS: Langevin / Brownian dynamics ────────────────────────────
        elif self.phase == "gas":
            σ = self._GAS_KICK_SIGMA
            γ = self._GAS_DAMPING
            v0 = self._GAS_TARGET_SPD
            for p in self.pts:
                # Random kick (Gaussian, independent x/y)
                p["vx"] += random.gauss(0.0, σ)
                p["vy"] += random.gauss(0.0, σ)

                # Soft speed regulation: damp if too fast, boost if too slow
                spd = math.hypot(p["vx"], p["vy"])
                if spd > 1e-6:
                    # Langevin damping toward target speed
                    factor = 1.0 - γ + γ * (v0 / spd)
                    p["vx"] *= factor
                    p["vy"] *= factor

                p["pos"][0] += p["vx"]
                p["pos"][1] += p["vy"]

                # Elastic reflection at walls
                if p["pos"][0] < r.left  + 4: p["vx"] =  abs(p["vx"]); p["pos"][0] = r.left  + 4
                if p["pos"][0] > r.right - 4: p["vx"] = -abs(p["vx"]); p["pos"][0] = r.right - 4
                if p["pos"][1] < r.top   + 4: p["vy"] =  abs(p["vy"]); p["pos"][1] = r.top   + 4
                if p["pos"][1] > r.bottom- 4: p["vy"] = -abs(p["vy"]); p["pos"][1] = r.bottom- 4

    # ── Draw ─────────────────────────────────────────────────────────────────

    def draw(self, surf, active):
        boost = 35 if active else 0
        col   = tuple(min(255, c + boost) for c in self.color)
        dim   = tuple(max(0, c - 55) for c in col)

        if self.phase == "solid":
            # Small filled squares — bond lines between nearest neighbours
            # give the lattice feel
            for p in self.pts:
                x, y = int(p["pos"][0]), int(p["pos"][1])
                pygame.draw.rect(surf, col, (x - 3, y - 3, 6, 6))

        elif self.phase == "liquid":
            # Circles with a velocity-direction streak showing local flow
            for p in self.pts:
                x, y = int(p["pos"][0]), int(p["pos"][1])
                pygame.draw.circle(surf, col, (x, y), 5)
                vl = math.hypot(p["vx"], p["vy"])
                if vl > 0.05:
                    scale = min(12.0, vl * 4.0)
                    ex = x + int(p["vx"] / vl * scale)
                    ey = y + int(p["vy"] / vl * scale)
                    pygame.draw.line(surf, dim, (x, y), (ex, ey), 1)

        elif self.phase == "gas":
            # Circles with a velocity arrow showing the Brownian trajectory
            for p in self.pts:
                x, y = int(p["pos"][0]), int(p["pos"][1])
                pygame.draw.circle(surf, col, (x, y), 4)
                vl = math.hypot(p["vx"], p["vy"])
                if vl > 1e-6:
                    ex = x + int(p["vx"] / vl * 10)
                    ey = y + int(p["vy"] / vl * 10)
                    pygame.draw.line(surf, dim, (x, y), (ex, ey), 1)

# ---------------------------------------------------------------------------
# Slider widget
# ---------------------------------------------------------------------------

class Slider:
    def __init__(self, x, y, w, h, vmin, vmax, value, label="", log=False):
        self.rect     = pygame.Rect(x, y, w, h)
        self.vmin     = vmin
        self.vmax     = vmax
        self.value    = value
        self.label    = label
        self.log      = log
        self.dragging = False
        self._upd()

    def _upd(self):
        if self.log:
            t = (math.log10(max(self.value, 1e-10)) - math.log10(self.vmin)) / \
                (math.log10(self.vmax) - math.log10(self.vmin))
        else:
            t = (self.value - self.vmin) / (self.vmax - self.vmin)
        self.kx = int(self.rect.x + max(0.0, min(1.0, t)) * self.rect.w)

    def set_value(self, v):
        self.value = max(self.vmin, min(self.vmax, v))
        self._upd()

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.dragging = True; self._from_x(ev.pos[0])
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self.dragging = False
        elif ev.type == pygame.MOUSEMOTION and self.dragging:
            self._from_x(ev.pos[0])

    def _from_x(self, mx):
        t = max(0.0, min(1.0, (mx - self.rect.x) / self.rect.w))
        if self.log:
            self.value = 10.0 ** (math.log10(self.vmin) + t *
                                  (math.log10(self.vmax) - math.log10(self.vmin)))
        else:
            self.value = self.vmin + t * (self.vmax - self.vmin)
        self._upd()

    def draw(self, surf, font):
        pygame.draw.rect(surf, SLIDER_BG, self.rect, border_radius=4)
        fw = max(0, self.kx - self.rect.x)
        pygame.draw.rect(surf, SLIDER_FG,
                         pygame.Rect(self.rect.x, self.rect.y, fw, self.rect.h),
                         border_radius=4)
        pygame.draw.rect(surf, BORDER, self.rect, 1, border_radius=4)
        pygame.draw.circle(surf, (220, 230, 255), (self.kx, self.rect.centery), 7)
        pygame.draw.circle(surf, BORDER,          (self.kx, self.rect.centery), 7, 1)
        surf.blit(font.render(self.label, True, DIM),
                  (self.rect.x, self.rect.y - 18))

# ---------------------------------------------------------------------------
# Button widget
# ---------------------------------------------------------------------------

class Button:
    def __init__(self, rect, label, color=PANEL2, active_color=ACCENT):
        self.rect         = pygame.Rect(rect)
        self.label        = label
        self.color        = color
        self.active_color = active_color
        self.active       = False
        self.hovered      = False

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(ev.pos)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                return True
        return False

    def draw(self, surf, font):
        col = (self.active_color if self.active
               else tuple(min(255, c + 18) for c in self.color) if self.hovered
               else self.color)
        pygame.draw.rect(surf, col,    self.rect, border_radius=6)
        pygame.draw.rect(surf, BORDER, self.rect, 1, border_radius=6)
        s = font.render(self.label, True, TEXT)
        surf.blit(s, s.get_rect(center=self.rect.center))

# ---------------------------------------------------------------------------
# Phase layer layout
# ---------------------------------------------------------------------------

PHASE_ORDER = ["gas", "liquid", "solid"]   # top to bottom
INACTIVE_H  = 120
CENTER_TOP  = 35
CENTER_BOT  = WIN_H - 20

def phase_heights(active):
    """All three phase layers have equal height regardless of which is active."""
    h = (CENTER_BOT - CENTER_TOP) // len(PHASE_ORDER)
    return {p: h for p in PHASE_ORDER}


def phase_layer_rects():
    """Return dict phase -> pygame.Rect for hit-testing (must call after heights)."""
    h = (CENTER_BOT - CENTER_TOP) // len(PHASE_ORDER)
    rects = {}
    cur_y = CENTER_TOP
    for ph in PHASE_ORDER:
        rects[ph] = pygame.Rect(MID_X + 2, cur_y, MID_W - 4, h)
        cur_y += h
    return rects

# ---------------------------------------------------------------------------
# Simulation state
# ---------------------------------------------------------------------------

class SimState:
    P_MIN, P_MAX = 0.001, 100.0

    def __init__(self):
        self.sub_idx = 1    # Water
        self.T_C = 20.0
        self.P   = 1.0

    # T range is dynamic — computed from the current substance.
    # Fixed margins: 50°C below mp (solid region) and 150°C above bp (gas region),
    # so the slider gives natural resolution across all three phases.
    @property
    def T_MIN(self):
        return round(self.sub["mp_K"] - 273.15 - 50.0, 0)

    @property
    def T_MAX(self):
        return round(self.sub["bp_K"] - 273.15 + 150.0, 0)

    @property
    def T_K(self): return self.T_C + 273.15

    @property
    def sub(self): return SUBSTANCES[SUBSTANCE_KEYS[self.sub_idx]]

    @property
    def phase(self): return determine_phase(self.sub, self.T_K, self.P)

    def snap(self, target):
        sub  = self.sub
        self.P = 1.0
        T_m  = sub["mp_K"]
        T_b  = sub["bp_K"]
        if target == "solid":
            self.T_C = T_m - 273.15 - 40.0
        elif target == "liquid":
            self.T_C = (T_m + T_b) / 2.0 - 273.15
        elif target == "gas":
            self.T_C = T_b - 273.15 + 40.0
        self.T_C = max(self.T_MIN, min(self.T_MAX, self.T_C))

# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

class PhaseTransitionSim:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("TSCG — Phase Transition Simulation")
        self.clock  = pygame.time.Clock()

        self.F = {k: pygame.font.SysFont("DejaVuSans", s, b)
                  for k, s, b in [("xl", 22, True), ("lg", 17, True),
                                   ("md", 15, False), ("sm", 13, False),
                                   ("xs", 11, False)]}

        self.st = SimState()
        self.t  = 0.0

        sx, sw = LEFT_X + PAD, LEFT_W - 2 * PAD
        self.sl_T = Slider(sx, WIN_H - 130, sw, 14,
                           self.st.T_MIN, self.st.T_MAX,
                           self.st.T_C, "Temperature (°C)", log=False)
        self.sl_P = Slider(sx, WIN_H - 80, sw, 14,
                           SimState.P_MIN, SimState.P_MAX,
                           self.st.P, "Pressure (atm) — log scale", log=True)

        self._mk_sub_btns()
        self._mk_state_btns()

        self._ps: dict[str, ParticleSystem] = {}
        self._ph_cache = ""
        self._si_cache = -1

    # ── Button builders ──────────────────────────────────────────────────────

    def _mk_sub_btns(self):
        bw = (LEFT_W - 2 * PAD - PAD) // 2
        bh = 28
        self.sub_btns = []
        for i, name in enumerate(SUBSTANCE_KEYS):
            col = i % 2
            row = i // 2
            btn = Button((LEFT_X + PAD + col * (bw + PAD), 55 + row * (bh + 6), bw, bh),
                         name, active_color=(60, 100, 180))
            btn.active = (i == self.st.sub_idx)
            self.sub_btns.append(btn)

    def _mk_state_btns(self):
        bw, bh = 106, 30
        by = WIN_H - 178
        specs = [("SOLID", (50,60,140)), ("LIQUID", (20,80,170)), ("GAS", (40,130,155))]
        self.state_btns = []
        for i, (lbl, col) in enumerate(specs):
            btn = Button((LEFT_X + PAD + i * (bw + 8), by, bw, bh), lbl,
                         color=tuple(c // 2 for c in col), active_color=col)
            self.state_btns.append(btn)

    # ── T slider range updater ──────────────────────────────────────────────

    def _update_T_range(self):
        """Rebuild T slider range based on current substance, clamping T_C."""
        tmin = self.st.T_MIN
        tmax = self.st.T_MAX
        self.sl_T.vmin = tmin
        self.sl_T.vmax = tmax
        self.st.T_C = max(tmin, min(tmax, self.st.T_C))
        self.sl_T.set_value(self.st.T_C)

    # ── Events ───────────────────────────────────────────────────────────────

    def events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: return False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return False

            for i, btn in enumerate(self.sub_btns):
                if btn.handle_event(ev):
                    self.st.sub_idx = i
                    for b in self.sub_btns: b.active = False
                    self.sub_btns[i].active = True
                    self._ps.clear()
                    # Adapt T slider range to the new substance
                    self._update_T_range()

            for i, btn in enumerate(self.state_btns):
                if btn.handle_event(ev):
                    self.st.snap(["solid", "liquid", "gas"][i])
                    self.sl_T.set_value(self.st.T_C)
                    self.sl_P.set_value(self.st.P)

            # Click on a phase layer in the center panel
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for ph, rect in phase_layer_rects().items():
                    if rect.collidepoint(ev.pos):
                        self.st.snap(ph)
                        self.sl_T.set_value(self.st.T_C)
                        self.sl_P.set_value(self.st.P)
                        break

            self.sl_T.handle_event(ev)
            self.sl_P.handle_event(ev)

        self.st.T_C = self.sl_T.value
        self.st.P   = self.sl_P.value
        return True

    # ── Particle management ──────────────────────────────────────────────────

    def _ensure_ps(self, heights):
        sub_col = self.st.sub["color"]
        phase   = self.st.phase
        si      = self.st.sub_idx

        if phase != self._ph_cache or si != self._si_cache:
            self._ps.clear()
            self._ph_cache = phase
            self._si_cache = si

        cur_y = CENTER_TOP
        for ph in PHASE_ORDER:
            h    = heights[ph]
            rect = pygame.Rect(MID_X + 4, cur_y + 4, MID_W - 8, h - 8)
            if ph not in self._ps:
                self._ps[ph] = ParticleSystem(ph, rect,
                                              phase_particle_color(ph, sub_col))
            else:
                self._ps[ph].resize(rect)
            cur_y += h

    # ── Main draw ────────────────────────────────────────────────────────────

    def draw(self):
        self.screen.fill(BG)
        heights = phase_heights(self.st.phase)
        self._ensure_ps(heights)
        sub    = self.st.sub
        T_melt = sub["mp_K"]
        for ps in self._ps.values():
            ps.update(self.t, T_K=self.st.T_K, T_melt=T_melt)
        self._left()
        self._center(heights)
        self._right()
        pygame.display.flip()

    # ── Text / panel helpers ─────────────────────────────────────────────────

    def _txt(self, font_key, text, x, y, color=TEXT, anchor="topleft"):
        s = self.F[font_key].render(text, True, color)
        r = s.get_rect(); setattr(r, anchor, (x, y))
        self.screen.blit(s, r)

    def _panel(self, rect, color=PANEL, border=True):
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        if border:
            pygame.draw.rect(self.screen, BORDER, rect, 1, border_radius=8)

    def _hline(self, x, y):
        pygame.draw.line(self.screen, BORDER,
                         (x, y), (RIGHT_X + RIGHT_W - PAD, y))

    def _bar(self, x, y, w, score, fill_col):
        pygame.draw.rect(self.screen, SLIDER_BG, (x, y, w, 11), border_radius=3)
        pygame.draw.rect(self.screen, fill_col,  (x, y, int(w * score), 11), border_radius=3)
        self._txt("xs", f"{score:.2f}", x + w + 4, y, TEXT)

    # ── Left panel ───────────────────────────────────────────────────────────

    def _left(self):
        self._panel(pygame.Rect(LEFT_X, 0, LEFT_W, WIN_H), PANEL)

        self._txt("xl", "PHASE TRANSITION", LEFT_X + PAD, 10, GOLD)
        self._txt("sm", "TSCG M0 Poclet Simulation", LEFT_X + PAD, 34, DIM)
        self._txt("sm", "Select Substance:", LEFT_X + PAD, 42, DIM)

        for btn in self.sub_btns:
            btn.draw(self.screen, self.F["sm"])

        self._txt("sm", "Jump to Phase:", LEFT_X + PAD, WIN_H - 195, DIM)
        for i, btn in enumerate(self.state_btns):
            btn.active = (self.st.phase == ["solid", "liquid", "gas"][i])
            btn.draw(self.screen, self.F["sm"])

        self.sl_T.draw(self.screen, self.F["sm"])
        self.sl_P.draw(self.screen, self.F["sm"])

        self._txt("md", f"T = {self.st.T_C:+.1f} C  ({self.st.T_K:.1f} K)",
                  LEFT_X + PAD, WIN_H - 55, TEXT)
        self._txt("xs",
                  f"range [{self.st.T_MIN:.0f} .. {self.st.T_MAX:.0f}] C",
                  LEFT_X + PAD, WIN_H - 43, DIM)
        self._txt("md", f"P = {self.st.P:.4g} atm",
                  LEFT_X + PAD, WIN_H - 36, TEXT)

        sub = self.st.sub
        P   = self.st.P
        y_s = WIN_H - 225
        self._txt("sm",
                  f"{SUBSTANCE_KEYS[self.st.sub_idx]}  "
                  f"({sub['formula']})  M = {sub['molar_mass']} g/mol",
                  LEFT_X + PAD, y_s, sub["color"])

        if sub.get("hazard"):
            self._txt("xs", f"WARN: {sub['hazard']}", LEFT_X + PAD, y_s + 14, RED_C)

        mp_C  = sub["mp_K"] - 273.15
        bp_C  = sub["bp_K"] - 273.15
        T_m_P = melting_point_at_P(sub, P) - 273.15
        T_b_P = boiling_point_at_P(sub, P) - 273.15
        self._txt("xs",
                  f"mp(1atm)={mp_C:.1f}C  bp(1atm)={bp_C:.1f}C",
                  LEFT_X + PAD, y_s - 28, DIM)
        self._txt("xs",
                  f"mp({P:.3g}atm)={T_m_P:.1f}C  bp({P:.3g}atm)={T_b_P:.1f}C",
                  LEFT_X + PAD, y_s - 15, DIM)

        if is_sublimating(sub, P):
            Ptp = sub["Ttp_Pa"] / ATM_PA
            extra = 28 if sub.get("hazard") else 14
            self._txt("xs",
                      f"** P < Ptp ({Ptp:.4f} atm) -- SUBLIMATION **",
                      LEFT_X + PAD, y_s + extra, GOLD)

    # ── Center panel ─────────────────────────────────────────────────────────

    def _center(self, heights):
        s     = self.screen
        phase = self.st.phase
        sub   = self.st.sub
        P     = self.st.P

        self._panel(pygame.Rect(MID_X, 0, MID_W, WIN_H), PANEL2)
        self._txt("xl", "Phase Layers",
                  MID_X + MID_W // 2, 8, TEXT, "midtop")

        BG  = {"gas": COL_GAS,  "liquid": COL_LIQUID, "solid": COL_SOLID}
        HL  = {"gas": HL_GAS,   "liquid": HL_LIQUID,  "solid": HL_SOLID}
        LBL = {"gas": "GAS",    "liquid": "LIQUID",   "solid": "SOLID"}
        DSC = {
            "gas":    "Rapid random motion  --  pV = nRT",
            "liquid": "Short-range order  --  free flow",
            "solid":  "Crystalline lattice  --  vibration only",
        }

        cur_y = CENTER_TOP
        for ph in PHASE_ORDER:
            h      = heights[ph]
            rect   = pygame.Rect(MID_X + 2, cur_y, MID_W - 4, h)
            active = (ph == phase)

            bg = lerp_color(BG[ph], (20, 20, 40), 0.2 if active else 0.0)
            self._panel(rect, bg)

            ps = self._ps.get(ph)
            if ps and active:
                ps.draw(s, active)

            if active:
                for thick in range(3, 0, -1):
                    pygame.draw.rect(s, HL[ph], rect, thick, border_radius=8)

            lbl_col  = HL[ph] if active else DIM
            lbl_font = self.F["xl"] if active else self.F["lg"]
            lbl_s    = lbl_font.render(LBL[ph], True, lbl_col)
            lx = rect.centerx - lbl_s.get_width()  // 2
            ly = rect.centery - lbl_s.get_height() // 2 - (12 if active and h > 110 else 0)
            s.blit(lbl_s, (lx, ly))

            if active and h > 90:
                d = self.F["sm"].render(DSC[ph], True, TEXT)
                s.blit(d, (rect.centerx - d.get_width() // 2,
                           ly + lbl_s.get_height() + 3))

            # Boundary temperature labels
            if ph != PHASE_ORDER[-1]:
                T_m = melting_point_at_P(sub, P) - 273.15
                T_b = boiling_point_at_P(sub, P) - 273.15
                next_ph = PHASE_ORDER[PHASE_ORDER.index(ph) + 1]
                bnd = {("gas", "liquid"):  (f"T_b = {T_b:.1f}C @ {P:.3g}atm", HL_GAS),
                       ("liquid", "solid"): (f"T_m = {T_m:.1f}C @ {P:.3g}atm", HL_LIQUID)}
                if (ph, next_ph) in bnd:
                    txt, col = bnd[(ph, next_ph)]
                    bs = self.F["xs"].render(txt, True, col)
                    s.blit(bs, (rect.left + 6, rect.bottom - 13))

            cur_y += h

    # ── Right panel ──────────────────────────────────────────────────────────

    def _right(self):
        s    = self.screen
        sub  = self.st.sub
        T_K  = self.st.T_K
        T_C  = self.st.T_C
        P    = self.st.P
        ph   = self.st.phase

        self._panel(pygame.Rect(RIGHT_X, 0, RIGHT_W, WIN_H), PANEL)
        x = RIGHT_X + PAD
        y = 12

        # Phase badge
        BC = {"solid": HL_SOLID, "liquid": HL_LIQUID, "gas": HL_GAS}
        bs = self.F["xl"].render(f"  {ph.upper()}  ", True, (8, 8, 18))
        br = bs.get_rect(topright=(RIGHT_X + RIGHT_W - PAD, y))
        pygame.draw.rect(s, BC[ph], br.inflate(10, 6), border_radius=6)
        s.blit(bs, br)

        self._txt("xl", "Properties", x, y, GOLD)
        y += 30

        self._txt("lg", SUBSTANCE_KEYS[self.st.sub_idx], x, y, sub["color"])
        y += 20
        self._txt("sm", f"Formula: {sub['formula']}    M = {sub['molar_mass']} g/mol", x, y, DIM)
        y += 16
        self._txt("sm", sub.get("note", ""), x, y, DIM)
        if sub.get("hazard"):
            y += 14
            self._txt("xs", f"WARN: {sub['hazard']}", x, y, RED_C)
        y += 18

        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y))
        y += 8
        self._txt("lg", "Phase Diagram Data", x, y, ACCENT)
        y += 22

        T_m_P = melting_point_at_P(sub, P)
        T_b_P = boiling_point_at_P(sub, P)
        rows = [
            ("mp (1 atm)",         f"{sub['mp_K']-273.15:.2f} C  ({sub['mp_K']:.2f} K)"),
            ("bp (1 atm)",         f"{sub['bp_K']-273.15:.2f} C  ({sub['bp_K']:.2f} K)"),
            (f"mp ({P:.3g} atm)",  f"{T_m_P-273.15:.2f} C  ({T_m_P:.2f} K)"),
            (f"bp ({P:.3g} atm)",  f"{T_b_P-273.15:.2f} C  ({T_b_P:.2f} K)"),
            ("Critical T",         f"{sub['Tc_K']-273.15:.1f} C   Pc = {sub['Pc_atm']:.1f} atm"),
            ("Triple point",       f"{sub['Ttp_K']-273.15:.2f} C,  {sub['Ttp_Pa']:.1f} Pa  "
                                   f"({sub['Ttp_Pa']/ATM_PA:.5f} atm)"),
            ("dH_vap",             f"{sub['dHvap']/1000:.2f} kJ/mol"),
            ("dH_fus",             f"{sub['dHfus']/1000:.2f} kJ/mol"),
        ]
        for lbl, val in rows:
            self._txt("sm", f"  {lbl}:", x, y, DIM)
            self._txt("sm", val, x + 158, y, TEXT)
            y += 17

        y += 4
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y))
        y += 8

        self._txt("lg", "Ideal Gas Law  pV = nRT", x, y, ACCENT)
        y += 22
        V = ideal_gas_volume_L(1.0, T_K, P)
        if ph == "gas":
            for line, col, fk in [
                (f"n = 1 mol", DIM, "sm"),
                (f"T = {T_K:.2f} K", DIM, "sm"),
                (f"P = {P*ATM_PA:.1f} Pa  ({P:.4g} atm)", DIM, "sm"),
                (f"V = nRT/P = {V:.4g} L", GREEN, "sm"),
                ("R = 8.314 J mol-1 K-1", DIM, "xs"),
                (f"V_STP (0C,1atm) = {ideal_gas_volume_L(1,273.15,1):.3f} L/mol", DIM, "xs"),
            ]:
                self._txt(fk, line, x, y, col)
                y += 16
        else:
            self._txt("sm", "(pV=nRT applies in gas phase)", x, y, DIM); y += 16
            self._txt("xs", f"Hyp. V = {V:.4g} L/mol at current T, P", x, y, DIM); y += 14

        y += 4
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y))
        y += 8

        self._txt("lg", "Clausius-Clapeyron  (bp vs P)", x, y, ACCENT)
        y += 20
        self._txt("xs", "ln(P2/P1) = (dHvap/R) * (1/T1 - 1/T2)", x, y, DIM)
        y += 14
        for p_ref in [0.01, 0.1, 1.0, 10.0, 100.0]:
            T_b_ref = boiling_point_at_P(sub, p_ref) - 273.15
            col = GOLD if abs(p_ref - 1.0) < 0.001 else DIM
            self._txt("xs", f"  bp({p_ref:.4g} atm) = {T_b_ref:.1f} C", x, y, col)
            y += 13

        y += 4
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y))
        y += 8

        self._txt("lg", "Gibbs Phase Rule  F = C - P + 2", x, y, ACCENT)
        y += 20
        for line in ["C = 1 (pure substance)",
                     "1 phase: F=2  (T,P both free)",
                     "2-phase coexist: F=1  (boundary curve)",
                     "Triple point: F=0  (unique T,P)"]:
            self._txt("xs", line, x, y, DIM); y += 13

        y += 4
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y))
        y += 8

        self._txt("lg", "ASFID Scores", x, y, ACCENT); y += 20
        bw = RIGHT_W - 2 * PAD - 125
        for lbl, sc in [("A Attractor", 0.92), ("S Structure", 0.88),
                        ("F Flow", 0.85), ("I Information", 0.80), ("D Dynamics", 0.90)]:
            self._txt("xs", lbl, x, y + 1, DIM)
            self._bar(x + 120, y, bw, sc, HL_GAS)
            y += 15
        self._txt("xs", "ASFID total = 0.87", x + 120, y, GOLD); y += 18

        self._txt("lg", "REVOI Scores", x, y, ACCENT); y += 20
        bw2 = RIGHT_W - 2 * PAD - 150
        for lbl, sc in [("R Representability", 0.90), ("E Evolvability", 0.75),
                        ("V Verifiability", 0.95), ("O Observability", 0.92),
                        ("I Interoperability", 0.88)]:
            self._txt("xs", lbl, x, y + 1, DIM)
            self._bar(x + 144, y, bw2, sc, (100, 200, 130))
            y += 15
        self._txt("xs", "REVOI = 0.88  |  Epistemic gap = 0.12", x + 144, y, GOLD)

    # ── Run loop ─────────────────────────────────────────────────────────────

    def run(self):
        while True:
            self.t += self.clock.tick(FPS) / 1000.0
            if not self.events():
                break
            self.draw()
        pygame.quit()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    PhaseTransitionSim().run()
