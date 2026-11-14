# WS-14 — Simulation convergence (FourLegs / TwoLegs → ThreeLegs)

**Author:** Echopraxium with the collaboration of Claude AI
**Opened:** 2026-11-14 · **Status:** scoped · **Priority:** to set by Michel
**State:** [`worksite.yaml`](worksite.yaml) (source of truth for items and status)

## Origin

Playing the Kit's Thermostat workshop, Michel named a "black box" problem, the
*electronic-piano syndrome*: the demo key plays by itself and gives the illusion of
knowing how to play (in the literature: illusion of explanatory depth, Rozenblit & Keil;
fluency illusion, Bjork; blackboxing, Latour). Reading HEAD confirmed it: the Synoptic
showed the topology, but the physics was hard-coded (if/else per kind in the engine, a
second copy of a law in the scale model, nothing in the M0 file). The defect was visible
in the code but nothing flagged it: the purpose (pedagogical transparency) was not a
checked rule. Lesson: turn the purpose into checks that can fail.

## Direction

Three generations of simulations coexist ([`lib/simulation/README.md`](../../../../lib/simulation/README.md)):
FourLegs (PyGame, obsolete), TwoLegs (one page per poclet, frozen), ThreeLegs (the Kit:
Synoptic + one engine whose laws are data, active). Everything converges to ThreeLegs, in
the spirit of LTspice: an explicit netlist, components whose laws are declared, a generic
solver, probes everywhere. The engine's vocabulary is effort / flow (bond graphs), shared
by electrical, mechanical, hydraulic and thermal systems; only a subset of M2 / M1 is
simulable, and that subset is explicit ([`kit/ENGINE_SCOPE.md`](../../../../kit/ENGINE_SCOPE.md)).

## Invariants

1. No physics outside `K.LAWS` (checked: `node kit/tools/check_laws.js`).
2. Maquette, Panel and curves read the model; they never recompute a law.
3. A concept of tier B (FeedbackLoop, Homeostasis…) emerges from the wiring; it is never a block.
4. A new kind in `K.LAWS` is an engine change; its concept passes the M2 candidate filter first.
5. A migration is done when the old script or page is deleted and no README points to it.

## Items

See [`worksite.yaml`](worksite.yaml): SIM-0 (done) to SIM-12.
