# Canopée — controls guide

*Echopraxium with the collaboration of Claude AI.*

Every option in the left panel, what it does, and — more importantly — *why* it exists. The
panel is split into three tabs: **Navigation** (everyday use), **Advanced** (encoding choices),
**Help** (a short in-app version of this document).

The guiding idea: you stand **inside** the graph and look outward. Nodes are celestial bodies,
relations are constellations. Rather than untangling a flat hairball, you fly through the graph
and aim an instrument at what you want to see.

---

## Moving around

These are not panel options but the core interaction:

- **Drag** the view to look around — up, down, behind you. There is no horizon; you can look
  in any direction.
- **↑ ↓**, or **Z / X**, or **W / S** — fly forward or backward along your line of sight
  (the "jetpack"). Flying *back* far enough lifts you out of the graph entirely.
- **← →** — turn your head left/right.
- **Mouse wheel** — zoom the lens. This changes your *field of view*, not your *position*:
  it magnifies what you already see, it does not move you. (Movement is the keyboard's job.)
- **Hover** a body — a tooltip shows its details; a wobbling selection ring marks it.
- **Right-click** a body — a context menu of actions (below).
- **Double-click** a body — teleport your vantage onto it.

---

## Navigation tab

### Observer
Shows which node you are currently standing on (your vantage point). The graph is laid out
*from* this node.

### Arrangement
The same graph, laid out in fundamentally different ways. This is a **style choice**, not a
different graph — the data underneath never changes.

- **Canopy — trees from the observer** *(default)*. A containment forest grows outward from
  you: each subtree is a trunk with a fan of leaves. This is the egocentric, immersive view.
- **Clusters — sectors by facet**. Nodes fan out into angular sectors, one per value of the
  chosen facet (grammar, family, …).
- **Cone — stratified layers (genesis)**. The M3→M2→M1→M0 layers become a stack of widening
  discs, like the standard "history of the universe" cone: few foundations at the tip, many
  instances at the base. **Best seen from the side** — use *Teleport outside* — because from
  the tip every stratum projects onto the others.
- **Nautilus — logarithmic shell**. The layers coil into a shell whose room per turn grows by
  a constant factor. This is the one arrangement that structurally absorbs the explosive growth
  of a deep hierarchy (each turn has ~1.6× the room of the last).

### Instrument
Couples your field of view to a **seeing limit**, exactly like an optical instrument. A wide
field (naked eye) shows only the **bright** bodies — the well-connected ones; narrowing toward
a telescope reveals **faint** ones. The readout shows *field angle · seeing magnitude · visible
count*. This is how you keep a large graph legible: you don't hide nodes by rule, you simply
can't see the faint ones until you look harder.

- **Show every node** — overrides the seeing limit; every body becomes visible regardless of
  magnitude. Useful for an exhaustive check, at the cost of clutter.

### Jetpack (readout)
Shows how far out from centre you have flown (`at centre` / `N out`). Purely informational —
you fly with the keyboard.

### Focus distance
Hides bodies beyond a chosen distance, measured along the current radial axis. Slide it down to
peel the graph outward shell by shell — a blunt but instant way to thin a dense view.

### Object explorer
- **Layer filter** + **text filter** — narrow the list to a layer (M3/M2/M1/M0/vocabulary) and
  a search term.
- **Click** an entry — *aim* at it: a guidance arrow appears at the screen edge pointing which
  way to turn your head, and the body is ringed when it comes into view.
- **Set centre on selection** — teleport your vantage onto the selected node.
- **Teleport outside — see the whole graph** — pull straight back along your gaze by the
  graph's own size (its bounding-box diagonal), so the entire structure fits in view. This is
  how you get the *outside* view of the cone or nautilus.
- **Reset view** — return to the default: egocentric canopy, centred, all filters cleared.

### Folding
- **Limit selector** — *Exclusive (1) / 3 / 5 / 10 / No limit*. How many subtrees may be
  expanded at once. Opening one past the limit **closes the oldest** (never refuses the click),
  so the sky can't flood. Default: 5.
- Right-click a star → **Expand / Collapse**. A **folded star grows brighter** in proportion to
  how much it hides, so you can see *where the mass is* even while it's closed — a dense body
  announces that it's worth opening.
- **Collapse all** / **Expand all (no limit)** — bulk actions.

### Cone: slices & travel *(shown only in Cone arrangement)*
- **◄ / All / ►** — isolate a single stratum (M3, then M2, …). Links leaving it don't vanish;
  they become clickable **stubs** you follow like hyperlinks to the other layer. This is what
  keeps the layer cake connected while you look at one layer at a time.
- **◄ retro / chrono ►** — glide smoothly along the cone axis, toward M3 (retro) or M0
  (chronological), like travelling the timeline.

### Legend
A reading guide generated *from* the stylesheet: it shows the shape→kind mapping, the current
hue binding, the relation colours, and the current reference frame. It always matches what's on
screen because it is produced from the same object that drives the render.

### Show imported vocabulary
Off by default. The graph imports terms from `owl`, `rdfs`, `skos`, `dcterms`, `xsd`. These are
plumbing, not content, and they act as hairball magnets — so they're hidden unless you ask.

---

## Advanced tab

These change the *encoding*, and are hidden by default to keep the panel approachable.

### Radial axis
The arrangement fixes **direction**; this fixes **distance from you**. They are independent, so
you can combine them freely (e.g. "canopy shape, but distance = specialization depth").
Options: **tree depth**, **specialization** (subClassOf/hasFamily depth), **meta-level**
(M3=near … M0=far), **hops** (BFS distance from you), **trophic flow** (position in the directed
flow of relations).

### Colour by
Shape *always* encodes the **kind** of node (▲ concept, ◆ combo, ■ family, ● instance,
⬢ foundation, ⬟ root). Hue can encode either:
- **a facet** (grammar / family / layer / type) — so you read two channels at once, or
- **node kind** — hue simply matches the shapes.

### Facet
Which facet the sectors (in Clusters) and the hue (when *Colour by = facet*) are based on:
dominant grammar (Territory/Map/Stereopsis), concept family, meta-layer, ontology type, or
source vocabulary.

### Constellations (relation types)
Toggle which relation types are drawn as edges. Edges are shown **only near your gaze**, never
across the whole sphere, so switching several on doesn't re-create the hairball. Colours match
the legend.

### Reveal hidden structure (spectral)
Ignores the *declared* facets entirely and re-discovers clusters from the **link pattern alone**
(normalized-Laplacian spectral clustering, k adjustable). The interesting part is the **gap**:
where the clusters it finds disagree with the facets you declared, that disagreement is a
Map/Territory signal — the structure is saying something the labels don't.

---

## Right-click menu (per node)

- **Expand / Collapse** — fold or unfold this node's subtree, with the count it affects.
- **Teleport there** — make this node your new vantage point; the canopy re-forms around it.
- **Aim at this** — point the guidance arrow at it without moving.
- **Isolate its stratum** — *(cone only)* show only its layer, with stubs to the rest.
- **Open simulation ↗** — *(instances that have one)* open the poclet's published interactive
  simulation in a new tab.

---

## The 3D radar (bottom-right, collapsible)

An egocentric radar in the spirit of *Elite*: a disc centred on you, each contact placed by
azimuth and distance, with a vertical **stem** giving its elevation above or below your plane.
A shaded wedge shows the slice of sky your instrument currently covers. The counter reads
**Visible** (bodies in the scene) · **Observed** (bodies actually on screen right now).

---

## A note on the current data

The graph shipped in `src/canopy-data.js` is a **synthetic stand-in** (~380 nodes:
M3 = 14, M2 = 60, M1 = 135, M0 = 164), shaped to match the real TSCG corpus's proportions so
the layout, folding and slicing behave realistically. Its concept names are plausible but
invented; only the *shape* of the graph is faithful. Replacing this one file with a real M0–M3
JSON-LD parser is the next milestone — nothing else in the app needs to change.
