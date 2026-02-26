# M2 Scope GenericConcept - Proposal Documentation

**Version:** 14.3.3  
**Date:** 2026-02-03  
**Author:** Echopraxium with the collaboration of Claude AI  
**Status:** ✅ VALIDATED - Ready for integration

---

## 📋 Executive Summary

**Scope** is proposed as the 69th GenericConcept in M2_GenericConcepts.jsonld. It fills a critical semantic gap between **Constraint** (prohibition) and **Domain** (entire field) by representing **positive boundaries of validity and authority**.

**Key Discovery:** Scope is essential for properly modeling **Autonomy** in VSM as `GenericConceptCombo(Agent, Scope)`.

---

## 🎯 GenericConcept Definition

### Basic Properties

| Property | Value |
|----------|-------|
| **@id** | m2:Scope |
| **Label** | Scope |
| **Category** | m2:Regulatory |
| **Perspective** | Map |
| **Polarity** | Neutral |
| **Epistemic Gap** | 0.35 |

### Tensor Formula

**Primary (ASFID basis):**
```
Scope = S⊗I⊗A⊗R
```

**Components:**
- **S (Structure)**: Delimits a structural space
- **I (Information)**: Contains information about what is in/out of scope
- **A (Attractor)**: Defines a stable zone of applicability
- **R (Representability)**: Map dimension - scope is always a conceptual construction

**Dimensionality:** 4D

**LaTeX notation:**
```latex
S \otimes I \otimes A \otimes R
```

**ASCII notation:**
```
S (x) I (x) A (x) R
```

### REVOI Characterization

**Primary formula (Sphinx Eye):**
```
R⊗V⊗O
```
- **R (Representability)**: Can the scope be symbolically defined?
- **V (Verifiability)**: Can we verify if something is in/out of scope?
- **O (Observability)**: Can we observe the scope boundaries?

**Fallback formula (Eagle Eye):**
```
S⊗I⊗A
```

---

## 🔬 Transdisciplinary Validation

**Validated across 10 domains:**

1. **Programming**: Variable scope (lexical, global, block scope)
2. **Cybernetics**: VSM S1 operational authority scope (Beer 1979)
3. **Management**: Span of control, delegation scope
4. **Juridical**: Jurisdiction boundaries, territorial scope
5. **Project Management**: Project scope definition (scope triangle)
6. **Biology**: Animal territory (defended area)
7. **Optics**: Depth of field (zone of acceptable sharpness)
8. **Mathematics**: Domain of function (ensemble de définition)
9. **Linguistics**: Scope of quantifier in formal logic
10. **Networks**: Broadcast domain, routing scope

**Transdisciplinary Strength:** ✅ Strong (≥8 domains validated)

---

## 🆚 Semantic Distinctions

### Scope vs Constraint

| Aspect | Constraint | Scope |
|--------|-----------|-------|
| **Polarity** | Negative | Positive |
| **Meaning** | What is PROHIBITED | What is PERMITTED |
| **Nature** | Hard limit, restriction | Domain of validity, playground |
| **Example (VSM)** | "S1 cannot hire without S3 approval" | "S1 can decide on budgets < 10k€" |
| **Metaphor** | "You cannot leave the garden" | "The garden is your playground" |

### Scope vs Domain

| Aspect | Domain | Scope |
|--------|--------|-------|
| **Scale** | Entire knowledge field | Limited region within field |
| **Formula** | Full ASFID⊗REVOI hybrid (5D after SVD) | S⊗I⊗A⊗R (4D) |
| **Example** | "Chemistry as a discipline" | "Valid pH range for this reaction" |

### Scope vs Boundary

| Aspect | Boundary | Scope |
|--------|----------|-------|
| **Nature** | Geometric/topological surface | Domain of applicability |
| **Type** | Spatial separator | Authority/validity region |
| **Example** | "Cell membrane" | "Enzyme active site specificity" |

### Scope vs Capacity

| Aspect | Capacity | Scope |
|--------|----------|-------|
| **Meaning** | Maximum structural limit | Extent of valid operation |
| **Metaphor** | Ceiling (upper bound) | Floor plan (operational area) |
| **Example** | "Max bandwidth: 100 Mbps" | "Network segment range: 192.168.1.0/24" |

---

## 💡 Discovery Context

**Origin:** Identified during VSM (Viable System Model) M0 modeling refinement.

**Problem:** How to properly model **Autonomy** in VSM?

Beer's definition of Autonomy:
> "Maximum local freedom; minimum central constraint"

This requires:
- **Agent** (S⊗I⊗D): Capability to act
- **Scope** (S⊗I⊗A⊗R): Bounded domain where action is authorized

**Solution:** `Autonomy = GenericConceptCombo(Agent, Scope)`

**Semantic Gap Filled:** 
- Constraint existed (what you CANNOT do)
- Domain existed (entire knowledge field)
- **Missing:** What you CAN do within defined boundaries → **Scope**

---

## 🧮 Mathematical Properties

### Coupling Analysis (for GenericConceptCombo)

When used in `Agent ⊗ Scope ⇒ Autonomy`:

```
Agent:  S⊗I⊗D           (3D)
Scope:  S⊗I⊗A⊗R         (4D)
Shared: {S, I}          → 2 shared dimensions

Emergent space dimension: ≤ 3 + 4 - 2 = 5D
```

**Shared dimension semantics:**
- **S (Structure)**: Agent's structure aligns with scope's structure
- **I (Information)**: Agent's capabilities align with scope's boundaries

**Coupling strength:** Medium-strong (2 shared dims out of 3-4)

### Dimensionality Justification

**Why 4D?**
- Not minimal (1D-2D) → Scope has internal structure
- Not maximal (5D) → Simpler than full domain concepts
- Balanced complexity for regulatory concept
- Distinct from related concepts:
  - Constraint: 2D (S⊗I)
  - Domain: 5D (ASFID⊗REVOI reduced)
  - Boundary: 2D-3D typically

---

## 📊 Integration Impact

### Metadata Updates

**M2_GenericConcepts.jsonld v14.3.3:**
- Total GenericConcepts: **68 → 69**
- Map GenericConcepts: **9 → 10**
- Neutral polarity: **50 → 51**
- Version: **14.3.2 → 14.3.3**

### Changelog Entry (v14.3.3)

```
NEW: Scope GenericConcept (S⊗I⊗A⊗R) - map perspective, 10 transdisciplinary domains
DISCOVERY: Scope required for VSM Autonomy modeling (GenericConceptCombo of Agent⊗Scope)
DISTINCTION: Scope (positive boundary - what is permitted) vs Constraint (negative boundary - what is prohibited)
CATEGORY: Scope in Regulatory (domain of validity and authority)
VALIDATION: Scope validated across programming, cybernetics, management, law, biology, optics, mathematics, linguistics, networks
TOTAL: 69 GenericConcepts (10 Map GenericConcepts including Scope)
```

---

## 🔗 VSM Integration

### Autonomy Modeling

**Before (problematic):**
```
Autonomy → instantiates [Modularity, Agent]
```
- Semantic gap: Missing the "bounded domain" concept
- Modularity alone doesn't capture authority limits

**After (with Scope):**
```
Autonomy = GenericConceptCombo(Agent, Scope)
```
- ✅ Complete semantic coverage
- ✅ Agent provides action capability
- ✅ Scope provides authority boundaries
- ✅ Emergence: "bounded autonomy" exactly as Beer defined

### Complete VSM GenericConceptCombo Mappings

| VSM Concept | GenericConceptCombo | Shared Dims | Status |
|-------------|------------------|-------------|--------|
| VarietyAmplification | ValueSpace ⊗ Amplification↑ | {It,R,O} = 3 | ✅ Canonical |
| VarietyAttenuation | ValueSpace ⊗ Amplification↓ | {It,R,O} = 3 | ✅ Canonical |
| Cohesion | Identity ⊗ Constraint | {S,I,V} = 3 | ✅ Validated |
| AlgedonicSignal | Trigger ⊗ Signal | {I} = 1 | ✅ Validated |
| ResourceBargain | Trade-off ⊗ Feedback | {A,F} = 2 | ✅ Validated |
| **Autonomy** | **Agent ⊗ Scope** | **{S,I} = 2** | ✅ **NEW** |

---

## 🎓 Examples Across Domains

### 1. Programming (Variable Scope)
```javascript
function outer() {
  let x = 10;  // Scope: function 'outer'
  
  function inner() {
    let y = 20;  // Scope: function 'inner'
    console.log(x);  // x is IN SCOPE (accessible)
  }
  
  console.log(y);  // y is OUT OF SCOPE (error)
}
```
**Scope formula application:**
- S: Code block structure
- I: Variable identifier information
- A: Stable region where identifier resolves
- R: Lexical scope rules (representable in language spec)

### 2. VSM S1 Operational Scope
```
System 1 Manager has scope:
- Budget authority: < 10,000€
- Hiring authority: temporary staff only
- Geographical scope: regional operations
- Temporal scope: day-to-day decisions
```
**Scope formula application:**
- S: Organizational structure boundary
- I: Authority delegation information
- A: Stable zone of decision-making power
- R: Explicitly defined in delegation policy

### 3. Biology (Territorial Scope)
```
Wolf pack territory:
- Spatial scope: 200 km² defended area
- Resource scope: hunting grounds, water sources
- Social scope: pack members only
- Temporal scope: seasonal adjustments
```
**Scope formula application:**
- S: Geographical boundary structure
- I: Territory markers (scent, boundaries)
- A: Stable defended region
- R: Observable territory demarcation

### 4. Optics (Depth of Field)
```
Camera DoF:
- In-scope: Sharp focus region
- Out-of-scope: Blur regions (bokeh)
- Scope determined by: aperture, focal length, distance
```
**Scope formula application:**
- S: 3D spatial volume structure
- I: Sharpness information distribution
- A: Stable acceptable sharpness zone
- R: Geometrically calculable from lens formula

---

## ✅ Validation Checklist

- [x] **Transdisciplinary:** ≥8 validated domains (10 achieved)
- [x] **Distinct:** Semantically different from existing GenericConcepts
- [x] **Necessary:** Fills real semantic gap (Autonomy modeling)
- [x] **Tensor formula:** Coherent 4D structure (S⊗I⊗A⊗R)
- [x] **REVOI characterization:** Defined (R⊗V⊗O primary)
- [x] **Examples:** Concrete instances across domains
- [x] **Distinctions:** Clear vs Constraint, Domain, Boundary, Capacity
- [x] **Integration:** Properly updates M2 metadata
- [x] **Documentation:** Complete specification

---

## 📚 References

### Primary Sources
- Beer, S. (1979). *The Heart of Enterprise*. Wiley. (Chapter on S1 autonomy)
- Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press. (Variable scope)
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. (Variety and control)

### TSCG Internal
- M2_GenericConcepts.jsonld v14.3.3
- M0_VSM.jsonld (Viable System Model instantiation)
- TSCG_Smart_Prompt_v14_3_0.md (Framework overview)

---

## 🚀 Next Steps

1. **Update M0_VSM.jsonld** to use new Scope-based Autonomy mapping
2. **Update M2_FormulasReference.json** to include Scope formula
3. **Validate** Scope in additional poclets (e.g., M0_TRIZ, M0_TPACK)
4. **Document** Scope usage patterns in M1 domain extensions

---

**Status:** ✅ APPROVED for integration into M2_GenericConcepts.jsonld v14.3.3

---

**End of Proposal**
