# M3_SphinxEye.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 3.3.0
**Date**: 2026-05-13
**Layer**: M3 — Map Grammar Gm
**Status**: Active

---

## Overview

`M3_SphinxEye.jsonld` defines the **Map Grammar Gm** of TSCG — the
epistemic perspective on systems-as-map. It declares the 5 primitive
types of the REVOI family and their role in the TSCG Structural Grammar.

The Sphinx Eye constructs, synthesises, and evaluates the quality of
conceptual models — independently of what those models represent.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld   ← APEX (imported by this file)
        ↓
M3_SphinxEye.jsonld           ← THIS FILE
        ↓ imported by
M3_GenesisGrammar.jsonld
        ↓ imported by
M2_GenericConcepts.jsonld  →  M1_xxx.jsonld  →  M0_xxx.jsonld
```

**Imports**: `M3_GrammarFoundation.jsonld` (operators, abstract classes)
**Imported by**: `M3_GenesisGrammar.jsonld`

---

## Map Grammar Gm

```json
"grammar_properties": {
  "grammar_name":   "Map Grammar Gm",
  "grammar_type":   "free_commutative_monoidal",
  "primitives":     ["R", "E", "V", "O", "I"],
  "product":        "⊗ᵐ  (structural co-activation, Map)",
  "perspective":    "epistemic / representational",
  "independence":   "verified"
}
```

The 5 REVOI primitive types are **analytically independent** generators —
no primitive is derivable from the others. They are independent in the
conceptual sense, not in the metric/orthogonality sense.

---

## The 5 Primitive Types (REVOI)

| Symbol | Name | Meaning | Range |
|---|---|---|---|
| **R** | Representable | Semantic decodability — can the phenomenon be encoded in symbols? | [0,1] |
| **E** | Evolvable | Generativity and emergence — does the map create new phenomena? | [0,1] |
| **V** | Verifiable | Testability and falsifiability — can map predictions be tested? | [0,1] |
| **O** | Observable | Measurability and detectability — can the phenomenon be observed? | [0,1] |
| **I** | Interoperable | Integration and compatibility — can the map interface with others? | [0,1] |

> ⚠️ **R = Representable** (NEVER Reproducible). This is a standing
> convention — always verify before writing any documentation.

### Naming Convention

REVOI dimensions use **adjective form** (`-able`) for grammatical
consistency and conciseness. Former names (`-ability` suffix, v2.x)
are preserved in `m3:sphinx_eye:formerName` for traceability.

```
Representability  →  Representable  (R)
Evolvability      →  Evolvable      (E)
Verifiability     →  Verifiable     (V)
Observability     →  Observable     (O)
Interoperability  →  Interoperable  (I)
```

---

## Two Mathematical Roles

The same 5 labels play different roles depending on the layer:

```
M3 / M2  →  Primitive types (generators)
             "which epistemic qualities does this concept require?"
             Qualitative — no numbers involved

M0       →  Evaluation functors
             F_R, F_E, F_V, F_O, F_I : System → [0,1]
             Quantitative — real-valued measurements
```

At M0, scores are **norm-referenced** against domain-specific canonical
poclets (`m3gf:intersubjectiveBenchmark`) — not against absolute standards.

### Impact of intersubjectiveBenchmark on REVOI

Using calibrated benchmarks systematically improves REVOI scores:

```
R (Representable)  ↑  calibrated against a recognised domain canon
E (Evolvable)      ↑  benchmarks updatable by new consensus
V (Verifiable)  ↑↑  multi-cook convergence makes scores reproducible
O (Observable)     ↑  scoring methodology is explicit and documented
I (Interoperable)  ↑  shared benchmarks enable cross-team exchange
```

---

## Connection to Territory Grammar Gt

Map Grammar Gm and Territory Grammar Gt are structurally separate.
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

| δ₁ range | SpectralClass | Interpretation |
|---|---|---|
| [0.00, 0.05) | Coherent | Near-perfect Territory/Map alignment |
| [0.05, 0.15) | OnCriticalLine | Productive epistemic tension |
| [0.15, 0.30) | Liminal | Significant gap |
| [0.30, 1.00) | Enigmatic | Fundamental modelling challenge |

---

## Usage in M2 Structural Formulas

REVOI primitives appear in M2 GenericConcept formulas as Map-indexed
product types:

```
Observability    =  O ⊗ᵐ R
ModelQuality     =  ⊗ᵐ⇒(Representable, Verifiable)
Observable^opᵐ  =  Unobservable
```

Mixed formulas (bicephalous concepts) combine both grammars:

```
Coherence  =  A ⊗ᵗ S ⊗ᵗ I ⊗ᵐ R ⊗ᵐ O
```

---

## Metaphor

```
Image    :  Sphinx at the crossroads, posing riddles
Wisdom   :  Enigmatic knowledge that constructs understanding
Action   :  Constructs, synthesises, composes, evaluates
Domain   :  Map (Model)
Nature   :  Half-human (reason) / half-lion (instinct)
Quadrant :  Synthesis of Model (Map)
```

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **3.3.0** | 2026-05-13 | IMPORT UPDATE: owl:imports → M3_GrammarFoundation.jsonld. m3: namespace → M3_GenesisGrammar.jsonld. Aligns with new M3 apex architecture. |
| **3.2.0** | 2026-05-11 | FORMALISM REFORM: basis_properties → grammar_properties (Gm). Removed hilbert_space, orthonormality, Sigma matrix. coupling_with_ASFID → coupling_with_TerritoryGrammar (natural transformations). orthogonality_matrix → independence_matrix. |
| **3.1.0** | 2026-02-16 | REFACTORING: Removed M3Dimension class (now in GenesisSpace). Removed common properties. Kept REVOI-specific properties. |

---

## See Also

- `M3_GrammarFoundation.jsonld` — apex ontology (operators, type system)
- `M3_EagleEye.jsonld` — Territory Grammar Gt (ASFID primitives)
- `M3_GenesisGrammar.jsonld` — bicephalous hub (Φ/Ψ, δ₁)
- `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
- `TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md`

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
