# Fractal Explorer — TSCG Exercise

**Domain:** Mathematics / dynamical systems / geometry
**Difficulty:** Intermediate
**Natural simulation:** 2D (canvas/p5.js) — escape-time render with zoom & pan

## 1. The system in one paragraph
Fractals show detail at every scale. The **Mandelbrot set** is the set of complex
numbers `c` for which `z → z² + c` (starting at `z = 0`) stays bounded; its
boundary is infinitely intricate and self-similar. The **Sierpiński** triangle /
carpet are built the opposite way — by recursively removing sub-parts (an
iterated function system). Two flavours: *escape-time iteration* vs *recursive
geometric construction*.

## 2. Suggested scope (minimal + complete)
Model **one** as the poclet. Recommended: the **Mandelbrot** escape-time system
(richest dynamics) with zoom, colouring by iteration count. Note Sierpiński as a
sibling recursion exercise if you prefer geometric construction.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **bounded/escape dichotomy** (set membership); more
  deeply, the actual attractors of the iterated map per `c`, and **self-similarity**
  as a scale-invariant.
- **S** (Structure): the **complex plane** sampled as a pixel grid (or the
  recursion tree for an IFS).
- **F** (Flow): the **iteration** `z → z² + c` — escape trajectories.
- **I** (Information): the **escape time** (→ colour) and the generating rule.
- **D** (Dynamics): the iterative process; zooming reveals scale-invariance.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- An **Iteration / recursion** concept.
- A **Self-similarity / scale-invariance** concept.
- A **Boundary / threshold** concept (bounded vs escaped).
- Strong **Map/Territory** angle: the rendered image is a finite **Map** of an
  infinite mathematical **Territory**. Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** mathematics/dynamical-systems domain →
  **new-domain finding**.
- **Possible M2 candidate?** "Self-similarity across scales" is a candidate
  transdisciplinary pattern (coastlines, trees, turbulence). Flag with anti-
  overfitting discipline; it may relate to emergence (Game of Life / Truchet).

## 6. Source documentation
References on the Mandelbrot set and Sierpiński fractals / IFS (the Wikipedia
articles "Mandelbrot set" and "Sierpiński triangle"). Attach in the Proposition step.

## 7. Simulation hint (2D)
Render the Mandelbrot set; let the user click-zoom and pan, adjust max iterations
and palette. (Compute-heavy — note performance and consider a resolution cap.)
For Sierpiński, animate the recursive subdivision instead.
