# TSCG Intersubjective Benchmark for Defeasible Knowledge

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-05-11
**Framework**: TSCG (Transdisciplinary System Construction Game) v16.0.0+
**Status**: Foundational Concept — design specification

---

## Table of Contents

1. [Overview](#1-overview)
2. [Not Absolute Truth — Defeasible Knowledge](#2-not-absolute-truth)
3. [The Measurement Spectrum](#3-the-measurement-spectrum)
4. [Contextualized Canon as Default](#4-contextualized-canon-as-default)
5. [The Cook and Kitchen Metaphor](#5-the-cook-and-kitchen-metaphor)
6. [The Virtuous Circle](#6-the-virtuous-circle)
7. [Mathematical Grounding](#7-mathematical-grounding)
8. [Connection to REVOI](#8-connection-to-revoi)
9. [Formal Design of m3:intersubjectiveBenchmark](#9-formal-design)
10. [Philosophical Grounding](#10-philosophical-grounding)
11. [Summary](#11-summary)

---

## 1. Overview

TSCG M0 poclet scores (ASFID/REVOI dimensions, epistemic gap δ₁) are
**not absolute measurements** — they are qualitative evaluations made by
human experts. This raises an immediate epistemological question: how can
such measurements be trusted, compared, or accumulated across different
users, tools, and domains?

The answer is the **intersubjective benchmark** (`m3:intersubjectiveBenchmark`):
a domain-contextualized canonical poclet that serves as a shared scoring
reference — not a fixed absolute truth, but a **consensual, revisable,
defeasible anchor** that grounds measurements in an explicit community of
practice.

This concept is simultaneously:
- An **epistemological key** — grounding TSCG measurement in legitimate
  philosophy of science
- A **mathematical key** — connecting TSCG to norm-referenced measurement
  theory and statistical inter-rater reliability
- A **systemic key** — enabling a virtuous self-improvement cycle as the
  poclet corpus grows and diversifies

---

## 2. Not Absolute Truth — Defeasible Knowledge

### The Distinction

```
Absolute truth    :  speed of light in vacuum = 299,792,458 m/s
                     → immutable, observer-independent, permanent

Defeasible truth  :  "M0_Transistor is the canonical benchmark
                      for the Electronics domain"
                     → valid UNTIL superseded by better consensus
                     → revisable, ephemeral, but operationally solid
```

### Defeasible Knowledge

**Defeasible knowledge** is knowledge that holds *until defeated* by
stronger evidence or broader consensus. It is not a weakness — it is the
normal epistemic status of most scientific, legal, and practical knowledge:

| Domain | Defeasible canon | Revision trigger |
|---|---|---|
| Common law | Legal precedent (*stare decisis*) | Overruling judgment |
| Science | Accepted paradigm (Kuhn) | Anomaly accumulation |
| Industry | ISO standard | Periodic revision cycle |
| Medicine | Clinical guideline | New clinical trial evidence |
| **TSCG** | **Contextualized benchmark poclet** | **Richer corpus + new consensus** |

### Explicit Revisability in TSCG

The defeasible nature of benchmarks must be **explicitly declared**, not
hidden. A benchmark poclet carries:

```json
"m3:defeasibilityStatus": {
  "status":          "provisional",
  "validUntil":      "superseded_by_better_consensus",
  "revisionTrigger": [
    "new_canonical_poclet_identified",
    "expert_consensus_challenged",
    "domain_expansion",
    "corpus_maturation"
  ],
  "establishedBy":   "community_consensus",
  "establishedDate": "2026-05-11"
}
```

This explicit declaration is a philosophical and scientific *strength*,
not a concession. It is what distinguishes a living knowledge framework
from a frozen dogma.

---

## 3. The Measurement Spectrum

M0 scoring is not binary (subjective OR objective). It occupies a
**spectrum** from purely subjective to quasi-objective:

```
SUBJECTIVE ──────────────────────────────────────── QUASI-OBJECTIVE

  1. Free scoring         2. Multi-expert      3. Canon-         4. Physical
     (single expert,         consensus            calibrated        measurement
      no reference)          (same setup)         (domain          (thermometer,
                                                   benchmark,        spectrometer)
                                                   different setups)
         │                       │                    │                  │
    fully            intersubjective           intersubjective       absolute
    subjective           (weak)                    (strong)           (out of
                                                                     TSCG scope)
```

TSCG currently operates at level 1–2. The `m3:intersubjectiveBenchmark`
mechanism targets level 3 — strong intersubjective objectivity through
domain-contextualized, multi-cook convergence.

Level 4 (absolute physical measurement) is outside TSCG's scope and
outside the scope of most transdisciplinary frameworks.

---

## 4. Contextualized Canon as Default

### Why Context Matters

A single universal benchmark for all domains would be epistemologically
naive. The same ASFID/REVOI dimensions carry different structural
expectations depending on domain:

- A **Process** in chemistry (M0_MethaneCycle) has different typical
  Flow/Dynamics ratios than a **Process** in economics (M0_MarketCycle)
- What constitutes a "high Attractor score" in biology differs from
  what constitutes one in electronics

This mirrors established practice everywhere:

| Domain | Contextualized benchmark | Why context matters |
|---|---|---|
| Oenology | Bordeaux judged vs Bordeaux refs | Style, terroir, grape variety |
| Medicine | Glycaemia norms by age group | Metabolic baselines differ |
| Psychometrics | IQ normed by age cohort | Cognitive baseline differs |
| Law | Precedents by jurisdiction | Legal tradition differs |
| **TSCG** | **Canon by M1 domain** | **Structural patterns differ** |

### Canon Resolution Order

```
1.  DomainSpecific benchmark   (same M1 domain as poclet)   ← DEFAULT
2.  CrossDomain benchmark      (adjacent M1 domain)
3.  Universal benchmark        (M0_AdaptiveImmuneResponse)
4.  Free scoring + explicit justification                   ← last resort
```

The contextualized canon is the **default case** — the universal canon
is the fallback when no domain-specific reference exists yet.

### Existing TSCG Canonical Instances

The TSCG corpus already contains natural benchmark candidates:

| Poclet | Domain | Canonical status |
|---|---|---|
| `M0_AdaptiveImmuneResponse` | Biology / Universal | Fully conformant — universal reference |
| `M0_Transistor` | Electronics | Near-exemplary template |
| `M0_TrophicPyramid` | Ecology | Near-exemplary template |

These three poclets are the **founding jurisprudence** of TSCG measurement.
All subsequent poclets in their respective domains should be scored
*by comparison* with them.

---

## 5. The Cook and Kitchen Metaphor

### The Setup as Kitchen

In TSCG, a **"cook"** is any user who creates poclets. Their **"kitchen"**
is their complete working setup:

```
Kitchen (setup) = LLM choice (Claude, Gemini, DeepSeek, GPT-4...)
               + Reference corpus (domain documents, TSCG ontologies)
               + User expertise profile (domain knowledge, background)
               + Domains explored (biology, electronics, music...)
               + Epoch (available knowledge at time of creation)
```

### Why Different Kitchens Matter

The strength of intersubjective consensus is NOT the convergence of
identical cooks using identical kitchens — it is the convergence of
**different cooks using different kitchens**:

| Scenario | Convergence strength |
|---|---|
| 1 cook, 1 kitchen | Subjective — no consensus possible |
| N cooks, **same** kitchen | Weak intersubjective (shared biases) |
| N cooks, **different** kitchens | **Strong intersubjective** |
| N cooks, different kitchens, different domains | **Quasi-objective** |

### The Scientific Parallel

This is precisely how science establishes objectivity:

> Independent laboratories, different equipment, different teams,
> converging toward the same physical constant
> → the constant is a real structural attractor of nature.

Translated to TSCG:

> Independent cooks, different LLMs, different corpora, different
> domains, converging toward the same canonical poclet
> → that poclet is a real structural attractor of its conceptual domain.

If a researcher in Tokyo (GPT-4 + physics corpus), a biologist in
São Paulo (Claude + biomedical corpus), and an engineer in Namur
(Gemini + electronics corpus) all independently converge on the same
benchmark for "Process" — that benchmark has achieved genuine
intersubjective objectivity.

---

## 6. The Virtuous Circle

### Emergence Through Corpus Growth

As the TSCG poclet corpus grows and diversifies, a **self-improving
calibration dynamic** emerges naturally:

```
PHASE 1 — Embryonic corpus  (< 30 poclets)
  ├── Few poclets per domain
  ├── Benchmarks are subjective (single expert, single setup)
  └── Scoring approximation is high

PHASE 2 — Growing corpus  (30–100 poclets)
  ├── Statistical patterns begin to emerge per domain
  ├── "Central" poclets self-identify as natural proto-benchmarks
  │   (lowest mean δ₁, highest cross-expert consistency)
  └── Scoring precision improves

PHASE 3 — Mature corpus  (100+ poclets, multiple cooks)
  ├── Stable domain benchmarks established by consensus
  ├── Calibrated scoring → new poclets better positioned
  ├── Benchmarks refined by new evidence
  └── Cross-domain patterns become visible

PHASE 4 — Rich corpus  (multi-cook, multi-domain, multi-setup)
  ├── Inter-setup convergence → quasi-objective benchmarks
  ├── Universal attractors emerge across domains
  └── TSCG achieves strong intersubjective objectivity
```

### The Acceleration Effect

The virtuous circle **accelerates** with diversity:

```
More cooks      →  More poclets per domain
More poclets    →  Better benchmark identification
Better benchmarks →  More reliable scoring
More reliable scoring →  More cooks adopt TSCG
More cooks      →  More diverse setups
More diverse setups →  Stronger intersubjective consensus
                    →  cycle continues and strengthens
```

### TscgPocletMiner as Natural Benchmark Identifier

The TscgPocletMiner tool, with its RAG system over the growing corpus,
is structurally positioned to **automatically identify emerging benchmarks**
by finding cluster centroids in the ASFID/REVOI score space — poclets
with the lowest mean distance to all other poclets in their domain.

---

## 7. Mathematical Grounding

### Norm-Referenced Measurement

TSCG M0 scoring is a form of **norm-referenced measurement** — a
well-established branch of applied mathematics and measurement theory
(Stevens 1946; Lord & Novick 1968):

```
Criterion-referenced  :  score against an absolute standard
                          "is temperature > 37.5°C?"

Norm-referenced       :  score relative to a reference population
                          "how does this poclet compare to the
                           canonical benchmark for its domain?"
                          → this is what TSCG does
```

### Inter-Rater Reliability

When multiple independent experts score the same poclet against the
same benchmark, their convergence is measurable by established
statistical coefficients:

- **Cohen's Kappa κ**: agreement between two raters beyond chance
- **Intraclass Correlation Coefficient (ICC)**: agreement among
  multiple raters on continuous scales
- **Krippendorff's Alpha**: reliability across multiple raters
  and measurement scales

As the TSCG community grows, these metrics can quantify the
**objectivity level** achieved by each benchmark:

```json
"m3:intersubjectiveBenchmark": {
  "expertConsensus": {
    "numberOfExperts":  3,
    "convergenceScore": 0.84,
    "metric":           "ICC",
    "interpretation":   "strong agreement (> 0.75)"
  }
}
```

### Law of Large Numbers Applied

The statistical grounding: as N independent experts with different
setups converge on the same benchmark, the probability that the
benchmark reflects a genuine structural attractor approaches 1:

```
P(genuine attractor | N independent convergences) → 1  as  N → ∞
```

This is the law of large numbers applied to epistemology — exactly how
physical constants were established: not by decree, but by accumulated
independent measurement.

### Peirce's Limit of Inquiry

The philosophical formalisation (Charles Sanders Peirce, 1878):

> *"The opinion which is fated to be ultimately agreed to by all who
> investigate is what we mean by truth."*

Translated to TSCG:

> *The canonical benchmark for a domain is the poclet that all cooks,
> using all kitchens, investigating the same domain, are fated to
> converge upon — provisionally, defeasibly, until a better one emerges.*

---

## 8. Connection to REVOI

The intersubjective benchmark mechanism has a direct, measurable impact
on the REVOI scores of all poclets that use it:

| REVOI Dimension | Impact | Mechanism |
|---|---|---|
| **R** Representability | ↑ | Poclet calibrated against recognised domain canon |
| **E** Evolvability | ↑ | Benchmarks explicitly updatable by new consensus |
| **V** Verifiability | ↑↑ | Multi-cook convergence makes scores reproducible |
| **O** Observability | ↑ | Scoring methodology is explicit and documented |
| **I** Interoperability | ↑ | Shared benchmarks enable cross-team exchange |

**The systemic coherence**: the measurement device improves the scores
of what it measures. A poclet that is properly benchmark-calibrated
will score higher on Verifiability — the very dimension that validates
the calibration process. This is a rare and valuable **positive
feedback loop** in an ontological framework.

---

## 9. Formal Design

### The `m3:intersubjectiveBenchmark` Property

```json
{
  "@id":    "m3:intersubjectiveBenchmark",
  "@type":  "owl:ObjectProperty",
  "rdfs:label":   "intersubjective benchmark",
  "rdfs:comment": "Domain-contextualized canonical poclet(s) used as
                   scoring reference for M0 instances. Grounds TSCG
                   measurement in norm-referenced intersubjective
                   consensus. Defeasible by design — valid until
                   superseded by broader consensus.",

  "m3:structure": {

    "epistemicScore": {
      "property":     "m0:epistemicGap",
      "value":        "δ₁ ∈ [0.0, 1.0]",
      "formula":      "||ASFID_mean − REVOI_mean|| / √2",
      "interpretation": "SpectralClass (Coherent / OnCriticalLine /
                          Liminal / Enigmatic)"
    },

    "objectivityLevel": {
      "type":    "xsd:string",
      "values":  [
        "Subjective              — single expert, no reference",
        "MultiExpertConsensus    — several experts, same setup",
        "CanonCalibrated         — scored against domain benchmark",
        "ContextualizedBenchmark — multi-cook, multi-setup convergence"
      ],
      "default": "ContextualizedBenchmark"
    },

    "benchmarkRefs": {
      "type":        "array",
      "description": "Ordered list of canonical poclets used as anchors",
      "items": {
        "uri":       "IRI of canonical poclet",
        "domain":    "M1 domain  (e.g. m1:Biology, m1:Electronics)",
        "canonType": "DomainSpecific | CrossDomain | Universal",
        "weight":    "xsd:float  [0.0, 1.0]"
      }
    },

    "expertConsensus": {
      "numberOfExperts":  "xsd:integer",
      "convergenceScore": "xsd:float  (ICC / Cohen's κ)",
      "metric":           "ICC | CohensKappa | KrippendorffsAlpha",
      "method":           "comparative | absolute | hybrid"
    },

    "defeasibilityStatus": {
      "status":          "provisional",
      "validUntil":      "superseded_by_better_consensus",
      "revisionTrigger": [
        "new_canonical_poclet_identified",
        "expert_consensus_challenged",
        "domain_expansion",
        "corpus_maturation"
      ]
    }
  },

  "m3:resolutionOrder": [
    "1. DomainSpecific benchmark   (M1 domain of the poclet)   ← DEFAULT",
    "2. CrossDomain benchmark      (adjacent M1 domain)",
    "3. Universal benchmark        (e.g. M0_AdaptiveImmuneResponse)",
    "4. Free scoring + explicit justification                  ← last resort"
  ]
}
```

### Usage in a M0 Poclet

```json
"m3:intersubjectiveBenchmark": {
  "epistemicScore":    0.08,
  "objectivityLevel":  "ContextualizedBenchmark",
  "benchmarkRefs": [
    {
      "uri":       "instances/poclets/electronics/M0_Transistor.jsonld",
      "domain":    "m1:Electronics",
      "canonType": "DomainSpecific",
      "weight":    1.0
    }
  ],
  "expertConsensus": {
    "numberOfExperts":  1,
    "convergenceScore": null,
    "metric":           "ICC",
    "method":           "comparative"
  },
  "defeasibilityStatus": {
    "status":   "provisional",
    "validUntil": "superseded_by_better_consensus"
  }
}
```

---

## 10. Philosophical Grounding

Three philosophical traditions converge on this concept:

**Popper — Falsifiability (1934)**
> Scientific knowledge is always provisional and falsifiable.
> A benchmark is TSCG's equivalent of a falsifiable hypothesis —
> held until refuted by broader evidence.

**Kuhn — Paradigm Shifts (1962)**
> Consensus knowledge is organised around paradigms that hold until
> anomalies accumulate. Benchmark poclets are TSCG's paradigms —
> stable attractors of domain knowledge, revisable when the corpus
> outgrows them.

**Peirce — Pragmatism and the Limit of Inquiry (1878)**
> Truth is the limit toward which the indefinite community of
> investigators converges. TSCG benchmarks are exactly this:
> provisional limits of a growing, diversifying community of cooks.

---

## 11. Summary

### What Has Been Identified

```
1. EPISTEMOLOGICAL KEY
   TSCG M0 scores are defeasible intersubjective measurements —
   not absolute truths, but consensual anchors valid "until further
   notice." This is the normal epistemic status of scientific,
   legal, and practical knowledge.

2. MATHEMATICAL KEY
   Norm-referenced measurement (Stevens 1946) + inter-rater
   reliability (ICC, Cohen's κ) provide rigorous statistical
   grounding for TSCG scoring — without requiring physical
   measurement or Hilbert spaces.

3. SYSTEMIC KEY
   The contextualized benchmark (canon by M1 domain) is the
   DEFAULT case. Universal benchmarks are fallbacks.

4. VIRTUOUS CIRCLE
   Corpus growth → better benchmark identification → better
   calibration → more cooks → more diverse setups → stronger
   intersubjective consensus → better benchmarks → ...

5. THE COOK/KITCHEN INSIGHT
   Convergence of DIFFERENT cooks using DIFFERENT kitchens
   (LLMs, corpora, domains) is the engine of quasi-objectivity.
   Independent convergence is the TSCG equivalent of independent
   laboratory replication in science.

6. REVOI COHERENCE
   The benchmark mechanism improves the very REVOI scores
   (V, R, O, I, E) that validate it — a positive feedback loop
   rare in ontological frameworks.
```

### The One-Sentence Formulation

> *TSCG benchmarks are provisional structural attractors of
> conceptual domains — identified by multi-cook convergence,
> domain-contextualized by default, explicitly defeasible by design,
> and self-improving through corpus growth.*

---

## References

- Stevens, S.S. (1946). *On the theory of scales of measurement.*
  Science, 103(2684), 677–680.
- Lord, F.M. & Novick, M.R. (1968). *Statistical theories of mental
  test scores.* Addison-Wesley.
- Popper, K. (1934). *Logik der Forschung.* Springer.
- Kuhn, T.S. (1962). *The Structure of Scientific Revolutions.*
  University of Chicago Press.
- Peirce, C.S. (1878). *How to Make Our Ideas Clear.*
  Popular Science Monthly.
- Cohen, J. (1960). *A coefficient of agreement for nominal scales.*
  Educational and Psychological Measurement, 20(1), 37–46.
- Koo, T.K. & Mae, A.Y. (2016). *A guideline for selecting and
  reporting intraclass correlation coefficients.* Journal of
  Chiropractic Medicine, 15(2), 155–163.

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
