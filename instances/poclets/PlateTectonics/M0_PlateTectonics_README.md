# Finite Element Simulation of Plate Tectonics – Realistic Deformations

## Overview
This simulation uses a simplified finite‑element approach (stress diffusion) to model lithosphere‑mantle interaction.

## Deformation by Layer

### 1. Plate (Lithosphere)
- Elastic flexure at ridges and subduction zones.
- Plastic (brittle) faulting in the upper crust.
- Viscous creep in the lower lithosphere.

### 2. Mantle (Asthenosphere + Lower Mantle)
- Non‑Newtonian viscous flow (power‑law creep, n≈3).
- Incompressible flow (∇·v=0).
- Strain rates: 10⁻¹⁵ – 10⁻¹² s⁻¹.

### 3. Magma (Partial Melt Zones)
- Localised pockets (ridges, plumes, subduction zones).
- Newtonian viscosity (10¹–10⁴ Pa·s).

## Simulation Controls
- **Convection** : intensity of mantle circulation.
- **Slab density** : weight of subducting plate (slab pull).
- **Asymmetry** : preferred direction of plate motion.
- **Propagation** : stress diffusion coefficient.
- **Radius** : influence distance for neighbour coupling.

## Interaction
- **Click on a mantle cell** → injects a stress perturbation (e.g., mantle plume or magmatic intrusion).
- Stress then diffuses to neighbours according to a non‑linear viscosity law (n=3).
- Cell colour and scale reflect stress level.
- Earthquake triggers when average stress > 90%.

## Visual Feedback
- Cell colour : from orange (low stress) to red (high stress).
- Cell scaling : expands with stress.
- Fault lines : colour changes with global stress.
- Earthquake : camera shake and domino effect on buildings.

## Technical Notes
- Grid : 16×3×4 prismatic cells (doubled in length).
- Stress diffusion : non‑linear, exponent n=3.
- Forcing : slab pull (right side) + ridge push (center) + basal drag.