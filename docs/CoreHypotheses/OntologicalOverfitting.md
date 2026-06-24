# Ontological Overfitting — Anti-Pattern in TSCG Modelling

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-06-23
**Framework**: TSCG (Transdisciplinary System Construction Game) v16.14.0+
**Status**: Core Hypothesis — architectural guard-rail
**Location**: `docs/CoreHypotheses/OntologicalOverfitting.md`
**See also**:
- `ontology/docs/TerritoryMap_Dichotomy.md`
- `M2_GenericConcepts.jsonld` — m2:Modelisation, m2:TriadicBalance
- `M1_CoreConcepts.jsonld` — m1:ConstraintBalance
- `skills/tscg-m2-candidate-filter/SKILL.md`

---

## Table of Contents

1. [Definition](#1-definition)
2. [The ML Analogy](#2-the-ml-analogy)
3. [How It Manifests in TSCG](#3-how-it-manifests-in-tscg)
4. [The TSCG Architecture as Remedy](#4-the-tscg-architecture-as-remedy)
5. [The Three Filter Tests](#5-the-three-filter-tests)
6. [The M1 Safety Valve](#6-the-m1-safety-valve)
7. [Historical Examples from TSCG Development](#7-historical-examples-from-tscg-development)
8. [The ConstraintBalance Triad](#8-the-constraintbalance-triad)
9. [Relationship to Korzybski](#9-relationship-to-korzybski)
10. [References](#10-references)

---

## 1. Definition

> **Ontological Overfitting** is the anti-pattern of adding a new M2 concept
> for every observed phenomenon, rather than composing existing concepts.
> It produces an ontology that mirrors the world 1:1 — losing the
> generalization capacity that makes TSCG useful as a transdisciplinary framework.

Formally, Ontological Overfitting is the instance of **m1:OverConstrained**
applied to **m2:Modelisation**:

```
Ontological Overfitting  =  m1:ConstraintBalance | _$
                             applied to m2:Modelisation
```

It sacrifices **E (Evolvability)** and **V (Verifiability)** for local
**R (Representability)** — the ontology can represent the specific phenomenon
but cannot generalize, compose, or predict.

---

## 2. The ML Analogy

The term is deliberately borrowed from machine learning, where the structural
parallel is exact:

| ML Overfitting | Ontological Overfitting |
|---|---|
| Too many parameters for the training data | Too many M2 concepts for the phenomenon corpus |
| High variance, low bias | High local expressivity, low generalization |
| Does not generalize to new data | Does not compose to model new phenomena |
| Remedy: regularization | Remedy: decomposability + atomicity filter |
| Metric: validation set error | Metric: ratio primitives/concepts |

The key insight from ML is that overfitting is caused by **fitting the noise**
rather than the signal — treating every particular as if it were a universal.
In TSCG, Ontological Overfitting occurs when a modeller treats every domain
phenomenon as if it required a new M2 universal.

---

## 3. How It Manifests in TSCG

### 3.1 The Temptation

When analysing a new system or phenomenon, the modeller observes:
> "This phenomenon is not exactly covered by existing M2 concepts."

The temptation is to immediately propose a new M2 concept. This is often
premature — the phenomenon may be:

- **Composable** from existing M2 concepts via Fm2 (→ belongs in M1_CoreConcepts)
- **Domain-specific** (→ belongs in M1_Domain extension)
- **An instance** of an existing M2 concept with a different attribute value
- **Correctly modelled** by an existing M2 concept whose semantics were misread

### 3.2 Warning Signs

A candidate M2 concept may be an Ontological Overfitting if:

```
□  It is only validated in 1-3 domains (not ≥6 unrelated)
□  Its formula is reducible to a combo of existing M2 concepts
□  It requires domain expertise to understand (not universally accessible)
□  It was proposed immediately after observing a specific phenomenon
□  Its formula adds a dimension already present in a related concept
□  It cannot be expressed without domain-specific vocabulary
```

### 3.3 The 1:1 Trap

Jorge Luis Borges described the reductio ad absurdum:
a map at 1:1 scale is not a map — it is the territory itself.

```
Map at 1:1  =  Territory  →  useless as a map
M2 at 1:1   =  Phenomenon catalogue  →  useless as a framework
```

A framework that has one concept per phenomenon has zero compositional power —
it cannot predict, generalize, or model phenomena it has not explicitly seen.

---

## 4. The TSCG Architecture as Remedy

TSCG's layered architecture is specifically designed to prevent
Ontological Overfitting:

```
M3  — 16 primitives (Base16)     HARD LIMIT — immutable generators
M2  — ~80 atomic concepts        GUARDED — strict triple filter
M1  — unlimited combos           SAFETY VALVE — absorbs non-atomic patterns
M0  — unlimited instances        OPEN — concrete system models
```

The **M1 Safety Valve** is architectural: it provides a legitimate home
for patterns that are transdisciplinary but not atomic — preventing the
pressure to "promote" them to M2 inappropriately.

The **M2 Triple Filter** (see Section 5) is the operational guard.

The **Base16 Hard Limit** is the ultimate constraint: M3 primitives are
never added lightly. A proposed new primitive requires demonstrating that
it cannot be derived from the 16 existing ones.

---

## 5. The Three Filter Tests

Before admitting a candidate to M2, apply all three tests in order.
A candidate must pass ALL THREE.

### Test 1 — Decomposability

> *Can this concept be expressed as Fm2(C1, C2, ...) where C1, C2, ... are
> existing M2 concepts?*

```
IF decomposable  →  belongs in M1_CoreConcepts as a combo
IF not decomposable  →  proceed to Test 2
```

**Example (session 2026-06-23):**
- `Permeability` → decomposable as Fm2(Channel, Interface, Gradient) → M1_CoreConcepts ✓
- `TriadicBalance` → not decomposable (no existing M2 encodes 3-state topology) → proceed

### Test 2 — Transdisciplinarity

> *Is the concept validated in ≥6 unrelated domains, accessible without
> domain expertise?*

```
IF < 6 domains  →  belongs in M1_Domain extension
IF domain expertise required  →  belongs in M1_CoreConcepts at most
IF ≥ 6 domains AND universally accessible  →  proceed to Test 3
```

**Threshold**: 6 domains minimum. The domains must be genuinely unrelated
(physics + biology + economics + social sciences + computing + arts counts;
physics + chemistry + materials science + engineering does not).

### Test 3 — Atomicity

> *Does the concept's formula add at least one M3 dimension genuinely absent
> from all related existing M2 concepts?*

```
IF formula = recombination of dimensions already present in related M2 concepts
  →  not atomic — reject or refine
IF formula introduces genuinely new dimensional combination
  →  atomic — admit to M2
```

**Example:**
- `SpontaneousEquilibration` → reducible to Convergence + Balance → rejected
- `Modelisation` → D×F×It|R+V+E — the directed Territory→Map construction
  is genuinely absent from Process (D×F), Representation (St×It|R), and
  Alignment (I×A×S) → admitted ✓

---

## 6. The M1 Safety Valve

M1_CoreConcepts acts as a **bidirectional safety valve**:

```
Pressure DOWN (M2 → M1):
  Concepts too specialized for M2 migrate down
  Example: TopologicalDefect (requires topology knowledge)

Pressure UP (M1 → M2):
  Concepts appearing in ≥6 domains may be promoted
  Example: MultipolarNetwork (candidate under observation)

Absorption (lateral):
  Non-atomic but transdisciplinary patterns are created as M1 combos
  Example: Permeability, ConstraintBalance, CascadeAmplification
```

A healthy TSCG M2 layer shows **more M1 concepts than M2 concepts**.
This is a sign that the M2 filter is working, not that M2 is insufficient.

---

## 7. Historical Examples from TSCG Development

### Session 2026-06-23 — Transport Phenomena Analysis

Starting from the question: "Do viscosity, conductivity, and diffusion
require new M2 concepts?"

| Candidate | Tests Applied | Final Placement |
|---|---|---|
| `EntropicDrive` | Causal loop detected | Rejected (conceptual confusion) |
| `SpontaneousEquilibration` | Decomposes to Convergence+Balance | Rejected |
| `Cohesion` | Reduces to Resilience | Rejected (M1 candidate) |
| `Permeability` | Passes Test 1 (decomposable) | M1_CoreConcepts |
| `TriadicBalance` | Passes all 3 tests | M2 admitted ✓ |
| `Modelisation` | Passes all 3 tests | M2 admitted ✓ |

**Lesson**: Of 6 candidates examined, only 2 were genuine M2 additions.
The 4 rejections prevented Ontological Overfitting without losing
the conceptual insights — they were correctly placed at M1 or rejected.

### Earlier migrations

- `TopologicalDefect` — migrated M2 → M1 (requires topological knowledge)
- `Cascade`, `Propagation`, `Processor` — migrated M2 → M1 (decomposable combos)

---

## 8. The ConstraintBalance Triad

Ontological Overfitting is itself the central instance of the
**m1:ConstraintBalance** triad:

```
UnderConstrained (_^):
  M2 too vague — concepts cover everything but predict nothing
  Example: a single concept "Change" covering all dynamics

BalancedConstraint (_0):
  M2 correctly calibrated — ~80 atomic concepts, composable, generative
  Each concept validated ≥6 domains, irréductible, accessible

OverConstrained (_$):  ← Ontological Overfitting lives here
  M2 too specific — one concept per phenomenon
  Example: adding m2:Viscosity, m2:FickDiffusion, m2:FourierConduction
  as separate M2 concepts instead of composing from Gradient+Dissipation
```

The optimal point `_0` is not a number — it is the quality of
**generative compositionality**: can the M2 layer model new phenomena
it has never explicitly seen, using only existing concepts?

---

## 9. Relationship to Korzybski

Korzybski's principle: *"The map is not the territory."*

Ontological Overfitting is the failure mode where the modeller
unconsciously tries to make the map equal the territory — adding
detail until every feature of the territory has a corresponding
feature in the map.

TSCG's extension of Korzybski:
> *"A good map is not the territory — and its value lies precisely
> in what it leaves out."*

The epistemic gap δ₁ > 0 is not a failure of TSCG — it is constitutive
of its usefulness. A framework with δ₁ = 0 (perfect map) is no longer
a framework — it is a mirror.

---

## 10. References

1. **Korzybski, A.** (1933). *Science and Sanity*. Institute of General Semantics.
2. **Borges, J.L.** (1946). *On Exactitude in Science* — the 1:1 map parable.
3. **Geman, S., Bienenstock, E., Doursat, R.** (1992). Neural networks and
   the bias/variance dilemma. *Neural Computation*, 4(1), 1–58.
   — Original ML bias-variance tradeoff formalisation.
4. **TSCG internal**: `TerritoryMap_Dichotomy.md` — Map/Territory dichotomy
5. **TSCG internal**: `M2_GenericConcepts.jsonld` — m2:Modelisation, m2:TriadicBalance
6. **TSCG internal**: `M1_CoreConcepts.jsonld` — m1:ConstraintBalance, m1:Permeability

---

*Document generated from session analysis — 2026-06-23*
*Transport phenomena (viscosity/conductivity/diffusion/permeability) →
Ontological Overfitting identification → TriadicBalance + Modelisation M2 additions*
