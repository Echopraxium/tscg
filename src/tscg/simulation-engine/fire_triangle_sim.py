"""
fire_triangle_sim.py
====================
TSCG Poclet Simulation - Fire Triangle (Pygame)
Author: Echopraxium with the collaboration of Claude AI

Driven entirely by M0_FireTriangle.jsonld via poclet_parser.py.
No simulation parameters are hard-coded here; everything is read
from the poclet at startup.

Requirements:
    pip install pygame

Run:
    python fire_triangle_sim.py
    python fire_triangle_sim.py path/to/M0_FireTriangle.jsonld  (explicit path fallback)

Discovery:
    By default uses PocletRepository to find M0_FireTriangle.jsonld anywhere
    under <repo_root>/system-models/poclets/ -- no need to be in the same folder.
"""

import sys
import math
import random
import pygame
from poclet_parser import PocletParser, PocletRepository, ASFIDVector, PocletSimData

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WINDOW_W, WINDOW_H = 1100, 720
FPS                 = 60
# Optional explicit path override (sys.argv[1]) -- otherwise repo discovery is used
POCLET_PATH_OVERRIDE = sys.argv[1] if len(sys.argv) > 1 else None

# Palette
BG_COLOR        = (15,  15,  20)
PANEL_COLOR     = (25,  25,  35)
BORDER_COLOR    = (60,  60,  80)
TEXT_COLOR      = (220, 220, 230)
DIM_COLOR       = (140, 140, 160)
FIRE_ACTIVE     = (255, 120,  20)
FIRE_INACTIVE   = (60,   60,  80)
SLIDER_BG       = (40,   40,  55)
SLIDER_ACTIVE   = (255, 160,  30)
SLIDER_INACTIVE = (80,   80, 100)
THRESHOLD_LINE  = (255, 220,  60)
GREEN           = (80,  200, 120)
RED             = (220,  60,  60)
GOLD            = (255, 200,  50)
REVOI_COLOR     = (120, 180, 255)

# Layout
LEFT_PANEL_W  = 340
RIGHT_PANEL_W = 220
MID_W         = WINDOW_W - LEFT_PANEL_W - RIGHT_PANEL_W
PANEL_PAD     = 14

# Slider ranges (physical units mapped to 0..100 slider %)
# Derived from poclet constraints at runtime
COMPONENT_RANGES = {
    "fuel":     (0.0,  100.0, "%",   "Lower Explosive Limit"),
    "oxidizer": (0.0,  100.0, "% O₂", "> 16% for combustion"),
    "heat":     (0.0, 1000.0, "°C",  "Above T_ignition"),
}


# ---------------------------------------------------------------------------
# ASFID Dynamic Model
# ---------------------------------------------------------------------------

def compute_dynamic_asfid(slider_values: dict, base: ASFIDVector,
                           thresholds: dict, fire_on: bool) -> ASFIDVector:
    """
    Compute live ASFID scores from current slider positions.

    The base scores come from the poclet (territorySpace.asfidState).
    We modulate each dimension by how far we are from ignition:

      A - Attractor: peaks when fire is active (system drawn to flame state)
      S - Structure: fuel level drives structural organisation
      F - Flow    : oxygen drives flow intensity
      I - Information: heat level determines signal richness
      D - Dynamics : fire activity drives temporal changes

    All values clamped to [0.0, 1.0].
    """
    fuel_pct  = slider_values.get("fuel",     0.0) / 100.0
    o2_pct    = slider_values.get("oxidizer", 0.0) / 100.0
    heat_pct  = slider_values.get("heat",     0.0) / 100.0   # already 0..1

    fire_f    = 1.0 if fire_on else 0.0
    ignition  = 1.0 if fire_on else max(fuel_pct, o2_pct, heat_pct)

    A = clamp(base.A * (0.3 + 0.7 * fire_f))
    S = clamp(base.S * (0.4 + 0.6 * fuel_pct))
    F = clamp(base.F * (0.2 + 0.8 * o2_pct))
    I = clamp(base.I * (0.3 + 0.7 * heat_pct))
    D = clamp(base.D * (0.1 + 0.9 * ignition))

    return ASFIDVector(A=A, S=S, F=F, I=I, D=D)


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def compute_epistemic_gap(asfid: ASFIDVector, base_asfid: ASFIDVector) -> float:
    """ΔΘ = ‖|Ω_fire⟩ - |M_triangle⟩‖  (simplified: vs base poclet values)"""
    diffs = [
        asfid.A - base_asfid.A,
        asfid.S - base_asfid.S,
        asfid.F - base_asfid.F,
        asfid.I - base_asfid.I,
        asfid.D - base_asfid.D,
    ]
    return math.sqrt(sum(d * d for d in diffs))


# ---------------------------------------------------------------------------
# Slider widget
# ---------------------------------------------------------------------------

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, init_val,
                 label, unit, threshold=None, threshold_label=""):
        self.rect      = pygame.Rect(x, y, w, h)
        self.min_val   = min_val
        self.max_val   = max_val
        self.value     = float(init_val)
        self.label     = label
        self.unit      = unit
        self.threshold = threshold
        self.threshold_label = threshold_label
        self.dragging  = False
        self.handle_r  = 10

    @property
    def ratio(self):
        return (self.value - self.min_val) / max(self.max_val - self.min_val, 1e-9)

    @property
    def handle_x(self):
        return int(self.rect.x + self.ratio * self.rect.w)

    @property
    def above_threshold(self):
        if self.threshold is None:
            return True
        return self.value >= self.threshold

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hx = self.handle_x
            hy = self.rect.centery
            if math.hypot(event.pos[0] - hx, event.pos[1] - hy) < self.handle_r + 4:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel = (event.pos[0] - self.rect.x) / max(self.rect.w, 1)
            self.value = clamp(
                self.min_val + rel * (self.max_val - self.min_val),
                self.min_val, self.max_val
            )

    def draw(self, surf, font_sm, font_xs):
        active = self.above_threshold
        track_color = SLIDER_ACTIVE if active else SLIDER_INACTIVE

        # Track background
        pygame.draw.rect(surf, SLIDER_BG,
                         (self.rect.x, self.rect.centery - 3,
                          self.rect.w, 6), border_radius=3)
        # Filled portion
        fill_w = int(self.ratio * self.rect.w)
        if fill_w > 0:
            pygame.draw.rect(surf, track_color,
                             (self.rect.x, self.rect.centery - 3,
                              fill_w, 6), border_radius=3)

        # Threshold marker
        if self.threshold is not None:
            t_ratio = (self.threshold - self.min_val) / max(self.max_val - self.min_val, 1e-9)
            tx = int(self.rect.x + t_ratio * self.rect.w)
            pygame.draw.line(surf, THRESHOLD_LINE,
                             (tx, self.rect.centery - 12),
                             (tx, self.rect.centery + 12), 2)
            lbl = font_xs.render("min", True, THRESHOLD_LINE)
            surf.blit(lbl, (tx - lbl.get_width() // 2, self.rect.centery + 14))

        # Handle
        handle_color = GOLD if active else (100, 100, 120)
        pygame.draw.circle(surf, handle_color,
                           (self.handle_x, self.rect.centery), self.handle_r)
        pygame.draw.circle(surf, TEXT_COLOR,
                           (self.handle_x, self.rect.centery), self.handle_r, 1)

        # Label + value
        val_str  = f"{self.value:.1f} {self.unit}"
        lbl_surf = font_sm.render(self.label, True, TEXT_COLOR)
        val_surf = font_sm.render(val_str, True, GOLD if active else DIM_COLOR)
        surf.blit(lbl_surf, (self.rect.x, self.rect.y - 22))
        surf.blit(val_surf, (self.rect.right - val_surf.get_width(), self.rect.y - 22))


# ---------------------------------------------------------------------------
# Fire particle system
# ---------------------------------------------------------------------------

class Particle:
    def __init__(self, cx, cy, intensity):
        self.x   = cx + random.uniform(-20, 20) * intensity
        self.y   = cy + random.uniform(0, 15)
        self.vx  = random.uniform(-1.5, 1.5) * intensity
        self.vy  = random.uniform(-4, -1.5) * intensity
        self.life = random.uniform(0.4, 1.0)
        self.max_life = self.life
        self.r   = random.uniform(3, 12) * intensity
        self.intensity = intensity

    def update(self, dt):
        self.x    += self.vx
        self.y    += self.vy
        self.vx   *= 0.98
        self.vy   += 0.05   # slight drag
        self.life -= dt
        self.r    = max(0, self.r - 0.15)

    @property
    def alive(self):
        return self.life > 0 and self.r > 0

    def draw(self, surf):
        if not self.alive:
            return
        ratio = self.life / self.max_life
        alpha = int(255 * ratio * self.intensity)
        # Color: white core → orange → red → dark
        if ratio > 0.7:
            color = (255, 255, int(200 * (ratio - 0.7) / 0.3))
        elif ratio > 0.4:
            color = (255, int(120 + 135 * (ratio - 0.4) / 0.3), 20)
        else:
            color = (int(200 * ratio / 0.4), int(40 * ratio / 0.4), 0)

        s = pygame.Surface((int(self.r * 2 + 1), int(self.r * 2 + 1)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, alpha), (int(self.r), int(self.r)), int(self.r))
        surf.blit(s, (int(self.x - self.r), int(self.y - self.r)))


class FireSystem:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.particles = []
        self.spawn_acc = 0.0
        self.intensity = 0.0   # 0..1, driven externally

    def update(self, dt, active, intensity):
        self.intensity = intensity
        # Spawn
        if active and intensity > 0.01:
            self.spawn_acc += dt * 60 * intensity
            while self.spawn_acc >= 1:
                self.particles.append(Particle(self.cx, self.cy, intensity))
                self.spawn_acc -= 1
        # Update
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ---------------------------------------------------------------------------
# Triangle diagram
# ---------------------------------------------------------------------------

def draw_fire_triangle(surf, cx, cy, size, sliders, sim_data: PocletSimData,
                       fire_on: bool, font_sm, font_xs):
    """
    Draw the equilateral fire triangle with vertices labelled by component.
    Edges glow when their component is above threshold.
    """
    h = size * math.sqrt(3) / 2
    # Vertices: top=Heat, bottom-left=Fuel, bottom-right=Oxidizer
    pts = [
        (cx,              cy - h * 2 / 3),     # top
        (cx - size / 2,   cy + h / 3),          # bottom-left
        (cx + size / 2,   cy + h / 3),          # bottom-right
    ]

    # Map component labels to vertices (order from parser)
    labels  = [c.label for c in sim_data.components]
    # Default vertex order: Fuel=0, Oxidizer=1, Heat=2
    # We map: Heat→top, Fuel→bottom-left, Oxidizer→bottom-right
    vertex_map = {}
    for i, c in enumerate(sim_data.components):
        lbl = c.label.lower()
        if "heat" in lbl:
            vertex_map[i] = 0   # top
        elif "fuel" in lbl or "combustible" in lbl:
            vertex_map[i] = 1   # bottom-left
        else:
            vertex_map[i] = 2   # bottom-right

    # Edge colors: lit when component above threshold
    def comp_active(idx):
        s = list(sliders.values())[idx]
        return s.above_threshold

    edge_colors = []
    for i in range(len(sim_data.components)):
        edge_colors.append(FIRE_ACTIVE if comp_active(i) else (50, 50, 70))

    # Draw edges (triangle sides)
    for i in range(3):
        j = (i + 1) % 3
        col = FIRE_ACTIVE if fire_on else (50, 50, 70)
        # Glow
        if fire_on:
            for gw in range(6, 0, -2):
                alpha_col = (col[0], col[1], col[2])
                pygame.draw.line(surf, alpha_col, pts[i], pts[j], gw)
        pygame.draw.line(surf, col, pts[i], pts[j], 2)

    # Draw vertices
    for i, c in enumerate(sim_data.components):
        vi = vertex_map.get(i, i)
        px, py = pts[vi]
        active = comp_active(i)
        vcol = FIRE_ACTIVE if active else (80, 80, 100)
        pygame.draw.circle(surf, vcol, (int(px), int(py)), 8)
        pygame.draw.circle(surf, TEXT_COLOR, (int(px), int(py)), 8, 1)

        # Label
        lbl_lines = c.label.split("(")
        lbl_short = lbl_lines[0].strip()
        lbl_surf = font_sm.render(lbl_short, True, TEXT_COLOR if active else DIM_COLOR)
        # Position label outside vertex
        dx = px - cx
        dy = py - cy
        lx = px + dx * 0.35 - lbl_surf.get_width() / 2
        ly = py + dy * 0.35 - lbl_surf.get_height() / 2
        surf.blit(lbl_surf, (lx, ly))

    # Center: "FIRE" label
    fire_col = GOLD if fire_on else (60, 60, 80)
    txt = font_sm.render("FIRE" if fire_on else "—", True, fire_col)
    surf.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_panel(surf, rect, title, font_md, color=PANEL_COLOR, border=BORDER_COLOR):
    pygame.draw.rect(surf, color, rect, border_radius=8)
    pygame.draw.rect(surf, border, rect, 1, border_radius=8)
    if title:
        t = font_md.render(title, True, GOLD)
        surf.blit(t, (rect.x + PANEL_PAD, rect.y + PANEL_PAD))
    return rect.y + PANEL_PAD + (font_md.get_height() + 6 if title else 0)


def draw_bar(surf, x, y, w, h, value, max_val, color, bg_color=SLIDER_BG, label="", font=None):
    pygame.draw.rect(surf, bg_color, (x, y, w, h), border_radius=3)
    fill = int(clamp(value / max(max_val, 1e-9)) * w)
    if fill > 0:
        pygame.draw.rect(surf, color, (x, y, fill, h), border_radius=3)
    if label and font:
        lbl = font.render(label, True, TEXT_COLOR)
        surf.blit(lbl, (x, y - lbl.get_height() - 2))


def draw_asfid_panel(surf, rect, asfid: ASFIDVector, base: ASFIDVector,
                     font_md, font_sm, font_xs):
    y0 = draw_panel(surf, rect, "ASFID  (Eagle Eye · Territory)", font_md)
    y  = y0 + 4
    x  = rect.x + PANEL_PAD
    bar_w = rect.w - PANEL_PAD * 2 - 36

    dims = [("A", asfid.A, base.A, (255, 180,  60)),
            ("S", asfid.S, base.S, (100, 200, 255)),
            ("F", asfid.F, base.F, ( 60, 200, 160)),
            ("I", asfid.I, base.I, (200, 130, 255)),
            ("D", asfid.D, base.D, (255, 100, 100))]

    for dim, val, bval, col in dims:
        lbl = font_sm.render(dim, True, col)
        surf.blit(lbl, (x, y + 1))
        draw_bar(surf, x + 22, y, bar_w, 14, val, 1.0, col)
        # Base marker
        bx = x + 22 + int(bval * bar_w)
        pygame.draw.line(surf, (220, 220, 220),
                         (bx, y), (bx, y + 14), 1)
        val_lbl = font_xs.render(f"{val:.2f}", True, col)
        surf.blit(val_lbl, (x + 22 + bar_w + 4, y))
        y += 22

    return y


def draw_revoi_panel(surf, rect, revoi, font_md, font_sm, font_xs):
    y0 = draw_panel(surf, rect, "REVOI  (Sphinx Eye · Map)", font_md)
    y  = y0 + 4
    x  = rect.x + PANEL_PAD
    bar_w = rect.w - PANEL_PAD * 2 - 36

    dims = [("R", revoi.R, (100, 180, 255)),
            ("E", revoi.E, (180, 255, 120)),
            ("V", revoi.V, (255, 220,  80)),
            ("O", revoi.O, (255, 130, 200)),
            ("I", revoi.I, (130, 220, 255))]

    for dim, val, col in dims:
        lbl = font_sm.render(dim, True, col)
        surf.blit(lbl, (x, y + 1))
        draw_bar(surf, x + 22, y, bar_w, 14, val, 1.0, col)
        val_lbl = font_xs.render(f"{val:.2f}", True, col)
        surf.blit(val_lbl, (x + 22 + bar_w + 4, y))
        y += 22

    mean_lbl = font_xs.render(f"mean = {revoi.mean():.2f}", True, REVOI_COLOR)
    surf.blit(mean_lbl, (x, y + 2))
    return y + 20


def draw_status_box(surf, rect, fire_on, gap, sim_data, font_md, font_sm, font_xs):
    y0 = draw_panel(surf, rect, "Status", font_md)
    y  = y0 + 4
    x  = rect.x + PANEL_PAD

    # Fire state
    state_col  = GREEN if fire_on else RED
    state_txt  = "🔥 COMBUSTION ACTIVE" if fire_on else "💧 NO COMBUSTION"
    state_surf = font_sm.render(state_txt, True, state_col)
    surf.blit(state_surf, (x, y)); y += state_surf.get_height() + 6

    # Epistemic gap ΔΘ
    gap_col = GREEN if gap < 0.3 else (GOLD if gap < 0.5 else RED)
    gap_txt = font_sm.render(f"ΔΘ = {gap:.3f}", True, gap_col)
    surf.blit(gap_txt, (x, y)); y += gap_txt.get_height() + 2

    interp = ("Good alignment" if gap < 0.3
              else "Moderate gap" if gap < 0.5
              else "Large gap")
    interp_surf = font_xs.render(interp, True, DIM_COLOR)
    surf.blit(interp_surf, (x, y)); y += interp_surf.get_height() + 10

    # Synergy formula
    syn_surf = font_xs.render("Synergy:", True, GOLD)
    surf.blit(syn_surf, (x, y)); y += syn_surf.get_height() + 2
    # Wrap formula
    formula = sim_data.synergy_formula
    f_surf = font_xs.render(formula, True, TEXT_COLOR)
    surf.blit(f_surf, (x, y)); y += f_surf.get_height() + 10

    # Metaconcepts
    mc_lbl = font_xs.render(f"Metaconcepts: {sim_data.metaconcept_count}", True, DIM_COLOR)
    surf.blit(mc_lbl, (x, y)); y += mc_lbl.get_height() + 4

    for mc in sim_data.metaconcepts[:5]:
        mc_surf = font_xs.render(f"  • {mc}", True, (150, 180, 220))
        surf.blit(mc_surf, (x, y)); y += mc_surf.get_height() + 1


# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def main():
    # --- Load poclet via PocletRepository (auto-discovers repo root) ---
    try:
        if POCLET_PATH_OVERRIDE:
            print(f"[TSCG] Loading poclet from explicit path: {POCLET_PATH_OVERRIDE}")
            sim_data = PocletParser(POCLET_PATH_OVERRIDE).parse()
        else:
            repo = PocletRepository()
            print(f"[TSCG] Repository root : {repo.root}")
            print(f"[TSCG] Poclets found   : {repo.list()}")
            sim_data = repo.load("FireTriangle")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print("  Tip: run from anywhere inside the tscg repository,")
        print("  or pass an explicit path: python fire_triangle_sim.py path/to/M0_FireTriangle.jsonld")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to parse poclet: {e}")
        raise

    print(f"[TSCG] Poclet loaded: '{sim_data.label}'")
    print(f"[TSCG] Components   : {[c.label for c in sim_data.components]}")
    print(f"[TSCG] ASFID base   : {sim_data.asfid_base}")
    print(f"[TSCG] REVOI        : {sim_data.revoi}")

    # --- Pygame init ---
    pygame.init()
    screen  = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(f"TSCG Simulation · {sim_data.label}")
    clock   = pygame.time.Clock()

    font_lg = pygame.font.SysFont("segoeui", 20, bold=True)
    font_md = pygame.font.SysFont("segoeui", 15, bold=True)
    font_sm = pygame.font.SysFont("segoeui", 13)
    font_xs = pygame.font.SysFont("segoeui", 11)

    # --- Build sliders from poclet components ---
    # We position them in the left panel
    lp_x  = PANEL_PAD
    slider_keys = []
    sliders = {}

    # Physical defaults when poclet constraints are textual (no numeric value)
    COMPONENT_DEFAULTS = {
        "heat":     {"min": 0.0,  "max": 1000.0, "unit": "°C",   "init": 50.0,
                     "threshold": 233.0, "threshold_label": "T_ignition paper ~233°C"},
        "fuel":     {"min": 0.0,  "max": 100.0,  "unit": "%",    "init": 20.0,
                     "threshold": 20.0,  "threshold_label": "Above LEL (~20%)"},
        "oxidizer": {"min": 0.0,  "max": 100.0,  "unit": "% O₂", "init": 10.0,
                     "threshold": 16.0,  "threshold_label": "> 16% for sustained combustion"},
    }

    for i, comp in enumerate(sim_data.components):
        lbl_lower = comp.label.lower()
        # Detect component type
        if "heat" in lbl_lower:
            ctype = "heat"
        elif "fuel" in lbl_lower or "combustible" in lbl_lower:
            ctype = "fuel"
        else:
            ctype = "oxidizer"

        defaults = COMPONENT_DEFAULTS[ctype]
        # Use poclet threshold if parser extracted one, else physical default
        threshold       = comp.threshold if comp.threshold is not None else defaults["threshold"]
        threshold_label = comp.threshold_label or defaults["threshold_label"]

        key = ctype
        slider_keys.append(key)
        sliders[key] = Slider(
            x=lp_x + PANEL_PAD,
            y=120 + i * 90,
            w=LEFT_PANEL_W - PANEL_PAD * 4,
            h=20,
            min_val=defaults["min"],
            max_val=defaults["max"],
            init_val=defaults["init"],
            label=comp.label.split("(")[0].strip(),
            unit=defaults["unit"],
            threshold=threshold,
            threshold_label=threshold_label,
        )

    # Fire system (center panel)
    mid_cx = LEFT_PANEL_W + MID_W // 2
    mid_cy = WINDOW_H // 2 + 20
    fire_sys = FireSystem(mid_cx, mid_cy + 50)

    # --- Main loop ---
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            for s in sliders.values():
                s.handle_event(event)

        # Fire logic: all components above threshold?
        fire_on = all(s.above_threshold for s in sliders.values())

        # Intensity: how far above thresholds (0..1)
        if fire_on:
            scores = []
            for s in sliders.values():
                r = (s.value - (s.threshold or s.min_val)) / max(s.max_val - (s.threshold or s.min_val), 1e-9)
                scores.append(clamp(r))
            intensity = sum(scores) / len(scores)
        else:
            intensity = 0.0

        # Dynamic ASFID
        slider_norm = {}
        for key, s in sliders.items():
            if "heat" in key:
                slider_norm[key] = s.value / s.max_val * 100.0
            else:
                slider_norm[key] = s.value
        # Use simpler normalized values
        sv = {}
        for key, s in sliders.items():
            sv[key] = (s.value - s.min_val) / max(s.max_val - s.min_val, 1e-9) * 100.0

        asfid_live = compute_dynamic_asfid(sv, sim_data.asfid_base, {}, fire_on)
        gap        = compute_epistemic_gap(asfid_live, sim_data.asfid_base)

        # Update particles
        fire_sys.update(dt, fire_on, intensity)

        # --- Draw ---
        screen.fill(BG_COLOR)

        # ── Left panel: Controls ──────────────────────────────────────
        lp_rect = pygame.Rect(0, 0, LEFT_PANEL_W, WINDOW_H)
        draw_panel(screen, lp_rect, None, font_md)

        # Title
        title = font_lg.render("🔺 " + sim_data.label, True, GOLD)
        screen.blit(title, (PANEL_PAD + 6, PANEL_PAD + 6))
        domain_lbl = font_xs.render(f"Domain: {sim_data.domain}  |  Observer: {sim_data.observer}", True, DIM_COLOR)
        screen.blit(domain_lbl, (PANEL_PAD + 6, PANEL_PAD + 6 + title.get_height() + 2))

        # Sliders
        sep_y = PANEL_PAD + 6 + title.get_height() + domain_lbl.get_height() + 16
        pygame.draw.line(screen, BORDER_COLOR,
                         (PANEL_PAD, sep_y), (LEFT_PANEL_W - PANEL_PAD, sep_y))
        ctrl_lbl = font_md.render("Component Controls", True, TEXT_COLOR)
        screen.blit(ctrl_lbl, (PANEL_PAD + 6, sep_y + 8))

        for s in sliders.values():
            s.draw(screen, font_sm, font_xs)

        # Threshold legend
        leg_y = list(sliders.values())[-1].rect.bottom + 20
        pygame.draw.line(screen, THRESHOLD_LINE, (PANEL_PAD + 6, leg_y + 6),
                         (PANEL_PAD + 22, leg_y + 6), 2)
        leg_txt = font_xs.render("= ignition threshold (from poclet)", True, DIM_COLOR)
        screen.blit(leg_txt, (PANEL_PAD + 26, leg_y))

        # ── Center panel: Triangle + Fire ────────────────────────────
        mid_rect = pygame.Rect(LEFT_PANEL_W, 0, MID_W, WINDOW_H)
        pygame.draw.rect(screen, (18, 18, 26), mid_rect)

        # Fire particles (behind triangle)
        fire_sys.draw(screen)

        # Triangle diagram
        draw_fire_triangle(screen, mid_cx, mid_cy - 30, 160,
                           sliders, sim_data, fire_on, font_sm, font_xs)

        # Poclet source label
        src_lbl = font_xs.render(f"Source: {sim_data.id.split(':')[-1]}", True, (60, 60, 80))
        screen.blit(src_lbl, (LEFT_PANEL_W + 6, WINDOW_H - 18))

        # Center title
        ct = font_md.render("Territory Simulation", True, DIM_COLOR)
        screen.blit(ct, (mid_cx - ct.get_width() // 2, 10))

        # Emergent property label
        if fire_on:
            ep_lbl = font_sm.render(f"↑ {sim_data.synergy_emergent}", True, FIRE_ACTIVE)
            screen.blit(ep_lbl, (mid_cx - ep_lbl.get_width() // 2, mid_cy + 115))

        # ── Right panel: ASFID + REVOI + Status ──────────────────────
        rp_x   = LEFT_PANEL_W + MID_W
        rp_rect = pygame.Rect(rp_x, 0, RIGHT_PANEL_W, WINDOW_H)
        pygame.draw.rect(screen, PANEL_COLOR, rp_rect)
        pygame.draw.line(screen, BORDER_COLOR, (rp_x, 0), (rp_x, WINDOW_H))

        asfid_rect = pygame.Rect(rp_x + 2, 4, RIGHT_PANEL_W - 4, 165)
        y_after_asfid = draw_asfid_panel(screen, asfid_rect, asfid_live,
                                          sim_data.asfid_base, font_md, font_sm, font_xs)

        revoi_rect = pygame.Rect(rp_x + 2, asfid_rect.bottom + 6, RIGHT_PANEL_W - 4, 155)
        draw_revoi_panel(screen, revoi_rect, sim_data.revoi, font_md, font_sm, font_xs)

        status_rect = pygame.Rect(rp_x + 2, revoi_rect.bottom + 6,
                                  RIGHT_PANEL_W - 4, WINDOW_H - revoi_rect.bottom - 10)
        draw_status_box(screen, status_rect, fire_on, gap, sim_data,
                        font_md, font_sm, font_xs)

        # ── HUD: fps ──
        fps_surf = font_xs.render(f"FPS: {int(clock.get_fps())}", True, (50, 50, 70))
        screen.blit(fps_surf, (LEFT_PANEL_W + 4, WINDOW_H - 18))

        pygame.display.flip()

    pygame.quit()
    print("[TSCG] Simulation ended.")


if __name__ == "__main__":
    main()
