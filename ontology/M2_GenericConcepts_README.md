# M2_GenericConcepts.jsonld

**Version:** 15.18.0  
**Layer:** M2  
**Type:** Generic Concepts Ontology  
**Created:** 2026-01-14  
**Last Modified:** 2026-05-13

---

## 🎯 Role

**M2_GenericConcepts** is the **middle layer** of TSCG — the bridge between abstract M3 grammars and concrete M0 instances. It defines **transdisciplinary systemic patterns** (GenericConcepts) that emerge from structural composition (⊗) of M3 primitives.

**Key insight:** Patterns like "Process", "Memory", "Feedback" appear across all domains (Biology, Computing, Economics, Physics) — M2 formalizes these as **structural grammar formulas**.

---

## 📐 Key Concepts

### 1. **GenericConcepts**

Abstract systemic patterns with three defining characteristics:

1. **Structural grammar formula** — composition of M3 primitives via monoidal product ⊗
2. **Transdisciplinary** — applies across multiple knowledge domains
3. **Instantiable at M0** — can be measured/evaluated in concrete systems

**Example:**
```
Process = D ⊗ It ⊗ F
- D (Dynamics): changes over time
- It (Information Territory): encodes state/content  
- F (Flow): movement/transformation
```

### 2. **Structural Grammar Formulas**

GenericConcepts are defined by **monoidal products** of M3 primitives:

**Notation:** Three equivalent representations
- **Standard:** `D ⊗ It ⊗ F` (Unicode, symbolic)
- **TeX:** `D \otimes I_t \otimes F` (LaTeX typesetting)
- **Raw Text:** `D (x) It (x) F` (plain text safe)

**Properties:**
- `m2:hasStructuralGrammarFormula` — standard notation
- `m2:hasStructuralGrammarFormulaTeX` — LaTeX variant
- `m2:hasStructuralGrammarFormulaRawText` — plain text variant

### 3. **It vs Im — Critical Distinction**

Both ASFID and REVOI have an "I" dimension — **M2 distinguishes them explicitly:**

| Symbol | Full Name | Grammar | Context | Meaning |
|--------|-----------|---------|---------|---------|
| **It** | Information (Territory) | Eagle (Gt) | ASFID | Encoded content, signals, data |
| **Im** | Interoperable (Map) | Sphinx (Gm) | REVOI | Integration capability, compatibility |

**Why critical:** Many GenericConcepts use **mixed formulas** (ASFID + REVOI), so ambiguity must be eliminated.

**Examples:**
- `Process = D ⊗ It ⊗ F` (pure ASFID)
- `Context = O ⊗ R ⊗ Im ⊗ E` (pure REVOI)
- `Layer = S ⊗ It ⊗ A ⊗ R` (mixed: ASFID + REVOI)

---

## 📊 Statistics (v15.18.0)

- **Total GenericConcepts:** 108
- **Families:** 10
- **Dual perspective:** 33 (exist in Territory AND Map)
- **Notation consistency:** 100% (all formulas use ⊗, all I disambiguated to It/Im)
- **Property definitions:** Fully formalized with owl:DatatypeProperty

---

## 🔄 Recent Changes

### v15.18.0 (2026-05-13) — **PROPERTY DEFINITION CLEANUP**
- Fixed property definition: `m2:hasTensorFormula` → `m2:hasStructuralGrammarFormula` (definition was not migrated)
- Renamed: `hasStructuralGrammarFormulaASCII` → `hasStructuralGrammarFormulaRawText` (84 occurrences)
- Ensures complete consistency: both property definitions AND usages now use "structural grammar" terminology

### v15.17.0 (2026-05-13) — **NOTATION UNIFICATION**
- Replaced → with ⊗ in 98 formula definitions across all perspectives
- Ensures consistent use of monoidal product notation (⊗) throughout structural grammar formulas
- Arrow notation (→) retained only for mathematical functors (e.g., `Cat_M3 → Cat_M2`) and logical implications in comments
- Completes notation consistency across entire M2 layer
- **Migrated from official repository v15.11.0**

### v15.16.0 (2026-05-13) — **NOTATION CORRECTIONS**
- Corrected ambiguous 'I' occurrences in eagleView/sphinxView formulas (replaced with 'It')
- Ensures full consistency with It/Im distinction across all GenericConcept perspectives

### v15.15.0 (2026-05-13) — **PROPERTY FORMALIZATION**
- Renamed property usages: `hasStructuralFormula` → `hasStructuralGrammarFormula` (+ TeX/ASCII variants)
- Added formal `owl:DatatypeProperty` definitions with `rdfs:comment` documentation
- Emphasizes Lambek Calculus foundation and monoidal product semantics

### v15.14.0 (2026-05-13) — **NOTATION CLARIFICATION**
- Systematic migration: `I` → `It` (Information Territory) in all primary formulas
- 54 GenericConcepts updated to distinguish from `Im` (Interoperable Map)
- Ensures unambiguous notation for dual/mixed Territory-Map concepts

### v15.13.0 (2026-05-13) — **TERMINOLOGY CLEANUP**
- Completed "tensor" → "monoidal product" migration (11 occurrences)
- Renamed properties: `tensorExpansion` → `structuralExpansion`, `tensorNote` → `structuralNote`

### v15.12.0 (2026-05-13) — **FORMALISM REFORM**
- Renamed tensor properties to structural grammar terminology
- `hasTensorFormula` → `hasStructuralGrammarFormula` (249 automated renames in usages)

---

## 🎯 Key Takeaways

1. **M2 = Transdisciplinary patterns** formalized as structural grammar formulas
2. **It/Im distinction is crucial** for bicephalous architecture
3. **108 GenericConcepts** spanning 10 families
4. **Monoidal products** (not tensor products) are the mathematical foundation
5. **100% notation consistency** achieved — properties fully defined and used consistently
6. **Three notation formats:** Standard (⊗), TeX (\otimes), RawText ((x))

**M2 is where TSCG's transdisciplinary power becomes explicit.** 🌟
