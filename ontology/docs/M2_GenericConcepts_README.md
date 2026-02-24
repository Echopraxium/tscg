# M2_GenericConcepts.jsonld

**Version:** 15.7.0 · **Date:** 2026-02-24  
**Author:** Echopraxium with the collaboration of Claude AI  
**Layer:** M2 — Transdisciplinary GenericConcepts  
**Category:** `m2:GenericConcept`

---

## Overview

`M2_GenericConcepts.jsonld` defines the **transdisciplinary pattern layer** of the TSCG (Transdisciplinary System Construction Game) framework. It contains **74 GenericConcepts** — abstract systemic patterns derived as tensor products of M3 basis dimensions (ASFID/REVOI) that apply universally across scientific disciplines, from biology and physics to economics and computer science.

Each GenericConcept is formalized as a tensor formula over the ASFID and/or REVOI dimensions:

**Eagle Eye — ASFID (Territory measurement)**

| Symbol | Dimension | Role |
|--------|-----------|------|
| **A** | Attractor | Stable states, set points, goals |
| **S** | Structure | Spatial/organizational configurations |
| **F** | Flow | Transfers, currents, exchanges |
| **I** | Information | Signals, codes, representations |
| **D** | Dynamics | Temporal evolution, change |

**Sphinx Eye — REVOI (Map construction)**

| Symbol | Dimension | Role |
|--------|-----------|------|
| **R** | Representability | Semantic encodability/decodability |
| **E** | Evolvability | Capacity to adapt to new formats |
| **V** | Verifiability | Testability of interface contracts |
| **O** | Observability | Accessibility to an Observer |
| **I** | Interoperability | Cross-system compatibility |

> **Note on ⊗ semantics:** In TSCG, `⊗` between dimensions is a **lattice join (⊔)**, not a Kronecker tensor product. Shared dimensions between parents contract: `F ⊔ F = F`. The compiled formula of a GenericConceptCombo is the union of unique dimensions across all parents. Exception: `⊗₂F` denotes a *structural* repetition (e.g. Gradient = differential between two distinct F states) — not duplication.

The M2 layer bridges the M3 mathematical foundation (Genesis Space) and the M1 KnowledgeField-specific ontologies.

---

## Architecture

```
M3_GenesisSpace.jsonld     (Mathematical foundation — ASFID ⊕ REVOI)
        ↓  imports
M2_GenericConcepts.jsonld  (Universal patterns — pure transdisciplinary)
        ↓  characterizedBy
M1_CoreConcepts.jsonld     (KnowledgeFieldConcept, KnowledgeField, KnowledgeFieldGenericCombo)
M1_Biology.jsonld, M1_Chemistry.jsonld, …  (KnowledgeField-specific concepts)
        ↓  instantiates
M0_RAAS.jsonld, M0_Yggdrasil.jsonld, …    (Concrete systems — Poclets)
```

### M2 Purity Principle

M2 contains **only universally transdisciplinary GenericConcepts** — patterns valid across ALL knowledge fields without exception. Epistemological meta-concepts (`KnowledgeField`, `KnowledgeFieldConcept`, `KnowledgeFieldGenericCombo`) are defined in `M1_CoreConcepts.jsonld`, not in M2.

### Bicephalous Perspective

Each GenericConcept has a dual reading:

- **Eagle Eye (ASFID / Territory):** measures the pattern in the real system
- **Sphinx Eye (REVOI / Map):** constructs a representation of the pattern

The `m2:eagleView` and `m2:sphinxView` properties encode both perspectives. `m2:hasDominantM3` indicates the primary ASFID dimensions.

---

## File Structure

```json
{
  "@context": { "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/", ... },
  "@graph": [
    { "@id": "m2:M2_GenericConcepts",    "@type": "owl:Ontology" },
    { "@id": "m2:GenericConcept",        "@type": "owl:Class" },
    { "@id": "m2:GenericConceptFamily",  "@type": "owl:Class" },
    { "@id": "m2:GenericConceptCombo",   "@type": "owl:Class" },
    { "@id": "m2:ConceptContract",       "@type": "owl:Class" },
    /* OWL properties (28) */
    /* GenericConceptFamily instances (10) */
    /* ConceptContract instances (4) */
    /* GenericConcept instances (74) */
  ]
}
```

### IRI Resolution

```json
"@context": {
  "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
  "m2": "M2_GenericConcepts.jsonld#",
  "m3": "M3_GenesisSpace.jsonld#"
}
```

`m2:Homeostasis` resolves to:  
`https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#Homeostasis`

---

## OWL Classes

| Class | Description |
|-------|-------------|
| `m2:GenericConcept` | A universally transdisciplinary systemic pattern. Applicable across ALL knowledge fields. |
| `m2:GenericConceptFamily` | Taxonomic grouping by dominant dimensions and functional role. 10 families. |
| `m2:GenericConceptCombo` | GenericConcept produced by synergistic N-ary combination (⊗ⁿ⇒). `rdfs:subClassOf m2:GenericConcept`. |
| `m2:GenericConceptPair` | Structural dual pair of GenericConcepts. |
| `m2:ConceptContract` | Abstract behavioral specification (analogous to OOP interface). No tensor formula. |
| `m2:Triggerable` | ConceptContract: can be initiated by an external `m2:Trigger`. |
| `m2:Observable` | ConceptContract: can be measured by an `m2:Observer` in Territory. |
| `m2:Composable` | ConceptContract: can serve as structural building block in a larger assembly. |
| `m2:Stateful` | ConceptContract: maintains persistent internal state across interactions. |

---

## OWL Properties

### Core GenericConcept properties

| Property | Type | Description |
|----------|------|-------------|
| `m2:hasFamily` | ObjectProperty | GenericConceptFamily of this concept |
| `m2:hasTensorFormula` | DatatypeProperty | ASFID/REVOI tensor formula (Unicode) |
| `m2:hasTensorFormulaTeX` | DatatypeProperty | LaTeX encoding |
| `m2:hasTensorFormulaASCII` | DatatypeProperty | ASCII fallback |
| `m2:hasDominantM3` | ObjectProperty | Primary ASFID dimensions |
| `m2:hasEpistemicGap` | DatatypeProperty | Epistemic uncertainty (0.0–1.0) |
| `m2:hasPolarity` | DatatypeProperty | `neutral`, `dual`, `ternary`, `N-ary` |
| `m2:hasExample` | DatatypeProperty | Domain examples |
| `m2:eagleView` | ObjectProperty | Territory-side (ASFID) specification |
| `m2:sphinxView` | ObjectProperty | Map-side (REVOI) specification |
| `m2:dualCounterpart` | ObjectProperty | Structural dual of this concept |

### Relational properties

| Property | Type | Description |
|----------|------|-------------|
| `m2:triggeredBy` | ObjectProperty | Stimulus that initiates this Triggerable |
| `m2:triggers` | ObjectProperty | Inverse of `triggeredBy` |
| `m2:componentOf` | ObjectProperty | This Composable is part of a larger structure |
| `m2:decomposedInto` | ObjectProperty | Inverse of `componentOf` |
| `m2:implementsProcess` | ObjectProperty | Links structural container to its Process |
| `m2:hasGradient` | ObjectProperty | Associates concept with driving Gradient |

### GenericConceptCombo properties

| Property | Type | Description |
|----------|------|-------------|
| `m2:hasComboComponent` | ObjectProperty | Parent GenericConcept in a Combo |
| `m2:comboRole` | DatatypeProperty | Role of a component: `core_mechanism`, `medium`, `material`, `path`… |

### ConceptContract property

| Property | Type | Description |
|----------|------|-------------|
| `m2:implements` | AnnotationProperty | Explicit declaration of ConceptContract implementation (complements `rdfs:subClassOf` mixin) |

### M1 bridge property

| Property | Type | Description |
|----------|------|-------------|
| `m2:characterizedBy` | ObjectProperty | Associates a M1 KnowledgeFieldConcept with its M2 GenericConcept basis. Replaces former heterogeneous `m2Basis` fields. |

---

## GenericConcept Families

The 74 GenericConcepts are organized into **10 families**:

| Family | Count | Primary dimensions | Representative members |
|--------|------:|-------------------|----------------------|
| Structural | 19 | S, I | Hierarchy, Network, Component, Node, Workflow, Interoperability |
| Dynamic | 13 | D, F | Process, Event, Behavior, Transformation, FeedbackLoop |
| Ontological | 9 | S, F, I | System, State, Observer, Resource, Gradient |
| Regulatory | 9 | A, S, F | Homeostasis, Regulation, Threshold, Trigger |
| Informational | 8 | I, S | Code, Representation, Signal, ValueSpace |
| Relational | 5 | S, I, F | Agent, Mediator, Link, Relation |
| Adaptive | 4 | A, I, D | Resilience, Adaptation, Emergence, Memory |
| **Combo** | **5** | **— (compiled)** | **GenericConceptCombo, Cascade, Processor, LALI, ButterflyEffect** |
| Energetic | 2 | F, D | Dissipation, Storage |
| Teleonomic | 1 | A, I, D | Self-Organization |

---

## ConceptContract System

ConceptContracts are behavioral specifications **orthogonal** to families. A GenericConcept implements a contract via **mixin** `rdfs:subClassOf` (OWL-inferable) + `m2:implements` annotation (human-readable):

```json
{
  "@id": "m2:Event",
  "rdfs:subClassOf": ["m2:GenericConcept", "m2:Triggerable"],
  "m2:implements": { "@id": "m2:Triggerable" }
}
```

| ConceptContract | Implementors |
|----------------|-------------|
| `m2:Triggerable` | Event, Action, Process, Cascade, Transformation |
| `m2:Observable` | State, Trajectory, Behavior, Gradient, Observer |
| `m2:Composable` | Component, Node, Step |
| `m2:Stateful` | Memory, Storage, Homeostasis, State |

> `m2:State` implements both `Observable` and `Stateful`.  
> `m2:Cascade` has `rdfs:subClassOf: [m2:GenericConceptCombo, m2:Triggerable]`.

---

## Complete GenericConcept Reference

### Adaptive (4)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Resilience | `A ⊗ S` | — |
| Adaptation | `I ⊗ F ⊗ D` | — |
| Emergence | `I ⊗ S ⊗ D` | — |
| Memory | `∫(D−F)dτ` | Stateful |

### Combo (5)

| GenericConcept | Formula | Notes |
|----------------|---------|-------|
| GenericConceptCombo | `⊗ᵢ₌₁ⁿ Mᵢ ⇒ M_result` | Abstract N-ary combination pattern |
| Cascade | `⊗⇒(Process, Step, Trajectory)` | Triggerable |
| Processor | `S ⊗ I ⊗ D ⊗ F ⊗ V ⊗ R` | Bicephalous, compiled formula |
| LocalActivationLateralInhibition | `⊗⇒(Amplification, Regulation) \| range(F_A) << range(F_R)` | Turing pattern |
| ButterflyEffect | `⊗⇒(Amplification, Trajectory) \| λ > 0` | Chaotic amplification |

### Dynamic (13)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Bifurcation | `∂D/∂F` | — |
| Transformation | `D ⊗ S ⊗ I` | Triggerable |
| Process | `D ⊗ F` | Triggerable |
| Trajectory | `A ⊗ D ⊗ F` | Observable |
| Event | `D ⊗ I` | Triggerable |
| Synergy | `I ⊗ D` | — |
| Fusion | `S ⊗ D` | — |
| Convergence | `-∇·D / ∇·D` | — |
| Behavior | `S ⊗ D ⊗ F` | Observable |
| Action | `D ⊗ I` | Triggerable |
| Amplification | `Ft → D → It → R → O` | — |
| Alignment | `I ⊗ A ⊗ S` | — |
| FeedbackLoop | `⊗⇒(Process, Alignment, Homeostasis)` | — |

### Energetic (2)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Dissipation | `F ⊗ D` | — |
| Storage | `S ⊗ F` | Stateful |

### Informational (8)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Code | `I ⊗ S` | — |
| Coding | `I ⊗ S ⊗ D` | — |
| Representation | `I ⊗ S` | — |
| Language | `I ⊗ S ⊗ F` | — |
| Pattern | `S → I → A` | — |
| Signature | `I ⊗ S` | — |
| Signal | `I ⊗ F` | — |
| ValueSpace | `It → V → O → R → Im` | — |

### Ontological (9)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| System | `S ⊗ F` | — |
| Environment | `F ⊗ I` | — |
| Observer | `I ⊗ A` | Observable |
| State | `I` | Observable, Stateful |
| Substrate | `S ⊗ F` | — |
| Gradient | `⊗₂F or ⊗₂I` | Observable |
| Space | `S ⊗ I` | — |
| Imbrication | `S → S` | — |
| **Resource** *(new)* | `F ⊗ I ⊗ R` | — |

### Regulatory (9)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Homeostasis | `A ⊗ S ⊗ F` | Stateful |
| Regulation | `A ⊗ S ⊗ F` | — |
| Constraint | `S ⊗ I` | — |
| Scope | `S → I → A → R` | — |
| Threshold | `A ⊗ I` | — |
| Trigger | `D ⊗ I` | — |
| Activation | `A ⊗ D` | — |
| Balance | `A ⊗ S ⊗ F` | — |
| Trade-off | `A ⊗ I ⊗ F ⊗ A ⊗ A` | — |

### Relational (5)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Agent | `S ⊗ I ⊗ D` | — |
| Role | `S ⊗ I` | — |
| Mediator | `F ⊗ I ⊗ S` | — |
| Link | `S ⊗ I ⊗ F` | — |
| Relation | `S ⊗ I` | — |

### Structural (19)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Hierarchy | `S ⊗ A` | — |
| Network | `S ⊗ I ⊗ F` | — |
| Symmetry | `S` | — |
| Modularity | `S ⊗ I` | — |
| Topology | `S ⊗ I` | — |
| Segmentation | `S ⊗ I ⊗ D` | — |
| Invariant | `S ⊗ A` | — |
| Capacity | `S ⊗ I` | — |
| Node | `S ⊗ I` | Composable |
| Path | `S ⊗ I ⊗ D` | — |
| Channel | `S ⊗ I ⊗ F` | — |
| Cluster | `S ⊗ I ⊗ A` | — |
| Component | `S ⊗ I` | Composable |
| Hub | `S ⊗ F` | — |
| Composition | `S ⊗ I ⊗ A` | — |
| Polarity | `S ⊗ I ⊗ A` | — |
| Identity | `S → I → A → V → E` | — |
| Workflow | `S ⊗ D ⊗ F` | — |
| Step | `S ⊗ I ⊗ D` | Composable |
| **Interoperability** *(new)* | `S ⊗ I ⊗ F ⊗ V ⊗ E` | — |

### Teleonomic (1)

| GenericConcept | Formula | ConceptContract |
|----------------|---------|----------------|
| Self-Organization | `A ⊗ I ⊗ D` | — |

---

## M1 Integration

### KnowledgeField concepts (defined in M1_CoreConcepts.jsonld)

| Concept | Role |
|---------|------|
| `m1:core:KnowledgeField` | Epistemological meta-concept organizing M1. SVD formula: `∑ᵢ σᵢ |uᵢ⟩ ⊗ |vᵢ⟩` |
| `m1:core:KnowledgeFieldConcept` | Abstract class for all M1 concepts (formerly DomainConcept) |
| `m1:core:KnowledgeFieldGenericCombo` | Disciplinary qualification: `KnowledgeField ⊙ GenericConcept(s)` |

### Referencing a GenericConcept in M1

```json
{
  "@id": "m1:biology:CellularCommunication",
  "@type": "owl:Class",
  "rdfs:subClassOf": "m2:GenericConcept",
  "m2:characterizedBy": [
    { "@id": "m2:Signal" },
    { "@id": "m2:Channel" }
  ]
}
```

### Referencing in M0 (Poclets)

```json
{
  "@id": "m0raas:BloodPressureRegulation",
  "@type": ["owl:NamedIndividual", "m1:biology:FeedbackLoop"],
  "rdfs:comment": "RAAS negative feedback loop maintaining blood pressure homeostasis"
}
```

---

## Changelog (recent)

| Version | Date | Summary |
|---------|------|---------|
| **v15.7.0** | 2026-02-24 | NEW: ConceptContract system — `m2:ConceptContract` (abstract), 4 contracts: Triggerable, Observable, Composable, Stateful. 16 GenericConcepts updated with mixin + `m2:implements`. |
| **v15.6.1** | 2026-02-24 | RENAME: `M2_MetaConcepts` → `M2_GenericConcepts`. 132 terminology replacements (`metaconcept` → `genericConcept`). Preserved biological real words. |
| **v15.6.0** | 2026-02-24 | M2 purification: removed `m2:Domain`, `m2:KnowledgeField`, `m2:KnowledgeFieldGenericCombo` (moved to M1). New 10th family `m2:Combo`. Declared `m2:characterizedBy`. |
| **v15.5.3** | 2026-02-24 | Created `m2:Resource` (Ontological, `F⊗I⊗R`), `m2:Interoperability` (Structural, `S⊗I⊗F⊗V⊗E`). Corrected `m2:Flow` → `m3:eagle_eye:Flow` in Processor. |
| **v15.5.2** | 2026-02-24 | Renamed MetaconceptCombo → GenericConceptCombo. Added `m2:hasComboComponent`, `m2:comboRole`. Updated Processor, Cascade, LALI, ButterflyEffect with explicit components and compiled formulas. |
| **v15.5.0–15.5.1** | 2026-02-24 | OWL architecture migration: NamedIndividuals → `owl:Class` hierarchy. `m2:MetaConcept` → `m2:GenericConcept`. 15 missing properties declared. |
| v15.3.0 | 2026-02-18 | NEW: `m2:Alignment` (`I⊗A⊗S`), `m2:FeedbackLoop` (GenericConceptCombo). |

---

## Related Files

| File | Layer | Role |
|------|-------|------|
| `M3_GenesisSpace.jsonld` | M3 | Mathematical foundation — ASFID ⊕ REVOI |
| `M3_EagleEye.jsonld` | M3 | ASFID dimension definitions |
| `M3_SphinxEye.jsonld` | M3 | REVOI dimension definitions |
| `M1_CoreConcepts.jsonld` | M1 | KnowledgeFieldConcept, KnowledgeField, KnowledgeFieldGenericCombo |
| `M1_Biology.jsonld` | M1 | Biological KnowledgeField concepts |
| `M1_Chemistry.jsonld` | M1 | Chemical KnowledgeField concepts |
| `M1_Optics.jsonld` | M1 | Optical KnowledgeField concepts |
| `M1_Photography.jsonld` | M1 | Photography KnowledgeField concepts |
| `M1_Mythology.jsonld` | M1 | Mythological KnowledgeField concepts |
| `M0_RAAS.jsonld` | M0 | Poclet — Renin-Angiotensin-Aldosterone System |
| `M0_Yggdrasil.jsonld` | M0 | Poclet — World Tree mythological system |

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
