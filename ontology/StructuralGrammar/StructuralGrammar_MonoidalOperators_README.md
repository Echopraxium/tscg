# TSCG Structural Grammar — Monoidal Operators & Symbolic Alphabet

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-05-18  
**Framework**: TSCG (Transdisciplinary System Construction Game) v16.0.0+  
**Status**: Foundational — M3 Level  

---

## Table of Contents

1. [Overview](#overview)
2. [Guiding Principle: Metaphor First, Formalism Second](#guiding-principle)
3. [The Two Alphabets](#the-two-alphabets)
4. [The Three Operators](#the-three-operators)
5. [The Three Monoids](#the-three-monoids)
6. [Special Elements](#special-elements)
7. [Visual Representation](#visual-representation)
8. [Notation Examples](#notation-examples)
9. [Migration from ⊗ Notation](#migration-from--notation)

---

## Overview

This document formalizes the **monoidal operator system** of TSCG Structural
Grammar, replacing the former single `⊗` operator (with or without subscripts)
with three distinct operators: `×`, `+`, and `|`.

This reform introduces:
- Two typed **symbolic alphabets** (ASFID and REVOI)
- Three **monoidal operators** with explicit neutral elements
- A **symbolic grammar** combining color and shape intuitively
- A set of **special elements** grounded in stereopsis metaphor

> **Anti-bullshit principle**: This document does not claim a semi-ring or any
> algebraic structure beyond three monoids. The symbolic foundation stands on
> its own. Mathematical formalism is the "cherry on top", not the foundation.

---

## Guiding Principle: Metaphor First, Formalism Second

TSCG is built on a **bicephalous architecture**:

| Eye | Acronym | Perspective | Metaphor |
|---|---|---|---|
| 🦅 Eagle Eye | **ASFID** | Territory (empirical reality) | **Colors** |
| 🦁 Sphinx Eye | **REVOI** | Map (cognitive model) | **Shapes / Sectors** |

The key insight: **colors** are intrinsic properties of objects (perceived
sensorially), while **shapes** are cognitive structures projected onto reality
(perceived mentally). This mirrors the Territory/Map distinction exactly.

**Stereopsis** — the fusion of two slightly different images (one per eye) to
create depth perception — is the central metaphor for how TSCG combines ASFID
and REVOI into systemic understanding.

---

## The Two Alphabets

### Alphabet ASFID — Colors (6 types)

Colors represent **empirical properties** of the Territory (Eagle Eye).
Additive synthesis (light): combining colors *enriches*.

| # | Type | Color | ASFID Dimension |
|---|---|---|---|
| 0 | `m3:EmptyTerritory` | **Black** | Neutral element of `×` |
| 1 | A | **White** | Attractor |
| 2 | S | **Blue** | Structure |
| 3 | F | **Red** | Flow |
| 4 | I | **Orange** | Information |
| 5 | D | **Green** | Dynamics |

> Color assignments A, S, F, D inspired by Magic: The Gathering color philosophy
> (White=order/equilibrium, Blue=intellect/structure, Red=energy/movement,
> Green=growth/evolution). Orange added for Information (communication, exchange).

**Black** is reserved as `m3:EmptyTerritory` — the absence of any empirical
property. It belongs to no ASFID dimension.

### Alphabet REVOI — Pentagon Sectors (6 types)

Sectors represent **cognitive structures** of the Map (Sphinx Eye).
Each sector is one of the 5 triangular regions obtained by drawing lines from
the center to each vertex of a regular pentagon.

| # | Type | Shape | REVOI Dimension |
|---|---|---|---|
| 0 | `m3:EmptyMap` | **Empty pentagon** | Neutral element of `+` |
| 1 | R | Sector 1 | Representability |
| 2 | E | Sector 2 | Evolvability |
| 3 | V | Sector 3 | Verifiability |
| 4 | O | Sector 4 | Observability |
| 5 | I | Sector 5 | Interoperability |

**Empty pentagon** (no sectors, no dividing lines) is `m3:EmptyMap` — the
absence of any epistemic property.

---

## The Three Operators

| Operator | Space | Meaning | Replaces |
|---|---|---|---|
| `×` | intra-ASFID | Structural product of colors | `⊗` (Territory) |
| `+` | intra-REVOI | Structural sum of sectors | `⊗` (Map) |
| `\|` | ASFID → REVOI | Stereopsic fusion (bicephalous) | *(new)* |

### `×` — Structural Product (Territory)

Operates within ASFID. Combines color-types into compound Territory expressions.
Additive synthesis: combining colors produces new colors.

```
A × S        →  White + Blue = Cyan  (Attractor + Structure)
D × F        →  Green + Red = Yellow (Dynamics + Flow)
A × S × F   →  compound Territory expression
```

### `+` — Structural Sum (Map)

Operates within REVOI. Displays multiple sectors simultaneously.

```
R + E        →  Sectors 1 and 2 active (Representability + Evolvability)
V + O + I   →  Sectors 3, 4, 5 active
```

### `|` — Stereopsic Fusion (Bicephalous)

Bridges Territory and Map. Interpreted as **union**: each side contributes
its own properties. This is the mathematical expression of stereopsis —
the fusion of Eagle Eye and Sphinx Eye into systemic depth perception.

```
A × S | R         →  Attractor+Structure (Territory) fused with Representability (Map)
F | V + O         →  Flow (Territory) fused with Verifiability+Observability (Map)
A × S × F | R + E →  complex bicephalous expression
```

---

## The Three Monoids

Each operator defines a monoid — a set with one associative operator and one
neutral element. **This is the extent of the algebraic claim.**

```
(ASFID,        ×,  m3:EmptyTerritory)   →  Territory Monoid
(REVOI,        +,  m3:EmptyMap)          →  Map Monoid
(ASFID×REVOI,  |,  m3:StereopsisEmptySet) →  Bicephalous Monoid
```

### Neutral elements verification

```
m3:EmptyTerritory × A  =  A    ✓  (Black adds no color)
A × m3:EmptyTerritory  =  A    ✓

m3:EmptyMap + R  =  R          ✓  (Empty pentagon adds no sector)
R + m3:EmptyMap  =  R          ✓

m3:StereopsisEmptySet | expr  =  expr  ✓
expr | m3:StereopsisEmptySet  =  expr  ✓
```

---

## Special Elements

### Neutral Elements (one per operator)

| Element | Operator | Visual | Meaning |
|---|---|---|---|
| `m3:EmptyTerritory` | `×` | Black | No empirical property |
| `m3:EmptyMap` | `+` | Empty pentagon | No epistemic property |
| `m3:StereopsisEmptySet` | `\|` | Black \| Empty pentagon | No stereopsis possible |

Fundamental relation:
```
m3:StereopsisEmptySet  =  m3:EmptyTerritory | m3:EmptyMap
```

### Limit Elements (semantic, not algebraic)

These are **TSCG semantic concepts**, not algebraic special elements:

#### `m3:StereopsisUniversalSet`
- **δ₁ = 0** — perfect Map/Territory alignment (1:1 case, Borges paradox)
- Documentation metaphor: **Convergent Strabismus**
  > Both eyes converge on exactly the same focal point — Territory and Map
  > describe the same reality with zero epistemic gap.
- SpectralClass: `Coherent` (limit case, δ₁ = 0 strictly)

#### `m3:StereopsisEmptySet`
- **δ₁ = max** — Map/Territory intersection is empty
- Documentation metaphor: **Divergent Strabismus**
  > Both eyes look in opposite directions — Territory and Map share no
  > common point. No stereopsis is possible.
- SpectralClass: `Incoherent` (limit case, δ₁ = maximum)
- Also serves as neutral element of `|`

---

## Visual Representation

### A Face of the Systemic Die

Each poclet is represented as a **5-faced die** (square-base pyramid).
Each face encodes both alphabets simultaneously:

```
┌─────────────────────┐
│   ASFID COLOR        │  ← Eagle Eye / Territory (color of the face)
│   ┌─────────┐        │
│   │  ██████ │        │  ← Black circle (pupil)
│   │ ╱  ╲   │        │
│   │╱ pen ╲  │        │  ← Pentagon with active sectors (white on black)
│   │╲ tagon╱ │        │
│   │ ╲  ╱   │        │
│   └─────────┘        │
└─────────────────────┘
```

**Reading a face:**
- **Color surrounding the circle** → dominant ASFID dimension (Eagle Eye)
- **Black circle** → the "pupil" — necessary darkness for perception
- **White pentagon sectors** → active REVOI dimensions (Sphinx Eye)

> The face is literally an **eye**: iris (ASFID color) + pupil (black) +
> retina (REVOI pentagon). Bicephaly made anatomically visible.

### The Square-Base Pyramid

| Face | ASFID Dimension | Color |
|---|---|---|
| Square base | S (Structure) | Blue |
| Lateral face 1 | A (Attractor) | White |
| Lateral face 2 | F (Flow) | Red |
| Lateral face 3 | I (Information) | Orange |
| Lateral face 4 | D (Dynamics) | Green |

### The Pentagon

5 triangular sectors (center → vertex lines), one per REVOI dimension:

```
        V (Sector 3)
       /|\
      / | \
    E   |   O
  (2)   |   (4)
    \   |   /
     \  |  /
      R   I
     (1) (5)
```

### Special Visual Encodings

```
m3:StereopsisEmptySet    →  All faces black + empty pentagon
m3:StereopsisUniversalSet →  All faces white + all sectors filled
```

---

## Notation Examples

### Pure Territory expressions
```
A × S          →  Attractor + Structure
D × F × I      →  Dynamics + Flow + Information
```

### Pure Map expressions
```
R + E          →  Representability + Evolvability
V + O + I      →  Verifiability + Observability + Interoperability
```

### Bicephalous (hybrid) expressions
```
A × S | R            →  Territory(A,S) fused with Map(R)
F | V + O            →  Territory(F) fused with Map(V,O)
A × S × F | R + E    →  Territory(A,S,F) fused with Map(R,E)
```

### Reading `|` expressions
The `|` operator is **asymmetric**: left side is always Territory (ASFID),
right side is always Map (REVOI). There is no ambiguity.

---

## Migration from ⊗ Notation

The former `⊗` operator (with or without subscripts ₜ/ₘ) is replaced by
`×`, `+`, and `|` according to the following rules:

| Former notation | New notation | Rule |
|---|---|---|
| `D ⊗ It ⊗ F` | `D × It × F` | All ASFID → `×` |
| `O ⊗ R ⊗ Im ⊗ E` | `O + R + Im + E` | All REVOI → `+` |
| `S ⊗ It ⊗ A ⊗ R` | `S × It × A \| R` | Mixed → `\|` at boundary |

**Migration rule**: identify the boundary between the last ASFID symbol and
the first REVOI symbol — insert `|` there. Replace all `⊗` on the left
with `×`, all `⊗` on the right with `+`.

This migration applies to:
- `M3_GenesisGrammar.jsonld` (operator definitions — migrate first)
- `M2_GenericConcepts.jsonld` (GenericConcept formulas)
- `M0_*.jsonld` instances (if hybrid formulas present)

---

## Summary

| Concept | Value |
|---|---|
| Territory alphabet | 6 types: EmptyTerritory + {A, S, F, I, D} |
| Map alphabet | 6 types: EmptyMap + {R, E, V, O, I} |
| Operators | `×` (Territory), `+` (Map), `\|` (Bicephalous) |
| Algebraic claim | Three monoids — nothing more |
| Neutral of `×` | `m3:EmptyTerritory` (Black) |
| Neutral of `+` | `m3:EmptyMap` (Empty pentagon) |
| Neutral of `\|` | `m3:StereopsisEmptySet` (δ₁ = max) |
| Convergence limit | `m3:StereopsisUniversalSet` (δ₁ = 0) |
| Visual encoding | 5-faced die: color (ASFID) + pentagon sectors (REVOI) |
| Documentation metaphor | Convergent/Divergent Strabismus |

---

## Update v1.1.0 — Bicephalous Alphabet (2026-05-18)

### Decision

A **third primitive alphabet** is formally declared — the Bicephalous Alphabet —
alongside the Territory and Map alphabets.

### The three alphabets

```
Alphabet ×  =  {A, S, F, I, D}      6 types (5 primitives + EmptyTerritory)
Alphabet +  =  {R, E, V, O, Im}     6 types (5 primitives + EmptyMap)
Alphabet |  =  {T}                   2 types (1 primitive + EmptyStereopsis)
```

### T — Temporality (first bicephalous primitive)

T is the first member of the Bicephalous Alphabet, defined by stereopsic
equivalence:

```
T  :=  F | Im  ≡  D | Im
```

**Justification**: Im (Interoperability/Map) is the synchronisation lens.
Applied to F (flux-temporality) or D (evolution-temporality), it extracts
the same pure temporal interface — the synchronisation that underlies both.

**Consequence for Gradient**:

```
m2:Gradient  =  F × T   or   I × T   (preferred)
             =  F × D   or   I × D   (current approximation)
```

### Why this matters

Without its own alphabet, | would be merely a cartesian product operator
(juxtaposing pairs), not a genuine third monoid. The Bicephalous Alphabet
gives | proper monoid status: stereopsis genuinely creates new types that
exist in neither Territory nor Map alone.

### Open members

Further bicephalous primitives will emerge from poclet corpus analysis —
not from systematic search. The corpus drives discovery, as it did for
ASFID and REVOI.

---

## Clarification v1.2.0 — Intra-grammar vs Inter-grammar Operators

### The asymmetry of |

An apparent asymmetry exists between the three operators:

```
× : intra-grammar — operates within Gt, result stays in Gt
+ : intra-grammar — operates within Gm, result stays in Gm
| : inter-grammar — connects Gt, Gm and Gs, result always in Gs
```

### Why this is correct in the Lambek / free monoidal grammar framework

× and + are **closed** monoidal products — each one stays inside its own
grammar. | is **open** by definition — its constitutive role is to connect
two structurally separate grammars (Gt and Map Gm) to produce types in Gs.

If | could only operate on 𝕋₀(|) = {T}, it could not traverse the
Gt/Gm boundary — it would lose its defining purpose.

```
× and +  →  intra-grammar operators  (closed within their grammar)
|        →  inter-grammar operator   (traverses grammars → always produces Gs)
```

### What this is NOT

This asymmetry is explained **entirely within the Lambek calculus /
free monoidal grammar framework**. No tensor algebra, no multi-sorted
algebra, no algebraic structure beyond monoids is needed or assumed.

The | operator is simply a monoidal product whose domain spans multiple
grammars — exactly as the stereopsic fusion of Eagle Eye and Sphinx Eye
spans both Territory and Map to produce the Bicephalous Perspective.

### Constraint that preserves coherence

| always produces a type of Gs — never T nor M. This ensures the system
remains well-defined despite | being inter-grammar:

```
expr_Gt | expr_Gm  →  Gs type  ✓
expr_Gt | expr_Gs  →  Gs type  ✓
expr_Gs | expr_Gm  →  Gs type  ✓
expr_Gs | expr_Gs  →  Gs type  ✓
```

---

## The Cell Membrane Analogy — Why | Traverses the Boundary

### Intuition

The inter-grammar nature of | can be understood through the analogy of a
**cell membrane** — the interface between the interior (cytoplasm) and
exterior of a biological cell.

```
Interior (cytoplasm)     ≈  Territory Grammar Gt  (Eagle Eye / ASFID)
Exterior (environment)   ≈  Map Grammar Gm         (Sphinx Eye / REVOI)
Cell membrane            ≈  Operator |              (Stereopsic fusion)
```

### Why the cell membrane — not just an osmotic membrane

A simple osmotic membrane passively lets water through by gradient.
The cell membrane is **active** — it generates its own functionalities:

| Cell membrane component | Correspondence in TSCG |
|---|---|
| Ion channels (selective, temporally gated) | T (Temporality) — first Gs primitive |
| Surface proteins (recognition, signalling) | Future Gs primitives |
| Pumps (transport against gradient) | Ψ : Gm → Gt (reverse osmosis / interpretation) |
| Passive diffusion | Φ : Gt → Gm (osmosis / observation) |

### The key insight

> | is not a *crossing point* in the Territory/Map boundary —
> it IS the boundary, with its own active functionalities.

The primitives of 𝕋₀(|) = {T, ...} are the "surface proteins" of this
interface — types that exist **in the membrane itself**, neither in
Territory nor in Map alone.

### Osmosis / Reverse Osmosis poclet (planned)

```
Osmosis          →  Φ : Gt → Gm   (natural flow, Territory → Map)
Reverse osmosis  →  Ψ : Gm → Gt   (imposed flow, Map → Territory)
```

This would be the first poclet directly modelling the Φ/Ψ bicephalous dynamics.
