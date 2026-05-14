# M3_EagleEye.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 2.5.0
**Date**: 2026-05-13
**Layer**: M3 — Territory Grammar Gt
**Status**: Active

---

## Overview

`M3_EagleEye.jsonld` defines the **Territory Grammar Gt** of TSCG — the
analytical perspective on systems-as-territory. It declares the 5 primitive
types of the ASFID family and their role in the TSCG Structural Grammar.

The Eagle Eye observes, measures, and characterises phenomena as they exist
in the world — independently of how they are modelled or represented.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld   ← APEX (imported by this file)
        ↓
M3_EagleEye.jsonld            ← THIS FILE
        ↓ imported by
M3_GenesisGrammar.jsonld
        ↓ imported by
M2_GenericConcepts.jsonld  →  M1_xxx.jsonld  →  M0_xxx.jsonld
```

**Imports**: `M3_GrammarFoundation.jsonld` (operators, abstract classes)
**Imported by**: `M3_GenesisGrammar.jsonld`

---

## Territory Grammar Gt

```json
"grammar_properties": {
  "grammar_name":   "Territory Grammar Gt",
  "grammar_type":   "free_commutative_monoidal",
  "primitives":     ["A", "S", "F", "I", "D"],
  "product":        "⊗ᵗ  (structural co-activation, Territory)",
  "perspective":    "ontological / empirical",
  "independence":   "verified"
}
```

The 5 ASFID primitive types are **analytically independent** generators —
no primitive is derivable from the others. They are independent in the
conceptual sense, not in the metric/orthogonality sense.

---

## The 5 Primitive Types (ASFID)

| Symbol | Name | Meaning | Range | Critical Axiom |
|---|---|---|---|---|
| **A** | Attractor | Asymptotic convergence tendency, stability landscape | [0,1] | — |
| **S** | Structure | Topological organisation, connectivity, relational patterns | [0,1] | — |
| **F** | Flow | Exchange rate with environment, openness, dissipation | [0.1,1] | F ≥ 0.1 (Universal Openness) |
| **I** | Information | State complexity (synchronic), variety, Shannon entropy | [0,1] | — |
| **D** | Dynamics | State evolution (diachronic), temporal change rate | [0,1] | — |

### Flow — Special Status

Flow (F) is the only ASFID dimension with a **critical axiom**: `F ≥ 0.1`.
No perfectly isolated system exists — all real systems exchange at least
minimally with their environment. `F = 0` is a theoretical ground state
(Stase), not a physical reality.

Flow also has a unique dual nature: it is both an object (a dimension that
can be measured) and a morphism (a transformation between states). It is
the only ASFID dimension with intrinsic entity/morphism duality.

---

## Two Mathematical Roles

The same 5 labels play different roles depending on the layer:

```
M3 / M2  →  Primitive types (generators)
             "which dimensions does this concept mobilise?"
             Qualitative — no numbers involved

M0       →  Evaluation functors
             F_A, F_S, F_F, F_I, F_D : System → [0,1]
             Quantitative — real-valued measurements
```

At M0, scores are **norm-referenced** against domain-specific canonical
poclets (`m3gf:intersubjectiveBenchmark`) — not against absolute standards.

---

## Connection to Map Grammar Gm

Territory Grammar Gt and Map Grammar Gm are structurally separate.
Their connection is formalised in `M3_GenesisGrammar.jsonld` via
**natural transformations**:

```
Φ : Gt → Gm    (observation — Territory measurements inform Map construction)
Ψ : Gm → Gt    (interpretation — Map predictions guide Territory measurement)
```

The **epistemic gap** δ₁ measures the non-isomorphism of Φ:

```
δ₁ = ||ASFID_mean − REVOI_mean|| / √2  ∈ [0, 1]
```

Korzybski formalised: *Φ is never a perfect isomorphism* — the map is not
the territory, δ₁ > 0 in all real systems.

---

## Usage in M2 Structural Formulas

ASFID primitives appear in M2 GenericConcept formulas as Territory-indexed
product types:

```
Process      =  D ⊗ᵗ I ⊗ᵗ F
FeedbackLoop =  A ⊗ᵗ F ⊗ᵗ D
Resilience   =  A ⊗ᵗ S ⊗ᵗ D
Entropy      =  D ⊗ᵗ F^opᵗ
```

Mixed formulas (bicephalous concepts) combine both grammars:

```
Coherence    =  A ⊗ᵗ S ⊗ᵗ I ⊗ᵐ R ⊗ᵐ O
```

---

## Metaphor

```
Image    :  Eagle soaring above the territory
Vision   :  Penetrating sight that perceives reality as-is
Action   :  Observes, measures, decomposes, analyses
Domain   :  Territory (Reality)
Acuity   :  8× human vision — precision at distance
Quadrant :  Analysis of Reality (Territory)
```

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **2.5.0** | 2026-05-13 | IMPORT UPDATE: owl:imports → M3_GrammarFoundation.jsonld. m3: namespace → M3_GenesisGrammar.jsonld. Aligns with new M3 apex architecture. |
| **2.4.0** | 2026-05-11 | FORMALISM REFORM: basis_properties → grammar_properties (Gt). Removed hilbert_space, orthonormality. coupling_with_REVOI → coupling_with_MapGrammar (natural transformations). orthogonality_matrix → independence_matrix. |
| **2.3.0** | 2026-02-16 | REFACTORING: Removed M3Dimension class (now in GenesisSpace). Removed common properties (now in GenesisSpace). |

---

## See Also

- `M3_GrammarFoundation.jsonld` — apex ontology (operators, type system)
- `M3_SphinxEye.jsonld` — Map Grammar Gm (REVOI primitives)
- `M3_GenesisGrammar.jsonld` — bicephalous hub (Φ/Ψ, δ₁)
- `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
