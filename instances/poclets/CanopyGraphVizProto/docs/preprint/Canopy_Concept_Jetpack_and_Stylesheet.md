# Canopée — the Jetpack viewpoint and the Stylesheet-as-ontology

*Echopraxium with the collaboration of Claude AI.*

A conceptual note, written to stand on its own and to serve as raw material for a short
(~7–10 page) exploratory paper. It presents two ideas the Canopée prototype puts on the table:
a **mobile, jetpack-driven viewpoint** that unifies inside and outside views of a graph, and a
**stylesheet that is itself a representation ontology**. Both are offered as a *way to explore*
graph visualisation, not as a claim of innovation — the egocentric navigation of graphs is
decades old, and honesty about that is part of the argument.

---

## 1. The problem: neither the hairball nor the local map

Two familiar approaches each throw away half of what you want.

A **force-directed layout** drawn on a plane is a *global* picture, but past a few hundred nodes
it collapses into a hairball: edges cross everything, hubs overlap, and — crucially — there is
**no interior**. You look *at* it; you cannot stand *in* it.

An **egocentric browser** in the PersonalBrain lineage gives a comfortable *local* view — the
node you chose and its immediate neighbours — but there is **no exterior**. You can walk from
node to node, yet you can never step back and see the whole shape.

The two failure modes are duals: one has an outside and no inside, the other an inside and no
outside. The question Canopée puts on the table is whether a single view can hold **both**.

---

## 2. The proposition: a mobile viewpoint (the "Jetpack")

Canopée's answer is to make the **viewpoint itself mobile**, and to treat interior and exterior
not as two modes but as two *positions* of one observer.

The observer begins **inside** the graph, at its **barycentre**, and looks outward. Nodes are
rendered as celestial bodies, relations as constellations; the founding image is standing on
the floor of a planet-wide forest and looking up through the canopy — you see a near-infinity of
leaves, and the branches that carry them do not hide them.

Three motions, one continuous space:

- **Interior.** At or near the barycentre, the observer is immersed. Nearby nodes loom; distant
  strata recede. This is the view the hairball cannot offer.
- **Exterior.** Flying **back** along the line of sight (the "jetpack") continuously lifts the
  observer out until the whole graph falls inside the field of view. There is no separate
  "overview mode" — the outside view is simply what the inside view becomes when you retreat far
  enough. A one-step *Teleport outside* performs the same retreat instantly, and for the
  stratified *cone* arrangement it places the observer **broadside** to the cone's axis, so the
  layers separate instead of projecting onto one another.
- **Teleport.** Right-clicking a node re-centres the observer **onto** it; the layout re-forms
  around the new vantage, like following a hyperlink into a new room.

The interaction vocabulary keeps a strict separation that matters for immersion: **movement**
belongs to the keyboard (fly forward/back along the gaze, turn the head), while the **mouse
wheel changes only the lens** — the field of view, an optical zoom that magnifies what you
already see without moving you. Confusing zoom with travel is a common source of disorientation
in 3D navigators; keeping them on different channels is a deliberate choice.

### 2.1 An optical instrument, not a filter slider

Legibility at scale is handled the way an astronomer handles a crowded sky: with a **seeing
limit** coupled to the field of view. A wide field shows only the **bright** bodies — here,
brightness (stellar *magnitude*) encodes how structurally important a node is. Narrowing the
field toward a telescope raises the limit and reveals **faint** ones. You do not toggle nodes
off by rule; you simply cannot see the faint ones until you look harder in a narrower cone. It
is filtering reframed as *observation*, and it fits the metaphor exactly.

A companion move: a node that has been **folded** (its subtree collapsed) is drawn **brighter in
proportion to how much it hides**. A dense body therefore *announces* that it is worth opening,
and the observer allocates attention the way an astronomer is drawn to a bright star. Folding is
kept honest by a small policy — only so many subtrees open at once, the oldest closing when a
new one opens — so the sky never floods.

### 2.2 Why "exploration path", not "innovation"

None of the primitives here is new. Hyperbolic and 3D egocentric graph navigation goes back to
the 1990s — Munzner's **H3**, the **Cone Tree** of Robertson, Mackinlay and Card, the hyperbolic
**StarTree** of Lamping and Rao. Claiming novelty for "standing inside a graph" would invite the
easiest possible rebuttal. What is worth putting forward is the **combination** and the
**posture**: the optical instrument coupling field of view to a magnitude limit; folded stars
whose brightness reports hidden mass; the continuous inside↔outside travel with no mode switch;
and — the next section — a stylesheet that is simultaneously encoding and legend. Offered as a
*direction*, this is defensible even to a hostile reader, because it is true.

---

## 3. The Stylesheet as a representation ontology

The second idea is quieter and, arguably, the more interesting one.

Everything visible in Canopée is produced from a single declarative object, the **stylesheet**,
which has **two faces at once**:

1. the **machine encoding** — the rules that position and paint every node, and
2. the **on-screen legend** — generated *from that same object*.

Because they are the same object, the legend can never drift from the render: the reading guide
*is* the encoding, shown in human-readable form. Edit the stylesheet and both change together.

### 3.1 The channels

The stylesheet binds graph *semantics* to visual *variables*, in Bertin's sense:

- **Shape** encodes the node's **kind** (concept, combo, family, instance, foundation…).
- **Hue** encodes a chosen **facet** — the dominant grammar, the concept family, the meta-layer.
- **Size and brightness** encode **magnitude** — structural importance.
- **Position** is a **layout strategy** chosen as a style channel — canopy, clusters, cone,
  nautilus. Treating position as a channel (rather than a fixed algorithm) matters because
  position is the strongest visual variable available; choosing it is a representational
  decision, not a mechanical default.

### 3.2 Why this is an ontology, not just a theme

A CSS theme decorates; it says nothing about meaning. This stylesheet is different: each rule is
a claim of the form *"this aspect of the graph's meaning shall be shown by that visual
variable"*. That is exactly what a **representation ontology** does — it declares a mapping from
a domain's structure to a chosen set of signs. The stylesheet is therefore a small ontology of
*representation*, layered above the domain ontology it renders.

This makes it a **second-order Map** in TSCG terms. The graph is the Territory. A rendering is a
Map of it. The stylesheet is a Map of *how to Map* — it does not describe the domain, it
describes the act of representing the domain. Two different stylesheets are two different Maps of
the same Territory, each defensible, each defeasible, and each **travelling with the view** so
that a shared visualisation carries its own interpretation key.

### 3.3 Reflexivity: the tool embodies Map/Territory

The payoff is that the instrument enacts the very distinction it helps explore. The observer
stands *in* the Territory (at the barycentre, among the nodes) while reading a *Map* (the
stylesheet's rendering), and can fly *out* to see that Map whole. And when the tool **recovers**
structure from the raw links — clustering nodes by their connection pattern alone, independently
of any declared facet — the **gap** between what it recovers and what was declared becomes
visible. That gap is a δ₁ epistemic signal: the Territory quietly disagreeing with a Map laid
over it. A visualisation that can show the discrepancy between its own encoding and the data's
latent structure is doing something a decorative view cannot.

### 3.4 What is deliberately *not* done

Formalising the stylesheet itself as an OWL+SHACL ontology — giving it classes, shapes,
validation — is **deliberately deferred**. For a single-author prototype it would be
OntologicalOverfitting: machinery heavier than the thing it governs. The principle is
demonstrated here; the formal engine belongs to the mature tool. Naming that boundary is itself
part of the method — a representation should be no more elaborate than its subject earns.

---

## 4. Where this sits, and where it goes

This note describes the **prototype** stage: a serverless HTML artifact
(`TscgCanopyGraphVizProto`, an `m3:Poclet`). The projected mature form is an ElectronJS tool
(`TscgCanopyGraphViz`, an `m3:TscgTool`) able to visualise arbitrary graphs and ontologies, with
a full stylesheet engine.

The honest limitations travel with the idea and belong in any write-up: the current renderer
does not yet scale to the full corpus; magnitude is derived from raw degree rather than from
richer epistemic properties; concentric shells saturate with depth (the nautilus arrangement is
the structural answer); and visual behaviour is verified by eye rather than by machine. A paper
that leads with these is more credible, not less — and the framing as an *exploration path*
rather than an innovation is what those limitations honestly support.

---

## 5. One-paragraph abstract (seed for the paper)

> Graph layouts tend to force a choice between a global picture that collapses into a hairball
> and a local browser with no sense of the whole. Canopée explores a third option: a mobile,
> first-person viewpoint that begins inside the graph — at its barycentre, looking outward at
> nodes-as-stars — and reaches the classic exterior view simply by flying back, with teleport to
> re-centre on any node. Legibility at scale is handled optically, by coupling field of view to a
> brightness (magnitude) limit, so filtering becomes observation. Rendering is driven by a single
> stylesheet that is at once the machine encoding and the on-screen legend, and which — because it
> declares how graph semantics map to visual variables — behaves as a small representation
> ontology, a second-order Map that travels with the view. We present this not as an innovation,
> the egocentric navigation of graphs being decades old, but as an exploration path, and we
> report its current limitations frankly.
