# Logic Gates — TSCG Exercise

**Domain:** Digital electronics / Boolean logic
**Difficulty:** Starter
**Natural simulation:** 2D (p5.js) — a gate diagram beside a live truth table

> A great first poclet: it is small, fully deterministic, and every claim it
> makes can be **checked by hand** against a truth table. That makes it the
> cleanest possible test of the modelling loop.

## 1. The system in one paragraph

A **logic circuit** is an arrangement of **logic gates** (AND, OR, NOT, NAND,
NOR, XOR, XNOR) that turns binary inputs (0/1) into a binary output according to
a **Boolean expression**. Every circuit has an equivalent **truth table** listing
the output for all `2^n` input combinations, and every truth table can be turned
back into a circuit — the three are three views of one thing: circuit ↔
expression ↔ table.

## 2. Suggested scope (minimal + complete)

Don't model "logic gates" in the abstract. Model **one small combinational
circuit** end to end. The recommended one is the **storage-room security alarm**
from the source material, because it uses three inputs and three gate types and
still fits on one page:

> The alarm sounds if there is **motion (M)** *or* the **door is open (D)** — but
> **not** if the **correct code (C)** is entered.
>
> **Expression:** `Alarm = (M OR D) AND (NOT C)`

That single expression, its gates, and its 8-row truth table are your poclet.
(A simpler fallback is a lone **XOR** gate: "light on if dark *or* occupied, but
not both".)

## 3. ASFID sketch (Territory / Eagle Eye)

- **A** (Attractor): the **specified output behaviour** — the circuit settles to
  exactly the truth-table value for each input; there is no other stable output.
- **S** (Structure): the **gates and wiring** — an OR gate (M, D), a NOT gate (C),
  and an AND gate combining them, with intermediate signals labelled.
- **F** (Flow): **signals propagating** from inputs through gates to the output.
- **I** (Information): the **input bits** M, D, C and the **logic rules** each
  gate enforces — this is almost pure Information; the circuit *is* a rule.
- **D** (Dynamics): the (near-instant) **combinational update** — change an input,
  the output re-settles. Minimal but present.

> Watch this one: Logic Gates is **Information-dominant** and has very light
> Dynamics. That imbalance is itself interesting to discuss in Analysis — it is
> a legitimate, honest shape for a poclet, not a defect.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)

These are *guesses to test*, not settled formulas. Verify names and formulas
against `M2_GenericConcepts.jsonld` at HEAD during Analysis:

- A **mapping / function** concept: input combinations → output (the truth table
  as a total function).
- A **composition** concept: gates composed into a larger circuit.
- Possibly a **threshold / gate** concept: each gate as a Boolean decision.
- Possibly a **transformation** concept: expression ↔ circuit ↔ table as three
  representations of one relation (a nice **Map/Territory** angle).

## 5. Domain question

- **Existing M1 extension?** **Yes — `electronics`** (`M1_extensions/electronics/`).
  Check whether it already carries digital-logic concepts (gate, Boolean signal);
  if not, this poclet may *enrich* it with a `LogicGate` / `BooleanSignal` concept.
- **Possible M2 candidate?** Probably not on its own — Boolean composition is
  likely expressible with existing concepts. But if a "discrete rule table /
  total function over a finite input space" pattern recurs across domains, flag
  it. Let Analysis decide.

## 6. Source documentation

Primary reference: **Computer Science Cafe — "Boolean Logic Circuits (CIE)"**,
<https://www.computersciencecafe.com/10-boolean-logic-circuits-cie.html>
(a copy of the page text is included in this folder as `source_boolean_logic.md`).
It defines problem statements, logic expressions, circuits and truth tables, and
walks through worked examples including the security-alarm circuit above.

## 7. Simulation hint (2D, p5.js)

Draw the gate diagram (OR, NOT, AND) with the three inputs as toggles the user
can flip. As the user flips M/D/C, animate the signals lighting up along the
wires and highlight the matching row in a live-rendered truth table. The
**Attractor** reads visually as "the output snaps to the table value"; the
**Information** dominance reads as "structure barely moves, the rule does all the
work". Keep it 2D — there is no spatial third dimension to earn a 3D view.
