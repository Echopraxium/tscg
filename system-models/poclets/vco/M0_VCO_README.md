# M0_VCO — Voltage Controlled Oscillator

**TSCG Poclet · Electronics / Modular Synthesis · v1.0.0**  
*Author: Echopraxium with the collaboration of Claude AI*

---

## Overview

A **VCO (Voltage Controlled Oscillator)** is the fundamental pitch-generation component of a modular synthesizer. It produces a periodic audio-frequency waveform whose frequency is controlled by an input voltage following the **V/Oct standard** (1 volt per octave).

This poclet is the **first M0 instantiation of `m2:Oscillator`** (introduced in M2 v15.8.0), validating the GenericConceptCombo in the Electronics / Music Technology domain.

---

## TSCG Positioning

| Layer | Concept | Role |
|---|---|---|
| **M3** | ASFID (Eagle Eye) | Territory: S, A, F, I, D |
| **M2** | `m2:Oscillator` | Primary — `⊗⇒(Component, Process, Trajectory\|Circular)` |
| **M2** | `m2:Amplification` | V/Oct exponential CV→frequency mapping |
| **M2** | `m2:Transformation` | CV domain → audio frequency domain |
| **M2** | `m2:Mode` | Waveform selector (N=4: Sine, Square, Triangle, Sawtooth) |
| **M2** | `m2:Signal` | Audio output waveform |
| **M0** | `m0:VCO` | This poclet |

### Why `m2:Oscillator` and not just `m2:Process`?

The VCO is a **system component** — a bounded, identifiable, patchable module, not just an abstract process. Subclassing `m2:Component` adds **S** (Structure) and unlocks full ASFID 5D coverage: `S ⊗ A ⊗ I ⊗ D ⊗ F`.

---

## ASFID Analysis

| Dim | Score | Interpretation |
|---|---|---|
| **A** | 0.90 | Target frequency `f = f₀ × 2^(CV)` — circular attractor |
| **S** | 0.75 | Integrator core, V/Oct converter, waveform shaper, buffers |
| **F** | 0.85 | Audio output ±5V, CV input, FM input |
| **I** | 0.80 | Phase φ(t), waveform shape, pitch CV |
| **D** | 0.90 | V/Oct law: `f(CV) = f₀ × 2^(CV/1V)` |
| **Total** | **0.84** | Epistemic gap: **0.16** |

---

## REVOI Analysis

| Dim | Score | Interpretation |
|---|---|---|
| **R** | 0.90 | Closed-form formula, analytic Fourier waveforms |
| **E** | 0.85 | FM, hard sync, PWM, wavetable extend cleanly |
| **V** | 0.95 | Frequency counter, oscilloscope, FFT |
| **O** | 0.95 | All state variables directly measurable |
| **I** | 0.95 | V/Oct universal Eurorack standard |
| **Total** | **0.92** | Map-strong: highest REVOI in Combo family |

---

## The V/Oct Law

```
f(CV) = f₀ × 2^(CV / 1V)

CV =  0V  →  440 Hz  (A4)
CV = +1V  →  880 Hz  (A5,  +1 octave)
CV = +2V  → 1760 Hz  (A6,  +2 octaves)
CV = -1V  →  220 Hz  (A3,  -1 octave)
CV = 1/12 V ≈ 83 mV  →  A#4  (+1 semitone)
```

---

## Waveform Modes (`m2:Mode`, N=4)

| Mode | Harmonics | Timbre |
|---|---|---|
| **Sine** | Fundamental only | Pure, flute-like |
| **Square** | Odd (1/n) | Hollow, woodwind |
| **Triangle** | Odd (1/n²) | Soft, mellow |
| **Sawtooth** | All (1/n) | Bright, string/brass |

---

## Interfaces

### Inputs
| Jack | Signal | ASFID | Description |
|---|---|---|---|
| `PITCH` | CV V/Oct | A + D | Primary frequency control |
| `FM` | ±5V | D + F | Frequency modulation |
| `SYNC` | Gate | I + D | Hard sync — resets phase |

### Outputs
| Jack | Level | Description |
|---|---|---|
| `SIN` | ±5V | Sine |
| `SQR` | ±5V | Square |
| `TRI` | ±5V | Triangle |
| `SAW` | ±5V | Sawtooth |

---

## Transdisciplinary Analogies

| Domain | Analogue | CV equivalent |
|---|---|---|
| Biology | Cardiac pacemaker (SA node) | Autonomic nervous system tone |
| Mechanics | Driven variable-length pendulum | Effective gravity control |
| Economics | Business cycle oscillator | Interest rate policy |
| Chemistry | Belousov-Zhabotinsky reaction | Reagent input rate |

---

## Files

| File | Description |
|---|---|
| `M0_VCO.jsonld` | Ontology (this poclet) |
| `M0_VCO_README.md` | This document |
| `vco_sim.py` | Interactive Pygame simulation |
| `VCO_SIM_README.md` | Simulation user guide |

---

*TSCG v15.8.0 · 2026-02-27*
