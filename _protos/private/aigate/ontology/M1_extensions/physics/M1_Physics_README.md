# M1_Physics — TSCG Physics Domain Extension

**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** 1.0.0  
**Date:** 2026-02-26  
**Domain:** Physics / Thermodynamics  
**Ontology file:** `M1_Physics.jsonld`  
**Bootstrap source:** M0_PhaseTransition v1.1.0

---

## 1. Overview

`M1_Physics.jsonld` is the domain extension for the **Physics** knowledge field in the TSCG framework. It belongs to the M1 layer: domain-specific concepts that are reusable within a disciplinary family but do not achieve the universal applicability required for M2 metaconcept status.

**Version 1.0.0** contains **6 seed concepts** derived from the systematic analysis of the `M0_PhaseTransition` poclet. Each concept is grounded in M2 metaconcepts via tensor product formulas.

```
M3 (Genesis Space — ASFID / REVOI)
    ↕
M2 (Metaconcepts — universal patterns: Attractor, Threshold, Switch, ...)
    ↕
M1_Physics (Physics-specific: LatentHeat, TriplePoint, CriticalPoint, ...)    ← this file
    ↕
M0 (Poclets: M0_PhaseTransition, ...)
```

---

## 2. Concepts (v1.0.0)

### 2.1 LatentHeat

**M2 basis:** `Switch ⊗ Threshold ⊗ Flow`

Energy absorbed or released during a first-order phase transition at **constant temperature**. The word *latent* (hidden) reflects that no temperature change accompanies the transfer — the energy is entirely consumed in structural reorganization.

LatentHeat is the primary thermodynamic observable of the **Switch M2 metaconcept**: it marks a first-order transition between two Attractor basins.

| Substance | L_fus (kJ/mol) | L_vap (kJ/mol) | Ratio L_vap/L_fus |
|-----------|---------------|----------------|-------------------|
| H₂O       | 6.01          | 40.65          | 6.8               |
| CO₂       | 9.02          | 16.51          | 1.8               |
| N₂        | 0.72          | 5.57           | 7.7               |

**Hess's law:** L_sub = L_fus + L_vap (sublimation enthalpy = sum of fusion and vaporization)

**Measured by:** Differential Scanning Calorimetry (DSC)

---

### 2.2 TriplePoint

**M2 basis:** `Attractor ⊗ Polarity ⊗ Threshold`

The unique (T, P) at which all three phases coexist in thermodynamic equilibrium. By the **Gibbs phase rule** (F = C − Ph + 2), a single-component system (C=1) with three coexisting phases (Ph=3) has F=0: the triple point is **fully invariant** — both T and P are fixed by the substance itself.

The TriplePoint physically instantiates **Polarity(N=3)**: it is the only thermodynamic state where the three Attractor basins are simultaneously equal in Gibbs free energy.

| Substance  | T_tp (K) | P_tp (Pa) | Note |
|------------|----------|-----------|------|
| H₂O        | 273.16   | 611.73    | BIPM temperature reference (Kelvin scale) |
| CO₂        | 216.6    | 517,000   | P_tp > 1 atm → no liquid CO₂ at standard pressure |
| Ga         | 302.9146 | ~2 × 10⁻⁹ | ITS-90 fixed point; essentially zero pressure |
| Iodine I₂  | 386.65   | 11,700    | P_tp > standard vapor pressure → sublimes at RT |

---

### 2.3 CriticalPoint

**M2 basis:** `CriticalityRegime ⊗ Bifurcation ⊗ Threshold`

The temperature T_c and pressure P_c above which the liquid/gas distinction vanishes. The CriticalPoint ends the liquid-gas coexistence curve. At T_c, a first-order transition (with latent heat and Switch) becomes a **second-order continuous transition** (no latent heat, continuous density change, diverging correlation length).

The CriticalPoint directly validates **CriticalityRegime (M2)**:

| Region   | Transition type | Switch L⇌G? | Latent heat? |
|----------|----------------|-------------|-------------|
| T < T_c  | First-order    | Yes         | Yes         |
| T = T_c  | Second-order   | Boundary    | 0           |
| T > T_c  | Continuous     | No          | 0           |

**Critical opalescence:** At T_c exactly, density fluctuations occur at all length scales → milky opacity (observable REVOI signature).

**Supercritical applications:** SC-CO₂ extraction (coffee decaffeination), supercritical water oxidation, supercritical fluid chromatography.

---

### 2.4 OrderParameter

**M2 basis:** `Information ⊗ Attractor ⊗ Structure`

A measurable quantity that is **zero in the high-symmetry phase** and **non-zero in the ordered phase**. Introduced by Landau. The OrderParameter quantifies the degree of broken symmetry — it is the quantitative fingerprint of the **SymmetryBreaking M2 candidate**.

**Landau free energy:** F = F₀ + a(T)·φ² + b·φ⁴ + ...  
The sign change of a(T) at T_c drives the transition.

| System | Order Parameter | Value (disordered) | Value (ordered) |
|--------|-----------------|--------------------|-----------------|
| Crystal | Density wave amplitude ρ_q | 0 (liquid) | > 0 (crystal) |
| Ferromagnet | Magnetization M/V | 0 (T > T_Curie) | M ≠ 0 (T < T_Curie) |
| Superconductor | Cooper pair wavefunction |ψ| | 0 (T > T_c) | > 0 (T < T_c) |
| Bose-Einstein condensate | Condensate fraction |Ψ|² | 0 (T > T_BEC) | > 0 (T < T_BEC) |

**TSCG link:** OrderParameter = 0 → high-symmetry Attractor (gas/liquid); OrderParameter > 0 → broken-symmetry Attractor (crystal). The transition between them is the SymmetryBreaking event.

---

### 2.5 PhaseDiagram

**M2 basis:** `Attractor ⊗ Threshold ⊗ Representation`

A graphical Map in state-variable space (T-P axes) showing the stability regions of each phase and the transition boundaries. The PhaseDiagram is the canonical **REVOI (Sphinx Eye / Map)** representation of the **ASFID (Eagle Eye / Territory)** attractor landscape.

```
        P (pressure)
        │
   HIGH │    SOLID
        │          ╲  melting curve
        │           ╲
        │            ╲  triple point (•)────── LIQUID ──────── critical pt (★)
        │             ╲                                             │
        │              ╲        sublimation curve                   │  supercritical
        │               ╲──────────────────────── GAS ─────────────┤
        └────────────────────────────────────────────────────────── T
```

**TSCG structural analogy:** Reading a phase diagram is the **Sphinx Eye reading the Eagle Eye's landscape**:
- Phase regions = ASFID Attractors (Eagle Eye)
- Coexistence curves = TSCG Thresholds
- Triple point = Polarity(N=3) balance point
- Critical point = CriticalityRegime boundary

**Anomalous water:** The H₂O melting curve slopes to the LEFT (negative dP/dT) — ice is less dense than liquid water. This means pressure destabilizes solid water: ice can melt under sufficient pressure. This anomaly enables ice skating and glacier flow.

---

### 2.6 Nucleation

**M2 basis:** `Switch ⊗ Threshold ⊗ Process`

The stochastic kinetic process by which a new phase **begins to form** within the parent phase. A microscopic fluctuation must overcome the **nucleation barrier** (competition between volume free energy gain and surface energy cost) to produce a stable nucleus.

**Energy of nucleus of radius r:**
```
ΔG(r) = 4πr²γ − (4/3)πr³|ΔG_v|
```
→ Critical radius: `r* = 2γ / |ΔG_v|`  
→ Nuclei with r < r* dissolve; nuclei with r > r* grow spontaneously.

**TSCG significance:** Nucleation distinguishes two aspects of **Switch**:
1. **Thermodynamic Switch threshold** — when the new phase is energetically favored (the phase diagram)  
2. **Kinetic Switch barrier** — when the transition actually occurs (nucleation theory)

These are not the same. A system can be past the Threshold but unable to Switch (metastable).

| Metastable state | Example | Mechanism |
|-----------------|---------|-----------|
| Supercooled liquid | Water at −40°C (very pure, in droplets) | No nucleation sites |
| Supersaturated solution | Sugar in candy making | High viscosity inhibits crystallization |
| Superheated liquid | Bumping in laboratory glassware | Smooth walls, no bubble nucleation sites |
| Glassy solid | Window glass, metallic glass | Extremely rapid quench, insufficient time to nucleate |

**Types:**
- **Homogeneous nucleation:** In the pure bulk. Requires large supersaturation. Rare in practice.
- **Heterogeneous nucleation:** On surfaces, impurities, defects. Lower effective barrier. Dominates in practice.
- **Seeding:** Intentional addition of nucleation sites (industrial crystallization, cloud seeding).

---

## 3. Relationship to M2 Metaconcepts

```
M2_GenericConcepts.jsonld
    ├── Attractor      ← used by: TriplePoint, CriticalPoint, PhaseDiagram, OrderParameter
    ├── Threshold      ← used by: LatentHeat, TriplePoint, CriticalPoint, PhaseDiagram, Nucleation
    ├── Switch         ← used by: LatentHeat, Nucleation
    ├── Flow           ← used by: LatentHeat
    ├── Polarity       ← used by: TriplePoint
    ├── CriticalityRegime ← used by: CriticalPoint
    ├── Bifurcation    ← used by: CriticalPoint
    ├── Information    ← used by: OrderParameter
    ├── Structure      ← used by: OrderParameter
    ├── Representation ← used by: PhaseDiagram
    └── Process        ← used by: Nucleation
```

### M2 Candidate flagged by M0_PhaseTransition

| Candidate | Formula | Domains validated | Status |
|-----------|---------|-------------------|--------|
| **SymmetryBreaking** | `Structure ⊗ Threshold ⊗ Switch` | 10 (Physics, Math, Biology, Social, Economics, ...) | M2_CANDIDATE — requires formal entry in M2_GenericConcepts.jsonld |

The **OrderParameter** concept in M1_Physics is the quantitative operationalization of SymmetryBreaking.

---

## 4. Relationship to M0 Poclets

| Poclet | Uses M1_Physics concepts |
|--------|--------------------------|
| M0_PhaseTransition v1.1.0 | LatentHeat, TriplePoint, CriticalPoint, OrderParameter, PhaseDiagram, Nucleation — **all 6** |

---

## 5. Planned Extensions (future versions)

| Version | Subdomain | Planned concepts |
|---------|-----------|-----------------|
| v1.1.0 | Statistical Mechanics | MaxwellBoltzmannDistribution, PartitionFunction, FreeEnergy, EntropyProduction |
| v1.2.0 | Classical Mechanics | ConservationLaw, HamiltonianSystem, PhaseSpace, PeriodicOrbit |
| v1.3.0 | Quantum Mechanics | WaveFunction, QuantumTunnel, EnergyLevel, DeBroglieWavelength |
| v2.0.0 | Optics | (possible merge/alignment with existing M1_Optics) |

---

## 6. File Structure

```
ontology/M1_extensions/physics/
├── M1_Physics.jsonld          ← Ontology (this file)
└── M1_Physics_README.md       ← This documentation
```

---

## 7. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-26 | Initial release — 6 concepts from M0_PhaseTransition: LatentHeat, TriplePoint, CriticalPoint, OrderParameter, PhaseDiagram, Nucleation |
