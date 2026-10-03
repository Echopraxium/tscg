# TSCG HandOver — WS-1 Housekeeping (Vocabulary Consolidation)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-09-30
**Purpose**: resume cold in a fresh conversation and open WS-1 (VOC).
**Where to put this**: `ontology/docs/_01_Worksite/WS-1/Next_Conversation_2026-09-30/`
and/or Project Knowledge.

> This HandOver is a **thin loader**, not a content snapshot (Smart Prompt §4).
> Every volatile fact below (SHAs, counts, versions, file structure) is **session
> state at handover time** and must be re-verified against HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every WS-1 lot modifies ontologies.
3. Then read from HEAD:
   - `ontology/docs/_01_Worksite/TSCG_VocabularyConsolidation_Worksite_README.md`
     (the WS-1 scoping note — **the authority for this worksite**)
   - `ontology/docs/_01_Worksite/worksite.yaml` (entry `WS-1`)

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: `9505d03` on `main` — confirm with `git log --oneline -6`.
- **Push path**: this Claude session has **no GitHub write access** to
  `Echopraxium/tscg` (push → HTTP 403). Workflow that worked: Claude commits in its
  clone → `git format-patch` → Michel runs `git am <patch>`, re-runs the gate, then
  `git push origin main`.
- **Gate**: `cd ontology/cli-tools && python run_all_layers.py` → `GATE: PASS`
  (M1 151 errors / 664 SHACL; M0 125 / 22 — reference counts, not failures).
- **Metric board**: `python ontology/cli-tools/tscg_metrics.py` — VOC gauge
  "bare keys (occurrences)" was **4263** at handover (6444 at WS-1 scoping, 2026-07-22).

### Shipped this session (2026-09-30), all pushed

| Commit | Content |
|---|---|
| `97bde2b` | M2 16.20.0 — `m2:NaryAttribute` sole carrier of multiplicity: `m2:cardinality` + `m2:arity` (non-negative integers, UML notation `3`, `1..*`, `*`); exclusivity read from arity (`1` = exclusive, = cardinality = co-present). `m2:valueRange` on `m2:ValueSpace` (interval notation, decimals allowed, one value per disjoint interval). Companions: M1_CoreConcepts 2.11.0, M1_Chemistry 1.3.0, M1_Photography 1.3.0 |
| `83a3aa4` | M2 16.21.0 — `m2:hasAttribute` is now a **list of attribute nodes named by `rdfs:label`** (was a map keyed by name → dropped by JSON-LD expansion). `m1:hasAttribute` unified into `m2:hasAttribute`. M1_CoreConcepts 2.12.0 |
| `30a29a5` | M2 16.22.0 — `hasPolarity.allowedValues` completed; `m2:progress` polarity counters recounted; Polarity ket notation restated in plain terms; lost `≥` restored |
| `9505d03` | removed `ontology/sparql/M2_Processor.jsonld` (pre-migration vestige) |

Acceptance script used for these lots: `ontology/cli-tools/verify_multiplicity_lot.py`
(in Michel's working copy; not committed — decide whether to commit it).

### Decisions taken this session (Michel)

- Multiplicity: **one mechanism** (`NaryAttribute`), two integer facets; no separate
  exclusivity flag. `m2:exclusivePoles` proposal **withdrawn**.
- `m2:valueRange` = bounds of **values** (≠ `cardinality`, bounds of their number);
  floats allowed; disjoint intervals = list of intervals; decimal point, comma
  separates the bounds.
- `M3_GrammarFoundation` `epistemicScore.range` **stays as is**: different semantics
  (codomain of a measure), and `m2:` inside M3 would be a layer inversion.

---

## 2. Today's goal — open WS-1 with its step 1 (Family A)

WS-1 status at handover: `todo`, `items: []`, scoping note v0.1.0 "no file edited yet".

**Decisions pending (Michel), in this order:**

1. **Approve the Family A table** of the scoping note §2 (standard replacements:
   `description`→`dcterms:description`, `examples`→`skos:example`,
   `name`/`label`→`rdfs:label`, `alternative_names`→`skos:altLabel`,
   `comment`→`rdfs:comment`, `note`/`rationale`→`skos:note`,
   `definition`→`skos:definition`, `date`→`dcterms:date`, `version`→`owl:versionInfo`).
   Read the table **from HEAD**, not from this summary.
2. **Scope of the first lot**: (a) only the attribute nodes under `m2:hasAttribute`
   (measured 734 bare-key occurrences at handover: 631 M2, 103 M1), or
   (b) the whole canonical corpus as the note's step 1 plans.
3. **Model WS-1 items** in `worksite.yaml` (currently `items: []`) with a gauge.

**Watch-outs:**

- Standard replacement is **context-sensitive**: `value` inside
  `m2:possibleValues` names the value (→ `rdfs:label`?) but `value` elsewhere may be
  numeric — `value` is **B2**, not Family A. Same for `formula`, `characteristics`,
  `pros`/`cons`, `role`, `status` (false friends) — all B2, pending the §4
  "data vs documentation" decision.
- **Golden discipline** (note §6): making keys visible adds triples → the M1 SHACL
  golden may move. Isolated commits; `--update-golden` only with a recorded reason.
- `tscg_metrics.py` B1 gauge is **per file** (counts `m2:` terms used in M1 as
  undefined even when declared in M2) — read deltas accordingly.

---

## 3. Parked (not WS-1)

- **`Binder` candidate** (from the review of "The (3,1) Tuple", EARTH, 2026-09-24):
  Fm2(Mediator, Identity, Composition), polarity neutral, `hasAttribute`
  BoundComponent = NaryAttribute (cardinality `2..*`, arity `*`). Next: run
  `tscg-m2-candidate-filter`.
- **CodonReadingFrame** poclet (Step 2 analysis done, verdict Gap → now resolved by
  the multiplicity lot): codon positions = cardinality `3` / arity `3`; reading
  frames = ternary polarity (exclusive). Next: Step 3 modeling.
- `docs/reboot-kit/TSCG_FileTree.md` is stale (still lists
  `sparql/M2_Processor.jsonld`): regenerate with `python tscg_generate_filetree.py`,
  then reload into Project Knowledge.
- OWL reasoner (`cli_tools/owl_reasoning_test/owl_reasoning_test.py`) could not run
  in Claude's sandbox (Java version); run it locally once.
