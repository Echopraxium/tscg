# TSCG M0 Migration Report — v1.5.0

**Date:** 2026-06-20 16:24:11
**Summary:** ✅ 33 success  ❌ 0 failed  📊 33 total

---

## Changes applied

- `m0:` → `M0_Common.jsonld#` (shared canonical)
- `m0.<instance>:` added (local namespace)
- `m1.extensions.<domain>:` (canonical dot-separated)
- Obsolete score aliases removed (A_score...)
- `owl:imports M0_Common.jsonld` added
- Score values → bare numerics
- Enum values → IRI objects (`{@id: m0:spectralClass.Coherent}`)
- `m2:hasTensorFormula` → `m2:hasStructuralGrammarFormula`
- `m3:ontologyType` removed from sub-nodes
- `m2:changelog` truncated to 3 entries

---

## Detailed Results

### AdaptativeImmuneResponse (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### BloodPressureControl (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### ButterflyMetamorphosis (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### CellSignalingModes (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.cellSignalingModes:
- @context: Removed legacy entry 'm0:cell_signaling_modes'
- @context: m1.ext:biology → m1.extensions.biology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld#
- @context: Removed obsolete alias 'sm'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### ColorSynthesis (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.colorSynthesis:
- @context: Removed legacy entry 'm0:color_synthesis'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld

### ComplexChemicalSynapse (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- Complex Chemical Synapse Poclet - TSCG M0 Layer: Flattened m0:revoiScores{} → I
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.complexChemicalSynapse:
- @context: Removed legacy entry 'm0:synapse'
- @context: m1.ext:biology → m1.extensions.biology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld

### CounterPoint (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.counterPoint:
- @context: Removed legacy entry 'm1core'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent [0, 0.05)}

### ExposureTriangle (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.exposureTriangle:
- @context: Removed legacy entry 'm0:exposure-triangle'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### FireTriangle (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.fireTriangle:
- @context: Removed legacy entry 'm0:fire-triangle'
- @context: Removed legacy entry 'm0:epistemicGap'
- @context: Removed legacy entry 'm0:mean'
- @context: Removed legacy entry 'eagle_eye:Attractor'
- @context: Removed legacy entry 'eagle_eye:Structure'
- @context: Removed legacy entry 'eagle_eye:Flow'
- @context: Removed legacy entry 'eagle_eye:Information'
- @context: Removed legacy entry 'eagle_eye:Dynamics'
- @context: Removed legacy entry 'sphinx_eye:Representable'
- @context: Removed legacy entry 'sphinx_eye:Evolvable'
- @context: Removed legacy entry 'sphinx_eye:Verifiable'
- @context: Removed legacy entry 'sphinx_eye:Observable'
- @context: Removed legacy entry 'sphinx_eye:Interoperable'
- @context: m1.ext:chemistry → m1.extensions.chemistry: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### FourStrokeEngine (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.fourStrokeEngine:
- @context: Removed legacy entry 'm1core'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld

### Kidneys (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.kidneys:
- @context: m1bio → m1.extensions.biology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'sm'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- @context: Added missing rdf:
- owl:imports: Added M0_Common.jsonld

### KindlebergerMinsky (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.kindlebergerMinsky:
- @context: Removed legacy entry 'm1core'
- @context: m1econ → m1.extensions.economics: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- @context: Added missing rdf:
- owl:imports: Added M0_Common.jsonld

### MtgColorWheel (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.mtgColorWheel:
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld

### NakamotoConsensus (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- Nakamoto Consensus as Dissipative Structure — Phenomenological Statistical-Physics Framework: Flattened m0:territorySpace.asfidScores{} → A, S, F, I, D
- Nakamoto Consensus as Dissipative Structure — Phenomenological Statistical-Physics Framework: Flattened m0:mapSpace.revoiScores{} → R, E, V, O, I
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.nakamotoConsensus:
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- @context: Added missing rdf:
- @context: Added missing skos:
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### NuclearReactorsTypology (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.nuclearReactorsTypology:
- @context: Removed legacy entry 'm1core'
- @context: m1energy → m1.extensions.energy-generators: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/energy-generators/M1_EnergyGenerators.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'sm'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- Key rename: m1energy:moderatorType → m1.extensions.energy-generators:moderatorType
- Key rename: m1energy:coolantType → m1.extensions.energy-generators:coolantType
- Key rename: m1energy:neutronSpectrum → m1.extensions.energy-generators:neutronSpectrum
- Key rename: m1energy:fuelEnrichment → m1.extensions.energy-generators:fuelEnrichment
- Key rename: m1energy:criticalityControl → m1.extensions.energy-generators:criticalityControl
- Key rename: m1energy:thermalEfficiency → m1.extensions.energy-generators:thermalEfficiency
- Key rename: m1energy:typicalPower → m1.extensions.energy-generators:typicalPower
- @context: Added missing rdf:
- owl:imports: Added M0_Common.jsonld
- Removed m3:ontologyType from sub-node: Enneagram Connections Between Reactor Types
- Removed m3:ontologyType from sub-node: Nuclear Reactor Typology Poclet - Summary

### PhaseTransition (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.phaseTransition:
- @context: Removed legacy entry 'm1core'
- @context: m1chem → m1.extensions.chemistry: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld#
- @context: m1phys → m1.extensions.physics: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'sm'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- Key rename: m1phys:concept → m1.extensions.physics:concept
- Key rename: m1phys:concept → m1.extensions.physics:concept
- owl:imports: Added M0_Common.jsonld

### PlateTectonics (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.plateTectonics:
- @context: Removed legacy entry 'm1core'
- @context: m1geo → m1.extensions.geology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/geology/M1_Geology.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld

### Ptoe (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.ptoe:
- @context: m1.ext:chemistry → m1.extensions.chemistry: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld

### Raas (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.raas:
- @context: m1bio → m1.extensions.biology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'sm'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- @context: Added missing rdf:
- owl:imports: Added M0_Common.jsonld

### Tpack (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.tpack:
- @context: Removed legacy entry 'm0:tpack'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### Transistor (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.transistor:
- @context: m1elec → m1.extensions.electronics: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- @context: Added missing rdf:
- owl:imports: Added M0_Common.jsonld

### TrophicPyramid (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.trophicPyramid:
- @context: Removed legacy entry 'm1core'
- @context: m1bio → m1.extensions.biology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld

### TvTestPattern (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- Analogue TV Test Pattern (Mire): Flattened m0:revoiScores{} → I
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.tvTestPattern:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: m1.ext:electronics → m1.extensions.electronics: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld

### Vco (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.vco:
- @context: Removed legacy entry 'm1core'
- @context: m1elec → m1.extensions.electronics: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- Key rename: m1core:simulationTitle → m1:simulationTitle
- owl:imports: Added M0_Common.jsonld

### Yggdrasil (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.yggdrasil:
- @context: Removed legacy entry 'm0:yggdrasil'
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: m1.ext:mythology → m1.extensions.mythology: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology.jsonld#
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'sm'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld

### Triz (systemic_framework)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.triz:
- @context: Removed legacy alias m0triz:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.OnCriticalLine}

### Vsm (systemic_framework)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.vsm:
- @context: Removed legacy alias m0vsm:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

### Iching (symbolic_grammar)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.iching:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

### TriskeleToolchain (symbolic_grammar)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.triskeleToolchain:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

### TscgOntologyAPIServer (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.tscgOntologyAPIServer:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

### TscgOntologyExplorer (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.tscgOntologyExplorer:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

### TscgPocletGenerator (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.tscgPocletGenerator:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

### TscgPocletMiner (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: → M0_Common.jsonld# (shared canonical)
- @context: Added m0.tscgPocletMiner:
- @context: Removed legacy entry 'm3:eagle_eye'
- @context: Removed legacy entry 'm3:sphinx_eye'
- @context: Removed obsolete alias 'D_score'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 3 score(s) converted
- Enum IRI: m0:spectralClass → {@id: m0:spectralClass.Coherent}

