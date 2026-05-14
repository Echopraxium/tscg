# M3_GenesisGrammar.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 4.0.0
**Date**: 2026-05-13
**Layer**: M3 — Bicephalous Hub
**Status**: Active (renamed from M3_GenesisSpace.jsonld)

---

## Overview

`M3_GenesisGrammar.jsonld` is the **bicephalous hub** of the M3 layer.
It imports and connects the three foundational M3 ontologies:

- `M3_GrammarFoundation.jsonld` — operators, type system, measurement properties
- `M3_EagleEye.jsonld` — Territory Grammar Gt (ASFID primitives)
- `M3_SphinxEye.jsonld` — Map Grammar Gm (REVOI primitives)

It is the sole M3 file imported by `M2_GenericConcepts.jsonld`, making it
the **gateway** through which all of M3 becomes available to the rest of
the TSCG hierarchy.

> **Renamed from `M3_GenesisSpace.jsonld`** (v4.0.0). The rename reflects
> the formalism reform: the file no longer defines a "Hilbert space" but a
> "Structural Grammar" in the Lambek / monoidal category sense.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld   ─┐
M3_EagleEye.jsonld            ─┤─→  M3_GenesisGrammar.jsonld   ← THIS FILE
M3_SphinxEye.jsonld           ─┘             ↓ imported by
                                     M2_GenericConcepts.jsonld
                                             ↓
                                     M1_CoreConcepts.jsonld
                                             ↓
                                     M1_xxx.jsonld  →  M0_xxx.jsonld
```

---

## Grammar Foundation

```json
"grammar_foundation": {
  "formalism":    "Lambek Calculus / Free Commutative Monoidal Categories",
  "architecture": "Bicephalous Structural Grammar: Gt (Territory) + Gm (Map)",
  "grammars": {
    "Gt": "Territory Grammar — primitives {A,S,F,I,D} — Eagle Eye — ontological",
    "Gm": "Map Grammar     — primitives {R,E,V,O,I} — Sphinx Eye — epistemic"
  },
  "connection": {
    "Phi": "Φ : Gt → Gm  (natural transformation — observation)",
    "Psi": "Ψ : Gm → Gt  (natural transformation — interpretation)",
    "epistemic_gap": "δ₁ = ||ASFID_mean − REVOI_mean|| / √2",
    "korzybski":    "Φ is never a perfect isomorphism — the map is not the territory"
  }
}
```

---

## Bicephalous Architecture

The two grammars are **structurally separate** — this separation is
fundamental, not a consequence of orthogonality.

| Aspect | Territory Grammar Gt | Map Grammar Gm |
|---|---|---|
| File | `M3_EagleEye.jsonld` | `M3_SphinxEye.jsonld` |
| Primitives | {A, S, F, I, D} | {R, E, V, O, I} |
| Perspective | Ontological / empirical | Epistemic / representational |
| Role | What systems ARE | How systems are REPRESENTED |
| Eagle/Sphinx | Eagle Eye | Sphinx Eye |
| Model/Reality | Reality | Model |
| Analysis/Synthesis | Analysis | Synthesis |

### Natural Transformations Φ and Ψ

```
Φ : Gt → Gm    Observation — Territory measurements inform Map construction
               Example: neutron flux data (ASFID) → diffusion model (REVOI)

Ψ : Gm → Gt    Interpretation — Map predictions guide Territory measurement
               Example: oscillation model (REVOI) → install detectors (ASFID)
```

Φ and Ψ are **natural transformations** in the categorical sense —
structure-preserving maps between the two grammars.

### Epistemic Gap δ₁

```
δ₁ = ||ASFID_mean − REVOI_mean|| / √2
```

δ₁ measures the **non-isomorphism** of Φ — how far the Map is from
perfectly capturing the Territory.

| SpectralClass | δ₁ range | Interpretation |
|---|---|---|
| Coherent | [0.00, 0.05) | Near-perfect alignment |
| OnCriticalLine | [0.05, 0.15) | Productive tension |
| Liminal | [0.15, 0.30) | Significant gap |
| Enigmatic | [0.30, 1.00) | Fundamental challenge |

---

## TSCG Ontology Type System

GenesisGrammar defines the complete taxonomy of TSCG ontology types
via `m3:TscgOntologyType` and its 11 subclasses:

| Type | Layer | Description |
|---|---|---|
| `m3:Genesis` | M3 | Foundational structural grammar files |
| `m3:GenesisExtension` | M3 | Bicephalous components (EagleEye, SphinxEye) |
| `m3:GenericConcepts` | M2 | Named product types (transdisciplinary patterns) |
| `m3:DomainExtension` | M1 | Domain-specific concept sets |
| `m3:SystemicFramework` | M1 | Established methodology mappings |
| `m3:Poclet` | M0 | Minimal validated system instances |
| `m3:CaseStudy` | M0 | Pedagogical examples |
| `m3:RealWorldSystem` | M0 | Deployed system analyses |
| `m3:SymbolicSystemGrammar` | M0 | Formal symbolic systems (I Ching, Braille...) |
| `m3:TscgTool` | M0 | Software tools operating on TSCG itself |
| `m3:TransDisclet` | M0 | Systems native to multiple disciplines |

---

## Key Properties Defined

GenesisGrammar defines the core M3 properties used throughout the hierarchy:

| Property | Type | Description |
|---|---|---|
| `m3:ontologyType` | ObjectProperty | Architectural type of a TSCG ontology |
| `m3:M3Dimension` | Class | Abstract primitive type (generator / functor) |
| `m3:dimensionSymbol` | DatatypeProperty | Symbolic identifier for a primitive |
| `m3:dimensionIndex` | DatatypeProperty | Position index within grammar |
| `m3:dimensionExamples` | DatatypeProperty | Illustrative instances |
| `m3:semanticSignature` | DatatypeProperty | Minimal sufficient characterisation |
| `m3:AlignmentLoop` | Class | Φ/Ψ iterative refinement mechanism |
| `m3:KorzybskiPrinciple` | Class | Formalisation of Map ≠ Territory |

---

## Category Theory Foundation

GenesisGrammar formalises TSCG as a system of categories and functors:

```
Cat_TSCG         :  Category of TSCG layers {M3, M2, M1, M0}
Cat_M3_ASFID     :  Category of Gt primitives {A, S, F, I, D}
Cat_M3_REVOI     :  Category of Gm primitives {R, E, V, O, I}
Cat_M2           :  Category of GenericConcepts (derived types 𝕋₁)
Cat_KnowledgeField:  Category of knowledge domains

F_structuralFormula : Cat_M3 → Cat_M2  (grammar operators create 𝕋₁ types)
F_instantiation     : Cat_M2 → Cat_M1  (types → domain concepts)
F_concretize        : Cat_M1 → Cat_M0  (concepts → instances)
```

---

## Epistemological Foundation

GenesisGrammar grounds TSCG in five philosophical traditions:

| Tradition | Connection |
|---|---|
| **Korzybski** | Map/Territory — Φ is never a perfect isomorphism |
| **Constructivism** | Knowledge constructed through Map/Gm operations |
| **Cybernetics** | Systems observed through ASFID/Gt feedback |
| **Second-order cybernetics** | Observer part of observed system |
| **Process philosophy** | Systems as processes, not static entities |

---

## Validation Tests

| Test | Method | Result |
|---|---|---|
| Primitive independence | Conceptual non-redundancy check | ✅ All 10 primitives independent |
| Completeness | Domain coverage across 23+ poclets | ✅ Physical, biological, social, abstract |
| Structural homology | Cross-domain formula verification | ✅ No contradictions |
| Spanning | All system aspects expressible in Gt + Gm | ✅ Validated |

---

## Migration Note (v3.9.0 → v4.0.0)

This file was previously named `M3_GenesisSpace.jsonld`. The rename and
formalism reform were applied simultaneously in v4.0.0:

```
REMOVED                              REPLACED WITH
────────────────────────────────     ─────────────────────────────────────
mathematical_properties (Hilbert)  → grammar_foundation (Lambek/monoidal)
Σ coupling matrix (SVD)            → natural transformations Φ, Ψ
orthogonal_union                   → structurally_complementary
orthogonality_proof                → independence (conceptual)
F_tensorization                    → F_structuralFormula
"Tensor Product" altLabel          → "Structural Formula"
"Hilbert Space Basis" altLabel     → "Structural Grammar Basis"
H_ASFID, H_REVOI                   → Gt, Gm
10D Hilbert space                  → bicephalous grammar Gt + Gm
M3_GenesisSpace.jsonld             → M3_GenesisGrammar.jsonld
```

All formula VALUES (e.g. `D⊗I⊗F`) and all M2/M1/M0 data are unchanged.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **4.0.0** | 2026-05-13 | FORMALISM REFORM + RENAME: GenesisSpace → GenesisGrammar. Added M3_GrammarFoundation.jsonld to imports. mathematical_properties → grammar_foundation. All Hilbert/SVD/tensor references replaced. Φ/Ψ reframed as natural transformations. |
| **3.9.0** | 2026-03-23 | Flow (F) enriched: axiom relaxed F≥0, F_morphic annotation, F_potential/F_active spectrum. |
| **3.8.0** | — | RENAMED m3:TransdisciplinaryMetaConcepts → m3:GenericConcepts. |

---

## See Also

- `M3_GrammarFoundation.jsonld` — apex (operators, type system, benchmark)
- `M3_EagleEye.jsonld` — Territory Grammar Gt
- `M3_SphinxEye.jsonld` — Map Grammar Gm
- `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
- `TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md`

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
