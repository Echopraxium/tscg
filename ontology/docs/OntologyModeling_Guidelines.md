# TSCG Ontology Modeling Guidelines

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 1.4.0  
**Created**: 2026-05-20  
**Location**: `ontology/docs/OntologyModeling_Guidelines.md`  
**Status**: Foundational — applies to all TSCG layers (M3, M2, M1, M0)

---

## Purpose

This document collects the architectural principles and modeling rules that
govern the construction of TSCG ontologies across all layers. These guidelines
encode hard-won decisions made during corpus development and should be
consulted before creating or modifying any ontology file.

---

## Guideline 1 — The Phenomenological Stance of M2

### Principle

> **M2 describes phenomena as seen by an observer — not their implementation.**

The three layers have distinct epistemic orientations:

```
M3  →  Grammar     (formal structure — what CAN exist)
M2  →  Phenomenon  (observable pattern — what IS seen)
M1  →  Domain      (disciplinary context — WHERE it appears)
M0  →  Instance    (concrete realization — HOW it is built)
```

### Consequence for structural formulas

When writing a M2 structural formula `hasStructuralGrammarFormula`, include
only the ASFID/REVOI dimensions that an **observer** would perceive as
constitutive of the phenomenon — not the dimensions that describe how
it is physically realized.

**Example — m2:Amplification:**

```
Ft × D × It | R + O     ✓  phenomenological formula
                            Ft = signal observed, D = gain observed, It = information observed

S × Ft × D × It | R + O  ✗  implementation formula
                            S = circuit structure → belongs to M1/M0, not M2
```

The transistor, the op-amp, the enzymatic cascade — these are M0 realizations.
The M2 concept captures only what is common to all of them as observed.

### Consequence for absent dimensions

If an ASFID dimension is **absent** from a M2 formula, it is likely
**intentional** — that dimension belongs to the implementation (M1/M0),
not to the observable phenomenon (M2).

Before adding a dimension to a M2 formula, ask:
> *"Would an observer of the phenomenon see this dimension directly,
> or only after knowing how it is implemented?"*

If the answer is "only after knowing the implementation" → the dimension
belongs to M1/M0.

---

## Guideline 2 — ValueSpace is a Frozen Referential

### Principle

> **A ValueSpace defines the observation referential — it is frozen at the
> moment of observation. If it changes, it is a new ValueSpace.**

A ValueSpace that evolves during observation creates a "fluid" referential,
making measurements non-comparable — like changing the unit of measurement
mid-experiment.

```
ValueSpace v1  →  (re-evaluation process)  →  ValueSpace v2
                   external process
                   produces a NEW ValueSpace, not an evolution of the same
```

### Consequence for the formula

```
It | V + O + R + Im     ✓  E (Evolvable) is absent — intentional
                            The ValueSpace does not generate new predictions;
                            it defines the fixed space within which observations are made.
```

E (Evolvable) is a Map property meaning "the model generates novel predictions".
A ValueSpace does not generate predictions — it provides the referential frame
for existing ones. Therefore E is structurally excluded.

---

## Guideline 3 — Im (Interoperable) Exclusion Criterion

### Principle

> **If the concept being defined IS interoperability itself, Im must be
> excluded from its formula to avoid tautology.**

```
m2:Interoperability  :=  S × I × F | V + E   (Im excluded — tautological)
```

More generally: if a Map dimension is constitutive of the concept's identity
rather than an observable property of it, exclude it.

---

## Guideline 4 — Identical Formulas Are Acceptable

### Principle

> **Two GenericConcepts can share the same structural formula if their
> semantic distinction is captured by their definition, comment, and examples.**

Since TSCG uses a **commutative** monoidal grammar (A × B = B × A),
order does not disambiguate. The distinguishing power lies in:

- `rdfs:comment` — semantic definition
- `m2:hasExample` — cross-domain instantiations
- `m2:hasDominantM3` — primary dimension emphasis

**Known cases of identical formulas:**

| GenericConcept A | GenericConcept B | Formula |
|---|---|---|
| Layer | Scope | `S × I × A \| R` |
| Coherence | TopologicalDefect | `A × S × I \| R + O` |

These are not modeling errors — they reflect that different systemic
phenomena can share the same structural grammar while differing in meaning.

---

## Guideline 5 — T (Temporality) Usage Criterion

### Principle

> **Use T (from 𝕋₀(|), Stereopsis Grammar Gs) only when the concept
> describes the temporal interface between Territory and Map —
> not whenever time is involved.**

T is the first primitive of the Bicephalous Perspective Grammar (Gs).
It is distinct from D (Dynamics):

| Dimension | What it captures | Grammar |
|---|---|---|
| **D** | Temporal evolution of a system state — change, phase transitions | Gt (Territory) |
| **T** | Pure temporal interface between Territory observation and Map representation | Gs (Stereopsis) |

**Use T when:** the concept's formula requires the temporal *correspondence*
between Territory and Map — as in m2:Gradient (F × T), where T isolates
the temporal aspect of how flow variation (Territory) corresponds to a
measurable gradient (Map).

**Use D when:** the concept's formula requires temporal evolution of a
state within Territory — as in m2:Process (D × I × F), m2:Duplication
(S × I × F × D).

**Anti-pattern:** replacing D with T whenever time is involved.
D and T are not interchangeable.

---

## Guideline 6 — Layer Assignment Principle

### Principle

> **Assign each modeling decision to the most specific layer that
> can host it without loss of generality.**

```
Is it valid across ALL domains without exception?  →  M2 (GenericConcept)
Is it valid within a knowledge field?              →  M1 (DomainExtension)
Is it a concrete realization?                      →  M0 (Poclet instance)
```

A concept belongs to M2 only if it can be instantiated in at least 6
unrelated domains. If fewer domains validate it, it belongs to M1.

---

## Guideline 7 — Structural Formula Anti-Patterns

Avoid these patterns when writing `hasStructuralGrammarFormula`:

| Anti-pattern | Problem | Correct approach |
|---|---|---|
| Using ⊗ | Former notation — ambiguous | Use ×, + or \| explicitly |
| Using ⊗₂ or ⊗ₙ | Differential operator — not valid in free monoidal grammar | Use F × T (for gradients) |
| Using Im in a concept that IS interoperability | Tautology | Exclude Im |
| Using E in a fixed referential concept | Contradicts referential stability | Exclude E |
| Using S for implementation structure | Belongs to M0 | Describe phenomenon only |
| Replacing D with T indiscriminately | T ≠ D | Use T only for Territory/Map temporal interface |

---

---

## Guideline 8 — Operator Precedence in Structural Formulas

### Principle

> **The three TSCG operators follow an explicit precedence order
> (highest to lowest): × > + > |**

This rule, combined with alphabet constraints, makes all structural
formulas unambiguous without parentheses.

### Precedence table

| Rank | Operator | Name | Precedence |
|---|---|---|---|
| 1 (highest) | `×` | Territory structural product | Binds tightest |
| 2 | `+` | Map structural sum | Medium binding |
| 3 (lowest) | `\|` | Stereopsic fusion | Main separator — binds loosest |

### Reading rule

In any hybrid formula, `|` is always the **main separator** between
the Territory expression (left) and the Map expression (right):

```
A × S × I | R + O
=  (A × S × I) | (R + O)     ← always read this way

Territory part: A × S × I    (× groups tightest)
Map part:       R + O         (+ groups within Map)
```

### Why parentheses are NOT needed in current TSCG formulas

Two mechanisms combine to eliminate ambiguity:

**1. Alphabet constraints** (structurally restrictive):
```
×  operates only on 𝕋₀(×) = {A, S, F, I, D}   — never on REVOI types
+  operates only on 𝕋₀(+) = {R, E, V, O, Im}  — never on ASFID types
```
Cross-alphabet combinations like `O × I` are **invalid by definition** —
they cannot appear in any well-formed formula.

**2. Precedence rule** (× > + > |):
```
Any expression left of |  → grouped by ×  (Territory)
Any expression right of | → grouped by +  (Map)
|                          → always the outermost operator
```

### Verification on all current hybrid formulas

| Formula | Unambiguous reading |
|---|---|
| `A × S × I \| R + O` | `(A × S × I) \| (R + O)` ✓ |
| `S × I × F \| V + E` | `(S × I × F) \| (V + E)` ✓ |
| `Ft × D × It \| R + O` | `(Ft × D × It) \| (R + O)` ✓ |
| `It \| V + O + R + Im` | `It \| (V + O + R + Im)` ✓ |
| `S × I × F × D \| V` | `(S × I × F × D) \| V` ✓ |
| `S × I × A \| R` | `(S × I × A) \| R` ✓ |

### When parentheses ARE recommended

Use explicit parentheses when:
1. A formula contains **T from 𝕋₀(|)** combined with × :
   `F × T` — no ambiguity but T's special status warrants clarity
2. A future formula mixes × and | on the **same side** (unusual):
   `(A | R) × S` — explicit parentheses required
3. For **documentation or pedagogy** — parentheses always improve readability

### This rule must be stated explicitly

This precedence was previously only **implicit** in TSCG. It is now
formally documented here and in `M3_GrammarFoundation.jsonld`
(`operator_grammar_types.precedence` section).


---

## Guideline 9 — It/Im Disambiguation in Hybrid Formulas

### Principle

> **In any formula containing |, always use `It` (Information/Territory)
> and `Im` (Interoperable/Map) — never bare `I`.**

Both ASFID and REVOI have a dimension abbreviated `I`:

```
It  =  Information  (Territory/Eagle Eye — encoded content, state complexity)
Im  =  Interoperable (Map/Sphinx Eye    — integration capability, compatibility)
```

### Rule

```
Pure Territory formula (no |):   I alone is acceptable
                                  D × I × F  (Process)

Hybrid formula (with |):         ALWAYS use It and Im
                                  S × It × A | R + O  ← NOT S × I × A | R + O
```

### Rationale

The | operator and the bare `I` character look similar in many fonts.
Using `It` and `Im` in all hybrid formulas eliminates visual ambiguity
and makes the grammar of each side explicit.

---

## Guideline 10 — Pole Primitives _^ and _$

### Principle

> **Use _^ and _$ (primitives of 𝕋₀(|)) to select the positive or
> negative pole of a GenericConcept pair — applied via | after the
> full formula.**

```
formula | _^   →  positive/onset/amplifying pole
formula | _$   →  negative/terminus/attenuating pole
```

### Why not ^op

`^op` was a vestige of the tensor algebra formalism. In the structural
grammar, types are not vectors — their polarity cannot be "inverted".
`_^` and `_$` are proper type primitives of Gs that SELECT a pole
without any inversion.

### Usage

```
A × S × It | R + O | _^   =  Coherence      (positive pole)
A × S × It | R + O | _$   =  Incoherence    (negative pole)
A × S × F  | _^           =  Homeostasis    (positive pole)
A × S × F  | _$           =  Dysregulation  (negative pole)
```

### Notation rationale

`_^` and `_$` are valid identifiers in Python, JavaScript, SPARQL,
and most programming languages. The underscore prefix signals
"special reserved type", distinct from operators (×, +, |).


---

## Guideline 11 — One Free Monoid, Multiple Named Vocabularies

### Principle

> **TSCG has ONE free monoid — the layers M3/M2/M1/M0 are not separate
> monoids but named vocabularies within the same free monoid on 𝕋₀.**

### The single TSCG free monoid

```
𝕋₀  =  {A, S, F, I, D, R, E, V, O, Im, T, _^, _$}   13 generators
𝕋*  =  free monoid on 𝕋₀ via ×, +, |                 all well-formed expressions

𝕋ₙ  =  expressions of complexity n
        (formed by exactly n operator applications on 𝕋₀)
```

### The four layers as named vocabularies

```
M3  →  defines 𝕋₀ and the operators (×, +, |)
M2  →  named subset of 𝕋*: GenericConcepts
        (frequently-occurring, transdisciplinary expressions of 𝕋*)
M1  →  named subset of 𝕋*: Combos, domain extensions
        (disciplinary expressions, KnowledgeFieldConceptCombo)
M0  →  concrete instantiations of M2/M1 expressions (Poclets)
```

None of M2, M1, M0 is itself a monoid — they are **lexicons** of
privileged expressions within the single free monoid 𝕋*.

### Why M2 is NOT a monoid

A monoid requires closure under its operator. M2 fails this:

```
Process   =  D × It × F              (Territory expression)
Coherence =  A × S × It | R + O      (Bicephalous expression)

Process × Coherence  →  D × It × F × (A × S × It | R + O)
                         INVALID: × cannot operate on a Gs expression
```

The composition of two M2 GenericConcepts is not guaranteed to produce
another M2 GenericConcept. M2 is a named vocabulary, not a closed set.

### Consequence for modeling

When combining GenericConcepts (Combos), one is not composing monoids —
one is composing expressions of the single free monoid 𝕋* and giving
the result a new name. The algebraic structure is always that of 𝕋*.


---

## Guideline 12 — Composition Morphisms Fm2 and Fm1m2

### Principle

> **Use Fm2 and Fm1m2 to express the composition of GenericConcepts —
> not as monoidal operators but as morphisms at the M2/M1 level.**

### Why not operators

×, +, | operate on 𝕋₀ primitives and produce expressions in 𝕋*.
Fm2 and Fm1m2 operate on 𝕋₁ expressions (GenericConcepts, KnowledgeFields)
and produce new named 𝕋₁ expressions — they are morphisms, not operators.

### Fm2 — GenericConcept composition

```
Fm2 : 𝕋₁(M2) × 𝕋₁(M2)ⁿ → 𝕋₁(M2)

Fm2(Memory, Entropy)            = Inertia
Fm2(Incoherence, Invariant)     = TopologicalDefect
Fm2(Process, Step, Trajectory)  = PipelineProcess
```

Use Fm2 when a concept emerges from two or more existing GenericConcepts
with properties not reducible to their simple juxtaposition.

### Fm1m2 — KnowledgeField + GenericConcept composition

```
Fm1m2 : 𝕋₁(M1) × 𝕋₁(M2)ⁿ → 𝕋₁(M1/M2)

Fm1m2(Biology, Process)              = BiologicalProcess
Fm1m2(Economics, Flow, Gradient)     = MarketFlow
Fm1m2(Physics, Coherence)            = LaserCoherence
Fm1m2(Education, Memory, Structure)  = CurriculumDesign
```

Use Fm1m2 for KnowledgeFieldConceptCombo — domain-specific instantiations
of generic patterns (M1 KnowledgeField combined with M2 GenericConcept(s)).

### TSCG function family

```
Φ      : Gt → Gm                  M3 natural transformation (observation)
Ψ      : Gm → Gt                  M3 natural transformation (interpretation)
Fm2    : 𝕋₁(M2)ⁿ → 𝕋₁(M2)       M2 composition morphism
Fm1m2  : 𝕋₁(M1) × 𝕋₁(M2)ⁿ → 𝕋₁  M1/M2 composition morphism
```

### Replaces former ⊗⇒ notation

`⊗⇒` incorrectly suggested a monoidal operator. Fm2 and Fm1m2 make
the functional nature and operating level explicit.


## Changelog

| Version | Date | Changes |
|---|---|---|
| 1.4.0 | 2026-05-20 | Added Guideline 12: Fm2 and Fm1m2 composition morphisms. Replaces ⊗⇒. |
| 1.3.0 | 2026-05-20 | Added Guideline 11: one free monoid, multiple named vocabularies. |
| 1.2.0 | 2026-05-20 | Added Guidelines 9-10: It/Im disambiguation and _^/_$ pole primitives. |
| 1.1.0 | 2026-05-20 | Added Guideline 8: operator precedence × > + > | — formally documents implicit rule. |
| 1.0.0 | 2026-05-20 | Initial release. 7 guidelines: phenomenological stance, ValueSpace, Im exclusion, identical formulas, T criterion, layer assignment, anti-patterns. |
