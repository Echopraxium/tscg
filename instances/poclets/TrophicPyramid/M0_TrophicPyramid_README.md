# M0_TrophicPyramid — TSCG Poclet

**File:** `instances/poclets/TrophicPyramid/M0_TrophicPyramid.jsonld`
**Version:** 1.0.0 · **Date:** 2026-03-13
**Author:** Echopraxium with the collaboration of Claude AI
**Domain:** Ecology / Biology — Trophodynamics, Community Ecology, Thermodynamics of Ecosystems
**Reference:** Lindeman R.L. (1942) *The Trophic-Dynamic Aspect of Ecology*, Ecology 23(4):399–417

---

## 1. System Overview

A **Trophic Pyramid** is a hierarchical ecological structure in which each trophic level consumes biomass from the level below and dissipates approximately 90% of received energy as metabolic heat (respiration, faeces, uneaten biomass). This law-like thermodynamic constraint — **Lindeman's 10% efficiency rule** — creates an inescapable pyramidal shape: as rank increases, available energy budget decreases by one order of magnitude per level.

The pyramid is simultaneously:
- A **structural pattern** (ordered positional strata — `m2:Layer`)
- A **thermodynamic funnel** (irreversible energy loss — `m2:Dissipation`)
- An **epistemic object** (universally representable, verifiable and inter-operable across biomes — `m2:Context`)

### TSCG Synergy Formula

```
StratifiedDissipation = Biology ⊙ (m2:Layer ⊗ m2:Dissipation)
Compiled tensor:         S ⊗ I ⊗ A ⊗ R ⊗ F ⊗ D
```

**StratifiedDissipation** is the core `KnowledgeFieldConceptCombo` introduced by this poclet: *energy dissipation structured by stable positional strata*. No ecosystem designer required — thermodynamic flow (F⊗D) through ordered partitions (S⊗I⊗A⊗R) inevitably produces the pyramid.

---

## 2. Architecture — 5 Trophic Poles

| Pole | Trophic Level | Rank | Biomass (terrestrial) | Energy available |
|------|--------------|------|-----------------------|-----------------|
| `level_1_producers` | Primary Producers (Autotrophs) | 1 | ~99% | 10 000 kJ/m²/yr |
| `level_2_herbivores` | Primary Consumers (Herbivores) | 2 | ~1% | 1 000 kJ/m²/yr |
| `level_3_carnivores` | Secondary Consumers (Carnivores) | 3 | ~0.1% | 100 kJ/m²/yr |
| `level_4_apex` | Apex Predators (Tertiary Consumers) | 4 | ~0.01% | 10 kJ/m²/yr |
| `level_5_decomposers` | Decomposers (cross-cutting) | ⟂ | variable | 40–60% of total flux |

### Structural Invariants

Three constraints ensure pyramid integrity:

1. **Lindeman Efficiency** — `η = E_(n+1)/E_n ≈ 0.10` (thermodynamic; violation → collapse)
2. **Positional Ordering** — strict total order on trophic ranks; no cyclic predation at the same level
3. **Autotrophic Base** — `Biomass(Producers) ≥ Σ Biomass(all other levels)`

---

## 3. TSCG Bicephalous Analysis

### 3.1 Eagle Eye (ASFID — Territory Space)

| Dimension | Score | Interpretation |
|-----------|-------|----------------|
| **A** Attractor | **0.95** | Pyramid shape is a universal thermodynamic attractor. Lindeman's 10% rule functions as a positional-stability law: no ecosystem escapes this energy basin. |
| **S** Structure | **0.90** | Discrete, ordered strata. Each trophic level is a bounded positional partition (`m2:Layer`). Structure stable across terrestrial, aquatic and marine biomes. |
| **F** Flow | **0.95** | Energy/biomass flow is the fundamental mechanism. Unidirectional (bottom-up primary flux) with bidirectional regulation (top-down trophic cascades). |
| **I** Information | **0.80** | Trophic position encodes metabolic role, niche, and energy budget. Biomagnification: persistent pollutants concentrate upward. |
| **D** Dynamics | **0.85** | Lotka-Volterra population oscillations, trophic cascades (apex removal → herbivore irruption), seasonal succession, geomorphic effects (Yellowstone wolf reintroduction 1995). |

**ASFID mean = 0.89** — high across all 5 dimensions, no structural weakness.

### 3.2 Sphinx Eye (REVOI — Map Space)

| Dimension | Score | Interpretation |
|-----------|-------|----------------|
| **R** Representability | **0.95** | Most iconic ecological diagram. Three canonical variants: energy pyramid, biomass pyramid, numbers pyramid. Semantically unambiguous across all scientific communities. |
| **E** Evolvability | **0.70** | Core thermodynamic structure is law-like (constrained). Extensions possible: inverted pyramids (phytoplankton-rich aquatic), trophic web-to-pyramid projections, climate change scenarios. |
| **V** Verifiability | **0.90** | Lindeman's law validated across hundreds of ecosystems since 1942. Energy budgets measurable via calorimetry, isotope tracing (¹⁵N, ¹³C stable isotope analysis). |
| **O** Observability | **0.80** | Species identifiable, populations countable. Energy flow requires indirect measurement (metabolic assays, radiotracer). Decomposer activity often underestimated. |
| **I** Interoperability | **0.85** | Bridges thermodynamics (entropy), evolutionary biology (niche theory), biogeochemistry (nutrient cycling), conservation biology (minimum viable population). |

**REVOI mean = 0.84**

### 3.3 Epistemic Gap

```
δ = |ASFID_mean − REVOI_mean| = |0.89 − 0.84| = 0.05
```

**Exceptionally low gap** — one of ecology's best-characterised systems. The only notable residual gap is on the E (Evolvability) axis: ASFID A = 0.95 (the attractor is universally observed) vs REVOI E = 0.70 (modelling ecosystem evolvability under climate change remains challenging).

**Balance type:** Eagle Eye dominant — strong empirical grounding (Lindeman's law, isotope tracing, field studies across all biomes).

---

## 4. GenericConcepts Mobilised

### Primary

| GenericConcept | Formula | Role in Trophic Pyramid |
|----------------|---------|------------------------|
| `m2:Layer` | S⊗I⊗A⊗R | **Structural backbone** — each trophic level IS a Layer. 5 ordered positional partitions. |
| `m2:Dissipation` | F⊗D | **Core mechanism** — ~90% energy lost as heat at each trophic boundary. Lindeman's 10% rule. |
| `m2:Context` | O⊗R⊗Im⊗E | **Epistemic frame** — the biome context (tropical, arctic, marine) determines which species fill each Layer. Same trophic structure, different species across contexts. |

### Secondary

| GenericConcept | Formula | Role |
|----------------|---------|------|
| `m2:Hierarchy` | A⊗S | Positional ordering base → apex |
| `m2:Flow` | F | Energy/biomass transfer between levels |
| `m2:Gradient` | ⊗₂F | Energy density gradient from base to apex |
| `m2:Homeostasis` | A⊗S⊗F⊗I⊗D | Ecosystem equilibrium under perturbation |
| `m2:Regulation` | A⊗S⊗F | Predator-prey negative feedback loops |
| `m2:Cascade` | ⊗⇒(Process,Step,Trajectory) | Trophic cascade: apex removal → top-down destabilisation |
| `m2:Threshold` | A⊗I⊗F | Minimum viable population; trophic collapse triggers |
| `m2:Network` | S⊗F⊗I | Food web underlying the pyramid |
| `m2:Emergence` | — | Ecosystem services (pollination, carbon sequestration) from level interactions |

**Total M2 GenericConcepts mobilised: 12**

---

## 5. KnowledgeFieldConceptCombo — StratifiedDissipation

**StratifiedDissipation** is a new `KnowledgeFieldConceptCombo` introduced by this poclet, defined in `M1_Biology.jsonld`:

```
StratifiedDissipation = Biology ⊙ (Layer ⊗ Dissipation)
Qualification operator:  ⊙ (disciplinary, not tensor product)
Compiled tensor formula: S ⊗ I ⊗ A ⊗ R ⊗ F ⊗ D
Dominant dimensions:     S, I, A (Layer scaffold) + F, D (Dissipation engine)
```

**Semantics:** Energy dissipation that is *structured* by stable positional strata. The key insight: `Layer` provides the spatial/positional scaffold (where the dissipation happens), while `Dissipation` provides the thermodynamic engine (how it happens). Their combination produces the pyramidal biomass distribution as an emergent property.

**Empirical law:** Lindeman's 10% rule — `η ≈ 0.1` at each trophic boundary.

**Cross-domain validation:**
- Terrestrial ecology (forests, grasslands)
- Marine ecology (pelagic zone)
- Freshwater ecology (lakes, rivers)
- Aquatic microbial ecology (microbial loop)
- Agro-ecology (managed agricultural systems)

---

## 6. Special Dynamics — Trophic Cascade

The **Trophic Cascade** is the most dramatic emergent behaviour of the pyramid system. When an apex predator is removed:

```
Step 1: Apex predators → removed / collapsed
Step 2: Secondary consumers → released from predation → irruption
Step 3: Herbivores → intensified predation → collapse
Step 4: Producers → released from herbivory → vegetation restructuring
Step 5: Geomorphic / hydrological cascades follow (rivers, soil composition)
```

**Empirical signature:** Yellowstone wolf reintroduction (1995) — rivers changed course as elk grazing patterns shifted, triggering geomorphic changes. This phenomenon ("the wolves that changed rivers") is the most famous trophic cascade in conservation biology.

GenericConcepts mobilised by cascade: `m2:Cascade`, `m2:Threshold`, `m2:Regulation`, `m2:Homeostasis`, `m2:Bifurcation`.

---

## 7. m2:Context — Biome-Dependent Layer Filling

The `m2:Context` GenericConcept (O⊗R⊗Im⊗E) finds its clearest ecological instantiation in the biome-specific filling of trophic Layers:

| Context (Biome) | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------------|---------|---------|---------|---------|
| Tropical Rainforest | Canopy trees, epiphytes | Leaf-cutter ants, tapirs | Ocelots, harpy eagles | Jaguars, anacondas |
| Arctic Tundra | Mosses, lichens, sedges | Lemmings, caribou | Arctic fox | Polar bear, wolf |
| Open Ocean | Phytoplankton | Zooplankton, krill | Herring, anchovy | Tuna, sharks, orca |

Same `m2:Layer` hierarchy; radically different species filling each stratum. The **Context** (`O⊗R⊗Im⊗E`) is the epistemic frame that conditions which species are observable, representable, interoperable across scientific communities, and evolvable over geological time.

---

## 8. TSCG Framework Contributions

| Layer | Contribution | Type |
|-------|-------------|------|
| **M2** | `m2:Layer` (S⊗I⊗A⊗R) — validated by Trophic Pyramid + 6 other domains | GenericConcept (new) |
| **M2** | `m2:Context` (O⊗R⊗Im⊗E) — validated by ecology + linguistics + computing + law + biology + mathematics | GenericConcept (new) |
| **M1_Biology** | `StratifiedDissipation` — KnowledgeFieldConceptCombo (Biology ⊙ Layer⊗Dissipation) | New M1 concept |
| **M0** | `M0_TrophicPyramid.jsonld` — 5-pole poclet with trophic cascade modelling | Poclet (new) |

---

## 9. Repository Location

```
instances/
  poclets/
    TrophicPyramid/
      M0_TrophicPyramid.jsonld      ← Ontology
      M0_TrophicPyramid_README.md   ← This file
      sim/
        main.js                     ← Electron main process
        index.html                  ← Simulation UI (template)
        renderer.js                 ← P5.js simulation
        styles.css                  ← TSCG simulation stylesheet
```

---

## 10. References

- Lindeman R.L. (1942) — *The Trophic-Dynamic Aspect of Ecology*, Ecology 23(4):399–417
- Elton C.S. (1927) — *Animal Ecology*, Sidgwick & Jackson, London (first food chain concept)
- Hairston N.G., Smith F.E., Slobodkin L.B. (1960) — *Community structure, population control, and competition*, American Naturalist 94(879):421–425
- Ripple W.J. et al. (2014) — *Status and Ecological Effects of the World's Largest Carnivores*, Science 343(6167)
- Paine R.T. (1966) — *Food Web Complexity and Species Diversity* (keystone species concept)

---

*Generated by TSCG Framework v15.10.1 — Echopraxium with the collaboration of Claude AI — 2026-03-13*
