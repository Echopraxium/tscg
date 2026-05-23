# Multisubjective Score Evaluation Protocol

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-05-23  
**Framework**: TSCG (Transdisciplinary System Construction Game) v16.0.0+  
**Status**: Foundational Concept — design specification  
**Location**: `docs/MultisubjectiveScoreEvaluationProtocol.md`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Terminological Foundations](#2-terminological-foundations)
3. [Why Scalar Scores Are Legitimate at M0](#3-why-scalar-scores-are-legitimate-at-m0)
4. [The Evaluation Process](#4-the-evaluation-process)
5. [Subjectivity vs Multisubjectivity](#5-subjectivity-vs-multisubjectivity)
6. [Cooks and Kitchens](#6-cooks-and-kitchens)
7. [The Two Axes of Objectivity](#7-the-two-axes-of-objectivity)
8. [Simulation as Independent Kitchen](#8-simulation-as-independent-kitchen)
9. [The scoringHistory Mechanism](#9-the-scoringhistory-mechanism)
10. [Current State and Roadmap](#10-current-state-and-roadmap)

---

## 1. Overview

TSCG M0 poclet scores (ASFID/REVOI types, epistemic gap δ₁) are **not absolute
measurements** — they are qualitative evaluations made by human experts or LLMs.
This raises an immediate epistemological question: how can such evaluations be
trusted, compared, or accumulated across different users, tools, and domains?

This document defines the **Multisubjective Score Evaluation Protocol**: the
methodology by which TSCG M0 scores are produced, calibrated, and progressively
strengthened toward intersubjective objectivity through multiple independent
evaluations across diverse cooks and kitchens.

The term **"multisubjective"** is deliberate: it emphasizes the *plurality of
evaluating subjects* (cooks × kitchens) as the engine of objectivity — more
concrete and operational than the philosophical term "intersubjective".

---

## 2. Terminological Foundations

### Monoidal Types, Not Dimensions

ASFID (`{A, S, F, I, D}`) and REVOI (`{R, E, V, O, I}`) are **monoidal
primitive types** (`m3:MonoidalType`) — generators of a type algebra, not
metric axes of a vector space. The term "dimension" must be avoided: it
incorrectly implies a Euclidean space with a metric, which the Structural
Grammar reform explicitly eliminated.

### The Structural Product × (Territory Monoidal Product)

Since v2.6.0 of `M3_EagleEye` (2026-05-13), the product operator has been
reformed:

```
⊗ᵗ  →  ×   (Structural Product, Territory Monoidal Product / ASFID)
```

M2 structural formulas now read:

```
Process  =  D × I × F
Stase    =  S × A
Entropy  =  F × I × D
```

The structural composition functor is:

```
F_× : Cat_M3 → Cat_M2
```

### Two Mathematical Roles, Two Levels

The same 10 labels play **fundamentally different roles** depending on the layer:

| Layer | Role | Mathematical object | Metric? |
|---|---|---|---|
| **M3 / M2** | Primitive types of the Monoidal Grammar | Generators `{A,S,F,I,D}` and `{R,E,V,O,I}` | ❌ None |
| **M0** | Evaluation functions | Morphisms `F_x : System → [0,1]` | ✅ Yes |

At M2, `S × F` is a **type expression** — purely qualitative, no numbers.  
At M0, each monoidal type instantiates as a **real-valued measurement** in `[0,1]`.

---

## 3. Why Scalar Scores Are Legitimate at M0

### The Curry-Howard Correspondence

The deep justification comes from the correspondence between types and proofs:

```
M2 formula (e.g. D × I × F = Process)  ↔  Logical proposition
M0 poclet  (e.g. M0_FireTriangle)       ↔  Proof term
δ₁ (epistemic gap)                      ↔  Degree of proof completeness
```

A poclet does not merely *describe* a system — it **proves** that the system
inhabits a conceptual type. The scalar scores are the **degrees of satisfaction**
of each monoidal type by the concrete system.

A score of `A: 0.8` means: *"this system exhibits the Attractor type at 80%
of the maximum observable strength"* — relative to a canonical reference.

### Category-Theoretic Grounding

At M0 level, each monoidal type instantiates as a **functor**:

```
F_A : SystemCategory  →  ScoreCategory   (maps systems to Attractor scores)
F_S : SystemCategory  →  ScoreCategory   (maps systems to Structure scores)
...
F_R : SystemCategory  →  ScoreCategory   (maps systems to Representability scores)
```

The space `[0,1]⁵` is a legitimate metric space, and δ₁ is a valid distance
within it. This duality — qualitative grammar at M2, quantitative evaluation
at M0 — is a **structural virtue** mirroring the Eagle/Sphinx bicephalous
architecture.

---

## 4. The Evaluation Process

### What It Is Not

There is **no formal computation** that produces `A: 0.8` from raw data.
Assuming a direct physical measurement of monoidal types would be
epistemologically naive.

### What It Is: Norm-Referenced Measurement

The technical term is **norm-referenced measurement** (Stevens 1946) — the
same logic as:

| Domain | Reference | Score |
|---|---|---|
| Oenology | Bordeaux judged vs Bordeaux references | 88/100 |
| Medicine | Glycaemia normed by age group | 0.9 (normal) |
| Psychometrics | IQ normed by age cohort | 115 |
| **TSCG** | **Poclet evaluated vs M1 domain canon** | A: 0.8 |

### The Concrete Process (for a score like `A: 0.8`)

**Step 1 — Identify the reference benchmark** using the resolution order:

```
1. DomainSpecific  (same M1 domain)           ← DEFAULT
2. CrossDomain     (adjacent M1 domain)
3. Universal       (M0_AdaptiveImmuneResponse)
4. Free scoring + explicit justification      ← last resort
```

**Step 2 — Ask the structural question** for each monoidal type:

| Type | Structural question |
|---|---|
| **A** Attractor | What does this system converge toward? Is there a stable state, cycle, or clearly identifiable attractive trajectory? |
| **S** Structure | What internal organisation does the system maintain? |
| **F** Flow | What intensity of flux (matter, energy, information) traverses it? (F=0 = Stase, valid) |
| **I** Information | What quantity/quality of information is processed or transmitted? |
| **D** Dynamics | What amplitude of state change can the system undergo? |
| **R** Representable | To what degree can the system be faithfully encoded/decoded? |
| **E** Evolvable | To what degree can the system adapt or evolve? |
| **V** Verifiable | To what degree can assertions about the system be tested/falsified? |
| **O** Observable | To what degree are the system's internal states accessible from outside? |
| **I** Interoperable | To what degree can the system exchange information with other systems? |

**Step 3 — Comparative expert evaluation** (1 or N independent experts/LLMs):

```
High score  (0.8 – 1.0) : strong, well-defined, dominant type expression
Medium score (0.4 – 0.7) : partial or multiple expression
Low score   (0.0 – 0.3) : no identifiable expression of this type
```

**Step 4 — Document the justification** in the poclet (field `justification`).

---

## 5. Subjectivity vs Multisubjectivity

### The Analogy with Personal Certainty

The evaluation process resembles a statement like:
> *"I answer this question but with a certainty I subjectively evaluate at 90%."*

This analogy is partially correct: both are **normalized subjective estimates**
on a `[0,1]` or `[0%,100%]` scale, without direct physical measurement. And
both are **defeasible** — revisable when new information arrives.

### The Critical Difference

A personal certainty is **purely individual** — anchored in an internal cognitive
state, not shareable or verifiable by others.

A TSCG ASFID/REVOI score aims to be **multisubjective**: grounded in explicit
structural criteria, reproducible by another expert or LLM confronting the same
system with the same canonical poclet as reference.

```
Subjective      :  "I feel 90% certain"
                    → anchored in ME, non-transferable

Multisubjective :  "relative to canonical poclet M0_Transistor,
                    this system expresses type A (Attractor) at 0.8"
                    → anchored in a SHARED REFERENCE,
                      reproducible by another cook
```

---

## 6. Cooks and Kitchens

### Definition

A **"cook"** is any user who creates TSCG poclets or instances.  
Their **"kitchen"** is their complete working setup:

```
Kitchen = LLM choice (Claude, Gemini, DeepSeek, GPT-4...)
        + Reference corpus (domain documents, TSCG ontologies)
        + User expertise profile (domain knowledge, background)
        + Domains explored (biology, electronics, music...)
        + Epoch (available knowledge at time of creation)
```

### Why Different Kitchens Matter

The strength of multisubjective consensus is **not** the convergence of
identical cooks using identical kitchens — it is the convergence of
**different cooks using different kitchens**:

| Scenario | Consensus strength |
|---|---|
| 1 cook, 1 kitchen | Subjective — no consensus possible |
| N cooks, **same** kitchen | Weak (shared biases) |
| N cooks, **different** kitchens | **Strong multisubjective** |
| N cooks, different kitchens, different domains | **Quasi-objective** |

### The Scientific Parallel

Independent laboratories, different equipment, different teams, converging
toward the same physical constant → the constant is a real structural
attractor of nature.

Translated to TSCG: if a researcher in Tokyo (GPT-4 + physics corpus), a
biologist in São Paulo (Claude + biomedical corpus), and an engineer in Namur
(Gemini + electronics corpus) all independently converge on the same score for
a given system — that score has achieved genuine multisubjective objectivity.

---

## 7. The Two Axes of Objectivity

Score quality improves along two independent axes:

### Axis 1 — Cook Diversity (different people)

Multiple independent human experts model the same system independently.
Convergence = strong objectivity signal.

### Axis 2 — Kitchen Diversity (same cook, different contexts)

The **same cook** can generate multiple independent evaluations by varying:

| Kitchen variation | Concrete example | What it tests |
|---|---|---|
| Different LLM | Claude → Gemini → GPT-4 | Model-specific biases |
| Improved version | Claude Sonnet 4.5 → 4.6 | Temporal stability |
| Extended RAG corpus | +50 domain documents | Context sensitivity |
| Different simulation | 2D p5.js → 3D BabylonJS | Hidden property revelation |
| New domain instance | Chemistry → Biology analogue | Structural generality |

Both axes are legitimate and complementary paths toward multisubjective
objectivity.

---

## 8. Simulation as Independent Kitchen

A simulation is not merely a visualisation — it is an **instantiation of the
system** that can reveal ASFID/REVOI properties that the `.jsonld` file alone
did not capture.

For example: if a 3D BabylonJS simulation of a poclet reveals an attractor
behaviour stronger than initially estimated → the `A` score should be revised
upward. The simulation acts as a **partial oracle** that challenges declared
scores.

This means that adding a new simulation to an existing instance is a legitimate
**kitchen change** — it can and should trigger score re-evaluation.

---

## 9. The `scoringHistory` Mechanism

### Formal Design

To track the convergence of scores across multiple cooks and kitchens, a
`scoringHistory` array must be integrated into the M0 instance structure:

```json
"m3:intersubjectiveBenchmark": {
  "objectivityLevel": "MultiExpertConsensus",
  "scoringHistory": [
    {
      "cook":    "Echopraxium",
      "kitchen": "Claude Sonnet 4.5 + TSCG corpus v1",
      "date":    "2025-11-10",
      "asfid":   { "A": 0.7, "S": 0.8, "F": 0.6, "I": 0.7, "D": 0.5 },
      "revoi":   { "R": 0.8, "E": 0.6, "V": 0.7, "O": 0.7, "I": 0.6 },
      "justification": "Initial scoring, no domain benchmark available"
    },
    {
      "cook":    "Echopraxium",
      "kitchen": "Claude Sonnet 4.6 + 3D BabylonJS simulation",
      "date":    "2026-02-14",
      "asfid":   { "A": 0.8, "S": 0.8, "F": 0.6, "I": 0.7, "D": 0.5 },
      "revoi":   { "R": 0.8, "E": 0.6, "V": 0.7, "O": 0.8, "I": 0.6 },
      "justification": "A revised upward: 3D simulation revealed stronger attractor basin. O revised upward: simulation makes internal states directly observable."
    },
    {
      "cook":    "ExpertX",
      "kitchen": "Gemini 2.0 + physics corpus",
      "date":    "2026-05-10",
      "asfid":   { "A": 0.8, "S": 0.7, "F": 0.6, "I": 0.8, "D": 0.5 },
      "revoi":   { "R": 0.7, "E": 0.6, "V": 0.8, "O": 0.8, "I": 0.6 },
      "justification": "Independent evaluation. A confirms 0.8. S slightly lower (0.7): structure less rigid from physics perspective."
    }
  ],
  "convergenceScore": 0.91,
  "convergenceMetric": "ICC",
  "defeasibilityStatus": {
    "status":    "provisional",
    "validUntil": "superseded_by_better_consensus"
  }
}
```

### What the convergenceScore Expresses

The `convergenceScore` (Intraclass Correlation Coefficient — ICC) measures
the degree to which independent evaluations agree beyond chance:

```
ICC < 0.50  →  poor agreement       → scores unreliable
ICC 0.50–0.75 →  moderate agreement  → scores usable with caution
ICC 0.75–0.90 →  good agreement      → scores reliable
ICC > 0.90  →  excellent agreement  → scores quasi-objective
```

### Declared objectivityLevel

The `objectivityLevel` field must reflect the actual state of the
`scoringHistory`:

```
Subjective              ← 1 cook, 1 kitchen, no canonical reference
MultiExpertConsensus    ← N cooks or N kitchens, ICC computed
CanonCalibrated         ← scored against a domain benchmark poclet
ContextualizedBenchmark ← multi-cook, multi-kitchen, ICC > 0.75
```

---

## 10. Current State and Roadmap

### Phase 1 — Embryonic corpus (current state)

```
Cooks       : 1  (Echopraxium)
Kitchens    : 1  (Claude + TSCG GitHub corpus)
Poclets     : 24+
Benchmarks  : 3 canonical poclets identified
              (M0_AdaptiveImmuneResponse, M0_Transistor, M0_TrophicPyramid)
Score status: Subjective — honest approximation by a single expert
```

At this stage, scores are effectively similar to a personal certainty estimate.
Their value lies in **structural consistency** within the corpus and in being
**explicitly declared as provisional** — not in false objectivity claims.

### Roadmap toward multisubjective objectivity

```
Phase 1  Embryonic   (<30 poclets, 1 cook)
  └── Scores: subjective, approximated
  └── Value: structural consistency + explicit provisionality

Phase 2  Growing     (30–100 poclets, 1 cook, N kitchens)
  └── Scores: compared across LLM versions + simulations
  └── scoringHistory populated per poclet
  └── First ICC values computed

Phase 3  Mature      (100+ poclets, multiple cooks)
  └── Stable domain benchmarks established by consensus
  └── ICC > 0.75 for canonical poclets
  └── objectivityLevel → ContextualizedBenchmark

Phase 4  Rich        (multi-cook, multi-domain, multi-kitchen)
  └── Quasi-objective scores for core poclets
  └── Universal attractors emerge across domains
  └── TscgPocletMiner identifies benchmark centroids automatically
```

### Integration with SHACL Grammar

The `scoringHistory` mechanism must be integrated into
`M0_Instances_Schema.shacl.ttl` as an optional but strongly recommended
property for all M0 instances — not only poclets.

---

## References

- Stevens, S.S. (1946). *On the theory of scales of measurement.* Science, 103(2684), 677–680.
- Lord, F.M. & Novick, M.R. (1968). *Statistical theories of mental test scores.* Addison-Wesley.
- Popper, K. (1934). *Logik der Forschung.* Springer.
- Kuhn, T.S. (1962). *The Structure of Scientific Revolutions.* University of Chicago Press.
- Peirce, C.S. (1878). *How to Make Our Ideas Clear.* Popular Science Monthly.
- Cohen, J. (1960). *A coefficient of agreement for nominal scales.* Educational and Psychological Measurement, 20(1), 37–46.
- Koo, T.K. & Mae, A.Y. (2016). *A guideline for selecting and reporting intraclass correlation coefficients.* Journal of Chiropractic Medicine, 15(2), 155–163.
- Lambek, J. (1958). *The mathematics of sentence structure.* The American Mathematical Monthly, 65(3), 154–170.

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
