# TSCG Poclet Creation Guide: Using Templates

**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-04-18  
**Version:** 2.0.0  
**Target Audience:** TSCG Users, Researchers, Framework Adopters

---

## 📋 Executive Summary

This guide provides a **complete methodology** for creating TSCG poclets using standardized templates. It addresses the need for **replicable modeling workflows** suitable for academic publication and framework adoption.

**What you'll learn:**
- How to select systems suitable for TSCG modeling
- How to use templates to create valid poclets
- How to validate and simulate your poclets
- Best practices from 23+ validated poclets

---

## 🎯 Why Templates Matter

### The Problem
Creating a TSCG poclet from scratch requires:
- Understanding JSON-LD syntax and RDF semantics
- Knowing SHACL validation constraints
- Implementing correct `xsd:float` typing
- Following TSCG architectural conventions
- Setting up proper namespace declarations

**This creates a high barrier to entry for new users.**

### The Solution: Templates
Pre-validated, well-structured templates that:
- ✅ Handle all technical complexities
- ✅ Enforce TSCG architectural standards
- ✅ Pass SHACL validation out-of-the-box
- ✅ Include inline documentation
- ✅ Enable focus on **content** not **syntax**

---

## 📦 Available Templates

### Core Templates (v2 - It/Im Nomenclature)

#### 1. **M0_POCLET_TEMPLATE_v2.jsonld**
**Purpose:** Complete poclet ontology structure

**Includes:**
- Bicephalous @context with It/Im nomenclature
- All required metadata fields
- ASFID/REVOI score structures
- Component/interaction modeling
- Float typing for all numeric properties

**Use when:** Creating any new poclet

---

#### 2. **M0_CONTEXT_TEMPLATE_v2.json**
**Purpose:** @context block reference

**Includes:**
- Standard RDF/OWL namespaces
- TSCG core namespaces (m0, m1, m2, m3)
- It/Im shorthand keys with xsd:float typing
- Optional M1 extension namespaces

**Use when:** Need to verify/update @context

---

### Supporting Scripts

#### 1. **create_new_poclet.ps1** (PowerShell)
**Purpose:** Automated poclet scaffolding

**Features:**
- Creates directory structure
- Copies and customizes template
- Replaces placeholders automatically
- Validates naming conventions

**Use when:** Starting a new poclet project

---

#### 2. **fix_scores_final.py** (Python)
**Purpose:** Fix float typing issues

**Use when:** SHACL validation fails with xsd:double errors

---

## 🚀 Quick Start: Create Your First Poclet

### Prerequisites
- TSCG repository cloned locally
- Python 3.7+ installed
- pyshacl installed (`pip install pyshacl`)
- Basic understanding of the system you want to model

### 5-Minute Workflow

```bash
# 1. Navigate to repository
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg

# 2. Create poclet from template
.\create_new_poclet.ps1 -Name "CrystalGrowth" -Domain "Chemistry"

# 3. Edit the generated file
# - Fill in ASFID/REVOI scores
# - Model components and interactions
# - Add justifications

# 4. Validate
pyshacl -s ontology\M0_Instances_Schema.shacl.ttl -df json-ld instances\poclets\CrystalGrowth\M0_CrystalGrowth.jsonld

# Expected: Conforms: True
```

---

## 📖 Detailed Poclet Creation Methodology

### Phase 1: System Selection

#### 1.1 Candidate Criteria
**Good poclet candidates:**
- ✅ Compact (3-5 key components)
- ✅ Well-understood scientifically
- ✅ Observable in practice
- ✅ Pedagogically valuable
- ✅ Cross-disciplinary connections

**Examples:**
- FireTriangle (chemistry/safety)
- FourStrokeEngine (thermodynamics/engineering)
- PhaseTransition (physics/chemistry)

**Poor candidates:**
- ❌ Overly complex systems (20+ components)
- ❌ Purely abstract concepts
- ❌ Systems without clear boundaries
- ❌ Domain-specific jargon-heavy systems

#### 1.2 Transdisciplinarity Test
Ask: **Can this system be understood through ≥2 disciplinary lenses?**

**Example:** FireTriangle
- Chemistry: Combustion reaction
- Thermodynamics: Energy transfer
- Safety Engineering: Risk management
- ✅ **Passes test**

---

### Phase 2: ASFID/REVOI Analysis

#### 2.1 Eagle Eye (ASFID) - Territory Analysis

**Process:**
1. **Attractor (A):** What stable states does the system tend toward?
2. **Structure (S):** What organized components/relationships exist?
3. **Flow (F):** What processes/transformations occur? (F=0 for static systems)
4. **Information (It):** What signals/data does the system produce?
5. **Dynamics (D):** How does the system change over time?

**Scoring Scale:** 0.0 (absent) to 1.0 (dominant)

**Example:** FireTriangle ASFID
```json
{
  "A": 0.75,  // Strong thermal attractor (equilibrium temp)
  "S": 0.90,  // Rigid triangular structure
  "F": 0.60,  // Continuous combustion flow
  "It": 0.80, // Observable flame characteristics
  "D": 0.50   // Moderate temporal dynamics
}
```

#### 2.2 Sphinx Eye (REVOI) - Map Quality Analysis

**Process:**
1. **Representable (R):** Can the model be easily visualized/diagrammed?
2. **Evolvable (E):** Can the model be extended (fire tetrahedron, etc.)?
3. **Verifiable (V):** Can predictions be experimentally tested?
4. **Observable (O):** Can system states be measured?
5. **Interoperable (Im):** Does the model connect with other frameworks?

**Example:** FireTriangle REVOI
```json
{
  "R": 0.90,  // Simple triangle diagram
  "E": 0.70,  // Evolvable to tetrahedron/pentagon
  "V": 0.95,  // Easily testable predictions
  "O": 0.80,  // Flame/temperature observable
  "Im": 0.90  // Connects to chemistry, safety, thermodynamics
}
```

#### 2.3 Epistemic Gap Calculation
Formula: **δ₁** (normalized vectorial - recommended)

The gap measures mismatch between Territory complexity and Map simplicity.

**Typical ranges:**
- **δ < 0.05:** Coherent (excellent match)
- **0.05 ≤ δ < 0.15:** On Critical Line (good match)
- **0.15 ≤ δ < 0.30:** Liminal (acceptable)
- **δ ≥ 0.30:** Enigmatic (poor match)

---

### Phase 3: Template Customization

#### 3.1 Metadata Fields

```json
{
  "@id": "",  // Leave empty (uses @base)
  "@type": "owl:Ontology",
  "m3:ontologyType": {"@id": "m3:Poclet"},
  "rdfs:label": "SystemName - Descriptive Title",
  "rdfs:comment": "Detailed description...",
  "owl:versionInfo": "1.0.0",
  "dcterms:creator": "Echopraxium with the collaboration of Claude AI",
  "dcterms:created": "2026-04-18",
  "m1:domain": ["Domain1", "Domain2"],  // Multi-domain support
  "owl:imports": [
    "M3_GenesisSpace.jsonld",
    "M2_GenericConcepts.jsonld",
    "M1_CoreConcepts.jsonld"
  ]
}
```

**Key Points:**
- Use **rdfs:label**, not dcterms:title (SHACL constraint)
- Use **rdfs:comment**, not dcterms:description
- Use **owl:versionInfo**, not m0:version
- Use **m1:domain**, not m0:domain
- Multi-domain: Use array `["Chemistry", "Physics"]`

#### 3.2 ASFID/REVOI Scores

**Template structure:**
```json
"m0:asfidScores": {
  "A": 0.75,
  "S": 0.90,
  "F": 0.60,
  "It": 0.80,
  "D": 0.50,
  "m0:mean": 0.71,
  "m0:justification": "Detailed explanation..."
}
```

**Critical:**
- Use **It** (Information/Territory), not `I` or `I_asfid`
- Use **Im** (Interoperability/Map) in REVOI, not `I` or `I_revoi`
- All scores MUST be 0.0-1.0
- Calculate mean: `(A + S + F + It + D) / 5`
- Provide detailed justification for each dimension

#### 3.3 Component Modeling

**Use M2 GenericConcepts** from `M2_GenericConcepts.jsonld` (75 concepts, 9 families)

**Example:**
```json
"m0:components": [
  {
    "@id": "m0:Oxygen",
    "@type": "m0:PocletComponent",
    "rdfs:label": "Oxygen (O₂)",
    "rdfs:comment": "Comburant enabling combustion",
    "m2:genericConcept": {"@id": "m2:Reagent"}
  },
  {
    "@id": "m0:Fuel",
    "@type": "m0:PocletComponent",
    "rdfs:label": "Fuel",
    "rdfs:comment": "Combustible material",
    "m2:genericConcept": {"@id": "m2:Reagent"}
  }
]
```

**Tips:**
- Keep components minimal (3-5 ideal)
- Use clear, domain-neutral labels where possible
- Reference appropriate M2 GenericConcepts
- Add scientific details in comments

#### 3.4 Interaction Modeling

**Example:**
```json
"m0:interactions": [
  {
    "@id": "m0:CombustionReaction",
    "@type": "m0:PocletInteraction",
    "rdfs:label": "Combustion Reaction",
    "rdfs:comment": "Exothermic oxidation process",
    "m0:source": {"@id": "m0:Oxygen"},
    "m0:target": {"@id": "m0:Fuel"},
    "m2:genericConcept": {"@id": "m2:Reaction"}
  }
]
```

---

### Phase 4: Validation

#### 4.1 SHACL Validation
```bash
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld instances/poclets/YourPoclet/M0_YourPoclet.jsonld
```

**Expected output:**
```
Validation Report
Conforms: True
```

#### 4.2 Common Validation Errors

**Error 1: xsd:double instead of xsd:float**
```
Value Node: Literal("0.75", datatype=xsd:double)
```
**Fix:** Use `fix_scores_final.py`

**Error 2: Missing required property**
```
Message: rdfs:label is MANDATORY
```
**Fix:** Add missing property to JSON-LD

**Error 3: Wrong namespace**
```
Message: Use rdfs:label instead of dcterms:title
```
**Fix:** Replace with correct property

---

### Phase 5: Documentation (Optional but Recommended)

#### 5.1 README Structure
Create `M0_PocletName_README.md` with:

1. **Header** - Title, domain, version
2. **Overview** - What system is modeled
3. **ASFID Analysis** - Territory perspective with state vector
4. **REVOI Analysis** - Map quality perspective with state vector
5. **Epistemic Gap** - δ calculation and spectral classification
6. **Components** - Detailed component descriptions
7. **Synergies** - Key interactions and emergent properties
8. **References** - Scientific sources

**Template available:** See FireTriangle README as reference

#### 5.2 Simulation (Advanced)
For interactive p5.js HTML simulations:
- Use `M0_FireTriangle.html` as canonical layout reference
- Follow CSS Grid pattern (header / left | center | split | sidebar)
- Include 4-tab sidebar (Description, Concepts, Synergy, Scores)
- Use dark theme with TSCG color palette

---

## ✅ Quality Checklist

### Ontology (JSON-LD)
- [ ] Uses `M0_POCLET_TEMPLATE_v2.jsonld` as base
- [ ] All metadata fields completed
- [ ] ASFID scores justified (each dimension explained)
- [ ] REVOI scores justified
- [ ] Epistemic gap calculated and classified
- [ ] Components reference M2 GenericConcepts
- [ ] Interactions modeled with source/target
- [ ] SHACL validation passes (`Conforms: True`)
- [ ] File encoding is UTF-8
- [ ] Uses It/Im nomenclature (not I_asfid/I_revoi)

### Documentation
- [ ] README created with complete analysis
- [ ] State vectors in Dirac notation
- [ ] References to scientific sources
- [ ] Clear component descriptions
- [ ] Synergy principles explained

### Technical
- [ ] File named `M0_PocletName.jsonld` (PascalCase)
- [ ] Located in `instances/poclets/PocletName/`
- [ ] @base URL is correct
- [ ] No forbidden namespaces (tscg:)
- [ ] Changelog follows array format
- [ ] Multi-domain when applicable

---

## 🎓 Learning from Examples

### Canonical Reference Poclets

#### 1. **FireTriangle** (Beginner-friendly)
**Why it's canonical:**
- Simple 3-component structure
- Well-known scientific model
- Clear ASFID/REVOI scores
- Excellent documentation
- Interactive simulation

**Path:** `instances/poclets/FireTriangle/`

**Learn:** Basic poclet structure, documentation standards

---

#### 2. **FourStrokeEngine** (Intermediate)
**Why it's valuable:**
- Temporal/cyclic dynamics (4 stages)
- Multiple Generic Concepts used
- Engineering domain
- Shows F (Flow) dimension clearly

**Path:** `instances/poclets/FourStrokeEngine/`

**Learn:** Modeling cyclic processes, engineering systems

---

#### 3. **TrophicPyramid** (Advanced)
**Why it's complex:**
- Hierarchical structure
- External parameter (AP - Anthropic Pressure)
- Ecological modeling
- Collapse dynamics

**Path:** `instances/poclets/TrophicPyramid/`

**Learn:** Hierarchies, external parameters, collapse modeling

---

## 📊 Validation Statistics (Corpus of 23+ Poclets)

### SHACL Compliance Rates
- **@type: owl:Ontology:** 100% (after normalization)
- **m3:ontologyType:** 100% (after migration)
- **rdfs:label:** 100%
- **rdfs:comment:** 100%
- **owl:versionInfo:** 100%
- **dcterms:creator:** 100%
- **m1:domain:** 100%
- **ASFID/REVOI scores:** 54% (optional but recommended)

### Common GenericConcepts Used
1. **Reagent** - 18 poclets
2. **Reaction** - 15 poclets
3. **Equilibrium** - 12 poclets
4. **Threshold** - 10 poclets
5. **Flow** - 9 poclets

**Tip:** Check existing poclets to see how GenericConcepts are applied in your domain

---

## 🚨 Common Pitfalls

### 1. Over-Complexity
**Problem:** Trying to model entire domain in one poclet

**Solution:** Focus on **minimal complete system** (3-5 components)

**Example:** Don't model "entire chemistry" - model "acid-base reaction"

---

### 2. Domain-Specific Jargon
**Problem:** Using only specialist terminology

**Solution:** Balance domain terms with Generic Concepts

**Example:** "Oxidizer" (domain) + "Reagent" (M2 generic)

---

### 3. Missing Justifications
**Problem:** Scores without explanation

**Solution:** Always justify each ASFID/REVOI dimension

**Example:**
```json
"m0:justification": "A=0.75: Strong thermal attractor (equilibrium temp 800-1200°C). S=0.90: Rigid triangular structure with 3 vertices..."
```

---

### 4. Wrong Property Names
**Problem:** Using `dcterms:title` instead of `rdfs:label`

**Solution:** Follow SHACL constraints (see template)

**Quick reference:**
- ✅ rdfs:label, rdfs:comment, owl:versionInfo, m1:domain
- ❌ dcterms:title, dcterms:description, m0:version, m0:domain

---

## 🔮 Advanced Topics

### Multi-Domain Modeling
**When to use:**
- System inherently spans disciplines
- Transdisciplinary analysis is core value

**Example:**
```json
"m1:domain": ["Chemistry", "Thermodynamics", "Fire Safety"]
```

**SHACL support:** Fully supported (string or array)

---

### M1 Extensions
**When to use:**
- Domain-specific concepts needed
- Generic M2 concepts insufficient

**Available extensions:**
- M1_Biology.jsonld
- M1_Chemistry.jsonld
- M1_Optics.jsonld
- M1_Photography.jsonld
- M1_Economics.jsonld
- M1_Mythology.jsonld

**Usage:**
```json
"@context": {
  "m1chem": "M1_extensions/chemistry/M1_Chemistry.jsonld#"
},
"owl:imports": ["M1_extensions/chemistry/M1_Chemistry.jsonld"],

// In components:
"m1chem:Combustion": {...}
```

---

## 📚 Additional Resources

### TSCG Core Documentation
- **TSCG Smart Prompt** - Complete framework specification
- **M2_GenericConcepts.jsonld** - 75 transdisciplinary concepts
- **M3_GenesisSpace.jsonld** - ASFID/REVOI dimension definitions
- **M0_Instances_Schema.shacl.ttl** - Validation constraints

### Tools
- **pyshacl** - SHACL validation (`pip install pyshacl`)
- **TscgPocletMiner** - LLM-assisted poclet discovery (ElectronJS app)

### Community
- **GitHub:** https://github.com/Echopraxium/tscg
- **GitHub Pages:** https://echopraxium.github.io/tscg/
- **Zenodo:** DOI: 10.5281/zenodo.18471860 (research article)

---

## 🤝 Contributing Your Poclets

### Submission Guidelines
1. Validate with SHACL (`Conforms: True`)
2. Include README documentation
3. Provide scientific references
4. Test on multiple browsers (if simulation included)
5. Submit via GitHub pull request

### Review Criteria
- Scientific accuracy
- TSCG architectural compliance
- Documentation completeness
- Code quality (for simulations)
- Pedagogical value

---

## 📜 License

**Templates:** BSD 3-Clause (free to use, modify, distribute)  
**Documentation:** CC BY 4.0 (attribution required)

---

## 🎓 Citation

If you use these templates in academic work:

```bibtex
@misc{tscg_templates_2026,
  author = {Echopraxium and Claude AI},
  title = {TSCG Poclet Creation Templates and Methodology},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/Echopraxium/tscg}
}
```

---

## 🙏 Acknowledgments

These templates and methodology were developed through iterative collaboration between:
- **Michel (Echopraxium):** TSCG framework creator, 25+ years development
- **Claude AI (Anthropic):** Collaborative refinement, template design, validation

**Template lineage:**
- v1.0 (2024): Initial templates with long-form property names
- v2.0 (2026): It/Im nomenclature, multi-domain support, SHACL-compliant

This work demonstrates the TSCG principle of **human-AI synergy** in knowledge framework evolution.

---

**Last Updated:** 2026-04-18  
**Template Version:** 2.0.0  
**Framework Version:** TSCG v15.11.0
