# M0_CMYK_Subtractive — CMYK Subtractive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**  
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25  
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

`M0_CMYK_Subtractive` is a TSCG M0-layer poclet modeling the **practical subtractive
color synthesis** used in the commercial printing industry.

It extends the theoretical CMY model with a fourth **Key (Black)** channel, solving
the fundamental failure of pure CMY (`CMY(100,100,100) ≠ black`). CMYK is the global
industry standard for all printed materials.

> **TSCG insight:** CMYK exemplifies the `m2:Optimization` GenericConcept — the K channel
> optimizes the CMY model for real-world constraints (true black, ink cost reduction,
> process stability). It also demonstrates Map evolution through falsification.

### Key Characteristics

| Attribute | Value |
|---|---|
| Domain | Printing / Commercial Graphics |
| Principle | Subtractive Synthesis (ink layering) + Practical Optimization (K channel) |
| Physical basis | Spectral absorption by inks + opaque black overlay |
| Components | 4 (C, M, Y, K channels) |
| Poclet type | Composite (Specialized, Extended) |
| Extends | CMY (adds Key channel) |
| M2 GenericConcepts | 15 |

---

## TSCG Dual-Space Analysis

### Territory Space — Eagle Eye (ASFID)

```
|Ω_print⟩ = 0.70|A⟩ + 0.80|S⟩ + 0.65|F⟩ + 0.85|I⟩ + 0.25|D⟩
```

### Map Space — Sphinx Eye (REVOI)

```
|M_CMYK⟩_REVOI = 0.90|R⟩ + 0.85|E⟩ + 0.90|V⟩ + 0.85|O⟩ + 0.95|I⟩
```

| Dimension | Score | Justification |
|---|---|---|
| R (Representability) | 0.90 | (C%, M%, Y%, K%) — printer-intuitive notation |
| E (Evolvability) | 0.85 | CMY→CMYK; spawned hexachrome; GCR/UCR algorithms refined |
| V (Verifiability) | 0.90 | Measured with densitometers; ISO 12647 compliance |
| O (Observability) | 0.85 | Ubiquitous in printed materials; halftone dots visible under loupe |
| I (Interoperability) | 0.95 | ISO 12647, SWOP, Fogra — global standards |

**REVOI mean ≈ 0.89** — Excellent Map quality (best subtractive model).  
**Epistemic Gap:** `ΔΘ ≈ 0.27` — Small gap; CMYK is an excellent practical model.

---

## Channels (Components)

| Channel | GenericConcept | Mechanism | Range |
|---|---|---|---|
| Cyan (C) | `m2:Channel` | Absorbs red light | [0%, 100%] |
| Magenta (M) | `m2:Channel` | Absorbs green light | [0%, 100%] |
| Yellow (Y) | `m2:Channel` | Absorbs blue light | [0%, 100%] |
| Key (K) | `m2:Channel` | Opaque black overlay (non-spectral) | [0%, 100%] |

**TAC (Total Area Coverage):** C + M + Y + K ≤ 300–400% (paper saturation limit)

---

## GenericConcepts Mobilized (15)

| Category | GenericConcepts |
|---|---|
| Structural | Space |
| Informational | Channel · Signal · Representation · Code |
| Regulatory | Constraint · Optimization |
| Dynamic | Transformation · Fusion |
| Relational | Synergy |

**Core pattern:** `Channel × Optimization(K) × Fusion → practical printed Color`

---

## Black Generation Strategies

| Strategy | Principle | Best Use |
|---|---|---|
| **GCR** (Gray Component Replacement) | `K = min(C,M,Y)` | General commercial printing |
| **UCR** (Under Color Removal) | Replace CMY only in dark areas | High-quality reproduction |
| Maximum K | Maximize K, minimize CMY | Newspapers, low-cost |
| Minimum K | Minimize K, maximize CMY | Fine art reproduction |

---

## Halftoning

CMYK uses halftone screening to simulate continuous tone with discrete ink dots:

| Technique | Method | Use |
|---|---|---|
| AM Screening | Fixed spacing, variable dot size | Traditional offset |
| FM Screening | Fixed dot size, variable spacing | High-quality digital |

**Rosette angles** (avoid moiré): C: 105° / M: 75° / Y: 90° / K: 45°

---

## Key Color Mixtures

| Result | CMYK | Notes |
|---|---|---|
| Pure Black | (0%, 0%, 0%, 100%) | K only — true deep black |
| Rich Black | (60%, 40%, 40%, 100%) | Very dense for large areas |
| White | (0%, 0%, 0%, 0%) | Paper white — no ink |
| Red | (0%, 100%, 100%, 0%) | M+Y only |
| Green | (100%, 0%, 100%, 0%) | C+Y only |

---

## Industry Standards

| Standard | Scope |
|---|---|
| ISO 12647 | International graphic technology process control |
| SWOP | USA web offset publications |
| GRACoL | USA commercial offset lithography |
| Fogra 39/51 | European standards |
| ICC profiles | Device calibration |

---

## TSCG Validation

- ✅ All 5 ASFID dimensions present  
- ✅ 15 GenericConcepts  
- ✅ Minimality (4 channels — practical minimum for quality printing)  
- ✅ Emergence (color from 4-channel fusion)  
- ✅ Optimization GenericConcept: K channel solves CMY failure  
- ✅ Map evolution: CMY (theory) → CMYK (practice)

---

## Related Files

| File | Relationship |
|---|---|
| [M0_ColorSynthesis_Federated.jsonld](./M0_ColorSynthesis_Federated.jsonld) | Parent federation |
| [M0_CMY_Subtractive.jsonld](./M0_CMY_Subtractive.jsonld) | CMY is theoretical predecessor |
| [M0_RGB_Additive.jsonld](./M0_RGB_Additive.jsonld) | CMYK is print equivalent of RGB |

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected `dcterms:creator`; renamed `oriveAnalysis` → `revoiAnalysis`; added `m2:changelog` |
| 1.0.1 | 2026-01-20 | Added halftoning section (AM/FM, rosette); added `blackGenerationStrategies` |
| 1.0.0 | 2026-01-17 | Initial creation |

---

## References

- ISO 12647:2013 — Graphic technology standard
- Adobe (2001). *PostScript Language Reference Manual*
- Sharma, G. (2003). *Digital Color Imaging Handbook*
- Kipphan, H. (2001). *Handbook of Print Media*
