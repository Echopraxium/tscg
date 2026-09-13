# TSCG Session HandOver — `World2DProjection` poclet · Step 4 (Simulation)

**Date**: 2026-09-13 · **Author**: Echopraxium with the collaboration of Claude AI
**This session did**: **Step 3 — modeled `M0_World2DProjection`** (M0 JSON-LD + README) and realigned the Step-2 `analysis.md` (name freeze `MapProjections`→`World2DProjection`, status reconciled with HEAD). **GATE 1 (SHACL) + GATE 2 (check_m0_instances C01–C15) both green.** Committed & pushed.
**Next session goal**: **Step 4 — standalone HTML simulation** of the poclet.

---

## 0. Bootstrap (do this first)

1. Load skills by name: `head-over-memory`, `tscg-create-instance-simulation` (and `tscg-instance-pipeline` for Step-4 context).
2. Fetch the Smart Prompt from HEAD (`docs/reboot-kit/TSCG_SmartPrompt.md`) and follow it.
3. **HEAD is the only authority.** The poclet below is committed by the time you read this — re-verify every fact (anchors, facet-value IRIs, scores) from HEAD before relying on it. This document is a pointer, not a source of truth.

---

## 1. Fresh session state

- **Current HEAD**: `<sha = 9d09e8>` — *confirm with `git show HEAD` (this poclet's commit).*
- **Committed poclet** at `instances/poclets/World2DProjection/`:
  - `M0_World2DProjection.jsonld` — the model (classification + metadata only; **no projection math**).
  - `M0_World2DProjection_README.md` — incl. the formal Theorema-Egregium proof of the irreducible epistemic gap.
  - `M0_World2DProjection_analysis.md` — Step-2 record + the **consolidated simulation spec** (§ "Simulation design").
- **In flight**: nothing (working copy clean).
- **Gate open**: none. Both M0 gates green; SC-6 / golden-debt items are pre-existing and NOT ours (see the 2026-09-09 HandOver §2).

---

## 2. NEXT — Step 4: the simulation (read the spec, don't re-derive it)

The full, consolidated spec already lives on HEAD in TWO concordant places — **read them first**:
- `M0_World2DProjection_analysis.md` → section **"Simulation design (Step 4 — consolidated spec)"**.
- `instances/_01_Worksite/2026_09_12/TSCG_Session_Handover_2026-09-09_World2DProjection.md` → **§4**.

Essential shape (orientation only — authoritative detail is in the spec above):
- **Two stacked panels = the Territory/Map duality made interactive.**
  - **BOTTOM — 3D globe (the Territory)**: uniform beige, black bg, neutral referent; selected zone = thick black contour; Triz-style rotation (slerp/quaternion) to face the zone centroid. BabylonJS/Three.
  - **TOP — 2D projection (the Map)**: p5.js. **Diverging choropleth** on `r = area_2D/area_sphere` (normalized): `r>1+τ`→grey→**magenta**, neutral band→**light grey**, `r<1−τ`→grey→**cyan**; intensity in **log |log r|**; **`τ` = user slider** (tolerance = a Map convention → a TSCG lesson); continuity at the neutral hinge.
  - **EqualArea caveat**: choropleth measures AREA → on an EqualArea projection all-grey though shapes distort → when active `distortionProperty=EqualArea`, switch hue to **shape distortion (Tissot a/b)**; always an explicit legend.
- **Selection = ZONES not points** (country/state/continent/polar). **Arctic = flagship** (Mercator explodes at the poles) ⇒ **forward-only** (project known (lat,lon) vertices — no numerical inverse).
- **Morphing**: intra-family scalar = exact; across facet-values = interpolate (x,y) by *t* (transient views, **NOT M0 instances**). The globe does NOT move; only the Map morphs = **the epistemic gap animated.**
- **Area measure**: Girard spherical excess / spherical-shoelace over GeoJSON (lat/lon); Tissot = its infinitesimal version.

## 3. Reminders / invariants for Step 4

- **The map is a client of M0.** Code derives from the committed M0 (5 anchors + their `m3:hasFacetValue`); links point **up** (M0→M1→M2→M3). M0 is never a rival source of truth.
- **Do NOT reify** morph frames or parametric variants as new M0 instances — richness lives in the simulation, parsimony in M0 (~5 anchors).
- **Data (simulation, not ontology)**: zone boundaries = **GeoJSON** (Natural Earth, public domain). Countries are not M0 instances.
- **Template + stack**: start from `instances/poclets/_00_template/` (`M0_Template.html` + `src/tscg-shell.*`); p5.js (2D) + BabylonJS (3D); serverless single `.html`; CSP + CDN per the `tscg-create-instance-simulation` skill; iterative rounds (interactivity / pedagogy / polish), Michel-piloted, ⏸ after each.
- **Colour grammar (no collisions)**: cyan/magenta/grey = distortion (2D Map) · thick black contour = selection · beige = neutral globe (Territory).
