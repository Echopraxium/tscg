# WS-14 / SIM-13 — Simulation laws in the ontology (M1 "Simulation Engine" + physical domains)

**Author:** Echopraxium with the collaboration of Claude AI
**Status:** SCOPING NOTE, draft 0.1.0 (2026-11-15). No ontology file is modified by this note.
**Facts read at HEAD `39ca12d`** (re-read before relying on them).

## Why

The Kit engine's laws are data (`K.LAWS`, lib/simulation/ThreeLegs/engine/sim.js), but that
data lives in JavaScript: the ontology only comments the model, it does not hold it.
Michel, 2026-11-15: the simulation logic belongs in M1 ontologies, with a "Simulation
Engine" domain; an M0 simulation can use several domains, which fits the Layer Cake.
Goal: the map becomes executable. `K.LAWS` is generated from the ontology, or at least
checked against it, and the truth of a model is in its M0 / M1 files, not in a page.

## Layering (proposal)

| Layer | Holds | Example (Thermostat) |
|---|---|---|
| M2 | the transdisciplinary roles, already there | m2:Storage, m2:Dissipation, m2:Inertia, m2:Transducer, m2:Threshold |
| M1 `simulation_engine` (new extension) | the formalism: effort / flow, elements C, R, I, Se, Sf, junctions 0 / 1, coupling elements TF / GY, the solver's rules (fixed step, pass order, first source that speaks) | "a C element integrates the net flow into an effort" |
| M1 physical domains (existing extensions) | each domain's laws and its mapping to the formalism (which quantity is the effort, which is the flow, units) | M1_Physics: Newton's law of cooling; thermal effort = temperature, flow = heat power |
| M0 instance | the netlist: which elements, which wires, which parameter values, which domains it uses | room C = 0.5 kWh/°C, leak k = 0.1 kW/°C, wall at 5 °C |

Precedent for a formalism as an M1 extension: `ontology/M1_extensions/systemic_modeling/`.

## Several domains in one M0

Already the case at HEAD: `M0_PhaseTransition` imports `M1_Chemistry` and `M1_Physics`;
`M0_Transistor` declares five `m1:domain` values. The formalism handles it natively: a
model crosses domains through coupling elements (bond graphs: TF transformer, GY
gyrator). The Kit's `transducer` kind is the first of them (a signal driving a flow).
Examples: an electric heater (electrical -> thermal, R as a coupling), a four-stroke engine
(thermal -> mechanical), a transistor (electrical, with thermal dissipation).

## What changes for the Kit

1. `K.LAWS` is derived from M1 `simulation_engine` + the domain M1 (generation), or a
   check fails when they disagree (verification). Decision D3.
2. A workshop's netlist is its M0 (SIM-11): the page loads the model instead of building it.
3. `kit/ENGINE_SCOPE.md` tiers A-D become checkable: a tier-A concept has an element in
   M1 `simulation_engine`.

## Open decisions (Michel)

- **D1** name and namespace of the extension (`simulation_engine`? `bond_graph`?).
- **D2** where a law lives when it is not physical (economics, ecology: a stock-and-flow
  law of M1_Economics follows the same formalism; System Dynamics is the same family).
- **D3** generation of `K.LAWS` from the ontology, or verification only.
- **D4** laws extracted from the legacy simulations (FourLegs PyGame, TwoLegs pages):
  straight into the domain M1, or first a neutral intermediate form in `lib/simulation/`.
- **D5** `m1:domain` free strings vs `owl:imports` of M1 extensions: two ways to say "this
  M0 uses that domain" coexist at HEAD. Probably WS-10 (M0 namespace harmonisation)
  territory: a dependency to declare?
- **D6** effort / flow: M1 formalism terms only, or M2 candidates? Through
  `tscg-m2-candidate-filter` before any M2 change.

## Method when it starts

Ontology change: `tscg-ontology-diagnosis-pipeline` (gates), acceptance gate
`run_all_layers.py` and the reasoner on every touched file; new M2 terms only after the
candidate filter. First pilot: Thermostat (one domain, the laws already explicit in `K.LAWS`).
