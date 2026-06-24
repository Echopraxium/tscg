# M2_GenericConcepts.jsonld

**Version:** 16.14.0
**Layer:** M2
**Type:** Generic Concepts Ontology
**Created:** 2026-01-14
**Last Modified:** 2026-06-23
**Author:** Echopraxium with the collaboration of Claude AI

---

## 🎯 Role

**M2_GenericConcepts** is the **middle layer** of TSCG — the bridge between
abstract M3 grammars and concrete M0 instances. It defines **transdisciplinary
systemic patterns** (GenericConcepts) that emerge from structural composition
of M3 primitive types via the three monoidal operators ×, +, and |.

**Key insight:** Patterns like "Process", "Memory", "Feedback" appear across
all domains (Biology, Computing, Economics, Physics) — M2 formalizes these
as **structural grammar formulas**.

---

## 📐 Three Primitive Alphabets in M2 Formulas — Base16

M2 formulas draw from all three M3 alphabets, **16 primitives total (Base16)**:

```
𝕋₀(×) = {A, S, F, I, D}        Territory (Eagle Eye / Gt)  — ASFID
𝕋₀(+) = {R, E, V, O, Im}       Map       (Sphinx Eye / Gm)  — REVOI
𝕋₀(|) = {T, _^, _$, K, Ss, L}  Stereopsis (Gs)             — TKSL + poles

𝕋₀ = 16 primitives total (Base16)
```

**Derived Gs elements (v16.14.0)** — not primitives, Base16 preserved:

```
_0  =  _^ | _$   (EquilibriumPole — see M3_BicephalousPerspective v1.3.0)
```

**Notation convention — hybrid formulas (with `|`):**

In any formula containing `|`, Territory types that could be confused with
Gs type `Ss` carry their monoid index:

| Symbol | Indexed | Why |
|---|---|---|
| `S` (Structure/Gt) | `St` | avoids confusion with `Ss` (Symbol/Gs) |
| `I` (Information/Gt) | `It` | avoids confusion with `Im` (Interoperability/Gm) |
| `O` (Observability/Gm) | `O` | no ambiguity — unchanged |

Pure intra-monoid formulas and ASFID/REVOI scoring terminology are **unaffected**.

---

## 📐 The Three Operators

### × — Territory structural product

```
D × I × F  =  Process
A × S × F  =  Homeostasis
S × I × A  =  Composition
```

### + — Map structural sum

```
O + R + Im + E  =  Context
V + E           =  Invariant (Map perspective)
```

### | — Stereopsic fusion (bicephalous)

```
A × St × It | R + O   =  Coherence
St × It × A | R        =  Layer
F × T                  =  Gradient      (Territory × Gs primitive T)
D × F | L              =  Bifurcation   (Gs primitive L)
It × Ss                =  Code          (Gs primitive Ss)
Ss × F | K             =  Language      (Gs primitives Ss + K)
A × S × F | _0         =  Balance       (DerivedGsElement _0)      ← v16.14.0
A × F × D | _0         =  TriadicBalance (DerivedGsElement _0)     ← v16.14.0
D × F × It | R + V + E =  Modelisation  (functionally stereopsic)  ← v16.14.0
```

**38 GenericConcepts** currently use `|` or a Gs primitive — including
11 dual-polarity pairs and 2 ternary-polarity concepts (v16.14.0).

---

## ⊕⊖ Dual-Polarity Formulas — `_^` and `_$`

**11 GenericConcepts** are defined as **dual-polarity pairs** — their formula takes
two forms, one per Gs pole primitive. The property `m2:hasStructuralGrammarFormula`
is stored as a **2-element array** `[formula | _^, formula | _$]`:

| Concept (pair) | `_^` pole | `_$` pole |
|---|---|---|
| Coherence / Incoherence | `A × St × It \| R + O \| _^` | `A × St × It \| R + O \| _$` |
| Amplification / Attenuation | `F × D × It \| R + O \| _^` | `F × D × It \| R + O \| _$` |
| Pattern (Recognition/Reuse) | `St × It × A \| K \| _^` | `St × It × A \| K \| _$` |
| Activation / Inhibition | `A × D \| _^` | `A × D \| _$` |
| Convergence / Divergence | `F × D \| _^` | `F × D \| _$` |
| Coding (Encoding/Decoding) | `It × St × D \| _^` | `It × St × D \| _$` |
| Fusion / Fission | `St × D \| _^` | `St × D \| _$` |
| Composition / Decomposition | `St × It × A \| _^` | `St × It × A \| _$` |
| Entropy / Negentropy | `F × It × D \| _^` | `F × It × D \| _$` |
| Synergy (Positive/Negative) | `It × D \| _^` | `It × D \| _$` |
| Potentialization / F-Depletion | `A × D × F \| _^` | `A × D × F \| _$` |

**Note Entropy:** `_^` = Entropy (natural disorder increase) / `_$` = Negentropy (artificial order).

## ⊕◎⊖ Ternary-Polarity — `_^`, `_0`, `_$`

**1 GenericConcept** (v16.14.0) uses the **DerivedGsElement `_0 = _^ | _$`** as its
equilibrium pole, producing a **ternary** polarity structure:

| Concept | `_^` pole | `_0` pole | `_$` pole |
|---|---|---|---|
| TriadicBalance | UnderConstrained (excess openness) | BalancedConstraint (optimal) | OverConstrained (excess rigidity) |

**Note Balance revision (v16.14.0):** `m2:Balance` formula revised from `A × S × F`
(Territory pure) to `A × S × F | _0` (stereopsic) — equilibrium is intrinsically
a Territory/Map correspondence phenomenon. `isStereopsic` updated to `true`.

---

## 🆕 v16.14.0 — Three New GenericConcepts

### m2:Balance (REVISED)

```
Formula (old): A × S × F
Formula (new): A × S × F | _0
isStereopsic:  false → true
hasPolarity:   neutral → dual
```

**Rationale**: Equilibrium is intrinsically a Territory/Map correspondence
phenomenon — the static equilibrium IS the point where Territory and Map
optimally correspond (`_0 = _^ | _$`). The Exposure Triangle poclet
(Balance's discovery context) confirms this: ISO/Aperture/Speed balance
exists only when the photographer's Map matches the Territory light conditions.

### m2:Modelisation (NEW)

```
Formula     : D × F × It | R + V + E
Family      : Dynamic
isStereopsic: true (FUNCTIONAL)
Polarity    : neutral
```

The process of constructing a Map from Territory observations — the M2
reification of the natural transformation Φ: Gt → Gm.

**Functionally stereopsic** — the only M2 concept whose stereopsic nature
is **constitutive** rather than incidental: its purpose IS the Territory→Map
traversal. Unlike structurally stereopsic concepts (formula crosses Gt/Gm
as a side-effect), Modelisation reifies the Φ operator itself.

```
D × F   =  Process heritage — directed temporal construction act
It      =  Territory information being captured
R+V+E   =  Map quality targets: Representable, Verifiable, Evolvable
```

**Distinct from:**
- `m2:Representation` (St×It|R) — the static MAP that results from modelisation
- `m2:Alignment` (I×A×S) — iterative bidirectional; Modelisation is directed
- `m2:Process` (D×F) — generic temporal unfolding without Territory→Map direction

**Ontological Overfitting link**: Modelisation is the process susceptible to
Ontological Overfitting — adding one M2 concept per phenomenon sacrifices
E (Evolvability) and V (Verifiability) for local R (Representability).
See `OntologicalOverfitting.md` in CoreHypotheses/.

**Validated ≥7 domains**: Science, Cartography, TSCG, Machine Learning,
Law, Medicine, Urbanism.

### m2:TriadicBalance (NEW)

```
Formula     : A × F × D | _0
Family      : Regulatory
isStereopsic: true
Polarity    : ternary (_^, _0, _$)
```

A system organisation pattern with three qualitatively distinct states:
two opposed excess poles and a central optimal state (`_0`) that is not
the absence of both poles but their **qualitative synthesis**.

```
_^   UnderConstrained  — insufficient constraint, excess openness
_0   BalancedConstraint — optimal calibration (_^ | _$ synthesis)
_$   OverConstrained   — excessive constraint, excess rigidity
```

The central state `_0` is an **Attractor** (`A`) — the system tends toward it
from both extremes via its own dynamic (`D`).

**Distinct from:**
- `m2:Balance` (A×S×F|_0) — static equilibrium STATE reached
- `m2:Homeostasis` (A×St×F|L) — actively maintained equilibrium via regulator
- `m2:Convergence` (F×D|_^) — geometric focusing, not 3-state topology

**Open question**: Does `_0` require a new Gs primitive (C=Calibration,
As=Adjustment, N=Normativity) for the degree of Territory/Map fit?
Deferred — Base16 preserved. Revisit when ≥3 M0 poclets demonstrate
insufficiency of `_0` as DerivedGsElement.

**Validated ≥7 domains**: Machine Learning, Mechanics, Management,
Immunology, TSCG Ontology, Ecology, Chemistry.

---

## 🔭 Gs Primitives in M2 — T, K, Ss, L

The 4 nominal Gs primitives (TKSL) each appear in M2 formulas as inter-grammar mediators:

| Primitive | Question | M2 usage | Example formula |
|---|---|---|---|
| **T** | When? | Temporal interface Gt↔Gm | `F × T` (Gradient) |
| **K** | What? | Cognitive contextualisation of It | `Ss × F \| K` (Language), `St × It × D \| K` (Agent), `St × It × A \| K` (Pattern), `F × It \| K` (Mediator), `Ss \| K` (Role) |
| **Ss** | Sign? | Semiotic bridge signifier↔signified | `It × Ss` (Code), `It × Ss \| V` (Signature), `St × Ss` (Relation), `St × F \| Ss` (Channel) |
| **L** | Converging? | Cybernetic convergence toward A | `St × It \| L` (Node/Component/Capacity), `St \| L` (Topology/Space/Constraint), `A × St × F \| L` (Homeostasis), `D × F \| L` (Bifurcation) |

T supersedes the former approximation `F × D / I × D` for Gradient by isolating
the temporal component precisely.

---

## 🔑 Critical: It vs Im Disambiguation

Both ASFID and REVOI have an "I" type — M2 distinguishes them explicitly:

| Symbol | Full Name | Grammar | Meaning |
|---|---|---|---|
| **I** (or It) | Information | Gt (Eagle) | Encoded content, state complexity |
| **Im** | Interoperable | Gm (Sphinx) | Integration capability, compatibility |

---

## 📊 Statistics (v16.14.0)

| Metric | Value |
|---|---|
| Total atomic GenericConcepts | 82 |
| GenericConcept combos | 4 |
| GenericConcept families | 9 |
| Bicephalous formulas (`\|`) | 38 |
| Gs primitives used | 6 + _0 (derived) |
| `isStereopsic=true` | 38 GenericConcepts |
| Dual-polarity pairs (`[f\|_^, f\|_$]`) | 11 |
| Ternary-polarity (`_^`, `_0`, `_$`) | 1 (TriadicBalance) |
| M3 primitives available | 16 — Base16 (𝕋₀) |
| Functionally stereopsic | 1 (Modelisation) |

---

## 🔭 m2:isStereopsic — Stereopsic Flag

**`m2:isStereopsic`** marks GenericConcepts whose structural formula uses
`|` or any Gs primitive (T, K, Ss, L, _^, _$, _0):

```
m2:isStereopsic = true   →  formula contains | or any of {T, K, Ss, L, _^, _$, _0}
m2:isStereopsic = false  →  formula is purely Territory (×) or Map (+)
```

**Functional vs structural stereopsic:**

```
Structural stereopsic  →  formula crosses Gt/Gm as a structural feature
                           (all 37 stereopsic concepts except Modelisation)

Functional stereopsic  →  concept's PURPOSE is the Territory→Map traversal
                           (m2:Modelisation only — reifies Φ: Gt→Gm)
```

---

## 🔬 M2 Phenomenological Stance

### M2 describes phenomena — not implementations

```
M3  →  Grammar     (what CAN exist — formal structure)
M2  →  Phenomenon  (what IS seen — observer perspective)
M1  →  Domain      (WHERE it appears — disciplinary context)
M0  →  Instance    (HOW it is built — concrete realization)
```

**At M2, structural formulas capture what an observer perceives as
constitutive of the phenomenon — not how it is physically realized.**

### The M2 Triple Filter (Anti-Ontological Overfitting)

Before admitting any candidate to M2, apply three sequential tests:

```
Test 1 — Decomposability   Can it be expressed as Fm2(C1, C2)?
                            IF YES → M1_CoreConcepts
Test 2 — Transdisciplinarity  Validated in ≥6 unrelated domains?
                            IF < 6 → M1_Domain extension
Test 3 — Atomicity         Formula adds genuinely new dimensional combination?
                            IF NO → Reject or reformulate
```

See `OntologicalOverfitting.md` (CoreHypotheses/) and
`tscg-m2-candidate-filter` skill for the full pipeline.

### ValueSpace is a frozen referential

A ValueSpace defines the observation frame — it is frozen at the moment
of observation. Therefore E (Evolvable) is **intentionally absent** from
ValueSpace: `It | V + O + R + Im`.

---

## 🏗️ Architecture Position

```
M3_GrammarFoundation (apex)
         ↓
M3_EagleEye + M3_SphinxEye + M3_BicephalousPerspective
         ↓ all imported by
M3_GenesisGrammar
         ↓ imported by
M2_GenericConcepts ← YOU ARE HERE
         ↓ imported by
M1_* extensions + M0_* instances
```

M2 accesses all M3 primitives (including T from Gs) **transitively**
via M3_GenesisGrammar — no direct import of M3_BicephalousPerspective needed.

---

## 🎯 Key Takeaways

1. **M2 = Transdisciplinary patterns** as structural grammar formulas
2. **Three operators** ×, +, | — three alphabets from three M3 grammars
3. **16 primitives (Base16)** in 𝕋₀ — ASFID(5) + REVOI(5) + TKSL+poles(6)
4. **It/Im distinction is crucial** for hybrid formulas
5. **Notation convention** — St/It in hybrid formulas; ASFID/REVOI unaffected
6. **38 stereopsic GenericConcepts** use `|` or a Gs primitive
7. **11 dual-polarity pairs** — `hasStructuralGrammarFormula` is a 2-element array
8. **1 ternary-polarity** — TriadicBalance with `_^/_0/_$` (v16.14.0)
9. **1 functionally stereopsic** — Modelisation reifies Φ: Gt→Gm (v16.14.0)
10. **_0 = _^ | _$** — DerivedGsElement, Base16 preserved (v16.14.0)
11. **Triple Filter** guards M2 against Ontological Overfitting

**M2 is where TSCG's transdisciplinary power becomes explicit.** 🌟

---

## 🔄 Changelog

| Version | Date | Changes |
|---|---|---|
| **16.14.0** | 2026-06-23 | REVISION: m2:Balance A×S×F → A×S×F\|_0 (isStereopsic=true). NEW: m2:Modelisation (D×F×It\|R+V+E, functionally stereopsic). NEW: m2:TriadicBalance (A×F×D\|_0, ternary polarity). DerivedGsElement _0=_^\|_$ introduced (M3_BicephalousPerspective v1.3.0). Anti-Ontological Overfitting Triple Filter documented. |
| **16.13.0** | 2026-05-28 | CLEANUP: m2:hasStructuralGrammarFormulaRawText and m2:hasStructuralGrammarFormulaTeX removed (83+82 nodes). Standard formula notation is now the sole representation. |
| **16.12.0** | 2026-05-28 | DUAL-POLARITY: 11 concepts updated. hasStructuralGrammarFormula → array [f\|_^, f\|_$]. 8 new stereopsic (Activation, Convergence, Coding, Fusion, Composition, Entropy, Synergy, Potentialization). isStereopsic total: 36. |

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — June 2026*
