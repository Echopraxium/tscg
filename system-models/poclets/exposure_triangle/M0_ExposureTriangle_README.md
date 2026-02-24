# M0_ExposureTriangle — TSCG Poclet README

**Poclet:** `M0_ExposureTriangle`  
**Domain:** Photography / Optics / Image Formation  
**Version:** 1.2.0 · **Date:** 2026-02-24  
**Author:** Echopraxium with the collaboration of Claude AI  
**Ontology URI:** `https://raw.githubusercontent.com/Echopraxium/tscg/main/system-models/poclets/exposure_triangle/M0_ExposureTriangle.jsonld`  
**Status:** ACTIVE — Canonical pedagogical model

---

## Table of Contents

1. [Overview](#1-overview)
2. [System Description](#2-system-description)
3. [ASFID Analysis (Eagle Eye — Territory)](#3-asfid-analysis-eagle-eye--territory)
4. [REVOI Analysis (Sphinx Eye — Map)](#4-revoi-analysis-sphinx-eye--map)
5. [Epistemic Gap](#5-epistemic-gap)
6. [Metaconcepts Mobilized (22)](#6-metaconcepts-mobilized-22)
7. [M2 Metaconcepts Discovered from this Poclet](#7-m2-metaconcepts-discovered-from-this-poclet)
8. [Map–Territory Comparison](#8-mapterritory-comparison)
9. [Analogy to the Fire Triangle](#9-analogy-to-the-fire-triangle)
10. [Validation](#10-validation)
11. [Future Extensions](#11-future-extensions)
12. [Simulation (exposure_triangle_sim.py)](#12-simulation-exposure_triangle_simpy)
13. [Changelog](#13-changelog)

---

## 1. Overview

The **Exposure Triangle** is the canonical pedagogical model of photography. It represents the three interdependent parameters that govern the amount of light reaching the camera sensor:

| Parameter | Physical Role | Primary Effect |
|-----------|--------------|----------------|
| **ISO** | Sensor gain (signal amplification) | Brightness ↑, Noise ↑ |
| **Aperture** (f-number) | Lens opening area (light flux control) | Brightness ↑/↓, Depth of Field ↔ |
| **Shutter Speed** | Exposure duration (temporal integration) | Brightness ↑, Motion Blur ↔ |

**Core physical law:**

```
Exposure ∝ ISO × Aperture_Area × Time
```

In logarithmic stop space:
```
log₂(ISO) + log₂(1/f²) + log₂(T) = log₂(Scene_Luminance) + K
```

Every stop (+1 or −1) represents a doubling or halving of light. This makes compensatory adjustments symmetric: `+1 stop ISO` exactly compensates `−1 stop Aperture` or `−1 stop Shutter`.

**Pedagogical role:** The Exposure Triangle is the universal teaching model for photographic exposure — equivalent to the Fire Triangle for combustion, the OSI model for networking, or the Iron Triangle for project management. A simple Map that simplifies a complex Territory with remarkable practical effectiveness.

---

## 2. System Description

### 2.1 Components

#### ISO Sensitivity (Sensor Gain)
- **Physical correlate:** Analog = film grain/silver halide concentration; Digital = voltage amplification of photosensor output
- **Range:** ISO 100–204800 (professional cameras)
- **Log scale:** Each ISO doubling = +1 stop
- **ASFID tensor:** `S ⊗ I` (Structure of sensor architecture × Information amplification)
- **Trade-off:** Higher ISO → brighter image **but** more grain/noise (SNR degrades)

#### Aperture (f-number / f-stop)
- **Physical correlate:** Iris diaphragm; light area ∝ 1/N² where N = f-number
- **Range:** f/1.4 to f/22 (lens dependent)
- **Full stop scale:** f/1.4, f/2, f/2.8, f/4, f/5.6, f/8, f/11, f/16, f/22, f/32
- **ASFID tensor:** `S ⊗ F` (Structure of iris geometry × Flow of photons entering)
- **Trade-off:** Wide aperture (f/1.4) → more light, shallow DoF; Narrow aperture (f/16) → less light, deep DoF

#### Shutter Speed (Exposure Time)
- **Physical correlate:** Mechanical curtain or electronic shutter duration
- **Range:** 30s to 1/8000s (+ Bulb mode)
- **Hand-holding rule:** T ≥ 1/focal_length (e.g. 50mm lens → 1/50s minimum)
- **ASFID tensor:** `F ⊗ D` (Temporal flux accumulation × Temporal dynamics of scene)
- **Trade-off:** Fast shutter → freezes motion; Slow shutter → motion blur, more light

### 2.2 The Reciprocity Law

Any combination satisfying the exposure equation yields the **same total exposure** (same histogram brightness), but with **different image qualities**:

```
ISO 400 + f/4 + 1/250s  →  Same EV as:
ISO 800 + f/5.6 + 1/250s  (same exposure, shallower DoF)
ISO 400 + f/4 + 1/500s  (same exposure, frozen motion ↑)
```

This is the fundamental **Trade-off** (m2:Trade-off): infinite equivalent exposures on the Pareto frontier, each sacrificing one quality dimension to gain another.

---

## 3. ASFID Analysis (Eagle Eye — Territory)

Territory state vector: `|Ω_exposure⟩ = 0.80|A⟩ + 0.85|S⟩ + 0.95|F⟩ + 0.75|I⟩ + 0.60|D⟩`

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **A** Attractor | 0.80 | System converges toward correct exposure (metering system acts as set-point) |
| **S** Structure | 0.85 | Three-parameter coupling ISO × Aperture × Time with well-defined logarithmic interdependence |
| **F** Flow | 0.95 | Massive photon flux (10¹⁵–10¹⁸ photons per typical exposure) — dominant physical phenomenon |
| **I** Information | 0.75 | Spatial + spectral + temporal information encoded in captured photons |
| **D** Dynamics | 0.60 | Exposure spans milliseconds to seconds — present but not fast-changing dynamics |

**ASFID completeness:** All 5 dimensions present ✅

---

## 4. REVOI Analysis (Sphinx Eye — Map)

Map state vector: `|M_triangle⟩_REVOI = 0.95|R⟩ + 0.85|E⟩ + 0.95|V⟩ + 0.95|O⟩ + 0.90|I⟩`

**REVOI_mean = 0.92 → Exceptional Map quality**

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **R** Representability | 0.95 | Perfectly representable: triangular diagram, stop arithmetic (±1, ±2, ±3 stops), log₂ formula. `spaceCoverage ≈ 0.65` (covers 3 parameters + trade-offs; omits scene luminance, metering, optical physics) |
| **E** Evolvability | 0.85 | Evolved from film to digital (ISO now variable per shot). Extends gracefully to computational photography (HDR, AI metering) without becoming obsolete |
| **V** Verifiability | 0.95 | Predictions testable instantly: change any parameter → immediate visual feedback (histogram, chimping). Reproduced by millions of photographers daily |
| **O** Observability | 0.95 | Ubiquitous in every photography textbook, tutorial, camera manual. Photographers internalize it as muscle memory through practice |
| **I** Interoperability | 0.90 | Lingua franca of photography. Works across film/digital, all camera brands. Formalized in EXIF standard (ISO 12234) |

### REVOI Map Analysis State (also encoded in ASFID for comparison)

Map ASFID state: `|M_triangle⟩ = 0.85|A⟩ + 0.95|S⟩ + 0.70|F⟩ + 0.85|I⟩ + 0.50|D⟩`

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **A** | 0.85 | Strong pedagogical attractor — teaches correct exposure with high clarity |
| **S** | 0.95 | Perfect triangular geometry (3 vertices, 3 edges — minimal and complete) |
| **F** | 0.70 | Moderate — conceptual flow only (no actual photon flux in the diagram) |
| **I** | 0.85 | High — encodes 3 parameters + trade-off relationships |
| **D** | 0.50 | Low — static diagram (does not model the temporal adjustment process) |

> **Sphinx Eye insight:** Why does the Exposure Triangle work so well as a teaching tool?
> 1. Reduces complex optics physics to 3 intuitive parameters  
> 2. Immediate visual feedback reinforces learning in every practice session  
> 3. Trade-offs are universal human experience (no free lunch) — the model resonates cognitively  
> — *Korzybski principle: the Map simplifies the Territory, but captures the essential structure for practical decision-making.*

---

## 5. Epistemic Gap

```
ΔΘ = ‖|Ω_exposure⟩ − |M_triangle⟩‖ ≈ 0.32
```

Deviation vector: `(−0.05, −0.10, +0.25, +0.10, +0.10)`

| Dimension | Gap | Interpretation |
|-----------|-----|----------------|
| **F (Flow)** | +0.25 | Largest divergence: Territory has massive photon flux (10¹⁸ photons); Map is abstract diagram with no actual flow representation |
| **S (Structure)** | −0.10 | Territory has complex sensor/lens/optics physics; Map reduces to simple triangle |
| **I, D** | +0.10 each | Information and dynamics richer in Territory than the static diagram captures |

**Assessment:** Moderate gap (ΔΘ ≈ 0.32) — the Triangle is a good pedagogical Map but simplifies the Territory significantly. This is by design, not a defect: the Triangle's strength lies in its deliberate simplification.

**Known limitations of the Map:**
- Omits scene luminance (the 4th implicit parameter)
- Ignores metering system complexity (TTL, spot, matrix metering algorithms)
- Simplifies optical physics (diffraction limit at f/16+, lens aberrations)
- Doesn't model reciprocity failure (film limitation at extreme exposures)
- Static — doesn't represent the dynamic feedback adjustment process

---

## 6. Metaconcepts Mobilized (22)

**Coverage: 22 of 71 M2 metaconcepts (31%)**  
`m3:semanticSignature`: `light_balance_attractor + parameter_trade-off_map + photon_flow_amplification`

| # | Metaconcept | Formula | Role in Exposure Triangle |
|---|-------------|---------|---------------------------|
| 1 | `m2:Balance` | `A ⊗ S ⊗ F` | Equilibrium: ISO × Aperture × Shutter → correct exposure via compensatory stops |
| 2 | `m2:Trade-off` | `R ⊗ V ⊗ E` (REVOI) / `A ⊗ I` (fallback) | Cannot simultaneously maximize DoF, freeze motion, minimize noise — Pareto frontier |
| 3 | `m2:Amplification` | `Ft ⊗ D ⊗ It` | ISO = sensor signal amplification (+1 stop = ×2 gain); ND filter = attenuation |
| 4 | `m2:FeedbackLoop` | `Process ⊗ Alignment ⊗ Homeostasis` | Camera metering = negative feedback loop (scene → meter → compare EV → adjust) |
| 5 | `m2:Polarity` | `S ⊗ I ⊗ A` | Stops scale: bipolar axis centered on correct exposure (over-/under-exposed as opposing poles) |
| 6 | `m2:Behavior` | `S ⊗ D ⊗ F` | Photographer's structured exposure evaluation routine (observe → meter → assess → adjust → capture → review) |
| 7 | `m2:Component` | `S ⊗ I` | ISO, Aperture, Shutter as elementary constitutive parts |
| 8 | `m2:Synergy` | `A ⊗ S ⊗ I` | Multiplicative (not additive) interaction: E ∝ ISO × Area × Time |
| 9 | `m2:Constraint` | `S ⊗ I` | Physical limits: ISO [100–25600], Aperture [f/1.4–f/22], Shutter [1/8000–30s] |
| 10 | `m2:Threshold` | `A ⊗ I` | Critical transitions: 1/focal_length rule, ISO >1600 (visible noise), f/16 (diffraction) |
| 11 | `m2:Regulation` | `A ⊗ S ⊗ F` | Auto-exposure modes (AE, Av, Tv) — camera adjusts parameters to maintain target EV |
| 12 | `m2:Signal` | `I ⊗ F` | Light as information carrier: photon flux encodes scene luminance, color, spatial info |
| 13 | `m2:Code` | `I ⊗ S ⊗ D` | EXIF metadata: ISO/Aperture/Shutter encoded in image file per ISO 12234 standard |
| 14 | `m2:Representation` | `I ⊗ S` | Triangle diagram as Map; `spaceCoverage ≈ 0.65` |
| 15 | `m2:Space` | `S ⊗ I` | 3D exposure parameter space (ISO, Aperture, Shutter) — all possible settings |
| 16 | `m2:Invariant` | `S ⊗ A` | EV = log₂(ISO × A² / T) invariant across all equivalent settings for same scene luminance |
| 17 | `m2:Transformation` | `D ⊗ I ⊗ S` | Equivalent exposure conversions: ISO 400 + f/4 + 1/250 ↔ ISO 800 + f/5.6 + 1/250 |
| 18 | `m2:Process` | `D ⊗ F` | Exposure as temporal process: photon accumulation from shutter open to close |
| 19 | `m2:Event` | `D ⊗ I` | Shutter actuation as discrete capture event |
| 20 | `m2:Memory` | `∫(D − F)dτ` | Photographer's learned exposure intuition (muscle memory from thousands of shots) |
| 21 | `m2:Adaptation` | `I ⊗ F ⊗ D` | ISO ramp across lighting conditions: ISO 100 (noon) → ISO 6400 (dusk) |
| 22 | `m2:Language` | `I ⊗ S ⊗ F` | Photography jargon: 'stop down to f/8', '+2 EV compensation', 'push 2 stops' |

### By Category

| Category | Metaconcepts |
|----------|-------------|
| **Structural** | Component, Space, Representation |
| **Informational** | Signal, Code, Language |
| **Regulatory** | Balance, Trade-off, Regulation, Constraint, Threshold, Polarity |
| **Dynamic** | Process, Event, Transformation, Adaptation, Amplification, FeedbackLoop, Behavior |
| **Adaptive** | Memory |
| **Relational** | Synergy, Invariant |

---

## 7. M2 Metaconcepts Discovered from this Poclet

The Exposure Triangle poclet served as the **discovery context** for two M2 metaconcepts that were subsequently validated across 8+ disciplines and promoted to established M2 status:

### m2:Balance  `A ⊗ S ⊗ F`

> *State of equilibrium between multiple interacting factors where variations compensate to maintain system stability.*

**Discovered via:** The compensatory stops arithmetic — `+1 ISO stop` exactly cancels `−1 Aperture stop`. This is not Homeostasis (dynamic active regulation) nor Regulation (mechanism) — it is a **static equilibrium state** achieved through mutual parameter compensation.

**Validated in 8 domains:** Photography, Chemistry (chemical equilibrium), Thermodynamics (energy balance), Economics (trade balance), Ecology (predator-prey), Audio engineering (frequency balance), Nutrition (macronutrient balance), Accounting (balance sheet).

### m2:Trade-off  `R ⊗ V ⊗ E` (REVOI) / `A ⊗ I` (ASFID fallback)

> *Deliberate exchange where improving one desirable property necessarily degrades another due to inherent constraints.*

**Discovered via:** The photographer's dilemma — no exposure setting simultaneously maximizes depth of field, freezes motion, AND minimizes noise. The Triangle makes the Pareto frontier explicit.

**Validated in 8 domains:** Photography (DoF/Grain/Motion), Machine Learning (Bias-Variance), Engineering (Speed-Accuracy), Economics (Inflation-Unemployment), Project Management (Cost-Quality-Time), Computer Science (Time-Space complexity), Biology (r-K selection), Reinforcement Learning (Exploration-Exploitation).

> **Architectural note:** `m2:Trade-off` has `m2:perspective: "map"` — it is a Map-space metaconcept (the photographer's decision model), not a Territory-space observable. This is why its primary formula uses REVOI dimensions (`R ⊗ V ⊗ E`) with ASFID as fallback (`A ⊗ I`).

---

## 8. Map–Territory Comparison

| Aspect | Territory (Physical Reality) | Map (Exposure Triangle) |
|--------|------------------------------|------------------------|
| **Phenomenon** | Photon accumulation on sensor (quantum events) | Abstract diagram (3 vertices, 3 edges) |
| **Parameters** | ISO, Aperture, Shutter + Scene Luminance + Metering | Only ISO, Aperture, Shutter |
| **Flow** | 10¹⁵–10¹⁸ photons per exposure | Conceptual arrows between vertices |
| **Physics** | Diffraction, aberrations, reciprocity failure, ADC noise | Simplified linear model |
| **Dynamics** | Milliseconds (shutter) to hours (astrophotography) | Static, timeless diagram |
| **REVOI quality** | — | R=0.95, E=0.85, V=0.95, O=0.95, I=0.90 → Mean 0.92 |
| **Epistemic gap** | — | ΔΘ ≈ 0.32 (moderate, pedagogically acceptable) |

---

## 9. Analogy to the Fire Triangle

The Exposure Triangle is structurally analogous to the **Fire Triangle** (Fuel ⊗ O₂ ⊗ Heat → Fire):

| Dimension | Fire Triangle | Exposure Triangle |
|-----------|--------------|-------------------|
| **Structure** | 3-component synergistic system | 3-component synergistic system |
| **Removal test** | Remove ANY component → fire stops | Set any parameter to extreme → no usable image (ISO≈0, f/∞, T≈0) |
| **Dominant principle** | Synergy (emergent chemical reaction) | Balance (equilibrium of light parameters) |
| **Pedagogy** | Universal for fire safety training | Universal for photography education |
| **Map limitation** | Omits chain reaction → led to Fire Tetrahedron | Omits scene luminance → could extend to Exposure Square |
| **TSCG layer** | `M0_FireTriangle` | `M0_ExposureTriangle` |

Both are **Canonical Pedagogical Triangle** poclets — the TSCG type `m3:TscgOntologyType` for this class of reducible, 3-component teaching models.

---

## 10. Validation

| Criterion | Status |
|-----------|--------|
| ASFID completeness (all 5 dimensions present) | ✅ |
| Minimality (exactly 3 components, irreducible) | ✅ |
| Emergence (correct exposure emerges from parameter balance) | ✅ |
| Balance & Trade-off validated in M2 (v15.1.0, 8 domains each) | ✅ |
| Metaconcept coverage (22 of 71 M2 = 31%) | ✅ |
| New metaconcepts v1.1.0 (Amplification, FeedbackLoop, Polarity, Behavior) | ✅ |
| spaceCoverage ValueSpace on m2:Representation (RSC ≈ 0.65) | ✅ |
| REVOI analysis complete (Mean = 0.92) | ✅ |
| JSON-LD encoding valid | ✅ |

---

## 11. Future Extensions

### Exposure Square (4th parameter)
Add **Scene Luminance** (EV of the scene) as 4th explicit parameter, making the implicit assumption of the Triangle explicit. The Square would have lower epistemic gap (ΔΘ < 0.20) at the cost of pedagogical simplicity.

### Computational Photography Layer
Modern cameras and AI are reducing Trade-off severity without eliminating it:

| Technology | Trade-off addressed | Method |
|-----------|-------------------|--------|
| HDR | Dynamic range vs single exposure | Multi-exposure merge |
| Focus stacking | DoF vs sharpness | Multi-focus merge |
| AI noise reduction | ISO noise vs resolution | Neural denoising |
| IBIS / OIS | Shutter speed vs shake | Optical/sensor stabilization |
| Computational exposure | All three | Real-time AI parameter optimization |

These extend the Triangle's Map but do not obsolete it — the physical law `E ∝ ISO × A × T` remains invariant.

### Ansel Adams Zone System
Extension of the Triangle to a 10-zone tonal mapping system (Zone 0 = pure black, Zone X = pure white). Adds explicit tonal placement awareness to the exposure decision — a more complete Map (spaceCoverage ≈ 0.80 vs. Triangle's ≈ 0.65).

---

## 12. Simulation (exposure_triangle_sim.py)

The poclet is accompanied by an interactive Pygame simulation that applies **live photo effects** to a sample image (`photo_sample.jpg`) driven by the three exposure parameter sliders.

### Sample Image

`photo_sample.jpg` — Autumn maple leaves on wet cobblestones. Used as reference scene because it contains:
- Fine-grain texture (cobblestone joints) that clearly shows **ISO noise** artifacts
- Both bright (yellow leaves) and dark (wet stone) tonal zones that reveal **over/under-exposure** clipping
- Natural colour richness that highlights **white-balance neutrality** at the baseline exposure

**Baseline exposure** (EV offset = 0): `ISO 400 · f/5.6 · 1/250s`

### Visual Effects per Parameter

| Parameter | Effect on Image | Physical Justification |
|-----------|----------------|------------------------|
| **ISO** | Grain/noise overlay — amplitude grows from 0 (ISO 100) to ±55 px (ISO 6400) | Signal amplification raises both signal and read noise proportionally |
| **Aperture** | Edge vignette (DoF indicator) — active below f/4, maximum at f/1.4 | Shallow depth-of-field renders out-of-focus areas at image periphery |
| **Shutter Speed** | Horizontal motion blur — onset at 1/50 s, kernel up to 40 px at 2 s | Hand-held camera shake during long exposures |
| **All three** | Brightness shift (EV offset) | E ∝ ISO × Aperture_Area × Time — any surplus/deficit shifts tonal range |

### TSCG Connections

- **I (Information) / ASFID**: The photograph *is* the encoded territory information — each pixel encodes scene luminance, colour, texture. The simulation makes the **Signature** metaconcept (I⊗F) visible: the image changes signature depending on capture parameters.
- **V (Verifiability) / REVOI**: Changing any slider immediately verifies the Triangle's prediction. The EV bar and trade-off panel make the Pareto frontier tangible.
- **A (Attractor)**: The baseline settings form the stable attractor state — the image "wants" to look correctly exposed; any deviation is penalised by a visible artefact.

### Requirements & Usage

```bash
pip install pygame numpy
python exposure_triangle_sim.py
# Optional: explicit poclet path
python exposure_triangle_sim.py path/to/M0_ExposureTriangle.jsonld
```

Place `photo_sample.jpg` in the **same folder** as `exposure_triangle_sim.py`.

---

## 13. Changelog

| Version | Date | Description |
|---------|------|-------------|
| **1.2.0** | 2026-02-24 | Added `m0:sampleImage` property (`photo_sample.jpg`). Documents baseline exposure (ISO 400 / f/5.6 / 1/250s) and simulation effects (ISO→noise, Aperture→vignette, Shutter→motion blur). Added `exposure_triangle_sim.py` Pygame simulation with live photo effects driven by poclet ASFID/REVOI data. |
| **1.1.0** | 2026-02-21 | Synchronized with M2 v15.4.0 and M3 v3.5.0. Author corrected. ORIVE → REVOI throughout. Tensor formula spacing normalized. Balance and Trade-off no longer labeled '(NEW)'. Added 4 metaconcepts: `Amplification`, `FeedbackLoop`, `Polarity`, `Behavior`. Added `spaceCoverage` ValueSpace (RSC ≈ 0.65) on Representation. Added `m3:semanticSignature`. Total: 18 → 22 metaconcepts. |
| **1.0.0** | 2026-01-20 | Initial creation. 18 metaconcepts (34%). First identification of `m2:Balance` and `m2:Trade-off` as new M2 metaconcepts from photography domain analysis. |

---

## References

- Adams, A. (1981). *The Negative* (The Ansel Adams Photography Series)
- Freeman, M. (2007). *The Photographer's Eye: Composition and Design*
- Peterson, B. (2016). *Understanding Exposure* (4th ed.)
- Langford, M. (2010). *Langford's Basic Photography* (9th ed.)
- ISO 12232:2019 — Photography — Digital still cameras — Determination of exposure index

---

*See also: `M0_FireTriangle` (structural analogy — both are 3-component canonical pedagogical models)*
