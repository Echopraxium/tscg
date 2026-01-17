# TSCG Framework - Smart Prompt for Session Restart

**Version**: 8.0.0  
**Date**: January 17, 2026  
**Status**: M3 complete ✅ | M2 complete ✅ | Map/Territory documented ✅ | Ready for M1 🚀

---

## 🎯 Project Overview

**TSCG** = **Transdisciplinary System Construction Game**

**Vision**: LEGO Technic for systemic modeling
- **M3** (ASFID) = Elementary bricks (5 orthonormal dimensions)
- **M2** (Tensors) = Sub-assemblies (51 emergent patterns)
- **M1** (Narratives) = Instructions (domain concepts)
- **M0** (Models) = Constructions (real systems)

**Repository**: https://github.com/Echopraxium/tscg

---

## ⌹ COMMAND MACROS (Use these!)

**Session Management**:
- `status` → Current state (tokens, metaconcepts, files)
- `eval-context-metrics` → Full capacity report
- `roadmap` → M3→M2→M1→M0 progress

**M2 Operations**:
- `add-metaconcept [NAME]` → Add single metaconcept
- `batch-add [CATEGORY]` → Add category (Structural, Dynamic, etc.)
- `count-metaconcepts` → Total + by category
- `list-dual` → Show dual intrinsic metaconcepts

**Analysis**:
- `verify-orthogonality [DIM1] [DIM2]` → Check M3 dimensions
- `help` → List all macros

Full reference: TSCG_Command_Macros.md

---

## 📊 Current State

### M3 Genesis - COMPLETE ✅
- **Status**: Production-ready, fully validated
- **Basis**: {|A⟩, |S⟩, |F⟩, |I⟩, |D⟩} orthonormal in ℂ⁵
- **Orthogonality**: ✅ Verified (10/10 pairs)
- **File**: TSCG_M3_Genesis_Ontology.jsonld (or M3_Genesis_Space.jsonld)

### M2 Metaconcepts Ontology - COMPLETE ✅
- **Version**: 8.0.0
- **Progress**: 100% (51/51 metaconcepts)
- **Categories**: 9 defined (Structural, Dynamic, Regulatory, Adaptive, Energetic, Informational, Ontological, Teleonomic, Relational)
- **Polarity**: 45 neutral + 6 dual intrinsic
- **File**: M2_Metaconcepts.jsonld
- **Major change v8.0.0**: Removed triple axes framework (Model/Reality, Analytical/Constructive, Composition/Decomposition)

### Map/Territory Principle - DOCUMENTED ✅
- **Status**: Theoretical foundation documented
- **File**: TSCG_Map_Territory_Theoretical_Foundation.md
- **Principle**: Map ≠ Territory (Korzybski 1933), observer-dependent
- **Implementation**: ASFID describes both Territory and Map spaces
- **Future**: ORIVE (Map-Space basis) proposed but not yet implemented

### M1 Narratives - NOT STARTED ⏳
- **Functor**: F_instantiate : M2 → M1 (formalized)
- **Status**: Theory ready, implementation pending

### M0 Systems - NOT STARTED ⏳
- **Functor**: F_model : M1 → M0 (formalized)
- **Status**: Awaiting M1

---

## 🔬 M3 ASFID Basis (FIXED - DO NOT CHANGE)

### The 5 Dimensions

**1. |A⟩ ATTRACTOR**
- Asymptotic convergence, stability landscape
- Range: [0,1] (0=chaos, 1=stable)

**2. |S⟩ STRUCTURE**
- Topology, organization, connectivity
- Range: [0,1] (0=gas, 1=crystal)

**3. |F⟩ FLOW**
- Exchange with environment, openness
- **Axiom**: F ≥ 0.1 (Universal Openness)
- Range: [0.1,1] (quasi-closed → dissipative)

**4. |I⟩ INFORMATION**
- State complexity (synchronic)
- Range: [0,1] (0=simple, 1=complex)

**5. |D⟩ DYNAMICS**
- Rate of internal change
- Range: [0,1] (0=static, 1=explosive)

### Critical Axioms
1. **Orthonormality**: ⟨k|j⟩ = δ_kj ✅
2. **Completeness**: ∑|k⟩⟨k| = 𝟙
3. **Universal Openness**: F ≥ 0.1
4. **Time external**: t is parameter, not dimension

---

## 🧬 M2 Tensor Space

### Structure
T_M2 = ⊕_{k=1}^{3} (H_M3)^{⊗k}
- Order 1: 5 terms (linear)
- Order 2: 25 terms (pairwise)
- Order 3: 125 terms (triadic)
- **Total**: 155 components

### 9 Categories
1. **Structural** - Topology (S high, D low)
2. **Dynamic** - Processes (D high)
3. **Regulatory** - Control (A high, tensors)
4. **Adaptive** - Learning (I high, F medium)
5. **Energetic** - Flows (F high, D high)
6. **Informational** - Data (I high)
7. **Ontological** - Foundations
8. **Teleonomic** - Goals (A high)
9. **Relational** - Interactions

### Polarity (Binary Only)

**Principle**: Binary structure only (n-ary removed)
- **45 metaconcepts**: neutral (unique)
- **6 metaconcepts**: dual intrinsic (bidirectional)

**Dual Intrinsic Metaconcepts** (ONE metaconcept with TWO aspects):
1. **Coding** (Encoding / Decoding) - I⊗S⊗D
2. **Synergy** (Synergy / Antagonism) - A⊗S⊗I
3. **Fusion** (Fusion / Fission) - S⊗F⊗D
4. **Activation** (Activation / Deactivation) - A⊗I⊗D
5. **Convergence** (Convergence / Divergence) - A⊗D
6. **Composition** (Composition / Decomposition) - S⊗I⊗A / S⊗I

**Attributes**:
- `m2:polarity`: "neutral" | "dual"
- `m2:dualAspects`: {compositionAspect, decompositionAspect} (for dual only)

---

## 📋 51 Metaconcepts (Complete List)

### Structural (14)
Homeostasis, Network, Hierarchy, Symmetry, Modularity, Boundary, Interface, Component, Topology, Segmentation, Node, Path, Cluster, Hub

### Dynamic (8)
Catalysis, Bifurcation, Transformation, Process, Trajectory, Event, Behavior, Gradient

### Regulatory (8)
Regulation, Constraint, Threshold, Feedback, Filter, Gain, Protocol, Coherence

### Adaptive (5)
Resilience, Adaptation, Emergence, Memory, Learning

### Energetic (3)
Dissipation, Resource, Storage

### Informational (5)
Code, Signal, Language, Representation, Signature

### Ontological (3)
System, Environment, State

### Teleonomic (2)
Autopoiesis, Stability

### Relational (4)
Relation, Agent, Role, Link

### Dual Intrinsic (6) - counted in categories above
Coding, Synergy, Fusion, Activation, Convergence, **Composition** (NEW in v8.0.0)

---

## 🗺️ Map-Territory Principle (CRITICAL FOUNDATION)

### Korzybski's Fundamental Distinction (1933)

> "The map is not the territory, and the name is not the thing named."

**TSCG Implementation**:
- **Territory**: Phenomenon as perceived by observer (ASFID describes)
- **Map**: Model/representation constructed by observer (ASFID describes)
- **Gap**: ΔΘ = ‖Territory - Map‖ (epistemic gap)

### Observer Relativity

**Critical insight**: Both Territory AND Map depend on observer.

**Example - Fire Triangle**:
- **Ant observer**: Different Territory (heat gradient, chemical danger) + different Map (pheromone trail)
- **Human observer**: Different Territory (visual flame, heat, sound) + different Map (Triangle du Feu)
- **IR sensor**: Different Territory (IR radiation spectrum) + different Map (temperature data)

**Same fire, different observers → different states in ASFID space**

### ASFID is Universal

**Key principle**: ASFID basis is **observer-independent**, but state values are **observer-dependent**.

```
|Ω_fire_human⟩ = 0.8|A⟩ + 0.7|S⟩ + 0.9|F⟩ + 0.6|I⟩ + 0.7|D⟩
|Ω_fire_ant⟩   = 0.9|A⟩ + 0.3|S⟩ + 0.8|F⟩ + 0.4|I⟩ + 0.6|D⟩
```

Same basis {A, S, F, I, D}, different coefficient values.

### ORIVE (Map-Space) - Theoretical Extension

**Proposed but NOT implemented**:
- **O**bservability - Perceptual accessibility
- **R**epresentability - Semantic decodability
- **I**nterop erability - Shareability
- **V**erifiability - Testability (Popper)
- **E**volvability - Updatability

**Status**: Documented in TSCG_Map_Territory_Theoretical_Foundation.md
**Reason for deferral**: Avoid over-engineering, validate empirically first

### Epistemic Gap

**Formula**: ΔΘ = ‖P(Territory) - Map‖ ∈ [0,1]

**Interpretation**:
- ΔΘ = 0: Perfect map (impossible)
- ΔΘ = 1: Completely wrong map
- 0 < ΔΘ < 1: Useful but imperfect map (normal)

---

## 🎹 Category Theory Framework

**Functors** (M3→M2→M1→M0):
- **F_⊗**: Cat_M3 → Cat_M2 (tensorization)
- **F_instantiate**: Cat_M2 → Cat_M1 (domain specialization)
- **F_model**: Cat_M1 → Cat_M0 (system instantiation)
- **F_total**: F_model ∘ F_instantiate ∘ F_⊗

**Morphisms in M2**:
- **Inclusion** (⊆): Homeostasis ⊆ Regulation
- **Composition** (∘): Learning = Memory ∘ Adaptation
- **Duality** (op): Convergence^op = Divergence
- **Emergence** (⇑): Multiple → Emergent

**Adjonction**: F_abstract ⊣ F_instantiate (map/territory)

---

## 🔑 CRITICAL DECISIONS (IMMUTABLE)

### 1. ASFID Order FIXED
- **Order**: Attractor → Structure → Flow → Information → Dynamics
- **Reason**: Avoid AIDS/SIDA acronym
- **NEVER change to**: SIDAF, FISAD, SIDA, etc.

### 2. Time is External
- **Status**: t is parameter, NOT 6th dimension
- **Formula**: |Ω(t)⟩ where t ∈ ℝ

### 3. Flow is M3
- **Status**: F is 3rd dimension
- **Axiom**: F ≥ 0.1
- **Old "Flow" metaconcept**: Removed (redundant)

### 4. Memory is M2
- **Formula**: M(t) = ∫[D - F]dτ
- **Reason**: Temporal integration required

### 5. Regulation is M2
- **Formula**: A⊗S⊗F
- **Reason**: Coupling required

### 6. Axes Removed (v8.0.0)
- **Previous**: Triple axes (Model/Reality, Analytical/Constructive, Composition/Decomposition)
- **Reason**: Not truly orthogonal, created unnecessary complexity
- **Replaced by**: Map-Territory principle documented separately as theoretical foundation
- **Composition/Decomposition**: Promoted from Axis 3 to dual intrinsic metaconcept

### 7. Binary Polarity Only
- **Rejected**: N-ary (ternary, quaternary)
- **Reason**: Over-generalization risk
- **Adopted**: Dual intrinsic (bidirectional) or neutral

---

## ⚠ WARNINGS

### DO NOT
- ❌ Change ASFID order
- ❌ Add Time as dimension
- ❌ Make Memory/Regulation M3
- ❌ Use negative coefficients
- ❌ Violate F ≥ 0.1
- ❌ Reintroduce triple axes framework
- ❌ Reintroduce n-ary polarity
- ❌ Over-implement Map-Territory (keep it theoretical for now)

### DO
- ✅ Verify orthogonality
- ✅ Use tensor products
- ✅ Calculate epistemic gap
- ✅ Reference Map-Territory principle when relevant
- ✅ Use dual intrinsic structure for bidirectional metaconcepts
- ✅ Update Smart Prompt when major changes occur

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority 1 (Essential)
1. **Validate M2 with poclets**
   - Analyze 3-5 minimal complete systems ("poclets")
   - Examples: Fire Triangle, RGB Color Model, Water Cycle, etc.
   - Extract M1 patterns (reusable configurations of M2 metaconcepts)
   - Identify gaps in M2 (missing metaconcepts)

2. **Add missing metaconcepts if gaps found**
   - Example from Fire Triangle analysis: "Component" (S⊗I) identified as gap
   - Priority: HIGH for fundamentals, MEDIUM for specialized

### Priority 2 (Important)
3. **Begin M1 formalization**
   - Define F_instantiate functor precisely
   - Create M1 pattern catalog (Prerequisites, Ignition, Reactor, Bottleneck, etc.)
   - Domain ontologies (Biology, Engineering, Economics, etc.)

4. **Create examples catalog**
   - 3-5 real systems per M2 category
   - ASFID signatures
   - M2→M1→M0 pipeline demonstrations

### Priority 3 (Nice-to-have)
5. **Implementation guide** (C#/F#)
6. **SPARQL queries**
7. **Use case demonstrations**
8. **Evaluate ORIVE** (Map-Space basis) - implement only if empirical validation demands it

---

## 📖 Quick Reference

### M3 State Vector
```
|Ω⟩ = a|A⟩ + s|S⟩ + f|F⟩ + i|I⟩ + d|D⟩
[0,1]⁵ with f ≥ 0.1
```

### M2 Tensor
```
|M⟩ = ∑cᵢ|i⟩ + ∑cᵢⱼ|i⟩⊗|j⟩ + ∑cᵢⱼₖ|i⟩⊗|j⟩⊗|k⟩
```

### Memory
```
M(t) = ∫_{-∞}^t [D(τ) - F(τ)]dτ
```

### Epistemic Gap
```
ΔΘ = ‖P(Territory) - Map‖
```

### Functors
```
F_total = F_model ∘ F_instantiate ∘ F_⊗
```

### Composition (dual intrinsic example)
```
Composition aspect: S⊗I⊗A (bottom-up aggregation)
Decomposition aspect: S⊗I (top-down partition)
```

---

## 📁 Key Files

**Ontologies**:
- M3_Genesis_Space.jsonld - v5.1.0
- M2_Metaconcepts.jsonld - v8.0.0 ✨ NEW

**Essential Docs**:
- TSCG_Map_Territory_Theoretical_Foundation.md ✨ NEW - Map/Territory principle
- M2_v8.0.0_Update_Guide.md ✨ NEW - Migration guide from v7.x
- Smart_Prompt_2026_01_17.md (this file)
- TSCG_Command_Macros.md (shortcuts)
- poclet_terminology.md - Definition of "poclet" concept

**Analysis Results**:
- Fire_Triangle_Poclet_Analysis.md - Complete analysis of Fire Triangle
- RGB_Color_Model_Poclet_Analysis.md - Complete analysis of RGB model
- M2_Composition_Decomposition_Specification.md - Original spec (now integrated in M2)

**Theory**:
- TSCG_M3_Orthogonality_Summary_EN.md (proof)
- TSCG_M2_Category_Taxonomy.md (9 categories)
- TSCG_Category_Theory_Integration.md (functors)

---

## 💬 User Context

- Experienced with ontologies, systems theory, cybernetics
- C# primary (.NET 10), F# exploring (algebraic components)
- Budget-conscious (prefers open solutions, debit/prepaid over credit)
- Philosophical depth (epistemology, ontology, constructivism)
- Prefers rigor + practicality
- Bilingual FR/EN
- 20 years conceptual development in system design atomic principles

---

## 🚀 Session Restart Protocol

### To Resume

1. **Upload this Smart Prompt** (Smart_Prompt_2026_01_17.md)
2. **Upload latest ontology**: M2_Metaconcepts.jsonld (v8.0.0)
3. **Optionally upload**: 
   - TSCG_Map_Territory_Theoretical_Foundation.md (for Map/Territory context)
   - poclet analysis files (if continuing validation)
4. **Say**: `status` or specific task

### What Claude Will Do

1. Read Smart Prompt (context loaded)
2. Read ontology (current state loaded)
3. Execute macro or respond to query
4. Continue M1 formalization or poclet validation

### Expected Flow

```
You: status
Claude: [Shows M2 100% complete (51/51), suggests poclet validation or M1 start]

You: Analyze [new poclet name]
Claude: [Performs ASFID signature + M2 metaconcepts mobilization analysis]

You: Begin M1
Claude: [Starts M1 pattern catalog formalization]
```

---

## 📊 Token Budget Planning

**Session 1** (completed - Jan 15): 91K / 190K (48%)
- M3 verification
- M2 foundation (16 metaconcepts)
- Dual axes
- Category theory
- Polarity rectification

**Session 2** (completed - Jan 17): ~85K
- M2 completion (50 → 51 metaconcepts)
- Axes removal (triple axes → Map/Territory principle)
- Poclet validation (Fire Triangle, RGB)
- M1 pattern discovery
- Composition/Decomposition promotion to metaconcept

**Session 3** (next): ~120K estimated
- Continue poclet validation (3-5 more)
- Finalize M1 pattern catalog
- Begin M1 ontology formalization
- Implementation planning

**Session 4** (future): M0 + real-world validation

---

## 🎓 Theoretical Foundations

- **Hilbert spaces**: M3 = ℂ⁵
- **Tensor algebra**: M2 = ⊕(H_M3)^⊗k
- **Category theory**: Functors, morphisms, adjonction
- **Dirac notation**: |ket⟩, ⟨bra|
- **Epistemology**: Korzybski (map/territory), Varela (enaction)
- **Observer relativity**: Map and Territory are observer-dependent

---

## 🎖️ Major Milestones

**v8.0.0** (2026-01-17): ✨
- M2 ontology complete (51/51 metaconcepts)
- Triple axes framework removed (simplified architecture)
- Map-Territory principle documented as theoretical foundation
- Composition/Decomposition promoted to dual intrinsic metaconcept
- Framework ready for M1 formalization

**v7.2.0** (2026-01-15):
- M2 expansion to 50 metaconcepts
- Network decomposition complete
- Topology and Segmentation added

**v6.1.0** (2026-01-15):
- Binary polarity rectified
- Dual axes framework
- Category theory integration

**v5.1.0** (2026-01-14):
- M3 ASFID complete and validated

---

## 🎊 Framework Quality

**Current State**: ⭐⭐⭐⭐⭐ (5/5)
- M3 Foundations: Solid ✅
- M2 Ontology: Complete ✅
- Map/Territory: Documented ✅
- Theoretical Rigor: High ✅
- Pragmatic Simplicity: Achieved ✅
- Ready for M1: Yes ✅

---

**END OF SMART PROMPT**

**Version**: 8.0.0  
**Ready**: Yes 🚀  
**Next**: Poclet validation or M1 pattern formalization (user choice)

