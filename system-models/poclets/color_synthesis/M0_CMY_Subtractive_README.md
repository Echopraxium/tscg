# M0_CMY_Subtractive — CMY Subtractive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**  
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25  
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

`M0_CMY_Subtractive` is a TSCG M0-layer poclet modeling **subtractive color synthesis**
using Cyan, Magenta, and Yellow pigment primaries.

This is the **theoretical model** of pigment/ink mixing: each primary **absorbs** (subtracts)
a portion of white incident light, and the remaining transmitted spectrum produces the
perceived color. It is the complement of RGB additive synthesis.

> **TSCG insight:** CMY demonstrates Map falsification in action — the theoretical
> prediction `CMY(100,100,100) = black` fails with real pigments (produces muddy brown),
> which forced evolution to the CMYK model (Popper's falsification principle).

### Key Characteristics

| Attribute | Value |
|---|---|
| Domain | Optics / Color Science / Printing |
| Principle | Subtractive Synthesis (pigment mixing / spectral filtering) |
| Physical basis | Wavelength-selective absorption by pigments |
| Components | 3 (C, M, Y channels) |
| Poclet type | Composite (Specialized) |
| Complementary to | RGB Additive |
| M2 Metaconcepts | 13 |

---

## TSCG Dual-Space Analysis

### Territory Space — Eagle Eye (ASFID)

```
|Ω_pigment⟩ = 0.65|A⟩ + 0.75|S⟩ + 0.70|F⟩ + 0.80|I⟩ + 0.30|D⟩
```

| Dimension | Score | Justification |
|---|---|---|
| A (Attractor) | 0.65 | Moderate (color stability under illumination) |
| S (Structure) | 0.75 | Pigment particle organization, surface texture |
| F (Flow) | 0.70 | Incident white light, reflected spectrum |
| I (Information) | 0.80 | Spectral absorption profile |
| D (Dynamics) | 0.30 | Low (pigments stable) |

### Map Space — Sphinx Eye (REVOI)

```
|M_CMY⟩_REVOI = 0.85|R⟩ + 0.60|E⟩ + 0.75|V⟩ + 0.70|O⟩ + 0.80|I⟩
```

| Dimension | Score | Justification |
|---|---|---|
| R (Representability) | 0.85 | Well representable as (C%, M%, Y%) |
| E (Evolvability) | 0.60 | Low — largely superseded by CMYK |
| V (Verifiability) | 0.75 | Partial (black failure test is instructive) |
| O (Observability) | 0.70 | Requires pigments/inks to observe |
| I (Interoperability) | 0.80 | Standard in color theory education |

**REVOI mean ≈ 0.74** — Good theoretical Map, poor practical Map.  
**Epistemic Gap:** `ΔΘ ≈ 0.28` — Small gap for ideal pigments; larger for real materials.

---

## Channels (Components)

| Channel | Metaconcept | Absorbs | Transmits | Complement |
|---|---|---|---|---|
| Cyan (C) | `m2:Channel` | Red (~620–750 nm) | G + B → Cyan | Red (RGB) |
| Magenta (M) | `m2:Channel` | Green (~495–570 nm) | R + B → Magenta | Green (RGB) |
| Yellow (Y) | `m2:Channel` | Blue (~450–495 nm) | R + G → Yellow | Blue (RGB) |

Range: `[0%, 100%]` absorption percentage

**CMY ↔ RGB approximate conversion:** `C = 1−R, M = 1−G, Y = 1−B` (ideal pigments only)

---

## Metaconcepts Mobilized (13)

| Category | Metaconcepts |
|---|---|
| Structural | Space |
| Informational | Channel · Signal · Representation |
| Regulatory | Constraint · Filter |
| Dynamic | Transformation · Fusion |
| Energetic | Dissipation |
| Relational | Synergy |

**Core pattern:** `Channel(Filter) × Fusion(spectral absorption) → emergent Synergy`

---

## Key Color Mixtures (Subtractive)

| Result | CMY | Mechanism |
|---|---|---|
| White | (0%, 0%, 0%) | No absorption — paper shows through |
| Black (theoretical) | (100%, 100%, 100%) | All wavelengths absorbed — *fails in practice* |
| Red | (0%, 100%, 100%) | M+Y absorb green+blue → red transmitted |
| Green | (100%, 0%, 100%) | C+Y absorb red+blue → green transmitted |
| Blue | (100%, 100%, 0%) | C+M absorb red+green → blue transmitted |

---

## Why CMY Evolved into CMYK

| Problem | Cause | Solution |
|---|---|---|
| `CMY(100,100,100) ≠ black` | Real pigments not spectrally pure | Add K (Key/Black) channel |
| Brown instead of black | Incomplete absorption, scattering | K provides true deep black |
| High ink cost | Three inks needed for dark areas | K cheaper than C+M+Y |

---

## TSCG Validation

- ✅ All 5 ASFID dimensions present  
- ✅ 13 metaconcepts  
- ✅ Minimality (3 channels — theoretical primaries)  
- ✅ Emergence (color from spectral fusion/absorption)  
- ✅ Channel metaconcept correctly used  
- ✅ Falsification principle illustrated (CMY → CMYK evolution)

---

## Related Files

| File | Relationship |
|---|---|
| [M0_ColorSynthesis_Federated.jsonld](./M0_ColorSynthesis_Federated.jsonld) | Parent federation |
| [M0_CMYK_Subtractive.jsonld](./M0_CMYK_Subtractive.jsonld) | CMY extended with K channel |
| [M0_RGB_Additive.jsonld](./M0_RGB_Additive.jsonld) | CMY is complement of RGB |

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected `dcterms:creator`; renamed `oriveAnalysis` → `revoiAnalysis`; added `m2:changelog` |
| 1.0.1 | 2026-01-20 | Added Popper falsification analysis in `revoiAnalysis`; clarified gamut limitations |
| 1.0.0 | 2026-01-17 | Initial creation |

---

## References

- Kuehni, R. G. (2005). *Color: An Introduction to Practice and Principles*
- Pointer, M. R. (1980). *The Gamut of Real Surface Colours*
- Hunt, R. W. G. (2004). *The Reproduction of Colour* (6th ed.)
