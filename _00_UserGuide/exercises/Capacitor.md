# Capacitor — TSCG Exercise

**Domain:** Electronics
**Difficulty:** Starter
**Natural simulation:** 2D (p5.js) — a charge/discharge curve with a fill gauge

## 1. The system in one paragraph
A capacitor stores charge on two plates separated by a dielectric. In an RC
circuit it **charges** toward the supply voltage and **discharges** back toward
zero, each following an exponential curve set by the time constant τ = R·C.

## 2. Suggested scope (minimal + complete)
A single **RC circuit**: one resistor, one capacitor, a supply, and a switch that
toggles charge/discharge. Model the charge/discharge behaviour, not a whole
power-supply board.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **target voltage** — supply voltage when charging, zero
  when discharging (a moving equilibrium the system approaches asymptotically).
- **S** (Structure): **plates + dielectric + resistor** in a loop.
- **F** (Flow): **current** into or out of the capacitor.
- **I** (Information): the **voltage across the capacitor** — the state variable.
- **D** (Dynamics): the **exponential approach** governed by τ = R·C.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- An **Accumulation / storage** concept (charge builds up).
- An **Equilibrium / relaxation-to-attractor** concept (asymptotic approach).
- A **Flow** concept (current). Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **Yes — `electronics`**. Check whether it already
  has capacitor / RC / time-constant concepts; if not, this poclet enriches it.
- **Possible M2 candidate?** Unlikely — "exponential relaxation to an
  equilibrium" is a common, probably-covered pattern. Let Analysis confirm.

## 6. Source documentation
A basic electronics reference on RC charging/discharging (any textbook or the
Wikipedia "RC circuit" article). Attach it in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Show V(t) tracing the exponential curve alongside a "fill level" gauge on the
capacitor; let the user set R and C (changing τ) and flip the charge/discharge
switch. The asymptote is the visible **Attractor**.
