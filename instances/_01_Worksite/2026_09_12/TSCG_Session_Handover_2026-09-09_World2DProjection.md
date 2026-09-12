# TSCG Session HandOver — `World2DProjection` poclet

**Date**: 2026-09-09 · **Author**: Echopraxium with the collaboration of Claude AI
**This session did**: Step 1 (Proposition) + Step 2 (Analysis) of the instance pipeline, and an **ontology lot** (new Cartography domain + first M1-declared facets + instance-vocabulary reform + tooling move). Gates green for the lot; committed/ready to commit.
**Next session goal**: **Step 3 — model `M0_World2DProjection`** (the M0 + README), then **Step 4 — standalone HTML simulation**.

---

## 0. Bootstrap (do this first)

1. Load skills by name: `head-over-memory`, `tscg-instance-pipeline`, `tscg-create-instance-simulation` (and `tscg-ontology-diagnosis-pipeline` only if touching the ontology again).
2. Fetch the Smart Prompt from HEAD and follow it.
3. **HEAD is the only authority.** The M1 lot below should be committed by the time you read this — re-verify every framework fact (facet IRIs, domain entry, foci names, `m1:Domain`) from HEAD before relying on it. This document is a pointer, not a source of truth.

---

## 1. Delivered this session (verify on HEAD)

- **`M0_MapProjections_analysis.md`** (Step 2) — full ASFID/REVOI diagnostic, facet design, three-layer split, and the complete simulation spec. *(Working name was `MapProjections`; final name is `World2DProjection` — rename the file/contents when convenient.)*
- **Ontology lot "Cartography domain + instance-vocabulary reform"**:
  - `M1_extensions/cartography/M1_Cartography.jsonld` (**new**) — first M1-declared facets under the SC-3 `m3:Facet` mechanism, namespace prefix **`cartography:`**:
    - `cartography:DistortionProperty` (closed) → `Conformal · EqualArea · Equidistant · Compromise`
    - `cartography:GraticuleGeometry` (extensible) → `Cylindrical · Conic · Azimuthal · Pseudocylindrical`
    - geopolitical contract-on-value in `rdfs:comment` on `Conformal`/`EqualArea`.
    - `@context` includes `m3:eagle_eye` / `m3:sphinx_eye` (required by check_M1).
  - `M1_Domains.jsonld` — `+ m1:domain:Cartography` (domainCount 21→22, totalInstances 26→27); **rename** `m1:pocletCount`/`pocletExamples` → `m1:instanceCount`/`instanceExamples` (22 each) + generic "poclet"→"instance" wording (typed mentions kept).
  - `M1_CoreConcepts.jsonld` v2.10.0 — declared `m1:instanceCount` (xsd:integer) + `m1:instanceExamples` (xsd:string); **also declared the `m1:Domain` class** (owl:Class, rdfs:subClassOf owl:Thing) — it had been used implicitly on 22 entries but never declared (this resolved 2 linter "undefined domain" warnings).
  - `M1_Schema_shacl.ttl` — `+ FacetShape`, `FacetValueShape`, `DomainShape` (guard-rails; forbid retired `poclet*`).
- **Tooling**:
  - Moved `cli_tools/ontology-linter/` → **`ontology/cli-tools/ontology-linter/`** (linter is self-contained; no path deps; no external references to fix). New invocation from that folder: `python ontology_linter.py ../../<ontology-file>`.
  - `ontology/cli-tools/_run_all_layers.bat` — rewritten (CRLF) to **stay open** via `cmd /k` (the old `pause` was being skipped on double-click).

### Gate results (this session)
- **ontology_linter**: all files PASSED. `M1_Cartography` clean; the other files carry only the baseline `@base` warning (repo-wide, do not "fix" — it keeps relative IRIs working).
- **check_M1.py --shacl** on `M1_Cartography`: **0 errors / 0 warnings / SHACL: conforms** ✅ (exercises DomainShape/FacetShape/FacetValueShape; negative tests bite).
- **run_all_layers.py**: `GATE: FAIL` — but **baseline**, not ours. Proven: HEAD *without* this lot gives the identical `shacl_violations 664 / expected 680 (-16)`. The lot is **neutral** on the count. See §2.4.
- **Pellet reasoner**: pending on Windows (Java) — optional; risk near-nil (lot adds individuals + properties + one class only).

---

## 2. Open items

1. **Namespace** — kept **`cartography:`** (dedicated prefix, mirrors the Audience precedent). The documented repo convention `m1:extension:<domain>:` is an alternative that was **not** adopted; revisit only if you want uniformity with domain *concept* IRIs.
2. **Counter derivability** *(deferrable, hygiene)* — `instanceCount` is a pure rename (values unchanged), so inherited inconsistencies remain (e.g. BusinessModeling `instanceCount:0` yet 1 framework). Optional lot: recompute `instanceCount = len(instanceExamples)` + a SHACL `sh:sparql` constraint.
3. **`m1:systemicFrameworkCount`** *(deferrable)* — kept as-is (1×, Bmc). Keep as sub-counter or absorb into `instanceCount` (with `m1:instanceType` carrying the kind)?
4. **Golden debt (hygiene, NOT ours)** — `run_all_layers` shows `shacl_violations 664 vs golden 680 (-16)`, present on pure HEAD before this lot: `golden_values.json` is stale (16 violations were removed earlier without `--update-golden`). **Do NOT `--update-golden`** just to green the gate — the repo warns a drop can mean "a shape stopped biting". Investigate the antecedent debt separately (SC-6 / a golden-reconciliation pass).
5. **SC-6 debt (NOT ours)** — `check_M1 --shacl` without `--file` shows **7 SC-1 errors** on M1_CoreConcepts combos (monoidal operator inside combo formulas), plus the wider SHACL debt. All baseline, flagged for SC-6. Our lot adds zero.

6. **Tooling gap — undeclared-term guard (NEW, from this session's lessons)** — TSCG-namespace terms can be *used* without ever being *declared*, and it slips through every gate. Hit twice this lot: `m1:Domain` (implicit class on 22 entries) and `m1:pocletCount`/`pocletExamples` (never declared). Why undetected: the linter's `_check_owl_semantics` only checks `rdfs:domain`/`rdfs:range` of *already-declared* properties — it does not check `@type` values nor predicates; SHACL validates shapes on typed nodes, so a missing *declaration* is invisible to it.
   **Proposed guard (per layer M0–M3):** collect every `m0:/m1:/m2:/m3:` term appearing as (a) a `@type` object, (b) a predicate, (c) an `rdfs:domain`/`range` / `sh:class` / `sh:path` target; verify each has a declaration (`owl:Class` | `owl:*Property` | `rdf:Property`).
   - **Cross-layer resolution is mandatory**: check against the **merged graph (layer + imported parents)**, not the file alone — else massive false positives (e.g. `m3:Facet` used in M1 is declared in M3). Exclude external vocabularies (owl/rdfs/skos/dcterms/xsd/rdf).
   - **Roll out like golden values**: the repo already carries undeclared-term debt → don't hard-fail on the backlog. Measure the baseline, store it in `golden_values.json` as `undeclared_terms`, wire it into `run_all_layers`, gate on **no increase** (new undeclared term = FAIL; a drop = a repair → `--update-golden`). Note: declaring `m1:Domain` this session already reduced this debt by one.
   - **Where**: extend the linter's `_check_owl_semantics` (it already builds `defined_terms`) and/or a dedicated check invoked by `run_all_layers`. Severity: error, once baselined. A worthwhile standalone session.

---

## 3. NEXT — Step 3: model `M0_World2DProjection` (BEFORE the simulation)

The simulation is a **client** of M0 (code derives from M0). Model M0 first.

- **Path**: `instances/poclets/World2DProjection/M0_World2DProjection.jsonld` + `M0_World2DProjection_README.md`
- Follow the **FireTriangle** reference pattern. Must pass **GATE 1** (`validate_m0_instance.py`) + **GATE 2** (`check_m0_instances.py`, C01–C15).
- `m1:domain: "Cartography"`.
- **4 canonical anchors**, each carrying `m3:hasFacetValue` → the M1 foci (`cartography:distortionProperty.*`, `cartography:graticuleGeometry.*`):

  | Anchor | distortionProperty | graticuleGeometry |
  |---|---|---|
  | Mercator | Conformal | Cylindrical |
  | Mollweide *(or Gall-Peters)* | EqualArea | Pseudocylindrical *(or Cylindrical)* |
  | Azimuthal Equidistant | Equidistant | Azimuthal |
  | Robinson | Compromise | Pseudocylindrical |

  Optional 5th anchor to *prove* facet orthogonality (same `distortionProperty`, different `graticuleGeometry`).
- **M0 stores classification + metadata only** (author, year, facet-values, family, param range). **Projection MATH lives in the simulation code**, never in M0 (links point up).
- **ASFID**: S+I dominant. **REVOI**: Representability / Verifiability / Observability strong.
- **Epistemic gap = Theorema Egregium** (formal proof — put it in the README). Store `m0:epistemicGap` as a **plain `xsd:float` in [0,1]**, NOT a structured object (Group-C C15 lesson).
- **M2 concepts**: read `M2_GenericConcepts.jsonld` on HEAD at Step 3.1 — do NOT recite from memory. Candidate themes: Representation, Transformation/Mapping, Constraint/Tradeoff. Possible `RepresentationShift` resonance — verify on HEAD.

---

## 4. Step 4 — standalone HTML simulation (consolidated spec)

Serverless single `.html` (start from `instances/poclets/_00_template/`). Driven by `tscg-create-instance-simulation`. **Two stacked horizontal panels = the Territory/Map duality made interactive.**

- **BOTTOM — 3D globe (the Territory)** · BabylonJS/Three. Uniform **beige**, black background, **neutral referent**. Selected zone = **thick black contour**. Rotation à la **Triz**: bring the zone centroid to face the camera (slerp/quaternion).
- **TOP — 2D projection (the Map)** · p5.js. **Diverging choropleth** on `r = area_2D / area_sphere` (normalized), three regions sharing one neutral hinge:
  - `r > 1+τ` oversized → light-grey → **magenta**
  - `1−τ ≤ r ≤ 1+τ` neutral → flat **light grey**
  - `r < 1−τ` undersized → light-grey → **cyan**
  - **intensity in log** `|log r|` (oversized side unbounded at poles); `τ` linear around 1.
  - **`τ` = a user slider** (tolerance = a Map convention → itself a TSCG lesson).
  - **continuity at borders** (light grey = shared hinge/floor).
  - **hue measures AREA** → on an EqualArea projection everything is neutral grey though shapes are distorted; when active `distortionProperty = EqualArea`, **switch hue to shape distortion** (Tissot a/b); always an explicit legend.
- **Selection = ZONES, not points** (country / state / continent / polar region). **Arctic = flagship** (Mercator explodes at the poles). ⇒ **forward-only** (project known-(lat,lon) vertices) — **no numerical inverse needed**.
- **Morphing**: (a) intra-family scalar = exact; (b) across facet-values = interpolate (x,y) source→target by *t* (transient views, **NOT M0 instances**). The **globe does not move**; only the Map morphs — the epistemic gap animated.
- **Area measurement**: Girard spherical excess / spherical-shoelace over GeoJSON (lat/lon). Tissot = the infinitesimal version.
- **Data (simulation, NOT ontology)**: zone boundaries = **GeoJSON** (Natural Earth, public domain). Countries are not M0 instances.
- **Richness** = zones × projections × parametric morphing (hundreds of rendered views) while **M0 stays small** (~4 anchors). Colour grammar: cyan/magenta/grey = distortion (2D Map); thick black contour = selection; beige = neutral globe.

---

## 5. Commit + housekeeping (this session)

- **Order matters**: `git add -A` → `python tscg_generate_filetree.py` (reads `git ls-files`, so add first) → `git add docs/reboot-kit/TSCG_FileTree.md` → commit → push.
- Files: `M1_Cartography.jsonld` (new), `M1_Domains.jsonld`, `M1_CoreConcepts.jsonld`, `M1_Schema_shacl.ttl`, the linter move, `_run_all_layers.bat`, regenerated `TSCG_FileTree.md`. (Analysis + this HandOver: commit as session docs, or later with the M0.)
- Do **not** commit `gate_report.txt` (leftover from the old .bat) — gitignore or delete.
- After push: **reload the FileTree into Project Knowledge** (it changed).

## 6. Formal gates to run on Windows

- Pellet reasoner (`owl_reasoning_test`) on the M1 layer.
- `check_M1.py --shacl` from `ontology/cli-tools/` (per-file on Cartography = 0/0; whole-M1 shows the 7 baseline SC-1 errors — not ours).
- `run_all_layers.py` — expect the baseline `664 vs 680` FAIL (not ours; do not `--update-golden`).
