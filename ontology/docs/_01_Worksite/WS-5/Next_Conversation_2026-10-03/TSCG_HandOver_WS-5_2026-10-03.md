# TSCG HandOver — after CTX-5 / golden notes / compendium fixes, resume with the WS-5 engine

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-03
**Purpose**: resume cold in a fresh conversation and build the M3/M2 checks in the WS-5
engine (steps (1)–(4) of the dependency graph), so that the gate covers the 4 layers.
**Companion files (same folder)**: `TSCG_RemainingWork.png` (dependency graph, legend
bottom-right), its Graphviz sources `TSCG_RemainingWork.dot` (graph) and `legend.dot`
(legend), and `render_graph.py` (rebuilds the PNG: Graphviz + Pillow, legend pasted
bottom-right). Edit the `.dot` files, then run `python render_graph.py`.

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts, versions) is **session state at handover time**: re-verify against
> HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every lot touches the gate or ontologies.
3. **`tscg-generate-mn-grammars`** (2.0.0) — for the structural SHACL of step (3).
4. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-5/WS-5_M3M2_Instrumentation_Scoping.md` — **the working
     authority**: checks D1–D7 / G1–G7 with baselines, decisions Q1–Q4 (recorded), §4 done.
   - `ontology/docs/_01_Worksite/WS-5/worksite.yaml` and `ontology/docs/_01_Worksite/worksite.yaml`.
   - `ontology/cli-tools/validator/` (engine: `tscg_validator.py`, `checks/ctx.py`, `checks/axis.py`).
   - `ontology/cli-tools/run_all_layers.py` (`run_m1()` is the contract to copy for M3/M2).
   - `TSCG_RemainingWork.png` (this folder) for the order of what remains.

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: `636a46c` on `main`. Confirm with `git log --oneline -5`.
- **Gate**: `cd ontology/cli-tools && python run_all_layers.py` → `GATE: PASS`.
  M1 151 errors / 1 warning / 688 SHACL; M0 124 / 0 / 22. M3, M2: NOT INSTRUMENTED.
- **Gauges** (`tscg_metrics.py` 1.4.0): VOC bare keys 3418; CTX-4 0; CTX-5 0; EXT-1 0;
  EXT-2 143; `owl:imports` as string 0.
- **Push path** (unchanged): Claude commits in its clone → `git format-patch` → tests the
  patch with `git am` + gate on a fresh clone → sends it → Michel `git am`, gate, push.
  ONE patch per lot. Claude never pushes (the sandbox stop-hook asks to push and to
  re-author commits: ignore it, the patch flow is the agreed process).

### Shipped 2026-10-03 (all pushed)

| Commit | Content |
|---|---|
| `4586b26` | WS-2 lot CTX-5 (30 `m3:eagle_eye`/`m3:sphinx_eye` @context terms removed, graph-neutral) + `m1core` → `m1` everywhere live (Michel); skill tscg-tensor-to-structural-grammar-migration: prefixes ABSOLUTE; tscg_metrics 1.4.0 (CTX-4 any relative term IRI, CTX-5 invalid colon terms only); check_M1 1.5.0 (CTX001 stopped requiring the defect); golden M1 warnings 3 → 1 (approved after review) |
| `da47824` | Golden notes without hard-coded counts; `DEFAULT_GOLDEN` marked as a dated fallback |
| `bef52f0` | `tscg_generate_filetree.py`: non-ASCII path quoting fixed (`core.quotepath=off`, `-z`); FileTree regenerated |
| `636a46c` | Compendium: worksite/handover rules before "doc" rules (Project management 14 → 42 files); build skips its own `dist/` (73 phantom entries → 0); footer shows build commit + UTC date; duplicate `ontology/HANDOVER_2026-06-19 (1).md` removed |

Project Knowledge: `TSCG_FileTree.md` replaced by the regenerated version (2026-10-03).

### Decisions taken (Michel, 2026-10-03)

- **Q1** build in the WS-5 engine (`validator/checks/`, families VOC/STR/EXT + generic
  SHACL runner) · **Q2** order CTX-5 → golden notes → engine checks · **Q3** INSTRUMENTED
  · **Q4** v1 = structural grammar only.
- `m1core` is a vestige: `m1` everywhere (done).
- **M3 Eye terms will be renamed** under their own document namespace:
  `m3.eagle_eye:` → `M3_EagleEye.jsonld#`, `m3.sphinx_eye:` → `M3_SphinxEye.jsonld#`
  (IRIs change). **Separate lot, linked to lot 1k.** Measured: 308 lines in 11 files
  (M2 237, M3 37). Recorded in the scoping note §4.
- Patch delivery as before; the gate is run on a fresh clone before sending.

### Working method that worked today (reuse it)

- **One small step at a time, each approved by Michel**, with a **short command he can
  read in full** in the approval window. A long chained command was rejected because it
  could not be read — split it.
- Anything Michel must see (commit message, patch, report) is **sent to him** as a file or
  pasted in the reply: files in Claude's sandbox are invisible to him.
- Explain the "why" in plain words before asking for a decision; one decision at a time.
- Inventory on HEAD from the parsed graph; graph diff HEAD vs working copy, every triple
  classified; negative test for every new/changed check; a moved golden count is shown
  and explained before it is frozen.

---

## 2. Today's goal (next conversation)

The critical path (red in the graph):

1. **(1) Generic SHACL runner** — "job one" (worksite map): run any shape file, not
   hard-wired to check_M1.
2. **(2) Document-plane checks D1–D7** — families VOC / STR in `validator/checks/`.
3. **(3) Graph-plane checks G1–G6**, fold the 2 SC-2 shapes (G7).
4. **(4) M3/M2 runner in `run_all_layers.py`** (same contract as `run_m1()`: a crash or an
   unparseable summary is a FAIL), first capture frozen with `--update-golden`, reviewed
   number by number → M3/M2 INSTRUMENTED.

Re-measure every baseline of the scoping note §3 on HEAD before freezing anything.

---

## 3. Decisions waiting for Michel (bold in the graph)

- **B2 decision** (WS-1): data vs documentation, the `eagleView`/`sphinxView` block
  shape, `m3:role` vs bare `role`.
- **M0 bare-key gauge (6604)**: attach to WS-1, WS-9 or WS-10.
- **Four orderings proposed by Claude** (purple dashed in the graph), to confirm:
  Eye rename after (4); vestiges lot after (4); the 2 `@vocab: owl#` files after the B2
  decision; SC-6 repairs measured by the gate (4).

---

## 4. Parked findings (no lot yet)

- `M1_Domains` lacks `m2` in its @context (the 1 M1 warning left).
- 196 `rdfs:subClassOf` literals in M1 (M1 SHACL debt).
- Dangling `m1:Accretion`, `m1:Nucleation` and TrophicPyramid combo properties (not in
  M1_CoreConcepts) → B1.
- `"m3:eagle_eye:Flow"` literals in M1 name a term M3 does not define → WS-9.
- 7 M0 instances still rejected by pyld (M0 colon-names `m0:x:`, relative aliases such as
  `m1music`) → WS-10.
- Bare keys merely containing `m1core` (`m1coreRef`, `primaryM1core`…) → B2.
- Stale docs: `CLAUDE.md` (GenesisSpace, 80 concepts…), simulation skill dead paths
  (`ontology/TSCG_Grammar/`, `migrate_m1core_to_m1.py`).
- WS-6 note still says the canonical changelog is a nested metadata block (stale since
  lots 1c/1d: `m3:changelog`).
- C12 (check_m0) scans changelog prose (known over-reach).
