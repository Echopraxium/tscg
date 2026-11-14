# TSCG Kit — what the engine can simulate (scope)

**Author:** Echopraxium with the collaboration of Claude AI
**Status:** DRAFT, proposal to validate. No ontology file is modified by this document.
Concept names were read from `ontology/M2_GenericConcepts.jsonld` and
`ontology/M1_CoreConcepts.jsonld` at HEAD `5a26560`; re-read them before relying on this list.

## Why this file exists

The Kit engine (`lib/sim.js`) is a lumped, deterministic, fixed-step simulator: blocks
exchange **fluxes** (power) and **information** (signals), and storages integrate.
Its laws are now data (`K.LAWS`, one entry per generic kind, plus `K.ENGINE` for the
solver's own rules), shown "under the hood". That kind of engine can only simulate a
**subset** of the M2 / M1 concepts. That is fine, but the subset must be explicit, so a
workshop never looks like it "plays" a concept that the engine does not actually model
(the electronic-piano syndrome: the demo plays by itself, and gives the illusion of
knowing how to play).

## The engine's vocabulary (effort / flow)

The kinds follow the bond-graph vocabulary (Paynter), which is shared by electrical,
mechanical, hydraulic and thermal systems:

| Element | Role | Kit kind today | Thermal | Electrical | Mechanical | Hydraulic |
|---|---|---|---|---|---|---|
| **C** | stores, integrates a flux into a level | `storage` | heat capacity | capacitor | spring | tank |
| **R** | dissipates, flux ∝ level difference | *hidden in the wire* (`k` of the storage) | conductance | resistor | friction | restriction |
| **I** | inertia, stores momentum | *missing* | (none) | inductor | mass | fluid inertia |
| **Se** | imposes a level | `sink` | outside air | voltage source | imposed force | reservoir at fixed pressure |
| **Sf** | imposes a flux | `source`, `transducer` | heater | current source | imposed speed | pump |
| sig | information only, no power | `threshold`, `amplify`, `gradient`, `clock` | thermostat | comparator, op-amp | governor | float switch |

## Proposed classification of M2 / M1 concepts

### A. Engine primitive: a block (or a wire) carries the law

| Concept | Where in the engine | Note |
|---|---|---|
| m2:Storage | `storage` (C) | |
| m2:Capacity | parameter `C` of a storage | |
| m2:Dissipation | R, today a parameter `k` on the storage, applied on the wire | should become visible (wire label or block) |
| m2:Threshold | `threshold` | |
| m2:Amplification | `amplify` | |
| m2:Transducer | `transducer` | |
| m2:Gradient | `gradient` | |
| m2:Signal, m2:Channel | information wire, flux wire | |
| m2:Inertia | element I | **not yet**: needed for any harmonic oscillation |

Kit kinds with **no M2 class** at HEAD: `source`, `sink`, `clock`. To be decided:
skins over an existing concept (m2:Resource?), or simulator-only primitives that are
deliberately outside the ontology.

### B. Observable: emerges from the wiring, no block of its own

The player builds it from primitives; the curves show it. These are the concepts the Kit
is for, and they must **never** be a block.

| Concept | How it shows in a simulation |
|---|---|
| m2:FeedbackLoop | a closed path through the graph (sign = product of the signs along it) |
| m2:Regulation, m2:Homeostasis, m2:Balance | a level that returns to a band after a perturbation |
| m2:Resilience | recovery time after a perturbation (open window) |
| m2:Trajectory, m2:State | the curves, the state vector |
| m2:Event | a threshold crossing |
| m2:Memory | a storage, a hysteresis band |
| m2:Bifurcation | a qualitative change when one parameter is swept |
| m2:Tropism | the Sunflower workshop: tracking a moving target |
| m1:Hysteresis | the threshold band `set ± h/2` |
| m1:Oscillator | **relaxation only** today (Thermostat, Drinking bird); harmonic needs I |
| m1:Cascade, m1:CascadeAmplification, m1:Propagation, m1:StratifiedDissipation | chains of storages / amplifiers |

### C. Structural: visible in the Synoptic, not simulated

The netlist shows them; the engine has nothing to compute about them.
m2:Node, m2:Link, m2:Path, m2:Relation, m2:Network, m2:Component, m2:Composition,
m2:Modularity, m2:Hierarchy, m2:Layer, m2:Hub, m2:Cluster, m2:Topology, m2:System,
m2:Environment, m2:Context, m2:Scope, m2:Constraint (only as clamps `lo` / `hi`).

### D. Out of scope for this engine

- **Needs another engine** (not yet): spatial fields (m1:LocalActivationLateralInhibition,
  m2:Self-Organization, m2:TopologicalDefect), agents and learning (m2:Agent, m2:Adaptation),
  sensitivity to initial conditions (m1:ButterflyEffect needs at least three coupled
  nonlinear states; possible later, not with the current workshops).
- **Not dynamic** (semantic, representational): m2:Code, m2:Coding, m2:Language,
  m2:Representation, m2:Modelisation, m2:Identity, m2:Observer, m2:Signature,
  m2:Invariant, m2:Pattern, m2:Symmetry, m2:Emergence, m1:Narration.
- **Unclassified** (to discuss): every other concept of M2 / M1, including m2:Process,
  m2:Processor, m2:Resource, m2:Stase, m2:Potentialization, m2:AbsorbingState, m2:Trade-off,
  m2:Synergy, m2:Fusion, m2:Coherence, m2:Entropy, m2:Alignment, m2:Polarity,
  m2:TriadicBalance, m2:Mediator, m2:Interoperability.

Families (Structural, Dynamic, …), concept contracts (Observable, Stateful, …) and
meta-classes (GenericConceptCombo, …) are not concepts to simulate.

## Rules for workshops

1. A workshop may only **claim** a concept of A or B. Tier B must emerge from the wiring.
2. No physics outside `K.LAWS`: the Maquette, the Panel and the curves read the model
   (`n.s`, `w.power`), they never recompute a law.
3. Adding a kind to `K.LAWS` (R as a block, I) is an engine change; the corresponding
   concept goes through the M2 candidate filter first.
