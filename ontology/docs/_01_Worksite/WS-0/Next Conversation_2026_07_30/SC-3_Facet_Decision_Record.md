# SC-3 — Facet as an M3 Principle: Decision Record

**Version**: 1.0.0
**Date**: 2026-07-30
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Worksite**: WS-0 / SC-3
**Status**: DESIGN DECIDED — no ontology file edited; graving deferred to a future
HEAD-anchored session, after Michel's formal gates.
**Supersedes**: `_01_Facet_as_M3_Principle_ArchitectureNote.md` v0.1.0 **§5 only**
(the Conferred/Derived sub-typing). The rest of that note stands.

**Authority**: every corpus fact below was measured at `git show HEAD:<file>` on
2026-07-30 (M0_Common 1.1.0, M2_GenericConcepts 16.19.0, M3_GenesisGrammar 4.5.0).
Re-measure before graving.

---

## 0. WHAT SC-3 ACTUALLY IS (corrected)

SC-3 is **not** "invent faceting". Measured at HEAD:

- `m0:Facet` (abstract class) and `m0:hasFacet` (owl:ObjectProperty, **multi-valued**,
  "Multiple values allowed") **already exist** in `M0_Common.jsonld`, with one
  registered focus `m0:facet.Democratization`.
- The HEAD doctrine of `m0:Facet` is explicit: *"a facet is a role externally
  conferred by usage context ... anchored on m2:Role (Ss | K, perspective map) ...
  Distinct from m0:ScoringProperty (derived quality) and m0:FocalProperty."*
- `m3:Facet` / `m3:Focus` are **absent** from M3 (grep = 0).

Therefore **SC-3 = lift the existing `m0:Facet` to `m3:Facet`**, because the same
conferred-classificatory pattern lives at several layers (ontologyType at M3,
hasFamily at M2, domain at M1). The mechanism is recognised, not created.

---

## 1. THE FOUR-AXIS MODEL (decided)

`ontologyType` at HEAD was **overloaded** — a single enumeration fusing at least
three distinct classification axes. The corpus admits the fusion in its own words:
`TscgTool` is defined as *"typed as TscgTool **rather than Poclet**"* and
`SystemicFramework` as *"distinct from ... **Poclet (minimal instances)**"*. Every
"rather than Poclet" is the signature of a value forced to compete across axes.

Decomposed and reconciled:

| axis | status | cardinality | foci (provisional — names → WS-4) |
|---|---|---|---|
| **SCALE** (reductionScale) | NEW | mandatory, 1 | Poclet · CaseStudy · RealWorldSystem |
| **NATURE** (systemNature) | NEW | mandatory, 1, default *SystemModel* | SystemModel · Framework · Grammar · Tool |
| **AUDIENCE** (targetAudience) | RECAST from m0:Facet/Democratization | `minCount 1`, no maxCount | KitArchitect · KitCrafter · KitUser |
| **DOMAIN** (appliesToDomains) | EXISTING — coupled to SC-5 | multi | Biology · Optics · … |

Canonical rewrites that validate the decomposition (no fused value survives):
- `CanopyGraphVizProto` = SCALE:Poclet × NATURE:Tool × AUDIENCE:{KitArchitect,KitCrafter}
  — replaces the illegal "poclet **and** TscgTool" single-axis clash.
- `TransDisclet` = SCALE:Poclet × DOMAIN:{≥2 foci} — the fused value is dissolved;
  "transdisciplinary" is simply DOMAIN carrying ≥2 foci, not a new axis.

**Set-aside residues** (deliberately NOT forced into the four axes):
- *Layer role* (`Genesis`, `GenesisExtension`, `GenericConcepts`, `DomainExtension`)
  — a candidate third structural axis, but probably **redundant with the file's
  meta-level** (an M3 file *is* the Genesis; no property needed to say so). Treat as
  a separate cleanup, not part of SC-3.

---

## 2. DECISIONS

### A — `m3:Facet` = axis, `m3:Focus` = value (A1)
**Adopted.** `m3:Facet` is the abstract meta-class of classification *axes*; the
concrete axes (ontologyType, hasFamily, the three new axes, domain) are the facets;
their values are `m3:Focus`. A2 (Facet = value-registry) rejected — it would re-open
at M3 the very gap this worksite closes.
- **A1 debt discharged**: the note flagged "name the axis of which Democratization is
  a focus". It is now named: **AUDIENCE**. `Democratization` = AUDIENCE:KitUser (an
  unnamed focus, not an autonomous facet).

### B — Conferred/Derived sub-typing: **RETRACTED**
The architecture note §5 proposed `m3:ConferredFacet` / `m3:DerivedFacet`
(+ `m3:StateFacet`). **Withdrawn**, for a corpus-grounded reason:
- The HEAD `m0:Facet` doctrine already draws the sharp line the sub-typing would blur:
  facets are **conferred, Map-perspective roles**, explicitly **distinct from**
  `m0:ScoringProperty` (derived quality) and `m0:FocalProperty`. So the "derived"
  candidates (`spectralClass`, `focalClass`, `hasDominantM3`) **are not facets** —
  they stay ScoringProperty / FocalProperty, outside the facet family.
- `DerivedFacet` would have re-absorbed them *into* facets — the wrong direction,
  reversing a distinction the corpus makes on purpose. "Worse than better."
- `StateFacet` (for `scoringStatus`) is rejected independently: population 1 fails the
  ≥3-instance admission rule. `scoringStatus` is neither a conferred role nor,
  strictly, a facet; left as-is (a scoring-process state), outside the facet family.

Net: **no facet sub-typing.** Facet vs (ScoringProperty | FocalProperty) is the
distinction, and it already exists.

---

## 3. REJECTED CANDIDATE AXES (with reasons — the filter in action)

Admission filter: an axis enters only if (1) orthogonal to all existing axes AND
(2) not derivable from them.

| candidate | verdict | reason |
|---|---|---|
| PERIMETER (transdisciplinary) | reject | derived from DOMAIN (= ≥2 domain foci); not a new axis |
| OBJECTIVE (pedagogical, toolchain, …) | reject | "pedagogical" = AUDIENCE:KitUser; "toolchain" = NATURE:Tool; residual "objective" is correlated with scale+nature → not orthogonal |
| Map/Territory/Stereopsis triad | reject | level confusion (facets are *already* Map-perspective; the triad founds that split, one layer up) + §3 forbids grammars as facets + `hasDominantM3` is *derived*, opposite provenance to a *conferred* intent |
| UserRole (grand public vs Aki) | reject | classifies *persons/usage*, not the artifact; Aki has no IRI in a controlled value-set — a usage log, not a facet |
| KitTester | reject | testing is an *activity* the Architect/Crafter perform on their own output, transversal to the produce→consume chain — not an autonomous audience; keeps the triple closed |

---

## 4. THE AUDIENCE AXIS (detail)

Derived from TSCG's own mission ("a toolkit to fabricate Kits", Lego-Technic sense),
so the value-set is **closed and principled**, not an open list:

- `KitArchitect` — models/refactors the ontology architecture (M3/M2/M1), using M0
  tools to help (e.g. TscgOntologyExplorer, future TscgOntologyValidator).
- `KitCrafter` — fabricates Kits using an Architect's ontologies.
- `KitUser` — uses what the Crafter fabricated.

**Read as AUDIENCE (for whom), not stage (by whom).** The two are offset by one along
the produce→consume chain (an artifact produced at stage N is consumed at N+1);
modelling *audience* keeps the facet a conferred, Map-perspective property of the
artifact. Stage is derivable and not separately modelled.

**Orthogonality to meta-level — proven empirically on the corpus** (discharges the
"is this the layer axis in disguise?" doubt): two M0 artifacts with different
audiences — `TscgOntologyExplorer` (M0, AUDIENCE:KitArchitect) vs `FireTriangle`
(M0, AUDIENCE:KitUser). Audience varies at fixed meta-level → not derived from it.

**Cardinality**: `minCount 1`, no `maxCount`. Primary + secondary audiences allowed
when authentic (e.g. Canopy serves Architect and Crafter). Forcing single-value would
recreate the "rather than" collision just dissolved. Consistent with the existing
`m0:hasFacet` (already multi-valued at HEAD).

`KitDesigner` → **`KitArchitect`** (working name): the role *structures/refactors*,
and it disambiguates from "designer" as an audience focus (e.g. the type-designer user
of GlyphClay). One role only — not split Architect(M3)/Designer(M1). Name → WS-4.

---

## 5. TWO CONCEPTUAL RESULTS (carry forward)

1. **Legitimacy criterion for faceting.** A facet is *legitimate* when it **reveals**
   an orthogonality already present that the backbone tree ignored; it is *abusive*
   when it **fabricates** an orthogonality to dodge either real modelling or a needed
   correction of the backbone. (The faceting-specific form of the anti-overfitting
   discipline: recognise present structure vs graft a mechanism to circumvent.)

2. **Axis filter.** Orthogonal to all existing axes AND non-derivable from them.
   PERIMETER sank on (2); OBJECTIVE and Map/Territory on (1).

---

## 6. NAMING — DEFERRED TO WS-4

Semantics are frozen here; the exact IRIs are a GrammarSignature (WS-4) matter.
Working names: `reductionScale` (SCALE), `systemNature` + `SystemModel` (NATURE),
`targetAudience` + `KitArchitect`/`KitCrafter`/`KitUser` (AUDIENCE). Note the
"SystemModel" trap: do NOT name the NATURE default just "Model" — every M0 is a
reduced model, so "Model" classifies nothing (fails the classificatory criterion).

---

## 7. IMPACTS IF GRAVED (checklist — none performed)

```
□  M3_GenesisGrammar.jsonld : add m3:Facet (+ m3:Focus); admission criteria (§3 of the
                              architecture note) as the facet contract. NO sub-kinds.
□  M3 admission contract     : §3 criteria (controlled value-set, classificatory,
                              orthogonal) — likely belongs to the WS-5 validator as an
                              executable check rather than frozen M3 SHACL (to decide).
□  ontologyType              : decompose into SCALE + NATURE; migrate the 11 values;
                              handle the layer-role residue separately.
□  m0:Facet                  : re-type as/aligned with m3:Facet (the lift); Democratization
                              re-expressed as AUDIENCE:KitUser (A1 rename).
□  AUDIENCE / SCALE / NATURE : declare the three axes a m3:Facet at their home layers.
□  DOMAIN facet              : realised as m2:appliesToDomains — coupled to SC-5, graved
                              WITH the Domain-fusion, not here.
□  changelogs                : 3 most recent — except M3 files (up to 7).
□  re-run golden gate + SHACL after each isolated lot; interpret each delta.
```

---

## 8. STILL OWED / NOT DECIDED

- **Formal gates** (linter, Pellet OWL DL, SHACL CONFORMS:True) — Michel's, at graving.
- **Punning check**: A1 types existing *properties* (spectralClass, hasFamily…) as
  *individuals* `a m3:Facet` (OWL 2 punning, same pattern as `ontologyType`). Confirm
  Pellet tolerates it before graving; if not, fall back to a literal facet marker.
- **Sequencing vs SC-5**: the Facet principle lands *before* the Domain fusion (giving
  it its rationale); the DOMAIN axis is typed *with* SC-5, not in SC-3.
- **Layer-role residue** (§1) — separate cleanup, likely redundant with meta-level.
- **Graving happens in a fresh, HEAD-anchored session**, one isolated lot at a time.

---

## CHANGELOG

- **1.0.0** (2026-07-30) — Initial decision record. Four-axis model
  (SCALE/NATURE/AUDIENCE/DOMAIN); A1 adopted; §5 Conferred/Derived sub-typing
  retracted (contradicts HEAD m0:Facet doctrine); ontologyType decomposition;
  AUDIENCE axis derived from the Kit mission with empirical orthogonality proof;
  rejected axes and the two conceptual results recorded; names deferred to WS-4.
