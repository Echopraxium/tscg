# M3_GrammarFoundation.jsonld

**Version:** 1.0.0  
**Layer:** M3  
**Type:** Foundational Interface Ontology  
**Created:** 2026-05-12  
**Status:** Foundational

---

## 🎯 Role

**M3_GrammarFoundation** is the **mathematical foundation** for all TSCG M3-level grammars. It defines:
- Lambek Calculus formalism (free commutative monoidal categories)
- Monoidal product ⊗ with indexed forms
- Abstract classes for M3 grammars and dimensions
- Common properties shared by all M3 components

This interface ontology **resolves circular dependencies** in the M3 layer by providing a common foundation that EagleEye, SphinxEye, and GenesisGrammar all import.

---

## 📐 Mathematical Foundation

### Lambek Calculus

TSCG structural grammars use **Lambek Calculus** — a logical framework for composition based on **free commutative monoidal categories**:

```
Category C with:
- Objects: M3 dimensions (A, S, F, I, D, R, E, V, O, I)
- Morphisms: Composition operations
- Monoidal product: ⊗ (tensor-like but without metric)
```

**Key properties:**
- **Associative:** (A ⊗ B) ⊗ C = A ⊗ (B ⊗ C)
- **Commutative:** A ⊗ B = B ⊗ A
- **Neutral element:** 1 where A ⊗ 1 = A

---

## ⊗ Monoidal Product

The **monoidal product ⊗** is the core composition operator with **indexed forms** for different perspectives:

### Base Form
```
⊗ : C × C → C
```

### Indexed Forms
```
⊗ⁱ where i ∈ {t, m}

⊗ᵗ (Territory/Eagle):  D ⊗ᵗ I ⊗ᵗ F = Process (Territory context)
⊗ᵐ (Map/Sphinx):       R ⊗ᵐ V ⊗ᵐ O = ModelQuality (Map context)
```

### Emergence Operator
```
⊗ⁱ⇒ : Tuple[Concept] → Concept

⊗ᵗ⇒(Memory, Entropy) = Inertia (Territory emergence)
⊗ᵐ⇒(Representable, Verifiable) = ModelQuality (Map emergence)
```

### Duality Operator
```
^opⁱ : Concept → Concept

Coherence^opᵗ = Incoherence (Territory duality)
Observable^opᵐ = Unobservable (Map duality)
```

---

## 🏗️ Architecture Position

```
M3_GrammarFoundation ← YOU ARE HERE
(Mathematical foundation)
         ↓ imported by
    ┌────┴────┬─────────┐
    │         │         │
M3_Eagle  M3_Sphinx  M3_Genesis
    │         │         │
    └────┬────┴─────────┘
         ↓ imported by
    M2_GenericConcepts
```

**Design pattern:** Interface/Implementation
- **Interface:** M3_GrammarFoundation (this file)
- **Implementations:** EagleEye, SphinxEye, GenesisGrammar

---

## 📚 Why Monoidal (not Vectorial)?

TSCG uses **monoidal categories** instead of vector spaces because:

### Vector Spaces are TOO RICH
- Require scalar multiplication (what's "2 × Attractor"?)
- Require metric/norm structure
- Force artificial linearity

### Monoidal Categories are MINIMAL
- Only need composition: A ⊗ B
- Order doesn't matter (commutative)
- Grouping doesn't matter (associative)
- Neutral element exists (1)

### Mathematical Hierarchy
```
Monoidal Category ← TSCG uses this
    ↓ add structure
Group
    ↓ add scalar field
Module
    ↓ add division
Vector Space
    ↓ add inner product
Hilbert Space
```

TSCG stays at the **monoidal level** — just enough structure for composition, nothing artificial.

---

## 🎯 Abstract Classes

### m3gf:M3Grammar
Base class for all M3-level structural grammars.

**Subclasses:**
- m3e:EagleEye (Territory Grammar)
- m3s:SphinxEye (Map Grammar)
- m3:GenesisGrammar (Bicephalous aggregation)

### m3gf:M3Dimension
Base class for M3 primitive dimensions.

**Subclasses:**
- ASFID dimensions (m3e:Attractor, m3e:Structure, etc.)
- REVOI dimensions (m3s:Representable, m3s:Evolvable, etc.)

---

## 🔧 Common Properties

### m3gf:grammarType
**Type:** `owl:DatatypeProperty`  
**Range:** `xsd:string`  
**Purpose:** Disambiguate grammar types across TSCG layers

**Enum values:**
- `M3_StructuralGrammar` (monoidal composition at M3)
- `M2_GenericConcepts` (formula grammars at M2)
- `M1_DomainConcepts` (domain specializations)
- `M0_InstanceOntology` (SHACL validation)

**Why needed:** Prevents collision between M3 structural grammar and M0 instance grammar.

### m3gf:monoidalProduct
**Type:** `owl:ObjectProperty`  
**Purpose:** Define monoidal product relationships

---

## 📚 Historical Foundation

**Braille Structural Grammar (2022-07, updated 2026-5)**  
`ontology/StructuralGrammar/Braille_StructuralGrammar.pdf`

The Lambek Calculus formalism was **empirically validated** through the Braille writing system modeling — a complete 6-dot structural grammar demonstrating:
- Character composition via monoidal products
- Phonetic/semantic emergence
- Dual perspective (tactile/symbolic)

This provided concrete proof that monoidal categories work for real-world complex systems.

---

## 🎯 Key Takeaways

1. **Foundation for all M3 grammars** — imported by Eagle, Sphinx, Genesis
2. **Lambek Calculus formalism** — free commutative monoidal categories
3. **Indexed operators** — ⊗ⁱ, ⊗ⁱ⇒, ^opⁱ for Territory/Map perspectives
4. **Resolves circular dependencies** — clean architecture
5. **Minimal mathematical structure** — just enough, nothing artificial

**M3_GrammarFoundation is where TSCG's mathematical rigor becomes explicit.** 🌟
