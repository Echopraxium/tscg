# TSCG M2 MetaConcepts Framework

**T**ransdisciplinary **S**ystem **C**onstruction **G**ame - A systemic modeling framework based on a tensor algebra with two vector spaces (Territory ASFID and Map REVOI) and their hybrid couplings.

[![Version](https://img.shields.io/badge/version-15.4.0-blue.svg)](https://github.com/Echopraxium/tscg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [The Map/Territory Double Perspective](#the-maperritory-double-perspective)
- [4-Layer Architecture](#4-layer-architecture)
- [M3 - Genesis Space (The Two Fundamental Spaces)](#m3---genesis-space-the-two-fundamental-spaces)
  - [Territory Space (ASFID) - What Is](#territory-space-asfid---what-is)
  - [Map Space (REVOI) - How We Model It](#map-space-revoi---how-we-model-it)
  - [Hybrid Spaces (Map/Territory Coupling)](#hybrid-spaces-maperritory-coupling)
  - [Coupling Operators Φ and Ψ](#coupling-operators-φ-and-ψ)
- [M2 - MetaConcepts (Systemic Tensors)](#m2---metaconcepts-systemic-tensors)
  - [Notation Conventions](#notation-conventions)
  - [Families Overview](#families-overview)
  - [Dynamic Family](#dynamic-family-processes-transformations)
  - [Structural Family](#structural-family-organization-topology)
  - [Regulatory Family](#regulatory-family-control-stabilization)
  - [Informational Family](#informational-family-data-representation)
  - [Adaptive Family](#adaptive-family-learning-evolution)
  - [Relational Family](#relational-family-interactions)
  - [Energetic Family](#energetic-family-energy-matter)
  - [Ontological Family](#ontological-family-fundamental-entities)
  - [Teleonomic Family](#teleonomic-family-goal-directedness)
  - [Composite Metaconcepts (MetaconceptCombo)](#composite-metaconcepts-metaconceptcombo)
  - [Mathematical Operators](#mathematical-operators)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [SHACL Validation](#shacl-validation)
- [Protégé Export](#protégé-export)
- [Mathematical Formulas](#mathematical-formulas)
- [Tensor Calculus API](#tensor-calculus-api)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## 🔭 Overview

TSCG (Transdisciplinary System Construction Game) is a formal framework for **building and modeling systemic patterns** that transcend disciplines. Designed as a conceptual construction game, it uses a **tensor algebra with two vector spaces** to represent concepts from biology, physics, economics, computer science, and social sciences in a unified way.

### The "Game" in TSCG

TSCG is a **systemic construction game** where:

- 🎲 **M3** are the elementary pieces (ASFID and REVOI base vectors)
- 🧩 **M2** are the reusable patterns (tensor assemblies)
- 🏗️ **M1** are the domain-specific constructions
- 🎮 **M0** are the played games (concrete cases)

### Key Features

- 🧮 **Tensor Algebra**: Each metaconcept is a tensor in either ASFID space, REVOI space, or their hybrid product
- 🔄 **Dual Perspective**: Explicit separation between Territory (what is) and Map (how we model it)
- 📐 **Formal**: Precise mathematical definitions (tensor products, differential operators, SVD decompositions)
- 🌐 **Standardized**: JSON-LD encoding + SHACL validation
- 🔍 **Explorable**: Visualization in Protégé via Turtle export
- 🐍 **Computable**: Python API for tensor manipulations

---

## 🗺️ The Map/Territory Double Perspective

The framework is built on Korzybski's fundamental principle: **"The map is not the territory."** This duality is explicitly encoded in the algebra:

```
┌─────────────────────────────────────────────────────────────┐
│                        REALITY                              │
│  ┌─────────────────┐              ┌─────────────────┐       │
│  │   TERRITORY     │              │      MAP        │       │
│  │   (What Is)     │ ←───Φ/Ψ───→  │  (How We Model) │       │
│  │                 │  coupling    │                 │       │
│  │    ASFID        │    operators │     REVOI       │       │
│  │ 5-dim vectors   │              │  5-dim vectors  │       │
│  └─────────────────┘              └─────────────────┘       │
│           ↑                            ↑                    │
│           │                            │                    │
│      Observable                    Representable            │
│      Phenomena                      Models                  │
└─────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Territory (ASFID)** : The phenomena themselves, independent of observation
2. **Map (REVOI)** : Our models, theories, and representations
3. **Φ/Ψ Operators** : Bidirectional coupling between Territory and Map
4. **Epistemic Gap** : δ = ||P(Reality) - Model|| ∈ [0,1] measures model quality
5. **Hybrid Spaces** : Tensor products ASFID ⊗ REVOI for concepts that bridge both perspectives

---

## 🏗 4-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      M3 - Genesis Space                     │
│  ┌─────────────────┐              ┌─────────────────┐       │
│  │    TERRITORY    │              │      MAP        │       │
│  │    (ASFID)      │              │    (REVOI)      │       │
│  │  A, D, F, I, S  │              │  R, E, V, O, I  │       │
│  │  basis vectors  │              │  basis vectors  │       │
│  └─────────────────┘              └─────────────────┘       │
│           ↑                            ↑                    │
│           └──────────┬─────────────────┘                    │
│                      ↓                                      │
│              ┌───────────────┐                              │
│              │ HYBRID SPACES │                              │
│              │ ASFID ⊗ REVOI │                              │
│              │ (SVD reduced) │                              │
│              └───────────────┘                              │
│           ═══════════════════════════════                   │
│           "The elementary pieces of the game"               │
├─────────────────────────────────────────────────────────────┤
│                      M2 - MetaConcepts                      │
│  ┌─────────────────┐              ┌─────────────────┐       │
│  │  Territory      │              │    Map          │       │
│  │  Tensors        │              │    Tensors      │       │
│  │  (ASFID-based)  │              │  (REVOI-based)  │       │
│  └─────────────────┘              └─────────────────┘       │
│           ↑                            ↑                    │
│           └──────────┬─────────────────┘                    │
│                      ↓                                      │
│              ┌───────────────┐                              │
│              │ HYBRID TENSORS│                              │
│              │ (Metaconcepts │                              │
│              │  that bridge  │                              │
│              │ both worlds)  │                              │
│              └───────────────┘                              │
│           ═══════════════════════════════                   │
│           "The reusable pieces of the game"                 │
├─────────────────────────────────────────────────────────────┤
│                   M1 - Domain Models                        │
│  ┌─────────────────┐              ┌─────────────────┐       │
│  │  Biology        │              │  HTTP           │       │
│  │  Economics      │              │  VSM            │       │
│  │  Physics        │              │  etc.           │       │
│  └─────────────────┘              └─────────────────┘       │
│           ═══════════════════════════════                   │
│           "Domain-specific game rules"                      │
├─────────────────────────────────────────────────────────────┤
│                      M0 - Poclets                           │
│  ┌─────────────────┐              ┌─────────────────┐       │
│  │  RAAS Cascade   │              │  HTTP Request   │       │
│  │  Turing Patterns│              │  VSM System     │       │
│  │  etc.           │              │  etc.           │       │
│  └─────────────────┘              └─────────────────┘       │
│           ═══════════════════════════════                   │
│           "Concrete game moves"                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 M3 - Genesis Space (The Two Fundamental Spaces)

### Territory Space (ASFID) - What Is

The Territory space is a 5-dimensional vector space representing observable phenomena:

| Symbol |  Dimension  | Index | Definition                                  | Analogy         |
|--------|-------------|-------|---------------------------------------------|-----------------|
| **A**  | Attractor   | 0     | Basin of attraction, equilibrium state      | ⚖️ The balance   |
| **D**  | Dynamics    | 1     | Temporal evolution, change                  | ⏱️ The movement |
| **F**  | Flow        | 2     | Transfer of matter, energy, information     | 🌊 The flux     |
| **I**  | Information | 3     | Data, meaning, representation               | 📝 The message  |
| **S**  | Structure   | 4     | Topology, organization, spatial arrangement | 🏛️ The form     |

**Vector representation:**
```json
{
  "@id": "m3:Attractor",
  "@type": "math:BasisVector",
  "math:space": "Territory",
  "math:symbol": "A",
  "math:index": 0,
  "math:coordinates": [1, 0, 0, 0, 0]
}
```

### Map Space (REVOI) - How We Model It

The Map space is a 5-dimensional vector space representing modeling and epistemological dimensions:

| Symbol | Dimension     | Index | Definition                    | Epistemic Role       |
|--------|---------------|-------|-------------------------------|----------------------|
| **R**  | Representable | 0     | Can be represented in a model | 📊 Modelability      |
| **E**  | Explainable   | 1     | Can be explained by theory    | 🔍 Understandability |
| **V**  | Verifiable    | 2     | Can be verified/measured      | ✅ Measurability     |
| **O**  | Observable    | 3     | Can be observed               | 👁️ Observability     |
| **I**  | Interoperable | 4     | Can be shared across models   | 🔄 Shareability      |

**Vector representation:**
```json
{
  "@id": "m3:Representable",
  "@type": "math:BasisVector",
  "math:space": "Map",
  "math:symbol": "R",
  "math:index": 0,
  "math:coordinates": [1, 0, 0, 0, 0]
}
```

### Hybrid Spaces (Map/Territory Coupling)

The full conceptual space is the **tensor product** of Territory and Map spaces:

```
H_full = Territory ⊗ Map = ASFID ⊗ REVOI  (25 dimensions)
```

However, most concepts live in a **reduced 5D space** obtained via SVD:

```
H_reduced = ∑ᵢ σᵢ |uᵢ⟩ ⊗ |vᵢ⟩  (i=1..5)
```

Where:
- |uᵢ⟩ are orthonormal vectors in Territory space (ASFID)
- |vᵢ⟩ are orthonormal vectors in Map space (REVOI)
- σᵢ are singular values (coupling strengths)

**SVD representation:**
```json
{
  "@type": "math:SVD",
  "math:space": "Hybrid",
  "math:components": {
    "singular_values": [0.95, 0.85, 0.72, 0.48, 0.31],
    "left_vectors": ["|u₁⟩ = 0.8A + 0.6D", "..."],
    "right_vectors": ["|v₁⟩ = 0.7R + 0.7E", "..."]
  },
  "math:latex": "\\sum_{i=1}^{5} \\sigma_i |u_i\\rangle \\otimes |v_i\\rangle"
}
```

### Coupling Operators Φ and Ψ

The bidirectional feedback between Territory and Map is formalized by two operators:

- **Φ: Territory → Map** (Observation/Measurement)
- **Ψ: Map → Territory** (Intervention/Prediction)

```
Φ(A) = R    # Observing an attractor makes it representable
Ψ(R) = A'   # A model prediction affects the actual territory
```

The **Alignment Loop** is the process of minimizing:
```
||Φ(Territory) - Map|| + ||Ψ(Map) - Territory||
```

---

## 🧠 M2 - MetaConcepts (Systemic Tensors)

Metaconcepts are **tensors** that can live in:
- **Territory space** (ASFID-based)
- **Map space** (REVOI-based)
- **Hybrid space** (ASFID ⊗ REVOI)

### Notation Conventions

| Notation                    | Meaning                       | Example           |
|-----------------------------|-------------------------------|-------------------|
| D ⊗ I                       | Territory tensor (ASFID only) | Action (D⊗I)      |
| R ⊗ O                       | Map tensor (REVOI only)       | Observation (R⊗O) |
| It → V → O → R → Im         | Hybrid sequence               | ValueSpace        |
| ∑ σᵢ \|uᵢ⟩ ⊗ \|vᵢ⟩            | SVD-reduced hybrid            | KnowledgeField    |
| ⊗⇒_Territory(X) × ⊗⇒_Map(Y) | Hybrid combo                  | Processor         |

### Families Overview

| Family             | Space                | Description                | Count |
|--------------------|----------------------|----------------------------|-------|
| **Dynamic**        | Territory            | Processes, transformations | 14    |
| **Structural**     | Territory            | Organization, topology     | 15    |
| **Regulatory**     | Territory            | Control, stabilization     |  9    |
| **Informational**  | Territory/Map        | Data, representation       |  9    |
| **Adaptive**       | Territory            | Learning, evolution        |  4    |
| **Relational**     | Territory            | Interactions               |  4    |
| **Energetic**      | Territory            | Energy, matter             |  2    |
| **Ontological**    | Territory/Map/Hybrid | Fundamental entities       | 10    |
| **Teleonomic**     | Territory            | Goal-directedness          |  1    |
| **Composite**      | Hybrid               | Metaconcept combinations   |  6    |

---

### 🔄 Dynamic Family (Processes, Transformations)
*Territory space (ASFID)*

| Concept            | Formula                                               | Dimensions  | Rank | Description                       |
|--------------------|-------------------------------------------------------|-------------|------|-----------------------------------|
| **Action**         | D ⊗ I                                                 | [D, I]      |   2  | Atomic triggered operation        |
| **Process**        | D ⊗ F                                                 | [D, F]      |   2  | Temporal sequence                 |
| **Event**          | D ⊗ I                                                 | [D, I]      |   2  | Discrete occurrence               |
| **Trigger**        | D ⊗ I                                                 | [D, I]      |   2  | Initiating stimulus               |
| **Behavior**       | S ⊗ D ⊗ F                                             | [S, D, F]   |   3  | Structured behavioral pattern     |
| **Workflow**       | S ⊗ D ⊗ F                                             | [S, D, F]   |   3  | Prescriptive implementation       |
| **Step**           | S ⊗ I ⊗ D                                             | [S, I, D]   |   3  | Sequential unit                   |
| **Trajectory**     | A ⊗ D ⊗ F                                             | [A, D, F]   |   3  | Observed path                     |
| **Transformation** | D ⊗ S ⊗ I                                             | [D, S, I]   |   3  | Fundamental change                |
| **Cascade**        | S ⊗ I ⊗ A ⊗ D ⊗ F                                     | [S,I,A,D,F] |   5  | Multi-stage process (full tensor) |
| **FeedbackLoop**   | Process ⊗ Alignment ⊗ Homeostasis = A ⊗ S ⊗ F ⊗ I ⊗ D | -           |   -  | Cyclic regulation                 |
| **Bifurcation**    | ∂D/∂F                                                 | -           |   -  | Qualitative change                |
| **Convergence**    | (-1)^p ∇·D                                            | -           |   -  | Convergence/divergence            |
| **Amplification**  | F ⊗ D ⊗ I                                             | [F, D, I]   |   3  | Amplification/attenuation         |
| **Tropism**        | A ⊗ S ⊗ D ⊗ F                                         | [A,S,D,F]   |   4  | Attractor-directed orientation    |
| **Synergy**        | (-1)^p (I ⊗ D)                                        | [I, D]      |   2  | Emergent combined effect          |

---

### 🏗 Structural Family (Organization, Topology)
*Territory space (ASFID)*

| Concept          | Formula     | Dimensions | Rank | Description                     |
|------------------|-------------|------------|------|---------------------------------|
| **Node**         | S ⊗ I       | [S, I]     |   2  | Connection point                |
| **Component**    | S ⊗ I       | [S, I]     |   2  | Constitutive part               |
| **Link**         | S ⊗ I ⊗ F   | [S, I, F]  |   3  | Physical connection             |
| **Network**      | S ⊗ I ⊗ F   | [S, I, F]  |   3  | Set of connected nodes          |
| **Channel**      | S ⊗ I ⊗ F   | [S, I, F]  |   3  | Structured conduit              |
| **Hierarchy**    | S ⊗ A       | [S, A]     |   2  | Organizational levels           |
| **Modularity**   | S ⊗ I       | [S, I]     |   2  | Functional decomposition        |
| **Cluster**      | S ⊗ I ⊗ A   | [S, I, A]  |   3  | Dense grouping                  |
| **Hub**          | S ⊗ F       | [S, F]     |   2  | Redistribution point            |
| **Topology**     | S ⊗ I       | [S, I]     |   2  | Connectivity class              |
| **Symmetry**     | S           | [S]        |   1  | Invariance under transformation |
| **Segmentation** | S ⊗ I ⊗ D   | [S, I, D]  |   3  | Homogeneous partition           |
| **Composition**  | S ⊗ I ⊗ A^p | [S, I, A]  |   3  | Assembly/disassembly            |
| **Fusion**       | S ⊗ D       | [S, D]     |   2  | Union/separation                |
| **Capacity**     | S ⊗ I       | [S, I]     |   2  | Structural limit                |

---

### ⚖️ Regulatory Family (Control, Stabilization)
*Territory space (ASFID)*

| Concept         | Formula        | Dimensions | Rank | Description                  |
|-----------------|----------------|------------|------|------------------------------|
| **Activation**  | (-1)^p (A ⊗ D) | [A, D]     |    2 | Activation/inhibition        |
| **Regulation**  | A ⊗ S ⊗ F      | [A, S, F]  |    3 | Control mechanisms           |
| **Homeostasis** | A ⊗ S ⊗ F      | [A, S, F]  |    3 | Stable state maintenance     |
| **Balance**     | A ⊗ S ⊗ F      | [A, S, F]  |    3 | Static equilibrium           |
| **Constraint**  | S ⊗ I          | [S, I]     |    2 | Restriction                  |
| **Threshold**   | A ⊗ I          | [A, I]     |    2 | Critical value               |
| **Trade-off**   | A ⊗ I ⊗ F      | [A, I, F]  |    3 | Compromise under constraints |
| **Scope**       | S ⊗ I ⊗ A      | [S, I, A]  |    3 | Validity domain              |
| **Polarity**    | S ⊗ I ⊗ A      | [S, I, A]  |    3 | N-ary pole configuration     |

---

### 📊 Informational Family (Data, Representation)
*Territory and Map spaces*

| Concept            | Formula   | Space     | Dimensions | Description             |
|--------------------|-----------|-----------|------------|-------------------------|
| **Code**           | I ⊗ S     | Territory | [I, S]     | Rule system             |
| **Signal**         | I ⊗ F     | Territory | [I, F]     | Information carrier     |
| **Language**       | I ⊗ S ⊗ F | Territory | [I, S, F]  | Communication system    |
| **Pattern**        | S ⊗ I ⊗ A | Territory | [S, I, A]  | Recurring motif         |
| **Signature**      | I ⊗ S     | Territory | [I, S]     | Identifying fingerprint |
| **Representation** | I ⊗ S     | Territory | [I, S]     | Cross-domain mapping    |
| **Coding**         | I ⊗ S ⊗ D | Territory | [I, S, D]  | Encoding/decoding       |
| **Path**           | S ⊗ I ⊗ D | Territory | [S, I, D]  | Planned route (map)     |
| **Observation**    | R ⊗ O     | Map       | [R, O]     | Measurement process     |

---

### 🔄 Adaptive Family (Learning, Evolution)
*Territory space (ASFID)*

| Concept        | Formula   | Dimensions | Rank | Description              |
|----------------|-----------|------------|------|--------------------------|
| **Adaptation** | I ⊗ F ⊗ D | [I, F, D]  |    3 | Progressive modification |
| **Memory**     | ∫(D−F)dτ  | -          |    - | Past state retention     |
| **Emergence**  | I ⊗ S ⊗ D | [I, S, D]  |    3 | Novel properties         |
| **Resilience** | A ⊗ S     | [A, S]     |    2 | Disturbance absorption   |

---

### 🤝 Relational Family (Interactions)
*Territory space (ASFID)*

| Concept      | Formula   | Dimensions | Rank | Description          |
|--------------|-----------|------------|------|----------------------|
| **Relation** | S ⊗ I     | [S, I]     |    2 | Abstract association |
| **Role**     | S ⊗ I     | [S, I]     |    2 | Functional position  |
| **Agent**    | S ⊗ I ⊗ D | [S, I, D]  |    3 | Autonomous entity    |
| **Mediator** | F ⊗ I ⊗ S | [F, I, S]  |    3 | Intermediary         |

---

### ⚡ Energetic Family (Energy, Matter)
*Territory space (ASFID)*

| Concept         | Formula | Dimensions | Rank | Description              |
|-----------------|---------|------------|------|--------------------------|
| **Dissipation** | F ⊗ D   | [F, D]     |    2 | Irreversible degradation |
| **Storage**     | S ⊗ F   | [S, F]     |    2 | Accumulation             |

---

### 🌌 Ontological Family (Fundamental Entities)
*Territory, Map, and Hybrid spaces*

| Concept            | Formula          | Space     | Description                    |
|--------------------|------------------|-----------|--------------------------------|
| **System**         | S ⊗ F            | Territory | Organized set with boundary    |
| **Environment**    | F ⊗ I            | Territory | External context               |
| **Substrate**      | S ⊗ F            | Territory | Material/informational support |
| **Space**          | S ⊗ I            | Territory | Dimensional framework          |
| **State**          | I                | Territory | Instantaneous configuration    |
| **Observer**       | I ⊗ A            | Territory | Measuring entity               |
| **Gradient**       | ⊗₂F or ⊗₂I       | Territory | Differential variation         |
| **Domain**         | ∑ σᵢ \|uᵢ⟩ ⊗ \|vᵢ⟩ | Hybrid    | Knowledge field                |
| **KnowledgeField** | ∑ σᵢ \|uᵢ⟩ ⊗ \|vᵢ⟩ | Hybrid    | Renamed from Domain            |
| **Identity**       | S ⊗ I ⊗ A        | Territory | Distinctive persistence        |
| **Imbrication**    | S ⊗ S            | Territory | Recursive nesting              |

---

### 🎯 Teleonomic Family (Goal-Directedness)
*Territory space (ASFID)*

| Concept               | Formula   | Dimensions | Rank | Description                 |
|-----------------------|-----------|------------|------|-----------------------------|
| **Self-Organization** | A ⊗ I ⊗ D | [A, I, D]  |    3 | Spontaneous order emergence |

---

### 🔧 Composite Metaconcepts (MetaconceptCombo)
*Hybrid and Territory spaces*

| Concept | Parent Formulas | Space | Description |
|---------|-----------------|-------|-------------|
| **Cascade** | Process ⊗ Step ⊗ Trajectory | Territory | Multi-stage process (5D) |
| **Processor** | ⊗⇒_Territory(T, F, R) × ⊗⇒_Map(T, R, I) | Hybrid | Input/output processor |
| **LALI** | ⊗⇒(Amplification, Regulation) \| range(F_A) << range(F_R) | Territory | Local activation, lateral inhibition |
| **ButterflyEffect** | ⊗⇒(Amplification, Trajectory) \| λ > 0 | Territory | Sensitive dependence on initial conditions |
| **VarietyAmplification** | ValueSpace ⊗ Amplification | Hybrid | Variety amplification (VSM S2) |
| **VarietyAttenuation** | ValueSpace ⊗ Amplification | Hybrid | Variety attenuation (VSM S3) |
| **Alignment** | I ⊗ A ⊗ S | Territory | Bidirectional discrepancy reduction |

---

### 🔣 Mathematical Operators

| Operator            | Symbol           | Meaning                  | Example                         |
|---------------------|------------------|--------------------------|---------------------------------|
| Tensor product      | ⊗                | Dimension combination    | D ⊗ I                           |
| Partial derivative  | ∂/∂              | Sensitivity              | ∂D/∂F                           |
| Divergence          | ∇·               | Convergence/divergence   | -∇·D                            |
| Integral            | ∫                | Temporal accumulation    | ∫(D−F)dτ                        |
| Sign polarity       | (-1)^p           | Signed duality           | (-1)^p (A ⊗ D)                  |
| Emergence           | ⊗⇒               | Synergistic combination  | ⊗⇒(Process, Step, Trajectory)   |
| Hybrid product      | ×                | Territory/Map coupling   | ⊗⇒_Territory(...) × ⊗⇒_Map(...) |
| SVD decomposition   | ∑ σᵢ \|uᵢ⟩ ⊗ \|vᵢ⟩ | Dimensional reduction    | ∑ σᵢ \|uᵢ⟩ ⊗ \|vᵢ⟩                |
| Second-order tensor | ⊗₂               | Gradient operator        | ⊗₂F                             |
| Dimension presence  | A^p              | Present/absent dimension | S ⊗ I ⊗ A^p                     |

---

## 💻 Installation

### Prerequisites
- Python 3.8+
- pip
- Git (optional)

### Quick Install

```bash
# Clone the repository (or download files directly)
git clone https://github.com/Echopraxium/tscg.git
cd tscg

# Install dependencies
pip install rdflib pyshacl PyLD numpy sympy graphviz
```

### Dependencies

```txt
rdflib>=6.3.2
pyshacl>=0.20.0
PyLD>=2.0.4
numpy>=1.24.3
sympy>=1.11.1
graphviz>=0.20.1
flask>=2.3.2  # Optional, for API
requests>=2.31.0  # Optional, for API
```

### Verification

```python
from tscg_migration import TSCGPaths
paths = TSCGPaths()
print(paths)
# Should show: Root: /path/to/tscg, Ontology: /path/to/tscg/ontology, etc.
```

---

## 🚀 Usage

### 1. Generate JSON-LD Files

```bash
# Full migration
python tscg_migration.py

# Specific options
python tscg_migration.py --m3-only      # Generate only M3
python tscg_migration.py --m2-only      # Generate only M2
python tscg_migration.py --no-validate  # Skip SHACL validation
```

### 2. Validate the Framework

```bash
# Full validation
python tscg_migration.py --validate-only

# Detailed validation report
python tscg_migration.py --validate --verbose
```

### 3. Export for Protégé

```bash
# Generate Turtle file
python tscg_migration.py --export-protege

# Then open in Protégé:
# File -> Open -> ontology/M2_MetaConcepts.ttl
```

### 4. Generate Documentation

```bash
# Generate README and LaTeX documentation
python tscg_migration.py --generate-docs

# Generate diagrams
python tscg_migration.py --generate-diagrams
```

### 5. Start the Tensor Calculus API

```bash
# Start Flask server
python api.py

# Example request
curl -X POST http://localhost:5000/api/tensor-product \
  -H "Content-Type: application/json" \
  -d '{"metaconcepts": ["Process", "Step", "Trajectory"]}'
```

---

## 📁 File Structure

```
tscg/
├── ontology/
│   ├── M3_GenesisSpace.jsonld      # Fundamental dimensions (ASFID & REVOI)
│   ├── M2_MetaConcepts.jsonld       # Metaconcepts (DEFAULT)
│   ├── M2_MetaConcepts.ttl          # Protégé export
│   └── shacl_shapes.jsonld          # SHACL constraints
├── docs/
│   ├── README.md                     # This file
│   ├── diagrams/                     # Generated diagrams
│   └── latex/                        # LaTeX documentation
├── examples/
│   ├── m0_poclets/                   # Concrete examples
│   │   ├── http_request.jsonld
│   │   ├── baroreceptor.jsonld
│   │   ├── turing_morphogenesis.jsonld
│   │   └── raas_cascade.jsonld
│   └── m1_domains/                   # Domain models
│       ├── biology.jsonld
│       ├── http.jsonld
│       ├── economics.jsonld
│       └── vsm.jsonld
├── tscg_migration.py                 # Migration script
├── api.py                            # Flask API server
└── LICENSE                           # MIT License
```

---

## 🔍 SHACL Validation

The framework includes SHACL constraints to ensure metaconcept consistency.

### Example Constraint

```turtle
m2:MetaConceptShape a sh:NodeShape ;
    sh:targetClass m2:MetaConcept ;
    sh:property [
        sh:path m2:polarity ;
        sh:in ("dual" "neutral" "hybrid" "nary") ;
    ] ;
    sh:property [
        sh:path m2:epistemicGap ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 0.0 ;
        sh:maxInclusive 1.0 ;
    ] ;
    sh:property [
        sh:path math:expression ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] .
```

### Programmatic Validation

```python
from tscg_validate import TSCGValidator

validator = TSCGValidator("ontology/M2_MetaConcepts.jsonld")
conforms, report = validator.validate()

if conforms:
    print("✅ Framework is valid")
else:
    print("❌ Issues detected:")
    print(report)
```

### Validation Rules

| Rule | Description | Action on Failure |
|------|-------------|-------------------|
| **Polarity** | Must be in {dual, neutral, hybrid, nary} | Fix property value |
| **Epistemic Gap** | Between 0 and 1 | Adjust value |
| **Expression** | Must have mathematical formula | Add math:expression |
| **Dimensions** | Factors must be in M3 | Check references |
| **Rank** | Formula-dimension consistency | Recompute tensor |

---

## 🦉 Protégé Export

The `M2_MetaConcepts.ttl` file can be imported directly into Protégé for visual exploration.

### Import Steps

1. **Open Protégé** (version 5.5+ recommended)
2. **File → Open** → select `ontology/M2_MetaConcepts.ttl`
3. **Explore**:
   - **Classes**: Metaconcept hierarchy by family
   - **Individuals**: M3 dimensions (ASFID & REVOI)
   - **Annotations**: Formulas, examples, epistemic gap
4. **Visualize**:
   - **OntoGraf**: Relationships between concepts
   - **DL Query**: Query concepts

### Example DL Query

```
MetaConcept and (hasPolarity value dual)
```

Returns all dual-polarity metaconcepts.

---

## 📐 Mathematical Formulas

Formulas are encoded in JSON-LD with LaTeX support:

```json
{
  "@id": "m2:Action",
  "math:expression": {
    "@type": "math:TensorProduct",
    "math:space": "Territory",
    "math:factors": [
      { "@id": "m3:Dynamics", "math:symbol": "D" },
      { "@id": "m3:Information", "math:symbol": "I" }
    ],
    "math:latex": "D \\otimes I",
    "math:ascii": "D (x) I"
  }
}
```

### Hybrid Formula Example (KnowledgeField)

```json
{
  "@id": "m2:KnowledgeField",
  "math:expression": {
    "@type": "math:SVD",
    "math:space": "Hybrid",
    "math:latex": "\\sum_{i=1}^{5} \\sigma_i |u_i\\rangle \\otimes |v_i\\rangle",
    "math:components": {
      "left_space": "ASFID",
      "right_space": "REVOI",
      "singular_values": [0.92, 0.87, 0.71, 0.45, 0.28]
    }
  }
}
```

### Automatic Conversion

The framework automatically converts formulas to:

- **LaTeX**: `D \otimes I`
- **MathML**: `<math><mi>D</mi><mo>⊗</mo><mi>I</mi></math>`
- **ASCII**: `D (x) I`
- **SymPy**: `TensorProduct(D, I)`
- **Python**: For API calculations

---

## 🐍 Tensor Calculus API

### Start the API Server

```bash
python api.py
# Server running at http://localhost:5000
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tensor-product` | POST | Compute tensor product of metaconcepts |
| `/api/validate` | POST | Validate a formula |
| `/api/decompose` | POST | SVD decomposition of hybrid concept |
| `/api/concepts` | GET | List all metaconcepts |
| `/api/concept/{name}` | GET | Get concept details |

### Example Requests

```python
import requests

# Compute tensor product
response = requests.post(
    "http://localhost:5000/api/tensor-product",
    json={"metaconcepts": ["Process", "Step", "Trajectory"]}
)
print(response.json())

# Validate formula
response = requests.post(
    "http://localhost:5000/api/validate",
    json={"formula": "D ⊗ I", "space": "Territory"}
)
print(response.json())

# SVD decomposition
response = requests.post(
    "http://localhost:5000/api/decompose",
    json={"hybrid_concept": "KnowledgeField"}
)
print(response.json())
```

---

## 🎯 Use Cases

### Biology - RAAS Cascade

```json
{
  "@id": "m0:raas_cascade",
  "@type": "m2:Cascade",
  "m2:space": "Territory",
  "m2:steps": [
    { "m2:step": "Renin secretion", "m2:triggers": "Angiotensinogen → Angiotensin I" },
    { "m2:step": "ACE action", "m2:triggers": "Angiotensin I → Angiotensin II" },
    { "m2:step": "Vasoconstriction", "m2:triggers": "Blood pressure increase" }
  ],
  "math:expression": "S ⊗ I ⊗ A ⊗ D ⊗ F"
}
```

### HTTP Request

```json
{
  "@id": "m0:http_get_example",
  "@type": "m1:HTTPRequest",
  "m2:space": "Territory",
  "m2:process": {
    "@type": "m2:Process",
    "m2:steps": [
      { "@type": "m2:Step", "m2:name": "parse", "m2:triggers": "tokenize" },
      { "@type": "m2:Step", "m2:name": "validate", "m2:triggers": "check_method" }
    ]
  }
}
```

### Economics - Supply/Demand

```json
{
  "@id": "m0:market_equilibrium",
  "@type": "m2:FeedbackLoop",
  "m2:space": "Territory",
  "m2:polarity": "negative",
  "m2:components": {
    "process": "Price adjustment",
    "alignment": "Supply-demand gap",
    "homeostasis": "Equilibrium price"
  }
}
```

### VSM - Variety Management

```json
{
  "@id": "m0:vsm_s2",
  "@type": "m2:VarietyAmplification",
  "m2:space": "Hybrid",
  "m2:components": {
    "valueSpace": {
      "@type": "m2:ValueSpace",
      "it": "operational_states",
      "v": "variety",
      "o": "observable_states",
      "r": "representable_states",
      "im": "interoperable_models"
    },
    "amplification": {
      "@type": "m2:Amplification",
      "direction": "increase"
    }
  }
}
```

---

## 🤝 Contributing

Contributions are welcome!

### Contribution Guidelines

1. **Fork** the repository
2. **Branch** (`git checkout -b feature/new-concept`)
3. **Commit** (`git commit -m 'Add concept X'`)
4. **Push** (`git push origin feature/new-concept`)
5. **Pull Request**

### Rules

- Every new metaconcept must have a tensor formula
- Specify its space (Territory, Map, or Hybrid)
- Include examples from at least 2 domains
- Pass SHACL validation
- Update documentation

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 📚 Citation

If you use TSCG in your research, please cite:

```bibtex
@software{tscg2026,
  author = {Echopraxium and Claude AI},
  title = {TSCG: Transdisciplinary System Construction Game},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/Echopraxium/tscg}
}
```

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/Echopraxium/tscg/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Echopraxium/tscg/discussions)

---

**Version**: 15.4.0  
**Last Updated**: 2026-02-23  
**Status**: Active 🟢