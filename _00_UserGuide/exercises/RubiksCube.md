# Rubik's Cube — TSCG Exercise

**Domain:** Combinatorics / puzzles (group theory)
**Difficulty:** Intermediate
**Natural simulation:** 3D (BabylonJS) — the obvious case for a 3D view

## 1. The system in one paragraph
A 3×3×3 cube of 26 movable cubies. Each of the six faces can rotate, permuting
stickers. From ~4.3×10¹⁹ reachable states there is exactly **one solved state**;
solving is finding a sequence of face turns that reaches it.

## 2. Suggested scope (minimal + complete)
The standard 3×3×3 cube, modelled as a **state + a move set**, with "solved" as
the target. You do not need to implement a solver — model the *system*, and let
the simulation allow scrambling and turning. (A 2×2×2 cube is a fine reduction if
3×3×3 feels heavy.)

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **solved state** — the single distinguished configuration.
- **S** (Structure): the **cubies and faces**, and the permutation group the legal
  moves generate.
- **F** (Flow): **face turns** carrying the cube from state to state.
- **I** (Information): the **current configuration** (which sticker is where) and
  the **legal-move rules**.
- **D** (Dynamics): the **trajectory through state space** as moves are applied.

> This is a strong **Map vs Territory** teaching case: the *Territory* is the
> physical cube and its state; a solving *method* (a sequence of moves) is a
> **Map** — a path chosen through the space, not the space itself. Expect that
> distinction to come up in Analysis.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **State space** concept (the set of configurations).
- A **Path / trajectory** concept (a move sequence) — and the Map/Territory
  contrast between a *path* and the *space*.
- An **Attractor / goal state** concept (solved).
- Possibly a **Symmetry / group** concept (the moves form a group).
Verify against `M2_GenericConcepts.jsonld` at HEAD; don't trust remembered formulas.

## 5. Domain question
- **Existing M1 extension?** **No** combinatorics/puzzle/group-theory domain at
  HEAD. This is a **new-domain finding** — Analysis may open one, or model with
  M1_CoreConcepts. A well-argued new domain here is a real contribution.
- **Possible M2 candidate?** "Navigation through a large state space toward a
  single goal state under a fixed move set" recurs widely (search, planning,
  puzzles). If it isn't already captured, this is a plausible candidate to flag.

## 6. Source documentation
A reference on the Rubik's Cube and, optionally, a short note on its permutation
group (the Wikipedia articles "Rubik's Cube" and "Rubik's Cube group"). Attach it
in the Proposition step.

## 7. Simulation hint (3D, BabylonJS)
Render the cube; let the user drag to orbit, click-drag a face to turn it, and
scramble/reset. Colour-highlight how far each sticker is from solved. This is the
exercise that earns a 3D scene — start from `instances/poclets/_00_template/`.
