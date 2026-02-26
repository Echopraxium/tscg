# TSCG M2 GenericConcepts Ontology

**Version**: 7.2.0  
**Status**: Production Ready - COMPLETE ✅  
**Date**: January 15, 2026  
**Namespace**: `https://github.com/Echopraxium/tscg/blob/main/ontology/TSCG_M2_GenericConcepts_Ontology.jsonld#`

---

## Table of Contents

1. [Overview](#overview)
2. [Mathematical Framework](#mathematical-framework)
3. [Triple Axes Framework](#triple-axes-framework)
4. [The Nine Categories](#the-nine-categories)
5. [The 50 GenericConcepts](#the-42-GenericConcepts)
6. [Polarity System](#polarity-system)
7. [Epistemic Gap](#epistemic-gap)
8. [Category Theory Integration](#category-theory-integration)
9. [Critical Design Decisions](#critical-design-decisions)
10. [Usage Guidelines](#usage-guidelines)
11. [References](#references)

---

## Overview

### What is M2?

**M2** (GenericConcepts Layer) is the second foundational layer of the **TSCG** (Transdisciplinary System Construction Game) framework. In the LEGO Technic analogy:

- **M3** = Elementary bricks (5 orthonormal dimensions: A, S, F, I, D)
- **M2** = Sub-assemblies (systemic patterns from tensor products of M3)
- **M1** = Instructions (domain-specific concepts)
- **M0** = Constructions (actual systems)

M2 defines **50 GenericConcepts** that represent recognizable organizational patterns found across multiple domains. These are not domain-specific terms (biology, economics, sociology) but **pure systemic vocabulary** drawn from:

- Systems Theory (von Bertalanffy, Laszlo)
- Cybernetics (Wiener, Ashby, Beer)
- Information Theory (Shannon)
- Control Theory (Kalman)
- Complex Systems Science (Prigogine, Kauffman)

### Design Philosophy

**Purity Principle**: M2 uses only transdisciplinary systemic vocabulary. Domain-specific concepts belong to M1 extensions.

**Examples**:
- ✅ M2: Network, Hierarchy, Feedback, Memory
- ❌ M2: Neuron, Market, Gene, Organization (→ M1)

**Purpose**: Enable **ontological weaving** - GenericConcepts relate to each other through semantic proximity, inclusion, composition, causality, and duality relationships, forming a coherent systemic fabric.

---

## Mathematical Framework

### Tensor Space Structure

M2 is constructed as a **graded tensor algebra** over the M3 Hilbert space ℂ⁵:

```
T_M2 = ⊕_{k=1}^{3} (H_M3)^{⊗k}
```

Where:
- **Order 1**: 5 components (linear: A, S, F, I, D)
- **Order 2**: 25 components (bilinear: A⊗S, S⊗F, I⊗D, etc.)
- **Order 3**: 125 components (trilinear: A⊗S⊗F, I⊗S⊗D, etc.)
- **Total**: 155 possible tensor components

### From Tensors to GenericConcepts

Not all 155 tensor components correspond to meaningful GenericConcepts. M2 selects 50 patterns that:

1. Have clear **systemic semantics** (recognizable across domains)
2. Are **non-redundant** (minimal collisions)
3. Cover the **essential systemic vocabulary**
4. Enable **compositional reasoning** (GenericConcepts combine)

### Tensor Notation Examples

| GenericConcept | Tensor Formula | Interpretation |
|-------------|----------------|----------------|
| Homeostasis | A⊗S⊗F | Attractor coupled with structure and flow |
| Memory | ∫(D-F)dτ | Temporal integration of dynamics minus flow |
| Network | S⊗I⊗F | Structure enabling information flow |
| Bifurcation | ∂D/∂F | Sensitivity of dynamics to flow changes |
| Symmetry | S | Pure structural invariance |
| Capacity | S⊗I | Structural support for information complexity |

---

## Triple Axes Framework

M2 GenericConcepts are characterized by **three orthogonal axes**:

### Axis 1: Ontological Nature

**Question**: *Does this GenericConcept exist in models, reality, or both?*

- **ModelSpace**: Abstract representations, maps, theories
  - Examples: Constraint, Hierarchy, Symmetry, Code
  - Properties: Static, analytical, measurable
  
- **RealitySpace**: Tangible processes, territories, phenomena
  - Examples: Homeostasis, Dissipation, Process, Event
  - Properties: Dynamic, observable, causal
  
- **DualNature**: Exists in both spaces simultaneously
  - Examples: Regulation, Network, Bifurcation, Link
  - Properties: Bridge between model and reality

### Axis 2: Operational Direction

**Question**: *Is this GenericConcept about observing/analyzing or generating/building?*

- **Analytical** (Φ_A: M0 → M3): Observe, decompose, measure
  - Examples: Constraint, Threshold, Representation, Role
  - Use: Understanding existing systems
  
- **Constructive** (Φ_C: M3 → M0): Generate, synthesize, build
  - Examples: Homeostasis, Adaptation, Transformation, Agent
  - Use: Designing new systems
  
- **DualProjection**: Both analytical and constructive
  - Examples: Regulation, Memory, Coding, Mediator
  - Use: Bidirectional system engineering

### Axis 3: Granularity Direction

**Question**: *Does this GenericConcept aggregate or disaggregate?*

- **Composition**: Bottom-up (atoms → molecule, parts → whole)
  - Examples: Emergence, Modularity (when building)
  - LEGO analogy: Assembling bricks into construction
  
- **Decomposition**: Top-down (molecule → atoms, whole → parts)
  - Examples: Modularity (when analyzing), Dissipation
  - LEGO analogy: Disassembling construction into bricks
  
- **Bidirectional**: Intrinsically operates in both directions
  - Examples: Coding (Encoding/Decoding), Convergence/Divergence
  
- **N/A**: Not applicable (no clear granularity direction)
  - Examples: Symmetry, State, Threshold

### Independence of Axes

These three axes are **orthogonal** (independent):
- A GenericConcept can be (ModelSpace, Analytical, N/A)
- Another can be (RealitySpace, Constructive, Composition)
- A third can be (DualNature, DualProjection, Bidirectional)

---

## The Nine Categories

GenericConcepts are grouped into **9 functional categories** based on dominant M3 dimensions and systemic role:

### 1. Structural Category

**Dominant M3**: S (Structure), low D (Dynamics)  
**Focus**: Topology, organization, spatial arrangement

**GenericConcepts (14)**:
- Hierarchy, Network, Symmetry, Modularity, Topology, Segmentation
- Invariant, Signature, Capacity, Space
- Node, Path, Cluster, Hub

**Examples**: Crystal lattices, network graphs, organizational charts

---

### 2. Dynamic Category

**Dominant M3**: D (Dynamics)  
**Focus**: Processes, transformations, temporal evolution

**GenericConcepts (8)**:
- Transformation, Bifurcation, Process, Event
- Synergy (dual), Fusion (dual), Convergence (dual), Gradient

**Examples**: Phase transitions, chemical reactions, evolutionary processes

---

### 3. Regulatory Category

**Dominant M3**: A (Attractor), tensor couplings  
**Focus**: Control, stabilization, constraint mechanisms

**GenericConcepts (7)**:
- Homeostasis, Regulation, Constraint
- Threshold, Trigger, Activation (dual), Tropism (dual)

**Examples**: Feedback loops, thermostats, homeostatic systems

---

### 4. Adaptive Category

**Dominant M3**: I (Information), medium F (Flow)  
**Focus**: Learning, evolution, environmental response

**GenericConcepts (4)**:
- Resilience, Adaptation, Emergence, Memory

**Examples**: Neural plasticity, ecosystem resilience, machine learning

---

### 5. Energetic Category

**Dominant M3**: F (Flow), high D (Dynamics)  
**Focus**: Energy, matter, information flows

**GenericConcepts (2)**:
- Dissipation, Storage

**Examples**: Heat dissipation, battery storage, data buffers

---

### 6. Informational Category

**Dominant M3**: I (Information)  
**Focus**: Data, representation, communication

**GenericConcepts (6)**:
- Code, Coding (dual), Representation, Language, Signature, Signal

**Examples**: Genetic code, natural languages, data formats

---

### 7. Ontological Category

**Dominant M3**: S⊗F patterns  
**Focus**: Fundamental system entities and boundaries

**GenericConcepts (7)**:
- System, Environment, Observer, State, Substrate, Gradient, Space

**Examples**: System-environment boundary, state space, phase space

---

### 8. Teleonomic Category

**Dominant M3**: A (Attractor)  
**Focus**: Goal-directedness, purpose, optimization

**GenericConcepts (1)**:
- Self-Organization

**Examples**: Crystal formation, pattern emergence, autopoietic systems

---

### 9. Relational Category

**Dominant M3**: S⊗I patterns  
**Focus**: Interactions between entities, roles, connections

**GenericConcepts (5)**:
- Agent, Role, Mediator, Link, Relation

**Examples**: Actor-role assignments, API mediators, network edges

---

## The 50 GenericConcepts

### Complete Reference Table

| # | GenericConcept | Category | Formula | Nature | Direction | Granularity | Gap | Polarity |
|---|-------------|----------|---------|--------|-----------|-------------|-----|----------|
| 1 | Capacity | Structural | S⊗I | ModelSpace | Analytical | N/A | 0.25 | neutral |
| 2 | Cluster | Structural | S⊗I⊗A | RealitySpace | Constructive | Composition | 0.3 | neutral |
| 3 | Hierarchy | Structural | S⊗A | ModelSpace | Analytical | N/A | 0.3 | neutral |
| 4 | Hub | Structural | S⊗F | DualNature | DualProjection | N/A | 0.2 | neutral |
| 5 | Invariant | Structural | S⊗A | ModelSpace | Analytical | N/A | 0.2 | neutral |
| 6 | Modularity | Structural | S⊗I | ModelSpace | Analytical | Decomposition | 0.3 | neutral |
| 7 | Network | Structural | S⊗I⊗F | DualNature | DualProjection | N/A | 0.25 | neutral |
| 8 | Node | Structural | S⊗I | DualNature | DualProjection | N/A | 0.2 | neutral |
| 9 | Path | Structural | S⊗I⊗D | DualNature | DualProjection | Composition | 0.25 | neutral |
| 10 | Segmentation | Structural | S⊗I⊗D | ModelSpace | Analytical | Decomposition | 0.3 | neutral |
| 11 | Symmetry | Structural | S | ModelSpace | Analytical | N/A | 0.2 | neutral |
| 12 | Topology | Structural | S⊗I | ModelSpace | Analytical | N/A | 0.2 | neutral |
| 13 | Bifurcation | Dynamic | ∂D/∂F | RealitySpace | DualProjection | N/A | 0.4 | neutral |
| 14 | Convergence (Convergence/Divergence) | Dynamic | -∇·D (convergence) / ∇·D (divergence) | RealitySpace | DualProjection | N/A | 0.3 | dual |
| 15 | Event | Dynamic | D⊗I | RealitySpace | Constructive | N/A | 0.25 | neutral |
| 16 | Fusion (Fusion/Fission) | Dynamic | S⊗D | RealitySpace | Constructive | Bidirectional | 0.25 | dual |
| 17 | Process | Dynamic | D⊗F | RealitySpace | Constructive | N/A | 0.2 | neutral |
| 18 | Synergy (Positive/Negative) | Dynamic | I⊗D | RealitySpace | Constructive | N/A | 0.3 | dual |
| 19 | Transformation | Dynamic | D⊗S⊗I | RealitySpace | Constructive | N/A | 0.3 | neutral |
| 20 | Activation (Activation/Inhibition) | Regulatory | A⊗D | RealitySpace | Constructive | N/A | 0.2 | dual |
| 21 | Constraint | Regulatory | S⊗I | ModelSpace | Analytical | N/A | 0.25 | neutral |
| 22 | Homeostasis | Regulatory | A⊗S⊗F | RealitySpace | Constructive | N/A | 0.2 | neutral |
| 23 | Regulation | Regulatory | A⊗S⊗F | DualNature | DualProjection | N/A | 0.35 | neutral |
| 24 | Threshold | Regulatory | A⊗I | ModelSpace | Analytical | N/A | 0.2 | neutral |
| 25 | Trigger | Regulatory | D⊗I | RealitySpace | Constructive | N/A | 0.25 | neutral |
| 26 | Adaptation | Adaptive | I⊗F⊗D | RealitySpace | Constructive | N/A | 0.3 | neutral |
| 27 | Emergence | Adaptive | I⊗S⊗D | RealitySpace | Constructive | Composition | 0.5 | neutral |
| 28 | Memory | Adaptive | ∫(D - F)dτ | RealitySpace | DualProjection | N/A | 0.3 | neutral |
| 29 | Resilience | Adaptive | A⊗S | RealitySpace | Constructive | N/A | 0.25 | neutral |
| 30 | Dissipation | Energetic | F⊗D | RealitySpace | Constructive | Decomposition | 0.15 | neutral |
| 31 | Storage | Energetic | S⊗F | RealitySpace | Constructive | N/A | 0.2 | neutral |
| 32 | Code | Informational | I⊗S | ModelSpace | Analytical | N/A | 0.2 | neutral |
| 33 | Coding (Encoding/Decoding) | Informational | I⊗S⊗D | RealitySpace | DualProjection | Bidirectional | 0.2 | dual |
| 34 | Language | Informational | I⊗S⊗F | DualNature | DualProjection | N/A | 0.3 | neutral |
| 35 | Representation | Informational | I⊗S | ModelSpace | Analytical | N/A | 0.25 | neutral |
| 36 | Signal | Informational | I⊗F | RealitySpace | Constructive | N/A | 0.2 | neutral |
| 37 | Signature | Informational | I⊗S | ModelSpace | Analytical | N/A | 0.2 | neutral |
| 38 | Environment | Ontological | F⊗I | RealitySpace | Analytical | N/A | 0.25 | neutral |
| 39 | Gradient | Ontological | ∇F or ∇I | RealitySpace | Analytical | N/A | 0.2 | neutral |
| 40 | Observer | Ontological | I⊗A | ModelSpace | Analytical | N/A | 0.35 | neutral |
| 41 | Space | Ontological | S⊗I | ModelSpace | Analytical | N/A | 0.25 | neutral |
| 42 | State | Ontological | I | ModelSpace | Analytical | N/A | 0.15 | neutral |
| 43 | Substrate | Ontological | S⊗F | RealitySpace | Constructive | N/A | 0.2 | neutral |
| 44 | System | Ontological | S⊗F | DualNature | DualProjection | N/A | 0.3 | neutral |
| 45 | Self-Organization | Teleonomic | A⊗I⊗D | RealitySpace | Constructive | Composition | 0.4 | neutral |
| 46 | Agent | Relational | S⊗I⊗D | RealitySpace | Constructive | N/A | 0.35 | neutral |
| 47 | Link | Relational | S⊗I⊗F | RealitySpace | Constructive | N/A | 0.2 | neutral |
| 48 | Mediator | Relational | F⊗I⊗S | DualNature | DualProjection | N/A | 0.3 | neutral |
| 49 | Relation | Relational | S⊗I | ModelSpace | Analytical | N/A | 0.25 | neutral |
| 50 | Role | Relational | S⊗I | ModelSpace | Analytical | N/A | 0.25 | neutral |

**Note**: This table shows all 50 GenericConcepts. Tropism was originally #43 but is now #44 due to Signal insertion. The 5 Network decomposition GenericConcepts (Node, Relation, Path, Cluster, Hub) were added in v7.1.0.

---

## Polarity System

### Binary and Dual Polarity

M2 uses a **minimal polarity system**:

- **Neutral** (~70%): Single, unique concept
- **Dual** (~30%): Intrinsically bidirectional (Encoding/Decoding, Fusion/Fission)

**No n-ary polarity** (ternary, quaternary) - rejected as over-generalization.

### Dual GenericConcepts (7)

| GenericConcept | Aspect 1 | Aspect 2 | Interpretation |
|-------------|----------|----------|----------------|
| Coding | Encoding | Decoding | Source → Code vs Code → Source |
| Synergy | Positive Synergy | Negative Synergy | Enhancement vs Inhibition |
| Fusion | Fusion | Fission | Union vs Separation |
| Activation | Activation | Inhibition | Enable vs Block |
| Convergence | Convergence | Divergence | Focusing vs Dispersing |
| Tropism | Positive Tropism | Negative Tropism | Attraction vs Repulsion |

**Note**: These are not binary opposites (positive/negative pairs) but intrinsically dual processes.

---

## Epistemic Gap

### Definition

The **epistemic gap** ΔΘ measures the inevitable discrepancy between model and reality:

```
ΔΘ(M) = ‖P(Reality) - Model‖ ∈ [0,1]
```

Where:
- **0.0**: Perfect model-reality correspondence (impossible for most GenericConcepts)
- **1.0**: Maximal gap (model completely fails to capture reality)

### Interpretation by Range

- **Low gap (0.10-0.20)**: Well-defined, easily modeled
  - Examples: Symmetry (0.20), State (0.15), Dissipation (0.15)
  
- **Medium gap (0.25-0.35)**: Moderate modeling challenges
  - Examples: Constraint (0.25), Network (0.25), Regulation (0.35)
  
- **High gap (0.40-0.50)**: Difficult to model accurately
  - Examples: Bifurcation (0.40), Self-Organization (0.40), Emergence (0.50)

### Why Emergence has ΔΘ = 0.50

**Emergence** represents the appearance of novel properties **not predictable from components**. By definition, this creates maximal epistemic uncertainty - we cannot fully model what emerges before it actually emerges.

---

## Category Theory Integration

### Functors

M2 is connected to other layers through categorical functors:

```
F_⊗: Cat_M3 → Cat_M2        (tensorization)
F_instantiate: Cat_M2 → Cat_M1   (domain specialization)
F_model: Cat_M1 → Cat_M0         (system instantiation)
```

**Total Functor**:
```
F_total = F_model ∘ F_instantiate ∘ F_⊗
```

### Morphisms in M2

M2 supports several types of morphisms (structure-preserving relationships):

1. **Inclusion (⊆)**: A ⊆ B
   - Example: Homeostasis ⊆ Regulation
   - Interpretation: Homeostasis is a special case of Regulation

2. **Composition (∘)**: C = A ∘ B
   - Example: Learning = Memory ∘ Adaptation
   - Interpretation: Learning emerges from Memory composed with Adaptation

3. **Duality (op)**: B = A^op
   - Example: Divergence = Convergence^op
   - Interpretation: Dual aspects of same process

4. **Emergence (⇑)**: E ⇑ {A₁, A₂, ...}
   - Example: Consciousness ⇑ {Neural Network, Memory, Attention}
   - Interpretation: E emerges from interaction of multiple GenericConcepts

### Adjunction

There exists an adjunction between abstraction and instantiation:

```
F_abstract ⊣ F_instantiate
```

This captures the Korzybski map-territory relationship: moving from concrete systems (M0) to abstract patterns (M2) and back.

---

## Critical Design Decisions

### 1. Time is External

**Decision**: Time (t) is a **parameter**, not a 6th dimension in M3.

**Consequence**: Temporal GenericConcepts (Memory, Process) require **temporal integration** → They belong to M2, not M3.

**Formula Example**:
```
Memory(t) = ∫_{-∞}^{t} [D(τ) - F(τ)]dτ
```

---

### 2. Memory is M2, not M3

**Reason**: Memory requires integrating (D - F) over time. This is a **derived pattern**, not an elementary dimension.

**Distinction**:
- M3: Instantaneous dimensions (A, S, F, I, D at time t)
- M2: Temporal accumulation (Memory integrates history)

---

### 3. Regulation is M2, not M3

**Reason**: Regulation = A⊗S⊗F coupling. This is a **tensor product**, not a single dimension.

**Interpretation**: Regulation emerges from the coordination of:
- Attractor (target state)
- Structure (control pathways)
- Flow (error correction)

---

### 4. Flow is M3, not M2

**Decision**: F (Flow) is the **3rd dimension** in M3 with axiom F ≥ 0.1.

**Reason**: Openness to environment is **fundamental**, not derived. All systems exchange with their context.

**Old mistake**: Having "Flow" as both M3 dimension and M2 GenericConcept (redundant).

---

### 5. Triple Axes are Orthogonal

**Critical**: The three axes are **independent** (not conflated):

- Axis 1 (Model/Reality) ⊥ Axis 2 (Analytical/Constructive) ⊥ Axis 3 (Composition/Decomposition)

**Wrong interpretation**: Thinking "Model = Analytical" or "Reality = Constructive"  
**Correct**: A GenericConcept can be (Reality, Analytical) like Gradient, or (Model, Constructive) - though rare.

---

### 6. Binary/Dual Polarity Only

**Rejected**: N-ary polarity (ternary: positive/neutral/negative, quaternary, etc.)

**Reason**: Over-generalization risk. Simplicity principle.

**Adopted**: 
- Most GenericConcepts are **neutral** (unique)
- Some are **dual** (intrinsically bidirectional)

---

### 7. No Domain-Specific Terms in M2

**Purity Principle**: M2 uses only transdisciplinary vocabulary.

**Rejected Terms**:
- Autopoiesis (biology-specific) → Replaced by Self-Organization (cybernetic)
- Catalysis (chemistry-specific) → Replaced by Synergy (general)
- Neuron, Gene, Market, etc. → Belong to M1 extensions

**Accepted Vocabulary**:
- Systems Theory, Cybernetics, Information Theory, Control Theory

---

### 8. Self-Referential Namespace

**Format**: 
```
https://github.com/Echopraxium/tscg/blob/main/ontology/TSCG_M2_GenericConcepts_Ontology.jsonld#
```

**Reason**: Linked Data compliance, URI dereferenceability.

**Standard**: RDF, RDFS, OWL, Dublin Core only (no SKOS dependency).

---

## Usage Guidelines

### When to Use M2

Use M2 GenericConcepts when:

1. **Analyzing existing systems** (Analytical direction)
   - Identify patterns: "This system exhibits Network structure with Hierarchical control"
   - Measure properties: "The Capacity is 100 MB, with current Storage at 60%"

2. **Designing new systems** (Constructive direction)
   - Specify requirements: "Need Resilience + Adaptation under perturbations"
   - Combine patterns: "Build Regulation through Feedback + Threshold"

3. **Transdisciplinary communication**
   - Bridge domains: "Both ant colonies and markets show Self-Organization"
   - Common vocabulary: Avoid domain jargon, use M2 terms

### Combining GenericConcepts

M2 supports **compositional reasoning**:

```
Homeostatic_System = Homeostasis + Feedback + Threshold + Memory
Adaptive_Network = Network + Adaptation + Self-Organization
Regulatory_Process = Process + Regulation + Constraint + Trigger
```

### M2 → M1 Instantiation

To move from M2 (generic) to M1 (domain-specific):

```
M2: Network → M1_Biology: Neural Network
M2: Self-Organization → M1_Physics: Crystal Formation
M2: Regulation → M1_Economics: Market Stabilization
```

**Functor**: F_instantiate(Network, Biology) = Neural_Network

---

## Examples

### Example 1: Thermostat System

**M3 State**: |Ω⟩ = 0.8|A⟩ + 0.7|S⟩ + 0.3|F⟩ + 0.2|I⟩ + 0.2|D⟩

**M2 GenericConcepts**:
- **Homeostasis** (A⊗S⊗F): Maintains temperature
- **Threshold** (A⊗I): Target temperature (20°C)
- **Trigger** (D⊗I): Activates heating/cooling
- **Regulation** (A⊗S⊗F): Control loop

**M1 Domain**: HVAC (Heating, Ventilation, Air Conditioning)

**M0 System**: Specific thermostat model (Nest, Honeywell, etc.)

---

### Example 2: Ecosystem

**M3 State**: |Ω⟩ = 0.6|A⟩ + 0.8|S⟩ + 0.7|F⟩ + 0.9|I⟩ + 0.5|D⟩

**M2 GenericConcepts**:
- **Network** (S⊗I⊗F): Food web
- **Resilience** (A⊗S): Recovery from disturbance
- **Emergence** (I⊗S⊗D): Ecosystem properties
- **Self-Organization** (A⊗I⊗D): Pattern formation
- **Memory** (∫(D-F)dτ): Ecological succession history

**M1 Domain**: Ecology

**M0 System**: Specific ecosystem (Amazon rainforest, coral reef, etc.)

---

### Example 3: Software Architecture

**M3 State**: |Ω⟩ = 0.7|A⟩ + 0.9|S⟩ + 0.6|F⟩ + 0.8|I⟩ + 0.4|D⟩

**M2 GenericConcepts**:
- **Hierarchy** (S⊗A): Layered architecture
- **Modularity** (S⊗I): Independent components
- **Link** (S⊗I): API connections
- **Mediator** (F⊗I⊗S): Message broker
- **Capacity** (S⊗I): System throughput limits
- **Storage** (S⊗F): Database, cache

**M1 Domain**: Software Engineering

**M0 System**: Specific application (e-commerce platform, social network, etc.)

---

## References

### Foundational Works

1. **General Systems Theory**
   - von Bertalanffy, L. (1968). *General System Theory*
   - Laszlo, E. (1972). *Introduction to Systems Philosophy*

2. **Cybernetics**
   - Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*
   - Ashby, W.R. (1956). *An Introduction to Cybernetics*
   - Beer, S. (1972). *Brain of the Firm*

3. **Information Theory**
   - Shannon, C.E. (1948). *A Mathematical Theory of Communication*

4. **Complex Systems**
   - Prigogine, I. (1984). *Order Out of Chaos*
   - Kauffman, S. (1995). *At Home in the Universe*

5. **Category Theory**
   - Mac Lane, S. (1971). *Categories for the Working Mathematician*
   - Spivak, D.I. (2014). *Category Theory for the Sciences*

6. **Epistemology**
   - Korzybski, A. (1933). *Science and Sanity* (Map-Territory Relation)

### TSCG Documentation

- **M3 Genesis Ontology**: Elementary dimensions (A, S, F, I, D)
- **M2 GenericConcepts Ontology**: This document
- **M1 Narrative Extensions**: Domain-specific instantiations (TBD)
- **M0 System Models**: Concrete system descriptions (TBD)

### Related Standards

- **RDF**: Resource Description Framework
- **RDFS**: RDF Schema
- **OWL**: Web Ontology Language
- **Dublin Core**: Metadata terms
- **Linked Data**: Principles for web-scale ontologies

---

## Appendix: Glossary

### Key Terms

- **GenericConcept**: Systemic pattern emerging from M3 tensor products
- **Tensor Product (⊗)**: Mathematical operation combining M3 dimensions
- **Epistemic Gap (ΔΘ)**: Model-reality discrepancy measure
- **Functor**: Structure-preserving map between categories
- **Morphism**: Relationship preserving category structure
- **Ontological Nature**: Model vs Reality characterization (Axis 1)
- **Operational Direction**: Analytical vs Constructive (Axis 2)
- **Granularity Direction**: Composition vs Decomposition (Axis 3)

---

## Version History

### v7.1.0 (2026-01-15)
- Network decomposition complete: 48 GenericConcepts total
- Added Node (Structural, dual): elementary network entity
- Added Relation (Relational, analytical): abstract connection
- Added Path (Structural, dual): sequence through network  
- Added Cluster (Structural, constructive): active processing group
- Added Hub (Structural, dual): passive relay point
- Modified Link: Formula S⊗I→S⊗I⊗F, Nature Dual→Reality, Direction Dual→Constructive
- Structural category: 8→12 GenericConcepts
- Relational category: 4→5 GenericConcepts
- Completion: 96% (48/50)

### v7.0.0 (2026-01-15)
- Complete ontology with 43 GenericConcepts
- Added: Storage, Capacity, Agent, Role, Mediator, Link, Space, Tropism, Signal
- Added: Convergence/Divergence (dual)
- Removed: Resource (replaced by Storage + Capacity)
- Added: Comprehensive README documentation
- Updated: Triple axes framework (added Axis 3: Granularity)

### v6.5.0 (2026-01-15)
- Added: Invariant, Signature, Self-Organization, Synergy, Fusion, Activation
- Removed: Autopoiesis (biology-specific), Catalysis (chemistry-specific)
- Updated: Purity principle enforcement

### v6.4.0 (2026-01-15)
- Added: Event, Threshold, Trigger (Dynamic/Regulatory)
- Added: System, Environment, Observer, Process, State, Substrate, Gradient (Ontological)
- Added: Axis 3 (Granularity Direction)

### v6.3.0 (2026-01-15)
- Added: Code, Coding, Representation, Language (Informational)
- Introduced: Dual polarity for bidirectional GenericConcepts

### v6.0.0 (2026-01-14)
- Foundation: 16 core GenericConcepts
- Established: Dual axes (Model/Reality, Analytical/Constructive)
- Formalized: Binary polarity principle

---

**Document Status**: Complete ✅  
**Validation**: Pending expert review  
**License**: [To be specified]  
**Contact**: TSCG Project - https://github.com/Echopraxium/tscg

---

**END OF README**
