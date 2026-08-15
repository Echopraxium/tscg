# Image Processing — TSCG Exercise

**Domain:** Image processing / computer vision (adjacent to optics, photography)
**Difficulty:** Starter
**Natural simulation:** 2D (p5.js) — an image with live contrast / grayscale / ANSI controls

## 1. The system in one paragraph
An image is a grid of pixels. A chain of operations transforms it: **contrast**
stretching (remap intensities), **grayscale** conversion (weighted luminance),
**quantisation** (reduce to few levels, with optional dithering), and mapping to a
reduced palette to produce **ANSI / ASCII art**. Each step is a point or
neighbourhood operation, and several discard information irreversibly.

## 2. Suggested scope (minimal + complete)
Model a short transform pipeline — grayscale → contrast → quantise → ANSI mapping
— on one image. That is enough to show the facets and the information loss.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): weak — there is no dynamical attractor, only a **target
  representation**. Be honest: this poclet is **transformation-dominant**, light
  on Attractor (like Logic Gates is Information-dominant). That imbalance is a
  legitimate, discussable shape, not a defect.
- **S** (Structure): the **pixel grid** and its channels.
- **F** (Flow): pixels flowing through the **transform pipeline**.
- **I** (Information): pixel values, transform parameters, and the **information
  lost** at grayscale/quantisation (a nice entropy angle).
- **D** (Dynamics): sequential application of operations (weak temporal dynamics).

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Transformation / mapping** concept.
- A **Pipeline / composition** concept.
- A **Reduction / quantisation (information loss)** concept.
- A **Projection** angle: colour → gray → symbols is a chain of successive
  reductions (Map/Territory). Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** raster image-processing domain. Note the
  **adjacency to `optics` and `photography`** (both exist) — but those model the
  physics of vision / the photographic act, not pixel operations. Discuss with
  Claude whether this belongs in a new domain or enriches an existing one.
- **Possible M2 candidate?** "Lossy reduction of a representation" may generalise;
  flag if it recurs, don't assume.

## 6. Source documentation
Any intro to image point-operations, luminance weighting, and dithering (e.g. the
Wikipedia articles "Grayscale", "Contrast (vision)", "Dither", "ASCII art").
Attach in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Load or generate an image; sliders for contrast and quantisation levels, a
grayscale toggle, and a live ANSI/ASCII rendering beside the raster — so the user
sees the successive **reductions** and where information is discarded.
