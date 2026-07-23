# M3_BicephalousPerspective.jsonld

**Version:** 1.5.0
**Layer:** M3
**Type:** Stereopsis Grammar (Gs) — Reification of stereopsic synergy
**Created:** 2026-05-18
**Last Modified:** 2026-07-23
**Author:** Echopraxium with the collaboration of Claude AI

---

## 🎯 Role

**M3_Stereopsis** is the **reification of stereopsis** — the formal algebraic
structure that emerges from the mutual enrichment loop (Φ/Ψ) between Territory
Grammar Gt (Eagle Eye) and Map Grammar Gm (Sphinx Eye).

```
Stereopsis = the depth perception born from binocular fusion
           = what the two TSCG eyes create together
           = formally: the bicephalous monoid (Gs, |, EmptyStereopsis)
```

**Key insight:** The bicephalous architecture (Eagle Eye + Sphinx Eye) remains
the foundational metaphor — two eyes, two perspectives. Stereopsis is the
**synergy** that emerges from their fusion. Gs **reifies** that synergy as a
first-class algebraic structure with its own operator (|), neutral element
(EmptyStereopsis), and **Base16 primitive alphabet** — 6 primitives:
`{T, _^, _$, K, Ss, L}` (acronym: **TKSL** for the 4 nominal primitives + poles).

---

## 📐 Stereopsis Grammar Gs — Base16

**Bicephalous monoidal operator | :**
```
|  :  (Gt ∪ Gm ∪ Gs)_expr × (Gt ∪ Gm ∪ Gs)_expr  →  Gs_expr
```

| operates universally across all three grammars, always producing
a bicephalous (Gs) type expression.

**𝕋₀(|) = {T, _^, _$, K, Ss, L} — 6 primitives (Base16)**

| Idx | Symbol | Name | Question | Role |
|---|---|---|---|---|
| 0 | **T** | Temporality | When? | Temporal interface Gt↔Gm |
| 1 | **_^** | PositivePole | *(polarity)* | Onset/amplifying modifier |
| 2 | **_$** | NegativePole | *(polarity)* | Terminus/attenuating modifier |
| 3 | **K** | Knowledge | What? | Cognitive contextualisation of It |
| 4 | **Ss** | Symbol *(Stereopsic)* | Sign? | Semiotic bridge signifier↔signified |
| 5 | **L** | Localizability | Converging? | Cybernetic convergence toward A |

**TKSL acronym** — the 4 nominal Gs primitives (T, K, Ss, L). The poles _^/_$
are polarity modifiers and not included in the acronym.

**Example formulas (with St/It/O indexation):**
```
A × St × It | R + O | _^  =  Coherence      (bicephalous + positive pole)
F × T                      =  Gradient        (Territory × Gs primitive T)
It | V + O + R + Im       =  ValueSpace      (Territory | Map)
St × It | L                =  Node/Component  (structure+info, converging)
It × Ss                    =  Code            (information encoded as symbol)
Ss × F | K                 =  Language        (symbol-flow in knowledge context)
A × St × F | L             =  Homeostasis     (attractor+structure+flow, converging)
A × St × F | _0            =  Balance         (equilibrium — _0 = _^ | _$)
A × F × D | _0             =  TriadicBalance  (3-state optimum)
```

**Neutral element:** `m3:bicephalous:StereopsisEmptySet = EmptyTerritory | EmptyMap`

---

## 🆕 v1.3.0 — Derived Gs Elements

### DerivedGsElement — a new category

A **DerivedGsElement** is a named constant of the Gs monoide that is expressible
from primitives of 𝕋₀(|) via the `|` operator. It is **not a primitive** —
it does not extend Base16.

```
DerivedGsElement  ≠  new primitive
                  =  named expression in 𝕋₀(|)

Analogy in Gt:  F × D  names  m2:Process   (derived expression, not new primitive)
Analogy in Gs:  _^ | _$  names  _0         (derived element, not new primitive)
```

Base16 is **preserved** when adding DerivedGsElements.

### _0 — EquilibriumPole

```
_0  =  _^ | _$   (EquilibriumPole)
```

| Property | Value |
|---|---|
| Symbol | `_0` |
| Name | EquilibriumPole |
| Definition | `_^ | _$` |
| Type | `m3:DerivedGsElement` |
| Base16 impact | None — derived, not primitive |

**Semantics**: The stereopsic fusion of the two poles produces their synthesis —
not their average (quantitative) but their qualitative resolution.
The PositivePole (_^) encodes excess / onset; the NegativePole (_$) encodes
deficit / terminus. Their fusion `_0` encodes the **optimal calibration** between
Territory and Map — the point where neither excess nor deficit dominates.

**Triadic pattern** — the three states of any system with a qualitative optimum:

```
_^   →  Under-pole   (insufficient constraint, excess openness)
_0   →  Equilibrium  (_^ | _$  — qualitative optimum, emergent from tension)
_$   →  Over-pole    (excessive constraint, excess closure)
```

**Usage in M2:**
- `m2:Balance = A × St × F | _0` — static equilibrium state (Territory/Map optimal correspondence)
- `m2:TriadicBalance = A × F × D | _0` — structural topology with intrinsic 3-state optimum

**Open question (deferred)**: Does _0 require a new Gs primitive (C=Calibration,
As=Adjustment, N=Normativity) to fully encode the *degree* of Territory/Map fit?
Current solution (_0 as DerivedGsElement) is sufficient for the current M0 corpus.
Base16→Base17 transition requires ≥3 M0 poclets demonstrating insufficiency.

---

## 🔭 T — Temporality

**T (Temporality)** answers: *When?*

The temporal inter-grammar mediator — bridges Territory's dynamic `D` (state
evolution) with Map's recording of temporal observations. Key: `T` is a
**relational** primitive (bridges Gt↔Gm), unlike `D` which is pure Territory.

```
D  (Territory)  =  "the system state evolves"
T  (Gs)         =  "when does this Gt↔Gm correspondence occur?"
```

**Formula role**: `F × T = m2:Gradient` — the most common T-containing formula.
Gradient captures variation of a flux **in time** (temporal derivative F→Gm).

---

## 🔭 _^ and _$ — PositivePole and NegativePole

**_^ (PositivePole)** and **_$ (NegativePole)** are polarity modifiers.

They appear as suffixes in formula expressions:

```
expr | _^   →  positive/amplifying/onset pole
expr | _$   →  negative/attenuating/terminus pole
```

**Key distinction from T, K, Ss, L**: The poles are not inter-grammar
mediators answering a transcendental question — they are **polarity discriminators**
applied to an already-complete expression. Hence excluded from TKSL acronym.

**Derived element**: `_0 = _^ | _$` — the equilibrium pole (v1.3.0).

---

## 🔭 K — Knowledge

**K (Knowledge)** answers: *What?*

The cognitive inter-grammar mediator — contextualises raw Territory Information
(`It`) into Map-level meaning. K is the Gs primitive that formalises the
Bateson sense: *"a difference that makes a difference."*

```
It  (Territory)  =  raw data
K   (Gs)         =  "what does this It mean in a Map context?"
```

Theoretical basis: Maturana/Varela (cognition as enaction), Husserl
(intentionality), Peirce (interpretant), Bateson (meaningful difference).

---

## 🔭 Ss — Symbol (Stereopsic)

**Ss (Symbol/Stereopsic)** answers: *Sign?*

The semiotic inter-grammar mediator — the sign-relation between a Territory
entity (signifier) and a Map meaning (signified). Formalises Peirce's triad
(sign / object / interpretant) at the M3 level.

**Notation disambiguation (SC-2 rule, v1.5.0)**: `S` and `I` are **always**
monoid-subscripted in **every atom formula** — they are the only letters that collide
across the three grammars:

| Bare | Subscripted | Monoid | Meaning |
|---|---|---|---|
| `S` | `St` | Gt | Structure (Territory) |
| `S` | `Ss` | Gs | Symbol (Stereopsic) |
| `I` | `It` | Gt | Information (Territory) |
| `I` | `Im` | Gm | Interoperability (Map) |

`A`, `F` and `D` stay **bare** — no collision.

**Scope**: atom formulas only (`m2:hasStructuralGrammarFormula`). Combos carry a
function signature (`Fm2`/`Fm1m2`) whose arguments are **named concepts**, never
primitives — no subscript applies there. ASFID/REVOI scoring terminology is unaffected.

> **Retired rule (pre-v1.5.0)**: indexation used to be *context-dependent* — bare in
> pure-Territory formulas, indexed only in formulas containing `|`. That gave one
> primitive two spellings depending on its neighbours: ambiguous to read, impossible
> to check mechanically.

---

## 🔭 L — Localizability

**L (Localizability)** answers: *Converging?*

The cybernetic inter-grammar mediator — ordinal discrimination of convergence
direction toward an Attractor (A). L answers *converging or diverging?* without
requiring a metric (purely ordinal, not quantitative).

```
A  (Territory)  =  the goal state
V  (Map)        =  the model's verifiability
L  (Gs)         =  "is the system converging toward A as defined in the Map?"
```

Theoretical basis: Wiener (1948 cybernetics), Ashby (1956 regulation),
Conant & Ashby (good regulator theorem), Powers (perceptual control theory).

---

## 🔵 Special Elements

### Neutral element — StereopsisEmptySet

```
EmptyStereopsis  =  EmptyTerritory | EmptyMap   (neutral of |, δ₁ = max)
x | EmptyStereopsis  =  x  for all x
```

*Divergent Strabismus* — Territory and Map share nothing. Opposite of Universal.

### Pseudo-absorbent — StereopsisUniversalSet

```
StereopsisUniversalSet  =  𝕋₀(×) ∪ 𝕋₀(+) ∪ 𝕋₀(|)  =  all 16 Base16 primitives
StereopsisUniversalSet | a  =  StereopsisUniversalSet
```

*Convergent Strabismus* — degenerate limit: everything is said, nothing means
anything (Borges 1:1 map paradox). NOT a semantic ideal.

### DerivedGsElement — EquilibriumPole _0 (v1.3.0)

```
_0  =  _^ | _$   (EquilibriumPole — named derived constant)
```

See [v1.3.0 section](#-v130--derived-gs-elements) above.

---

## 🔭 Stereopsis Metaphor

Binocular vision creates **depth** from two slightly different flat images:
- Left eye (Eagle Eye / Territory) sees one perspective
- Right eye (Sphinx Eye / Map) sees another
- Brain fuses them → **depth perception** (stereopsis)

Analogously in TSCG:
- Eagle Eye measures Territory (ASFID)
- Sphinx Eye qualifies Map (REVOI)
- Stereopsis fuses them → **systemic depth** — understanding that exists
  in neither perspective alone

**Gs is this depth, formalized.**

---

## 📚 Key Takeaways

1. **Reification of stereopsis** — not a third head, but the formal algebraic
   structure of what two heads produce together
2. **Bicephalous monoid** (Gs, |, EmptyStereopsis) — closes the structural gap
3. **Base16 alphabet** — 𝕋₀(|) = {T, _^, _$, K, Ss, L} — **6 primitives**
4. **TKSL acronym** — 4 nominal Gs primitives (T, K, Ss, L), each answering
   a transcendental question
5. **5-5-6 asymmetry** — Gs has 6 primitives vs 5 for Gt/Gm; semantically justified
6. **Notation convention (SC-2)** — `S`/`I` always subscripted in every atom formula
   (`St`/`Ss`, `It`/`Im`); `A`/`F`/`D` bare; ASFID/REVOI scoring unaffected
7. **| is universal** — operates across all three grammars, always produces Gs types
8. **DerivedGsElement** (v1.3.0) — named Gs constants derived from primitives;
   Base16 preserved. First instance: `_0 = _^ | _$` (EquilibriumPole)
9. **Divergent/Convergent Strabismus** — documentation metaphors for Empty/Universal

**Stereopsis is where Territory and Map fuse into something neither is alone.** 🔭

---

## 📋 Changelog

| Version | Date | Changes |
|---|---|---|
| **1.5.0** | 2026-07-23 | **SC-2 STEP 1 — notation convention revised at the source.** `m3:notation_disambiguation` no longer states the retired hybrid-only rule. New rule: `S` and `I` are **always** monoid-subscripted in **every atom formula** (`St`/`Ss`, `It`/`Im`); `A`/`F`/`D` stay bare. Scope: atoms only — combo signatures take named concepts, not primitives. The old rule gave one primitive two spellings depending on its neighbours: ambiguous to read, unenforceable mechanically. Also corrected: the `m2:Balance` example read `A × S × F | _0`, now `A × St × F | _0`. Closes the contradiction opened by `M3_EagleEye` 2.10.0 (SC-2 step 2). NEXT: step 3 (SHACL `FormulaShape`), then step 4 (43 M2 atom formulas, gauge NOT-1 → 0). |
| **1.4.0** | 2026-07-23 | **VOC/B1 — 19 properties declared.** This file used **24 `m3:*` keys with 0 declared**; 19 are now `owl:AnnotationProperty`: `role`, `semantics`, `symbol`, `grammar`, `visual`, `usage`, `derivation`, `formula_role`, `independence`, `analogyInGt`, `analogyInGs`, `pairWith`, `triadicPattern`, `theoretical_basis`, `transcendentalQuestion`, `openQuestion`, `rejected_names`, `notation_note`, `notation_disambiguation`. **Declaration only** — no usage, no data changed. HELD: `definition`, `examples` (Family-A candidates → `skos:definition`/`skos:example`), `epistemicGap`. EXCLUDED: `typeSymbol`/`typeIndex` (already defined in `M3_GenesisGrammar` — would have been an STR-1 duplicate). FLAGGED: `pairWith` carries a string where an `@id` is expected (latent reference defect). Also `m2:changelog` → `m3:changelog` (layer inversion + CTX-1). |
| **1.3.1** | 2026-07-18 | @context hygiene fix (CTX): `m3` prefix made **absolute** (`.../ontology/M3_GenesisGrammar.jsonld#`). It was relative and, with `@vocab`=owl#, resolved `m3:*` terms (incl. `MonoidalType`) against owl# — desynchronising this file's IRIs from EagleEye/SphinxEye. Data graph unchanged. |
| **1.3.0** | 2026-06-23 | NEW: `m3:DerivedGsElement` class — named Gs constants derived from primitives, Base16 preserved. NEW: `_0 = _^ | _$` (EquilibriumPole) as first DerivedGsElement. Supports m2:Balance revision and m2:TriadicBalance (M2 v16.14.0). Open question documented: Base16→Base17 deferred. |
| **1.2.0** | 2026-05-27 | BASE16 EXTENSION: K (Knowledge), Ss (Symbol/Stereopsic), L (Localizability) added. TKSL acronym. Transcendental questions map. 5-5-6 asymmetry documented. St/It/O notation convention. |
| **1.1.0** | 2026-05-20 | PositivePole (_^) and NegativePole (_$) added as Gs type primitives. |
| **1.0.0** | 2026-05-18 | Initial release. T (Temporality) as first Gs primitive. |

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — June 2026*
