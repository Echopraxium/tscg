# TSCG HandOver — WS-5, 2026-11-01: finish the ontology/docs cleanup → then lot K1

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-11-01
**Follows**: `../Next_Conversation_2026-10-22/TSCG_HandOver_WS-5_2026-10-22.md` (superseded
for "what next"; still the reference for lot NS-SEP, which moves to §3).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD before use.

---

## FIRST — finish the `ontology/docs/` cleanup (housekeeping, round 2)

Before K1, Michel wants the rest of the cleanup done. Round 1 (commit "Housekeeping
ontology/docs round 1", on HEAD) removed 19 files he decided. **69 files remain
undecided.** Why it matters: the RAG builder (`src/tscg/rag/create_tscg_rag.py` and its
high-compress twin) tags every file under `ontology/docs` as *authoritative ontology
documentation*, and the Compendium publishes them — obsolete vocabulary (tensor/⊗,
KnowledgeField, MetaConcept, GenesisSpace, ORIVE…) is served as authority.

- **Read first**: `_02_housekeeping/2026_11_01/Housekeeping_OntologyDocs_2026-11-01.md`
  (method, what was removed, what remains) and the table
  `_02_housekeeping/2026_11_01/OntologyDocs_Cleanup_Triage.xlsx` (yellow column = Michel's
  decision; empty = undecided).
- **Remaining (re-measure on HEAD)**: 53 with no live reference (proposal: delete),
  9 cited only by documents that are obsolete themselves (proposal: delete + remove the
  citing line), 6 to decide (`Poclet_Analysis_Methodology.md` — cited by CLAUDE.md, README,
  ReferenceCorpus, index.html and two instance READMEs but full of retired vocabulary;
  `TSCG_Architectural_Extensions.md` — cited by the ReferenceCorpus;
  `TSCG_M1_Architecture.md` — cited by M1_CoreConcepts; `M1_Mythology_Core_Concepts.md` and
  `CatastrophicBifurcation_M1_Analysis.md` — cited by the Yggdrasil README;
  `M0_VSM_Prerequisites_Analysis.md` — cited by the VSM session note), 1 to keep
  (`OntologyModeling_Guidelines.md`, live, cited by the M3 apex).
- **Method** (same as 2026-09-27 and round 1): Michel fills the table → Claude removes the
  decided files in one commit per group, fixes every LIVE line that cites a removed file
  (never the archive snapshot `ontology/Ref/`), checks name collisions (a live file with the
  same name elsewhere is not affected), appends a "round 2" section to the trace note,
  updates the table in `_02_housekeeping/2026_11_01/`, regenerates `TSCG_FileTree.md`, and —
  after Michel's push — updates `TSCG_FileTree.md` in the Project itself. Nothing is lost:
  `git show <commit>^:<path>`.
- **Not concerned**: the gate (reads no file of `ontology/docs`), the reasoner (no ontology
  file changes).
- **Next to look at, once `ontology/docs` is clean**: `docs/reboot-kit/` holds copies and
  summaries of the same era (e.g. `Cascade_Modeling_README.md`,
  `Namespace_Refactoring_Summary.md`, `Amplification_Integration_Summary (1).md`).

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** (1.3.0) — K1 changes M2 data; read its
   **debt-honesty rule**, **Scenario 5 (bare-key reduction)** and Phase 3.3 (Michel runs
   the reasoner; Claude asks and waits).
3. Then read from HEAD:
   - `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` — hard invariant "Every term used
     is declared".
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` **§8.0g** (lot K0).
   - `ontology/M2_GenericConcepts.jsonld` — the declarations of `m2:eagleView` and
     `m2:sphinxView` (their `rdfs:comment` describes the expected inner keys).

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver update, on top of `df5947d` (housekeeping
  round 1); before it: skill 1.3.0, gate 1.6.0 (reasoner reminder), grammar G2 0.3.0
  (hollow comments), lot K0.
- **Reasoner baseline for K1** (Michel, 2026-11-01, Windows, Java 25):
  `M2_GenericConcepts.jsonld` (+ 5 M3 imports) **PASSED** — no inconsistency, no
  unsatisfiable class. Noted, not blocking: "Reparenting … => owl.Thing" on several M2/M3
  properties (`valueRange`, `hasPolarity`, `arity`, `Fm2`, `Fm1m2`…) and the M3 monoidal
  types (`eagle_eye:typeS`…) typed both `owl:DatatypeProperty` and `MonoidalType` — likely
  punning; a candidate for a future role-separation lot.
- **Gate**: `GATE: PASS` on Linux and on Michel's Windows machine; the 5 engine test suites
  pass (61/61). M2: files 1, errors 169 (of which G8 168), warnings 1368 (= D1), SHACL 7.
- **K0 recap**: G8 (phantom TSCG predicates) in the engine and the gate; M1/M0 `engine`
  section frozen (D1, D7, G5, G8…); Health Map 0.5.0 colours G8. K0 **reduced nothing**: it
  revealed and froze. Real reductions start with K1.

## 2. Next goal — lot K1: the bare keys inside `m2:eagleView` / `m2:sphinxView`

Both properties ARE declared (`owl:ObjectProperty`, M2) — not phantoms. Their VALUES are
nested objects whose keys are bare: **423 D1 occurrences = 31 % of M2** (eagleView 209,
sphinxView 214). Measured on HEAD `b502c47`:

| Key | eagleView (67 nodes) | sphinxView (43 nodes) |
|---|---|---|
| `basis` | 67 — always `"ASFID"` | 7 — `"REVOI (via ASFID fallback)"` 5, `"REVOI"` 2 |
| `status` | 67 — `IMMUTABLE` 58, `PRIMARY` 8, `SECONDARY` 1 | 7 — `EXPERIMENTAL` 4, `IMMUTABLE`, `VALIDATED`, `PRIMARY` |
| `role` | 67 — `"Measure observable phenomenon"` 30, `"Measure territory perspective"` 17, 20 specific | 7 — all specific |
| `formula` | — | 7 |
| `formulaPrimary` | — | 36 (the only key in 35 nodes) |
| rare | `dimensionSemantics`, `formulaComposition`, `formulaDecomposition`, `constraint` (1 each) | `dimensionSemantics` 1 |

Also: the `rdfs:comment` of `m2:sphinxView` announces "a primary formula … and a fallback
formula"; the data holds mostly `formulaPrimary` alone — a doc/data drift to settle in K1.

**Method** (Scenario 5 of the pipeline skill):
1. Phase 1: gate baseline; note M2 D1 (warnings) and G8.
2. **Decision table** (xlsx, like SC-5b, in `WS-5/K1/`): one line per key × property, the
   value profile above, and the options **delete** (redundant / derivable — e.g. `basis`
   under eagleView is implied by the property itself), **map** (to an existing property —
   check HEAD first, e.g. whether a formula property already exists in M2), **declare**
   (owl property + `rdfs:label` + an `rdfs:comment` **written or approved by Michel**, in
   M2, with a `@context` entry). Michel decides each line; Claude never invents a meaning.
   Guard: G2 (grammar 0.3.0) refuses a hollow comment — blank, = label, < 3 words, TODO/
   TBD/… — so a token declaration fails the gate (G2 +1) even though G8 does not move.
3. Phase 2: apply. Phase 3: gate — **D1 must drop by exactly the planned number, G8 and
   G2 must not rise** (a declared key is declared in M2 itself, so it is not a phantom). Show the move,
   `--update-golden`, reason written.

## 3. Then, in order

1. **Lot NS-SEP** — unchanged (HandOver 2026-10-22 §2): one prefix per defining file; two
   questions first (archives untouched? extension-local properties renamed too?). Now
   guarded by G8: a rename that breaks a declaration/use pair shows up as +G8.
2. **K2** — `m2:possibleValues` (404 bare keys in M2; also a phantom predicate itself:
   72 triples) and `m2:perspective` (phantom, 86 triples).
3. **Lot M0** (HandOver 2026-10-22 §3) — now also owns M0 D7 (28 instances rejected by a
   strict JSON-LD processor) and G5 (129).
4. **SC-5c** — usefulness test first.

## 4. Notes

- **Correction recorded in this commit**: K0's Debt Overview §8.0g and the K0 commit message
  listed `m2:eagleView` among the phantom predicates — wrong: it is declared. §8.0g is
  corrected; the commit message (pushed) stays as is.
- G2's hollow-comment guard covers M3/M2 only: register it for M1/M0 before any lot that
  declares properties there.
- `check_M1` counts every SHACL result twice (unchanged, its own lot).
- Worksite map `WS-0/_00_TSCG_Worksite_Map.md` still uses "SC-5b" for "SHACL-hardening".

## 5. Housekeeping

- Project Knowledge: reload `TSCG_FileTree.md` (new folder `WS-5/Next_Conversation_2026-11-01/`).
