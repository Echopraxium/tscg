# M0_TVTestPattern_README.md

**File:** `M0_TVTestPattern.jsonld`  
**Version:** 1.0.0 · **Date:** 2026-03-02  
**Author:** Echopraxium with the collaboration of Claude AI  
**Status:** ACTIVE — Primary validator for `m2:Calibration`

---

## Overview

`M0_TVTestPattern.jsonld` models the **analogue television test pattern** (*mire* in French) as a complete TSCG poclet. A test pattern is a standardised reference image injected into the full analogue TV signal chain — from signal generator to display — in order to **calibrate, diagnose, and validate** every link in that chain.

This poclet is the **primary empirical validator** for `m2:Calibration` (A ⊗ F ⊗ It ⊗ D, Regulatory family, territory mode, v15.10.0).

### Architectural Position

```
M3  Genesis Space  (ASFID ⊗ REVOI — 10 fundamental dimensions)
 ↓
M2  m2:Calibration  (A ⊗ F ⊗ It ⊗ D)  ← PRIMARY GenericConcept validated here
 ↓
M1  M1_Electronics (planned) · M1_CoreConcepts (planned)
 ↓
M0  M0_TVTestPattern.jsonld  ← THIS FILE
```

---

## System Description

### What is a TV Test Pattern?

A **test pattern** (*mire*) is a precisely constructed image containing a set of reference elements specifically designed to make every measurable parameter of a video signal chain visible and quantifiable simultaneously:

| Element | What it tests |
|---|---|
| **Greyscale staircase** (5–10 steps) | Luminance linearity, black/white levels (IRE 7.5–100%) |
| **EBU/SMPTE colour bars** (8 colours) | Chrominance phase, saturation, subcarrier accuracy |
| **Resolution wedges** (spatial freq.) | Horizontal/vertical bandwidth in TVL (TV lines) |
| **Geometric grid + circle** | Linearity, aspect ratio (4:3), geometric distortion |
| **Multiburst packets** | Frequency response (0.5 → 4.43 MHz luma bandwidth) |
| **Sync pulses** | Line/field synchronisation timing, colour burst stability |

### Standards

| Standard | Region | Pattern |
|---|---|---|
| **EBU (ITU-R BT.471)** | Europe | PM5544 (Philips, 1967) — de facto European standard |
| **SMPTE colour bars** | USA / North America | SMPTE 75% / 100% colour bars |
| **Indian Head chart** | USA | Classic monochrome resolution chart (1939–1970) |

---

## Bicephalous Architecture — Key Architectural Insight

This poclet exhibits a unique **self-referential Territory/Map duality** that makes it architecturally exceptional in the TSCG framework:

```
Eagle Eye  (Territory) :  the test pattern IS a physical analogue signal
                           → measurable, degradable, subject to noise and distortion

Sphinx Eye (Map)        :  the test pattern IS the external Attractor
                           → the normative reference standard the chain must reproduce
```

**Consequence:** The residual gap between the emitted and received pattern is simultaneously:
- A **Territory measurement** (waveform deviation in IRE, degrees, TVL)
- A **Map quality metric** (the epistemic gap δ made directly visible on instruments)

This is the only known TSCG poclet where the same physical artefact occupies both the **A** (Attractor / reference) and **F** (Flow / stimulus) roles simultaneously.

---

## TSCG Analysis

### Eagle Eye — ASFID Scoring (Territory)

| Dim | Score | Rationale |
|---|---|---|
| **A** Attractor | **0.95** | Externally imposed, sovereign reference: IRE levels, EBU colour vectors, spatial frequencies — all normalised and certified. Exceptionally high: the reference is physically instantiated and unambiguous. |
| **S** Structure | **0.85** | Sequential chain topology clearly defined: Generator → Encoder → Transmission → Decoder → Display. Each link independently isolable for diagnosis. |
| **F** Flow | **0.90** | Composite analogue video signal (Y+C+sync): continuous, structured in lines/fields, physically measurable at every node with a waveform monitor. |
| **I** Information | **0.90** | Rich Territory information: IRE levels, chrominance vectors, frequency response, geometry — all captured quantitatively by calibrated instruments. |
| **D** Dynamics | **0.80** | Iterative correction loop (measure → adjust → re-measure → iterate). Slightly lower due to human-in-the-loop latency and non-automated convergence. |
| **Mean** | **0.88** | All 5 ASFID dimensions robustly present — poclet completeness criterion satisfied. |

### Sphinx Eye — REVOI Scoring (Map)

| Dim | Score | Rationale |
|---|---|---|
| **R** Representability | **0.90** | The test pattern directly encodes every parameter it tests — the model is visually and electronically readable in the signal itself. |
| **E** Evolvability | **0.75** | Standards have evolved (EBU, SMPTE, ITU updates; extension to HD). Moderate: constrained by regulatory and interoperability requirements. |
| **V** Verifiability | **0.95** | Exceptional: all deviations quantifiable in IRE, degrees of chrominance phase, TVL. Pass/fail defined by broadcast specification. Highest REVOI dimension. |
| **O** Observability | **0.90** | Waveform monitor, vectorscope, spectrum analyser make every internal chain state directly observable and quantitative. |
| **I** Interoperability | **0.85** | EBU/SMPTE standards are globally recognised. Slight penalty: NTSC/PAL/SECAM incompatibility across regions. |
| **Mean** | **0.87** | Strong Map quality — consistent with δ = 0.13. |

### Epistemic Gap

```
δ = 1 − (ASFID_mean + REVOI_mean) / 2
  = 1 − (0.88 + 0.87) / 2
  = 0.13
```

**Quality: Very low — mature coupling.**

The exceptionally low δ reflects the near-identity of Territory and Map in this poclet: the test pattern is simultaneously the physical signal and the reference standard. A correctly calibrated chain achieves δ → 0 in practice (emitted pattern = received pattern within tolerance). Reducing δ is the explicit operational goal of the system.

---

## System Components

| Component | ASFID role | Description |
|---|---|---|
| **Reference Pattern** (mire) | **A** + F | The external Attractor and the injected stimulus simultaneously. Contains all calibration parameters. |
| **Signal Chain** | **S** | Generator → Encoder → Transmission → Decoder → Display. Sequential, isolable topology. |
| **Composite Video Signal** | **F** | Y + C + sync waveform. Continuous, measurable at every node. |
| **Measurement Instruments** | **I** | Waveform monitor, vectorscope, resolution reader, spectrum analyser. |
| **Correction Loop** | **D** | Iterative measure → adjust → re-measure cycle until convergence within tolerance. |

### Measurement Instruments Detail

| Instrument | Measures | Key parameters |
|---|---|---|
| **Waveform Monitor** | Luminance, sync | Black level (7.5 IRE), white level (100 IRE), sync tip (−40 IRE) |
| **Vectorscope** | Chrominance phase & amplitude | Colour vector directions (±2° tolerance), saturation |
| **Resolution reader** | Spatial frequency | Horizontal/vertical TVL, corner resolution (convergence) |
| **Spectrum analyser** | RF bandwidth | Video BW (MHz), carrier-to-noise ratio (dB) |

---

## GenericConcepts Mobilised (M2)

| GenericConcept | Family | Role in this poclet |
|---|---|---|
| **`m2:Calibration`** ⭐ | Regulatory | **Primary** — direct instantiation of A ⊗ F ⊗ It ⊗ D |
| `m2:Signal` | Informational | Composite video signal as territory information carrier |
| `m2:Pattern` | Informational | Geometric and chromatic structure of the test pattern |
| `m2:Threshold` | Regulatory | IRE level boundaries, colour tolerances, resolution limits |
| `m2:FeedbackLoop` | Dynamic | Measure → Adjust → Re-measure iterative cycle |
| `m2:Channel` | Structural | Each link in the signal chain as independent channel |
| `m2:Trajectory` | Dynamic | Convergence of parameters toward reference across iterations |
| `m2:Representation` | Informational | Test pattern as visual/electronic encoding of the standard |
| `m2:Alignment` | Regulatory | Geometric alignment (sync, aspect ratio, CRT convergence) |
| `m2:Decomposition` | Structural | Separation of Y, Cb, Cr, sync, burst from composite signal |
| `m2:Regulation` | Regulatory | Each adjustment control constraining a signal parameter within bounds |

---

## Validation of `m2:Calibration`

This poclet confirms the following architectural decisions made during the creation of `m2:Calibration` (v15.10.0):

**Eagle Eye formula `A ⊗ F ⊗ It ⊗ D` — CONFIRMED ✅**

| Dimension | Concrete instantiation |
|---|---|
| **A** | The test pattern reference (IRE levels, EBU colour bars, resolution spec) |
| **F** | The composite video signal injected into the chain |
| **It** | The received/displayed signal measured by waveform monitor and vectorscope |
| **D** | The engineer's iterative adjustment loop (gain, gamma, phase, geometry) |

**Sphinx Eye — `V ⊗ O` belongs to REVOI poclet scoring, NOT to `m2:Calibration` — CONFIRMED ✅**

V (Verifiability, 0.95) and O (Observability, 0.90) characterise the quality of the calibration procedure as assessed from the Map perspective. They are scores assigned to this poclet during REVOI analysis, not constitutive dimensions of the GenericConcept itself.

---

## M1 Concepts Identified

### M1_Electronics (to be created)

| Concept | M2 Basis | Description |
|---|---|---|
| `SignalChainCalibration` | `m2:Calibration` | Full end-to-end calibration of a multi-link analogue signal chain |
| `ChrominanceCalibration` | `m2:Calibration ⊗ m2:Signal` | Colour subcarrier phase, amplitude, and vector accuracy calibration |
| `LuminanceCalibration` | `m2:Calibration ⊗ m2:Threshold` | Greyscale response calibration (black level, white level, gamma) |
| `ResolutionMeasurement` | `m2:Signal ⊗ m2:Threshold` | Horizontal/vertical spatial resolution measurement in TVL |

### M1_CoreConcepts (to be created)

| Concept | M2 Basis | Description |
|---|---|---|
| `CalibrationReference` | `m2:Calibration` (A dim.) | Externally defined, normatively sovereign reference state (the Attractor) |
| `CalibrationProcedure` | `m2:Calibration ⊗ m2:FeedbackLoop` | Structured, repeatable sequence of measurement and adjustment steps |

---

## Transdisciplinary Bridges

The TV test pattern demonstrates that the `m2:Calibration` pattern A ⊗ F ⊗ It ⊗ D is identical in structure across domains:

| Domain | A (Reference) | F (Stimulus) | It (Measurement) | D (Correction) |
|---|---|---|---|---|
| **Video Engineering** | Test pattern (IRE / EBU) | Composite video signal | Waveform monitor reading | Gain, gamma, phase adjustment |
| **Metrology** | SI etalon (kelvin, metre…) | Reference signal | Instrument reading | Scale factor / offset |
| **Medical Imaging** | MRI phantom values | RF pulse sequence | Scanner output | Gain, B0 shimming |
| **Audio Engineering** | Pink noise reference | Test tone | Frequency response curve | EQ adjustment |
| **Robotics** | Certified target pose | Commanded trajectory | End-effector position | Joint offset correction |

---

## Historical Context

- **1930s**: Test patterns introduced with the first experimental TV broadcasts
- **1967**: PM5544 (Philips) becomes the de facto European standard — broadcast overnight by many European networks for decades
- **1950s–2000s**: Waveform monitors and vectorscopes are standard broadcast equipment worldwide
- **1990s–2000s**: Transition to digital (SDI, DVB) — analogue test patterns gradually replaced
- **Today**: Digital HD/4K calibration systems (CalMAN, Lightspace, SMPTE ST 2110) are direct successors — same conceptual structure A ⊗ F ⊗ It ⊗ D, different signal substrate

---

## Framework Contributions

| Layer | Contribution | Status |
|---|---|---|
| **M2** | `m2:Calibration` — territory mode A ⊗ F ⊗ It ⊗ D **empirically validated** | ✅ CONFIRMED |
| **M2** | V ⊗ O belongs to REVOI poclet scoring, not to `m2:Calibration` definition | ✅ CONFIRMED |
| **M1_Electronics** | `SignalChainCalibration`, `ChrominanceCalibration`, `LuminanceCalibration`, `ResolutionMeasurement` | To be created |
| **M1_CoreConcepts** | `CalibrationReference`, `CalibrationProcedure` | To be created |
| **Architecture** | Self-referential Territory/Map duality confirmed as a valid TSCG poclet pattern | ✅ NEW INSIGHT |

---

## Related Files

| File | Layer | Relation |
|---|---|---|
| `M2_GenericConcepts.jsonld` | M2 | Defines `m2:Calibration` (v15.10.0) validated by this poclet |
| `M1_CoreConcepts.jsonld` | M1 | Will receive `CalibrationReference`, `CalibrationProcedure` |
| `M1_extensions/electronics/M1_Electronics.jsonld` | M1 | Will receive `SignalChainCalibration`, `ChrominanceCalibration` (planned) |
| `M0_TVTestPattern.jsonld` | M0 | **This poclet** |

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
