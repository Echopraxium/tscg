# M0_RGB_Additive — RGB Additive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**  
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25  
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

`M0_RGB_Additive` is a TSCG M0-layer poclet (Portable Ontological Compact Let) modeling
**additive color synthesis** using Red, Green, and Blue light primaries.

It is the canonical model for all light-emitting displays (LCD, OLED, CRT, projectors)
and is the primary member of the [Color Synthesis Federated Poclet](./M0_ColorSynthesis_Federated.jsonld).

### Key Characteristics

| Attribute | Value |
|---|---|
| Domain | Optics / Color Science |
| Principle | Additive Synthesis (light emission + superposition) |
| Physical basis | Electromagnetic wave superposition (380–740 nm) |
| Components | 3 (R, G, B channels) |
| Poclet type | Composite (Specialized) |
| M2 GenericConcepts | 15 (29% coverage) |

---

## TSCG Dual-Space Analysis

### Territory Space — Eagle Eye (ASFID)

```
|Ω_RGB⟩ = 0.75|A_score⟩ + 0.85|S_score⟩ + 0.95|F_score⟩ + 0.95|It_score⟩ + 0.40|D_score⟩
```

| Dimension | Score | Justification |
|---|---|---|
| A_score (Attractor) | 0.75 | Strong perceptual attractor (trichromatic vision) |
| S_score (Structure) | 0.85 | Well-structured 3-channel architecture |
| F_score (Flow) | 0.95 | Dominant photon flux (light emission) |
| It_score (Information) | 0.95 | High information content (3 × 8-bit channels) |
| D_score (Dynamics) | 0.40 | Low dynamics (static model) |

### Map Space — Sphinx Eye (REVOI)

```
|M_RGB⟩_REVOI = 0.90|R_score⟩ + 0.95|E_score⟩ + 0.95|V_score⟩ + 0.90|O_score⟩ + 0.95|It_score⟩
```

| Dimension | Score | Justification |
|---|---|---|
| R_score (Representability) | 0.90 | Excellent — RGB triplet, hex notation, widely understood |
| E_score (Evolvability) | 0.95 | Spawned HSL, sRGB, HDR standards |
| V_score (Verifiability) | 0.95 | Directly measurable with spectrophotometers |
| O_score (Observability) | 0.90 | Directly visible on any screen |
| It_score (Interoperability) | 0.95 | Universal standard (CSS, OpenGL, web, cameras) |

---

## Channels (Components)

| Channel | GenericConcept | Tensor Formula | Wavelength | Biological Target |
|---|---|---|---|---|
| Red (R) | `m2:Signal` | `I⊗F` | ~620–750 nm | L-cones |
| Green (G) | `m2:Signal` | `I⊗F` | ~495–570 nm | M-cones |
| Blue (B) | `m2:Signal` | `I⊗F` | ~450–495 nm | S-cones |

Digital range: `[0, 255]` (8-bit) — Analog range: `[0.0, 1.0]`

---

## GenericConcepts Mobilized (15)

| Category | GenericConcepts |
|---|---|
| Structural | Component · Space · Topology · Symmetry · Invariant |
| Informational | Signal · Code · Representation · Language · Signature |
| Regulatory | Constraint · Threshold |
| Dynamic | Transformation · Fusion |
| Relational | Synergy |

**Core pattern:** `Signal × Fusion → emergent Synergy`

Fusion formula: `R_wave ⊕ G_wave ⊕ B_wave → Perceived Color`

---

## Key Color Mixtures

| Result | RGB | Mechanism |
|---|---|---|
| White | (255, 255, 255) | All cones equally stimulated |
| Yellow | (255, 255, 0) | L+M cones — no yellow wavelength in stimulus! |
| Cyan | (0, 255, 255) | M+S cones |
| Magenta | (255, 0, 255) | L+S cones — non-spectral color |
| Black | (0, 0, 0) | Absence of light |

---

## TSCG Validation

- ✅ All 5 ASFID dimensions present  
- ✅ 15 GenericConcepts (29% coverage)  
- ✅ Minimality (3 channels — irreducible for trichromatic vision)  
- ✅ Emergence (perceived color emerges from signal fusion)  
- ✅ Signal GenericConcept central to model  
- ✅ Fusion GenericConcept explains wave superposition

---

## Applications

- Computer monitors and displays (LCD, OLED, CRT)
- Digital cameras and scanners
- Image processing and computer graphics
- Web design (CSS colors: `rgb()`, `#RRGGBB`)
- Video production and editing
- LED lighting and signage

---

## Related Files

| File | Relationship |
|---|---|
| [M0_ColorSynthesis_Federated.jsonld](./M0_ColorSynthesis_Federated.jsonld) | Parent federation |
| [M0_HSL_Additive.jsonld](./M0_HSL_Additive.jsonld) | Perceptual alternative representation |
| [M0_CMY_Subtractive.jsonld](./M0_CMY_Subtractive.jsonld) | Complementary subtractive model |
| [M0_CMYK_Subtractive.jsonld](./M0_CMYK_Subtractive.jsonld) | Printing equivalent |

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected `dcterms:creator`; renamed `oriveAnalysis` → `revoiAnalysis`; added `m2:changelog` |
| 1.0.1 | 2026-01-20 | Minor corrections in `GenericConceptsMobilized`; added `owl:versionInfo` |
| 1.0.0 | 2026-01-17 | Initial creation |

---

## References

- Poynton, C. (2003). *Digital Video and HD: Algorithms and Interfaces*
- Fairchild, M. D. (2013). *Color Appearance Models* (3rd ed.)
- ITU-R BT.709 (HDTV color primaries)
- sRGB IEC 61966-2-1:1999
