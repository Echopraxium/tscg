# 🦇 TSCG Framework
## Transdisciplinary System Construction Game

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Echopraxium%2Ftscg-181717?logo=github)](https://github.com/Echopraxium/tscg)
[![Version](https://img.shields.io/badge/Version-16.1.0-green.svg)](https://github.com/Echopraxium/tscg/releases)
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
- **Common grammar**: Structural rules for combining concepts (Lambek calculus / monoidal categories)
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

The **epistemic gap (δ₁)** between these perspectives tells us how aligned our understanding is with reality — and where to improve.

This creates a **layered model** (M3 → M2 → M1 → M0) where universal foundations cascade into domain-specific applications.

#### 🔭 The Third Eye: Stereopsic Focal Score (δ₂ / SFE)

Beyond the bicephalous duality, TSCG introduces a **third perspective** — the **Stereopsis Grammar Gs** — which formalizes the synergy that emerges from fusing Eagle Eye and Sphinx Eye:

```
Stereopsis = the depth perception born from binocular fusion
           = formally: the bicephalous monoid (Gs, |, EmptyStereopsis)
           = Base16 alphabet: 𝕋₀(|) = {T, _^, _$, K, Ss, L}
```

The **Epistemic Focal Score (SFE)** — or **δ₂** — measures the *sharpness* of this binocular fusion using an ophthalmic metaphor:

```
δ₂ = SFE = stereopsicDepth × (1 − |focalBias|)
```

Where:
- **`stereopsicDepth`** — depth of Gs engagement, computed from active TKSL primitives:
  `(T_present × 0.25) + (K_present × 0.25) + (Ss_present × 0.25) + (L_present × 0.25)`
- **`focalBias`** — signed Map/Territory imbalance: `REVOI_mean − ASFID_mean` ∈ [−1, +1]
  - Positive → **Hyperopic** (Map too abstract, Territory blurred)
  - Negative → **Myopic** (Territory too detailed, Map inadequate)
  - Zero → **Emmetropic candidate** (perfect balance)

| Focal Class | SFE Range | Meaning |
|-------------|-----------|---------|
| **Emmetropic** | SFE ≥ 0.70 | Sharp combined image — Map+Territory in focus |
| **SlightlyMyopic / SlightlyHyperopic** | 0.50 ≤ SFE < 0.70 | Slight bias toward Territory or Map |
| **Myopic / Hyperopic** | 0.30 ≤ SFE < 0.50 | Significant Map/Territory imbalance |
| **Astigmatic** | SFE < 0.30 | Insufficient Gs depth — no stereopsis possible |

The **TKSL primitives** (4 nominal Gs generators) each answer a transcendental question:

| Primitive | Name | Question |
|-----------|------|----------|
| **T** | Temporality | *When?* — temporal interface Gt↔Gm |
| **K** | Knowledge | *What?* — cognitive contextualisation of Information |
| **Ss** | Symbol *(Stereopsic)* | *Sign?* — semiotic bridge signifier↔signified |
| **L** | Localizability | *Converging?* — cybernetic convergence toward Attractor |

δ₂/SFE is **optional** and **conditional**: only present in M0 instances that mobilize at least one stereopsic GenericConcept (`m0:focalApplicable = true`). The two scores are complementary:

| Score | Formula | Measures |
|-------|---------|---------|
| **δ₁** (epistemic gap) | `|ASFID_mean − REVOI_mean| / √2` | Map/Territory *alignment* (distance) |
| **δ₂ / SFE** (focal score) | `stereopsicDepth × (1 − |focalBias|)` | Map+Territory *fusion sharpness* (binocular depth) |

---

### 3️⃣ **LEGO Technic Metaphor: Build System Models Like Toys**

Think of TSCG as **LEGO Technic® for the mind**:

| LEGO Concept | TSCG Equivalent | Example |
|--------------|-----------------|---------|
| **Basic bricks** | GenericConcepts (M2) | Feedback, Hierarchy, Transformation |
| **Specialized kits** | Domain extensions (M1) | Biology, Chemistry, Electronics, Music, Mythology |
| **Finished models** | Validated instances (M0) | Fire Triangle, Four-Stroke Engine, Cell Signaling |
| **Building instructions** | Structural Grammar (Lambek calculus) | How concepts combine via monoidal products |

**Just like LEGO Technic® offers themed sets**, TSCG offers:
- **M1_Biology**: Cell structures, homeostasis, immune response
- **M1_Electronics**: Transistors, oscillators, signal processing
- **M1_Optics**: Color synthesis, exposure control, light filtering
- **M1_Music**: Counterpoint, harmony, voice leading
- **M1_Mythology**: Cosmological structures, archetypal patterns
- **M1_BusinessModeling**: BM Canvas, lifecycle phases, transitions ← *new*
- ...and 13 other domains

**The "Game" in TSCG**: Building minimal, validated system models (called **"Poclets"**) is like assembling a functional LEGO model — it must be coherent, complete, and actually work.

---

## 🏗️ Architecture at a Glance

```
M3 (Genesis Space)      → Universal foundation: ASFID ⊕ REVOI dimensions
                           Formalized via Lambek calculus / monoidal categories
                           Three monoids: Territory Gt (×, ASFID), Map Gm (+, REVOI), Stereopsis Gs (|, TKSL)
    ↓
M2 (GenericConcepts)    → ~80 transdisciplinary atomic patterns
                           Validated across ≥6 unrelated domains each
    ↓
M1 (Extensions)         → 13+ domain-specific vocabularies
                           + M1_CoreConcepts (GenericConceptCombo instances)
    ↓
M0 (Instances)          → 33+ validated system models
                           Poclets | SystemicFrameworks | SymbolicSystemGrammars | TscgTools
```

---

## 📦 M0 Corpus — 33 Validated Instances

### Poclets (26) — `instances/poclets/`

Minimal yet complete system models spanning 15+ domains:

| Domain | Poclets |
|--------|---------|
| Biology / Physiology | AdaptativeImmuneResponse, BloodPressureControl, ButterflyMetamorphosis, CellSignalingModes, Kidneys, Raas |
| Chemistry / Physics | FireTriangle, PhaseTransition, NuclearReactorsTypology |
| Electronics | Transistor, Vco, Theremin *(stub)* |
| Music | CounterPoint |
| Art / Optics | ColorSynthesis (RGB/HSL/CMY/CMYK), ExposureTriangle, TvTestPattern |
| Geology | PlateTectonics |
| Chemistry (elements) | Ptoe *(Periodic Table — BabylonJS 3D)* |
| Engineering | FourStrokeEngine |
| Neuroscience | ComplexChemicalSynapse |
| Economics | KindlebergerMinsky |
| Ecology | TrophicPyramid |
| Blockchain | NakamotoConsensus |
| Game Theory | MtgColorWheel |
| Pedagogy | Tpack |
| Mythology | Yggdrasil |

### SystemicFrameworks (3) — `instances/systemic-frameworks/`

| Framework | Domain | SpectralClass |
|-----------|--------|---------------|
| **Vsm** | Cybernetics (Viable System Model) | OnCriticalLine (δ₁=0.057) |
| **Triz** | Innovation methodology | OnCriticalLine (δ₁=0.057) |
| **Bmc** ← *new* | Business Model Canvas lifecycle simulation | pending |

### SymbolicSystemGrammars (1) — `instances/symbolic-system-grammars/`

| Grammar | Domain |
|---------|--------|
| **IChing** | Chinese divination / combinatorial logic |

### TscgTools (3 active + 1 stub) — `instances/tscg-tools/`

| Tool | Type | Description |
|------|------|-------------|
| **TscgOntologyExplorer** | ElectronJS | 4-layer ontology browser with SPARQL panel |
| **TscgPocletMiner** | ElectronJS + LLM | AI-powered corpus analysis (Gemini/Ollama/Claude) |
| **TscgPocletGenerator** | ElectronJS | Guided poclet creation wizard |
| **TscgOntologyAPIServer** | FastAPI *(stub)* | REST API over pyoxigraph triple store |

---

## 🎮 Interactive Simulations

Every validated instance includes a **standalone HTML simulation** (no server required):

| Technology | Use | Example |
|------------|-----|---------|
| **p5.js** (Canvas2D) | 2D dynamic simulations | FireTriangle, BMC lifecycle |
| **BabylonJS 6.26.0** | 3D immersive simulations | Ptoe (Periodic Table) |
| **Tone.js** | Audio simulations | CounterPoint |

**Live gallery**: [https://echopraxium.github.io/tscg/](https://echopraxium.github.io/tscg/)

### 🆕 BMC Simulation — Business Model Canvas SystemicFramework

The most feature-rich TSCG simulation to date:

- **12 real-world companies** with documented lifecycle phases and business model mutations:
  Netflix, Nokia, Nintendo, Apple, Amazon, Google, Microsoft, IBM, Kodak, Xerox, Michelin, Airbnb
- **34 documented transitions** (✅ Success / ❌ Failure / 🔄 InProgress) with bibliographic sources
- **Decline mechanics**: not a button — induced automatically by slider manipulation (VP ↓ + Cost ↑)
- **JSON-LD ontology** (`M0_BmcSimulation.jsonld`) — SHACL-validable, loaded via GitHub raw URL with local fallback
- **Osterwalder PhD scoring**: Value Level, Revenue Type, Segment Type, Relationship Type per block × phase

**Path**: `instances/systemic-frameworks/Bmc/static/M0_Bmc.html`

---

## 🚀 Quick Start: Your First "Echolocation"

Want to model a system with TSCG? Follow the **bat's cycle**:

### 1. **Emit a pulse (Build your Map)**
   - Identify relevant GenericConcepts from M2
   - Score your model on REVOI dimensions (0–1)

### 2. **Listen for the echo (Measure the Territory)**
   - Observe the real-world system
   - Score it on ASFID dimensions (0–1)

### 3. **Compute the gap (Calculate δ₁ and δ₂)**
   - **δ₁** (epistemic gap) = `|ASFID_mean − REVOI_mean| / √2`
     - Spectral classes: **Coherent** (δ₁ < 0.05) | **OnCriticalLine** (0.05–0.15) | **Liminal** (0.15–0.30) | **Enigmatic** (≥ 0.30)
   - **δ₂ / SFE** (focal score, optional) = `stereopsicDepth × (1 − |focalBias|)`
     - Only when stereopsic GenericConcepts are mobilized (`focalApplicable = true`)
     - Focal classes: **Emmetropic** (SFE ≥ 0.70) → **Astigmatic** (SFE < 0.30)

### 4. **Correct your flight (Refine the model)**
   - Use the gap to identify mismatches
   - Adjust your GenericConcept selection
   - Iterate until coherence is achieved

---

## 📁 Repository Structure

```
tscg/
├── ontology/                          # M3 / M2 / M1 reference ontologies (JSON-LD)
│   ├── M3_GenesisGrammar.jsonld       # Structural grammar foundation
│   ├── M3_EagleEye.jsonld             # ASFID Territory perspective
│   ├── M3_SphinxEye.jsonld            # REVOI Map perspective
│   ├── M3_BicephalousPerspective.jsonld  # Unified bicephalous view
│   ├── M2_GenericConcepts.jsonld      # ~80 universal atomic patterns
│   ├── M1_CoreConcepts.jsonld         # GenericConceptCombo instances
│   ├── M1_Domains.jsonld              # Domain registry (19 domains)
│   ├── M1_extensions/                 # 13 domain vocabularies
│   │   ├── biology/
│   │   ├── chemistry/
│   │   ├── business-modeling/         # ← new (BMC simulation)
│   │   └── ... (11 others)
│   ├── InstanceSimulations/           # UX controls catalog + simulation metadata
│   ├── TSCG_InstanceGrammar/          # SHACL v1.5 grammar + migration tools
│   └── docs/                          # Theoretical foundations
│
├── instances/                         # M0 Layer — 33 validated instances
│   ├── poclets/                       # 26 system models (Fire Triangle → Periodic Table)
│   ├── systemic-frameworks/
│   │   ├── Vsm/                       # Viable System Model
│   │   ├── Triz/                      # TRIZ icosahedron
│   │   └── Bmc/                       # Business Model Canvas ← new
│   │       ├── M0_BmcSimulation.jsonld   # Pure JSON-LD ontology (SHACL-validable)
│   │       └── static/                   # Standalone HTML simulation
│   │           ├── M0_Bmc.html
│   │           └── src/
│   │               ├── Bmc.js
│   │               ├── Bmc.css
│   │               └── M0_BmcSimulation.jsonld.js  # JS wrapper (file:// fallback)
│   ├── symbolic-system-grammars/
│   │   └── Iching/
│   └── tscg-tools/
│       ├── TscgOntologyExplorer/      # ElectronJS browser
│       ├── TscgPocletMiner/           # AI-powered corpus analysis
│       ├── TscgPocletGenerator/       # Guided creation wizard
│       └── TscgOntologyAPIServer/     # FastAPI REST (stub)
│
├── cli_tools/                         # Python/Node.js utilities
│   ├── generate_index-html/           # Gallery auto-generator
│   ├── migrate_properties/            # Property rename CLI
│   ├── ontology-linter/               # JSON-LD linting
│   └── verify_migration/              # Post-migration validation
│
├── docs/
│   ├── CoreHypotheses/                # Theoretical foundation (8 documents)
│   └── methodology/                   # Poclet Analysis Methodology
│
└── index.html                         # Live gallery (auto-generated)
```

---

## 🛠️ Tools

### TscgOntologyExplorer

An Electron-based ontology browser dedicated to the TSCG framework:

| Layer | Files | What you can explore |
|-------|-------|---------------------|
| **M3** | `M3_GenesisGrammar.jsonld`, `M3_EagleEye.jsonld`, `M3_SphinxEye.jsonld` | ASFID/REVOI structural primitives |
| **M2** | `M2_GenericConcepts.jsonld` | ~80 GenericConcepts with structural formulas |
| **M1** | `ontology/M1_extensions/` | Domain vocabularies (Biology, Physics…) |
| **M0** | `instances/poclets/` | Validated Poclets with ASFID/REVOI scores |

**Key features:**
- **Object Explorer** — class hierarchy, mode selector, regex search
- **Property Inspector** — real JSON-LD values, clickable IRI cross-navigation
- **SPARQL panel** — 16 predefined queries, export CSV/TTL
- **Imports tab** — namespace prefixes, `owl:imports` cross-loading

### TscgPocletMiner

AI-powered corpus analysis — multi-backend LLM (Gemini Free Tier default | Ollama | DeepSeek | Anthropic Claude), on-the-fly RAG, no database required. Optimized for RTX 3050 Ti 4GB VRAM → phi3.5:3.8b model.

---

## 📚 Essential Documentation

- **[Poclet Analysis Methodology](docs/methodology/Poclet_Analysis_Methodology.md)** — How to create a validated instance
- **[M3 Bicephalous Architecture](ontology/docs/M3_BicephalousPerspective_README.md)** — Philosophical foundation
- **[Structural Grammar Foundation](ontology/docs/Structural_Grammar_Foundation.md)** — Lambek calculus formalism
- **[UX Controls Catalog](ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md)** — Reusable simulation UI patterns

**Research article (v4.0 submission pending):**
📄 [Zenodo v3.0 Preprint](https://doi.org/10.5281/zenodo.18471860) — Complete M3→M2→M1→M0 architecture with 10+ case studies (~11,300 words)

---

## 🔍 For the Curious Reader

If the three pillars above sparked genuine questions — *"But is this scientifically legitimate?"*, *"What exactly does TSCG claim?"*, *"How do I know this isn't circular?"* — two documents in `docs/CoreHypotheses/` are written precisely for you:

**[What TSCG Is — and What It Is Not](docs/CoreHypotheses/_00_TSCG_as_StereoscopicGlasses.md)**
The clearest one-page answer to *"what does TSCG actually do?"* — stereoscopic glasses, Eiffel Tower maquettes, and why reformulating without proving is already ambitious enough.

**[Narcissus and Icarus as Safeguards](docs/CoreHypotheses/_01_Narcissus_and_Icarus_as_Safeguards.md)**
An honest, no-concessions diagnosis of the project: what it genuinely contributes, what it does not, and the architectural mechanisms that prevent it from becoming what most transdisciplinary frameworks eventually become — a mirror admiring its own reflection.

> *These are not marketing documents. They are the questions a sceptical reviewer would ask — asked first, from the inside.*

---

## 🤝 Contributing

TSCG is currently a **single-developer project** (Michel/Echopraxium) with Claude AI collaboration. Contributions welcome through:
- **Poclet proposals**: New validated system models
- **M1 extensions**: New domain vocabularies (requires M2 compliance — ≥6 unrelated domains per concept)
- **Documentation**: Clarifications, translations, educational materials
- **Simulation improvements**: UI/UX enhancements, new visualization techniques

**Key conventions:**
- Files in **English**, conversations in **French**
- Author: `"Echopraxium with the collaboration of Claude AI"`
- `@base` URI: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`
- Changelog: max 3 rolling entries per file
- `tscg:` namespace: **forbidden** (use `m3:`, `m2:`, `m1:`, `m0:`)

---

## 🔗 Links

- **GitHub Repository**: https://github.com/Echopraxium/tscg
- **Live Gallery**: https://echopraxium.github.io/tscg/
- **BMC Simulation**: https://echopraxium.github.io/tscg/instances/systemic-frameworks/Bmc/static/M0_Bmc.html
- **Research Article (v3.0)**: https://doi.org/10.5281/zenodo.18471860
- **Author**: Michel (Echopraxium) — Namur, Belgium

---

## 🦇 Final Thought

> *"The bat doesn't see the cave.
> It hears the cave's echo.
> And that echo is enough to navigate any darkness."*

**TSCG doesn't give you direct access to reality.**
**It gives you a way to emit models, receive measurements, compute gaps, and refine your understanding.**
**And that is enough to navigate any complex system.**

---

**Version:** 16.1.0
**Last Updated:** 2026-06-24
**Framework Status:** Active development — v4.0 research article submission in progress

*"The map is not the territory, but the echo is enough to fly."*
— **The Bat's Wisdom**
