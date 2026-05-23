# TSCG Smart Prompt v16.0.0 - Complete Migration & SHACL Compliance

**Framework**: TSCG (Transdisciplinary System Construction Game)  
**Version**: 16.0.0  
**Date**: 2026-04-20  
**Author**: Echopraxium with the collaboration of Claude AI  

**Major Updates v15.10.1→v16.0.0**:
- ✅ **Complete M0 Migration**: 26/26 instances 100% SHACL-compliant (v2.7.0)
- ✅ **SHACL Grammar v1.0 FINAL**: Extracted from 100% corpus coverage (26 instances analyzed)
- ✅ **Namespace Standardization**: All relative URLs → absolute URLs in @context (pyshacl requirement)
- ✅ **REVOI Terminology**: R=Representability (NEVER Reproducibility) - ORIVE is obsolete
- ✅ **M1_Domains.jsonld**: 19 registered domains with hierarchical structure
- ✅ **Automated Migration Tools**: v2.7.0 script + 3 specialized fix scripts
- ✅ **Instance Types Support**: Poclets (24) + SymbolicSystemGrammars (1) + SystemicFrameworks (1)
- ✅ **Forbidden tscg: namespace**: All instances migrated to m0: namespace

---

## 🎯 Context: What is TSCG?

TSCG (Transdisciplinary System Construction Game) is an **ontological framework** for analyzing and modeling complex systems across disciplines. It provides a rigorous mathematical foundation for understanding systemic patterns through a **bicephalous architecture** that combines Territory measurement (Eagle Eye/ASFID) with Map construction (Sphinx Eye/REVOI).

### Core Principle (Korzybski Extended)
**"The map is not the territory, but the map influences how we observe the territory"**
- Classic (Korzybski, 1933): Map ≠ Territory
- TSCG Extension: **Bidirectional feedback loop** formalized through Σ coupling matrix

---

## 📐 Authoring & File Conventions (CRITICAL)

These rules apply to **all generated ontology files** (.jsonld). The conversation with Claude may be in French, but all generated files must be in **English**.

### 1. Author field (MANDATORY - SHACL Enforced)
All `.jsonld` files MUST carry **EXACTLY** this author declaration:
```json
"dcterms:creator": "Echopraxium with the collaboration of Claude AI"
```
⚠️ **CRITICAL**: No variants allowed (e.g., "Claude Sonnet 4.6", "Claude AI Pro") - SHACL validation will fail.

### 2. URI root (MANDATORY - SHACL Enforced)
The canonical base URI for the TSCG repository is:
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
```

### 3. @base — Short IRIs for M0 and M1 files (MANDATORY)
All `M0_xxx.jsonld`, `M1_CoreConcepts.jsonld`, and `M1_xxx.jsonld` extension files must use `@base` in their `@context`:
```json
{
  "@context": {
    "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dcterms": "http://purl.org/dc/terms/"
  }
}
```

⚠️ **CRITICAL**: Namespaces m1/m2/m3 MUST use **ABSOLUTE URLs**, NOT relative URLs like `"M1_CoreConcepts.jsonld#"` - pyshacl cannot resolve relative URLs and validation will fail.

### 4. Forbidden namespace: tscg:
The `tscg:` namespace is **FORBIDDEN** in all M0 instance files. Use `m0:` for instance-specific properties.

❌ **WRONG**:
```json
"tscg:domain": "Biology",
"tscg:primaryPhenomenon": "...",
"@type": "tscg:Poclet"
```

✅ **CORRECT**:
```json
"m1:domain": "Biology",
"m0:primaryPhenomenon": "...",
"@type": "owl:NamedIndividual"
```

### 5. M1 extension IRI pattern
When referencing M1 domain extensions in `M0_xxx.jsonld` files:
```
M1_extensions/extension_name/M1_ExtensionName.jsonld
```
**Examples**:
- `M1_extensions/biology/M1_Biology.jsonld`
- `M1_extensions/chemistry/M1_Chemistry.jsonld`
- `M1_extensions/optics/M1_Optics.jsonld`
- `M1_extensions/economics/M1_Economics.jsonld`

### 6. Changelog discipline
In the `m2:changelog` field, **keep only the 3 most recent entries**.

---

## 🗂️ Framework Architecture (4 Layers)

```
M3_GenesisSpace.jsonld      ← Mathematical foundation (ASFID ⊕ REVOI, 10D Hilbert space)
        ↓ imports
M2_GenericConcepts.jsonld   ← Universal atomic patterns (75 GenericConcepts, 9 families)
                              + m2:GenericConceptCombo (class) + m2:KnowledgeFieldConceptCombo (class)
        ↓ instantiates (combo classes)
M1_CoreConcepts.jsonld      ← KnowledgeField root concepts + GenericConceptCombo instances
M1_Domains.jsonld           ← Domain registry (19 registered domains with hierarchies)
M1_extensions/biology/M1_Biology.jsonld
M1_extensions/chemistry/M1_Chemistry.jsonld
M1_extensions/economics/M1_Economics.jsonld  …
        ↓ instantiates
instances/poclets/RAAS/M0_RAAS.jsonld, …             ← Concrete systems (24 Poclets)
instances/symbolic-system-grammars/Iching/M0_Iching.jsonld  ← Symbolic grammars
instances/systemic-frameworks/Vsm/M0_Vsm.jsonld      ← External methodologies
instances/tscg-tools/…                               ← TSCG tooling instances
```

---

## 🗃️ Repository Structure — instances/

The `instances/` folder contains **26 validated instances** organized by type:

| Sub-folder | Content | Count | Examples |
|---|---|---|---|
| `instances/poclets/` | Single-domain concrete poclets (M0) | **24** | RAAS, FireTriangle, NakamotoConsensus |
| `instances/symbolic-system-grammars/` | Formal symbolic grammars | **1** | Iching (I Ching hexagram system) |
| `instances/systemic-frameworks/` | External methodologies | **1** | Vsm (Viable System Model - Stafford Beer) |
| `instances/tscg-tools/` | Reflexive tools (TSCG as domain) | **0** | (Future: TscgPocletMiner ElectronJS app) |

**Total M0 Instances**: 26 (100% SHACL-compliant as of 2026-04-20)

> ⚠️ **TscgTool vs Poclet**: TscgTools are reflexive (TSCG is the domain) and do not require a domain-specific M1 extension. Poclets validate single-domain systems and reference a M1 extension.

---

## 🧬 M3 — Bicephalous Genesis Space

### Dual-Eye Architecture (Eagle ⊕ Sphinx)

TSCG employs a **bicephalous scoring system** that evaluates systems from two complementary perspectives:

| Eye | Acronym | Full Name | Perspective | Dimensions |
|-----|---------|-----------|-------------|------------|
| 🦅 **Eagle Eye** | **ASFID** | Attractor-Structure-Flow-Information-Dynamics | **Territory** (empirical reality) | A, S, F, I, D |
| 🦁 **Sphinx Eye** | **REVOI** | Representability-Evolvability-Verifiability-Observability-Interoperability | **Map** (model quality) | R, E, V, O, I |

⚠️ **CRITICAL TERMINOLOGY**:
- **R in REVOI = Representability** (semantic encodability/decodability)
- **NEVER use "Reproducibility"** - this is a persistent error
- **ORIVE is OBSOLETE** - always use REVOI (correct acronym order)

### Dimension Definitions

**ASFID (Territory / Eagle Eye)**:
- **A (Attractor)**: System's equilibrium points, stable states, basins of attraction
- **S (Structure)**: Static organization, topology, connectivity patterns, architectural invariants
- **F (Flow)**: Material/energy/information throughput, flux dynamics, transport phenomena
- **I (Information)**: Signal processing, encoding, communication channels, cybernetic loops
- **D (Dynamics)**: Temporal evolution, feedback loops, phase transitions, emergent behaviors

**REVOI (Map / Sphinx Eye)**:
- **R (Representability)**: Semantic encodability in formal notation systems (equations, diagrams, ontologies)
- **E (Evolvability)**: Adaptive capacity, parameter tunability, version migration paths
- **V (Verifiability)**: Empirical testability, falsifiability (Popperian), experimental validation protocols
- **O (Observability)**: Measurability of state variables, instrumentation accessibility, data availability
- **I (Interoperability)**: Cross-framework translation, compatibility with established methodologies

### Epistemic Gap (δ₁)

The **epistemic gap** quantifies the misalignment between Territory (ASFID) and Map (REVOI):

```
δ₁ = ||ASFID_mean - REVOI_mean|| / √2
```

**Spectral Classes** (empirically derived from corpus analysis):
- **Coherent**: δ₁ ∈ [0, 0.05) — Near-perfect alignment
- **OnCriticalLine**: δ₁ ∈ [0.05, 0.15) — Productive tension
- **Liminal**: δ₁ ∈ [0.15, 0.30) — Significant gap requires attention
- **Enigmatic**: δ₁ ∈ [0.30, 1.0) — Fundamental modeling challenges

---

## 🧩 M2 — GenericConcepts (Universal Atomic Patterns)

**M2 Status**: 75 atomic GenericConcepts organized into 9 families (strictly transdisciplinary).

**Families**:
1. **Structural**: Node, Edge, Network, Hierarchy, Module, Interface, Boundary, Layer, Component
2. **Flow**: Flow, Gradient, Diffusion, Convection, Flux, Channel, Pathway, Conduit
3. **Informational**: Signal, Encoding, Noise, Feedback, Information, Message, Code
4. **Energetic**: Source, Sink, Reservoir, Potential, Dissipation, Work, Energy, Power
5. **Temporal**: Cycle, Rhythm, Period, Phase, Duration, Timescale, Delay, Hysteresis
6. **Regulatory**: Homeostasis, Setpoint, Controller, Actuator, Sensor, Regulation, Adaptation
7. **Emergent**: Attractor, Bifurcation, Criticality, Emergence, Self-Organization, Symmetry, Asymmetry, Threshold
8. **Relational**: Coupling, Decoupling, Resonance, Amplification, Attenuation, Saturation, Convergence, Divergence
9. **Contextual**: Envelope, Context, Constraint, Affordance, Niche, Scale

**Combo Mechanisms**:
- **m2:GenericConceptCombo** (owl:Class in M2, instances in M1_CoreConcepts): Synergistic combinations validated across ≥6 domains
- **m2:KnowledgeFieldConceptCombo** (owl:Class in M2, instances in M1 extensions): Domain-specific concept combinations

**M2 Purity Constraint**: Only universally transdisciplinary atomic patterns belong in M2. Domain-specific or combo patterns live in M1.

---

## 🌐 M1 — Knowledge Field Extensions & Domain Registry

### M1_Domains.jsonld (v1.1.0)

**Registered Domains** (19 total as of 2026-04-20):

| Domain | Subdomains | Related Domains | Example Poclet |
|--------|------------|-----------------|----------------|
| **Biology** | Physiology, Immunology, Developmental Biology, Ecology, Molecular Biology, Neuroscience | Chemistry, Medicine | RAAS, AdaptiveImmuneResponse, ButterflyMetamorphosis, TrophicPyramid |
| **Chemistry** | Physical Chemistry, Thermodynamics, Reaction Kinetics, Combustion | Physics, Materials Science | FireTriangle, PhaseTransition |
| **Physics** | Thermodynamics, Electromagnetism, Quantum Mechanics, Condensed Matter | Engineering, Mathematics | PhaseTransition, Transistor, VCO |
| **Electronics** | Analog Circuits, Signal Processing, Semiconductors | Physics, Engineering | Transistor, VCO |
| **Computer Science** | Algorithms, Data Structures, Systems | Mathematics, Engineering | — |
| **Economics** | Macroeconomics, Financial Markets, Behavioral Economics | Game Theory, Sociology | KindlebergerMinsky |
| **Optics** | Geometric Optics, Physical Optics, Photonics | Physics, Photography | — |
| **Photography** | Exposure Control, Imaging Systems | Optics, Art | ExposureTriangle |
| **Music Theory** | Counterpoint, Harmony, Composition | Mathematics, Acoustics | CounterPoint |
| **Game Theory** | Strategic Interaction, Nash Equilibria | Economics, Mathematics | MtgColorWheel |
| **Geology** | Plate Tectonics, Geophysics, Mineralogy | Physics, Earth Sciences | PlateTectonics |
| **Engineering** | Systems Engineering, Control Theory | Physics, Mathematics | FourStrokeEngine |
| **Mythology** | Comparative Mythology, Symbolic Systems | Anthropology, Psychology | Yggdrasil |
| **Cybernetics** | Management Cybernetics, Organizational Theory, Systems Theory | Engineering, Biology | Vsm (Viable System Model) |
| **Semiotics** | Symbolic Systems, Sign Theory | Linguistics, Philosophy | Iching (I Ching) |
| **Art** | Color Theory, Visual Perception | Psychology, Optics | ColorSynthesis, TVTestPattern |
| **Blockchain** | Cryptography, Distributed Systems, Consensus Algorithms, Decentralized Networks | Computer Science, Economics, Game Theory | NakamotoConsensus |
| **Pedagogy** | Instructional Design, Educational Technology | Psychology, Cognitive Science | TPACK |
| **Physiology** | Cardiovascular System, Endocrinology, Homeostasis | Biology, Medicine | BloodPressureControl, RAAS, CellSignalingModes |

**Domain Hierarchy Rules**:
- Most domains have 3-7 subdomains
- Related domains share conceptual or methodological overlap
- Each domain references at least 1 example poclet when available

### M1 Extensions (Active)

**Implemented Extensions**:
- `M1_Biology.jsonld` (v1.0.0) — 24 concepts + KnowledgeFieldConceptCombo instances
- `M1_Chemistry.jsonld` (v1.0.0) — Chemical bond types, reaction kinetics concepts
- `M1_Optics.jsonld` (v1.0.0) — Light interaction modes, optical phenomena
- `M1_Photography.jsonld` (v1.0.0) — Exposure triangle concepts
- `M1_Mythology.jsonld` (v1.0.0) — Cosmological concepts (Yggdrasil)
- `M1_Economics.jsonld` (v1.0.0) — Financial crisis phases, market dynamics

---

## 📦 M0 — Instance Types & Validation

### Instance Types (m3:ontologyType)

TSCG defines 5 instance types at M0 level:

| Type | m3:ontologyType | Description | Count | Examples |
|------|-----------------|-------------|-------|----------|
| **Poclet** | `m3:Poclet` | Minimal complete validated system model | **24** | RAAS, FireTriangle, NakamotoConsensus |
| **SymbolicSystemGrammar** | `m3:SymbolicSystemGrammar` | Formal symbolic grammar systems | **1** | Iching (64 hexagrams) |
| **SystemicFramework** | `m3:SystemicFramework` | Established external methodologies | **1** | Vsm (Viable System Model) |
| **TransDisclet** | `m3:TransDisclet` | Natively cross-disciplinary (structural homology ≥2 domains) | **0** | (Future: Electromagnetic/Acoustic wave equations) |
| **Enigma** | `m3:Enigma` | Apparent-impossibility models with mandatory ternary mediators | **0** | (Future: Schrödinger's Cat, Maxwell's Demon) |

### SHACL Grammar v1.0 FINAL

**Extraction Methodology**:
- **Corpus Coverage**: 100% (26/26 instances analyzed in 6 batches)
- **Consensus Threshold**: 70% for mandatory constraints
- **Analysis Period**: 2026-04-18 to 2026-04-20

**Mandatory Properties** (9 total):

| Property | Constraint | Consensus | Notes |
|----------|------------|-----------|-------|
| `rdfs:label` | xsd:string (mandatory) | 100% | Instance display name |
| `rdfs:comment` | xsd:string (mandatory) | 100% | Brief description |
| `dcterms:creator` | EXACT string match | 100% | MUST be "Echopraxium with the collaboration of Claude AI" |
| `m3:ontologyType` | sh:class m3:OntologyType | 96% | {"@id": "m3:Poclet"} or other types |
| `m1:domain` | xsd:string or array | 73% | Registered in M1_Domains.jsonld |
| `owl:versionInfo` | xsd:string (pattern: `\d+\.\d+\.\d+`) | 100% | Semantic versioning |
| `owl:imports` | sh:nodeKind sh:IRI | 92% | Array of ontology imports |
| `@type` | MUST be "owl:Ontology" | 100% | For @graph[0] only |
| `@id` | sh:nodeKind sh:IRI | 100% | Unique identifier |

**Forbidden Patterns** (10 total):

| Pattern | Reason | Violations Found |
|---------|--------|------------------|
| `tscg:*` namespace | Use m0: instead | 141 (BloodPressureControl - fixed) |
| `m0:domain` | Use m1:domain | 15 instances (all fixed) |
| `m2:ontologyCategory` | Use m3:ontologyType | 8 instances (all fixed) |
| `m3:ontologyCategory` | Use m3:ontologyType | 3 instances (all fixed) |
| `dcterms:title` | Use rdfs:label | 12 instances (all fixed) |
| `dcterms:description` | Use rdfs:comment | 8 instances (all fixed) |
| `m0:version` | Use owl:versionInfo | 2 instances (all fixed) |
| `rdf:type` with Poclet value | Redundant with m3:ontologyType | 4 instances (all fixed) |
| Relative URLs in @context | pyshacl requires absolute URLs | 26 instances (all fixed) |
| Custom @type classes in M0 | Use owl:NamedIndividual | 2 instances (ButterflyMetamorphosis - fixed) |

### Migration Tools

**Automated Migration** (`automated_migration_easy_instances.py` v2.7.0):
- Supports 3 instance types: Poclets, SymbolicSystemGrammars, SystemicFrameworks
- Applies 15+ transformation rules automatically
- SHACL validation integrated
- Backup system (timestamped migration_backups/)
- Success rate: 25/26 instances (96%)

**Manual Fix Scripts** (for complex cases):
- `fix_bloodpressure_namespace.py` — Replaces tscg: → m0: (141 violations), fixes @type, corrects ORIVE→REVOI
- `fix_butterfly_classes.py` — Removes custom OWL classes, converts instances to owl:NamedIndividual
- `fix_cellsignaling_inline.py` — Extracts inline components to @graph objects

**Validation**:
```bash
pyshacl -s M0_Instances_Schema.shacl.ttl -df json-ld M0_PocletName.jsonld
```

---

## 📊 Validated Poclet Corpus (24 Total)

**By Domain**:

| Domain | Count | Poclets |
|--------|-------|---------|
| **Biology** | 7 | RAAS, AdaptiveImmuneResponse, ButterflyMetamorphosis, CellSignalingModes, ComplexChemicalSynapse, TrophicPyramid, Kidneys |
| **Physics/Chemistry** | 3 | FireTriangle, PhaseTransition, FourStrokeEngine |
| **Electronics** | 2 | Transistor, VCO |
| **Economics** | 1 | KindlebergerMinsky |
| **Photography** | 1 | ExposureTriangle |
| **Music** | 1 | CounterPoint |
| **Game Theory** | 1 | MtgColorWheel |
| **Geology** | 1 | PlateTectonics |
| **Blockchain** | 1 | NakamotoConsensus |
| **Art** | 2 | ColorSynthesis (federated), TVTestPattern |
| **Mythology** | 1 | Yggdrasil |
| **Pedagogy** | 1 | TPACK |
| **Nuclear Engineering** | 1 | NuclearReactorsTypology |
| **Physiology** | 1 | BloodPressureControl |

**Special Instance Types**:
- **SymbolicSystemGrammar**: Iching (64 hexagrams from I Ching)
- **SystemicFramework**: Vsm (Viable System Model - Stafford Beer)

---

## 🔧 Development Workflow

### Creating a New Poclet

1. **Proposition Phase** — ASFID/REVOI feasibility analysis
2. **Analysis Phase** — Epistemic alignment check (δ₁ calculation)
3. **Modeling Phase** — JSON-LD ontology + README
4. **Validation Phase** — SHACL validation
5. **Simulation Phase** (optional) — Standalone HTML interactive

### Key Principles

- **M2 Purity**: Only universally transdisciplinary atomic patterns
- **REVOI not ORIVE**: R=Representability (semantic encodability)
- **Absolute URLs**: All @context namespaces must use full GitHub URLs
- **No tscg: namespace**: Forbidden in M0 instances (use m0:)
- **Author Consistency**: EXACT string "Echopraxium with the collaboration of Claude AI"
- **F ≥ 0 Axiom**: Flow dimension cannot be negative (universal openness)

---

## 📝 Critical Reminders

1. **REVOI Dimension Order**: R-E-V-O-I (NEVER spell it ORIVE)
2. **R = Representability**: NEVER say "Reproducibility" (persistent error)
3. **dcterms:creator**: EXACT match required by SHACL (no variants)
4. **@context URLs**: MUST be absolute (pyshacl cannot resolve relative)
5. **tscg: namespace**: FORBIDDEN in all M0 instances
6. **m3:ontologyType**: NOT m2:ontologyCategory or m3:ontologyCategory
7. **Changelog**: Maximum 3 entries (rolling window)
8. **UTF-8 Encoding**: Mathematical symbols (⊗, →, Φ, Ψ) are fragile - verify after edits

---

## 📚 Key Files Reference

**Core Ontologies**:
- `M3_GenesisSpace.jsonld` — Bicephalous foundation (ASFID ⊕ REVOI)
- `M2_GenericConcepts.jsonld` — 75 atomic patterns + Combo classes
- `M1_CoreConcepts.jsonld` — Root concepts + GenericConceptCombo instances
- `M1_Domains.jsonld` — 19 registered domains with hierarchies

**Validation**:
- `M0_Instances_Schema.shacl.ttl` — SHACL grammar v1.0 FINAL

**Migration Tools**:
- `automated_migration_easy_instances.py` v2.7.0 — Automated realignment
- `fix_bloodpressure_namespace.py` — tscg: namespace violations
- `fix_butterfly_classes.py` — Custom OWL classes removal
- `fix_cellsignaling_inline.py` — Inline components extraction

**Documentation**:
- `TSCG_Grammar_Extraction_Final_Report.md` — Complete SHACL analysis
- `M0_Realignment_Tracker.md` — Instance-by-instance migration status
- `TSCG_Smart_Prompt_v16_0_0.md` — This file

---

**Version**: 16.0.0  
**Last Updated**: 2026-04-20  
**Migration Status**: 26/26 instances (100% SHACL-compliant)  
**Author**: Echopraxium with the collaboration of Claude AI
