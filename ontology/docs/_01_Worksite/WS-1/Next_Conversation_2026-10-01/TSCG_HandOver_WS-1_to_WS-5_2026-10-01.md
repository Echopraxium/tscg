# TSCG HandOver — after WS-1 lots 1h–1j, resume with M3/M2 instrumentation (WS-5)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-01
**Purpose**: resume cold in a fresh conversation: decide Q1–Q5 of the M3/M2
instrumentation scoping, then run the CTX-5 lot.
**Where to put this**: `ontology/docs/_01_Worksite/WS-1/Next_Conversation_2026-10-01/`
and/or Project Knowledge.

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts, versions) is **session state at handover time**: re-verify against
> HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every lot below modifies ontologies or the gate.
3. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-5/WS-5_M3M2_Instrumentation_Scoping.md` — **the
     working authority for the next step**: two planes, proposed checks D1–D7 / G1–G7
     with baselines, CTX-5 prerequisite, decisions **Q1–Q5**.
   - `ontology/docs/_01_Worksite/WS-1/WS-1_FamilyA_Triage.md` — Progress table
     (lots 1a–1j DONE, 1k DEBT) and the remaining Family A lines.
   - `ontology/docs/_01_Worksite/WS-0/_00_TSCG_Worksite_Map.md` (WS-5, SC-11) and
     `ontology/docs/_01_Worksite/worksite.yaml` (WS-2 item CTX-5, WS-5 items).
   - `ontology/M3_GrammarFoundation.jsonld` — node
     `m3:grammar_foundation:ExternalVocabularyPolicy` (rules for external terms).

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: `ac74136` on `main` (WS-1 lot 1j). Confirm with `git log --oneline -6`.
- **Push path**: no GitHub write access from Claude's sandbox. Claude commits in its
  clone → `git format-patch` → Michel `git am <patch>`, runs the gate,
  `git push origin main`. ONE patch per lot, tested with `git am` on Michel's HEAD.
  The SHA changes on Michel's side: re-fetch before the next lot.
- **Sandbox prerequisites**: `pip install --break-system-packages rdflib pyshacl pyld`.
  Shell network reaches GitHub only; read standard vocabularies with WebFetch.
- **Gate**: `cd ontology/cli-tools && python run_all_layers.py` → `GATE: PASS`
  (M1 151 errors / 3 warnings / 688 SHACL; M0 124 / 0 / 22). M3 and M2: NOT
  INSTRUMENTED. The gate's `note` texts carry stale numbers (163, 476, x25): the
  compared values are right, the notes are not (fix planned, scoping §5).
- **Gauges** (`python ontology/cli-tools/tscg_metrics.py`, v1.3.0): VOC bare keys
  **3418**; EXT-1 **0**; EXT-2 **143**; `owl:imports` as string **0**; CTX-5 **35**.

### Shipped 2026-09-30 / 10-01 (all pushed)

| Lot | Content |
|---|---|
| 1h | every external term used declared once in the apex (34 declarations + policy node); schema.org accepted; `rdf:value` → `schema:value`; 5 non-terms fixed; gauges EXT-1/EXT-2 |
| 1i | 173 `owl:imports` strings → IRIs (canonical + M0, not `static/`); 3 broken paths fixed; linter / migration tools / guides updated; gauge `STR_imports_literal`; golden M0 125 → 124 (false positive, C12) |
| 1j | 9 ontology copies under `static/` deleted; 3 named-graph files repaired (Transistor, Kidneys, Physics); golden M1 SHACL 664 → 688 (hidden debt of M1_Physics revealed) |

### Decisions taken (Michel)

- **External vocabularies**: DCMI Terms, SKOS, ADMS, **schema.org** (only where it fills
  a DCMI/SKOS gap, checked by meaning, never by name). Declared once in the apex with
  `rdfs:isDefinedBy`; **never `owl:imports`** of an external vocabulary (would leave
  OWL 2 DL).
- **Reserved vocabulary**: the OWL 2 built-in annotation properties are declared; the
  axiom vocabulary (`rdf:type`, `rdfs:subClassOf`, `owl:imports`…) is never declared
  (OWL 2 Structural Spec §5.1–§5.6). Stay in OWL 2 DL: reasoner results must stay
  trustworthy.
- **SKOS** keeps its official typing (relations ObjectProperty, `related` symmetric,
  `notation` DatatypeProperty). `skos:broader` between the 11 ontology types = "derives
  from" in the scheme, not class inclusion (punning, DL-legal).
- `unit` → `schema:unitText` approved **in principle**, only for the 5 M1 occurrences
  (the M3 adjunction unit `η` stays native).
- **`owl:imports`**: only inside the Layer Cake, upward; written `{"@id": …}`; target =
  the imported file's document URL (ontology IRIs ≠ document URLs here → lot 1k, debt).
- **`static/`**: no ontology under `static/`, except instance data (e.g. Bmc case
  studies, `M0_BmcSimulation.jsonld.js`).
- Golden values may move only with a written reason in `golden_values.json`; a moved
  count is shown to Michel before it is frozen.

### Method that worked (reuse it)

Inventory on HEAD from the **parsed graph**, not the text → Michel decides point by
point (one decision at a time, plain explanation first) → text-level edit (minimal
diff) → **structural check** (no node lost; graph diff HEAD vs working copy shows only
the intended triples) → negative test for any new check (a check that cannot fail
proves nothing) → gate (explain any moved count, show it before freezing) → gauges →
minor bump + `m3:changelog` entry (keep 3, M3 files 7) → triage note → one commit +
patch, `git am`-tested.

Lesson learned on 2026-09-30: a regex-based changelog trim deleted a node in two files;
caught by the node-count check. Always use the bracket-aware helper and compare `@id`
sets HEAD vs working copy.

---

## 2. Today's goal

1. **Decide Q1–Q5** of `WS-5_M3M2_Instrumentation_Scoping.md` §6, one at a time.
   Recommendations there: Q1 build in the WS-5 engine; Q2 CTX-5 lot first; Q3
   INSTRUMENTED with frozen backlog; Q4 structural grammar only for v1; Q5 refresh the
   stale `tscg-generate-mn-grammars` skill.
2. **CTX-5 lot (canonical part)**: remove `m3:eagle_eye` / `m3:sphinx_eye` @context
   terms from 15 M1 files (30 terms). Measured graph-neutral (they produce no IRI);
   verify by triple counts; expected effect: pyld expands all canonical files. Refine
   the CTX-5 gauge so the 3 valid `{"@type": "@id"}` coercions of M1_CoreConcepts do
   not count. Not in scope: M0 colon-names (WS-10), FireTriangle / template (WS-9).
3. **Golden notes**: remove hard-coded numbers from the `note` texts.
4. Then the M3/M2 checks (document plane first, then structural SHACL).

---

## 3. Remaining WS-1 work (after the gate covers the 4 layers)

- **Family A §2 conditional lines**: `unit` → `schema:unitText` (5 M1, approved in
  principle), `value` in `m2:possibleValues` (103), `pros`/`cons`
  (`schema:positiveNotes`/`negativeNotes` now available), `symbol`, `abbreviation`,
  `use`/`usage`/`application`, `ontology`, `see_also`, `authors`,
  `supersedes`/`references`, `range` (M1 Photography → `m2:valueRange`).
- **Vestiges lot**: `metadata` blocks, map-shaped changelogs, `changelogLegacy`,
  M2/GenesisGrammar `v1`/`v2` history.
- **B1** (853 prefixed-but-undefined) and **B2** (~2 500 native keys: `role`, `status`,
  `formula`, `basis`… — needs the data-vs-documentation decision, scoping note §4 of
  the VOC README). The two `@vocab: owl#` files (142 fake `owl:<key>`, gauge EXT-2).
- **1k (debt)**: align ontology IRIs with document URLs.
- `tscg_metrics.py` `STANDARD_REPLACEABLE`: align with the approved table.
- `worksite.yaml`: WS-1 still has `items: []`.

## 4. Parked findings (not WS-1)

- 196 `rdfs:subClassOf` with a literal object, all in M1 (part of M1's SHACL debt).
- `xsd:boolean` used as a node `@type` in M1_CoreConcepts (×2) — counted by EXT-2.
- M1 values like `"m3:eagle_eye:Flow"` (in `m2:dominantASFID`) are literals naming terms
  M3 does not define (EagleEye defines `eagle_eye:typeF`) → WS-9 / SC.
- C12 (check_m0) scans changelog prose for `⊗`: known over-reach, decide separately.
- From earlier HandOvers: `M0_CONTEXT_TEMPLATE.json` (WS-9 AP-5); `Binder` candidate;
  CodonReadingFrame poclet; stale `docs/reboot-kit/TSCG_FileTree.md`; OWL reasoner to
  run locally (now meaningful: imports are IRIs); `verify_multiplicity_lot.py`.
