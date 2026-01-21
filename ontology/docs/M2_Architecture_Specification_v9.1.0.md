# M2 Architecture Specification v9.1.0

**Version**: 9.1.0  
**Date**: 2026-01-20  
**Previous**: v9.0.0 (2026-01-17)  
**Status**: Bicephalous architecture with ORIVE validation period  
**Framework**: TSCG (Transdisciplinary System Construction Game)

---

## Executive Summary

**M2 v9.1.0** introduces a fundamental architectural change: **metaconcepts are now categorized by their Map-Territory nature** and receive formulas accordingly:

1. **Territory-only metaconcepts**: ASFID formula (stable ✅)
2. **Map-only metaconcepts**: ORIVE formula (proposition 🧪) + fallback ASFID
3. **Dual metaconcepts**: ASFID formula (stable ✅) + ORIVE formula (proposition 🧪) + fallback ASFID

This reflects TSCG's bicephalous philosophy: Eagle Eye (ASFID - Territory) and Sphinx Eye (ORIVE - Map) measure/construct systems from complementary perspectives.

**Key changes**:
- Total metaconcepts: 53 → 55 (+2)
- New metaconcepts: **Balance** (Territory), **Trade-off** (not added - see rationale)
- ORIVE proposals: 6 Dual metaconcepts now have ORIVE formulas (with fallback)
- Architecture: Territory/Map/Dual trichotomy introduced

---

## Table of Contents

1. [Architectural Philosophy](#1-architectural-philosophy)
2. [Three Types of Metaconcepts](#2-three-types-of-metaconcepts)
3. [ORIVE Validation Strategy](#3-orive-validation-strategy)
4. [New Metaconcept: Balance](#4-new-metaconcept-balance)
5. [Rejected: Trade-off](#5-rejected-trade-off)
6. [Dual Metaconcepts ORIVE Proposals](#6-dual-metaconcepts-orive-proposals)
7. [M2 Complete Inventory](#7-m2-complete-inventory)
8. [Changelog v9.0.0 → v9.1.0](#8-changelog)

---

## 1. Architectural Philosophy

### 1.1 Bicephalous Foundation

**Eagle Eye** (🦅 M3_Eagle_Eye.jsonld):
- Measures **Territory** (observed phenomena)
- Basis: **ASFID** {|A⟩, |S⟩, |F⟩, |I⟩, |D⟩} in ℂ⁵
- Perspective: Mathematical (quantification, formalization)
- Status: **IMMUTABLE** ✅ (validated 2026-01-14)

**Sphinx Eye** (🗿 M3_Sphinx_Eye.jsonld):
- Constructs **Map** (models, representations)
- Basis: **ORIVE** {|O⟩, |R⟩, |I⟩, |V⟩, |E⟩} in ℂ⁵
- Perspective: Philosophical (interpretation, meaning)
- Status: **PROPOSITION** ⏳ (validated on 6 poclets, target: 15+)

### 1.2 Map ≠ Territory (Korzybski 1933)

**Principle**: The Map is NOT the Territory.

**Implications for M2**:
- Some metaconcepts exist primarily in **Territory** (physical laws, structural realities)
- Some metaconcepts exist primarily in **Map** (epistemic concepts, modeling constraints)
- Some metaconcepts are **Dual** (bidirectional processes, manifesting in both)

**Example**:
- **Balance** (Territory): Physical law P₁ × P₂ = constant (Boyle's Law)
- **Representation** (Map): How we encode/model systems (color spaces)
- **Coding** (Dual): Encoding (Territory→Map) + Decoding (Map→Territory)

### 1.3 Why This Architecture?

**Problem solved**: Until v9.0.0, all 53 metaconcepts used only ASFID formulas. This was incomplete because:
1. ASFID measures Territory excellently but doesn't capture Map quality
2. Some metaconcepts (like Representation, Code, Signature) are fundamentally about **Maps**
3. Dual metaconcepts (like Coding) have two faces: Territory process + Map representation

**Solution**: Assign formulas based on **metaconcept nature**:
- If primarily Territory phenomenon → ASFID (stable)
- If primarily Map concept → ORIVE (proposition) + fallback ASFID
- If Dual (bidirectional) → Both ASFID + ORIVE (+ fallback)

---

## 2. Three Types of Metaconcepts

### 2.1 Territory-only Metaconcepts

**Definition**: Metaconcepts that describe **physical/systemic phenomena** in the Territory, observable regardless of observer/model.

**Formula**: ASFID tensor (Eagle Eye) - **STABLE** ✅

**Examples**:
- **Balance** (A⊗I): Physical law of inverse coupling (Boyle's Law: P × V = constant)
- **Homeostasis** (A⊗S⊗F): Self-regulating equilibrium (thermostat, body temperature)
- **Dissipation** (F⊗D): Energy dispersion (heat loss, entropy increase)
- **Flow** (F): Material/energy/information exchange with environment

**Characteristics**:
- Exist objectively in Territory
- Measurable with ASFID dimensions
- Independent of observer or model quality
- Status: **STABLE** (ASFID validated)

**No ORIVE formula**: Not needed - these are Territory phenomena, not Map constructions.

### 2.2 Map-only Metaconcepts

**Definition**: Metaconcepts that describe **epistemic/representational concepts** primarily relevant to how we construct Maps.

**Formula**:
- Primary: ORIVE tensor (Sphinx Eye) - **PROPOSITION** 🧪
- Fallback: ASFID tensor (for safety during validation period)

**Examples** (to be identified from current 53):
- **Representation** (I⊗S): How systems are encoded/modeled
- **Language** (S⊗I⊗F): Symbolic communication systems
- **Code** (I⊗S): Information encoding schemes
- **Signature** (I): Identifying pattern unique to system
- Potentially others TBD

**Characteristics**:
- Primarily about Maps, models, representations
- ORIVE captures Map quality better than ASFID
- Still have fallback ASFID (during ORIVE validation)
- Status: **PROPOSITION** (ORIVE being validated via poclets)

**Validation**: If ORIVE fails empirical testing (success rate <60%), revert to ASFID-only or revise ORIVE formula.

### 2.3 Dual Metaconcepts

**Definition**: Metaconcepts with **bidirectional nature** - they manifest in both Territory AND Map with different aspects.

**Formula**:
- Territory aspect: ASFID tensor - **STABLE** ✅
- Map aspect: ORIVE tensor - **PROPOSITION** 🧪 + fallback ASFID

**Current 6 Dual metaconcepts**:
1. **Coding** (Encoding/Decoding)
2. **Synergy** (Synergy/Antagonism)
3. **Fusion** (Fusion/Fission)
4. **Activation** (Activation/Deactivation)
5. **Convergence** (Convergence/Divergence)
6. **Composition** (Composition/Decomposition)

**Example - Coding**:

**Territory aspect (Encoding/Decoding)**:
```json
{
  "ASFID_formula": "I⊗S⊗D",
  "status": "STABLE ✅",
  "nature": "Physical transformation process (DNA→RNA, plaintext→ciphertext)"
}
```

**Map aspect (How encoding appears in models)**:
```json
{
  "ORIVE_formula": "R⊗I⊗E",
  "fallback_ASFID": "I⊗S⊗D",
  "status": "PROPOSITION 🧪",
  "nature": "Representational mapping in models (UTF-8, compression algorithms)"
}
```

**Characteristics**:
- Two perspectives on same phenomenon
- Territory formula stable (ASFID)
- Map formula in validation (ORIVE + fallback)
- Dual polarity reflects bidirectionality

---

## 3. ORIVE Validation Strategy

### 3.1 Current Status

**ORIVE validated on 6 poclets** (2026-01-17):
1. Fire Triangle (ORIVE: 0.85)
2. RGB (ORIVE: 0.92)
3. HSL (ORIVE: 0.89)
4. CMY (ORIVE: 0.74)
5. CMYK (ORIVE: 0.89)
6. ColorSynthesis (federated)

**Success**: ORIVE successfully distinguishes Map quality, correlates with real-world success.

**Target**: 15+ poclets for statistical validation.

### 3.2 Validation Phases

**Phase 1 (Current)**: ORIVE proposals
- ✅ ORIVE formulas proposed for:
  - 6 Dual metaconcepts (see §6)
  - Map-only metaconcepts (TBD - need classification of existing 53)
- ✅ Fallback ASFID mandatory for all ORIVE formulas

**Phase 2 (Next 3-6 months)**: Poclet expansion
- Test ORIVE on 9+ additional poclets:
  - Economics (Supply-Demand Triangle)
  - Biology (Predator-Prey, Lotka-Volterra)
  - Mechanics (Pendulum, Spring-Mass-Damper)
  - Social systems (Opinion dynamics)
- Target: 15+ total poclets

**Phase 3 (6-12 months)**: Refinement decision
- **If ORIVE success rate >80%**: Remove fallback, mark STABLE ✅
- **If 60-80%**: Refine ORIVE dimensions, keep fallback
- **If <60%**: Revert to ASFID-only OR abandon ORIVE

**Phase 4 (Mature)**: Full bicephalous M2
- All relevant metaconcepts have validated ASFID + ORIVE
- Eagle and Sphinx fully operational
- Framework demonstrates true bicephalous architecture

### 3.3 Success Criteria

**ORIVE formula is successful if**:
1. **Distinguishes Map quality**: ORIVE scores correlate with real-world utility
2. **Orthogonality**: ORIVE dimensions are independent (⟨O|R⟩ ≈ 0, etc.)
3. **Predictive**: High ORIVE → successful Maps; Low ORIVE → failed Maps
4. **Evolvable**: ORIVE captures how Maps improve over time
5. **Falsifiable**: Bad Maps get low ORIVE (Popperian verifiability)

**Example validation**: CMY (ORIVE: 0.74) failed practically → CMYK (ORIVE: 0.89) succeeded.

---

## 4. New Metaconcept: Balance

### 4.1 Specification

```json
{
  "@id": "m2:Balance",
  "@type": "m2:TerritoryMetaconcept",
  "rdfs:label": "Balance",
  "rdfs:comment": "State of mutual compensation between parameters where increasing one requires decreasing another to maintain system invariant. Physical law observable in Territory.",
  "m2:hasCategory": "m2:Regulatory",
  "m2:hasTensorFormula": "A⊗I",
  "m2:formulaSpace": "ASFID (Eagle Eye - Territory)",
  "m2:hasDominantM3": ["m3eagle:Attractor", "m3eagle:Information"],
  "m2:hasEpistemicGap": 0.15,
  "m2:hasPolarity": "neutral",
  "m2:status": "STABLE ✅",
  "m2:discoveredFrom": {
    "poclet": "M0_ExposureTriangle_Photography.jsonld",
    "pattern": "Compensatory Triplet (A × S × ISO = constant)",
    "date": "2026-01-20"
  }
}
```

### 4.2 Mathematical Formulation

**Basic formula**: `P₁ × P₂ = Constant`

**Generalized**: `∏ᵢ Pᵢ = C` (product of parameters = invariant)

**Derivative form**: `dP₁/dt × P₂ + P₁ × dP₂/dt = 0`

**Implication**: If ΔP₁ > 0 then ΔP₂ < 0 such that ΔP₁/P₁ = -ΔP₂/P₂

### 4.3 Examples (Transdisciplinary)

| Domain | Example | Formula | Constant |
|--------|---------|---------|----------|
| **Photography** | Exposure Triangle | ISO × Shutter = E/Aperture | Exposure |
| **Thermodynamics** | Boyle's Law | P × V = nRT | Temperature |
| **Optics** | Focal length | f × FoV ≈ constant | Sensor size |
| **Economics** | Revenue | Price × Quantity | Revenue (simplified) |
| **Mechanics** | Lever | Force × Distance | Work |
| **Quantum** | Uncertainty | Δx × Δp ≥ ℏ/2 | Planck constant |

### 4.4 Tensor Justification (A⊗I)

**Why A⊗I?**
- **A (Attractor)**: System maintains invariant C (equilibrium attractor)
- **I (Information)**: Parameters encode their reciprocal relationship

**Not F**: Flow not essential (Balance can exist in closed systems)  
**Not D**: Dynamics not required (static balances exist)  
**Not S**: Structure secondary (Balance is about relationship, not topology)

**Order 2 tensor**: Simple coupling, like Resilience (A⊗S), Dissipation (F⊗D)

### 4.5 Why Not "Reciprocity"?

**Problem**: "Reciprocity" has 34+ conflicting definitions across disciplines:
- Social reciprocity (Malinowski: "I scratch your back, you scratch mine")
- Direct reciprocity (biology: tit-for-tat)
- Physical reciprocity (physics: source/observer interchange)
- Economic reciprocity (Polanyi: mutual exchange)
- Mathematical reciprocity (our usage: inverse relationship)

**Source**: "What is reciprocity?" (2023) - survey of 85 cooperation experts shows NO CONSENSUS

**Solution**: Use **"Balance"** - unambiguous, precise, no interdisciplinary baggage.

---

## 5. Rejected: Trade-off

### 5.1 Why Trade-off Was Considered

**Pattern identified**: In Exposure Triangle poclet, photographers face impossible choices:
- Fast shutter (freeze motion) ⇔ Low ISO (low noise)
- Large aperture (shallow DoF) ⇔ Deep DoF (everything sharp)

**Initial proposal**: Trade-off as Map metaconcept (ORIVE: V⊗E⊗I)

### 5.2 Why Trade-off Was Rejected

**Insight from designer**: Trade-off is NOT the systematic complement of Balance.

**Reasoning**:
- **Balance exists in Territory**: Boyle's Law (P × V = constant) is physical reality
- **Trade-off is context-dependent**: A system with Balance doesn't automatically create a Trade-off for the observer
- **Counter-example**: Boyle's Law has Balance (P × V = constant) but NO Trade-off for scientist (can measure P and V independently). Trade-off only appears if trying to OPTIMIZE (e.g., compress gas for storage).

**Conclusion**: Trade-off is **situational** (depends on observer's goals), not **systematic** (universal property of balanced systems).

**Decision**: Do NOT add Trade-off to M2 at this time. May reconsider if:
1. Clear ASFID or ORIVE formula emerges
2. Transdisciplinary validation on 3+ poclets
3. Distinct from existing metaconcepts (Constraint, Regulation)

---

## 6. Dual Metaconcepts ORIVE Proposals

All 6 Dual metaconcepts now have **proposed ORIVE formulas** (Map aspect) in addition to **stable ASFID formulas** (Territory aspect).

**Full details**: See `M2_Dual_ORIVE_Proposals.md`

### Summary Table

| Dual Metaconcept | ASFID (Territory - STABLE ✅) | ORIVE (Map - PROPOSITION 🧪) | Fallback |
|------------------|------------------------------|------------------------------|----------|
| **Coding** (Encoding/Decoding) | I⊗S⊗D | R⊗I⊗E | I⊗S⊗D |
| **Synergy** (Synergy/Antagonism) | A⊗S⊗I | V⊗I⊗O | A⊗S⊗I |
| **Fusion** (Fusion/Fission) | S⊗F⊗D | O⊗R⊗E | S⊗F⊗D |
| **Activation** (Activation/Deactivation) | A⊗I⊗D | V⊗R⊗O | A⊗I⊗D |
| **Convergence** (Convergence/Divergence) | A⊗D | O⊗V⊗E | A⊗D |
| **Composition** (Composition/Decomposition) | S⊗I⊗A / S⊗I | R⊗I⊗V | S⊗I⊗A |

**Status**: All ORIVE formulas are PROPOSITIONS 🧪 requiring validation via poclets.

**Validation target**: 3 poclets per Dual metaconcept = 18 total poclet validations.

---

## 7. M2 Complete Inventory

### 7.1 By Category (9 categories)

| Category | Count | Examples |
|----------|-------|----------|
| **Structural** | 15 | Homeostasis, Network, Hierarchy, Symmetry, Modularity, Boundary, Interface, Component, Topology, Segmentation, Node, Path, Channel, Cluster, Hub |
| **Dynamic** | 8 | Catalysis, Bifurcation, Transformation, Process, Trajectory, Event, Behavior, Gradient |
| **Regulatory** | 9 | Regulation, Constraint, Threshold, Feedback, Filter, Gain, Protocol, Coherence, **Balance** |
| **Adaptive** | 5 | Resilience, Adaptation, Emergence, Memory, Learning |
| **Energetic** | 3 | Dissipation, Resource, Storage |
| **Informational** | 6 | Code, Signal, Language, Representation, Signature, Channel |
| **Ontological** | 3 | System, Environment, State |
| **Teleonomic** | 2 | Autopoiesis, Stability |
| **Relational** | 4 | Relation, Agent, Role, Link |

**Total**: 55 metaconcepts

### 7.2 By Polarity

| Polarity | Count | Examples |
|----------|-------|----------|
| **Neutral** | 49 | Homeostasis, Network, Component, Balance, Regulation, ... |
| **Dual** | 6 | Coding, Synergy, Fusion, Activation, Convergence, Composition |

### 7.3 By Type (Territory/Map/Dual)

**This classification is PARTIAL** - needs completion:

| Type | Count (current) | Examples | Formula |
|------|-----------------|----------|---------|
| **Territory-only** | ~40+ | Balance, Homeostasis, Dissipation, Flow, ... | ASFID ✅ |
| **Map-only** | ~5-10 (TBD) | Representation?, Code?, Language?, ... | ORIVE 🧪 + fallback ASFID |
| **Dual** | 6 | Coding, Synergy, Fusion, Activation, Convergence, Composition | ASFID ✅ + ORIVE 🧪 + fallback |

**TODO**: Complete classification of all 55 metaconcepts into Territory/Map/Dual.

---

## 8. Changelog v9.0.0 → v9.1.0

### 8.1 Added

1. **New metaconcept: Balance** (A⊗I, Regulatory, Territory-only)
   - Discovered from Exposure Triangle poclet
   - Captures inverse coupling P₁ × P₂ = constant
   - Transdisciplinary validation: Photography, Thermodynamics, Optics, Economics

2. **ORIVE formulas for 6 Dual metaconcepts**:
   - Coding: R⊗I⊗E (Map aspect)
   - Synergy: V⊗I⊗O (Map aspect)
   - Fusion: O⊗R⊗E (Map aspect)
   - Activation: V⊗R⊗O (Map aspect)
   - Convergence: O⊗V⊗E (Map aspect)
   - Composition: R⊗I⊗V (Map aspect)
   - All with fallback ASFID (proposition status)

3. **Architectural trichotomy**: Territory/Map/Dual classification introduced

### 8.2 Modified

1. **M2 architecture**: Now explicitly bicephalous
   - Territory metaconcepts: ASFID only
   - Map metaconcepts: ORIVE (+ fallback ASFID)
   - Dual metaconcepts: ASFID + ORIVE (+ fallback)

2. **Validation strategy**: ORIVE validation roadmap formalized (4 phases)

### 8.3 Rejected

1. **Trade-off metaconcept**: Not added (see §5 for rationale)
   - Not systematic complement of Balance
   - Context-dependent, not universal
   - May reconsider with stronger evidence

### 8.4 Pending

1. **Territory/Map/Dual classification**: Needs completion for all 55 metaconcepts
2. **Map-only metaconcept identification**: Likely candidates include Representation, Code, Language, Signature
3. **ORIVE validation**: Expand from 6 to 15+ poclets (Phase 2)

---

## 9. Next Steps

### 9.1 Immediate (This week)

1. ✅ Document M2 v9.1.0 architecture (this file)
2. ✅ Create ORIVE proposals for 6 Dual metaconcepts
3. ✅ Add Balance to M2 ontology JSON-LD
4. ⏳ Update M2_MetaConcepts_Ontology.jsonld with v9.1.0 changes

### 9.2 Short-term (Next month)

1. Complete Territory/Map/Dual classification for all 55 metaconcepts
2. Identify Map-only metaconcepts and propose ORIVE formulas
3. Create 3-5 new poclets for ORIVE validation:
   - Supply-Demand Triangle (economics)
   - Predator-Prey (biology)
   - Pendulum (mechanics)

### 9.3 Medium-term (3-6 months)

1. Expand poclet library to 15+ for statistical ORIVE validation
2. Test ORIVE formulas for Dual metaconcepts (18 poclet validations)
3. Decide: Stabilize ORIVE ✅ or Refine 🔧 or Revert ❌

### 9.4 Long-term (6-12 months)

1. Achieve full bicephalous M2 with validated ASFID + ORIVE
2. Remove fallback ASFID if ORIVE success rate >80%
3. Publish M2 v10.0.0 (Stable bicephalous architecture)

---

## Appendices

### A. Glossary

**ASFID**: Attractor, Structure, Flow, Information, Dynamics - 5D basis for Eagle Eye (Territory measurement)

**ORIVE**: Observability, Representability, Interoperability, Verifiability, Evolvability - 5D basis for Sphinx Eye (Map construction)

**Bicephalous**: Two-headed architecture (Eagle + Sphinx)

**Territory**: Observed phenomena (physical reality, "the thing itself")

**Map**: Constructed models/representations ("our understanding of the thing")

**Poclet**: Minimal yet complete system representation (Proof-of-Concept + -let suffix)

**Fallback ASFID**: Safety mechanism - if ORIVE fails validation, revert to ASFID formula

### B. References

- Smart Prompt v10.0.0 (2026-01-17)
- M3_Eagle_Eye.jsonld v2.0.0
- M3_Sphinx_Eye.jsonld v2.0.0
- M2_MetaConcepts_Ontology.jsonld v9.0.0
- M0_ExposureTriangle_Photography.jsonld v1.0.0
- Korzybski, A. (1933). "Science and Sanity" - Map is not Territory
- Popper, K. (1959). "The Logic of Scientific Discovery" - Falsifiability principle

---

**END OF SPECIFICATION**

**Version**: 9.1.0  
**Status**: Ready for implementation  
**Next milestone**: Complete Territory/Map/Dual classification (all 55 metaconcepts)
