"""
phase_transition_sim.py
=======================
TSCG Poclet Simulation — Phase Transition (Solid / Liquid / Gas)
Author: Echopraxium with the collaboration of Claude AI
Version: 1.6.0  (2026-02-26)

Driven by the M0_PhaseTransition poclet.

Physics:
  - Ideal Gas Law:        pV = nRT  (n = 1 mol)
  - Clausius-Clapeyron:   ln(P2/P1) = (dHvap/R) * (1/T1 - 1/T2)
  - Gibbs Phase Rule:     F = C - P + 2

Particle animations (active phase only):
  - GAS    : Langevin / Brownian dynamics
  - LIQUID : Divergence-free stream-function (incompressible turbulence)
             + transient dashed bonds between close neighbours
  - SOLID  : Lattice vibrations proportional to T / T_melt
             + permanent solid bonds between grid neighbours

Seven reference substances with characteristic colours:
  Methanol (light grey), Water (light blue), Gallium (silver),
  Sulfur (vivid yellow), Iodine (deep violet), Camphor (ivory),
  Dichloromethane (pale grey-blue)

Layout (1440 x 820):
  LEFT   (370 px) : Substance selector + State buttons + T / P / V sliders
  CENTER (530 px) : 3 equal phase layers — click a layer to switch phase
  RIGHT  (540 px) : Properties — ideal gas law, Clausius-Clapeyron, ASFID/REVOI

Controls:
  Substance tabs         — select reference substance
  [SOLID][LIQUID][GAS]   — snap T, P, V to canonical values
  Click phase layer      — same as state buttons
  T slider               — temperature (range adapts to substance)
  P slider               — pressure [Pa], log scale
  V slider               — volume [m³], log scale; moves P at constant T
  ESC                    — quit

Requirements:  pip install pygame
Run:           python phase_transition_sim.py
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

COL_SOLID  = ( 50,  58, 105)
COL_LIQUID = ( 22,  80, 165)
COL_GAS    = ( 30, 108, 142)

HL_SOLID   = ( 88, 108, 195)
HL_LIQUID  = ( 48, 135, 235)
HL_GAS     = ( 88, 195, 225)

# ---------------------------------------------------------------------------
# Physics constants
# ---------------------------------------------------------------------------
R_GAS  = 8.314          # J mol-1 K-1
ATM_PA = 101_325.0      # Pa per atm
N_MOL  = 1.0            # fixed amount of substance

# Pressure slider range (Pa)
P_MIN_PA =       100.0   # ~0.001 atm
P_MAX_PA = 10_000_000.0  # ~99 atm

# Volume slider range (m3), log scale
V_MIN_M3 = 1e-5
V_MAX_M3 = 30.0

# ---------------------------------------------------------------------------
# Reference substances  — characteristic colours per substance
# ---------------------------------------------------------------------------
SUBSTANCES = {
    "Methanol": {
        "formula": "CH3OH", "molar_mass": 32.04,
        "mp_K": 175.60, "bp_K": 337.75,
        "dHvap": 35_200, "dHfus": 3_215,
        "Tc_K": 512.60, "Pc_atm": 79.8,
        "Ttp_K": 175.60, "Ttp_Pa": 0.18,
        "mp_slope": 0.01,
        # Light grey (transparent / colourless liquid)
        "color": (195, 198, 208),
        "note": "Highly toxic; colourless; cryogenic antifreeze",
        "hazard": "TOXIC: blindness/death",
    },
    "Water": {
        "formula": "H2O", "molar_mass": 18.015,
        "mp_K": 273.15, "bp_K": 373.15,
        "dHvap": 40_700, "dHfus": 6_010,
        "Tc_K": 647.10, "Pc_atm": 217.7,
        "Ttp_K": 273.16, "Ttp_Pa": 611.7,
        "mp_slope": -0.0075,
        # Light blue
        "color": ( 80, 170, 240),
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
        # Silver metallic grey
        "color": (192, 194, 205),
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
        # Vivid yellow
        "color": (245, 215,  18),
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
        # Deep violet
        "color": ( 95,  22, 135),
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
        # Off-white / ivory
        "color": (238, 232, 205),
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
        # Pale grey-blue
        "color": (155, 182, 210),
        "note": "Very low bp (39.6C); dense chlorinated lab solvent",
        "hazard": "Suspected carcinogen",
    },
}

SUBSTANCE_KEYS = list(SUBSTANCES.keys())

# ---------------------------------------------------------------------------
# Phase physics
# ---------------------------------------------------------------------------

def boiling_point_at_P(sub, P_Pa):
    """Clausius-Clapeyron: T_b at pressure P_Pa."""
    P_Pa = max(P_Pa, 1.0)
    T_b0 = sub["bp_K"]
    dHv  = sub["dHvap"]
    try:
        return max(1.0 / (1.0 / T_b0 - R_GAS / dHv * math.log(P_Pa / ATM_PA)), 0.1)
    except (ValueError, ZeroDivisionError):
        return T_b0

def melting_point_at_P(sub, P_Pa):
    P_atm = P_Pa / ATM_PA
    return sub["mp_K"] + sub.get("mp_slope", 0.01) * (P_atm - 1.0)

def determine_phase(sub, T_K, P_Pa):
    """Return 'solid' | 'liquid' | 'gas'."""
    T_m = melting_point_at_P(sub, P_Pa)
    if T_K < T_m:
        return "solid"
    if P_Pa < sub["Ttp_Pa"]:    # below triple-point pressure: no liquid
        return "gas"
    T_b = boiling_point_at_P(sub, P_Pa)
    if T_K < T_b:
        return "liquid"
    return "gas"

def ideal_gas_V(T_K, P_Pa):
    """Volume in m³ for n=1 mol: V = nRT/P."""
    return N_MOL * R_GAS * max(T_K, 1.0) / max(P_Pa, 1e-6)

def is_sublimating(sub, P_Pa):
    return P_Pa < sub["Ttp_Pa"]

def fmt_Pa(P_Pa):
    """Format pressure as SI string."""
    if P_Pa >= 1e6:
        return f"{P_Pa/1e6:.3g} MPa"
    if P_Pa >= 1e3:
        return f"{P_Pa/1e3:.4g} kPa"
    return f"{P_Pa:.4g} Pa"

def fmt_V(V_m3):
    """Format volume as SI string."""
    if V_m3 >= 1.0:
        return f"{V_m3:.3g} m³"
    if V_m3 >= 1e-3:
        return f"{V_m3*1e3:.3g} L"
    return f"{V_m3*1e6:.3g} mL"

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def phase_particle_color(phase, sub_col):
    """Blend substance colour strongly into the phase base colour."""
    base = {"solid": HL_SOLID, "liquid": HL_LIQUID, "gas": HL_GAS}[phase]
    return lerp_color(base, sub_col, 0.65)

def draw_dashed_line(surf, color, p1, p2, dash=6, gap=5):
    """Draw a dashed line between p1 and p2."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length < 1.0:
        return
    ux, uy = dx / length, dy / length
    step = dash + gap
    pos = 0.0
    while pos < length:
        end = min(pos + dash, length)
        sx = int(p1[0] + ux * pos)
        sy = int(p1[1] + uy * pos)
        ex = int(p1[0] + ux * end)
        ey = int(p1[1] + uy * end)
        pygame.draw.line(surf, color, (sx, sy), (ex, ey), 1)
        pos += step

# ---------------------------------------------------------------------------
# Particle system
# ---------------------------------------------------------------------------

# Liquid bond thresholds (computed from panel width at runtime)
LIQ_BOND_APPEAR_DIV  = 13   # bond forms when dist <= width / 13
LIQ_BOND_VANISH_DIV  = 12   # bond INSTANTLY killed when dist >  width / 12
LIQ_BOND_MAX         = 4    # max bonds per particle
BOND_RISE            = 0.12 # life increment per frame when in range

class ParticleSystem:
    """
    SOLID  — regular grid + stable bond lines + thermal vibrations (amp ∝ T/Tm)
    LIQUID — stream-function advection + transient dashed bonds between neighbours
    GAS    — Langevin / Brownian dynamics
    """

    COUNTS = {"solid": 72, "liquid": 123, "gas": 36}

    # Stream-function modes: (amplitude, freq_x, freq_y, omega_x, omega_y)
    _STREAM_MODES = [
        (0.55, 0.018, 0.015,  0.18, -0.14),
        (0.40, 0.042, 0.035, -0.28,  0.22),
        (0.25, 0.080, 0.065,  0.40, -0.32),
    ]
    _VEL_SCALE  = 66.0   # stream velocity → px/frame  (×1.2 vs v1.3)

    _GAS_DAMPING    = 0.04
    _GAS_KICK_SIGMA = 0.83   # ×1.5 vs v1.3
    _GAS_TARGET_SPD = 3.3    # ×1.5 vs v1.3

    def __init__(self, phase, rect, color):
        self.phase      = phase
        self.rect       = rect
        self.color      = color
        self.pts        = []
        self.bonds      = []          # solid: permanent (i,j) pairs
        self._bond_life: dict = {}    # liquid: (i,j) → float [0,1]
        self._init()

    # ── Init ──────────────────────────────────────────────────────────────────

    def _init(self):
        r = self.rect
        n = self.COUNTS[self.phase]
        self.pts   = []
        self.bonds = []
        self._bond_life = {}

        if self.phase == "solid":
            cols = 9
            rows = n // cols          # 72 / 9 = 8
            cw = (r.width  - 20) / cols
            ch = (r.height - 12) / max(rows, 1)
            idx = 0
            for row in range(rows):
                for col in range(cols):
                    ox = r.left + 10 + col * cw + cw / 2
                    oy = r.top  +  6 + row * ch + ch / 2
                    self.pts.append({
                        "orig": [ox, oy], "pos":  [ox, oy],
                        "phi_x": random.uniform(0.0, 6.28),
                        "phi_y": random.uniform(0.0, 6.28),
                        "wx": random.uniform(4.8, 5.6),
                        "wy": random.uniform(4.4, 5.2),
                        "row": row, "col": col,
                    })
                    idx += 1
            # Pre-compute nearest-neighbour bond pairs (right + down)
            for i, pi in enumerate(self.pts):
                for j, pj in enumerate(self.pts):
                    if j <= i:
                        continue
                    dr = abs(pi["row"] - pj["row"])
                    dc = abs(pi["col"] - pj["col"])
                    if (dr == 0 and dc == 1) or (dr == 1 and dc == 0):
                        self.bonds.append((i, j))

        elif self.phase == "liquid":
            for _ in range(n):
                x = random.uniform(r.left + 6, r.right  - 6)
                y = random.uniform(r.top  + 6, r.bottom - 6)
                # tx, ty : smoothed wall-turbulence vector
                # svx/svy: low-pass filtered total velocity (removes all jerkiness)
                self.pts.append({"pos": [x, y], "vx": 0.0, "vy": 0.0,
                                 "tx": 0.0, "ty": 0.0,
                                 "svx": 0.0, "svy": 0.0})

        elif self.phase == "gas":
            for _ in range(n):
                x   = random.uniform(r.left + 6, r.right  - 6)
                y   = random.uniform(r.top  + 6, r.bottom - 6)
                spd = self._GAS_TARGET_SPD * random.uniform(0.6, 1.4)
                ang = random.uniform(0.0, 6.28)
                self.pts.append({"pos": [x, y],
                                 "vx": spd * math.cos(ang),
                                 "vy": spd * math.sin(ang)})

    def resize(self, new_rect):
        if self.rect != new_rect:
            self.rect = new_rect
            self._init()

    # ── Stream-function ───────────────────────────────────────────────────────

    def _stream_vel(self, x, y, t):
        vx = vy = 0.0
        for A, fx, fy, ox, oy in self._STREAM_MODES:
            sx = math.sin(fx * x + ox * t); cx = math.cos(fx * x + ox * t)
            sy = math.sin(fy * y + oy * t); cy = math.cos(fy * y + oy * t)
            vx += A * sx * fy * cy
            vy -= A * fx * cx * sy
        return vx, vy

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, t, T_K=300.0, T_melt=273.15):
        r = self.rect

        if self.phase == "solid":
            T_ratio = max(0.0, T_K) / max(T_melt, 1.0)
            # ×0.8 speed factor: max amp 1.28 px at melting point
            amp = max(0.10, min(1.28, T_ratio * 1.20))
            for p in self.pts:
                p["pos"][0] = p["orig"][0] + amp * math.sin(t * p["wx"] + p["phi_x"])
                p["pos"][1] = p["orig"][1] + amp * math.cos(t * p["wy"] + p["phi_y"])

        elif self.phase == "liquid":
            S        = self._VEL_SCALE
            MARGIN     = max(16, r.width // 14)   # wall-repulsion zone
            TURB_AMP   = 1.68                      # peak wall-turbulence amplitude
            TURB_ALPHA = 0.03   # turbulence low-pass (0.03 → ~33 frame ramp)
            VEL_ALPHA  = 0.12   # total velocity low-pass  (0.12 → ~8 frame ramp)
            cx         = (r.left + r.right)  * 0.5
            cy         = (r.top  + r.bottom) * 0.5
            CENTRE_R   = min(r.width, r.height) * 0.22
            CENTRE_K   = 0.35
            RADIUS   = 5                         # particle draw radius (px)
            DIAM     = RADIUS * 2                # hard contact diameter (px)
            REPEL_R  = RADIUS * 4                # repulsion starts at 4× radius (20 px)
            REPEL_K  = 6.0                       # repulsion stiffness (stronger = less clustering)

            n = len(self.pts)

            # ── Phase 1: stream-function velocity + wall repulsion ────────────
            for p in self.pts:
                lx = p["pos"][0] - r.left
                ly = p["pos"][1] - r.top
                vx, vy = self._stream_vel(lx, ly, t)
                vx *= S; vy *= S

                x, y = p["pos"][0], p["pos"][1]
                # Desired turbulence: sum of wall contributions (deterministic direction,
                # random target amplitude that changes slowly via low-pass filter)
                tx_target = 0.0; ty_target = 0.0
                if x - r.left   < MARGIN:
                    tx_target += TURB_AMP * (1.0 - (x - r.left)   / MARGIN)
                if r.right  - x < MARGIN:
                    tx_target -= TURB_AMP * (1.0 - (r.right  - x) / MARGIN)
                if y - r.top    < MARGIN:
                    ty_target += TURB_AMP * (1.0 - (y - r.top)    / MARGIN)
                if r.bottom - y < MARGIN:
                    ty_target -= TURB_AMP * (1.0 - (r.bottom - y) / MARGIN)

                # Add small slowly-varying noise to the target (changes every ~40 frames)
                noise_scale = 0.10
                tx_target += noise_scale * math.sin(t * 0.7 + p["tx"] * 3.1)
                ty_target += noise_scale * math.cos(t * 0.6 + p["ty"] * 2.9)

                # Low-pass filter: tx/ty smoothly track the target
                p["tx"] += TURB_ALPHA * (tx_target - p["tx"])
                p["ty"] += TURB_ALPHA * (ty_target - p["ty"])
                vx += p["tx"]; vy += p["ty"]

                # Gentle centrifugal push near panel centre (prevents central clustering)
                dcx = x - cx; dcy = y - cy
                dc  = math.hypot(dcx, dcy)
                if dc < CENTRE_R and dc > 1e-4:
                    scale = CENTRE_K * (1.0 - dc / CENTRE_R)
                    vx += (dcx / dc) * scale
                    vy += (dcy / dc) * scale

                # Low-pass filter on total velocity: smooths out all sudden changes
                p["svx"] += VEL_ALPHA * (vx - p["svx"])
                p["svy"] += VEL_ALPHA * (vy - p["svy"])
                p["vx"] = p["svx"]; p["vy"] = p["svy"]
                p["pos"][0] += p["svx"]; p["pos"][1] += p["svy"]

            # ── Phase 2: particle-particle repulsion (soft sphere) ────────────
            # For each overlapping pair push both particles apart by half the
            # overlap distance, preventing visual superposition.
            for i in range(n):
                for j in range(i + 1, n):
                    dx = self.pts[j]["pos"][0] - self.pts[i]["pos"][0]
                    dy = self.pts[j]["pos"][1] - self.pts[i]["pos"][1]
                    dist = math.hypot(dx, dy)
                    if dist < REPEL_R and dist > 1e-4:
                        # Linear repulsion: strongest at contact, zero at REPEL_R
                        overlap  = REPEL_R - dist
                        ux = dx / dist; uy = dy / dist
                        push = overlap * REPEL_K * 0.5 / REPEL_R * DIAM
                        self.pts[i]["pos"][0] -= ux * push
                        self.pts[i]["pos"][1] -= uy * push
                        self.pts[j]["pos"][0] += ux * push
                        self.pts[j]["pos"][1] += uy * push
                    elif dist <= 1e-4:
                        # Exact overlap: push in random direction
                        ang = random.uniform(0, 6.2832)
                        self.pts[i]["pos"][0] -= math.cos(ang) * REPEL_R * 0.5
                        self.pts[i]["pos"][1] -= math.sin(ang) * REPEL_R * 0.5
                        self.pts[j]["pos"][0] += math.cos(ang) * REPEL_R * 0.5
                        self.pts[j]["pos"][1] += math.sin(ang) * REPEL_R * 0.5

            # ── Phase 3: hard clamp — particles can NEVER leave the rect ─────
            for p in self.pts:
                if p["pos"][0] < r.left  + 2:
                    p["pos"][0] = r.left  + 2
                    p["vx"] = abs(p["vx"]) * 0.6
                if p["pos"][0] > r.right - 2:
                    p["pos"][0] = r.right - 2
                    p["vx"] = -abs(p["vx"]) * 0.6
                if p["pos"][1] < r.top   + 2:
                    p["pos"][1] = r.top   + 2
                    p["vy"] = abs(p["vy"]) * 0.6
                if p["pos"][1] > r.bottom - 2:
                    p["pos"][1] = r.bottom - 2
                    p["vy"] = -abs(p["vy"]) * 0.6
            # Update bond lifetimes
            # appear_thresh = width/13 ; vanish_thresh = width/12
            # When dist > vanish_thresh → bond is IMMEDIATELY destroyed (hard-kill).
            # This prevents long cross-panel lines if particles are far apart.
            appear_thresh = r.width / LIQ_BOND_APPEAR_DIV
            vanish_thresh = r.width / LIQ_BOND_VANISH_DIV
            n             = len(self.pts)

            # Step 1: keep / strengthen existing bonds; hard-kill any that exceed vanish_thresh
            new_life: dict = {}
            for key, life in self._bond_life.items():
                i, j = key
                dist = math.hypot(self.pts[i]["pos"][0] - self.pts[j]["pos"][0],
                                  self.pts[i]["pos"][1] - self.pts[j]["pos"][1])
                if dist > vanish_thresh:
                    continue            # hard-kill: drop from dict immediately
                life = min(1.0, life + BOND_RISE)
                new_life[key] = life

            # Step 2: count current degree per particle
            degree = [0] * n
            for (i, j) in new_life:
                degree[i] += 1; degree[j] += 1

            # Step 3: form new bonds for close pairs not yet bonded,
            #         respecting the max-degree constraint; closest pairs first
            candidates = []
            for i in range(n):
                if degree[i] >= LIQ_BOND_MAX:
                    continue
                for j in range(i + 1, n):
                    if degree[j] >= LIQ_BOND_MAX:
                        continue
                    if (i, j) in new_life:
                        continue
                    dist = math.hypot(self.pts[i]["pos"][0] - self.pts[j]["pos"][0],
                                      self.pts[i]["pos"][1] - self.pts[j]["pos"][1])
                    if dist <= appear_thresh:
                        candidates.append((dist, i, j))
            candidates.sort()

            for dist, i, j in candidates:
                if degree[i] < LIQ_BOND_MAX and degree[j] < LIQ_BOND_MAX:
                    new_life[(i, j)] = BOND_RISE
                    degree[i] += 1; degree[j] += 1

            self._bond_life = new_life

        elif self.phase == "gas":
            σ = self._GAS_KICK_SIGMA; γ = self._GAS_DAMPING; v0 = self._GAS_TARGET_SPD
            for p in self.pts:
                p["vx"] += random.gauss(0.0, σ); p["vy"] += random.gauss(0.0, σ)
                spd = math.hypot(p["vx"], p["vy"])
                if spd > 1e-6:
                    f = 1.0 - γ + γ * (v0 / spd)
                    p["vx"] *= f; p["vy"] *= f
                p["pos"][0] += p["vx"]; p["pos"][1] += p["vy"]
                if p["pos"][0] < r.left  + 4: p["vx"] =  abs(p["vx"]); p["pos"][0] = r.left  + 4
                if p["pos"][0] > r.right - 4: p["vx"] = -abs(p["vx"]); p["pos"][0] = r.right - 4
                if p["pos"][1] < r.top   + 4: p["vy"] =  abs(p["vy"]); p["pos"][1] = r.top   + 4
                if p["pos"][1] > r.bottom- 4: p["vy"] = -abs(p["vy"]); p["pos"][1] = r.bottom- 4

    # ── Draw ─────────────────────────────────────────────────────────────────

    def draw(self, surf):
        col  = tuple(min(255, c + 35) for c in self.color)
        dim  = tuple(max(0, c - 45)  for c in col)
        bond_col = tuple(max(0, c - 80) for c in col)

        if self.phase == "solid":
            # Stable bond lines first (drawn under particles)
            for (i, j) in self.bonds:
                pi = self.pts[i]; pj = self.pts[j]
                pygame.draw.line(surf, bond_col,
                                 (int(pi["pos"][0]), int(pi["pos"][1])),
                                 (int(pj["pos"][0]), int(pj["pos"][1])), 1)
            # Particles
            for p in self.pts:
                x, y = int(p["pos"][0]), int(p["pos"][1])
                pygame.draw.rect(surf, col, (x - 3, y - 3, 6, 6))

        elif self.phase == "liquid":
            # Transient dashed bonds (drawn under particles)
            vanish_draw = self.rect.width / LIQ_BOND_VANISH_DIV
            for (i, j), life in self._bond_life.items():
                if life < 0.05:
                    continue
                pi = self.pts[i]; pj = self.pts[j]
                # Safety guard: never draw a bond longer than vanish_thresh
                # (safety: never draw a bond longer than vanish_thresh)
                dist = math.hypot(pi["pos"][0] - pj["pos"][0],
                                  pi["pos"][1] - pj["pos"][1])
                if dist > vanish_draw:
                    continue
                bc = tuple(max(0, min(255, int(c * life))) for c in bond_col)
                if bc[0] + bc[1] + bc[2] > 10:
                    draw_dashed_line(surf, bc,
                                     (int(pi["pos"][0]), int(pi["pos"][1])),
                                     (int(pj["pos"][0]), int(pj["pos"][1])),
                                     dash=5, gap=4)
            # Particles
            for p in self.pts:
                x, y = int(p["pos"][0]), int(p["pos"][1])
                pygame.draw.circle(surf, col, (x, y), 5)
                vl = math.hypot(p["vx"], p["vy"])
                if vl > 0.05:
                    sc = min(10.0, vl * 3.5)
                    ex = x + int(p["vx"] / vl * sc)
                    ey = y + int(p["vy"] / vl * sc)
                    pygame.draw.line(surf, dim, (x, y), (ex, ey), 1)

        elif self.phase == "gas":
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
            t = (math.log10(max(self.value, 1e-30)) - math.log10(self.vmin)) / \
                (math.log10(self.vmax) - math.log10(self.vmin))
        else:
            t = (self.value - self.vmin) / (self.vmax - self.vmin)
        self.kx = int(self.rect.x + max(0.0, min(1.0, t)) * self.rect.w)

    def set_value(self, v):
        self.value = max(self.vmin, min(self.vmax, v))
        self._upd()

    def handle_event(self, ev):
        moved = False
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.dragging = True; self._from_x(ev.pos[0]); moved = True
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self.dragging = False
        elif ev.type == pygame.MOUSEMOTION and self.dragging:
            self._from_x(ev.pos[0]); moved = True
        return moved

    def _from_x(self, mx):
        t = max(0.0, min(1.0, (mx - self.rect.x) / self.rect.w))
        if self.log:
            self.value = 10.0 ** (math.log10(self.vmin) +
                                  t * (math.log10(self.vmax) - math.log10(self.vmin)))
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

PHASE_ORDER = ["gas", "liquid", "solid"]   # top → bottom
CENTER_TOP  = 35
CENTER_BOT  = WIN_H - 20

def phase_heights():
    h = (CENTER_BOT - CENTER_TOP) // len(PHASE_ORDER)
    return {p: h for p in PHASE_ORDER}

def phase_layer_rects():
    h = (CENTER_BOT - CENTER_TOP) // len(PHASE_ORDER)
    rects = {}; cur_y = CENTER_TOP
    for ph in PHASE_ORDER:
        rects[ph] = pygame.Rect(MID_X + 2, cur_y, MID_W - 4, h)
        cur_y += h
    return rects

# ---------------------------------------------------------------------------
# Simulation state
# ---------------------------------------------------------------------------

class SimState:
    P_MIN_PA = P_MIN_PA
    P_MAX_PA = P_MAX_PA

    def __init__(self):
        self.sub_idx = 1           # Water
        self.T_C     = 20.0
        self.P_Pa    = ATM_PA      # 101 325 Pa

    # ── Dynamic T range based on substance ───────────────────────────────────
    @property
    def T_MIN(self): return round(self.sub["mp_K"] - 273.15 - 50.0, 0)
    @property
    def T_MAX(self): return round(self.sub["bp_K"] - 273.15 + 150.0, 0)

    @property
    def T_K(self): return self.T_C + 273.15

    @property
    def sub(self): return SUBSTANCES[SUBSTANCE_KEYS[self.sub_idx]]

    @property
    def phase(self): return determine_phase(self.sub, self.T_K, self.P_Pa)

    # ── Volume (ideal gas, n=1 mol) ──────────────────────────────────────────
    @property
    def V_m3(self): return ideal_gas_V(self.T_K, self.P_Pa)

    def set_V(self, V_m3):
        """Isothermal: move V → update P."""
        V = max(V_MIN_M3, min(V_MAX_M3, V_m3))
        self.P_Pa = N_MOL * R_GAS * self.T_K / V

    # ── Snap to phase ────────────────────────────────────────────────────────
    def snap(self, target):
        sub  = self.sub
        self.P_Pa = ATM_PA
        T_m = sub["mp_K"]; T_b = sub["bp_K"]
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

        # Three sliders stacked in bottom of left panel
        sx, sw = LEFT_X + PAD, LEFT_W - 2 * PAD
        self.sl_T = Slider(sx, WIN_H - 168, sw, 14,
                           self.st.T_MIN, self.st.T_MAX,
                           self.st.T_C, "Temperature (°C)", log=False)
        self.sl_P = Slider(sx, WIN_H - 118, sw, 14,
                           P_MIN_PA, P_MAX_PA,
                           self.st.P_Pa, "Pressure (Pa, log)", log=True)
        self.sl_V = Slider(sx, WIN_H - 68, sw, 14,
                           V_MIN_M3, V_MAX_M3,
                           self.st.V_m3, "Volume m³ (n=1 mol, log)", log=True)

        self._mk_sub_btns()
        self._mk_state_btns()

        self._ps: dict[str, ParticleSystem] = {}
        self._ph_cache = ""
        self._si_cache = -1

    # ── Button builders ──────────────────────────────────────────────────────

    def _mk_sub_btns(self):
        bw = (LEFT_W - 2 * PAD - PAD) // 2
        bh = 26
        self.sub_btns = []
        for i, name in enumerate(SUBSTANCE_KEYS):
            btn = Button((LEFT_X + PAD + (i % 2) * (bw + PAD),
                          52 + (i // 2) * (bh + 5), bw, bh),
                         name, active_color=(60, 100, 180))
            btn.active = (i == self.st.sub_idx)
            self.sub_btns.append(btn)

    def _mk_state_btns(self):
        bw, bh = 104, 28
        by = WIN_H - 215
        specs = [("SOLID", (50,60,140)), ("LIQUID", (20,80,170)), ("GAS", (40,130,155))]
        self.state_btns = []
        for i, (lbl, col) in enumerate(specs):
            btn = Button((LEFT_X + PAD + i * (bw + 8), by, bw, bh), lbl,
                         color=tuple(c // 2 for c in col), active_color=col)
            self.state_btns.append(btn)

    # ── T slider range updater ────────────────────────────────────────────────

    def _update_T_range(self):
        tmin, tmax = self.st.T_MIN, self.st.T_MAX
        self.sl_T.vmin = tmin; self.sl_T.vmax = tmax
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
                    self._update_T_range()

            for i, btn in enumerate(self.state_btns):
                if btn.handle_event(ev):
                    self.st.snap(["solid", "liquid", "gas"][i])
                    self._sync_sliders_from_state()

            # Click on phase layer in center panel
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for ph, rect in phase_layer_rects().items():
                    if rect.collidepoint(ev.pos):
                        self.st.snap(ph)
                        self._sync_sliders_from_state()
                        break

            # Sliders — track which moved to sync V↔P
            moved_T = self.sl_T.handle_event(ev)
            moved_P = self.sl_P.handle_event(ev)
            moved_V = self.sl_V.handle_event(ev)

            if moved_T:
                self.st.T_C  = self.sl_T.value
                # T changed → recompute V at current P (isothermal → V = nRT/P)
                self.sl_V.set_value(self.st.V_m3)
            if moved_P:
                self.st.P_Pa = self.sl_P.value
                self.sl_V.set_value(self.st.V_m3)
            if moved_V:
                self.st.set_V(self.sl_V.value)
                self.sl_P.set_value(self.st.P_Pa)

        # Always sync state from sliders
        self.st.T_C  = self.sl_T.value
        self.st.P_Pa = self.sl_P.value
        return True

    def _sync_sliders_from_state(self):
        self.sl_T.set_value(self.st.T_C)
        self.sl_P.set_value(self.st.P_Pa)
        self.sl_V.set_value(self.st.V_m3)

    # ── Particle management ───────────────────────────────────────────────────

    def _ensure_ps(self, heights):
        sub_col = self.st.sub["color"]
        phase   = self.st.phase
        si      = self.st.sub_idx
        if phase != self._ph_cache or si != self._si_cache:
            self._ps.clear()
            self._ph_cache = phase; self._si_cache = si
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

    # ── Main draw ─────────────────────────────────────────────────────────────

    def draw(self):
        self.screen.fill(BG)
        heights = phase_heights()
        self._ensure_ps(heights)
        sub = self.st.sub
        for ps in self._ps.values():
            ps.update(self.t, T_K=self.st.T_K, T_melt=sub["mp_K"])
        self._left()
        self._center(heights)
        self._right()
        pygame.display.flip()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _txt(self, fk, text, x, y, color=TEXT, anchor="topleft"):
        s = self.F[fk].render(text, True, color)
        r = s.get_rect(); setattr(r, anchor, (x, y))
        self.screen.blit(s, r)

    def _panel(self, rect, color=PANEL, border=True):
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        if border:
            pygame.draw.rect(self.screen, BORDER, rect, 1, border_radius=8)

    def _hline(self, x, y):
        pygame.draw.line(self.screen, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y))

    def _bar(self, x, y, w, score, fill_col):
        pygame.draw.rect(self.screen, SLIDER_BG, (x, y, w, 11), border_radius=3)
        pygame.draw.rect(self.screen, fill_col,  (x, y, int(w * score), 11), border_radius=3)
        self._txt("xs", f"{score:.2f}", x + w + 4, y, TEXT)

    # ── Left panel ────────────────────────────────────────────────────────────

    def _left(self):
        sub = self.st.sub
        P   = self.st.P_Pa

        self._panel(pygame.Rect(LEFT_X, 0, LEFT_W, WIN_H), PANEL)
        self._txt("xl", "PHASE TRANSITION", LEFT_X + PAD, 10, GOLD)
        self._txt("sm", "TSCG M0 Poclet Simulation", LEFT_X + PAD, 34, DIM)
        self._txt("sm", "Select Substance:", LEFT_X + PAD, 40, DIM)

        for btn in self.sub_btns:
            btn.draw(self.screen, self.F["sm"])

        # Substance colour swatch
        sub_name = SUBSTANCE_KEYS[self.st.sub_idx]
        y_s = WIN_H - 252
        pygame.draw.rect(self.screen, sub["color"], (LEFT_X + PAD, y_s, 12, 12), border_radius=2)
        self._txt("sm",
                  f"  {sub_name} ({sub['formula']})  M={sub['molar_mass']} g/mol",
                  LEFT_X + PAD + 14, y_s, sub["color"])
        if sub.get("hazard"):
            self._txt("xs", f"WARN: {sub['hazard']}", LEFT_X + PAD, y_s + 14, RED_C)

        # mp / bp info
        T_m_P = melting_point_at_P(sub, P) - 273.15
        T_b_P = boiling_point_at_P(sub, P) - 273.15
        mp_C  = sub["mp_K"] - 273.15; bp_C = sub["bp_K"] - 273.15
        self._txt("xs", f"mp(1atm)={mp_C:.1f}C  bp(1atm)={bp_C:.1f}C",
                  LEFT_X + PAD, y_s - 26, DIM)
        self._txt("xs", f"mp({fmt_Pa(P)})={T_m_P:.1f}C  bp({fmt_Pa(P)})={T_b_P:.1f}C",
                  LEFT_X + PAD, y_s - 13, DIM)
        if is_sublimating(sub, P):
            extra = 28 if sub.get("hazard") else 14
            self._txt("xs",
                      f"** P < Ptp ({fmt_Pa(sub['Ttp_Pa'])}) -- SUBLIMATION **",
                      LEFT_X + PAD, y_s + extra, GOLD)

        # State buttons
        by = WIN_H - 215
        self._txt("sm", "Jump to Phase:", LEFT_X + PAD, by - 14, DIM)
        for i, btn in enumerate(self.state_btns):
            btn.active = (self.st.phase == ["solid", "liquid", "gas"][i])
            btn.draw(self.screen, self.F["sm"])

        # Sliders
        self.sl_T.draw(self.screen, self.F["sm"])
        self.sl_P.draw(self.screen, self.F["sm"])
        self.sl_V.draw(self.screen, self.F["sm"])

        # Live readout
        self._txt("xs", f"T = {self.st.T_C:+.1f} C  ({self.st.T_K:.1f} K)  "
                        f"[{self.st.T_MIN:.0f}..{self.st.T_MAX:.0f}]",
                  LEFT_X + PAD, WIN_H - 49, TEXT)
        self._txt("xs", f"P = {fmt_Pa(self.st.P_Pa)}  "
                        f"({self.st.P_Pa/ATM_PA:.4g} atm)",
                  LEFT_X + PAD, WIN_H - 36, TEXT)
        self._txt("xs", f"V = {fmt_V(self.st.V_m3)}  (n=1 mol, ideal gas)",
                  LEFT_X + PAD, WIN_H - 23, TEXT)

    # ── Center panel ──────────────────────────────────────────────────────────

    def _center(self, heights):
        s     = self.screen
        phase = self.st.phase
        sub   = self.st.sub
        P     = self.st.P_Pa

        self._panel(pygame.Rect(MID_X, 0, MID_W, WIN_H), PANEL2)
        self._txt("xl", "Phase Layers",
                  MID_X + MID_W // 2, 8, TEXT, "midtop")

        BG_C  = {"gas": COL_GAS,  "liquid": COL_LIQUID, "solid": COL_SOLID}
        HL_C  = {"gas": HL_GAS,   "liquid": HL_LIQUID,  "solid": HL_SOLID}
        LBLS  = {"gas": "GAS",    "liquid": "LIQUID",   "solid": "SOLID"}
        DESCS = {
            "gas":    "Rapid random motion  --  pV = nRT",
            "liquid": "Short-range order  --  turbulent flow",
            "solid":  "Crystalline lattice  --  thermal vibration",
        }
        HINTS = {"gas": "click to jump to gas", "liquid": "click to jump to liquid",
                 "solid": "click to jump to solid"}

        cur_y = CENTER_TOP
        for ph in PHASE_ORDER:
            h      = heights[ph]
            rect   = pygame.Rect(MID_X + 2, cur_y, MID_W - 4, h)
            active = (ph == phase)

            bg = lerp_color(BG_C[ph], (20, 20, 40), 0.2 if active else 0.0)
            self._panel(rect, bg)

            # Active phase: draw particles
            ps = self._ps.get(ph)
            if ps and active:
                ps.draw(s)

            # Active glow border
            if active:
                for thick in range(3, 0, -1):
                    pygame.draw.rect(s, HL_C[ph], rect, thick, border_radius=8)

            # Label
            lbl_col  = HL_C[ph] if active else DIM
            lbl_font = self.F["xl"] if active else self.F["lg"]
            lbl_s    = lbl_font.render(LBLS[ph], True, lbl_col)
            lx = rect.centerx - lbl_s.get_width()  // 2
            ly = rect.centery - lbl_s.get_height() // 2 - (10 if active else 0)
            s.blit(lbl_s, (lx, ly))

            if active:
                d = self.F["sm"].render(DESCS[ph], True, TEXT)
                s.blit(d, (rect.centerx - d.get_width() // 2,
                           ly + lbl_s.get_height() + 3))
            else:
                # Hint "click to ..." on inactive layers
                hint = self.F["xs"].render(HINTS[ph], True, DIM)
                s.blit(hint, (rect.right - hint.get_width() - 8, rect.bottom - 13))

            # Boundary temperature label
            if ph != PHASE_ORDER[-1]:
                T_m = melting_point_at_P(sub, P) - 273.15
                T_b = boiling_point_at_P(sub, P) - 273.15
                next_ph = PHASE_ORDER[PHASE_ORDER.index(ph) + 1]
                bnd = {
                    ("gas",    "liquid"): (f"T_b = {T_b:.1f}C @ {fmt_Pa(P)}", HL_GAS),
                    ("liquid", "solid"):  (f"T_m = {T_m:.1f}C @ {fmt_Pa(P)}", HL_LIQUID),
                }
                if (ph, next_ph) in bnd:
                    txt, col = bnd[(ph, next_ph)]
                    bs = self.F["xs"].render(txt, True, col)
                    s.blit(bs, (rect.left + 6, rect.bottom - 13))

            cur_y += h

    # ── Right panel ───────────────────────────────────────────────────────────

    def _right(self):
        s    = self.screen
        sub  = self.st.sub
        T_K  = self.st.T_K
        T_C  = self.st.T_C
        P_Pa = self.st.P_Pa
        V    = self.st.V_m3
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

        # Substance colour swatch + name
        pygame.draw.rect(s, sub["color"], (x, y + 2, 14, 18), border_radius=3)
        self._txt("xl", "Properties", x + 18, y, GOLD)
        y += 30

        self._txt("lg", SUBSTANCE_KEYS[self.st.sub_idx], x, y, sub["color"])
        y += 20
        self._txt("sm", f"Formula: {sub['formula']}    M = {sub['molar_mass']} g/mol", x, y, DIM)
        y += 15
        self._txt("sm", sub.get("note", ""), x, y, DIM)
        if sub.get("hazard"):
            y += 13
            self._txt("xs", f"WARN: {sub['hazard']}", x, y, RED_C)
        y += 16

        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y)); y += 7
        self._txt("lg", "Phase Diagram Data", x, y, ACCENT); y += 20

        T_m_P = melting_point_at_P(sub, P_Pa)
        T_b_P = boiling_point_at_P(sub, P_Pa)
        rows = [
            ("mp (1 atm)",              f"{sub['mp_K']-273.15:.2f} C  ({sub['mp_K']:.2f} K)"),
            ("bp (1 atm)",              f"{sub['bp_K']-273.15:.2f} C  ({sub['bp_K']:.2f} K)"),
            (f"mp ({fmt_Pa(P_Pa)})",    f"{T_m_P-273.15:.2f} C  ({T_m_P:.2f} K)"),
            (f"bp ({fmt_Pa(P_Pa)})",    f"{T_b_P-273.15:.2f} C  ({T_b_P:.2f} K)"),
            ("Critical T",              f"{sub['Tc_K']-273.15:.1f} C   "
                                        f"Pc = {sub['Pc_atm']*ATM_PA/1000:.0f} kPa"),
            ("Triple point",            f"{sub['Ttp_K']-273.15:.2f} C,  "
                                        f"{fmt_Pa(sub['Ttp_Pa'])}"),
            ("dH_vap",                  f"{sub['dHvap']/1000:.2f} kJ/mol"),
            ("dH_fus",                  f"{sub['dHfus']/1000:.2f} kJ/mol"),
        ]
        for lbl, val in rows:
            self._txt("sm", f"  {lbl}:", x, y, DIM)
            self._txt("sm", val, x + 150, y, TEXT)
            y += 16

        y += 3
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y)); y += 7

        self._txt("lg", "Ideal Gas Law  pV = nRT  (n = 1 mol)", x, y, ACCENT); y += 20
        P_display = fmt_Pa(P_Pa)
        P_atm     = P_Pa / ATM_PA
        if ph == "gas":
            for line, col, fk in [
                (f"T = {T_K:.2f} K", DIM, "sm"),
                (f"P = {P_display}  ({P_atm:.4g} atm)", DIM, "sm"),
                (f"V = nRT/P = {fmt_V(V)}  ({V:.4e} m³)", GREEN, "sm"),
                ("R = 8.314 J mol-1 K-1", DIM, "xs"),
                (f"V_STP (0C,101325Pa) = {ideal_gas_V(273.15, ATM_PA)*1000:.3f} L", DIM, "xs"),
            ]:
                self._txt(fk, line, x, y, col); y += 15
        else:
            self._txt("sm", "(pV=nRT applies in gas phase)", x, y, DIM); y += 15
            self._txt("xs", f"Hyp. V = {fmt_V(V)} at current T, P", x, y, DIM); y += 13

        y += 3
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y)); y += 7

        self._txt("lg", "Clausius-Clapeyron  (bp vs P)", x, y, ACCENT); y += 18
        self._txt("xs", "ln(P2/P1) = (dHvap/R) * (1/T1 - 1/T2)", x, y, DIM); y += 13
        for p_ref_atm in [0.01, 0.1, 1.0, 10.0, 100.0]:
            p_ref_Pa  = p_ref_atm * ATM_PA
            T_b_ref   = boiling_point_at_P(sub, p_ref_Pa) - 273.15
            col = GOLD if abs(p_ref_atm - 1.0) < 0.001 else DIM
            self._txt("xs",
                      f"  bp({fmt_Pa(p_ref_Pa)}) = {T_b_ref:.1f} C",
                      x, y, col); y += 12

        y += 3
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y)); y += 7

        self._txt("lg", "Gibbs Phase Rule  F = C - P + 2", x, y, ACCENT); y += 18
        for line in ["C=1 (pure substance)",
                     "1 phase: F=2  (T,P both free)",
                     "2-phase coexist: F=1  (boundary curve)",
                     "Triple point: F=0  (unique T,P)"]:
            self._txt("xs", line, x, y, DIM); y += 12

        y += 3
        pygame.draw.line(s, BORDER, (x, y), (RIGHT_X + RIGHT_W - PAD, y)); y += 7

        self._txt("lg", "ASFID Scores", x, y, ACCENT); y += 18
        bw = RIGHT_W - 2 * PAD - 125
        for lbl, sc in [("A Attractor", 0.92), ("S Structure", 0.88),
                        ("F Flow", 0.85), ("I Information", 0.80), ("D Dynamics", 0.90)]:
            self._txt("xs", lbl, x, y + 1, DIM)
            self._bar(x + 120, y, bw, sc, HL_GAS); y += 14
        self._txt("xs", "ASFID total = 0.87", x + 120, y, GOLD); y += 16

        self._txt("lg", "REVOI Scores", x, y, ACCENT); y += 18
        bw2 = RIGHT_W - 2 * PAD - 150
        for lbl, sc in [("R Representability", 0.90), ("E Evolvability", 0.75),
                        ("V Verifiability", 0.95), ("O Observability", 0.92),
                        ("I Interoperability", 0.88)]:
            self._txt("xs", lbl, x, y + 1, DIM)
            self._bar(x + 144, y, bw2, sc, (100, 200, 130)); y += 14
        self._txt("xs", "REVOI = 0.88  |  Epistemic gap = 0.12", x + 144, y, GOLD)

    # ── Run loop ──────────────────────────────────────────────────────────────

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
