# 🦇 TSCG Framework
## Transdisciplinary System Construction Game

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Echopraxium%2Ftscg-181717?logo=github)](https://github.com/Echopraxium/tscg)
[![Version](https://img.shields.io/badge/Version-16.2.0-green.svg)](https://github.com/Echopraxium/tscg/releases)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18471860.svg)](https://doi.org/10.5281/zenodo.18471860)

**Author:** Echopraxium with the collaboration of Claude AI
**License:** BSD 3-Clause (source code) | CC BY 4.0 (documentation & research article)
**Repository:** https://github.com/Echopraxium/tscg

---

## 🦇 The Bat's Lesson

A bat navigates a pitch-black cave without ever seeing it. It emits a pulse, listens to the echo, and from the gap between what it sent and what returned, it builds a usable map of the dark. It never touches reality directly — yet it flies.

We are in the same position with complex systems. We never access them directly; we work with our **Maps** (how we represent them) and infer the **Territory** (what is actually there) from the gap between model and observation. TSCG borrows the bat's strategy — emit, measure, correct — and turns it into a disciplined workflow for building system models.

---

## An Invitation — Not a Universal Theory

TSCG is a **proposal**, offered to a specific and probably small audience.

If you build models of systems — as a researcher, engineer, inventor, or artist — and you have ever noticed the *same structural pattern* reappearing across unrelated fields (a feedback loop in an ecosystem, a market, and a circuit; a hierarchy in a cell, a company, and a myth), then TSCG offers two things: a shared vocabulary for naming those patterns, and a discipline for testing whether the resemblance is real or merely poetic.

That is all it offers — and it is deliberate about not offering more.

**This is likely not for most people.** In an era where LLMs have made it effortless to publish elaborate unifying frameworks, the honest thing to state up front is what TSCG does *not* do:

- It discovers **no universal laws** and claims no theory that explains complex systems.
- It has **not** been validated by controlled comparison — its value, if any, remains to be demonstrated by people other than its author.
- It resists the "everything is a system" reflex: a pattern earns a place in the vocabulary only after surviving a **≥6-domain** cross-check, precisely so the framework cannot quietly become a mirror admiring its own generality.

If that framing interests you, read on. If it reads like one more grand unified theory, your skepticism is well placed — and the two documents in [`docs/CoreHypotheses/`](docs/CoreHypotheses/) were written to meet it head-on rather than deflect it.

---

## Why TSCG?

Complex systems are hard to reason about because we constantly confuse two things: the **system itself** (the Territory) and our **representation of it** (the Map). TSCG keeps them apart on purpose and turns the distinction into a repeatable workflow:

1. **Build** a model of the system from shared building blocks.
2. **Observe** how the real system behaves.
3. **Measure** the gap between model and observation.
4. **Refine** the model — and repeat.

The goal is never a perfect representation. It is to make the gap *visible and measurable*, so that "my model is wrong here" becomes a precise, actionable statement instead of a vague unease.

---

## 🌍 Three Pillars of TSCG

### 1️⃣ **An "Esperanto" for Systems Thinking**

TSCG proposes a **shared transdisciplinary vocabulary** for describing systems across the domains covered so far — from chemical reactions to blockchain consensus, from cellular biology to musical counterpoint.

Just as Esperanto aims to bridge human languages, TSCG provides:
- **Shared vocabulary**: ~80 atomic GenericConcepts (Feedback, Hierarchy, Flow, etc.)
- **Common grammar**: Structural rules for combining concepts (Lambek calculus / monoidal categories)
- **Cross-domain translation**: The same pattern "Homeostasis" applies to thermostats, ecosystems, and economies

**Working hypothesis:** many systems share recurring structural patterns. TSCG's ≥6-domain validation rule exists precisely to *test* this claim concept by concept, rather than assume it — once a pattern is admitted, you can look for it in new domains and check whether it actually holds.

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

#### 🔭 A Third Measure: the Focal Score (δ₂)

Beyond the Map/Territory *gap* (δ₁), TSCG defines an optional second score, δ₂, that measures the *sharpness* of the fusion between the two perspectives — an ophthalmic metaphor borrowed from binocular vision. Where δ₁ asks "how far apart are Map and Territory?", δ₂ asks "how well do they fuse into a single, in-focus image?".

| Score | Captures | Question |
|-------|----------|----------|
| **δ₁** (epistemic gap) | Map/Territory *alignment* | *How far apart?* |
| **δ₂** (focal score) | Map/Territory *fusion sharpness* | *How in-focus?* |

δ₂ is **optional and conditional** — it applies only to instances that mobilize at least one *stereopsic* GenericConcept. Its full definition (the Stereopsis grammar Gs, the TKSL primitives, focal classes from Emmetropic to Astigmatic, and the exact formulas) lives in **[Scoring System](docs/CoreHypotheses/ScoringSystem.md)** — deliberately kept out of this overview.

---

### 3️⃣ **LEGO Technic Metaphor: Build System Models Like Toys**

Think of TSCG as **LEGO Technic® for the mind**:

| LEGO Concept | TSCG Equivalent | Example |
|--------------|-----------------|---------|
| **Basic bricks** | GenericConcepts (M2) | Feedback, Hierarchy, Transformation |
| **Specialized kits** | Domain extensions (M1) | Biology, Chemistry, Electronics, Music, Mythology |
| **Finished models** | Grammatically-consistent instances (M0) | Fire Triangle, Four-Stroke Engine, Cell Signaling |
| **Building instructions** | Structural Grammar (Lambek calculus) | How concepts combine via monoidal products |

**Just like LEGO Technic® offers themed sets**, TSCG offers:
- **M1_Biology**: Cell structures, homeostasis, immune response
- **M1_Electronics**: Transistors, oscillators, signal processing
- **M1_Optics**: Color synthesis, exposure control, light filtering
- **M1_Music**: Counterpoint, harmony, voice leading
- **M1_Mythology**: Cosmological structures, archetypal patterns
- **M1_BusinessModeling**: BM Canvas, lifecycle phases, transitions ← *new*
- ...and 13 other domains

**The "Game" in TSCG**: Building minimal, grammatically-consistent system models (called **"Poclets"**) is like assembling a functional LEGO model — it must be coherent, complete, and actually work.

---

## 🏗️ Architecture at a Glance

```
M3 (Genesis Space)      → Universal foundation: ASFID (Territory) and REVOI (Map) dimensions
                           Formalized via Lambek calculus / monoidal categories
                           Three monoids: Territory Gt (×, ASFID), Map Gm (+, REVOI), Stereopsis Gs (|, TKSL)
    ↓
M2 (GenericConcepts)    → ~80 transdisciplinary atomic patterns
                           Validated across ≥6 unrelated domains each
    ↓
M1 (Extensions)         → 13+ domain-specific vocabularies
                           + M1_CoreConcepts (GenericConceptCombo instances)
    ↓
M0 (Instances)          → 33+ grammatically-consistent system models
                           Poclets | SystemicFrameworks | SymbolicSystemGrammars | TscgTools
```

---

## 📦 M0 Corpus — 33 Grammatically-Consistent Instances

*"Grammatically consistent" means each instance conforms to the M0 **structural grammar** (validated via SHACL) and carries explicit ASFID/REVOI scores. It does **not** mean empirically confirmed — the scores are intersubjective judgments, revisable as the evaluating community grows.*

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

Most instances include a **standalone HTML simulation** (no server required):

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

### 3. **Compute the gap**
   - **δ₁** — the epistemic gap between ASFID and REVOI means.
     Small δ₁ (**Coherent**) means Map and Territory agree; large δ₁ (**Enigmatic**) flags a mismatch to investigate.
   - **δ₂** *(optional)* — the focal score, when stereopsic concepts apply.
   - Exact formulas, spectral classes and focal classes: see **[Scoring System](docs/CoreHypotheses/ScoringSystem.md)**.

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
├── instances/                         # M0 Layer — 33 grammatically-consistent instances
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
│   ├── CoreHypotheses/                # Theoretical foundation (+ ScoringSystem.md)
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
| **M0** | `instances/poclets/` | Grammatically-consistent Poclets with ASFID/REVOI scores |

**Key features:**
- **Object Explorer** — class hierarchy, mode selector, regex search
- **Property Inspector** — real JSON-LD values, clickable IRI cross-navigation
- **SPARQL panel** — 16 predefined queries, export CSV/TTL
- **Imports tab** — namespace prefixes, `owl:imports` cross-loading

### TscgPocletMiner

AI-powered corpus analysis — multi-backend LLM (Gemini Free Tier default | Ollama | DeepSeek | Anthropic Claude), on-the-fly RAG, no database required. Optimized for RTX 3050 Ti 4GB VRAM → phi3.5:3.8b model.

---

## 📚 Essential Documentation

- **[Poclet Analysis Methodology](docs/methodology/Poclet_Analysis_Methodology.md)** — How to create a grammatically-consistent instance
- **[M3 Bicephalous Architecture](ontology/docs/M3_BicephalousPerspective_README.md)** — Philosophical foundation
- **[Structural Grammar Foundation](ontology/docs/Structural_Grammar_Foundation.md)** — Lambek calculus formalism
- **[Scoring System](docs/CoreHypotheses/ScoringSystem.md)** — δ₁, δ₂/EFS, TKSL primitives, spectral & focal classes
- **[UX Controls Catalog](ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md)** — Reusable simulation UI patterns

**Research article (v4.0 submission pending):**
📄 [Zenodo v3.0 Preprint](https://doi.org/10.5281/zenodo.18471860) — Complete M3→M2→M1→M0 architecture with 10+ case studies (~11,300 words)

---

## 🔍 For the Curious Reader

The [`An Invitation`](#an-invitation--not-a-universal-theory) section above already stated what TSCG does *not* claim. If you want the long-form version of that honesty — *"is this scientifically legitimate?"*, *"how do I know this isn't circular?"* — two documents in `docs/CoreHypotheses/` go further:

**[What TSCG Is — and What It Is Not](docs/CoreHypotheses/_00_TSCG_as_StereoscopicGlasses.md)**
The clearest one-page answer to *"what does TSCG actually do?"* — stereoscopic glasses, Eiffel Tower maquettes, and why reformulating without proving is already ambitious enough.

**[Narcissus and Icarus as Safeguards](docs/CoreHypotheses/_01_Narcissus_and_Icarus_as_Safeguards.md)**
An honest, no-concessions diagnosis of the project: what it genuinely contributes, what it does not, and the architectural mechanisms that prevent it from becoming what most transdisciplinary frameworks eventually become — a mirror admiring its own reflection.

> *These are not marketing documents. They are the questions a sceptical reviewer would ask — asked first, from the inside.*

---

## 🤝 Contributing

TSCG is currently a **single-developer project** (Michel/Echopraxium) with Claude AI collaboration. Contributions welcome through:
- **Poclet proposals**: New grammatically-consistent system models
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

## 🔄 A Framework That Expects to Be Superseded

<!-- TRANSITIONAL / TO VALIDATE — new closing section (ModelSupersession + defeasible knowledge).
     Keep, cut, or rework after re-reading. -->

TSCG treats its own results the way it treats any model: as the **state of the art until further notice**. Every score is an intersubjective judgment, defeasible by better consensus; every Poclet is the best current reading of its system, not its final word.

This is not a rhetorical disclaimer — it is built into the architecture. TSCG includes a formal **`ModelSupersession`** mechanism (M3 ontology type #12) whose job is to record, explicitly and traceably, when one model is superseded by another and *why*. A framework about the gap between Map and Territory has no honest choice but to apply that same discipline to itself: to keep, at all times, a Map of its own obsolescence.

So the corpus you see here is a snapshot. If TSCG is doing its job, some of it should already be on its way to being replaced — and the framework is designed to say so out loud when it happens.

---

## 🦇 Final Thought

> *"The bat doesn't see the cave.
> It hears the cave's echo.
> And that echo is enough to navigate any darkness."*

**TSCG doesn't give you direct access to reality.**
**It gives you a way to emit models, receive measurements, compute gaps, and refine your understanding.**
**And that is often enough to navigate complexity.**

---

**Version:** 16.2.0
**Last Updated:** 2026-07-08
**Framework Status:** Active development — v4.0 research article submission in progress

*"The map is not the territory, but the echo is enough to fly."*
— **The Bat's Wisdom**
