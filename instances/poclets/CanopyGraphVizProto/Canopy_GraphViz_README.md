# Canopée — egocentric graph star-map

*Echopraxium with the collaboration of Claude AI.*

An interactive 3D graph explorer built on the idea of viewing a graph **from the inside**.
Instead of laying a graph out on a plane and watching it collapse into a hairball, the
observer stands *within* it and looks outward: nodes become celestial bodies, relations become
constellations, and exploration becomes a matter of aiming an instrument rather than
untangling a knot.

The name comes from the founding image: standing on the floor of a planet-wide forest and
looking up through the canopy. You see a near-infinity of leaves, fruit and animals; the
trunks and branches are there but do not hide them.

---

## 1. Quick start

The prototype loads external `.js` and `.css` files, so a browser will refuse to open it via
`file://` (each `file:` URL is treated as a unique security origin). Serve the folder:

```bash
cd canopy
python -m http.server 8080
```

then open <http://127.0.0.1:8080/M0_CanopyGraphviz.html>.

BabylonJS is pulled from a CDN; everything else is local. No build step, no bundler, no server
logic — the demo is genuinely serverless.

---

## 2. Controls

| Action | Control |
|---|---|
| Look around (up, down, behind) | drag, or `←` `→` |
| Fly along the gaze (jetpack) | `↑` `↓`, or `Z` `X`, or `W` `S` |
| Zoom — the instrument's field of view | mouse wheel, or the *Instrument* slider |
| Node actions (expand/collapse, observe from, aim, isolate) | **right-click a star** |
| Inspect | hover |
| Follow a cross-layer link | click a **stub** (in isolated-stratum mode) |

Zoom and movement are deliberately distinct: changing focal length is not changing position.
Backing away far enough makes the whole structure fall inside the field of view — a continuous
transition from an inside view to an outside one, with no separate "mode".

---

## 3. What is on screen

- **Bodies (nodes).** Shape encodes the *kind* of node (tetrahedron = generic concept,
  octahedron = combo, cube = family, sphere = instance, icosahedron = foundation); hue encodes
  a chosen facet; size and brightness encode **magnitude**.
- **Magnitude** works like stellar magnitude: it is a rank, not a raw count, so the scale
  stays evenly populated. A *folded* star's magnitude instead reflects **how much it hides**,
  so a dense body announces that it is worth opening.
- **The instrument** couples field of view to a seeing limit: a wide field shows only bright
  bodies, narrowing to a telescope reveals faint and distant ones — exactly as in observational
  astronomy. `Show every node` overrides the limit.
- **Constellations** are relation types, toggled individually. Edges are drawn only near the
  gaze, so they never re-form the hairball the whole design exists to avoid.
- **3D radar** (bottom right, collapsible): an egocentric disc with elevation stems, showing
  every contact around you and which slice of sky your instrument currently covers.

### Arrangements

The same graph, four ways — all selectable at runtime:

- **Canopy** — a containment forest rooted at the observer; each subtree grows outward as a
  trunk with a fan of leaves.
- **Clusters** — angular sectors driven by a declared facet.
- **Cone** — stratified layers, observer at the apex, each stratum a widening disc. The cone
  widens because cardinality grows with depth.
- **Nautilus** — a logarithmic shell. Each turn's perimeter grows by a constant factor
  (≈ ×1.6), i.e. geometrically, which absorbs the b^d growth of a branching hierarchy the way
  hyperbolic space does, by other means.

The **radial axis** is independent of the arrangement: the arrangement fixes *direction*, the
axis fixes *distance* (tree depth, specialization, meta-level, hops, trophic flow).

---

## 4. Architecture

Three concerns, three files. The boundary is the point of the design, not a filing convenience.

```
canopy/
  M0_CanopyGraphviz.html     markup only
  src/
    canopy.css               panel presentation
    canopy-data.js           DATA    — the {nodes, edges} graph
    canopy-stylesheet.js     STYLE   — the encoding, and the legend
    canopy-core.js           CORE    — domain-agnostic engine
  test/
    boot-smoke.js            full-initialisation smoke test
```

- **`canopy-data.js`** is the only file to replace to plug in real data. A JSON-LD parser, a
  Neo4j/Bolt reader or a GEXF loader all emit the same `{nodes, edges}` shape; nothing else
  changes.
- **`canopy-stylesheet.js`** is the single declarative encoding — glyphs, hues, adornments,
  palettes. **The on-screen legend is generated from it**, so editing it changes the render and
  its reading guide together. Several stylesheets can exist and be swapped per audience.
- **`canopy-core.js`** is domain-agnostic: layout strategies, structure recovery, rendering,
  radar, explorer, interaction. Nothing in it is TSCG-specific.

Load order matters: **data → stylesheet → core**.

### Containment vs. contract

The folding tree follows *containment*, and the test is **cardinality**:

> A relation that may carry several values cannot define a single parent, so it is a
> **contract** the node satisfies, not a **container** it sits in.

`M0 appliesToDomains M1_Biology` is a contract — an instance may honour several domains — so it
creates no parent/child link. Single-valued classification relations (`hasFamily`,
`ontologyType`, `domain`, `parentCombo`) do. Edge **direction** matters too: in these triples
the *object* is the container, so the tree is walked against the arrow.

---

## 5. Current state

- The graph in `canopy-data.js` is **synthetic** — a faithful-shaped stand-in with real
  relation types, not the real corpus. It is deliberately small (82 nodes) to iterate quickly
  on the visualisation.
- The real corpus is roughly **599 nodes** once schema plumbing is excluded (property and
  shape definitions, document headers, score reifications — none of which are graph nodes).
- Structure recovery (spectral clustering, trophic levels) runs in pure JS with no
  dependencies, and is used to show that declared facets can be *rediscovered* from usage
  alone — the gap between the two is a measurable Map/Territory signal.

### Known limits

- **Rendering does not yet scale to the real corpus.** One mesh and one material per node,
  plus per-edge meshes rebuilt on every interaction, would reach several thousand draw calls.
  Two fixes come first: merge all edges into a single line system with per-vertex colours, and
  share materials. Instancing (one master mesh per shape) is only needed beyond a few thousand
  nodes — and beyond ~1–2 000 simultaneously visible bodies the limit is human, not technical.
- **Magnitude is derived from degree**, the crudest centrality measure, computed over all
  relation types regardless of which constellations are switched off. Numeric properties in the
  real corpus (`epistemicGap`, `asfidMean`, `revoiMean`) would be far more meaningful drivers.
- **Shells are linear.** Shell area grows as r² while node count grows as b^d, so concentric
  layouts saturate with depth. The nautilus arrangement is the answer to this; folding and the
  seeing limit postpone it in the others.
- Cross-slice **stubs** exist only in the cone's isolated-stratum mode, not in every
  arrangement.

---

## 6. Companion documents

Read in this order:

1. **`Canopee_Stylesheet_and_Legend_Spec.md`** — the frozen architecture: the layer boundary,
   the stylesheet schema, the *stylesheet = legend* principle, channel-effectiveness guidance,
   prior art (GEXF `viz`, Cytoscape.js, Neo4j GraSS), and the deferred worksite on treating a
   stylesheet as a representation ontology.
2. **`MIGRATION_knowledgeField_to_domain.md`** — an in-progress corpus rename, and the
   `rdfs:domain` collision hazard that will bite any parser keying properties by local name.
3. **`test/README.md`** — what the smoke test covers and why it exists.

---

## 7. Prior art

Canopée is not the first egocentric graph navigator, and it helps to know the neighbours:
Munzner's **H3** (hyperbolic 3D navigation of large graphs, spanning tree, focus+context),
**Cone Trees** (Robertson, Mackinlay & Card), and the hyperbolic **StarTree** (Lamping & Rao).
What appears distinctive here is the combination rather than the projection: type-and-facet
slices as first-class filters, the optical instrument coupling field of view to a seeing limit,
folded stars whose brightness reports their hidden mass, and a legend generated from the same
object that drives the render.
