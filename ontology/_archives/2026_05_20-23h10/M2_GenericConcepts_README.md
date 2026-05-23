# M2_GenericConcepts.jsonld

**Version:** 16.10.7  
**Layer:** M2  
**Type:** Generic Concepts Ontology  
**Created:** 2026-01-14  
**Last Modified:** 2026-05-18

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

## 📐 Three Primitive Alphabets in M2 Formulas

M2 formulas draw from all three M3 alphabets:

```
𝕋₀(×) = {A, S, F, I, D}      Territory (Eagle Eye / Gt)
𝕋₀(+) = {R, E, V, O, Im}     Map       (Sphinx Eye / Gm)
𝕋₀(|) = {T, _^, _$}                   Stereopsis (Gs — reification of stereopsic synergy)

𝕋₀ = 13 primitives total
```

**Formula types:**

| Type | Example | Operator |
|---|---|---|
| Pure Territory | `D × I × F` (Process) | × only |
| Pure Map | `O + R + Im + E` (Context) | + only |
| Bicephalous | `A × S × I \| R + O` (Coherence) | × and + and \| |
| With Gs primitive | `F × T` (Gradient) | × with T |

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
A × S × It | R + O  =  Coherence
S × It × A | R      =  Layer
F × T              =  Gradient  (Territory × Gs primitive)
```

**10 GenericConcepts** currently use | in their primary formula:
Layer, Resource, Interoperability, Scope, Duplication, Identity,
ValueSpace, Amplification, Coherence, TopologicalDefect.

---

## 🔭 T — Stereopsis Primitive in M2

**T (Temporality)** is the first primitive of 𝕋₀(|) — defined in
`M3_BicephalousPerspective.jsonld`. It appears in M2 as the refined Gradient formula:

```
m2:Gradient  =  F × T   or   I × T

T = pure temporal interface between Territory and Map
  = irreducible bicephalous primitive (not derived from F, D, or Im)
```

T supersedes the former approximation `F × D / I × D` by isolating the
temporal component precisely. See `PotentialRefinements_MonoidalOperators.md`.

---

## 🔑 Critical: It vs Im Disambiguation

Both ASFID and REVOI have an "I" dimension — M2 distinguishes them explicitly:

| Symbol | Full Name | Grammar | Meaning |
|---|---|---|---|
| **I** (or It) | Information | Gt (Eagle) | Encoded content, state complexity |
| **Im** | Interoperable | Gm (Sphinx) | Integration capability, compatibility |

Examples:
```
Process    =  D × I × F        (pure Territory — I = Information)
Context    =  O + R + Im + E   (pure Map — Im = Interoperable)
Layer      =  S × It × A | R    (bicephalous — I = Information, R = Representable)
```

---

## 📊 Statistics (v16.10.6)

| Metric | Value |
|---|---|
| Total GenericConcepts | 80+ atomic, 8 combos |
| GenericConcept families | 9 |
| Bicephalous formulas (\|) | 10 |
| Gs primitive T used | 1 (m2:Gradient) |
| `isStereopsic=true` | 11 GenericConcepts |
| M3 primitives available | 11 (𝕋₀) |
| Notation formats | 3 (Standard, TeX, RawText) |


---

## 🔭 m2:isStereopsic — Stereopsic Flag

**`m2:isStereopsic`** is a boolean property marking GenericConcepts whose
structural formula uses the `|` operator or a Gs primitive (T):

```
m2:isStereopsic = true   →  formula contains | or T
m2:isStereopsic = false  →  formula is purely Territory (×) or Map (+)
```

### The 11 stereopsic GenericConcepts

| GenericConcept | Formula | Reason |
|---|---|---|
| Layer | `S × I × A \| R` | uses \| |
| Resource | `F × I \| R` | uses \| |
| Interoperability | `S × I × F \| V + E` | uses \| |
| Scope | `S × I × A \| R` | uses \| |
| Duplication | `S × I × F × D \| V` | uses \| |
| Identity | `S × I × A \| V + E` | uses \| |
| ValueSpace | `It \| V + O + R + Im` | uses \| |
| Amplification | `Ft × D × It \| R + O` | uses \| |
| Coherence | `A × S × I \| R + O` | uses \| |
| TopologicalDefect | `S × A × I \| R + O` | uses \| |
| **Gradient** | `F × T  or  I × T` | uses **T** (Gs primitive) |

### Usage

```sparql
# Find all stereopsic GenericConcepts
?concept m2:isStereopsic true .
```

Useful in `generate_index.js` (gallery filter), `TscgPocletMiner` (RAG),
and SHACL validation (formula ↔ flag consistency).


---

## 🔬 M2 Phenomenological Stance

### M2 describes phenomena — not implementations

The four TSCG layers have distinct epistemic orientations:

```
M3  →  Grammar     (what CAN exist — formal structure)
M2  →  Phenomenon  (what IS seen — observer perspective)
M1  →  Domain      (WHERE it appears — disciplinary context)
M0  →  Instance    (HOW it is built — concrete realization)
```

**At M2, structural formulas capture what an observer perceives as
constitutive of the phenomenon — not how it is physically realized.**

### Consequence: absent dimensions are often intentional

If an ASFID dimension is absent from a M2 formula, it likely belongs
to the implementation (M1/M0), not the observable phenomenon:

```
m2:Amplification  =  Ft × D × It | R + O
                      ↑
                      S (circuit structure) is ABSENT — intentional
                      The transistor, op-amp, enzymatic cascade are M0 realizations
                      The observer sees: signal × gain × information | measurable
```

Before adding a dimension to a M2 formula, ask:
> *"Would an observer perceive this dimension directly,
> or only after knowing the implementation?"*

### ValueSpace is a frozen referential

A ValueSpace defines the observation frame — it is frozen at the moment
of observation. A fluid referential makes measurements non-comparable:

```
ValueSpace v1  →  (re-evaluation)  →  ValueSpace v2
                   external process = NEW ValueSpace, not an evolution
```

Therefore E (Evolvable) is **intentionally absent** from ValueSpace:
`It | V + O + R + Im` — the ValueSpace does not generate predictions;
it provides the fixed frame within which observations are made.

See `ontology/docs/OntologyModeling_Guidelines.md` for the full set of
modeling rules.

---

## 🔄 Recent Changes

### v16.10.7 (2026-05-18) — **isStereopsic FLAG**
- Added `m2:isStereopsic` boolean property
- Set to `true` for 11 GenericConcepts using `|` or Gs primitive T
- Property definition includes `skos:definition`, `m2:stereopsicCriteria`

### v16.10.6 (2026-05-18) — **DESCRIPTION UPDATE**
- `dcterms:description` and `rdfs:comment` updated: 13 primitives (𝕋₀),
  Stereopsis Grammar Gs, T primitive, bicephalous architecture
- `m2:structuralSpace` updated to reflect full 𝕋₀
- `m2:categoryTheory` functors updated: F_×, F_+, F_|

### v16.10.5 (2026-05-18) — **GRADIENT REFINEMENT**
- `m2:Gradient` formula: `F × D / I × D` → `F × T / I × T`
- T (Temporality, 𝕋₀(|)) replaces D as temporal component
- `m2:hasDominantM3` updated to include `m3:stereopsis:Temporality`

### v16.10.4 (2026-05-18) — **GRADIENT FIX**
- Invalid `⊗₂F / ⊗₂I` notation replaced by `F × D / I × D`

### v16.10.3 (2026-05-18) — **OPERATOR REFORM**
- `⊗` → `×` (intra-ASFID), `+` (intra-REVOI), `|` (bicephalous boundary)
- 301 occurrences migrated. Formulas migrated: ×, +, | applied correctly

---

## 🏗️ Architecture Position

```
M3_GrammarFoundation (apex)
         ↓
M3_EagleEye + M3_SphinxEye + M3_Stereopsis
         ↓ all imported by
M3_GenesisGrammar
         ↓ imported by
M2_GenericConcepts ← YOU ARE HERE
         ↓ imported by
M1_* extensions + M0_* instances
```

M2 accesses all M3 primitives (including T from Gs) **transitively**
via M3_GenesisGrammar — no direct import of M3_Stereopsis needed.

---

## 🎯 Key Takeaways

1. **M2 = Transdisciplinary patterns** as structural grammar formulas
2. **Three operators** ×, +, | — three alphabets from three M3 grammars
3. **13 primitives** in 𝕋₀ — including T (Temporality) from Gs
4. **It/Im distinction is crucial** for bicephalous formulas
5. **10 bicephalous GenericConcepts** use | in their primary formula
6. **Gradient = F × T** — first M2 formula using a Gs primitive
7. **`m2:isStereopsic`** — boolean flag for GenericConcepts using `|` or T

**M2 is where TSCG's transdisciplinary power becomes explicit.** 🌟
