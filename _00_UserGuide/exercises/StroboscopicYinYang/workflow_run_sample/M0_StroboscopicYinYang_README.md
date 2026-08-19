# Stroboscopic Yin-Yang — TSCG Instance

*Author: Echopraxium with the collaboration of Claude AI — 2026-08-19 — v1.0.0*

## Overview

A **Poclet** modelling how a spinning **order-2 symmetric yin-yang disc**, when
**discretely sampled** by the eye (retinal persistence) or a strobe, produces
different **perceived regimes** — smooth rotation, a **frozen** figure, or apparent
**reversal** (the wagon-wheel effect). Its whole point is to make the reduction
**Φ: Gt → Gm** — from a continuous *Territory* to a sampled *Map* — directly visible,
and directly **verifiable by the reader's own eyes**.

## System Description

A yin-yang disc rotates at true angular speed **ω** (the Territory). The observer does
not see the continuous motion; it is **sampled** at rate **f_s** (retina ~1/16 s, or a
strobe frame rate). The interaction of the two rates governs perception:

| Regime | Condition | What you perceive |
|---|---|---|
| Smooth rotation | ω ≪ f_s | Faithful — Map ≈ Territory |
| Frozen figure | ω = k·f_s | Apparent standstill (fixed point of *perception*) |
| Apparent reversal | ω slightly above k·f_s | Wagon-wheel effect — disc seems to spin backwards |
| Morphing pattern | ω near half-integer multiples of f_s | Doubled / shifting, unstable figures |

Because of the disc's **order-2 symmetry**, freeze and reversal recur **twice as often**
as they would for a single-mark wheel.

## TSCG Analysis

### ASFID State (Territory / Eagle Eye)

| Dim | Score | Reading |
|---|---|---|
| A — Attractor | 0.30 | Weak/honest: no convergence state; freeze points belong to perception, not the disc |
| S — Structure | 0.65 | Order-2 rotational symmetry + sampling apparatus |
| F — Flow | 0.80 | Continuous rotation (Territory) vs discrete sample stream (Map) |
| I — Information | 0.90 | Drivers ω, f_s, φ — dominant |
| D — Dynamics | 0.90 | The beat between two rates — dominant |

`|Ω_disc⟩ = 0.30|A⟩ + 0.65|S⟩ + 0.80|F⟩ + 0.90|It⟩ + 0.90|D⟩` · asfidMean **0.71**

### REVOI State (Map / Sphinx Eye)

| Dim | Score | Reading |
|---|---|---|
| R — Representability | 0.85 | One disc + two sliders |
| E — Evolvability | 0.75 | Generalises to any sampled continuous process |
| V — Verifiability | 0.95 | Confirmed by the reader's own eyes — first-person falsifiability |
| O — Observability | 0.90 | Freeze/reversal directly perceptible |
| Im — Interoperability | 0.85 | "Aliasing" shared across audio, imaging, film |

`|M_perceived⟩_REVOI = 0.85|R⟩ + 0.75|E⟩ + 0.95|V⟩ + 0.90|O⟩ + 0.85|Im⟩` · revoiMean **0.86**

### Epistemic Gap

**δ₁ = |0.71 − 0.86| / √2 = 0.106 → OnCriticalLine** (0.05 ≤ δ₁ < 0.15).
The gap is not model error; it **is** the phenomenon — perception builds a Map that
legitimately diverges from the Territory. Focal (Gs): stereopsicDepth 0.75,
focalBias +0.15, **focalScore ≈ 0.64 → SlightlyHyperopic** (the perceived Map is
marginally dominant over the raw Territory — exactly the lesson).

## Components

1. **Rotating Yin-Yang Disc** (`m2:System`) — the Territory; continuous rotation,
   order-2 symmetry. Contributes S, F, D.
2. **Sampler / Retina / Strobe** (`m2:Channel`) — the Map-building apparatus; two modes
   (retinal persistence → motion blur; stroboscopic sampling → aliasing). Contributes
   F, I, D.
3. **Perceived Image** (`m2:Representation`) — the Map; encodes the regime. Contributes
   weak A, I.

Drivers: **ω** (rotation rate, Territory), **f_s** (sampling rate, Map), **φ** (phase).

## GenericConcepts Mobilized

**23 total**, formulas verified against `M2_GenericConcepts.jsonld` at HEAD
(operators `×` Gt · `+` Gm · `|` Gs; `⊗` forbidden):

- **Structural:** Symmetry (`St`), Component (`St × It | L`), System (`St × F`), Topology (`St | L`)
- **Dynamic:** Process (`D × F`), Trajectory (`A × D × F`), Transformation (`D × St × It`), Bifurcation (`D × F | L`)
- **Regulatory:** Threshold (`A × It`), Trigger (`D × It`)
- **Informational:** Signal (`It × F`), Channel (`St × F | Ss`), Transducer (`F × St × It`),
  Coding (`It × St × D`), Segmentation (`St × It × D`), Representation (`It × St`),
  Signature (`It × Ss | V`), State (`It`), Pattern (`St × It × A | K`)
- **Epistemic:** Observer (`It × A`), Observable, Coherence/Incoherence (`A × St × It | R + O`),
  Modelisation (`D × F × It | R + V + E`)

## Key Insights

- **Sampling has no single M2 concept** — it emerges from a *cluster* (Transducer +
  Channel + Segmentation + Coding). That absence is itself a finding.
- **The freeze is in the eye, not the disc.** A perfect illustration of the
  Territory/Map distinction and of observer-relativity (`m2:Observer`).
- **Self-verifying poclet.** The reader tests the model against their own perception —
  the reason V = 0.95.

## Transdisciplinary Analogies

The same aliasing artifact recurs across domains — the basis for the flagged M2
candidate: digital-audio foldback, moiré patterns, strobing wheels on film, strobe
photography, and any Nyquist-rate violation.

## Framework Findings

- **New-domain (Gap):** no `Perception`/`psychophysics` M1 extension at HEAD (verified
  404; `optics` exists but models light/lenses, not temporal sampling). `m1:domain =
  "Perception"` set as a free string; registering a full `M1_Perception.jsonld` is
  **deferred** pending a second perception poclet.
- **M2 candidate (flag only):** *Aliasing (Stroboscopic Sampling Artifact)*, proposed
  `F × D × It | Ss` — held under the anti-overfitting rule (needs ≥6 independent domains).

## Validation

- SHACL: **Conforms: True** against `M0_Instances_Schema.shacl.ttl` (v1.6) at HEAD
  (Pattern-B flat scores, all namespaces absolute, focal block coherent).
- ASFID completeness ✅ · 23 GenericConcepts ✅ · minimality (3+3) ✅ · emergence ✅ ·
  first-person verifiability ✅.

## References

- Wikipedia — *Persistence of vision*, *Wagon-wheel effect*, *Stroboscopic effect*
- Nyquist–Shannon sampling theorem (temporal aliasing)

*Note: these are standard references cited from the exercise brief; verify any specific
citation independently.*
