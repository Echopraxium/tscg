# Source — Boolean Logic Circuits (reference material)

> Reference text for the Logic Gates exercise. Adapted from
> Computer Science Cafe — "Boolean Logic Circuits (CIE)":
> <https://www.computersciencecafe.com/10-boolean-logic-circuits-cie.html>
> Truth tables normalised to 0/1. Provided so the exercise is self-contained;
> attach this file in the Proposition step.

## What is a problem statement

A problem statement defines a scenario or requirement to be solved with a
combination of logic gates. It outlines the conditions and the desired output,
which can be translated into a logical circuit.

**Example.** Design a security system for a storage room that triggers an alarm
when motion is detected inside the room, or when the door is opened without a
security code — but the alarm must not sound if the correct code is entered,
regardless of motion or door status.

## What is a logic expression

A logic (Boolean) expression specifies logic operations on logical variables,
using operators AND (·), OR (+), NOT (¬), NAND, NOR, XOR, XNOR. Variables (A, B,
C…) represent inputs/outputs; constants are 0 (false) and 1 (true). Every circuit
can be described by an expression, and every expression implemented as a circuit.

Example — a 2-input AND gate: `Y = A AND B` → `Y = A · B`.

## What is a logic circuit

A physical arrangement of logic gates performing a logical operation. It operates
on binary values (0/1), is composed of gates (AND, OR, NOT, NAND, NOR, XOR,
XNOR), performs a specific function determined by the arrangement of gates, and
can range from a single gate to millions.

## What is a truth table

A table giving the output for every combination of inputs. For `n` inputs there
are `2^n` combinations. List inputs in standard binary counting order (000, 001,
010, …) so no combination is missed. (In exams, marks are lost when inputs are
not listed in this order.)

---

## Worked example 1 — single gate (XOR)

Turn on a light when it is night-time (A) **or** the room is occupied (B), **but
not both**. This is exclusive-OR.

**Expression:** `X = A XOR B`

| A (night) | B (occupied) | X = A XOR B |
|:--:|:--:|:--:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

## Worked example 2 — three inputs (the security alarm)

Trigger the alarm if motion (M) **or** door open (D), **but not** if the correct
code (C) is entered.

- Step 1 — combine motion/door: `M OR D` (OR gate).
- Step 2 — the code override: `NOT C` (NOT gate).
- Step 3 — combine: `(M OR D) AND (NOT C)` (AND gate).

**Final expression:** `Alarm = (M OR D) AND (NOT C)`

| M | D | C | A = (M OR D) | B = (NOT C) | Alarm = A AND B |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 0 |

## Worked example 3 — combining NOR / NAND

Activate a robot function (X) when: the safety sensor (A) is **not** triggered
**or** the manual override (B) is engaged, but **not** in maintenance mode (C);
**and also** when the safety sensor **is** triggered and it is **not** in
maintenance, but not if override is disengaged.

- Part 1: `((NOT A OR B) NOR C)`
- Part 2: `((A AND C) NOR B)`
- Combine: `X = ((NOT A OR B) NOR C) NAND ((A AND C) NOR B)`

(List intermediate signals in the truth table to avoid slips.)

---

## From a truth table back to a circuit (sum-of-products)

Look only at rows where the output is 1. For each such row:
1. if an input is 0, apply NOT to it;
2. AND the inputs of that row together;
3. OR all the rows together.

Example rows with X = 1: `A=1,B=0,C=0` and `A=1,B=1,C=1`
→ `((A AND NOT B) AND NOT C) OR ((A AND B) AND C)`.

## Practice scenario (from CIE specimen)

A library lighting/security system. Lights (L) turn on if it is dark outside (D)
**or** people are present (P). The alarm (S) activates if it is dark, the library
is meant to be closed (C), but people are still inside (P).

Tasks: write the two logic expressions, build the truth table, and draw the
circuit.
