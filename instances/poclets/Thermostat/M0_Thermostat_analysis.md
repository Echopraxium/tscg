# TSCG Analysis — Thermostat (studio flat, F1)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-11-07
**Pipeline**: `tscg-instance-pipeline` — Step 1 (Proposition) and Step 2 (Analysis)
**Source**: TSCG Kit workshop `kit/thermostat/` (Kit 0.9.2) — first kit to go through the
pipeline: the kit is the test airlock, the poclet is where a validated kit lands
**Measured on**: HEAD `40e33d5` (formulas below read from `M2_GenericConcepts.jsonld` /
`M1_CoreConcepts.jsonld` at that commit)

---

## Step 1 — Proposition

**System**: a studio flat (one single room, F1) heated by a heater and a radiator,
losing heat through its wall and window to the outside, and regulated by a wall
thermostat with a set point and a hysteresis (on/off control).

**Classification: 🟢 Valid instance.** Five active ASFID dimensions, a closed negative
feedback loop, two time scales (radiator, room), an external perturbation (window,
outside temperature) and an emergent limit cycle (sawtooth). Small enough to be complete
(5 blocks, 5 wires), rich enough to mobilise about fifteen GenericConcepts. It already
exists as a playable, tested scale model (the kit), which is unusual for a poclet.

## Verdict: ⚠️ Gap (three precise holes, no refutation)

## ASFID Lens

- **A (Attractor)**: the set point of the thermostat, and the hysteresis band around it
  (`set ± h/2`); the room temperature is pulled toward it but never rests on it.
- **S (Structure)**: the room (thermal capacity), the radiator (capacity in series),
  the wall (conductance, plus the window that can open), the thermostat (contact with
  hysteresis), and the topology of the loop (room → thermostat → heater → radiator → room).
- **F (Flow)**: heat flux heater → radiator → room → wall → outside; an information
  flux temperature → thermostat → on/off command.
- **I (Information)**: the measured temperature, the 1-bit command, the set point;
  the panel instruments (thermometers, lamp, slider) read and write them.
- **D (Dynamics)**: exponential heating and cooling with time constants C/k, the
  sawtooth limit cycle of on/off control, the delay added by the radiator (overshoot),
  perturbations (window opened, colder outside).

## Anticipated M2 GenericConcepts (formulas at HEAD)

| Kit element | GenericConcept | Formula | Role |
|---|---|---|---|
| Room, Radiator | `m2:Storage` | `St × F` | accumulate heat |
| Room, Radiator | `m2:Inertia` | `St × F × It × D` | thermal inertia; the radiator's delay causes overshoot |
| Heater | `m2:Transducer` | `F × St × It` | converts electric power (or gas) into heat |
| Heater on/off | `m2:Activation` | `A × D \| _^` / `_$` | the command enables or blocks the heat flow |
| Wall (losses) | `m2:Dissipation` | `F × D` | heat degraded toward the outside |
| Outside | `m2:Environment` | `F × It` | the cold the room exchanges with |
| Room − outside | `m2:Gradient` | `F × T` | the temperature gap drives the losses |
| Thermostat | `m2:Threshold` | `A × It` | switches the heater around the set point |
| Thermostat (band) | `m2:Memory` | `∫(D−F)dτ` | hysteresis: the state depends on where it came from |
| Information wires | `m2:Signal` | `It × F` | temperature and command |
| Whole loop | `m2:FeedbackLoop` | `m2:Process × m2:Alignment × m2:Homeostasis` | negative loop |
| Whole loop | `m2:Regulation` | `A × St × F` | keeps the room within a range |
| Whole loop | `m2:Homeostasis` | `A × St × F \| L` | stable temperature despite perturbations |
| Mean regime | `m2:Balance` | `A × St × F \| _0` | on average, heating compensates the losses |
| Curve | `m2:Trajectory` | `A × D × F` | the temperature path, the sawtooth |
| Thermometers, panel | `m2:Observer` | `It × A` | measurement and reading |

M1: `m1:Oscillator` (`Fm2(Component, Process, Trajectory) | trajectoryShape=Circular`)
for the sawtooth — see Gap G3. Domain: Physics (thermodynamics); `M1_Physics` has
`Thermodynamics` as a domain class.

## Comparison with existing instances

- **BloodPressureControl**: the closest (homeostatic regulation by negative feedback),
  but continuous and biological; its M0 still names phantom M2 classes
  (`m2:Attractor`, `m2:Feedback`, `m2:Flow`, `m2:Redundancy`, `m2:Timescale`).
  The Thermostat would be the *minimal technical* counterpart, with on/off control.
- **FourStrokeEngine**: thermal flows, but a cycle driven by mechanics, not regulation.
- **Vco / Theremin**: oscillators — harmonic or electronic, not relaxation.

## Detailed Verdict — the three gaps

- **G1 — The wall is a Boundary, and `m2:Boundary` does not exist.** The wall (and the
  window that opens) separates the system from its environment and modulates the heat
  flow. `m2:Dissipation` types what crosses it, not the wall itself. `m2:Boundary` is a
  known phantom (WS-5 lot-NSRESOLVE, WS-13 D9 / Addendum A DA3). The window is
  `m1:Permeability`, whose formula still uses the phantom `m2:Interface`.
- **G2 — No concept for hysteresis.** A threshold whose switching value depends on
  the direction of travel is `Threshold` + `Memory`. Candidate M1 combo:
  `m1:Hysteresis = Fm2(Threshold, Memory)` — transdisciplinary (magnetism, thermostats,
  Schmitt triggers, the drinking bird's tilt, labour markets). To go through
  `tscg-m2-candidate-filter` (or straight to M1 as a combo: decomposable by construction).
- **G3 — The sawtooth is a relaxation oscillation; `m1:Oscillator` describes a
  harmonic one.** Its comment (return around an attractor, damping ratio) and its guard
  `| trajectoryShape=Circular` fit a pendulum, not an on/off limit cycle. The guard is
  also an SC-1 violation already listed by the M1 report (GCC009, repair in SC-6).

Observation (not a gap of this instance): the formula of `m2:FeedbackLoop` is written
with concept names joined by `×` (`m2:Process × m2:Alignment × m2:Homeostasis`), whereas
every other atom uses primitives. Logged for the friction log.

## Recommended Decision

**Discuss** (sync point), then continue to Step 3 with one of:

1. **Model now, gaps visible**: type the wall with `m2:Dissipation` + `m2:Environment`,
   the thermostat with `m2:Threshold` + `m2:Memory`, the curve with `m2:Trajectory`;
   record G1–G3 in the M0's `validation` section and in the kit friction log.
2. **Wait for WS-13 L1a** (Boundary) and the Hysteresis candidate, then model.

Proposed name and place: `instances/poclets/Thermostat/` (`M0_Thermostat.jsonld`,
`M0_Thermostat_README.md`, this analysis, and the kit page as its simulation).
