# Blood Pressure Control Poclet - TSCG M0 Layer

**Poclet Name**: Blood Pressure Homeostasis (5-Effector System)  
**Domain**: Physiology / Cardiovascular System  
**Namespace**: `m0:blood_pressure_control:`  
**Version**: 1.0.0  
**Date**: 2026-01-22  
**Authors**: Echopraxium with the collaboration of Claude AI

---

## Overview

The **Blood Pressure Control** poclet models the long-term regulation of arterial blood pressure through the coordinated action of five physiological effector systems. This poclet demonstrates how multiple feedback loops operating at different timescales (seconds to days) maintain homeostasis of a critical physiological parameter.

### The Phenomenon

**Central Question**: How does the body maintain stable blood pressure (~120/80 mmHg in humans) despite continuous perturbations (stress, exercise, posture changes, sodium intake variations)?

**Answer**: Through five parallel regulatory systems that converge on arterial pressure:

1. **Renin-Angiotensin-Aldosterone System (RAAS)**: Hormonal cascade controlling volemia and vasoconstriction
2. **Sympathetic Nervous System**: Rapid neural reflex modulating heart rate and vascular tone
3. **Anti-Diuretic Hormone (ADH/Vasopressin)**: Water retention and vasoconstriction
4. **Natriuretic Peptides (ANP/BNP)**: Counter-regulatory hormones promoting sodium/water excretion
5. **Cardiac Output & Volemia**: Downstream hemodynamic parameters resulting from effectors 1-4

**Pathological State**: Chronic hypertension results from dysregulation in one or more of these systems (e.g., RAAS hyperactivity, impaired natriuretic response).

---

## TSCG Analysis

### ASFID Dimensions (Territory Perspective - Eagle Eye)

#### **A (Attractor)** - Score: 0.85
- **Set-point**: 120/80 mmHg (systolic/diastolic)
- **Basin of attraction**: Homeostatic zone (~100-140 mmHg systolic)
- **Multiple attractors**: Resting, exercise, stress states
- **Stability mechanisms**: Negative feedback loops (baroreflex, RAAS, ANP)
- **Pathological attractor**: Hypertensive state (>140/90 mmHg) - can become stable through vascular remodeling

**Formula**: `A = S(Feedback_strength × Attractor_depth)`

#### **S (Structure)** - Score: 0.80
- **5 effector subsystems** organized in parallel network
- **Hierarchical organization**: 
  - Fast control: Sympathetic nervous system (seconds)
  - Medium-term: Hormonal systems (minutes-hours)
  - Long-term: Renal mechanisms (hours-days)
- **Anatomical components**: Heart, kidneys, blood vessels, adrenal glands, hypothalamus, baroreceptors
- **Topological pattern**: Convergent network (5 ? 1 controlled variable)

**Formula**: `S = Network_complexity × Hierarchical_depth`

#### **F (Flow)** - Score: 0.90
- **Blood flow**: Cardiac output (5 L/min in humans)
- **Hormonal flux**: Renin, angiotensin, aldosterone, ADH, ANP circulation
- **Renal flux**: Sodium/water filtration and excretion (~180 L/day glomerular filtrate)
- **Intercompartmental exchange**: Vascular ? interstitial ? intracellular fluid shifts
- **Energy flow**: ATP consumption for cardiac work, ion pumps

**Formula**: `F = S(Flux_rates) × Exchange_surface`

#### **I (Information)** - Score: 0.85
- **Primary signal**: Arterial pressure (baroreceptors in aortic arch, carotid sinus)
- **Hormonal signaling**: 
  - RAAS cascade (renin ? angiotensinogen ? Ang I ? Ang II ? aldosterone)
  - ADH from hypothalamus
  - ANP/BNP from heart
- **Neural signaling**: Sympathetic efferents (norepinephrine release)
- **Feedback loops**: Multiple negative feedback (baroreceptor reflex, ANP response to volume overload)
- **Coding**: Frequency-encoded (neural firing), concentration-encoded (hormones)

**Formula**: `I = Shannon_entropy(signals) × Feedback_loop_count`

#### **D (Dynamics)** - Score: 0.75
- **Multi-scale temporal dynamics**:
  - **Fast** (seconds): Baroreceptor reflex (sympathetic activation/inhibition)
  - **Medium** (minutes-hours): RAAS activation, ADH secretion
  - **Slow** (hours-days): Renal sodium/water excretion, vascular remodeling
- **Transient response**: Overshoot/undershoot during rapid pressure changes
- **Pathological transition**: Normotension ? hypertension (bifurcation through positive feedback in RAAS or vascular stiffening)
- **Adaptation**: Chronic reset of baroreceptor sensitivity in sustained hypertension

**Formula**: `D = S(dState/dt) across all timescales`

---

### ORIVE Metrics (Map Perspective - Sphinx Eye)

#### **O (Observability)** - Score: 0.85
**What can we measure directly?**
- ? **Arterial pressure**: Direct (arterial catheter) or indirect (sphygmomanometer) - highly accurate
- ? **Cardiac output**: Echocardiography, thermodilution - good accuracy
- ? **Heart rate**: ECG - perfect accuracy
- ?? **Circulating hormones**: Blood sampling (renin, angiotensin, aldosterone, ADH, ANP) - invasive but feasible
- ?? **Sympathetic activity**: Indirect (heart rate variability, plasma norepinephrine) - moderate accuracy
- ? **Baroreceptor firing rate**: Requires invasive nerve recording - rarely done in humans

**Limitation**: Some components (neural activity, local paracrine signaling) are difficult to observe directly in vivo.

#### **R (Reproducibility)** - Score: 0.80
**Can we reproduce this system experimentally?**
- ? **Cross-species universality**: Mechanism conserved across mammals (human, rat, dog, cat)
- ? **Experimental models**: Extensively studied in animal models (Goldblatt hypertension, DOCA-salt, etc.)
- ? **In silico models**: Guyton's mathematical model (1972) - validated and widely reproduced
- ?? **Individual variability**: Genetics, age, comorbidities create inter-individual differences
- ? **Controlled interventions**: Reproducible responses to drugs (ACE inhibitors, beta-blockers, diuretics)

**Limitation**: Human variability requires large sample sizes for statistical reproducibility.

#### **I (Interoperability)** - Score: 0.90
**How well does this model connect with other systems?**
- ? **Cross-domain integration**: Links cardiovascular + renal + endocrine + neural physiology
- ? **Bidirectional coupling**: Stress ? cortisol ? RAAS; heart failure ? ANP ? ? diuresis
- ? **Translational validity**: Applies to humans, rodents (preclinical models), clinical trials
- ? **Framework compatibility**: Fits homeostasis, cybernetics, systems biology paradigms
- ? **Clinical actionability**: Directly informs antihypertensive drug development

**Strength**: Excellent interoperability - central hub connecting multiple physiological domains.

#### **V (Validity)** - Score: 0.90
**Is this model empirically validated?**
- ? **Empirical foundation**: Decades of research (Guyton, Laragh, Brenner, etc.)
- ? **Quantitative predictions**: Guyton model quantitatively predicts pressure-natriuresis relationship
- ? **Clinical validation**: 
  - ACE inhibitors reduce BP by blocking Ang II formation ?
  - Beta-blockers reduce BP by blocking sympathetic drive ?
  - Diuretics reduce BP by decreasing volemia ?
- ? **Mechanistic understanding**: Molecular targets identified (AT1 receptor, ß1-adrenergic receptor, etc.)
- ? **Pathophysiology explained**: Renovascular hypertension = RAAS activation; heart failure = ANP resistance

**Limitation**: Some details (e.g., tissue RAAS vs circulating RAAS contribution) still under investigation.

#### **E (Expressiveness/Évolutivité)** - Score: 0.75
**Can this model be extended and refined?**
- ? **Extensible**: Can add additional systems (kallikrein-kinin, endothelin, nitric oxide)
- ? **Detail-oriented**: RAAS can be expanded to include Ang(1-7)/Mas receptor axis (counter-regulatory)
- ?? **Complexity explosion**: Adding details creates non-linear interaction challenges
- ? **Pathology modeling**: Applicable to heart failure, chronic kidney disease, diabetes complications
- ? **Therapeutic exploration**: Can model combination therapies (ACE inhibitor + diuretic + beta-blocker)

**Limitation**: High detail leads to parameter explosion - balance needed between completeness and tractability.

---

### ORIVE Global Score

**ORIVE = (O + R + I + V + E) / 5 = (0.85 + 0.80 + 0.90 + 0.90 + 0.75) / 5 = 0.84**

**Interpretation**: **High-quality Map** - Strong empirical grounding, excellent interoperability, well-validated predictions.

---

### Bicephalous Perspective

**Eagle Eye (Territory/ASFID)**: **DOMINANT**
- This poclet is strongly rooted in **observable physiological phenomena**
- Quantitative experimental data abundant (pressure recordings, hormone assays, renal function tests)
- Mathematical models validated (Guyton's differential equations)
- Parameters measurable (volumes, pressures, concentrations, flows)

**Sphinx Eye (Map/ORIVE)**: **STRONG**
- Excellent Map quality (ORIVE = 0.84)
- Clear conceptual model (5 effectors ? 1 controlled variable)
- High predictive power (validated clinically through antihypertensive drugs)

**Epistemic Gap**: ?e ˜ **0.16** (low - excellent Territory-Map alignment)

**Verdict**: **Territory-Dominant Poclet with High-Quality Map**

---

## M2 Metaconcepts Mobilized

This poclet validates **12 M2 metaconcepts**:

### 1. **Homeostasis** (A?S?F) - ? CENTRAL
- **Role**: Core regulatory principle
- **Manifestation**: Multi-effector system maintaining pressure within narrow range
- **Formula**: A?S?F (stable attractor + structural organization + material/energy flows)

### 2. **Balance** (A?S?F) - ? CENTRAL
- **Role**: Equilibrium between opposing forces
- **Manifestation**: 
  - Vasoconstriction (RAAS, Sympathetic, ADH) ? Vasodilation (ANP, Nitric Oxide)
  - Water/sodium retention ? Excretion
- **Formula**: A?S?F (equilibrium state)

### 3. **Regulation** (A?S?F) - ? CENTRAL
- **Role**: Active control mechanisms
- **Manifestation**: Neural (sympathetic), hormonal (RAAS, ADH, ANP), renal (pressure-natriuresis)
- **Formula**: A?S?F (control loops maintaining attractor)

### 4. **Network** (S?I?F)
- **Role**: Distributed architecture
- **Manifestation**: 5 effector systems in parallel, converging on arterial pressure
- **Formula**: S?I?F (structural connectivity + information exchange + flows)

### 5. **Feedback** (A?I?D)
- **Role**: Self-regulation through loops
- **Manifestation**: 
  - Negative feedback: Baroreceptor reflex (?BP ? ?Sympathetic)
  - Negative feedback: ANP release (?Volume ? ?ANP ? ?Excretion)
- **Formula**: A?I?D (attractor stability through information-driven dynamics)

### 6. **Trade-off** (R?V?E / A?I)
- **Role**: Conflicting optimization criteria
- **Manifestation**: 
  - Speed vs Robustness: Sympathetic (fast but unstable) vs Renal (slow but robust)
  - Perfusion vs Pressure: Must maintain pressure without overloading heart
- **Formula**: R?V?E (Map perspective - design choices) / A?I (Territory - constraint)

### 7. **Hierarchy** (S?A)
- **Role**: Levels of control
- **Manifestation**: 
  - **Tier 1**: Neural (baroreceptor reflex) - seconds
  - **Tier 2**: Hormonal (RAAS, ADH) - minutes-hours
  - **Tier 3**: Renal (pressure-natriuresis) - hours-days
- **Formula**: S?A (structural organization with priority ordering)

### 8. **Cascade** (S?I?D)
- **Role**: Sequential signal amplification
- **Manifestation**: RAAS enzymatic cascade
  - Renin (kidney) ? Angiotensinogen ? Angiotensin I ? ACE ? Angiotensin II ? Aldosterone
- **Formula**: S?I?D (structural sequence + information propagation + temporal dynamics)

### 9. **Threshold** (A?I)
- **Role**: Switching behavior at critical values
- **Manifestation**: 
  - Baroreceptor firing threshold (~60-180 mmHg)
  - ANP secretion threshold (atrial stretch)
- **Formula**: A?I (attractor boundary triggering information state change)

### 10. **Dynamics** (D?F)
- **Role**: Temporal evolution
- **Manifestation**: Multi-scale kinetics (fast neural, medium hormonal, slow renal)
- **Formula**: D?F (rate of change coupled to flows)

### 11. **Bifurcation** (?D/?F)
- **Role**: Qualitative state transition
- **Manifestation**: Normotension ? Hypertension (irreversible due to vascular remodeling)
- **Formula**: ?D/?F (critical parameter threshold causing phase transition)

### 12. **Memory** (?(D-F)dt)
- **Role**: System retains past states
- **Manifestation**: 
  - Vascular remodeling (structural memory of chronic pressure elevation)
  - Baroreceptor resetting (adaptation to sustained hypertension)
- **Formula**: ?(D-F)dt (temporal integration of dynamics-flow mismatch)

---

## M1 Concepts Mobilized

### M1_Biology (Existing: `m1:biology:`)
- ? **Paracrine signaling**: Local angiotensin II in kidneys and vessels
- ? **Endocrine signaling**: Circulating aldosterone, ADH, ANP
- ? **Neurotransmission**: Sympathetic norepinephrine release (to be added)
- ? **Receptor-mediated response**: AT1/AT2, V1/V2, NPR-A receptors (to be added)

### M1_Physiology (NEW - Proposed: `m1:physio:`)
- **Baroreflex Arc**: Baroreceptors ? Vasomotor center ? Sympathetic output
- **Renal Autoregulation**: Myogenic mechanism + tubuloglomerular feedback
- **Starling Forces**: Hydrostatic/osmotic balance in capillary exchange
- **Cardiac Output**: CO = HR × SV (Heart Rate × Stroke Volume)
- **Pressure-Natriuresis**: Kidney's intrinsic pressure-dependent sodium excretion

### M1_Pharmacology (NEW - Proposed: `m1:pharma:`)
- **Enzyme Inhibition**: ACE inhibitors (captopril, enalapril), renin inhibitors (aliskiren)
- **Receptor Blockade**: AT1 antagonists (losartan), beta-blockers (metoprolol)
- **Diuretic Action**: Loop diuretics (furosemide), thiazides (hydrochlorothiazide)
- **Dose-Response Curves**: Sigmoidal relationships for antihypertensive drugs

---

## Gamification Potential

### Score: ????? (5/5)

### Game Mode 1: "Physiologist"
**Objective**: Maintain blood pressure at 120/80 mmHg for 24 simulated hours

**Mechanics**:
- **Baseline state**: Normal physiology at rest
- **Random perturbations**: 
  - Stress event (? sympathetic) every 2-4 hours
  - Exercise bout (? cardiac output, ? sympathetic)
  - Dehydration (? volemia)
  - High sodium meal (? volemia after 1-2 hours)
- **Player controls**: 5 sliders to modulate each effector system (0-200%)
  - RAAS activity
  - Sympathetic tone
  - ADH secretion
  - ANP release
  - Renal excretion rate
- **Feedback**: Real-time pressure graph, color-coded zones (green = 110-130, yellow = 90-110 or 130-150, red = <90 or >150)
- **Scoring**: 
  - +10 points/minute in green zone
  - -5 points/minute in yellow zone
  - -20 points/minute in red zone
  - Bonus: Minimize effector interventions (efficiency)

**Learning objectives**:
- Understand multi-scale dynamics (fast sympathetic vs slow renal)
- Recognize trade-offs (sympathetic gives fast response but causes oscillations)
- Appreciate redundancy (multiple pathways to same goal)

---

### Game Mode 2: "Clinician"
**Objective**: Treat a hypertensive patient (BP = 160/100) with minimal side effects

**Mechanics**:
- **Patient profile**: Age, comorbidities (diabetes, kidney disease, heart failure)
- **Available drugs**:
  - ACE inhibitor (blocks RAAS)
  - Beta-blocker (blocks sympathetic)
  - Diuretic (enhances renal excretion)
  - Calcium channel blocker (vasodilation)
- **Constraints**:
  - Each drug has side effects (e.g., ACE inhibitor ? hyperkalemia risk if kidney disease)
  - Must avoid hypotension (<90/60)
  - Budget limit (drugs have different costs)
- **Progression**: Treat over simulated weeks, titrate doses
- **Scoring**: 
  - Target achieved: BP normalized (<140/90)
  - Side effects minimized
  - Cost-effectiveness

**Learning objectives**:
- Understand drug mechanisms (which effector each targets)
- Recognize contraindications (beta-blocker in heart failure)
- Appreciate combination therapy (synergistic effects)

---

### Game Mode 3: "Pathology Explorer"
**Objective**: Investigate how specific lesions lead to hypertension

**Scenarios**:
1. **Renal artery stenosis**: Reduced perfusion ? ? Renin ? ? RAAS ? Hypertension
2. **Heart failure**: ? Cardiac output ? Compensatory ? RAAS + ? Sympathetic ? Volume overload
3. **Cushing's syndrome**: ? Cortisol ? Mineralocorticoid receptor activation ? Sodium retention
4. **Pheochromocytoma**: Catecholamine-secreting tumor ? ?? Sympathetic ? Severe hypertension

**Mechanics**:
- **Induce lesion**: Player selects pathology
- **Observe cascade**: System shows step-by-step how lesion propagates (e.g., stenosis ? ? renal perfusion ? juxtaglomerular cells detect ? ? renin release ? etc.)
- **Intervene**: Player chooses treatment to break cascade
- **Validation**: Correct diagnosis and treatment = success

**Learning objectives**:
- Understand pathophysiology (why hypertension develops)
- Identify root cause vs downstream effects
- Apply targeted therapy (e.g., ACE inhibitor for renovascular hypertension)

---

### Game Mode 4: "Research Lab"
**Objective**: Perform virtual experiments to test hypotheses

**Examples**:
1. **"Is RAAS necessary for hypertension?"**
   - Experiment: Block RAAS completely (ACE inhibitor + AT1 blocker)
   - Prediction: If yes ? BP normalizes; If no ? BP remains high
   - Validation: Compare to real-world data (RAAS blockade does reduce BP, but not always to normal)

2. **"What happens if we remove baroreceptor reflex?"**
   - Experiment: Simulate baroreceptor denervation
   - Prediction: Loss of short-term buffering ? Increased BP variability
   - Validation: Matches animal studies (baroreceptor denervation ? labile hypertension)

3. **"Can ANP alone control pressure?"**
   - Experiment: Disable RAAS + Sympathetic, rely only on ANP
   - Prediction: Inadequate compensation ? Persistent hypertension or hypotension instability
   - Validation: ANP is counter-regulatory, not primary controller

**Learning objectives**:
- Scientific method (hypothesis ? experiment ? conclusion)
- Systems thinking (removing one component affects others)
- Historical context (reproduce classic studies like Guyton's experiments)

---

## Implementation Recommendations

### Step 1: Validate Mathematical Model
Use **Guyton's model** (1972) as foundation:
- Differential equations for renal function (pressure-natriuresis curve)
- Cardiac output regulation (Starling curve)
- RAAS dynamics (renin secretion kinetics)

**Key equations**:
```
dVolume/dt = Intake - Excretion(Pressure, RAAS, ADH, ANP)
dPressure/dt = f(CardiacOutput, TotalPeripheralResistance, Volume)
dRAAS/dt = g(RenalPerfusion, AngII_feedback)
```

**Numerical solver**: Runge-Kutta 4th order for stiff ODEs

---

### Step 2: Create M1_Physiology.jsonld
Define reusable physiological patterns:
- `m1:physio:BaroreflexArc`
- `m1:physio:PressureNatriuresis`
- `m1:physio:CardiacOutputRegulation`
- `m1:physio:StarlingForces`

---

### Step 3: Prototype UI
**Minimal viable product**:
- **Graph**: Real-time blood pressure (systolic/diastolic)
- **Controls**: 5 sliders for effector systems
- **Events**: Random perturbations (stress, exercise)
- **Feedback**: Color-coded zones, score display

**Technology stack** (suggested):
- Frontend: React.js (for interactive graph)
- Visualization: D3.js or Plotly
- Simulation: JavaScript (ODE solver library like `numeric.js`)

---

### Step 4: Extend to Other Modes
Once Mode 1 ("Physiologist") is functional:
- Add drug database for Mode 2 ("Clinician")
- Add pathology scenarios for Mode 3 ("Pathology Explorer")
- Add experimental protocols for Mode 4 ("Research Lab")

---

## Scientific References

1. **Guyton, A.C. (1972)**. "Arterial Pressure and Hypertension". *W.B. Saunders*. Philadelphia.
   - **Key contribution**: Quantitative model of long-term BP regulation (pressure-natriuresis curve)

2. **Laragh, J.H. (1985)**. "The renin system and four lines of hypertension research". *Hypertension* 7(3):299-303.
   - **Key contribution**: RAAS central role in hypertension pathophysiology

3. **Cowley, A.W. (1992)**. "Long-term control of arterial blood pressure". *Physiol Rev* 72(1):231-300.
   - **Key contribution**: Integration of neural, hormonal, and renal mechanisms

4. **DiBona, G.F. & Kopp, U.C. (1997)**. "Neural control of renal function". *Physiol Rev* 77(1):75-197.
   - **Key contribution**: Sympathetic regulation of kidney function

5. **Brenner, B.M. et al. (1988)**. "Diverse biological actions of atrial natriuretic peptide". *Physiol Rev* 68(3):665-699.
   - **Key contribution**: Counter-regulatory role of natriuretic peptides

6. **Hall, J.E. et al. (2012)**. "Obesity-induced hypertension: interaction of neurohumoral and renal mechanisms". *Circ Res* 111(7):962-973.
   - **Key contribution**: Modern understanding of pathophysiology

---

## Clinical Relevance

### Prevalence
- **Hypertension affects ~30-40% of adults worldwide** (WHO, 2021)
- Leading risk factor for cardiovascular disease, stroke, kidney failure

### Therapeutic Targets
This poclet's 5 effector systems map directly to **5 drug classes**:

| Effector | Drug Class | Example | Mechanism |
|----------|-----------|---------|-----------|
| **RAAS** | ACE inhibitors | Enalapril | Block Ang I ? Ang II conversion |
| **RAAS** | AT1 blockers | Losartan | Block Ang II receptor |
| **Sympathetic** | Beta-blockers | Metoprolol | Block ß1-adrenergic receptors |
| **Sympathetic** | Alpha-blockers | Doxazosin | Block a1-adrenergic receptors |
| **Renal Excretion** | Diuretics | Hydrochlorothiazide | ? Sodium/water excretion |
| **Vascular Tone** | Calcium channel blockers | Amlodipine | Vasodilation (not modeled as separate effector) |

**Combination therapy** is common (e.g., ACE inhibitor + diuretic) - reflects system redundancy.

---

## Future Extensions

### 1. Add Endothelial Regulation
- **Nitric Oxide (NO)**: Vasodilator produced by endothelium
- **Endothelin**: Vasoconstrictor peptide
- Creates 6th and 7th effector systems

### 2. Model Circadian Variation
- Blood pressure follows 24-hour rhythm (dipping at night)
- Integrate circadian clock ? sympathetic/RAAS modulation

### 3. Include Genetic Factors
- Polymorphisms in renin, ACE, angiotensinogen genes affect hypertension risk
- Add patient genetic profile as parameter

### 4. Link to Chronic Kidney Disease
- Hypertension ? kidney disease (bidirectional causality)
- Model progression: Hypertension ? glomerular damage ? ? GFR ? ? RAAS ? worsening hypertension

### 5. Integrate with Other Poclets
- **Cardiac Output** could become standalone poclet (Starling curve, contractility)
- **Renin-Angiotensin Cascade** as detailed sub-poclet
- **Baroreceptor Reflex** as neural control poclet

---

## Conclusion

The **Blood Pressure Control poclet** is a **high-priority addition** to the TSCG portfolio:

? **Complete ASFID** - All 5 dimensions robustly present  
? **High ORIVE (0.84)** - Excellent Map quality, well-validated  
? **12 M2 metaconcepts** - Rich theoretical validation  
? **Clinical relevance** - Hypertension = major public health issue  
? **Pedagogical value** - Complex system, clear conceptual structure  
? **Maximal gamifiability** - 4 game modes with deep learning potential  

**Epistemic gap ?e = 0.16** - Strong Territory-Map alignment

This poclet would be the **first physiological system** in the TSCG framework and the **first with 5 effectors** (vs 3-4 in existing poclets), pushing the boundaries of multi-component modeling.

**Next steps**:
1. Create `M1_Physiology.jsonld`
2. Implement Guyton model equations
3. Develop "Physiologist" game mode prototype
4. Validate with medical educators

---

**Document Version**: 1.0.0  
**Date**: January 22, 2026  
**Framework**: TSCG (Transdisciplinary System Construction Game)  
**Namespace**: `m0:blood_pressure_control:`  
**Location**: `ontology/poclets/blood_pressure_control/M0_BloodPressureControl_README.md`