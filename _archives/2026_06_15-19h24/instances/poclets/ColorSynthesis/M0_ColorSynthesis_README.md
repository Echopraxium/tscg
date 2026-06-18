# M0_ColorSynthesis_Federated — Color Synthesis Federated Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**  
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25  
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

`M0_ColorSynthesis_Federated` is a TSCG **Federated Poclet** that aggregates four specialized
color synthesis poclets into a unified comparative ontology. It demonstrates one of TSCG's
core epistemological principles:

> **Same Territory (perceived color), multiple Maps (RGB, HSL, CMY, CMYK)**  
> *"The map is not the territory"* — Korzybski

### Federated Instances

| Poclet | File | Principle | Medium | Components |
|---|---|---|---|---|
| **RGB Additive** | [M0_RGB_Additive.jsonld](./M0_RGB_Additive.jsonld) | Additive (light-based) | Screens / Displays | 3 |
| **HSL Additive** | [M0_HSL_Additive.jsonld](./M0_HSL_Additive.jsonld) | Additive (perceptual) | Screens / UI design | 3 |
| **CMY Subtractive** | [M0_CMY_Subtractive.jsonld](./M0_CMY_Subtractive.jsonld) | Subtractive (pigment) | Inks (theoretical) | 3 |
| **CMYK Subtractive** | [M0_CMYK_Subtractive.jsonld](./M0_CMYK_Subtractive.jsonld) | Subtractive (practical) | Commercial printing | 4 |

---

## TSCG Map-Territory Analysis

### Territory

- **Phenomenon:** Human color perception (qualia)
- **Physical basis:** Electromagnetic radiation 380–740 nm interpreted by trichromatic cones
- **Nature:** Continuous spectrum → discrete trichromatic perception
- **ASFID:** High I (spectral information), Medium S (wavelength structure)

### Multiple Maps

The same Territory is described by four distinct Maps, each optimized for a different purpose:

| Map | Physical Principle | Observer | Epistemic Gap |
|---|---|---|---|
| RGB | Light emission | Display engineer | ~0.30 |
| HSL | Perceptual transform | Designer / Artist | ~0.37 |
| CMY | Pigment absorption | Painter / Theorist | ~0.28 (ideal) |
| CMYK | Ink printing | Prepress technician | ~0.27 |

*"No single 'correct' Map — each optimized for a specific observer and use case."*

---

## Comparison Matrix

### Physical Principle

| Model | Type | Mechanism |
|---|---|---|
| RGB | **Additive** | Light superposition (sum → white) |
| HSL | **Additive** | Perceptual transform of RGB |
| CMY | **Subtractive** | Spectral absorption (product → black) |
| CMYK | **Subtractive** | Spectral absorption + opaque black |

### Application Domain

| Screen / Displays | Printing |
|---|---|
| RGB, HSL | CMY, CMYK |

---

## Shared GenericConcepts (common to all 4 variants)

| GenericConcept | Formula | Role |
|---|---|---|
| `m2:Component` / `m2:Channel` | `S⊗I` / `S⊗I⊗F` | Color channels as functional units |
| `m2:Fusion` | `S⊗F⊗D` | Channels merge into perceived color |
| `m2:Signal` | `I⊗F` | Intensity/absorption carried by channels |
| `m2:Synergy` | `A⊗S⊗I` | Emergent color from channel combination |
| `m2:Space` | `S⊗I` | Color space geometry |
| `m2:Representation` | `I⊗S` | Model as encoding of color |
| `m2:Code` | `I⊗S⊗D` | Numerical encoding (e.g., `#FF0000`) |
| `m2:Transformation` | `D⊗I⊗S` | Conversions between color spaces |

---

## Transformation Network

| From | To | Type | Reversible |
|---|---|---|---|
| RGB | HSL | Bijective (lossless) | ✅ Yes |
| RGB | CMY | Approximate | ≈ (gamut differences) |
| CMY | CMYK | Augmentation (add K) | ✅ Yes |
| RGB | CMYK | Complex (multi-step) | ≈ |

---

## Transdisciplinary Value

The Color Synthesis federation provides exceptional pedagogical value for TSCG because:

1. **Map-Territory plurality** — Same phenomenon, multiple valid models
2. **Observer-relativity** — Each model optimized for a different observer
3. **Physical principle duality** — Additive (light) vs Subtractive (matter)
4. **Model evolution** — CMY → CMYK demonstrates falsification and refinement
5. **Visual intuition** — Colors are universally understood across cultures

### Connections to Other Poclets

| Poclet | Similarity | Difference |
|---|---|---|
| Fire Triangle | 3-component synergistic systems | Fire = emergent process; Color = emergent perception |
| RAAS System | Homeostatic regulation with multiple channels | RAAS = biological; Color = physical/perceptual |

---

## Future Extensions

| Model | Type | Components |
|---|---|---|
| CIELAB (L\*a\*b\*) | Perceptually uniform | L\*, a\*, b\* |
| HSV / HSB | Alternative perceptual | Hue, Saturation, Value |
| CIE XYZ | Device-independent | X, Y, Z |

---

## TSCG Validation

- ✅ Demonstrates Map-Territory distinction with multiple Maps  
- ✅ 4 federated instances (2 additive + 2 subtractive)  
- ✅ Shared GenericConcept identification across all variants  
- ✅ Transformation network between models documented  
- ✅ Observer-relativity principle illustrated

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected `dcterms:creator` (was 'TSCG Project - Michel Favre'); added `m2:changelog`; bumped version |
| 1.0.1 | 2026-01-20 | Added `transformationNetwork` with conversion formulas; added `futureExtensions` |
| 1.0.0 | 2026-01-17 | Initial creation |

---

## References

- Poynton, C. (2003). *Digital Video and HD: Algorithms and Interfaces*
- Fairchild, M. D. (2013). *Color Appearance Models* (3rd ed.)
- Adobe (2000). *PostScript Language Reference* (3rd ed.)
- CIE (Commission Internationale de l'Éclairage) standards
