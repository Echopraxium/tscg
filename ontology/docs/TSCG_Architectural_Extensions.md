# TSCG Architectural Extensions
## N-ary MetaconceptCombo and Typed Attributes via ValueSpace

**Version**: 1.0.0  
**Date**: 2026-02-05  
**Author**: Echopraxium with the collaboration of Claude AI  
**Status**: Proposed Architecture (Trajectory attributes implemented in v14.3.6)

---

## Table of Contents

1. [Overview](#overview)
2. [Extension 1: N-ary MetaconceptCombo](#extension-1-n-ary-metaconceptcombo)
3. [Extension 2: Typed Attributes via ValueSpace](#extension-2-typed-attributes-via-valuespace)
4. [Implementation Status](#implementation-status)
5. [Case Study: Cascade](#case-study-cascade)
6. [Future Directions](#future-directions)

---

## Overview

### Motivation

During RAAS poclet analysis, two architectural needs emerged:

1. **N-ary MetaconceptCombo**: Cascade requires 3 parents (Process, Step, Trajectory) to capture full semantics
2. **Typed Attributes**: Trajectory needs configurable `shape` attribute without creating explosion of subtypes

### Core Innovations

#### Innovation 1: Generalize MetaconceptCombo from Binary to N-ary

**Current** (v14.3.5):
```
MetaconceptCombo: M_A ⊗⇒ M_B → M_C  (2 parents only)
```

**Proposed**:
```
MetaconceptCombo: ⊗⇒(M₁, M₂, ..., Mₙ) → M_result  (n ≥ 2 parents)
```

#### Innovation 2: Typed Attributes via ValueSpace

**Mechanism**: Leverage existing `m2:ValueSpace` metaconcept to define attribute domains

**Benefit**: Add configurability without ontological proliferation

---

## Extension 1: N-ary MetaconceptCombo

### Theoretical Foundation

#### Tensor Product Associativity

In tensor algebra:
```
(A ⊗ B) ⊗ C = A ⊗ (B ⊗ C) = A ⊗ B ⊗ C
```

**Implication**: N-ary tensor products are mathematically well-defined.

#### Coupling Rule Generalization

**Binary case** (current):
```
M_A: dims(A)
M_B: dims(B)
Shared: dims(A) ∩ dims(B)
───────────────────────────
Result: (dims(A) ∪ dims(B)) with coupling on shared dimensions
```

**N-ary case** (proposed):
```
M₁: dims(1)
M₂: dims(2)
...
Mₙ: dims(n)
Shared: ∩ᵢ dims(i)  (pairwise intersections)
─────────────────────────────────────────────
Result: (⋃ᵢ dims(i)) with coupling on all shared dimensions
```

### Formal Definition

```json
{
  "@id": "m2:MetaconceptCombo",
  "@type": ["owl:NamedIndividual", "m2:MetaConcept"],
  "rdfs:label": "MetaconceptCombo (N-ary Synergistic Combination)",
  "rdfs:comment": "Parameterized metaconcept produced by synergistic combination of N parent metaconcepts (N ≥ 2) via N-ary tensor assembly and emergence morphism (⊗⇒). Shared dimensions couple (trace-like contraction), unique dimensions add. Generalization from binary (v14.3.5) to N-ary (v14.4.0+).",
  
  "m2:hasTensorFormula": "⊗⇒(M₁, M₂, ..., Mₙ)",
  "m2:arity": "n ≥ 2",
  
  "m2:formulaSemantics": {
    "M_i": "i-th parent metaconcept (parameter)",
    "⊗⇒": "N-ary synergistic tensor assembly with emergence morphism",
    "n": "Number of parents (arity), must be ≥ 2",
    "coupling": "Dimensions shared among ≥2 parents couple (do not duplicate)",
    "result": "Union of all dimensions minus coupling contractions"
  },
  
  "m2:couplingAlgorithm": {
    "step1": "Collect all dimensions from all parents: D_all = ⋃ᵢ dims(Mᵢ)",
    "step2": "Identify shared dimensions: D_shared = {d ∈ D_all : d appears in ≥2 parents}",
    "step3": "For each d ∈ D_shared, keep single instance (couple via trace contraction)",
    "step4": "Result formula: unique(D_all)"
  },
  
  "m2:examples": {
    "binary": {
      "name": "VarietyAmplification",
      "formula": "ValueSpace ⊗⇒ Amplification",
      "arity": 2,
      "note": "Existing pattern, unchanged"
    },
    "ternary": {
      "name": "Cascade",
      "formula": "⊗⇒(Process, Step, Trajectory)",
      "arity": 3,
      "parents": {
        "Process": "D⊗F",
        "Step": "S⊗I⊗D",
        "Trajectory": "A⊗D⊗F"
      },
      "shared": ["D", "F"],
      "result": "S⊗I⊗A⊗D⊗F (all 5 ASFID dimensions!)"
    }
  }
}
```

### Validation

#### Mathematical Soundness
- ✅ Tensor product is associative
- ✅ Coupling rule extends naturally to N-way intersection
- ✅ Dimension semantics preserved

#### Practical Need
- ✅ Cascade requires 3 parents for complete semantics
- ✅ Future complex systems may require 4+ parents
- ✅ No artificial limit on composition depth

---

## Extension 2: Typed Attributes via ValueSpace

### Motivation

**Problem**: How to represent variations within a metaconcept without creating subtype explosion?

**Example**: Trajectory can be Linear, Circular, Spiral, Chaotic, etc.

**Bad solution** ❌:
```
m2:TrajectoryLinear subClassOf m2:Trajectory
m2:TrajectoryCircular subClassOf m2:Trajectory
m2:TrajectorySpiral subClassOf m2:Trajectory
...  (9+ subtypes!)
```

**Good solution** ✅:
```
m2:Trajectory
  m2:hasAttribute:
    shape: ValueSpace{Linear, Circular, Spiral, ...}
```

### Mechanism

Leverage **m2:ValueSpace** (existing M2 metaconcept) to define attribute domains.

#### ValueSpace Recap

```
ValueSpace = It ⊗ V ⊗ O ⊗ R ⊗ Im
```

Defines space of possible values with:
- **It** (Territory): Cardinality/dimension
- **V, O, R, Im** (Map): Epistemic quality (Verifiability, Observability, Reproducibility, Interoperability)

#### Attribute Schema

```json
{
  "m2:hasAttribute": {
    "attributeName": {
      "@type": "m2:ValueSpace",
      "m2:valueType": "Discrete symbolic | Continuous | Discrete numeric | ...",
      "m2:possibleValues": [
        {
          "value": "ValueName",
          "description": "...",
          "examples": [...],
          "characteristics": "..."
        },
        ...
      ],
      "m2:default": "DefaultValue",
      "m2:constraint": "Optional constraint expression"
    }
  }
}
```

---

## Implementation Status

### v14.3.6 (Completed)

✅ **Trajectory.shape attribute implemented**

```json
{
  "@id": "m2:Trajectory",
  "m2:hasAttribute": {
    "shape": {
      "@type": "m2:ValueSpace",
      "m2:valueType": "Discrete symbolic",
      "m2:possibleValues": [
        "Linear", "Circular", "Elliptical", "Spiral", 
        "Hyperbolic", "Random", "Constrained", "Chaotic", "Piecewise"
      ],
      "m2:default": "Linear"
    }
  }
}
```

**9 shape values** with descriptions, examples, and characteristics.

### v14.4.0+ (Planned)

🔄 **N-ary MetaconceptCombo**
- Generalize from binary to N-ary
- Update all MetaconceptCombo instances
- Implement Cascade as ⊗⇒(Process, Step, Trajectory)

🔄 **Additional Attributes**
- Cascade.amplifying (boolean)
- Cascade.branching (boolean)
- Others as identified

---

## Case Study: Cascade

### Evolution Through RAAS Analysis

#### Iteration 1: Binary Combo
```
Cascade = Process ⊗⇒ Step
Formula: S⊗I⊗D⊗F
```
**Problem**: Lacks Attractor (A) dimension for goal-directed cascades

#### Iteration 2: Different Binary Combo
```
Cascade = Workflow ⊗⇒ Trajectory
Formula: S⊗A⊗D⊗F
```
**Problem**: Loses Information (I) dimension (critical for signal transfer)

#### Iteration 3: Ternary Combo (Proposed)
```
Cascade = ⊗⇒(Process, Step, Trajectory)
Formula: S⊗I⊗A⊗D⊗F
```
**Result**: ALL 5 ASFID dimensions! Complete characterization.

### Cascade with Attributes

```json
{
  "@id": "m2:Cascade",
  "@type": ["m2:MetaConcept", "m2:MetaconceptCombo"],
  "m2:hasTensorFormula": "⊗⇒(Process, Step, Trajectory)",
  "m2:hasTensorFormulaExpanded": "S⊗I⊗A⊗D⊗F",
  
  "m2:parentMetaconcepts": [
    {"@id": "m2:Process", "formula": "D⊗F"},
    {"@id": "m2:Step", "formula": "S⊗I⊗D"},
    {"@id": "m2:Trajectory", "formula": "A⊗D⊗F"}
  ],
  
  "m2:sharedDimensions": {
    "D": "Shared by all three (temporal dynamics)",
    "F": "Shared by Process and Trajectory (flow)"
  },
  
  "m2:hasAttribute": {
    "trajectoryShape": {
      "@type": "m2:ValueSpace",
      "m2:possibleValues": ["Linear", "Circular", "Spiral", "Chaotic", ...],
      "m2:default": "Linear"
    },
    "amplifying": {
      "@type": "xsd:boolean",
      "m2:description": "Whether cascade includes amplification (gain > 1) at stages",
      "m2:default": false
    },
    "branching": {
      "@type": "xsd:boolean",
      "m2:description": "Whether cascade includes branching (one stage → multiple stages)",
      "m2:default": false
    }
  }
}
```

### RAAS Instantiation

```json
{
  "@id": "m0:RAAS_Cascade",
  "@type": "m2:Cascade",
  "m2:trajectoryShape": "Linear",  // Convergence to BP setpoint
  "m2:amplifying": true,            // Enzymatic gain at each stage
  "m2:branching": true,             // Ang II → multiple effector pathways
  "m2:stages": [
    "Renin secretion",
    "Angiotensinogen → Angiotensin I",
    "Angiotensin I → Angiotensin II (via ACE)",
    "Angiotensin II → Multiple effects"
  ]
}
```

---

## Future Directions

### Additional Attributes Candidates

#### For Trajectory
- `deterministic` (boolean): Whether trajectory is deterministic or stochastic
- `reversible` (boolean): Whether trajectory can be reversed
- `smooth` (boolean): Whether trajectory is differentiable
- `bounded` (boolean): Whether trajectory remains in bounded region

#### For Cascade
- `reversible` (boolean): Whether cascade can run backwards
- `error_correcting` (boolean): Whether cascade includes error correction mechanisms
- `parallel_stages` (boolean): Whether stages can execute in parallel

#### For Process
- `discrete` (boolean): Discrete-time vs continuous-time
- `ergodic` (boolean): Whether all states are reachable

### Systematic Attribute Discovery

**Process**:
1. Analyze existing M2 metaconcepts
2. Identify natural variations/subtypes
3. Extract common variation dimensions
4. Formalize as ValueSpace attributes

**Benefits**:
- Prevents subtype explosion
- Enables configuration without ontology modification
- Maintains clean M2 structure

---

## Validation Checklist

### For N-ary MetaconceptCombo

- ✅ Mathematical foundation (tensor product associativity)
- ✅ Clear coupling algorithm (dimension intersection)
- ✅ Concrete example (Cascade with 3 parents)
- ✅ Practical need (cannot be reduced to binary combos)
- ⏳ Implementation (planned v14.4.0+)

### For Typed Attributes

- ✅ Leverages existing M2 construct (ValueSpace)
- ✅ Prevents ontology proliferation
- ✅ Concrete example (Trajectory.shape with 9 values)
- ✅ Implemented (v14.3.6)
- ⏳ Systematic application to other metaconcepts

---

## Appendix: Shape Values for Trajectory

### Complete List (9 values)

| Shape | Description | Examples | Characteristics |
|-------|-------------|----------|-----------------|
| **Linear** | Straight line | Ballistic, free fall | No curvature, monotonic |
| **Circular** | Closed periodic loop | Orbit, oscillator | Periodic, closed, constant radius |
| **Elliptical** | Closed with varying radius | Planetary orbit, comet | Periodic, two foci, eccentricity < 1 |
| **Spiral** | Converging/diverging helix | Damped oscillator, galaxy | Asymptotic, stable/unstable |
| **Hyperbolic** | Open escape trajectory | Comet flyby, saddle escape | Unbounded, approaches asymptote |
| **Random** | Stochastic, unpredictable | Brownian motion, diffusion | Probabilistic, no deterministic pattern |
| **Constrained** | Confined to manifold | Pendulum, bead on wire | Lower-dimensional, obeys constraints |
| **Chaotic** | Deterministic but aperiodic | Lorenz attractor, double pendulum | Sensitive to initial conditions |
| **Piecewise** | Composed of distinct segments | Rocket trajectory, lifecycle | Discontinuous derivatives at transitions |

---

**End of Document**

*Version 1.0.0 - 2026-02-05*
