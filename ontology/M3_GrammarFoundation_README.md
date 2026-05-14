# M3_GrammarFoundation.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 1.1.0
**Date**: 2026-05-13
**Layer**: M3 — Apex Ontology
**Status**: Active

---

## Overview

`M3_GrammarFoundation.jsonld` is the **apex ontology** of the TSCG hierarchy.
It has no imports and no dependencies — every other TSCG ontology depends on it,
directly or transitively.

It defines the complete mathematical and epistemological foundation of the
TSCG Structural Grammar: operators, abstract classes, type system, and
measurement properties.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld        ← APEX (no owl:imports)
        ↓ imported by
   M3_EagleEye.jsonld              (Territory Grammar Gt, ASFID primitives)
   M3_SphinxEye.jsonld             (Map Grammar Gm, REVOI primitives)
   M3_GenesisGrammar.jsonld        (bicephalous hub)
        ↓ imported by
   M2_GenericConcepts.jsonld
        ↓ imported by
   M1_CoreConcepts.jsonld  →  M1_xxx.jsonld  →  M0_xxx.jsonld
```

---

## Mathematical Foundation

The TSCG Structural Grammar is rooted in two well-established theories:

**Lambek Calculus** (Joachim Lambek, 1958)
A typed logical calculus for syntactic composition. Originally designed for
natural language grammars; adapted here for transdisciplinary concept grammars.
Key property: complex types are built from primitive types using compositional
operators — without any metric structure.

**Free Commutative Monoidal Categories** (Saunders MacLane, 1963/1971)
The algebraic framework underlying the `⊗` operator. A monoidal category
requires only three axioms: associativity, commutativity, and a neutral element.
No norm, no inner product, no scalar multiplication.

### Why Not Tensor Products / Hilbert Spaces?

```
Hilbert space requires:    Monoidal category requires:
  scalar multiplication  →    NOT needed in TSCG
  vector addition        →    NOT needed in TSCG
  inner product / norm   →    NOT needed in TSCG
  metric structure       →    NOT needed in TSCG
```

The `⊗` symbol is shared with tensor algebra by notational convention only —
exactly as `×` denotes both scalar multiplication and the vector cross product.
The mathematical context is explicitly different and must be read as such.

---

## Abstract Classes

### `m3gf:M3Grammar`

Abstract base class for all M3-level structural grammars.
Concrete subclasses defined in dependent files:

| Subclass | File | Primitives |
|---|---|---|
| Territory Grammar Gt | `M3_EagleEye.jsonld` | {A, S, F, I, D} |
| Map Grammar Gm | `M3_SphinxEye.jsonld` | {R, E, V, O, I} |

A grammar is characterised by four elements:
- **Primitives** — finite set of irreducible generators
- **Monoidal product** `⊗ⁱ` — co-activation operator
- **Emergence operator** `⊗ⁱ⇒` — produces emergent concept types
- **Duality operator** `^opⁱ` — produces structural opposites

### `m3gf:M3Dimension`

Abstract base class for M3 primitive types.
Plays two distinct mathematical roles depending on layer:

| Layer | Role | Mathematical object | Metric? |
|---|---|---|---|
| M3 / M2 | Generator of type expressions | Primitive type in a monoidal grammar | ❌ None |
| M0 | Evaluation function | Functor `F_x : System → [0,1]` | ✅ Real-valued |

> The word "dimension" is used in the **analytical sense** (independent axis
> of characterisation), NOT in the metric/Hilbert sense.

---

## The Six Indexed Operators

All operators carry an index `i ∈ {t, m}` indicating whether they operate
in the Territory Grammar (Gt) or Map Grammar (Gm).

### `⊗ⁱ` — Monoidal Product (Co-activation)

```
⊗ᵗ  :  Territory co-activation   (Eagle Eye / ASFID)
⊗ᵐ  :  Map co-activation         (Sphinx Eye / REVOI)
⊗ⁱ  :  general indexed form
```

**Axioms:**
```
Associativity  :  (A ⊗ B) ⊗ C  =  A ⊗ (B ⊗ C)
Commutativity  :  A ⊗ B  =  B ⊗ A
Neutral element:  A ⊗ 1  =  A
No metric      :  no norm, no inner product, no scalar multiplication
```

**Meaning**: both primitive types are simultaneously active in the concept
signature.

**Example**: `Process = D ⊗ᵗ I ⊗ᵗ F`
(Process mobilises Dynamics, Information, and Flow together)

---

### `⊗ⁱ⇒` — Emergence Operator

```
⊗ᵗ⇒  :  Territory emergence   (ontological)
⊗ᵐ⇒  :  Map emergence         (epistemic)
⊗ⁱ⇒  :  general indexed form
```

**Meaning**: produces a derived concept whose properties are **irreducible**
to the sum of its parts. Corresponds to the function type `(→)` in the
Curry-Howard correspondence.

**Examples**:
```
⊗ᵗ⇒(Memory, Entropy)           =  Inertia
⊗ᵐ⇒(Representable, Verifiable) =  ModelQuality
```

---

### `^opⁱ` — Duality Operator

```
^opᵗ  :  Territory duality
^opᵐ  :  Map duality
^opⁱ  :  general indexed form
```

**Meaning**: produces the **polar opposite** of a concept type within the
same dimensional space. Corresponds to negation in propositional logic via
the Curry-Howard correspondence.

**Examples**:
```
Coherence^opᵗ   =  Incoherence
Observable^opᵐ  =  Unobservable
Entropy^opᵗ     =  NegEntropy  (e.g. information, life)
```

---

## Type System Hierarchy

The three operators generate a complete four-level type system:

```
𝕋₀  Primitive Types       M3   {A, S, F, I, D, R, E, V, O, I}
                                10 generators, no metric

𝕋₁  Derived Types         M2   τ₁ ⊗ⁱ τ₂ ⊗ⁱ ... ⊗ⁱ τₙ  |  τᵢ ∈ 𝕋₀
                                ~80 M2 GenericConcepts (named product types)

𝕋₂  Compound Types        M1   τ₁ ⊗ⁱ⇒ τ₂  |  τᵢ ∈ 𝕋₁
                                M1 GenericConceptCombos (emergent types)

𝕄₀  Terms (Proof Terms)   M0   poclets inhabiting a type τ ∈ 𝕋₁ ∪ 𝕋₂
                                instances that prove a system fits a type
```

### Curry-Howard Correspondence

Under this type system, TSCG acquires a logical interpretation:

| Type Theory | TSCG |
|---|---|
| Primitive type | ASFID/REVOI dimension |
| Product type `τ₁ ⊗ τ₂` | M2 structural formula |
| Named type | M2 GenericConcept |
| Term inhabiting a type | M0 Poclet |
| Proof of a proposition | Poclet demonstrating system fits type |
| Degree of proof | Epistemic gap δ₁ |

A poclet does not merely *describe* a system — it *proves* that the system
inhabits a conceptual type. δ₁ measures how strongly.

---

## Measurement Properties

### `m3gf:intersubjectiveBenchmark`

Domain-contextualized canonical poclet used as scoring reference for M0
instances. Grounds TSCG measurement in **norm-referenced intersubjective
consensus**.

**Canon resolution order (default = DomainSpecific):**
```
1. DomainSpecific  —  same M1 domain as the poclet          ← DEFAULT
2. CrossDomain     —  adjacent M1 domain
3. Universal       —  e.g. M0_AdaptiveImmuneResponse
4. Free scoring    —  with explicit justification            ← last resort
```

**Objectivity levels:**
```
Subjective              →  single expert, no reference
MultiExpertConsensus    →  several experts, same setup
CanonCalibrated         →  scored against domain benchmark
ContextualizedBenchmark →  multi-cook, multi-setup convergence  ← default
```

### `m3gf:defeasibilityStatus`

Explicit declaration that a benchmark is **provisional** — valid until
superseded by broader consensus.

```json
{
  "status":          "provisional",
  "validUntil":      "superseded_by_better_consensus",
  "revisionTrigger": [
    "new_canonical_poclet_identified",
    "expert_consensus_challenged",
    "domain_expansion",
    "corpus_maturation"
  ]
}
```

This is not a weakness — it is the normal epistemic status of scientific,
legal, and practical knowledge. Analogous to:
- *Stare decisis* in law (precedent holds until overruled)
- Scientific paradigms (Kuhn: valid until anomalies accumulate)
- Peirce: truth as the limit of indefinite communal inquiry

---

## Properties Summary

| Property | Type | Defined on | Description |
|---|---|---|---|
| `m3gf:grammarType` | DatatypeProperty | M3Grammar | e.g. `free_commutative_monoidal` |
| `m3gf:monoidalProduct` | DatatypeProperty | M3Grammar | `⊗ⁱ` operator definition |
| `m3gf:emergenceOperator` | DatatypeProperty | M3Grammar | `⊗ⁱ⇒` operator definition |
| `m3gf:dualityOperator` | DatatypeProperty | M3Grammar | `^opⁱ` operator definition |
| `m3gf:intersubjectiveBenchmark` | ObjectProperty | M0 instances | benchmark reference |
| `m3gf:defeasibilityStatus` | DatatypeProperty | M0 instances | provisional status |

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **1.1.0** | 2026-05-13 | MAJOR UPDATE: dcterms metadata, 6 indexed operators (⊗ᵗ ⊗ᵐ ⊗ᵗ⇒ ⊗ᵐ⇒ ^opᵗ ^opᵐ), type system 𝕋₀/𝕋₁/𝕋₂/𝕄₀, intersubjectiveBenchmark, defeasibilityStatus. Apex position confirmed. |
| **1.0.0** | 2026-05-12 | Initial skeleton: M3Grammar, M3Dimension, grammarType, monoidalProduct. |

---

## References

- Lambek, J. (1958). *The mathematics of sentence structure.*
  American Mathematical Monthly, 65(3), 154–170.
- MacLane, S. (1963). *Natural associativity and commutativity.*
  Rice University Studies.
- MacLane, S. (1971). *Categories for the Working Mathematician.* Springer.
- Howard, W. (1980). *The formulae-as-types notion of construction.*
- Stevens, S.S. (1946). *On the theory of scales of measurement.*
  Science, 103(2684), 677–680.
- Peirce, C.S. (1878). *How to Make Our Ideas Clear.*
  Popular Science Monthly.

---

## See Also

- `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
- `TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md`
- `M3_EagleEye.jsonld` — Territory Grammar Gt
- `M3_SphinxEye.jsonld` — Map Grammar Gm
- `M3_GenesisGrammar.jsonld` — Bicephalous hub

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
