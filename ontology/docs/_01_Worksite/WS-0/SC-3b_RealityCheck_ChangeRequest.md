# SC-3b — Change Request: the `RealityCheck` facet
## Ontology-Diagnosis Pipeline — Phase 0 (awaiting Michel's approval)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-19
**Base**: HEAD `fee9ba8` (the 2026-10-18 epistemology patch is not yet on HEAD)
**Origin**: `docs/CoreHypotheses/ModelSupersession.md` §3.5 (proposal) — Michel chose
**option (a)**: grave optional first, migrate, then make mandatory.
**Precedent**: SC-3 (`2026_09_02/SC-3_Facet_Decision_Record.md` v2.0.0) — the Facet
mechanism and the `Audience` facet.
**Status**: ❌ **WITHDRAWN (Michel, 2026-10-19)** — kept as a documented dead end.
`RealityCheck` labels the *kind* of a paradigm; it classifies without explaining and
quietly ranks (Experimentable first, Dream last). Replaced, as a principle, by **declared
criteria** — see `docs/CoreHypotheses/ContextSwitching.md` §3.4–§3.5. No facet is planned
for paradigms, until further notice. Nothing below was ever graved.

---

## 1. What and why

**What.** A second facet on the existing M3 Facet mechanism: `RealityCheck`, recording
**what kind of paradigm an M0 maquette stands in**, as the paradigm claims it for itself.
Eight values: `Experimentable` · `Formalised` · `Fiction` (label *Alternative Paradigms*)
· `Dream` · `Religion` · `Ideology` · `Myth` · `CulturalArtifact`.

**Why.** The epistemological postulate (ModelSupersession §0; LayerCake §1): an M0
maquette may stand in any coherent paradigm — science, myth, fiction… — provided it
**states clearly which kind**. Today nothing in the ontology carries that statement.

## 2. Three steps (option a)

| Step | Content | Files | Gate effect |
|---|---|---|---|
| **1 — Grave, optional** | `m3:RealityCheck` (`a m3:Facet, skos:ConceptScheme`) + 8 `m3:FacetValue` individuals in `M3_GenesisGrammar.jsonld`; AXIS registry updated | M3_GenesisGrammar, `validator/checks/axis.py` (+ a negative test) | No count should move |
| **2 — Migrate** | One `m3:hasFacetValue {"@id": "m3:realityCheck.<Value>"}` per M0 instance (42 after the patch), from a value table **validated by Michel before any edit** | 42 `M0_*.jsonld` | No count should move (values are registered IRIs) |
| **3 — Make mandatory** | M0 SHACL: exactly one `RealityCheck` value per instance (qualified shape on `m3:valueOf m3:RealityCheck`) | `check-M0/M0_Instances_Schema_shacl.ttl` | New shape; 0 violation expected after step 2 |

Each step is its own lot, with Phases 1–5 of the pipeline.

## 3. The legitimacy test — to pass before step 1

SC-3 v2.0.0 §7 carries two criteria that disqualified NATURE, SCALE and PERIMETER.
`RealityCheck` must pass them.

**Conferred / contingent / Map-perspective.** Plausibly yes: the value is *attributed*
from a source (the paradigm's own claim), it can change (a paradigm may reframe itself),
and it concerns how a paradigm presents its knowledge — Map side.

**Axis filter — orthogonal to existing axes and non-derivable from them.** This is the
real risk, on two fronts:

- **vs the backbone (`ontologyType`).** Partial correlation is expected: a
  SymbolicSystemGrammar ("neither prescriptive nor empirically arbitrated") will often be
  `CulturalArtifact` or `Myth`. Correlation is tolerated; *derivability* is not.
- **vs DOMAIN (SC-5).** The sharper risk: `Mythology → Myth`, `Physics → Experimentable`,
  `Mathematics → Formalised`. If the value were always deducible from the domain,
  `RealityCheck` would be a derived axis — like PERIMETER, rejected for that reason.
  The counter-argument: the domain is the *subject field*, `RealityCheck` the *paradigm's
  claim*; Aristotelian physics and a Norse cosmology of earthquakes do not share a value
  even when they share a subject.

**Proposed proof (falsifiable).** Step 2's value table, built *before* any graving
commit, doubles as the orthogonality measurement: for the 42 instances, cross the
proposed value with `ontologyType` and with the declared domain. If the value is a
function of either, the facet fails the axis filter and the lot stops at Phase 0.
**This means: build the step-2 table first, then grave step 1 only if the test passes.**

## 4. Decisions reserved for Michel

- **D1 — Proceed under the axis-filter risk**, with the orthogonality test of §3 run
  first (value table before graving)?
- **D2 — Names.** Axis `m3:RealityCheck`; values `m3:realityCheck.<Value>`
  (SC-3 naming convention (A), as `m3:audience.<Value>`); `skos:prefLabel` "Alternative
  Paradigms" on `Fiction`. British spelling `Formalised`.
- **D3 — Source of the value.** At step 2, is the author's declaration enough (the value
  is justified in the instance README), or does each instance cite a source? The lighter
  form is proposed; a per-instance source property would be a new mechanism to pay for.
- **D4 — Tooling.** `axis.py` hard-codes the ratified facet values (`_FACET_VALUES`,
  Audience only); its own docstring plans to "load from M3_GenesisGrammar" so the two
  cannot drift. Proposed: do that refactor in step 1 (with a negative test in
  `validator/tests/`), rather than extend the literal.
- **D5 — First mandatory facet.** SC-3 Decision #2 made Audience optional (reversing
  v1's `minCount 1`). Step 3 makes `RealityCheck` the first *mandatory* facet. Confirm
  this is intended for this axis.

## 5. Notes for Phase 1 / Phase 5

- `M3_GenesisGrammar.jsonld` is at 4.17.0 with **7** `m3:changelog` entries (the M3
  maximum): a new entry drops the oldest (4.11.0).
- The only existing M0 facet guard (`m0:ForbidStringHasFacetValueShape`) is generic and
  already covers `RealityCheck` values; step 1 needs no SHACL change.
- No M0 instance currently uses `m3:hasFacetValue` for `Audience` except
  QRCodeToPocketCity / World2DProjection — to re-check at Phase 1.
- Baseline (`run_all_layers.py`) to be taken on HEAD **after** the epistemology patch is
  applied (it removes one M0 file).
