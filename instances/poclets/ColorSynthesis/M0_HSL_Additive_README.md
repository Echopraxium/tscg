# M0_HSL_Additive — HSL Additive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**  
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25  
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

`M0_HSL_Additive` is a TSCG M0-layer poclet modeling **perceptual additive color synthesis**
using Hue, Saturation, and Lightness channels.

HSL is a **bijective transformation of RGB** — same Territory (perceived color),
different Map (cylindrical vs cubic coordinate system). It is optimized for
human perception and artistic manipulation rather than hardware rendering.

### Key Characteristics

| Attribute | Value |
|---|---|
| Domain | Optics / Color Science |
| Principle | Additive Synthesis (Perceptual Representation) |
| Physical basis | Same as RGB — electromagnetic superposition in perceptual coordinates |
| Components | 3 (H, S, L channels) |
| Poclet type | Composite (Specialized) |
| Relation to RGB | Bijective transformation (lossless, reversible) |
| M2 GenericConcepts | 14 |

---

## TSCG Dual-Space Analysis

### Territory Space — Eagle Eye (ASFID)

```
|Ω_color⟩ = 0.70|A⟩ + 0.85|S⟩ + 0.90|F⟩ + 0.95|I⟩ + 0.40|D⟩
```

*Identical to RGB Territory — same physical light, same perception.*

### Map Space — Sphinx Eye (REVOI)

```
|M_HSL⟩_REVOI = 0.90|R⟩ + 0.95|E⟩ + 0.85|V⟩ + 0.85|O⟩ + 0.90|I⟩
```

| Dimension | Score | Justification |
|---|---|---|
| R (Representability) | 0.90 | (H°, S%, L%) matches human perceptual language |
| E (Evolvability) | 0.95 | Spawned HSV, HSI, HSB variants; RGB → HSL demonstrates Map evolution |
| V (Verifiability) | 0.85 | Testable via bijective RGB conversion |
| O (Observability) | 0.85 | Directly observable in all color pickers (Photoshop, CSS) |
| I (Interoperability) | 0.90 | CSS3 `hsl()`, standard in all design tools |

**Epistemic Gap:** `ΔΘ ≈ 0.37` — Small gap; HSL is a good perceptual model.

---

## Channels (Components)

| Channel | GenericConcept | Tensor Formula | Range | Geometry |
|---|---|---|---|---|
| Hue (H) | `m2:Channel` | `S⊗I⊗F` | [0°, 360°) circular | Angular |
| Saturation (S) | `m2:Channel` | `S⊗I⊗F` | [0%, 100%] | Radial |
| Lightness (L) | `m2:Channel` | `S⊗I⊗F` | [0%, 100%] | Vertical |

**Geometry:** HSL Cylinder = S¹ × [0,1] × [0,1]

### Hue Color Wheel

| Angle | Color | Angle | Color |
|---|---|---|---|
| 0° | Red | 180° | Cyan |
| 60° | Yellow | 240° | Blue |
| 120° | Green | 300° | Magenta |

---

## GenericConcepts Mobilized (14)

| Category | GenericConcepts |
|---|---|
| Structural | Space · Topology · Symmetry · Invariant |
| Informational | Channel · Signal · Code · Representation |
| Regulatory | Constraint |
| Dynamic | Transformation · Fusion |
| Relational | Synergy |

**Core pattern:** `Channel × Transformation(HSL↔RGB) × Fusion → emergent Color`

---

## RGB ↔ HSL Transformation (Bijective)

```
HSL → RGB:
  C = (1 - |2L - 1|) × S   // Chroma
  X = C × (1 - |(H/60°) mod 2 - 1|)
  (R, G, B) = sector-dependent formula + L offset

RGB → HSL:
  L = (max + min) / 2
  S = (max - min) / (1 - |2L - 1|)
  H = from dominant channel
```

---

## Key Advantages and Limitations

| Aspect | Detail |
|---|---|
| ✅ Perceptually intuitive | Hue = color type, adjustable independently |
| ✅ Matches artistic color theory | Analogous, complementary, triadic harmonies |
| ⚠️ Not perceptually uniform | Equal HSL distance ≠ equal perceived difference |
| ⚠️ Singularity at gray | H undefined when S = 0 |

---

## TSCG Validation

- ✅ All 5 ASFID dimensions present  
- ✅ 14 GenericConcepts  
- ✅ 3 channels (perceptual triplet)  
- ✅ Emergence (color from perceptual channel fusion)  
- ✅ Channel GenericConcept correctly used  
- ✅ Bijective lossless HSL ↔ RGB

---

## Related Files

| File | Relationship |
|---|---|
| [M0_ColorSynthesis_Federated.jsonld](./M0_ColorSynthesis_Federated.jsonld) | Parent federation |
| [M0_RGB_Additive.jsonld](./M0_RGB_Additive.jsonld) | HSL is bijective transformation of RGB |

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected `dcterms:creator`; renamed `oriveAnalysis` → `revoiAnalysis`; added `m2:changelog` |
| 1.0.1 | 2026-01-20 | Added bijective transformation algorithm details; clarified Lightness axis semantics |
| 1.0.0 | 2026-01-17 | Initial creation |

---

## References

- Smith, A. R. (1978). *Color Gamut Transform Pairs.* SIGGRAPH  
- Joblove, G. H., & Greenberg, D. (1978). *Color spaces for computer graphics.* SIGGRAPH  
- W3C CSS Color Module Level 3
