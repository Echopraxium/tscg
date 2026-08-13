# Osmosis and Reverse Osmosis — TSCG Exercise

**Domain:** Chemistry / Biology (membrane transport)
**Difficulty:** Intermediate (nice because it contains its own *reversal*)
**Natural simulation:** 2D (p5.js) — two compartments, a membrane, moving particles

## 1. The system in one paragraph
Across a **semipermeable membrane**, solvent (water) moves from the dilute side to
the concentrated side to equalise concentration — this is **osmosis**, driven by
the concentration gradient. Apply enough external pressure on the concentrated
side and you push water the *other* way, against the gradient — **reverse
osmosis** (used to desalinate water).

## 2. Suggested scope (minimal + complete)
Two compartments separated by one semipermeable membrane, with a solute
concentration difference, plus an optional applied pressure that can drive the
reverse case. Model both regimes in one poclet.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): **concentration equilibrium** — the natural end state osmosis
  moves toward (and that reverse osmosis is *forced away from*).
- **S** (Structure): **two compartments + the semipermeable membrane**.
- **F** (Flow): **solvent flux** across the membrane (either direction).
- **I** (Information): the **concentration gradient** and the **applied pressure**
  — the drivers that set flow direction.
- **D** (Dynamics): **relaxation to equilibrium** (osmosis) vs **pressure-driven
  transport** (reverse osmosis).

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Gradient** concept (the driving difference).
- A **Flow / transport** concept (solvent flux).
- An **Equilibrium / Balance** concept (the attractor state).
- Possibly a **driven-reversal / pump** concept for reverse osmosis (a system held
  *away* from its natural attractor by an external input). This last one is the
  interesting part — discuss whether it's covered or a candidate.
Verify all against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **Yes** — `chemistry` and `biology` both plausibly
  host membrane transport. Decide with Claude which is the better home (and
  whether a shared concept belongs in M1_CoreConcepts).
- **Possible M2 candidate?** "A system held away from its equilibrium by a
  sustained external drive" is a broad transdisciplinary pattern (pumps, active
  transport, refrigeration). Worth flagging if it isn't already captured.

## 6. Source documentation
An introductory reference on osmosis and reverse osmosis (a biology/chemistry
textbook section or the Wikipedia articles "Osmosis" and "Reverse osmosis").
Attach it in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Two boxes, a dashed membrane, solute dots on one side and water dots that cross;
a slider for the concentration difference and one for applied pressure. When
pressure exceeds the osmotic pressure, the net flow visibly reverses — the moment
the system is pushed off its **Attractor**.
