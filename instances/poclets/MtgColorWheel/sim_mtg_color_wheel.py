"""
MTG Color Wheel — Interactive Pygame Simulation
================================================
TSCG Poclet: Magic: The Gathering Color Wheel
Author: Echopraxium with the collaboration of Claude AI
Version: 1.1.0
Date: 2026-02-26

Controls:
  - Hover a color node  : show full color profile in the side panel
  - Click a color node  : toggle "selected" state (highlights allies/enemies)
  - Click background    : deselect
  - Press [A]           : toggle ally edges visibility
  - Press [E]           : toggle enemy edges visibility
  - Press [L]           : toggle labels
  - Press [ESC] / [Q]   : quit
"""

import pygame
import math
import sys

# ---------------------------------------------------------------------------
# Constants & Palette
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1200, 750
FPS = 60

BG_COLOR      = (18, 18, 28)       # Dark slate background
PANEL_COLOR   = (28, 28, 44)       # Side panel
PANEL_BORDER  = (60, 60, 90)
WHITE_COLOR   = (240, 230, 200)    # Readable white text

# Pentagon angles (clockwise from top):  W=90°, U=18°, B=306°, R=234°, G=162°
# Note: in pygame y-axis is inverted, so we negate sin
COLORS_DATA = [
    {
        "id":         "White",
        "symbol":     "W",
        "angle":      90,
        "fill":       (245, 238, 210),
        "border":     (200, 190, 150),
        "text_color": (40, 30, 20),
        "keyword":    "ORDER",
        "subtitle":   "Laws of Man / Community",
        "philosophy": "The many are stronger than the one.\nOrder brings peace, law brings justice.\nIndividual desires yield to common good.",
        "values":     ["Structure", "Peace", "Community", "Absolute Morality"],
        "methods":    ["Laws", "Institutions", "Collective Work", "Discipline"],
        "strengths":  ["Exile / Removal", "Life Gain", "Board Wipes", "Protection"],
        "weaknesses": ["Rigid Conformism", "Lacks Card Draw", "Sacrifices Individual"],
        "lacks":      ["Flexibility", "Individuality", "Spontaneity"],
        "symbol_art": "☀",
        "allies":     ["Blue", "Green"],
        "enemies":    ["Black", "Red"],
    },
    {
        "id":         "Blue",
        "symbol":     "U",
        "angle":      18,
        "fill":       (50, 100, 200),
        "border":     (30, 70, 160),
        "text_color": (220, 230, 255),
        "keyword":    "KNOWLEDGE",
        "subtitle":   "Logic / Technology / Omniscience",
        "philosophy": "Everything can be improved.\nKnowledge is power. Through understanding\nwe transcend our limits.",
        "values":     ["Knowledge", "Perfection", "Progress", "Intellect"],
        "methods":    ["Study", "Technology", "Magic", "Manipulation"],
        "strengths":  ["Counterspells", "Card Draw", "Flying", "Illusions", "Control"],
        "weaknesses": ["Analytical Coldness", "Unethical Manipulation", "Perfectionism"],
        "lacks":      ["Intuition", "Tradition", "Acceptance of Imperfection"],
        "symbol_art": "◈",
        "allies":     ["White", "Black"],
        "enemies":    ["Red", "Green"],
    },
    {
        "id":         "Black",
        "symbol":     "B",
        "angle":      306,
        "fill":       (35, 25, 35),
        "border":     (120, 80, 130),
        "text_color": (200, 160, 220),
        "keyword":    "AMBITION",
        "subtitle":   "Selfishness / Amorality / Parasitism",
        "philosophy": "Every being has the right to do whatever it\ntakes to survive and thrive.\nMorality is a luxury of the weak.",
        "values":     ["Power", "Personal Achievement", "Pragmatism"],
        "methods":    ["Power at Any Cost", "Resource Exploitation", "Death as Resource"],
        "strengths":  ["Targeted Removal", "Hand Disruption", "Reanimation", "Sacrifice"],
        "weaknesses": ["Pathological Egoism", "Destructive Cynicism", "Parasitism"],
        "lacks":      ["Altruism", "Scruples", "Community Sense"],
        "symbol_art": "☽",
        "allies":     ["Blue", "Red"],
        "enemies":    ["White", "Green"],
    },
    {
        "id":         "Red",
        "symbol":     "R",
        "angle":      234,
        "fill":       (200, 45, 45),
        "border":     (240, 80, 60),
        "text_color": (255, 220, 190),
        "keyword":    "FREEDOM",
        "subtitle":   "Impulse / Chaos / Emotion",
        "philosophy": "Feel, don't think. Act now, worry later.\nFreedom is worth any price.\nLive in the moment.",
        "values":     ["Freedom", "Emotion", "Spontaneity", "Action"],
        "methods":    ["Intuition", "Passion", "Creative Destruction", "Art"],
        "strengths":  ["Direct Damage (Burn)", "Haste", "Aggro Creatures", "Chaos"],
        "weaknesses": ["Self-destructive Chaos", "Impulsivity", "Cards have Drawbacks"],
        "lacks":      ["Discipline", "Planning", "Restraint"],
        "symbol_art": "⚡",
        "allies":     ["Black", "Green"],
        "enemies":    ["White", "Blue"],
    },
    {
        "id":         "Green",
        "symbol":     "G",
        "angle":      162,
        "fill":       (30, 110, 40),
        "border":     (60, 170, 70),
        "text_color": (190, 240, 190),
        "keyword":    "NATURE",
        "subtitle":   "Instinct / Interdependence / Growth",
        "philosophy": "Everything has its place in the natural order.\nRespect tradition and the web of life.\nGrowth through time, not force.",
        "values":     ["Nature", "Tradition", "Organic Growth", "Destiny"],
        "methods":    ["Adaptation", "Ecosystem Reliance", "Acceptance"],
        "strengths":  ["Large Creatures", "Mana Ramp", "Enchantments", "Buffs"],
        "weaknesses": ["Fatalism", "Rejects Progress", "Law of the Jungle"],
        "lacks":      ["Innovation", "Will to Change Destiny", "Individualism"],
        "symbol_art": "🌿",
        "allies":     ["Red", "White"],
        "enemies":    ["Blue", "Black"],
    },
]

ALLY_COLOR    = (100, 220, 130, 160)   # Soft green, semi-transparent
ENEMY_COLOR   = (220, 70, 70, 160)     # Soft red, semi-transparent
NODE_RADIUS   = 52
RING_RADIUS   = 210                    # Pentagon circumradius

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def angle_to_vec(deg, radius, cx, cy):
    """Convert polar angle (math convention, 0=right, CCW) to screen coords."""
    rad = math.radians(deg)
    # Pygame: y-axis points down → negate sin
    x = cx + radius * math.cos(rad)
    y = cy - radius * math.sin(rad)
    return (int(x), int(y))


def draw_aa_circle(surf, color, center, radius, width=0):
    pygame.draw.circle(surf, color, center, radius, width)


def blend_alpha_surface(surf, color_rgba, rect):
    """Draw a semi-transparent filled rect."""
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill(color_rgba)
    surf.blit(s, rect.topleft)


def draw_thick_aa_line(surf, color, p1, p2, width=3):
    pygame.draw.line(surf, color, p1, p2, width)


def find_color_by_id(color_id):
    for c in COLORS_DATA:
        if c["id"] == color_id:
            return c
    return None


def wrap_text(text, font, max_width):
    """Split text into lines fitting max_width."""
    lines = []
    for raw_line in text.split("\n"):
        words = raw_line.split()
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        lines.append(current)
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MTG Color Wheel — TSCG Poclet (v1.1.0)")
    clock = pygame.time.Clock()

    # Fonts
    font_title  = pygame.font.SysFont("segoeuisymbol", 22, bold=True)
    font_sub    = pygame.font.SysFont("segoeuisymbol", 15)
    font_small  = pygame.font.SysFont("segoeuisymbol", 13)
    font_symbol = pygame.font.SysFont("segoeuisymbol", 38, bold=True)
    font_key    = pygame.font.SysFont("segoeuisymbol", 17, bold=True)

    # Layout
    WHEEL_CX = 400
    WHEEL_CY = 375
    PANEL_X  = 810
    PANEL_W  = WIDTH - PANEL_X - 10
    PANEL_H  = HEIGHT - 20

    # Compute node positions
    node_positions = {}
    for cd in COLORS_DATA:
        pos = angle_to_vec(cd["angle"], RING_RADIUS, WHEEL_CX, WHEEL_CY)
        node_positions[cd["id"]] = pos

    # State
    hovered    = None
    selected   = None
    show_allies  = True
    show_enemies = True
    show_labels  = True

    # Glow animation counter
    tick = 0

    running = True
    while running:
        clock.tick(FPS)
        tick += 1
        mx, my = pygame.mouse.get_pos()

        # ------------------------------------------------------------------
        # Events
        # ------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_a:
                    show_allies = not show_allies
                elif event.key == pygame.K_e:
                    show_enemies = not show_enemies
                elif event.key == pygame.K_l:
                    show_labels = not show_labels
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = None
                for cd in COLORS_DATA:
                    pos = node_positions[cd["id"]]
                    dist = math.hypot(mx - pos[0], my - pos[1])
                    if dist <= NODE_RADIUS:
                        clicked = cd["id"]
                        break
                if clicked:
                    selected = None if selected == clicked else clicked
                else:
                    selected = None

        # Detect hover
        hovered = None
        for cd in COLORS_DATA:
            pos = node_positions[cd["id"]]
            dist = math.hypot(mx - pos[0], my - pos[1])
            if dist <= NODE_RADIUS:
                hovered = cd["id"]
                break

        # ------------------------------------------------------------------
        # Draw
        # ------------------------------------------------------------------
        screen.fill(BG_COLOR)

        # ---- Pentagon background glow ----
        for i, cd in enumerate(COLORS_DATA):
            p = node_positions[cd["id"]]
            pulse = int(30 + 15 * math.sin(tick * 0.03 + i * 1.2566))
            s = pygame.Surface((NODE_RADIUS * 4, NODE_RADIUS * 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*cd["fill"][:3], pulse),
                               (NODE_RADIUS * 2, NODE_RADIUS * 2), NODE_RADIUS * 2)
            screen.blit(s, (p[0] - NODE_RADIUS * 2, p[1] - NODE_RADIUS * 2))

        # ---- Pentagon outline ----
        pts = [node_positions[cd["id"]] for cd in COLORS_DATA]
        pygame.draw.polygon(screen, (70, 70, 90), pts, 1)

        # ---- Relationship edges ----
        active_color = selected or hovered

        def edge_alpha(c1_id, c2_id, rel_type):
            """Return alpha for an edge given current selection."""
            if active_color is None:
                return 180
            cd = find_color_by_id(active_color)
            if rel_type == "ally" and c2_id in cd["allies"] or c1_id in cd["allies"] and c2_id == active_color:
                return 240
            if rel_type == "enemy" and c2_id in cd["enemies"] or c1_id in cd["enemies"] and c2_id == active_color:
                return 240
            return 40

        # Draw ENEMY edges (pentagram diagonals) first (behind)
        if show_enemies:
            enemy_pairs_drawn = set()
            for cd in COLORS_DATA:
                for en in cd["enemies"]:
                    pair_key = tuple(sorted([cd["id"], en]))
                    if pair_key in enemy_pairs_drawn:
                        continue
                    enemy_pairs_drawn.add(pair_key)
                    p1 = node_positions[cd["id"]]
                    p2 = node_positions[en]
                    alpha = edge_alpha(cd["id"], en, "enemy")
                    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.line(s, (220, 60, 60, alpha), p1, p2, 2)
                    screen.blit(s, (0, 0))

        # Draw ALLY edges (pentagon sides)
        if show_allies:
            ally_pairs_drawn = set()
            for cd in COLORS_DATA:
                for al in cd["allies"]:
                    pair_key = tuple(sorted([cd["id"], al]))
                    if pair_key in ally_pairs_drawn:
                        continue
                    ally_pairs_drawn.add(pair_key)
                    p1 = node_positions[cd["id"]]
                    p2 = node_positions[al]
                    alpha = edge_alpha(cd["id"], al, "ally")
                    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.line(s, (80, 220, 120, alpha), p1, p2, 3)
                    screen.blit(s, (0, 0))

        # ---- Color Nodes ----
        for cd in COLORS_DATA:
            pos = node_positions[cd["id"]]
            is_hov = hovered == cd["id"]
            is_sel = selected == cd["id"]

            # Determine dimming
            if active_color and not is_hov and not is_sel:
                act_cd = find_color_by_id(active_color)
                if cd["id"] not in act_cd["allies"] and cd["id"] not in act_cd["enemies"]:
                    alpha = 90
                else:
                    alpha = 200
            else:
                alpha = 255

            # Outer ring (border)
            ring_w = 4 if (is_hov or is_sel) else 2
            ring_color = cd["border"]
            if is_sel:
                pulse_ring = int(200 + 55 * math.sin(tick * 0.08))
                ring_color = (min(255, cd["border"][0] + 60),
                              min(255, cd["border"][1] + 60),
                              min(255, cd["border"][2] + 60))
                ring_w = 5

            # Draw node
            node_surf = pygame.Surface((NODE_RADIUS * 2 + 10, NODE_RADIUS * 2 + 10), pygame.SRCALPHA)
            nc = NODE_RADIUS + 5
            pygame.draw.circle(node_surf, (*cd["fill"], alpha), (nc, nc), NODE_RADIUS)
            pygame.draw.circle(node_surf, (*ring_color, min(255, alpha + 20)), (nc, nc), NODE_RADIUS, ring_w)
            screen.blit(node_surf, (pos[0] - nc, pos[1] - nc))

            # Symbol inside node
            sym_surf = font_symbol.render(cd["symbol"], True, (*cd["text_color"], alpha))
            screen.blit(sym_surf, (pos[0] - sym_surf.get_width() // 2,
                                   pos[1] - sym_surf.get_height() // 2))

            # Label below node
            if show_labels:
                lbl = font_key.render(cd["id"].upper(), True,
                                      (min(255, cd["fill"][0] + 80),
                                       min(255, cd["fill"][1] + 80),
                                       min(255, cd["fill"][2] + 80)))
                kw  = font_small.render(cd["keyword"], True, WHITE_COLOR)
                # Position label away from center
                dx = pos[0] - WHEEL_CX
                dy = pos[1] - WHEEL_CY
                dist_c = math.hypot(dx, dy) or 1
                lbl_x = pos[0] + int(dx / dist_c * (NODE_RADIUS + 14)) - lbl.get_width() // 2
                lbl_y = pos[1] + int(dy / dist_c * (NODE_RADIUS + 14)) - lbl.get_height() // 2
                screen.blit(lbl, (lbl_x, lbl_y))

        # ---- Center label ----
        title_surf = font_title.render("Color Wheel", True, (180, 160, 220))
        sub_surf   = font_small.render("Magic: The Gathering", True, (120, 110, 160))
        screen.blit(title_surf, (WHEEL_CX - title_surf.get_width() // 2, WHEEL_CY - 16))
        screen.blit(sub_surf,   (WHEEL_CX - sub_surf.get_width() // 2,   WHEEL_CY + 8))

        # ---- Side Panel ----
        panel_rect = pygame.Rect(PANEL_X, 10, PANEL_W, PANEL_H)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=8)
        pygame.draw.rect(screen, PANEL_BORDER, panel_rect, 1, border_radius=8)

        display_cd = find_color_by_id(hovered or selected)

        px = PANEL_X + 14
        py = 20

        if display_cd is None:
            # Instructions
            lines = [
                ("MTG Color Wheel", font_title, (180, 160, 220)),
                ("TSCG Poclet v1.1.0", font_small, (120, 110, 160)),
                ("", None, None),
                ("HOVER a color to inspect", font_sub, WHITE_COLOR),
                ("CLICK to select / deselect", font_sub, WHITE_COLOR),
                ("", None, None),
                ("[A] Toggle ally edges", font_small, (80, 220, 120)),
                ("[E] Toggle enemy edges", font_small, (220, 80, 80)),
                ("[L] Toggle labels", font_small, (180, 180, 220)),
                ("[ESC/Q] Quit", font_small, (160, 130, 130)),
                ("", None, None),
                ("━━━━━━━━━━━━━━━━━━━━", font_small, (70, 70, 90)),
                ("Pentagon order (CW):", font_small, (160, 160, 200)),
                ("W → U → B → R → G", font_sub, (200, 200, 160)),
                ("", None, None),
                ("— Adjacent = ALLIES", font_small, (80, 220, 120)),
                ("— Diagonal = ENEMIES", font_small, (220, 80, 80)),
            ]
            for text, font, color in lines:
                if font is None:
                    py += 8
                    continue
                s = font.render(text, True, color)
                screen.blit(s, (px, py))
                py += s.get_height() + 4
        else:
            cd = display_cd
            # Header strip
            header_rect = pygame.Rect(PANEL_X + 4, 10 + 4, PANEL_W - 8, 60)
            header_surf = pygame.Surface((header_rect.width, header_rect.height), pygame.SRCALPHA)
            header_surf.fill((*cd["fill"], 120))
            screen.blit(header_surf, header_rect.topleft)

            # Color name
            name_surf = font_title.render(cd["id"].upper(), True, cd["text_color"])
            kw_surf   = font_key.render(cd["keyword"], True, cd["text_color"])
            sub_t     = font_small.render(cd["subtitle"], True, cd["text_color"])
            screen.blit(name_surf, (px, py))
            screen.blit(kw_surf,   (px + name_surf.get_width() + 10, py + 4))
            py += name_surf.get_height() + 2
            screen.blit(sub_t, (px, py))
            py += sub_t.get_height() + 10

            def section(title, items, color, bullet="•"):
                nonlocal py
                t = font_key.render(title, True, color)
                screen.blit(t, (px, py))
                py += t.get_height() + 2
                for item in items:
                    item_surf = font_small.render(f"  {bullet} {item}", True, WHITE_COLOR)
                    screen.blit(item_surf, (px, py))
                    py += item_surf.get_height() + 2
                py += 4

            def para(title, text, title_color):
                nonlocal py
                t = font_key.render(title, True, title_color)
                screen.blit(t, (px, py))
                py += t.get_height() + 2
                for line in wrap_text(text, font_small, PANEL_W - 28):
                    s = font_small.render(line, True, (190, 190, 210))
                    screen.blit(s, (px + 6, py))
                    py += s.get_height() + 2
                py += 4

            para("Philosophy", cd["philosophy"], (200, 180, 240))
            section("Strengths", cd["strengths"],   (80, 220, 120), "✦")
            section("Weaknesses", cd["weaknesses"], (220, 100, 80), "✧")

            # Allies
            ally_str = "  " + "  |  ".join(cd["allies"])
            t = font_key.render("Allies:", True, (80, 220, 120))
            screen.blit(t, (px, py))
            v = font_small.render(ally_str, True, (130, 230, 150))
            screen.blit(v, (px + t.get_width() + 6, py + 3))
            py += t.get_height() + 6

            # Enemies
            en_str = "  " + "  |  ".join(cd["enemies"])
            t = font_key.render("Enemies:", True, (220, 80, 80))
            screen.blit(t, (px, py))
            v = font_small.render(en_str, True, (240, 130, 130))
            screen.blit(v, (px + t.get_width() + 6, py + 3))
            py += t.get_height() + 6

            section("Lacks", cd["lacks"], (180, 160, 100), "○")

        # ---- Controls bar at bottom of wheel area ----
        controls = "[A] Allies  [E] Enemies  [L] Labels  [Q] Quit"
        ctrl_surf = font_small.render(controls, True, (80, 80, 110))
        screen.blit(ctrl_surf, (10, HEIGHT - 22))

        # ---- Legend ----
        legend_x, legend_y = 10, HEIGHT - 46
        pygame.draw.line(screen, (80, 220, 120), (legend_x, legend_y),
                         (legend_x + 30, legend_y), 3)
        screen.blit(font_small.render("Allied", True, (80, 220, 120)),
                    (legend_x + 34, legend_y - 7))
        pygame.draw.line(screen, (220, 70, 70), (legend_x + 110, legend_y),
                         (legend_x + 140, legend_y), 2)
        screen.blit(font_small.render("Enemy", True, (220, 70, 70)),
                    (legend_x + 144, legend_y - 7))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
