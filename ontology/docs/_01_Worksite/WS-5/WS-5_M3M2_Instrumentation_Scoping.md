# WS-5 — Instrumenting M3 and M2 in the acceptance gate (scoping)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-01
**Status**: DECIDED 2026-10-03 — Q1 (a) engine, Q2 order, Q3 INSTRUMENTED, Q4 structural v1; Q5 done. CTX-5 lot done (§4).
**Measured on**: HEAD `ac74136` (after WS-1 lots 1h/1i/1j). Every count below is
session state: re-measure before use (`head-over-memory`).

---

## 0. Goal

`run_all_layers.py` reports M3 and M2 as `NOT INSTRUMENTED`. Goal: the gate covers the
four layers, with the same discipline as M1/M0 — **exact reference values**, a backlog
that is measured and frozen, never blessed, and that may only move on purpose.

Why now: WS-1 lots 1h–1j made the Layer Cake structurally sound (external terms
declared in the apex, imports are IRIs, no named graph, no ontology copy under
`static/`). Without M3/M2 instrumentation nothing prevents those gains from regressing
in the two layers that host the apex.

## 1. Ownership — already decided by the worksite map

- `_00_TSCG_Worksite_Map.md` (WS-5): `toolchain/check-M2/` and `check-M3/` are the
  intended home of the future checkers; "a runner for an arbitrary shape file is job
  one" (the SHACL pass is hard-wired to check_M1).
- `check-M2/M2_MonoidalFormula_Schema_shacl.ttl` 0.1.0 (WS-0/SC-2) already holds 2
  targeted shapes, explicitly **not** an M2 grammar, run only through
  `tscg_metrics.py --shacl-path`; its header asks for a third gate state `PARTIAL`.
- SC-11 (map): M2 grammar in two planes — **11a document plane** (JSON Schema, WS-5
  only) and **11b graph plane** (SHACL, blocked by WS-1 VOC).
- `M3_Schema.shacl.ttl` (2026-07-03, "CONFORMS: True, 13 shapes") is cited by
  run_all_layers' DEFAULT_GOLDEN note **but is not in the repository** (searched
  2026-10-01). Treat as lost; do not trust the July CONFORMS (SHAPE 9 lesson).
- The validator engine exists: `toolchain/validator/tscg_validator.py` (lot 1: CTX
  family, `--source local|head|github`, `--layers M3,M2,M1`).

## 2. Two planes — what each one can see

| Plane | Reads | Sees bare keys? | Tool |
|---|---|---|---|
| **Document** | the JSON as written | **yes, all of them** | checker (Python) |
| **Graph** | the expanded RDF | no — a bare key is dropped on expansion | SHACL (pyshacl) + graph checks |

Consequence: "zero bare keys" can only be enforced by the document plane. SHACL can
only constrain what reaches the graph (exception: the two M3 files with
`@vocab: owl#`, whose bare keys become fake `owl:<key>` terms — gauge EXT-2).

## 3. Proposed checks (first version)

### 3.1 Document plane (M3: 5 files, M2: 1 file)

| Id | Check | Baseline 2026-10-01 | Target |
|---|---|---|---|
| D1 | bare keys (VOC) | M2 1368, M3 619 (GenesisGrammar 283, GrammarFoundation 150, SphinxEye 67, EagleEye 60, BicephalousPerspective 59) | frozen backlog, ↓ |
| D2 | `@vocab` in @context | 2 files (GrammarFoundation, BicephalousPerspective) | 0 |
| D3 | root object with `@id` + `@graph` (named graph) | 0 | 0 |
| D4 | `owl:imports` value not an IRI | 0 | 0 |
| D5 | changelog: `m3:changelog` list, entries `{owl:versionInfo, dcterms:date, adms:versionNotes}`, retention 7 (M3) / 3 (M2), no `m2:changelog` | legacy `metadata.changelog` maps remain (vestiges lot) | 0 |
| D6 | layer inversion (`m2:` term in an M3 file) | 0 | 0 |
| D7 | file expandable by a strict JSON-LD processor (pyld) | M2/M3: all expand. Corpus-wide: **15 M1 files fail**, cause CTX-5 (§4) | 0 |

### 3.2 Graph plane

| Id | Check | Baseline | Target |
|---|---|---|---|
| G1 | `owl:Ontology` header: exactly 1 node; `owl:versionInfo`, `dcterms:created`, `dcterms:creator`, `rdfs:label`, `m3:ontologyType` (value in `m3:TscgOntologyTypeScheme`), `m3:changelog` | M2 lacks `rdfs:label`; 4 M3 files lack `m3:ontologyType` (BicephalousPerspective, EagleEye, GrammarFoundation, SphinxEye) | 0 |
| G2 | every declared property / class has `rdfs:label` and `rdfs:comment` | M2 7, M3 14 | 0 |
| G3 | `rdfs:subClassOf` object is an IRI (never a literal) | M2 0, M3 0 (M1 196 — M1's own debt) | 0 |
| G4 | changelog entry shape (3 properties, typed) | to measure | 0 |
| G5 | standard term used but undeclared in the apex (EXT-1) | 0 | 0 |
| G6 | non-term in a standard namespace (EXT-2) | 143 (142 `owl:<key>` in the two `@vocab` files + `xsd:boolean` as a class in M1_CoreConcepts) | 0 |
| G7 | the 2 existing SC-2 monoidal-formula shapes, folded in | as measured by tscg_metrics `--shacl` | frozen |

G5/G6 are cross-file (they need the apex): graph checks in the engine, not SHACL.

### 3.3 Out of scope for v1 — the semantic M2 grammar (SC-11b)

A grammar of GenericConcepts (formulas, polarity, families…) waits for WS-1: M2 still
carries 1368 bare-key occurrences that never reach the graph, so a graph grammar would
validate only part of the file and pass. v1 is a **structural** grammar only.

## 4. Prerequisite — CTX-5 (canonical part), small lot

> **DONE 2026-10-03** (re-measured on HEAD `9033baf`, baselines §3 unchanged). 30 terms removed
> from 15 M1 files, graphs isomorphic; pyld expands all 27 canonical files (D7 = 0). A second
> pyld blocker was found in M1_Economics: the unused relative alias `"m1core"`; on Michel's
> decision `m1core` was replaced by `m1` everywhere live (10 M0 instances, producers, guides).
> check_M1 1.5.0 stopped requiring the two terms (it enforced the defect; golden M1 CTX001
> 3 → 1). tscg_metrics 1.4.0: CTX-4 = any relative term IRI, CTX-5 = invalid colon terms only
> (gauge refinement below applied). Decisions Q1 (a), Q2, Q3 INSTRUMENTED, Q4: approved.
>
> *Decision (Michel, 2026-10-03): the M3 Eye terms will be renamed under their own document
> namespace, `m3.eagle_eye:` → `M3_EagleEye.jsonld#` and `m3.sphinx_eye:` → `M3_SphinxEye.jsonld#`
> (option 2, IRIs change). Separate lot, linked to lot 1k (ontology IRIs = document URLs).
> Measured 2026-10-03: 308 lines in 11 files use `m3:eagle_eye:` / `m3:sphinx_eye:` (M2 237, M3 37).*

`@context` terms containing `:` — in the canonical corpus: `m3:eagle_eye` and
`m3:sphinx_eye` in 15 M1 files (M1_CoreConcepts + 14 extensions), 30 terms. The CTX-5
gauge reads 35 = these 30 + 3 valid coercions in M1_CoreConcepts + 2 terms in the M0
instance template. Measured 2026-10-01:

- they produce **no IRI at all** in any graph (rdflib ignores them: 0 IRIs under
  `M3_EagleEye.jsonld#` / `M3_SphinxEye.jsonld#` in the whole canonical corpus);
- if honoured, they would point to the **wrong** IRI: M3 defines its terms as
  `m3:eagle_eye:X` = `M3_GenesisGrammar.jsonld#eagle_eye:X`;
- they make pyld (strict JSON-LD 1.1) **reject** the 15 files ("term in form of IRI
  must expand to definition").

So removing them is graph-neutral (to verify by triple counts) and unblocks D7.
Tracked as WS-2 item `CTX-5` ("scheduled as its own fix (R3)"). Not in it: M0
colon-names (`m0:instance:…`, WS-10) and the archaeological `eagle_eye:` terms of
FireTriangle / the generation template (WS-9 AP-1 / AP-5). Gauge refinement:
`rdfs:subClassOf` / `rdfs:domain` / `rdfs:range` → `{"@type": "@id"}` in M1_CoreConcepts are
**valid** coercions (each term expands to its own IRI) and should not count as CTX-5.

Side finding (not CTX-5): M1 values such as `"m3:eagle_eye:Flow"` in
`m2:dominantASFID` are **literals** and name terms M3 does not define (EagleEye
defines `eagle_eye:typeF`, not `eagle_eye:Flow`). Record for WS-9 / SC work.

## 5. Gate integration

- Add a per-layer runner for M3/M2 to `run_all_layers.py`, same contract as
  `run_m1()`: a crash or an unparseable summary is a FAIL, never a pass.
- Freeze the first capture with `--update-golden`, reviewed number by number.
- Golden notes: stop hard-coding numbers in `note` texts. Today they are stale ("163
  check_M1 errors" → 151, "476 violations" → 688, "C12 x25" → 24, "18 PASS / 25 FAIL"
  unverified): a confident wrong number in the gate's own output. Point the note at
  the frozen values instead.

## 6. Decisions for Michel

**Q1 — Where to build.** (a) inside the WS-5 engine (`validator/checks/`, new
families VOC/STR/EXT + a generic SHACL runner; run_all_layers calls the engine for
M3/M2) — aligned with the map, reusable for M1/M0 later, more upfront work;
(b) standalone `check-M3/check_M3.py` and `check-M2/check_M2.py` modelled on check_M1 —
faster, but a third and fourth copy of the same logic. *Recommendation: (a).*

**Q2 — Order.** CTX-5 lot first (small, graph-neutral, unblocks pyld), then the
golden-notes fix, then the engine checks. *Recommendation: yes.*

**Q3 — Gate status.** INSTRUMENTED with frozen backlog (as M1), or a new `PARTIAL`
state while the graph plane is structural only. *Recommendation: INSTRUMENTED for the
document plane, with the graph-plane coverage stated in the note; add `PARTIAL` only if
the gate output would otherwise overstate coverage.*

**Q4 — v1 ambition.** Structural grammar (§3) only; semantic M2 grammar after WS-1.
*Recommendation: yes.*

**Q5 — Stale skill.** `tscg-generate-mn-grammars` targets the dead `M3_GenesisSpace`
and proposes M2 constraints that do not exist on HEAD (`m2:conceptFamily` with 9
families, `m2:hasM3Origin`, `m2:asfidScores`, `m3:dimensionType` — all 0 occurrences,
measured 2026-10-01). **DONE 2026-10-01** (Michel's request): skill rewritten as 2.0.0
— catalog-driven from HEAD, pre-flight checks, focus-node count and negative test per
shape, gate integration; bundled `generate_shacl_schema.py` retired.

## 7. Step (1) — generic SHACL runner: DONE 2026-10-04

Measured on HEAD `8db41cf`. `validator/checks/shacl_runner.py` 0.1.0, engine 0.2.0
(`tscg_validator.py --shacl` / `--shapes <ttl>`), negative tests in
`validator/tests/test_shacl_runner.py` (8/8). The gate is NOT wired yet (step 4):
golden values untouched, gate PASS unchanged.

- **One runner, grammars as data.** `GRAMMARS` maps a layer to its `.ttl` files
  (M1, M0, M2-SC-2; M3 none — reported as NOT INSTRUMENTED, never silently skipped).
- **Parity with the existing checkers**: M1 344 results, file by file equal to
  check_M1's count / 2 (17/17); M0 22 instances with ≥ 1 result = C15's 22 FAIL.
  Cross-checks: ComboFormulaShape 138 = SC-1 gauge; DomainConceptComboShape 196 =
  the 196 `rdfs:subClassOf` literals.

Findings (no lot yet, Michel to decide):

- **check_M1 counts each SHACL violation twice.** `run_shacl` keeps the lines
  "Message:" and "Focus Node:": the gate's frozen M1 `shacl_violations` (688) is a
  count of lines, i.e. 344 violations. Consistent over time, wrong unit.
- **The interim SC-2 runner measured nothing.** `tscg_metrics --shacl --shacl-path
  check-M2/…` iterates M1 files only and keeps only "(SC-1)" messages: it always
  printed 0. Run through the new runner, both SC-2 shapes bite on M2 (focus 86 and 2)
  and find 0 violations — consistent with the document-plane NOT-1 gauge (0).
- **Two M0 files are invisible to the M0 grammar.** `instances/systemic-frameworks/
  Triz/M0_Triz_Examples.jsonld` and its copy `instances/tscg-tools/TscgLittleBigBrain/
  M0_Triz_Examples.jsonld` have no `owl:Ontology` node: every M0 shape targets
  `owl:Ontology`, so C15 reports them as passing without validating anything (focus
  41 for 43 files). Also a duplicate file.

## 8. Step (2) — document-plane checks D1–D7: DONE 2026-10-04

Measured on HEAD `c2ac85a`. `validator/checks/doc.py` 0.1.0, engine 0.3.0
(`tscg_validator.py --doc`), negative tests `validator/tests/test_doc.py` (14/14:
each check moves by exactly the expected delta on a mutated copy of real data).
Not wired into the gate yet (step 4): nothing frozen.

**Decision D5(a)** (Michel, 2026-10-04): the only changelog is `m3:changelog` on the
owl:Ontology node. Any other key containing "changelog" (case-insensitive) is a D5
finding — this catches the per-concept `m2:changeLog` on `m2:Trade-off`, which a
case-sensitive "no `m2:changelog`" rule would miss.

| Check | M2 | M3 | vs §3 |
|---|---|---|---|
| D1 bare keys (occurrences) | 1368 | 619 | equal |
| D2 `@vocab` | 0 | 2 | equal |
| D3 named graph | 0 | 0 | equal |
| D4 `owl:imports` not an IRI | 0 | 0 | equal |
| D5 changelog | 1 (`m2:changeLog`) | 4 (`metadata.changelog` in EagleEye, GenesisGrammar, GrammarFoundation, SphinxEye) | precised |
| D6 layer inversion (keys, `@id`, `@type`) | 0 | 0 | equal |
| D7 strict pyld expansion (offline) | 0 | 0 | equal |

Notes:
- All M2/M3 bare keys sit inside `@graph`: tscg_metrics' VOC gauge (which walks
  `@graph` only) is complete for these layers. The engine walks the whole document.
- D1 and D5 overlap on the bare `changelog` key of the 4 M3 vestiges (counted in
  both): D1 measures vocabulary, D5 the changelog rule.
- D6 counts references, not prose: `m2:` mentions inside `rdfs:comment`, `m3:usage`
  etc. are not inversions.
- Informative run on M1/M0 (not in this step's scope, not frozen): D1 M1 1268 / M0
  6604 (= the M0 bare-key gauge of the 2026-10-03 HandOver); D5 M1 2 / M0 7; **D7
  M0 28**, not 7 as the 2026-10-03 HandOver said: 18 instances carry a relative IRI
  in their `@context` ("@context @id value must be an absolute IRI", e.g.
  `M1_extensions/biology/M1_Biology.jsonld#`) and 10 a colon-named term that does
  not expand to itself (CTX-5 pattern). Remote contexts are blocked in this check,
  so none of the 28 is a network artefact. Owner: WS-10.
