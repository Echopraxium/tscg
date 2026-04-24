# TRIZ — Theory of Inventive Problem Solving

**SystemicFramework Instance**  
**Domain:** Systemic Modeling  
**Author:** Genrich Altshuller (1946-1998)  
**TSCG Model:** Echopraxium with the collaboration of Claude AI  
**Version:** 1.0.0  
**Date:** 2026-04-20

---

## 📋 Overview

TRIZ (Teoriya Resheniya Izobretatelskikh Zadatch — "Theory of Inventive Problem Solving") is a systematic innovation methodology developed by Soviet inventor Genrich Altshuller through analysis of over 200,000 patents across all engineering domains. TRIZ identifies **40 universal inventive principles** and a **39×39 contradiction matrix** to guide technical problem-solving.

### Bicephalous Nature (AnzÛ Principle)

- **🦅 Eagle Eye (Territory):** Technical systems being analyzed and improved
- **🦉 Sphinx Eye (Map):** TRIZ methodology itself as prescriptive framework

TRIZ is primarily a **Map** (methodology) that operates on **Territories** (technical systems). The REVOI scores (4.8) are superior to ASFID (4.4), reflecting its nature as an epistemic construction.

---

## 🎯 Core Components

| Component | Count | Description |
|-----------|-------|-------------|
| **Inventive Principles** | 40 | Universal solution patterns |
| **Technical Parameters** | 39 | System attributes for contradiction encoding |
| **Contradiction Matrix** | 39×39 | Maps contradictions → recommended principles |
| **Inventivity Levels** | 5 | Hierarchical classification of solution novelty |
| **Evolution Trends** | 8 | Patterns of technical system evolution |

---

## 🦅 ASFID Scores (Eagle Eye — Territory)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **A — Attractor** | 5.0 | 40 principles as solution attractors; contradiction resolution as ultimate attractor |
| **S — Structure** | 5.0 | Triple hierarchy: 39×39 matrix + 40 principles + evolution laws |
| **F — Flow** | 4.0 | Unidirectional flow (problem→solution); no internal feedback loop |
| **I — Information** | 5.0 | Systematic codification: 39 parameters encode problems, 40 principles encode solutions |
| **D — Dynamics** | 3.0 | Evolution laws present but external to framework; no autonomous dynamics |

**ASFID Mean:** 4.4

---

## 🦉 REVOI Scores (Sphinx Eye — Map)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **R — Representability** | 5.0 | Principles encode solution classes bidirectionally; matrix represents problem→solution space |
| **E — Evolvability** | 4.0 | Framework has evolved (TRIZ extensions); evolution driven by community, not autonomous |
| **V — Verifiability** | 5.0 | Massive empirical validation (200,000+ patents); cross-domain reproducibility |
| **O — Observability** | 5.0 | Principles observable in patents; applications observable in products; fully transparent methodology |
| **Im — Interoperability** | 5.0 | Transdisciplinary by design; compatible with other frameworks (QFD, Lean, Six Sigma) |

**REVOI Mean:** 4.8

---

## 📊 Epistemic Gap Analysis

```
δ₁ = |ASFID_mean - REVOI_mean| / max(ASFID_mean, REVOI_mean)
δ₁ = |4.4 - 4.8| / 4.8 = 0.083
```

**Spectral Class:** **OnCriticalLine** [0.05, 0.15)

**Interpretation:** Low epistemic gap confirms TRIZ is coherent as both Map (methodology) and Territory representation (technical systems). The slight REVOI superiority (4.8 vs 4.4) is expected for a prescriptive framework — it is primarily an epistemic construction.

---

## 🔤 40 Inventive Principles with Codes

Each principle has a **3-5 character abbreviated code** for compact display (e.g., in icosahedron simulation).

### Code Conventions

| Symbol | Meaning | Example |
|--------|---------|---------|
| **#** | "tion", "sion", "ion" | Sgm# = Segmentation |
| **%** | "ing" | Merg% = Merging |
| **Y** | "y" (suffix) | AsmY = Asymmetry |
| **$** | "ics" | Dyn$ = Dynamics |
| **==** | "Through" | Rus== = Rushing Through |
| **:=** | "Change" (Pascal) | Clr:= = Color Changes |
| **&** | "and" | Ds&Rc = Discarding & Recovering |
| **\*** | "ant" | Oxy*+ = Oxidant |
| **@** | "rial" (material) | PorM@ = Porous Material |

---

### Complete Principle List

| # | Principle | Code | Family |
|---|-----------|------|--------|
| 1 | Segmentation | **Sgm#** | Transformational |
| 2 | Extraction | **Xtrc#** | Transformational |
| 3 | Local Quality | **LocQ** | Transformational |
| 4 | Asymmetry | **AsmY** | Transformational |
| 5 | Merging | **Merg%** | Compositional |
| 6 | Universality | **UnivY** | Compositional |
| 7 | Nesting | **Nest#** | Transformational |
| 8 | Anti-weight | **AWght** | Physicochemical |
| 9 | Preliminary Anti-action | **PrAA#** | Geometric |
| 10 | Preliminary Action | **PrA#** | Methodological |
| 11 | Beforehand Cushioning | **B4Cus** | Methodological |
| 12 | Equipotentiality | **EquiP** | Geometric |
| 13 | Do it in Reverse | **DIIR** | Transformational |
| 14 | Spheroidality | **SphrY** | Transformational |
| 15 | Dynamics | **Dyn$** | Transformational |
| 16 | Partial/Excessive Action | **P/ExA** | Methodological |
| 17 | Another Dimension | **OthD#** | Transformational |
| 18 | Mechanical Vibration | **MecV#** | Geometric |
| 19 | Periodic Action | **PerA#** | Methodological |
| 20 | Continuity of Useful Action | **CUA#** | Methodological |
| 21 | Rushing Through | **Rus==** | Methodological |
| 22 | Convert Harm into Benefit | **CH2B** | Geometric |
| 23 | Feedback | **FeedB** | Methodological |
| 24 | Intermediary | **IntmY** | Substitution |
| 25 | Self-service | **SlfS** | Methodological |
| 26 | Copying | **Copy%** | Substitution |
| 27 | Cheap Short-lived Objects | **CSLO** | Substitution |
| 28 | Replacement of Mechanical System | **RMS** | Physicochemical |
| 29 | Pneumatics or Hydraulics | **P/H$** | Physicochemical |
| 30 | Flexible Shells or Thin Films | **FS/TF** | Physicochemical |
| 31 | Porous Materials | **PorM@** | Physicochemical |
| 32 | Color Changes | **Clr:=** | Transformational |
| 33 | Homogeneity | **HmgY** | Substitution |
| 34 | Discarding and Recovering | **Ds&Rc** | Transformational |
| 35 | Transformation of Properties | **Prp:=** | Transformational |
| 36 | Phase Transition | **Phs:=** | Physicochemical |
| 37 | Thermal Expansion | **ThXp#** | Physicochemical |
| 38 | Strong Oxidants | **Oxy*+** | Physicochemical |
| 39 | Inert Atmosphere | **InAtm** | Physicochemical |
| 40 | Composite Materials | **CmpM@** | Compositional |

---

## 🏗️ Principle Families

### 1. Methodological (8 principles)
**GenericConceptCombo:** Process ⊗ Workflow ⊗ Pattern

Systematic application of universal patterns through prescribed steps.

**Members:** #10 PrA#, #11 B4Cus, #16 P/ExA, #19 PerA#, #20 CUA#, #21 Rus==, #23 FeedB, #25 SlfS

---

### 2. Transformational (12 principles)
**GenericConceptCombo:** Transformation ⊗ Pattern

Structural transformation guided by reusable patterns.

**Members:** #1 Sgm#, #2 Xtrc#, #3 LocQ, #4 AsmY, #7 Nest#, #13 DIIR, #14 SphrY, #15 Dyn$, #17 OthD#, #32 Clr:=, #34 Ds&Rc, #35 Prp:=

---

### 3. Compositional (3 principles)
**GenericConceptCombo:** Composition ⊗ Modularity

Modular combination creating emergent functionality.

**Members:** #5 Merg%, #6 UnivY, #40 CmpM@

---

### 4. Physicochemical (9 principles)
**KnowledgeFieldConceptCombo:** Pattern ⊗ Transformation (Physics/Chemistry)

Inventive principles based on physical or chemical phenomena.

**Members:** #8 AWght, #28 RMS, #29 P/H$, #30 FS/TF, #31 PorM@, #36 Phs:=, #37 ThXp#, #38 Oxy*+, #39 InAtm

---

### 5. Substitution (4 principles)
**GenericConceptCombo:** Transformation ⊗ Pattern (substitution context)

Strategic replacement guided by functional equivalence.

**Members:** #24 IntmY, #26 Copy%, #27 CSLO, #33 HmgY

---

### 6. Geometric (4 principles)
**GenericConceptCombo:** Pattern ⊗ Space

Spatial or geometric optimization of system structure.

**Members:** #9 PrAA#, #12 EquiP, #18 MecV#, #22 CH2B

---

## 🧬 GenericConcepts Mobilized

### M2 GenericConcepts (16)
- Attractor, Pattern, Transformation, Hierarchy
- Trade-off, Constraint, Code, Coding
- Network, Modularity, Process, Workflow
- Information, Representation, Observable, Interoperability

### M1 Core GenericConceptCombos (3)
- **MethodologicalPrinciple:** Process ⊗ Workflow ⊗ Pattern
- **TransformationalPrinciple:** Transformation ⊗ Pattern
- **CompositionalPrinciple:** Composition ⊗ Modularity

### M1 Systemic Modeling Extension (6)
- **SubstitutionPrinciple:** Transformation ⊗ Pattern | substitution_context
- **GeometricPrinciple:** Pattern ⊗ Space | geometric_optimization
- **PhysicochemicalPrinciple:** Pattern ⊗ Transformation | physicochemical_domain
- **ContradictionMatrix:** S ⊗ S ⊗ I (39×39 problem→solution encoding)
- **InventivityLevel:** S ⊗ I ⊗ A (5-level novelty hierarchy)
- **TechnicalParameter:** I ⊗ S (39 system attributes)

---

## 🎨 Simulation Architecture

### Icosahedron Geometry
- **Base shape:** Icosahedron (20 faces)
- **Subdivision:** Each face divided into 2 right triangles
- **Total triangles:** 40 (perfect mapping to 40 principles)
- **Display:** Each triangle shows its principle code (3-5 characters)

### Interactions
- **Hover:** Tooltip with full principle name
- **Click:** Panel with principle description + examples
- **Color coding:** By family (Methodological, Transformational, etc.)
- **Rotation:** Interactive 3D camera controls

### Technology
- **3D Engine:** BabylonJS 6.26.0
- **Format:** Standalone HTML (no external fetch)
- **Deployment:** `instances/systemic-frameworks/Triz/M0_Triz_Simulation.html`

---

## 📚 References

- Altshuller, G. (1984). *Creativity as an Exact Science*
- Altshuller, G. (1996). *And Suddenly the Inventor Appeared*
- Mann, D. (2002). *Hands-On Systematic Innovation*
- Salamatov, Y. (1999). *TRIZ: The Right Solution at the Right Time*
- [The TRIZ Journal](https://triz-journal.com/)

---

## 📁 File Structure

```
instances/systemic-frameworks/Triz/
├── M0_Triz.jsonld                    # Main ontology
├── M0_Triz_README.md                 # This file
└── M0_Triz_Simulation.html           # Interactive icosahedron (planned)
```

---

## 🔗 Related TSCG Components

- **M3 Genesis Space:** Bicephalous foundation (ASFID/REVOI)
- **M2 GenericConcepts:** 16 atomic patterns mobilized
- **M1 Core Concepts:** 3 GenericConceptCombos defined
- **M1 Systemic Modeling:** 6 framework-specific concepts
- **M1 Domains:** Systemic Modeling domain (20th entry)

---

## 🌐 External Resources

- **International TRIZ Association (MATRIZ):** [https://www.matriz.org](https://www.matriz.org)
  - Global organization for TRIZ development and certification
  - Conference proceedings, research papers, and educational materials
  - Professional network of TRIZ practitioners and consultants

---

## 📝 Changelog

### v1.1.0 (2026-04-24)
- Added 20 case studies with real-world applications
- Improved visualization with CSG boolean operations for tube/triangle cutting
- Added family legend in controls bar with interactive filtering
- Implemented Reset and Auto-Rotate buttons
- Added MATRIZ link in description panel
- Enhanced UI with Home and TSCG navigation buttons

### v1.0.0 (2026-04-20)
- Initial TRIZ SystemicFramework modeling
- Complete 40 inventive principles with abbreviated codes
- ASFID/REVOI scoring (4.4 / 4.8, δ₁=0.083)
- 6 principle families with GenericConceptCombo mapping
- M1 extension created (M1_SystemicModeling.jsonld)
- 3 new M1 Core GenericConceptCombos added
- Code conventions established for icosahedron simulation

---

**TSCG Architecture:** M3 (Genesis) → M2 (GenericConcepts) → M1 (Domains/Combos) → M0 (TRIZ Instance)

**Epistemic Status:** OnCriticalLine (δ₁=0.083) — Coherent bicephalous alignment between Map and Territory
