# lib/simulation — three generations of TSCG simulations

**Author:** Echopraxium with the collaboration of Claude AI

The folders follow the riddle of the Sphinx (four legs in the morning, two at noon, three
in the evening), read as stages of how a simulation relates to its map:

| Generation | Stage | What it is | Status |
|---|---|---|---|
| [`FourLegs/`](FourLegs/README.md) | the infant: groping, a personal map built from scratch (a proto-language) | PyGame simulations, one script per poclet, physics hard-coded in each; a reader of the M0 file (`poclet_parser.py`) | **obsolete**, to migrate |
| [`TwoLegs/`](TwoLegs/README.md) | the adult: knows and uses shared maps | one self-contained BabylonJS or p5 page per poclet (`instances/poclets/<Name>/static/`), shared conventions (UX controls) but no shared code; physics hard-coded in each page | frozen, to converge |
| [`ThreeLegs/`](ThreeLegs/README.md) | the sage: stereopsis map / territory, with a feedback loop; the third leg is the cane, an instrument | the Kit: a Synoptic (node editor) over one engine whose laws are data (`K.LAWS`); Panel (map) and scale model (territory) face to face | **active**: every new simulation |

Direction: everything converges to **ThreeLegs**. A simulation migrated there gets its
physics from `K.LAWS` (or claims, in `kit/ENGINE_SCOPE.md`, that it is out of the engine's
scope), never from code written for that one page.
