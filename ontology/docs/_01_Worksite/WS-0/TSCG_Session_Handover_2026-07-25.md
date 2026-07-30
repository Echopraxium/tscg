# TSCG — Session Handover 2026-07-25

**Author**: Echopraxium with the collaboration of Claude AI
**Supersedes**: handover 2026-07-23.
**Companion**: `_00_TSCG_Worksite_Map.md` v2.0.0 — the durable index. This handover
is the SNAPSHOT of this session; the map is the standing structure. Read the map first.

**Authority**: `git show HEAD:<file>` only. Every figure below was measured against
HEAD during the session, then GRAVED — so HEAD has since moved past those numbers.
Re-measure at the start of the next session; do not trust the counts here as current.

---

## 1. WHAT WAS GRAVED THIS SESSION — SC-2 COMPLETE

WS-0 / SC-2 (notation reform) is **finished, verified on the real repo, pushed to
`origin/main`** in two commits + one fix commit.

**Commit 1 — CTX (isolated)**: `M2_GenericConcepts.jsonld` 16.18.1.
Two named defects, nothing else: CTX-4 (m2/m3 prefixes relative → absolute) and
CTX-1 (skos used but undeclared → declared). Unresolved predicates 174→0, triples
2345 unchanged, identifiers unchanged.

**Commit 2 — notation**: `M2_GenericConcepts.jsonld` 16.19.0 +
`M3_BicephalousPerspective.jsonld` 1.5.1 + `M2_GenericConcepts_README.md` 16.19.0 +
`cli-tools/check-M2/M2_MonoidalFormula_Schema_shacl.ttl` 0.1.0 +
`cli-tools/tscg_metrics.py` 1.1.0.
76 formula values migrated (58 Gt: S→St,I→It; 18 Gm: I→Im), 4 tensor-era TeX fields
deleted (triples →2343), "atom formula" → "monoidal formula" throughout.

**Commit 3 — fix**: `tscg_metrics.py` line 54 `VERSION = "1.0.0"` → `"1.1.0"`
(banner was inconsistent with the docstring; my packaging error, not Michel's).

**Regression verification on Michel's repo** (the real gate, done this session):
- `run_all_layers.py`: `fc` before/after = **no difference**, GATE: PASS, M1/M0 untouched.
- `tscg_metrics.py`: NOT-1 **43→0**; CTX-1 1→0; CTX-4 21→19; VOC occ 4287→4285
  (−2 = the two deleted `formulaTeX` bare keys); banner now `tool v1.1.0`.
- `git status`: `working tree clean`, up to date with origin/main.

Still owed by Michel (his formal gates, NOT done in-session): linter + Pellet on the
two jsonld. The green `tscg_metrics` gauge is not a reasoner verdict.

---

## 2. WORKSITE NUMBERING — NOW RECONCILED

Two numbering systems existed: the on-disk folders (sequential by creation) and the
map's WS-n (grouped by nature). They conflicted. Resolved this session by making the
**map authoritative** and renaming the folders to match. Michel applied:

```
_00_Worksite_00_SC1-9  →  WS-0   (Structural Cleanup, SC-1…SC-11)
_01_Worksite_01        →  WS-8   (Until Further Notice)   [was going to be WS-1]
_02_Worksite_02        →  WS-3   (M2 Formulas Review with Gs) [was going to be WS-2]
```

The naive sequential rename (WS-0/1/2) would have collided: in the map WS-1 = VOC and
WS-2 = CTX. Folder creation order carries no semantic meaning; the map groups by
subject. One identifier, one referent — the rule that also flagged the SC-5 debt (§5).

**Folders not yet created** for WS-1 (VOC), WS-2 (CTX), WS-4 (GrammarSignature),
WS-5 (Validator), WS-6, WS-7. Create as each opens.

---

## 3. DOCUMENTS PRODUCED THIS SESSION — NOT YET PLACED

These are in the session outputs, NOT in any commit. They are working documents, to
be placed under the appropriate `WS-n` folder or `docs/` per Michel's layout.

| file | version | destination | role |
|---|---|---|---|
| `_00_TSCG_Worksite_Map.md` | 2.0.0 | index root | **replaces the 2026-07-11 map**; merge of that map + WS-n scheme |
| `M2_Formulas_Review_with_Gs_Residues.md` | 1.0.0 | WS-3 | feeds the Gs worksite; pre-Gs cohort recorded before SC-2 erased the marker |
| `TSCG_GrammarSignature_Worksite_README.md` | 1.0.0 | WS-4 | scoping; five naming criteria, four open decisions |
| `tscg_term_registry.draft.json` | 0.1.0 | WS-5 | sample registry, 14 terms / 4 classes / 194 M2 predicates |

**Placement caveat**: the map v2.0.0 SUPERSEDES the 2026-07-11 map. The on-disk
predecessor content of `WS-0/` was READ during this session (two files surfaced:
`_01_Facet_as_M3_Principle_ArchitectureNote.md` and `cli-tools/README.md`) and
reconciled into map v2.1.0 (§5 findings updated, three corrections). No further
reconciliation known to be owed, but the WS-0 folder may hold more than those two
files — a full listing at HEAD would confirm.

**What the WS-0 read corrected** (folded into map v2.1.0):
- The 151/163 mystery is resolved (see §5) — a legitimate drop, stale note.
- **D11 is RULED** (not open): `cli-tools/README.md` states an option with an
  orthogonal axis + controlled value-set IS a facet, "ruled in SC-3". The map had
  SC-3 as fully un-graved; D11 specifically is decided even if `hasPolarity` is not.
- **Guard distinction is settled**: scalar guards (`| gain > 1`, `| λ > 0`) delete;
  enumerated guards (`| trajectoryShape=Circular`) keep — the differentia specifica.
- `cli-tools/README.md` v1.0.0 documents the **four silent SC-1 tooling bugs**
  (undefined `fix_imports_genesis`, `.shacl.ttl` vs `_shacl.ttl`, singular vs plural
  `symbolic-system-grammars`, hard-coded REPO_ROOT) and `tscg_paths.py`. It is the
  best description of the tooling and contradicts the assumption that the validator
  was under-documented. It also confirms `check-M2/`/`check-M3/` as the intended home
  for future checkers — exactly where SC-2's shape was placed.
- `_01_Facet_as_M3_Principle_ArchitectureNote.md` v0.1.0 supplies SC-3's substance:
  Decision A1 (Facet=axis, Focus=value) recommended, four open decisions (A axis vs
  registry, B StateFacet, v1 scope, sequencing vs Domain-fusion).

---

## 4. NEXT WORKSITE — one per session, opened from HEAD

Recommended order (map §2): **WS-5 engine → WS-2/CTX-4 → WS-0/SC-6**.

**WS-5 (Validator engine) — rank 2, recommended first.** This session proved the need
concretely: `tscg_metrics.py` hard-wires its SHACL pass to `check-M1`
(line 305) and IGNORES `--shacl-path` (line 400 is documented "path to
**M1**_Schema_shacl.ttl"). So decision D4 ("run the M2 shape via
`tscg_metrics --shacl-path`") rested on a capability the tool does not have — the M2
shape never actually ran; only the Python NOT-1 gauge did. The engine's first job is a
runner that executes an ARBITRARY shape file, plus a property-name manifest so gauges
stop being hard-coded strings (the NOT-1 gauge keyed on `endswith(...)` would read 0
silently the day WS-4 renames the property). Architecture already decided: Python
engine + Electron UI, JSON contract, headless rule, decision-capture not reporting,
engine-first scope guard.

**WS-2 / CTX-4 — rank 3, cheap alternative.** Gauge shows CTX-4 = 19; ~15 of those are
in 10 M1 extensions, mechanical like Lot A, golden-predictable and net-negative.
Clean: M1_CoreConcepts, M1_Domains, M1_Biology, M1_Chemistry, M1_BusinessModeling,
all 5 M3. Measure each file before/after; an unexplained delta blocks the commit.

Do NOT start SC-6 or VOC before WS-5: both are heavy and semantic, and become
measurable-per-decision once the engine exists instead of hand-adjudicated (as this
whole session was).

---

## 5. FINDINGS TO CARRY (measured this session, not yet actioned)

- **`tscg_metrics` SHACL is M1-only** (§4). → WS-5.
- **`check_M1` error count 151 vs 163 — RESOLVED, not a bug.** The `_01_Facet`/
  `cli-tools/README.md` (2026-07-13) gives the ventilation summing to 163
  (incl. `EXP001`=12). HEAD `golden_values.json` (measured 2026-07-23) reads
  **errors=151**, by_code `GCC009 4 / DCC010 18 / DCC009 1 / CTX001 3 / DCC006 127 /
  DCC008 1` — **EXP001 absent**. The 12 `EXP001` (retired D8
  `structuralGrammarFormulaExpanded`) were removed between 07-13 and 07-23 by the
  SC-6-partial work; the drop is legitimate and recorded in golden. **Only the prose
  `note` field still says "163"** — a stale narrative string, not a measurement
  defect. Fix: update that note to 151. This is NOT the `publicID=` Windows bug I
  earlier suspected. → tooling backlog (display only).
- **FRB gauge blind spot**: counts literal `⊗` (89) but NOT the `\otimes` macro
  (7, all inside the TeX fields SC-2 deleted). `(x)` is a false alarm outside
  M1_Geology. → SC-9.
- **SC-5 identifier collision**: `SC-5` denotes two referents in `M1_Schema_shacl.ttl`
  (Domain-fusion in a 2026-07-11 comment; SHACL-hardening in v1.2.0/1.3.0 changelog).
  First real test of the WS-n stability rule. → map §8 backlog.
- **9 SC-2 carve-outs** deferred to WS-3: 5 `m2:sphinxView` written in the ASFID
  alphabet (Behavior, Tropism, Workflow, Step, Action — a view in the wrong grammar),
  2 indexed generators, 2 prose glosses.
- **`Symmetry` (St) / `State` (It)**: correctly subscripted but single-primitive.
  Notation closed, semantics NOT. → WS-3.
- **`Gradient`** keeps prose `or` in `"F × T  or  It × T"`. → WS-3 debt.
- **δ₁ provenance**: ~17 scalar `m0:epistemicGap` (snapshot-measured), only 2 with a
  provenance marker; precision exceeds provenance; SpectralClass derives from them;
  the MultisubjectiveScoreEvaluationProtocol exists but was not followed. Needs a
  provenance field, not better numbers. HEAD path of M0 poclets not located this
  session — resolve the path first. → map §8.
- **Layered-architectures poclet** (candidate): a `m3:SystemicFramework` instance
  generalising MOF/OSI/Marr/TriskeleToolchain/Semantic-Web/TSCG — a taxonomy of layer
  relations. NOT named `StructuralGrammar`/`LayerCake` (loaded terms). Future.
- **`tscg-ontology-diagnosis-pipeline` skill**: Scenario 1 rates property renaming
  Risk:Low ~15min — true of execution, false of evaluation (this session spent five
  candidate names and ~20 measurements evaluating one rename). Add a Phase 0.5
  (name candidacy). → WS-4 §8.

---

## 6. METHOD NOTES REINFORCED THIS SESSION

- **Snapshots regress.** Michel's local `tscg_metrics.py` (already fixed to 1.1.0) was
  overwritten by my zip copy that still had `VERSION="1.0.0"`. `git diff` before
  commit, never after, would have shown the zip regressing his fix. HEAD is the only
  authority; a zip I produce is a snapshot and can be stale.
- **A gauge reading 0 is a claim, and claims get tested.** Three detector defects
  surfaced across two sessions (DUP-1 prefix, blank-node shape, FRB `\otimes`). Every
  gauge needs a fixture proving it can be non-zero.
- **My partial measurements were wrong where the tool's were right.** I measured on a
  fetched subset (no M0, not all extensions) and reported 4281 / 45; the real tool on
  26 canonical files gave 4287 / 43. Always prefer the tool on HEAD over my in-context
  arithmetic.
- **Two homonymous files by design**: lot_A and lot_B both ship
  `M2_GenericConcepts.jsonld` (16.18.1 and 16.19.0) — same file at two moments, to
  allow the isolated CTX commit. Not a duplicate; the sequencing device.

---

## 7. IMMEDIATE TODO (Michel, before next session)

1. Place the four session documents (§3) under their WS-n folders; the map v2.0.0
   replaces the 2026-07-11 map.
2. (optional) reconcile the map against the on-disk `WS-0/` predecessor content (§3 caveat).
3. Re-inject into "TSCG Cyclop v0" if that routine is kept.
4. Open ONE next worksite in a FRESH conversation, anchored on the updated HEAD.
