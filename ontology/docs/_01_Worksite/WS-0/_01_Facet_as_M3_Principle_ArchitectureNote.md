# Facet as an M3 Architectural Principle

**Version**: 0.1.0
**Date**: 2026-07-10
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Change type**: Foundational architecture — explicitation of an implicit principle
**Status**: PROPOSITION (architecture only — no ontology files edited; pending sign-off before graving)

---

## 1. Summary

TSCG **already** classifies its entities along several orthogonal axes — instance
type, concept family, dominant grammar, spectral class, focal class, scoring
status, role grounding, disciplinary domain. Each of these is a *facet* in the
faceted-classification sense (Ranganathan, 1933): an independent axis carrying a
controlled set of values, orthogonal to the others.

The framework has never named this pattern as such. It surfaced concretely only
once, as the M0 `Democratization` facet (2026-06-28), which explicited *one* axis
without recognising that the same shape was already present multiple times across
all layers.

This note proposes to lift **faceting as a principle** to M3, where its two most
foundational instances already live (`ontologyType`), and to register the
remaining facets at their natural layers. It edits nothing. It fixes the
concept, the boundary, the two naming/typing decisions it forces, and its
convergence with the pending Domain-fusion Phase 0.

---

## 2. Diagnosis — faceting is already present, and plural

Inventory of the orthogonal classification axes actually found in the corpus:

| Facet (axis) | Foci (values) | Current layer | Kind |
|---|---|---|---|
| `ontologyType` | Poclet, TscgTool, SystemicFramework, SymbolicSystemGrammar | **M3** | conferred |
| `hasFamily` | Structural, Dynamic, Ontological, … (9 families) | M2 | conferred |
| `hasDominantM3` | Territory, Map, Stereopsis | M2 | derived (from formula) |
| `spectralClass` | Coherent, OnCriticalLine, Liminal, Enigmatic | M0 | derived (from scores) |
| `focalClass` | Emmetropic, SlightlyMyopic, Hyperopic, Astigmatic, … | M0 | derived (from focal score) |
| `scoringStatus` | Complete, Partial, Pending | M0 | state |
| `roleGrounding` | Reused, Designed | M0 | conferred |
| `hasFacet` | Democratization, … | M0 | conferred |
| domain (`appliesToDomains`) | Biology, Optics, … | M1/M2 | conferred |

Reading: `ontologyType` is a facet; it is not alone; `Democratization` did not
*introduce* faceting, it explicited a pattern already instantiated eight other
times. That is the trigger for naming the principle at M3.

---

## 3. The unifying definition (and its boundary)

**A facet is an orthogonal classification axis with a controlled value-set.**

Admission criteria (all required):

1. **Orthogonal** — independent of the other facets; an entity's value on one
   facet does not fix its value on another.
2. **Controlled value-set** — values drawn from a defined enumeration
   (`owl:oneOf`) or a registry of named individuals, not a free continuum.
3. **Classificatory** — it *sorts* entities; it does not measure, generate, or
   compose them.

**Boundary — what is NOT a facet** (this is what keeps the principle from
collapsing into "everything is a facet", per the anti-overfitting discipline):

- **Raw scores** (`scoreA`, `revoiMean`, `focalScore`, …) — continuous
  measurements, not classifications. (Their *bucketed* forms `spectralClass`,
  `focalClass` are facets; the underlying scalars are not.)
- **Grammar primitives** (ASFID, REVOI, TKSL) — generative dimensions of the
  three monoidal grammars. They describe *how a system is constructed*, not
  *how an instance is filed*. This is the correction to an earlier misreading:
  the grammars are not facets.
- **Compositional / structural relations** (`comboOf`, `hasComboComponent`,
  `hasMorphism`, `structuralGrammarFormula`) — meronymy and construction, not
  classification.

---

## 4. Decision A — Facet (axis) vs Focus (value)

In Ranganathan's model the **facet** is the *axis* (`spectralClass`); the
**foci** are the *values* (`Coherent`, `OnCriticalLine`).

The current `m0:Facet` class does **not** follow this: its individuals are
*values* (`m0:facet.Democratization`), so `m0:Facet` in fact names a *focus*, or
a single facet's value-set, not the axis.

Lifting the principle to M3 forces a choice:

- **A1 (clean, recommended)** — `m3:Facet` denotes the **axis**. Then
  `ontologyType`, `hasFamily`, `spectralClass`, … are each typed `a m3:Facet`,
  and their values are **foci** (a companion notion, e.g. `m3:Focus`).
  *Cost:* a terminological cleanup in M0 (`Democratization` is a focus of a
  `Pedagogy`/`Democratization` axis, not an `m0:Facet` individual as currently
  named).
- **A2 (minimal, muddier)** — keep `m3:Facet` meaning the value-registry as M0
  already uses it. *Cost:* the principle stays half-named; the axis itself
  remains unmodelled, which is precisely the gap this note exists to close.

Recommendation: **A1**. The whole point is to name the axis; keeping the
value-registry meaning would re-create the gap at a higher layer.

---

## 5. Decision B — Derived vs Conferred (sub-typing, not exclusion)

Some facets are **conferred** (assigned by a modeller or by usage context:
`ontologyType`, `domain`, `roleGrounding`, `Democratization`, `hasFamily`).
Others are **derived** (computed from something else: `spectralClass` and
`focalClass` from scores, `hasDominantM3` from the structural formula).
`scoringStatus` is neither exactly — it is a **state** of the scoring process.

Rather than *exclude* derived axes (they belong in the list), sub-type them:

```
m3:Facet
 ├─ m3:ConferredFacet   (ontologyType, domain, roleGrounding, hasFacet, hasFamily)
 ├─ m3:DerivedFacet     (spectralClass, focalClass, hasDominantM3)
 └─ m3:StateFacet       (scoringStatus)          ← keep or fold into Conferred?
```

Open sub-decision: whether `scoringStatus` earns its own `StateFacet` kind or is
simply a conferred facet whose value is set by the scoring workflow. Weakest
member of the set; flagged, not resolved.

---

## 6. The M3 model (proposed shape, not graved)

M3's contribution is **the abstraction, not the axes themselves**:

- `m3:Facet` — abstract meta-class of classification axes, with the §3 admission
  criteria expressible as SHACL (orthogonality is documented, controlled
  value-set and classificatory nature are checkable).
- (optionally) `m3:Focus` — the companion notion for values, per Decision A1.
- The two `Facet` sub-kinds of §5.

**Cross-level registration pattern** (mirrors `ontologyType`, which is an M3
property whose values are M3 individuals): M3 *defines what a facet is*; each
layer *declares its own facets* by typing the relevant property `a m3:Facet`.
Nothing moves layers. `ontologyType` stays M3, `hasFamily`/`hasDominantM3` stay
M2, the `spectralClass`/`focalClass`/`scoringStatus`/`roleGrounding`/`hasFacet`
family stays M0, the domain facet lives at M1/M2. The only new M3 content is the
abstract vocabulary that lets them all *declare themselves* facets.

This is the same discipline as M2 concept admission: a small, generic
foundational addition that recognises structure already present, rather than a
new mechanism grafted on top.

---

## 7. Convergence with the Domain-fusion Phase 0

The disciplinary **domain axis** (the `Biology` in `Fm1m2(Biology, …)`, and the
planned `m2:appliesToDomains`) is a facet under this definition — a conferred
classification of a concept/instance by knowledge field.

Consequence: the Facet-M3 principle and the Domain-fusion Phase 0 are **the same
idea approached from two ends**. Naming faceting at M3 supplies the conceptual
frame that legitimises `appliesToDomains` — a concept "applies to domains"
because *domain is a facet* and a concept may carry multiple foci on it
(multi-domain right, e.g. biochemistry).

Sequencing question (to decide, not decided here): does the Facet-M3
explicitation land **before** the Domain fusion (giving it its rationale),
**with** it (one coherent edit), or **after** it (fusion first, then generalise)?
The etiological "validation first" logic and the fact that the fusion already has
a full change request argue for *at least* deciding the Facet principle before
graving `appliesToDomains`, so the property is introduced as a facet rather than
retrofitted into one.

---

## 8. Impacts if graved (checklist — none performed here)

```
□  M3_GenesisGrammar.jsonld : add m3:Facet (+ m3:Focus, + 2–3 sub-kinds), admission criteria
□  M3 SHACL grammar         : FacetShape (controlled value-set, classificatory, orthogonality note)
□  M2_GenericConcepts       : type hasFamily / hasDominantM3 as a m3:Facet
□  M0_Common.jsonld         : type spectralClass/focalClass/scoringStatus/roleGrounding/hasFacet
                              as facets; resolve Decision A (Facet→Focus rename if A1)
□  M1/M2 (domain)           : domain facet realised as m2:appliesToDomains (Domain-fusion CR)
□  changelogs               : keep 3 most recent — EXCEPT M3 files, which allow up
                              to 7 (rollback safety on the foundational layer;
                              documented in the M3 SHACL message so 7 is not read
                              as a violation). M3_GenesisGrammar is the first target.
□  re-run SHACL after each layer
```

---

## 9. Open decisions (for sign-off)

1. **Decision A** — `m3:Facet` = axis (A1, recommended) or value-registry (A2)?
2. **Decision B** — keep `m3:StateFacet` for `scoringStatus`, or fold into Conferred?
3. **Scope of v1** — all 9 axes typed at once, or start with the conferred core
   (`ontologyType`, `domain`, `hasFamily`, `roleGrounding`, `hasFacet`) and add
   the derived ones after?
4. **Sequencing** — Facet-M3 before / with / after the Domain-fusion Phase 0?

---

## 10. Explicitly out of scope

- No ontology files edited; this note precedes any graving (architecture before
  code). Formal gates (linter, Pellet, SHACL) and semantic sign-off remain with
  Michel before commit.
- Does not resolve the pre-existing 17 `M1_CoreConcepts` violations; the domain
  facet interacts with them only through the Domain-fusion Phase 0.
- Does not rename or reclassify any existing concept beyond the `Facet`/`Focus`
  cleanup that Decision A1 would imply.

---

## 11. References

- `M0_Common.jsonld` — current `m0:Facet` / `m0:hasFacet` (Democratization), the
  `spectralClass` / `focalClass` / `scoringStatus` / `roleGrounding` enumerations.
- `M3_GenesisGrammar.jsonld` — `m3:ontologyType` (the foundational facet already
  at M3).
- `M2_GenericConcepts.jsonld` — `m2:hasFamily`, `m2:hasDominantM3`.
- `M2_DomainFusion_ChangeRequest.md` — `m2:appliesToDomains` (the domain facet).
- `OntologicalOverfitting.md` — admission discipline; the §3 boundary is its
  application to faceting.
- Ranganathan, S. R. (1933). *Colon Classification* — faceted classification,
  facet vs focus.
- Base URI (all ontology IRIs): `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/` (via `@base`).
