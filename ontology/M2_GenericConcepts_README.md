# M2_GenericConcepts.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 15.12.0
**Date**: 2026-05-13
**Layer**: M2 — Derived Types (Named Product Types)
**Status**: Active

---

## Overview

`M2_GenericConcepts.jsonld` is the **M2 layer** of the TSCG hierarchy.
It defines ~80 **GenericConcepts** — transdisciplinary named product types
derived from M3 primitive types via structural grammar operators.

Each GenericConcept is a **named derived type** (𝕋₁) in the TSCG type system:
a structural formula combining M3 primitives from Territory Grammar Gt
and/or Map Grammar Gm.

> **v15.12.0 — Formalism Reform**: `m2:hasTensorFormula` renamed to
> `m2:hasStructuralFormula` (250 occurrences). The `⊗` operator is now
> explicitly a **monoidal product** in the Lambek grammar sense, not an
> algebraic tensor product.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld  ─┐
M3_EagleEye.jsonld           ─┤→  M3_GenesisGrammar.jsonld
M3_SphinxEye.jsonld          ─┘           ↓ imported by
                                  M2_GenericConcepts.jsonld   ← THIS FILE
                                           ↓ imported by
                                  M1_CoreConcepts.jsonld
                                           ↓
                                  M1_xxx.jsonld  →  M0_xxx.jsonld
```

**Imports**: `M3_GenesisGrammar.jsonld`
**Imported by**: `M1_CoreConcepts.jsonld`

---

## The Type System at M2

M2 GenericConcepts are **named product types (𝕋₁)**:

```
𝕋₁ = { τ₁ ⊗ⁱ τ₂ ⊗ⁱ ... ⊗ⁱ τₙ  |  τᵢ ∈ 𝕋₀ }
```

Where `𝕋₀ = {A, S, F, I, D, R, E, V, O, I}` are the 10 M3 primitive types.

### Three Formula Types

| Type | Operator | Example |
|---|---|---|
| Territory formula | `⊗ᵗ` | `Process = D ⊗ᵗ I ⊗ᵗ F` |
| Map formula | `⊗ᵐ` | `ModelQuality = R ⊗ᵐ V ⊗ᵐ O` |
| Bicephalous formula | `⊗ᵗ` + `⊗ᵐ` | `Coherence = A ⊗ᵗ S ⊗ᵗ I ⊗ᵐ R ⊗ᵐ O` |

### Curry-Howard Reading

Each M2 concept is both a **type** and a **logical proposition**:

```
Process = D ⊗ᵗ I ⊗ᵗ F
        = "a system that simultaneously exhibits Dynamics, Information, and Flow"
        = a proposition that a poclet can prove (or partially prove)
```

A poclet M0 *proves* its system inhabits the concept type. δ₁ measures
the strength of that proof.

---

## GenericConcept Properties

Each GenericConcept node carries these properties:

| Property | Description | Example |
|---|---|---|
| `m2:hasStructuralFormula` | Type formula (M3 primitives + ⊗) | `"D ⊗ I ⊗ F"` |
| `m2:hasStructuralFormulaTeX` | TeX rendering | `"D \\otimes I \\otimes F"` |
| `m2:hasStructuralFormulaASCII` | ASCII safe form | `"D (x) I (x) F"` |
| `m2:semanticSignature` | Human-readable counterpart of formula | `"temporal_change + information_transfer + exchange"` |
| `m2:hasPolarity` | Polar/bipolar/unipolar | `"bipolar"` |
| `m2:hasDominantM3` | Most characteristic primitive | `"m3:eagle_eye:Dynamics"` |
| `m2:conceptFamily` | Family grouping | `"Dynamics"` |

### hasStructuralFormula — Key Property

```json
{
  "@id": "m2:hasStructuralFormula",
  "@type": "owl:DatatypeProperty",
  "rdfs:label": "has structural formula",
  "rdfs:comment": "Structural formula combining M3 primitive types into a M2
                   GenericConcept type signature (TSCG Structural Grammar —
                   monoidal product, not algebraic tensor product)"
}
```

> **Notation note**: `⊗` in TSCG structural formulas is a **commutative
> monoidal product** (Lambek 1958, MacLane 1963), NOT the algebraic tensor
> product of Hilbert spaces. It encodes simultaneous co-activation of
> primitive types — no metric, no inner product required.

---

## Selected GenericConcepts

A sample of the 84 named product types defined at M2:

| Concept | Structural Formula | Reading |
|---|---|---|
| Homeostasis | `A ⊗ᵗ S ⊗ᵗ F` | Stable structure with regulated flow |
| Process | `D ⊗ᵗ I ⊗ᵗ F` | Dynamics + information + flow |
| FeedbackLoop | `A ⊗ᵗ F ⊗ᵗ D` | Attractor-driven dynamic flow |
| Emergence | `I ⊗ᵗ S ⊗ᵗ D` | Information + structure + change |
| Resilience | `A ⊗ᵗ S` | Attractor + structure |
| Dissipation | `F ⊗ᵗ D` | Flow + dynamics |
| Adaptation | `I ⊗ᵗ F ⊗ᵗ D` | Information-driven dynamic flow |
| Coherence | `A ⊗ᵗ S ⊗ᵗ I ⊗ᵐ R ⊗ᵐ O` | Bicephalous: stable structure, representable & observable |
| Interoperability | `S ⊗ᵗ I ⊗ᵗ F ⊗ᵐ V ⊗ᵐ E` | Bicephalous: structured flow, verifiable & evolvable |

---

## M2 Purity Constraint

> A GenericConcept belongs in M2 **only if** it is valid across ≥6 domains
> including non-physical domains (mathematics, mythology, music, economics...).
> Domain-specific concepts belong in M1 extensions.

This constraint prevents "ontological proliferation" — ensuring M2 remains
a set of genuinely transdisciplinary patterns.

---

## Bicephalous Architecture at M2

M2 builds on both M3 grammars:

```
Eagle Eye (ASFID / Gt)         →  empirical dimension of concepts
Sphinx Eye (REVOI / Gm)        →  epistemic dimension of concepts
Bicephalous formulas           →  concepts spanning both perspectives
```

Purely Territory concepts (only ASFID primitives) characterise what a
system *is*. Purely Map concepts (only REVOI primitives) characterise
how a system *can be known*. Bicephalous concepts capture both at once.

---

## M1 Combo Types (𝕋₂)

Some concepts cannot be expressed as simple product types (𝕋₁). These
**compound types (𝕋₂)** are defined in `M1_CoreConcepts.jsonld` using
the emergence operator:

```
𝕋₂ = { τ₁ ⊗ⁱ⇒ τ₂  |  τᵢ ∈ 𝕋₁ }

SelfOrganization = ⊗ᵗ⇒(Emergence, Coherence)
```

These were previously in M2 as `m2:GenericConceptCombo` instances but
were migrated to M1 to preserve M2 purity.

---

## Property Declarations

M2 defines 24 `owl:DatatypeProperty` and `owl:ObjectProperty` instances
used to characterise GenericConcepts:

| Property | Role |
|---|---|
| `m2:hasStructuralFormula` | Core type formula |
| `m2:hasStructuralFormulaTeX` | TeX rendering |
| `m2:hasStructuralFormulaASCII` | ASCII safe rendering |
| `m2:semanticSignature` | Human-readable formula complement |
| `m2:conceptFamily` | Family grouping (9 families) |
| `m2:hasPolarity` | Polar / bipolar / unipolar |
| `m2:hasDominantM3` | Most characteristic M3 primitive |
| `m2:hasEpistemicGap` | Expected δ₁ range |
| `m2:dualAspects` | Dual pole descriptions |
| `m2:shortName` | Abbreviated label |
| `m2:changelog` | Rolling 3-entry version history |

---

## Migration Note (v15.11.0 → v15.12.0)

The formalism reform renamed all tensor-related properties:

```
BEFORE (v15.11.0)              AFTER (v15.12.0)
──────────────────────         ──────────────────────────────
m2:hasTensorFormula       →    m2:hasStructuralFormula        (85 nodes)
m2:hasTensorFormulaTeX    →    m2:hasStructuralFormulaTeX     (82 nodes)
m2:hasTensorFormulaASCII  →    m2:hasStructuralFormulaASCII   (83 nodes)
m2:hasTensorFormulaNote   →    m2:hasStructuralFormulaNote
m2:hasTensorFormulaExpanded →  m2:hasStructuralFormulaExpanded
tensorFormula (text)      →    structuralFormula (text)
owl:imports GenesisSpace  →    GenesisGrammar
```

**Formula values are unchanged** — `"D ⊗ I ⊗ F"` remains `"D ⊗ I ⊗ F"`.
Only property names and mathematical interpretation changed.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **15.12.0** | 2026-05-13 | FORMALISM REFORM: hasTensorFormula → hasStructuralFormula (250 occurrences). owl:imports → GenesisGrammar. Property labels updated to monoidal grammar context. |
| **15.11.0** | 2026-03-13 | Added m2:hasStructuralFormulaNote for polarity semantics. Flow (F) amendment propagated to relevant formulas. |
| **15.10.1** | 2026-02-28 | 75 atomic GenericConcepts across 9 families. Combo family removed from M2, instances migrated to M1_CoreConcepts. |

---

## See Also

- `M3_GrammarFoundation.jsonld` — type system 𝕋₀/𝕋₁/𝕋₂/𝕄₀, operators
- `M3_GenesisGrammar.jsonld` — M3 hub (Gt, Gm, Φ/Ψ, δ₁)
- `M1_CoreConcepts.jsonld` — combo types 𝕋₂
- `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
