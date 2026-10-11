# TSCG HandOver (complement) — WS-5, after the 2026-10-10 Digital-Logic-Sim session: new targets for the validator, WS-13 registered, WS-3 L cluster

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-11
**Complements**: `ontology/docs/_01_Worksite/WS-5/Next_Conversation_2026-10-06/TSCG_HandOver_WS-5_2026-10-06.md`
— read that one first: its critical path, decisions and parked findings remain valid.
This file only adds what the 2026-10-10 session changed.
**Suggested location**: `ontology/docs/_01_Worksite/WS-5/Next_Conversation_2026-10-11/`
**Companion files (same folder)**:
- `WS-13_Phase0_Structural_Core.md` (new worksite — to register)
- `WS-3_Addendum_GS-3_GS-4_L-Cluster.md` (to merge into the WS-3 README → v1.1.0)

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every lot touches the gate or ontologies.
3. **`tscg-m2-candidate-filter`** — only for WS-13 L4 / WS-3 decisions.
4. Then read from HEAD: the 2026-10-06 HandOver (above), `TSCG_Debt_Overview.md`,
   `worksite.yaml` (+ `WS-n/worksite.yaml`), `WS-3/M2_Formulas_Review_with_Gs_README.md`.

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: `7d2cfb1` (2026-10-10 20:26). No commit was produced by the 2026-10-10
  session: it was analysis and decisions only. Confirm with `git log --oneline -5`.
- **Gate**: not re-run in that session — run `cd ontology/toolchain && python
  run_all_layers.py` first; expect `GATE: PASS` with the 2026-10-06 frozen counts
  unless commits landed in between.
- **Working copy in flight**: none in the repo. Three documents to commit (this file +
  the two companions).

---

## 2. What changed since 2026-10-06

The *Digital-Logic-Sim* poclet candidate (SebLague, MIT — a NAND-only logic sandbox with
recursive chip encapsulation) was used as a test bench for `Component`. It surfaced debt
that the validator does not see yet, and two new worksite decisions.

### 2.1 New concrete targets for WS-5 validator lots

| Lot (from WS-5/worksite.yaml) | New evidence | Gauge proposal |
|---|---|---|
| **lot-NSRESOLVE** (anti-phantom) — todo | **2 phantom M2 references**: `m2:Interface` (M1 Core `Permeability`, M1 Mythology, M0 Yggdrasil) and `m2:Boundary` (M0 Bmc, PhaseTransition, AdaptativeImmuneResponse; M1 Core) — used, never defined | `NSRESOLVE(M2)`: current 2 (to be confirmed by the check itself), target 0 — closed by WS-13 L1 |
| **lot-STR** (cross-file) — todo | `m2:Component.vs_Module` points to a non-existent `m2:Module` (a phantom *inside* a distinction text — decide whether STR scans prose references) | advisory |

**Recommended order inside WS-5**: keep the 2026-10-06 critical path (small M3/M2 lots,
worksite-map resync, `check_M1` double count) — then **lot-NSRESOLVE first** among the
remaining lots, because WS-13 L1 needs it as its gauge ("measure before fixing").

### 2.2 Two new checks proposed (placement to decide: WS-5 family or WS-11 GR-M2)

- **Rule A — formula inheritance** (DECIDED by Michel): a subclass's formula contains all
  of its parent's factors (commutative normalisation, WS-3 R3). At HEAD 3 of 5 M2
  subclass links fail (`Step ⊂ Node`, `Transducer ⊂ Processor`,
  `Dissipation ⊂ Transducer`). Fixes are semantic (WS-13 L3) — **never pad a factor**.
- **Rule H — no cross-layer homonym** (DECIDED): no M2 class may carry the label of an M3
  primitive. At HEAD the only case is `m2:Interoperability` (vs Gm `Im`), removed by
  WS-13 L1.

Both must come with negative tests in `ontology/toolchain/validator/tests/`. If the gate
freezes them before WS-13 L1/L3, their counts enter `golden_values.json` as frozen debt
(rule A: 3, rule H: 1) and go down lot by lot.

### 2.3 Worksite registry changes

- **Register WS-13** "Structural Core" in `worksite.yaml` (priority to set by Michel;
  dependencies: WS-3 GS-3, WS-1 B2, SC-6; batched with WS-9 / WS-10; measured by
  NSRESOLVE + rules A / H). Suggested items: L0…L6 from the WS-13 document.
- **WS-3**: merge the addendum (GS-3 `Convergence = A × F × D | L` DECIDED; GS-4
  "L = sense, Tropism = consumer" principle DECIDED; findings F7 L label, F8 Ss wording;
  L work front). Add the WS-3 gauge already requested on 2026-10-06 (§3.1c: share of M2
  formulas using a nominal Gs primitive) — the L work front will move it.
- **WS-9 / WS-10**: add a note that the M0 migration `m2:Component → m1:Component`
  (WS-13 L5) rides along their lots — FireTriangle (AP-1), RGB (AP-2),
  ExposureTriangle (AP-3), Transistor (AP-4, also touched by the Interface rename).
- **Do not create a separate "L audit" worksite**: it is folded into WS-3.
- `TSCG_RemainingWork.dot` (2026-10-06 folder): add WS-13 and its edges
  (WS-3 → WS-13, NSRESOLVE → L1, WS-1 B2 → L1/L4, SC-6 → L4, WS-9/WS-10 ⇄ L5), then
  `python render_graph.py`.

---

## 3. Decisions waiting for Michel (added to the 2026-10-06 list)

1. WS-13 **priority** in the registry.
2. Placement of the rule A / rule H checks: WS-5 validator family or WS-11 GR-M2.
3. Freeze rules A / H in the gate now (frozen debt) or only after WS-13 L1 / L3.
4. WS-3 open points: poles on `Convergence` (GS-3), `Tropism` formula (GS-4), renaming
   L (F7, M3 change).
5. WS-13 Q1–Q3 (Interface + `Im`?, combo + subclass under SC-1, Action / Event).

---

## 4. Next goal (proposed)

1. Run the gate; commit the three documents (registry + WS-3 merge) as one
   documentation lot — no count should move.
2. Continue the 2026-10-06 critical path.
3. Build **lot-NSRESOLVE** with its negative tests; freeze its first measurement.
4. In parallel, conversation-only: WS-3 L cluster sessions (Michel's decisions), and
   Steps 1–2 of the Digital-Logic-Sim poclet (`analysis.md`, no ontology file).

Push path unchanged (2026-10-06 HandOver §1): one patch per lot, tested with `git am` +
gate on a fresh clone; Michel applies and pushes.
