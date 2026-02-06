# Cascade Metaconcept: Modeling Guide

**Version**: 14.5.0  
**Date**: 2026-02-06  
**Author**: Echopraxium with the collaboration of Claude AI  
**Metaconcept Type**: Ternary MetaconceptCombo (N=3)

---

## Table of Contents

1. [Overview](#overview)
2. [Theoretical Foundation](#theoretical-foundation)
3. [When to Use Cascade](#when-to-use-cascade)
4. [Modeling Steps](#modeling-steps)
5. [Attribute Selection Guide](#attribute-selection-guide)
6. [Complete Examples](#complete-examples)
7. [Common Patterns](#common-patterns)
8. [Validation Checklist](#validation-checklist)
9. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Cascade?

**Cascade** is a sequential multi-stage process where:
- Output of each step becomes input of next step
- System evolves through discrete stages
- Evolution follows a trajectory toward a goal state

**Formula**: `Cascade = ⊗⇒(Process, Step, Trajectory)`

**Expanded**: `S ⊗ I ⊗ A ⊗ D ⊗ F` (ALL 5 ASFID dimensions)

### Key Characteristics

| Dimension | Meaning in Cascade |
|-----------|-------------------|
| **S** (Structure) | Ordered sequence of stages (Step₁ → Step₂ → ... → Stepₙ) |
| **I** (Information) | Data/signal/substrate transferred between stages |
| **A** (Attractor) | Goal state toward which cascade evolves |
| **D** (Dynamics) | Temporal progression through stages |
| **F** (Flow) | Material/energy/signal flowing through cascade |

### Ternary Composition

Cascade uniquely combines **three** parent metaconcepts:

```
Process (D⊗F)
   ↓
   + temporal evolution with flow
   
Step (S⊗I⊗D)
   ↓
   + structured stages with information transfer
   
Trajectory (A⊗D⊗F)
   ↓
   + goal-directed path
   
= Cascade (S⊗I⊗A⊗D⊗F)
```

---

## Theoretical Foundation

### Why Ternary?

Each parent contributes essential, irreducible aspects:

**Process alone** (D⊗F):
- ❌ No staged structure
- ❌ No information transfer
- ❌ No goal

**Process ⊗ Step** (S⊗I⊗D⊗F):
- ✅ Has stages
- ✅ Has information transfer
- ❌ No goal (aimless cascade)

**Process ⊗ Step ⊗ Trajectory** (S⊗I⊗A⊗D⊗F):
- ✅ Has stages
- ✅ Has information transfer
- ✅ Has goal state ← COMPLETE

### Shared Dimensions (Coupling)

```
Process:    D ⊗ F
Step:       S ⊗ I ⊗ D      (shares D with Process)
Trajectory: A ⊗ D ⊗ F      (shares D with both, F with Process)
────────────────────────────
Result:     S ⊗ I ⊗ A ⊗ D ⊗ F
```

**Coupling effects**:
- **D (Dynamics)**: Triplet coupling across all three
  - Temporal evolution (Process)
  - Sequential ordering (Step)
  - Goal-directed progression (Trajectory)
  
- **F (Flow)**: Pairwise coupling
  - Material/energy transfer (Process)
  - State-space navigation (Trajectory)

---

## When to Use Cascade

### ✅ Use Cascade When System Has:

1. **Sequential stages** (discrete steps, not continuous)
2. **Output → Input coupling** (Stage_i output feeds Stage_{i+1} input)
3. **Information/material transfer** between stages
4. **Goal state** (attractor, target, endpoint)
5. **Temporal progression** (evolves over time)

### ❌ Don't Use Cascade If:

1. **No discrete stages** → Use **Process** instead
2. **No goal state** → Consider **Process ⊗ Step** or **Sequence**
3. **Parallel processing** (no sequential dependency) → Use **Network** or **Parallel**
4. **No flow/transfer** between stages → Use **Sequence** or **Path**

### Decision Tree

```
Does system have discrete stages?
├─ NO → Use Process (continuous)
└─ YES
    ├─ Output of stage_i feeds input of stage_{i+1}?
    │   ├─ NO → Use Sequence or Path
    │   └─ YES
    │       ├─ Is there a goal state (attractor)?
    │       │   ├─ NO → Use Process⊗Step (or simple Sequence)
    │       │   └─ YES → Use Cascade ✓
    │       └─
    └─
```

---

## Modeling Steps

### Step 1: Identify Stages

**List all discrete stages** in your system:

**Example (RAAS)**:
1. Juxtaglomerular cells detect low blood pressure
2. Renin secretion
3. Angiotensinogen → Angiotensin I (via Renin)
4. Angiotensin I → Angiotensin II (via ACE)
5. Angiotensin II effects (vasoconstriction, aldosterone, etc.)

### Step 2: Verify Stage Coupling

**Check**: Does output of Stage_i become input of Stage_{i+1}?

**Example (RAAS)**:
```
Stage 1 output: Renin (enzyme)
    ↓ becomes input to Stage 2
Stage 2 output: Angiotensin I (peptide)
    ↓ becomes input to Stage 3
Stage 3 output: Angiotensin II (hormone)
    ✓ Cascade confirmed
```

### Step 3: Identify Goal State (Attractor)

**What is the cascade trying to achieve?**

**Examples**:
- **RAAS**: Blood pressure homeostasis (120/80 mmHg setpoint)
- **Coagulation**: Fibrin clot formation (hemostasis)
- **Compiler**: Executable binary
- **Development**: Mature organism

### Step 4: Determine Trajectory Shape

**How does system approach goal?**

| Shape | Use When |
|-------|----------|
| **Linear** | Monotonic convergence, no overshoot |
| **Spiral** | Oscillatory damped approach |
| **Piecewise** | Distinct developmental phases |
| **Chaotic** | Sensitive to initial conditions |

**Example (RAAS)**: Linear (smooth approach to BP setpoint)

### Step 5: Check Amplification

**Does each stage multiply the signal?**

- **YES** (Gain > 1): RAAS, coagulation, photomultiplier
- **NO** (Gain ≈ 1): Compiler pipeline, domino chain

### Step 6: Check Branching

**Does one stage feed multiple downstream stages?**

- **YES**: RAAS (Ang II → multiple effectors), signal transduction
- **NO**: Linear compiler, simple reaction chain

---

## Attribute Selection Guide

Cascade has **3 configurable attributes**:

### 1. trajectoryShape

**Type**: Discrete symbolic (from ValueSpace)  
**Values**: Linear, Circular, Elliptical, Spiral, Hyperbolic, Random, Constrained, Chaotic, Piecewise

**Selection Guide**:

```
How does system approach goal?
├─ Monotonic (no overshoot) → Linear
├─ Periodic return to start → Circular
├─ Damped oscillation → Spiral
├─ Distinct phases → Piecewise
├─ Unpredictable → Chaotic or Random
└─ On constrained manifold → Constrained
```

**Examples**:
- RAAS: `"Linear"` (smooth convergence to BP setpoint)
- Cell cycle: `"Circular"` (G1 → S → G2 → M → G1)
- Development: `"Piecewise"` (embryo → larva → pupa → adult)

---

### 2. amplifying

**Type**: Boolean  
**Values**: true, false

**Selection Guide**:

```
Is Gain > 1 at stages?
├─ YES → true
│   Examples: RAAS (enzymatic amplification)
│            Coagulation (exponential growth)
│            Photomultiplier (electron avalanche)
│
└─ NO → false
    Examples: Compiler (transformation, not amplification)
             Domino chain (gain ≈ 1)
```

**Formula**: `G_total = ∏ᵢ G_i`

If any stage has `G_i > 1`, consider `amplifying: true`

---

### 3. branching

**Type**: Boolean  
**Values**: true, false

**Selection Guide**:

```
Does one stage feed multiple parallel stages?
├─ YES → true
│   Examples: RAAS (Ang II → vasoconstriction + aldosterone + vasopressin)
│            Signal transduction (one receptor → multiple kinase pathways)
│
└─ NO → false
    Examples: Linear compiler pipeline
             Simple reaction chain A → B → C
```

**Topology**:
- **false**: Linear chain `A → B → C → D`
- **true**: Branching `A → B → {C₁, C₂, C₃}`

---

## Complete Examples

### Example 1: RAAS (Biological Cascade)

```json
{
  "@id": "m0:RAAS_Cascade",
  "@type": "m2:Cascade",
  "rdfs:label": "RAAS Hormonal Cascade",
  "rdfs:comment": "Renin-Angiotensin-Aldosterone System for blood pressure regulation",
  
  "trajectoryShape": "Linear",
  "trajectoryShape_rationale": "Monotonic convergence to BP setpoint without overshoot (typical homeostasis)",
  
  "amplifying": true,
  "amplifying_rationale": "Each enzymatic stage multiplies signal (one enzyme molecule converts multiple substrates)",
  
  "branching": true,
  "branching_rationale": "Angiotensin II activates multiple parallel effector pathways (vasoconstriction, aldosterone secretion, vasopressin stimulation)",
  
  "stages": [
    {
      "stage": 1,
      "name": "Pressure detection",
      "location": "Juxtaglomerular cells (kidney)",
      "input": "Blood pressure (sensor)",
      "output": "Renin secretion signal"
    },
    {
      "stage": 2,
      "name": "Renin catalysis",
      "input": "Angiotensinogen (substrate)",
      "process": "Renin cleaves Angiotensinogen",
      "output": "Angiotensin I (peptide)"
    },
    {
      "stage": 3,
      "name": "ACE conversion",
      "input": "Angiotensin I",
      "process": "ACE (lung capillaries) cleaves Ang I",
      "output": "Angiotensin II (active hormone)"
    },
    {
      "stage": 4,
      "name": "Effector activation",
      "input": "Angiotensin II",
      "branches": [
        "Vasoconstriction (immediate BP increase)",
        "Aldosterone secretion (Na⁺/H₂O retention)",
        "Vasopressin stimulation (H₂O retention)",
        "Sympathetic activation"
      ],
      "output": "Elevated blood pressure"
    }
  ],
  
  "attractor": {
    "description": "Blood pressure homeostasis",
    "setpoint": "120/80 mmHg (MAP ≈ 93 mmHg)",
    "type": "Stable fixed point"
  },
  
  "information_transfer": "Hormone concentrations ([Renin], [Ang I], [Ang II]) carry signal between stages",
  
  "flow_type": "Biochemical (peptide hormones in bloodstream)",
  
  "overall_gain": "G_total = G_renin × G_ACE × G_receptor ≫ 1 (high amplification)",
  
  "time_scale": "Minutes to hours (relatively slow hormonal response)"
}
```

---

### Example 2: Compiler Pipeline (Engineering Cascade)

```json
{
  "@id": "m0:Compiler_Cascade",
  "@type": "m2:Cascade",
  "rdfs:label": "Compiler Pipeline",
  "rdfs:comment": "Multi-stage transformation from source code to executable",
  
  "trajectoryShape": "Linear",
  "trajectoryShape_rationale": "Deterministic linear progression through compilation stages",
  
  "amplifying": false,
  "amplifying_rationale": "Each stage transforms representation but doesn't amplify information (lossy transformations, gain < 1 if anything)",
  
  "branching": false,
  "branching_rationale": "Strictly linear pipeline (one stage → one next stage)",
  
  "stages": [
    {
      "stage": 1,
      "name": "Lexical Analysis",
      "input": "Source code (text)",
      "process": "Tokenization",
      "output": "Token stream"
    },
    {
      "stage": 2,
      "name": "Parsing",
      "input": "Token stream",
      "process": "Syntax analysis (build AST)",
      "output": "Abstract Syntax Tree"
    },
    {
      "stage": 3,
      "name": "Semantic Analysis",
      "input": "AST",
      "process": "Type checking, symbol resolution",
      "output": "Annotated AST"
    },
    {
      "stage": 4,
      "name": "Optimization",
      "input": "Annotated AST",
      "process": "Code optimization (dead code elimination, constant folding, etc.)",
      "output": "Optimized IR (Intermediate Representation)"
    },
    {
      "stage": 5,
      "name": "Code Generation",
      "input": "Optimized IR",
      "process": "Generate machine code",
      "output": "Executable binary"
    }
  ],
  
  "attractor": {
    "description": "Executable binary",
    "type": "Terminal state (final product)"
  },
  
  "information_transfer": "Program semantics preserved through transformations (source → tokens → AST → IR → binary)",
  
  "flow_type": "Information flow (data structures representing program)",
  
  "overall_gain": "G ≈ 1 or < 1 (no amplification, possibly information loss in optimizations)",
  
  "time_scale": "Seconds to minutes (fast digital processing)"
}
```

---

### Example 3: Coagulation Cascade (Biological with Amplification)

```json
{
  "@id": "m0:Coagulation_Cascade",
  "@type": "m2:Cascade",
  "rdfs:label": "Blood Coagulation Cascade",
  "rdfs:comment": "Multi-enzyme cascade leading to fibrin clot formation",
  
  "trajectoryShape": "Linear",
  "trajectoryShape_rationale": "Exponential growth toward clot formation (runaway positive feedback until clot complete)",
  
  "amplifying": true,
  "amplifying_rationale": "Extreme amplification - each activated factor activates multiple downstream factors (exponential growth). Example: 1 Factor XIIa → 200 Factor XIa → 20,000 Thrombin molecules",
  
  "branching": true,
  "branching_rationale": "Intrinsic and extrinsic pathways converge, multiple feedback loops",
  
  "stages": [
    {
      "stage": 1,
      "name": "Initiation",
      "trigger": "Tissue damage or foreign surface",
      "pathways": ["Intrinsic pathway (contact activation)", "Extrinsic pathway (tissue factor)"],
      "output": "Factor XII activated → XIIa"
    },
    {
      "stage": 2,
      "name": "Amplification",
      "input": "Factor XIIa (or VIIa)",
      "cascade": "XIIa → XIa → IXa → Xa (each step amplifies)",
      "output": "Factor Xa (activated)"
    },
    {
      "stage": 3,
      "name": "Prothrombinase complex",
      "input": "Factor Xa + Va + Ca²⁺ + phospholipids",
      "process": "Formation of prothrombinase complex",
      "output": "Thrombin (Factor IIa) - MASSIVE amplification"
    },
    {
      "stage": 4,
      "name": "Fibrin formation",
      "input": "Thrombin",
      "process": "Thrombin cleaves Fibrinogen → Fibrin monomers → Fibrin polymer (cross-linked)",
      "output": "Fibrin mesh (clot)"
    }
  ],
  
  "attractor": {
    "description": "Stable fibrin clot (hemostasis achieved)",
    "type": "Stable state (clot formation complete)"
  },
  
  "information_transfer": "Activated enzyme concentrations propagate signal",
  
  "flow_type": "Enzymatic (proteases activating zymogens)",
  
  "overall_gain": "G_total ≫ 10,000 (one initiating molecule → thousands of fibrin strands)",
  
  "time_scale": "Seconds to minutes (rapid emergency response)",
  
  "regulation": "Anticoagulant factors (Protein C, Antithrombin) prevent runaway - otherwise lethal"
}
```

---

### Example 4: Photomultiplier Tube (Physics Cascade)

```json
{
  "@id": "m0:Photomultiplier_Cascade",
  "@type": "m2:Cascade",
  "rdfs:label": "Photomultiplier Tube",
  "rdfs:comment": "Electron avalanche cascade for photon detection",
  
  "trajectoryShape": "Linear",
  "trajectoryShape_rationale": "Linear amplification through dynode chain",
  
  "amplifying": true,
  "amplifying_rationale": "Each dynode produces 3-5 secondary electrons per incident electron (geometric growth)",
  
  "branching": false,
  "branching_rationale": "Linear dynode chain (but each electron branches into multiple at each dynode)",
  
  "stages": [
    {
      "stage": 1,
      "name": "Photoemission",
      "input": "Photon (light)",
      "process": "Photoelectric effect at photocathode",
      "output": "1 photoelectron"
    },
    {
      "stage": 2,
      "name": "Dynode 1",
      "input": "1 electron (accelerated by voltage)",
      "process": "Impact → secondary emission",
      "output": "δ₁ ≈ 4 electrons",
      "gain": "G₁ = 4"
    },
    {
      "stage": 3,
      "name": "Dynode 2",
      "input": "4 electrons",
      "output": "δ₁×δ₂ ≈ 16 electrons",
      "gain": "G₂ = 4"
    },
    "... (repeat for N dynodes)",
    {
      "stage": "N+1",
      "name": "Anode collection",
      "input": "δ₁×δ₂×...×δₙ electrons",
      "output": "Measurable current pulse"
    }
  ],
  
  "attractor": {
    "description": "Detectable electrical signal at anode",
    "type": "Signal above detection threshold"
  },
  
  "information_transfer": "Electron count (proportional to photon energy/count)",
  
  "flow_type": "Electron flow (charge carriers)",
  
  "overall_gain": "G_total = ∏ᵢ δᵢ ≈ 4^N. For N=10 dynodes: G ≈ 10⁶ (million-fold amplification)",
  
  "time_scale": "Nanoseconds (extremely fast electronic response)"
}
```

---

## Common Patterns

### Pattern 1: Homeostatic Biological Cascade

**Characteristics**:
- `trajectoryShape`: Linear
- `amplifying`: true
- `branching`: true (often)
- Attractor: Physiological setpoint

**Examples**: RAAS, thyroid axis, glucose regulation

**Template**:
```json
{
  "@type": "m2:Cascade",
  "trajectoryShape": "Linear",
  "amplifying": true,
  "branching": true,
  "attractor": "Homeostatic setpoint"
}
```

---

### Pattern 2: Linear Transformation Pipeline

**Characteristics**:
- `trajectoryShape`: Linear
- `amplifying`: false
- `branching`: false
- Attractor: Final product/state

**Examples**: Compiler, data pipeline, assembly line

**Template**:
```json
{
  "@type": "m2:Cascade",
  "trajectoryShape": "Linear",
  "amplifying": false,
  "branching": false,
  "attractor": "Final product"
}
```

---

### Pattern 3: Amplifying Exponential Cascade

**Characteristics**:
- `trajectoryShape`: Linear (but exponential growth rate)
- `amplifying`: true
- `branching`: true (often)
- Attractor: Threshold/saturation

**Examples**: Coagulation, nuclear chain reaction, viral spread

**Template**:
```json
{
  "@type": "m2:Cascade",
  "trajectoryShape": "Linear",
  "amplifying": true,
  "branching": true,
  "attractor": "Saturation/threshold",
  "note": "Requires regulation to prevent runaway"
}
```

---

### Pattern 4: Developmental Cascade

**Characteristics**:
- `trajectoryShape`: Piecewise
- `amplifying`: false (usually)
- `branching`: true (cell differentiation)
- Attractor: Mature organism

**Examples**: Embryogenesis, metamorphosis, cellular differentiation

**Template**:
```json
{
  "@type": "m2:Cascade",
  "trajectoryShape": "Piecewise",
  "amplifying": false,
  "branching": true,
  "attractor": "Mature state",
  "stages": "Distinct developmental phases"
}
```

---

## Validation Checklist

Before finalizing your Cascade model, verify:

### ✅ Structural Requirements

- [ ] System has discrete stages (not continuous)
- [ ] Output of Stage_i feeds input of Stage_{i+1}
- [ ] Stages are ordered sequentially
- [ ] Information/material transfers between stages

### ✅ ASFID Dimensions

- [ ] **S** (Structure): Stages clearly defined and ordered
- [ ] **I** (Information): What transfers between stages identified
- [ ] **A** (Attractor): Goal state clearly defined
- [ ] **D** (Dynamics): Temporal evolution characterized
- [ ] **F** (Flow): Flow type identified (material/energy/information)

### ✅ Attributes

- [ ] `trajectoryShape` selected and justified
- [ ] `amplifying` (true/false) determined
- [ ] `branching` (true/false) determined
- [ ] Rationales provided for each choice

### ✅ Distinction from Related Metaconcepts

- [ ] Not just a **Process** (has discrete stages)
- [ ] Not just **Step** sequence (has flow and goal)
- [ ] Not just a **Trajectory** (has staged structure)
- [ ] Not just a **Path** (observed in territory, not planned)

### ✅ Examples and Documentation

- [ ] At least 3 stage examples provided
- [ ] Attractor clearly described
- [ ] Gain/amplification quantified (if applicable)
- [ ] Time scale specified

---

## Troubleshooting

### Problem 1: "Is this Cascade or just Process?"

**Question**: My system evolves over time but I'm not sure if it's a Cascade.

**Solution**: Ask:
1. Can you identify discrete stages? (YES → might be Cascade)
2. Does each stage have distinct input/output? (YES → likely Cascade)
3. Is there stage-to-stage coupling? (YES → Cascade)

**Example**:
- ❌ Water heating (continuous temperature rise) → **Process**
- ✅ Water purification (filter₁ → filter₂ → UV → output) → **Cascade**

---

### Problem 2: "Cascade vs Workflow?"

**Question**: How is Cascade different from Workflow?

**Answer**:

| Aspect | Workflow | Cascade |
|--------|----------|---------|
| **Perspective** | Map (prescriptive) | Dual (map + territory) |
| **Formula** | S⊗D⊗F | S⊗I⊗A⊗D⊗F |
| **Goal** | Optional | Required (Attractor) |
| **Information** | Implicit | Explicit (I dimension) |
| **Use** | How process *should* be executed | How cascade *actually* evolves |

**Example**:
- Workflow: "Standard Operating Procedure for RAAS diagnosis"
- Cascade: "Actual RAAS hormonal cascade in patient"

---

### Problem 3: "No clear goal state"

**Question**: My system has stages but no obvious attractor. Can I still use Cascade?

**Answer**: 

**Option 1**: If truly no goal, consider:
- **Process ⊗ Step** (binary combo)
- **Sequence** (ordered without goal)

**Option 2**: Re-examine for implicit goal:
- Terminal state (e.g., "program exits")
- Equilibrium (e.g., "system stabilizes")
- Completion (e.g., "all stages done")

**Example**:
- "Domino chain" → Goal: All dominos fallen (terminal state)
- "Compiler" → Goal: Executable produced (terminal state)

If you identify implicit goal → Use Cascade with `trajectoryShape: "Linear"` and describe attractor as "Terminal state: [description]"

---

### Problem 4: "Amplifying unclear"

**Question**: How do I know if my cascade is amplifying?

**Answer**: Calculate stage gains:

```
G_i = Output_i / Input_i (for each stage)

If ANY G_i > 1 → amplifying: true
If ALL G_i ≈ 1 → amplifying: false
If ALL G_i < 1 → amplifying: false (attenuating)
```

**Examples**:
- RAAS enzyme (1 enzyme → 100 products) → G > 1 → **amplifying: true**
- Compiler (input tokens ≈ output AST nodes) → G ≈ 1 → **amplifying: false**
- Resistor cascade (voltage drops) → G < 1 → **amplifying: false**

---

### Problem 5: "Branching vs Parallel?"

**Question**: My cascade splits into multiple paths. Is this branching?

**Answer**: Distinguish:

**Branching** (Cascade attribute):
- One stage → multiple downstream stages
- Stages still sequential within each branch
- Example: RAAS (Ang II → [vasoconstriction, aldosterone, vasopressin])

**Parallel** (different metaconcept):
- Independent simultaneous processes
- No sequential dependency
- Example: Multi-core CPU (independent threads)

**Rule**: If branches are **downstream consequences** of earlier stage → **branching: true**

---

## Summary

### Quick Reference

**Cascade = ⊗⇒(Process, Step, Trajectory)**

**Use when**:
- Sequential stages ✓
- Output → Input coupling ✓
- Goal state ✓
- Information transfer ✓

**Attributes**:
1. `trajectoryShape`: How system approaches goal
2. `amplifying`: Whether gain > 1
3. `branching`: Whether one stage → multiple stages

**Formula**: `S ⊗ I ⊗ A ⊗ D ⊗ F` (complete ASFID)

**First metaconcept to cover all 5 ASFID dimensions!**

---

## References

- **M2_MetaConcepts.jsonld** (v14.5.0): Full Cascade definition
- **TSCG_Architectural_Extensions.md**: N-ary MetaconceptCombo theory
- **TSCG_ValueSpace_User_Guide.md**: Attribute usage
- **Poclet_Analysis_Methodology.md**: Discovery process

---

**End of Cascade Modeling Guide**

*Version 14.5.0 - 2026-02-06*
