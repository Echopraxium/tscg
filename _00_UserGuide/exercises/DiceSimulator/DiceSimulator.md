# Dice Simulator — TSCG Exercise

**Domain:** Probability / statistics (D&D lineage)
**Difficulty:** Starter
**Natural simulation:** 2D (p5.js) — roll dice, watch a histogram converge

## 1. The system in one paragraph
Roll polyhedral dice — **D4, D6, D8, D12, D20**. Each die is a uniform discrete
distribution over its faces. Rolling many times reveals that distribution; summing
several dice shifts the shape from flat toward a bell curve. A hands-on window
into randomness, the law of large numbers, and the central limit theorem.

## 2. Suggested scope (minimal + complete)
The five platonic dice, single rolls and multi-die **sums**, and an accumulating
**histogram**. That is enough to make the probabilistic facets concrete.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **limiting distribution** — the empirical histogram
  converges to the theoretical PMF as rolls accumulate (law of large numbers);
  sums of dice tend toward a Gaussian (CLT). The distribution *is* the attractor.
- **S** (Structure): the **dice** (their face sets) and the **histogram bins**.
- **F** (Flow): the **stream of rolls** accumulating into the histogram.
- **I** (Information): each roll outcome, the underlying uniform law, and the
  **entropy** of a single die (`log₂` of its face count).
- **D** (Dynamics): **convergence** of the empirical distribution to the
  theoretical one over trials.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Stochastic process / random draw** concept.
- A **Convergence to a distribution (LLN)** concept.
- An **Aggregation / superposition** concept (dice sums → CLT).
- A **Uniform distribution / entropy** concept. Verify against
  `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** probability/statistics domain → **new-domain
  finding**. (Fitting for TSCG's stated D&D / Gygax toolmaker lineage.)
- **Possible M2 candidate?** "Empirical convergence to a limiting law" is a broad
  transdisciplinary pattern; flag with discipline if it recurs.

## 6. Source documentation
References on dice probability, the law of large numbers, and the central limit
theorem (the Wikipedia articles of the same names). Attach in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Pick a die (or a sum like `3d6`), roll N times with a speed control, and animate
the histogram filling in and converging to the theoretical curve — single die
(flat) versus sums (bell). The convergence *is* the visible **Attractor**.
