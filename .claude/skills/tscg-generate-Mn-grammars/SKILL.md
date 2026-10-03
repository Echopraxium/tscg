---
name: tscg-generate-mn-grammars
description: Design, generate and validate SHACL grammars for the TSCG layers M3, M2 and M1 from the graph on HEAD, wired into the acceptance gate. Use when Michel says "grammaire SHACL pour M1/M2/M3", "générer la grammaire", or asks for shapes, an M1 extension grammar, or the M3/M2 checkers.
---

# TSCG Generate Mn Grammars

**Version**: 2.0.0
**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-01
**Status**: Active (supersedes 1.1.0 — see Changelog)

## Purpose

Produce a SHACL grammar for one TSCG layer (M3, M2, M1 core, or an M1 extension) that
validates **what the graph on HEAD actually contains**, catches regressions, and can be
wired into `run_all_layers.py`. A grammar is a measuring instrument: it is worth
something only if it can fail.

## Load first — by name

1. **`head-over-memory`** — this skill carries **no** verifiable fact you may reuse
   unread: file lists, prefixes, class names, property names, counts and versions are
   read from HEAD every time. Anything written below as an example is a pointer to
   where the fact lives, not the fact.
2. **`tscg-ontology-diagnosis-pipeline`** — a grammar change is an ontology-tooling
   change: same phases, same human gates.

## Five rules (learned the hard way)

1. **Catalog, don't invent.** Constraints come from the parsed graph on HEAD plus
   Michel's decisions. Never write a shape for a property, class or value list that
   does not exist on HEAD. (v1.x proposed `m2:conceptFamily` with 9 families,
   `m2:hasM3Origin`, `m2:asfidScores`, `m3:dimensionType`: 0 occurrences on HEAD.)
2. **SHACL sees only the graph.** A bare JSON key (declared in no `@context`) is
   dropped on JSON-LD expansion: no shape can see it. "Zero bare keys" is enforced by a
   document-plane checker (`tscg_metrics.py` VOC gauge / WS-5 engine), never by SHACL.
   Always report how much of the file is invisible to the grammar.
3. **Every shape must bite.** A shape whose target matches zero nodes reports
   CONFORMS while validating nothing (SHAPE 9 enforced only M1_CoreConcepts for months;
   a relative prefix made SC-2's shape match 0 nodes). For each shape: count its focus
   nodes (≥ 1) and run a negative test (a mutated copy must violate it).
4. **Exact reference values, never loosened.** In the gate a count is a thermometer of
   the debt: it may be non-zero, it may not move by accident. Never weaken a shape to
   lower a count; lower it by repairing data or fixing a genuine shape bug. A moved
   count is shown to Michel, explained, and frozen with a written reason in
   `golden_values.json`.
5. **Michel decides semantics.** Which properties are required, which values are
   allowed, what is forbidden: proposals with evidence, his decision, one point at a
   time.

---

## STEP 0 — Level and targets

If the request does not name the level, ask with the interactive question tool:
M3 / M2 / M1 core / M1 extension (for an extension, then ask which one, offering the
list read from HEAD). Then list the target files **from HEAD**, e.g.:

```bash
git fetch origin main && git reset --hard origin/main      # fresh clone = HEAD
ls ontology/M3_*.jsonld ontology/M2_*.jsonld ontology/M1_*.jsonld
ls ontology/M1_extensions/*/M1_*.jsonld
```

- M3 is several files (apex `M3_GrammarFoundation` + the others). All M3 terms share
  the `m3:` namespace of `M3_GenesisGrammar.jsonld#` (sub-namespaces are written
  `m3:eagle_eye:…`, `m3:sphinx_eye:…`) — verify in each file's `@context`.
- M1 already has a grammar: `ontology/toolchain/check-M1/M1_Schema_shacl.ttl`,
  run by `check-M1/check_M1.py --shacl`. For M1, **extend that file** (new numbered
  shape, version bump, changelog); do not generate a parallel one.
- Read the worksite state first: `ontology/docs/_01_Worksite/WS-0/_00_TSCG_Worksite_Map.md`
  (WS-5, SC-11), `worksite.yaml`, and any WS-5 scoping note for M3/M2 instrumentation.

## STEP 1 — Pre-flight: can a grammar see this layer at all?

Measure, report, and stop if a blocking item fails. Each one has silently blinded a
grammar before.

| Check | Why it blocks | How to measure |
|---|---|---|
| `m0..m3` prefixes absolute (`https://…`) | relative prefix ⇒ shapes match 0 nodes | read `@context`; `tscg_metrics.py` CTX-4 |
| no `@vocab` in the target | bare keys become fake `owl:<key>` / foreign terms | `@context`; gauge EXT-2 |
| no root object with `@id` + `@graph` | JSON-LD named graph: whole file invisible to pyshacl's default graph | load as `rdflib.Dataset`, compare default vs named triples |
| `owl:imports` are IRIs | strings are literals; nothing is imported | gauge `STR_imports_literal` |
| strict JSON-LD expansion works | pyld rejects colon-named `@context` terms (CTX-5) | `pyld.jsonld.expand(...)` |
| bare-key share | that part of the file is outside the grammar's reach | `tscg_metrics.py` VOC gauge |

## STEP 2 — Catalog the graph (evidence for every constraint)

Parse each target with rdflib (as the gate does: `format="json-ld"`, no inference) and
produce, per class family:

```python
from rdflib import Graph, RDF, RDFS, Literal, BNode
from collections import Counter
g = Graph(); g.parse(path, format="json-ld")
# 1. how things are typed: rdf:type objects and rdfs:subClassOf objects (with counts)
# 2. for each class / parent class: its members (typed OR subclassed — read which)
# 3. for each member set: predicates used, coverage (#members having it),
#    value kind per predicate (IRI / literal + datatype / blank node), cardinality
# 4. literals where an IRI is expected (e.g. rdfs:subClassOf "m2:X" written as a string)
```

Example of what this yields (2026-10-01, re-measure): M2 GenericConcepts are
`owl:Class` with `rdfs:subClassOf m2:GenericConcept` (not typed `m2:GenericConcept`);
the predicates actually present include `m2:hasFamily`, `m2:hasPolarity`,
`m2:hasStructuralGrammarFormula`, `m2:hasDominantM3`. Coverage is never 100 %:
the gaps are either debt or legitimate exceptions — Michel decides which.

Also record the cross-file facts a single-file SHACL run cannot see (they belong to
the WS-5 engine or `tscg_metrics.py`, not to SHACL): external terms declared in the
apex (EXT-1), non-terms in standard namespaces (EXT-2), import targets that exist.

## STEP 3 — Design (present to Michel before writing any Turtle)

Present a table: constraint · target · evidence (coverage from STEP 2) · severity
(`sh:Violation` for rules, `sh:Warning` for recommendations) · expected count on HEAD.

**Structural part — common to every grammar (v1 scope):**

- `owl:Ontology` header: exactly one node; `owl:versionInfo`, `dcterms:created`,
  `dcterms:creator`, `rdfs:label`, `m3:ontologyType` (value in
  `m3:TscgOntologyTypeScheme`), `m3:changelog`.
- `m3:changelog` entries: `owl:versionInfo`, `dcterms:date`, `adms:versionNotes`;
  `m2:changelog` forbidden (`sh:maxCount 0`). Retention (3 entries, M3 files 7) is a
  document-plane check.
- every declared property / class has `rdfs:label` and `rdfs:comment`.
- `rdfs:subClassOf`, `owl:imports`, `rdfs:isDefinedBy` objects are IRIs, never literals.
- forbidden retired formalism (tensor product / ket / `hasTensorFormula`, the D8
  serialisation triad): read the current list from the existing grammars and
  `tscg_metrics.py` (FRB, DUP gauges).
- external vocabularies: follow the apex node
  `m3:grammar_foundation:ExternalVocabularyPolicy` (declared once in the apex, never
  imported, reserved axiom vocabulary never declared). Do not restate in shapes what a
  cross-file check already measures.

**Layer-specific part — only from catalog evidence + Michel's decision:**

- **M3**: ontology-type scheme integrity (`m3:TscgOntologyTypeScheme`, concepts
  `owl:Class` + `skos:Concept`), the policy node, apex declarations. Never an `m2:`
  term in an M3 file (layer inversion).
- **M2**: the GenericConcept families as found in STEP 2; fold in the existing targeted
  shapes of `check-M2/M2_MonoidalFormula_Schema_shacl.ttl` (SC-2). A semantic M2
  grammar (SC-11b) waits for WS-1: while many M2 keys are still bare, a graph grammar
  validates only part of the file and passes.
- **M1**: combos and their signatures (SC-1: a combo formula is a function signature
  `Fm2(...)` / `Fm1m2(Domain, ...)`, no monoidal operator inside), domains registered in
  `M1_Domains.jsonld`. All already in `M1_Schema_shacl.ttl`: extend it.

## STEP 4 — Generate

- **Location / name**: `ontology/toolchain/check-Mn/Mn_<Scope>_Schema_shacl.ttl`
  (underscore before `shacl`: a dot-named file was once never found, and the gate
  validated nothing while exiting 0). Add a scope qualifier when the grammar is
  partial (precedent: `M2_MonoidalFormula_Schema_shacl.ttl`), keeping
  `Mn_Schema_shacl.ttl` for a full grammar.
- **Header**: what the file covers AND what it does not (bare-key share, cross-file
  checks left to the engine), version, date, worksite, runner command, changelog.
- **Prefixes**: copy them from the targets' `@context` on HEAD, absolute only. Today
  (verify): `m3:` = `…/ontology/M3_GenesisGrammar.jsonld#`, `m2:` =
  `…/ontology/M2_GenericConcepts.jsonld#`, `m1:` = `…/ontology/M1_CoreConcepts.jsonld#`,
  `m0:` = `…/ontology/M0_Common.jsonld#`, base
  `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`. Never `tscg:`.
- **Colon sub-namespaces**: `m3:eagle_eye:typeA` is valid Turtle and SPARQL (a local
  name may contain `:`) and expands to `…M3_GenesisGrammar.jsonld#eagle_eye:typeA`,
  the IRI the M3 files use. Never resolve it through an `m3:eagle_eye` `@context` alias
  (CTX-5): those aliases point to another IRI (WS-2 item CTX-5, to remove).
- **Shapes**: numbered `# SHAPE n : …` blocks, one concern per shape, an explicit
  `sh:targetClass` / `sh:targetSubjectsOf` per target (never an "inherited by" comment
  in place of a real target), `sh:message` on every constraint saying what is wrong and
  what to do. SPARQL constraints redeclare their prefixes.
- **Forbidden properties**: `sh:property [ sh:path <p> ; sh:maxCount 0 ; sh:message "FORBIDDEN: …" ]`
  (precedent: `m2:changelog` in M1/M0) or `sh:not` around a property shape.

## STEP 5 — Validate and wire into the gate

1. Turtle parses (rdflib); shapes count printed.
2. For **each shape**: number of focus nodes on the targets (≥ 1, else the shape is
   blind — fix the target, do not ship it).
3. Run pyshacl the way the gate does (`inference="none"`; `run_shacl` in
   `check_M1.py` is the reference). `inference="rdfs"` changes the results: never mix
   the two.
4. Negative tests: for each shape, a mutated in-memory copy of a real node must
   produce the expected violation.
5. Report: violations per shape and per message, compared with the STEP 3
   expectations. Unexpected numbers are investigated before anything is frozen.
6. Gate: M1 counts flow through `check_M1.py`; M3/M2 through the WS-5 runner (see the
   WS-5 scoping note). First capture with `run_all_layers.py --update-golden`, reviewed
   number by number with Michel, reason written in `golden_values.json`. Do not put
   numbers in the golden `note` texts — they go stale; point to the frozen values.
7. Deliver as one commit / patch (Michel applies with `git am`, runs the gate, pushes).

## Deliverables

- the `.ttl` file (or the new shapes + version bump of an existing one);
- a short report: targets, shapes, focus-node count per shape, violations per shape,
  negative tests passed, bare-key share left outside the grammar;
- golden values updated only with Michel's approval and a written reason;
- worksite note updated (triage / WS-5 item).

## Integration with other skills

- `tscg-ontology-diagnosis-pipeline`: this skill is its Phase 3.4 (SHACL) instrument.
- `tscg-instance-pipeline`: M0 instances are validated by
  `check-M0/M0_Instances_Schema_shacl.ttl` through `check_m0_instances.py` (C15); new
  M1 concepts by `M1_Schema_shacl.ttl`.
- `tscg-tensor-to-structural-grammar-migration`: its forbidden patterns (tensor, ket,
  Hilbert space) stay forbidden in every grammar.

## Retired

- `scripts/generate_shacl_schema.py` (1.0.0, 2026-05-11): removed from the repository
  copy of this skill; if a copy is still present anywhere, **do not run it**. It writes the
  dead `M3_GenesisSpace.jsonld#` and phantom `M0_Poclet#` prefixes, dot-named output
  files, and shapes for M2 properties that do not exist on HEAD. Grammars are designed
  from the STEP 2 catalog instead.

## Changelog

**v2.0.0 (2026-10-01)** — rewrite after WS-1 lots 1h–1j and the WS-5 M3/M2 scoping.
- Removed every hard-coded, now-false fact: dead `M3_GenesisSpace`, phantom `M0_Poclet#`
  prefix, M2 constraints on properties absent from HEAD (`m2:conceptFamily` and its 9
  families, `m2:hasM3Origin`, `m2:asfidScores` / `m2:revoiScores`, `m3:dimensionType`,
  `m3:Enigma`), dot-named output files, `/mnt/project/…` prerequisites.
- Loads `head-over-memory` and `tscg-ontology-diagnosis-pipeline` by name; facts come
  from HEAD (STEP 0, STEP 2).
- New STEP 1 pre-flight (absolute prefixes, `@vocab`, named graph, imports as IRIs,
  strict expansion, bare-key share).
- Two planes made explicit: SHACL cannot see bare keys.
- Anti-blindness: focus-node count ≥ 1 and a negative test per shape.
- Gate integration: exact reference values, never loosen a shape, moved counts shown
  and justified; validation with `inference="none"` like the gate.
- M1: extend `M1_Schema_shacl.ttl` instead of generating a parallel file.
- Bundled script retired.

**v1.1.0 (2026-05-11)**: interactive level selection (STEP 0).

**v1.0.0 (2026-05-11)**: initial skill.
