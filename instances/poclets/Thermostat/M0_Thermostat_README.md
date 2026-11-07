# Thermostat (studio flat, F1) — TSCG Instance

**Type**: Poclet · **Version**: 1.0.0 · **Created**: 2026-11-07
**Author**: Echopraxium with the collaboration of Claude AI
**Files**: [`M0_Thermostat.jsonld`](M0_Thermostat.jsonld) ·
[`M0_Thermostat_analysis.md`](M0_Thermostat_analysis.md) ·
simulation [`static/M0_Thermostat.html`](static/M0_Thermostat.html) (sources in `static/src/`)

## Overview

A one-room flat (F1) heated by a heater and a radiator, losing heat through its wall
and window, and kept near a set point by a wall thermostat with hysteresis. It is the
minimal technical **negative feedback loop**, and it shows a fact that surprises
newcomers: an on/off regulation never rests on its set point, it **oscillates** in a
sawtooth between the two edges of the hysteresis band.

This poclet is the first workshop of the **TSCG Kit** to go through the instance
pipeline. The Kit is the test airlock; a workshop that passes the pipeline lands here,
and its playable scale model becomes the poclet's simulation.

## System Description

| Block (Kit) | Generic kind (Kit) | Role |
|---|---|---|
| Room | storage | the space of the flat; its temperature is regulated |
| Radiator | storage | a smaller store between heater and room; it delays the heating |
| Heater | source | converts power into heat; on/off command |
| Wall | sink | heat leaks to the outside (more with the window open) |
| Thermostat (bimetal) | threshold | closes below the band, opens above it |

Five blocks, five wires: room → wall (heat), heater → radiator → room (heat),
room → thermostat (temperature), thermostat → heater (command).

## TSCG Analysis

### ASFID State (Territory / Eagle Eye)

| Dim. | Score | Justification |
|---|---|---|
| A | 0.85 | the set point and its hysteresis band |
| S | 0.85 | room, radiator, wall, thermostat, loop topology |
| F | 0.90 | heat flux to the outside, information flux to the command |
| It | 0.75 | one temperature, a one-bit command |
| D | 0.90 | relaxations, limit cycle, radiator delay, perturbations |

### REVOI State (Map / Sphinx Eye)

| Dim. | Score | Justification |
|---|---|---|
| R | 0.90 | the Synoptic is the block diagram |
| E | 0.80 | editable parameters; the house scenario extends it |
| V | 0.90 | curves checkable against Newton's law of cooling |
| O | 0.85 | every state variable has an instrument |
| Im | 0.70 | control theory, Schmitt trigger; three concepts missing (G1–G3) |

### Epistemic Gap

asfidMean 0.85, revoiMean 0.83, epistemicGap 0.014 → **Coherent**: the model was built
as a working scale model before being formalised.

## Components

| Component | Typed as (M2) |
|---|---|
| Room, Radiator | `Storage`, `Inertia` |
| Heater | `Transducer`, `Activation` |
| Wall and window | `Dissipation` (gap G1) |
| Outside | `Environment` |
| Inside–outside gap | `Gradient` |
| Thermostat | `Threshold`, `Memory` (gap G2) |
| Temperature, command | `Signal` |
| Regulation loop | `FeedbackLoop`, `Regulation`, `Homeostasis`, `Balance` |
| Sawtooth | `Trajectory` (gap G3) |
| Panel instruments | `Observer` |

## GenericConcepts Mobilized

Storage, Inertia, Transducer, Activation, Dissipation, Environment, Gradient,
Threshold, Memory, Signal, FeedbackLoop, Regulation, Homeostasis, Balance, Trajectory,
Observer (16).

## Key Insights

- **Regulation and oscillation are made of the same wires.** With hysteresis and no
  resting point inside the band, the negative loop draws a sawtooth. The Kit's Drinking
  bird workshop puts this oscillation in the foreground.
- **The radiator's delay causes overshoot**: a second store in series is enough.
- **Two views of one graph.** The Panel (instruments) and the Scale model (the flat)
  read and write the same graph; the Kit never names them, the player discovers the
  difference.
- **Three gaps, recorded rather than patched** (see the analysis):
  G1 the wall is a Boundary, which is not defined (WS-13);
  G2 no concept for hysteresis — candidate `Hysteresis = Fm2(Threshold, Memory)`;
  G3 the sawtooth is a relaxation oscillation, which `m1:Oscillator` does not describe.

## Transdisciplinary Analogies

Bang-bang control in engineering; the Schmitt trigger in electronics; a refrigerator,
a float valve in a cistern; hormonal on/off switches; any regulation with a dead band.

## References

- TSCG Kit — `kit/` (workshops, shared libraries, map of scenarios)
- WS-13 Phase 0 and Addendum A — `ontology/docs/_01_Worksite/WS-13/`
- Newton's law of cooling; on/off (bang-bang) control with hysteresis
