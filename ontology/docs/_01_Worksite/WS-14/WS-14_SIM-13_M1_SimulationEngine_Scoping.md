# WS-14 / SIM-13 — Simulation laws in the ontology (M1 "Simulation Engine" + physical domains)

**Author:** Echopraxium with the collaboration of Claude AI
**Status:** SCOPING NOTE, draft 0.2.0 (2026-11-15). No ontology file is modified by this note.
**Facts read at HEAD `2697cdf`** (re-read before relying on them).

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
| M1 `simulation_engine` (new extension, facet `Formalism`) | the formalism: effort / flow, elements C, R, I, Se, Sf, junctions 0 / 1, coupling elements TF / GY, the solver's rules (fixed step, pass order, first source that speaks) | "a C element integrates the net flow into an effort" |
| M1 physical domains (existing extensions) | each domain's laws and its mapping to the formalism (which quantity is the effort, which is the flow, units) | M1_Physics: Newton's law of cooling; thermal effort = temperature, flow = heat power |
| M0 instance | the netlist: which elements, which wires, which parameter values, which domains it uses | room C = 0.5 kWh/°C, leak k = 0.1 kW/°C, wall at 5 °C |

Precedent for a formalism as an M1 extension: `ontology/M1_extensions/systemic_modeling/`.

## Knowledge in `ontology/`, code in `lib/` (Michel, 2026-11-15)

- The laws (knowledge) are declarative and live in M1 JSON-LD files. `lib/simulation/`
  holds code only: the solver, which reads the laws from M1 or a `K.LAWS` generated from
  them. The engine itself carries no M1 knowledge: that is what keeps M1 from being
  dispersed (leaning D3 towards generation).
- The engine code does not move under `ontology/M1_extensions/`: at HEAD that folder holds
  only `.jsonld` and `.md`, and the tools that walk it rely on that. One link each way:
  the extension README points to the engine; the header of `sim.js` cites the M1 it runs.

## Placement: an M1 extension with a facet, not a new layer

- **No "M1.5" layer** (considered, rejected): it would break the four-layer chain
  (imports M0 -> M1 -> M2 -> M3, per-layer gate, check_M1, reasoner) for one case. The
  formalism is not between M1 and M2: it is orthogonal to the domains. An M0 imports the
  domain(s) of its subject (what it models) and the formalism it runs on (how).
- **Facet** (`m3:Facet`, already in M3_GenesisGrammar: an orthogonal axis that files
  instances without altering the type tree; a Map-perspective role). Proposal: a facet
  such as `ExtensionKind` with values `Domain` and `Formalism`; `systemic_modeling` and
  `simulation_engine` carry `Formalism`.
- A facet value may carry contractual obligations, SHACL-enforced on any carrier: the
  value `Formalism` could require the extension to declare its executor (engine) and its
  netlist SHACL grammar. The ontology-to-code link becomes a checked contract.
- **Constraint:** the Facet principle is SC-3 (design-decided, graved after WS-5); a new
  facet follows `ontology/docs/_01_Worksite/WS-0/2026_09_02/SC-3_Facet_Decision_Record.md`.
  Declared in worksite.yaml: WS-14 depends (soft) on WS-0.

## How an equation is written (D7)

| Need | Where | Form |
|---|---|---|
| the law (dynamics) | M1 | equation string with a known grammar, read by the solver |
| well-formedness of a netlist and of the laws | `ontology/toolchain/grammars/` | SHACL shapes, run by the gate |
| static relations (steady state, bounds, units) | M1 / M0 | SHACL constraints, checkable without simulating |

SHACL checks, it does not simulate: it validates a graph at one instant and does not
integrate `C·dx/dt = Σ flux` over time (SHACL-AF rules compute derived values in one pass,
with no time step). SHACL is the guard rail; the solver is the engine.

Candidate formats, to borrow from rather than adopt whole (the truth stays in JSON-LD):

| Format | Describes | Use for TSCG |
|---|---|---|
| XMILE (OASIS) | System Dynamics: stocks, flows, auxiliaries | closest to the Kit (stock = storage, flow = flux wire, auxiliary = information block); infix equation strings: the grammar for D7; covers economics / ecology (answers D2) |
| Modelica | acausal multi-domain equation models | coupling across domains |
| SBML / CellML | reaction networks, ODEs (MathML) | biological poclets |
| MathML Content | equations as trees | if a tree form is ever needed |
| QUDT (RDF) | quantities and units | units of the effort / flow mapping, as is |
| SPICE netlist | electrical circuits | the LTspice spirit, electrical only |

Rejected: BPML (business processes, discrete workflows; abandoned for BPEL / BPMN).

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
- **D4** *resolved 2026-11-15*: laws extracted from the legacy simulations (FourLegs
  PyGame, TwoLegs pages) go straight into the domain M1; no intermediate form in `lib/`.
  The legacy code only serves to compare results during a migration, then is deleted.
- **D5** `m1:domain` free strings vs `owl:imports` of M1 extensions: two ways to say "this
  M0 uses that domain" coexist at HEAD. Probably WS-10 (M0 namespace harmonisation)
  territory: a dependency to declare?
- **D6** effort / flow: M1 formalism terms only, or M2 candidates? Through
  `tscg-m2-candidate-filter` before any M2 change.
- **D7** equation syntax: proposal, an XMILE-like infix grammar (strings), SHACL as the
  guard rail. To confirm.
- **D8** facet name and values (`ExtensionKind`: `Domain` / `Formalism`?), under SC-3.

## Method when it starts

Ontology change: `tscg-ontology-diagnosis-pipeline` (gates), acceptance gate
`run_all_layers.py` and the reasoner on every touched file; new M2 terms only after the
candidate filter. First pilot: Thermostat (one domain, the laws already explicit in `K.LAWS`).
