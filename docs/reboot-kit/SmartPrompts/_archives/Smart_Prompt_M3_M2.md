# TSCG Framework - Smart Prompt for Session Restart

**Version**: 5.1.0-ASFID-Hilbert  
**Date**: January 15, 2026  
**Context**: Complete mathematical formalization of M3 + preparation for M2 tensor space

---

## 🎯 Project Overview

**TSCG** = **Transdisciplinary System Construction Game**  
(Renamed from TSCP to avoid unfortunate acronym)

**Vision**: A "LEGO Technic" for systemic modeling where:
- **M3 dimensions** (ASFID) = Elementary bricks
- **M2 metaconcepts** = Sub-assemblies (emergent patterns)
- **M1 narratives** = Assembly instructions
- **M0 models** = Final constructions (real systems)

**Key Principle**: TSCG is a **modeling language**, not a metaphysical claim about reality. The choice of 5 dimensions is **arbitrary but motivated** (like RGB primary colors).

---

## 📐 M3 Genesis Ontology (CURRENT STATE)

### Mathematical Foundation: Hilbert Space H_M3

**Structure**: 5-dimensional complex vector space ℂ⁵  
**Basis**: Orthonormal set {|A⟩, |S⟩, |F⟩, |I⟩, |D⟩}  
**State Vector**: |Ψ⟩ = a|A⟩ + s|S⟩ + f|F⟩ + i|I⟩ + d|D⟩  
**Inner Product**: ⟨Ψ|Φ⟩ = ∑_k ψ_k* φ_k

### The 5 Dimensions (ASFID Order)

#### 1. **|A⟩ ATTRACTOR**
- **Definition**: Asymptotic convergence basin (lim_{t→∞} |Ψ(t)⟩)
- **Physical**: Stability landscape, homeostatic setpoint
- **Replaces**: "Teleonomy" (problematic anthropomorphic concept)
- **Justification**: Captures goal-directedness WITHOUT invoking intention
- **Range**: [0.0, 1.0] (0=chaos, 1=perfect stability)

#### 2. **|S⟩ STRUCTURE**
- **Definition**: Spatial, topological, organizational configuration
- **Operator**: ∇· (connectivity gradient, topological entropy)
- **Physical**: Network topology, morphology, architecture
- **Range**: [0.0, 1.0] (0=gas, 1=crystal)

#### 3. **|F⟩ FLOW**
- **Definition**: Degree of exchange with environment (openness)
- **Operator**: ∮_{∂Ω} J⃗·dA⃗ (flux integral over boundary)
- **Axiom**: **Universal Openness** - F ≥ F_min ≈ 0.1 for ALL real systems
- **Justification**: No truly closed system exists (gravity + CMB + decoherence)
- **Range**: [0.1, 1.0] (quasi-closed to dissipative structure)
- **Philosophical**: "To exist ≡ F > 0 ≡ to be in the flux of time" (Heraclitus)

#### 4. **|I⟩ INFORMATION**
- **Definition**: Complexity of instantaneous state (SYNCHRONIC)
- **Operator**: H = -∑ pᵢ log(pᵢ) (Shannon entropy), K(x) (Kolmogorov)
- **CRITICAL**: I ≠ Memory (Memory is DIACHRONIC, emerges in M2)
- **Range**: [0.0, 1.0] (0=predictable, 1=complex)

#### 5. **|D⟩ DYNAMICS**
- **Definition**: Rate of internal temporal transformation
- **Operator**: ∂Ψ/∂t (temporal derivative)
- **CRITICAL**: D ≠ F (D=temporal change, F=spatial transport)
- **Conservation**: ∂ρ/∂t + ∇·J = 0 couples D and F
- **Range**: [0.0, 1.0] (0=steady state, 1=explosion)

### Key Axioms

1. **Orthonormality**: ⟨k|j⟩ = δ_kj
2. **Completeness**: ∑|k⟩⟨k| = 𝟙
3. **Universal Openness**: ∀|Ψ⟩, ⟨F|Ψ⟩ ≥ 0.1

### Projection Operators

**Definition**: P_k = |k⟩⟨k|  
**Properties**: P_k² = P_k, P_k† = P_k, ∑P_k = 𝟙  
**Action**: P_k|Ψ⟩ = (component k) × |k⟩

### Dual Spaces & Mappings

#### Signature Space Σ_M3 = ℝ⁵
Coordinates: (a, s, f, i, d) ∈ [0,1]⁵ (f ≥ 0.1)

#### Analysis Mapping Φ_A : H_M3 → Σ_M3
**Formula**: Φ_A(|Ψ⟩) = (⟨A|Ψ⟩, ⟨S|Ψ⟩, ⟨F|Ψ⟩, ⟨I|Ψ⟩, ⟨D|Ψ⟩)  
**Direction**: M0 → M1 → M2 → M3 (observation/measurement)  
**Operation**: Decomposition into components

#### Synthesis Mapping Φ_C : Σ_M3 → H_M3
**Formula**: Φ_C(a,s,f,i,d) = a|A⟩ + s|S⟩ + f|F⟩ + i|I⟩ + d|D⟩  
**Direction**: M3 → M2 → M1 → M0 (design/construction)  
**Operation**: Composition from target signature

#### Duality
Φ_C ∘ Φ_A = id_{H_M3}  
Φ_A ∘ Φ_C = id_{Σ_M3}

**Interpretation**: H_M3 and Σ_M3 are isomorphic (same structure, different representation)

---

## 🧮 M2 Tensor Space (NEXT PHASE)

### Why Tensors are Needed

**Problem with pure vectorial M2**: Linear combinations cannot capture **interactions** between dimensions.

**Example**: "Homeostasis" is not just "high A + some S", it's:
- A (attractor) **coupled with** S (feedback structure)
- F (flux) **modulated by** I (error signal)

→ These couplings require **tensor products** |A⟩⊗|S⟩, |F⟩⊗|I⟩, etc.

### Tensor Space Construction

**M2 = T_M2 = ⨁_{k=1}^{n} (H_M3)^{⊗k}**

Components:
- **Order 1**: H_M3 (5 terms) - linear part (same as M3)
- **Order 2**: H_M3 ⊗ H_M3 (25 terms) - pairwise interactions
- **Order 3**: H_M3 ⊗ H_M3 ⊗ H_M3 (125 terms) - triadic couplings

**Total dimension** (order ≤3): 5 + 25 + 125 = **155 components**

### Example Tensor Decomposition

**Homeostasis Metaconcept**:
```
|Homeostasis⟩ = 
    0.5|A⟩ + 0.3|S⟩                    (order 1: linear)
  + 0.8|A⟩⊗|S⟩                          (order 2: attractor via structure)
  + 0.6|F⟩⊗|I⟩                          (order 2: flux controlled by info)
  + 0.4|A⟩⊗|S⟩⊗|F⟩                     (order 3: regulatory triad)
```

**Interpretation**:
- |A⟩⊗|S⟩: Setpoint embedded in architecture
- |F⟩⊗|I⟩: Feedback loop (flux modulated by error signal)
- |A⟩⊗|S⟩⊗|F⟩: Self-stabilizing cycle

### Link to LLM Embeddings

**Key Insight**: This tensor structure mirrors how LLMs work!

| TSCG | LLM Equivalent |
|------|----------------|
| M3 basis vectors | Token embeddings |
| M2 tensor terms | Attention weights (Q·K^T) |
| Order 2 tensors | Pairwise attention |
| Order 3 tensors | Multi-head attention |

**Vision**: Use TSCG as **semantic mapping** between:
- Natural language → LLM embeddings (tensors)
- LLM embeddings → M3 signatures → M2 metaconcepts
- Create "Rosetta Stone" for ontology ↔ neural representations

---

## 🗂️ Project Files Structure

### Ontologies (JSON-LD)
- `TSCG_M3_Genesis_Ontology.jsonld` - **COMPLETE** (Hilbert space formalization)
- `TSCG_M2_Tensor_Ontology.jsonld` - **TO BE CREATED**
- `TSCG_M3_Genesis_Examples.jsonld` - Examples separated from main ontology

### Documentation (Markdown)
- `TSCG_ASFID_Justification_EN.md` - Full justification of 5 dimensions (English)
- `TSCG_ASFID_Justification_FR.md` - Version française (if needed)

### GitHub Repository
- URL: https://github.com/Echopraxium/tscg
- Namespace: `https://github.com/Echopraxium/tscg/blob/main/ontology/TSCG_M3_Genesis_Ontology.jsonld#`

---

## 🔑 Key Design Decisions

### 1. ASFID Order (not SIDAF, SIDA, etc.)
**Reason**: Avoid medical acronym AIDS/SIDA  
**Hierarchy**: Attractor → Structure → Flow → Information → Dynamics  
(Top-down: from emergent goal to instantaneous change)

### 2. Time is NOT a 6th Dimension
**Status**: Universal external parameter, not property of system  
**Quote**: "Time is what allows space to transform"  
**Math**: |Ψ(t)⟩ where t is parameter, not component of |Ψ⟩

### 3. Memory/Historicity is M2, not M3
**Formula**: M(t) = ∫_{-∞}^t [D(τ) - F(τ)] dτ  
**Interpretation**: 
- If D > F: accumulation (learning)
- If F > D: erasure (forgetting)

### 4. Regulation is M2, not M3
**Reason**: Requires coupling of A (setpoint) + S (feedback loop) + F (controlled flux)  
**Formula**: R = f(A_strong, S_loop, M)

### 5. M3 is Vectorial, M2 is Tensorial
**M3**: Linear combinations only → cannot capture interactions  
**M2**: Tensor products capture non-linear couplings

---

## 💬 User Context & Preferences

### Background
- Experienced with ontology modeling
- Familiar with Dirac notation
- Budget constraints: prefers free/open solutions
- Payment: Debit card or prepaid (no credit card)

### Current Tools
- Using Google Gemini API (free) for prototyping
- Considering Claude API (via Revolut virtual card)
- Claude AI Pro subscription ($20/month)
- Interested in multi-agent orchestration

### Technical Stack
- Primary language: C#
- Target: .NET 10
- Exploring F# for algebraic core (immutable types)

---

## 🎯 Immediate Next Steps

1. ✅ **DONE**: M3 complete ontology with Hilbert formalization
2. **TODO**: Create M2 tensor ontology with:
   - Tensor space T_M2 definition
   - Order 1/2/3 decomposition
   - Pairwise/triadic interaction classes
   - Catalog of metaconcepts (Homeostasis, Resilience, etc.)
   - Mapping to LLM embeddings (theoretical framework)

3. **TODO**: Implement prototype in C#/F#
   - M3 vector operations
   - Projection operators
   - Analysis/Synthesis mappings
   - M2 tensor compositions

---

## 📚 Key References

### Theoretical Foundations
- **Ashby** (1956): *Introduction to Cybernetics* - Variety, regulation
- **Prigogine** (1977): *Self-Organization* - Dissipative structures (high F)
- **Beer** (1972): *Brain of the Firm* - VSM
- **Dirac** (1930): *Quantum Mechanics* - Bra-ket notation

### Philosophical Grounding
- **Heraclitus**: Πάντα ῥεῖ (Everything flows) → F > 0 universal
- **Whitehead** (1929): *Process and Reality* - Process ontology
- **Wittgenstein** (1953): Limits of language = limits of world

---

## 🔄 Session Resumption Protocol

**To resume work**, provide Claude with:
1. This smart prompt
2. Latest ontology files (M3, M2 if created)
3. Specific task: "Continue M2 tensor ontology development" or similar

**Key context to maintain**:
- ASFID order is fixed
- M3 is vectorial (ℂ⁵), M2 is tensorial (⨁(H_M3)^⊗k)
- Universal openness F ≥ 0.1 is non-negotiable
- Time is parameter, Memory/Regulation are M2

---

## 📊 Current Token Usage

**Last session**: ~130K / 190K tokens (68%)  
**Recommendation**: Start fresh if approaching 85%+

---

**END OF SMART PROMPT**