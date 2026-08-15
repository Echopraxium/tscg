# Mini Alchemy Game — TSCG Exercise

**Domain:** Game / crafting systems / combinatorics
**Difficulty:** Starter
**Natural simulation:** 2D (HTML/p5.js) — drag-combine items, a discovery grid fills in

## 1. The system in one paragraph
Like *Little Alchemy*: start from a few base elements (earth, water, fire, air).
Combining a pair of items yields a new item according to a **recipe table**; the
new items combine further, and the player **discovers** the whole set (aim for
30–70 items) by exploring the combination graph.

## 2. Suggested scope (minimal + complete)
A small curated recipe graph (~30–40 items), the base elements, and the pairwise
combination rule. Model the **combination system and the discovery progression**,
not a polished game UI.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **complete collection** — the reachable **closure** of the
  recipe graph is the goal state discovery tends toward.
- **S** (Structure): the **items** and the **recipe (dependency) graph**.
- **F** (Flow): **combination** operations producing new items; discovery
  propagating through the graph.
- **I** (Information): the **recipe table** (the rules) plus the player's current
  known set / inventory.
- **D** (Dynamics): **monotone growth** of the discovered set toward closure — each
  combine only adds, never removes (progress toward the attractor).

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Combination / synthesis (two → one)** concept.
- A **Closure / reachable-set** concept.
- A **Monotone progress toward an attractor** concept (kin to Bubble Sort's
  convergence — worth comparing).
- A **Dependency graph** concept. Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** game/crafting-systems domain → **new-domain
  finding**. (Conceptually the "combine two things into a third" rule rhymes with
  chemistry combination combos — a nice cross-domain check for Claude.)
- **Possible M2 candidate?** A "synthesis closure over a combination graph" pattern
  may generalise; flag if it recurs across domains.

## 6. Source documentation
A reference on combination/crafting games and reachability (e.g. describe the
*Little Alchemy* mechanic; and the graph-theory notion of transitive closure).
Attach in the Proposition step.

## 7. Simulation hint (2D, HTML/p5.js)
Drag two items together to attempt a combine; discovered items populate a grid,
with a progress counter toward the full set and hints for undiscovered branches.
