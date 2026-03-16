# tscg_explorer.py — Simulation README

**Version**: 2.1.0  
**Date**: 2026-03-01  
**Authors**: Echopraxium with the collaboration of Claude AI  
**Type**: TscgTool — interactive corpus visualiser  
**Ontology**: `M0_TscgExplorer.jsonld`

---

## Executive Summary

`tscg_explorer.py` is a **self-referential visualisation tool**: a Python/pygame desktop application that renders the **81 M2 GenericConcepts** of the TSCG framework as an interactive 2D concept net. It is the first artefact of type `m3:TscgTool` — a software tool operating reflexively on TSCG framework artefacts rather than modelling an external domain.

The tool provides three complementary 2D projections of the underlying 10-dimensional ASFID⊗REVOI tensor space, allowing an analyst to navigate the concept corpus, inspect individual concepts, and reveal structural patterns (density zones, gaps, IS-A chains, Combo assemblies).

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [Installation & Launch](#2-installation--launch)
3. [UI Layout](#3-ui-layout)
4. [Controls Reference](#4-controls-reference)
5. [Projection Modes](#5-projection-modes)
6. [Node Encoding](#6-node-encoding)
7. [Edge Encoding](#7-edge-encoding)
8. [Concept Profile Panel](#8-concept-profile-panel)
9. [Formula Tile Display](#9-formula-tile-display)
10. [Tree Explorer Panel](#10-tree-explorer-panel)
11. [Concept Statistics](#11-concept-statistics)
12. [Architecture Notes](#12-architecture-notes)

---

## 1. Requirements

| Dependency | Version | Notes |
|------------|---------|-------|
| Python | ≥ 3.9 | Standard library only (+ pygame) |
| pygame | ≥ 2.0 | `pip install pygame` |

No other external dependency. The concept data is embedded directly in the script as Python structures mirroring the `M2_GenericConcepts.jsonld` ontology.

---

## 2. Installation & Launch

```bash
# Install pygame if not already present
pip install pygame

# Run the tool
python tscg_explorer.py
```

The window opens at **1280 × 760** pixels (laptop-optimised). All three panels are immediately visible and interactive.

---

## 3. UI Layout

The window is divided into three vertical panels separated by two draggable vertical splitters:

```
┌──────────────┬─────────────────────────────┬──────────────────────────┐
│              │                             │                          │
│  LEFT PANEL  │      CENTER PANEL           │      RIGHT PANEL         │
│  Tree        │      Concept Net            │      Concept Profile     │
│  Explorer    │      (2D projection)        │                          │
│  IS-A tree   │                             │ ─── splitter ────────── │
│  collapsible │      [A] [B] [C]            │                          │
│  families    │      mode buttons           │      README              │
│              │                             │      (scrollable)        │
│  230 px      │      560 px                 │      490 px              │
│  (default)   │      (default)              │      (default)           │
└──────────────┴─────────────────────────────┴──────────────────────────┘
│                        Status bar                                      │
└────────────────────────────────────────────────────────────────────────┘
```

**All panel widths are adjustable** by dragging the two vertical splitters.  
**The right panel** is itself split by a horizontal splitter into Profile (top) and README (bottom).

### Panel Summary

| Panel | Content | Key interactions |
|-------|---------|-----------------|
| Left | IS-A Tree | Click family header to expand/collapse · Click concept row to select · Scroll wheel to scroll |
| Center | 2D concept net | Click node to select · Drag to pan · Scroll wheel to zoom · Click [A][B][C] or press A/B/C to switch mode |
| Right (top) | Concept Profile | Scroll wheel to scroll profile content |
| Right (bottom) | README | Scroll wheel to scroll README |

---

## 4. Controls Reference

| Action | Method |
|--------|--------|
| **Switch projection mode** | Click `[A]` `[B]` `[C]` buttons, or press `A` / `B` / `C` on keyboard |
| **Select concept** | Click a node in the net · Click a row in the tree |
| **Pan concept net** | Click and drag anywhere on the net (not on a button) |
| **Zoom concept net** | Mouse wheel over the net (zoom centred on cursor) |
| **Resize left panel** | Drag the left vertical splitter bar |
| **Resize right panel** | Drag the right vertical splitter bar |
| **Resize Profile/README** | Drag the horizontal splitter bar inside the right panel |
| **Scroll tree** | Mouse wheel over the left panel |
| **Scroll profile** | Mouse wheel over the profile zone |
| **Scroll README** | Mouse wheel over the README zone |
| **Expand/collapse family** | Click the family header row in the tree |
| **Expand/collapse IS-A node** | Click the ▸/▾ arrow on a node that has children |
| **Quit** | Press `ESC` or close the window |

**Zoom range**: 0.2× – 4.0×. Node labels appear at zoom > 0.65 or when the node is selected / hovered.

---

## 5. Projection Modes

Each mode projects the 10-dimensional ASFID⊗REVOI tensor space onto a 2D plane, revealing different structural properties of the corpus.

### Mode A — ASFID ratio × Dimensionality *(default)*

```
X axis  =  ASFID_count / total_dims   ∈ [0.0, 1.0]
            0.0 = pure REVOI (Sphinx Eye / Map)
            1.0 = pure ASFID (Eagle Eye / Territory)

Y axis  =  total tensor dimensions     ∈ [1, 8]
            bottom = simple (1D)
            top    = complex (8D)
```

**What it reveals**:
- Left cluster → Map-dominant concepts (Representability, Evolvability…)
- Right cluster → Territory-dominant concepts (Attractors, Flows, Dynamics…)
- Height → semantic richness (number of M3 dimensions engaged)
- Density zones indicate where the corpus has strong coverage

### Mode B — Family × Dimensionality

```
X axis  =  family index (ordinal, 0–9)
            Structural · Dynamic · Informational · Ontological · Regulatory
            Relational · Adaptive · Energetic · Teleonomic · Combo

Y axis  =  total tensor dimensions     ∈ [1, 8]
```

**What it reveals**:
- Within-family dimensional spread (Y range per column)
- Cross-family comparison: which families have simple vs complex concepts
- Combo column is wide — assemblies span the full dimensional range

### Mode C — ASFID count × REVOI count

```
X axis  =  number of ASFID dimensions in tensor formula  ∈ [0, 5]
Y axis  =  number of REVOI dimensions in tensor formula  ∈ [0, 5]
```

**What it reveals**:
- Pure bicephalous decomposition — most direct map of Territory vs Map
- Concepts on X-axis only: pure Territory
- Concepts on Y-axis only: pure Map
- Concepts on the diagonal: balanced bicephalous signature
- The abstract `GenericConceptCombo` sits at origin (0 ASFID, 0 REVOI)

---

## 6. Node Encoding

### Shape

| Shape | Meaning | Count |
|-------|---------|-------|
| ▲ **Triangle** | Atomic GenericConcept | 73 |
| ◆ **Diamond** | GenericConceptCombo (n-ary tensor assembly) | 8 |

The abstract `GenericConceptCombo` node is rendered darker than other Combos.

### Colour — by Family

| Family | Colour | Count |
|--------|--------|-------|
| Structural | Blue | 21 |
| Dynamic | Orange | 15 |
| Informational | Green | 8 |
| Ontological | Purple | 9 |
| Regulatory | Red | 8 |
| Relational | Teal | 5 |
| Adaptive | Yellow | 4 |
| Energetic | Deep orange | 2 |
| Teleonomic | Sky blue | 1 |
| Combo | Grey-white | 8 |

The colour legend is displayed **in the top-left corner of the concept net**, alongside edge type examples (solid IS-A / dashed Combo).

### Size

Node radius scales linearly with the concept's total tensor dimensionality (number of M3 dimensions in its formula). A 1D concept has radius ~6, an 8D concept has radius ~15 (at zoom=1).

---

## 7. Edge Encoding

| Edge type | Style | Colour | Meaning |
|-----------|-------|--------|---------|
| **IS-A** | Solid line | Blue | `rdfs:subClassOf` relationship |
| **Combo component** | Dashed line | Orange | Concept is a component of a GenericConceptCombo |

IS-A edges:
- `Bifurcation` → `Duplication`
- `Oscillator` → `GenericConceptCombo` *(Oscillator is a Combo, not a sub-Duplication)*
- All Combo nodes → `GenericConceptCombo` (abstract root)

Combo ⊗⇒ edges connect each `GenericConceptCombo` to its component concepts:

| Combo | Components |
|-------|-----------|
| Cascade | Process ⊗ Step ⊗ Trajectory |
| Oscillator | Component ⊗ Process ⊗ Trajectory |
| Propagation | Cascade ⊗ Duplication ⊗ Network |
| Narration | Transformation ⊗ Representation ⊗ Relation |
| FeedbackLoop | Process ⊗ Alignment ⊗ Homeostasis |
| Processor | Component ⊗ Process ⊗ Signal |
| ButterflyEffect | Cascade ⊗ Amplification |
| LALI | Activation ⊗ Regulation ⊗ Threshold |

---

## 8. Concept Profile Panel

Clicking a node or a tree row opens its **Concept Profile** in the top zone of the right panel. The profile is scrollable. It displays:

| Section | Content |
|---------|---------|
| **Name** | Concept name with family colour dot |
| **Family / Type / Abstract** | Family name, shape type (▲/◆), abstract flag |
| **Formula** | Tensor tiles (see §9) + text form `A ⊗ S ⊗ I …` |
| **Dimensions** | Total count, ASFID count, REVOI count, ASFID ratio |
| **IS-A** | Superclass name (if any), colour-coded by its family |
| **Assembly** | For Combos: list of component concepts, colour-coded |
| **Subclasses** | Concepts that declare this one as their superclass |
| **Used in Combos** | Combos in which this concept appears as a component |
| **ConceptContracts** | Heuristic badges: Observable · Triggerable · Composable · Stateful |

**ConceptContract heuristics**:

| Contract | Condition |
|----------|-----------|
| Observable | At least 1 ASFID dimension present |
| Triggerable | A (Attractor) or D (Dynamics) in formula |
| Composable | S (Structure) or Im (Interoperability) in formula |
| Stateful | I (Information) or It in formula |

---

## 9. Formula Tile Display

Tensor formulas are rendered as a sequence of **coloured tiles** separated by **⊗ operators drawn as circles with a cross** (not a Unicode glyph — rendered via `pygame.draw.circle` + two `pygame.draw.line` calls for portability).

### ASFID Tile Colours (warm palette)

| Dimension | Colour | Meaning |
|-----------|--------|---------|
| **A** | Red-orange | Attractor — stable states, goals |
| **S** | Blue | Structure — topology, architecture |
| **F** | Cyan | Flow — flux, transfer |
| **I** | Green | Information — content, signal, state |
| **D** | Amber | Dynamics — temporal evolution |

### REVOI Tile Colours (cool palette)

| Dimension | Colour | Meaning |
|-----------|--------|---------|
| **R** | Purple | Representability — semantic encodability *(NOT Reproducibility)* |
| **E** | Magenta | Evolvability — model adaptability |
| **V** | Mauve | Verifiability — testability |
| **O** | Teal | Observability — measurability |
| **Im** | Lavender | Interoperability — subsystem compatibility |

**Example — `Network` (S ⊗ I ⊗ F ⊗ D ⊗ Im)**:

```
[S:blue] ⊗ [I:green] ⊗ [F:cyan] ⊗ [D:amber] ⊗ [Im:lavender]
```

The text form `S ⊗ I ⊗ F ⊗ D ⊗ Im` is shown below the tiles as a text fallback.

---

## 10. Tree Explorer Panel

The left panel displays all 81 concepts organised as a collapsible IS-A tree grouped by family.

### Tree Structure

```
▾ Structural (21)        ← family header (click to collapse)
    ▲ Channel            ← atomic concept (no children)
    ▲ Cluster
    ▲ Component
    ▾ Duplication        ← concept with IS-A children (click ▸ to collapse)
        ▲ Bifurcation    ← IS-A child (depth 2)
    ▲ ...
▾ Combo (8)
    ◆ ButterflyEffect    ← Combo concepts are always flat (depth 1)
    ◆ Cascade
    ◆ GenericConceptCombo
    ◆ Oscillator
    ...
```

**Important**: Combo family concepts are displayed **flat** (all at depth 1) even when they declare a superclass (e.g. `Oscillator IS-A GenericConceptCombo`). The IS-A relationships between Combos are visible as edges in the concept net. This avoids misleadingly nesting Combos under a concept from a different family.

### Row Appearance

| Element | Meaning |
|---------|---------|
| Coloured dot (family header) | Family colour |
| ▲ / ◆ icon | Atomic vs Combo |
| Bold yellow name | Currently selected concept |
| Blue highlight | Selected row |
| Dark hover | Mouse-over |
| ▸ / ▾ | Expand/collapse available |

---

## 11. Concept Statistics

| Metric | Value |
|--------|-------|
| Total GenericConcepts | 81 |
| Atomic (triangles ▲) | 73 |
| GenericConceptCombos (diamonds ◆) | 8 (incl. 1 abstract) |
| Families | 10 |
| IS-A edges | 10 |
| Combo ⊗⇒ edges | 22 (sum of all component counts) |
| Max dimensionality | 8D (Narration, FeedbackLoop) |
| Min dimensionality | 1D (Convergence, Gradient, Imbrication, State, Symmetry) |
| ASFID-only concepts | ~12 |
| Mixed ASFID+REVOI concepts | ~62 |
| REVOI-only concepts | ~7 |

---

## 12. Architecture Notes

### Code Structure

```python
# Constants
WIN_W, WIN_H = 1280, 760
FAMILY_COLORS = { ... }          # 10 family colours
DIM_COL = { ... }                # ASFID/REVOI tile colours

# Data
_RAW = [ ... ]                   # 81 concept dictionaries
CONCEPTS = [_norm(c) for c in _deduped]
NAME_MAP = { name: index }

# Tree
class TNode: ...                 # tree node with expand state
build_tree() → TREE_ROOTS        # one subtree per family
flatten_tree() → rows            # visible rows for rendering

# Projections
pos_A(), pos_B(), pos_C()        # return (nx, ny, jitter_idx, jitter_total)

# Primitives
dashed(), tri(), dia()           # drawing helpers
otimes()                         # ⊗ circle-cross operator
scrollbar_draw()
vsplitter_draw()

# App
class App:
    # Layout properties (computed from splitter positions)
    tree_w, net_x, net_w, info_x, info_w

    # Rendering
    draw_grid(), draw_edges(), draw_nodes()
    draw_legend(), draw_modes(), draw_axis()
    draw_tree(), draw_formula()
    draw_profile(), draw_hsplitter(), draw_readme()
    draw_vsplitters(), draw_status()

    # Interaction
    handle()         # main event loop
    _tree_click()    # tree row click handler
    _zoom()          # zoom centred on cursor
    _rebuild()       # recompute 2D positions after resize
```

### Design Decisions

**Self-contained data**: The concept data is embedded as Python dictionaries in the script (not loaded from `M2_GenericConcepts.jsonld` at runtime). This makes the tool dependency-free beyond pygame, and avoids JSON-LD parsing overhead. The data structure mirrors the ontology exactly.

**Jitter**: Concepts at the same grid position are offset by a deterministic jitter function to prevent total overlap. The jitter is based on collision count and index — reproducible between runs.

**Flat Combo tree**: Combos are always displayed at depth 1 in the tree regardless of their `superclass` declaration. The IS-A structure is visible on the graph; the tree prioritises family grouping.

**otimes() primitive**: The ⊗ operator is drawn procedurally (circle + two perpendicular lines) rather than via a Unicode glyph, to avoid pygame font rendering differences across platforms (bitmap fonts may not support ⊗).

**Dynamic panel widths**: `tree_w`, `net_w`, `info_w` are computed dynamically from splitter positions (`spl_l`, `spl_r`). `_rebuild()` recomputes all node positions whenever a vertical splitter moves, so the concept net always fills its panel.

---

## Companion Files

| File | Description |
|------|-------------|
| `tscg_explorer.py` | This simulation tool |
| `M0_TscgExplorer.jsonld` | Formal ontology of this tool (`m3:TscgTool`) |
| `M0_TscgExplorer_README.md` | Ontology-level README (ASFID/REVOI analysis) |

---

*Echopraxium with the collaboration of Claude AI — 2026-03-01*
