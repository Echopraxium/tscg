# Truchet Patterns Explorer — TSCG Exercise

**Domain:** Generative art / tiling / combinatorics
**Difficulty:** Starter
**Natural simulation:** 2D (p5.js) — a grid of Truchet tiles you can re-roll

## 1. The system in one paragraph
A **Truchet tile** is a square carrying a simple asymmetric motif (classically two
quarter-arcs, or a diagonal split). Filling a grid with copies of one tile in
varied **orientations** — random or rule-driven — produces surprisingly complex
global patterns: flowing contours, mazes, weaves. One tile plus an orientation
rule generates endless emergent designs.

## 2. Suggested scope (minimal + complete)
One tile type, a grid, and an orientation rule (random, or a simple deterministic
rule). Explore how the local per-tile choice shapes the global pattern.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): weak/statistical — no dynamical attractor, but a recognisable
  **pattern class** emerges. Be honest that this is a **generative** poclet, not a
  convergent one.
- **S** (Structure): the **grid**, the **tile motif**, and the **orientation set**.
- **F** (Flow): **visual continuity across tile edges** — arcs connect into
  flowing contours and paths.
- **I** (Information): the **per-tile orientation** (a few bits each) plus the tile
  design — low local information yielding high global complexity (emergence).
- **D** (Dynamics): weak when static; add re-rolling/animation to give it motion.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- An **Emergence (local → global)** concept.
- A **Combination / tiling** concept.
- A **Symmetry / orientation** concept.
- Possibly a **Continuity / edge-matching** concept.
Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** generative-art/tiling domain → **new-domain
  finding**.
- **Possible M2 candidate?** Emergence again — this **clusters with Game of Life**
  (and cellular automata generally). Convergence of the *same* pattern across
  independent exercises is exactly the attested residue the anti-overfitting rule
  wants before admitting an "Emergence" concept; flag it, don't formalise early.

## 6. Source documentation
A reference on Truchet tiles / tilings (the Wikipedia article "Truchet tiles").
Attach in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Grid of Truchet tiles; choose the tile type and orientation rule, adjust density,
and re-roll. A natural fit for a generative-art community when you publish (see
the Reddit distribution strategy — seed it where generative artists gather).
