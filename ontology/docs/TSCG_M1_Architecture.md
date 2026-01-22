# TSCG M1 Layer Architecture: Extension Mechanism

**Version**: 1.0.0  
**Date**: January 22, 2026  
**Authors**: Echopraxium with the collaboration of Claude AI  

---

## Overview

The M1 (Middle Layer) in TSCG serves as a bridge between:
- **M2** (Metaconcepts): Universal patterns applicable across ALL domains
- **M0** (Poclets): Concrete instantiations of specific systems

M1 contains **domain-bounded but transdisciplinary concepts** that:
- Are more specific than M2 (not universal to all domains)
- Are more general than M0 (reusable within domain families)
- Instantiate M2 metaconcepts with domain-specific constraints

---

## Architectural Principle: Base + Extensions

The M1 layer uses an **extension architecture**:

```
M1_CoreConcepts.jsonld (BASE)
    ↓ owl:imports
    ├── M1_Optics.jsonld (EXTENSION)
    ├── M1_Photography.jsonld (EXTENSION)
    ├── M1_Philosophy.jsonld (EXTENSION)
    ├── M1_Chemistry.jsonld (EXTENSION)
    ├── M1_Biology.jsonld (EXTENSION)
    └── M1_[OtherDomain].jsonld (EXTENSIONS...)
```

### Base Ontology: M1_CoreConcepts.jsonld

**Purpose**: Contains generic transdisciplinary concepts applicable across multiple domains.

**Content**:
- Generic mechanisms (Oscillator, Amplifier, Filter, Modulator)
- Structural templates (Loop, Cascade, Feedback, Hierarchy)
- Relational patterns (Competition, Cooperation, Parasitism)
- Process archetypes (Growth, Decay, Saturation)

**Namespace**: `m1:`  
**URI**: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#`

**Philosophy**: M1_CoreConcepts is intentionally **sparse** at initialization. It grows incrementally as patterns are discovered across multiple domain extensions.

### Extension Ontologies: M1_[Domain].jsonld

**Purpose**: Domain-specific patterns that instantiate M2 metaconcepts within a particular field.

**Structure**: Each extension:
1. **Imports** M1_CoreConcepts (inherits generic concepts)
2. **Defines** domain-specific namespace (e.g., `m1optics:`, `m1photo:`)
3. **Contains** patterns validated by poclets in that domain
4. **References** M2 metaconcepts as theoretical basis

---

## Current M1 Extensions

### M1_Optics.jsonld

- **Namespace**: `m1optics:` (proposed, currently uses `m1:`)
- **Domain**: Optics, Color Theory, Light Physics, Visual Perception
- **Patterns**: 8 validated
- **Key concepts**:
  - Additive Color Synthesis (RGB)
  - Subtractive Color Synthesis (CMY/CMYK)
  - Channel Multiplexing
  - Compensatory Triplet (Exposure Triangle)
  - Logarithmic Scaling (f-stops)
- **Validated by**: RGB, HSL, CMY, CMYK, ColorSynthesis, ExposureTriangle poclets

### M1_Photography.jsonld

- **Namespace**: `m1photo:` (proposed, currently uses `m1:`)
- **Domain**: Photography, Camera Technology, Exposure Control
- **Patterns**: 10 (6 validated, 4 proposed)
- **Key concepts**:
  - Compensatory Triplet (ISO × Aperture × Shutter)
  - Logarithmic Scaling (Stop system)
  - Depth of Field Control
  - Motion Blur Control
  - Noise/Grain Control
  - Creative Exposure Modes (PASM)
- **Validated by**: ExposureTriangle poclet

---

## Proposed M1 Extensions

### M1_Philosophy.jsonld

- **Namespace**: `m1phil:`
- **Domain**: Philosophy, Ethics, Value Systems, Political Theory
- **Needed for**: Magic Color Wheel, Political Compass, Moral Foundations Theory
- **Proposed concepts**:
  - Value System (normative principles)
  - Philosophical Position (stances on ontology/ethics/epistemology)
  - Allied Relationship (shared values)
  - Enemy Relationship (incompatible values)
  - Philosophical Pole (one of N value orientations)
- **Status**: To be created

### M1_Chemistry.jsonld

- **Namespace**: `m1chem:`
- **Domain**: Chemistry, Thermodynamics, Chemical Reactions
- **Needed for**: Fire Triangle, Chemical Equilibrium, Catalysis
- **Proposed concepts**:
  - Reactant, Product, Catalyst
  - Activation Energy, Enthalpy
  - Stoichiometry
  - Combustion, Oxidation-Reduction
- **Status**: To be created

### M1_Biology.jsonld

- **Namespace**: `m1bio:`
- **Domain**: Biology, Ecology, Cellular Systems
- **Needed for**: Cell Signaling, Predator-Prey, Mutualism
- **Proposed concepts**:
  - Population Dynamics
  - Carrying Capacity
  - Trophic Level
  - Symbiosis types (Mutualism, Parasitism, Commensalism)
- **Status**: To be created

### M1_Economics.jsonld

- **Namespace**: `m1econ:`
- **Domain**: Economics, Market Theory, Trade
- **Needed for**: Supply-Demand, Market Equilibrium
- **Proposed concepts**:
  - Supply, Demand, Equilibrium Price
  - Market Mechanism
  - Trade-off (economic sense)
- **Status**: To be created

### M1_PoliticalScience.jsonld

- **Namespace**: `m1polisci:`
- **Domain**: Political Science, Governance, Power Structures
- **Needed for**: Political Compass, Governance Models
- **Proposed concepts**:
  - Political Ideology
  - Governance Model
  - Authority-Liberty axis
  - Economic Left-Right axis
- **Status**: To be created

---

## Namespace Strategy

### Problem

If all M1 extensions use the same namespace (`m1:`), concepts from different domains can conflict.

### Solution: Domain-Specific Namespaces

Each M1 extension defines its own namespace:

```json
{
  "@context": {
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m1optics": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Optics.jsonld#",
    "m1photo": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Photography.jsonld#",
    "m1phil": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Philosophy.jsonld#",
    ...
  }
}
```

### Usage in M0 Poclets

Poclets reference both M1_CoreConcepts (for generic) and M1_Domain extensions (for specific):

```json
{
  "@context": {
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m1photo": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Photography.jsonld#",
    ...
  },
  "m0:component": {
    "@type": "m1:CoreConcept",
    "m1photo:pattern": "m1photo:CompensatoryTriplet"
  }
}
```

---

## Concept Discovery Process

### Step 1: Poclet Analysis

Analyze M0 poclets to identify recurring patterns specific to a domain.

**Example**: Exposure Triangle poclet reveals:
- Compensatory triplet (3 parameters balance)
- Logarithmic scaling (stop system)
- Image quality trade-offs

### Step 2: Check M2 First

Is this pattern universal across all domains?
- **Yes** → It's an M2 metaconcept (e.g., Balance, Trade-off)
- **No** → Continue to Step 3

### Step 3: Check Existing M1

Does this concept already exist in M1_CoreConcepts or a domain extension?
- **Yes** → Reuse existing concept
- **No** → Continue to Step 4

### Step 4: Create M1 Concept

Create new M1 concept with:
- **M2 basis**: Which M2 metaconcepts does it instantiate?
- **Domain scope**: Which domains does it apply to?
- **Principle**: Core operational principle
- **Formula**: Mathematical/logical formulation (if applicable)
- **Examples**: Concrete examples from domain
- **Validation**: Which poclets validate this concept?

### Step 5: Validation Threshold

- **1 poclet**: Concept is proposed
- **2 poclets**: Concept is plausible
- **3+ poclets**: Concept is validated

### Step 6: Promotion Consideration

If concept appears in **3+ different domains**, consider:
- **Promoting to M1_CoreConcepts** (if transdisciplinary but not universal)
- **Promoting to M2** (if truly universal across all domains)

---

## Example: Compensatory Triplet

### Discovery Path

1. **Observed in**: Exposure Triangle (Photography)
2. **Pattern**: Three parameters balance multiplicatively
3. **M2 basis**: Balance (A⊗S⊗F), Trade-off (R⊗V⊗E)
4. **Domain scope**: Initially photography-specific
5. **Created in**: M1_Photography.jsonld as `m1photo:CompensatoryTriplet`
6. **Cross-domain validation**: Fire Triangle (Chemistry) has similar structure
7. **Decision**: Remains in domain extensions for now; may promote to M1_Core if 3+ domains validate

---

## Import Mechanism

### M1_CoreConcepts (Base)

```json
{
  "@context": {
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#",
    ...
  },
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld"
  ]
}
```

### M1_Photography (Extension)

```json
{
  "@context": {
    "m1photo": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Photography.jsonld#",
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#",
    ...
  },
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld",
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld"
  ]
}
```

### M0_ExposureTriangle (Poclet)

```json
{
  "@context": {
    "m0": "...",
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m1photo": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Photography.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#",
    ...
  },
  "m0:component": {
    "@type": "m2:Component",
    "m1photo:pattern": "m1photo:CompensatoryTriplet"
  }
}
```

---

## Development Strategy

### Phase 1: Core Foundation (CURRENT)

- ✅ Create M1_CoreConcepts.jsonld base ontology
- ✅ Document extension architecture
- ✅ Define concept discovery process
- ✅ Establish validation criteria

### Phase 2: Domain Extensions (IN PROGRESS)

- ✅ M1_Optics.jsonld (8 patterns validated)
- ✅ M1_Photography.jsonld (6 validated, 4 proposed)
- ⏳ M1_Philosophy.jsonld (needed for Magic Color Wheel)
- ⏳ M1_Chemistry.jsonld (needed for Fire Triangle)
- ⏳ M1_Biology.jsonld (needed for Cell Signaling)

### Phase 3: Core Population (FUTURE)

As patterns emerge across multiple domains:
- Identify truly transdisciplinary concepts
- Promote from domain extensions to M1_CoreConcepts
- Examples: Oscillator, Filter, Feedback Loop, Cascade

### Phase 4: Refinement (ONGOING)

- Clarify boundaries between M1_Core and M1_Domain
- Identify patterns for promotion to M2 (if universal)
- Prune redundant concepts
- Standardize formalization approach

---

## Design Principles

### 1. Modularity

Each domain extension is independent. Adding M1_Philosophy doesn't affect M1_Optics.

### 2. Explicit Dependencies

Use `owl:imports` to make dependencies clear and machine-readable.

### 3. Namespace Hygiene

Each domain gets its own namespace to prevent collisions.

### 4. Empirical Grounding

Concepts must be validated by at least one poclet. No theoretical concepts without empirical instantiation.

### 5. Promotion Pathways

Clear criteria for promoting concepts:
- M1_Domain → M1_Core (3+ domains)
- M1_Core → M2 (universal across all domains)

### 6. Minimal Core

M1_CoreConcepts stays sparse. Don't add concepts prematurely.

### 7. Documentation

Each concept documents:
- M2 basis (theoretical foundation)
- Domain scope (applicability)
- Validated poclets (empirical grounding)
- Examples (concrete instantiations)

---

## Advantages of Extension Architecture

### vs. Monolithic M1

**Problem**: Single M1 ontology becomes bloated with domain-specific concepts.

**Solution**: Modular extensions keep concepts organized by domain.

### vs. No M1 Layer

**Problem**: Jump directly from M2 (universal) to M0 (particular) loses reusable patterns.

**Solution**: M1 captures domain-specific but reusable concepts.

### vs. Flat M1

**Problem**: All concepts in one namespace without structure.

**Solution**: Base + Extensions provides clear organization and dependency management.

---

## Future Extensions

Beyond current/proposed domains, consider:

- **M1_Mathematics.jsonld**: Topology, Algebra, Analysis concepts
- **M1_ComputerScience.jsonld**: Algorithms, Data Structures, Computational Patterns
- **M1_Linguistics.jsonld**: Grammar, Semantics, Pragmatics
- **M1_Psychology.jsonld**: Cognition, Perception, Personality
- **M1_Sociology.jsonld**: Social Structures, Group Dynamics
- **M1_Music.jsonld**: Harmony, Rhythm, Form
- **M1_Architecture.jsonld**: Design Patterns, Spatial Organization

---

## Conclusion

The M1 layer extension architecture provides:

1. **Clarity**: Clear separation between generic (M1_Core) and domain-specific (M1_Extensions)
2. **Modularity**: Independent domain ontologies
3. **Scalability**: Easy to add new domains
4. **Reusability**: Concepts can be shared across extensions via M1_Core
5. **Validation**: Empirical grounding through poclets
6. **Evolution**: Clear promotion pathways (Domain → Core → M2)

This architecture supports TSCG's goal of building a **transdisciplinary framework** that bridges universal patterns (M2) with concrete systems (M0) through domain-bounded reusable concepts (M1).

---

**Document Status**: v1.0  
**Last Updated**: January 22, 2026  
**Review Status**: Pending peer review  
**Related Files**:
- `M1_CoreConcepts.jsonld` - Base ontology
- `M1_Optics.jsonld` - Optics extension
- `M1_Photography.jsonld` - Photography extension
- `M2_MetaConcepts.jsonld` - Parent layer
