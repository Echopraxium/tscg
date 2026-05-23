# 🦇 TSCG Framework
## Transdisciplinary System Construction Game

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Echopraxium%2Ftscg-181717?logo=github)](https://github.com/Echopraxium/tscg)
[![Version](https://img.shields.io/badge/Version-16.0.0-green.svg)](https://github.com/Echopraxium/tscg/releases)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18471860.svg)](https://doi.org/10.5281/zenodo.18471860)

**Author:** Echopraxium with the collaboration of Claude AI  
**License:** BSD 3-Clause (source code) | CC BY 4.0 (documentation & research article)  
**Repository:** https://github.com/Echopraxium/tscg

---

## 🦇 The Bat's Lesson: Navigating Complexity Through Echolocation

In the silence of a cave, a bat emits an ultrasonic pulse. The sound bounces off invisible walls and returns transformed. In milliseconds, the bat **constructs a sonic map** of its environment. It never **sees** the cave directly — yet it navigates, hunts, and thrives.

**The bat teaches us something profound:** You don't need direct access to reality to navigate it effectively. You need:
1. A **model** to emit (your hypothesis)
2. **Echoes** to receive (measurements from reality)
3. A way to compute the **gap** between model and measurement
4. A process to **correct** and refine

**TSCG is the human version of echolocation for understanding complex systems.**

Just as the bat lives in the **hybrid space** between its emitted pulse and returning echo, we humans live in the hybrid space between our **Maps** (how we represent systems) and the **Territory** (what exists empirically). The gap between them is not a failure — it's the very mechanism that enables learning, navigation, and discovery.

---

## 🌍 Three Pillars of TSCG

### 1️⃣ **An "Esperanto" for Systems Thinking**

TSCG proposes a **universal transdisciplinary language** for describing any complex system — from chemical reactions to blockchain consensus, from cellular biology to musical counterpoint.

Just as Esperanto aims to bridge human languages, TSCG provides:
- **Universal vocabulary**: ~80 atomic GenericConcepts (Feedback, Hierarchy, Flow, etc.)
- **Common grammar**: Structural rules for combining concepts
- **Cross-domain translation**: The same pattern "Homeostasis" applies to thermostats, ecosystems, and economies

**Key insight:** Most systems share the **same underlying patterns**. Once you speak TSCG, you can recognize these patterns anywhere.

---

### 2️⃣ **Map-Territory Duality: The Bicephalous Vision**

At the heart of TSCG is a rigorous distinction inspired by Alfred Korzybski's principle: **"The map is not the territory."**

TSCG formalizes this through a **dual-layer architecture**:

| Perspective | Metaphor | What It Measures | 5 Dimensions |
|-------------|----------|------------------|--------------|
| **🦅 Eagle Eye (ASFID)** | The bat's echo | **Territory** — What exists empirically | **A**ttractor, **S**tructure, **F**low, **I**nformation, **D**ynamics |
| **🦁 Sphinx Eye (REVOI)** | The bat's emission | **Map** — How we represent it | **R**epresentability, **E**volvability, **V**erifiability, **O**bservability, **I**nteroperability |

**Why two perspectives?**
- **ASFID** asks: *"What is the system doing?"* (measurement)
- **REVOI** asks: *"How well can we model it?"* (representation)

The **epistemic gap (δ)** between these perspectives tells us how aligned our understanding is with reality — and where to improve.

This creates a **layered model** (M3 → M2 → M1 → M0) where universal foundations cascade into domain-specific applications.

---

### 3️⃣ **LEGO Technic Metaphor: Build System Models Like Toys**

Think of TSCG as **LEGO Technic® for the mind**:

| LEGO Concept | TSCG Equivalent | Example |
|--------------|-----------------|---------|
| **Basic bricks** | GenericConcepts (M2) | Feedback, Hierarchy, Transformation |
| **Specialized kits** | Domain extensions (M1) | Biology, Chemistry, Electronics, Music, Mythology |
| **Finished models** | Validated instances (M0) | Fire Triangle, Four-Stroke Engine, Cell Signaling |
| **Building instructions** | Structural Grammar | How concepts combine via tensor products |

**Just like LEGO Technic® offers themed sets** (Pneumatics, Sensors, Renewable Energy), TSCG offers:
- **M1_Biology**: Cell structures, homeostasis, immune response
- **M1_Electronics**: Transistors, oscillators, signal processing
- **M1_Optics**: Color synthesis, exposure control, light filtering
- **M1_Music**: Counterpoint, harmony, voice leading
- **M1_Mythology**: Cosmological structures, archetypal patterns
- ...and 11+ other domains

**The "Game" in TSCG**: Building minimal, validated system models (called **"Poclets"**) is like assembling a functional LEGO model — it must be coherent, complete, and actually work.

---

## 🏗️ Architecture at a Glance

```
M3 (Genesis Space)      → Universal foundation: ASFID/REVOI dimensions
                           (The "bat's echolocation mechanism")
    ↓
M2 (GenericConcepts)    → ~80 transdisciplinary patterns
                           (Universal "LEGO bricks")
    ↓
M1 (Extensions)         → 11+ domain-specific vocabularies
                           (Specialized "LEGO kits")
    ↓
M0 (Instances)          → 23+ validated system models
                           (Finished "LEGO models")
```

**Current M0 Corpus**: Fire Triangle, Four-Stroke Engine, Nakamoto Consensus (blockchain), Adaptive Immune Response, Counterpoint (music), MTG Color Wheel, Blood Pressure Control, Yggdrasil (Norse cosmology), TPACK (education), and 14+ others spanning chemistry, biology, electronics, ecology, economics, optics, mythology.

---

## 🎮 Interactive Simulations

Every validated system includes a **standalone HTML simulation** (no installation required):
- **2D simulations**: p5.js
- **3D simulations**: BabylonJS 6.26.0
- **Live demo**: [https://echopraxium.github.io/tscg/](https://echopraxium.github.io/tscg/)

**Features:**
- Real-time parameter controls
- ASFID/REVOI scoring visualization
- Epistemic gap (δ) calculation
- Interactive concept exploration

**Canonical reference**: `FireTriangle.html` — CSS Grid layout with Description | Concepts | Synergy | Scores tabs

---

## 🚀 Quick Start: Your First "Echolocation"

Want to model a system with TSCG? Follow the **bat's cycle**:

### 1. **Emit a pulse (Build your Map)**
   - What do you hypothesize about the system?
   - Identify relevant GenericConcepts from M2
   - Score your model on REVOI dimensions (0–1)

### 2. **Listen for the echo (Measure the Territory)**
   - Observe the real-world system
   - Score it on ASFID dimensions (0–1)
   - Note: Flow (F) ≥ 0.1 (no perfectly closed systems)

### 3. **Compute the gap (Calculate δ)**
   - Compare ASFID vs. REVOI vectors
   - δ₁ = √[Σ(ASFIDᵢ - REVOIᵢ)²] / √10
   - Spectral classes: Coherent (< 0.05) | OnCriticalLine (0.05–0.15) | Liminal (0.15–0.30) | Enigmatic (≥ 0.30)

### 4. **Correct your flight (Refine the model)**
   - Use the gap to identify mismatches
   - Adjust your GenericConcept selection
   - Iterate until coherence is achieved

```
TSCG Cycle = Emission (REVOI) → Echo (ASFID) → Gap (δ) → Correction → Action
```

---

## 🛠️ TscgPocletMiner: AI-Powered Corpus Analysis

**ElectronJS desktop tool** for exploring the TSCG knowledge base:
- **Multi-backend LLM**: Google Gemini Free Tier (default) | Ollama local | DeepSeek | Anthropic Claude
- **On-the-fly RAG**: Recursive repo scan (~5,797 chunks)
- **No database**: Pure dynamic retrieval from source files
- **Optimized for consumer hardware**: RTX 3050 Ti 4GB VRAM → phi3.5:3.8b model

**Use cases:**
- "What M2 concepts apply to protein folding?"
- "Find poclets with high Flow scores"
- "Compare ASFID profiles across domains"

---

## 📚 Essential Documentation

- **[Poclet Analysis Methodology](docs/methodology/Poclet_Analysis_Methodology.md)** — How to create a validated instance
- **[M3 Bicephalous Architecture](ontology/docs/00_TSCG_M3_Bicephalous_Architecture.md)** — Philosophical foundation
- **[M2 Formulas Reference](ontology/docs/M2_FormulasReference_v15.10.0.md)** — Mathematical framework
- **[UX Controls Catalog](ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md)** — Reusable simulation UI patterns

**Research article (v4.0 submission pending):**  
📄 [Zenodo v3.0 Preprint](https://doi.org/10.5281/zenodo.18471860) — Complete M3→M2→M1→M0 architecture with 10+ case studies (~11,300 words)

---

## 📁 Repository Structure

```
tscg/
├── ontology/                       # M3/M2/M1 reference ontologies (JSON-LD)
│   ├── M3_GenesisGrammar.jsonld     # Bicephalous foundation (Structural Grammar)
│   ├── M2_GenericConcepts.jsonld   # ~80 universal patterns
│   ├── M1_extensions/              # 11 domain vocabularies
│   └── docs/                       # Theoretical foundations
│
├── instances/                      # M0 Layer — Concrete validated systems
│   ├── poclets/                    # 23+ system models with simulations
│   ├── tscg-tools/                 # TscgPocletMiner, TscgPocletGenerator
│   ├── systemic-frameworks/        # VSM and cybernetic models
│   └── symbolic-system-grammars/   # I-Ching and similar systems
│
├── docs/                           # Methodology guides
├── index.html                      # Gallery of simulations (auto-generated)
└── cli_tools/                      # Python/Node.js utilities
```

---


## 🔧 Tools

### TscgOntologyExplorer

An Electron-based ontology browser dedicated to the TSCG framework, available at:

```
instances/tscg-tools/TscgOntologyExplorer/
```

Provides interactive navigation across all **four TSCG ontology layers**:

| Layer | Files | What you can explore |
|-------|-------|---------------------|
| **M3** | `M3_GenesisGrammar.jsonld`, `M3_EagleEye.jsonld`, `M3_SphinxEye.jsonld` | ASFID/REVOI structural primitives |
| **M2** | `M2_GenericConcepts.jsonld` | ~80 GenericConcepts with structural formulas |
| **M1** | `ontology/M1_extensions/` | Domain vocabularies (Biology, Physics…) |
| **M0** | `instances/poclets/` | Validated Poclets with ASFID/REVOI scores |

**Key features:**
- **Object Explorer** — class hierarchy, mode selector, search with regex (`^Me`, `loop$`, `/pattern/`)
- **Property Inspector** — real JSON-LD values, clickable IRI cross-navigation
- **SPARQL panel** — 16 predefined queries, export CSV/TTL
- **Imports tab** — namespace prefixes, `owl:imports` cross-loading
- **M1 dropdown** — one-click access to all domain extensions

> 📖 Full documentation: `instances/tscg-tools/TscgOntologyExplorer/docs/UserManual.md`

### TscgPocletMiner

AI-powered corpus analysis tool — see [🛠️ TscgPocletMiner](#️-tscgpocletminer-ai-powered-corpus-analysis) above.

---

## 🤝 Contributing

TSCG is currently a **single-developer project** (Michel/Echopraxium) with Claude AI collaboration. Contributions welcome through:
- **Poclet proposals**: New validated system models
- **M1 extensions**: New domain vocabularies (requires M2 compliance)
- **Documentation**: Clarifications, translations, educational materials
- **Simulation improvements**: UI/UX enhancements, new visualization techniques

**Key conventions:**
- Files in **English**, conversations in **French**
- Author: `"Echopraxium with the collaboration of Claude AI"`
- `@base` URI: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`
- Changelog: max 3 entries per file

---

## 🔗 Links

- **GitHub Repository**: https://github.com/Echopraxium/tscg
- **Live Gallery**: https://echopraxium.github.io/tscg/
- **Research Article (v3.0)**: https://doi.org/10.5281/zenodo.18471860
- **Author**: Michel (Echopraxium) — Namur, Belgium

---

## 🔍 For the Curious Reader

If the three pillars above sparked genuine questions — *"But is this
scientifically legitimate?"*, *"What exactly does TSCG claim?"*,
*"How do I know this isn't circular?"* — two documents in
`docs/CoreHypotheses/` are written precisely for you:

**[What TSCG Is — and What It Is Not](docs/CoreHypotheses/_00_TSCG_as_StereoscopicGlasses.md)**  
The clearest one-page answer to *"what does TSCG actually do?"* —
stereoscopic glasses, Eiffel Tower maquettes, and why reformulating
without proving is already ambitious enough.

**[Narcissus and Icarus as Safeguards](docs/CoreHypotheses/_01_Narcissus_and_Icarus_as_Safeguards.md)**  
An honest, no-concessions diagnosis of the project: what it genuinely
contributes, what it does not, and the architectural mechanisms that
prevent it from becoming what most transdisciplinary frameworks
eventually become — a mirror admiring its own reflection.

> *These are not marketing documents. They are the questions a sceptical
> reviewer would ask — asked first, from the inside.*
>
> *If you find something we missed — that is a contribution, not a refutation.*

---

## 🦇 Final Thought

> *"The bat doesn't see the cave.  
> It hears the cave's echo.  
> And that echo is enough to navigate any darkness."*

**TSCG doesn't give you direct access to reality.**  
**It gives you a way to emit models, receive measurements, compute gaps, and refine your understanding.**  
**And that is enough to navigate any complex system.**

---

**Version:** 16.0.0  
**Last Updated:** 2026-05-12  
**Framework Status:** Active development — v4.0 research article submission in progress

*"The map is not the territory, but the echo is enough to fly."*  
— **The Bat's Wisdom**
