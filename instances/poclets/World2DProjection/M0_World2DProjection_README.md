# World 2D Projection — TSCG Instance (Poclet)

**Author:** Echopraxium with the collaboration of Claude AI
**Domain:** Cartography · **Type:** `m3:Poclet` · **Version:** 1.0.0 · **Created:** 2026-09-13
**Files:** `M0_World2DProjection.jsonld` (this README) — simulation to follow (Step 4)

---

## Overview

Projecting the round Earth onto a flat sheet is the **Territory → Map** relation made
literal. It is therefore the canonical poclet for the single distinction on which the
whole TSCG framework rests: what a system **is** (the globe, the *Territory*, read
through ASFID / the Eagle Eye) versus how a system is **known** (the flat map, the
*Map*, read through REVOI / the Sphinx Eye).

This poclet does **not** compute projections. It **classifies** five canonical world
projections along two orthogonal cartographic facets, and it names — and proves — the
**irreducible epistemic gap** between globe and map. The projection mathematics belongs
to the Step-4 simulation (the map is a *client* of this model); the M0 stores
classification and metadata only.

---

## System Description

A map projection is a rule that sends every point `(lat, lon)` of the sphere to a point
`(x, y)` of the plane. Gauss proved (see *Epistemic Gap*) that **no such rule can be
distance-preserving**, so every projection must sacrifice something. Which invariant it
chooses to keep, and how it draws the meridian/parallel network, are the two
classification axes of this poclet.

### The five anchors

| Anchor | Author (year) | Distortion property | Graticule geometry |
|---|---|---|---|
| **Mercator** | Mercator (1569) | Conformal (angles) | Cylindrical |
| **Mollweide** | Mollweide (1805) | Equal-area | Pseudocylindrical |
| **Azimuthal Equidistant** | classical / Postel (1581) | Equidistant (from centre) | Azimuthal |
| **Robinson** | Robinson (1963) | Compromise (none exact) | Pseudocylindrical |
| **Gall-Peters** | Gall (1855) / Peters (1967) | Equal-area | Cylindrical |

The first four span the **closed tetra-lemma** of distortion properties
(Conformal · Equal-area · Equidistant · Compromise). **Gall-Peters is the fifth on
purpose**: it proves the two facets are independent (below).

---

## TSCG Analysis

### ASFID State (Territory / Eagle Eye)

Root scores describe the **projection-as-Map** profile; `territorySpace` describes the
**globe-as-observed**. The house convention (cf. FireTriangle) is that the root ASFID
scores are the Map-side profile.

| Dim | Map score | Reading |
|---|---|---|
| **A** Attractor | 0.55 | Each projection tends toward preserving its chosen invariant. |
| **S** Structure | **0.90** | The graticule geometry is the projection's defining skeleton. |
| **F** Flow | 0.35 | A projection is a static point-to-point mapping (flow appears only under morphing). |
| **It** Information | **0.85** | It encodes exactly *which* metric invariant is preserved. |
| **D** Dynamics | 0.45 | Only the parametric family / morphing is dynamic. |

**S + It dominant** — the projection is a *structural-informational* object.
`asfidMean = 0.62`.

### REVOI State (Map / Sphinx Eye)

| Dim | Score | Reading |
|---|---|---|
| **R** Representability | **0.95** | Projections are the paradigm of representation. |
| **E** Evolvability | 0.70 | New compromise projections keep appearing (Robinson 1963, Natural Earth 2011). |
| **V** Verifiability | **0.90** | Distortion is exactly measurable (Tissot, Girard); Theorema Egregium is proven. |
| **O** Observability | **0.90** | Distortion is naked-eye visible (Greenland vs Africa). |
| **Im** Interoperability | 0.85 | Standardised and shared via EPSG codes / PROJ / OGC. |

**R / V / O strong.** `revoiMean = 0.86` — an excellent Map.

### Epistemic Gap — the Theorema Egregium

```
epistemicGap  δ₁ = |asfidMean − revoiMean| / √2
                 = |0.62 − 0.86| / √2
                 = 0.17        →  spectralClass = Liminal  (0.15 ≤ δ₁ < 0.30)
```

The scalar is only the surface. The **deep** gap here is not statistical — it is a
**theorem**, which is exactly why this poclet is the archetype of the Map/Territory
distinction:

> **Theorema Egregium (Gauss, 1827).** The Gaussian curvature `K` of a surface is
> intrinsic: it is invariant under any *isometry* (any distance-preserving map).

**Consequence for cartography (formal argument):**

1. For the sphere of radius `R`, Gaussian curvature is `K_sphere = 1/R² > 0`
   (constant, everywhere positive).
2. For the plane, `K_plane = 0` everywhere.
3. An isometry preserves Gaussian curvature pointwise (Theorema Egregium).
4. A distance-preserving map sphere → plane would be an isometry, hence would require
   `K_sphere = K_plane`, i.e. `1/R² = 0` — **contradiction**.
5. Therefore **no distance-preserving projection of the sphere onto the plane exists.**
   Every projection *must* distort; it can at best preserve *one* metric invariant
   (angle, **or** area, **or** distance-along-select-lines) while sacrificing the others.

This is the **irreducible epistemic gap**: the Map can be made arbitrarily good along a
chosen axis, yet can *never* equal the Territory. The Liminal δ₁ is not a defect to be
tuned away — it is the lesson.

---

## The two facets, and why they are orthogonal

The Cartography M1 extension declares two facets under the SC-3 `m3:Facet` mechanism:

- **`cartography:DistortionProperty`** *(closed, Map/REVOI side)* — which invariant is
  preserved: `Conformal · EqualArea · Equidistant · Compromise`.
- **`cartography:GraticuleGeometry`** *(extensible, Territory/Structure side)* — the
  construction family: `Cylindrical · Conic · Azimuthal · Pseudocylindrical`.

Each anchor carries both via `m3:hasFacetValue` (IRI-only, multi-valued).

**Orthogonality is proven inside the anchor set:**

- **Mollweide vs Gall-Peters** — same `distortionProperty = EqualArea`, different
  `graticuleGeometry` (Pseudocylindrical vs Cylindrical).
- **Mollweide vs Robinson** — same `graticuleGeometry = Pseudocylindrical`, different
  `distortionProperty` (EqualArea vs Compromise).

The two facets cross-cut the anchors; neither is derivable from the other — the defining
test of a genuine Ranganathan facet.

---

## GenericConcepts Mobilized (11)

Formulas read from `M2_GenericConcepts.jsonld` at HEAD (× Territory · + Map · | Stereopsis).

| Concept | Formula | Role in the poclet |
|---|---|---|
| **Representation** | `It × St` | A projection *is* a representation of the globe. |
| **Constraint** | `St × A × D \| O + V` | Theorema Egregium: the irreducible trade-off. |
| **Invariant** | `St × A` | Each projection preserves exactly one metric invariant (or none). |
| **Signature** | `It × Ss \| V` | Tissot's indicatrix — the local distortion signature. |
| **Modelisation** | `D × F × It \| R + V + E` | The map as a knowable model of an un-fully-knowable Territory. |
| **Gradient** | `F × T`  or  `It × T` | Distortion grows with latitude (Mercator) / radius (Azimuthal). |
| **Symmetry** | `St` | The graticule symmetry of each family. |
| **Topology** | `St \| L` | Sphere vs plane — the un-preservable relation. |
| **Space** | `St \| L` | Maps sphere-space onto plane-space. |
| **Observer** | `It × A` | *Which* invariant to keep is an observer's (Map-side) choice. |
| **Polarity** | `St × It × A` | Over- vs under-sized area — the diverging choropleth of the simulation. |

**M2 finding (Step 3.1):** no new M2 candidate is required. The HandOver's tentative
`Transformation` / `Mapping` / `RepresentationShift` are **not** present in M2 on HEAD,
and the projection trade-off is fully expressible with existing `Constraint` +
`Invariant`. Reported as an honest alignment, not a gap.

---

## Key Insights

1. **The literal Territory/Map poclet.** Globe = Territory (ASFID), flat map = Map
   (REVOI). No other poclet embodies the framework's founding distinction so directly.
2. **The gap is a theorem, not a tuning error.** Theorema Egregium makes the epistemic
   gap *provably irreducible*. δ₁ = Liminal is the point of the exercise.
3. **Two independent facets.** Distortion property (what is preserved) and graticule
   geometry (how it is drawn) are orthogonal — demonstrated, not asserted.
4. **The map is a client of the model.** All projection mathematics is deferred to the
   simulation; M0 links point *up* (M0 → M1 → M2 → M3) and store classification only.

---

## Transdisciplinary Analogies

The same *forced-choice-of-invariant* shape recurs wherever a rich source is
lossily represented:

- **Exposure Triangle** (photography) — one exposure cannot optimise motion, depth and
  noise at once.
- **Colour-gamut mapping** (image processing) — squeezing a wide gamut into a smaller
  one preserves hue *or* lightness *or* saturation, not all.
- **Dimensionality reduction** (PCA / t-SNE) — a 2D embedding keeps global variance *or*
  local neighbourhoods — the same Theorema-Egregium-shaped bind.

---

## References

- Gauss, C.F. (1827). *Disquisitiones generales circa superficies curvas* (Theorema Egregium).
- Tissot, N.A. (1859). *Mémoire sur la représentation des surfaces* (indicatrix of distortion).
- Snyder, J.P. (1987). *Map Projections — A Working Manual* (USGS Professional Paper 1395).
- Lapaine, M. & Frančula, N. (2022). Classification of map projections by graticule geometry.

---

## Next — Step 4 (Simulation)

A serverless single-file HTML simulation: a **3D globe** (the Territory, neutral beige)
stacked over a **2D projection** (the Map) with a diverging distortion choropleth and a
tolerance slider. Zone selection is forward-only (project known vertices — no numerical
inverse). Driven by the `tscg-create-instance-simulation` skill; full spec in the
2026-09-09 session HandOver, §4.
