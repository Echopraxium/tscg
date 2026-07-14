# M0_PlateTectonics — TSCG Poclet

**File:** `instances/poclets/PlateTectonics/M0_PlateTectonics.jsonld`
**Version:** 1.2.0 · **Date:** 2026-07-12
**Author:** Echopraxium with the collaboration of Claude AI
**Domain:** Geology / Geophysics — Geodynamics, Seismology, Volcanology, Paleoclimatology, Biogeography, Geohazard Science
**ontologyType:** `m3:Poclet`
**Observer:** Geophysicist / Earth System Scientist

**References:**
Wegener A. (1912) *Die Entstehung der Kontinente* — continental drift ·
Vine F.J. & Matthews D.H. (1963) — magnetic anomalies over ocean ridges ·
Wilson J.T. (1963) — hotspot concept ·
Morgan W.J. (1968) *Rises, Trenches, Great Faults, and Crustal Blocks*

> **Simulation**: a BabylonJS prototype lives in `_static/`, with its **own** README
> (`M0_PlateTectonics_Simulation_README.md` — finite-element stress diffusion, controls,
> visual feedback). This file is the **ontology** README. The two are deliberately distinct.
>
> ⚠️ **The leading underscore in `_static/` is functional, not cosmetic.** The poclet-gallery
> index generator **skips underscore-prefixed folders**. A prototype simulation therefore
> lives in `_static/`; only a finished one is promoted to `static/`, where the gallery
> publishes it. **Renaming `_static/` → `static/` would publish this prototype.**

---

## 1. The system

The governing geodynamic system of Earth's lithosphere: **rigid plates floating on a
viscous asthenosphere**, driven by mantle convection, continuously **creating** crust at
mid-ocean ridges and **destroying** it at subduction zones, while releasing accumulated
stress along seismic faults.

What makes it a Poclet rather than a description: the **five poles are not parts, they are
roles in a single thermodynamic cycle**, and the cycle regulates itself. Remove any one and
the system does not degrade — it stops.

**A note on causality that the model encodes explicitly**: *the mantle drives the plates.*
Plates are **passive riders**, not self-propelled agents (slab pull ≈ 70 % of the driving
force). This is the standard misconception the poclet is built to prevent.

---

## 2. The five poles

| Pole | M1_Geology type | Role in the cycle |
|---|---|---|
| **LithosphericPlate** | `m1geo:LithosphericPlate` | The rigid carrier — the thing that moves |
| **MidOceanRidge** | `m1geo:MidOceanRidge` | **Accretion / Negentropy** — new crust created |
| **SubductionZone** | `m1geo:SubductionZone` | **Transformation / Entropy export** — crust destroyed |
| **MantleConvectionCell** | `m1geo:MantleConvectionCell` | The thermodynamic **driver** (Ra ≈ 10⁷) |
| **SeismicFault** | `m1geo:SeismicFault` | **Stress release** — the discrete failure channel |

Two poles (ridge, subduction) form an **antisymmetric pair**: one is the negentropic source,
the other the entropic sink. Their coupling *is* the Wilson cycle.

---

## 3. Synergy principle

```
PlateTectonics = Fm1m2(Geology, Entropy, Accretion, Transformation)
```

**Emergent property — the Wilson Cycle**: a self-regulating, planetary-scale geodynamic
engine (~500 Ma period). Oceanic crust is continuously created at ridges and consumed at
trenches; the two rates are coupled through the mantle, so the surface area of the Earth
stays constant while its crust is entirely renewed. **No single pole contains this cycle.**

> ⚠️ **SC-1 notation note.** `M0_PlateTectonics.jsonld` still stores this as
> `m0:synergyPrinciple = "Geological ⊙ (m2:Entropy[Negentropy] ⊗ m1core:Accretion ⊗ m2:Transformation)"`.
> `⊙` was the **disciplinary qualification operator** — i.e. `Fm1m2` before it had a name —
> and `⊗` was the retired tensor product. The data still carries the old form; the purge is
> **SC-9**. This README states the current model.

---

## 4. GenericConcepts mobilised

| GenericConcept | Role in Plate Tectonics |
|---|---|
| `m2:Layer` | Lithospheric stratification (crust / lithospheric mantle / asthenosphere) |
| `m2:Entropy` | **Dual — both poles active at once**: Negentropy at ridges, Entropy export at trenches |
| `m1core:Accretion` | Seafloor spreading — **the canonical geological validation** of the combo |
| `m2:Transformation` | Subduction — oceanic lithosphere returns to the asthenosphere |
| `m2:Equilibrium` | **Isostasy** — the gravitational attractor of crustal thickness/density |
| `m2:Convection` | The mantle thermodynamic driver |
| `m2:Trajectory` | Continental drift — Euler rotation vectors |
| `m2:Threshold` | Seismic failure — Coulomb criterion |
| `m2:Cycle` | The Wilson cycle (~500 Ma) |
| `m2:Bifurcation` | Ridge genesis — a divergent boundary appearing |

`m2:Entropy` deserves the emphasis: this poclet is one of the few where **both polarities
of a dual concept are simultaneously instantiated**, in two different places of the same
system. That is not a modelling convenience — it is what the Earth does.

---

## 5. DomainConceptCombo

**`m1geo:GeologicalAccretion`** — introduced by this poclet, defined in `M1_Geology.jsonld`:

```
GeologicalAccretion = Fm1m2(Geology, Accretion)
```

A `DomainConceptCombo` is defined **by its `Fm1m2` formula** — a hybrid of **≥ 1 Domain and
≥ 1 GenericConcept**. Domain **qualification** is the membership criterion (SC-1, 2026-07-12);
it is *not* "parents from distinct epistemological domains", which was the previous, unenforced
criterion. `Fm1m2(Geology, Accretion)` is well-formed with a single concept argument, because
the *domain × concept hybridisation* is itself the emergence.

> The data currently stores `"m1geo:GeologicalAccretion = Geological ⊙ Accretion"` — same
> residue, same fate (SC-9).

---

## 6. Scores

### Territory (ASFID) — mean **0.890**

| | Score | Why |
|---|---|---|
| **A** | 0.85 | **Isostasy is the primary attractor**: any crustal perturbation triggers compensatory adjustment. Below 1.0 because the Wilson-cycle attractors (~500 Ma) are hard to quantify precisely. |
| **S** | 0.95 | Plate geometry, boundary types and layering are exceptionally well characterised. |
| **F** | 0.90 | Mass and heat flux are continuous, measurable, and conserved. |
| **I** | 0.85 | The magnetic-stripe record encodes seafloor age directly — the crust is its own archive. |
| **D** | 0.90 | Slow but relentless dynamics; the system never rests. |

### Map (REVOI) — mean **0.854**

| | Score | Why |
|---|---|---|
| **R** | 0.90 | Global plate-boundary maps, GPlates, NUVEL velocity models — one of the most complete scientific representations ever built. |
| **E** | 0.80 | The core framework has been mature since the 1970s; extension is active but incremental. |
| **V** | 0.92 | GPS geodesy verifies predicted plate velocities directly. Very few Earth-system models are falsifiable this cleanly. |
| **O** | 0.80 | The mantle is not directly observable — tomography is an inference, not a photograph. |
| **Im** | 0.85 | Couples cleanly to climatology, biogeography, oceanography. |

### Epistemic gap

```
delta = ||ASFID − REVOI|| / √5 ≈ 0.078      spectralClass: OnCriticalLine   [0.05, 0.15)
```

**OnCriticalLine** — a mature model with two residual gaps, and they are *informative*:

- **S**: ASFID 0.95 vs REVOI 0.80. The plate structure is nearly perfectly **known**, but
  the mantle it floats on is **not directly observable**. The territory is more structured
  than the map can see.
- The gap is not a defect of the model. It is the **honest signature of a system whose
  driver is buried 100 km down**.

---

## 7. M1 contribution

| Layer | Contribution |
|---|---|
| **M1_Geology** | **New extension** — the first TSCG Earth Sciences extension (9 concepts + 1 DomainConceptCombo) |
| **M1_CoreConcepts** | `m1core:Accretion` — **MidOceanRidge is its canonical geological validation** |
| **M1_CoreConcepts** | `m1core:Nucleation` — confirmed by the slab partial-melting threshold (arc magma genesis) |
| **M2** | `m2:Entropy` (dual) — **both poles active simultaneously**; plus `m2:Layer`, `m2:Convection`, `m2:Bifurcation`, `m2:Transformation` confirmed |

---

## 8. Transdisciplinary resonances

| Domain | Resonance |
|---|---|
| **Climatology** | Continental positions steer ocean circulation; orogenic weathering regulates CO₂ (Walker cycle) |
| **Biogeography** | Plate separation → allopatric speciation; collisions → faunal exchange (Great American Biotic Interchange) |
| **Oceanography** | Plate tectonics creates and destroys ocean basins |

**Environmental significance**: silicate weathering of uplifted rock consumes atmospheric CO₂
over Ma timescales — the **long-term planetary thermostat** (Walker–Hays–Kasting 1981). Plate
boundaries also generate ~90 % of Earth's seismicity, the major tsunamis, and arc volcanism —
the primary geohazard exposure for 500 M+ people.

---

## 9. Files

```
instances/poclets/PlateTectonics/
├── M0_PlateTectonics.jsonld                     the ontology (v1.2.0)
├── M0_PlateTectonics_README.md                  ← this file (ontology)
└── _static/                                     ← underscore = HIDDEN from the gallery
    ├── M0_PlateTectonics.html                   BabylonJS 6.26.0 (v2.0.0 — PROTOTYPE)
    └── M0_PlateTectonics_Simulation_README.md   the SIMULATION README
```

**Convention**: `_static/` = prototype, not published. `static/` = finished, published by the
gallery index generator. The underscore is the switch.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **1.2.0** | 2026-07-12 | **SC-1** — `m2:KnowledgeFieldConceptCombo` → `m2:DomainConceptCombo`, re-defined by its `Fm1m2` formula (hybrid ≥1 Domain + ≥1 GenericConcept). **This ontology README created** — the previous `M0_PlateTectonics_README.md` was in fact the *simulation* README; it stays in `_static/M0_PlateTectonics_Simulation_README.md`, where it already lived (the underscore hides the prototype from the gallery). Remaining `⊙` / `⊗` in the `.jsonld` (`m0:synergyPrinciple`, `m0:m1ContributionSummary`) are flagged for **SC-9**. |
| 1.1.0 | 2026-04-05 | Initial poclet (5 poles, M1_Geology extension) |
