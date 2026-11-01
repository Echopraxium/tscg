# TSCG HandOver — WS-5, 2026-11-01: K0 done → lot K1 (first real bare-key reduction)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-11-01
**Follows**: `../Next_Conversation_2026-10-22/TSCG_HandOver_WS-5_2026-10-22.md` (superseded
for "what next"; still the reference for lot NS-SEP, which moves to §3).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** (1.2.0) — K1 changes M2 data; read its
   **debt-honesty rule** and **Scenario 5 (bare-key reduction)**.
3. Then read from HEAD:
   - `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` — hard invariant "Every term used
     is declared".
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` **§8.0g** (lot K0).
   - `ontology/M2_GenericConcepts.jsonld` — the declarations of `m2:eagleView` and
     `m2:sphinxView` (their `rdfs:comment` describes the expected inner keys).

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of `b502c47` (skill 1.2.0 repo copy)
  and `ff049bc` (lot K0).
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
   (owl property + `rdfs:label` in M2, with a `@context` entry). Michel decides each line;
   Claude never invents a meaning.
3. Phase 2: apply. Phase 3: gate — **D1 must drop by exactly the planned number, G8 must not
   rise** (a declared key is declared in M2 itself, so it is not a phantom). Show the move,
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
- `check_M1` counts every SHACL result twice (unchanged, its own lot).
- Worksite map `WS-0/_00_TSCG_Worksite_Map.md` still uses "SC-5b" for "SHACL-hardening".

## 5. Housekeeping

- Project Knowledge: reload `TSCG_FileTree.md` (new folder `WS-5/Next_Conversation_2026-11-01/`).
