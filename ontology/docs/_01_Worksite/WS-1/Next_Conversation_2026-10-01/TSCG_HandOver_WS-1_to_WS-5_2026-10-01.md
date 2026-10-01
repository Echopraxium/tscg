# TSCG HandOver — after WS-1 lots 1h–1j, resume with M3/M2 instrumentation (WS-5)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-01
**Purpose**: resume cold in a fresh conversation: decide Q1–Q4 of the M3/M2
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
   For the SHACL work, also **`tscg-generate-mn-grammars`** (2.0.0).
3. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-5/WS-5_M3M2_Instrumentation_Scoping.md` — **the
     working authority for the next step**: two planes, proposed checks D1–D7 / G1–G7
     with baselines, CTX-5 prerequisite, decisions **Q1–Q4** (Q5 done).
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

1. **Decide Q1–Q4** of `WS-5_M3M2_Instrumentation_Scoping.md` §6, one at a time.
   Recommendations there: Q1 build in the WS-5 engine; Q2 CTX-5 lot first; Q3
   INSTRUMENTED with frozen backlog; Q4 structural grammar only for v1. Q5 is DONE:
   `tscg-generate-mn-grammars` rewritten as 2.0.0 (2026-10-01) — load it by name for
   the SHACL work.
2. **CTX-5 lot (canonical part)**: remove `m3:eagle_eye` / `m3:sphinx_eye` @context
   terms from 15 M1 files (30 terms). Measured graph-neutral (they produce no IRI);
   verify by triple counts; expected effect: pyld expands all canonical files. Refine
   the CTX-5 gauge so the 3 valid `{"@type": "@id"}` coercions of M1_CoreConcepts do
   not count. Not in scope: M0 colon-names (WS-10), FireTriangle / template (WS-9).
3. **Golden notes**: remove hard-coded numbers from the `note` texts (stale: "163",
   "476", "C12 x25", "18 PASS / 25 FAIL"; and the M3 note claims "M3_Schema.shacl.ttl
   exists" — it is not in the repository).
4. Then the M3/M2 checks (document plane first, then structural SHACL).

---

## 3. Remaining WS-1 work (after the gate covers the 4 layers)

### Planned order (agreed with Michel, 2026-10-01)

| Conversation | Content |
|---|---|
| **n+1** (this HandOver) | Q1–Q4, CTX-5 lot, golden notes, M3/M2 checks + structural SHACL. If time remains: start B1 (safest). |
| **n+2** | **B1** (declare only) + the **B2 decision** (VOC README §4: data or documentation, the `eagleView` / `sphinxView` block shape, the `m3:role` / bare `role` duplication) + a first B2 lot if decided. |
| **n+3 and later** | B2 execution in lots: frequent keys first, then the default rule for the long tail. |

Why this order: the M3/M2 checks lock every later B1/B2 lot in the gate.

### Re-measure before B1 / B2 (do not trust these figures)

- **B1 is much smaller than its gauge.** The VOC README names **24** undeclared `m3:*`
  keys (M3_BicephalousPerspective); the gauge `VOC_prefixed_but_undefined` shows **853**
  because it is per-file and conservative (it counts a prefixed key not defined *in the
  same file*, even if defined in the apex or another imported file). Measure B1 with a
  check that follows `owl:imports` (now possible: imports are IRIs since lot 1i).
- **B2 figures in the VOC README are from 2026-07-22** (e.g. `role` 308); on HEAD
  2026-10-01 `role` = 152. Re-measure.
- **Bare-key gauge vs family C.** The VOC README classes single-letter primitives
  (`S`, `I`, `D`, `F`, `A`…) as family **C — false positives, to exclude**; the VOC gauge
  still counts them (~80 occ. as keys on 2026-10-01). Decide whether they are formula
  values (exclude from the gauge) or primitive → value tables (a B2 pattern), then
  adjust the gauge — no data change.
- Concentration (2026-10-01): 1253 distinct keys; top 100 = 51 % of occurrences; 861
  keys occur once (long tail → the default `m3:documentation` rule of §4).

### Working rule (Michel, 2026-10-01) — no new bare keys

Bare keys were introduced by earlier LLM generations, silently (JSON-LD drops them
without any error). From now on:
- **every lot reports the VOC gauge before → after** (`tscg_metrics.py`), and it must
  not rise;
- **every new or modified M0 instance reports 0 bare keys** (check in
  `tscg-instance-pipeline` 2.2.0, step 3.5 (a));
- once the M3/M2 checkers exist, the gate locks this (any rise = FAIL).

**Finding (2026-10-01): the M0 instances are outside the VOC gauge.** `tscg_metrics.py`
measures the canonical scope (`ontology/`) only. Measured separately: **6604 bare keys
in the 43 M0 instances** (KindlebergerMinsky 1000, CellSignalingModes 467, TPACK 443,
ExposureTriangle 376, RGB_Additive 267, FireTriangle 262 …; only QRCodeToPocketCity
has 0). Decide in n+1 or n+2: add an M0 VOC gauge (and freeze it in the gate's M0
section), and whether M0 bare keys are WS-1, WS-9 (archaeological poclets) or WS-10.
Also: many instances use `m1.ext:<domain>` (colon-named) while check_m0 C08 documents
`m1.extensions.<domain>` and does not flag the colon form.

### Other remaining lines

- **Family A §2 conditional lines**: `unit` → `schema:unitText` (5 M1, approved in
  principle), `value` in `m2:possibleValues` (103), `pros`/`cons`
  (`schema:positiveNotes`/`negativeNotes` now available), `symbol`, `abbreviation`,
  `use`/`usage`/`application`, `ontology`, `see_also`, `authors`,
  `supersedes`/`references`, `range` (M1 Photography → `m2:valueRange`).
- **Vestiges lot**: `metadata` blocks, map-shaped changelogs, `changelogLegacy`,
  M2/GenesisGrammar `v1`/`v2` history.
- **B1** (gauge 853, true size much smaller — see above) and **B2** (~2 500 native keys: `role`, `status`,
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
