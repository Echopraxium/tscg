# M0_TrophicPyramid — TSCG Poclet

**File:** `instances/poclets/TrophicPyramid/M0_TrophicPyramid.jsonld`
**Version:** 2.1.0 · **Date:** 2026-04-02
**Author:** Echopraxium with the collaboration of Claude AI
**Domain:** Ecology / Biology — Trophodynamics, Community Ecology, Thermodynamics of Ecosystems, Anthropocene Ecology
**Reference (trophic model):** Lindeman R.L. (1942) *The Trophic-Dynamic Aspect of Ecology*, Ecology 23(4):399–417
**Reference (AP model):** Meadows D.H. et al. (1972) *The Limits to Growth*, Club of Rome / Universe Books, New York

---

## 1. System Overview

A **Trophic Pyramid** is a hierarchical ecological structure in which each trophic level consumes biomass from the level below and dissipates approximately 90% of received energy as metabolic heat (respiration, faeces, uneaten biomass). This law-like thermodynamic constraint — **Lindeman's 10% efficiency rule** — creates an inescapable pyramidal shape: as rank increases, available energy budget decreases by one order of magnitude per level.

This poclet extends the classical model with two additions:

1. **Level 6 — Humanity** as a supra-trophic super-predator that bypasses Lindeman's rule via fossil fuel energy, consuming simultaneously at all levels and exerting global meta-regulatory control.
2. **Anthropic Pressure (AP)** — a normalised scalar ∈ [0, 1] quantifying the combined impact of fossil fuel exploitation and extractive mining on trophic biodiversity, grounded in Meadows et al. (1972) *The Limits to Growth* overshoot-and-collapse scenario.

The pyramid is simultaneously:
- A **structural pattern** (ordered positional strata — `m2:Layer`)
- A **thermodynamic funnel** (irreversible energy loss — `m2:Dissipation`)
- An **epistemic object** (universally representable, verifiable and inter-operable across biomes — `m2:Context`)
- An **anthropogenic target** (all levels under top-down pressure from humanity — `AnthropogenicDomination`)

### TSCG Synergy Formulas

```
StratifiedDissipation   = Biology ⊙ (m2:Layer ⊗ m2:Dissipation)
Compiled tensor:          S ⊗ I ⊗ A ⊗ R ⊗ F ⊗ D

AnthropogenicDomination = Biology ⊙ (m2:Transducer ⊗ m2:Regulation ⊗ m2:Entropy)
Compiled tensor:          F ⊗ I ⊗ A ⊗ S ⊗ D
```

---

## 2. Architecture — 6 Trophic Poles

| Pole | Trophic Level | Rank | Biomass (terrestrial) | Energy available |
|------|--------------|------|-----------------------|-----------------|
| `level_1_producers` | Primary Producers (Autotrophs) | 1 | ~99% | 10 000 kJ/m²/yr |
| `level_2_herbivores` | Primary Consumers (Herbivores) | 2 | ~1% | 1 000 kJ/m²/yr |
| `level_3_carnivores` | Secondary Consumers (Carnivores) | 3 | ~0.1% | 100 kJ/m²/yr |
| `level_4_apex` | Apex Predators (Tertiary Consumers) | 4 | ~0.01% | 10 kJ/m²/yr |
| `level_5_decomposers` | Decomposers (base — transversal) | ⟂ | variable | 40–60% of total flux |
| `level_6_humanity` | Humanity (Supra-Trophic Super-Predator) | meta | ~0.01% biomass / ~35% NPP | ~21 000 kJ/m²/yr (fossil bypass) |

### Visualisation Convention — Split Base

Decomposers are represented as the **right compartment of the pyramid base**, bisected vertically from Level 1 Producers (left compartment). The total base width is fixed; each compartment rescales dynamically with AP:

```
        /\
       /L4\
      /----\
     /  L3  \
    /--------\
   /    L2    \
  /------------\
 /      L1      \
/-------+--------\
│  L1   │  Deco  │
│Producers│posers│
└───────┴────────┘
```

This preserves the pyramid as a unified geometric form while correctly representing the transversal nature of decomposers (`rank = "base-level (transversal)"`).

### Structural Invariants

Three constraints ensure natural pyramid integrity (AP = 0):

1. **Lindeman Efficiency** — `η = E_(n+1)/E_n ≈ 0.10` (thermodynamic; violation → collapse)
2. **Positional Ordering** — strict total order on trophic ranks; no cyclic predation at the same level
3. **Autotrophic Base** — `Biomass(Producers) ≥ Σ Biomass(all other levels)`

A fourth constraint governs the anthropogenic dimension:

4. **Anthropic Pressure Threshold** — `AP_crit = 0.70` (above this, cascade is irreversible — m2:Entropy)

---

## 3. TSCG Bicephalous Analysis

### 3.1 Eagle Eye (ASFID — Territory Space)

| Dimension | Score | Interpretation |
|-----------|-------|----------------|
| **A** Attractor | **0.97** | Dual attractor: Lindeman's thermodynamic basin (universal) + anthropogenic meta-attractor (global ecosystem dominance by humanity). No ecosystem escapes either basin. |
| **S** Structure | **0.92** | Discrete, ordered strata stable across biomes + humanity's meta-layer (agriculture, cities, fishing fleets) overlying all natural levels. |
| **F** Flow | **0.97** | Bottom-up energy flow + top-down cascades + fossil-fuel bypass (~20 000 kJ/m²/yr exceeding natural primary production). |
| **I** Information | **0.90** | Trophic position encodes metabolic role + biomagnification of toxins. Humanity adds unprecedented information processing (technology, global monitoring, conservation science). |
| **D** Dynamics | **0.95** | Lotka-Volterra oscillations, trophic cascades + 6th mass extinction, climate change, habitat destruction. Anthropocene dynamics now dominate. |

**ASFID mean = 0.94**

### 3.2 Sphinx Eye (REVOI — Map Space)

| Dimension | Score | Interpretation |
|-----------|-------|----------------|
| **R** Representability | **0.85** | Classic pyramid diagram iconic but strained by humanity as meta-level: a single species commanding all levels simultaneously challenges standard representational conventions. |
| **E** Evolvability | **0.80** | Core thermodynamic structure constrained (Lindeman). Model gains evolvability: Anthropocene scenarios, rewilding, climate-driven trophic shifts, AP trajectory modelling. |
| **V** Verifiability | **0.85** | Lindeman's law validated across hundreds of ecosystems. Human impact harder to quantify: HANPP estimated at 30–40% globally; AP calibration requires Earth System Science methods. |
| **O** Observability | **0.90** | Species identifiable, populations countable. Human activities highly observable via satellite, fishery data, IUCN Red List, Living Planet Index. |
| **I** Interoperability | **0.95** | Bridges thermodynamics, evolutionary biology, biogeochemistry, conservation biology, economics (ecosystem services), Earth System Science, *Limits to Growth* modelling. |

**REVOI mean = 0.87**

### 3.3 Epistemic Gap

```
δ = |ASFID_mean − REVOI_mean| = |0.94 − 0.87| = 0.07  →  OnCriticalLine [0.05, 0.15)
```

Gap increased from 0.05 (v1.0.0, Coherent) to 0.07 (v2.x, OnCriticalLine) with the addition of humanity and AP. Main residual gaps on A/R, S/E and F/V axes (+0.12 each): the meta-trophic attractor and fossil-fuel bypass are empirically undeniable but harder to represent and verify than classical trophic levels.

**Balance type:** Eagle Eye dominant — thermodynamic + anthropogenic empirical grounding.

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
| `m2:Regulation` | A⊗S⊗F | Predator-prey feedback loops + anthropogenic meta-regulation |
| `m2:Cascade` | ⊗⇒(Process,Step,Trajectory) | Natural trophic cascade + Anthropogenic super-cascade |
| `m2:Threshold` | A⊗I⊗F | Minimum viable population; AP_crit = 0.70 (irreversible collapse) |
| `m2:Network` | S⊗F⊗I | Food web underlying the pyramid |
| `m2:Emergence` | — | Ecosystem services (pollination, carbon sequestration) |
| `m2:Transducer` | F⊗I | Humanity converts geological energy into trophic control (fossil-fuel bypass) |
| `m2:Entropy` | D⊗F | Accelerated irreversibility: mass extinction = absorbing state; AP ≥ 0.70 seals cascade |
| `m2:Processor` | I | Humanity's technological information processing enabling supra-trophic strategy |

**Total M2 GenericConcepts mobilised: 15**

---

## 5. KnowledgeFieldConceptCombos

### 5.1 StratifiedDissipation

**StratifiedDissipation** is the core `KnowledgeFieldConceptCombo` introduced by this poclet, defined in `M1_Biology.jsonld`:

```
StratifiedDissipation = Biology ⊙ (Layer ⊗ Dissipation)
Qualification operator:  ⊙ (disciplinary, not tensor product)
Compiled tensor formula: S ⊗ I ⊗ A ⊗ R ⊗ F ⊗ D
Dominant dimensions:     S, I, A (Layer scaffold) + F, D (Dissipation engine)
```

**Semantics:** Energy dissipation *structured* by stable positional strata. `Layer` provides the spatial/positional scaffold; `Dissipation` provides the thermodynamic engine. Their combination produces the pyramidal biomass distribution as an emergent property. Empirical law: Lindeman's 10% rule — `η ≈ 0.1` at each trophic boundary.

### 5.2 AnthropogenicDomination

**AnthropogenicDomination** is the second `KnowledgeFieldConceptCombo`, capturing humanity's supra-trophic role:

```
AnthropogenicDomination = Biology ⊙ (Transducer ⊗ Regulation ⊗ Entropy)
Compiled tensor formula:  F ⊗ I ⊗ A ⊗ S ⊗ D
Dominant dimensions:      F, I, A, D
```

**Semantics:** Humanity as a meta-transducer converting geological energy (fossil fuels) into ecosystem regulation, amplifying global entropy through mass extinction and climate forcing. Unlike StratifiedDissipation (thermodynamic law), AnthropogenicDomination is a contingent but now dominant meta-pattern of the Anthropocene.

---

## 6. Anthropic Pressure (AP) Model

Grounded in Meadows et al. (1972) **"The Limits to Growth"** (Club of Rome), the AP model operationalises the overshoot-and-collapse scenario as a single trophic pressure parameter.

### 6.1 Definition

```
AP ∈ [0.0, 1.0]
AP = 0.0  →  pre-industrial natural pyramid (Lindeman baseline)
AP = 0.46 →  current situation (2024 estimate)
AP = 0.70 →  AP_crit — irreversible cascade threshold
AP = 1.00 →  maximum exploitation — full pyramid collapse
```

**Drivers:** fossil fuel extraction (CO₂/CH₄ → acidification, warming, habitat loss) + extractive mining (direct habitat destruction, freshwater pollution).

### 6.2 Biomass Impact Formulas

Top-down cascade: Level 4 collapses first; decomposers exhibit non-monotonic irruption then collapse.

| Level | Formula B_n(AP) | Collapses at |
|-------|----------------|-------------|
| L4 Apex | `max(0, 1.0 − 3.0 × AP)` | AP = 0.33 |
| L3 Carnivores | `max(0, 1.0 − 2.0 × AP)` | AP = 0.50 |
| L2 Herbivores | `(1 + 0.5×AP) × max(0, 1.0 − 1.8×AP)` | AP ≈ 0.55 (irruption peak ~AP=0.28) |
| L1 Producers | `max(0, 1.0 − 1.0 × AP)` | AP = 1.00 |
| Decomposers | `(1 + 0.8×AP) × max(0, 1.0 − 3.0 × max(0, AP−0.6))` | AP ≈ 0.93 (irruption peak ~AP=0.60) |

### 6.3 Limits to Growth — Scenario Mapping

| LtG Scenario | AP value | Outcome |
|---|---|---|
| Pre-industrial baseline | 0.00 | Natural Lindeman pyramid |
| 1972 (publication year) | ~0.20 | Moderate stress, L4 declining |
| 2024 (current) | ~0.46 | L4 severely reduced, L3 declining, L2 irruption |
| BAU 2050 | ~0.85 | Past AP_crit — irreversible collapse underway |
| Stabilised transition | ~0.50 | Aggressive decarbonisation + rewilding |
| Recovery 2100 | ~0.35 | Full energy transition + ecosystem restoration |

The **"standard run"** of *Limits to Growth* maps directly onto crossing AP_crit = 0.70 between 2030 and 2050, triggering the `m2:Entropy` absorbing state.

---

## 7. Special Dynamics — Trophic Cascade

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

## 8. m2:Context — Biome-Dependent Layer Filling

The `m2:Context` GenericConcept (O⊗R⊗Im⊗E) finds its clearest ecological instantiation in the biome-specific filling of trophic Layers:

| Context (Biome) | Level 1 | Level 2 | Level 3 | Level 4 | Humanity (Level 6) |
|-----------------|---------|---------|---------|---------|-------------------|
| Tropical Rainforest | Canopy trees, epiphytes | Leaf-cutter ants, tapirs | Ocelots, harpy eagles | Jaguars, anacondas | Deforestation, agribusiness, bushmeat trade |
| Arctic Tundra | Mosses, lichens, sedges | Lemmings, caribou | Arctic fox | Polar bear, wolf | Oil extraction, climate forcing, trophy hunting |
| Open Ocean | Phytoplankton | Zooplankton, krill | Herring, anchovy | Tuna, sharks, orca | Industrial fishing, ocean acidification, plastic pollution |

Same `m2:Layer` hierarchy; radically different species filling each stratum. The **Context** (`O⊗R⊗Im⊗E`) is the epistemic frame that conditions which species are observable, representable, interoperable across scientific communities, and evolvable over geological time.

---

## 9. TSCG Framework Contributions

| Layer | Contribution | Type |
|-------|-------------|------|
| **M2** | `m2:Layer` (S⊗I⊗A⊗R) — validated by Trophic Pyramid + 6 other domains | GenericConcept |
| **M2** | `m2:Context` (O⊗R⊗Im⊗E) — validated across biomes and disciplines | GenericConcept |
| **M2** | `m2:Transducer`, `m2:Entropy`, `m2:Processor` — mobilised by humanity / AP model | GenericConcepts |
| **M1_Biology** | `StratifiedDissipation` — KnowledgeFieldConceptCombo (Biology ⊙ Layer⊗Dissipation) | New M1 concept |
| **M1_Biology** | `AnthropogenicDomination` — KnowledgeFieldConceptCombo (Biology ⊙ Transducer⊗Regulation⊗Entropy) | New M1 concept |
| **M0** | `M0_TrophicPyramid.jsonld` — 6-pole poclet with AP model, trophic cascade, humanity as super-predator | Poclet |

---

## 10. Repository Location

```
instances/
  poclets/
    TrophicPyramid/
      M0_TrophicPyramid.jsonld      ← Ontology (v2.1.0)
      M0_TrophicPyramid_README.md   ← This file
      sim/
        index.html                  ← Standalone HTML simulation (static)
```

---

## 11. References

- Lindeman R.L. (1942) — *The Trophic-Dynamic Aspect of Ecology*, Ecology 23(4):399–417
- Meadows D.H., Meadows D.L., Randers J., Behrens W.W. (1972) — *The Limits to Growth*, Club of Rome / Universe Books, New York (**AP model basis**)
- Elton C.S. (1927) — *Animal Ecology*, Sidgwick & Jackson, London (first food chain concept)
- Hairston N.G., Smith F.E., Slobodkin L.B. (1960) — *Community structure, population control, and competition*, American Naturalist 94(879):421–425
- Ripple W.J. et al. (2014) — *Status and Ecological Effects of the World's Largest Carnivores*, Science 343(6167)
- Paine R.T. (1966) — *Food Web Complexity and Species Diversity* (keystone species concept)
- Bar-On Y.M., Phillips R., Milo R. (2018) — *The biomass distribution on Earth*, PNAS 115(25):6506–6511 (humanity + livestock biomass data)
- IPBES (2019) — *Global Assessment Report on Biodiversity and Ecosystem Services* (1 million threatened species)

---

*Generated by TSCG Framework v15.11.0 — Echopraxium with the collaboration of Claude AI — 2026-04-02*
