# lib/simulation/FourLegs — PyGame generation (obsolete)

**Author:** Echopraxium with the collaboration of Claude AI
**Status:** OBSOLETE. Everything written with PyGame is to be migrated to
[`ThreeLegs`](../ThreeLegs/README.md). Do not extend; do not start a new PyGame simulation.
Formerly `src/tscg/simulation-engine/` (moved 2026-11-14).

## What it is

- `poclet_parser.py` — reads an M0 poclet (JSON-LD): components, thresholds from
  constraints, ASFID / REVOI scores, synergy, epistemic gap. Finds the repository root by
  walking up from its own folder. Reads score keys that the Debt Overview lists as debt
  (bare keys, `It_score`).
- one `*_sim.py` per poclet, physics hard-coded in each script (the black box that
  ThreeLegs removes: no law is declared, inspectable or checkable).
- `_00_*.txt`: notes from the time (a reasoner / RAG pipeline to generate PyGame
  simulations from an ontology). History, not an authority.

Run (if needed for comparison during a migration): `pip install -r requirements.txt`,
then `python <name>_sim.py`.

## Migration backlog (inventory of 2026-11-14, every `import pygame` in the repository)

| Poclet | PyGame script(s) | TwoLegs page in `static/` | Priority |
|---|---|---|---|
| ComplexChemicalSynapse | here + `instances/poclets/ComplexChemicalSynapse/` | none | **PyGame only** |
| tpack | here + `instances/poclets/tpack/` | none | **PyGame only** |
| TvTestPattern | `instances/poclets/TvTestPattern/` | none | **PyGame only** |
| ColorSynthesis | here | vanilla JS | |
| ExposureTriangle | here | p5 | |
| FireTriangle | here | p5 | |
| FourStrokeEngine | here + `instances/poclets/FourStrokeEngine/sim/` | p5 | |
| PhaseTransition | here + `instances/poclets/PhaseTransition/sim/` | p5 | |
| Transistor | here + `instances/poclets/Transistor/sim/` | vanilla JS | |
| KindlebergerMinsky | `instances/poclets/KindlebergerMinsky/sim/` | p5 | |
| MtgColorWheel | `instances/poclets/MtgColorWheel/sim/` | BabylonJS | |
| Vco | `instances/poclets/Vco/sim/` | p5 | |

Several scripts exist twice (here and in the poclet folder): before migrating one,
diff the two copies. `instances/poclets/Transistor/sim/` and `FourStrokeEngine/sim/`
also carry their own copy of `poclet_parser.py`.

A migration is done when the poclet's simulation runs on ThreeLegs (its physics in
`K.LAWS`, or declared out of scope in `kit/ENGINE_SCOPE.md`); the PyGame script(s) are
then deleted, and the poclet README no longer points to them.
