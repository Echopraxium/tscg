# The TSCG Scoring System
## δ₁ (Epistemic Gap) and δ₂ (Focal Score)
### Two Complementary Measures of Map–Territory Relationship

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-07-08  
**Framework**: TSCG (Transdisciplinary System Construction Game) v16.2.0+  
**Status**: Reference — scoring definitions extracted from the main README  
**Location**: `docs/CoreHypotheses/ScoringSystem.md`  
**See also**: `docs/CoreHypotheses/TerritoryMap_Dichotomy.md`,
`docs/CoreHypotheses/_00_TSCG_as_StereoscopicGlasses.md`,
`docs/CoreHypotheses/MultisubjectiveScoreEvaluationProtocol.md`

---

## Purpose of This Document

The main `README.md` keeps only the *what* and the *why* of TSCG scoring:
there are two measures, one for Map/Territory **alignment** (δ₁) and one
for Map/Territory **fusion sharpness** (δ₂). This document holds the
*how* — the exact formulas, thresholds, and underlying primitives —
deliberately kept out of the overview so a first-time reader is not asked
to parse an ophthalmic formula before deciding whether TSCG is relevant
to them.

A reminder on epistemic status, consistent with the rest of the
framework: these scores are **intersubjective judgments**, not absolute
measurements. They are revisable as the evaluating community grows (see
`MultisubjectiveScoreEvaluationProtocol.md`). Their usefulness remains to
be demonstrated by evaluators other than the framework's author.

---

## 1. δ₁ — The Epistemic Gap

Every M0 instance is scored on two five-dimensional bases:

- **ASFID** (Territory / Eagle Eye) — **A**ttractor, **S**tructure,
  **F**low, **I**nformation, **D**ynamics. Answers *"what is the system
  doing?"*
- **REVOI** (Map / Sphinx Eye) — **R**epresentability, **E**volvability,
  **V**erifiability, **O**bservability, **I**nteroperability. Answers
  *"how well can we model it?"*

Each dimension is scored in `[0, 1]`. The epistemic gap is the normalized
distance between the two means:

```
δ₁ = |ASFID_mean − REVOI_mean| / √2
```

The `√2` normalizes the maximum possible gap to `1`, so δ₁ ∈ [0, 1].

### Spectral Classes

δ₁ sorts instances into qualitative bands. A small δ₁ means Map and
Territory agree; a large δ₁ flags a mismatch worth investigating (which
is a *finding*, not a failure).

| Spectral Class | δ₁ Range | Interpretation |
|----------------|----------|----------------|
| **Coherent** | δ₁ < 0.05 | Map and Territory strongly agree |
| **OnCriticalLine** | 0.05 ≤ δ₁ < 0.15 | Minor, expected divergence |
| **Liminal** | 0.15 ≤ δ₁ < 0.30 | Noticeable mismatch to examine |
| **Enigmatic** | δ₁ ≥ 0.30 | Strong mismatch — model or observation questioned |

---

## 2. δ₂ — The Focal Score (EFS)

δ₂, also called the **Epistemic Focal Score (EFS)**, measures a different
thing than δ₁. Where δ₁ measures *distance* between the two perspectives,
δ₂ measures the *sharpness of their fusion* — an ophthalmic metaphor
borrowed from binocular vision. Two eyes that are merely close together
(low δ₁) do not automatically yield a sharp stereoscopic image; the image
still has to come into focus. δ₂ captures that second, orthogonal quality.

```
δ₂ = EFS = stereopsicDepth × (1 − |focalBias|)
```

### 2.1 stereopsicDepth

The depth of engagement of the Stereopsis grammar **Gs**, computed from
which of the four TKSL primitives are active in the instance:

```
stereopsicDepth = (T_present × 0.25)
                + (K_present × 0.25)
                + (Ss_present × 0.25)
                + (L_present × 0.25)
```

Each present primitive contributes `0.25`, so `stereopsicDepth ∈ {0,
0.25, 0.5, 0.75, 1.0}`.

### 2.2 focalBias

The signed Map/Territory imbalance:

```
focalBias = REVOI_mean − ASFID_mean   ∈ [−1, +1]
```

| Sign | Regime | Meaning |
|------|--------|---------|
| **Positive** | **Hyperopic** | Map too abstract, Territory blurred |
| **Negative** | **Myopic** | Territory too detailed, Map inadequate |
| **Zero** | **Emmetropic candidate** | Balanced Map and Territory |

### 2.3 Focal Classes

The resulting EFS sorts instances by the sharpness of their combined
image:

| Focal Class | EFS Range | Meaning |
|-------------|-----------|---------|
| **Emmetropic** | EFS ≥ 0.70 | Sharp combined image — Map + Territory in focus |
| **SlightlyMyopic / SlightlyHyperopic** | 0.50 ≤ EFS < 0.70 | Slight bias toward Territory or Map |
| **Myopic / Hyperopic** | 0.30 ≤ EFS < 0.50 | Significant Map/Territory imbalance |
| **Astigmatic** | EFS < 0.30 | Insufficient Gs depth — no stereopsis possible |

---

## 3. The TKSL Primitives

The four nominal generators of the Stereopsis grammar **Gs**. Each answers
one transcendental question, and each acts as a bridge between two of the
other TSCG structures:

| Primitive | Name | Question | Role |
|-----------|------|----------|------|
| **T** | Temporality | *When?* | Temporal interface Gt ↔ Gm |
| **K** | Knowledge | *What?* | Cognitive contextualisation of Information |
| **Ss** | Symbol *(Stereopsic)* | *Sign?* | Semiotic bridge signifier ↔ signified |
| **L** | Localizability | *Converging?* | Cybernetic convergence toward Attractor |

The full Base16 alphabet of Gs, including the `_^` / `_$` poles, is:

```
𝕋₀(|) = { T, _^, _$, K, Ss, L }
```

with the Stereopsis grammar written formally as the bicephalous monoid
`(Gs, |, EmptyStereopsis)`.

---

## 4. When Does δ₂ Apply?

δ₂ is **optional and conditional**. It is present only in M0 instances
that mobilize at least one *stereopsic* GenericConcept — signalled by the
flag `m0:focalApplicable = true`. Instances that do not engage the
Stereopsis grammar carry only δ₁.

This conditionality is intentional. Not every system model needs the
third measure; forcing δ₂ on instances that do not warrant it would be
its own form of overfitting.

---

## 5. The Two Scores Side by Side

| Score | Formula | Measures | Question |
|-------|---------|----------|----------|
| **δ₁** (epistemic gap) | `\|ASFID_mean − REVOI_mean\| / √2` | Map/Territory *alignment* (distance) | *How far apart?* |
| **δ₂ / EFS** (focal score) | `stereopsicDepth × (1 − \|focalBias\|)` | Map+Territory *fusion sharpness* (binocular depth) | *How in-focus?* |

The two are complementary, not redundant: an instance can have a small δ₁
(Map and Territory close) yet a poor δ₂ (the fusion never sharpens into
usable depth), and vice versa.

---

## Changelog

- **2026-07-08** — Initial version. Scoring definitions (δ₁ spectral
  classes, δ₂/EFS formula, TKSL primitives, focal classes) migrated out
  of the main `README.md` to reduce the overview's cognitive load.
