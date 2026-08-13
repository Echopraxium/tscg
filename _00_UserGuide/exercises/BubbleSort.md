# Bubble Sort — TSCG Exercise

**Domain:** Computer science / algorithms
**Difficulty:** Starter
**Natural simulation:** 2D (p5.js) — bars swapping until sorted

## 1. The system in one paragraph
Bubble sort repeatedly walks through a list, comparing each adjacent pair and
swapping them if they are out of order. Large values "bubble" to the end pass by
pass; when a full pass makes no swaps, the list is sorted.

## 2. Suggested scope (minimal + complete)
One small array (say 6–8 integers) sorted ascending. That is enough to show every
facet without noise.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **sorted arrangement** — the one stable end state.
- **S** (Structure): the **array** of elements and their positions.
- **F** (Flow): **swaps** moving elements past one another.
- **I** (Information): each **pairwise comparison** (is left > right?).
- **D** (Dynamics): the **pass-by-pass** evolution toward order.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Process / iteration** concept (repeated passes).
- A **Comparison / decision** concept (the swap test).
- A **Convergence toward an attractor** concept (progress to "sorted").
Verify names and formulas against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** — there is no computing/algorithms domain at
  HEAD. This is a genuine **new-domain finding**: your Analysis may propose a
  first `computing` (or `algorithms`) extension, or model it with M1_CoreConcepts
  only. Treat that decision carefully with Claude.
- **Possible M2 candidate?** A "monotone convergence by local repair" pattern
  (each step never worsens the global order) might generalise across domains
  (annealing, gradient descent, settling). Flag it; don't assume it.

## 6. Source documentation
Any standard algorithms reference (e.g. the Wikipedia "Bubble sort" article) plus
a short trace of one sort by hand. Attach it in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Vertical bars for the values; highlight the compared pair, animate the swap, mark
the "settled" tail after each pass, and stop when a pass makes no swaps. The
sorted state reads visually as the **Attractor**.
