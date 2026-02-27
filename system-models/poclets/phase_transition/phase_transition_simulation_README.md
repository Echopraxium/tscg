# Phase Transition Simulation

**TSCG M0 Poclet Simulation — Solid / Liquid / Gas**  
Author: Echopraxium with the collaboration of Claude AI  
Version: 1.6.0 — 2026-02-26

---

## Overview

Interactive simulation of phase transitions for seven reference substances. Driven by the `M0_PhaseTransition` TSCG poclet, it combines real thermodynamic physics (Ideal Gas Law, Clausius-Clapeyron, Gibbs Phase Rule) with physically-inspired particle animations for each of the three phases.

---

## Requirements

```bash
pip install pygame
python phase_transition_sim.py
```

Python 3.9+ and `pygame` are the only dependencies.

---

## Layout (1440 × 820 px)

```
┌──────────────────┬───────────────────┬────────────────────┐
│   LEFT  (370 px) │  CENTER  (530 px) │   RIGHT  (540 px)  │
│                  │                   │                    │
│ Substance tabs   │  GAS  layer       │  Properties panel  │
│ [SOLID][LIQ][GAS]│  LIQUID layer     │  Phase diagram     │
│ T slider         │  SOLID layer      │  Ideal Gas Law     │
│ P slider (Pa)    │                   │  Clausius-Clapeyron│
│ V slider (m³)    │  ← click to snap  │  ASFID / REVOI     │
└──────────────────┴───────────────────┴────────────────────┘
```

---

## Controls

| Control | Action |
|---|---|
| Substance tabs (7 buttons) | Select the reference substance |
| `[SOLID]` `[LIQUID]` `[GAS]` | Snap T, P, V to canonical phase values |
| Click a phase layer (centre panel) | Same as state buttons |
| **T slider** | Temperature (°C) — range adapts to selected substance |
| **P slider** | Pressure (Pa, logarithmic scale) |
| **V slider** | Volume (m³, logarithmic scale) — isothermal coupling with P |
| `ESC` | Quit |

### T / P / V coupling

The three sliders are coupled via the Ideal Gas Law (n = 1 mol, isothermal):

```
V = nRT / P
```

Moving **P** recalculates **V** at constant T, and moving **V** recalculates **P** at constant T.  
Moving **T** recalculates **V** at current P.

---

## Reference Substances

| Substance | Formula | mp (°C) | bp (°C) | Colour | Notable property |
|---|---|---|---|---|---|
| **Methanol** | CH₃OH | −97.6 | 64.6 | Light grey | Highly toxic; colourless |
| **Water** | H₂O | 0.0 | 100.0 | Light blue | Anomalous: dTm/dP < 0 |
| **Gallium** | Ga | 29.8 | 2402.9 | Silver metallic | Melts in the hand; widest liquid range (2373 K) |
| **Sulfur** | S₈ | 112.8 | 444.6 | Vivid yellow | Viscosity max ~160 °C (polymerisation) |
| **Iodine** | I₂ | 113.7 | 184.4 | Deep violet | Sublimates visibly at 1 atm |
| **Camphor** | C₁₀H₁₆O | 175.0 | 204.0 | Ivory | Very strong sublimation; narrow 29 °C liquid range |
| **Dichloromethane** | CH₂Cl₂ | −96.7 | 39.6 | Pale grey-blue | Very low bp; suspected carcinogen |

The **T slider range** adapts automatically to each substance: `[mp − 50 °C … bp + 150 °C]`.

---

## Physics

### 1. Phase determination

```
T < Tm(P)          → SOLID
P < P_tp           → GAS   (sublimation: no liquid phase)
Tm(P) ≤ T < Tb(P)  → LIQUID
T ≥ Tb(P)          → GAS
```

### 2. Clausius-Clapeyron — boiling point vs pressure

```
ln(P₂/P₁) = (ΔHvap / R) × (1/T₁ − 1/T₂)
```

Used to compute `Tb(P)` from the reference boiling point at 1 atm.

### 3. Melting point vs pressure (linear Clapeyron)

```
Tm(P) = Tm(1 atm) + (dTm/dP) × (P_atm − 1)
```

Water uses a negative slope (−0.0075 K/atm), matching the anomalous behaviour observed experimentally.

### 4. Ideal Gas Law

```
pV = nRT     (n = 1 mol, R = 8.314 J mol⁻¹ K⁻¹)
```

### 5. Gibbs Phase Rule

```
F = C − P + 2
```

For a pure substance (C = 1): 1 phase → F = 2, two-phase coexistence → F = 1, triple point → F = 0.

---

## Particle Animations

All animations run only in the **active phase** layer (the one currently occupied by the substance at the selected T and P).

### Solid — thermal lattice vibrations

Particles sit on a regular 9 × 8 grid (72 particles). Each particle oscillates around its rest position with **independent phases** on x and y:

```
x(t) = x₀ + A × sin(ωx × t + φx)
y(t) = y₀ + A × cos(ωy × t + φy)
```

The amplitude A is proportional to temperature:

```
A = clamp(T/Tm × 1.20,  0.10,  1.28)   [pixels]
```

Near absolute zero the lattice is nearly static; near the melting point it quivers visibly.

**Stable bonds** (solid lines) are pre-computed between every pair of adjacent grid neighbours (right + down). 127 permanent bonds for 72 particles. They vibrate with their particles.

### Liquid — incompressible turbulent flow

123 particles advect through a time-varying, **analytically divergence-free** velocity field derived from a stream-function sum of three modes:

```
ψ(x, y, t) = Σk Ak × sin(fxk x + ωxk t) × sin(fyk y + ωyk t)

vx =  ∂ψ/∂y   (divergence-free by construction)
vy = −∂ψ/∂x
```

The three modes have different spatial scales (~350, ~150, ~80 px wavelength) producing organic vortex-like swirling flow. Divergence is analytically zero (verified numerically to < 10⁻¹²).

**Anti-clustering forces** maintain a uniform particle distribution:
- Wall repulsion: proportional kick away from each nearby edge (within `width/14`)
- Centrifugal nudge: gentle outward push within 22 % of the panel centre
- All forces are **low-pass filtered** (two cascaded stages, α = 0.03 and α = 0.12) so velocity changes are always smooth — no sudden jumps

**Particle-particle repulsion** (soft sphere): pairs within 20 px are pushed apart symmetrically, preventing visual superposition.

**Elastic boundary reflection** with hard clamp ensures no particle can leave the zone.

**Transient bonds** (dashed lines) form and dissolve dynamically:
- A bond appears when two particles come within `width/13` (≈ 40 px)
- It is **immediately destroyed** if the distance exceeds `width/12` (≈ 43 px)
- Each particle can participate in at most **4 bonds** simultaneously
- Bond opacity is proportional to its lifetime [0, 1]

### Gas — Langevin / Brownian dynamics

36 particles follow Langevin equations:

```
v(t + dt) = v(t) × (1 − γ + γ × v₀/|v|) + ξ
```

where `ξ ~ N(0, σ)` is a Gaussian random kick (σ = 0.83 px/frame), γ = 0.04 is damping, and v₀ = 3.3 px/frame is the soft target speed. The result is the characteristic jittery, directionless random walk of gas molecules with elastic wall reflections.

---

## Particle Count Summary

| Phase | Particles | Bonds |
|---|---|---|
| Solid | 72 | 127 permanent (grid) |
| Liquid | 123 | Transient, ≤ 4 per particle |
| Gas | 36 | None |

---

## Right Panel — Properties

For the selected substance at current T, P, V:

- Phase diagram data: mp, bp, critical point, triple point, ΔHvap, ΔHfus
- Ideal Gas Law calculator: V = nRT/P for n = 1 mol
- Clausius-Clapeyron table: bp at 5 reference pressures (0.01, 0.1, 1, 10, 100 atm)
- Gibbs Phase Rule explanation
- ASFID scores (Attractor, Structure, Flow, Information, Dynamics)
- REVOI scores (Representability, Evolvability, Verifiability, Observability, Interoperability)

---

## TSCG Integration

This simulation is the executable form of the `M0_PhaseTransition` poclet in the TSCG (Transdisciplinary System Construction Game) framework. It serves as:

1. **Proof-of-concept** for the TSCG modelling methodology
2. **Validation** of ASFID/REVOI scoring on a well-understood physical system
3. **Pedagogical tool** for exploring phase behaviour across seven substances

The poclet ontology (`M0_PhaseTransition.jsonld`) encodes the same physics in JSON-LD / OWL format, making it machine-readable and interoperable with the broader TSCG ontology graph.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-24 | Initial release: 4 phases, 7 substances |
| 1.1.0 | 2026-02-25 | Simplified to 3 phases (removed plasma) |
| 1.2.0 | 2026-02-25 | Brownian gas, stream-function liquid, thermal solid vibrations |
| 1.3.0 | 2026-02-26 | Equal phase heights; particles only in active phase; dynamic T range; click-to-switch layers |
| 1.4.0 | 2026-02-26 | Substance colours; pressure in Pa; V slider; ×1.3 particles; stable + transient bonds |
| 1.5.x | 2026-02-26 | Improved bond rules (dist-based, max 4/particle); ×1.5 gas speed; ×1.6 liquid particles; elastic boundary reflection; particle repulsion; smooth wall turbulence |
| 1.6.0 | 2026-02-26 | Double low-pass velocity filter (α = 0.03 / 0.12); eliminates all particle jumps |
