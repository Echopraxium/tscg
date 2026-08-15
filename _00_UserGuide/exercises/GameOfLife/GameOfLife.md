# Game of Life — TSCG Exercise

**Domain:** Cellular automata / complexity
**Difficulty:** Starter (concept) / Intermediate (rule-driven generalisation)
**Natural simulation:** 2D (p5.js) — an editable grid ticking through generations

## 1. The system in one paragraph
Conway's Game of Life runs on a grid of cells, each **live** or **dead**. Every
generation, each cell updates from its 8 neighbours by two rules: a dead cell
with exactly 3 live neighbours is **born**; a live cell **survives** with 2 or 3,
otherwise it dies. From these trivial local rules, complex global behaviour
emerges — still lifes, oscillators, and travelling **gliders**. Generalises to
any birth/survival rule string (a rules-driven cellular automaton).

## 2. Suggested scope (minimal + complete)
Standard Life (`B3/S23`) on a finite grid, with the birth/survival rule editable
so the user can explore other automata. A handful of seed patterns (block,
blinker, glider) is enough.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): **still lifes and oscillators** — the fixed points and cycles
  the field settles into (many seeds end quiescent or periodic).
- **S** (Structure): the **grid** and the **Moore neighbourhood** (8 neighbours).
- **F** (Flow): **information travelling** across the grid — a glider literally
  transports a pattern.
- **I** (Information): each cell's state **plus the rule table** (B/S).
- **D** (Dynamics): **synchronous discrete updates**; emergence over generations.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- An **Emergence / local-rule → global-pattern** concept (the heart of it).
- An **Iteration / discrete-time process** concept.
- An **Attractor** concept (fixed points and limit cycles).
Verify against `M2_GenericConcepts.jsonld` at HEAD; do not recite formulas from memory.

## 5. Domain question
- **Existing M1 extension?** **No** cellular-automata/complexity domain at HEAD →
  **new-domain finding**.
- **Possible M2 candidate?** "Global complexity emerging from simple local rules"
  is a deep transdisciplinary pattern — but it **clusters with Truchet Patterns**
  (and any other CA). Do not formalise on one instance: gather attested residue
  across ≥6 independent domains first. Flag, don't improvise.

## 6. Source documentation
Any reference on Conway's Life and cellular automata (e.g. the Wikipedia
"Conway's Game of Life" article, and "Life-like cellular automaton" for the rule
notation). Attach it in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Toggle cells to seed, play/step/reset, an editable `B/S` rule field, and a small
pattern palette. Highlight a glider moving to make the **Flow** facet visible.
