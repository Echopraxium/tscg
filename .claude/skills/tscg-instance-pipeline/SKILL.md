---
name: tscg-instance-pipeline
description: >
  Complete pipeline for creating a TSCG Instance in 4 sequential steps: Proposition,
  Analysis, Modeling, and Simulation. Use this skill whenever the user mentions
  an instance, wants to model a system with TSCG, wants to create an M0 JSON-LD ontology,
  or proposes a system/process to analyze through the TSCG lens (ASFID/REVOI dimensions,
  M2 GenericConcepts, M1 extensions). Also applicable when the user asks "what do you
  think?" about a known system, or requests an HTML/Electron simulation of a TSCG system.
  Do NOT use for Case Studies or Real World Systems (too complex) — this pipeline is
  reserved for Instances.
---

# TSCG Instance Pipeline

4-step pipeline for creating a complete TSCG Instance:
**Proposition → Analysis → Modeling → Simulation**

Each step may contain **human synchronization points** (⏸) that suspend
the pipeline until Michel's explicit decision to continue.

---

## GitHub References (raw URLs)

Base: `https://raw.githubusercontent.com/echopraxium/tscg/main/`

**Ontology:**
- `ontology/M3_GenesisSpace.jsonld` — M3 genesis space
- `ontology/M3_EagleEye.jsonld` — ASFID dimensions
- `ontology/M3_SphinxEye.jsonld` — REVOI dimensions
- `ontology/M2_GenericConcepts.jsonld` — 58+ GenericConcepts
- `ontology/M1_CoreConcepts.jsonld` — core concepts
- `ontology/M1_extensions/M1_Chemistry.jsonld` — domain extension example

**Canonical reference instance:**
- `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`
- `instances/poclets/FireTriangle/M0_FireTriangle_README.md`

**Other existing instances (for comparison):**
AdaptativeImmuneResponse, BloodPressureControl, ButterflyMetamorphosis,
CellSignalingModes, ColorSynthesis (RGB/HSL/CMY/CMYK/Federated),
ComplexChemicalSynapse, ExposureTriangle, FourStrokeEngine, Kidneys,
KindlebergerMinsky, MtgColorWheel, NuclearReactorsTypology, PhaseTransition,
Raas, Tpack, Transistor, TrophicPyramid, TvTestPattern, VCO

**Reference documentation:**
- `docs/reboot-kit/M2_FormulasReference_v15.10.0.md`
- `docs/reboot-kit/SmartPrompts/` (Smart_Prompt_M3_M2_Updated.md if uploaded in session)

**SHACL validation:**
- `ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl` — grammar schema
- `ontology/TSCG_Grammar/validate_m0_instance.py` — validation script

**This skill (source of truth in repo):**
- `.claude/skills/tscg-instance-pipeline/SKILL.md`

---

## Step 1 — PROPOSITION

### Expected Input from Michel
1. **System name** (e.g., "Color Synthesis", "Fire Triangle")
2. **Brief description + examples** (few sentences, often pre-generated with DeepSeek)
3. **Diagnostic request** (e.g., "what do you think?")

### Expected Response: TSCG Feasibility Diagnostic

Produce a **dual evaluation**:

**A. TSCG Lens**
- Which ASFID dimensions are active? (A/S/F/I/D)
- Which M2 GenericConcepts seem relevant a priori?
- Is the system well-bounded (minimal + complete)?

**B. Experience Perspective**
- Comparison with existing instances (similarities, close domain)
- Anticipated difficulties
- Estimated richness (number of mobilizable GenericConcepts)

### System Classification — MANDATORY DECISION

| Verdict | Criterion | Next Step |
|---------|-----------|-----------|
| 🟡 **Too trivial** | Too few active dimensions, no dynamics, no feedback | ⏸ Stop with explanation |
| 🟢 **Valid instance** | Appropriate complexity, modelable in minimal complete JSON-LD | → Continue to Step 2 |
| 🔵 **Too complex** | LLM, Microprocessor, Mitochondria… → requires different pipeline | ⏸ Stop with orientation |

> If the system is "borderline", propose a reduced scope to make it
> a valid instance (e.g., "simple chemical synapse" instead of "the brain").

⏸ **Sync point if verdict ≠ Valid instance** — wait for Michel's decision.

---

## Step 2 — ANALYSIS

### Objective
Assess the alignment between the proposed system and the TSCG framework.
This is an **epistemic act**, not just a technical verification.

### Three Possible Outcomes

| Result | Description | Behavior |
|--------|-------------|----------|
| ✅ **Alignment** | System models well with existing metaconcepts and dimensions | Continue to Step 3 |
| ⚠️ **Gap** | Modeling reveals a "hole" in the framework | ⏸ Document + discuss with Michel |
| 🔬 **Refutation (Popper)** | System challenges a TSCG axiom or principle | ⏸ Explain, justify in detail |

> A Gap or Refutation has **positive value**: it contributes to TSCG's evolution.
> Refutation has maximum value — it forces framework strengthening or revision.

### Output: `analysis.md`

File structure:
```
# TSCG Analysis — [System Name]

## Verdict: [Alignment | Gap | Refutation]

## ASFID Lens
- A (Attractor): ...
- S (Structure): ...
- F (Flow): ...
- I (Information): ...
- D (Dynamics): ...

## Anticipated M2 GenericConcepts
- [Name] ([tensor formula]) — anticipated role

## Comparison with existing instances
- [Similar instance]: [similarities / differences]

## Detailed Verdict
[If Gap: precise description of identified hole]
[If Refutation: complete Popperian argument + justification]

## Recommended Decision
[Continue | Discuss | Revise scope]
```

⏸ **Sync point if Gap or Refutation** — wait for Michel's decision before continuing.

---

## Step 3 — MODELING

### Internal Pipeline (sequential sub-steps)

#### 3.1 — M2 Identification (GenericConcepts)
- List relevant **existing GenericConcepts** with their tensor formula
  (e.g., `Synergy = A⊗S⊗I`, `Trigger = D⊗I`, `Process = D⊗F`)
- Identify **new candidates** if a necessary concept doesn't exist yet
- Response format for new candidate:
  ```
  🆕 M2 Candidate: [Name]
  Tensor formula: [e.g., S⊗I]
  Role: [description]
  Status: "Proposal — to be validated"
  ```

#### 3.2 — M1 Identification (KnowledgeFieldConceptCombos)
- List used KnowledgeFieldConceptCombos (e.g., `m1:chemistry:Combustion`)
- Identify **new M1 candidates** if necessary
- Identify if a **new M1 extension** is required or if an existing extension
  should be enriched (e.g., new class in `M1_Chemistry.jsonld`)

#### 3.3 — M0 JSON-LD Generation

Follow **scrupulously** the FireTriangle pattern as reference template.

**Mandatory `@context` structure:**
```json
{
  "@context": {
    "dcterms": "http://purl.org/dc/terms/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m1:core": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m1:[domain]": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/M1_[Domain].jsonld#",
    "m0:[instance-id]": "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/[type]/[InstanceName]/M0_[InstanceName].jsonld#"
  }
}
```

**Mandatory JSON-LD sections:**
1. Metadata (`rdfs:label`, `rdfs:comment`, `dcterms:created`, `dcterms:creator`, `m2:changelog`)
2. `m3:ontologyType`, `m1:domain`, `completeness`, `minimality`, `pedagogy`, `observer`
3. `components` (list of components with `asfidContribution` per component)
4. `process` or main mechanism
5. `territorySpace` (ASFID / Eagle Eye) with `stateVector` and `norm`
6. `mapSpace` (REVOI / Sphinx Eye) with `reviStateVector` and `reviNorm`
7. `epistemicGap` (ΔΘ formula, `deltaVector`, `norm`, interpretation)
8. `revoi` (detailed analysis of 5 REVOI dimensions with justification)
9. `GenericConceptsMobilized` (total + `byCategory`)
10. `validation` (checklist ASFID completeness, GenericConcept coverage, minimality, emergence)

> ⏸ **"Duo analysis" mode** if any blocking occurs at any sub-step
> (concept not found, tension between dimensions, namespace doubt) —
> suspend and open discussion with Michel.

#### 3.4 — README.md Generation

After JSON-LD validation, generate `M0_[InstanceName]_README.md` with:
```
# [Instance Name] — TSCG Instance

## Overview
## System Description
## TSCG Analysis
### ASFID State (Territory / Eagle Eye)
### REVOI State (Map / Sphinx Eye)
### Epistemic Gap
## Components
## GenericConcepts Mobilized
## Key Insights
## Transdisciplinary Analogies (if relevant)
## References
```

#### 3.5 — SHACL Grammar Validation

**CRITICAL STEP**: After generating the M0 JSON-LD file, validate it against
the TSCG SHACL grammar schema to ensure complete conformance.

**Validation script location:**
- `ontology/TSCG_Grammar/validate_m0_instance.py` (standalone Python script)
- **Note**: Script must be run from repository root directory

**Usage:**
```bash
# From repository root
python ontology/TSCG_Grammar/validate_m0_instance.py instances/[type]/[InstanceName]/M0_[InstanceName].jsonld

# Example
python ontology/TSCG_Grammar/validate_m0_instance.py instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

**Expected outcome:**
- ✅ **Validation PASSED**: "Conforms: True" — Continue to Step 4
- ❌ **Validation FAILED**: SHACL constraint violations detected

**If validation fails:**
1. Review the SHACL violation report
2. Identify which constraints were violated:
   - Missing mandatory properties (rdfs:label, m3:ontologyType, m1:domain, etc.)
   - Incorrect property values (wrong namespace, wrong type, etc.)
   - Forbidden properties (dcterms:title, m2:ontologyCategory, etc.)
   - Incorrect @context URLs (relative instead of absolute)
3. Fix the JSON-LD file accordingly
4. Re-run validation until it passes

**Common validation errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| "m3:ontologyType MUST be one of..." | Missing or wrong ontologyType | Add `"m3:ontologyType": {"@id": "m3:Poclet"}` |
| "m1:domain is MANDATORY" | Missing domain property | Add `"m1:domain": "Chemistry"` |
| "Use rdfs:label instead of dcterms:title" | Wrong property name | Rename `dcterms:title` → `rdfs:label` |
| "pyshacl cannot resolve relative URLs" | Relative namespace URLs in @context | Replace `"M3_GenesisSpace.jsonld#"` with full `https://raw.githubusercontent.com/...` |
| "owl:Ontology required" | Wrong @type value | Change `"@type": "owl:NamedIndividual"` → `"owl:Ontology"` |

> ⏸ **Mandatory sync point if validation fails repeatedly** — discuss structural
> issues with Michel before continuing.

**Only proceed to Step 4 (Simulation) after successful SHACL validation.**

---

## Step 4 — SIMULATION

### Objective
Generate a **standalone HTML application** (Electron and browser compatible)
visualizing the instance in an interactive, pedagogical, and aesthetic way.

### Reference Template
The FireTriangle HTML is the **canonical template**. Conform to it for:
- CSS Grid layout: `header / canvas + splitter + sidebar / controls`
- GitHub-style dark theme (CSS variables for ASFID/REVOI colors)
- Tabbed sidebar: Description | ASFID/REVOI | GenericConcepts | README
- Draggable splitter between canvas and sidebar
- Everything inline in a single `.html` file (no external files except CDN)

### ASFID/REVOI Color Palette (reusable CSS variables)
```css
--col-A: #f78166;  /* Attractor — red-salmon */
--col-S: #56d364;  /* Structure — green */
--col-F: #79c0ff;  /* Flow — light blue */
--col-I: #d2a8ff;  /* Information — purple */
--col-D: #e3b341;  /* Dynamics — amber */
--col-R: #79c0ff;  /* Representability */
--col-E: #56d364;  /* Evolvability */
--col-V: #f78166;  /* Verifiability */
--col-O: #d2a8ff;  /* Observability */
--col-Im: #e3b341; /* Interoperability */
--eagle:  #f78166; /* Eagle Eye accent */
--sphinx: #79c0ff; /* Sphinx Eye accent */
```

### Allowed Libraries (cdnjs.cloudflare.com CDN only)
- **p5.js** — main canvas animation (mandatory)
- Chart.js, D3 — complementary visualizations (optional)

### CSP Header (Electron + standalone compatible)
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self' https://cdnjs.cloudflare.com;
               script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
               style-src  'self' 'unsafe-inline';
               img-src    'self' data: blob:;
               connect-src http://127.0.0.1:* ws://127.0.0.1:*;">
```

### Iterative Process

**First draft**: generate a functional simulation covering:
- p5.js canvas animation representing system dynamics
- Sidebar with ASFID/REVOI scores (colored progress bars)
- List of mobilized GenericConcepts
- README tab with instance description

**Refinement rounds** (successive iterations with Michel):
- Ergonomics round: interactive controls, sliders, buttons
- Pedagogy round: labels, tooltips, annotations, legends
- Aesthetics round: animations, colors, proportions, visual polish

> Michel decides the number of rounds and priorities at each iteration. ⏸ after each round.

---

## File Naming Conventions

```
instances/[type]/[InstanceName]/
├── M0_[InstanceName].jsonld         ← M0 ontology
├── M0_[InstanceName]_README.md      ← documentation
├── M0_[InstanceName]_analysis.md    ← TSCG analysis (step 2)
└── [InstanceName]_sim.html          ← standalone simulation
```

`[InstanceName]` is in PascalCase (e.g., `FireTriangle`, `ColorSynthesis`).
`[type]` is one of: `poclets`, `symbolic-system-grammars`, `systemic-frameworks`

---

## Pipeline Summary and Sync Points

```
PROPOSITION
  └─ Diagnostic (TSCG lens + experience perspective)
  └─ Classification: Trivial⏸ | Valid instance✅ | Too complex⏸
       ↓ (if Valid instance)
ANALYSIS → analysis.md
  └─ Alignment✅ | Gap⏸ | Refutation⏸
       ↓ (if Alignment)
MODELING
  ├─ 3.1 M2 GenericConcepts (existing + candidates)
  ├─ 3.2 M1 KnowledgeFieldConceptCombos (existing + candidates)
  ├─ 3.3 M0 JSON-LD  ← duo mode if blocking ⏸
  ├─ 3.4 README.md
  └─ 3.5 SHACL validation ← MANDATORY, must pass ✅⏸
       ↓ (only if SHACL validation passes)
SIMULATION
  └─ First HTML standalone draft
  └─ Iterative rounds (ergonomics / pedagogy / aesthetics) ⏸⏸⏸
```

---

## Validation Script Requirements

The `validate_m0_instance.py` script (located in `ontology/TSCG_Grammar/`) must:
- Accept a single JSON-LD file path as argument
- Auto-detect the SHACL schema in `ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl`
- Allow optional custom schema path via `--schema` argument
- Use `pyshacl` library for validation
- Display clear success/failure messages
- Return exit code 0 for success, 1 for failure
- Show detailed violation report if validation fails

**Installation requirement:**
```bash
pip install pyshacl --break-system-packages
```

**Script location:**
```
ontology/TSCG_Grammar/
├── M0_Instances_Schema.shacl.ttl    ← SHACL schema
└── validate_m0_instance.py          ← validation script
```

**Example validation output:**
```
======================================================================
TSCG M0 INSTANCE SHACL VALIDATION
======================================================================

📄 Instance file: instances/poclets/FireTriangle/M0_FireTriangle.jsonld
📋 Schema file:   ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl

======================================================================

✅ VALIDATION PASSED - Instance conforms to TSCG SHACL grammar

======================================================================
```
