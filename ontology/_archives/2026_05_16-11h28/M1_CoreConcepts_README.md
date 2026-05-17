# M1_CoreConcepts.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 1.0.0
**Date**: 2026-05-14
**Layer**: M1 — Domain-Neutral Core Concepts
**Status**: Active

---

## Overview

`M1_CoreConcepts.jsonld` is the **foundational M1 ontology** that defines core
transdisciplinary concept types shared across all knowledge domains. It sits
between M2 (GenericConcepts) and the domain-specific M1 extensions (biology,
physics, etc.).

This file declares abstract concept categories that serve as organizing
principles for domain-specific knowledge, without being tied to any particular
field of study.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld  ─┐
M3_EagleEye.jsonld           ─┤→  M3_GenesisGrammar.jsonld
M3_SphinxEye.jsonld          ─┘           ↓ imported by
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
**Imported by**: Domain-specific M1 extensions (biology, physics, chemistry...)

---

## Core Concept Categories

M1_CoreConcepts defines 16 abstract concept classes that organize domain
knowledge:

### **1. CoreConcept** (Base Class)

Abstract superclass for all M1-level concepts. Serves as the common ancestor
for domain-specific concepts across all knowledge fields.

### **2. GenericMechanism**

Represents transdisciplinary operational principles — "how things work" patterns
that apply across domains.

**Examples:**
- Feedback loops (biology, engineering, economics)
- Resonance (physics, psychology, social systems)
- Catalysis (chemistry, social change, cognitive processes)

### **3. StructuralTemplate**

Represents organizational patterns and architectural blueprints that recur
across different systems.

**Examples:**
- Hierarchical structures (biology, organizations, information systems)
- Network topologies (neural, social, computational)
- Modular architectures (software, organisms, ecosystems)

### **4. ProcessArchetype**

Represents canonical process patterns — temporal sequences that exhibit similar
dynamics across domains.

**Examples:**
- Growth curves (biological, economic, technological)
- Decay patterns (radioactive, institutional, memory)
- Transformation sequences (metamorphosis, phase transitions, paradigm shifts)

### **5. RelationalPattern**

Represents fundamental relationship types that structure interactions between
entities.

**Examples:**
- Competition/cooperation (ecology, economics, game theory)
- Mutualism/parasitism (biology, social systems, information ecology)
- Dependency/autonomy (development, systems, organizations)

### **6. DomainPattern**

Represents field-specific conceptual patterns that don't fit other categories
but require formal representation.

**Examples:**
- Domain-specific heuristics
- Field-specific methodologies
- Discipline-native abstractions

### **7-16. Additional Core Categories**

The ontology includes additional abstract categories for organizing:
- Measurement patterns
- Transformation types
- Constraint patterns
- Emergence types
- Adaptation mechanisms
- Information patterns

(Full list available in the `.jsonld` file)

---

## Role in TSCG Architecture

### **Bridging Layer**

M1_CoreConcepts acts as a **conceptual bridge**:

```
M2 GenericConcepts     →  transdisciplinary named types (Process, Homeostasis)
         ↓
M1 CoreConcepts        →  organizational categories (Mechanism, Template)
         ↓
M1 Domain Extensions   →  domain-specific instances (DNA_Replication, Diffusion)
         ↓
M0 Instances           →  concrete systems (E_coli_metabolism, Uranium_235_decay)
```

### **Type System Position**

In the TSCG type system hierarchy:

```
𝕋₀  Primitive Types      M3   {A, S, F, I, D, R, E, V, O, I}
𝕋₁  Derived Types        M2   Process, Homeostasis, FeedbackLoop...
𝕋₁⁺ Core Categories      M1   GenericMechanism, ProcessArchetype...    ← THIS LEVEL
𝕋₂  Domain Concepts      M1   DNA_Replication, Newton_Second_Law...
𝕄₀  Instances (Poclets)  M0   E_coli_glucose_metabolism, Uranium_fission...
```

M1_CoreConcepts defines **meta-types** (types of types) — organizational
categories that group domain concepts by their structural role.

---

## Compound Types (𝕋₂)

M1_CoreConcepts also defines **compound types** using the emergence operator
`⊗ⁱ⇒`:

### **GenericConceptCombo**

Previously defined in M2, these emergent concept types were migrated to M1 to
preserve M2's purity constraint (only simple product types in M2).

**Structure:**
```
𝕋₂ = τ₁ ⊗ⁱ⇒ τ₂  where τᵢ ∈ 𝕋₁ (M2 GenericConcepts)
```

**Examples:**
```
SelfOrganization = ⊗ᵗ⇒(Emergence, Coherence)
Inertia          = ⊗ᵗ⇒(Memory, Entropy)
Adaptation       = ⊗ᵗ⇒(Information, Flow, Dynamics)
```

These types exhibit **emergent properties** irreducible to their components —
corresponding to function types `(→)` in the Curry-Howard correspondence.

---

## Properties Defined

### **simulationTitle**

```json
{
  "@id": "m1core:simulationTitle",
  "@type": "owl:DatatypeProperty",
  "rdfs:domain": {"@id": "owl:Ontology"},
  "rdfs:range": {"@id": "xsd:string"},
  "rdfs:comment": "Human-readable title for interactive M0 simulations"
}
```

Used to annotate M0 instance ontologies with display names for their
corresponding BabylonJS/Three.js 3D simulations.

---

## Validation Status

**OWL/RDFS Compliance:** ✅ Validated (May 14, 2026)
- RDFS diagnostic: 0 errors (9 errors fixed)
- OWL Pellet reasoning: PASSED
- Protégé compatibility: Confirmed

**Errors corrected:**
- 7 `rdfs:subClassOf` literals → URI references
- 1 `rdfs:domain` literal → URI reference
- 1 `rdfs:range` literal → URI reference

For validation details, see: `TSCG_OWL_Validation_Session_Summary.md`

---

## Import Dependencies

M1_CoreConcepts imports M2_GenericConcepts, which transitively imports the
entire M3 layer:

```
M3_GrammarFoundation  (operators, type system)
M3_EagleEye           (ASFID primitives)
M3_SphinxEye          (REVOI primitives)
M3_GenesisGrammar     (Φ/Ψ, epistemic gap)
         ↓
M2_GenericConcepts    (80 derived types)
         ↓
M1_CoreConcepts       (16 core categories + combo types)
```

All M3 dimensions and M2 GenericConcepts are available for use in
M1_CoreConcepts definitions.

---

## Usage in Domain Extensions

Domain-specific M1 extensions (M1_Biology, M1_Physics, etc.) instantiate
M1_CoreConcepts classes:

```turtle
m1bio:DNA_Replication a m1core:GenericMechanism ;
    rdfs:subClassOf m2:Process ;
    m2:hasStructuralFormula "D ⊗ᵗ I ⊗ᵗ F" .

m1phys:Wave_Particle_Duality a m1core:DomainPattern ;
    rdfs:subClassOf m2:Duality ;
    m2:hasStructuralFormula "S^opᵗ ⊗ᵗ F^opᵗ" .
```

---

## Ontology Statistics

**Classes:** 16
**Properties:** 1 (simulationTitle)
**Imports:** M2_GenericConcepts.jsonld
**Triples:** 324

---

## Design Principles

### **1. Domain Neutrality**

All concepts in M1_CoreConcepts must apply across ≥6 distinct knowledge domains.
Domain-specific patterns belong in M1 extensions.

### **2. Organizational Role**

M1_CoreConcepts classes serve as **organizing categories**, not directly
instantiable concepts. Actual domain concepts are defined in M1 extensions.

### **3. Structural Clarity**

Each core concept category has a clear structural role:
- Mechanisms → operational principles
- Templates → organizational patterns
- Archetypes → process patterns
- Patterns → relational structures

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **1.0.0** | 2026-05-14 | OWL/RDFS validation complete. 9 errors corrected (7 subClassOf, 1 domain, 1 range). RDFS: 0 errors. OWL Pellet: PASSED. Production-ready. |
| **0.9.x** | 2026-03-xx | Initial development. GenericConceptCombo types migrated from M2. Core categories defined. |

---

## See Also

- `M2_GenericConcepts.jsonld` — M2 derived types (structural formulas)
- `M1_Domains.jsonld` — Domain registry and metadata
- `M1_Biology.jsonld` — Biological domain concepts
- `M1_Physics.jsonld` — Physical domain concepts
- `M3_GenesisGrammar.jsonld` — M3 structural grammar foundation
- `TSCG_OWL_Validation_Session_Summary.md` — Validation methodology

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
