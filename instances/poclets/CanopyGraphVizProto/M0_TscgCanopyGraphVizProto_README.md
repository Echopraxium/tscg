# M0_TscgCanopyGraphVizProto — README

*Echopraxium with the collaboration of Claude AI.*

**Type:** `m3:Poclet` · **Domain:** TSCG · **Version:** 0.1.0 · **Stage:** prototype (serverless HTML)

---

## What this poclet is

`TscgCanopyGraphVizProto` is the M0 specification of a **serverless HTML prototype** for
*egocentric* 3D graph visualisation. The observer stands **inside** the graph — at its
barycentre by default — and looks outward: nodes are celestial bodies, relations are
constellations. A first-person "jetpack" flies the observer along the line of sight, so a
single continuous view spans an **interior** vantage (within the graph) and, by backing far
enough out, an **exterior** one (the classic outside view). A right-click **teleports** the
observer onto any node, which then becomes the new centre.

This is deliberately the **prototype** stage: a single HTML file, BabylonJS from a CDN, no
server and no build step. The mature tool is projected separately as **`TscgCanopyGraphViz`**
(an ElectronJS `m3:TscgTool`) — a fuller application able to visualise arbitrary graphs and
ontologies beyond TSCG, with a more advanced Stylesheet engine. Keeping the two distinct is the
point of the `_Proto` suffix: it names the artifact that *exists* rather than the one that is
*projected*.

---

## The phenomenon it models

Two long-standing failure modes of graph layout:

- The **hairball** — a force-directed graph on a plane collapses into an unreadable tangle and
  has *no interior* to stand in.
- **PersonalBrain**-style egocentric browsers give a comfortable local neighbourhood but *no
  exterior* — you can never see the whole.

The prototype's proposition is that a **mobile viewpoint** dissolves the dichotomy: the same
scene is read from inside (immersive, local) or from outside (global) depending only on where
the observer flies. The founding image is standing on the floor of a planet-wide forest and
looking up through the canopy — hence the name.

---

## Mobilized GenericConcepts (M2)

Only concepts that actually exist in `M2_GenericConcepts.jsonld` are cited (anti-overfitting):

| GenericConcept | Role in the prototype |
|---|---|
| **Observer** | The viewpoint is a first-class entity at the barycentre; the layout is computed *from* it and it can be teleported. |
| **Representation** | The stylesheet is an explicit, editable representation layer; editing it changes render and legend together. |
| **Layer** | The M3→M2→M1→M0 strata drive the cone arrangement and the meta radial axis. |
| **Hierarchy** | Single-valued (containment) relations build the folding forest; multi-valued (contract) relations stay lateral. |
| **Composition (Decomposition)** | Folding composes a subtree into one bright body and decomposes it on demand; a folded star's brightness encodes hidden mass. |
| **Emergence** | Structure recovery (spectral clustering, trophic levels) lets grouping *emerge* from usage links, to compare against declared facets. |

---

## Map / Territory reflexivity

What makes this more than a viewer: the tool **embodies the very distinction it explores**.

- The **Territory** is the typed graph — nodes and edges with their declared relations.
- The **Map** is the stylesheet-driven rendering — glyph, hue, magnitude, arrangement, legend.
- The observer stands *in* the Territory (barycentre) yet reads a *Map* (the stylesheet), and
  can step out to see that Map whole.

The gap between clusters the tool **recovers** from usage links and the facets that were
**declared** is a measurable δ₁ epistemic signal — surfaced by the tool on its own subject
matter. This is why the poclet is defensible as a *poclet* and not merely a `TscgTool`: the
visualisation is a transdisciplinary phenomenon (representation of structure) analysed through
the TSCG grid, not just an instrument that displays TSCG.

---

## ASFID / REVOI scoring

Means: **ASFID 0.796**, **REVOI 0.780**, **δ₁ (epistemic gap) 0.016** — SpectralClass
**Coherent**.

The two scores worth reading are the extremes:

- **E (Evolvability) 0.88** — the highest. The data adapter, layout library and stylesheet are
  each designed to be swapped and grown; the prototype is explicitly a *way to explore*, not a
  finished claim.
- **V (Verifiability) 0.62** — the lowest, and honestly so. Verification is headless smoke
  tests plus manual on-screen inspection. Visual behaviour — occlusion, billboarding, browser
  event ordering — is **not** machine-verified. Several real bugs in this class were found only
  by looking at the screen. This is a genuine limitation, recorded rather than rounded away.

Full per-axis justifications are in the `m0:scoreJustification` block of the ontology.

---

## The Stylesheet principle

Rendering is driven by one declarative **STYLESHEET** object with two faces:

1. the **machine encoding** that positions and paints every node, and
2. the **on-screen legend**, generated from that same object.

Shape encodes node **kind**, hue a chosen **facet**, size and brightness the **magnitude**, and
**position** is a layout strategy chosen as a style *channel* (position being the strongest
visual variable). Because the stylesheet declares how graph *semantics* map to visual
*variables*, it is itself a small **representation ontology** — a second-order Map. Different
stylesheets are different Maps of the same Territory, and they travel with the view.

Formalising the stylesheet as an OWL+SHACL ontology is **deliberately deferred** for a
single-author prototype — doing it now would be OntologicalOverfitting. The mature
`TscgCanopyGraphViz` tool is the place for that.

---

## Architecture (three concerns, three files)

```
M0_CanopyGraphviz.html      markup only; loads data -> stylesheet -> core
src/canopy-data.js          DATA   — {nodes, edges}; the only file to replace for real data
src/canopy-stylesheet.js    STYLE  — the encoding, and the legend generated from it
src/canopy-core.js          CORE   — domain-agnostic engine
src/canopy.css              panel presentation
test/boot-smoke.js          headless full-init smoke test
```

Arrangements: **canopy** (default), **clusters**, **cone** (stratified genesis, best seen
side-on via *Teleport outside*), **nautilus** (logarithmic shell). Radial axis is independent of
arrangement: tree / subclass / meta / hops / trophic.

---

## Known limitations (recorded, not hidden)

- Rendering does not yet scale to the full ~599-node corpus; edge-merge + shared materials come
  first, thin-instance glyphs later.
- Magnitude derives from raw degree over all relation types; corpus properties
  (`epistemicGap`, `asfidMean`, `revoiMean`) would be more meaningful drivers.
- Concentric shells saturate with depth; the nautilus arrangement is the structural answer.
- The shipped data is a synthetic fixture matched to the corpus's proportions — the real
  JSON-LD parser is the next milestone.
- Visual behaviour is verified by eye, not by machine (hence V = 0.62).

---

## Relationship to the projected tool

| | `TscgCanopyGraphVizProto` (this) | `TscgCanopyGraphViz` (projected) |
|---|---|---|
| Type | `m3:Poclet` | `m3:TscgTool` |
| Form | Serverless single-file HTML | ElectronJS application |
| Scope | The TSCG graph | Arbitrary graphs / ontologies |
| Stylesheet | Principle demonstrated | Full engine, OWL+SHACL-formalised |
| Purpose | A way to *explore* the idea | A tool to *use* it |

---

## Live prototype

`https://echopraxium.github.io/tscg/` (see the project site for the current deployment path).

Served locally: `python -m http.server 8080`, then open `M0_CanopyGraphviz.html` over
`http://127.0.0.1:8080/` (external modules will not load over `file://`).
