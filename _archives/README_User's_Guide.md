# TSCG Framework
## Transdisciplinary System Construction Game

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Echopraxium%2Ftscg-181717?logo=github)](https://github.com/Echopraxium/tscg)
[![Version](https://img.shields.io/badge/Version-16.0.0-green.svg)](https://github.com/Echopraxium/tscg/releases)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18471860.svg)](https://doi.org/10.5281/zenodo.18471860)

A sophisticated **transdisciplinary ontological framework** for modeling complex systems through universal patterns. TSCG provides a four-layer architecture (M3→M2→M1→M0) built on a **bicephalous foundation** that distinguishes Territory (measurement via ASFID) from Map (representation via REVOI).

**Author:** Echopraxium with the collaboration of Claude AI  
**License:** BSD 3-Clause (source code) | CC BY 4.0 (documentation & research article)  
**Research Paper:** [Zenodo v3.0 Preprint](https://doi.org/10.5281/zenodo.18471860) | v4.0 submission in progress

---

## 🎯 What is TSCG?

TSCG (Transdisciplinary System Construction Game) is a **formalized ontological framework** for:
- **Modeling complex systems** across disciplines (physics, biology, economics, mythology, etc.)
- **Identifying universal patterns** through ~80 transdisciplinary GenericConcepts
- **Measuring systemic coherence** via dual epistemic lenses (ASFID/REVOI)
- **Creating validated instances** (Poclets) with interactive HTML simulations
- **Enabling AI-assisted analysis** through multi-backend LLM tooling (TscgPocletMiner)

The framework bridges **Territory** (what exists empirically) and **Map** (how we represent it) through a rigorous mathematical foundation inspired by differential geometry and category theory.

---

## 🏗️ Architecture Overview

### The Bicephalous Foundation (M3 Genesis Space)

TSCG is built on a **dual-head** metaphor inspired by the Mesopotamian deity Anzû:
- **🦅 Eagle Eye (ASFID)**: Measures Territory through 5 dimensions  
  **A**ttractor | **S**tructure | **F**low | **I**nformation | **D**ynamics
- **🦁 Sphinx Eye (REVOI)**: Constructs Map through 5 dimensions  
  **R**epresentability | **E**volvability | **V**erifiability | **O**bservability | **I**nteroperability

Together, these perspectives create **binocular vision** — a complete understanding of systems that reconciles empirical measurement with epistemological representation.

### Four-Layer Hierarchy

```
M3 (Genesis Space)      → Bicephalous foundation: ASFID/REVOI dimensions
M2 (GenericConcepts)    → ~80 atomic transdisciplinary patterns (9 families)
M1 (CoreConcepts)       → Domain-specific extensions (11 disciplines)
M0 (Instances)          → Concrete validated systems (23+ Poclets)
```

**Key Innovation:** M2 contains **only universally transdisciplinary** atomic patterns. Domain-specific combinations migrate to M1 extensions (biology, chemistry, economics, electronics, energy_generators, music, mythology, optics, photography, physics, education).

---

## 📦 Repository Structure

```
tscg/
├── ontology/                       # Reference ontologies (JSON-LD + Turtle)
│   ├── M3_GenesisSpace.jsonld      # Bicephalous foundation
│   ├── M3_EagleEye.jsonld          # ASFID dimensions (Territory)
│   ├── M3_SphinxEye.jsonld         # REVOI dimensions (Map)
│   ├── M2_GenericConcepts.jsonld   # ~80 universal patterns
│   ├── M1_CoreConcepts.jsonld      # Core domain concepts
│   ├── M1_Domains.jsonld           # Domain registry (centralized)
│   ├── M1_extensions/              # 11 domain-specific extensions
│   └── docs/                       # Ontology documentation & formulas
│
├── instances/                      # M0 Layer - Concrete Systems
│   ├── poclets/                    # 23+ validated system models
│   │   ├── FireTriangle/           # Combustion triangle (canonical simulation)
│   │   ├── MtgColorWheel/          # Magic: The Gathering color system
│   │   ├── FourStrokeEngine/       # Internal combustion cycle
│   │   ├── NakamotoConsensus/      # Bitcoin consensus mechanism
│   │   ├── CounterPoint/           # Musical counterpoint theory
│   │   └── ...                     # 18+ additional poclets
│   │
│   ├── tscg-tools/                 # Meta-analytical tools
│   │   ├── TscgPocletMiner/        # ElectronJS LLM-powered corpus analyzer
│   │   ├── TscgPocletGenerator/    # AI-assisted poclet creation
│   │   └── TscgExplorer/           # TSCG self-analysis tool
│   │
│   ├── systemic-frameworks/        # VSM and other systemic models
│   └── symbolic-system-grammars/   # I-Ching and similar systems
│
├── src/tscg/                       # Python package
│   ├── engine/                     # Core analysis engine
│   ├── cli/                        # Command-line interface
│   ├── ontology_tools/             # JSON-LD ↔ OWL converters
│   └── simulation-engine/          # Shared simulation components
│
├── docs/                           # Documentation
│   ├── papers/                     # Research articles & preprints
│   ├── methodology/                # Development guides
│   └── reboot-kit/                 # Quick-start package
│
└── index.html                      # Gallery of HTML simulations
```

---

## 🎮 Interactive Simulations

All poclets include **standalone HTML simulations** (no backend required):
- **Technology Stack:** p5.js (2D) | BabylonJS 6.26.0 (3D)
- **Migration Complete:** Python/Pygame → Static HTML for GitHub Pages
- **Canonical Reference:** `FireTriangle.html` (CSS Grid layout with 4 tabs)
- **Deployment:** [https://echopraxium.github.io/tscg/](https://echopraxium.github.io/tscg/)

**Simulation Features:**
- Real-time parameter controls with responsive UI
- Draggable splitter between canvas and sidebar
- Description | Concepts | Synergy | Scores tabs
- ASFID/REVOI scoring visualization
- Epistemic gap δ₁ calculation (normalized vectorial)

---

## 🔬 Key Concepts

### ASFID Scoring (Territory/Eagle Eye)
Measures systemic **empirical coherence** through 5 dimensions:
- **Attractor (A):** System stability and equilibrium tendencies
- **Structure (S):** Architectural organization and component relationships
- **Flow (F):** Dynamic exchanges and transformations
- **Information (I):** Encoded knowledge and semantic content
- **Dynamics (D):** Temporal evolution and behavioral patterns

### REVOI Scoring (Map/Sphinx Eye)
Measures **representational adequacy** through 5 dimensions:
- **Representability (R):** Symbolic expressiveness (⚠️ NEVER "Reproducibility")
- **Evolvability (E):** Capacity for incremental refinement
- **Verifiability (V):** Empirical testability and validation
- **Observability (O):** Measurability and instrumentation
- **Interoperability (I):** Cross-system compatibility

### Epistemic Gap (δ)
Quantifies the **mismatch** between Territory (ASFID) and Map (REVOI):

**δ₁ Formula (normalized vectorial, recommended):**
```
δ₁ = √Σ(ASFIDᵢ - REVOIᵢ)² / √10
```

**Spectral Classes:**
- **Coherent:** [0, 0.05) — Excellent Territory-Map alignment
- **OnCriticalLine:** [0.05, 0.15) — Good alignment with minor tensions
- **Liminal:** [0.15, 0.30) — Moderate epistemic divergence
- **Enigmatic:** [0.30, 1.0) — Significant Map-Territory gap (requires investigation)

---

## 🛠️ TscgPocletMiner

**ElectronJS-based LLM tool** for corpus analysis and knowledge extraction:

**Features:**
- **Multi-backend LLM support:** Google Gemini Free Tier (default) | Ollama local | DeepSeek Cloud | Anthropic Claude API
- **On-the-fly RAG:** Recursive whole-repo scan (~5,797 chunks) with no pre-built ChromaDB
- **Corpus rebuild:** `rebuild_m2_corpus.py` for M2 concept extraction
- **Hardware-optimized:** RTX 3050 Ti 4GB VRAM → phi3.5:3.8b for full GPU execution

**Local LLM Configuration:**
```bash
# Recommended for 16GB RAM / 4GB VRAM
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M
```

---

## 📚 Documentation

### Essential Reading
- **[M3 Bicephalous Architecture](ontology/docs/00_TSCG_M3_Bicephalous_Architecture.md)** — Philosophical foundation
- **[M2 Formulas Reference v15.10.0](ontology/docs/M2_FormulasReference_v15.10.0.md)** — Complete mathematical framework
- **[Poclet Analysis Methodology](docs/methodology/Poclet_Analysis_Methodology.md)** — Pipeline for creating instances
- **[TSCG File Tree](TSCG_File_Tree.md)** — Complete repository structure

### Quick Start
1. **Explore simulations:** Visit [GitHub Pages gallery](https://echopraxium.github.io/tscg/)
2. **Read a poclet:** Start with `instances/poclets/FireTriangle/README.md`
3. **Understand M2:** Review `ontology/docs/M2_GenericConcepts_README.md`
4. **Try TscgPocletMiner:** Follow `instances/tscg-tools/TscgPocletMiner/README.md`

---

## 📊 Current Poclet Corpus (23+ instances)

**Physics & Chemistry:**
- FireTriangle | PhaseTransition | FourStrokeEngine | NuclearReactorsTypology

**Electronics & Optics:**
- Transistor | VCO (Voltage-Controlled Oscillator) | ExposureTriangle | ColorSynthesis | TvTestPattern

**Biology & Medicine:**
- AdaptativeImmuneResponse | BloodPressureControl | CellSignalingModes | ComplexChemicalSynapse | Kidneys | RAAS (Renin-Angiotensin-Aldosterone System) | ButterflyMetamorphosis

**Ecology & Geology:**
- TrophicPyramid | (PlateTectonics in development)

**Economics & Governance:**
- KindlebergerMinsky (financial cycles) | NakamotoConsensus (blockchain) | GovernanceTrinity

**Music & Mythology:**
- CounterPoint (polyphonic voice leading) | MtgColorWheel (game design ontology) | Yggdrasil (Norse cosmology)

**Education:**
- TPACK (Technological Pedagogical Content Knowledge)

---

## 🔧 Installation & Usage

### Prerequisites
```bash
# For Python tools
python >= 3.9
pip install -r requirements.txt

# For TscgPocletMiner (ElectronJS)
node >= 16.x
npm install

# For local LLM (optional)
ollama >= 0.1.0
```

### Running Simulations Locally
```bash
# Start local HTTP server (required for file:/// security restrictions)
./_serve_index-html.bat  # Windows
# Or use Python
python -m http.server 8080
# Navigate to http://127.0.0.1:8080
```

### Generating Gallery Index
```bash
# Auto-generates index.html from poclet simulations
node cli_tools/generate_index-html/generate_index.js
```

---

## 📖 Research & Publications

### Preprint Article (v4.0 in progress)
- **Current:** [Zenodo v3.0](https://doi.org/10.5281/zenodo.18471860) (~8,500 words)
- **Target:** Zenodo v4.0 (~11,300 words) — submission pending
- **License:** CC BY 4.0
- **Scope:** Complete M3→M2→M1→M0 architecture, ASFID/REVOI theoretical foundation, 10+ poclet case studies

**Submission History:**
- ❌ HAL (rejected — requires academic affiliation)
- ✅ Zenodo (accepted — institutional-grade DOI)

---

## 🤝 Contributing

TSCG is currently a **single-developer project** (Michel/Echopraxium) with Claude AI collaboration. Contributions are welcome through:
- **Issue reporting:** Bug reports, simulation improvements, ontology suggestions
- **Poclet proposals:** New system models following the [4-stage pipeline](docs/methodology/Poclet_Analysis_Methodology.md)
- **Documentation:** Translations, clarifications, educational materials
- **Extensions:** New M1 domain extensions (requires M2 compliance)

**Authoring Conventions:**
- Files in **English**, conversations in **French**
- Author attribution: `"Echopraxium with the collaboration of Claude AI"`
- `@base` = `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`
- Changelog: max 3 entries (rolling window)
- PascalCase naming for poclets (1–4 words)

---

## 📜 License

**Source Code:** BSD 3-Clause License  
**Documentation & Article:** Creative Commons Attribution 4.0 International (CC BY 4.0)

See [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **GitHub Repository:** https://github.com/Echopraxium/tscg
- **GitHub Pages Gallery:** https://echopraxium.github.io/tscg/
- **Research Article (v3.0):** https://doi.org/10.5281/zenodo.18471860
- **Author:** Michel (Echopraxium) — Namur, Belgium

---

## 🙏 Acknowledgments

**Technical Collaboration:** Claude AI (Anthropic) — ontology design, poclet analysis, simulation development, documentation

**Theoretical Foundations:**
- Differential geometry & category theory for epistemic gap formalization
- Mesopotamian mythology (Anzû) for bicephalous metaphor
- VSM (Viable System Model) cybernetic principles

**Open Source Stack:**
- BabylonJS 6.26.0 (3D simulations)
- p5.js (2D simulations)
- ElectronJS (desktop tooling)
- Ollama (local LLM inference)
- Google Gemini Free Tier (cloud LLM)

---

**Version:** 16.0.0  
**Last Updated:** 2026-04-28  
**Framework Status:** Active development — M0 corpus expansion ongoing

---

*"Two eyes, two perspectives, one complete vision. From Territory to Map, from measurement to meaning."*  
— **TSCG Bicephalous Principle**
