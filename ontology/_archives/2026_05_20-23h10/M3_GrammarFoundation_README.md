# M3_GrammarFoundation.jsonld

**Version:** 1.3.0  
**Layer:** M3  
**Type:** Apex Ontology — Mathematical Foundation  
**Created:** 2026-05-12  
**Last Modified:** 2026-05-18  
**Status:** Foundational — no imports

---

## 🎯 Role

**M3_GrammarFoundation** is the **mathematical foundation** for all TSCG M3-level
grammars. It defines:

- Lambek Calculus formalism (free commutative monoidal categories)
- Three monoidal operators (×, +, |) with their neutral elements
- **Three primitive alphabets** — one per operator
- Abstract classes for M3 grammars and dimensions
- Special elements (EmptyTerritory, EmptyMap, StereopsisEmptySet,
  StereopsisUniversalSet)

This apex ontology **resolves circular dependencies** by providing a common
foundation imported by EagleEye, SphinxEye, Stereopsis, and GenesisGrammar.

---

## 📐 Three Primitive Alphabets

TSCG defines **three alphabets** — one per monoidal operator:

```
𝕋₀(×) = {A, S, F, I, D}      Territory primitives   (Eagle Eye)
𝕋₀(+) = {R, E, V, O, Im}     Map primitives         (Sphinx Eye)
𝕋₀(|) = {T, _^, _$}                   Bicephalous primitives (Stereopsis)

𝕋₀ = 𝕋₀(×) ∪ 𝕋₀(+) ∪ 𝕋₀(|)  = 13 primitives total
```

| Alphabet | Operator | Neutral | Perspective |
|---|---|---|---|
| 𝕋₀(×) | `×` | EmptyTerritory | What systems ARE |
| 𝕋₀(+) | `+` | EmptyMap | How models QUALIFY |
| 𝕋₀(\|) | `\|` | EmptyStereopsis | How Territory and Map CORRESPOND |

---

## ⊗ Three Monoidal Operators

### × — Territory structural product (intra-ASFID)

```
D × I × F = Process      (Territory formula)
A × S × F = Homeostasis
```

**Axioms:**
```
(A × B) × C  =  A × (B × C)    associativity
A × B        =  B × A           commutativity
A × EmptyTerritory  =  A        neutral element
```

### + — Map structural sum (intra-REVOI)

```
R + E = ModelQuality    (Map formula)
O + R + Im + E = Context
```

**Axioms:** same structure as ×, over Map primitives.

### | — Stereopsic fusion (bicephalous, inter-space)

```
A × S | R + O = Coherence    (bicephalous formula)
F × T         = Gradient     (Territory × Bicephalous)
```

**Asymmetric:** left side = Territory/Bicephalous expression,
right side = Map/Bicephalous expression.

**Neutral element:** EmptyStereopsis = EmptyTerritory | EmptyMap

### _(removed — see PotentialRefinements_MonoidalOperators.md)_

```
_(×⇒ and +⇒ removed — no corpus usage. See PotentialRefinements_MonoidalOperators.md Refinement 8.)_
```

### _^ / _$ — Pole primitives (replaces former ^op)

```
A × S × It | R + O | _^   =  Coherence    (positive pole)
A × S × It | R + O | _$   =  Incoherence  (negative pole)
```

`^op` was a vestige of tensor algebra — abandoned. `_^` and `_$` are proper primitives of 𝕋₀(|).

---

## 🌀 Special Elements

| Element | Role | Visual | δ₁ |
|---|---|---|---|
| `EmptyTerritory` | Neutral of × | Black (no color) | — |
| `EmptyMap` | Neutral of + | Empty pentagon | — |
| `EmptyStereopsis` | Neutral of \| | Black + Empty pentagon | max |
| `StereopsisUniversalSet` | Perfect alignment | White + Full pentagon | 0 |

```
EmptyStereopsis        =  EmptyTerritory | EmptyMap          (neutral of |)
StereopsisUniversalSet =  𝕋₀(×) ∪ 𝕋₀(+) ∪ 𝕋₀(|) = 𝕋₀      (pseudo-absorbent of |)

StereopsisUniversalSet | a  =  StereopsisUniversalSet  for all a
→ "empty of meaning" — contains ALL types, discriminates nothing
→ Borges 1:1 paradox — a DEGENERATE LIMIT, not a semantic ideal
→ distinct from δ₁ ≈ 0 (SpectralClass Coherent — desirable alignment)

EmptyStereopsis        →  Divergent Strabismus  (δ₁ = max) — neutral
StereopsisUniversalSet →  Convergent Strabismus (δ₁ = 0)  — pseudo-absorbent
```

---

## 🏗️ Architecture Position

```
M3_GrammarFoundation ← YOU ARE HERE (apex — no imports)
         ↓ imported by
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
M3_Eagle  M3_Sphinx  M3_Stereo  M3_Genesis
(Gt/×)   (Gm/+)    (Gs/|)       (aggregates all)
    └────────┴──────────┴──────────┘
         ↓ imported by
    M2_GenericConcepts
```

---

## 📚 Why Monoidal (not Vectorial)?

TSCG uses **monoidal categories** because:

```
Monoidal Category ← TSCG uses this
    ↓ add structure
Group
    ↓ add scalar field
Module / Vector Space
    ↓ add inner product
Hilbert Space  ← former (abandoned) TSCG formalism
```

Monoidal categories are **minimal** — just enough for composition, nothing
artificial. No scalar multiplication, no metric, no inner product required.

---

## 📚 Key Takeaways

1. **Apex ontology** — imported by all M3 grammars, no dependencies
2. **Three operators** × (Territory), + (Map), | (Stereopsis)
3. **Three alphabets** — 𝕋₀(×), 𝕋₀(+), 𝕋₀(|) — 13 primitives total
4. **Three monoids** with explicit neutral elements
5. **Lambek Calculus** — free commutative monoidal categories
6. **Minimal structure** — just enough, nothing artificial

**M3_GrammarFoundation is where TSCG's mathematical rigour becomes explicit.** 🌟

---

## Intra-grammar vs Inter-grammar Operators

### The asymmetry of |

```
× : intra-grammar  →  operates within Gt, result stays in Gt
+ : intra-grammar  →  operates within Gm, result stays in Gm
| : inter-grammar  →  connects Gt, Gm and Gs — result always in Gs
```

× and + are **closed** within their grammar.
| is **open** — its constitutive role is to cross the Gt/Gm boundary.

### This is NOT tensor algebra or multi-sorted algebra

This asymmetry is explained **entirely within the Lambek calculus /
free monoidal grammar framework** — no tensor product, no algebraic
structure beyond free monoids is needed or assumed.

| is simply a monoidal product whose domain spans multiple grammars —
exactly as stereopsic fusion spans both Territory (Eagle Eye) and
Map (Sphinx Eye) to produce the Bicephalous Perspective.

### Why | must be inter-grammar

If | could only operate within 𝕋₀(|) = {T, _^, _$}, it could not traverse
the Gt/Gm boundary — and it would lose its constitutive role as
the stereopsic fusion operator. The asymmetry is **intentional and
necessary**, not a privilege.

### Coherence constraint

| always produces a type of Gs — never Territory nor Map:

```
expr_Gt | expr_Gm  →  Gs type  ✓
expr_Gs | expr_Gm  →  Gs type  ✓
expr_Gt | expr_Gs  →  Gs type  ✓
```

This constraint preserves well-definedness despite | being inter-grammar.
