# 🎯 New Category: m3:SystemicFramework

**Date:** January 27, 2026  
**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** M3_GenesisSpace v2.4.0  
**Total Categories:** 7 → 8

---

## 📋 Category Definition

### m3:SystemicFramework

**Preferred Label:** Systemic Framework  
**Alternative Labels:**
- External Framework Mapping
- Framework Integration
- Theoretical Framework Bridge

**Definition:**  
Ontologies that map established systemic/theoretical frameworks (TRIZ, VSD, TPACK, etc.) into TSCG formalism. These provide bridges between TSCG and existing methodologies, enabling cross-framework analysis and integration.

**Scope Note:**  
Open-ended set. Any established framework with systemic structure can be mapped. Typically 10-20 major frameworks. Distinct from DomainExtension (which are disciplinary) and from Poclet (which are minimal instances).

---

## 🎯 Purpose and Rationale

### Why SystemicFramework?

**1. Validate TSCG Expressiveness**
- Demonstrate that TSCG can represent established frameworks
- Prove framework's generality and completeness

**2. Enable Cross-Framework Analysis**
- Compare TRIZ and Design Thinking within unified formalism
- Identify commonalities and differences
- Find synergies between frameworks

**3. Leverage Existing Knowledge**
- Practitioners familiar with TRIZ can use it within TSCG
- No need to abandon proven methodologies
- Bridge between traditional and TSCG approaches

**4. Facilitate Adoption**
- Lower barrier to entry for TSCG
- "You can still use TRIZ, but with more rigor"
- Gradual migration path

---

## 📊 Hierarchy and Relationships

```
m3:TransdisciplinaryPattern (M2 - Universal patterns)
  │
  ├─── m3:DomainExtension (M1 - Disciplinary knowledge)
  │    └─ Examples: Biology, Chemistry, Optics
  │
  └─── m3:SystemicFramework ⭐ (M1 - Methodological frameworks)
       └─ Examples: TRIZ, VSD, TPACK, Design Thinking
```

**Relationship:**
- `skos:broader` → m3:TransdisciplinaryPattern
- `skos:related` → m3:DomainExtension, m3:Poclet
- `m3:layerOrder` → 3 (same as M1 DomainExtension)

---

## 🔍 Distinction from Other Categories

### SystemicFramework vs DomainExtension

| Aspect | DomainExtension | SystemicFramework |
|--------|-----------------|-------------------|
| **Nature** | Disciplinary knowledge | Methodological framework |
| **Examples** | Biology, Chemistry, Physics | TRIZ, VSD, Design Thinking |
| **Focus** | Domain concepts | Problem-solving methods |
| **Structure** | Ontology of entities | Process/workflow formalization |
| **Origin** | Scientific disciplines | Systems theory, design, innovation |

**Example:**
- `M1_Chemistry.jsonld` → DomainExtension (domain)
- `M1_TRIZ.jsonld` → SystemicFramework (methodology)

---

### SystemicFramework vs Poclet

| Aspect | Poclet | SystemicFramework |
|--------|--------|-------------------|
| **Scope** | Minimal instance | Complete framework |
| **Size** | Small, focused | Large, comprehensive |
| **Purpose** | Validation | Integration |
| **Completeness** | Deliberately minimal | Full theoretical foundation |
| **Examples** | Fire Triangle | TRIZ (40 principles + contradictions matrix) |

**Example:**
- `M0_FireTriangle.jsonld` → Poclet (minimal)
- `M1_TRIZ.jsonld` → SystemicFramework (complete methodology)

---

## 📚 Examples of SystemicFrameworks

### 1. TRIZ (Theory of Inventive Problem Solving)

**File:** `M1_TRIZ.jsonld`  
**Origin:** Genrich Altshuller (1946-1998)  
**Components:**
- 40 Inventive Principles
- Contradictions Matrix
- Substance-Field Analysis
- ARIZ algorithm

**TSCG Mapping:**
- Principles → M2 metaconcepts (Modularity, Segmentation, etc.)
- Contradictions → Tensor conflicts (A⊗S vs F⊗D)
- Evolution patterns → Dynamics transformations

---

### 2. VSD (Value-Sensitive Design)

**File:** `M1_VSD.jsonld`  
**Origin:** Batya Friedman (1996-)  
**Components:**
- Conceptual investigations
- Empirical investigations
- Technical investigations
- Stakeholder analysis

**TSCG Mapping:**
- Values → Information dimensions
- Stakeholders → Agent networks
- Trade-offs → Constraint metaconcepts

---

### 3. TPACK (Technological Pedagogical Content Knowledge)

**File:** `M1_TPACK.jsonld` (already exists as poclet)  
**Origin:** Mishra & Koehler (2006)  
**Components:**
- Technology Knowledge (TK)
- Pedagogy Knowledge (PK)
- Content Knowledge (CK)
- 4 intersections (TPK, TCK, PCK, TPACK)

**TSCG Mapping:**
- TK, PK, CK → ASFID dimensions
- Intersections → Tensor products
- TPACK center → Full tensor space

**Status:** Currently M0 Poclet, could be expanded to full SystemicFramework

---

### 4. Design Thinking

**File:** `M1_DesignThinking.jsonld`  
**Origin:** IDEO, d.school Stanford (1990s-)  
**Components:**
- Empathize
- Define
- Ideate
- Prototype
- Test

**TSCG Mapping:**
- 5 phases → Sequential Steps (Process)
- Iteration loops → Cycles
- User insights → Information ⊗ Observability

---

### 5. Systems Thinking

**File:** `M1_SystemsThinking.jsonld`  
**Origin:** Ludwig von Bertalanffy, Peter Senge  
**Components:**
- Feedback loops
- Stocks and flows
- Leverage points
- Mental models
- System archetypes

**TSCG Mapping:**
- Feedback loops → Homeostasis, Regulation
- Stocks/flows → Storage, Flow
- Archetypes → M2 metaconcept patterns

---

## 🛠️ Integration Guidelines

### Step 1: Identify Framework Components

List all core concepts, processes, and relationships.

**Example (TRIZ):**
- Concepts: Contradiction, Ideality, Resources
- Processes: Problem formulation → Solution search → Evaluation
- Relationships: Technical contradictions vs Physical contradictions

---

### Step 2: Map to M2 Metaconcepts

Identify which M2 metaconcepts correspond to framework elements.

**Example (TRIZ):**
```
TRIZ Principle 1 (Segmentation) → m2:Modularity
TRIZ Principle 2 (Taking out) → m2:Decomposition
TRIZ Principle 35 (Parameter changes) → m2:Transformation
Technical Contradiction → m2:Constraint ⊗ m2:Trade-off
```

---

### Step 3: Express as Tensor Formulas

Formalize framework operations using ASFID/ORIVE dimensions.

**Example (TRIZ Ideality):**
```
Ideality = (Useful Functions) / (Cost + Harm)
         ≈ (F⊗I) / (S⊗A)  [in TSCG]
         
High Ideality → Maximize Flow ⊗ Information
              → Minimize Structure ⊗ Attractors
```

---

### Step 4: Validate with Framework Experts

Ensure mapping preserves framework's intent and utility.

**Validation criteria:**
- Does TSCG representation capture framework essence?
- Can practitioners recognize their familiar framework?
- Are key insights preserved or enhanced?

---

### Step 5: Document Epistemic Gaps

Acknowledge what TSCG adds or cannot represent.

**Example (TRIZ):**
```json
{
  "epistemic_alignment": 0.85,
  "tscg_adds": [
    "Rigorous mathematical formalism",
    "Bicephalous Territory-Map distinction",
    "Quantitative ORIVE scoring"
  ],
  "tscg_loses": [
    "TRIZ's historical evolution narratives",
    "Some domain-specific heuristics"
  ]
}
```

---

## 📊 Expected Frameworks (5-20)

### High Priority (Core Systemic Frameworks)

1. ✅ **TPACK** (already exists as M0, upgrade to M1)
2. **TRIZ** - Inventive problem solving
3. **VSD** - Value-sensitive design
4. **Design Thinking** - IDEO methodology
5. **Systems Thinking** - General systems theory

### Medium Priority (Specialized Frameworks)

6. **Cynefin** - Decision framework (simple/complicated/complex/chaotic)
7. **Theory U** - Social change (Otto Scharmer)
8. **Lean Startup** - Innovation methodology
9. **Agile/Scrum** - Software development framework
10. **Six Sigma** - Quality management

### Lower Priority (Domain-Specific)

11. **TOGAF** - Enterprise architecture
12. **ITIL** - IT service management
13. **PMBOK** - Project management
14. **Balanced Scorecard** - Strategy execution
15. **Blue Ocean Strategy** - Business strategy

---

## 🎯 Use Cases

### Use Case 1: Cross-Framework Comparison

**Question:** "How do TRIZ and Design Thinking differ in handling contradictions?"

**TSCG Analysis:**
```sparql
# Find contradiction-handling metaconcepts in both frameworks
SELECT ?framework ?metaconcept
WHERE {
  ?framework m3:ontologyCategory m3:SystemicFramework ;
             :uses ?metaconcept .
  ?metaconcept rdfs:subClassOf m2:Constraint .
}
```

**Result:** Direct comparison of approaches within unified formalism.

---

### Use Case 2: Framework Synergy

**Question:** "Can we combine TRIZ's technical principles with Design Thinking's empathy?"

**TSCG Integration:**
```
TRIZ Principles (S⊗I focused) 
  + 
Design Thinking Empathy (I⊗O focused)
  =
Hybrid methodology with both technical rigor and user insight
```

---

### Use Case 3: Practitioner Onboarding

**Scenario:** Expert in TRIZ wants to learn TSCG.

**Path:**
1. Start with `M1_TRIZ.jsonld` (familiar territory)
2. See how TRIZ maps to M2 metaconcepts
3. Understand ASFID/ORIVE through TRIZ lens
4. Gradually expand to full TSCG framework

---

## 🔗 SPARQL Query Examples

### List All Systemic Frameworks

```sparql
PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?framework ?title
WHERE {
  ?framework a owl:Ontology ;
             m3:ontologyCategory m3:SystemicFramework ;
             dcterms:title ?title .
}
```

---

### Find Frameworks Using Specific Metaconcept

```sparql
# Find all frameworks that use m2:Modularity
SELECT ?framework
WHERE {
  ?framework m3:ontologyCategory m3:SystemicFramework ;
             :containsMetaconcept m2:Modularity .
}
```

---

## 📝 Template: M1_[Framework].jsonld

```json
{
  "@context": { ... },
  "@id": "m1:framework:[FrameworkName]",
  "@type": "owl:Ontology",
  "m3:ontologyCategory": {"@id": "m3:SystemicFramework"},
  
  "dcterms:title": "[Framework Full Name]",
  "dcterms:creator": "[Original Author(s)]",
  "dcterms:created": "[Original Year]",
  
  "framework_metadata": {
    "origin": "Description of framework's history",
    "purpose": "What problem does it solve?",
    "core_components": [...],
    "key_principles": [...]
  },
  
  "tscg_mapping": {
    "m2_metaconcepts_used": [...],
    "tensor_formulas": {...},
    "epistemic_alignment": 0.85
  },
  
  "validation": {
    "expert_review": "Validated by [Expert Name]",
    "case_studies": [...]
  }
}
```

---

## ✅ Benefits of SystemicFramework Category

### 1. TSCG Validation
- Demonstrates expressiveness by representing established frameworks
- Shows TSCG can handle complex methodologies

### 2. Practitioner Value
- Familiar entry point into TSCG
- Leverage existing expertise
- No need to abandon proven methods

### 3. Research Opportunities
- Compare frameworks scientifically
- Identify common patterns across methodologies
- Synthesize hybrid approaches

### 4. Teaching Aid
- Use known frameworks to teach TSCG concepts
- Concrete examples from practice
- Bridge theory and application

---

## 🚀 Next Steps

### Immediate (v2.4.0 deployment)
1. ✅ Deploy M3_GenesisSpace v2.4.0
2. Create M1_TRIZ.jsonld template
3. Create M1_VSD.jsonld template
4. Upgrade M0_TPACK to M1_TPACK

### Short-term
5. Document 3-5 core frameworks
6. Validate mappings with experts
7. Create cross-framework comparison guide
8. Update Smart Prompt with SystemicFramework

### Long-term
9. Build framework library (10+ frameworks)
10. Develop automated mapping tools
11. Create framework synthesis methodology
12. Publish cross-framework analysis papers

---

## 📊 Updated Category Hierarchy

```
m3:OntologyCategoryScheme (8 categories total)
│
├─── m3:Genesis (1)
│    └─── m3:GenesisExtension (2)
│
├─── m3:TransdisciplinaryPattern (1)
│    │
│    ├─── m3:DomainExtension (6+)
│    │    └─ Disciplinary knowledge
│    │
│    └─── m3:SystemicFramework ⭐ (5-20)
│         └─ Methodological frameworks
│              │
│              ├─── m3:Poclet (16+)
│              ├─── m3:CaseStudy (0)
│              └─── m3:RealWorldSystem (0)
```

---

**Version:** M3_GenesisSpace v2.4.0  
**Categories:** 8 total  
**New Addition:** m3:SystemicFramework ⭐  
**Status:** READY FOR DEPLOYMENT ✅
