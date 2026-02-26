"""
tpack_sim.py
============
TSCG Poclet Simulation - TPACK Knowledge Network (Pygame)
Author: Echopraxium with the collaboration of Claude AI

Driven by the TPACK poclet (M0_TPACK.jsonld) and M1_Education extension.

TPACK = Technological Pedagogical Content Knowledge
        Mishra & Koehler (2006)

Network layout (7 nodes):
  Core poles  : TK (Technology), PK (Pedagogy), CK (Content)
  Intersections: TPK, TCK, PCK, TPACK (center sweet spot)

Layout (1280x760):
  LEFT   (280px) : TK / PK / CK sliders + GenericConcept legend
  CENTER (690px) : Interactive knowledge network graph
  RIGHT  (310px) : ASFID live | REVOI scores | selected node details

Controls:
  Mouse drag sliders  : adjust TK / PK / CK levels
  Click a node        : inspect details (formula, GenericConcepts, description)
  ESC                 : quit

Requirements:
    pip install pygame
Run:
    python tpack_sim.py
"""

import sys
import math
import random
import pygame

# ---------------------------------------------------------------------------
# Window & layout constants
# ---------------------------------------------------------------------------
WINDOW_W, WINDOW_H = 1280, 760
FPS = 60

LEFT_W  = 280
RIGHT_W = 310
MID_W   = WINDOW_W - LEFT_W - RIGHT_W   # 690

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG          = (10,  12,  20)
PANEL       = (18,  20,  32)
PANEL2      = (24,  26,  40)
BORDER      = (50,  55,  80)
TEXT        = (220, 220, 235)
DIM         = (110, 115, 145)
GOLD        = (255, 200,  50)
WHITE       = (255, 255, 255)
PAD         = 12

SLIDER_TRACK = (35, 38, 58)

# Node colours
NODE_TK_COL  = ( 70, 140, 255)
NODE_PK_COL  = ( 80, 210, 120)
NODE_CK_COL  = (255, 165,  60)
NODE_TPK_COL = ( 80, 200, 200)
NODE_TCK_COL = (180, 100, 255)
NODE_PCK_COL = (180, 220,  70)
NODE_TPACK   = (255, 210,  50)

# ---------------------------------------------------------------------------
# TPACK data model
# ---------------------------------------------------------------------------
NODE_DEFS = {
    "TK": {
        "full": "Technology Knowledge",
        "color": NODE_TK_COL,
        "formula": "S \u2297 I \u2297 D",
        "generic_concepts": ["Component", "Transformation", "Adaptation"],
        "desc": (
            "Understanding of digital tools, platforms\n"
            "and resources. Continuously updated:\n"
            "desktop \u2192 Web2.0 \u2192 Mobile \u2192 AI.\n"
            "Examples: LMS (Moodle), Zoom, GeoGebra."
        ),
    },
    "PK": {
        "full": "Pedagogical Knowledge",
        "color": NODE_PK_COL,
        "formula": "S \u2297 I \u2297 A",
        "generic_concepts": ["Behavior", "Pattern", "Workflow", "Adaptation"],
        "desc": (
            "Knowledge of teaching methods and learning\n"
            "theories. Foundations: Bloom, Gagné, Merrill.\n"
            "Includes: Constructivism, Inquiry-Based,\n"
            "Scaffolding, ZPD."
        ),
    },
    "CK": {
        "full": "Content Knowledge",
        "color": NODE_CK_COL,
        "formula": "S \u2297 I",
        "generic_concepts": ["Hierarchy", "Composition", "Scope", "Language"],
        "desc": (
            "Deep subject matter expertise — knowing\n"
            "WHAT to teach.\n"
            "Shulman's insight: cannot teach what you\n"
            "don't know deeply."
        ),
    },
    "TPK": {
        "full": "Technological Pedagogical Knowledge",
        "color": NODE_TPK_COL,
        "formula": "TK \u2229 PK",
        "generic_concepts": ["Constraint", "Adaptation", "Affordance"],
        "desc": (
            "How technology supports or constrains\n"
            "pedagogical approaches.\n"
            "Example: Google Docs enables peer feedback;\n"
            "Zoom breakout \u2192 online collaboration."
        ),
    },
    "TCK": {
        "full": "Technological Content Knowledge",
        "color": NODE_TCK_COL,
        "formula": "TK \u2229 CK",
        "generic_concepts": ["Transformation", "Representation"],
        "desc": (
            "How technology transforms subject matter\n"
            "representation.\n"
            "Example: GeoGebra changes how math is\n"
            "EXPLORED, not just delivered."
        ),
    },
    "PCK": {
        "full": "Pedagogical Content Knowledge",
        "color": NODE_PCK_COL,
        "formula": "PK \u2229 CK",
        "generic_concepts": ["Synergy", "Integration", "Context"],
        "desc": (
            "Shulman (1986) \u2014 the original insight.\n"
            "HOW to teach SPECIFIC content.\n"
            "PCK \u2260 PK + CK : synergistic emergence.\n"
            "Example: manipulatives for fractions."
        ),
    },
    "TPACK": {
        "full": "Tech. Pedagogical Content Knowledge",
        "color": NODE_TPACK,
        "formula": "TK \u2229 PK \u2229 CK",
        "generic_concepts": ["Synergy (triple)", "Emergence", "Balance", "Trade-off"],
        "desc": (
            "The sweet spot \u2014 emergent knowledge.\n"
            "TPACK >> TK + PK + CK (strict).\n"
            "REVOI score: 0.94\n"
            "(highest of all poclets analysed)"
        ),
    },
}

EDGE_DEFS = [
    # Hexagon ring — each node connected to its two neighbours
    ("TK",  "TPK"), ("TPK", "PK"),
    ("PK",  "PCK"), ("PCK", "CK"),
    ("CK",  "TCK"), ("TCK", "TK"),
    # Spokes — intersections to TPACK centre
    ("TPK", "TPACK"),
    ("PCK", "TPACK"),
    ("TCK", "TPACK"),
    # Primary poles also reach TPACK
    ("TK",  "TPACK"),
    ("PK",  "TPACK"),
    ("CK",  "TPACK"),
]

REVOI_SCORES = {"R": 0.98, "E": 0.92, "V": 0.90, "O": 0.95, "I": 0.95}
REVOI_LABELS = {
    "R": "Representability", "E": "Evolvability",
    "V": "Verifiability",    "O": "Observability",
    "I": "Interoperability",
}
REVOI_COLORS = {
    "R": (100, 180, 255), "E": (100, 220, 140),
    "V": (255, 180,  80), "O": (200, 130, 255),
    "I": (255, 120, 120),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def draw_rounded_rect(surf, color, rect, radius=8, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surf, border_color or BORDER, rect, border, border_radius=radius)

# ---------------------------------------------------------------------------
# Slider
# ---------------------------------------------------------------------------
class Slider:
    H = 8

    def __init__(self, x, y, w, label, color, value=0.5):
        self.rect   = pygame.Rect(x, y, w, 44)
        self.label  = label
        self.color  = color
        self.value  = value
        self._drag  = False
        self._track = pygame.Rect(x, y + 28, w, self.H)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._track.inflate(0, 18).collidepoint(event.pos):
                self._drag = True
                self._update(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._drag = False
        elif event.type == pygame.MOUSEMOTION and self._drag:
            self._update(event.pos[0])

    def _update(self, mx):
        self.value = clamp((mx - self._track.x) / self._track.w, 0.0, 1.0)

    def draw(self, surf, font_md, font_xs):
        lbl  = font_md.render(self.label, True, self.color)
        pct  = font_xs.render(f"{int(self.value*100)}%", True, TEXT)
        surf.blit(lbl, (self._track.x, self.rect.y))
        surf.blit(pct, (self._track.right - pct.get_width(), self.rect.y + 2))
        pygame.draw.rect(surf, SLIDER_TRACK, self._track, border_radius=4)
        fw = int(self._track.w * self.value)
        if fw > 4:
            pygame.draw.rect(surf, self.color,
                             (self._track.x, self._track.y, fw, self.H),
                             border_radius=4)
        hx = self._track.x + fw
        pygame.draw.circle(surf, self.color, (hx, self._track.centery), 7)
        pygame.draw.circle(surf, WHITE,      (hx, self._track.centery), 3)

# ---------------------------------------------------------------------------
# Particles
# ---------------------------------------------------------------------------
class Particle:
    def __init__(self, p1, p2, color, speed=0.3):
        self.p1    = p1
        self.p2    = p2
        self.color = color
        self.t     = random.random() * 0.3
        self.speed = speed * (0.6 + random.random() * 0.8)

    def update(self, dt):
        self.t += self.speed * dt
        return self.t < 1.0

    def pos(self):
        return (
            int(self.p1[0] + (self.p2[0] - self.p1[0]) * self.t),
            int(self.p1[1] + (self.p2[1] - self.p1[1]) * self.t),
        )


class ParticleSystem:
    MAX = 180

    def __init__(self):
        self._parts  = []
        self._timers = {}

    def update(self, dt, edges_active):
        self._parts = [p for p in self._parts if p.update(dt)]
        for key, (p1, p2, col, strength) in edges_active.items():
            if strength < 0.04:
                continue
            t = self._timers.get(key, 0.0) - dt
            if t <= 0 and len(self._parts) < self.MAX:
                self._timers[key] = 0.25 + (1.0 - strength) * 1.2
                self._parts.append(Particle(p1, p2, col, 0.20 + strength * 0.55))
            else:
                self._timers[key] = max(0.0, t)

    def draw(self, surf):
        for p in self._parts:
            x, y = p.pos()
            fade = lerp_color(p.color, BG, p.t * 0.8)
            r    = max(1, int(3 * (1.0 - p.t)))
            pygame.draw.circle(surf, fade, (x, y), r)

# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------
class KnowledgeNetwork:

    def __init__(self, cx, cy, radius=210):
        self.cx, self.cy = cx, cy
        self.radius  = radius
        self._sel    = None
        self._hover  = None
        self._pos    = {}
        self._r      = {}
        self._vals   = {}
        self._particles = ParticleSystem()
        self._setup()

    def _setup(self):
        r  = self.radius
        cx, cy = self.cx, self.cy

        def pt(deg, dist=1.0):
            a = math.radians(deg)
            return (int(cx + r * dist * math.cos(a)),
                    int(cy + r * dist * math.sin(a)))

        # Hexagon: alternating primary poles and intersections
        # TK(top) → TPK → PK → PCK → CK → TCK → back to TK
        # Each intersection sits exactly between its two parent poles
        self._pos = {
            "TK":    pt(-90),    #  top
            "TPK":   pt(-30),    #  top-right   (between TK and PK)
            "PK":    pt(30),     #  bottom-right
            "PCK":   pt(90),     #  bottom       (between PK and CK)
            "CK":    pt(150),    #  bottom-left
            "TCK":   pt(210),    #  top-left     (between CK and TK)
            "TPACK": (cx, cy),   #  centre
        }
        self._r    = {k: 18.0 for k in self._pos}
        self._vals = {k: 0.0  for k in self._pos}

    def update(self, dt, tk, pk, ck):
        tpk   = math.sqrt(tk * pk)
        tck   = math.sqrt(tk * ck)
        pck   = math.sqrt(pk * ck)
        tpack = (tk * pk * ck) ** (1.0 / 3.0)
        self._vals = {
            "TK": tk, "PK": pk, "CK": ck,
            "TPK": tpk, "TCK": tck, "PCK": pck,
            "TPACK": tpack,
        }
        for k, v in self._vals.items():
            target = 18 + v * 28
            self._r[k] += (target - self._r[k]) * min(1.0, dt * 5)

        edges_active = {}
        for a, b in EDGE_DEFS:
            s = min(self._vals[a], self._vals[b])
            if s > 0.02:
                col = lerp_color(NODE_DEFS[a]["color"], NODE_DEFS[b]["color"], 0.5)
                edges_active[f"{a}-{b}"] = (self._pos[a], self._pos[b], col, s)
        self._particles.update(dt, edges_active)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._hover = self._hit(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            h = self._hit(event.pos)
            self._sel = h if h != self._sel else None

    def _hit(self, pos):
        mx, my = pos
        for k, (nx, ny) in self._pos.items():
            r = self._r[k] + 6
            if (mx - nx) ** 2 + (my - ny) ** 2 <= r * r:
                return k
        return None

    @property
    def selected(self):
        return self._sel

    @property
    def node_values(self):
        return dict(self._vals)

    def draw(self, surf, font_md, font_sm, font_xs):
        # Edges
        for a, b in EDGE_DEFS:
            s = min(self._vals[a], self._vals[b])
            col = lerp_color(BORDER, lerp_color(NODE_DEFS[a]["color"], NODE_DEFS[b]["color"], 0.5), s)
            w   = max(1, int(1 + s * 3))
            pygame.draw.line(surf, col, self._pos[a], self._pos[b], w)

        self._particles.draw(surf)

        # Nodes
        for k, (nx, ny) in self._pos.items():
            v   = self._vals[k]
            r   = int(self._r[k])
            col = NODE_DEFS[k]["color"]

            # Glow
            if v > 0.08:
                gc = lerp_color(BG, col, v * 0.25)
                pygame.draw.circle(surf, gc, (nx, ny), r + int(8 * v))

            # Selection / hover ring
            if k == self._sel:
                pygame.draw.circle(surf, GOLD,  (nx, ny), r + 6, 2)
            elif k == self._hover:
                pygame.draw.circle(surf, WHITE, (nx, ny), r + 4, 1)

            # Body
            body_col = lerp_color(PANEL, col, 0.25 + v * 0.75)
            pygame.draw.circle(surf, body_col, (nx, ny), r)
            pygame.draw.circle(surf, col,      (nx, ny), r, 2)

            # Label
            lbl = font_md.render(k, True, col if v > 0.15 else DIM)
            surf.blit(lbl, (nx - lbl.get_width() // 2, ny - lbl.get_height() // 2))

            # Value pct below node
            if v > 0.04:
                ps = font_xs.render(f"{int(v*100)}%", True, lerp_color(DIM, WHITE, v))
                surf.blit(ps, (nx - ps.get_width() // 2, ny + r + 2))

# ---------------------------------------------------------------------------
# Panel draw helpers
# ---------------------------------------------------------------------------

def draw_panel(surf, rect, color=None):
    pygame.draw.rect(surf, color or PANEL, rect)
    pygame.draw.rect(surf, BORDER, rect, 1)


def draw_asfid(surf, rect, node_vals, font_md, font_sm, font_xs):
    draw_rounded_rect(surf, PANEL2, rect, 8, 1)
    y = rect.y + PAD

    t = font_md.render("\u26a1 ASFID  (Eagle Eye)", True, GOLD)
    surf.blit(t, (rect.x + PAD, y));  y += t.get_height() + 6

    tk = node_vals.get("TK", 0.0)
    pk = node_vals.get("PK", 0.0)
    ck = node_vals.get("CK", 0.0)
    dims = [
        ("A", "Attractors",   node_vals.get("TPACK", 0.0),        "Integration centre"),
        ("S", "Structure",    (tk + pk + ck) / 3.0,               "7-node Venn topology"),
        ("F", "Flows",        node_vals.get("TPK", 0.0),           "Knowledge transfer"),
        ("I", "Information",  node_vals.get("PCK", 0.0),           "Content encoding"),
        ("D", "Dynamics",     node_vals.get("TCK", 0.0),           "Epistemic change"),
    ]
    bw = rect.w - PAD * 2 - 36
    for letter, name, val, _ in dims:
        lbl = font_sm.render(letter, True, GOLD)
        nm  = font_xs.render(f" {name}", True, DIM)
        surf.blit(lbl, (rect.x + PAD, y))
        surf.blit(nm,  (rect.x + PAD + 14, y + 1))
        bx, by = rect.x + PAD, y + lbl.get_height() + 2
        pygame.draw.rect(surf, SLIDER_TRACK, (bx, by, bw, 6), border_radius=3)
        fw = int(bw * clamp(val, 0, 1))
        if fw > 4:
            c = lerp_color((40, 80, 120), (80, 200, 255), val)
            pygame.draw.rect(surf, c, (bx, by, fw, 6), border_radius=3)
        ps = font_xs.render(f"{int(val*100)}%", True, TEXT)
        surf.blit(ps, (bx + bw + 4, y))
        y += lbl.get_height() + 10
    return y


def draw_revoi(surf, rect, font_md, font_sm, font_xs):
    draw_rounded_rect(surf, PANEL2, rect, 8, 1)
    y = rect.y + PAD

    t = font_md.render("\U0001f5ff REVOI  (Sphinx Eye)", True, (180, 140, 255))
    surf.blit(t, (rect.x + PAD, y));  y += t.get_height() + 4

    mean_s = font_xs.render("Mean: 0.94  \u2190 highest of all poclets", True, GOLD)
    surf.blit(mean_s, (rect.x + PAD, y));  y += mean_s.get_height() + 6

    bw = rect.w - PAD * 2 - 36
    for letter, score in REVOI_SCORES.items():
        col  = REVOI_COLORS[letter]
        name = REVOI_LABELS[letter]
        lbl  = font_sm.render(letter, True, col)
        nm   = font_xs.render(f" {name}", True, DIM)
        surf.blit(lbl, (rect.x + PAD, y))
        surf.blit(nm,  (rect.x + PAD + 14, y + 1))
        bx, by = rect.x + PAD, y + lbl.get_height() + 2
        pygame.draw.rect(surf, SLIDER_TRACK, (bx, by, bw, 6), border_radius=3)
        pygame.draw.rect(surf, col, (bx, by, int(bw * score), 6), border_radius=3)
        sc_s = font_xs.render(f"{score:.2f}", True, TEXT)
        surf.blit(sc_s, (bx + bw + 4, y))
        y += lbl.get_height() + 10
    return y


def draw_node_detail(surf, rect, node_key, node_vals, font_md, font_sm, font_xs):
    draw_rounded_rect(surf, PANEL2, rect, 8, 1)
    if not node_key:
        hint = font_sm.render("Click a node to inspect", True, DIM)
        surf.blit(hint, (rect.x + PAD, rect.y + PAD))
        return

    nd  = NODE_DEFS[node_key]
    col = nd["color"]
    pygame.draw.rect(surf, col, (rect.x, rect.y, rect.w, 4), border_radius=8)
    y = rect.y + PAD + 4

    surf.blit(font_md.render(node_key, True, col), (rect.x + PAD, y))
    y += font_md.get_height() + 2
    surf.blit(font_xs.render(nd["full"], True, DIM), (rect.x + PAD, y))
    y += font_xs.get_height() + 6

    # Formula
    fm  = font_sm.render("Formula:", True, GOLD)
    fmv = font_sm.render(nd["formula"], True, TEXT)
    surf.blit(fm,  (rect.x + PAD, y))
    surf.blit(fmv, (rect.x + PAD + fm.get_width() + 6, y))
    y += fm.get_height() + 6

    # Level bar
    val = node_vals.get(node_key, 0.0)
    surf.blit(font_sm.render("Level:", True, GOLD), (rect.x + PAD, y))
    y += font_sm.get_height() + 2
    bw = rect.w - PAD * 2
    pygame.draw.rect(surf, SLIDER_TRACK, (rect.x + PAD, y, bw, 8), border_radius=4)
    fw = int(bw * val)
    if fw > 4:
        pygame.draw.rect(surf, col, (rect.x + PAD, y, fw, 8), border_radius=4)
    surf.blit(font_xs.render(f"{int(val*100)}%", True, TEXT),
              (rect.x + PAD + bw - 28, y - 1))
    y += 14

    # GenericConcepts
    surf.blit(font_sm.render("GenericConcepts:", True, GOLD), (rect.x + PAD, y))
    y += font_sm.get_height() + 2
    for gc in nd["generic_concepts"]:
        s = font_xs.render(f"  \u2022 {gc}", True, lerp_color(DIM, col, 0.6))
        surf.blit(s, (rect.x + PAD, y))
        y += s.get_height() + 1
    y += 4

    # Description
    surf.blit(font_sm.render("Description:", True, GOLD), (rect.x + PAD, y))
    y += font_sm.get_height() + 2
    for line in nd["desc"].split("\n"):
        ls = font_xs.render(line, True, DIM)
        if y + ls.get_height() < rect.bottom - 4:
            surf.blit(ls, (rect.x + PAD, y))
            y += ls.get_height() + 2


def draw_legend(surf, x, y, font_xs):
    items = [
        ("\u25cf", NODE_TK_COL,  "TK  Technology"),
        ("\u25cf", NODE_PK_COL,  "PK  Pedagogy"),
        ("\u25cf", NODE_CK_COL,  "CK  Content"),
        ("\u2500", (55, 58, 80), "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        ("\u25cf", NODE_TPK_COL, "TPK  TK \u2229 PK"),
        ("\u25cf", NODE_TCK_COL, "TCK  TK \u2229 CK"),
        ("\u25cf", NODE_PCK_COL, "PCK  PK \u2229 CK"),
        ("\u2605", NODE_TPACK,   "TPACK  sweet spot"),
    ]
    for sym, col, name in items:
        s = font_xs.render(f"{sym}  {name}", True, col)
        surf.blit(s, (x, y))
        y += s.get_height() + 3
    return y

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(
        "TSCG | TPACK Knowledge Network \u2014 Poclet Simulation"
    )
    clock = pygame.time.Clock()

    def try_font(names, size, bold=False):
        for n in names:
            try:
                f = pygame.font.SysFont(n, size, bold=bold)
                if f:
                    return f
            except Exception:
                pass
        return pygame.font.SysFont(None, size, bold=bold)

    font_lg = try_font(["segoeui", "arial", "freesansbold"], 20, bold=True)
    font_md = try_font(["segoeui", "arial"],                  15, bold=True)
    font_sm = try_font(["segoeui", "arial"],                  13)
    font_xs = try_font(["dejavusansmono", "couriernew", "monospace"], 11)

    # Sliders
    sx, sw = PAD, LEFT_W - PAD * 2
    sliders = {
        "TK": Slider(sx, 80,  sw, "TK  Technology", NODE_TK_COL, 0.65),
        "PK": Slider(sx, 136, sw, "PK  Pedagogy",   NODE_PK_COL, 0.70),
        "CK": Slider(sx, 192, sw, "CK  Content",    NODE_CK_COL, 0.55),
    }

    # Network (centre of middle panel)
    net_cx = LEFT_W + MID_W // 2
    net_cy = WINDOW_H // 2 + 15
    network = KnowledgeNetwork(net_cx, net_cy, radius=210)

    # Rects
    lp = pygame.Rect(0,           0, LEFT_W,  WINDOW_H)
    mp = pygame.Rect(LEFT_W,      0, MID_W,   WINDOW_H)
    rp = pygame.Rect(LEFT_W+MID_W,0, RIGHT_W, WINDOW_H)

    asfid_rect  = pygame.Rect(rp.x + 4,   4, RIGHT_W - 8, 195)
    revoi_rect  = pygame.Rect(rp.x + 4, 204, RIGHT_W - 8, 214)
    detail_rect = pygame.Rect(rp.x + 4, 424, RIGHT_W - 8, WINDOW_H - 428)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            for s in sliders.values():
                s.handle_event(event)
            network.handle_event(event)

        tk = sliders["TK"].value
        pk = sliders["PK"].value
        ck = sliders["CK"].value

        network.update(dt, tk, pk, ck)
        node_vals = network.node_values
        tpack_v   = node_vals.get("TPACK", 0.0)

        # ── Draw ────────────────────────────────────────────
        screen.fill(BG)

        # ── LEFT ────────────────────────────────────────────
        draw_panel(screen, lp, PANEL)

        title = font_lg.render("\U0001f393 TPACK Network", True, GOLD)
        screen.blit(title, (PAD, PAD))
        screen.blit(
            font_xs.render("Mishra & Koehler (2006)", True, DIM),
            (PAD, PAD + title.get_height() + 1)
        )
        pygame.draw.line(screen, BORDER, (PAD, 68), (LEFT_W - PAD, 68))

        for s in sliders.values():
            s.draw(screen, font_md, font_xs)

        pygame.draw.line(screen, BORDER, (PAD, 248), (LEFT_W - PAD, 248))

        # TPACK integration bar
        screen.blit(font_sm.render("TPACK Integration Level", True, DIM), (PAD, 254))
        tpack_col = lerp_color(DIM, NODE_TPACK, tpack_v)
        bx, by, bw, bh = PAD, 272, LEFT_W - PAD * 2, 14
        pygame.draw.rect(screen, SLIDER_TRACK, (bx, by, bw, bh), border_radius=6)
        fw = int(bw * tpack_v)
        if fw > 6:
            pygame.draw.rect(screen, tpack_col, (bx, by, fw, bh), border_radius=6)
        tv = font_md.render(f"{int(tpack_v*100)}%", True, tpack_col)
        screen.blit(tv, (bx + bw // 2 - tv.get_width() // 2, by - 1))

        # Emergence
        emergence = max(0.0, tpack_v - (tk + pk + ck) / 3.0)
        em_col = lerp_color(DIM, GOLD, clamp(emergence * 8, 0, 1))
        screen.blit(
            font_xs.render(f"Emergence: +{int(emergence*100)}%", True, em_col),
            (PAD, 292)
        )
        screen.blit(
            font_xs.render("(TPACK >> TK+PK+CK)", True, lerp_color(DIM, GOLD, clamp(emergence*6,0,1))),
            (PAD, 306)
        )

        pygame.draw.line(screen, BORDER, (PAD, 325), (LEFT_W - PAD, 325))

        # Legend
        screen.blit(font_sm.render("Node Legend", True, DIM), (PAD, 331))
        draw_legend(screen, PAD, 349, font_xs)

        screen.blit(
            font_xs.render("Source: M0_TPACK.jsonld", True, (40, 42, 60)),
            (PAD, WINDOW_H - 16)
        )

        # ── CENTER ──────────────────────────────────────────
        pygame.draw.rect(screen, (11, 13, 22), mp)

        ct = font_lg.render("Knowledge Network \u2014 7 Regions", True, TEXT)
        screen.blit(ct, (LEFT_W + MID_W // 2 - ct.get_width() // 2, PAD))
        cs = font_xs.render(
            "ASFID: Territory view  |  Click nodes to inspect  |  Drag sliders to adjust knowledge levels",
            True, DIM
        )
        screen.blit(cs, (LEFT_W + MID_W // 2 - cs.get_width() // 2, PAD + ct.get_height() + 2))

        network.draw(screen, font_md, font_sm, font_xs)

        screen.blit(
            font_xs.render(
                "REVOI = 0.94  \u2022  50 000+ citations  \u2022  193 validation studies  \u2022  50+ countries",
                True, (45, 48, 68)
            ),
            (LEFT_W + PAD, WINDOW_H - 16)
        )
        fps_s = font_xs.render(f"FPS: {int(clock.get_fps())}", True, (40, 42, 60))
        screen.blit(fps_s, (LEFT_W + MID_W - fps_s.get_width() - PAD, WINDOW_H - 16))

        # ── RIGHT ───────────────────────────────────────────
        draw_panel(screen, rp, PANEL)
        pygame.draw.line(screen, BORDER, (rp.x, 0), (rp.x, WINDOW_H))

        draw_asfid(screen, asfid_rect, node_vals, font_md, font_sm, font_xs)
        draw_revoi(screen, revoi_rect, font_md, font_sm, font_xs)
        draw_node_detail(screen, detail_rect, network.selected, node_vals,
                         font_md, font_sm, font_xs)

        pygame.display.flip()

    pygame.quit()
    print("[TSCG] TPACK simulation ended.")


if __name__ == "__main__":
    main()
