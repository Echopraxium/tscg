# M2_GenericConcepts.jsonld

**Version:** 16.13.0  
**Layer:** M2  
**Type:** Generic Concepts Ontology  
**Created:** 2026-01-14  
**Last Modified:** 2026-05-28

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
𝕋₀(×) = {A, S, F, I, D}      Territory (Eagle Eye / Gt)  — ASFID
𝕋₀(+) = {R, E, V, O, Im}     Map       (Sphinx Eye / Gm)  — REVOI
𝕋₀(|) = {T, _^, _$, K, Ss, L}  Stereopsis (Gs)           — TKSL + poles

𝕋₀ = 16 primitives total (Base16)
```

**Notation convention — hybrid formulas (with `|`):**

In any formula containing `|`, Territory types that could be confused with
new Gs type `Ss` carry their monoid index:

| Symbol | Indexed | Why |
|---|---|---|
| `S` (Structure/Gt) | `St` | avoids confusion with `Ss` (Symbol/Gs) |
| `I` (Information/Gt) | `It` | avoids confusion with `Im` (Interoperability/Gm) |
| `O` (Observability/Gm) | `O` | no ambiguity — unchanged |

Pure intra-monoid formulas and ASFID/REVOI scoring terminology are **unaffected**.

**Formula types:**

| Type | Example | Operator |
|---|---|---|
| Pure Territory | `D × I × F` (Process) | × only |
| Pure Map | `O + R + Im + E` (Context) | + only |
| Bicephalous | `A × St × It \| R + O` (Coherence) | × and + and \| |
| With Gs primitive | `F × T` (Gradient), `It × Ss` (Code), `St \| L` (Topology) | × or \| with Gs type |

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
A × St × It | R + O  =  Coherence
St × It × A | R      =  Layer
F × T                =  Gradient  (Territory × Gs primitive T)
D × F | L            =  Bifurcation  (Gs primitive L)
It × Ss              =  Code         (Gs primitive Ss)
Ss × F | K           =  Language     (Gs primitives Ss + K)
```

**36 GenericConcepts** currently use `|` or a Gs primitive (K, Ss, L, T) — including the 11 dual-polarity pairs (see below).

---

## ⊕⊖ Dual-Polarity Formulas — `_^` and `_$`

**11 GenericConcepts** are defined as **dual-polarity pairs** — their formula takes
two forms, one per Gs pole primitive. The property `m2:hasStructuralGrammarFormula`
is stored as a **2-element array** `[formula | _^, formula | _$]` :

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

**Note Entropy :** `_^` = Entropy (augmentation naturelle du désordre) / `_$` = Negentropy (ordre artificiel).

All 11 dual-polarity concepts have `m2:isStereopsic = true` (formula contains `|`).

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

Examples:
```
Process    =  D × I × F        (pure Territory — I = Information)
Context    =  O + R + Im + E   (pure Map — Im = Interoperable)
Layer      =  S × It × A | R    (bicephalous — I = Information, R = Representable)
```

---

## 📊 Statistics (v16.13.0)

| Metric | Value |
|---|---|
| Total GenericConcepts | 75 atomic, 8 combos |
| GenericConcept families | 9 |
| Bicephalous formulas (`\|`) | 36 |
| Gs primitives used | 6 (T, _^, _$, K, Ss, L) |
| `isStereopsic=true` | 36 GenericConcepts |
| Dual-polarity pairs (`[f\|_^, f\|_$]`) | 11 |
| M3 primitives available | 16 — Base16 (𝕋₀) |
| Formula notation | 1 (Standard — `×`, `+`, `\|`) |


---

## 🔭 m2:isStereopsic — Stereopsic Flag

**`m2:isStereopsic`** marks GenericConcepts whose structural formula uses
`|` or any Gs primitive (T, K, Ss, L):

```
m2:isStereopsic = true   →  formula contains | or any of {T, K, Ss, L}
m2:isStereopsic = false  →  formula is purely Territory (×) or Map (+)
```

### The 36 stereopsic GenericConcepts (v16.13.0)

**Original 11 (`|` operator):** Layer, Resource, Interoperability, Scope,
Duplication, Identity, ValueSpace, Amplification, Coherence, TopologicalDefect, Gradient (T)

**17 (Base16 extension — K, Ss, L):**

| GenericConcept | Formula | Gs primitive |
|---|---|---|
| Code | `It × Ss` | Ss |
| Signature | `It × Ss \| V` | Ss |
| Relation | `St × Ss` | Ss |
| Channel | `St × F \| Ss` | Ss |
| Language | `Ss × F \| K` | Ss + K |
| Role | `Ss \| K` | Ss + K |
| Agent | `St × It × D \| K` | K |
| Pattern | `St × It × A \| K` | K |
| Mediator | `F × It \| K` | K |
| Node | `St × It \| L` | L |
| Component | `St × It \| L` | L |
| Capacity | `St × It \| L` | L |
| Topology | `St \| L` | L |
| Space | `St \| L` | L |
| Constraint | `St \| L` | L |
| Homeostasis | `A × St × F \| L` | L |
| Bifurcation | `D × F \| L` | L |

**8 (Polar extension — `_^`/`_$` added):**
Activation, Convergence, Coding, Fusion, Composition, Entropy, Synergy, Potentialization

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

### Consequence: absent types are often intentional

If an ASFID types is absent from a M2 formula, it likely belongs
to the implementation (M1/M0), not the observable phenomenon:

```
m2:Amplification  =  F × D × It | R + O
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

See `CLAUDE.md` for the full set of modeling rules and conventions.

---

## 🔄 Recent Changes

### v16.13.0 (2026-05-28) — **CLEANUP: RawText & TeX removed**
- `m2:hasStructuralGrammarFormulaRawText` supprimée (83 valeurs + nœud `owl:DatatypeProperty`)
- `m2:hasStructuralGrammarFormulaTeX` supprimée (82 valeurs + nœud `owl:DatatypeProperty`)
- La formule standard (`×`, `|`, `St`, `It`) est désormais la seule représentation

### v16.12.0 (2026-05-28) — **DUAL-POLARITY FORMULAS**
- **11 concepts duaux** : `m2:hasStructuralGrammarFormula` → array `[f | _^, f | _$]`
- 3 déjà hybrides (`Coherence`, `Amplification`, `Pattern`) — trivial
- 8 nouveaux hybrides (ajout de `|` + pôles) : `Activation`, `Convergence`, `Coding`, `Fusion`, `Composition`, `Entropy`, `Synergy`, `Potentialization`
- `isStereopsic=True` pour les 8 nouveaux (total : **36**)
- Entropy : `_^`=Entropy / `_$`=Negentropy

### v16.11.0 (2026-05-27) — **BASE16 EXTENSION**
- 25 formulas updated (St/It indexation + S×I collision resolution via Ss, L, K)
- 17 new `isStereopsic=True` (total was 28)
- Notation convention: St/It in hybrid formulas

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
6. **36 stereopsic GenericConcepts** use `|` or a Gs primitive (T, K, Ss, L, _^, _$)
7. **11 dual-polarity pairs** — `hasStructuralGrammarFormula` is a 2-element array `[f|_^, f|_$]`
8. **S×I collision resolved** — 33 former collisions disambiguated via Ss, L, K
9. **Single formula notation** — `m2:hasStructuralGrammarFormula` only (RawText & TeX removed)

**M2 is where TSCG's transdisciplinary power becomes explicit.** 🌟
