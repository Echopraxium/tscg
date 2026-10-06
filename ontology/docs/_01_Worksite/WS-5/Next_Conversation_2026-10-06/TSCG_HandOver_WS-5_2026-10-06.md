# TSCG HandOver — WS-5 critical path done (gate covers M3→M0); next: LayerCake Health tab

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-06
**Purpose**: resume cold in a fresh conversation. The WS-5 critical path is closed: the
gate measures the four layers. Next: the Compendium tab "LayerCake Health", then the
small debt-reduction lots.
**Companion files (same folder)**: `TSCG_RemainingWork.png` (dependency graph, legend
bottom-right), its Graphviz sources `TSCG_RemainingWork.dot` and `legend.dot`, and
`render_graph.py` (Graphviz + Pillow). Edit the `.dot` files, then `python render_graph.py`.

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts, versions) is **session state at handover time**: re-verify against
> HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every lot touches the gate or ontologies.
3. **`tscg-generate-mn-grammars`** (2.0.0) — only if a lot touches a SHACL grammar.
4. Then read from HEAD:
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` — **the working authority** for
     the debt: how it is measured, the map, debt by owner, questions §6, reduction §7.
   - `ontology/docs/_01_Worksite/WS-5/WS-5_M3M2_Instrumentation_Scoping.md` §7–§10
     (steps 1–4 as built) and `WS-5/worksite.yaml`.
   - For the Compendium tab: `cli_tools/compendium/build_compendium.py`,
     `compendium_template.html`, `Compendium_Generator_DesignNote.md`,
     `.github/workflows/pages.yml`, and `ontology/toolchain/tscg_layercake_health_map.py`.
   - `TSCG_RemainingWork.png` (this folder) for the order of what remains.

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of `ffa6206`. Confirm with
  `git log --oneline -12`.
- **Gate**: `cd ontology/toolchain && python run_all_layers.py` → `GATE: PASS`, the
  four layers INSTRUMENTED:

  | Layer | files | errors | warnings | shacl_violations |
  |---|---|---|---|---|
  | M3 | 5 | 148 | 619 | 7 |
  | M2 | 1 | 1 | 1368 | 8 |
  | M1 | 17 | 151 | 1 | 688 (= 344 violations, counted twice — §4) |
  | M0 | 43 | 124 | 0 | 22 |

- **Prerequisites**: `python -m pip install -r ontology/toolchain/requirements.txt`
  (rdflib, pyshacl, pyld). The gate names a missing package at start-up, with the
  interpreter it runs on, and FAILS.
- **Michel's machine has two Pythons**: `pip` → Python 3.12, `python` → Python 3.14.
  Always `python -m pip`. (pyld was "already satisfied" in 3.12 and missing in 3.14:
  the gate showed it as D7 +5 / +1.)
- **Push path** (unchanged): Claude commits in its clone → `git format-patch` → tests
  every patch with `git am` + gate on a fresh clone → sends it → Michel `git am`, gate,
  push. ONE patch per lot. Claude never pushes. When several patches are pending,
  send them renamed `1_…`, `2_…` (all `format-patch -1` files start with `0001-`).

### Shipped 2026-10-03 → 10-06 (all pushed)

| Commit | Content |
|---|---|
| `8db41cf` | `ontology/cli-tools` → `ontology/toolchain` (git mv); `owl_reasoning_test` moved in from root `cli_tools/`; `CLI_TOOLS_DIR` → `TOOLCHAIN_DIR` (alias kept); live refs updated, dated archives untouched |
| `c2ac85a` | WS-5 (1) generic SHACL runner (`validator/checks/shacl_runner.py`, engine 0.2.0): one finding per `sh:ValidationResult`, focus count per shape, SHACL-BLIND, missing pyshacl = ERROR |
| `3720876` | WS-5 (2) document plane D1–D7 (`checks/doc.py`, `--doc`, engine 0.3.0), decision D5(a) |
| `1344c97` | WS-5 (3) structural grammar G1–G4 (`ontology/toolchain/grammars/M3_Structural_Schema_shacl.ttl`, registered for M3 and M2) + EXT G1b/G5/G6 (`checks/ext.py`, `--ext`, engine 0.4.0) |
| `5baa97b` | WS-5 (4) M3/M2 INSTRUMENTED (`run_all_layers.py` 1.4.0 `run_engine`); first golden capture reviewed and frozen; `--update-golden` no longer rewrites unchanged layers' history |
| `c358267` | `TSCG_Debt_Overview.md` (master level) + map generator + first snapshot |
| `7470326` | `requirements.txt`, gate start-up package check (1.4.1), UserGuide setup step + dead `validate_m0_instance.py` path fixed |
| `a2a6ea8` | `python -m pip` everywhere; gate prints its interpreter (1.4.2) |
| `ffa6206` | UserGuide: Claude project is **"TSCG Workshop v1"** (was "TSCG Cyclop v0") |
| *(this lot)* | map renamed **LayerCake Health Map** (`tscg_layercake_health_map.py` 0.4.0, `_01_Worksite/LayerCakeHealthMap/`); snapshot regenerated on `ffa6206`; this HandOver |

### Decisions taken (Michel, 2026-10-03 → 10-06)

- `ontology/cli-tools` → `ontology/toolchain`; root `cli_tools/` **kept**;
  `owl_reasoning_test` belongs under `ontology/toolchain/`.
- **One validation script** (`tscg_validator.py`): grammars are DATA, not scripts.
  New grammars live in **`ontology/toolchain/grammars/`**; the 3 existing ones (M1, M0,
  SC-2) move there in a later lot.
- **D5(a)**: the only changelog is `m3:changelog` on the owl:Ontology node; any other
  "changelog" key (any case) is a finding.
- G2: label = `rdfs:label` **or** `skos:prefLabel`; G2 covers TSCG-namespace terms only;
  changelog dates checked for **format** `YYYY-MM-DD` (no `xsd:date` in v1).
- First M3/M2 golden capture **approved number by number** and frozen.
- Debt document: **(c)** = master-level document now **(b)**, worksite-map resync
  later **(a)**. It belongs at master level, not in WS-5 (instrument) nor WS-0.
- **LayerCake Health Map** (name by Michel): concentric hex map, M3 at the centre;
  one cell per node, one meta-hexagon per cluster (M3: the three Eyes on three axes
  Gt/Gm/Gs; M2: families; M1: domains; M0: instances); "persillé" cells; links only
  where the data carries a relation; colours **green** none · **bright orange** bare
  keys · **magenta** other technical debt · **red** invisible/misread · grey not
  measured. Generated, never hand-drawn; snapshots dated and named after a HEAD
  commit that is on `main`.
- **Compendium tab "LayerCake Health"**, generated at build time. Visibility
  proposed **KitArchitect only** — not explicitly confirmed (§3).
- Claude project name: **TSCG Workshop v1**.

### Working method that worked (reuse it)

- One small step at a time, approved by Michel; short commands he can read in full.
- Anything Michel must see is **sent** (files in the sandbox are invisible to him).
- Every new check gets a **negative test**; every shape a **focus count ≥ 1**;
  parity with the existing instrument before anything is frozen.
- Test the gate **after each patch**, before pushing (it caught a missing pyld that
  Claude's sandbox could not have seen).
- Generate dated artefacts (snapshots) on a commit that is on `main`, never on a
  local commit (git am gives the pushed commit another SHA).

---

## 2. Next goal

The critical path is red in the graph:

1. **(1) Compendium tab "LayerCake Health"** (KitArchitect only):
   `build_compendium.py` calls `tscg_layercake_health_map.py --no-png` into `dist/`,
   the template gets a rubric showing the SVG **inline** (tooltips work); if the
   generation fails in CI, the tab says "map unavailable: <reason>" — never an empty
   tab. `pages.yml` installs `requirements.txt` (no Playwright). One patch.
2. **(2) Small safe lots on M3/M2** (~25 points): 5 headers (G1), 5 changelog vestiges
   (D5), 10 labels/comments (G2 — **text by Michel**). Each lowers a frozen counter,
   re-frozen with `--update-golden` and the reason in the commit.
3. **(3) Worksite-map resync (a)**: `_00_TSCG_Worksite_Map.md` v2.3.0 dates from
   2026-08-08; sync it and add gauges to `worksite.yaml` (incl. a WS-3 gauge if §3.3).
4. **(4) `check_M1` double count**: 688 lines = 344 violations; fix and re-freeze with
   the change of unit documented.

---

## 3. Decisions waiting for Michel

1. **Debt overview §6**: (a) confirm the 22 M2 classes without family are all
   meta-schema; (b) the 16 M0 instances with no M1 domain link — expected or a gap;
   (c) WS-3 gauge "share of M2 formulas using a nominal Gs primitive", no target.
2. **Compendium tab visibility**: KitArchitect only (proposed) or KitCrafter too?
3. **B2 decision** (WS-1) — the biggest lever: removing the two `@vocab: owl#` turns
   the red core of the map (D2 2 + G6 142 drop together).
4. **M0 bare-key gauge (6604)**: attach to WS-1, WS-9 or WS-10.
5. **Orderings proposed by Claude** (purple dashed in the graph): Eye rename after the
   gate (now possible); vestiges inside lot (2); the 2 `@vocab` files after B2; SC-6
   repairs measured by the gate.
6. Optional: a short spike of `open-ontologies` (Rust, MCP, OWL2-DL reasoner, linting)
   as a COMPLEMENT (reasoner, pitfalls) — it cannot see bare keys.

---

## 4. Parked findings (no lot yet)

- `check_M1` counts each SHACL violation twice ("Message:" + "Focus Node:").
- `tscg_metrics --shacl --shacl-path <M2 grammar>` never measured M2 (M1 files only,
  "(SC-1)" messages only); golden `_known_pre_existing_not_counted_here` quotes July
  figures.
- M0: **28** instances fail strict JSON-LD expansion (18 relative `@context` IRIs,
  10 CTX-5 terms) → WS-10. (The 2026-10-03 HandOver said 7.)
- The two copies of `M0_Triz_Examples.jsonld` have no `owl:Ontology` node: invisible to
  every M0 shape, counted as passing by C15; also a duplicate.
- `m2:FeedbackLoop` formula `m2:Process × m2:Alignment × m2:Homeostasis` — a combo of
  named concepts written with `×` → SC-8.
- 13 M1 domains do not link to any M2 concept (combos still carry monoidal formulas) —
  the SC-6 work list, dashed on the map.
- From 2026-10-03, still open: `M1_Domains` lacks `m2` in its @context; dangling
  `m1:Accretion` / `m1:Nucleation` → B1; `"m3:eagle_eye:Flow"` literals → WS-9; C12 scans
  changelog prose; WS-6 note stale; root `CLAUDE.md` stale; simulation-skill dead paths;
  untracked files on Michel's disk to triage (incl. anything left in the old
  `ontology/cli-tools/` folder, which git did not move).

## 5. Outside git — Project Knowledge to refresh

`UserGuide.md` (Michel, in progress), `TSCG_FileTree.md` (regenerated in several lots),
`TSCG_ReferenceCorpus.md` (paths changed by the toolchain rename). Provisioned skills
that cite `ontology/cli-tools/` (instance-pipeline, generate-mn-grammars,
ontology-diagnosis-pipeline) were updated in the repo — re-provision them from HEAD.
