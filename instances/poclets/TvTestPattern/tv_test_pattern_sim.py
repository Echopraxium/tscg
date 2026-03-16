"""
TV Test Pattern Simulator — TSCG M0_TVTestPattern
B&W analogue test pattern (inspired by the 1939 Indian Head / RMA resolution chart)

Controls:
  - Hover a zone   : orange highlight + diagnostic in right panel
  - FIX  button    : click a degraded zone to restore it
  - DEGRADE button : click any zone to add degradation
  FIX and DEGRADE are mutually exclusive.

Requirements: pip install pygame
Author: Echopraxium with the collaboration of Claude AI
"""

import pygame
import pygame.gfxdraw
import random
import math
import sys

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
WIN_W, WIN_H = 1280, 780
PAT_W        = 680
DESC_W       = WIN_W - PAT_W
PAT_H        = WIN_H

BG_COLOR     = (10,  10,  10)
PANEL_BG     = (18,  18,  22)
BORDER_COLOR = (50,  50,  60)
WHITE        = (240, 240, 240)
BLACK        = (0,   0,   0)
ORANGE       = (255, 140,  0)
AMBER        = (245, 166,  35)
GREEN_DIM    = (40,  180,  80)
RED_DIM      = (200,  50,  50)
GREY_DIM     = (70,   70,  80)
TEXT_COLOR   = (200, 200, 210)

FPS = 30

# ─────────────────────────────────────────────
#  ZONE DEFINITIONS
# ─────────────────────────────────────────────
ZONE_DEFS = [
    {
        "id":    "greyscale",
        "name":  "Greyscale Staircase",
        "rect":  pygame.Rect(0, 0, 680, 72),
        "asfid": "A · It",
        "desc":  (
            "7 luminance steps: 7.5 IRE (black) → 100 IRE (white).\n\n"
            "Instrument: Waveform Monitor\n\n"
            "Defects revealed:\n"
            "  • Gain error — white clipping or black crush\n"
            "  • Gamma non-linearity — unequal step heights\n"
            "  • Dynamic range compression\n\n"
            "The 7.5 IRE black level (US pedestal) is the\n"
            "critical calibration anchor for the entire\n"
            "luminance chain."
        ),
        "degradations": [
            ("noise",  "SNR degradation — steps become indistinct under noise."),
            ("lines",  "Dropped scan lines — partial frame loss (sync fault)."),
            ("bright", "Black level lifted — dynamic range crushed to grey."),
        ],
    },
    {
        "id":    "portrait",
        "name":  "Indian Head Portrait",
        "rect":  pygame.Rect(265, 78, 150, 160),
        "asfid": "A · R",
        "desc":  (
            "Central reference image: Native American chief\n"
            "in full headdress (RCA/NBC, 1939).\n\n"
            "Instrument: Direct visual inspection\n\n"
            "Fine feather detail = natural high-frequency\n"
            "resolution target. Defects:\n"
            "  • Ringing / edge ghosting (impedance mismatch)\n"
            "  • Interlace combing (field mis-alignment)\n"
            "  • Smearing (bandwidth loss in signal chain)"
        ),
        "degradations": [
            ("noise",  "Ghosting / multipath reflection on coaxial cable."),
            ("lines",  "Interlace combing — odd/even field mis-alignment."),
        ],
    },
    {
        "id":    "wedge_tl",
        "name":  "Wedge — Vertical Resolution (Top-Left)",
        "rect":  pygame.Rect(60, 220, 160, 140),
        "asfid": "A · It · D",
        "desc":  (
            "Converging lines fan (100 → 500 TVL).\n\n"
            "Horizontal wedge → tests vertical resolution\n"
            "(limited by line count: 625 lines PAL).\n\n"
            "Instrument: Direct visual reading\n\n"
            "Where lines merge into grey = resolution limit.\n"
            "Target: > 400 TVL for broadcast quality."
        ),
        "degradations": [
            ("blur",  "High-frequency rolloff — lines merge prematurely."),
            ("noise", "Noise floor raised — fine lines buried in static."),
        ],
    },
    {
        "id":    "wedge_tr",
        "name":  "Wedge — Horizontal Resolution (Top-Right)",
        "rect":  pygame.Rect(460, 220, 160, 140),
        "asfid": "A · It · D",
        "desc":  (
            "Converging lines fan (100 → 500 TVL).\n\n"
            "Vertical wedge → tests horizontal resolution\n"
            "(limited by bandwidth: 5.5 MHz PAL).\n\n"
            "Instrument: Waveform monitor + spectrum analyser\n\n"
            "Cable loss = progressive blur from narrow end\n"
            "outward. Each metre of coax costs bandwidth."
        ),
        "degradations": [
            ("blur",  "Bandwidth loss — high-freq content attenuated by cable."),
            ("noise", "Cable interference — random scatter on fine detail."),
        ],
    },
    {
        "id":    "wedge_bl",
        "name":  "Wedge — Diagonal Resolution (Bottom-Left)",
        "rect":  pygame.Rect(60, 430, 160, 130),
        "asfid": "A · It",
        "desc":  (
            "Rotated (90°) wedge — tests diagonal resolution\n"
            "and aliasing artefacts.\n\n"
            "Instrument: Direct visual inspection\n\n"
            "Reveals:\n"
            "  • Moire patterns (sampling artefacts)\n"
            "  • Geometric non-linearity\n"
            "  • Diagonal smearing (frame-store error)"
        ),
        "degradations": [
            ("lines", "Moire / aliasing — diagonal lines staircase."),
            ("noise", "Frame-store smearing — memory corruption artefact."),
        ],
    },
    {
        "id":    "wedge_br",
        "name":  "Wedge — Diagonal Resolution (Bottom-Right)",
        "rect":  pygame.Rect(460, 430, 160, 130),
        "asfid": "A · It",
        "desc":  (
            "Rotated (-90°) wedge — mirror of bottom-left.\n\n"
            "Symmetry check: both diagonals must degrade\n"
            "identically. Asymmetry reveals:\n"
            "  • Scan skew (horizontal deflection non-linearity)\n"
            "  • Left/right path mismatch\n\n"
            "Instrument: Direct visual comparison."
        ),
        "degradations": [
            ("lines", "Scan skew — deflection non-linearity on right side."),
            ("noise", "Asymmetric interference — right signal path fault."),
        ],
    },
    {
        "id":    "circle",
        "name":  "Geometry Circle",
        "rect":  pygame.Rect(195, 255, 290, 290),
        "asfid": "S · It",
        "desc":  (
            "Large circle: the perfect geometric invariant.\n"
            "Must be perfectly round on a calibrated display.\n\n"
            "Instrument: Direct visual inspection + ruler\n\n"
            "Distortions:\n"
            "  • Ellipse → aspect ratio not 4:3\n"
            "  • Barrel / pincushion → deflection coil fault\n"
            "  • Flat top/bottom → vertical linearity error\n"
            "  • Flat sides → horizontal linearity error\n\n"
            "Concentric rings give quantitative distortion scale."
        ),
        "degradations": [
            ("lines", "Geometric distortion — deflection non-linearity."),
            ("noise", "Sync jitter — circle wobbles horizontally."),
        ],
    },
    {
        "id":    "greyscale_bottom",
        "name":  "Greyscale Ramp (Bottom)",
        "rect":  pygame.Rect(0, 600, 680, 60),
        "asfid": "A · It",
        "desc":  (
            "Continuous gradient: black → white.\n\n"
            "Complements the staircase: reveals smooth\n"
            "transition quality.\n\n"
            "Instrument: Waveform Monitor\n\n"
            "Defects:\n"
            "  • Banding → quantisation (digital path)\n"
            "  • S-curve → gamma compression error\n"
            "  • Texture → noise in analogue path"
        ),
        "degradations": [
            ("noise",  "Quantisation banding — digital path artefact."),
            ("bright", "Gamma S-curve — non-linear transfer function."),
        ],
    },
    {
        "id":    "sync_bar",
        "name":  "Sync Pulse Reference Bar",
        "rect":  pygame.Rect(0, 660, 680, 40),
        "asfid": "D · It",
        "desc":  (
            "Reference black bar at 0 IRE (sync tip level).\n\n"
            "Instrument: Oscilloscope\n\n"
            "The sync tip at -40 IRE (US) / 0 mV (EBU) is\n"
            "the timing reference for every scan line.\n\n"
            "Defects:\n"
            "  • Bar not truly black → black level elevated\n"
            "  • Flickering bar → sync instability\n"
            "  • Rolling bar → field sync failure"
        ),
        "degradations": [
            ("lines",  "Sync instability — bar flickers and rolls."),
            ("bright", "Black level drift — bar lifted above 0 IRE."),
        ],
    },
]

ORIGIN_TITLE = "Indian Head Test Pattern"
ORIGIN_TEXT = (
    "Origin & History\n"
    "─────────────────────────────\n"
    "Developed by RCA for NBC in 1939 for the New\n"
    "York World's Fair broadcast. Became the de facto\n"
    "US standard, transmitted overnight by hundreds\n"
    "of stations from the 1940s through the 1970s.\n\n"
    "The Native American chief portrait was chosen\n"
    "for its fine feather detail (high-freq test),\n"
    "strong tonal contrasts (greyscale test), and\n"
    "as a flesh-tone reference for colour adapters.\n\n"
    "Technical Standard\n"
    "─────────────────────────────\n"
    "Format : NTSC  525-line / 60 Hz\n"
    "Aspect : 4:3\n"
    "Black  : 7.5 IRE   White: 100 IRE\n"
    "Ref    : RMA Standard, 1939\n\n"
    "TSCG Classification\n"
    "─────────────────────────────\n"
    "Poclet : M0_TVTestPattern v1.0.0\n"
    "M2     : m2:Calibration  A\u2297F\u2297It\u2297D\n"
    "ASFID  : 0.88\n"
    "REVOI  : 0.87\n"
    "delta  : 0.13  (mature coupling)\n"
    "Domain : Signal Engineering / Broadcast\n\n"
    "Hover any zone on the left to see\n"
    "its diagnostic description.\n"
    "Use DEGRADE / FIX buttons to simulate\n"
    "and repair signal chain faults."
)


# ─────────────────────────────────────────────
#  TEXT RENDERING HELPER
# ─────────────────────────────────────────────
def draw_text_wrapped(surface, text, font, color, rect, line_spacing=3):
    x, y = rect.x, rect.y
    max_w = rect.width
    lh    = font.get_height() + line_spacing
    for raw in text.split("\n"):
        if y + lh > rect.bottom:
            break
        if raw.strip() == "":
            y += lh // 2
            continue
        words = raw.split(" ")
        line  = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    surface.blit(font.render(line, True, color), (x, y))
                    y += lh
                    if y + lh > rect.bottom:
                        return
                line = w
        if line:
            surface.blit(font.render(line, True, color), (x, y))
            y += lh


# ─────────────────────────────────────────────
#  PATTERN DRAWING
# ─────────────────────────────────────────────
def draw_greyscale_strip(surf, rect, steps=7):
    w = rect.width // steps
    f = pygame.font.SysFont("monospace", 9)
    ire_labels = [7.5, 20, 35, 50, 65, 80, 100]
    for i in range(steps):
        v  = int(19 + (230 - 19) * i / (steps - 1))
        r  = pygame.Rect(rect.x + i * w, rect.y, w, rect.height)
        pygame.draw.rect(surf, (v, v, v), r)
        tc = (200, 200, 200) if v < 120 else (40, 40, 40)
        lbl = f.render(str(ire_labels[i]), True, tc)
        surf.blit(lbl, (r.centerx - lbl.get_width() // 2, rect.bottom - 14))
    # IRE label
    lbl2 = f.render("IRE", True, (180, 110, 0))
    surf.blit(lbl2, (rect.x + 3, rect.y + 3))


def draw_portrait(surf, cx, cy, r):
    pygame.draw.circle(surf, (225, 225, 225), (cx, cy + 8), r)
    pygame.draw.circle(surf, BLACK, (cx, cy + 8), r, 3)
    # feathers
    n = 20
    for i in range(n):
        ang = math.radians(-155 + i * (130 / (n - 1)))
        col = (15, 15, 15) if i % 2 == 0 else (155, 155, 155)
        x1  = cx + int(math.cos(ang) * (r - 12))
        y1  = (cy + 8) + int(math.sin(ang) * (r - 12))
        x2  = cx + int(math.cos(ang) * (r + 24))
        y2  = (cy + 8) + int(math.sin(ang) * (r + 24))
        pygame.draw.line(surf, col, (x1, y1), (x2, y2), 2)
        pygame.draw.circle(surf, (70, 70, 70), (x2, y2), 3)
    # headband
    band_y = cy + 8 - r + 16
    pygame.draw.rect(surf, (40, 40, 40), (cx - r + 5, band_y, (r - 5) * 2, 10))
    for i in range(0, (r - 5) * 2, 7):
        pygame.draw.line(surf, (190, 190, 190),
                         (cx - r + 5 + i, band_y + 1),
                         (cx - r + 5 + i, band_y + 9), 1)
    # face
    fh = int(r * 0.70)
    fw = int(r * 0.48)
    pygame.draw.ellipse(surf, (175, 175, 175),
                        (cx - fw, cy + 8 - fh // 2 + 6, fw * 2, fh))
    ey = cy + 8 - fh // 6
    pygame.draw.ellipse(surf, (25, 25, 25), (cx - 17, ey - 4, 12, 7))
    pygame.draw.ellipse(surf, (25, 25, 25), (cx + 5,  ey - 4, 12, 7))
    pygame.draw.lines(surf, (55, 55, 55), False,
                      [(cx, ey + 12), (cx - 5, ey + 22), (cx + 5, ey + 22)], 1)
    pygame.draw.arc(surf, (55, 55, 55),
                    (cx - 11, ey + 26, 22, 10), math.pi, 0, 1)
    # neck + shoulders
    pygame.draw.rect(surf, (155, 155, 155),
                     (cx - 11, cy + 8 + fh // 2 + 6, 22, 18))
    pygame.draw.rect(surf, (70, 70, 70),
                     (cx - r + 12, cy + 8 + fh // 2 + 22, (r - 12) * 2, 12),
                     border_radius=3)


def draw_wedge(surf, cx, cy, w, h, angle_deg=0, n=14):
    ws = pygame.Surface((w * 3, h * 3), pygame.SRCALPHA)
    wc, hc = w * 3 // 2, h * 3 // 2
    for i in range(n):
        t   = i / (n - 1)
        col = (195, 195, 195) if i % 2 == 0 else (15, 15, 15)
        xt  = wc + int((t - 0.5) * w * 2)
        yt  = hc - h
        xb  = wc
        yb  = hc + h // 2
        pygame.draw.line(ws, col, (xt, yt), (xb, yb), 1)
    f = pygame.font.SysFont("monospace", 7)
    for lbl_txt, yf in [("100", 0.05), ("300", 0.5), ("500", 0.95)]:
        lbl = f.render(lbl_txt, True, (160, 100, 0))
        ws.blit(lbl, (4, int(hc - h + yf * h * 2)))
    rot = pygame.transform.rotate(ws, angle_deg)
    rx, ry = rot.get_size()
    surf.blit(rot, (cx - rx // 2, cy - ry // 2))


def draw_geometry_circle(surf, cx, cy, radii):
    for i, r in enumerate(radii):
        g = max(30, 155 - i * 35)
        pygame.draw.circle(surf, (g, g, g), (cx, cy), r, 2)
    outer = radii[0]
    pygame.draw.line(surf, (90, 90, 90), (cx - outer, cy), (cx + outer, cy), 1)
    pygame.draw.line(surf, (90, 90, 90), (cx, cy - outer), (cx, cy + outer), 1)
    for off in [-outer, -outer // 2, 0, outer // 2, outer]:
        pygame.draw.line(surf, (130, 130, 130),
                         (cx + off, cy - 4), (cx + off, cy + 4), 1)
        pygame.draw.line(surf, (130, 130, 130),
                         (cx - 4, cy + off), (cx + 4, cy + off), 1)


def draw_greyscale_ramp(surf, rect):
    for x in range(rect.width):
        v = int(8 + (228 - 8) * x / rect.width)
        pygame.draw.line(surf, (v, v, v),
                         (rect.x + x, rect.y),
                         (rect.x + x, rect.bottom))


def draw_sync_bar(surf, rect):
    pygame.draw.rect(surf, (6, 6, 6), rect)
    f   = pygame.font.SysFont("monospace", 9)
    lbl = f.render("SYNC  0 IRE  /  LINE BLANKING  /  625L 50Hz PAL", True, (55, 55, 55))
    surf.blit(lbl, (rect.x + 8, rect.centery - lbl.get_height() // 2))


def render_static_pattern(pat_w, pat_h, zones):
    s = pygame.Surface((pat_w, pat_h))
    s.fill(BLACK)
    draw_greyscale_strip(s, pygame.Rect(0, 0, pat_w, 72))
    draw_portrait(s, pat_w // 2, 158, 60)
    draw_wedge(s, 140, 295, 110, 115, angle_deg=0,   n=16)
    draw_wedge(s, 540, 295, 110, 115, angle_deg=0,   n=16)
    draw_wedge(s, 140, 490, 110, 100, angle_deg=90,  n=14)
    draw_wedge(s, 540, 490, 110, 100, angle_deg=-90, n=14)
    draw_geometry_circle(s, pat_w // 2, 400, [130, 100, 70, 40])
    draw_greyscale_ramp(s, pygame.Rect(0, 600, pat_w, 60))
    draw_sync_bar(s, pygame.Rect(0, 660, pat_w, 40))
    # Faint zone name labels
    f = pygame.font.SysFont("monospace", 8)
    for z in zones:
        lbl = f.render(z["name"], True, (55, 50, 40))
        s.blit(lbl, (z["rect"].x + 3, z["rect"].y + 3))
    return s


# ─────────────────────────────────────────────
#  DEGRADATION SURFACE
# ─────────────────────────────────────────────
def make_degrade_surf(zone, seed):
    r    = zone["rect"]
    w, h = r.width, r.height
    rng  = random.Random(seed)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    dt   = zone["active_degradation"]

    if dt == "noise":
        for _ in range(w * h // 3):
            px = rng.randint(0, w - 1)
            py = rng.randint(0, h - 1)
            v  = rng.randint(0, 255)
            a  = rng.randint(130, 220)
            surf.set_at((px, py), (v, v, v, a))
        veil = pygame.Surface((w, h), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 75))
        surf.blit(veil, (0, 0))

    elif dt == "lines":
        for y in range(0, h, 4):
            ls = pygame.Surface((w, 2), pygame.SRCALPHA)
            ls.fill((0, 0, 0, 195))
            surf.blit(ls, (0, y))
        for _ in range(3):
            y  = rng.randint(0, h - 1)
            ts = pygame.Surface((w, 1), pygame.SRCALPHA)
            ts.fill((255, 255, 255, 150))
            surf.blit(ts, (0, y))

    elif dt == "blur":
        veil = pygame.Surface((w, h), pygame.SRCALPHA)
        veil.fill((100, 100, 100, 105))
        surf.blit(veil, (0, 0))
        for x in range(0, w, 3):
            bs = pygame.Surface((2, h), pygame.SRCALPHA)
            bs.fill((140, 140, 140, rng.randint(20, 75)))
            surf.blit(bs, (x, 0))

    elif dt == "bright":
        veil = pygame.Surface((w, h), pygame.SRCALPHA)
        veil.fill((125, 125, 125, 145))
        surf.blit(veil, (0, 0))
        for _ in range(2):
            y  = rng.randint(0, h - 5)
            bs = pygame.Surface((w, rng.randint(2, 5)), pygame.SRCALPHA)
            bs.fill((235, 235, 235, 175))
            surf.blit(bs, (0, y))

    return surf


# ─────────────────────────────────────────────
#  BUTTON
# ─────────────────────────────────────────────
class Button:
    def __init__(self, rect, label, col_off, col_on):
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.col_off = col_off
        self.col_on  = col_on
        self.active  = False
        self._font   = None

    def draw(self, surf):
        if not self._font:
            self._font = pygame.font.SysFont("monospace", 13, bold=True)
        col = self.col_on if self.active else self.col_off
        pygame.draw.rect(surf, col, self.rect, border_radius=5)
        pygame.draw.rect(surf, WHITE, self.rect, 1, border_radius=5)
        lbl = self._font.render(self.label, True, WHITE)
        surf.blit(lbl, (self.rect.centerx - lbl.get_width() // 2,
                        self.rect.centery - lbl.get_height() // 2))

    def hit(self, pos):
        return self.rect.collidepoint(pos)


# ─────────────────────────────────────────────
#  APP
# ─────────────────────────────────────────────
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("TV Test Pattern — TSCG M0_TVTestPattern")
        self.clock  = pygame.time.Clock()

        # Fonts
        self.f_hdr   = pygame.font.SysFont("monospace", 18, bold=True)
        self.f_title = pygame.font.SysFont("monospace", 13, bold=True)
        self.f_body  = pygame.font.SysFont("monospace", 11)
        self.f_small = pygame.font.SysFont("monospace", 9)
        self.f_lbl   = pygame.font.SysFont("monospace", 10, bold=True)

        # Build zones
        self.zones = []
        for zd in ZONE_DEFS:
            z = dict(zd)
            z["degraded"]           = False
            z["active_degradation"] = None
            z["degrade_surf"]       = None
            self.zones.append(z)

        # Buttons
        bx = PAT_W + 18
        self.btn_fix     = Button((bx,       WIN_H - 108, 148, 38), "\u2692  FIX",     (35, 75, 35), (55, 175, 55))
        self.btn_degrade = Button((bx + 158, WIN_H - 108, 148, 38), "\u2620  DEGRADE", (75, 35, 35), (195, 48, 48))

        self.hovered = None
        self.pattern = render_static_pattern(PAT_W, PAT_H, self.zones)

    # ── DESCRIPTION PANEL ─────────────────────────────────────────────────
    def draw_desc_panel(self):
        s  = self.screen
        px = PAT_W + 1
        pygame.draw.rect(s, PANEL_BG, (px, 0, DESC_W, WIN_H))
        pygame.draw.line(s, BORDER_COLOR, (px, 0), (px, WIN_H), 2)

        # Decide what to show
        if self.hovered:
            z = self.hovered
            if z["degraded"]:
                dtype    = z["active_degradation"]
                diag_msg = next(
                    (d[1] for d in z["degradations"] if d[0] == dtype), "Unknown fault.")
                title = f"\u26a0  {z['name']}"
                body  = (
                    f"DIAGNOSTIC\n"
                    f"Fault type: {dtype.upper()}\n"
                    f"\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
                    f"{diag_msg}\n\n"
                    f"{z['desc']}"
                )
            else:
                title = z["name"]
                body  = z["desc"]
        else:
            title = ORIGIN_TITLE
            body  = ORIGIN_TEXT

        # Title
        title_s = self.f_hdr.render(title[:34], True, AMBER)
        s.blit(title_s, (px + 14, 18))
        pygame.draw.line(s, (55, 55, 68), (px + 14, 50), (WIN_W - 14, 50), 1)

        # Body
        draw_text_wrapped(s, body, self.f_body, TEXT_COLOR,
                          pygame.Rect(px + 14, 58, DESC_W - 28, WIN_H - 210), line_spacing=3)

        # ASFID tag + state
        if self.hovered:
            z = self.hovered
            # ASFID chip
            cr = pygame.Rect(px + 14, WIN_H - 148, DESC_W - 28, 26)
            pygame.draw.rect(s, (28, 38, 28), cr, border_radius=4)
            pygame.draw.rect(s, (55, 95, 55), cr, 1, border_radius=4)
            asfid_lbl = self.f_lbl.render(f"ASFID:  {z['asfid']}", True, (110, 215, 110))
            s.blit(asfid_lbl, (cr.x + 8, cr.centery - asfid_lbl.get_height() // 2))

            # State chip
            sr = pygame.Rect(px + 14, WIN_H - 116, DESC_W - 28, 24)
            if z["degraded"]:
                pygame.draw.rect(s, (40, 18, 18), sr, border_radius=4)
                pygame.draw.rect(s, (165, 45, 45), sr, 1, border_radius=4)
                st_lbl = self.f_lbl.render(
                    f"\u26a0 DEGRADED: {z['active_degradation'].upper()}", True, (215, 70, 70))
            else:
                pygame.draw.rect(s, (18, 38, 18), sr, border_radius=4)
                pygame.draw.rect(s, (45, 155, 45), sr, 1, border_radius=4)
                st_lbl = self.f_lbl.render("\u2713  CALIBRATED", True, (70, 215, 70))
            s.blit(st_lbl, (sr.x + 8, sr.centery - st_lbl.get_height() // 2))

        # Mode line
        if self.btn_fix.active:
            mode_col = GREEN_DIM
            mode_txt = "MODE: FIX \u2014 click a degraded zone to repair"
        elif self.btn_degrade.active:
            mode_col = RED_DIM
            mode_txt = "MODE: DEGRADE \u2014 click any zone to add fault"
        else:
            mode_col = GREY_DIM
            mode_txt = "MODE: INSPECT \u2014 hover zones to analyse"
        ml = self.f_lbl.render(mode_txt, True, mode_col)
        s.blit(ml, (px + 14, WIN_H - 56))

        # Buttons
        self.btn_fix.draw(s)
        self.btn_degrade.draw(s)

    # ── HIGHLIGHT ─────────────────────────────────────────────────────────
    def draw_highlight(self, zone):
        r  = zone["rect"]
        hl = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        hl.fill((255, 140, 0, 38))
        self.screen.blit(hl, r.topleft)
        pygame.draw.rect(self.screen, ORANGE, r, 2)

    # ── MAIN LOOP ─────────────────────────────────────────────────────────
    def run(self):
        while True:
            mx, my = pygame.mouse.get_pos()

            # Detect hover (only in pattern area)
            self.hovered = None
            if mx < PAT_W:
                for z in self.zones:
                    if z["rect"].collidepoint(mx, my):
                        self.hovered = z
                        break

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_fix.hit((mx, my)):
                        self.btn_fix.active = not self.btn_fix.active
                        if self.btn_fix.active:
                            self.btn_degrade.active = False
                        continue

                    if self.btn_degrade.hit((mx, my)):
                        self.btn_degrade.active = not self.btn_degrade.active
                        if self.btn_degrade.active:
                            self.btn_fix.active = False
                        continue

                    if mx < PAT_W and self.hovered:
                        z = self.hovered
                        if self.btn_fix.active and z["degraded"]:
                            z["degraded"]           = False
                            z["active_degradation"] = None
                            z["degrade_surf"]       = None
                        elif self.btn_degrade.active:
                            dtype = random.choice([d[0] for d in z["degradations"]])
                            z["active_degradation"] = dtype
                            z["degraded"]           = True
                            z["degrade_surf"]       = make_degrade_surf(
                                z, seed=random.randint(0, 99999))

            # Draw
            self.screen.fill(BG_COLOR)
            self.screen.blit(self.pattern, (0, 0))

            for z in self.zones:
                if z["degraded"] and z["degrade_surf"]:
                    self.screen.blit(z["degrade_surf"], z["rect"].topleft)

            if self.hovered:
                self.draw_highlight(self.hovered)

            self.draw_desc_panel()
            pygame.draw.line(self.screen, BORDER_COLOR, (PAT_W, 0), (PAT_W, WIN_H), 2)

            pygame.display.flip()
            self.clock.tick(FPS)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    App().run()
