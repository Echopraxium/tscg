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
"hilbert_space": "ℋ_μ"  (remove)     δ₁ and SpectralClasses    (unchanged)
"orthonormality"         (remove)     @graph, @context, @base   (unchanged)
SVD / αᵢⱼ / ket notation (remove)     owl:imports, ontologyType  (unchanged)
"basis_properties"       (rename)     rdfs:label, rdfs:comment   (unchanged)
```

---

## Phase Overview

```
Phase 1 — M3 SURGERY    (manual, ~2h)
  ├── M3_EagleEye.jsonld    → Territory Grammar G_T
  ├── M3_SphinxEye.jsonld   → Map Grammar G_M
  └── M3_GenesisSpace.jsonld → Bicephalous Bicategory

Phase 2 — M2 RENAME     (script + manual cleanup, ~1h)
  ├── Run migrate_properties.py on all .jsonld files
  └── Manual: remove SVD/Hilbert from Domain and KnowledgeField metaconcepts

Phase 3 — M1/M0 VERIFY  (script verification, ~30min)
  ├── Run verify_migration.py to detect residual tensor references
  └── Fix any remaining occurrences
```

---

## Phase 1 — M3 Surgical Edits

Read the 3 M3 files before editing. Apply changes precisely with `str_replace`.

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
  "grammar_name":   "Territory Grammar G_T",
  "grammar_type":   "free_commutative_monoidal",
  "primitives":     ["A", "S", "F", "I", "D"],
  "product":        "⊗_T  (structural co-activation, Territory)",
  "primitive_role": "generators of Territory type expressions (M2 formulas)",
  "functor_role":   "F_A, F_S, F_F, F_I, F_D : System → [0,1]  (M0 evaluation)",
  "perspective":    "ontological / empirical",
  "independence":   "verified  (no primitive derivable from others)"
}
```

**UPDATE** `rdfs:comment` on the EagleEye ontology node:
- Remove: `"Orthonormal basis providing analytical perspective..."`
- Replace with: `"Territory Grammar G_T: free commutative monoidal grammar over primitive types {A,S,F,I,D}. Provides the ontological/empirical perspective on systems-as-territory. At M0, each primitive instantiates as an evaluation functor F_x : System → [0,1]."`

**UPDATE** `dcterms:description`:
- Remove mention of "analytical decomposition" and "basis"
- Replace with: "Territory Grammar G_T — primitive types {A,S,F,I,D} for empirical characterisation of systems. Part of the TSCG bicephalous architecture (G_T ⊕ G_M)."

**UPDATE** `coupling_with_REVOI` section if present:
- Remove: inner product notation `⟨i|j⟩`, Σ matrix, SVD references
- Keep: Φ and Ψ operators but reframe as natural transformations:
```json
"coupling_with_MapGrammar": {
  "description": "G_T (Territory) and G_M (Map) are connected via natural transformations",
  "Phi": "Φ : G_T → G_M  (observation: Territory → Map)",
  "Psi": "Ψ : G_M → G_T  (interpretation: Map → Territory)",
  "epistemic_gap": "δ₁ = ||ASFID_mean − REVOI_mean|| / √2  (non-isomorphism measure)"
}
```

**VERSION**: Bump to next minor (e.g. 2.3.0 → 2.4.0).

**CHANGELOG entry** (keep 3 most recent):
```json
{
  "version": "2.4.0",
  "date": "<today>",
  "changes": "FORMALISM REFORM: Replaced Hilbert space / orthonormal basis framing with Structural Grammar (Lambek calculus). basis_properties → grammar_properties. Removed hilbert_space, orthonormality fields. Φ/Ψ reframed as natural transformations. See TSCG_Structural_Grammar_Foundation_README.md."
}
```

---

### 1.2 — M3_SphinxEye.jsonld

Apply the same pattern as EagleEye, with Map Grammar specifics:

**REPLACE** `basis_properties` with:
```json
"grammar_properties": {
  "grammar_name":   "Map Grammar G_M",
  "grammar_type":   "free_commutative_monoidal",
  "primitives":     ["R", "E", "V", "O", "I"],
  "product":        "⊗_M  (structural co-activation, Map)",
  "primitive_role": "generators of Map type expressions (epistemic quality signatures)",
  "functor_role":   "F_R, F_E, F_V, F_O, F_I : System → [0,1]  (M0 evaluation)",
  "perspective":    "epistemic / representational",
  "independence":   "verified  (no primitive derivable from others)"
}
```

**UPDATE** `rdfs:comment`:
- Replace with: `"Map Grammar G_M: free commutative monoidal grammar over primitive types {R,E,V,O,I}. Provides the epistemic/representational perspective on systems-as-map. At M0, each primitive instantiates as an evaluation functor F_x : System → [0,1]."`

**REMOVE** in `coupling_with_ASFID`:
- `"operator": "Σ ∈ ℝ^(5×5)"` — remove
- `"10D Hilbert space"` references — remove
- Keep Φ/Ψ, reframe as in EagleEye step above

**VERSION**: Bump to next minor.  
**CHANGELOG**: Same pattern as EagleEye.

---

### 1.3 — M3_GenesisSpace.jsonld

This is the most important file. Targets: any remaining Hilbert/SVD/ket content,
and the bicephalous connection description.

**REMOVE** entirely wherever found:
- `"hilbert_space"`, `"hilbert_basis"`, `"ket_notation"` fields
- SVD formulas: `Σᵢ σᵢ |uᵢ⟩⊗|vᵢ⟩`
- Coupling matrix `Σ ∈ ℝ^(5×5)` and αᵢⱼ coefficients
- `"complete_space": "ASFID ⊕ REVOI (10D Hilbert space)"` → replace:
  ```json
  "complete_space": "G_T ⊕ G_M  (bicephalous grammar: Territory ⊕ Map)"
  ```
- Any `ℂ²⁵` or `ℋ_ASFID ⊗ ℋ_REVOI` references

**UPDATE** the bicephalous architecture description:
```json
"bicephalous_architecture": {
  "Territory_Grammar": {
    "@id": "m3:eagle_eye:EagleEye",
    "grammar": "G_T",
    "primitives": ["A","S","F","I","D"],
    "role": "what systems ARE  (ontological)"
  },
  "Map_Grammar": {
    "@id": "m3:sphinx_eye:SphinxEye",
    "grammar": "G_M",
    "primitives": ["R","E","V","O","I"],
    "role": "how systems are REPRESENTED  (epistemic)"
  },
  "connection": {
    "Phi": "Φ : G_T → G_M  (natural transformation — observation)",
    "Psi": "Ψ : G_M → G_T  (natural transformation — interpretation)",
    "korzybski": "Φ is never an isomorphism — the map is not the territory",
    "epistemic_gap": "δ₁ = ||ASFID_mean − REVOI_mean|| / √2"
  },
  "mathematical_foundation": "Lambek Calculus / free commutative monoidal categories",
  "see_also": "TSCG_Structural_Grammar_Foundation_README.md"
}
```

**ADD** a `m3:structuralGrammarOperators` node documenting the 3 operators:
```json
{
  "@id": "m3:structuralGrammarOperators",
  "@type": "owl:NamedIndividual",
  "rdfs:label": "TSCG Structural Grammar Operators",
  "rdfs:comment": "The three operators of the TSCG Structural Grammar",
  "m3:operators": {
    "coActivation": {
      "symbol": "⊗",
      "name": "Structural co-activation",
      "type": "commutative monoidal product",
      "meaning": "Both dimensions simultaneously present in concept signature",
      "example": "D⊗I⊗F = Process  (mobilises Dynamics, Information, Flow)"
    },
    "emergence": {
      "symbol": "⊗⇒",
      "name": "Structural emergence",
      "type": "derived monoidal product",
      "meaning": "Concept emerges from combination of two existing concepts",
      "example": "⊗⇒(Memory, Entropy) = Inertia"
    },
    "duality": {
      "symbol": "^op",
      "name": "Structural duality",
      "type": "monoidal opposition",
      "meaning": "Polar opposite of a concept signature",
      "example": "Coherence^op = Incoherence"
    }
  },
  "disclaimer": "⊗ shares notation with the algebraic tensor product but operates in a distinct context: a typed combinatorial grammar without metric structure. See Lambek (1958) and MacLane (1963)."
}
```

**VERSION**: Bump to next minor.  
**CHANGELOG**: Document the formalism reform.

---

## Phase 2 — M2 Property Renaming

### 2.1 — Run the Automated Script

Script located at: `scripts/migrate_properties.py`

```bash
cd <tscg_repo_root>
python scripts/migrate_properties.py --dry-run   # preview changes first
python scripts/migrate_properties.py             # apply changes
```

The script renames the 3 property families across ALL `.jsonld` files:

| Old | New |
|---|---|
| `m2:hasTensorFormula` | `m2:hasStructuralFormula` |
| `m2:hasTensorFormulaTeX` | `m2:hasStructuralFormulaTeX` |
| `m2:hasTensorFormulaASCII` | `m2:hasStructuralFormulaASCII` |

> ⚠️ The script validates JSON after every file. If validation fails, it
> restores the original and reports the error.

### 2.2 — Manual Cleanup in M2_GenericConcepts.jsonld

After running the script, apply these manual changes:

**A. Update property declarations** (the `owl:DatatypeProperty` nodes):
- Update `rdfs:label` of `m2:hasStructuralFormula`:
  ```json
  "rdfs:label": "has structural formula",
  "rdfs:comment": "Structural formula in the TSCG Structural Grammar. Encodes which primitive dimensions (ASFID/REVOI) are co-activated by this concept. ⊗ is a commutative monoidal product — NOT an algebraic tensor product. See Lambek (1958)."
  ```

**B. Remove Hilbert content from `Domain` metaconcept**:
- Remove: `svdDecomposition`, `couplingMatrix`, `feedbackOperators` (Φ/Ψ in Hilbert form), `fullSpace: "25-dimensional ASFID⊗REVOI tensor product"`
- Keep: the bicephalous connection idea, reformulated as natural transformations

**C. Remove Hilbert content from `KnowledgeField` metaconcept** (if present):
- Remove: `ℋ_ASFID ⊗ ℋ_REVOI`, SVD, `||ASFID|| · ||REVOI|| · cos(θ)` epistemic depth formula
- Keep: the concept of field maturity, σ_mean thresholds (these are heuristic, not Hilbert-derived)

**D. Update ValueSpace "tensor" entry**:
```json
"structural_formula": {
  "definition": "Structural co-activation in TSCG Structural Grammar (Lambek-style)",
  "examples": [
    "Process = D⊗I⊗F  (Territory Grammar)",
    "Coherence = A⊗S⊗I⊗R⊗O  (bicephalous)"
  ],
  "note": "⊗ here is a monoidal product, NOT an algebraic tensor product. No metric required."
}
```

**VERSION**: Bump M2_GenericConcepts to next minor.

---

## Phase 3 — M1 / M0 Verification

### 3.1 — Run the Verification Script

```bash
python scripts/verify_migration.py
```

The script scans all `.jsonld` files and reports any residual tensor references.
Expected output after successful migration: **0 violations**.

### 3.2 — Manual Fix if Needed

If violations are found, they will be one of:
1. `hasTensorFormula` not renamed — apply script again on that file
2. `hilbert_space` / `orthonormality` in an M1 extension — remove manually
3. `ℂ²⁵` or ket notation in a documentation field — replace with grammar description

### 3.3 — Checklist Before Closing

```
□  M3_EagleEye.jsonld     — grammar_properties present, hilbert_space absent
□  M3_SphinxEye.jsonld    — grammar_properties present, hilbert_space absent
□  M3_GenesisSpace.jsonld — structuralGrammarOperators added, SVD removed
□  M2_GenericConcepts     — hasStructuralFormula everywhere, Domain/KF cleaned
□  M2_FormulasReference   — title updated ("Structural Formulas" not "Tensor")
□  verify_migration.py    — 0 violations
□  JSON validation        — all files parse without error
□  Version numbers        — all modified files bumped
□  Changelogs             — 3-entry rolling maximum respected
```

---

## Critical Rules (Never Violate)

1. **Formula values are SACRED** — `"D⊗I⊗F"` strings must never change.
2. **⊗ symbol stays** — only the mathematical *interpretation* changes.
3. **JSON-LD structure untouched** — `@graph`, `@context`, `@base`, `owl:imports` unchanged.
4. **Always validate JSON** after every file modification.
5. **Encoding**: always `encoding='utf-8'` in Python file operations.
6. **Changelog max 3 entries** — remove oldest before adding new.
7. **str_replace** for surgical edits — never rewrite entire files.

---

## References

- `references/Structural_Grammar_Foundation.md` — full theoretical foundation
- `scripts/migrate_properties.py` — automated property renaming
- `scripts/verify_migration.py` — post-migration validation
- Lambek, J. (1958). *The mathematics of sentence structure.* American Mathematical Monthly.
- MacLane, S. (1963). *Natural associativity and commutativity.* Rice University Studies.
