# M2 Behavioral/Sequential Metaconcepts Family (v14.3.0)

**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-01-28  
**Version:** TSCG 14.3.0

---

## Executive Summary

This document introduces 5 new M2 metaconcepts that form a coherent family for modeling **sequential, temporal, and behavioral patterns**. These metaconcepts bridge the gap between pure temporal abstractions (Process) and pure structural patterns (Network).

### New Metaconcepts

| # | Metaconcept | Formula | Polarity | Parent | Role |
|---|-------------|---------|----------|--------|------|
| 1 | **Behavior** | S⊗D⊗F | Dual | - | Network of decomposable Steps |
| 2 | **Tropism** | A⊗S⊗D⊗F | Dual | Behavior | Gradient-directed Behavior |
| 3 | **Workflow** | S⊗D⊗F | Dual | - | Prescriptive Process implementation |
| 4 | **Step** | S⊗I⊗D | Dual | Node | Temporal Node that triggers Actions |
| 5 | **Action** | D⊗I | Dual | - | Atomic operation |

---

## 1. Behavior (S⊗D⊗F)

### Definition
**Behavior** is a network of coordinated Steps that can be decomposed and analyzed. It represents a structured operational pattern observable in Territory and modelable in Map.

### Tensor Formula
```
|Behavior⟩ = S ⊗ D ⊗ F
```

**Dimensions:**
- **S (Structure):** Network topology of Steps
- **D (Dynamics):** Temporal evolution
- **F (Flow):** Execution flow through network

### Polarity: Dual

| Perspective | Description |
|-------------|-------------|
| **Territory (Eagle Eye)** | Observable network of Steps with measured execution |
| **Map (Sphinx Eye)** | Modeled network of Steps with predicted execution |

### Key Properties

- **Decomposition:** `m2:decomposedInto m2:Step`
- **Category:** Dynamic
- **Epistemic Gap:** 0.20

### Examples

1. **Predator hunting:** stalk → chase → capture
2. **HTTP handling:** receive → parse → process → respond
3. **Photosynthesis:** light absorption → water splitting → CO2 fixation
4. **Learning algorithm:** initialize → iterate → converge

### Distinction from Related Metaconcepts

| vs | Distinction |
|----|-------------|
| **Process** | Process is pure temporal (D⊗F); Behavior adds structure (S) |
| **Workflow** | Workflow prescribes; Behavior describes observation |
| **Network** | Network is pure topology; Behavior adds dynamics |

---

## 2. Tropism (A⊗S⊗D⊗F)

### Definition
**Tropism** is a specialized Behavior directed by an external gradient stimulus. It represents orientation or movement towards (positive) or away from (negative) an Attractor source.

### Inheritance
```turtle
m2:Tropism rdfs:subClassOf m2:Behavior .
```

### Tensor Formula
```
|Tropism⟩ = A ⊗ S ⊗ D ⊗ F
```

**Dimensions:**
- **A (Attractor):** Gradient field directing movement *(NEW)*
- **S (Structure):** Network topology *(inherited)*
- **D (Dynamics):** Temporal evolution *(inherited)*
- **F (Flow):** Directional flow *(inherited)*

### Polarity: Dual (Double)

1. **Bicephalous Duality:**
   - Territory: Observable gradient-directed phenomenon
   - Map: Modeled gradient-directed behavior

2. **Directional Duality:**
   - Positive: Attraction towards stimulus
   - Negative: Repulsion away from stimulus

### Key Properties

- **Gradient:** `m2:hasGradient m3:eagle_eye:Attractor`
- **Polarity Sign:** {positive, negative}
- **Category:** Dynamic
- **Epistemic Gap:** 0.18

### Examples

1. **Phototropism:** Plant stem bends towards light source (positive)
2. **Chemotaxis:** Bacteria swims towards nutrient gradient (positive)
3. **Geotropism:** Plant roots grow downward (positive towards gravity)
4. **Negative phototropism:** Roots grow away from light (negative)
5. **Thermotaxis:** Organism moves towards optimal temperature

### Biological Validation

Tropism patterns are ubiquitous in biological systems:

- **Plants:** phototropism, geotropism, thigmotropism
- **Microorganisms:** chemotaxis, phototaxis, aerotaxis
- **Animals:** taxis behaviors (migration, foraging)

---

## 3. Workflow (S⊗D⊗F)

### Definition
**Workflow** is a structured network implementation of a Process. It provides a prescriptive representation (Map-oriented) of how a Process should be executed.

### Tensor Formula
```
|Workflow⟩ = S ⊗ D ⊗ F
```

**Note:** Same formula as Behavior, but different epistemic role.

### Polarity: Dual (Faceted)

| Facet | Description |
|-------|-------------|
| **Structural** | Static representation as network topology |
| **Executory** | Dynamic simulation or execution trace |

### Key Properties

- **Implementation:** `m2:implementsProcess m2:Process`
- **Category:** Structural
- **Epistemic Gap:** 0.22

### Examples

1. **Manufacturing:** Assembly line steps with dependencies
2. **CI/CD Pipeline:** build → test → deploy sequence
3. **Clinical Protocol:** diagnosis → treatment → follow-up
4. **Recipe:** Cooking steps with timing constraints

### Workflow vs Behavior

| Aspect | Workflow | Behavior |
|--------|----------|----------|
| **Epistemic Role** | Prescriptive (SHOULD) | Descriptive (IS) |
| **Primary View** | Map (Sphinx Eye) | Territory (Eagle Eye) |
| **Purpose** | Model what to do | Observe what occurs |
| **Relation to Process** | Implements | Independent |

---

## 4. Step (S⊗I⊗D)

### Definition
**Step** is a Node specialized for sequential/temporal contexts. It serves as an elementary unit in Behavior or Workflow networks.

### Inheritance
```turtle
m2:Step rdfs:subClassOf m2:Node .
```

### Tensor Formula
```
|Step⟩ = S ⊗ I ⊗ D
```

**Dimensions:**
- **S (Structure):** Network node position *(inherited)*
- **I (Information):** Step content/semantics *(inherited)*
- **D (Dynamics):** Temporal/sequential context *(NEW)*

### Specialization from Node

| Property | Node | Step |
|----------|------|------|
| **Context** | Generic network | Sequential/temporal |
| **Capability** | Connection point | Triggers Actions |
| **Formula** | S⊗I | S⊗I⊗D |

### Key Properties

- **Triggers:** `m2:triggers m2:Action` (1:N)
- **Component of:** `m2:componentOf` {m2:Behavior, m2:Workflow}
- **Category:** Structural
- **Epistemic Gap:** 0.20

### Examples

1. **Butterfly egg stage:** Triggers cell division actions
2. **Recipe "make roux":** Triggers heat, stir, add flour actions
3. **HTTP parse:** Triggers tokenize, validate actions
4. **Training epoch:** Triggers forward, backward, update actions

---

## 5. Action (D⊗I)

### Definition
**Action** is an atomic operation triggered by a Step. It represents an indivisible executable unit with informational content.

### Tensor Formula
```
|Action⟩ = D ⊗ I
```

**Dimensions:**
- **D (Dynamics):** Execution/operation
- **I (Information):** Semantic content

### Key Properties

- **Triggered by:** `m2:triggeredBy m2:Step`
- **Atomicity:** Not further decomposable in behavioral context
- **Category:** Dynamic
- **Epistemic Gap:** 0.15 (lowest - most concrete)

### Examples

1. **Cell division** (egg stage step)
2. **Heat butter** (make roux step)
3. **HTTP tokenize** (parse step)
4. **Gradient descent update** (training step)
5. **Baroreceptor activation** (sense step)

---

## Architectural Relationships

### Hierarchy Diagram

```
Behavior (S⊗D⊗F)                    [Dynamic Network]
    ↓ rdfs:subClassOf
Tropism (A⊗S⊗D⊗F)                   [Gradient-directed]
    ↓ decomposedInto
Step (S⊗I⊗D)                        [Temporal Node]
    ↓ triggers
Action (D⊗I)                        [Atomic operation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
(Parallel, independent hierarchy)

Process (D⊗F)                       [Temporal abstraction]
    ↓ implementedBy
Workflow (S⊗D⊗F)                    [Prescriptive network]

Node (S⊗I)                          [Generic network element]
    ↓ rdfs:subClassOf
Step (S⊗I⊗D)                        [Temporal specialization]
```

### Relationship Summary

| Relation | Type | Description |
|----------|------|-------------|
| `Tropism subClassOf Behavior` | Inheritance | Tropism is specialized Behavior |
| `Step subClassOf Node` | Inheritance | Step is specialized Node |
| `Behavior decomposedInto Step` | Composition | Behavior contains Steps |
| `Step triggers Action` | Causality | Step activates Actions |
| `Workflow implementsProcess Process` | Reification | Workflow realizes Process |

---

## Mathematical Validation

### Tensor Product Coherence

All formulas use valid tensor products of M3 ASFID dimensions:

```
Action:   D ⊗ I           (order 2)
Step:     S ⊗ I ⊗ D       (order 3)
Behavior: S ⊗ D ⊗ F       (order 3)
Workflow: S ⊗ D ⊗ F       (order 3)
Tropism:  A ⊗ S ⊗ D ⊗ F   (order 4)
```

### Epistemic Gap Distribution

| Metaconcept | Gap | Interpretation |
|-------------|-----|----------------|
| Action | 0.15 | Most concrete/measurable |
| Tropism | 0.18 | Very observable (gradient-driven) |
| Behavior | 0.20 | Observable pattern |
| Step | 0.20 | Observable unit |
| Workflow | 0.22 | More abstract (prescriptive) |

---

## Validation Through Poclets

### Butterfly Metamorphosis

```
Behavior: "Holometabolic development"
    ↓ decomposedInto
Steps:
    - Egg → triggers: cell_division
    - Larva → triggers: feeding, growth
    - Pupa → triggers: histolysis, histogenesis
    - Adult → triggers: reproduction, flight
```

### Blood Pressure Control

```
Behavior: "Baroreflex regulation"
    ↓ decomposedInto
Steps:
    - Sense → triggers: baroreceptor_activation
    - Integrate → triggers: medulla_processing
    - Respond → triggers: sympathetic_output, parasympathetic_output
```

### Phototropism (Plant)

```
Tropism: "Phototropism" (positive)
    ↓ hasGradient: Light intensity field
    ↓ decomposedInto
Steps:
    - Detect → triggers: photoreceptor_activation
    - Signal → triggers: auxin_redistribution
    - Grow → triggers: cell_elongation
```

---

## Design Rationale

### Why These 5 Metaconcepts?

1. **Behavior:** Needed to model decomposable sequential patterns (gap between Process and Network)

2. **Tropism:** Ubiquitous in biological systems; validates as specialized Behavior with gradient constraint

3. **Workflow:** Distinguishes prescriptive (Map) from descriptive (Territory) sequential models

4. **Step:** Temporal specialization of Node; bridge between structure and dynamics

5. **Action:** Atomic operational unit; finest-grained executable element

### Fills Critical Gap

**Before v14.3.0:**
- ✅ Process (D⊗F) for pure temporal sequences
- ✅ Network (S⊗F) for pure structural patterns
- ❌ Missing: Temporal + Structural fusion

**After v14.3.0:**
- ✅ Behavior/Workflow (S⊗D⊗F) bridges the gap
- ✅ Step/Action provide decomposition levels
- ✅ Tropism adds gradient constraint

---

## Implementation Notes

### OWL Relations to Define

```turtle
# New object properties
m2:decomposedInto a owl:ObjectProperty ;
    rdfs:domain m2:Behavior ;
    rdfs:range m2:Step .

m2:triggers a owl:ObjectProperty ;
    rdfs:domain m2:Step ;
    rdfs:range m2:Action .

m2:implementsProcess a owl:ObjectProperty ;
    rdfs:domain m2:Workflow ;
    rdfs:range m2:Process .

m2:hasGradient a owl:ObjectProperty ;
    rdfs:domain m2:Tropism ;
    rdfs:range m3:eagle_eye:Attractor .

m2:triggeredBy a owl:ObjectProperty ;
    rdfs:domain m2:Action ;
    rdfs:range m2:Step ;
    owl:inverseOf m2:triggers .
```

### Usage Guidelines

1. **Use Behavior when:** Modeling observable sequential patterns that decompose into steps
2. **Use Tropism when:** System responds to external gradient (attraction/repulsion)
3. **Use Workflow when:** Prescribing how a Process should be implemented
4. **Use Step when:** Defining units in sequential networks
5. **Use Action when:** Specifying atomic operations triggered by Steps

---

## Future Work

### Potential Extensions

1. **Composite Actions:** Actions composed of sub-Actions (currently atomic by definition)
2. **Step Dependencies:** Formalize precedence constraints between Steps
3. **Workflow Optimization:** Metrics for workflow efficiency (ORIVE dimensions)
4. **Multi-gradient Tropism:** Systems responding to multiple gradients simultaneously
5. **Emergent Behaviors:** Higher-order patterns emerging from Behavior composition

### Research Questions

1. Can Behaviors compose into meta-Behaviors? (hierarchy depth)
2. What is the relationship between Tropism and Regulation? (both have Attractor)
3. How do Workflows transform during execution? (Map→Territory trajectory)
4. Can Actions have ORIVE characterization? (Map-quality metrics)

---

## References

### Related M2 Metaconcepts

- **Process** (D⊗F): Parent abstraction for Workflow
- **Node** (S⊗I): Parent abstraction for Step
- **Network** (S⊗F): Related structural pattern
- **Regulation** (A⊗S⊗F): Related control pattern
- **Attractor** (A⊗S): Component in Tropism gradient

### Validated Poclets

- **Butterfly Metamorphosis:** 6-step lifecycle
- **Blood Pressure Control:** 5-effector homeostatic system
- **Magic Color Wheel:** Pentagonal polarity workflow

---

## Changelog

### v14.3.0 (2026-01-28)
- Initial release of 5 behavioral/sequential metaconcepts
- Total M2 metaconcepts: 60 → 65
- Dual polarity metaconcepts: 6 → 11
- Validated across 3 poclets

---

## Contact

For questions or contributions regarding these metaconcepts, please refer to the main TSCG repository documentation.

**Repository:** https://github.com/Echopraxium/tscg  
**Ontology URI:** https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts_Ontology.jsonld

---

**End of Document**
