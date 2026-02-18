# M2_MetaConcepts.jsonld

**Version:** 15.3.0 · **Date:** 2026-02-18  
**Author:** Echopraxium with the collaboration of Claude AI  
**Layer:** M2 — Transdisciplinary MetaConcepts  
**Category:** `m3:TransdisciplinaryMetaConcepts`

---

## Overview

`M2_MetaConcepts.jsonld` defines the **transdisciplinary pattern layer** of the TSCG (Transdisciplinary System Construction Game) framework. It contains **76 metaconcepts** — abstract systemic patterns derived as tensor products of M3 basis dimensions (ASFID) that apply universally across scientific disciplines, from biology and physics to economics and computer science.

Each metaconcept is formalized as a tensor formula over the 5 ASFID dimensions:

| Symbol | Dimension | Role |
|--------|-----------|------|
| **A** | Attractor | Stable states, set points, goals |
| **S** | Structure | Spatial/organizational configurations |
| **F** | Flow | Transfers, currents, exchanges |
| **I** | Information | Signals, codes, representations |
| **D** | Dynamics | Temporal evolution, change |

The M2 layer bridges the M3 mathematical foundation (Genesis Space) and the M1 domain-specific ontologies, acting as a universal vocabulary for transdisciplinary analysis.

---

## Architecture

```
M3_GenesisSpace.jsonld  (Mathematical foundation — ASFID ⊕ REVOI)
        ↓  imports
M2_MetaConcepts.jsonld  (Universal patterns — tensor products)
        ↓  instantiates
M1_Biology.jsonld, M1_Chemistry.jsonld, …  (Domain concepts)
        ↓  instantiates
M0_RAAS.jsonld, M0_Yggdrasil.jsonld, …  (Concrete systems — Poclets)
```

### Bicephalous Perspective

Each metaconcept has a dual reading:

- **Eagle Eye (ASFID / Territory):** measures the pattern in the real system
- **Sphinx Eye (REVOI / Map):** constructs a representation of the pattern

The `m2:hasDominantM3` property indicates which ASFID dimensions are primary for each metaconcept.

---

## File Structure

```json
{
  "@context": { "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/", ... },
  "@graph": [
    { "@id": "m2:M2_MetaConcepts",   "@type": "owl:Ontology" },
    { "@id": "m2:MetaConcept",       "@type": "owl:Class" },
    { "@id": "m2:Category",          "@type": "owl:Class" },
    { "@id": "m2:MetaconceptCombo",  "@type": "owl:Class" },
    /* OWL properties (9) */
    /* Category instances (10) */
    /* Metaconcept instances (76) */
  ]
}
```

### `@context` and IRI Resolution

The file uses `@base` to simplify IRIs:

```json
"@context": {
  "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
  "m2": "M2_MetaConcepts.jsonld#",
  "m3": "M3_GenesisSpace.jsonld#"
}
```

So `m2:Homeostasis` resolves to:  
`https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#Homeostasis`

### `owl:imports`

```json
"owl:imports": ["M3_GenesisSpace.jsonld"]
```

---

## OWL Classes

| Class | Description |
|-------|-------------|
| `m2:MetaConcept` | A systemic pattern emerging from tensor product of M3 dimensions. Represents a recognizable organizational or behavioral regularity applicable across multiple knowledge domains. |
| `m2:Category` | Taxonomic grouping of metaconcepts based on dominant M3 dimensions and functional role. |
| `m2:MetaconceptCombo` | A composite metaconcept emerging from the tensor coupling (⊗⇒) of two or more existing metaconcepts. Represents emergent, higher-order patterns. |

---

## OWL Properties

| Property | Type | Description |
|----------|------|-------------|
| `m2:hasCategory` | ObjectProperty | Taxonomic category of the metaconcept |
| `m2:hasTensorFormula` | DatatypeProperty | ASFID tensor formula (e.g., `A⊗S⊗F`) |
| `m2:hasDominantM3` | ObjectProperty | Primary ASFID dimensions driving the pattern |
| `m2:hasEpistemicGap` | DatatypeProperty | Degree of epistemic uncertainty (0.0–1.0) |
| `m2:hasPolarity` | DatatypeProperty | `positive`, `negative`, `neutral`, `dual` |
| `m2:shortName` | DatatypeProperty | Short identifier |
| `m2:fullName` | DatatypeProperty | Full expanded name |
| `m2:dualAspects` | ObjectProperty | Named poles for bipolar metaconcepts |
| `m2:hasExample` | DatatypeProperty | Domain examples illustrating the pattern |

---

## Categories

The 76 metaconcepts are organized into **10 functional categories**:

| Category | Count | Primary ASFID dimensions |
|----------|------:|--------------------------|
| Structural | 19 | S, I, A |
| Dynamic | 15 | D, F |
| Ontological | 12 | S, F, I |
| Regulatory | 9 | A, S, F |
| Informational | 8 | I, S |
| Adaptive | 4 | A, I, D |
| Relational | 5 | S, I, F |
| Energetic | 2 | F, D |
| Compositional | 1 | — |
| Teleonomic | 1 | A, I, D |

---

## Complete Metaconcept Reference

### Adaptive (4)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Resilience | `A⊗S` | Capacity to absorb disturbance and reorganize |
| Adaptation | `I⊗F⊗D` | Structural modification in response to environment |
| Emergence | `I⊗S⊗D` | Properties arising from component interactions |
| Memory | `D⊗F⊗D` | Retention of past states influencing future behavior |

### Compositional (1)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| KnowledgeFieldMetaCombo | `KnowledgeField ⊙ Metaconcept(s)` | Disciplinary specialization of a metaconcept |

### Dynamic (15)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Bifurcation | `∂D/∂F` | Qualitative state change at critical parameter |
| Transformation | `D⊗S⊗I` | Structural change preserving identity |
| Process | `D⊗F` | Temporal sequence of causally connected states |
| Trajectory | `A⊗D⊗F` | Path through state space toward attractor |
| Event | `D⊗I` | Discrete state transition with informational content |
| Synergy | `I⊗D` | Emergent benefit/loss from combination |
| Fusion | `S⊗D` | Merging/splitting of structural entities |
| Convergence | `-∇·D / ∇·D` | Geometric focusing/diverging of trajectories |
| **Cascade** | `⊗⇒(Process, Step, Trajectory)` | **[COMBO]** Chain of triggered processes |
| Behavior | `S⊗D⊗F` | Observable pattern of system actions |
| Tropism | `A⊗S⊗D⊗F` | Directional response to environmental gradient |
| Action | `D⊗I` | Elementary informational state change |
| Amplification | `Ft → D → It → R → O` | Signal gain/attenuation (bicephalous) |
| **Alignment** | `I⊗A⊗S` | Bidirectional iterative reduction of discrepancy |
| **FeedbackLoop** | `Process ⊗ Alignment ⊗ Homeostasis` | **[COMBO]** Cyclic regulatory circuit (see below) |

### Energetic (2)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Dissipation | `F⊗D` | Irreversible energy loss to environment |
| Storage | `S⊗F` | Accumulation and release of energy/matter |

### Informational (8)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Code | `I⊗S` | Mapping between symbol sets |
| Coding | `I⊗S⊗D` | Dynamic encoding/decoding process |
| Representation | `I⊗S` | Static structural mapping A→B |
| Language | `I⊗S⊗F` | Structured communication system |
| Pattern | `S → I → A` | Recognizable regularity enabling prediction |
| Signature | `I⊗S` | Identifying informational fingerprint |
| Signal | `I⊗F` | Information-bearing flow |
| ValueSpace | `It → V → O → R → Im` | Hybrid variety model (bicephalous) |

### Ontological (12)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| System | `S⊗F` | Bounded set of interacting components |
| Environment | `F⊗I` | Surrounding context of a system |
| Observer | `I⊗A` | Entity that measures and models |
| State | `I` | Complete informational description at instant t |
| Substrate | `S⊗F` | Physical/logical support medium |
| Gradient | `⊗₂F or ⊗₂I` | Spatial differential driving flow |
| Space | `S⊗I` | Abstract or physical extent |
| Imbrication | `S → S` | Nested hierarchical containment |
| Domain | `∑ᵢ σᵢ \|uᵢ⟩⊗\|vᵢ⟩` | Hybrid 5D SVD (ASFID ↔ REVOI) |
| MetaconceptCombo | `⊗ᵢ₌₁ⁿ Mᵢ ⇒ M_result` | Generic emergent combination pattern |
| **Processor** | `⊗⇒_T(Transf., Flow, Resource) × ⊗⇒_M(Transf., Repr., Interop.)` | **[COMBO]** Bicephalous transformation unit |
| KnowledgeField | `∑ᵢ σᵢ \|uᵢ⟩⊗\|vᵢ⟩` | Scientific/technical discipline (ASFID ⊗ REVOI) |

### Regulatory (9)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Homeostasis | `A⊗S⊗F` | Maintenance of stable internal state |
| Regulation | `A⊗S⊗F` | Active control toward target state |
| Constraint | `S⊗I` | Boundary limiting degrees of freedom |
| Scope | `S → I → A → R` | Defined domain of applicability |
| Threshold | `A⊗I` | Critical value triggering state change |
| Trigger | `D⊗I` | Event initiating a process |
| Activation | `A⊗D` | Enabling/inhibiting a process |
| Balance | `A⊗S⊗F` | Static equilibrium between forces |
| Trade-off | `A⊗I⊗F⊗A⊗A` | Constrained optimization between objectives |

### Relational (5)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Agent | `S⊗I⊗D` | Autonomous entity with goals and actions |
| Role | `S⊗I` | Functional position within a system |
| Mediator | `F⊗I⊗S` | Entity facilitating interaction between others |
| Link | `S⊗I⊗F` | Structural connection enabling flow |
| Relation | `S⊗I` | Abstract connection between entities |

### Structural (19)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Hierarchy | `S⊗A` | Ordered levels of authority/abstraction |
| Network | `S⊗I⊗F` | Graph of interconnected nodes |
| Symmetry | `S` | Invariance under transformation |
| Modularity | `S⊗I` | Decomposability into self-contained units |
| Topology | `S⊗I` | Shape properties invariant under deformation |
| Segmentation | `S⊗I⊗D` | Division into functionally distinct regions |
| Invariant | `S⊗A` | Property preserved under transformation |
| Capacity | `S⊗I` | Maximum throughput or storage |
| Node | `S⊗I` | Discrete junction point in a network |
| Path | `S⊗I⊗D` | Ordered sequence of connected nodes |
| Channel | `S⊗I⊗F` | Directed conduit for flow |
| Cluster | `S⊗I⊗A` | Densely connected subgraph |
| Component | `S⊗I` | Functionally identifiable sub-unit |
| Hub | `S⊗F` | High-connectivity central node |
| Composition | `S⊗I⊗A / S⊗I` | Assembly/disassembly of components |
| Polarity | `S⊗I⊗A` | N-ary opposition between defined poles |
| Identity | `S → I → A → V → E` | Persistent individuation across transformations |
| Workflow | `S⊗D⊗F` | Structured sequence of operational steps |
| Step | `S⊗I⊗D` | Elementary unit in a process or workflow |

### Teleonomic (1)

| Metaconcept | Formula | Notes |
|-------------|---------|-------|
| Self-Organization | `A⊗I⊗D` | Spontaneous emergence of ordered structure without external control |

---

## MetaconceptCombos

A `MetaconceptCombo` is a composite pattern emerging from tensor coupling (⊗⇒) of existing metaconcepts. It is typed both as `m2:MetaConcept` and `m2:MetaconceptCombo`.

### Cascade
```
Cascade = ⊗⇒(Process, Step, Trajectory)
```
A sequence of processes where each step triggers the next, propagating through a system.

### Processor
```
Processor = ⊗⇒_Territory(Transformation, Flow, Resource)
          × ⊗⇒_Map(Transformation, Representation, Interoperability)
```
A bicephalous transformation unit combining Territory-side processing (what the system does) with Map-side representation (how it is modeled). Bridges Eagle Eye and Sphinx Eye perspectives.

### FeedbackLoop *(v15.3.0)*
```
FeedbackLoop = Process ⊗ Alignment ⊗ Homeostasis
             = (D⊗F) ⊗ (I⊗A⊗S) ⊗ (A⊗S⊗F)
             = A⊗S⊗F⊗I⊗D  (full ASFID coverage)
```
A cyclic regulatory circuit encompassing the complete system phenomenology (all 5 ASFID dimensions):

| Component | Formula | Contribution |
|-----------|---------|-------------|
| Process | `D⊗F` | Temporal unfolding — sense→compare→act cycle |
| Alignment | `I⊗A⊗S` | Error detection and reduction toward set point |
| Homeostasis | `A⊗S⊗F` | Regulatory target — stable internal state |

**Dual polarity:**
- **Negative feedback** (stabilizing): output opposes deviation. Examples: thermostat, insulin-glucose, PID controller.
- **Positive feedback** (amplifying): output reinforces deviation. Examples: oxytocin in labor, blood clotting cascade, compound interest.

> **Architectural note:** `m2:FeedbackLoop` models systemic regulatory circuits across all domains. It is distinct from `m3:AlignmentLoop` (M3_GenesisSpace), which is the *epistemological* Territory↔Map alignment mechanism intrinsic to TSCG using operators Φ and Ψ.

---

## Notable Metaconcepts

### Alignment *(v15.3.0)*

```
Alignment = I⊗A⊗S   (Information ⊗ Attractor ⊗ Structure)
```

A bidirectional dynamic process progressively reducing mutual discrepancy toward coherent correspondence. Distinct from:

| Concept | Distinction |
|---------|------------|
| Representation | Static structural mapping A→B; Alignment is iterative bidirectional A↔B |
| Balance | Static equilibrium state; Alignment is an active process |
| Convergence | Geometric focusing of trajectories; Alignment is structural/semantic reconciliation |

Examples: DNA sequence alignment, wheel alignment, AI alignment, organizational strategic alignment, Territory↔Map alignment via Φ/Ψ.

### Domain

```
Domain = ∑ᵢ σᵢ |uᵢ⟩⊗|vᵢ⟩    (5D SVD, ASFID ↔ REVOI)
```

A knowledge field formalized as a hybrid tensor product of Territory (ASFID) and Map (REVOI) spaces via Singular Value Decomposition. The σᵢ values encode coupling strength between the two perspectives.

### ValueSpace

```
ValueSpace = It → V → O → R → Im
```

A hybrid variety model encoding the information-theoretic capacity of a system's state space, bridging Territory measurement (It, V, O) and Map construction (R, Im).

---

## Usage in the TSCG Hierarchy

### Referencing a Metaconcept in M1

In a domain ontology (e.g., `M1_Biology.jsonld`):

```json
{
  "@id": "m1bio:FeedbackLoop",
  "@type": ["owl:NamedIndividual", "m2:FeedbackLoop"],
  "m2:hasTensorFormula": "m2:Process ⊗ m2:Alignment ⊗ m2:Homeostasis",
  "rdfs:comment": "Biological regulatory circuit (sensor→integrator→effector)"
}
```

### Referencing a Metaconcept in M0

In a poclet (e.g., `M0_RAAS.jsonld`):

```json
{
  "@id": "m0raas:BloodPressureRegulation",
  "@type": ["owl:NamedIndividual", "m1bio:FeedbackLoop"],
  "rdfs:comment": "RAAS negative feedback loop maintaining blood pressure homeostasis"
}
```

---

## Dependencies and Imports

```
M2_MetaConcepts.jsonld
  └── imports: M3_GenesisSpace.jsonld
        └── defines: ASFID dimensions, REVOI dimensions, m3:AlignmentLoop
```

The `@base` URI ensures all relative IRIs resolve correctly:

```
@base: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
```

---

## Changelog (recent)

| Version | Date | Summary |
|---------|------|---------|
| **v15.3.0** | 2026-02-18 | NEW: `m2:Alignment` (I⊗A⊗S), `m2:FeedbackLoop` (MetaconceptCombo). Total: 74→76. |
| v15.2.0 | 2026-02-17 | IRI refactoring: `@base` added, simplified prefix notation. |
| v15.1.0 | 2026-02-10 | Bidirectional operators Φ/Ψ formalized for Territory↔Map feedback. |
| v14.5.0 | — | @context cleanup, REVOI naming aligned to v3.0.0 standard (-ability→-able). |
| v14.4.0 | — | Phase 4 ValueSpace attributes complete: 13 attributes, 72 discrete values. |
| v14.3.x | — | Systematic enrichment: Bifurcation, Symmetry, Threshold, Network, Signal, Gradient attributes. |
| v14.4.0 | — | MetaconceptCombo formalized; `Cascade` and `Processor` added. |

---

## Related Files

| File | Layer | Role |
|------|-------|------|
| `M3_GenesisSpace.jsonld` | M3 | Mathematical foundation — ASFID ⊕ REVOI Hilbert space |
| `M3_EagleEye.jsonld` | M3 | ASFID dimension definitions (Territory measurement) |
| `M3_SphinxEye.jsonld` | M3 | REVOI dimension definitions (Map construction) |
| `M1_Biology.jsonld` | M1 | Domain instantiation — biological concepts |
| `M1_Chemistry.jsonld` | M1 | Domain instantiation — chemical concepts |
| `M0_RAAS.jsonld` | M0 | Poclet — Renin-Angiotensin-Aldosterone System |
| `M0_Yggdrasil.jsonld` | M0 | Poclet — World Tree mythological system |

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
