# WS-13 — Phase 0 Addendum A: Interface as an M1 combo

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-11-07 — v1.0.0
**Status**: Phase 0 — decisions taken by Michel (2026-11-07); **no ontology file modified**
**Amends**: [`WS-13_Phase0_Structural_Core.md`](WS-13_Phase0_Structural_Core.md) v1.1.0 — revises D5, D6 and lot L1, closes Q1
**Measured on**: HEAD `aefb464` — re-measure at session start (head-over-memory)
**Evidence source**: TSCG Kit (`kit/`), the "map of scenarios" design and its *friction log*
(Claude Doc "TSCG Kit — Articulation des scénarios", 2026-11-07)
**Pipeline**: `tscg-m2-candidate-filter` (for `m2:Boundary`) + `tscg-ontology-diagnosis-pipeline` (Phases 0 → 5)

---

## 1. Trigger

The TSCG Kit asks, for every block and every wiring pattern a player builds, *which M2 or
M1 class would type it*. Designing the "house" scenario (rooms separated by walls, floors
and doors) needed a block for what separates two rooms and lets heat through. Typing it
hit the two WS-5 phantoms (`m2:Interface`, `m2:Boundary`) and the rule-H homonym
(`m2:Interoperability` vs the Gm primitive `Im`) — the same defects F3, F4 and F5 that
the Digital-Logic-Sim bench had found. Two independent benches, one diagnosis.

## 2. Findings (in addition to F1–F7)

| # | Finding | Evidence at HEAD |
|---|---|---|
| A1 | D6 (rename `Interoperability` → `Interface`) keeps a **single atom** for what is a composite: a limit, an intermediary through which the two sides interact, and shared rules. The current `Interoperability` comment already lists three ingredients (S "interface architecture", I "format and encoding", F "exchange protocol") | `M2_GenericConcepts.jsonld`, `m2:Interoperability` |
| A2 | Under SC-1 a combo formula is a function signature: **named concepts only, no monoidal operator, no primitive argument** (M1 SHACL SHAPE 9). So Q1 ("add `Im` to Interface's formula") can only be answered for an *atom*; for a combo it is moot | `toolchain/check-M1/M1_Schema_shacl.ttl` SHAPE 9 |
| A3 | SC-1 already allows **M1 combos as arguments of `Fm2`** (precedents: `m1:Propagation`, `m1:CascadeAmplification` take `m1:Cascade`). Michel confirms it as a regulation of Layer Cake overcrowding (2026-11-07) | `M1_CoreConcepts_README.md` (SC-1), `M1_CoreConcepts.jsonld` |
| A4 | `m1:Permeability = Fm2(Channel, Interface, Gradient)` and its comment says "neither purely static (a Boundary) nor fully open (a Channel)": it already reasons with Boundary, which does not exist | `M1_CoreConcepts.jsonld` |
| A5 | Stale cross-references found on the way (not defects of this worksite, logged): `Interoperability.vs_Mediator` quotes Mediator as `S × I × F × O` (HEAD: `F × It \| K`); `m1:Processor`'s comment names a Map combination `Fm2(Transformation, Representation, Interoperability)` | `M2_GenericConcepts.jsonld`, `M1_CoreConcepts.jsonld` |

## 3. Decisions (Michel, 2026-11-07)

- **DA1 — Interface is an M1 combo**, not an M2 atom:
  ```
  m1:Interface = Fm2(Boundary, Mediator, Code)
  ```
  - `m2:Boundary` — the limit between two systems (to define, see DA3);
  - `m2:Mediator` (`F × It | K`) — the intermediary *through which* the two sides interact;
    preferred to `m2:Channel` (`St × F | Ss`, a permanent conduit): an interface is not
    necessarily crossed by a flow (a socket with nothing plugged in is still an interface);
  - `m2:Code` (`It × Ss`) — "system of rules for systematic transformation between
    domains": the shared rules (protocol, contract) both sides follow. Preferred to
    `m2:Constraint` (any boundary restricts) and to `m2:Signature` (identification pattern;
    the software sense would create a new homonym).

  Proposed emergent property (to word in Phase 2): *a limit through which two systems
  interact by way of an intermediary that follows rules shared by both sides.*

- **DA2 — D6 revised: `m2:Interoperability` is removed, not renamed.** Its content is
  carried by the combo (S → Boundary / Mediator, I → Code, F → Mediator). Rule H then has
  no case left at HEAD. No new M2 concept is created (`m2:Protocol`, considered on the way,
  is not needed): one M1 combo more, one M2 atom less.

- **DA3 — `m2:Boundary` is defined first** (D9 unchanged, but now a prerequisite of
  DA1): through `tscg-m2-candidate-filter` (decomposability, transdisciplinarity,
  atomicity). Its formula is not proposed here.

- **DA4 — D5 revised**: the *contract* side of D5 is carried by `Code` inside the combo;
  the rest of D5 stands — Ports are `m2:Node` on the boundary (D4), a System *realises*
  an Interface by playing a `Role` (role, not subclass). `m2:ConceptContract` stays a
  distinct meta-level capability.

- **DA5 — Q1 closed**: no `Im` in Interface (a combo carries no primitive). Whether
  interoperability as a *measurement axis* (REVOI `Im`) applies to a model of an interface
  is an M3 question, unchanged.

- **DA6 — rule recalled (high priority)**: monoidal types are used only in M2 atom
  formulas; using them inside `Fm2` / `Fm1m2` would short-circuit M3 → M1. Already
  enforced by M1 SHACL SHAPE 9 (gate); the last M1 report at HEAD still lists cases that
  belong to SC-6 (e.g. `m1:Oscillator` guard `| trajectoryShape=Circular`, GCC009;
  `ElectronicOscillator` in `Fm1m2(Electronics, S × A × I × D × F)`, DCC006).

## 4. Lot L1, revised (replaces L1 of v1.1.0)

| Lot | Content | Prerequisite | Risk |
|---|---|---|---|
| **L1a** | Define `m2:Boundary` (candidate filter, then Phase 2 wording) | WS-5 `lot-NSRESOLVE` built | low–moderate |
| **L1b** | Create `m1:Interface = Fm2(Boundary, Mediator, Code)` in M1 Core | L1a | low |
| **L1c** | Remove `m2:Interoperability`; re-point every reference **case by case** (to `m1:Interface`, or to `Code` / `Mediator` when only one ingredient is meant) | L1b | moderate (semantic, Michel) |
| **L1d** | Re-point the `m2:Interface` phantom to `m1:Interface` (namespace change) | L1b | low |
| **L1e** | Revise `m1:Permeability` — Michel chooses: **P1** `Fm2(Boundary, Channel, Gradient)` or **P2** `Fm2(Interface, Gradient)` (allowed by A3) | L1b | semantic (Michel) |
| **L1f** | Fix the stale cross-references of A5 | L1c | nil |

L4 is unchanged in content: `m1:Component = Fm2(System, Interface, Role, Convergence)`
now takes an M1 combo as argument, which A3 allows.

## 5. Impact (measured at HEAD `aefb464`)

| Change | Files referencing today |
|---|---|
| `m2:Interoperability` removed (L1c) | M2 (definition + 1 internal list); M1 Electronics (+ README), M1 Education (+ README); 5 M0: Bmc, Transistor, Kidneys (+ README), PhaseTransition, TriskeleToolchain; text mention in `m1:Processor` |
| `m2:Interface` → `m1:Interface` (L1d) | M1 Core (`Permeability`), M1 Mythology; M0 Yggdrasil (+ README, `Heimdall_Interface_Constraint_Analysis.md`) |
| `m2:Boundary` now resolves (L1a) | M0 Bmc (+ README, `static/src/Bmc.js`, `usecases.js`), PhaseTransition (+ READMEs), AdaptativeImmuneResponse; M1 Core README; TscgPocletMiner corpus |

The gate's M2 / M1 / M0 counts will move (one M2 atom less, one defined, one M1 combo
more): show the moves to Michel before any `--update-golden`.

## 6. Test table (field check of DA1)

| Case | Boundary | Mediator | Code |
|---|---|---|---|
| Cell-membrane receptor | membrane | receptor | ligand–receptor specificity |
| USB port | connector | controller | USB protocol |
| Diplomatic border | border | embassy | diplomatic protocol |
| Port of a TSCG Kit block | edge of the block | the port | flux / information typing and wiring rules |

## 7. Open questions (Michel decides)

- **AQ1** — `Interoperability.vs_Mediator` says Mediator is "a third-party intermediary",
  whereas interoperability is "a property of the interface itself". Does `m2:Mediator`'s
  definition cover an intermediary that *is part of* the interface (a receptor, a port),
  or must its comment be widened in L1b?
- **AQ2** — Where do `Interoperability`'s REVOI views (V + E: verifiable and evolvable
  contracts) go? In the combo's comment as an emergent property, in `Code`, or nowhere
  (a Map-quality concern, not a Territory pattern)?
- **AQ3** — P1 or P2 for `m1:Permeability` (L1e).

## 8. Consequence for the TSCG Kit

The "house" workshop (Kit patch after the composite blocks) types its pieces on this
basis: a **Frontière** (Boundary) block between rooms (wall, floor, door — the door adds
`m1:Permeability`), the **port** as Mediator, the **wiring rules** as Code. It waits for
L1a–L1b so that it never relies on a phantom.

## 9. Exit criteria

Those of v1.1.0 §9, plus: `m2:Interoperability` absent from the live corpus, rule H scan
= 0, NSRESOLVE phantoms = 0, AQ1–AQ3 answered, `m3:changelog` entries written.

## 10. Changelog

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-11-07 | Interface as `Fm2(Boundary, Mediator, Code)` (DA1); Interoperability removed, not renamed (DA2); Boundary first (DA3); D5 revised (DA4); Q1 closed (DA5); SC-1 rule recalled (DA6); L1 split into L1a–L1f; impact measured at `aefb464`. |
