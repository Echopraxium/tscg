# Facets to characterise M0 instances — parked proposal

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 0.1.0 · **Date**: 2026-11-15
**Status**: **PARKED** — recorded, not to be touched for now (Michel, 2026-11-15).
**Measured at**: HEAD `ee07f1a`.
**Origin**: the epistemic-gap feasibility study
(`ontology/docs/_01_Worksite/WS-15/`), discussion of what remains to
characterise an M0 instance once the scores are gone.

---

## 1. The proposal (Michel, 2026-11-15)

Characterise M0 instances with **facets** rather than with a single type, so that one
instance can be, for example, both "poclet" and "symbolic system grammar": a *demo*
instance of the I Ching would carry both, while another I Ching instance would carry
only "symbolic system grammar", to study it in detail.

## 2. State at HEAD (`ee07f1a`)

- Every M0 instance carries `m3:ontologyType` on its `owl:Ontology` node. Values over the
  43 instances found by check_m0: 33 `m3:Poclet`, 4 `m3:TscgTool`,
  3 `m3:SystemicFramework`, 2 `m3:SymbolicSystemGrammar`, 1 without a type
  (`M0_Triz_Examples`).
- The values come from `m3:TscgOntologyTypeScheme` (11 types, `M3_GrammarFoundation`),
  whose class comment says "Each TSCG ontology belongs to **exactly one** type". The 11
  types mix layer kinds (Genesis, GenesisExtension, GenericConcepts, DomainExtension) and
  M0 instance kinds (Poclet, CaseStudy, RealWorldSystem, SystemicFramework,
  SymbolicSystemGrammar, TscgTool, TransDisclet).
- A facet mechanism exists (`M3_GenesisGrammar`, graved by SC-3): `m3:Facet` (an axis),
  `m3:FacetValue` (a value), `m3:hasFacetValue` (multi-valued, no domain), `m3:valueOf`.
  One axis so far, `m3:Audience`; 3 M0 instances use it.
- check_m0 discovers instances by **folder** (`instances/poclets/`,
  `symbolic-system-grammars/`, …; `tscg_paths.INSTANCE_DIRS`): today the folder equals
  the type.

## 3. The prior decision this would reopen

`ontology/docs/_01_Worksite/WS-0/2026_09_02/SC-3_Facet_Decision_Record.md` v2.0.0
(2026-09-01, GRAVED) withdrew the v1.0.0 decomposition of `ontologyType` into four
facets:
- NATURE (system model / framework / grammar / tool) is the **backbone** — what the
  artefact essentially is, exactly one, a tree; typing it as a facet "fabricates an
  orthogonality";
- SCALE (Poclet / CaseStudy / RealWorldSystem) is a refinement of the system-model
  branch, not a facet;
- only AUDIENCE passed the facet test (a role: conferred, contingent, Map-perspective).

## 4. A reading that keeps both (Claude's proposal, not decided)

The I Ching example holds two different statements:
- "symbolic system grammar" says **what the modelled object is** — nature, which can stay
  the backbone;
- "poclet" says **what this mock-up is for** — a small pedagogical demo. That is conferred
  and contingent (the same grammar can be mocked up as a demo or studied in detail), so it
  passes the SC-3 facet test.

The demo instance would then be nature `SymbolicSystemGrammar` + facet value "Poclet";
the study instance, the same nature without it. Multi-labelling without claiming that an
object has two natures. It also fits the position that a poclet is a mock-up, not a kind
of reality.

## 5. What any route would touch

- the "exactly one type" comment in M3, and the reclassification of the 33 poclets;
- check_m0 discovery by folder (what does the folder encode once an instance carries
  several facets?);
- the layer-kind residue in the 11 types, already noted as owed by SC-3 §8.

## 6. Open question for when it is unparked

Reopen SC-3 so that NATURE itself becomes a facet, or keep NATURE as the backbone and
make "Poclet" (and perhaps SCALE) a conferred facet?

## Changelog

| version | date | change |
|---|---|---|
| 0.1.0 | 2026-11-15 | Parked: proposal, state at HEAD, prior SC-3 decision, a conciliating reading, impacts. |
