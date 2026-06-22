# M1_Electronics — TSCG Electronics Extension

**TSCG M1 Domain Extension · Electronics / Signal Processing / Modular Synthesis · v1.0.0**  
*Author: Echopraxium with the collaboration of Claude AI*

---

## Overview

`M1_Electronics.jsonld` is the **domain-specific M1 extension** for the Electronics domain within the TSCG framework. It provides **18 KnowledgeFieldConcepts** organised in 5 categories, bridging M2 GenericConcepts (universal patterns) and M0 poclets (concrete electronic systems).

It serves as the required M1 foundation for all Electronics poclets, starting with `M0_Transistor.jsonld` and `M0_VCO.jsonld`.

---

## Position in the TSCG Stack

```
M3  GenesisSpace        — ASFID ⊕ REVOI (10D bicephalous basis)
M2  GenericConcepts     — 78 universal patterns (Oscillator, Process, Component…)
M1  M1_Electronics      — THIS FILE — 18 electronics-specific concepts
M0  M0_VCO, M0_Transistor… — Concrete electronic system instances
```

M1_Electronics **imports** M1_CoreConcepts and M2_GenericConcepts, and is itself **imported** by all Electronics M0 poclets.

---

## Namespace

```
Prefix:  m1:elec
Base:    https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
         M1_extensions/electronics/M1_Electronics.jsonld#
```

---

## Concepts (18)

### Category 1 — Active Components (4)

| Concept | M2 basis | Description |
|---|---|---|
| `ActiveComponent` | `m2:Component` + `m2:Amplification` | Any electronic component requiring power supply and capable of signal control |
| `Amplifier` | `m2:Amplification` + `m2:Component` | Voltage/current/power gain stage. Gain G = V_out/V_in |
| `SignalProcessor` | `m2:Processor` | Transforms signal via transfer function H(f) |
| `Filter` | `m2:Regulation` + `m2:Transformation` | Frequency-selective signal processor (LPF, HPF, BPF, Notch, APF) |

### Category 2 — Oscillation (4)

| Concept | M2 basis | Description |
|---|---|---|
| `ElectronicOscillator` | `m2:Oscillator` | Self-sustaining periodic signal generator. Subclasses: VCO, LFO, FeedbackOscillator |
| `VoltageControlledOscillator` | `m2:Oscillator` + `m2:Amplification` | Oscillator with CV-controlled frequency (V/Oct). Instantiated as M0_VCO |
| `LFO` | `m2:Oscillator` + `m2:Signal` | Sub-audio oscillator (0.01–20 Hz) for modulation |
| `FeedbackOscillator` | `m2:Oscillator` + `m2:FeedbackLoop` | Self-oscillating via Barkhausen criterion: \|βA\|=1 |

### Category 3 — Signal Types (4)

| Concept | M2 basis | Description |
|---|---|---|
| `AudioSignal` | `m2:Signal` + `m2:Flow` | AC signal in 20 Hz–20 kHz range (±5V Eurorack) |
| `ControlVoltage` | `m2:Signal` + `m2:Interoperability` | DC/slow signal controlling module parameters |
| `PitchCV` | `m2:Signal` + `m2:Transformation` | V/Oct pitch control: f = f₀ × 2^CV |
| `ModulationSource` | `m2:Signal` + `m2:Process` | LFO, envelope, sequencer — animates module parameters |

### Category 4 — Modulation & Processing (3)

| Concept | M2 basis | Description |
|---|---|---|
| `WaveformMode` | `m2:Mode` + `m2:ValueSpace` | N-ary selector: Sine/Square/Triangle/Sawtooth/Pulse |
| `ExponentialConverter` | `m2:Amplification` + `m2:Transformation` | V/Oct core sub-circuit: I = Is × exp(V/Vt) |
| `FrequencyModulation` | `m2:Process` + `m2:Oscillator` | FM synthesis/vibrato: f_inst(t) = fc + kf × m(t) |

### Category 5 — Modular Synthesis Architecture (3)

| Concept | M2 basis | Description |
|---|---|---|
| `EurorackModule` | `m2:Component` + `m2:Interoperability` | Standard Eurorack 3U/1U module (3.5mm jacks, ±12V, V/Oct) |
| `SignalChain` | `m2:Cascade` | Ordered module sequence: VCO → VCF → VCA → Out |

---

## Key M2 Couplings

| M1 Concept | M2 Parent(s) | Note |
|---|---|---|
| `VoltageControlledOscillator` | `m2:Oscillator` | First M1 specialisation of the new Oscillator combo |
| `ElectronicOscillator` | `m2:Oscillator` | Full ASFID 5D: S⊗A⊗I⊗D⊗F |
| `FeedbackOscillator` | `m2:Oscillator` + `m2:FeedbackLoop` | Barkhausen criterion = FeedbackLoop constraint |
| `SignalChain` | `m2:Cascade` | V/Oct signal path as directed cascade |
| `Filter` | `m2:Regulation` | Frequency-domain regulatory pattern |
| `WaveformMode` | `m2:Mode` (N=5) | Discrete N-ary operational mode |
| `PitchCV` | `m2:Amplification` | Exponential gain (V/Oct) |

---

## Validated Poclets

| Poclet | Primary M1 Concept(s) used |
|---|---|
| `M0_Transistor.jsonld` | `ActiveComponent`, `Amplifier`, `SignalProcessor` |
| `M0_VCO.jsonld` | `VoltageControlledOscillator`, `WaveformMode`, `AudioSignal`, `PitchCV`, `EurorackModule` |

---

## Import in M0 Poclets

```json
"owl:imports": [
  "M3_GenesisSpace.jsonld",
  "M2_GenericConcepts.jsonld",
  "M1_CoreConcepts.jsonld",
  "M1_extensions/electronics/M1_Electronics.jsonld"
]
```

Namespace declaration in `@context`:
```json
"m1:elec": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld#"
```

---

## V/Oct Law (central to this extension)

```
f(CV) = f₀ × 2^(CV / 1V)

Implemented by: PitchCV → ExponentialConverter → VoltageControlledOscillator
M2 chain:       m2:Signal → m2:Transformation (m2:Amplification) → m2:Oscillator
```

---

## Eurorack Standard Summary

| Parameter | Value |
|---|---|
| Rack height | 3U = 133.35 mm |
| Width unit | 1HP = 5.08 mm |
| Power | +12V / −12V / +5V (optional) |
| Audio signal | ±5V peak, AC |
| CV (unipolar) | 0 – 10V |
| CV (bipolar) | ±5V |
| Pitch standard | 1V/Oct |
| Connectors | 3.5mm mono TS |

---

## File Location

```
ontology/
  M1_extensions/
    electronics/
      M1_Electronics.jsonld    ← this file
      M1_Electronics_README.md ← this document
```

---

## Planned Extensions

| Concept | M2 basis | Status |
|---|---|---|
| `VoltageControlledFilter` (VCF) | `m2:Oscillator` (self-osc) + `m2:Regulation` | Planned for M0_VCF |
| `VoltageControlledAmplifier` (VCA) | `m2:Amplification` + `m2:Regulation` | Planned for M0_VCA |
| `EnvelopeGenerator` (ADSR) | `m2:Process` + `m2:Trajectory` | Planned |
| `WaveTable` | `m2:ValueSpace` + `m2:Memory` | Planned |
| `PhaseModulation` | `m2:Process` + `m2:Oscillator` | Planned |

---

*TSCG v15.8.0 · 2026-02-27*
