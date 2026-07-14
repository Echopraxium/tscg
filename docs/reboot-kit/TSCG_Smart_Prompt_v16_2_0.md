# TSCG Smart Prompt v16.2.0 — Structural Grammar + BMC SystemicFramework + δ₂/SFE

**Framework**: TSCG (Transdisciplinary System Construction Game)
**Version**: 16.2.0
**Date**: 2026-06-24
**Author**: Echopraxium with the collaboration of Claude AI

**Major Updates v16.1.0→v16.2.0**:
- ✅ **Structural Grammar formalism**: M3 foundation migrated from Hilbert space / tensor product to **Lambek calculus / free commutative monoidal categories**. `⊗` = monoidal product (no metric required). Braille diagram (©2022 Michel Kern) = canonical empirical proof.
- ✅ **M3_BicephalousPerspective.jsonld v1.3.0**: Gs monoid (|, TKSL), St/It indexation, Pole Annihilation Axiom, TriadicBalance `_0 = _^ | _$`
- ✅ **M2_GenericConcepts.jsonld v16.14.0**: 80 atomic patterns (+ `m2:Modelisation`, `m2:TriadicBalance`)
- ✅ **New SystemicFramework**: Bmc (Business Model Canvas) — total: 3 (Vsm + Triz + Bmc)
- ✅ **M0_BmcSimulation.jsonld**: 12 companies × 5 phases × 34 transitions, JSON-LD SHACL-validable, sim: namespace
- ✅ **New M1 extension**: M1_BusinessModeling.jsonld
- ✅ **δ₂ / SFE (Focal Score)**: `m0:focalScore = stereopsicDepth × (1 − |focalBias|)` — 6 FocalClasses
- ✅ **M0_Common.jsonld** canonical source for all shared M0 score properties
- ✅ **M1_CoreConcepts.jsonld v2.6.1**: `m1:Permeability` validated as M1 GenericConceptCombo
- ✅ **M3_GenesisGrammar.jsonld**: canonical name (replaces legacy `M3_GenesisSpace.jsonld`)
- ✅ **Corpus**: 34 validated instances (26 Poclets + 3 SystemicFrameworks + 1 SSG + 3 TscgTools + 1 stub)

**Major Updates v15.10.1→v16.1.0** (kept for reference):
- ✅ Score Convention Option B: `m0:scoreA/S/F/It/D/R/E/V/O/Im` distinct from MonoidalTypes
- ✅ TRIZ normalized: Altshuller 0–5 → 0–1 (÷5)
- ✅ Corpus: 24→26 poclets (+ Ptoe, PlateTectonics, NuclearReactorsTypology)
- ✅ SHACL Grammar v1.0 FINAL: 9 mandatory constraints, 100% corpus coverage

---

## 🎯 Context: What is TSCG?

TSCG (Transdisciplinary System Construction Game) is an **ontological framework** for analyzing and modeling complex systems across disciplines. It provides a rigorous mathematical foundation — **Lambek calculus / free commutative monoidal categories** — for understanding systemic patterns through a **bicephalous architecture** combining Territory measurement (Eagle Eye/ASFID) with Map construction (Sphinx Eye/REVOI), and their stereopsic fusion (Gs/TKSL).

### Core Principle (Korzybski Extended)
**"The map is not the territory, but the map influences how we observe the territory"**
- Classic (Korzybski, 1933): Map ≠ Territory
- TSCG Extension: **Bidirectional feedback loop** formalized through three monoidal grammars

---

## 📐 Authoring & File Conventions (CRITICAL)

These rules apply to **all generated ontology files** (.jsonld). Conversations may be in French, but all generated files must be in **English**.

### 1. Author field (MANDATORY — SHACL Enforced)
```json
"dcterms:creator": "Echopraxium with the collaboration of Claude AI"
```
⚠️ **CRITICAL**: Exact string. No variants allowed. SHACL validation will fail on any deviation.

### 2. URI root (MANDATORY)
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
```

### 3. @base — Short IRIs for M0 and M1 files (MANDATORY)
```json
{
  "@context": {
    "@base":    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
    "m0":       "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Common.jsonld#",
    "m1":       "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m2":       "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m3":       "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#",
    "owl":      "http://www.w3.org/2002/07/owl#",
    "rdfs":     "http://www.w3.org/2000/01/rdf-schema#",
    "dcterms":  "http://purl.org/dc/terms/"
  }
}
```
⚠️ MUST use **absolute URLs** — pyshacl cannot resolve relative URLs.
⚠️ `m3:` points to **`M3_GenesisGrammar.jsonld`** (NOT `M3_GenesisSpace.jsonld` — legacy name, forbidden).

### 4. Forbidden namespace: tscg:
The `tscg:` namespace is **FORBIDDEN** in all M0 instance files. Use `m0:`.

### 5. M1 extension IRI pattern
```
M1_extensions/extension_name/M1_ExtensionName.jsonld
```
Examples: `M1_extensions/biology/M1_Biology.jsonld`, `M1_extensions/business-modeling/M1_BusinessModeling.jsonld`

### 6. Score Convention Option B (MANDATORY — v16.1.0+)

Score DatatypeProperties sourced from **`M0_Common.jsonld`** (canonical):

```json
"m0:scoreA":  {"@value": "0.85", "@type": "xsd:float"},
"m0:scoreS":  {"@value": "0.70", "@type": "xsd:float"},
"m0:scoreF":  {"@value": "0.60", "@type": "xsd:float"},
"m0:scoreIt": {"@value": "0.75", "@type": "xsd:float"},
"m0:scoreD":  {"@value": "0.80", "@type": "xsd:float"},
"m0:scoreR":  {"@value": "0.90", "@type": "xsd:float"},
"m0:scoreE":  {"@value": "0.85", "@type": "xsd:float"},
"m0:scoreV":  {"@value": "0.80", "@type": "xsd:float"},
"m0:scoreO":  {"@value": "0.75", "@type": "xsd:float"},
"m0:scoreIm": {"@value": "0.70", "@type": "xsd:float"}
```

**It vs Im disambiguation:**
- `m0:scoreIt` = Information dimension (Territory/ASFID)
- `m0:scoreIm` = Interoperability dimension (Map/REVOI)

**In README tables:** `| A_score (Attractor) | 0.85 |` — NEVER bare `| A |`

**Flat storage** at `owl:Ontology` root level (never nested in sub-objects).

### 7. δ₂ / SFE — Focal Score Properties (optional, conditional)

Only when `m0:focalApplicable = true` (instance mobilizes ≥1 Gs/stereopsic GenericConcept):

```json
"m0:focalApplicable":   true,
"m0:stereopsicDepth":   {"@value": "0.75", "@type": "xsd:float"},
"m0:focalBias":         {"@value": "-0.08", "@type": "xsd:float"},
"m0:focalScore":        {"@value": "0.69", "@type": "xsd:float"},
"m0:focalClass":        {"@id": "m0:focalClass.SlightlyMyopic"}
```

Formula: `m0:focalScore = m0:stereopsicDepth × (1 − |m0:focalBias|)`

**`focalBias` sign convention:**
- Positive → **Hyperopic** (Map too abstract, Territory blurred)
- Negative → **Myopic** (Territory too detailed, Map inadequate)
- Zero → **Emmetropic candidate**

### 8. Changelog discipline
Keep only the **3 most recent entries** in `m2:changelog`. Rolling window — drop oldest on add.

---

## 🏗️ Framework Architecture (4 Layers)

```
M3_GenesisGrammar.jsonld      ← Mathematical foundation (Lambek calculus / monoidal categories)
  ├── M3_GrammarFoundation     (apex — base monoidal types)
  ├── M3_EagleEye              (Gt, ×, ASFID — Territory)
  ├── M3_SphinxEye             (Gm, +, REVOI — Map)
  └── M3_BicephalousPerspective (Gs, |, TKSL — Stereopsis)
        ↓ imports
M2_GenericConcepts.jsonld     ← 80 atomic patterns (9 families)
                                + m2:GenericConceptCombo + m2:DomainConceptCombo
        ↓ instantiates
M1_CoreConcepts.jsonld        ← GenericConceptCombo instances + KnowledgeField roots
M1_Domains.jsonld             ← 19 registered domains
M1_extensions/*/M1_*.jsonld   ← 13 domain vocabularies
        ↓ instantiates
instances/poclets/            ← 26 Poclets (M0)
instances/systemic-frameworks/ ← 3 SystemicFrameworks (Vsm, Triz, Bmc)
instances/symbolic-system-grammars/ ← 1 (Iching)
instances/tscg-tools/         ← 3 TscgTools + 1 stub
```

---

## 🧬 M3 — Bicephalous Genesis Space (Structural Grammar)

### Three Monoidal Grammars (Base16 = 16 primitives total)

| Grammar | Operator | Neutral | Acronym | Primitives (𝕋₀) | Count |
|---------|----------|---------|---------|-----------------|-------|
| **Gt** (Territory) | `×` | EmptyTerritory | **ASFID** | A, S, F, It, D | 5 |
| **Gm** (Map) | `+` | EmptyMap | **REVOI** | R, E, V, O, Im | 5 |
| **Gs** (Stereopsis) | `\|` | EmptyStereopsis | **TKSL** | T, _^, _$, K, Ss, L | 6 |

⚠️ **`⊗` is the monoidal product** — NOT a tensor product in Hilbert space sense. No metric required. Lambek calculus: free commutative monoidal categories.

⚠️ **TKSL acronym** = 4 nominal primitives (T, K, Ss, L). Poles `_^`/`_$` are modifiers, not in acronym.

### Dual-Eye Architecture

| Eye | Acronym | Perspective | Dimensions |
|-----|---------|-------------|------------|
| 🦅 **Eagle Eye** | **ASFID** | **Territory** — what exists empirically | **A**ttractor, **S**tructure, **F**low, **I**t (Information), **D**ynamics |
| 🦁 **Sphinx Eye** | **REVOI** | **Map** — how we represent it | **R**epresentability, **E**volvability, **V**erifiability, **O**bservability, **I**m (Interoperability) |

⚠️ **CRITICAL TERMINOLOGY**:
- **R = Representability** (semantic encodability/decodability) — NEVER "Reproducibility"
- **REVOI** (correct order) — ORIVE is **OBSOLETE**
- **It** = Information (Territory) vs **Im** = Interoperability (Map) — never confuse in formulas

### ASFID Dimension Definitions
- **A (Attractor)**: Equilibrium points, stable states, basins of attraction
- **S (Structure)**: Static organization, topology, architectural invariants
- **F (Flow)**: Material/energy/information throughput, flux dynamics
- **It (Information)**: Signal processing, encoding, cybernetic loops
- **D (Dynamics)**: Temporal evolution, feedback loops, phase transitions

### REVOI Dimension Definitions
- **R (Representability)**: Semantic encodability in formal notation
- **E (Evolvability)**: Adaptive capacity, parameter tunability
- **V (Verifiability)**: Empirical testability, Popperian falsifiability
- **O (Observability)**: Measurability, instrumentation accessibility
- **Im (Interoperability)**: Cross-framework translation, methodology compatibility

### Epistemic Gap δ₁

```
δ₁ = |ASFID_mean − REVOI_mean| / √2
```

**SpectralClasses** (stored as OWL enum IRIs):

| Class | δ₁ Range | Meaning |
|-------|----------|---------|
| `m0:spectralClass.Coherent` | [0, 0.05) | Near-perfect alignment |
| `m0:spectralClass.OnCriticalLine` | [0.05, 0.15) | Productive tension |
| `m0:spectralClass.Liminal` | [0.15, 0.30) | Significant gap |
| `m0:spectralClass.Enigmatic` | [0.30, 1.0) | Fundamental challenge |

### Focal Score δ₂ / SFE (Stereopsic Focal Score)

```
δ₂ = SFE = m0:stereopsicDepth × (1 − |m0:focalBias|)
```

- **stereopsicDepth**: proportion of active TKSL primitives (T:0.25, K:0.25, Ss:0.25, L:0.25)
- **focalBias**: `REVOI_mean − ASFID_mean` ∈ [−1, +1]

**FocalClasses** (stored as OWL enum IRIs):

| Class | SFE Range | Ophthalmic metaphor |
|-------|-----------|---------------------|
| `m0:focalClass.Emmetropic` | ≥ 0.70 | Perfect combined focus |
| `m0:focalClass.SlightlyMyopic` | [0.55, 0.70) | Slight Territory bias |
| `m0:focalClass.SlightlyHyperopic` | [0.55, 0.70) | Slight Map bias |
| `m0:focalClass.Myopic` | [0.35, 0.55) | Territory-dominant |
| `m0:focalClass.Hyperopic` | [0.35, 0.55) | Map-dominant |
| `m0:focalClass.Astigmatic` | < 0.35 | No stereopsis possible |

**Conditional**: only when `m0:focalApplicable = true` (≥1 Gs/TKSL GenericConcept mobilized).

### Gs Primitives — TKSL

| Primitive | Name | Question | Theoretical basis |
|-----------|------|----------|-------------------|
| **T** | Temporality | *When?* | Temporal interface Gt↔Gm |
| **_^** | PositivePole | *(polarity)* | Onset/amplifying modifier |
| **_$** | NegativePole | *(polarity)* | Terminus/attenuating modifier |
| **K** | Knowledge | *What?* | Maturana/Varela cognition, Husserl intentionality |
| **Ss** | Symbol (Stereopsic) | *Sign?* | Peirce sign theory, Saussure signifier/signified |
| **L** | Localizability | *Converging?* | Wiener 1948, Ashby 1956 cybernetics |

**Special elements:**
- `_^ | _$ = StereopsisEmptySet` (Pole Annihilation Axiom — named constant `#Null`, not a primitive)
- `_0 = _^ | _$` → TriadicBalance central state (DerivedGsElement, Base16 preserved)

### Notation Convention — St/It/O in hybrid formulas

In any formula containing `|`, Territory/Map types carry their monoid index:

```
Pure Territory:  A × S × F               ← ASFID unchanged
Hybrid formula:  A × St × It × D | V     ← St, It indexed
```

---

## 🧩 M2 — GenericConcepts (80 Atomic Patterns)

**Status**: 80 atomic GenericConcepts in 9 families (strictly transdisciplinary, ≥6 domains each).

**M2 Purity Constraint**: A concept belongs in M2 only if it is:
1. Truly irreducible to existing M2 concepts
2. Transdisciplinary across ≥6 **unrelated** domains
3. Not an Ontological Overfitting case (1:1 map/territory anti-pattern)

**Families (9)**:
1. **Structural** (9): Node, Edge, Network, Hierarchy, Module, Interface, Boundary, Layer, Component
2. **Flow** (8): Flow, Gradient, Diffusion, Convection, Flux, Channel, Pathway, Conduit
3. **Informational** (7): Signal, Encoding, Noise, Feedback, Information, Message, Code
4. **Energetic** (8): Source, Sink, Reservoir, Potential, Dissipation, Work, Energy, Power
5. **Temporal** (8): Cycle, Rhythm, Period, Phase, Duration, Timescale, Delay, Hysteresis
6. **Regulatory** (7): Homeostasis, Setpoint, Controller, Actuator, Sensor, Regulation, Adaptation
7. **Emergent** (8): Attractor, Bifurcation, Criticality, Emergence, Self-Organization, Symmetry, Asymmetry, Threshold
8. **Relational** (8): Coupling, Decoupling, Resonance, Amplification, Attenuation, Saturation, Convergence, Divergence
9. **Contextual** (6+): Envelope, Context, Constraint, Affordance, Niche, Scale, **Modelisation** ← new, **TriadicBalance** ← new

**Combo Mechanisms**:
- `m2:GenericConceptCombo` (owl:Class in M2, instances in M1_CoreConcepts): produced by `Fm2 : GenericConcept²⁺ → GenericConceptCombo` (≥2 named concepts); validated across ≥6 domains
- `m2:DomainConceptCombo` (owl:Class in M2, instances in M1 extensions): produced by `Fm1m2 : Domain⁺, GenericConcept⁺ → DomainConceptCombo` — a HYBRID of ≥1 Domain and ≥1 GenericConcept
- **A combo's formula IS the function signature.** No monoidal formula, no monoidal expansion — `Fm2`/`Fm1m2` are FUNCTIONS, not functors (emergence is non-compositional). Arguments = named concepts from M2 or M1_CoreConcepts only, comma-juxtaposed, never primitives, never joined by ×/+/\|. `Fm1` does not exist. See `StructuralGrammar/Functional_Grammar_Model.md`.

---

## 🌐 M1 — Knowledge Field Extensions

### M1_Domains.jsonld — 19 Registered Domains

| Domain | Example Poclets |
|--------|-----------------|
| Biology | RAAS, AdaptiveImmuneResponse, ButterflyMetamorphosis, CellSignalingModes, Kidneys |
| Chemistry | FireTriangle, PhaseTransition |
| Physics | PhaseTransition, Transistor, VCO |
| Electronics | Transistor, VCO |
| Economics | KindlebergerMinsky |
| Photography | ExposureTriangle |
| Music Theory | CounterPoint |
| Game Theory | MtgColorWheel |
| Geology | PlateTectonics |
| Engineering | FourStrokeEngine |
| Mythology | Yggdrasil |
| Cybernetics | Vsm |
| Semiotics | Iching |
| Art | ColorSynthesis, TVTestPattern |
| Blockchain | NakamotoConsensus |
| Pedagogy | TPACK |
| Physiology | BloodPressureControl |
| Nuclear Engineering | NuclearReactorsTypology |
| **Business Modeling** ← new | Bmc (BMC lifecycle simulation) |

### M1 Extensions (13 active)

| File | Version | Concepts |
|------|---------|---------|
| `M1_Biology.jsonld` | v1.0.0 | 24 concepts + KFCombo instances |
| `M1_Chemistry.jsonld` | v1.0.0 | Bond types, reaction kinetics |
| `M1_Physics.jsonld` | v1.0.0 | Thermodynamics, quantum |
| `M1_Electronics.jsonld` | v1.0.0 | Analog circuits, semiconductors |
| `M1_Economics.jsonld` | v1.0.0 | Financial crisis phases |
| `M1_Optics.jsonld` | v1.0.0 | Light interaction modes |
| `M1_Photography.jsonld` | v1.0.0 | Exposure triangle concepts |
| `M1_Music.jsonld` | v1.0.0 | Counterpoint, harmony |
| `M1_Mythology.jsonld` | v1.0.0 | Cosmological structures |
| `M1_SystemicModeling.jsonld` | v1.0.0 | VSM, cybernetics |
| `M1_Education.jsonld` | v1.0.0 | TPACK framework |
| `M1_Geology.jsonld` | v1.0.0 | Plate tectonics |
| **`M1_BusinessModeling.jsonld`** ← new | v1.0.0 | BM Canvas, lifecycle phases, transitions |

---

## 📦 M0 — Instance Types & Corpus (34 validated)

### Repository Structure

| Sub-folder | Type | Count | Examples |
|-----------|------|-------|---------|
| `instances/poclets/` | `m3:Poclet` | **26** | FireTriangle, RAAS, Ptoe, NakamotoConsensus |
| `instances/systemic-frameworks/` | `m3:SystemicFramework` | **3** | Vsm, Triz, **Bmc** ← new |
| `instances/symbolic-system-grammars/` | `m3:SymbolicSystemGrammar` | **1** | Iching |
| `instances/tscg-tools/` | `m3:TscgTool` | **3** (+1 stub) | TscgOntologyExplorer, TscgPocletMiner, TscgPocletGenerator |

**Total**: 34 validated + 1 stub (TscgOntologyAPIServer)

### Instance Types

| Type | `m3:ontologyType` | Count |
|------|-------------------|-------|
| Poclet | `m3:Poclet` | 26 |
| SystemicFramework | `m3:SystemicFramework` | 3 |
| SymbolicSystemGrammar | `m3:SymbolicSystemGrammar` | 1 |
| TscgTool | `m3:TscgTool` | 3 (+1 stub) |
| TransDisclet | `m3:TransDisclet` | 0 (future) |
| Enigma | `m3:Enigma` | 0 (future) |

⚠️ `m3:ontologyType` is the **sole valid property** for declaring instance type.
⚠️ NEVER use `m3:ontologyCategory` or `m2:ontologyCategory`.

### 🆕 Bmc SystemicFramework

**Path**: `instances/systemic-frameworks/Bmc/`
**Ontology**: `M0_BmcSimulation.jsonld` (+ `static/src/M0_BmcSimulation.jsonld.js` JS wrapper for `file://`)
**Simulation**: `instances/systemic-frameworks/Bmc/static/M0_Bmc.html`

Key architectural features:
- **`sim:` namespace** for simulation-specific vocabulary (SimulationCase, Phase, Transition, TransitionOutcome)
- **12 SimulationCases**: Netflix, Nokia, Nintendo, Apple, Amazon, Google, Microsoft, IBM, Kodak, Xerox, Michelin, Airbnb
- **34 documented transitions** with `sim:outcome` enum: `sim:outcome.Success` / `sim:outcome.Failure` / `sim:outcome.InProgress`
- **`sim:keyYears` + `sim:phaseYears`**: temporal anchors per case × phase
- **Fetch strategy**: `fetch(JSONLD_URL)` → GitHub raw URL, fallback to local `.jsonld.js`
- **`exportAsJsonLD()`**: exports pure `.jsonld` from JS wrapper

### SHACL Grammar (v1.5)

**9 Mandatory Constraints**:

| Property | Constraint |
|----------|-----------|
| `rdfs:label` | xsd:string |
| `rdfs:comment` | xsd:string |
| `dcterms:creator` | EXACT: "Echopraxium with the collaboration of Claude AI" |
| `m3:ontologyType` | sh:class m3:OntologyType (mandatory, NOT m3:ontologyCategory) |
| `m1:domain` | xsd:string or array |
| `owl:versionInfo` | pattern `\d+\.\d+\.\d+` |
| `owl:imports` | sh:nodeKind sh:IRI |
| `@type` | MUST be "owl:Ontology" for @graph[0] |
| `@id` | sh:nodeKind sh:IRI |

**10 Forbidden Patterns**: `tscg:*`, `m0:domain`, `m3:ontologyCategory`, `m2:ontologyCategory`, `dcterms:title`, `dcterms:description`, `m0:version`, relative URLs in @context, custom @type classes, bare `rdf:type` with Poclet value.

---

## 📊 Poclet Corpus (26 total)

| Domain | Count | Poclets |
|--------|-------|---------|
| Biology | 6 | RAAS, AdaptativeImmuneResponse, ButterflyMetamorphosis, CellSignalingModes, TrophicPyramid, Kidneys |
| Physics/Chemistry | 3 | FireTriangle, PhaseTransition, FourStrokeEngine |
| Electronics | 2 | Transistor, Vco |
| Economics | 1 | KindlebergerMinsky |
| Photography | 1 | ExposureTriangle |
| Music | 1 | CounterPoint |
| Game Theory | 1 | MtgColorWheel |
| Geology | 1 | PlateTectonics |
| Blockchain | 1 | NakamotoConsensus |
| Art | 2 | ColorSynthesis (federated), TvTestPattern |
| Mythology | 1 | Yggdrasil |
| Pedagogy | 1 | Tpack |
| Nuclear Engineering | 1 | NuclearReactorsTypology |
| Physiology | 1 | BloodPressureControl |
| Neuroscience | 1 | ComplexChemicalSynapse |
| Chemistry (elements) | 1 | Ptoe (BabylonJS 3D) |

---

## 🔧 Development Workflow

### Creating a New Instance (Pipeline)

1. **Étape 1 — Proposition**: ASFID/REVOI feasibility + domain identification
2. **Étape 2 — Analysis**: Epistemic alignment (δ₁ calculation), M2 concept mapping, M1 extension identification
3. **Étape 3 — Modeling**: JSON-LD ontology + README.md
4. **Étape 4 — Simulation** (optional): Standalone HTML (p5.js Canvas2D or BabylonJS 3D)

### Key Principles

- **M2 Purity**: Only universally transdisciplinary atomic patterns (≥6 unrelated domains). Anti-pattern: Ontological Overfitting (1:1 map/territory).
- **R = Representability** (NEVER Reproducibility) — persistent error to avoid
- **Absolute URLs**: All @context namespaces must use full GitHub URLs
- **No tscg: namespace**: Forbidden in M0 instances (use m0:)
- **Author Consistency**: EXACT string "Echopraxium with the collaboration of Claude AI"
- **F ≥ 0.1 Axiom**: Flow ≥ 0.1 (no perfectly closed systems)
- **Changelog**: Max 3 rolling entries
- **M0_Common.jsonld**: Canonical source for all shared M0 score properties — never duplicate

---

## 📝 Critical Reminders (v16.2.0)

1. **REVOI order**: R-E-V-O-I (NEVER spell it ORIVE)
2. **R = Representability**: NEVER "Reproducibility"
3. **M3 formalism**: Lambek calculus / monoidal product `⊗` — NOT Hilbert space / tensor product
4. **M3_GenesisGrammar.jsonld**: canonical name — `M3_GenesisSpace.jsonld` is FORBIDDEN
5. **St/It indexation**: mandatory in hybrid formulas containing `|`
6. **δ₂ / SFE**: `focalScore = stereopsicDepth × (1 − |focalBias|)` — only when `focalApplicable = true`
7. **focalBias sign**: positive = Hyperopic (Map bias), negative = Myopic (Territory bias)
8. **sim: namespace**: used ONLY in Bmc simulation ontology — not in generic M0 instances
9. **`m3:ontologyType`**: sole valid type property — NOT `m3:ontologyCategory`
10. **dcterms:creator**: EXACT match — SHACL enforced
11. **Changelog**: Maximum 3 entries (rolling window)
12. **UTF-8**: Mathematical symbols (⊗, →, Φ, Ψ, _^, _$) — verify after edits

---

## 📚 Key Files Reference

**Core Ontologies**:
- `M3_GenesisGrammar.jsonld` — Bicephalous foundation (Structural Grammar / Lambek calculus)
- `M3_BicephalousPerspective.jsonld` — Gs stereopsis grammar (TKSL, poles, TriadicBalance) v1.3.0
- `M2_GenericConcepts.jsonld` — 80 atomic patterns + Combo classes v16.14.0
- `M1_CoreConcepts.jsonld` — GenericConceptCombo instances + KF roots v2.6.1
- `M1_Domains.jsonld` — 19 registered domains
- `M0_Common.jsonld` — Canonical shared M0 properties (scores, focal, spectral)

**Bmc SystemicFramework**:
- `instances/systemic-frameworks/Bmc/M0_BmcSimulation.jsonld` — Pure JSON-LD (SHACL-validable)
- `instances/systemic-frameworks/Bmc/static/M0_Bmc.html` — Standalone simulation
- `instances/systemic-frameworks/Bmc/static/src/M0_BmcSimulation.jsonld.js` — JS wrapper

**Validation**:
- `M0_Instances_Schema.shacl.ttl` — SHACL grammar v1.5 (9 mandatory constraints)

**Migration Tools**:
- `automated_migration_easy_instances.py` v2.7.0
- `migrate_m0_scores_v1_3.py` — Score convention Option B migration
- `check_m0_instances.py` — Corpus health check

**Documentation**:
- `docs/CoreHypotheses/OntologicalOverfitting.md` — Anti-pattern documentation
- `docs/CoreHypotheses/_00_TSCG_as_StereoscopicGlasses.md`
- `docs/CoreHypotheses/_01_Narcissus_and_Icarus_as_Safeguards.md`
- `Structural_Grammar_Foundation.md` — Lambek calculus formalism

---

**Version**: 16.2.0
**Last Updated**: 2026-06-24
**Corpus**: 34 validated instances (100% SHACL-compliant)
**Author**: Echopraxium with the collaboration of Claude AI
