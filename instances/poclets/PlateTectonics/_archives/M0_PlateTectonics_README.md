# M0_PlateTectonics — TSCG Poclet

**File:** `instances/poclets/PlateTectonics/M0_PlateTectonics.jsonld`
**Version:** 1.1.0 · **Date:** 2026-04-05
**Author:** Echopraxium with the collaboration of Claude AI
**Domain:** Geology / Geophysics — Geodynamics, Seismology, Volcanology, Paleoclimatology, Geohazard Science

**References:**
- Wegener A. (1912) — *Die Entstehung der Kontinente*, continental drift hypothesis
- Wilson J.T. (1963) — *A possible origin of the Hawaiian Islands*, hotspot concept
- Morgan W.J. (1968) — *Rises, Trenches, Great Faults, and Crustal Blocks*
- Vine F.J. & Matthews D.H. (1963) — *Magnetic anomalies over oceanic ridges*
- Walker J.C.G., Hays P.B., Kasting J.F. (1981) — *Long-term stabilization of Earth's surface temperature*
- Ivanova V. & Perron J.T. (2013) — *Visual Earth: Plate Tectonics*, MIT ARTEMiS / OEIT

---

## 1. System Overview

**Plate tectonics** is the governing geodynamic system of Earth's outer shell: a set of rigid lithospheric plates floating on the viscous asthenosphere, driven by mantle convection, continuously **creating** new oceanic crust at mid-ocean ridges (Accretion / Negentropy) and **destroying** it at subduction zones (Transformation / Entropy export), while releasing accumulated stress along seismic faults and maintaining gravitational balance through isostasy.

### Key physical principle — the mantle drives the plates

A critical clarification often missed in simplified models: **plates do not move by themselves**. They are passive riders driven by sub-lithospheric mantle processes:

| Driving force | Fraction | Mechanism |
|--------------|---------|-----------|
| **Slab pull** | ~70% | Subducting oceanic slab denser than surrounding mantle → negative buoyancy → pulls entire plate toward trench |
| **Mantle drag** | ~20% | Viscous coupling between convecting asthenosphere and base of lithosphere exerts traction in convection direction |
| **Ridge push** | ~10% | Elevated ridge topography + thermal expansion pushes plates laterally away from axis |

In the simulation: the **Convection slider** drives plate drift (mantle drag + ridge push). The **Slab density slider** controls slab pull (subduction angle and speed).

### Euler rotation — the correct geometry of continental drift

Plate motion is mathematically described as **rotation about a fixed Euler pole on the unit sphere** (Euler's theorem for rigid body rotation on a sphere). This is why Africa and South America separated along curved paths, not straight translations. The **Asymmetry slider** introduces differential convection that breaks bilateral symmetry, causing the continental plate to rotate — as geophysically observed.

### TSCG Synergy Formula

```
PlateTectonics = Geological ⊙ (m2:Entropy[Negentropy] ⊗ m1core:Accretion ⊗ m2:Transformation)
Compiled tensor: A ⊗ S ⊗ F ⊗ I ⊗ D   (all 5 ASFID dimensions)
```

The emergent property is the **Wilson Cycle** — a self-regulating planetary-scale engine (~500 Ma period) in which oceanic crust is perpetually created and consumed.

### Environmental significance

| Domain | Tectonic connection |
|--------|-------------------|
| **Climate** | Silicate weathering of orogenic rocks consumes CO₂ over Ma timescales — Walker-Hays-Kasting thermostat (1981) |
| **Geohazards** | Plate boundaries generate 90% of Earth's seismicity, all major tsunamis, and arc volcanism |
| **Biodiversity** | Continental drift → allopatric speciation; collisions → biotic exchange corridors |
| **Resources** | Cu, Au, Ni, Cr, Pt ore deposits concentrated at fossil plate boundaries |

---

## 2. Architecture — 5 Poles

| # | Pole | M3 dominant | Role in system |
|---|------|-------------|----------------|
| 1 | `Pole_LithosphericPlate` | Structure (S) | Mobile structural unit — passive rider on asthenosphere |
| 2 | `Pole_MidOceanRidge` | Flow + Structure (F, S) | Accretion zone — new crust created (Negentropy) |
| 3 | `Pole_SubductionZone` | Dynamics + Flow (D, F) | Transformation zone — old crust destroyed (Entropy export) |
| 4 | `Pole_MantleConvectionCell` | Flow + Dynamics (F, D) | Thermodynamic driver — converts internal heat to plate motion |
| 5 | `Pole_SeismicFault` | Information + Dynamics (I, D) | Stress accumulator and releaser — seismic cycle interface |

### The Wilson Cycle — emergent long-term behaviour (~500 Ma)

```
1. Continental rifting      → East African Rift (today)
2. Young ocean              → Red Sea (today)
3. Mature ocean             → Atlantic (today)
4. Declining ocean          → Pacific (today)
5. Terminal ocean           → Mediterranean (today)
6. Continental collision    → Himalayas (today)
7. Cratonization            → Archean cratons → back to 1
```

---

## 3. TSCG Bicephalous Analysis

### 3.1 Eagle Eye (ASFID — Territory Space)

| Dimension | Score | Interpretation |
|-----------|-------|----------------|
| **A** Attractor | **0.85** | Isostasy is the primary attractor: any crustal perturbation triggers compensatory vertical adjustment. Wilson cycle provides long-term dynamical attractor. Slightly below 1.0: ~500 Ma attractors difficult to quantify precisely. |
| **S** Structure | **0.95** | Highest score — 7 major + ~15 minor plates fully mapped by GPS and seismicity. Three boundary types exhaustively classified. |
| **F** Flow | **0.90** | Mantle convection provides continuous thermodynamic flux (~44 TW). Ridge push + slab pull drive plate motion. |
| **I** Information | **0.85** | Seismicity, GPS vectors, paleomagnetic anomaly stripes, and arc geochemistry encode system state. Slab geometry imaged by seismic tomography. |
| **D** Dynamics | **0.90** | Multi-scale: seconds (earthquake) to Ma (Wilson cycle). GPS directly measures plate velocities. |

**ASFID mean = 0.89**

### 3.2 Sphinx Eye (REVOI — Map Space)

| Dimension | Score | Interpretation |
|-----------|-------|----------------|
| **R** Representability | **0.90** | Global plate maps, GPlates model, NUVEL-1A velocity field — among the most complete scientific representations ever developed. |
| **E** Evolvability | **0.80** | Framework mature since 1970s. Active frontiers: mantle plume dynamics, flat-slab subduction, tectonic-climate feedbacks. |
| **V** Verifiability | **0.92** | GPS, paleomagnetic anomalies, and radiometric dating cross-validate fully independently. |
| **O** Observability | **0.80** | Surface processes directly observable. Mantle requires indirect inference (tomography, gravity). |
| **I** Interoperability | **0.85** | Bridges climatology, biology, oceanography, geochemistry, geohazard science. MIT ARTEMiS four-data-layer approach validates this dimension. |

**REVOI mean = 0.854**

### 3.3 Epistemic Gap

```
δ₁ = ||ASFID − REVOI|| / √5 = √0.0304 / 2.236 ≈ 0.078
SpectralClass: OnCriticalLine  [0.05, 0.15)
```

Residual gaps: (1) S vs O — plate structure perfectly known but mantle observability limited to indirect imaging; (2) A vs E — isostasy universally observed but long-term geodynamic modeling under tectonic-climate coupling remains an open frontier.

---

## 4. GenericConcepts Mobilised

### Primary (6)

| GenericConcept | Formula | Role |
|----------------|---------|------|
| `m2:Layer` | S⊗I⊗A⊗R | Lithospheric stratification (crust / lithosphere / asthenosphere / mantle) |
| `m2:Entropy` | F⊗I⊗D | Both poles active: Negentropy (ridge) + Entropy (heat export, subduction) |
| `m1core:Accretion` | S⊗F⊗I⊗D | Seafloor spreading — canonical geological validation of this M1 combo |
| `m2:Transformation` | S⊗I⊗D⊗F⊗V | Subduction — oceanic lithosphere recycled into asthenosphere |
| `m2:Equilibrium` | A⊗S⊗F | Isostasy — gravitational attractor of crustal thickness/density |
| `m2:Convection` | F⊗D⊗S | Mantle driver (Ra ~ 10⁷, vigorously convecting regime) |

### Secondary (4)

| GenericConcept | Formula | Role |
|----------------|---------|------|
| `m2:Trajectory` | A⊗D⊗F | Continental drift — Euler rotation vectors on unit sphere |
| `m2:Threshold` | I⊗A | Seismic failure — Coulomb criterion: τ ≥ μ(σₙ − Pf) + C |
| `m2:Cycle` | A⊗D | Wilson cycle — ~500 Ma periodicity |
| `m2:Bifurcation` | S⊗A⊗D | Ridge genesis — divergent boundary bifurcation |

**Total: 10 M2 GenericConcepts mobilised**

---

## 5. KnowledgeFieldConceptCombo — GeologicalAccretion

```
GeologicalAccretion = Geological ⊙ Accretion
Compiled tensor:  S ⊗ F ⊗ I ⊗ D
Parent M1 combo:  m1core:Accretion (⊗⇒(Entropy[Negentropy], Process))
```

Canonical instances: mid-ocean ridge spreading, accretionary prism, continental arc accretion, coral reef growth.

---

## 6. M1 Framework Contributions

| Layer | Contribution | Type |
|-------|-------------|------|
| **M1_CoreConcepts v2.2.0** | `m1core:Accretion` — canonical geological validation | GenericConceptCombo (validated) |
| **M1_CoreConcepts v2.2.0** | `m1core:Nucleation` — confirmed by slab partial melting threshold | GenericConceptCombo (confirmed) |
| **M1_Geology v1.0.0** | 9 KnowledgeFieldConcepts + 1 KFCCombo | Domain extension (new) |

---

## 7. Simulation — `M0_PlateTectonics.html` v2.0.0

**Engine:** BabylonJS 6.26.0 · **Type:** static HTML

### Visual design — Hybrid Block (Option C)

Inspired by geological cross-section diagrams (MIT ARTEMiS, Becker et al. 2010 Chile subduction reference, physical 3D geological models):

- **Opaque surface** with terrain (mountain + ocean)
- **Coloured side sections** — geological strata visible on all four faces: red mantle → orange asthenosphere → brown lithosphere → beige continental crust / dark oceanic crust → blue ocean
- **Magnetic anomaly stripes** on oceanic floor (alternating dark bands)
- **Semi-transparent glass walls** (alpha 0.09) — interior layers visible in 3D
- **Wireframe edges** in blue
- **12 HTML overlay labels** projected 3D→2D via `BABYLON.Vector3.Project` — geological layers + 5 pole labels + 2 plate names

### Animated elements

| Element | Animation driver |
|---------|-----------------|
| Mantle convection cells | 2 flow loops with pulsing arrows — rate from Convection slider |
| Plate drift (translation) | Left plate moves left, right plate moves right — speed from Convection slider |
| Euler rotation | Continental plate rotates about Y-axis — from Asymmetry slider |
| Ridge magma | Pulsing glow + upwelling particles — from Convection slider |
| Subduction slab | Dynamic angle change — from Slab density slider |
| Volcanic eruption | Continuous lava particle stream |
| Seismic fault | Colour gradient green → red (stress) → burst + reset on Earthquake |

### Controls

| Control | Physical meaning | Effect |
|---------|-----------------|--------|
| **Convection** (5–100%) | Mantle heat flux | Plate drift speed + ridge activity + convection arrows |
| **Slab density** (10–100%) | Oceanic plate negative buoyancy | Subduction angle + speed |
| **Asymmetry** (−1 to +1) | Bilateral convection imbalance | Euler rotation of continental plate |
| **🌋 Earthquake** | Coulomb failure event | Fault particle burst + camera shake + stress reset |
| **🌍 Wilson Cycle** | ×1Ma timescale animation | 7-stage narration in status bar |
| **🏷️ Labels** | Toggle overlay | Show/hide 12 geological labels |

---

## 8. Pedagogical Design — MIT ARTEMiS Approach

The simulation is informed by *Visual Earth: Plate Tectonics* (Ivanova & Perron 2013, MIT ARTEMiS), which demonstrated that students learn most effectively through:

1. **Data-layer specialization** — each group examines one data type only (seismicity, volcanism, seafloor age, topography), then combines expertise
2. **Hypothesis formation** — groups determine plate boundaries from data, then justify interpretations
3. **Animated theory** — Wilson Cycle and Pangaea splitting animations reinforce concepts before exploration

The four MIT data layers map directly to TSCG REVOI dimensions:

| MIT data layer | REVOI dimension | Rationale |
|---------------|----------------|-----------|
| Seismicity | **V** Verifiability | Seismic data verify fault geometry and slab position |
| Volcanism | **O** Observability | Volcanic arcs are surface observables of subduction |
| Seafloor age | **R** Representability | Magnetic anomaly stripes are the canonical representation of spreading history |
| Topography | **I** Interoperability | Topography integrates geomorphic, tectonic, and climatic processes |

---

## 9. Transdisciplinary Resonances

| Domain | Connection |
|--------|-----------|
| **Climatology** | Orogenic silicate weathering = long-term CO₂ sink; volcanic degassing = long-term source; continental positions control ocean circulation |
| **Biogeography** | Plate separation → allopatric speciation; collisions → biotic corridors (Great American Biotic Interchange ~3 Ma) |
| **Oceanography** | Plate tectonics creates/destroys ocean basins; hydrothermal vents host chemosynthetic ecosystems independent of solar energy |
| **TrophicPyramid** | Both systems: stratified (`m2:Layer`), energy-flux driven, threshold-mediated |
| **PhaseTransition** | Mantle melting, eclogite transition, slab dehydration = first-order phase transitions at geological scale |

---

## 10. Repository Location

```
instances/
  poclets/
    PlateTectonics/
      M0_PlateTectonics.jsonld        ← Ontology v1.1.0
      M0_PlateTectonics_README.md     ← This file v2.0.0
      static/
        M0_PlateTectonics.html        ← Static HTML simulation v2.0.0 (BabylonJS 6.26.0)

ontology/
  M1_extensions/
    geology/
      M1_Geology.jsonld               ← Domain extension v1.0.0
```

---

## 11. References

- Wegener A. (1912) — *Die Entstehung der Kontinente und Ozeane*
- Hess H.H. (1962) — *History of Ocean Basins*
- Vine F.J. & Matthews D.H. (1963) — *Magnetic anomalies over oceanic ridges*, Nature 199:947–949
- Wilson J.T. (1963) — *A possible origin of the Hawaiian Islands*, Canadian Journal of Physics 41(6):863–870
- Morgan W.J. (1968) — *Rises, Trenches, Great Faults, and Crustal Blocks*, JGR 73(6):1959–1982
- Walker J.C.G., Hays P.B., Kasting J.F. (1981) — *A negative feedback mechanism for long-term stabilization*, JGR 86(C10):9776–9782
- Ivanova V. & Perron J.T. (2013) — *Visual Earth: Plate Tectonics*, MIT ARTEMiS / OEIT — https://news.mit.edu/2013/as-the-world-turns-learning-about-plate-tectonics-through-on-screen-interactions
- Kearey P., Klepeis K.A., Vine F.J. (2009) — *Global Tectonics*, 3rd ed., Wiley-Blackwell

---

*Generated by TSCG Framework v15.11.0 — Echopraxium with the collaboration of Claude AI — 2026-04-05*
