# TSCG Framework - Update v11.0.0 → v12.0.0

**Date**: January 21, 2026  
**Version M2**: 11.0.0 → **12.0.0** ✅  
**New GenericConcepts**: +3 (Layer, Switch, Mode)  
**Status**: Ready for integration ✅

---

## 📊 Main Changes

### M2 GenericConcepts Ontology

**Before (v11.0.0)**:
- Total: 55 GenericConcepts
- Territory: 29
- Map: 8
- Dual: 18

**After (v12.0.0)**:
- Total: **58 GenericConcepts** (+3)
- Territory: **30** (+1: Layer)
- Map: 8 (unchanged)
- Dual: **20** (+2: Switch, Mode)

### Distribution by Category

**Structural**: 12 → **13** (+1: Layer)
**Regulatory**: 10 → **11** (+1: Switch)
**Ontological**: 7 → **8** (+1: Mode)
**Other categories**: unchanged

---

## 🆕 New GenericConcept 1: **Layer**

### Identity
- **ID**: `m2:Layer`
- **Perspective**: Territory (Observable)
- **Category**: Structural
- **Tensor Formula**: **S⊗I⊗A**
- **Polarity**: Neutral

### Definition
Stratified organization where system components are arranged in distinct, stacked levels with hierarchical dependencies and sequential processing.

### ASFID Decomposition
```
|Layer⟩ = 0.85|S⟩ + 0.75|I⟩ + 0.70|A⟩ + 0.30|F⟩ + 0.20|D⟩
```

### Distinction from Existing GenericConcepts

| GenericConcept | Difference |
|-------------|------------|
| **Hierarchy** | Layer = HORIZONTAL stratification (stacked); Hierarchy = VERTICAL ordering (tree) |
| **Imbrication** | Layer = STACKING (adjacency); Imbrication = NESTING (containment) |
| **Modularity** | Layer = spatial stratification; Modularity = functional decomposition |
| **Network** | Layer = sequential linear stack; Network = arbitrary graph topology |

### Transdisciplinary Validation
✅ **8 domains validated**:
1. Networking (OSI Model: 7 layers Physical → Application)
2. Computing (Software Stack: Hardware → OS → Middleware → App)
3. Geology (Rock strata)
4. Biology (Skin layers: Epidermis → Dermis → Hypodermis)
5. Optics (Anti-reflective coating: thin-film layers)
6. Atmosphere (Troposphere → Stratosphere → Mesosphere → Thermosphere → Exosphere)
7. Deep Learning (Input → Hidden → Output layers)
8. Architecture (Building floors)

### Key Property
**Sequential dependency**: Each layer depends on layer(s) below, information flows vertically through stack.

---

## 🆕 New GenericConcept 2: **Switch**

### Identity
- **ID**: `m2:Switch`
- **Perspective**: Dual (Territory: physical switches; Map: logical transitions)
- **Category**: Regulatory
- **Tensor Formula**: **A⊗D⊗I**
- **Polarity**: Neutral

### Definition
Mechanism enabling discrete state transition between operational modes (binary or **N-ary**), triggered by control signal or threshold crossing. Operates over finite discrete state set {S₁, S₂, ..., Sₙ}.

### CRITICAL: N-ary Nature
**Switch is NOT inherently binary**:
- **Binary Switch** (N=2): ON/OFF, Open/Closed - special case
- **Ternary Switch** (N=3): Low/Medium/High
- **N-ary Switch** (N>2): Multi-position selector

**General Definition**:
```
Switch = (S, τ, C)
where:
  S = {s₁, s₂, ..., sₙ} - Finite state set
  τ: S × C → S - Transition function
  C - Control signal/trigger set
```

**Binary is special case where |S| = 2, NOT the defining property.**

### ASFID Decomposition
```
|Switch⟩ = 0.80|A⟩ + 0.75|D⟩ + 0.70|I⟩ + 0.40|S⟩ + 0.30|F⟩
```

### Distinction from Existing GenericConcepts

| GenericConcept | Difference |
|-------------|------------|
| **Bifurcation** | Bifurcation = CONTINUOUS parameter change; Switch = DISCRETE triggered transition |
| **Threshold** | Threshold = CRITICAL VALUE; Switch = MECHANISM using threshold |
| **Trigger** | Switch is SPECIFIC type of trigger (discrete multi-state with explicit mechanism) |
| **Activation** | Activation = binary enable/disable; Switch = generalized N-ary selection |
| **Mode** | Mode = STATES themselves; Switch = TRANSITION MECHANISM between modes |

### Transdisciplinary Validation
✅ **10 domains validated** (with N-ary breakdown):

**Binary Examples (N=2)**:
1. Electronics: Transistor (ON/OFF)
2. Biology: Simple ion channels (Open/Closed)

**N-ary Examples (N>2)**:
3. **Home Appliances**: Washing machine (N=8-12 cycles)
4. **Photography**: Camera mode dial (N=6: Auto, Manual, Aperture-P, Shutter-P, Scene modes)
5. **Transportation**: Car transmission (N=5-8: P, R, N, D, L, 2, 1)
6. **Audio**: Guitar pickup selector (N=3-5: Neck, Middle, Bridge)
7. **HVAC**: Thermostat (N=4: Off, Heat, Cool, Auto)
8. **Optics**: Filter wheel (N=6-12 color filters)
9. Computing: Process scheduler (N processes)
10. Neuroscience: Neural firing modes (Tonic, Burst, Silent)

**N-ary Examples Count**: 7/10 examples are N-ary (N>2) ✅

### Key Property
**Discrete state transition** over finite set with explicit control mechanism. N-ary generalization is fundamental, binary is merely common special case.

---

## 🆕 New GenericConcept 3: **Mode**

### Identity
- **ID**: `m2:Mode`
- **Perspective**: Dual (Territory: physical modes; Map: conceptual states)
- **Category**: Ontological
- **Tensor Formula**: **S⊗I⊗A**
- **Polarity**: Neutral

### Definition
Discrete operational state or configuration determining system behavior, persistent until switched. Defines qualitative behavioral category with distinct response patterns, not just different parameter values.

### ASFID Decomposition
```
|Mode⟩ = 0.80|S⟩ + 0.75|I⟩ + 0.75|A⟩ + 0.40|F⟩ + 0.30|D⟩
```

### Distinction from Existing GenericConcepts

| GenericConcept | Difference |
|-------------|------------|
| **State** | Mode = QUALITATIVE class; State = QUANTITATIVE point in continuous space |
| **Configuration** | Mode = BEHAVIORAL difference; Configuration = PARAMETER settings |
| **Phase** | Phase = continuous region; Mode = discrete category |
| **Attractor** (M3) | Attractor = convergence tendency; Mode = discrete basin identity |

### Transdisciplinary Validation
✅ **8 domains validated**:

1. **Photography**: Auto, Manual, Aperture Priority, Shutter Priority, Scene modes
2. **Biology**: Aerobic respiration, Anaerobic respiration
3. **Computing**: User mode, Kernel mode, Supervisor mode
4. **Transportation**: Park, Reverse, Neutral, Drive, Low (transmission)
5. **Communication**: Listen, Connect, Transmit, Disconnect (protocol states)
6. **Audio**: Standby, Active, Muted (amplifier)
7. **Optics**: Continuous Wave, Pulsed, Q-switched (laser)
8. **Fire Science**: Smoldering, Flaming, Explosive (combustion)

### Relationship to Switch
**Complementary pair**:
- **Mode** = What the system IS (states)
- **Switch** = How it CHANGES state (transitions)

Example: Camera has Modes (Auto, Manual, etc.), Mode Dial is the Switch transitioning between them.

---

## 🔗 Triad Coherence: Layer ↔ Switch ↔ Mode

### Conceptual Relationships

```
┌─────────────────────────────────────────────────┐
│                    LAYER                        │
│   (Spatial/Organizational Stratification)      │
│                                                 │
│  Layer 3: Application Logic                    │
│  Layer 2: Business Rules     ← MODE 2         │
│  Layer 1: Data Access        ← MODE 1         │
│                                    ↑            │
│                                 SWITCH          │
│                            (Transition between  │
│                             modes in layer)     │
└─────────────────────────────────────────────────┘
```

### Triad Properties

1. **Layer** provides SPATIAL organization (stacked levels)
2. **Mode** provides BEHAVIORAL states (discrete operational categories)
3. **Switch** provides TRANSITION mechanism (changes between modes)

### Example: Camera System

**Layers**:
```
Layer 4: User Interface (Menu, Display)
Layer 3: Shooting Logic (Exposure calculation)
Layer 2: Sensor Control (ISO, Duration, Aperture)
Layer 1: Hardware (Sensor, Shutter, Aperture mechanism)
```

**Modes** (at Layer 3 - Shooting Logic):
```
Mode 1: Manual      (User controls ISO, Aperture, Shutter)
Mode 2: Auto        (Camera controls all)
Mode 3: Aperture-P  (User: Aperture; Camera: Shutter, ISO)
Mode 4: Shutter-P   (User: Shutter; Camera: Aperture, ISO)
Mode 5: Scene       (Pre-programmed combinations)
```

**Switch** (Mode Selector):
```
Rotary dial or menu: Mode_i → Mode_j
User input triggers transition between 5 modes
```

### Formal Relationship

```
System = ⋃(Layers)
Each Layer_i can have Modes = {M₁, M₂, ..., Mₙ}
Switch: Mᵢ → Mⱼ (state transition within or across layers)
```

---

## 📊 Impact on M2 Structure

### Before v12.0.0
- **Total**: 55 GenericConcepts
- **Structural**: 12
- **Regulatory**: 10
- **Ontological**: 7

### After v12.0.0
- **Total**: **58 GenericConcepts** (+3, +5.5%)
- **Structural**: **13** (+Layer)
- **Regulatory**: **11** (+Switch)
- **Ontological**: **8** (+Mode)

### Bicephalous Distribution

| Perspective | Before | After | Change |
|-------------|--------|-------|--------|
| Territory   | 29     | 30    | +1 (Layer) |
| Map         | 8      | 8     | 0 |
| Dual        | 18     | 20    | +2 (Switch, Mode) |

---

## ✅ Validation Summary

### Layer
- [x] Transdisciplinary validation (8 domains)
- [x] Tensor formula justified (S⊗I⊗A)
- [x] Distinct from Hierarchy, Imbrication, Modularity, Network
- [x] Category assigned (Structural)
- [x] Perspective classified (Territory)

### Switch
- [x] Transdisciplinary validation (10 domains)
- [x] Tensor formula justified (A⊗D⊗I)
- [x] **N-ary nature emphasized** (binary is special case)
- [x] 7/10 examples are N-ary (N>2)
- [x] Distinct from Bifurcation, Threshold, Trigger, Activation
- [x] Category assigned (Regulatory)
- [x] Perspective classified (Dual)

### Mode
- [x] Transdisciplinary validation (8 domains)
- [x] Tensor formula justified (S⊗I⊗A)
- [x] Distinct from State, Configuration, Phase
- [x] Category assigned (Ontological)
- [x] Perspective classified (Dual)
- [x] Relationship to Switch clarified (complementary)

---

## 📚 Key Insights

### 1. Switch N-ary Generalization
**Critical correction**: Switch was initially conceived as binary (ON/OFF), but analysis reveals:
- **Binary is special case** (N=2)
- **N-ary is general form** (N ≥ 2)
- **Most real-world switches are N-ary**: washing machines (8 cycles), cameras (6 modes), transmissions (5-8 gears)

This generalization significantly strengthens the GenericConcept's transdisciplinary applicability.

### 2. Cohesive Triad Pattern
Layer, Switch, and Mode form a **coherent organizational triad**:
- **Layer**: Spatial stratification (WHERE organization happens)
- **Mode**: Behavioral states (WHAT the system does)
- **Switch**: Transition mechanism (HOW the system changes)

This triad captures fundamental patterns in structured systems across domains.

### 3. Complementarity: Switch ↔ Mode
Strong complementarity between Switch and Mode:
- **Mode without Switch**: Static, unchangeable states
- **Switch without Mode**: Transitions with no destination
- **Both together**: Complete state management pattern

Example validation: Camera systems, washing machines, transmissions all exhibit both GenericConcepts.

---

## 🎯 Recommendations

### Integration Priority

1. ✅ **HIGH PRIORITY**: Switch and Mode (strongly coupled, implement together)
2. ✅ **MEDIUM PRIORITY**: Layer (independent, can be added separately)

### Suggested Documentation Updates

1. Update M2 README to reflect 58 GenericConcepts
2. Add "Structured State Management" section showcasing Layer-Switch-Mode triad
3. Emphasize N-ary nature of Switch in all documentation
4. Create visual diagrams showing triad relationships

### Future Work

1. **Validate triad** in additional poclets (beyond Exposure Triangle, Camera systems)
2. **M1 Patterns**: Create domain-specific instantiations
   - M1_Networking: OSI Layers with protocol modes
   - M1_Computing: Software stack with execution modes
3. **Cross-validate** N-ary Switch across more domains (>15 domains target)

---

## 📁 Deliverables

### 1. **M2_GenericConcepts_v12.jsonld** (Complete)
Updated ontology with:
- 58 GenericConcepts (55→58)
- Layer, Switch, Mode definitions
- Full ASFID/ORIVE characterizations
- Transdisciplinary validation
- Changelog v12.0.0

### 2. **M2_Candidates_Analysis_Layer_Switch_Mode.md**
Detailed analysis document with:
- Individual GenericConcept analysis
- Transdisciplinary validation tables
- Distinction from existing GenericConcepts
- JSON-LD skeletons
- Triad coherence explanation

### 3. **TSCG_Update_v12_Summary.md** (this document)
Executive summary of v12.0.0 update

---

## ✨ Conclusion

**APPROVAL**: ✅ All three GenericConcepts (Layer, Switch, Mode) validated and integrated into M2 v12.0.0

**Key Achievements**:
1. ✅ Expanded M2 by 5.5% (55→58 GenericConcepts)
2. ✅ Filled genuine gaps in Structural, Regulatory, and Ontological categories
3. ✅ Discovered cohesive triad pattern (Layer ↔ Switch ↔ Mode)
4. ✅ **Corrected Switch to N-ary** (not binary-only)
5. ✅ Strong transdisciplinary validation (8-10 domains each)

**Framework Maturity**: ⭐⭐⭐⭐⭐ (5/5)
- M2 now captures structured state management patterns
- Triad provides powerful organizational vocabulary
- N-ary Switch enables modeling of complex multi-state systems

**Impact**:
- Immediate: Better modeling of layered systems, mode-based architectures, multi-state controllers
- Long-term: Foundation for M1 domain extensions, poclet analysis enhancements

---

**END OF UPDATE SUMMARY**

**Version**: 12.0.0  
**Date**: 2026-01-21  
**Status**: ✅ Validated and Integrated  
**Next**: Apply to additional poclets, develop M1 patterns 🚀
