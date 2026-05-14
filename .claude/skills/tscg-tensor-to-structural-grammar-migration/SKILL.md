---
name: tscg-tensor-to-structural-grammar-migration
description: >
  Migration pipeline for the TSCG foundational formalism reform: replaces the
  algebraic tensor product interpretation of ⊗ (Hilbert spaces, SVD, coupling
  matrices, ket notation) with the Structural Grammar formalism (Lambek calculus,
  monoidal product, categorical functors). Covers 3 phases: M3 surgical edits,
  M2 property renaming (automated script), M1/M0 verification. Use this skill
  whenever Michel mentions the structural grammar reform, the migration of
  hasTensorFormula, the Lambek calculus foundation, removing Hilbert space
  references from M3, or renaming tensor properties in M2. Also use when asked
  to apply the Structural Grammar reframing to any ontology file in the TSCG
  framework. Prerequisite: read references/Structural_Grammar_Foundation.md
  before starting any phase.
---

# TSCG — Tensor to Structural Grammar Migration

**Migration from**: Algebraic tensor product (Hilbert spaces, SVD, ket notation)  
**Migration to**: Structural Grammar formalism (Lambek calculus, monoidal product)  
**Scope**: M3 (manual surgery) → M2 (automated rename) → M1/M0 (verification)  
**Key invariant**: Formula VALUES are unchanged — only mathematical interpretation
and property NAMES change.  
**Status**: v16.0.0 COMPLETED (2026-05-13)

> ⚠️ **Read first**: `references/Structural_Grammar_Foundation.md`
> This is the authoritative specification of the new formalism.

---

## What Changes vs What Stays the Same

```
CHANGES                               STAYS THE SAME
──────────────────────────────────    ─────────────────────────────────────
m2:hasTensorFormula      (rename)     Formula values "D⊗I⊗F"   (unchanged)
m2:hasTensorFormulaTeX   (rename)     Symbol ⊗                  (unchanged)
m2:hasTensorFormulaASCII (rename)     Scores A/S/F/I/D/R/E/V/O/I (unchanged)
"hilbert_space"          (remove)     δ₁ and SpectralClasses    (unchanged)
"orthonormality"         (remove)     @graph, @context           (unchanged)
SVD / αᵢⱼ / ket notation (remove)     owl:imports, ontologyType  (unchanged)
"basis_properties"       (rename)     rdfs:label, rdfs:comment   (unchanged)
Any "Hilbert space" text (remove)     @base (factorised in M1)   (unchanged)
```

> **Zero tolerance**: "Hilbert space" must NOT appear anywhere in active
> ontology files. Only changelog entries documenting the reform are exempt.

---

## Phase Overview

```
Phase 1 — M3 SURGERY       (manual, ~2h)
  ├── M3_GrammarFoundation.jsonld  → NEW apex ontology (no imports)
  ├── M3_EagleEye.jsonld           → Territory Grammar Gt
  ├── M3_SphinxEye.jsonld          → Map Grammar Gm
  └── M3_GenesisGrammar.jsonld     → Bicephalous hub (ex-GenesisSpace)

Phase 2 — M2 RENAME         (script + manual cleanup, ~1h)
  ├── Run cli_tools/migrate_properties/migrate_properties.py
  └── Manual: remove SVD/Hilbert from Domain and KnowledgeField metaconcepts

Phase 3 — M1/M0 VERIFY     (script verification, ~30min)
  ├── Run cli_tools/verify_migration/verify_migration.py
  ├── Fix any remaining occurrences
  └── Delete legacy alignment files (e.g. M2_MetaConcepts_Alignment.jsonld)
```

---

## Phase 1 — M3 Surgical Edits

Read each M3 file before editing. Apply changes precisely with `str_replace`.

### 1.0 — M3_GrammarFoundation.jsonld (NEW — create first)

**This is the new apex ontology** — no `owl:imports`, no dependencies.
It defines: 6 indexed operators (⊗ᵗ ⊗ᵐ ⊗ᵗ⇒ ⊗ᵐ⇒ ^opᵗ ^opᵐ), abstract
classes M3Grammar and M3Dimension, type system 𝕋₀/𝕋₁/𝕋₂/𝕄₀,
`m3gf:intersubjectiveBenchmark`, `m3gf:defeasibilityStatus`.

See `ontology/M3_GrammarFoundation_README.md` for full specification.

---

### 1.1 — M3_EagleEye.jsonld

**TARGET**: `basis_properties` block and any Hilbert/orthonormality references.

**REMOVE** these fields wherever found:
```json
"hilbert_space": "ℋ_μ"
"orthonormality": "verified"
"completeness": "partial (completes with REVOI from Sphinx Eye)"
```

**REPLACE** `basis_properties` with:
```json
"grammar_properties": {
  "grammar_name":   "Territory Grammar Gt",
  "grammar_type":   "free_commutative_monoidal",
  "primitives":     ["A", "S", "F", "I", "D"],
  "product":        "⊗ᵗ  (structural co-activation, Territory)",
  "primitive_role": "generators of Territory type expressions (M2 formulas)",
  "functor_role":   "F_A, F_S, F_F, F_I, F_D : System → [0,1]  (M0 evaluation)",
  "perspective":    "ontological / empirical",
  "independence":   "verified  (no primitive derivable from others)"
}
```

**UPDATE** `owl:imports`: add `M3_GrammarFoundation.jsonld`

**UPDATE** `coupling_with_REVOI` → `coupling_with_MapGrammar`:
```json
"coupling_with_MapGrammar": {
  "Phi": "Φ : Gt → Gm  (natural transformation — observation)",
  "Psi": "Ψ : Gm → Gt  (natural transformation — interpretation)",
  "epistemic_gap": "δ₁ = ||ASFID_mean − REVOI_mean|| / √2"
}
```

**REPLACE** `orthogonality_matrix` → `independence_matrix`:
```json
"independence_matrix": {
  "description": "5 primitive types are analytically independent",
  "verified": "true",
  "note": "Independence here means conceptual non-redundancy, not metric orthogonality."
}
```

**VERSION**: bump minor. **CHANGELOG**: rolling 3 entries.

---

### 1.2 — M3_SphinxEye.jsonld

Same pattern as EagleEye with Map Grammar specifics:
- `grammar_name`: "Map Grammar Gm"
- `primitives`: ["R", "E", "V", "O", "I"]
- `product`: "⊗ᵐ  (structural co-activation, Map)"
- `coupling_with_ASFID` → `coupling_with_TerritoryGrammar`

**UPDATE** `owl:imports`: add `M3_GrammarFoundation.jsonld`

---

### 1.3 — M3_GenesisGrammar.jsonld (RENAME from GenesisSpace)

**RENAME FILE**: `M3_GenesisSpace.jsonld` → `M3_GenesisGrammar.jsonld`

**UPDATE** `owl:imports`: add `M3_GrammarFoundation.jsonld` alongside EagleEye + SphinxEye

**REPLACE** `mathematical_properties` (Hilbert block) with:
```json
"grammar_foundation": {
  "formalism":    "Lambek Calculus / Free Commutative Monoidal Categories",
  "architecture": "Bicephalous Structural Grammar: Gt (Territory) + Gm (Map)",
  "connection": {
    "Phi": "Φ : Gt → Gm  (natural transformation — observation)",
    "Psi": "Ψ : Gm → Gt  (natural transformation — interpretation)",
    "epistemic_gap": "δ₁ = ||ASFID_mean − REVOI_mean|| / √2"
  }
}
```

**REMOVE** entirely: SVD, αᵢⱼ, coupling matrix Σ, ket notation, ℂ²⁵, ℋ_ASFID, ℋ_REVOI

**UPDATE** all "Hilbert space" text references — zero tolerance, even in examples:
- `"Quantum Mechanics: Hilbert space dimension"` → `"state space dimension"`
- `"log₁₀(dim(⊗ᵢ Hᵢ)) where Hᵢ are Hilbert spaces"` → `"log₁₀(number of distinct states)"`

**VERSION**: bump major (e.g. 3.9.0 → 4.0.0). **CHANGELOG**: rolling 3 entries.

---

## Phase 2 — M2 Property Renaming

### 2.1 — Run the Automated Script

```bash
cd <tscg_repo_root>

# Windows — force UTF-8 encoding
python cli_tools/migrate_properties/migrate_properties.py --dry-run --root ontology
python cli_tools/migrate_properties/migrate_properties.py --root ontology
```

Renames across ALL `.jsonld` files:

| Old | New |
|---|---|
| `m2:hasTensorFormula` | `m2:hasStructuralFormula` |
| `m2:hasTensorFormulaTeX` | `m2:hasStructuralFormulaTeX` |
| `m2:hasTensorFormulaASCII` | `m2:hasStructuralFormulaASCII` |

### 2.2 — Manual Cleanup in M2_GenericConcepts.jsonld

- Remove `couplingMatrix`, `svdDecomposition` blocks from Domain/KnowledgeField
- Remove ALL "Hilbert space" text — zero tolerance
- Update `rdfs:label` of `m2:hasStructuralFormula`:
  ```json
  "rdfs:comment": "Structural formula in the TSCG Structural Grammar.
    ⊗ is a commutative monoidal product — NOT an algebraic tensor product."
  ```

### 2.3 — M1 Files: @base Factorisation

All M1 `.jsonld` files must have `@base` present and factorised:

```json
"@context": {
  "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
  "m1core": "M1_CoreConcepts.jsonld#",
  "m2": "M2_GenericConcepts.jsonld#"
}
```

Namespace prefixes must NOT repeat the base URL. Use relative paths.

---

## Phase 3 — M1 / M0 Verification

### 3.1 — Run the Verification Script

```bash
# Windows — UTF-8 encoding handled automatically by the script
python cli_tools/verify_migration/verify_migration.py --root ontology --strict

# Redirect output to file
python cli_tools/verify_migration/verify_migration.py --root ontology --strict > verify_output.txt 2>&1
```

Expected: **0 violations**.

> **Excluded automatically**: any directory whose name contains `backup`,
> `_archive`, `Ref`, `docs`, `sparql`, `tools`, `_protos`, `reboot-kit`.
> These are archives/references and do not need migration.

### 3.2 — Manual Fix if Needed

| Violation type | Fix |
|---|---|
| `hasTensorFormula` not renamed | Run `migrate_properties.py` on that file |
| `hilbert_space` / `orthonormality` | Remove manually — zero tolerance |
| `Hilbert space` in text | Replace with grammar/categorical equivalent |
| `couplingMatrix` / `svdDecomposition` | Remove blocks entirely |
| Legacy alignment file (e.g. `M2_MetaConcepts_Alignment.jsonld`) | Delete if no longer needed |
| Backup dir scanned | Already excluded — no action needed |

### 3.3 — Final Checklist

```
□  M3_GrammarFoundation.jsonld  — apex, no owl:imports, operators defined
□  M3_EagleEye.jsonld           — grammar_properties Gt, hilbert_space absent
□  M3_SphinxEye.jsonld          — grammar_properties Gm, hilbert_space absent
□  M3_GenesisGrammar.jsonld     — grammar_foundation, SVD/Hilbert removed
□  M2_GenericConcepts.jsonld    — hasStructuralFormula, no Hilbert text
□  All M1 files                 — @base present and factorised
□  verify_migration.py          — 0 violations
□  JSON validation              — all files parse without error
□  Version numbers              — all modified files bumped
□  Changelogs                   — 3-entry rolling maximum respected
□  git commit                   — with descriptive message
```

---

## Critical Rules (Never Violate)

1. **Formula values are SACRED** — `"D⊗I⊗F"` strings must never change.
2. **⊗ symbol stays** — only the mathematical *interpretation* changes.
3. **Zero Hilbert tolerance** — no "Hilbert space" in active files, even in examples.
4. **JSON-LD structure untouched** — `@graph`, `@context`, `@base`, `owl:imports`.
5. **Encoding**: always `encoding='utf-8'` in Python. Use `-X utf8` on Windows.
6. **Changelog max 3 entries** — remove oldest before adding new.
7. **str_replace** for surgical edits — never rewrite entire files.
8. **@base factorised** — M1 namespace prefixes must not repeat the base URL.

---

## References

- `references/Structural_Grammar_Foundation.md` — full theoretical foundation
- `cli_tools/migrate_properties/migrate_properties.py` — automated property renaming
- `cli_tools/verify_migration/verify_migration.py` — post-migration validation
- `ontology/StructuralGrammar/` — documentation folder (5 READMEs)
- Lambek, J. (1958). *The mathematics of sentence structure.* American Mathematical Monthly.
- MacLane, S. (1963). *Natural associativity and commutativity.* Rice University Studies.
