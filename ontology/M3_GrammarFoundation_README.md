# M3_GrammarFoundation.jsonld

**Version:** 2.5.0  
**Layer:** M3  
**Type:** Apex Ontology — Mathematical Foundation  
**Created:** 2026-05-12  
**Last Modified:** 2026-07-23  
**Author:** Echopraxium with the collaboration of Claude AI
**Status:** Foundational — no imports

---


## ⚠️ Fm2 / Fm1m2 are FUNCTIONS, not morphisms (v2.4.0 — SC-1, 2026-07-12)

Two foundational errors, corrected in this version. Both had **propagated into the corpus**.

### Error 1 — they were declared morphisms

The file stated *"Fm2 is a morphism, not a monoidal operator"*, grouped `Fm2`/`Fm1m2` in an
`m2_morphisms` block with a `morphismFamily` property.

A **morphism composes**. An **emergence does not**. `Fm2`/`Fm1m2` combine named concepts to produce
semantics **irreducible to any subset of their arguments** — that is non-compositional, hence
**non-functorial**, hence **not a morphism**. (The word *functor* stays reserved for M0 dimension
evaluation `F_x : System -> Score`.)

**The family is now split, not purged** — this matters:

| | | |
|---|---|---|
| **Morphisms** | `Φ (Gt -> Gm)`, `Ψ (Gm -> Gt)` | structure-preserving — **they compose** |
| **Functions** | `Fm2`, `Fm1m2` | emergence — **they do not compose** |

`Φ` and `Ψ` are genuine morphisms and are untouched.

### Error 2 — `Fm1m2` was defined as "crossing the M1/M2 boundary" ← **the root error**

```
BEFORE   Fm1m2 : T1(M1) x T1(M2)^n -> T1     "Crosses the M1/M2 boundary"
AFTER    Fm1m2 : Domain+, GenericConcept+ -> DomainConceptCombo
```

This is where the corpus defect was born. `M1_CoreConcepts` v1.4.0 applied this definition
*faithfully*, "correcting" `Propagation` and `CascadeAmplification` from `Fm2` to `Fm1m2`
**"because the parent m1:Cascade is M1, not an M2 atomic"** — producing
`Fm1m2(Cascade, Duplication, Network)`, a domain-less `Fm1m2`.

What distinguishes `Fm1m2` is **domain qualification**, nothing else. An `Fm2` argument may
legitimately be a named concept from `M1_CoreConcepts`, so "crossing M1/M2" distinguishes **nothing**.

The `x` that separated the signature slots is also gone: **`x` is reserved to the Gt monoid and is
never overloaded** — not in signatures, not for domain conjunction.

Full rationale: `StructuralGrammar/Functional_Grammar_Model.md`.

---

## 🎯 Role

**M3_GrammarFoundation** is the **mathematical foundation** for all TSCG M3-level
grammars. It defines:

- Lambek Calculus formalism (free commutative monoidal categories)
- Three monoidal operators (×, +, |) with their neutral elements
- **Three primitive alphabets** — one per operator
- Abstract classes for M3 grammars and MonoidalTypes
- Special elements (EmptyTerritory, EmptyMap, StereopsisEmptySet,
  StereopsisUniversalSet)

This apex ontology **resolves circular dependencies** by providing a common
foundation imported by EagleEye, SphinxEye, Stereopsis, and GenesisGrammar.

---

## 📐 Three Primitive Alphabets — Base16

TSCG defines **three alphabets** — one per monoidal operator, **16 primitives total (Base16)**:

```
𝕋₀(×) = {A, St, F, It, D}           5 Territory primitives   (Eagle Eye  — ASFID)
𝕋₀(+) = {R, E, V, O, Im}           5 Map primitives         (Sphinx Eye — REVOI)
𝕋₀(|) = {T, _^, _$, K, Ss, L}       6 Stereopsis primitives  (Bicephalous — TKSL + poles)

𝕋₀ = 𝕋₀(×) ∪ 𝕋₀(+) ∪ 𝕋₀(|)  =  16 primitives total
```

| Alphabet | Operator | Neutral | Acronym | Perspective |
|---|---|---|---|---|
| 𝕋₀(×) | `×` | EmptyTerritory | **ASFID** | What systems ARE |
| 𝕋₀(+) | `+` | EmptyMap | **REVOI** | How models QUALIFY |
| 𝕋₀(\|) | `\|` | EmptyStereopsis | **TKSL** (+ poles _^/_$) | How Territory and Map CORRESPOND |

**Why 5-5-6 asymmetry?** Gs carries 6 primitives because the inter-grammar axis encodes
convergence discrimination (L) that presupposes both Gt and Gm to make sense.
The asymmetry is semantically justified, not an artefact.

### TKSL — Gs Nominal Primitives

The 4 nominal Gs primitives each answer a **transcendental question** about Territory/Map correspondence:

| Symbol | Name | Question | Theoretical Basis |
|---|---|---|---|
| **T** | Temporality | When? | Pure temporal interface Gt↔Gm |
| **K** | Knowledge | What? | Cognitive contextualisation of It into meaning |
| **Ss** | Symbol *(Stereopsic)* | Sign? | Semiotic bridge signifier(Gt)↔signified(Gm) — Peirce |
| **L** | Localizability | Converging? | Cybernetic convergence toward A — Wiener 1948, Ashby 1956 |

The poles **_^** (PositivePole) and **_$** (NegativePole) are polarity modifiers — they
mark onset/terminus of a conceptual pair but do not answer a transcendental question.

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
A × St × It | R + O | _^   =  Coherence    (positive pole)
A × St × It | R + O | _$   =  Incoherence  (negative pole)
```

`^op` was a vestige of tensor algebra — abandoned. `_^` and `_$` are proper primitives of 𝕋₀(|).

---

## 📏 Notation Convention — St / It / O in Hybrid Formulas

> ⚠️ **Stale notation rule (SC-2 target).** The convention stated below is the *old* hybrid-only rule (`S` bare in pure-Territory formulas, indexed only in formulas containing `|`). SC-2 replaces it: **`S` and `I` are always monoid-subscripted in every ATOM formula** (`St`/`Ss`, `It`/`Im`); `A`/`F`/`D` stay bare. Combos are unaffected (function arguments are named concepts, not primitives). Not corrected here — it is SC-2's first step, and the value must change at the source in the `.jsonld`.

**Rule:** In any formula containing `|` (hybrid/bicephalous formula), Territory and Map
types that could be ambiguous with new Gs type `Ss` carry their monoid index:

| Bare symbol | Indexed | Monoid | Used in |
|---|---|---|---|
| `S` | `St` | Territory (Gt) | Hybrid formulas only |
| `I` | `It` | Territory (Gt) | Hybrid formulas only |
| `O` | `O` | Map (Gm) | Hybrid formulas only |

```
HYBRID   (with |): A × St × F × It × D | V        ← St and It indexed
PURE Gt  (no |):   A × S × F × I × D              ← no change (ASFID unaffected)
SCORING           ASFID / REVOI terminology        ← no change
```

This convention is **backward-compatible** — only hybrid formulas are affected.

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
→ "empty of meaning" — contains ALL 16 types (Base16), discriminates nothing
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
3. **Three alphabets** — 𝕋₀(×), 𝕋₀(+), 𝕋₀(|) — **16 primitives total (Base16)**
4. **Three acronyms** — ASFID (Gt/5), REVOI (Gm/5), TKSL (Gs nominal/4) + poles _^/_$
5. **Three monoids** with explicit neutral elements
6. **Lambek Calculus** — free commutative monoidal categories
7. **Notation convention** — St/It/O in hybrid formulas (containing |)
8. **Minimal structure** — just enough, nothing artificial

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

If | could only operate within 𝕋₀(|) = {T, _^, _$, K, Ss, L}, it could not traverse
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

---

## Changelog

*(Derived from `owl:versionInfo` / `m3:changelog` in `M3_GrammarFoundation.jsonld`.)*

| Version | Date | Changes |
|---|---|---|
| **2.5.0** | 2026-07-23 | **`m3:changelog` DEFINED** (`owl:AnnotationProperty`). The `changelog` property was used corpus-wide but **declared nowhere**, in three competing spellings. Defined here, in the apex, so every lower layer (M2/M1/M0 — all importing M3) can use it as a legal downward reference. Also applied to this file: `m2:changelog` → `m3:changelog`, fixing a dependency inversion (M3 referencing M2) and a CTX-1 defect (`m2` prefix undeclared here). Aligned **in intent** with `adms:versionNotes`; no `rdfs:subPropertyOf` asserted (pending a decision on external vocabulary). **Known limits**: changelog entry objects still carry undeclared bare keys (`version`/`date`/`changes`) and stay invisible on expansion; this file still declares `@vocab = owl#`. Both deferred to the VOC worksite. |
| **2.4.1** | 2026-07-18 | @context hygiene fix (CTX): `m3` prefix made **absolute** (`.../ontology/M3_GenesisGrammar.jsonld#`) and `@base` repaired (`.../main/` → `.../main/ontology/`). Both were relative/malformed and, with `@vocab`=owl#, left every `m3:*` term (incl. `MonoidalType`) resolving against owl# instead of the M3 namespace. Data graph unchanged. |
| **2.4.0** | 2026-07-12 | SC-1 — `Fm2`/`Fm1m2` were declared **morphisms**; they are **functions** (emergence is non-compositional — arguments are combined, not associated). `Φ`/`Ψ` remain genuine morphisms (family split, not purged). Root error corrected: `Fm1m2` was defined as "crossing the M1/M2 boundary" — it is distinguished by **domain qualification**, nothing else. Signatures: `Fm2 : GenericConcept²⁺ → GenericConceptCombo`; `Fm1m2 : Domain⁺, GenericConcept⁺ → DomainConceptCombo`. The slot-separating `×` removed (`×` reserved to Gt). RENAME `m2:KnowledgeFieldConceptCombo → m2:DomainConceptCombo`. |
| **2.3.0** | 2026-07-12 | SC-1 — `DomainConceptCombo` re-defined by its `Fm1m2` formula (≥1 Domain + ≥1 GenericConcept), superseding the "parents from distinct domains" criterion. A combo's formula **is** its function signature; no monoidal formula/expansion. Arguments = named concepts (comma-juxtaposed), never primitives, never `×`/`+`/`\|`. `Fm1` does not exist. File formulas flagged by SHACL v1.1.0, repair deferred to SC-6. |
| **2.2.0** | 2026-05-27 | BASE16 EXTENSION: Gs alphabet 3 → 6 primitives — K (Knowledge, idx 3), Ss (Symbol/Stereopsic, idx 4), L (Localizability, idx 5). 𝕋₀ cardinality 13 → 16. TKSL acronym. Transcendental questions {T: When?, K: What?, Ss: Sign?, L: Converging?}. 5-5-6 asymmetry documented. |
| **2.1.0** | 2026-05-20 | OPERATOR MIGRATION: `⊗ⁱ` → `×`/`+`/`\|` (three explicit operators). `^opⁱ` → `_^`/`_$` (Gs poles). `⊗ⁱ⇒` removed (replaced by `Fm2`/`Fm1m2`). |
| **2.0.0** | 2026-05-20 | RENAME `m3:M3Dimension → m3:MonoidalType`. MonoidalType class defined. |
