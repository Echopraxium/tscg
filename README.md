# TSCG: The Systemic Construction Game
### A LEGO Technic® Kit for Modeling Complex Systems

**Version**: 14.1.0  
**Authors**: Echopraxium with the collaboration of Claude AI  
**License**: BSD 3-Clause "Clear" License  
**Repository**: https://github.com/Echopraxium/tscg

---

## 🧱 Overview: Build Models Like You Build with LEGO

TSCG (Transdisciplinary System Construction Game) is not a theory of everything. It's a **construction kit**.

Think of it as **LEGO Technic® for the mind**:
*   Instead of plastic beams and gears, you get **conceptual building blocks** (like Attractors, Flows, Information).
*   Instead of assembly instructions, you get **universal assembly patterns** (like Feedback, Hierarchy, Homeostasis).
*   Your goal is not to replicate reality atom-by-atom, but to **build articulated, functional models** that capture the essential logic of any complex system—be it a cell, an engine, an economy, or a myth.

**The Core Promise**: Use a single, coherent set of blocks and rules to construct, analyze, and compare models across all disciplines. Bridge biology, chemistry, engineering, and social sciences with a common modeling language.

---

## 🦅🦁 Core Philosophy: Map and Territory

TSCG is grounded in Alfred Korzybski's principle: **"The map is not the territory"**.

- **Territory** (Eagle Eye/ASFID): Observable reality, measured phenomena, what actually happens.
- **Map** (Sphinx Eye/ORIVE): Conceptual models, representations, how we understand and communicate.

**Key Insight**: Both perspectives are necessary. Territory provides empirical grounding; Map enables understanding and communication. The epistemic gap between them (∆Θ) is not a failure—it's an inherent feature of knowledge construction.

---

## 🛠️ The Toolkit: Your Box of Conceptual Parts

### M3: The Universal Parts List (Bicephalous Basis)

Our fundamental building blocks are two complementary sets of 5 dimensions:

#### 🦅 Eagle Eye (ASFID) – Measures the "Territory"
*   `A`ttractor: Convergence tendency, equilibria  
*   `S`tructure: Topological organization  
*   `F`low: Exchange with environment (always ≥ 0.1 – no perfectly closed systems)  
*   `I`nformation: State complexity  
*   `D`ynamics: Rate of internal change  

**Mathematical Foundation**: ℋ_ASFID = ℂ⁵ (Hilbert space)

#### 🦁 Sphinx Eye (ORIVE) – Constructs the "Map"
*   `O`bserver: Observability, perceptual access  
*   `R`ecurse: Representability, semantic access  
*   `I`nteract: Interoperability, shareability  
*   `V`ary: Verifiability, testability  
*   `E`merge: Evolvability, updatability  

**Mathematical Foundation**: ℋ_ORIVE = ℂ⁵ (Hilbert space)

**Together they form**: ℋ_M3 = ℋ_ASFID ⊕ ℋ_ORIVE = ℂ¹⁰

---

### M2: The Assembly Manual of Patterns (68 Universal Metaconcepts)

These are the **core techniques** of systemic construction. Each is a proven way to combine the M3 blocks via tensor products.

**Example formulas**:
```
|Homeostasis⟩ = A⊗S⊗F  (order-3 tensor)
|Network⟩ = S⊗I        (order-2 tensor)
|Flow⟩ = F             (order-1 tensor)
```

**Categories include**:
- Ontological (Entity, Process, State...)
- Structural (Hierarchy, Module, Interface...)
- Dynamic (Feedback, Cycle, Emergence...)
- Control (Constraint, Regulation, Balance...)
- Information (Signal, Noise, Encoding...)

---

### M1: Themed Expansion Packs (Domain-Specific Concepts)

Ready-to-use parts for specific domains, built from the universal M2 patterns:

*   **M1_Biology**: Cell signaling, homeostasis
*   **M1_Chemistry**: Combustion, equilibrium
*   **M1_Optics**: Color synthesis, filtering
*   **M1_Photography**: Exposure control
*   **M1_Mythology**: Cosmological structures, world trees

**Think of it as**: Themed LEGO sets (Space, City, Technic). They use the same universal parts but pre-assemble them into useful domain-specific components.

---

### M0: Finished Showcase Models (Poclets)

These are **completed, minimal, working models** that validate the toolkit:

*   `Fire Triangle` (Chemistry) – Combustion fundamentals
*   `Four-Stroke Engine` (Engineering) – Mechanical cycle
*   `Cell Signaling` (Biology) – 4 communication patterns
*   `Yggdrasil` (Mythology) – Norse cosmological tree
*   `Blood Pressure Control` (Biology) – Cardiovascular regulation
*   `RGB/HSL/CMY/CMYK` (Optics) – Color synthesis family
*   `Exposure Triangle` (Photography) – ISO-Aperture-Speed balance

**Validation criteria**: All 5 ASFID dimensions present, ORIVE scored, minimal yet complete, domain-assigned.

---

## 🚀 Quick Start: Your First Build

Want to model a system? Here's the TSCG workflow:

1.  **Take Inventory (Measure ASFID)**
    Look at your real-world system. Score it (0-1) on each Eagle Eye dimension:
    *   **A**ttractor: What are its goals or stable states?
    *   **S**tructure: How is it organized?
    *   **F**low: What moves in/out? (Nothing is perfectly closed: `F ≥ 0.1`)
    *   **I**nformation: How complex is its state?
    *   **D**ynamics: How fast does it change?

2.  **Check Your Blueprint (Evaluate ORIVE - Optional)**
    Assess the model you're building in your mind:
    *   Can you **O**bserve the key parts?
    *   Can you **R**epresent it clearly?
    *   Is it **I**nteroperable with other models?
    *   Can you **V**erify it against reality?
    *   Is it **E**volvable with new data?

3.  **Assemble the Pattern (Use M2)**
    Browse the 68 patterns. Which ones fit?
    *   Is it a `Network`? A `Feedback` loop? A `Hierarchy`?
    *   Your ASFID scores will point you to the right patterns.

4.  **Install Domain Parts (Apply M1)**
    Does your model fit a known domain (Biology, Optics, etc.)? Use the specialized M1 concepts to refine it.

5.  **Display Your Prototype (Create an M0 Poclet)**
    Is your model **minimal yet complete**? Does it demonstrate a core principle? Document it as a "poclet" to add to the showcase.

---

## 📁 Project Structure

```
tscg/
├── README.md                    # This file
├── ontology/                    # Core TSCG ontologies
│   ├── M3_GenesisSpace.jsonld  # 10D bicephalous basis
│   ├── M3_EagleEye.jsonld      # ASFID (5D Territory)
│   ├── M3_SphinxEye.jsonld     # ORIVE (5D Map)
│   ├── M2_MetaConcepts.jsonld  # 68 universal patterns
│   ├── M1_CoreConcepts.jsonld  # Domain-agnostic concepts
│   ├── M1_extensions/          # Domain-specific extensions
│   ├── poclets/                # 11+ validated minimal systems
│   └── docs/                   # Technical specifications
├── docs/                       # Project documentation
└── src/                        # Source code (C# .NET 10)
```

---

## 🔄 Current Status

**Version 14.1.0 – November 2024**

✅ **Completed**:
- M3 Genesis Space: 10D bicephalous basis fully validated
- M2 Metaconcepts: 68 patterns validated
- M1 Extensions: 5 domains operational
- M0 Poclets: 11+ validated across disciplines

🔄 **In Progress**:
- ORIVE empirical validation
- Expanding poclet portfolio
- Software implementation (TSCG.Orchestrator)

🎯 **Planned**:
- Third-party mathematical validation
- Visualization tools (3D projections of 5D/10D spaces)
- Research paper publication

---

## 📄 Preprint & Prior Work

This framework builds upon foundational research published as a preprint:

**Michel Kern (aka Echopraxium) 2025.** *The Systemic Alphabet: A Foundational Meta-Model for Transdisciplinary Analysis* [Preprint]. Zenodo.  
🔗 **DOI:** [10.5281/zenodo.18471860] 
📥 **Direct download:** [PDF on Zenodo](https://zenodo.org/records/18471860)

*This prior work establishes the philosophical and methodological foundations that evolved into the formalized TSCG framework presented here.*

---

## 🤝 Contributing

TSCG is an open framework. We welcome:
- New poclet analyses
- Metaconcept proposals
- Domain extensions
- Mathematical validation
- Documentation improvements

See [CONTRIBUTING.md](https://github.com/Echopraxium/tscg) for details.

---

## 📚 References

- **Korzybski, A.** (1933). *Science and Sanity*
- **von Bertalanffy, L.** (1968). *General System Theory*
- **Ashby, W.R.** (1956). *Introduction to Cybernetics*
- Dirac notation, Hilbert spaces, tensor products
- Category theory, linear algebra

---

**TSCG Framework v14.1.0**  
*Bridging Theory and Practice Through Systematic Analysis*

**"The map is not the territory, but both are necessary for understanding."**

*Last Updated: February 2026*