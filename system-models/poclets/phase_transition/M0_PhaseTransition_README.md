# M0_PhaseTransition — TSCG Poclet README

**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** 1.1.0  
**Date:** 2026-02-26  
**Domain:** Physical Chemistry / Thermodynamics  
**Ontology file:** `M0_PhaseTransition.jsonld`  
**Simulation:** `phase_transition_sim.py`

---

## 1. Overview

The **Phase Transition** poclet models the four fundamental states of matter — **Solid, Liquid, Gas** — and the transitions between them, driven by two control parameters: **Temperature (T)** and **Pressure (P)**.

This poclet is a canonical example of:
- **Multi-attractor systems** (4 stable phase basins in Gibbs energy landscape)
- **First-order phase transitions** (discrete jumps in density, entropy, latent heat)
- **Second-order / continuous transitions** (liquid-gas supercritical region near critical point)
- **The Ideal Gas Law** as a governing analytical model: **pV = nRT**

---

## 2. Governing Physics

### 2.1 Ideal Gas Law

For the **gas phase**, the primary governing equation is:

```
pV = nRT
```

| Symbol | Meaning | Unit |
|--------|---------|------|
| p | Pressure | Pa |
| V | Volume | m³ |
| n | Amount of substance | mol |
| R | Universal gas constant = 8.314 | J·mol⁻¹·K⁻¹ |
| T | Temperature | K |

The volume occupied by `n` moles at given `T` and `p`:

```
V = nRT / p
```

For real gases, van der Waals equation corrects for molecular volume and interactions:

```
(p + a·n²/V²)(V − nb) = nRT
```

### 2.2 Clausius-Clapeyron Equation

The slope of each phase boundary in the P-T diagram:

```
dP/dT = L / (T · ΔV)
```

where `L` is the molar latent heat and `ΔV` is the molar volume change.

For the liquid-gas boundary (ideal gas approximation):

```
ln(P) = −L_vap / (R·T) + const
```

### 2.3 Gibbs Phase Rule

```
F = C − P + 2
```

| Term | Meaning |
|------|---------|
| F | Degrees of freedom (number of independent variables) |
| C | Number of chemical components |
| P | Number of coexisting phases |

For a **single-component** system (C=1):
- 1 phase: F = 2 (T and P both free)
- 2 phases (coexistence curve): F = 1 (only one free variable)
- 3 phases (triple point): F = 0 (invariant — unique T, P)

### 2.4 Saha Equation (Gas → Plasma)

Ionization equilibrium in the plasma transition:

```
n_e · n_i / n_a = (2π·m_e·k_B·T)^(3/2) / h³ · (g_i/g_a) · exp(−χ/k_B·T)
```

where `χ` is the ionization energy, `n_e`, `n_i`, `n_a` are number densities of electrons, ions, and neutral atoms.

---

## 3. The Four Phases

| Phase | Layer | Order | Entropy | Ideal Gas Law |
|-------|-------|-------|---------|---------------|
| **Solid** | Bottom (layer 0) | Crystalline (long-range) | Lowest | Not applicable |
| **Liquid** | Layer 1 | Short-range only | Medium | Via vapor pressure (Clausius-Clapeyron) |
| **Gas** | Layer 2 | None | High | **pV = nRT** (directly) |
| **Plasma** | Top (layer 3) | None (ionized) | Highest | Saha equation |

### Phase Color Codes
- Solid: `#3A5F8A` (dark blue)
- Liquid: `#2E86C1` (ocean blue)
- Gas: `#85C1E9` (sky blue)
- Plasma: `#A569BD` (purple)

---

## 4. Phase Transitions

| Transition | Direction | Type | Latent Heat |
|-----------|-----------|------|-------------|
| Melting / Freezing | Solid ↔ Liquid | First-order | L_fus |
| Vaporization / Condensation | Liquid ↔ Gas | First-order (below Tc) | L_vap |
| Sublimation / Deposition | Solid ↔ Gas | First-order | L_sub = L_fus + L_vap |
| Ionization / Recombination | Gas ↔ Plasma | Continuous (Saha) | χ (ionization energy) |

### Special Points

| Point | Definition | Water reference |
|-------|-----------|-----------------|
| **Triple Point** | S + L + G coexist; F = 0 | 273.16 K / 611.73 Pa |
| **Critical Point** | L-G boundary vanishes; supercritical fluid above | 647.1 K / 217.7 atm |

---

## 5. Reference Substances

Seven substances were selected to illustrate diverse phase transition behaviors:

### 5.1 Water (H₂O)
- **Melting:** 273.15 K (0°C) | **Boiling:** 373.15 K (100°C) at 1 atm
- **Triple point:** 273.16 K / 611.73 Pa
- **Critical point:** 647.1 K / 217.7 atm
- ⚠️ **Anomaly:** Negative melting curve slope (ice less dense than liquid water); density maximum at 277 K

### 5.2 Methanol (CH₃OH)
- **Melting:** 175.6 K (−97.6°C) | **Boiling:** 337.8 K (64.7°C)
- **Triple point:** 175.6 K / 0.187 Pa (very low — sublimes under even mild vacuum)
- ✅ Useful antifreeze example; wide liquid range

### 5.3 Gallium (Ga)
- **Melting:** 302.9 K (29.8°C) — melts in hand! | **Boiling:** 2477 K (2204°C)
- **Triple point:** 302.9146 K (ITS-90 fixed point)
- ⚠️ **Anomaly:** Expands on solidification; widest liquid range of metals (2174 K)

### 5.4 Sulfur (S)
- **Melting:** 388.4 K (115.2°C) | **Boiling:** 717.8 K (444.7°C)
- **Triple point:** 388.4 K / 21.3 kPa
- ⚠️ **Anomaly:** Two stable allotropes (α-S rhombic / β-S monoclinic); viscosity maximum near 430 K (S₈ ring polymerization)

### 5.5 Iodine (I₂)
- **Melting:** 386.9 K (113.8°C) | **Boiling:** 457.6 K (184.5°C)
- **Triple point:** 386.65 K / 11.7 kPa
- ⚠️ **Anomaly:** Triple point pressure (11.7 kPa) > standard vapor pressure at RT → sublimes visibly at room temperature; produces **violet vapor**
- Classic sublimation demonstration

### 5.6 Camphor (C₁₀H₁₆O)
- **Melting:** 452 K (179°C) | **Boiling:** 477 K (204°C)
- **Triple point:** 451.5 K / 6.6 kPa
- ⚠️ Very narrow liquid range (~25 K); sublimes at room temperature
- ✅ Cryoscopy calibrant (k_f = 5.5 K·mol⁻¹·kg⁻¹); Beckmann thermometer calibration

### 5.7 Dichloromethane (CH₂Cl₂)
- **Melting:** 176 K (−97°C) | **Boiling:** 312.7 K (39.6°C)
- **Triple point:** 176 K / 3.5 Pa
- ✅ Low boiling point; high vapor pressure at room temperature (47 kPa at 20°C); dense liquid (1.325 g/mL)
- Classic laboratory solvent for extraction and chromatography

---

## 6. TSCG ASFID Analysis

| Dimension | Phase Transition Manifestation | Score |
|-----------|-------------------------------|-------|
| **A — Attractor** | 4 stable Gibbs energy basins in (T,P) space | 0.90 |
| **S — Structure** | Crystalline → amorphous → disordered → ionized | 0.88 |
| **F — Flow** | Latent heat flows; ideal gas compressible flow | 0.85 |
| **I — Information** | Entropy as thermodynamic information; Boltzmann S = k_B ln(Ω) | 0.82 |
| **D — Dynamics** | Nucleation/growth kinetics; Maxwell-Boltzmann distribution | 0.87 |
| **ASFID Total** | | **0.86** |

### Key Tensor Formula
```
Phase Stability = A ⊗ D  (Attractor stability as balance of order and thermal energy)
Phase Transition = F ⊗ D  (Heat flow driving state change)
Structural Order = S ⊗ I  (Encoded structural information)
```

---

## 7. TSCG REVOI Analysis

| Dimension | Phase Transition Manifestation | Score |
|-----------|-------------------------------|-------|
| **R — Representability** | P-T phase diagram: complete 2D encoding of all phase regions | 0.92 |
| **E — Evolvability** | Extensible to binary systems, quantum phases, non-equilibrium | 0.78 |
| **V — Verifiability** | DSC, X-ray diffraction, PVT apparatus; pV=nRT < 1% error | 0.95 |
| **O — Observability** | Direct: color, opacity, density jump, latent heat plateau | 0.90 |
| **I — Interoperability** | Universally applicable: chemistry, astrophysics, geology, biology | 0.85 |
| **REVOI Total** | | **0.88** |

**Epistemic Gap (ΔΘ):** 0.12 (very low — well-constrained system)

---

## 8. Mobilized Metaconcepts

The Phase Transition poclet activates the following M2 metaconcepts:

| Metaconcept | Role in Phase Transition |
|------------|--------------------------|
| **m2:Attractor** | 4 Gibbs energy minima as stable attractors |
| **m2:Threshold** | Melting/boiling/sublimation/ionization boundaries |
| **m2:Bifurcation** | Phase boundaries as topological bifurcations |
| **m2:Equilibrium** | Thermodynamic equilibrium within each phase region |
| **m2:Emergence** | Macroscopic properties (viscosity, conductivity) from microscopic structure |
| **m2:Flow** | Latent heat flows; particle flows during evaporation |
| **m2:Dynamics** | Nucleation/growth kinetics; Maxwell-Boltzmann distribution |
| **m2:Order** | Crystalline order parameter; symmetry breaking at transitions |
| **m2:Boundary** | Coexistence curves defining phase region limits |
| **m2:Hierarchy** | Energy hierarchy: ΔH_fus ≪ ΔH_vap ≪ ΔH_ion |
| **m2:Constraint** | Gibbs phase rule constraining degrees of freedom |
| **m2:Symmetry** | Symmetry breaking at phase transitions (crystal symmetry groups) |

---

## 9. Cross-Domain Interoperability

The phase transition model applies universally:

| Domain | Phase Transition Application |
|--------|------------------------------|
| **Geophysics** | Mantle transitions: olivine → spinel → perovskite (pressure-driven) |
| **Astrophysics** | Stellar plasma phases; neutron star matter; quark-gluon plasma |
| **Materials Science** | Iron-carbon diagram (ferrite/austenite/cementite/martensite) |
| **Atmospheric Science** | Cloud formation (water condensation/ice nucleation); precipitation |
| **Cryogenics** | Helium superfluid lambda transition at 2.17 K |
| **Biology** | Lipid bilayer phase transitions (gel → fluid); protein folding |

---

## 10. Simulation: `phase_transition_sim.py`

### Layout (1280 × 760 px)

```
┌──────────────────┬────────────────────────────┬──────────────────────┐
│    LEFT (300px)  │     CENTER (500px)          │    RIGHT (480px)     │
│                  │                             │                      │
│  Substance       │  ┌─────────────────────┐   │  ASFID Scores        │
│  Selector        │  │  PLASMA  (layer 3)  │   │  REVOI Scores        │
│                  │  │  GAS     (layer 2)  │   │  Epistemic Gap       │
│  [SOLID] [LIQ]   │  │  LIQUID  (layer 1)  │   │                      │
│  [GAS]  [PLSM]   │  │  SOLID   (layer 0)  │   │  Ideal Gas Law       │
│                  │  └─────────────────────┘   │  pV = nRT calc       │
│  T slider        │                             │                      │
│  P slider        │  Phase Diagram (P-T plot)  │  Substance data      │
│                  │                             │                      │
└──────────────────┴────────────────────────────┴──────────────────────┘
```

### Controls

| Control | Action |
|---------|--------|
| **Temperature slider** | Adjust T (K) in substance-appropriate range |
| **Pressure slider** | Adjust P (atm) from 0.001 to 500 atm |
| **[SOLID]** button | Jump T,P to solid region |
| **[LIQUID]** button | Jump T,P to liquid region |
| **[GAS]** button | Jump T,P to gas region |
| **[PLASMA]** button | Jump T,P to plasma region |
| **Substance selector** | Switch between 7 reference substances |
| **ESC** | Quit |

### Running the Simulation

```bash
pip install pygame
python phase_transition_sim.py
```

---

## 11. File Structure

```
system-models/poclets/phase_transition/
├── M0_PhaseTransition.jsonld       ← Ontology (this file)
├── M0_PhaseTransition_README.md    ← This documentation
└── phase_transition_sim.py         ← Pygame simulation
```
