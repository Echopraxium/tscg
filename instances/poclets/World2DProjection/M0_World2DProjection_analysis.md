# TSCG Analysis — World 2D Projection *(former working name: `World2DProjection`)*

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-09-09
**Pipeline**: `tscg-instance-pipeline` — Step 2 (Analysis)
**Status**: Step-2 record (reconciled with HEAD on 2026-09-13 — see update box below). Name frozen: `World2DProjection`.

> All framework facts below were read from HEAD (raw CDN) at analysis time:
> `M3_GenesisGrammar.jsonld` (Facet mechanism), `M1_Domains.jsonld` (domain registry),
> `_01_Facet_as_M3_Principle_ArchitectureNote.md` (Facet criteria). M2 GenericConcept
> names/formulas are **not** asserted here — they must be read from
> `M2_GenericConcepts.jsonld` at Step 3.1.

---

> **Post-analysis update (2026-09-13) — reconciled with HEAD `5880d883`.**
> The Step-2 reasoning below is preserved as written (the Gap *was* real at analysis time);
> this box records what has since happened.
>
> - **Name frozen**: `World2DProjection` (was working name `MapProjections`).
> - **Gap CLOSED**: the `Cartography` domain (`m1:domainCount` 21→22) and the two M1-declared
>   facets (`cartography:DistortionProperty`, `cartography:GraticuleGeometry`) are graved and
>   committed on HEAD; the facet-in-M1 SHACL checkpoint passed.
> - **Doctrinal tension resolved**: `distortionProperty` is graved as a *conferred* classificatory
>   role (see the `rdfs:comment` on `cartography:DistortionProperty`), hence admissible as a facet.
> - **Step 3 done**: `M0_World2DProjection.jsonld` + `M0_World2DProjection_README.md` written;
>   **GATE 1 (SHACL) and GATE 2 (C01–C15) both green**. The *optional orthogonality anchor* is
>   **Gall-Peters** (EqualArea × Cylindrical) — the "second EqualArea in a different graticule"
>   this analysis proposed, contrasted with Mollweide (EqualArea × Pseudocylindrical). 5 anchors total.
> - **Step 3.1 M2 finding**: verified on HEAD — `Transformation` / `Mapping` / `RepresentationShift`
>   are **absent** from `M2_GenericConcepts.jsonld`. The trade-off is fully expressible via existing
>   `Constraint` + `Invariant`, so **no new M2 candidate** is required (alignment, not a new gap).
>   The "representation-shift M2 candidate" roadmap note did **not** materialise on HEAD.

---

## Verdict: Alignment **with a documented Gap**

The system models cleanly with the **already-graved** Facet mechanism (`m3:Facet` / `m3:FacetValue` / `m3:valueOf` / `m3:hasFacetValue`, SC-3). It nonetheless surfaces a genuine **Gap** in the framework, which Michel has decided to close:

1. **No `Cartography` domain.** `M1_Domains.jsonld` registers 21 domains (`m1:domainCount: 21`); cartography / projection / geodesy are **absent**. Decision: register **Cartography** as a legitimate *métier* domain (21 → 22), on the same footing as Photography / Game Theory / Television Engineering (comparably populated).
2. **Facet-declared-in-M1 is a first.** Only `m3:Audience` is currently graved as a concrete facet, and it lives in M3. M1 extensions today host DomainConceptCombos, not `m3:Facet` individuals. Declaring facets inside an M1 extension is new territory → **SHACL-M1 checkpoint** (confirm the M1 schema accepts an `m3:Facet` in an extension file; adjust the declaration mode otherwise).

Gap has positive value: it drives the Cartography domain into the registry and pilots the M1-declared-facet pattern.

---

## Why this instance is special (reflexive note)

The subject *is* the Territory/Map duality that founds TSCG (M3): the Earth = a **real** Territory (a 2-sphere), each projection = a **real** Map. Rare pedagogical asset ("here the Territory really is a territory"). Discipline: the poclet must model **the system** (projections + distortion), **not** re-derive M3.

---

## ASFID Lens (Territory / Eagle Eye)

- **A (Attractor)** — *weak*. A projection is a fixed transformation, no dynamical convergence; at most the design "target invariant".
- **S (Structure)** — *strong*. The graticule (meridian/parallel network), the sphere→plane geometry.
- **F (Flow)** — *weak*. Coordinate transport by the projection function; no material flow.
- **I (Information)** — *strong*. What is preserved vs lost (angles / areas / distances). The crux.
- **D (Dynamics)** — *weak* statically; **recoverable** as the simulation animates morphing.

Profile: **S + I dominant**, A/F/D weak. A Representation-centred system, not a Dynamics-centred one — unusual in the corpus.

## REVOI Lens (Map / Sphinx Eye) — the rich axis

- **R (Representability)** — *maximal*. Each projection **is** a representation choice.
- **V (Verifiability)** — *high*. Distortion is exactly measurable (Tissot's indicatrix locally; Girard's spherical excess per zone).
- **O (Observability)** — *high*. Distortion is directly visible (Greenland vs Africa on Mercator).
- **E / Im** — *moderate* (history of projections; coordinate/GIS standards).

**Epistemic gap = a theorem.** Gauss's *Theorema Egregium*: a sphere (non-zero Gaussian curvature) admits no isometry to the plane (zero curvature) → **no lossless Map exists**. The gap is proven, not approximate.

---

## The two facets (to declare in `M1_Cartography`)

Facet = the **axis**; its values are **foci** (Ranganathan; per the graved `m3:Facet`/`m3:FacetValue`).

### Facet 1 — `distortionProperty` *(spine)*
- **Foci**: `Conformal` · `EqualArea` · `Equidistant` · `Compromise`
- **Métier-grounded**: attested as "distortion property" (ITC Living Textbook) / "metric property" (map-projections.net). Chosen over `preservedInvariant` because that name excluded `Compromise` (which preserves *no* invariant exactly); `distortionProperty` classifies by distortion behaviour, so `Compromise` is a full value.
- **Side**: Map / REVOI / Representability. "What the Map refuses to lose."
- **Mutual exclusivity** of foci (Theorema Egregium: conformal ⊥ equal-area) ⇒ a closed value-set on one axis ⇒ **4 foci = minimal *and* complete** for the epistemic structure.
- **Contract-on-value (geopolitics)**: foci carry non-neutral weight — `EqualArea` championed (Peters, 1970s) for fair Global-South representation; `Conformal` tied to navigation. Attach as properties **on the foci** (the graved `m3:FacetValue` may carry contractual obligations), not as a separate axis. This is the poclet's punchline: the epistemic choice is never neutral.

### Facet 2 — `graticuleGeometry` *(secondary)*
- **Foci**: `Cylindrical` · `Conic` · `Azimuthal` · `Pseudocylindrical` (extensible: `Pseudoconic`, `Pseudoazimuthal`, `Polyconic`, `Circular`)
- **Métier-grounded**: the **modern** classification "by the shape of the meridian/parallel network" i.e. the graticule (Lapaine & Frančula, 2022) — more rigorous than "developable surface", which covers only 3 families and is academically contested (a pseudocylindric maps to a non-developable surface). This is why `developableSurface` was rejected.
- **Value-set choice (assumed asymmetry)**: adopts the rigorous graticule-shape classes, **not** map-projections.net's looser "Group" column (which mixes in `Polyhedral` / `Lenticular` / `Miscellaneous` — not graticule shapes). For Facet 1 the site term *was* the rigorous term; for Facet 2 it is not, so this is an intentional upgrade — a semantic call Michel has taken.
- **Side**: Territory / Structure.

### Orthogonality (facet admission criterion 1) — satisfied, but grid is not full
Knowing `distortionProperty` does **not** fix `graticuleGeometry`: Conformal exists as Cylindrical (Mercator), Conic (Lambert CC), Azimuthal (Stereographic). Criterion met. **But orthogonal ≠ freely combinable**: several cells are impossible (Conformal × Pseudocylindrical is degenerate — conformality needs an orthogonal graticule everywhere). ⇒ **NOT a 4×4 = 16 Cartesian product.** The poclet is not a product of the two facets.

### Doctrinal tension to resolve (Michel's call)
The graved semantics say a facet is **conferred, contingent, Map-perspective, non-derivable**. `graticuleGeometry` fits cleanly (a conferred construction choice). `distortionProperty` is *checkable from the projection's math* (angular distortion ≡ 0 ⇒ conformal), so under a strict reading of "non-derivable" it needs a ruling. Working reading: it is a **conferred classification** (a cartographic category one *assigns*), not a bucket derived from a TSCG score like `spectralClass` — therefore admissible. To confirm at the ontology worksite.

---

## Anticipated M2 GenericConcepts *(to verify at Step 3.1 — HEAD)*

Not asserted from memory. Candidate *themes* to check against `M2_GenericConcepts.jsonld`: a Representation / Modelisation concept, a Transformation / Mapping concept, a Constraint / Tradeoff concept. **Read HEAD before listing any formula.**

> Possible roadmap resonance *(memory archive says: a "representation-shift / diff between two Maps of one Territory" M2 candidate may be open — verify on HEAD)*: this poclet is its natural concrete pilot (the morph between two facet-values is literally that diff). One data point, not a proof; the M3-admission bar (recurrence across unrelated domains) is not cleared by a single poclet.

---

## Comparison with existing instances

- **ExposureTriangle** — closest structurally (a trade-off among parameters).
- **FireTriangle** — canonical reference pattern for M0 + README + SHACL.
- **ColorSynthesis** — precedent for a family with several related instances/variants.
- **Triz** — reference pattern for the 3D-globe rotation (bring the selected zone's centroid to face the camera).
- **PlateTectonics**, **QRCodeToPocketCity** — precedents for a 2D + 3D multi-render-context simulation (beyond the single-canvas template).

---

## Three-layer split (only M0 depends on "how many")

1. **M1 — skeleton (frozen, small)**: `m1:domain:Cartography` in `M1_Domains.jsonld` + the two facets in `M1_extensions/cartography/M1_Cartography.jsonld`. → **ontology worksite** (`tscg-ontology-diagnosis-pipeline`; gates: linter / Pellet / SHACL-M1).
2. **M0 — instances**: ~4–6 **canonical anchors** (poclet-grade, full TSCG treatment) + an *optional* light catalogue (tens of records, generated from a table à la map-projections.net — **not** hand-written, not poclet-grade). Anchors are **clients** of the M1 facets.
3. **Simulation (Step 4) — rich, parametric**: hundreds of *rendered* projections via sliders, without as many M0 files. Client of M0; links point up to the ontology.

The count the **user sees** is large (parametric); the count of **named M0 instances** stays controlled. This dissolves the "4 is too few" concern: parsimony lives in M0 (correct), profusion lives in the simulation (correct).

### The 4 canonical anchors

| Instance | `distortionProperty` | `graticuleGeometry` |
|---|---|---|
| Mercator | Conformal | Cylindrical |
| Mollweide *(or Gall-Peters)* | EqualArea | Pseudocylindrical *(or Cylindrical)* |
| Azimuthal Equidistant | Equidistant | Azimuthal |
| Robinson | Compromise | Pseudocylindrical |

*Optional extra anchor to prove facet orthogonality*: a second EqualArea in a different `graticuleGeometry` (same distortionProperty, different graticule) — earns its place by teaching orthogonality.

---

## Simulation design (Step 4 — consolidated spec)

Two stacked horizontal panels = the Territory/Map duality made interactive.

**Bottom panel — 3D globe (the Territory)**
- Uniform **beige**, black background; **neutral referent** (the Territory never colours itself with distortions).
- Selected zone outlined with a **thick black contour**.
- Rotation à la **Triz**: bring the zone centroid to face the camera (slerp / quaternion).

**Selection = zones, not points**
- Categories: country · state/province · continent · **polar/ocean region** (Arctic = the flagship demo — Mercator explodes at the poles).
- **Consequence — forward-only**: projecting known-(lat,lon) zone vertices to 2D and onto the globe needs no inverse. The earlier "closed-form inverse?" criterion is **dropped** — Robinson/Winkel/compromises are no longer blocked by numerical inversion.

**Top panel — 2D projection (the Map)**
- **Diverging choropleth** on `r = area_2D / area_sphere` (each normalized), three regions sharing one neutral hinge:

  | Region | Condition | Colour |
  |---|---|---|
  | Oversized | `r > 1 + τ` | light grey → **magenta** (intensity ↑ with departure) |
  | Neutral | `1 − τ ≤ r ≤ 1 + τ` | flat **light grey** |
  | Undersized | `r < 1 − τ` | light grey → **cyan** (intensity ↑ with departure) |

  - **Continuity at the borders**: hue departs from light grey at `1 ± τ` (no hard jump); light grey is both the neutral fill and the floor of both gradients.
  - **Intensity in log** `|log r|`: the oversized side is unbounded (Mercator → ∞ at the poles), so log makes both sides symmetric and legible. `τ` acts linearly around 1 (intuitive).
  - **`τ` = a slider** (tolerance). This is itself a TSCG lesson: "fair share" (r ≈ 1) is a **convention of the Map**, not a fact of the Territory — the user chooses the neutral band's width.

- **Honest caveat (pedagogical choice)**: the choropleth measures **area** only → on an **EqualArea** projection everything is neutral grey, though shapes are badly distorted. Do not let the user read "no distortion". Resolution: when the active `distortionProperty = EqualArea`, **switch the hue to shape distortion** (Tissot anisotropy a/b); always show an explicit legend ("hue = area distortion" / "shape distortion"). The colour then reads *what the active facet sacrifices* — more TSCG.

**Morphing** (on facet / scalar change)
- **Intra-family scalar** (cylindrical stretch, azimuthal eye position) → **exact**, continuous by nature.
- **Across facet-values** (Conformal→EqualArea, Cylindrical→Azimuthal) → interpolate (x,y) source→target by *t*. Smooth, but **transient views are NOT ontological instances** — do not reify them in M0.
- The **globe (Territory) does not move**; only the Map morphs, and the green/… zone deforms toward/away from its true form. This is the **epistemic gap animated**: Territory unchanged, Map revisable.

**Measurement**
- **Zone area on the sphere** = Girard's spherical excess (`A = R²·(Σθᵢ − (n−2)π)`), or a spherical-shoelace line integral over GeoJSON (lat/lon) edges. This is the **reference denominator** of distortion; **Tissot** is its infinitesimal (per-point) version. Caveat: GeoJSON edges are linear in (lat,lon), not great-circle arcs — negligible at poclet scale, but noted.

**Data dependencies (simulation, NOT ontology)**
- Zone boundaries = **GeoJSON** (Natural Earth, public domain). Countries are *not* M0 instances. Projection math lives **in the code** (code derives from M0, never a rival source of truth; links point up).

**Colour grammar (no collisions)**
- cyan / magenta / grey = distortion (2D Map) · thick black contour = selection · beige = neutral globe (Territory). Magenta/cyan sit outside the ASFID/REVOI palette.

---

## Recommended decision & sequencing

1. **Freeze the name** (becomes IRIs).
2. **Ontology worksite first** (`tscg-ontology-diagnosis-pipeline`): register `m1:domain:Cartography`; create `M1_Cartography` with the two facets; pass linter / Pellet / **SHACL-M1** (facet-in-M1 checkpoint).
3. **Then the poclet** (this pipeline, Step 3): the 4 anchors as clients (`m1:domain: "Cartography"` + `m3:hasFacetValue` → M1 foci); README; SHACL-M0.
4. **Then Step 4** simulation, iterative, Michel-piloted.

**Single artifact**: a poclet (anchors) is sufficient; the parametric simulation carries the profusion, so a separate explorer TscgTool is likely unnecessary — confirm.
