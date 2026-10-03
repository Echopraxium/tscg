# TSCG HandOver — WS-1 Vocabulary Consolidation, resume at lot 1h

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-09-30
**Purpose**: resume WS-1 cold in a fresh conversation, starting with lot 1h.
**Where to put this**: `ontology/docs/_01_Worksite/WS-1/Next_Conversation_2026-09-30/`
and/or Project Knowledge.

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts, versions) is **session state at handover time**: re-verify against
> HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every WS-1 lot modifies ontologies.
3. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-1/WS-1_FamilyA_Triage.md` — **the working
     authority for WS-1 Family A**: per-key verdicts, sources, and the **Progress**
     table (lots 1a–1g DONE, 1h TODO).
   - `ontology/docs/_01_Worksite/TSCG_VocabularyConsolidation_Worksite_README.md`
     (WS-1 scoping note: layering rails §1, B1/B2 §3, data-vs-documentation §4).
   - `ontology/M3_GrammarFoundation.jsonld` — the declarations of `m3:changelog`
     and `m3:rationale` (the pattern lot 1h follows).

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: `e88408d` on `main` (WS-1 lot 1g). Confirm with `git log --oneline -8`.
- **Push path**: no GitHub write access from Claude's sandbox. Claude commits in
  its clone → `git format-patch` → Michel `git am <patch>`, runs the gate,
  `git push origin main`. Deliver ONE patch per lot, rebased on Michel's HEAD;
  tell Michel which old patches are obsolete.
- **Sandbox prerequisites**: `pip install --break-system-packages rdflib pyshacl pyld`
  (without pyshacl the gate falsely FAILs: SHACL counts drop to 0). Shell network
  reaches GitHub only; read standard vocabularies with WebFetch.
- **Gate**: `cd ontology/cli-tools && python run_all_layers.py` → `GATE: PASS`
  (M1 151 errors / 3 warnings / 664 SHACL; M0 125 / 0 / 22). **M2 and M3 are not
  instrumented by the gate**: verify M2/M3 edits by triple counts (rdflib, HEAD vs
  working copy).
- **VOC gauge** (`python ontology/cli-tools/tscg_metrics.py`): bare keys
  **3418** occurrences (4177 at session start).

### Shipped this session (2026-09-30), all pushed

| Lot | Content |
|---|---|
| 1a | `examples`/`example` → `skos:example`; 5 map-valued examples → list of `{rdfs:label, rdf:value}` nodes |
| 1b | `description` → `dcterms:description` |
| 1c | changelog entry keys → `owl:versionInfo` / `dcterms:date` / `adms:versionNotes`; prefix `adms` declared |
| 1d | container `m1:`/`m2:changelog` → `m3:changelog` (canonical + check_M1 ONT007/ONT008, M1 SHACL 1.5.0, CLAUDE.md) |
| 1e | same for 45 M0 instances + check_m0 1.7.0 (C14), M0 SHACL v1.8, M0 templates, TscgPocletMiner prompt, RAG skip lists |
| fix | 4 `static/` poclet copies: dead `M3_GenesisSpace` → `M3_GenesisGrammar` (absolute m3 prefix) |
| 1f | `name` → `rdfs:label` |
| 1g | `alternative_names`→`skos:altLabel`, `comment`→`dcterms:description`, `note`→`skos:note`, `definition`→`skos:definition`, `label`→`rdfs:label`, `title`→`dcterms:title`, `id`→`dcterms:identifier`, `rationale`→**`m3:rationale`** (new) |

### Decisions taken this session (Michel)

- **Governing principle**: everything must be interpretable by an RDF parser, not
  only by humans; **no implicit terms** — every term used must be explicitly
  declared (including built-ins, whose explicit declaration OWL 2 does not forbid).
- External vocabularies: **local declarations** (`owl:AnnotationProperty` +
  `rdfs:isDefinedBy`), **never `owl:imports`** (DCMI terms are plain `rdf:Property`
  → importing would push the corpus into OWL Full).
- **ADMS accepted** as an external vocabulary (recorded in the `m3:changelog`
  declaration). schema.org still undecided.
- `description` and `comment` → `dcterms:description` (one predicate for
  descriptive text; chosen over `rdfs:comment` on semantic grounds).
- `rationale` → `m3:rationale`, `rdfs:subPropertyOf skos:note` (no standard
  rationale property exists; IBIS judged too heavy).
- Changelog: container `m3:changelog` only; **no `m2:changelog` anywhere**
  (enforced by check_M1 ONT008, check_m0 C14, M1/M0 SHACL `maxCount 0`).
- Legacy forms (`metadata` blocks, map-shaped changelogs keyed by version,
  `changelogLegacy`) are **not** renamed piecemeal: they go to a dedicated
  "vestiges" lot.

### Method that worked (reuse it)

Per lot: inventory on HEAD (usage context, value types, collisions with the
target) → Michel decides per key → text-level key rename (keeps diffs minimal)
→ **structural check**: parsed new file == parsed original with keys renamed
programmatically → rdflib triple counts HEAD vs working copy → gate → gauge →
minor version bump + `m3:changelog` entry `{owl:versionInfo, dcterms:date,
adms:versionNotes}` (keep 3, M3 files 7) → update the triage Progress table →
one isolated commit + patch.

---

## 2. Today's goal — lot 1h (explicit declarations)

Planned in the triage note (row 1h):

1. **Inventory from the graph** (not from memory) every external term used as a
   predicate in the canonical corpus (`dcterms:`, `skos:`, `adms:`, `rdf:`,
   `rdfs:`, `owl:` …), with how it is used (literal → annotation; resource →
   check whether object/annotation).
2. **Declare each one** in `M3_GrammarFoundation.jsonld` with its OWL type and
   `rdfs:isDefinedBy` pointing to its source vocabulary; built-ins (`rdfs:label`,
   `rdfs:comment`, `owl:versionInfo`…) declared too (Michel: no implicit).
3. **New gauge** in `tscg_metrics.py`: "external terms used but undeclared",
   target 0.
4. Verify that `m3:` resolves identically in every file (it did for all 24
   canonical files on 2026-09-30) and that the gate does not move.

---

## 3. Remaining WS-1 work (after 1h)

- **Triage §2 conditional lines**: `value` in `m2:possibleValues` (103 occ,
  → `rdfs:label`?), `pros`/`cons` (schema.org vs documentation container),
  `symbol` (`skos:notation` vs `m3:symbol`), `unit` → `schema:unitText`,
  `abbreviation` → `skos:notation`, `source` (2 of 6), `see_also`, `authors`,
  `supersedes`/`references`, `range` in M1 Photography → `m2:valueRange`.
- **Vestiges lot**: `metadata` blocks (stale `version`, `date_modified`, last
  bogus `owl:version` in M3_GrammarFoundation), map-shaped changelogs
  (M1_CoreConcepts `m1:changelog`, M3 EagleEye/GenesisGrammar/GrammarFoundation/
  SphinxEye), M1_Electronics `changelogLegacy`, M2/GenesisGrammar `v1`/`v2` history.
- **B1** (24 `m3:*` prefixed-but-undefined keys in M3_BicephalousPerspective) and
  **B2** (`formula`, `basis`, `value`, `characteristics`, `role`, `status`… —
  the data-vs-documentation decision of the scoping note §4). Many Family A
  conversions stay graph-invisible until their bare **parent** keys are resolved
  (e.g. M2 aspect/pole nodes).
- `tscg_metrics.py` `STANDARD_REPLACEABLE`: align with the approved table.
- `worksite.yaml`: WS-1 still has `items: []` — model the lots as items.

## 4. Parked (not WS-1)

- `ontology/TSCG_InstanceGrammar/M0_CONTEXT_TEMPLATE.json`: entirely built on the
  dead GenesisSpace → already scheduled as **WS-9 item AP-5**.
- `static/` poclet copies still carry relative prefixes (`m0`, `m1core`, `m2`…)
  → bogus IRIs → **WS-10** (M0 namespace harmonisation). check_m0 does not
  descend into `static/`.
- Pre-existing duplicate version labels in some instance changelogs (e.g. two
  "2.1.0" in TrophicPyramid) left as history.
- From the previous HandOver: `Binder` candidate, CodonReadingFrame poclet,
  stale `docs/reboot-kit/TSCG_FileTree.md`, OWL reasoner to run locally,
  `verify_multiplicity_lot.py` commit decision.
