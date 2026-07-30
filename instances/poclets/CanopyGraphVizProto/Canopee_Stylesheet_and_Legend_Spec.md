# Canopée — Stylesheet & Legend Specification (v1.0)

*Echopraxium with the collaboration of Claude AI.*

Purpose: freeze the abstraction we converged on so the design stops being clay on a
potter's wheel. This document fixes the **schema**; specific values (which shape, which
hue) stay editable, and new layout strategies can still be added. What is frozen is the
*shape of the thing*, not its contents.

---

## 1. Three layers

Canopée separates three concerns that were previously intermingled. They map onto the
single `canopy-core` interface: it consumes a graph, applies a layout strategy, and renders
through a stylesheet.

- **Data** — the typed graph `{ nodes, edges }`. Nodes carry static attributes; edges carry
  a `type` and a direction (`s → t`). This is the *Territory*. Providers (synthetic, real
  M0–M3 parser, Neo4j/Bolt, Obsidian/MetadataCache, Gephi-enriched GEXF) all emit this shape.
- **Layout strategies** — a *library* of position algorithms: `canopy` (spanning forest from
  the observer), `clusters` (facet sectors), `cone` (stratified genesis), `radial`, `trophic`,
  spectral embedding. These contain real algorithmic content (spanning trees, phyllotaxis,
  eigen-decomposition) and are implemented once in `canopy-core`.
- **Style** — the encoding: it binds node/edge properties to visual channels. This is the
  *Map*, and — per the legend insight below — it is also the map's legend.

**Correction (v1.1): layout is a style channel, not a third layer.** The v1.0 draft listed
Layout as a peer of Style. That was wrong. Position is a visual channel — in Bertin's terms
the *strongest* one — so choosing an arrangement is an encoding decision like choosing a hue
palette. The CSS precedent this spec keeps invoking says the same: `display: grid | flex` is a
*style property* that selects a layout algorithm which the engine implements. So:

> The stylesheet **selects and parameterizes** a layout strategy; the strategy library
> **implements** it.

Consequence, and it answers a real worry: **this keeps the tool general rather than
TSCG-specific.** `canopy-core` (strategies, channels, legend generation) is domain-agnostic;
only the *default stylesheet* (§4) is TSCG-flavoured. A cone-of-cosmic-history arrangement, a
nautilus shell, a hyperbolic embedding — these are stylesheet choices to be invented, swapped
per audience, and shipped alongside a view. Nothing about them is TSCG.

Only the **Style schema** and the **layer boundary** are frozen here. Layout strategies and
data providers remain open sets.

---

## 2. The Style layer *is* the map legend

The central principle. On a cartographic map the legend and the encoding are one object seen
from two sides:

- **Machine side (stylesheet):** the declarative rules that bind data → visual channels.
- **Human side (legend):** the on-screen panel that shows those bindings so a reader can
  decode the map.

Therefore:

1. **Single source of truth.** The legend is *generated from* the stylesheet, never
   hand-maintained. Edit the stylesheet → the legend re-renders → the scene re-renders.
2. **The stylesheet is the user-configuration surface.** "User-configurable glyphs" and
   "graph stylesheet" are the same request. There is one place to configure, one place to read.
3. **The legend travels with the view.** A shared or published Canopée carries its stylesheet;
   without it the marks are undecodable. This is the *guide de lecture*, and it is what makes
   a Canopée reproducible outside the head of the person who built it.

This is not plain web CSS. Web CSS selects on a static DOM; here selectors may bind to
**computed structural properties** of the graph (degree, trophic level, spectral cluster,
BFS/tree depth). The pipeline is therefore *transform then encode* — closer to a grammar of
graphics (Wilkinson; Vega-Lite) than to a fixed stylesheet, with Bertin's visual variables as
the channel vocabulary.

---

## 3. Stylesheet schema

A stylesheet is an ordered list of **rules**. Each rule = a **selector** (which nodes/edges it
matches) plus **channel bindings** (how they render). First matching rule wins; a default rule
closes the list.

### 3.1 Selectors

Selectors match on two kinds of field:

- **Static attributes** (carried by the data): `layer`, `family`, `dominantM3`,
  `ontologyType`, `sourceVocabulary`, `kind` (a derived category: foundation / root / concept /
  combo / domainCombo / family / domainConcept / instance / vocab), edge `type`.
- **Computed structural fields** (produced by the layout/analysis engines, recomputed on
  relayout): `degree` → magnitude, `treeDepth` (canopy), `bfsDepth` (from observer),
  `trophicLevel`, `spectralCluster(k)`.

A selector is a predicate over these fields (equality, membership, range).

### 3.2 Channels

Grouped as a cartographic legend groups its symbols — point symbols, line symbols, and the
reference frame.

**Point symbols (nodes)**
- `shape` — categorical. { sphere, cube, tetra, octa, ico, dodeca }.
- `hue` — categorical or by computed field.
- `size` + `brightness` — ordered (magnitude).
- `adornment` — a ring: { none, round, square } — a low-cardinality relational flag.

**Line symbols (edges)**
- `color` — categorical, by relation `type`.
- `opacity` — ordered, global "scaffolding" level (trunks/branches are transparent by default).

**Reference frame (the graticule & scale)**
- `radialAxis` — set by the active Layout strategy; the legend states which one is live.
- `instrument` — the FOV↦magnitude-limit coupling (naked eye → telescope); the legend states
  the current field and the seeing magnitude.

### 3.3 Channel-effectiveness guidance (Bertin / Mackinlay)

Channels are not equal. A well-formed stylesheet steers each field to a channel that can carry
its cardinality; the legend should warn, not forbid, on mismatch.

| Channel            | Nature              | Distinguishable values | Best for                         |
|--------------------|---------------------|------------------------|----------------------------------|
| Position (r, θ, φ) | ordered + categorical | very high            | the primary structural axis      |
| Size / brightness  | ordered             | ~4–6                   | magnitude / importance           |
| Hue                | categorical         | ~7–12                  | a facet with few values          |
| Shape              | categorical         | ~5–8                   | node *kind* (small closed set)   |
| Adornment (ring)   | categorical         | ~2–3 flags             | a binary/ternary relational flag |
| Opacity            | ordered             | low precision          | scaffolding / de-emphasis        |

Rule of thumb: bind the field you most need to read to **position**; bind *kind* to **shape**;
bind one low-cardinality facet to **hue**; keep **adornment** for flags. Do not bind a
high-cardinality field (e.g. 50 domains) to shape or hue.

---

## 4. Frozen default stylesheet (v1.0)

The baseline we built, written out as the canonical starting point. Editable; this is the
"proposed" set, not a constraint.

**Nodes — shape & default hue by `kind`:**

| kind          | shape        | hue      | ring   | meaning                    |
|---------------|--------------|----------|--------|----------------------------|
| foundation    | icosahedron  | gold     | —      | M3 foundation (fixed star) |
| root          | dodecahedron | slate    | —      | root class                 |
| concept       | tetrahedron  | yellow   | —      | GenericConcept             |
| combo         | octahedron   | green    | —      | GenericConceptCombo        |
| domainCombo   | octahedron   | green    | square | DomainConceptCombo (+domain) |
| family        | cube         | blue     | —      | family                     |
| domainConcept | cube         | green    | round  | M1 domain concept          |
| instance      | sphere       | pink     | —      | M0 instance (fruit)        |
| vocab         | octahedron   | grey     | —      | imported vocabulary        |

**Hue override (optional):** bind `hue` to a computed/facet field instead of kind —
`dominantM3` (3), `family` (≤10), or `spectralCluster(k)`. When hue is bound to a facet, shape
still carries kind, so both channels read at once.

**Size / brightness:** `magnitude` = degree, normalised over non-vocabulary nodes.

**Edges:** `color` by relation `type`; `opacity` = global scaffolding (default ~0.15).

**Reference frame:** `radialAxis` = active layout (default `canopy` tree-depth);
`instrument` = FOV coupling (field 20°–92°, seeing magnitude derived).

---

## 5. Placement in TSCG

The stylesheet-legend is a **Map** artifact (Sphinx Eye / REVOI side), not a Territory one. It
operationalises **Representability**: the legend is precisely what makes a representation
*interpretable and decodable* by a second reader. Two consequences worth recording:

- A Canopée view of a graph is only as reproducible as its legend is explicit — so the
  stylesheet is a first-class, versioned object, not a runtime afterthought.
- The Data/Layout/Style split mirrors Territory / measurement / Map: the graph is measured
  (degree, trophic, spectral — Eagle-Eye-like structural quantities) and then represented
  (encoded to channels — Sphinx-Eye-like). Structure recovery feeds selectors; the legend
  publishes the mapping.

---

## 6. Frozen vs. fluid

**Frozen (v1.0):** the three-layer split; the layer boundary at `canopy-core`; the stylesheet
= legend principle (single source, auto-generated, travels with the view); the schema
(selectors over static + computed fields; the channel set; the cartographic grouping).

**Fluid (still open):** which shapes/hues/rings map to what (the default table above is a
proposal); the set of layout strategies; the set of data providers; the set of computed
structural fields; a future in-canvas rule editor.

Next consolidation step: refactor the prototype so every scattered mapping reads from one
`stylesheet` object, and render the on-screen legend from it — firing this pot.

---

## 7. Deferred worksite — the stylesheet as a representation ontology

*Recorded, not opened.* A stylesheet is itself a formal object: classes (`Rule`, `Selector`,
`Channel`, `GlyphShape`…), properties (`bindsField`, `toChannel`, `hasCardinality`), instances
(the rules), and constraints that are naturally **SHACL shapes** — `shape` ∈ a closed set of 6;
a hue binding's field cardinality ≤ 12; `adornment` ∈ {none, round, square}; every `Rule` has
exactly one `Selector` and ≥ 1 `ChannelBinding`; a default rule closes the list; the §3.3
effectiveness table becomes range/warning constraints.

This is a **representation ontology**, orthogonal to and running in parallel with the M3..M0
content cake: the content stack says what the graph *is* (Territory); the representation stack
says how it is *shown* (Map). It has its own small meta-structure — a grammar of representation
(its SHACL shapes ≈ M3/M2) and concrete stylesheets (instances ≈ M1/M0). It is also
self-applicable — a representation ontology is a graph, viewable in Canopée through a
stylesheet — and that door stays shut.

**When it earns formalization, and not before.** A full OWL+SHACL representation ontology is
justified precisely when stylesheets become **shared, published, multi-authored** artifacts
that need validation and interoperability — the same trigger as "the legend must travel with
the view" (Zenodo, hand-off to a collaborator). Until then, by the project's own
anti-overfitting discipline, a plain declarative object (JSON / TypeScript types) carries the
entire schema at a fraction of the cost; building an ontological apparatus for a single-author
prototype config would itself be OntologicalOverfitting. **Deferred, scoped, named — kept out
of the current build.**

---

## 8. Prior art & interoperability — don't reinvent the wheel

Two different things exist to borrow, from two different places. They are not the same layer;
confusing them is what leads to reinvention.

**Channel vocabulary ← GEXF `viz` module (Gephi).** Gephi has *no* rule-based stylesheet
grammar. Its styling is GEXF's `viz` extension: per-element attributes `viz:color` (RGBA/hex),
`viz:position` (3D), `viz:size`, `viz:shape` (nodes: disc/square/triangle/diamond/image; edges:
solid/dotted/dashed/double), `viz:thickness`. These are **baked per element** — imperative
("this node is red"), not selector-based, and not dynamic in GEXF 1.3. We align our channel
*names and semantics* with this vocabulary for interoperability. Caveat: GEXF shapes are 2D;
our glyphs are 3D polyhedra — a mapping, not an identity.

**Rule/selector structure ← Cytoscape.js stylesheet / Neo4j GraSS / grammar of graphics.** The
declarative "selector → channel binding" paradigm this spec adopts is *not* in GEXF. It is
mature in Cytoscape.js's CSS-like stylesheet, in Neo4j's **GraSS** (Graph Style Sheet), and, at
the encoding-channel level, in Vega-Lite. Borrow the rule structure from these.

**They compose.** GEXF `viz` is the *output* of styling (baked per element); the Canopée
stylesheet is the *specification* (rules). The rules *compute* the baked attributes. Therefore:

- **Export** — bake a stylesheet into GEXF `viz` per element → round-trips with Gephi,
  sigma.js, gexf-js, Graphistry.
- **Import** — read GEXF `viz` as per-element defaults / fallback.

This slots into the already-chosen pipeline (Gephi upstream: compute Louvain / centrality →
GEXF carrying `modularity_class`, `degree`, … → Canopée consumes). The native stylesheet stays
a plain, rule-based `.json`; the GEXF bake is an **adapter**, not the native format.
