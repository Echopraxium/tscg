# Finite Element Simulation of Plate Tectonics – Realistic Deformations

## Overview
This document summarizes realistic deformation regimes for a **prismatic-element FEM** simulating the lithosphere, mantle, and magma. Suitable for geodynamic models at geological time scales (Myr).

## Deformation by Layer

### 1. Plate (Lithosphere)
- **Elastic** – Flexure at ridges, subduction zones, topographic loading.  
  Small strains (\(10^{-6}\)–\(10^{-4}\)).
- **Plastic (brittle)** – Faulting in the upper brittle part (0–15 km crust, up to 40 km cold mantle). Requires localization techniques.
- **Viscous (ductile)** – Dislocation creep below ~600–700 °C (lower lithosphere).  
  Viscosity depends on temperature and stress.

### 2. Mantle (Asthenosphere + Lower Mantle)
- **Dominant regime**: Non‑Newtonian viscous flow (power‑law creep, \(n \approx 3\)).
- **Realistic strain types**:
  - Simple shear (basal drag under plates)
  - Pure shear (divergence/convergence, plume upwelling)
  - Rigid‑body rotation (within convection cells)
- **Volume change**: Negligible → enforce **incompressibility** (\(\nabla\cdot\mathbf{v}=0\)).
- **Strain rates**: \(10^{-15}\) – \(10^{-12}\) s⁻¹.
- **Constitutive law**:  
  \(\dot{\varepsilon}_{ij} = A \; \sigma_{\text{II}}^{\,n-1} \sigma_{ij} \; \exp\left(-\frac{E+PV}{RT}\right)\)  
  (diffusion creep for low stress, dislocation creep for high stress).

### 3. Magma (Partial Melt Zones)
- Not a continuous layer; localized pockets (dorsal, plumes, subduction zones).
- **Rheology**: Newtonian viscous (\(\eta \sim 10^{1}\)–\(10^{4}\) Pa·s, much lower than mantle).
- **Deformation**:
  - Darcy‑type segregation (two‑phase flow) if melt migration is modelled.
  - Simplified: locally reduced viscosity.
  - Hydraulic fracturing (dykes) is hard with standard FEM; requires cohesive elements.
- **Incompressibility** holds for pure melt; porosity changes if volume expansion upon melting is included.

## Practical FEM Advice (Prismatic Cells)
| Layer | Recommended Formulation | Key Tensor / Invariant |
|-------|------------------------|------------------------|
| Plate | Elasto‑visco‑plastic (Perzyna, Drucker‑Prager) | \(\varepsilon_{el}\), \(\varepsilon_{pl}\), \(\dot{\varepsilon}_{vis}\) |
| Mantle | Non‑Newtonian viscous, mixed velocity‑pressure (P2/P1 or stabilized) | \(\dot{\varepsilon}_{vis}\) (deviatoric), \(\nabla\cdot\mathbf{v}=0\) |
| Magma | Newtonian viscous; optional two‑phase (porosity) | \(\dot{\varepsilon}_{vis}\) (Newtonian), trace (if porosity evolves) |

- **Element choice**: Quadratic velocities (P2) + linear pressure (P1) to avoid volumetric locking.
- **Strain localisation** (faults, shear bands) requires enrichment (e.g., strong discontinuities, regularisation).
- **Time scale**: Elastic strains are negligible for long‑term plate motion (except for seismic/flexure studies).

## Summary Table

| Component | Dominant Deformation | Key Characteristics |
|-----------|----------------------|----------------------|
| Plate | Elastic + Plastic (brittle) + Viscous (ductile) | Layered behaviour; flexure, faulting, creep |
| Mantle | Viscous, non‑Newtonian, incompressible | Convection, slab pull, ridge push |
| Magma | Viscous, Newtonian, localised | Melt segregation, low viscosity, two‑phase flow |

> **Note**: The mantle deforms viscously, enabling plate motion, but the primary driving force is **slab pull** (weight of subducting plate) and **ridge push**, not basal traction alone.