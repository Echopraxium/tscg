# Maze Generator and Solver — TSCG Exercise

**Domain:** Graph algorithms / computer science
**Difficulty:** Intermediate
**Natural simulation:** 2D (p5.js) — animate carving, then animate solving

## 1. The system in one paragraph
A maze is a **graph**: cells are nodes, passages are edges. **Generation** carves a
spanning tree (e.g. recursive backtracker, Prim, or Kruskal), producing a *perfect
maze* with exactly one path between any two cells. **Solving** then finds a route
from entrance to exit (BFS, DFS, or A*). Two coupled processes: build the
structure, then traverse it.

## 2. Suggested scope (minimal + complete)
One grid maze, one generation algorithm, and one solver. Model both phases as the
poclet — the structure it builds and the search that traverses it.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): two, one per phase — generation targets a **perfect maze**
  (a spanning tree); solving targets the **solution path**. Note the pair cleanly.
- **S** (Structure): the **cell grid** with walls/passages — i.e. a graph.
- **F** (Flow): the carving frontier during generation, and the search frontier /
  the discovered **path** from start to goal during solving.
- **I** (Information): passage state per edge, visited/frontier state during
  search, and the algorithm's rule.
- **D** (Dynamics): a clear two-stage temporal evolution — generation, then search.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Process / search** concept.
- A **Spanning structure / connectivity (tree)** concept.
- A **Path / trajectory** concept — with the **Map/Territory** angle: the maze is
  the Territory, the solution path a Map through it (**same structure as Rubik's
  Cube**).
- A **Frontier / exploration** concept. Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** algorithms/computer-science domain → **new-
  domain finding**. Note the **cluster**: Maze + Bubble Sort + Rubik's Cube now
  give *three independent instances* pointing at algorithms / state-space search.
  That accumulating attested residue — across genuinely different exercises — is
  exactly the evidence the anti-overfitting rule wants before opening a domain or
  admitting an M2 concept. Raise it with Claude; still don't formalise prematurely.
- **Possible M2 candidate?** "Navigation of a state space toward a goal under a
  move/search rule" (shared with Rubik's Cube). Flag; require ≥6 domains.

## 6. Source documentation
References on maze generation and graph search (the Wikipedia articles "Maze
generation algorithm" and "A* search algorithm"). Attach in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Animate the generator carving passages, then animate the solver's frontier
expanding and the final path lighting up. Let the user pick the generation and
solving algorithms to compare their **Dynamics**.
