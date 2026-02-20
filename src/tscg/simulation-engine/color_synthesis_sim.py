"""
color_synthesis_sim.py
======================
TSCG Poclet Simulation - Color Synthesis Federated (Pygame)
Author: Echopraxium with the collaboration of Claude AI

Driven by the Color Synthesis federated poclet family:
  - M0_RGB_Additive.jsonld
  - M0_HSL_Additive.jsonld
  - M0_CMY_Subtractive.jsonld
  - M0_CMYK_Subtractive.jsonld
  - M0_ColorSynthesis_Federated.jsonld

Layout (1280x760):
  LEFT   (300px) : Active model sliders + color swatch + codes (RGB/HSL/CMY/CMYK)
  CENTER (480px) : Isometric RGB cube + synthetic colors + model selector tabs
  RIGHT  (500px) : ASFID live | REVOI comparison (all 4 models) | ΔΘ + status

Key:  TAB or click tabs to switch active model
      Mouse drag sliders to change values
      ESC to quit

Requirements:
    pip install pygame

Run:
    python color_synthesis_sim.py
    python color_synthesis_sim.py path/to/folder/containing/poclets
"""

import sys
import math
import json
import re
import pygame
from pathlib import Path
from poclet_parser import (PocletParser, PocletRepository,
                            PocletSimData, ComponentData,
                            ASFIDVector, REVOIVector, EpistemicGap)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WINDOW_W, WINDOW_H = 1280, 760
FPS                = 60

LEFT_W   = 300
RIGHT_W  = 480
MID_W    = WINDOW_W - LEFT_W - RIGHT_W

# Palette
BG           = (12,  12,  18)
PANEL        = (22,  22,  32)
PANEL2       = (28,  28,  40)
BORDER       = (55,  55,  75)
TEXT         = (220, 220, 230)
DIM          = (120, 120, 145)
GOLD         = (255, 200,  50)
GREEN        = (80,  210, 120)
RED_C        = (220,  60,  60)
SLIDER_BG    = (38,  38,  52)
PAD          = 12

# Model definitions (index order matches tabs)
MODEL_KEYS  = ["RGB", "HSL", "CMY", "CMYK"]
MODEL_FILES = {
    "RGB":  "M0_RGB_Additive.jsonld",
    "HSL":  "M0_HSL_Additive.jsonld",
    "CMY":  "M0_CMY_Subtractive.jsonld",
    "CMYK": "M0_CMYK_Subtractive.jsonld",
}
MODEL_COLORS = {
    "RGB":  (255, 100, 100),
    "HSL":  (100, 200, 255),
    "CMY":  ( 80, 220, 160),
    "CMYK": (200, 150, 255),
}
MODEL_ADDITIVE = {"RGB": True, "HSL": True, "CMY": False, "CMYK": False}


# ---------------------------------------------------------------------------
# Multi-poclet Adapter
# ---------------------------------------------------------------------------

class ColorSynthesisAdapter:
    """
    Loads all 4 color synthesis poclets from a folder.
    All poclets use "m0:" prefix for fields regardless of @context namespace.
    """

    def __init__(self, folder=None):
        if folder:
            self.folder = Path(folder)
        else:
            self.folder = self._find_folder()
        self.models   = {}   # key -> PocletSimData
        self.raw      = {}   # key -> raw node dict
        self.federated = {}  # federated metadata
        self._load_all()

    def _find_folder(self):
        """
        Search for the folder containing M0_RGB_Additive.jsonld.

        Strategy (fastest first):
        1. Walk upward from script and cwd, check explicit known subpaths
           (validated + 00_to_be_fixed / _00_to_be_fixed variants).
        2. Fallback: rglob under system-models/ if explicit paths missed.
        3. Last resort: script directory (files placed alongside script).
        """
        TARGET = "M0_RGB_Additive.jsonld"
        EXPLICIT_SUBPATHS = [
            Path("system-models") / "poclets" / "color_synthesis",
            Path("system-models") / "poclets" / "00_to_be_fixed"  / "color_synthesis",
            Path("system-models") / "poclets" / "_00_to_be_fixed" / "color_synthesis",
        ]

        try:
            script_dir = Path(__file__).resolve().parent
        except NameError:
            script_dir = Path(sys.argv[0]).resolve().parent

        # Build ordered list of roots (walk upward from script then cwd)
        roots = []
        seen  = set()
        for base in [script_dir, Path.cwd().resolve()]:
            candidate = base
            for _ in range(12):
                if candidate not in seen:
                    seen.add(candidate)
                    roots.append(candidate)
                parent = candidate.parent
                if parent == candidate:
                    break
                candidate = parent

        # Pass 1: explicit subpaths (no filesystem scan, fast on Windows)
        for root in roots:
            for subpath in EXPLICIT_SUBPATHS:
                folder = root / subpath
                if (folder / TARGET).exists():
                    print(f"[TSCG] Found poclets at: {folder}")
                    return folder

        # Pass 2: rglob under system-models/ (slower but catches any layout)
        for root in roots:
            sm = root / "system-models"
            if sm.exists():
                for match in sm.rglob(TARGET):
                    print(f"[TSCG] Found poclets at: {match.parent}")
                    return match.parent

        # Last resort
        return script_dir

    def _load_all(self):
        for key, fname in MODEL_FILES.items():
            path = self.folder / fname
            if not path.exists():
                # Try cwd
                path = Path(fname)
            if path.exists():
                raw_node = self._read_node(path)
                self.raw[key] = raw_node
                self.models[key] = self._adapt(key, raw_node)
            else:
                print(f"[WARN] {fname} not found, skipping {key}")

        # Federated
        fed_path = self.folder / "M0_ColorSynthesis_Federated.jsonld"
        if not fed_path.exists():
            fed_path = Path("M0_ColorSynthesis_Federated.jsonld")
        if fed_path.exists():
            data = json.load(open(fed_path, encoding="utf-8"))
            self.federated = data["@graph"][0]

    def _read_node(self, path):
        data = json.load(open(path, encoding="utf-8"))
        for node in data["@graph"]:
            if "m0:channels" in node or "m0:components" in node:
                return node
        return data["@graph"][0]

    def _adapt(self, key, node):
        sim = PocletSimData()
        sim.id          = node.get("@id", "")
        sim.label       = node.get("rdfs:label", key)
        sim.comment     = node.get("rdfs:comment", "")
        sim.domain      = node.get("m0:domain", "")
        sim.poclet_type = node.get("m0:pocletType", "")
        sim.observer    = node.get("m0:territorySpace", {}).get("observer", "")

        # Fusion / synthesis principle
        fp = (node.get("m0:fusionPrinciple")
              or node.get("m0:synthesisPrinciple", {}))
        sim.synergy_formula  = fp.get("operation", fp.get("formula", ""))
        sim.synergy_emergent = fp.get("emergentProperty", "")

        # Components (RGB uses "components"; HSL/CMY/CMYK use "channels")
        raw_comps = node.get("m0:components", node.get("m0:channels", []))
        sim.components = []
        for c in raw_comps:
            label = c.get("rdfs:label", "")
            sim.components.append(ComponentData(
                cid=c.get("@id", ""),
                label=label,
                role=c.get("m0:role", ""),
                function=c.get("m0:function", ""),
                asfid_contribution=c.get("m0:asfidContribution", {}),
                threshold=None,
                threshold_label=c.get("m0:rangeDigital",
                                      c.get("m0:range", "0-255")),
                examples=c.get("m0:examples", [])
            ))

        # ASFID
        ts = node.get("m0:territorySpace", {})
        a  = ts.get("asfidState", {})
        sim.asfid_base = ASFIDVector(
            A=float(a.get("A", 0)), S=float(a.get("S", 0)),
            F=float(a.get("F", 0)), I=float(a.get("I", 0)),
            D=float(a.get("D", 0))
        )

        # REVOI (stored as oriveState in these poclets)
        oa = (node.get("m0:oriveAnalysis")
              or node.get("m0:reviAnalysis", {}))
        o  = oa.get("oriveState", oa.get("reviState", {}))
        sim.revoi = REVOIVector(
            R=float(o.get("R", 0)), E=float(o.get("E", 0)),
            V=float(o.get("V", 0)), O=float(o.get("O", 0)),
            I=float(o.get("I", 0))
        )

        # Epistemic gap
        eg = node.get("m0:epistemicGap", {})
        if eg:
            raw_dv = eg.get("deltaVector", "(0,0,0,0,0)")
            floats = [float(x) for x in re.findall(r"[+-]?\d+\.?\d*", raw_dv)]
            norm_s = str(eg.get("norm", "0")).replace("≈", "").strip()
            try:
                norm_f = float(norm_s)
            except ValueError:
                norm_f = 0.0
            sim.epistemic_gap = EpistemicGap(
                norm=norm_f, delta_vector=floats,
                interpretation=eg.get("interpretation", ""),
                assessment=eg.get("assessment", "")
            )

        # Metaconcepts
        mc = node.get("m0:metaconceptsMobilized", {})
        sim.metaconcept_count = int(mc.get("total", 0))
        critical = mc.get("critical", mc.get("criticalMetaconcepts", []))
        sim.metaconcepts = []
        for m in critical:
            raw_name = m.get("metaconcept", m.get("name", ""))
            name = raw_name.split(":")[-1] if ":" in raw_name else raw_name
            if name:
                sim.metaconcepts.append(name)

        return sim


# ---------------------------------------------------------------------------
# Color math
# ---------------------------------------------------------------------------

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def clamp_i(v, lo=0, hi=255):
    return max(lo, min(hi, int(round(v))))

def rgb_to_hsl(r, g, b):
    r0, g0, b0 = r/255, g/255, b/255
    cmax, cmin = max(r0, g0, b0), min(r0, g0, b0)
    delta = cmax - cmin
    l = (cmax + cmin) / 2
    s = 0 if delta == 0 else delta / (1 - abs(2*l - 1))
    if delta == 0:
        h = 0.0
    elif cmax == r0:
        h = 60 * (((g0 - b0) / delta) % 6)
    elif cmax == g0:
        h = 60 * (((b0 - r0) / delta) + 2)
    else:
        h = 60 * (((r0 - g0) / delta) + 4)
    return h, s * 100, l * 100   # H:0-360, S:0-100, L:0-100

def hsl_to_rgb(h, s, l):
    s /= 100; l /= 100
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if   h < 60:  r0, g0, b0 = c, x, 0
    elif h < 120: r0, g0, b0 = x, c, 0
    elif h < 180: r0, g0, b0 = 0, c, x
    elif h < 240: r0, g0, b0 = 0, x, c
    elif h < 300: r0, g0, b0 = x, 0, c
    else:         r0, g0, b0 = c, 0, x
    return clamp_i((r0+m)*255), clamp_i((g0+m)*255), clamp_i((b0+m)*255)

def rgb_to_cmy(r, g, b):
    return 100 - r*100//255, 100 - g*100//255, 100 - b*100//255

def cmy_to_rgb(c, m, y):
    return clamp_i((100-c)*255/100), clamp_i((100-m)*255/100), clamp_i((100-y)*255/100)

def rgb_to_cmyk(r, g, b):
    r0, g0, b0 = r/255, g/255, b/255
    k = 1 - max(r0, g0, b0)
    if k == 1:
        return 0, 0, 0, 100
    c = (1 - r0 - k) / (1 - k)
    m = (1 - g0 - k) / (1 - k)
    y = (1 - b0 - k) / (1 - k)
    return int(c*100), int(m*100), int(y*100), int(k*100)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c/100) * (1 - k/100)
    g = 255 * (1 - m/100) * (1 - k/100)
    b = 255 * (1 - y/100) * (1 - k/100)
    return clamp_i(r), clamp_i(g), clamp_i(b)

def compute_dynamic_asfid(r, g, b, base: ASFIDVector) -> ASFIDVector:
    r0, g0, b0 = r/255, g/255, b/255
    brightness = (r0 + g0 + b0) / 3
    h, s, l = rgb_to_hsl(r, g, b)
    ch = sorted([r0, g0, b0])
    spread = ch[2] - ch[0]
    mean_c = brightness
    var = ((r0-mean_c)**2 + (g0-mean_c)**2 + (b0-mean_c)**2) / 3
    colorfulness = clamp(math.sqrt(var) * math.sqrt(3))
    # Named attractor proximity
    named = [(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),
             (255,255,0),(0,255,255),(255,0,255),(128,128,128)]
    max_d = math.sqrt(3)*255
    min_d = min(math.sqrt((r-nr)**2+(g-ng)**2+(b-nb)**2)
                for nr,ng,nb in named)
    proximity = 1 - min_d / max_d
    A = clamp(base.A * (0.3 + 0.7 * proximity))
    S = clamp(base.S * (0.4 + 0.6 * spread))
    F = clamp(base.F * (0.1 + 0.9 * brightness))
    I = clamp(base.I * (0.3 + 0.7 * colorfulness))
    D = clamp(base.D * (0.1 + 0.9 * (s/100) * (1 - abs(2*l/100 - 1))))
    return ASFIDVector(A=A, S=S, F=F, I=I, D=D)

def epistemic_gap_norm(live: ASFIDVector, base: ASFIDVector) -> float:
    return math.sqrt(sum((getattr(live, d) - getattr(base, d))**2
                         for d in "ASFID"))


# ---------------------------------------------------------------------------
# Slider widget
# ---------------------------------------------------------------------------

class Slider:
    def __init__(self, x, y, w, h, min_v, max_v, init, label, unit, color):
        self.rect     = pygame.Rect(x, y, w, h)
        self.min_v    = min_v
        self.max_v    = max_v
        self.value    = float(init)
        self.label    = label
        self.unit     = unit
        self.color    = color
        self.dragging = False
        self.handle_r = 9

    @property
    def ratio(self):
        return (self.value - self.min_v) / max(self.max_v - self.min_v, 1e-9)

    @property
    def handle_x(self):
        return int(self.rect.x + self.ratio * self.rect.w)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hx, hy = self.handle_x, self.rect.centery
            if math.hypot(event.pos[0]-hx, event.pos[1]-hy) < self.handle_r + 5:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel = (event.pos[0] - self.rect.x) / max(self.rect.w, 1)
            self.value = clamp(self.min_v + rel * (self.max_v - self.min_v),
                               self.min_v, self.max_v)

    def draw(self, surf, font_sm, font_xs):
        # Track
        pygame.draw.rect(surf, SLIDER_BG,
                         (self.rect.x, self.rect.centery-3, self.rect.w, 6),
                         border_radius=3)
        fill_w = int(self.ratio * self.rect.w)
        if fill_w > 0:
            pygame.draw.rect(surf, self.color,
                             (self.rect.x, self.rect.centery-3, fill_w, 6),
                             border_radius=3)
        # Handle
        pygame.draw.circle(surf, self.color,
                           (self.handle_x, self.rect.centery), self.handle_r)
        pygame.draw.circle(surf, TEXT,
                           (self.handle_x, self.rect.centery), self.handle_r, 1)
        # Labels
        lbl = font_sm.render(self.label, True, TEXT)
        val_fmt = f"{int(self.value)}" if self.max_v > 2 else f"{self.value:.2f}"
        val = font_sm.render(f"{val_fmt} {self.unit}", True, self.color)
        surf.blit(lbl, (self.rect.x, self.rect.y - 20))
        surf.blit(val, (self.rect.right - val.get_width(), self.rect.y - 20))


# ---------------------------------------------------------------------------
# RGB Cube (isometric projection)
# ---------------------------------------------------------------------------

def iso_project(rx, gx, bx, cx, cy, scale=75):
    """Map RGB (0-1 each) to isometric 2D. R=right, G=left, B=up."""
    px = cx + (rx - gx) * scale * 0.866
    py = cy - bx * scale + (rx + gx) * scale * 0.5
    return int(px), int(py)

CUBE_VERTICES = {
    "Black":   (0, 0, 0),
    "Red":     (1, 0, 0),
    "Green":   (0, 1, 0),
    "Blue":    (0, 0, 1),
    "Yellow":  (1, 1, 0),
    "Cyan":    (0, 1, 1),
    "Magenta": (1, 0, 1),
    "White":   (1, 1, 1),
}
CUBE_EDGES = [
    ("Black","Red"), ("Black","Green"), ("Black","Blue"),
    ("Red","Yellow"), ("Red","Magenta"),
    ("Green","Yellow"), ("Green","Cyan"),
    ("Blue","Cyan"), ("Blue","Magenta"),
    ("Yellow","White"), ("Cyan","White"), ("Magenta","White"),
]

def draw_rgb_cube(surf, cx, cy, r, g, b, font_xs, scale=75):
    pts = {name: iso_project(vr, vg, vb, cx, cy, scale)
           for name, (vr, vg, vb) in CUBE_VERTICES.items()}
    # Edges
    for n1, n2 in CUBE_EDGES:
        pygame.draw.line(surf, (55, 55, 75), pts[n1], pts[n2], 1)
    # Vertices
    for name, (vr, vg, vb) in CUBE_VERTICES.items():
        col = (int(vr*255), int(vg*255), int(vb*255))
        pygame.draw.circle(surf, col, pts[name], 5)
        pygame.draw.circle(surf, TEXT, pts[name], 5, 1)
        lbl = font_xs.render(name, True, DIM)
        surf.blit(lbl, (pts[name][0]+6, pts[name][1]-6))
    # Current color marker
    r0, g0, b0 = r/255, g/255, b/255
    cp = iso_project(r0, g0, b0, cx, cy, scale)
    pygame.draw.circle(surf, (r, g, b), cp, 9)
    pygame.draw.circle(surf, (255, 255, 255), cp, 9, 2)
    # Achromatic diagonal
    p0 = iso_project(0, 0, 0, cx, cy, scale)
    p1 = iso_project(1, 1, 1, cx, cy, scale)
    pygame.draw.line(surf, (80, 80, 100), p0, p1, 1)


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_panel_bg(surf, rect, color=PANEL):
    pygame.draw.rect(surf, color, rect, border_radius=6)
    pygame.draw.rect(surf, BORDER, rect, 1, border_radius=6)

def draw_section_title(surf, x, y, title, font, color=GOLD):
    t = font.render(title, True, color)
    surf.blit(t, (x, y))
    return y + t.get_height() + 4

def draw_bar(surf, x, y, w, h, val, maxv, color, label="", font=None):
    pygame.draw.rect(surf, SLIDER_BG, (x, y, w, h), border_radius=3)
    fw = int(clamp(val/max(maxv,1e-9)) * w)
    if fw > 0:
        pygame.draw.rect(surf, color, (x, y, fw, h), border_radius=3)
    if label and font:
        lbl = font.render(label, True, TEXT)
        surf.blit(lbl, (x - lbl.get_width() - 4, y))

def draw_asfid_live(surf, rect, asfid, base, font_md, font_sm, font_xs):
    draw_panel_bg(surf, rect)
    y = rect.y + PAD
    y = draw_section_title(surf, rect.x+PAD, y, "ASFID  Eagle Eye · Territory", font_md)
    dims = [("A", asfid.A, base.A, (255,180,60)),
            ("S", asfid.S, base.S, (100,200,255)),
            ("F", asfid.F, base.F, (60, 200,160)),
            ("I", asfid.I, base.I, (200,130,255)),
            ("D", asfid.D, base.D, (255,100,100))]
    bw = rect.w - PAD*2 - 38
    for dim, val, bval, col in dims:
        lbl = font_sm.render(dim, True, col)
        surf.blit(lbl, (rect.x+PAD, y+1))
        draw_bar(surf, rect.x+PAD+20, y, bw, 13, val, 1.0, col)
        # Base marker
        bx = rect.x+PAD+20 + int(bval*bw)
        pygame.draw.line(surf, (200,200,200), (bx,y), (bx,y+13), 1)
        vs = font_xs.render(f"{val:.2f}", True, col)
        surf.blit(vs, (rect.x+PAD+20+bw+3, y))
        y += 20
    return y + 4

def draw_revoi_comparison(surf, rect, models, font_md, font_sm, font_xs):
    draw_panel_bg(surf, rect)
    y = rect.y + PAD
    y = draw_section_title(surf, rect.x+PAD, y, "REVOI  Sphinx Eye · Map  (all models)", font_md)
    dims = ["R", "E", "V", "O", "I"]
    dim_colors = {"R":(100,180,255),"E":(180,255,120),"V":(255,220,80),
                  "O":(255,130,200),"I":(130,220,255)}
    bw = rect.w - PAD*2 - 60 - len(MODEL_KEYS)*2

    # Header
    col_w = bw // len(MODEL_KEYS)
    hx = rect.x + PAD + 40
    for mk in MODEL_KEYS:
        col = MODEL_COLORS[mk]
        h = font_xs.render(mk, True, col)
        surf.blit(h, (hx, y))
        hx += col_w + 4
    y += font_xs.get_height() + 4

    for dim in dims:
        col = dim_colors[dim]
        lbl = font_sm.render(dim, True, col)
        surf.blit(lbl, (rect.x+PAD, y+1))
        x = rect.x + PAD + 40
        for mk in MODEL_KEYS:
            if mk in models:
                val = getattr(models[mk].revoi, dim)
                bar_w = col_w - 4
                pygame.draw.rect(surf, SLIDER_BG, (x, y, bar_w, 11), border_radius=2)
                fw = int(val * bar_w)
                if fw > 0:
                    pygame.draw.rect(surf, col, (x, y, fw, 11), border_radius=2)
                vs = font_xs.render(f"{val:.2f}", True, DIM)
                surf.blit(vs, (x, y+13))
            x += col_w + 4
        y += 26
    return y + 4

def draw_status(surf, rect, r, g, b, active_key, models, gap, font_md, font_sm, font_xs):
    draw_panel_bg(surf, rect)
    y = rect.y + PAD
    x = rect.x + PAD
    y = draw_section_title(surf, x, y, "Status", font_md)

    # Color swatch inline
    sw = 22
    pygame.draw.rect(surf, (r, g, b), (x, y, sw, sw), border_radius=4)
    pygame.draw.rect(surf, TEXT, (x, y, sw, sw), 1, border_radius=4)
    hex_str = f"#{r:02X}{g:02X}{b:02X}"
    hs = font_sm.render(hex_str, True, (r,g,b) if max(r,g,b)>60 else TEXT)
    surf.blit(hs, (x+sw+6, y+4))
    y += sw + 8

    # Active model
    acol = MODEL_COLORS.get(active_key, GOLD)
    am = font_sm.render(f"Active model: {active_key}", True, acol)
    surf.blit(am, (x, y)); y += am.get_height() + 4

    # Principle
    if active_key in models:
        prin = "Additive" if MODEL_ADDITIVE[active_key] else "Subtractive"
        ps = font_xs.render(f"Principle: {prin}", True, DIM)
        surf.blit(ps, (x, y)); y += ps.get_height() + 8

    # ΔΘ
    gap_col = GREEN if gap < 0.3 else (GOLD if gap < 0.5 else RED_C)
    gs = font_sm.render(f"ΔΘ = {gap:.3f}", True, gap_col)
    surf.blit(gs, (x, y)); y += gs.get_height() + 2
    interp = "Good alignment" if gap < 0.3 else ("Moderate gap" if gap < 0.5 else "Large gap")
    ins = font_xs.render(interp, True, DIM)
    surf.blit(ins, (x, y)); y += ins.get_height() + 8

    # Emergent property
    if active_key in models:
        em = models[active_key].synergy_emergent
        ems = font_xs.render(f"Emergent: {em}", True, GOLD)
        surf.blit(ems, (x, y)); y += ems.get_height() + 6

    # Metaconcepts
    if active_key in models:
        mc = models[active_key]
        mcs = font_xs.render(f"Metaconcepts: {mc.metaconcept_count}", True, DIM)
        surf.blit(mcs, (x, y)); y += mcs.get_height() + 2
        for name in mc.metaconcepts[:5]:
            ns = font_xs.render(f"  • {name}", True, (150, 180, 220))
            surf.blit(ns, (x, y)); y += ns.get_height() + 1


# ---------------------------------------------------------------------------
# Named/synthetic colors panel
# ---------------------------------------------------------------------------

SYNTHETIC = [
    ("Black",   (  0,   0,   0)),
    ("Red",     (255,   0,   0)),
    ("Green",   (  0, 255,   0)),
    ("Blue",    (  0,   0, 255)),
    ("Yellow",  (255, 255,   0)),
    ("Cyan",    (  0, 255, 255)),
    ("Magenta", (255,   0, 255)),
    ("White",   (255, 255, 255)),
    ("Gray",    (128, 128, 128)),
    ("Orange",  (255, 165,   0)),
]

def draw_synthetic_colors(surf, x, y, w, r, g, b, font_xs):
    cols = 5
    sw = (w - PAD) // cols - 4
    for i, (name, (sr, sg, sb)) in enumerate(SYNTHETIC):
        col = i % cols
        row = i // cols
        cx = x + col * (sw + 4)
        cy = y + row * (sw + 18)
        # Highlight if close to current
        dist = math.sqrt((r-sr)**2 + (g-sg)**2 + (b-sb)**2)
        border_col = GOLD if dist < 40 else BORDER
        pygame.draw.rect(surf, (sr, sg, sb), (cx, cy, sw, sw), border_radius=4)
        pygame.draw.rect(surf, border_col, (cx, cy, sw, sw), 2, border_radius=4)
        nl = font_xs.render(name, True, TEXT if dist > 40 else GOLD)
        surf.blit(nl, (cx, cy + sw + 2))

    return y + 2 * (sw + 18) + 4


# ---------------------------------------------------------------------------
# Model tab selector
# ---------------------------------------------------------------------------

class TabBar:
    def __init__(self, x, y, w, h, keys, colors):
        self.rects  = {}
        self.keys   = keys
        self.colors = colors
        tw = w // len(keys)
        for i, k in enumerate(keys):
            self.rects[k] = pygame.Rect(x + i*tw, y, tw-2, h)
        self.active = keys[0]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for k, r in self.rects.items():
                if r.collidepoint(event.pos):
                    self.active = k
                    return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            idx = self.keys.index(self.active)
            self.active = self.keys[(idx+1) % len(self.keys)]
            return True
        return False

    def draw(self, surf, font_md):
        for k, r in self.rects.items():
            is_active = (k == self.active)
            bg = (*[c//3 for c in self.colors[k]], 255) if not is_active else self.colors[k]
            col = self.colors[k]
            pygame.draw.rect(surf, (col[0]//3, col[1]//3, col[2]//3) if not is_active else col,
                             r, border_radius=5)
            pygame.draw.rect(surf, col, r, 2, border_radius=5)
            label_col = TEXT if is_active else DIM
            lbl = font_md.render(k, True, label_col)
            surf.blit(lbl, (r.centerx - lbl.get_width()//2,
                            r.centery - lbl.get_height()//2))


# ---------------------------------------------------------------------------
# Slider factory per model
# ---------------------------------------------------------------------------

def make_sliders(model_key, r=128, g=128, b=128):
    """Build slider list for the given model, initialised from RGB."""
    h, s, l = rgb_to_hsl(r, g, b)
    c, m, y = rgb_to_cmy(r, g, b)
    ck, mk, yk, k = rgb_to_cmyk(r, g, b)

    configs = {
        "RGB":  [
            (0, 255, r, "Red",        "", (220, 80,  80)),
            (0, 255, g, "Green",      "", ( 80, 200,  80)),
            (0, 255, b, "Blue",       "", ( 80, 120, 255)),
        ],
        "HSL":  [
            (0, 360, h, "Hue",        "°", (200, 180, 100)),
            (0, 100, s, "Saturation", "%", (180, 130, 220)),
            (0, 100, l, "Lightness",  "%", (180, 220, 180)),
        ],
        "CMY":  [
            (0, 100, c,  "Cyan",    "%", ( 60, 200, 200)),
            (0, 100, m,  "Magenta", "%", (220, 60,  180)),
            (0, 100, y,  "Yellow",  "%", (220, 200,  60)),
        ],
        "CMYK": [
            (0, 100, ck, "Cyan",    "%", ( 60, 200, 200)),
            (0, 100, mk, "Magenta", "%", (220, 60,  180)),
            (0, 100, yk, "Yellow",  "%", (220, 200,  60)),
            (0, 100, k,  "Key (K)", "%", (160, 160, 160)),
        ],
    }
    sliders = []
    base_y = 130
    for i, (mn, mx, iv, lbl, unit, col) in enumerate(configs[model_key]):
        sliders.append(Slider(
            x=PAD + 8,
            y=base_y + i * 72,
            w=LEFT_W - PAD*2 - 16,
            h=18,
            min_v=mn, max_v=mx, init=iv,
            label=lbl, unit=unit, color=col
        ))
    return sliders


def sliders_to_rgb(model_key, sliders):
    """Convert current slider values to (R, G, B) 0-255."""
    vals = [s.value for s in sliders]
    if model_key == "RGB":
        return int(vals[0]), int(vals[1]), int(vals[2])
    elif model_key == "HSL":
        return hsl_to_rgb(vals[0], vals[1], vals[2])
    elif model_key == "CMY":
        return cmy_to_rgb(int(vals[0]), int(vals[1]), int(vals[2]))
    elif model_key == "CMYK":
        return cmyk_to_rgb(int(vals[0]), int(vals[1]), int(vals[2]), int(vals[3]))
    return 128, 128, 128


def sync_sliders(model_key, sliders, r, g, b):
    """Sync slider values to match RGB after a model switch."""
    h, s, l = rgb_to_hsl(r, g, b)
    c, m, y = rgb_to_cmy(r, g, b)
    ck, mk, yk, k = rgb_to_cmyk(r, g, b)
    vals = {
        "RGB":  [r, g, b],
        "HSL":  [h, s, l],
        "CMY":  [c, m, y],
        "CMYK": [ck, mk, yk, k],
    }[model_key]
    for s_obj, v in zip(sliders, vals):
        s_obj.value = clamp(float(v), s_obj.min_v, s_obj.max_v)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # --- Locate poclets ---
    folder_override = sys.argv[1] if len(sys.argv) > 1 else None

    print("[TSCG] Loading Color Synthesis federated poclet family...")
    try:
        adapter = ColorSynthesisAdapter(folder_override)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if not adapter.models:
        print("[ERROR] No poclet files found.")
        print("  → Place M0_RGB_Additive.jsonld etc. next to this script,")
        print("    or pass the containing folder as argument.")
        sys.exit(1)

    for key, sim in adapter.models.items():
        print(f"  ✅ {key}: '{sim.label}'  REVOI mean={sim.revoi.mean():.2f}")

    models = adapter.models

    # --- Pygame ---
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("TSCG Simulation · Color Synthesis Federated")
    clock  = pygame.time.Clock()

    font_lg = pygame.font.SysFont("segoeui", 19, bold=True)
    font_md = pygame.font.SysFont("segoeui", 14, bold=True)
    font_sm = pygame.font.SysFont("segoeui", 13)
    font_xs = pygame.font.SysFont("segoeui", 11)

    # --- Tabs + sliders ---
    tabs = TabBar(LEFT_W + PAD, 8, MID_W - PAD, 28,
                  [k for k in MODEL_KEYS if k in models],
                  MODEL_COLORS)

    r, g, b     = 180, 80, 220     # initial color
    prev_model  = tabs.active
    sliders     = make_sliders(tabs.active, r, g, b)

    # --- Layout rects ---
    lp = pygame.Rect(0, 0, LEFT_W, WINDOW_H)
    mp = pygame.Rect(LEFT_W, 0, MID_W, WINDOW_H)
    rp = pygame.Rect(LEFT_W + MID_W, 0, RIGHT_W, WINDOW_H)

    asfid_rect  = pygame.Rect(rp.x+2, 4,       RIGHT_W-4, 162)
    revoi_rect  = pygame.Rect(rp.x+2, 170,     RIGHT_W-4, 260)
    status_rect = pygame.Rect(rp.x+2, 434,     RIGHT_W-4, WINDOW_H-438)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if tabs.handle_event(event):
                # Model switched → rebuild sliders keeping current RGB
                sliders = make_sliders(tabs.active, r, g, b)
                sync_sliders(tabs.active, sliders, r, g, b)
                prev_model = tabs.active
            for s in sliders:
                s.handle_event(event)

        # Current RGB from active model sliders
        r, g, b = sliders_to_rgb(tabs.active, sliders)
        r, g, b = clamp_i(r,0,255), clamp_i(g,0,255), clamp_i(b,0,255)

        # Derived values
        h, s_h, l_h  = rgb_to_hsl(r, g, b)
        c_c, m_c, y_c = rgb_to_cmy(r, g, b)
        ck, mk, yk, k = rgb_to_cmyk(r, g, b)
        hex_str       = f"#{r:02X}{g:02X}{b:02X}"

        # Dynamic ASFID for active model
        base_asfid  = models[tabs.active].asfid_base if tabs.active in models else ASFIDVector()
        asfid_live  = compute_dynamic_asfid(r, g, b, base_asfid)
        gap         = epistemic_gap_norm(asfid_live, base_asfid)

        # ── Draw ─────────────────────────────────────────────────────
        screen.fill(BG)

        # ── LEFT: sliders ────────────────────────────────────────────
        draw_panel_bg(screen, lp)

        # Title
        title = font_lg.render("🎨 Color Synthesis Federated", True, GOLD)
        screen.blit(title, (PAD, PAD))
        dom = font_xs.render("Domain: Optics / Color Science", True, DIM)
        screen.blit(dom, (PAD, PAD + title.get_height() + 2))

        pygame.draw.line(screen, BORDER, (PAD, 80), (LEFT_W-PAD, 80))
        mk_lbl = font_md.render(f"{tabs.active} Controls", True,
                                MODEL_COLORS.get(tabs.active, GOLD))
        screen.blit(mk_lbl, (PAD, 86))

        for s in sliders:
            s.draw(screen, font_sm, font_xs)

        # Color readout box
        ro_y = sliders[-1].rect.bottom + 24
        ro_rect = pygame.Rect(PAD, ro_y, LEFT_W-PAD*2, WINDOW_H-ro_y-PAD)
        draw_panel_bg(screen, ro_rect, PANEL2)
        ry = ro_rect.y + PAD

        # Big swatch
        sw_rect = pygame.Rect(ro_rect.x+PAD, ry, ro_rect.w-PAD*2, 40)
        pygame.draw.rect(screen, (r,g,b), sw_rect, border_radius=6)
        pygame.draw.rect(screen, TEXT, sw_rect, 1, border_radius=6)
        # Hex centered on swatch
        text_col = (255,255,255) if (r+g+b) < 380 else (0,0,0)
        hs = font_md.render(hex_str, True, text_col)
        screen.blit(hs, (sw_rect.centerx - hs.get_width()//2,
                         sw_rect.centery - hs.get_height()//2))
        ry += 48

        # Codes
        codes = [
            ("RGB",  f"({r}, {g}, {b})",               (220, 100, 100)),
            ("HSL",  f"({h:.0f}°, {s_h:.0f}%, {l_h:.0f}%)", (100, 180, 255)),
            ("CMY",  f"({c_c}%, {m_c}%, {y_c}%)",      ( 60, 200, 180)),
            ("CMYK", f"({ck}%, {mk}%, {yk}%, {k}%)",    (180, 140, 255)),
        ]
        for label, val, col in codes:
            is_active = (label == tabs.active)
            lbl = font_xs.render(label + ":", True, col if is_active else DIM)
            vs  = font_xs.render(val, True, col if is_active else TEXT)
            screen.blit(lbl, (ro_rect.x+PAD, ry))
            screen.blit(vs,  (ro_rect.x+PAD+40, ry))
            ry += lbl.get_height() + 3

        # ── CENTER ───────────────────────────────────────────────────
        pygame.draw.rect(screen, (16,16,24), mp)

        # Tabs
        tabs.draw(screen, font_md)

        # RGB Cube
        cube_cx = LEFT_W + MID_W // 2
        cube_cy = 260
        cube_title = font_md.render("RGB Color Cube", True, DIM)
        screen.blit(cube_title, (cube_cx - cube_title.get_width()//2, 44))
        draw_rgb_cube(screen, cube_cx, cube_cy, r, g, b, font_xs, scale=72)

        # Additive/subtractive note
        prin = "Additive (light)" if MODEL_ADDITIVE.get(tabs.active, True) else "Subtractive (pigment)"
        ps = font_xs.render(f"Principle: {prin}", True, DIM)
        screen.blit(ps, (LEFT_W+PAD, cube_cy+85))

        # Synthetic colors
        sc_title = font_md.render("Named Colors", True, DIM)
        screen.blit(sc_title, (LEFT_W+PAD, cube_cy+105))
        draw_synthetic_colors(screen, LEFT_W+PAD, cube_cy+122,
                              MID_W-PAD*2, r, g, b, font_xs)

        # Source label
        src = font_xs.render("Sources: M0_RGB/HSL/CMY/CMYK + M0_ColorSynthesis_Federated", True, (45,45,65))
        screen.blit(src, (LEFT_W+PAD, WINDOW_H-16))

        # FPS
        fps_s = font_xs.render(f"FPS: {int(clock.get_fps())}", True, (45,45,65))
        screen.blit(fps_s, (LEFT_W+MID_W-fps_s.get_width()-PAD, WINDOW_H-16))

        # ── RIGHT: ASFID + REVOI + Status ────────────────────────────
        pygame.draw.rect(screen, PANEL, rp)
        pygame.draw.line(screen, BORDER, (rp.x, 0), (rp.x, WINDOW_H))

        draw_asfid_live(screen, asfid_rect, asfid_live, base_asfid,
                        font_md, font_sm, font_xs)
        draw_revoi_comparison(screen, revoi_rect, models,
                              font_md, font_sm, font_xs)
        draw_status(screen, status_rect, r, g, b, tabs.active, models,
                    gap, font_md, font_sm, font_xs)

        pygame.display.flip()

    pygame.quit()
    print("[TSCG] Simulation ended.")


if __name__ == "__main__":
    main()
