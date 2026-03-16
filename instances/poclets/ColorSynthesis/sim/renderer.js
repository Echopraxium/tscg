/**
 * renderer.js
 * ===========
 * TSCG Poclet Simulation — Color Synthesis Federated (Electron renderer)
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Right panel — 3 tabs:
 *   Description → README markdown du modèle actif (RGB/HSL/CMY/CMYK)
 *   Concepts    → GenericConcepts par catégorie du modèle actif
 *   Scores      → ASFID live (dynamique) + REVOI comparaison 4 modèles + ΔΘ
 *
 * Title bar → bouton ⌂ Home pour basculer sur le Poclet Explorer
 */

'use strict';

// ─────────────────────────────────────────────────────────────────────────────
// README  (source Markdown par modèle)
// ─────────────────────────────────────────────────────────────────────────────

const README = {

// ── RGB ──────────────────────────────────────────────────────────────────────
RGB: `# M0_RGB_Additive — RGB Additive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

\`M0_RGB_Additive\` is a TSCG M0-layer poclet modeling **additive color synthesis** using Red, Green, and Blue light primaries.

It is the canonical model for all light-emitting displays (LCD, OLED, CRT, projectors) and the primary member of the Color Synthesis Federated Poclet.

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

\`\`\`
|Ω_RGB⟩ = 0.75|A⟩ + 0.85|S⟩ + 0.95|F⟩ + 0.95|I⟩ + 0.40|D⟩
\`\`\`

| Dimension | Score | Justification |
|---|---|---|
| A (Attractor) | 0.75 | Strong perceptual attractor (trichromatic vision) |
| S (Structure) | 0.85 | Well-structured 3-channel architecture |
| F (Flow) | 0.95 | Dominant photon flux (light emission) |
| I (Information) | 0.95 | High information content (3 × 8-bit channels) |
| D (Dynamics) | 0.40 | Low dynamics (static model) |

### Map Space — Sphinx Eye (REVOI)

\`\`\`
|M_RGB⟩_REVOI = 0.90|R⟩ + 0.95|E⟩ + 0.95|V⟩ + 0.90|O⟩ + 0.95|I⟩
\`\`\`

| Dimension | Score | Justification |
|---|---|---|
| R (Representability) | 0.90 | Excellent — RGB triplet, hex notation, widely understood |
| E (Evolvability) | 0.95 | Spawned HSL, sRGB, HDR standards |
| V (Verifiability) | 0.95 | Directly measurable with spectrophotometers |
| O (Observability) | 0.90 | Directly visible on any screen |
| I (Interoperability) | 0.95 | Universal standard (CSS, OpenGL, web, cameras) |

---

## Channels (Components)

| Channel | GenericConcept | Wavelength | Biological Target |
|---|---|---|---|
| Red (R) | \`m2:Signal\` | ~620–750 nm | L-cones |
| Green (G) | \`m2:Signal\` | ~495–570 nm | M-cones |
| Blue (B) | \`m2:Signal\` | ~450–495 nm | S-cones |

Digital range: \`[0, 255]\` (8-bit) — Analog range: \`[0.0, 1.0]\`

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

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected \`dcterms:creator\`; renamed \`oriveAnalysis\` → \`revoiAnalysis\` |
| 1.0.1 | 2026-01-20 | Minor corrections in GenericConceptsMobilized |
| 1.0.0 | 2026-01-17 | Initial creation |`,

// ── HSL ──────────────────────────────────────────────────────────────────────
HSL: `# M0_HSL_Additive — HSL Additive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

\`M0_HSL_Additive\` is a TSCG M0-layer poclet modeling **perceptual additive color synthesis** using Hue, Saturation, and Lightness channels.

HSL is a **bijective transformation of RGB** — same Territory (perceived color), different Map (cylindrical vs cubic coordinate system). Optimized for human perception and artistic manipulation rather than hardware rendering.

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

\`\`\`
|Ω_color⟩ = 0.70|A⟩ + 0.85|S⟩ + 0.90|F⟩ + 0.95|I⟩ + 0.40|D⟩
\`\`\`

*Identical to RGB Territory — same physical light, same perception.*

### Map Space — Sphinx Eye (REVOI)

\`\`\`
|M_HSL⟩_REVOI = 0.90|R⟩ + 0.95|E⟩ + 0.85|V⟩ + 0.85|O⟩ + 0.90|I⟩
\`\`\`

| Dimension | Score | Justification |
|---|---|---|
| R (Representability) | 0.90 | (H°, S%, L%) matches human perceptual language |
| E (Evolvability) | 0.95 | Spawned HSV, HSI, HSB variants; RGB → HSL demonstrates Map evolution |
| V (Verifiability) | 0.85 | Testable via bijective RGB conversion |
| O (Observability) | 0.85 | Directly observable in all color pickers (Photoshop, CSS) |
| I (Interoperability) | 0.90 | CSS3 \`hsl()\`, standard in all design tools |

**Epistemic Gap:** \`ΔΘ ≈ 0.37\` — Small gap; HSL is a good perceptual model.

---

## Channels (Components)

| Channel | Tensor Formula | Range | Geometry |
|---|---|---|---|
| Hue (H) | \`S⊗I⊗F\` | [0°, 360°) circular | Angular |
| Saturation (S) | \`S⊗I⊗F\` | [0%, 100%] | Radial |
| Lightness (L) | \`S⊗I⊗F\` | [0%, 100%] | Vertical |

**Geometry:** HSL Cylinder = S¹ × [0,1] × [0,1]

### Hue Color Wheel

| Angle | Color | Angle | Color |
|---|---|---|---|
| 0° | Red | 180° | Cyan |
| 60° | Yellow | 240° | Blue |
| 120° | Green | 300° | Magenta |

---

## RGB ↔ HSL Transformation (Bijective)

\`\`\`
HSL → RGB:
  C = (1 - |2L - 1|) × S   // Chroma
  X = C × (1 - |(H/60°) mod 2 - 1|)
  (R, G, B) = sector formula + L offset

RGB → HSL:
  L = (max + min) / 2
  S = (max - min) / (1 - |2L - 1|)
  H = from dominant channel
\`\`\`

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
- ✅ Bijective lossless HSL ↔ RGB

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected \`dcterms:creator\`; renamed \`oriveAnalysis\` → \`revoiAnalysis\` |
| 1.0.1 | 2026-01-20 | Added bijective transformation details |
| 1.0.0 | 2026-01-17 | Initial creation |`,

// ── CMY ──────────────────────────────────────────────────────────────────────
CMY: `# M0_CMY_Subtractive — CMY Subtractive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

\`M0_CMY_Subtractive\` is a TSCG M0-layer poclet modeling **subtractive color synthesis** using Cyan, Magenta, and Yellow pigment primaries.

This is the **theoretical model** of pigment/ink mixing: each primary **absorbs** (subtracts) a portion of white incident light, and the remaining transmitted spectrum produces the perceived color. It is the complement of RGB additive synthesis.

> **TSCG insight:** CMY demonstrates Map falsification in action — the theoretical prediction \`CMY(100,100,100) = black\` fails with real pigments (produces muddy brown), which forced evolution to the CMYK model (Popper's falsification principle).

### Key Characteristics

| Attribute | Value |
|---|---|
| Domain | Optics / Color Science / Printing |
| Principle | Subtractive Synthesis (pigment mixing / spectral filtering) |
| Physical basis | Wavelength-selective absorption by pigments |
| Components | 3 (C, M, Y channels) |
| Poclet type | Composite (Specialized) |
| Complementary to | RGB Additive |
| M2 GenericConcepts | 13 |

---

## TSCG Dual-Space Analysis

### Territory Space — Eagle Eye (ASFID)

\`\`\`
|Ω_pigment⟩ = 0.65|A⟩ + 0.75|S⟩ + 0.70|F⟩ + 0.80|I⟩ + 0.30|D⟩
\`\`\`

| Dimension | Score | Justification |
|---|---|---|
| A (Attractor) | 0.65 | Moderate (color stability under illumination) |
| S (Structure) | 0.75 | Pigment particle organization, surface texture |
| F (Flow) | 0.70 | Incident white light, reflected spectrum |
| I (Information) | 0.80 | Spectral absorption profile |
| D (Dynamics) | 0.30 | Low (pigments stable) |

### Map Space — Sphinx Eye (REVOI)

\`\`\`
|M_CMY⟩_REVOI = 0.85|R⟩ + 0.60|E⟩ + 0.75|V⟩ + 0.70|O⟩ + 0.80|I⟩
\`\`\`

**REVOI mean ≈ 0.74** — Good theoretical Map, poor practical Map.
**Epistemic Gap:** \`ΔΘ ≈ 0.28\` — Small gap for ideal pigments; larger for real materials.

---

## Channels (Components)

| Channel | Absorbs | Transmits | Complement |
|---|---|---|---|
| Cyan (C) | Red (~620–750 nm) | G + B → Cyan | Red (RGB) |
| Magenta (M) | Green (~495–570 nm) | R + B → Magenta | Green (RGB) |
| Yellow (Y) | Blue (~450–495 nm) | R + G → Yellow | Blue (RGB) |

**CMY ↔ RGB:** \`C = 1−R, M = 1−G, Y = 1−B\` (ideal pigments only)

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
| \`CMY(100,100,100) ≠ black\` | Real pigments not spectrally pure | Add K (Key/Black) channel |
| Brown instead of black | Incomplete absorption, scattering | K provides true deep black |
| High ink cost | Three inks needed for dark areas | K cheaper than C+M+Y |

---

## TSCG Validation

- ✅ All 5 ASFID dimensions present
- ✅ 13 GenericConcepts
- ✅ Minimality (3 channels — theoretical primaries)
- ✅ Falsification principle illustrated (CMY → CMYK evolution)

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected \`dcterms:creator\`; renamed \`oriveAnalysis\` → \`revoiAnalysis\` |
| 1.0.1 | 2026-01-20 | Added Popper falsification analysis |
| 1.0.0 | 2026-01-17 | Initial creation |`,

// ── CMYK ─────────────────────────────────────────────────────────────────────
CMYK: `# M0_CMYK_Subtractive — CMYK Subtractive Color Synthesis Poclet

**TSCG Framework · M0 Layer · Color Synthesis Domain**
**Version:** 1.1.0 | **Created:** 2026-01-17 | **Updated:** 2026-02-25
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

\`M0_CMYK_Subtractive\` is a TSCG M0-layer poclet modeling the **practical subtractive color synthesis** used in the commercial printing industry.

It extends the theoretical CMY model with a fourth **Key (Black)** channel, solving the fundamental failure of pure CMY (\`CMY(100,100,100) ≠ black\`). CMYK is the global industry standard for all printed materials.

> **TSCG insight:** CMYK exemplifies the \`m2:Optimization\` GenericConcept — the K channel optimizes the CMY model for real-world constraints (true black, ink cost reduction, process stability). It also demonstrates Map evolution through falsification.

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

\`\`\`
|Ω_print⟩ = 0.70|A⟩ + 0.80|S⟩ + 0.65|F⟩ + 0.85|I⟩ + 0.25|D⟩
\`\`\`

### Map Space — Sphinx Eye (REVOI)

\`\`\`
|M_CMYK⟩_REVOI = 0.90|R⟩ + 0.85|E⟩ + 0.90|V⟩ + 0.85|O⟩ + 0.95|I⟩
\`\`\`

| Dimension | Score | Justification |
|---|---|---|
| R (Representability) | 0.90 | (C%, M%, Y%, K%) — printer-intuitive notation |
| E (Evolvability) | 0.85 | CMY→CMYK; spawned hexachrome; GCR/UCR refined |
| V (Verifiability) | 0.90 | Measured with densitometers; ISO 12647 compliance |
| O (Observability) | 0.85 | Ubiquitous in printed materials; halftone dots visible under loupe |
| I (Interoperability) | 0.95 | ISO 12647, SWOP, Fogra — global standards |

**REVOI mean ≈ 0.89** — Excellent Map quality.
**Epistemic Gap:** \`ΔΘ ≈ 0.27\` — Small gap; CMYK is an excellent practical model.

---

## Channels (Components)

| Channel | Mechanism | Range |
|---|---|---|
| Cyan (C) | Absorbs red light | [0%, 100%] |
| Magenta (M) | Absorbs green light | [0%, 100%] |
| Yellow (Y) | Absorbs blue light | [0%, 100%] |
| Key (K) | Opaque black overlay (non-spectral) | [0%, 100%] |

**TAC (Total Area Coverage):** C + M + Y + K ≤ 300–400% (paper saturation limit)

---

## Black Generation Strategies

| Strategy | Principle | Best Use |
|---|---|---|
| **GCR** | \`K = min(C,M,Y)\` | General commercial printing |
| **UCR** | Replace CMY only in dark areas | High-quality reproduction |
| Maximum K | Maximize K, minimize CMY | Newspapers, low-cost |
| Minimum K | Minimize K, maximize CMY | Fine art reproduction |

---

## Halftoning

| Technique | Method | Use |
|---|---|---|
| AM Screening | Fixed spacing, variable dot size | Traditional offset |
| FM Screening | Fixed dot size, variable spacing | High-quality digital |

**Rosette angles:** C: 105° / M: 75° / Y: 90° / K: 45°

---

## Key Color Mixtures

| Result | CMYK | Notes |
|---|---|---|
| Pure Black | (0%, 0%, 0%, 100%) | K only — true deep black |
| Rich Black | (60%, 40%, 40%, 100%) | Dense for large areas |
| White | (0%, 0%, 0%, 0%) | Paper white — no ink |

---

## TSCG Validation

- ✅ All 5 ASFID dimensions present
- ✅ 15 GenericConcepts
- ✅ Minimality (4 channels — practical minimum for quality printing)
- ✅ Optimization GenericConcept: K channel solves CMY failure
- ✅ Map evolution: CMY (theory) → CMYK (practice)

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-02-25 | Corrected \`dcterms:creator\`; renamed \`oriveAnalysis\` → \`revoiAnalysis\` |
| 1.0.1 | 2026-01-20 | Added halftoning section (AM/FM, rosette) |
| 1.0.0 | 2026-01-17 | Initial creation |`,
}; // end README

// ─────────────────────────────────────────────────────────────────────────────
// GENERIC CONCEPTS DATA  (par modèle, par catégorie)
// ─────────────────────────────────────────────────────────────────────────────

const CONCEPTS = {
  RGB: {
    count: 15,
    pattern: 'Signal × Fusion → emergent Synergy\nR_wave ⊕ G_wave ⊕ B_wave → Perceived Color',
    categories: [
      { name: 'Structural', concepts: [
        { name: 'm2:Component',    formula: 'S⊗I',     role: 'R, G, B as elementary parts' },
        { name: 'm2:Space',        formula: 'S⊗I',     role: 'RGB color space (unit cube ℝ³)' },
        { name: 'm2:Topology',     formula: 'S⊗I',     role: 'Compact, connected, simply-connected' },
        { name: 'm2:Symmetry',     formula: 'S',        role: 'Octahedral symmetry group of RGB cube' },
        { name: 'm2:Invariant',    formula: 'S⊗A',     role: 'Cube topology, achromatic diagonal, complementary pairs' },
      ]},
      { name: 'Informational', concepts: [
        { name: 'm2:Signal',       formula: 'I⊗F',     role: 'R, G, B channels as intensity information carriers' },
        { name: 'm2:Code',         formula: 'I⊗S⊗D',  role: 'Color percept encoded as (R,G,B) triplet — hex, decimal' },
        { name: 'm2:Representation',formula:'I⊗S',    role: 'RGB cube as geometric representation of color space' },
        { name: 'm2:Language',     formula: 'I⊗S⊗F',  role: 'Color naming — #FF5733, named colors, CSS notation' },
        { name: 'm2:Signature',    formula: 'I⊗A',     role: 'Unique color identity (brand colors)' },
      ]},
      { name: 'Regulatory', concepts: [
        { name: 'm2:Constraint',   formula: 'S⊗I',     role: '0 ≤ R,G,B ≤ 255; overflow clipping' },
        { name: 'm2:Threshold',    formula: 'A⊗I',     role: 'JND — Just Noticeable Difference (~2-3 levels)' },
      ]},
      { name: 'Dynamic', concepts: [
        { name: 'm2:Transformation',formula:'D⊗I⊗S',  role: 'Color space conversions: RGB ↔ HSL, RGB ↔ CMYK' },
        { name: 'm2:Fusion',       formula: 'S⊗F⊗D',  role: 'Three light waves fuse into perceived color (+ fission)' },
      ]},
      { name: 'Relational', concepts: [
        { name: 'm2:Synergy',      formula: 'A⊗S⊗I',  role: 'Trichromatic integration → emergent color (yellow from R+G!)' },
      ]},
    ],
  },

  HSL: {
    count: 14,
    pattern: 'Channel × Transformation(HSL↔RGB) × Fusion → emergent Color\nHSL Cylinder = S¹ × [0,1] × [0,1]',
    categories: [
      { name: 'Structural', concepts: [
        { name: 'm2:Space',        formula: 'S⊗I',     role: 'HSL cylindrical color space' },
        { name: 'm2:Topology',     formula: 'S⊗I',     role: 'Cylindrical topology (circular Hue axis)' },
        { name: 'm2:Symmetry',     formula: 'S',        role: 'Rotational symmetry around L axis' },
        { name: 'm2:Invariant',    formula: 'S⊗A',     role: 'Bijection invariant — same Territory as RGB' },
      ]},
      { name: 'Informational', concepts: [
        { name: 'm2:Channel',      formula: 'S⊗I⊗F',  role: 'H, S, L as independent perceptual channels' },
        { name: 'm2:Signal',       formula: 'I⊗F',     role: 'Perceptual dimensions as information carriers' },
        { name: 'm2:Code',         formula: 'I⊗S⊗D',  role: 'hsl(H°, S%, L%) notation' },
        { name: 'm2:Representation',formula:'I⊗S',    role: 'Cylindrical map vs cubic RGB — different Map, same Territory' },
      ]},
      { name: 'Regulatory', concepts: [
        { name: 'm2:Constraint',   formula: 'S⊗I',     role: 'H: [0°,360°); S,L: [0%,100%]; singularity at S=0' },
      ]},
      { name: 'Dynamic', concepts: [
        { name: 'm2:Transformation',formula:'D⊗I⊗S',  role: 'Bijective lossless conversion RGB ↔ HSL' },
        { name: 'm2:Fusion',       formula: 'S⊗F⊗D',  role: 'Channel fusion → perceived color' },
      ]},
      { name: 'Relational', concepts: [
        { name: 'm2:Synergy',      formula: 'A⊗S⊗I',  role: 'Emergent color from perceptual channel combination' },
      ]},
    ],
  },

  CMY: {
    count: 13,
    pattern: 'Channel(Filter) × Fusion(spectral absorption) → emergent Synergy\nC_pigment ⊗ M_pigment ⊗ Y_pigment → Perceived Color (subtractive)',
    categories: [
      { name: 'Structural', concepts: [
        { name: 'm2:Space',        formula: 'S⊗I',     role: 'CMY color space (unit cube, subtractive)' },
      ]},
      { name: 'Informational', concepts: [
        { name: 'm2:Channel',      formula: 'S⊗I⊗F',  role: 'C, M, Y as spectral absorption channels' },
        { name: 'm2:Signal',       formula: 'I⊗F',     role: 'Reflected/transmitted spectrum as information' },
        { name: 'm2:Representation',formula:'I⊗S',    role: '(C%, M%, Y%) encoding of pigment mixture' },
      ]},
      { name: 'Regulatory', concepts: [
        { name: 'm2:Constraint',   formula: 'S⊗I',     role: '0% ≤ C,M,Y ≤ 100%; C+M+Y ≤ 300%' },
        { name: 'm2:Filter',       formula: 'S⊗I⊗F',  role: 'Each pigment filters specific wavelengths' },
      ]},
      { name: 'Dynamic', concepts: [
        { name: 'm2:Transformation',formula:'D⊗I⊗S',  role: 'C = 1−R, M = 1−G, Y = 1−B (ideal pigments)' },
        { name: 'm2:Fusion',       formula: 'S⊗F⊗D',  role: 'Spectral absorption stacking → color' },
      ]},
      { name: 'Energetic', concepts: [
        { name: 'm2:Dissipation',  formula: 'F⊗D',     role: 'Light energy dissipated by absorption; heat from dark pigments' },
      ]},
      { name: 'Relational', concepts: [
        { name: 'm2:Synergy',      formula: 'A⊗S⊗I',  role: 'Color emerges from combined spectral filtering' },
      ]},
    ],
  },

  CMYK: {
    count: 15,
    pattern: 'Channel × Optimization(K) × Fusion → practical printed Color\nK = 1 − max(C,M,Y)  [GCR strategy]',
    categories: [
      { name: 'Structural', concepts: [
        { name: 'm2:Space',        formula: 'S⊗I',     role: 'CMYK color space (4D ink gamut)' },
      ]},
      { name: 'Informational', concepts: [
        { name: 'm2:Channel',      formula: 'S⊗I⊗F',  role: 'C, M, Y, K as ink deposition channels' },
        { name: 'm2:Signal',       formula: 'I⊗F',     role: 'Ink percentage as absorption signal' },
        { name: 'm2:Representation',formula:'I⊗S',    role: '(C%, M%, Y%, K%) printer-native encoding' },
        { name: 'm2:Code',         formula: 'I⊗S⊗D',  role: 'ICC profiles, CMYK color codes for print' },
      ]},
      { name: 'Regulatory', concepts: [
        { name: 'm2:Constraint',   formula: 'S⊗I',     role: 'TAC ≤ 300–400%; 0% ≤ each channel ≤ 100%' },
        { name: 'm2:Optimization', formula: 'D⊗I⊗A',  role: 'K channel: true black + ink cost reduction + stability' },
      ]},
      { name: 'Dynamic', concepts: [
        { name: 'm2:Transformation',formula:'D⊗I⊗S',  role: 'GCR/UCR algorithms; CMYK ↔ RGB conversion' },
        { name: 'm2:Fusion',       formula: 'S⊗F⊗D',  role: 'Four-ink halftone fusion → printed color' },
      ]},
      { name: 'Relational', concepts: [
        { name: 'm2:Synergy',      formula: 'A⊗S⊗I',  role: 'K resolves CMY failure → emergent print quality' },
      ]},
    ],
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// MODEL DATA  (scores ASFID/REVOI par modèle)
// ─────────────────────────────────────────────────────────────────────────────

const MODEL_KEYS    = ['RGB', 'HSL', 'CMY', 'CMYK'];
const MODEL_RGB_CSS = { RGB: '#ff6464', HSL: '#64c8ff', CMY: '#50dca0', CMYK: '#c896ff' };
const MODEL_ADDITIVE= { RGB: true, HSL: true, CMY: false, CMYK: false };

const MODEL_DATA = {
  RGB:  { asfid: { A:0.75, S:0.85, F:0.95, I:0.95, D:0.40 }, revoi: { R:0.90, E:0.95, V:0.95, O:0.90, I:0.95 }, synergy: 'Perceived color (light emission)' },
  HSL:  { asfid: { A:0.70, S:0.85, F:0.90, I:0.95, D:0.40 }, revoi: { R:0.90, E:0.95, V:0.85, O:0.85, I:0.90 }, synergy: 'Perceived color (perceptual coords)' },
  CMY:  { asfid: { A:0.65, S:0.75, F:0.70, I:0.80, D:0.30 }, revoi: { R:0.85, E:0.60, V:0.75, O:0.70, I:0.80 }, synergy: 'Perceived color (pigment absorption)' },
  CMYK: { asfid: { A:0.70, S:0.80, F:0.65, I:0.85, D:0.25 }, revoi: { R:0.90, E:0.85, V:0.90, O:0.85, I:0.95 }, synergy: 'Printed color (ink optimization)' },
};

const ASFID_COLORS = { A:'#ffb43c', S:'#64c8ff', F:'#3cc8a0', I:'#c882ff', D:'#ff6464' };
const REVOI_COLORS = { R:'#64b4ff', E:'#b4ff78', V:'#ffdc50', O:'#ff82c8', I:'#82dcff' };

const SYNTHETIC = [
  // Rangée 1 — spectre chromatique
  ['Red',     [255,   0,   0]],
  ['Orange',  [255, 128,   0]],
  ['Yellow',  [255, 255,   0]],
  ['Green',   [  0, 255,   0]],
  ['Cyan',    [  0, 255, 255]],
  ['Blue',    [  0,   0, 255]],
  ['Magenta', [255,   0, 255]],
  // Rangée 2 — du noir au blanc (niveaux de gris)
  ['Black',   [  0,   0,   0]],
  ['#222',    [ 34,  34,  34]],
  ['#555',    [ 85,  85,  85]],
  ['Gray',    [128, 128, 128]],
  ['#AAA',    [170, 170, 170]],
  ['#DDD',    [221, 221, 221]],
  ['White',   [255, 255, 255]],
];

// ─────────────────────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────────────────────

let activeModel  = 'RGB';
let activeRTab   = 'description';   // 'description' | 'concepts' | 'scores'
let currentRGB   = [180, 80, 220];
const DEFAULT_AZ = 30.0;   // orientation initiale (correspond au screenshot)
const DEFAULT_EL = 20.0;
let cubeAz       = DEFAULT_AZ;
let cubeEl       = DEFAULT_EL;
let cubeDragging = false;
let dragLastPos  = [0, 0];

// ─────────────────────────────────────────────────────────────────────────────
// MARKDOWN RENDERER  (minimal, sans dépendance externe)
// ─────────────────────────────────────────────────────────────────────────────

function renderMarkdown(md) {
  // Échappe HTML sauf dans les blocs code
  const escHtml = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

  // Blocs de code (``` ... ```)
  const codeBlocks = [];
  md = md.replace(/```[\w]*\n?([\s\S]*?)```/g, (_, code) => {
    const i = codeBlocks.length;
    codeBlocks.push(`<pre><code>${escHtml(code.trimEnd())}</code></pre>`);
    return `\x00CODE${i}\x00`;
  });

  const lines = md.split('\n');
  let html = '';
  let inTable = false;
  let inList  = false;

  const flushList = () => { if (inList) { html += '</ul>'; inList = false; } };
  const flushTable= () => { if (inTable){ html += '</tbody></table>'; inTable = false; } };

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];

    // Code block placeholder
    if (/^\x00CODE\d+\x00$/.test(line.trim())) {
      flushList(); flushTable();
      const idx = parseInt(line.match(/\d+/)[0]);
      html += codeBlocks[idx];
      continue;
    }

    // Headings
    const hm = line.match(/^(#{1,3})\s+(.+)$/);
    if (hm) {
      flushList(); flushTable();
      const level = hm[1].length;
      html += `<h${level}>${inlineFormat(hm[2])}</h${level}>`;
      continue;
    }

    // HR
    if (/^---+$/.test(line.trim())) {
      flushList(); flushTable();
      html += '<hr>';
      continue;
    }

    // Table row
    if (/^\|/.test(line)) {
      const cells = line.replace(/^\||\|$/g,'').split('|');
      if (/^[\s|:-]+$/.test(line)) continue; // separator row
      if (!inTable) {
        flushList();
        html += '<table><thead><tr>';
        cells.forEach(c => html += `<th>${inlineFormat(c.trim())}</th>`);
        html += '</tr></thead><tbody>';
        inTable = true;
      } else {
        html += '<tr>';
        cells.forEach(c => html += `<td>${inlineFormat(c.trim())}</td>`);
        html += '</tr>';
      }
      continue;
    }
    if (inTable) { flushTable(); }

    // List item
    if (/^[-*]\s+/.test(line)) {
      if (!inList) { flushTable(); html += '<ul>'; inList = true; }
      html += `<li>${inlineFormat(line.replace(/^[-*]\s+/, ''))}</li>`;
      continue;
    }
    if (inList && line.trim() === '') { flushList(); }

    // Blockquote
    if (/^>\s*/.test(line)) {
      flushList(); flushTable();
      html += `<blockquote>${inlineFormat(line.replace(/^>\s*/, ''))}</blockquote>`;
      continue;
    }

    // Empty line
    if (line.trim() === '') {
      flushList(); flushTable();
      continue;
    }

    // Paragraph
    flushTable();
    if (!inList) html += `<p>${inlineFormat(line)}</p>`;
  }

  flushList(); flushTable();
  return `<div class="md-body">${html}</div>`;
}

function inlineFormat(s) {
  return s
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    // Code inline (avant bold/italic pour ne pas interférer)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Bold
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // Liens [text](url)
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '<a>$1</a>');
}

// ─────────────────────────────────────────────────────────────────────────────
// COLOR MATH
// ─────────────────────────────────────────────────────────────────────────────

function clamp(v, lo=0, hi=1) { return Math.max(lo, Math.min(hi, v)); }
function clampI(v) { return Math.max(0, Math.min(255, Math.round(v))); }

function rgbToHsl(r, g, b) {
  r/=255; g/=255; b/=255;
  const mx=Math.max(r,g,b), mn=Math.min(r,g,b), d=mx-mn;
  const l=(mx+mn)/2, s=d===0?0:d/(1-Math.abs(2*l-1));
  let h=0;
  if(d!==0) {
    if(mx===r) h=60*(((g-b)/d)%6);
    else if(mx===g) h=60*((b-r)/d+2);
    else h=60*((r-g)/d+4);
    if(h<0) h+=360;
  }
  return [h, s*100, l*100];
}
function hslToRgb(h, s, l) {
  s/=100; l/=100;
  const c=(1-Math.abs(2*l-1))*s, x=c*(1-Math.abs((h/60)%2-1)), m=l-c/2;
  let r0,g0,b0;
  if(h<60){r0=c;g0=x;b0=0;}else if(h<120){r0=x;g0=c;b0=0;}
  else if(h<180){r0=0;g0=c;b0=x;}else if(h<240){r0=0;g0=x;b0=c;}
  else if(h<300){r0=x;g0=0;b0=c;}else{r0=c;g0=0;b0=x;}
  return [clampI((r0+m)*255),clampI((g0+m)*255),clampI((b0+m)*255)];
}
function rgbToCmy(r,g,b){return[100-Math.round(r*100/255),100-Math.round(g*100/255),100-Math.round(b*100/255)];}
function cmyToRgb(c,m,y){return[clampI((100-c)*2.55),clampI((100-m)*2.55),clampI((100-y)*2.55)];}
function rgbToCmyk(r,g,b){
  const r0=r/255,g0=g/255,b0=b/255,k=1-Math.max(r0,g0,b0);
  if(k>=0.9999)return[0,0,0,100];
  return[Math.round((1-r0-k)/(1-k)*100),Math.round((1-g0-k)/(1-k)*100),Math.round((1-b0-k)/(1-k)*100),Math.round(k*100)];
}
function cmykToRgb(c,m,y,k){return[clampI(255*(1-c/100)*(1-k/100)),clampI(255*(1-m/100)*(1-k/100)),clampI(255*(1-y/100)*(1-k/100))];}

function computeDynAsfid(r, g, b, base) {
  const r0=r/255,g0=g/255,b0=b/255, brightness=(r0+g0+b0)/3;
  const [,s,l]=rgbToHsl(r,g,b);
  const sorted=[r0,g0,b0].sort((a,b)=>a-b), spread=sorted[2]-sorted[0];
  const variance=((r0-brightness)**2+(g0-brightness)**2+(b0-brightness)**2)/3;
  const colorfulness=clamp(Math.sqrt(variance)*Math.sqrt(3));
  const NAMED=[[0,0,0],[255,255,255],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255],[128,128,128]];
  const maxD=Math.sqrt(3)*255;
  const minD=Math.min(...NAMED.map(([nr,ng,nb])=>Math.sqrt((r-nr)**2+(g-ng)**2+(b-nb)**2)));
  const prox=1-minD/maxD;
  return {
    A:clamp(base.A*(0.3+0.7*prox)), S:clamp(base.S*(0.4+0.6*spread)),
    F:clamp(base.F*(0.1+0.9*brightness)), I:clamp(base.I*(0.3+0.7*colorfulness)),
    D:clamp(base.D*(0.1+0.9*(s/100)*(1-Math.abs(2*l/100-1)))),
  };
}
function epGapNorm(live,base){return Math.sqrt(['A','S','F','I','D'].reduce((acc,d)=>acc+(live[d]-base[d])**2,0));}

// ─────────────────────────────────────────────────────────────────────────────
// RGB CUBE
// ─────────────────────────────────────────────────────────────────────────────

function isoProject(rx,gx,bx,cx,cy,scale,az,el){
  const cA=Math.cos(az*Math.PI/180),sA=Math.sin(az*Math.PI/180);
  const cE=Math.cos(el*Math.PI/180),sE=Math.sin(el*Math.PI/180);
  const x=rx-0.5,y=gx-0.5,z=bx-0.5;
  const x2=x*cA-y*sA, y2=x*sA+y*cA;
  return[cx+x2*scale, cy-(z*cE+y2*sE)*scale];
}
const CUBE_VERTS={Black:[0,0,0],Red:[1,0,0],Green:[0,1,0],Blue:[0,0,1],Yellow:[1,1,0],Cyan:[0,1,1],Magenta:[1,0,1],White:[1,1,1]};
const CUBE_EDGES=[['Black','Red'],['Black','Green'],['Black','Blue'],['Red','Yellow'],['Red','Magenta'],['Green','Yellow'],['Green','Cyan'],['Blue','Cyan'],['Blue','Magenta'],['Yellow','White'],['Cyan','White'],['Magenta','White']];
const INNER_EDGES=[['000','100'],['000','010'],['100','110'],['010','110'],['001','101'],['001','011'],['101','111'],['011','111'],['000','001'],['100','101'],['010','011'],['110','111']];

function drawInnerCube(ctx,cx,cy,r,g,b,scale,az,el){
  const r0=r/255, g0=g/255, b0=b/255, H=0.32;

  // Petit cube FIXE au centre (0.5,0.5,0.5) — seules les couleurs changent.
  const v={};
  for(const ri of[0,1])for(const gi of[0,1])for(const bi of[0,1])
    v[`${ri}${gi}${bi}`]=isoProject(0.5+(ri?H:-H),0.5+(gi?H:-H),0.5+(bi?H:-H),cx,cy,scale,az,el);

  // ── Direction de vue (projection orthographique) ──────────────────
  // V = e1 × e2  avec e1=screen-right, e2=screen-up dans l'espace 3D
  //   V = (-sinAz·cosEl, -cosAz·cosEl, sinEl)
  // Une face est visible si dot(V, normale) > 0  (backface culling)
  const cosAz=Math.cos(az*Math.PI/180), sinAz=Math.sin(az*Math.PI/180);
  const cosEl=Math.cos(el*Math.PI/180), sinEl=Math.sin(el*Math.PI/180);
  const Vx=-sinAz*cosEl, Vy=-cosAz*cosEl, Vz=sinEl;

  // 6 faces : [sommets], normale, rôle visuel
  const FACES6=[
    {pts:["100","110","111","101"], nx: 1,ny: 0,nz: 0}, // R+
    {pts:["000","010","011","001"], nx:-1,ny: 0,nz: 0}, // R-
    {pts:["010","110","111","011"], nx: 0,ny: 1,nz: 0}, // G+
    {pts:["000","100","101","001"], nx: 0,ny:-1,nz: 0}, // G-
    {pts:["001","101","111","011"], nx: 0,ny: 0,nz: 1}, // B+ (haut)
    {pts:["000","100","110","010"], nx: 0,ny: 0,nz:-1}, // B- (bas)
  ];

  // Trier par profondeur (painter's algo) : faces les plus éloignées en premier
  const visible=FACES6
    .map(f=>({...f, dot:Vx*f.nx+Vy*f.ny+Vz*f.nz}))
    .filter(f=>f.dot>0)
    .sort((a,b)=>a.dot-b.dot); // dot faible = plus éloigné de la caméra

  for(const face of visible){
    const isTop = face.nz===1 && Vz>0; // face B+ visible = face haute
    // Luminosité relative selon inclinaison vers le viewer
    const lum = 0.5 + 0.5*(face.dot/1.0); // [0.5 .. 1.0]
    const fr=Math.round(r*lum), fg=Math.round(g*lum), fb=Math.round(b*lum);
    ctx.globalAlpha = isTop ? 1.0 : 0.50;
    ctx.fillStyle=`rgb(${fr},${fg},${fb})`;
    ctx.beginPath();
    ctx.moveTo(...v[face.pts[0]]);
    face.pts.slice(1).forEach(k=>ctx.lineTo(...v[k]));
    ctx.closePath();
    ctx.fill();
  }
  ctx.globalAlpha=1;

  // ── Face haute B+ : même alpha que les autres + carré opaque central ────────
  // (isTop détecté dans la boucle ci-dessus ; on re-dessine par-dessus)
  const topFace = FACES6.find(f=>f.nz===1);
  if (topFace && (Vz > 0)) {
    const tp = topFace.pts.map(k=>v[k]);
    // Carré central = moyenne des 4 coins ± 50% du vecteur vers chaque coin
    const mx4 = tp.reduce((s,p)=>s+p[0],0)/4, my4 = tp.reduce((s,p)=>s+p[1],0)/4;
    const sq  = tp.map(p=>[ mx4+(p[0]-mx4)*0.5, my4+(p[1]-my4)*0.5 ]);
    const lum = 0.5 + 0.5*(Vz); // luminosité face haute
    const fr=Math.round(r*lum), fg=Math.round(g*lum), fb=Math.round(b*lum);
    ctx.globalAlpha=1.0;
    ctx.fillStyle=`rgb(${fr},${fg},${fb})`;
    ctx.beginPath();ctx.moveTo(...sq[0]);sq.slice(1).forEach(p=>ctx.lineTo(...p));ctx.closePath();ctx.fill();
    ctx.globalAlpha=1;
  }

  // ── Arêtes blanches ───────────────────────────────────────────────────────
  ctx.globalAlpha=1;
  ctx.strokeStyle='rgba(255,255,255,0.9)';ctx.lineWidth=2;
  for(const[k1,k2]of INNER_EDGES){ctx.beginPath();ctx.moveTo(...v[k1]);ctx.lineTo(...v[k2]);ctx.stroke();}

  // ── Marqueur de couleur courante : octogone wireframe + pointillés vers centre ──
  const cp  = isoProject(r0,g0,b0,cx,cy,scale,az,el);
  const ctr = isoProject(0.5,0.5,0.5,cx,cy,scale,az,el);
  const OCT_R = 8, SIDES = 8;

  // Ligne pointillée du centre du grand cube → point couleur
  ctx.save();
  ctx.setLineDash([4,4]);
  ctx.strokeStyle='rgba(255,255,255,0.55)';
  ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(ctr[0],ctr[1]);ctx.lineTo(cp[0],cp[1]);ctx.stroke();
  ctx.restore();

  // Octogone wireframe blanc
  ctx.strokeStyle='rgba(255,255,255,0.95)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  for(let i=0;i<SIDES;i++){
    const a=i*(2*Math.PI/SIDES)-Math.PI/SIDES; // orienté pointe en haut
    const px=cp[0]+OCT_R*Math.cos(a), py=cp[1]+OCT_R*Math.sin(a);
    i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
  }
  ctx.closePath();ctx.stroke();

  // Petit cercle plein blanc au centre de l'octogone
  ctx.fillStyle='white';
  ctx.beginPath();ctx.arc(cp[0],cp[1],2.5,0,Math.PI*2);ctx.fill();
}

// ── Petit cube wireframe blanc au centre (0.5,0.5,0.5) du grand cube ───────
function drawCentreMarker(ctx,cx,cy,scale,az,el){
  // Cube plein blanc — H = 0.32/7 ≈ 0.046 (7× plus petit que le petit cube coloré)
  const H=0.0115; // 4× plus petit que la version précédente
  const vc={};
  for(const ri of[0,1])for(const gi of[0,1])for(const bi of[0,1])
    vc[`${ri}${gi}${bi}`]=isoProject(0.5+(ri?H:-H),0.5+(gi?H:-H),0.5+(bi?H:-H),cx,cy,scale,az,el);

  // Direction de vue (même logique que drawInnerCube)
  const cosAz=Math.cos(az*Math.PI/180),sinAz=Math.sin(az*Math.PI/180);
  const cosEl=Math.cos(el*Math.PI/180),sinEl=Math.sin(el*Math.PI/180);
  const Vx=-sinAz*cosEl,Vy=-cosAz*cosEl,Vz=sinEl;

  const FACES6=[
    {pts:["100","110","111","101"],nx: 1,ny: 0,nz: 0},
    {pts:["000","010","011","001"],nx:-1,ny: 0,nz: 0},
    {pts:["010","110","111","011"],nx: 0,ny: 1,nz: 0},
    {pts:["000","100","101","001"],nx: 0,ny:-1,nz: 0},
    {pts:["001","101","111","011"],nx: 0,ny: 0,nz: 1},
    {pts:["000","100","110","010"],nx: 0,ny: 0,nz:-1},
  ];

  // Faces visibles triées (painter's algo — plus éloignées en premier)
  const visible=FACES6
    .map(f=>({...f,dot:Vx*f.nx+Vy*f.ny+Vz*f.nz}))
    .filter(f=>f.dot>0)
    .sort((a,b)=>a.dot-b.dot);

  for(const face of visible){
    const lum=0.7+0.3*face.dot;
    ctx.globalAlpha=1.0;
    ctx.fillStyle=`rgba(${Math.round(255*lum)},${Math.round(255*lum)},${Math.round(255*lum)},1)`;
    ctx.beginPath();
    ctx.moveTo(...vc[face.pts[0]]);
    face.pts.slice(1).forEach(k=>ctx.lineTo(...vc[k]));
    ctx.closePath();
    ctx.fill();
  }
  ctx.globalAlpha=1;
}

function renderCube(r,g,b){
  const canvas=document.getElementById('cubeCanvas');
  // Adapter la hauteur du canvas à l'espace disponible dans le wrapper
  const wrapper=canvas.parentElement;
  const titleH =(wrapper.querySelector('.cube-title')||{offsetHeight:20}).offsetHeight||20;
  const lblH   =(wrapper.querySelector('.principle-lbl')||{offsetHeight:16}).offsetHeight||16;
  const availH =wrapper.clientHeight - titleH - lblH - 10;
  if(availH > 80) canvas.height = availH;
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height,cx=W/2,cy=H/2,scale=Math.min(172, H*0.42);
  ctx.clearRect(0,0,W,H);ctx.fillStyle='#101018';ctx.fillRect(0,0,W,H);
  const pts={};
  for(const[name,[vr,vg,vb]]of Object.entries(CUBE_VERTS))pts[name]=isoProject(vr,vg,vb,cx,cy,scale,cubeAz,cubeEl);
  ctx.strokeStyle='#373750';ctx.lineWidth=1;
  for(const[n1,n2]of CUBE_EDGES){ctx.beginPath();ctx.moveTo(...pts[n1]);ctx.lineTo(...pts[n2]);ctx.stroke();}
  drawInnerCube(ctx,cx,cy,r,g,b,scale,cubeAz,cubeEl);
  drawCentreMarker(ctx,cx,cy,scale,cubeAz,cubeEl);
  const centre=isoProject(0.5,0.5,0.5,cx,cy,scale,cubeAz,cubeEl);
  ctx.font='11px Consolas, monospace';ctx.textBaseline='middle';
  const MARGIN=14;
  for(const[name,[vr,vg,vb]]of Object.entries(CUBE_VERTS)){
    const p=pts[name],col=`rgb(${Math.round(vr*255)},${Math.round(vg*255)},${Math.round(vb*255)})`;
    ctx.fillStyle=col;ctx.beginPath();ctx.arc(p[0],p[1],7,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle='rgba(220,220,230,0.8)';ctx.lineWidth=1;ctx.beginPath();ctx.arc(p[0],p[1],7,0,Math.PI*2);ctx.stroke();
    const dx=p[0]-centre[0],dy=p[1]-centre[1],dist=Math.hypot(dx,dy)||1;
    const ndx=dx/dist,ndy=dy/dist,w=ctx.measureText(name).width;
    let lx=p[0]+ndx*(7+MARGIN),ly=p[1]+ndy*(7+MARGIN);
    if(ndx<-0.1)lx-=w;if(ndy<-0.1)ly-=11;
    ctx.fillStyle='#dcdce6';ctx.fillText(name,lx,ly);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// RIGHT PANEL — rendu des 3 onglets
// ─────────────────────────────────────────────────────────────────────────────

function setRTab(tab) {
  activeRTab = tab;
  document.querySelectorAll('.rtab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.querySelectorAll('.rtab-content').forEach(c => c.classList.toggle('active', c.dataset.tab === tab));
}

// ── Description ──────────────────────────────────────────────────────────────
function updateDescriptionTab() {
  const el = document.getElementById('rtab-description');
  el.innerHTML = renderMarkdown(README[activeModel]);
}

// ── Concepts ─────────────────────────────────────────────────────────────────
function updateConceptsTab() {
  const data = CONCEPTS[activeModel];
  const mcol = MODEL_RGB_CSS[activeModel];
  let h = `<div class="section-title">GenericConcepts — ${activeModel}</div>`;
  h += `<div class="concepts-meta">Total: <strong>${data.count}</strong> GenericConcepts mobilized</div>`;
  h += `<div class="concepts-pattern">${data.pattern.replace(/\n/g,'<br>')}</div>`;
  for (const cat of data.categories) {
    h += `<div class="cat-block"><div class="cat-title">${cat.name}</div>`;
    for (const c of cat.concepts) {
      h += `<div class="concept-row">
              <span class="concept-name" style="color:${mcol}">${c.name}</span>
              <span class="concept-formula">${c.formula}</span>
              <span class="concept-role">${c.role}</span>
            </div>`;
    }
    h += '</div>';
  }
  document.getElementById('rtab-concepts').innerHTML = h;
}

// ── Scores ────────────────────────────────────────────────────────────────────
function updateScoresTab(r, g, b, hex, live, base, gap) {
  const acol = MODEL_RGB_CSS[activeModel];
  const gapCol = gap < 0.3 ? '#50d278' : (gap < 0.5 ? '#ffc832' : '#dc3c3c');
  const gapTxt = gap < 0.3 ? 'Good alignment' : (gap < 0.5 ? 'Moderate gap' : 'Large gap');
  const prin   = MODEL_ADDITIVE[activeModel] ? 'Additive' : 'Subtractive';

  let h = '';

  // ΔΘ + color identity
  h += `<div class="scores-section">
    <div class="section-title">Current Color</div>
    <div class="gap-box">
      <div class="st-swatch-row">
        <div class="st-swatch" style="background:rgb(${r},${g},${b})"></div>
        <span class="st-hex" style="color:${(r+g+b)>200?`rgb(${r},${g},${b})`:'#dcdce6'}">${hex}</span>
      </div>
      <div class="st-row"><span class="lbl">Active model: </span><span style="color:${acol};font-weight:bold">${activeModel}</span></div>
      <div class="st-row" style="margin-bottom:8px"><span class="lbl">Principle: </span><span style="font-weight:bold">${prin}</span></div>
      <div class="gap-row"><span class="gap-value" style="color:${gapCol}">ΔΘ = ${gap.toFixed(3)}</span></div>
      <div class="gap-interp">${gapTxt} (Map–Territory epistemic gap)</div>
    </div>
    <div class="emergent-box">
      <div class="emergent-lbl">Emergent property</div>
      ${MODEL_DATA[activeModel].synergy}
    </div>
  </div>`;

  // ASFID live
  h += '<div class="scores-section"><div class="section-title">ASFID — Eagle Eye · Territory (live)</div>';
  for (const d of ['A','S','F','I','D']) {
    const val=live[d], bval=base[d], col=ASFID_COLORS[d];
    h += `<div class="abar-row">
      <span class="abar-dim" style="color:${col}">${d}</span>
      <div class="abar-track">
        <div class="abar-fill" style="width:${val*100}%;background:${col}"></div>
        <div class="abar-base" style="left:${bval*100}%"></div>
      </div>
      <span class="abar-val" style="color:${col}">${val.toFixed(2)}</span>
    </div>`;
  }
  h += '<div style="font-size:10px;color:var(--dim);margin-top:3px">│ = base score · bar = live value</div></div>';

  // REVOI comparison
  h += '<div class="scores-section"><div class="section-title">REVOI — Sphinx Eye · Map (all models)</div>';
  h += '<div class="revoi-header"><div class="revoi-d-col"></div>';
  for (const mk of MODEL_KEYS) h += `<div class="revoi-m-col" style="color:${MODEL_RGB_CSS[mk]}">${mk}</div>`;
  h += '</div>';
  for (const d of ['R','E','V','O','I']) {
    const col = REVOI_COLORS[d];
    h += `<div class="revoi-row"><div class="revoi-dim" style="color:${col}">${d}</div>`;
    for (const mk of MODEL_KEYS) {
      const val = MODEL_DATA[mk].revoi[d];
      h += `<div class="revoi-cell">
              <div class="revoi-bar-track"><div class="revoi-bar-fill" style="width:${val*100}%;background:${col}"></div></div>
              <div class="revoi-num">${val.toFixed(2)}</div>
            </div>`;
    }
    h += '</div>';
  }
  h += '</div>';

  document.getElementById('rtab-scores').innerHTML = h;
}

// ─────────────────────────────────────────────────────────────────────────────
// NAMED COLORS
// ─────────────────────────────────────────────────────────────────────────────

function buildNamedColors() {
  let h = '';
  for (const [name,[r,g,b]] of SYNTHETIC)
    h += `<div class="nc-btn" id="nc-${name}" onclick="setColor(${r},${g},${b})">
            <div class="nc-swatch" style="background:rgb(${r},${g},${b})"></div>
            <div class="nc-lbl">${name}</div>
          </div>`;
  document.getElementById('namedGrid').innerHTML = h;
}

function refreshNamedColors(r,g,b) {
  for (const [name,[sr,sg,sb]] of SYNTHETIC) {
    const el=document.getElementById(`nc-${name}`);
    if(el) el.classList.toggle('active', Math.sqrt((r-sr)**2+(g-sg)**2+(b-sb)**2)<20);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// FULL UI UPDATE
// ─────────────────────────────────────────────────────────────────────────────

function updateAll() {
  const [r,g,b]         = currentRGB;
  const [h,s,l]         = rgbToHsl(r,g,b);
  const [c,m,y]         = rgbToCmy(r,g,b);
  const [ck,mk,yk,k]    = rgbToCmyk(r,g,b);
  const hex = '#'+[r,g,b].map(v=>v.toString(16).padStart(2,'0').toUpperCase()).join('');

  // Swatch + codes
  const sw = document.getElementById('swatch');
  sw.style.background = `rgb(${r},${g},${b})`;
  sw.style.color      = (r+g+b)<380?'white':'black';
  // Mettre à jour le span hex sans toucher au bouton pipette
  const hexSpan = document.getElementById('hex-val');
  if (hexSpan) hexSpan.textContent = hex;
  document.querySelector('#code-rgb  .c-val').textContent=`(${r}, ${g}, ${b})`;
  document.querySelector('#code-hsl  .c-val').textContent=`(${Math.round(h)}°, ${Math.round(s)}%, ${Math.round(l)}%)`;
  document.querySelector('#code-cmy  .c-val').textContent=`(${c}%, ${m}%, ${y}%)`;
  document.querySelector('#code-cmyk .c-val').textContent=`(${ck}%, ${mk}%, ${yk}%, ${k}%)`;
  for (const mk2 of MODEL_KEYS)
    document.getElementById(`code-${mk2.toLowerCase()}`).style.opacity = mk2===activeModel?'1':'0.45';

  // Model label + principle
  const lbl = document.getElementById('modelLbl');
  lbl.textContent = `${activeModel} Controls`;
  lbl.style.color = MODEL_RGB_CSS[activeModel];
  document.getElementById('principleLbl').textContent =
    `Principle: ${MODEL_ADDITIVE[activeModel]?'Additive (light)':'Subtractive (pigment)'}`;

  // ASFID + gap (needed by Scores tab)
  const base = MODEL_DATA[activeModel].asfid;
  const live = computeDynAsfid(r,g,b,base);
  const gap  = epGapNorm(live, base);

  // Named colors
  refreshNamedColors(r,g,b);

  // Cube
  renderCube(r,g,b);

  // Right panel tabs (update active only + rebuild all on model change)
  updateDescriptionTab();
  updateConceptsTab();
  updateScoresTab(r,g,b,hex,live,base,gap);
}

// ─────────────────────────────────────────────────────────────────────────────
// SLIDER SYNC
// ─────────────────────────────────────────────────────────────────────────────

function syncSlidersFromRGB() {
  const [r,g,b]      = currentRGB;
  const [h,s,l]      = rgbToHsl(r,g,b);
  const [c,m,y]      = rgbToCmy(r,g,b);
  const [ck,mk,yk,k] = rgbToCmyk(r,g,b);
  function sv(id,v,fmt){ const e=document.getElementById(id); if(e)e.value=v; const ve=document.getElementById('v'+id.slice(1)); if(ve)ve.textContent=fmt; }
  sv('sr',r,r); sv('sg',g,g); sv('sb',b,b);
  sv('sh',h,Math.round(h)+'°'); sv('ss',s,Math.round(s)+'%'); sv('sl',l,Math.round(l)+'%');
  sv('scy',c,c+'%'); sv('smg',m,m+'%'); sv('syw',y,y+'%');
  sv('sck',ck,ck+'%'); sv('smk',mk,mk+'%'); sv('syk',yk,yk+'%'); sv('skk',k,k+'%');
}

function onSlide() {
  let r,g,b;
  const v=id=>+document.getElementById(id).value;
  const txt=(id,s)=>{const e=document.getElementById(id);if(e)e.textContent=s;};
  if(activeModel==='RGB'){
    r=v('sr');g=v('sg');b=v('sb'); txt('vr',r);txt('vg',g);txt('vb',b);
  } else if(activeModel==='HSL'){
    const H=v('sh'),S=v('ss'),L=v('sl');
    txt('vh',Math.round(H)+'°');txt('vs',Math.round(S)+'%');txt('vl',Math.round(L)+'%');
    [r,g,b]=hslToRgb(H,S,L);
  } else if(activeModel==='CMY'){
    const C=v('scy'),M=v('smg'),Y=v('syw');
    txt('vcy',Math.round(C)+'%');txt('vmg',Math.round(M)+'%');txt('vyw',Math.round(Y)+'%');
    [r,g,b]=cmyToRgb(C,M,Y);
  } else {
    const C=v('sck'),M=v('smk'),Y=v('syk'),K=v('skk');
    txt('vck',Math.round(C)+'%');txt('vmk',Math.round(M)+'%');txt('vyk',Math.round(Y)+'%');txt('vkk',Math.round(K)+'%');
    [r,g,b]=cmykToRgb(C,M,Y,K);
  }
  currentRGB=[r,g,b];
  syncSlidersFromRGB();
  updateAll();
}

// ─────────────────────────────────────────────────────────────────────────────
// MODEL / COLOR SETTERS
// ─────────────────────────────────────────────────────────────────────────────

function setModel(key) {
  activeModel=key;
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.m===key));
  document.querySelectorAll('.slider-group').forEach(g=>g.classList.toggle('active',g.dataset.m===key));
  syncSlidersFromRGB();
  updateAll();
}

function setColor(r,g,b) {
  currentRGB=[r,g,b];
  syncSlidersFromRGB();
  updateAll();
}

function resetColor() {
  cubeAz = DEFAULT_AZ;
  cubeEl = DEFAULT_EL;
  setColor(180, 80, 220);
}

// ── Pipette : EyeDropper API (native Chromium / Electron) ─────────────────
async function pickColor() {
  if (!window.EyeDropper) {
    console.warn('EyeDropper API non disponible dans cette version Electron');
    return;
  }
  try {
    const btn = document.getElementById('btn-eyedropper');
    if (btn) btn.style.opacity = '1';
    const result = await new EyeDropper().open();
    // result.sRGBHex = "#rrggbb"
    const h = result.sRGBHex;
    const r = parseInt(h.slice(1,3), 16);
    const g = parseInt(h.slice(3,5), 16);
    const b = parseInt(h.slice(5,7), 16);
    setColor(r, g, b);
  } catch(e) {
    // L'utilisateur a appuyé sur Échap — pas d'erreur à afficher
  } finally {
    const btn = document.getElementById('btn-eyedropper');
    if (btn) btn.style.opacity = '0.7';
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// CUBE DRAG ROTATION
// ─────────────────────────────────────────────────────────────────────────────

function initCubeDrag() {
  const canvas=document.getElementById('cubeCanvas');
  const hint  =document.getElementById('dragHint');

  // ── Clic sur un sommet → change la couleur courante ──────────────
  // On mesure le déplacement entre mousedown et mouseup :
  // si < 4px c'est un clic, sinon c'est un drag.
  let clickStartPos = null;

  canvas.addEventListener('mousedown', e => {
    cubeDragging = true;
    dragLastPos  = [e.clientX, e.clientY];
    clickStartPos= [e.clientX, e.clientY];
    canvas.classList.add('dragging');
    hint.textContent = '[rotating...]';
    e.preventDefault();
  });

  window.addEventListener('mouseup', e => {
    if (!cubeDragging) return;
    cubeDragging = false;
    document.getElementById('cubeCanvas').classList.remove('dragging');
    hint.textContent = '[drag to rotate]';

    // Clic détecté si le curseur n'a pas bougé de plus de 4px
    if (clickStartPos) {
      const dx = e.clientX - clickStartPos[0];
      const dy = e.clientY - clickStartPos[1];
      if (Math.hypot(dx, dy) < 4) {
        trySelectVertex(canvas, e.clientX, e.clientY);
      }
    }
    clickStartPos = null;
  });

  window.addEventListener('mousemove', e => {
    if (cubeDragging) {
      cubeAz=(cubeAz+(e.clientX-dragLastPos[0])*0.4)%360;
      cubeEl=Math.max(-80,Math.min(80,cubeEl-(e.clientY-dragLastPos[1])*0.3));
      dragLastPos=[e.clientX,e.clientY];
      renderCube(...currentRGB);
      return;
    }
    // Curseur pointer au survol d'un sommet
    const rect  = canvas.getBoundingClientRect();
    const mx    = e.clientX - rect.left, my = e.clientY - rect.top;
    const W=canvas.width, H=canvas.height, cx=W/2, cy=H/2, scale=172;
    const onVertex = Object.values(CUBE_VERTS).some(([vr,vg,vb]) => {
      const [px,py]=isoProject(vr,vg,vb,cx,cy,scale,cubeAz,cubeEl);
      return Math.hypot(mx-px, my-py) < 18;
    });
    canvas.style.cursor = onVertex ? 'pointer' : 'grab';
  });
}

// ── Sélection du sommet le plus proche du clic ───────────────────
function trySelectVertex(canvas, clientX, clientY) {
  const rect  = canvas.getBoundingClientRect();
  const mx    = clientX - rect.left;
  const my    = clientY - rect.top;
  const W     = canvas.width, H = canvas.height;
  const cx    = W / 2,        cy = H / 2, scale = 172;
  const HIT_R = 18;   // rayon de détection en pixels

  let bestDist = Infinity, bestRGB = null;

  for (const [name, [vr, vg, vb]] of Object.entries(CUBE_VERTS)) {
    const [px, py] = isoProject(vr, vg, vb, cx, cy, scale, cubeAz, cubeEl);
    const d = Math.hypot(mx - px, my - py);
    if (d < HIT_R && d < bestDist) {
      bestDist = d;
      bestRGB  = [Math.round(vr * 255), Math.round(vg * 255), Math.round(vb * 255)];
    }
  }

  if (bestRGB) setColor(...bestRGB);
}

// ── Splitter haut/bas (cube / named colors) ─────────────────────────────────
function initSplitterTB() {
  const splitter  = document.getElementById('splitter-tb');
  const namedArea = document.getElementById('namedArea');
  const canvas    = document.getElementById('cubeCanvas');
  if (!splitter || !namedArea) return;

  // Hauteur initiale (+30% vs contenu naturel)
  namedArea.style.height    = '172px';
  namedArea.style.flexShrink= '0';
  namedArea.style.overflow  = 'hidden';

  let dragging=false, startY=0, startH=0;

  splitter.addEventListener('mousedown', e=>{
    dragging=true; startY=e.clientY;
    startH=namedArea.getBoundingClientRect().height;
    splitter.classList.add('dragging');
    document.body.style.cssText='cursor:row-resize;user-select:none;-webkit-user-select:none';
    e.preventDefault();
  });
  document.addEventListener('mousemove', e=>{
    if(!dragging)return;
    const newH=Math.max(172, Math.min(320, startH+(startY-e.clientY)));
    namedArea.style.height=newH+'px';
    namedArea.style.flexShrink='0';
    namedArea.style.overflow='hidden';
  });
  document.addEventListener('mouseup', ()=>{
    if(!dragging)return;
    dragging=false;
    splitter.classList.remove('dragging');
    document.body.style.cssText='';
    renderCube(...currentRGB);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// KEYBOARD
// ─────────────────────────────────────────────────────────────────────────────

window.addEventListener('keydown', e => {
  if (e.key==='Tab') {
    e.preventDefault();
    setModel(MODEL_KEYS[(MODEL_KEYS.indexOf(activeModel)+1)%MODEL_KEYS.length]);
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  buildNamedColors();
  syncSlidersFromRGB();
  initCubeDrag();
  initSplitter();
  initSplitterLC();
  initSplitterTB();
  setRTab('description');  // onglet droit par défaut
  updateAll();
});

// ── Splitter left / center ───────────────────────────────────────────────────
function initSplitterLC() {
  const splitter   = document.getElementById('splitter-lc');
  const panelLeft  = document.querySelector('.panel-left');
  if (!splitter || !panelLeft) return;

  let dragging=false, startX=0, startW=0;

  splitter.addEventListener('mousedown', e=>{
    dragging=true; startX=e.clientX;
    startW=panelLeft.getBoundingClientRect().width;
    splitter.classList.add('dragging');
    document.body.style.cssText='cursor:col-resize;user-select:none;-webkit-user-select:none';
    e.preventDefault();
  });
  document.addEventListener('mousemove', e=>{
    if(!dragging)return;
    const newW=Math.max(220, Math.min(480, startW+(e.clientX-startX)));
    panelLeft.style.width=newW+'px';
  });
  document.addEventListener('mouseup', ()=>{
    if(!dragging)return;
    dragging=false;
    splitter.classList.remove('dragging');
    document.body.style.cssText='';
    renderCube(...currentRGB);
  });
}

// ── Splitter center/right ────────────────────────────────────────────────
function initSplitter() {
  const splitter    = document.getElementById('splitter-cr');
  const panelCenter = document.querySelector('.panel-center');
  const panelRight  = document.querySelector('.panel-right');
  if (!splitter) return;

  let dragging=false, startX=0, startW=0;

  splitter.addEventListener('mousedown', e=>{
    dragging=true; startX=e.clientX;
    startW=panelRight.getBoundingClientRect().width;
    splitter.classList.add('dragging');
    document.body.style.cssText='cursor:col-resize;user-select:none;-webkit-user-select:none';
    e.preventDefault();
  });
  document.addEventListener('mousemove', e=>{
    if(!dragging)return;
    const newW=Math.max(320, Math.min(680, startW+(startX-e.clientX)));
    panelRight.style.width=newW+'px';
  });
  document.addEventListener('mouseup', ()=>{
    if(!dragging)return;
    dragging=false;
    splitter.classList.remove('dragging');
    document.body.style.cssText='';
    // Redessiner le cube après redimensionnement
    renderCube(...currentRGB);
  });
}
