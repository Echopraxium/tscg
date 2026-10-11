# WS-13 — Phase 0 Change Request: Structural Core (Component, Interface, Boundary, Imbrication)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-11 (session of 2026-10-10) — v1.1.0
**Status**: Phase 0 — change request (not started; no file modified)
**Measured on**: HEAD `7d2cfb1` — re-measure at session start (head-over-memory)
**Worksite number**: WS-13 (renumbered from the draft "WS-14": the draft "WS-13 — Audit of L"
was folded into WS-3 as GS-3 / GS-4) — to register in `worksite.yaml`
**Depends on**: WS-3 GS-3 (`Convergence` carries L) · WS-1 decision B2 · SC-6
**Batched with**: WS-9 (AP-1…AP-4) and WS-10 (M0 lots) for the M0 migration
**Measured by**: WS-5 `lot-NSRESOLVE` (phantom references), future rule A / rule H checks
**Test bench**: *Digital-Logic-Sim* (github.com/SebLague/Digital-Logic-Sim, MIT), scope
"NAND → SR latch"; second bench for state: the *Rubik's Cube* exercise
**Pipeline**: `tscg-ontology-diagnosis-pipeline` (Phases 0 → 5) + `tscg-m2-candidate-filter`

---

## 1. Trigger

Digital-Logic-Sim offers a single primitive gate (`Nand`, in `ChipTypes.cs`) and lets the
user encapsulate any circuit as a `Custom` chip reusable inside other chips. It exercises
exactly the concepts below — and revealed defects in all of them.

## 2. Findings at HEAD

| # | Finding | Evidence |
|---|---|---|
| F1 | `m2:Component` is frozen as *elementary*; its `vs_Module` points to `m2:Module`, which **does not exist** | `M2_GenericConcepts.jsonld` |
| F2 | `m2:Imbrication = St × St` covers only **self-similar** nesting; heterogeneous recursive nesting (XOR chip made of NANDs) has no home. Used by **0** M0 instances | idem; grep `instances/` |
| F3 | **`m2:Interoperability` is a cross-layer homonym** of the Gm primitive `Im` (its own comment pleads "distinct from the REVOI types"); its content describes an *interface contract* | `M2_GenericConcepts.jsonld` |
| F4 | **`m2:Interface` is a phantom reference** — used with formula `St × It × F \| V + E` (= exactly `m2:Interoperability`) by the combo `Permeability`, by `M1_Mythology` and `M0_Yggdrasil`; never defined | `M1_CoreConcepts.jsonld` |
| F5 | **`m2:Boundary` is a phantom reference** — used in 3 M0 instances (Bmc, PhaseTransition, AdaptativeImmuneResponse), quoted in M1 Core, never defined | grep |
| F6 | **No formula-inheritance rule**: of 5 M2 subclass links, only 2 contain the parent's factors (`Duplication ⊂ Process`, `Tropism ⊂ Behavior`); 3 do not (`Step ⊂ Node`, `Transducer ⊂ Processor`, `Dissipation ⊂ Transducer`) | computed at HEAD |
| F7 | **Formula collisions as signals** (not defects — WS-3 rule R4: *a formula is not an identifier*): `Component` = `Node` = `Capacity`; `Link` = `Network`; `Action` = `Event`; `Dissipation` ≡ `Process` (R3 commutativity). Examined only where the test bench needs to discriminate | computed at HEAD |

(M3 wording finding on `Ss` moved to WS-3 as F8.)

## 3. Decisions taken (Michel, 2026-10-10)

- **D1 — Rule A (strict refinement), no forcing.** A subclass contains all of its parent's
  factors. When it does not, either the child formula is genuinely incomplete or the
  subclass link is wrong — never pad a factor to make it fit. To become a gate check.
- **D2 — `Component` migrates M2 → M1 Core** as a combo (decomposability test passed;
  M2 lighter = good epistemic sign; M1 Core hosts the combos needed by M1 extensions):
  ```
  m1:Component = Fm2(System, Interface, Role, Convergence)
  ```
  emergent property: *a system that is also a functional part of a larger whole,
  replaceable through its interface*. A Component **may be composite** (recursive via
  `m2:componentOf`) and has **1..n Process** (`m2:implementsProcess`), each with its own
  **Workflow** (network of `Step` / `Action` / `Event` / `Relation`).
  Reading of the parents: `Role = Ss | K` → its place in the whole (K) and its Symbol
  (Ss); `Convergence` (WS-3 GS-3) → its orientation toward the whole's Attractor (L).
- **D3 — State variables** (Markovian: the present configuration suffices, no history —
  e.g. a Rubik's Cube configuration) are carried by the contract **`m2:Stateful`**, which
  receives **T** — consistent with WS-3 GS-1 `State = It × D | T`. Not in the Component
  signature: a NAND has no own state variable, an SR latch has one — that contrast is
  what the poclet shows.
- **D4 — Port / connector = `m2:Node`** located on the boundary of a Component.
- **D5 — Interface = contract** (Map side, `| V + E`), structured like a
  `Network | V + E` of Ports; a System may *realise* it by playing a **Role** — role,
  not subclass (the System→Interface→System regress stops at Ports). Distinguish from
  `m2:ConceptContract` (meta-level capability) in an explicit distinction.
- **D6 — `m2:Interoperability` is removed and renamed `m2:Interface`.** No alias, no
  deprecated node. Repairs F4 at once.
- **D7 — Rule H (no cross-layer homonym)**: no M2 class may carry the label of an M3
  primitive — to become a gate check. Scan at HEAD: `Interoperability` was the only case.
- **D8 — Imbrication = homothetic case** of the composite Component (children isomorphic
  to the parent); its `vs_Composition` is rewritten accordingly.
- **D9 — Boundary** enters this worksite (defined together with Interface).

## 4. Lots (in execution order)

| Lot | Content | Prerequisite | Risk |
|---|---|---|---|
| **L0** | Register WS-13 in `worksite.yaml` | — | nil |
| **L1** | Rename `m2:Interoperability` → `m2:Interface`; define `m2:Boundary` | WS-5 `lot-NSRESOLVE` built (gauge: 2 phantoms → 0) · WS-1 B2 state known | low–moderate (2 M1 ext + 5 M0) |
| **L2** | Rule A and rule H as checks (negative tests) | WS-5 engine (done) · WS-11 GR-M2 placement | low |
| **L3** | Apply rule A to the 3 non-conforming links (likely: `Dissipation ⊂ Process` with a distinguishing factor or demotion; `Transducer` ± D; `Step` after WS-3 settles `Node`) | L2 · WS-3 L front | semantic (Michel) |
| **L4** | Create `m1:Component`; remove `m2:Component`; rewrite the distinctions that referred to it (`Channel.vs_Component`, `Node`, `Composable`…); T into `m2:Stateful`; rewrite `m2:Imbrication` | WS-3 GS-3 executed · SC-6 named-args form · Q2 answered | moderate–high |
| **L5** | M0 migration `m2:Component` → `m1:Component` (10 instances) | L4 · **batched inside WS-9 / WS-10 lots** (same files) | moderate |
| **L6** | Enrich `M1_Electronics` with digital logic (logic gate, Boolean signal, latch, clock) | L4 | low |

Collisions (F7): only `Link`/`Network` and `Action`/`Event` are examined, because the
poclet must discriminate wire vs circuit and produced vs occurring; the others are logged.

## 5. Open questions (Michel decides)

- **Q1** — Should `m2:Interface` add `Im` to its formula (`… | V + E + Im`)? For: the
  contract exists to make interoperation possible. Against: may reintroduce the homonymy
  through the formula.
- **Q2** — Can an M1 combo carry both `m1:comboOf` and a subclass link to `m2:System`
  without violating SC-1? To verify at HEAD before L4.
- **Q3** — `Action` / `Event` discrimination: Gs poles `_^` / `_$` (produced /
  occurring), or another factor? (Precedent R4: `Synergy = It × D | _^ / _$` shares its
  Territory core with Event, Trigger and Action.)

## 6. Impact (measured at HEAD `7d2cfb1`; re-measure in Phase 1)

| Change | Files referencing today | Overlap |
|---|---|---|
| `m2:Component` → `m1:Component` | 10 M0: FireTriangle, Vco, Ptoe, RGB_Additive, QRCodeToPocketCity, TPACK, FourStrokeEngine, ExposureTriangle, CellSignalingModes, TriskeleToolchain | WS-9 AP-1 (FireTriangle), AP-2 (RGB), AP-3 (ExposureTriangle); WS-10 lots |
| `m2:Interoperability` → `m2:Interface` | M2 (definition + 1 internal list); M1 Electronics, M1 Education; 5 M0: Bmc, Transistor, Kidneys, PhaseTransition, TriskeleToolchain (`ontology/Ref/` archive untouched) | WS-9 AP-4 (Transistor) |
| `m2:Interface` (now resolves) | M1 Core (`Permeability`), M1 Mythology, M0 Yggdrasil | — |
| `m2:Boundary` (now resolves) | M0 Bmc, PhaseTransition, AdaptativeImmuneResponse; M1 Core | — |

The gate's M2 / M1 / M0 counts will move: show the moves to Michel before any
`--update-golden`. Every new node: **zero bare keys** (WS-1 rule).

## 7. Phase 1 — baseline to run before any lot

```bash
cd ontology/toolchain && python run_all_layers.py          # must end GATE: PASS
python ontology/toolchain/validator/tscg_validator.py --layers M2 M1 M0 --doc --ext --shacl --report pre_WS13.json
python ontology/toolchain/check-M1/check_M1.py             # from ontology/toolchain/
python ontology/toolchain/check-M0/check_m0_instances.py
python ontology/toolchain/tscg_metrics.py                  # VOC / DUP gauges before
```

## 8. Follow-up deliverable

Poclet **Digital-Logic-Sim — "From NAND to memory"** (`tscg-instance-pipeline`).
Steps 1–2 (Proposition, `analysis.md`) can run **now** — no ontology file, and they are
the field evidence for this worksite. Step 3 (M0) after L4, with the final concepts.
Content: NAND universality → encapsulation (composite Component, port promotion: inner
`In`/`Out` become the chip's pins) → SR latch (cycle in the Workflow, bistable Attractor,
`Stateful`).

## 9. Exit criteria

Gate PASS (or approved moved counts), no new validator finding, NSRESOLVE phantoms = 0,
rule A and rule H checks live with negative tests, Phase 4 semantic approval by Michel,
`m3:changelog` entries written.

## 10. Changelog

| Version | Date | Changes |
|---|---|---|
| 1.1.0 | 2026-10-11 | Renumbered WS-14 → WS-13 (L audit folded into WS-3 GS-3/GS-4). F7 reframed per WS-3 R4 (collisions are signals). Lots L0–L6 ordered against WS-1/3/5/9/10/11 and SC-6. Ss finding moved to WS-3 F8. |
| 1.0.0 | 2026-10-10 | Draft (as WS-14). |
