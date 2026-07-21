# M1_CoreConcepts.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 2.9.0
**Date**: 2026-07-17
**Layer**: M1 — Domain-Neutral Core Concepts
**Status**: Active

---

## Overview

`M1_CoreConcepts.jsonld` is the **foundational M1 ontology** that defines:
1. Abstract concept categories (CoreConcept, GenericMechanism, etc.)
2. **GenericConceptCombos** — transdisciplinary patterns built from M2 concepts
   via `Fm2(C1, C2, ...)` — the **M1 Safety Valve** against Ontological Overfitting

It sits between M2 (GenericConcepts) and the domain-specific M1 extensions
(biology, physics, etc.).

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld  ─┐
M3_EagleEye.jsonld           ─┤→  M3_GenesisGrammar.jsonld
M3_SphinxEye.jsonld          ─┘           ↓ imported by
M3_BicephalousPerspective.jsonld           ↓
                                  M2_GenericConcepts.jsonld
                                           ↓ imported by
                                  M1_CoreConcepts.jsonld    ← THIS FILE
                                           ↓ imported by
                                  M1_Biology.jsonld
                                  M1_Physics.jsonld
                                  M1_xxx.jsonld
                                           ↓
                                  M0_xxx.jsonld (instances)
```

**Imports**: `M2_GenericConcepts.jsonld`
**Imported by**: Domain-specific M1 extensions

---

## The M1 Safety Valve

M1_CoreConcepts is architecturally designed as a **bidirectional safety valve**
against Ontological Overfitting:

```
Pressure DOWN (M2 → M1):
  Concepts too specialized for M2 purity migrate down
  Example: TopologicalDefect (requires topological knowledge)

Pressure UP (M1 → M2):
  Combos validated in ≥6 domains may be promoted to M2
  (requires passing the M2 Triple Filter)

Absorption (lateral):
  Non-atomic but transdisciplinary patterns created as GenericConceptCombos
  Example: Permeability, ConstraintBalance, CascadeAmplification
```

A **healthy M2** layer shows more M1 combos than M2 concept additions.
This is a sign the M2 filter is working, not that M2 is insufficient.

See `OntologicalOverfitting.md` (CoreHypotheses/) for the full architectural
rationale.

---

## GenericConceptCombos Catalogue (v2.6.0)

**12 combos** defined — each built from M2 atomic concepts via `Fm2(...)`:

| ID | Label | Formula | Parents |
|---|---|---|---|
| `m1:Cascade` | Cascade | `Fm2(Process, Step, Trajectory)` | Process, Step, Trajectory |
| `m1:Oscillator` | Oscillator | `Fm2(Component, Process, Trajectory) \| trajectoryShape=Circular` | Component, Process, Trajectory |
| `m1:Processor` | Processor | `Fm2(Process, Structure, Information) \| V + R` | Process, Structure, Information |
| `m1:LocalActivationLateralInhibition` | LALI | `Fm2(Amplification, Regulation) \| range(F_A) << range(F_R)` | Amplification, Regulation |
| `m1:ButterflyEffect` | ButterflyEffect | `Fm2(Amplification, Trajectory) \| trajectoryShape=Chaotic ∧ λ > 0` | Amplification, Trajectory |
| `m1:Propagation` | Propagation | `Fm1m2(Cascade, Duplication, Network)` | Cascade (M1), Duplication, Network |
| `m1:Narration` | Narration | `Fm2(Transformation, Representation, Relation)` | Transformation, Representation, Relation |
| `m1:StratifiedDissipation` | StratifiedDissipation | `Fm2(Layer, Dissipation)` | Layer, Dissipation |
| `m1:CascadeAmplification` | CascadeAmplification | `Fm1m2(Cascade, Amplification) \| gain_per_stage > 1` | Cascade (M1), Amplification |
| `m1:TopologicalDefect` | Topological Defect | `Fm2(Coherence, Invariant)` | Coherence, Invariant |
| `m1:Permeability` | Permeability (Permeability/Impermeability) | `Fm2(Channel, Interface, Gradient)` | Channel, Interface, Gradient |
| `m1:ConstraintBalance` | Constraint Balance | `Fm2(TriadicBalance, Constraint)` | TriadicBalance, Constraint |

---

## GenericConceptCombos — Detailed Fiches

### m1:Cascade

```
Formula  : Fm2(Process, Step, Trajectory)
Parents  : Process, Step, Trajectory
```

Sequential multi-stage process where the output of each step becomes the
input of the next, following a directed trajectory toward a goal state.
The emergent property is **sequential dependency** — each stage is both
consumer and producer, creating a directed causal chain absent from any
single parent.

---

### m1:Oscillator

```
Formula  : Fm2(Component, Process, Trajectory) | trajectoryShape=Circular
Parents  : Component, Process, Trajectory
```

A system component that sustains periodic return to previous states through
a cyclic trajectory around an attractor. The emergent property is **sustained
periodicity** — the circular trajectory is maintained without external driving,
distinguishing it from a transient oscillation.

---

### m1:Processor

```
Formula  : Fm2(Process, Structure, Information) | V + R
Parents  : Process, Structure, Information
```

Generic system with inputs and outputs that transforms incoming resources,
signals, or matter into outputs. The `V + R` Map qualification encodes that
the transformation must be verifiable and representable — a Processor is
not a black box.

---

### m1:LocalActivationLateralInhibition (LALI)

```
Formula  : Fm2(Amplification, Regulation) | range(F_A) << range(F_R)
Parents  : Amplification, Regulation
```

Binary combo where a local self-reinforcing process (Amplification, short
range) is structurally coupled with a longer-range inhibitory process
(Regulation). The range asymmetry `range(F_A) << range(F_R)` is the
constitutive constraint — without it, the combo collapses to undifferentiated
feedback. Canonical pattern for morphogenetic pattern formation (Turing, 1952),
neural lateral inhibition, market concentration dynamics.

---

### m1:ButterflyEffect

```
Formula  : Fm2(Amplification, Trajectory) | trajectoryShape=Chaotic ∧ λ > 0
Parents  : Amplification, Trajectory
```

Unconstrained local positive feedback (Amplification) coupled with a chaotic
system trajectory (positive Lyapunov exponent λ > 0). The emergent property
is **sensitive dependence on initial conditions** — infinitesimal differences
in state diverge exponentially. Distinct from CascadeAmplification (bounded,
staged) — ButterflyEffect is topologically chaotic, not merely cumulative.

---

### m1:Propagation

```
Formula  : Fm1m2(Cascade, Duplication, Network)
Parents  : Cascade, Duplication, Network
```

Branching spread of a faithfully copied entity through a network, where each
receiving node becomes a new emitter. The emergent property is **faithful
branching** — the combination of Cascade (sequential direction), Duplication
(faithful copying), and Network (branching topology) produces exponential
spread with content preservation. Instance: biological contagion, meme
propagation, blockchain consensus, rumour spreading.

---

### m1:Narration

```
Formula  : Fm2(Transformation, Representation, Relation)
Parents  : Transformation, Representation, Relation
```

Temporal transformation of a semantic network of Representations and their
Relations — a semantic network morphism unfolding over time. The emergent
property is **semantic coherence through transformation** — the Relations
between Representations are preserved (or meaningfully altered) as the
narrative unfolds, distinguishing Narration from mere sequence.

---

### m1:StratifiedDissipation

```
Formula  : Fm2(Layer, Dissipation)
Parents  : Layer, Dissipation
```

Layered dissipation process where energy or matter is progressively absorbed
across ordered strata, each stratum capturing a portion of the incoming flux.
`Fm2(Layer, Dissipation)` — both parents are M2 atomics
level. The emergent property is **graduated absorption** — the stratification
produces a spatial/structural profile of dissipation absent from undifferentiated
Dissipation alone.

---

### m1:CascadeAmplification

```
Formula  : Fm1m2(Cascade, Amplification) | gain_per_stage > 1
Parents  : Cascade, Amplification
```

Sequential multi-stage process where each stage amplifies the output of the
previous, producing exponential cumulative gain. `gain_per_stage > 1` is the
constitutive constraint. `Fm1m2` — m1:Cascade is an M1 combo, not a M2 atomic.
The emergent property is **exponential cumulative gain** — absent from Cascade
(neutral transfer) and Amplification (single-stage). Instance: transistor
cascade, enzymatic signalling cascade, compound interest, nuclear chain reaction.

---

### m1:TopologicalDefect *(migrated from M2 v2.5.0)*

```
Formula  : Fm2(Coherence, Invariant)
Expanded : St × A × It | R + O
```

Localized Incoherence whose singularity is topologically protected by a
discrete invariant (winding number n ∈ ℤ). Not eliminable by continuous
local transformation — stability is global, not energetic. Migrated from M2:
too specialized (requires topological knowledge, limiting transdisciplinary
accessibility at M2 level).

**Validated ≥7 domains**: Condensed Matter (Abrikosov vortex), Materials
(crystal dislocation), Soft Matter (liquid crystal disclination), Cosmology
(cosmic string), Distributed Systems (blockchain persistent fork),
Neuroscience (phase singularity in neural oscillations), Biology
(morphogenetic singularity).

---

### m1:Permeability *(new v2.5.0)*

```
Formula  : Fm2(Channel, Interface, Gradient)
Expanded : St × It × F × T | Ss × (V + E)
Polarity : dual (_^ Permeability / _$ Impermeability)
Regime   : Static | Threshold-dependent | History-dependent
```

Structural property of a boundary that modulates flux passage — neither
purely static (a Boundary) nor fully open (a Channel). The `T` (Gradient
inheritance) encodes that permeability changes as flux accumulates — the
paper absorbing oil, the cell membrane gating, the market opening to capital.

```
Impermeability      (_$)  ←  regime: closed
SelectivePermeability(_0) ←  selective — neither fully open nor closed
Permeability        (_^)  →  regime: open
```

**Distinct from:**
- `m2:Boundary` (S×A) — static existence of a frontier
- `m2:Channel` (St×F|Ss) — dedicated open conduit, no blocking capacity
- `m2:Constraint` (St|L) — static opposition to flux

**Validated ≥7 domains**: Physics (osmosis, Darcy law), Biology (membranes,
aquaporins), Finance (capital markets, credit scoring), Epistemology
(disciplinary openness vs silos), Social (cultural boundaries),
Computing (API/firewall), Geology (aquifers, petroleum reservoirs).

---

### m1:ConstraintBalance *(new v2.6.0)*

```
Formula  : Fm2(TriadicBalance, Constraint)
Expanded : A × F × D × St | _0
Polarity : ternary (_^, _0, _$)
```

Instance of `m2:TriadicBalance` in the context of system design and
ontological modelling. Three qualitatively distinct states:

| State | Symbol | Semantics | Examples |
|---|---|---|---|
| UnderConstrained | `_^` | Too open — loses precision | ML underfitting, legal vacuum, M2 concept too vague |
| BalancedConstraint | `_0` | Optimal — generalizes AND is precise | Good ML model, clear law, validated M2 concept |
| OverConstrained | `_$` | Too rigid — loses generalizability | ML overfitting, hyper-legalism, **Ontological Overfitting** |

**Ontological Overfitting** is the instance of `OverConstrained (_$)` applied
to `m2:Modelisation` — adding one M2 concept per phenomenon instead of
composing existing ones.

**Validated ≥6 domains**: Machine Learning, Law, TSCG Ontology,
Biology, Management, Mechanics.

---

## Core Concept Categories

M1_CoreConcepts defines 16 abstract concept classes:

| Category | Role |
|---|---|
| `CoreConcept` | Abstract superclass — common ancestor |
| `GenericMechanism` | How things work — operational principles |
| `StructuralTemplate` | Organizational patterns and blueprints |
| `ProcessArchetype` | Canonical temporal sequences |
| `RelationalPattern` | Multi-entity interaction structures |
| `TransformationPattern` | State-change patterns |
| `RegulationPattern` | Control and feedback patterns |
| `EmergencePattern` | Emergent property patterns |
| `InformationPattern` | Information processing patterns |
| `EnergyPattern` | Energy transfer and conversion patterns |
| `BoundaryPattern` | Interface and frontier patterns |
| `ScalePattern` | Multi-scale organisation patterns |
| `TemporalPattern` | Time-based dynamics patterns |
| `SpatialPattern` | Spatial organisation patterns |
| `AdaptationPattern` | Adaptive response patterns |
| `CollapsePattern` | Failure and dissolution patterns |

---

## Ontology Statistics (v2.6.0)

| Metric | Value |
|---|---|
| Core concept categories | 16 |
| GenericConceptCombos | 12 |
| Total concepts defined | 14 (combos with full fiches) |
| Properties | 1 (simulationTitle) |
| Imports | M2_GenericConcepts.jsonld |

---

## Design Principles

### 1. Domain Neutrality

All GenericConceptCombos must apply across ≥6 distinct knowledge domains.
Domain-specific patterns belong in M1 extensions (M1_Physics, M1_Biology...).

### 2. Safety Valve Role

M1_CoreConcepts is the primary defense against Ontological Overfitting.
When a candidate fails the M2 Triple Filter (Decomposability / Transdisciplinarity /
Atomicity) but is still transdisciplinarily valuable — it lands here as a combo.

### 3. Emergent Property Requirement

Each GenericConceptCombo must have a documented `emergentProperty` — the
quality the combo produces that neither parent concept has alone.
A combo without emergent property is not a combo — it is redundant juxtaposition.

### 4. Lego Systemic Principle

M1 combos are **new bricks built from M2 bricks**. The phototransistor
(Photodiode + Transistor) is the canonical illustration: two M0 components
combine into a new M1-level functional brick with emergent amplification
properties irreducible to either component.

### 5. Fm2 vs Fm1m2 — Composition Types

Two composition notations distinguish parent levels:

```
Fm2(C1, C2, ...)    all parents are M2 atomic concepts
                     → @type: GenericConceptCombo

Fm1m2(C1, C2, ...)  at least one parent is an M1 combo
                     → @type: DomainConceptCombo
```

**Fm2 combos (10):** Cascade, Oscillator, Processor, LALI, ButterflyEffect,
Narration, StratifiedDissipation, Permeability, TopologicalDefect, ConstraintBalance

**Fm1m2 combos (2):**
```
m1:Propagation        =  Fm1m2(Cascade, Duplication, Network)
  m1:Cascade is M1 — Propagation composites an M1 combo with M2 concepts

m1:CascadeAmplification  =  Fm1m2(Cascade, Amplification) | gain_per_stage > 1
  Same pattern — m1:Cascade as M1 parent
```

---

## Validation Status

**OWL/RDFS Compliance:** ✅ Validated (May 14, 2026)
- RDFS diagnostic: 0 errors
- OWL Pellet reasoning: PASSED
- Protégé compatibility: Confirmed

---


## 🧩 The Functional Grammar — combos are function signatures (SC-1, 2026-07-12)

```
Fm2   : GenericConcept²⁺            ->  m2:GenericConceptCombo   (>= 2 concepts)
Fm1m2 : Domain+ , GenericConcept+   ->  m2:DomainConceptCombo    (>= 1 Domain AND >= 1 concept)
```

- **Atoms** carry a **monoidal formula** (`x`, `+`, `|`). **Combos** carry a **function signature**.
  A combo has **NO monoidal formula and NO monoidal expansion**: `Fm2`/`Fm1m2` are **functions,
  not functors** — emergence is *non-compositional* (the arguments are **combined, not associated**),
  and a functor must *preserve* composition. `m1:structuralGrammarFormulaExpanded` is therefore
  **retired** (D8) and, as of **v2.9.0**, **physically removed** from every combo
  (together with its `TeX`/`RawText` siblings): there was never anything to expand.
- **Arguments are NAMED CONCEPTS** from `M2_GenericConcepts.jsonld` or `M1_CoreConcepts.jsonld` —
  never primitives, never a monoidal expression, **comma-juxtaposed**, never joined by an operator.
- **`Fm1` does not exist.** Multi-domain conjunction = juxtaposed domain arguments.

### ⚠️ What distinguishes `Fm1m2` from `Fm2` (correction of a propagated error)

**`Fm1m2` is NOT "the function that crosses the M1/M2 boundary."** That reading was graved in
`M3_GrammarFoundation` (`Fm1m2 : T1(M1) x T1(M2)^n -> T1`) and applied faithfully in v1.4.0 of this
file, which "corrected" `Propagation` and `CascadeAmplification` from `Fm2` to `Fm1m2` *"because the
parent m1:Cascade is M1, not an M2 atomic"*. **That correction was itself the error.**

What distinguishes `Fm1m2` is **DOMAIN QUALIFICATION** — nothing else. An `Fm2` argument may
legitimately be a named concept from `M1_CoreConcepts`, so "crossing M1/M2" distinguishes nothing.

```
BAD   Fm1m2(Cascade, Duplication, Network)      no Domain -> this is an Fm2
BAD   Fm1m2(Optics, A x St x F x It | R + O)    monoidal expression as argument
BAD   Fm1m2(Cascade, Amplification) | gain > 1  scalar guard -> an M0 measurement leaking into M1
GOOD  Fm2(Cascade, Duplication, Network)        >= 2 named concepts (Cascade is M1_Core: legal)
GOOD  Fm1m2(Optics, Refraction)                 >= 1 Domain + >= 1 named concept
```

These are **flagged by the SHACL (v1.1.0), not repaired here** — repair belongs to **SC-6**.

Full rationale: `StructuralGrammar/Functional_Grammar_Model.md`.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **2.9.0** | 2026-07-17 | SC-6 (partial) — **physically removed** the retired D8 property family from all 12 GenericConceptCombos: `m1:structuralGrammarFormulaExpanded`, `m1:structuralGrammarFormulaTeX`, `m1:structuralGrammarFormulaRawText`. A combo has no monoidal expansion; the live `m1:structuralGrammarFormula` (Fm2/Fm1m2 signature) carries all information (verified: 0 nodes left formula-less; 6 still held the obsolete `×⇒`/`(x)=>` residue, now gone). Also removed `m1:hasEpistemicGap` — a scalar δ₁ is an **M0** measurement (a modelled system), not a property of an abstract combo **type**: an M0 quantity leaking into M1. **Not touched**: the domain-less `Fm1m2` of Propagation/CascadeAmplification (separate SC-6 semantic repair). Golden: EXP001 drops 12 → 0 in `run_all_layers` (deliberate → `--update-golden`). Noted SHACL blind spot: `hasEpistemicGap` and the TeX/RawText siblings had no shape (SHAPE 10 covered only `Expanded`) → SC-5 hardening candidate. |
| **2.8.0** | 2026-07-14 | SC-1.5 — **@context COERCION**: added `{"@type": "@id"}` for `rdfs:subClassOf` (and `rdfs:domain`, `rdfs:range`). All 19 `subClassOf` values were serialised as string literals instead of IRIs, so Pellet **ignored the entire class hierarchy** (the file was *unanalysable*, not merely inconsistent) and this was the root of most pre-existing SHACL `subClassOf` violations. Three `@context` lines fix all of it — no data migration. `owl:imports` **deliberately left un-coerced**: coercing it makes reasoners try to resolve it over the network and die; the import stays inert until the import graph is actually wired up. |
| **2.7.0** | 2026-07-12 | SC-1 FUNCTIONAL GRAMMAR MODEL. RENAME (hard): `m2:KnowledgeFieldConceptCombo` → `m2:DomainConceptCombo`, **re-defined** by its `Fm1m2` formula (hybrid ≥1 Domain + ≥1 GenericConcept — domain qualification, NOT parent provenance). ⚠️ The v1.4.0 "CORRECTION" (Propagation/CascadeAmplification `Fm2`→`Fm1m2` *"because parent m1:Cascade is M1"*) **is itself erroneous** and traces back to a wrong `Fm1m2` definition in M3_GrammarFoundation (now fixed, v2.4.0). `Fm2` arguments may legitimately come from M1_CoreConcepts. Flagged by SHACL v1.1.0, **repair = SC-6**. Also retired: `m1:structuralGrammarFormulaExpanded` (no monoidal expansion) and the scalar guards. |

---

## See Also

- `M2_GenericConcepts.jsonld` — M2 atomic concepts (source of Fm2 parents)
- `M2_GenericConcepts_README.md` — M2 formulas reference
- `M3_BicephalousPerspective.jsonld` — DerivedGsElement _0 = _^ | _$
- `M1_Domains.jsonld` — Domain registry
- `docs/CoreHypotheses/OntologicalOverfitting.md` — anti-pattern documentation
- `skills/tscg-m2-candidate-filter/SKILL.md` — candidate evaluation pipeline
- `CLAUDE.md` — Modeling conventions and authoring rules

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — June 2026*
