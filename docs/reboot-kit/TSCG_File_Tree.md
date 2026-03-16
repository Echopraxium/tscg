# 📁 TSCG Framework - Complete File Tree

**Date:** 2026-03-16  
**Framework Version:** TSCG v15.10.0  
**Total Files:** 593

---

## 📊 Project Statistics

**Ontology Files:**
- M3 Layer: 4 files (M3_EagleEye, M3_GenesisSpace, M3_GenesisSpace_Ref, M3_SphinxEye; .ttl only for Ref and SphinxEye)
- M2 Layer: 1 main file (M2_GenericConcepts) + 1 standalone (M2_Calibration) + archived versions in docs/
- M1 Layer: 1 core file + 10 domain extensions (biology, chemistry, **economics**, education, electronics, energy_generators, mythology, optics, photography, physics)
- M0 Layer: 21 poclets (instances/poclets/) + TSCG Tools (instances/tscg-tools/) + 1 VSM systemic framework + 1 symbolic grammar

**Documentation:** ~120 files  
**Source Code:** extensive `src/tscg/` Python package  
**Scripts & Tools:** 30+ files  
**Root & Config:** 9 files

**Total:** 593 files

---

## 🆕 What's New (vs v15.9.0)

### v15.10.0 (2026-03-16) — Current
- ✅ New poclet: `TrophicPyramid/` (M0_TrophicPyramid.jsonld + README + sim/)
- ✅ New poclet: `TvTestPattern/` (M0_TVTestPattern.jsonld + README + tv_test_pattern_sim.py)
- ✅ New TSCG tool: `TscgPocletGenerator/` (M0_TscgPocletGenerator.jsonld + tscg_poclet_generator.py + tscg_rag_augmentor.py)
- ✅ New TSCG tool stub: `TscgPocletExplorer/` (00_Run.bat)
- ✅ New standalone M2 file: `ontology/M2_Calibration.jsonld`
- ✅ Smart Prompt v15.9.0 added to reboot-kit
- ✅ `M2_GenericConcepts.jsonld` and `M2_FormulasReference_v15.10.0.md` added to reboot-kit

### v15.9.0 (2026-03-01)
- ✅ New M1 extension: `economics/` (M1_Economics.jsonld + M1_Economics_README.md)
- ✅ New poclet: `KindlebergerMinsky/` (M0_KindlebergerMinsky + simulation)
- ✅ New section: `instances/tscg-tools/TscgExplorer/` (M0_TscgExplorer + tscg_explorer.py)
- ❌ `instances/validation/` directory removed (validated poclets now live only in `poclets/`)
- ❌ `.ttl` twins removed for `M3_EagleEye` and `M3_GenesisSpace` in `ontology/`
- ❌ `.ttl` twins removed for several poclets (ColorSynthesis, ComplexChemicalSynapse, Tpack, Vco, PhaseTransition, MtgColorWheel)

### v15.8.0 (2026-02-27)
- Smart Prompt v15.8.0 released
- New M1 extensions: `education/`, `physics/`, `electronics/` (VCO domain)
- New poclets: `PhaseTransition/` (simulation) + `Vco/` (first m2:Oscillator instantiation)
- `M1_Electronics.jsonld` — 17 concepts covering analog electronics & modular synthesis
- Preprints reorganized with `previous/` subfolder; v3 is now current

---

## 🏛️ M3 Layer - Genesis Space

Core foundation defining the bicephalous architecture (Territory/Map distinction).

### Main ontology/
- [M3_EagleEye.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_EagleEye.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_EagleEye.ttl) - Territory perspective (ASFID dimensions)
- [M3_GenesisSpace.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld) - Foundational ontology
- [M3_GenesisSpace_Ref.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisSpace_Ref.ttl) - Reference copy (TTL only in root ontology/)
- [M3_SphinxEye.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_SphinxEye.ttl) - Map perspective (REVOI dimensions)

### ontology/Ref/ (reference copies)
- [M2_GenericConcepts_2026_02_17_17h-00min.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M2_GenericConcepts_2026_02_17_17h-00min.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M2_GenericConcepts_2026_02_17_17h-00min.ttl)
- [M2_MetaConcepts_Ref.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M2_MetaConcepts_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M2_MetaConcepts_Ref.ttl)
- [M3_GenesisSpace_Ref.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M3_GenesisSpace_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M3_GenesisSpace_Ref.ttl)

---

## 🌐 M2 Layer - Universal GenericConcepts

### Main ontology/ files
- [M2_GenericConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld) - Generic/universal metaconcepts *(primary)*
- [M2_Calibration.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M2_Calibration.jsonld) - Calibration standalone metaconcept — **NEW**

### ontology/sparql/ (SPARQL tools)
- [M2_MetaConcepts_2026_02_08_encoding_lint_ok.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_2026_02_08_encoding_lint_ok.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_2026_02_08_encoding_lint_ok.ttl)
- [M2_MetaConcepts_v15_0_0_WITH_Processor.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_v15_0_0_WITH_Processor.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_v15_0_0_WITH_Processor.ttl)
- [M2_Processor.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_Processor.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_Processor.ttl)
- [M2_MetaConcepts_SPARQL_Querie_README.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_SPARQL_Querie_README.txt)
- [SPARQL_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/SPARQL_README.md)
- [m2_sparql_analysis.py](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/m2_sparql_analysis.py)

### ontology/tools/
- [M2_MetaConcepts_Ref.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/tools/M2_MetaConcepts_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/tools/M2_MetaConcepts_Ref.ttl)

### M2 Documentation (ontology/docs/)
- [M2_Architecture_Specification_v9.1.0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Architecture_Specification_v9.1.0.md)
- [M2_Behavioral_Sequential_Metaconcepts_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Behavioral_Sequential_Metaconcepts_README.md)
- [M2_Behavioral_Visual_Guide.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Behavioral_Visual_Guide.md)
- [M2_Candidates_Analysis_Layer_Switch_Mode (1).md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Candidates_Analysis_Layer_Switch_Mode%20(1).md)
- [M2_Coherence_Analysis.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Coherence_Analysis.md)
- [M2_Component_Channel_Addition_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Component_Channel_Addition_Summary.md)
- [M2_Dual_ORIVE_Proposals.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Dual_ORIVE_Proposals.md)
- [M2_FormulasReference_v15.10.0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_FormulasReference_v15.10.0.md)
- [M2_GenericConcepts_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_GenericConcepts_README.md)
- [M2_Generation_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Generation_Summary.md)
- [M2_Imbrication_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Imbrication_README.md)
- [M2_KnowledgeField_Integration_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_KnowledgeField_Integration_Summary.md)
- [M2_KnowledgeField_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_KnowledgeField_README.md)
- [M2_MetaConcepts_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_README.md)
- [M2_OntologyCategory_Proposal (1).md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_OntologyCategory_Proposal%20(1).md)
- [M2_Scope_Metaconcept_Proposal.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Scope_Metaconcept_Proposal.md)
- [MetaconceptPair_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/MetaconceptPair_README.md)

**M2 Archived Ontology Files (ontology/docs/):**
- [M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.ttl)
- [M2_MetaConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts.ttl) *(archived)*
- [M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_2026_02_06_encoding_lint_checked.ttl)
- [M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.ttl)
- [M2_MetaconceptCombo.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaconceptCombo.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaconceptCombo.ttl)
- [M2_Metaconcepts_v13.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Metaconcepts_v13.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Metaconcepts_v13.ttl)
- [M2_New_5_Metaconcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_New_5_Metaconcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_New_5_Metaconcepts.ttl)
- [M2_Pattern_metaconcept.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Pattern_metaconcept.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Pattern_metaconcept.ttl)
- [m2_Imbrication_entry.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/m2_Imbrication_entry.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/m2_Imbrication_entry.ttl)

---

## 🎯 M1 Layer - Domain Extensions

### Core Concepts (ontology/)
- [M1_CoreConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld) - Core domain-agnostic concepts

### M1 Extensions Root (ontology/M1_extensions/)
- [M1_CoreConcepts_NuclearUpdate.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/M1_CoreConcepts_NuclearUpdate.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/M1_CoreConcepts_NuclearUpdate.ttl)
- [M1_Extensions_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/M1_Extensions_Summary.md)

### Domain Extensions

**Biology (M1_extensions/biology/):**
- [M1_Biology.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.ttl)
- [M2_MetaConcepts_Alignment.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M2_MetaConcepts_Alignment.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M2_MetaConcepts_Alignment.ttl)

**Chemistry (M1_extensions/chemistry/):**
- [M1_Chemistry.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.ttl)

**Economics (M1_extensions/economics/):**
- [M1_Economics.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics.ttl)
- [M1_Economics_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics_README.md)

**Education (M1_extensions/education/):**
- [M1_Education.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education.ttl)
- [M1_Education_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education_README.md)

**Electronics (M1_extensions/electronics/):**
- [M1_Electronics.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.ttl) — 17 KnowledgeFieldConcepts : ActiveComponent, Amplifier, Filter, ElectronicOscillator, VoltageControlledOscillator, LFO, FeedbackOscillator, WaveformMode, AudioSignal, ControlVoltage, PitchCV, ExponentialConverter, ModulationSource, EurorackModule, SignalChain, FrequencyModulation, SignalProcessor
- [M1_Electronics_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics_README.md)

**Energy Generators (M1_extensions/energy_generators/):**
- [M1_EnergyGenerators.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/energy_generators/M1_EnergyGenerators.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/energy_generators/M1_EnergyGenerators.ttl)

**Mythology (M1_extensions/mythology/):**
- [M1_Mythology.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology.ttl)
- [M1_Mythology_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology_README.md)

**Optics (M1_extensions/optics/):**
- [M1_Optics.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/optics/M1_Optics.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/optics/M1_Optics.ttl)

**Photography (M1_extensions/photography/):**
- [M1_Photography.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/photography/M1_Photography.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/photography/M1_Photography.ttl)

**Physics (M1_extensions/physics/):**
- [M1_Physics.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics.ttl)
- [M1_Physics_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics_README.md)

---

## 🔬 M0 Layer - System Models

### Systemic Frameworks (instances/systemic-frameworks/Vsm/)

- [M0_VSM.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/M0_VSM.jsonld) - Viable System Model (Stafford Beer)
- [M0_VSM.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/M0_VSM.ttl)
- [M0_VSM_Metaconcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/M0_VSM_Metaconcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/M0_VSM_Metaconcepts.ttl)
- [M0_VSM_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/M0_VSM_README.md)
- [M0_VSM_README_Metaconcepts.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/M0_VSM_README_Metaconcepts.md)
- [Session_VSM_Capacity_Evaluation.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/systemic-frameworks/Vsm/Session_VSM_Capacity_Evaluation.md)

### Symbolic System Grammars (instances/symbolic-system-grammars/)

**I-Ching (symbolic-system-grammars/Iching/):**
- [M0_IChing.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/symbolic-system-grammars/Iching/M0_IChing.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/symbolic-system-grammars/Iching/M0_IChing.ttl)
- [M0_IChing_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/symbolic-system-grammars/Iching/M0_IChing_README.md)

### TSCG Tools (instances/tscg-tools/)

**TSCG Explorer (tscg-tools/TscgExplorer/):**
- [M0_TscgExplorer.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgExplorer/M0_TscgExplorer.jsonld) / [.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgExplorer/M0_TscgExplorer.ttl) - Meta-analytical poclet (TSCG analyzing itself)
- [M0_TscgExplorer_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgExplorer/M0_TscgExplorer_README.md)
- [TSCG_Explorer_Simulation_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgExplorer/TSCG_Explorer_Simulation_README.md)
- [tscg_explorer.py](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgExplorer/tscg_explorer.py)
- _00_Run_Simulation.bat, _00_setup_notes.txt, _open_cmd_window.bat, requirements.txt

**TSCG Poclet Explorer (tscg-tools/TscgPocletExplorer/) — NEW:**
- [00_Run.bat](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgPocletExplorer/00_Run.bat)

**TSCG Poclet Generator (tscg-tools/TscgPocletGenerator/) — NEW:**
- [M0_TscgPocletGenerator.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgPocletGenerator/M0_TscgPocletGenerator.jsonld)
- [M0_TscgPocletGenerator_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgPocletGenerator/M0_TscgPocletGenerator_README.md)
- [tscg_poclet_generator.py](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgPocletGenerator/tscg_poclet_generator.py)
- [tscg_rag_augmentor.py](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/tscg-tools/TscgPocletGenerator/tscg_rag_augmentor.py)
- _00_Run_Simulation.bat, _00_setup_notes.txt, _google_cloud_login.bat, _open_cmd_window.bat, _open_powershell.bat, requirements.txt

### Experimental Poclets (instances/poclets/)

Each poclet folder contains `.jsonld`, `_README.md` and sometimes simulation scripts. `.ttl` twins are present only for certain poclets (see individual entries). Folder names use CamelCase as in the repository.

**Active poclets (21 total):**
- `AdaptativeImmuneResponse/` — M0_AdaptiveImmuneResponse.jsonld / .ttl + README
- `BloodPressureControl/` — M0_BloodPressureControl.jsonld / .ttl + README
- `ButterflyMetamorphosis/` — M0_ButterflyMetamorphosis.jsonld / .ttl + README + executive summary
- `CellSignalingModes/` — M0_CellSignalingModes.jsonld / .ttl + README
- `ColorSynthesis/` — CMYK, CMY, ColorSynthesis_Federated, HSL, RGB (.jsonld only) + READMEs *(sim lives in src/tscg/simulation-engine/)*
- `ComplexChemicalSynapse/` — M0_ComplexChemicalSynapse.jsonld / .ttl + README + complex_chemical_synapse_sim.py
- `ExposureTriangle/` — M0_ExposureTriangle.jsonld + README *(sim lives in src/tscg/simulation-engine/)*
- `FireTriangle/` — M0_FireTriangle.jsonld + README *(sim lives in src/tscg/simulation-engine/)*
- `FourStrokeEngine/` — M0_FourStrokeEngine.jsonld / .ttl + README + four_stroke_engine_sim.py
- `Kidneys/` — M0_Kidneys.jsonld / .ttl + README
- `KindlebergerMinsky/` — M0_KindlebergerMinsky.jsonld / .ttl + README + KindlebergerMinsky_Simulation_README + kindleberger_minsky_sim.py
- `MtgColorWheel/` — M0_MtgColorWheel.jsonld + README + sim_mtg_color_wheel.py
- `NuclearReactorsTypology/` — M0_NuclearReactorTypology.jsonld / .ttl + README
- `PhaseTransition/` — M0_PhaseTransition.jsonld / .ttl + README + phase_transition_sim.py
- `Raas/` — M0_RAAS.jsonld + README
- `Tpack/` — M0_TPACK.jsonld / .ttl + README + tpack_sim.py
- `Transistor/` — M0_Transistor.jsonld / .ttl + README + transistor_sim.py + companion doc
- `TrophicPyramid/` — M0_TrophicPyramid.jsonld + README + sim/ (INSTALL.md, MIGRATION_GUIDE.md) — **NEW**
- `TvTestPattern/` — M0_TVTestPattern.jsonld + README + tv_test_pattern_sim.py — **NEW**
- `Vco/` — M0_VCO.jsonld / .ttl + README + VCO_Simulation_README + vco_sim.py *(first m2:Oscillator instantiation)*
- `Yggdrasil/` — M0_Yggdrasil.jsonld / .ttl + README + companion documents

**Yggdrasil companion documents:**
- [Heimdall_Interface_Constraint_Analysis.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/Yggdrasil/Heimdall_Interface_Constraint_Analysis.md)
- [Loki_As_Representation_Transformer.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/Yggdrasil/Loki_As_Representation_Transformer.md)
- [Yggdrasil_7_vs_9_Analysis.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/Yggdrasil/Yggdrasil_7_vs_9_Analysis.md)
- [Yggdrasil_Discussion_Points.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/Yggdrasil/Yggdrasil_Discussion_Points.md)
- [Yggdrasil_Reformulation_Analysis.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/Yggdrasil/Yggdrasil_Reformulation_Analysis.md)

**Poclets documentation (instances/poclets/_00_docs/):**
- [poclet_terminology.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/_00_docs/poclet_terminology.md)
- [minimal_systems_engineering_frameworks.md](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/_00_docs/minimal_systems_engineering_frameworks.md)
- [Poclet Ideas.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/instances/poclets/_00_docs/Poclet%20Ideas.txt)

---

## 💻 Source Code (src/tscg/)

Full Python package structure for the TSCG engine.

### Engine (src/tscg/engine/)
- `core/` — models.py, ontology_loader.py
- `analysis/` — metrics/orthogonality.py, sparql/executor.py
- `classifier/` — metaconcept_classifier.py
- `exporters/` — turtle_exporter.py
- `facade/` — export.py, metrics.py, ontology.py, query.py, rag.py
- `math/` — category/, spaces/, tensor/
- `rag/` — embeddings.py, retrieval.py, vector_store.py
- `reasoner/` — reasoner.py

### CLI (src/tscg/cli/)
- `batch/`, `repl/` (context.py, interpreter.py), `utils/`

### Demos (src/tscg/demos/)
- basic_usage.py, rag_demo.py

### Web API (src/tscg/webapi/)
- middleware/, routes/, schemas/

### Ontology Tools (src/tscg/ontology_tools/)

**JSON-LD to OWL/Turtle converter (jsonld-to-owl/):**
- [jsonld_to_turtle.py](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/jsonld-to-owl/jsonld_to_turtle.py)
- [GUIDE_FR.md](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/jsonld-to-owl/GUIDE_FR.md), [README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/jsonld-to-owl/README.md), [CHANGELOG.md](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/jsonld-to-owl/CHANGELOG.md)
- test_converter.py, requirements.txt

**Migration tools (migration/):**
- [tscg_migration.py](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/migration/tscg_migration.py)
- [TSCG_migration_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/migration/TSCG_migration_README.md)

### RAG (src/tscg/rag/)
- [create_tscg_rag.py](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/create_tscg_rag.py)
- [query_tscg_rag.py](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/query_tscg_rag.py)
- [TSCG_RAG_Segmentation_Guide.md](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/TSCG_RAG_Segmentation_Guide.md)
- [TSCG_RAG_Standalone_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/TSCG_RAG_Standalone_README.md)

### Simulation Engine (src/tscg/simulation-engine/)

Shared simulation scripts (poclets with no local `poclet_parser.py` dependency use their own folder).

- color_synthesis_sim.py, complex_chemical_synapse_sim.py, exposure_triangle_sim.py
- fire_triangle_sim.py, four_stroke_engine_sim.py, phase_transition_sim.py
- tpack_sim.py, transistor_sim.py
- poclet_parser.py, requirements.txt, setup_notes.txt

> **Note:** `vco_sim.py` and `kindleberger_minsky_sim.py` live in their respective poclet folders (no dependency on `poclet_parser.py`). `tv_test_pattern_sim.py` likewise lives in `TvTestPattern/`.

### Tests (src/tscg/tests/)
- test_facades.py

---

## 📚 Documentation

### Reboot Kit (docs/reboot-kit/)

**Essential Quick-Start Package** - Complete framework context in one directory.

**Core Documentation:**
- [00_TSCG_M3_Bicephalous_Architecture.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/00_TSCG_M3_Bicephalous_Architecture.md)
- [00_TSCG_Map_Territory_Theoretical_Foundation.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/00_TSCG_Map_Territory_Theoretical_Foundation.md)
- [00_Map_Territory_v1.2_Update_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/00_Map_Territory_v1.2_Update_Summary.md)
- [00_M3_Cyclops_Correction_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/00_M3_Cyclops_Correction_Summary.md)
- [Cascade_Modeling_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/Cascade_Modeling_README.md)
- [ENCODING_CORRESPONDANCES.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/ENCODING_CORRESPONDANCES.txt)
- [TSCG_ValueSpace_Quick_Reference.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_ValueSpace_Quick_Reference.md)
- [TSCG_ValueSpace_User_Guide.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_ValueSpace_User_Guide.md)

**M2 GenericConcepts Documentation:**
- [Domain_Hybrid_Tensor_Product_5D_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/Domain_Hybrid_Tensor_Product_5D_README.md)
- [HYBRID_FORMULAS_NOTATION_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/HYBRID_FORMULAS_NOTATION_README.md)
- [Amplification_Integration_Summary (1).md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/Amplification_Integration_Summary%20(1).md)
- [ValueSpace_Integration_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/ValueSpace_Integration_Summary.md)
- [M2_OntologyCategory_Proposal.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_OntologyCategory_Proposal.md)
- [M2_FormulasReference_v15.10.0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_FormulasReference_v15.10.0.md) — **NEW**
- [M2_GenericConcepts_README (1).md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_GenericConcepts_README%20(1).md) — **NEW**

**M0 VSM Documentation:**
- [M0_VSM_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M0_VSM_README.md)

**Project Management:**
- [TSCG_File_Tree.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_File_Tree.md) - **This file (v15.10.0)**
- [TO_DO.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TO_DO.txt)
- [poclet_terminology.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/poclet_terminology.md)
- [Namespace_Refactoring_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/Namespace_Refactoring_Summary.md)
- [Session_Summary_TSCG_v14.2.0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/Session_Summary_TSCG_v14.2.0.md)
- [check_encoding_issues.py](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/check_encoding_issues.py)
- [files.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/files.txt)
- [macros.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/macros.txt)

**Smart Prompts (docs/reboot-kit/SmartPrompts/):**
- [TSCG_Smart_Prompt_v15_1_0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v15_1_0.md)
- [TSCG_Smart_Prompt_v15_7_0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v15_7_0.md)
- [TSCG_Smart_Prompt_v15_8_0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v15_8_0.md)
- [TSCG_Smart_Prompt_v15_9_0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v15_9_0.md) — **NEW**
- [SmartPrompts/Smart_Prompt_2026_01_17.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/Smart_Prompt_2026_01_17.md)
- [SmartPrompts/TSCG_Smart_Prompt_11_0_0.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_11_0_0.md)
- [SmartPrompts/TSCG_Smart_Prompt_v14.2_Step.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_v14.2_Step.md)
- [SmartPrompts/TSCG_Smart_Prompt_v14_Domain.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_v14_Domain.md)
- [SmartPrompts/macros.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/macros.txt)
- [SmartPrompts/macros_extended.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/macros_extended.txt)

**Ontology Files (Reboot Kit Copies):**
- [00_M3_Philosophical_Basis_Sketch.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/00_M3_Philosophical_Basis_Sketch.jsonld)
- [M0_VSM.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M0_VSM.jsonld)
- [M1_CoreConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M1_CoreConcepts.jsonld)
- [M2_MetaConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_MetaConcepts.jsonld)
- [M2_GenericConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_GenericConcepts.jsonld) — **NEW**
- [M2_MetaconceptCombo.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_MetaconceptCombo.jsonld)
- [M2_Pattern_metaconcept.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M2_Pattern_metaconcept.jsonld)
- [M3_EagleEye.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M3_EagleEye.jsonld)
- [M3_GenesisSpace.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M3_GenesisSpace.jsonld)
- [M3_SphinxEye.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/M3_SphinxEye.jsonld)

### Methodology (docs/methodology/)
- [Bicephalous_Integration_Guide.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/methodology/Bicephalous_Integration_Guide.md)
- [M2_Completeness_and_3D_Visualization_Strategy.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/methodology/M2_Completeness_and_3D_Visualization_Strategy.md)
- [M2_Component_Addition.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/methodology/M2_Component_Addition.jsonld)
- [Standard_Referencing_Pattern.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/methodology/Standard_Referencing_Pattern.md)

### Orchestration (docs/Orchestration/)
- [Multi-Conversation_Orchestration_Guide.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/Orchestration/Multi-Conversation_Orchestration_Guide.md)

### Papers (docs/papers/)

**Preprints (docs/papers/preprints/):**
- [TSCG_Research_Paper_Draft_v3.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/TSCG_Research_Paper_Draft_v3.md) *(current)*
- [new draft specification.txt](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/new%20draft%20specification.txt)
- [HAL Guidelines.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/HAL%20Guidelines.md)
- [TSCG_HAL_Additions_v1.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/TSCG_HAL_Additions_v1.md)

**Previous versions (docs/papers/preprints/previous/):**
- [TSCG_Research_Paper_Draft_v1.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/previous/TSCG_Research_Paper_Draft_v1.md)
- [TSCG_Research_Paper_Draft_v2.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/previous/TSCG_Research_Paper_Draft_v2.md)

**White Paper:**
- [TSCG_WhitePaper.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/white-paper/TSCG_WhitePaper.md)

**Input Sources (docs/papers/inputs/):**
- [00_M3_Cyclops_Correction_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/00_M3_Cyclops_Correction_Summary.md)
- [00_M3_Philosophical_Basis_Sketch.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/00_M3_Philosophical_Basis_Sketch.jsonld)
- [00_Map_Territory_v1.2_Update_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/00_Map_Territory_v1.2_Update_Summary.md)
- [00_TSCG_M3_Bicephalous_Architecture.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/00_TSCG_M3_Bicephalous_Architecture.md)
- [00_TSCG_Map_Territory_Theoretical_Foundation.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/00_TSCG_Map_Territory_Theoretical_Foundation.md)
- [M2_v7.2.0_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/M2_v7.2.0_Summary.md)
- [M2_v8.0.0_Update_Guide.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/M2_v8.0.0_Update_Guide.md)
- [TSCG-M3_Ontology_Documentation.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/TSCG-M3_Ontology_Documentation.md)
- [TSCG_Session_Complete_Summary_Claude_2025_01_14.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/TSCG_Session_Complete_Summary_Claude_2025_01_14.md)
- [Network_Decomposition_Report.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/inputs/Network_Decomposition_Report.md)

### Other Documentation
- [docs/M2_MetaConcepts_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/M2_MetaConcepts_README.md)
- [docs/TSCG_M2_Category_Taxonomy.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/TSCG_M2_Category_Taxonomy.md)
- [docs/TSCG_Session_Complete_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/TSCG_Session_Complete_Summary.md)
- [docs/TSCG_Update_v11_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/TSCG_Update_v11_Summary.md)
- [docs/TSCG_File_Tree.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/TSCG_File_Tree.md) *(copy in docs/ root)*

---

## 📈 Repository Structure

```
echopraxium/tscg/                      # Repository root
├── CLAUDE.md                          # Claude AI instructions
├── README.md
├── _open_cmd_window.bat
├── _Run_Poclet_Explorer.bat
├── claude_setup.txt
├── files.txt                          # Complete file list
├── create_files_URIS.py
├── cli_tools/
│   └── _open_powershell.bat
├── ontology/                          # Reference ontologies (M3, M2, M1)
│   ├── M1_CoreConcepts.jsonld
│   ├── M2_GenericConcepts.jsonld
│   ├── M2_Calibration.jsonld          # NEW — standalone M2 file
│   ├── M3_EagleEye.jsonld/ttl
│   ├── M3_GenesisSpace.jsonld
│   ├── M3_GenesisSpace_Ref.ttl        # .ttl only in root ontology/
│   ├── M3_SphinxEye.jsonld/ttl
│   ├── shacl_shapes.ttl
│   ├── M1_extensions/                 # Domain-specific extensions
│   │   ├── M1_CoreConcepts_NuclearUpdate.jsonld/ttl
│   │   ├── biology/
│   │   ├── chemistry/
│   │   ├── economics/
│   │   ├── education/
│   │   ├── electronics/
│   │   ├── energy_generators/
│   │   ├── mythology/
│   │   ├── optics/
│   │   ├── photography/
│   │   └── physics/
│   ├── Ref/                           # Reference copies
│   │   ├── M2_GenericConcepts_2026_02_17_17h-00min.jsonld/ttl
│   │   ├── M2_MetaConcepts_Ref.jsonld/ttl
│   │   └── M3_GenesisSpace_Ref.jsonld/ttl
│   ├── docs/                          # Ontology documentation & archives
│   ├── sparql/                        # SPARQL queries & enriched ontologies
│   └── tools/                         # Reference tool files
├── instances/                         # System instances (M0 layer)
│   ├── poclets/                       # 21 experimental models (CamelCase subfolders)
│   │   ├── _00_docs/                  # Poclets documentation
│   │   ├── AdaptativeImmuneResponse/
│   │   ├── BloodPressureControl/
│   │   ├── ButterflyMetamorphosis/
│   │   ├── CellSignalingModes/
│   │   ├── ColorSynthesis/
│   │   ├── ComplexChemicalSynapse/
│   │   ├── ExposureTriangle/
│   │   ├── FireTriangle/
│   │   ├── FourStrokeEngine/
│   │   ├── Kidneys/
│   │   ├── KindlebergerMinsky/
│   │   ├── MtgColorWheel/
│   │   ├── NuclearReactorsTypology/
│   │   ├── PhaseTransition/
│   │   ├── Raas/
│   │   ├── Tpack/
│   │   ├── Transistor/
│   │   ├── TrophicPyramid/            # NEW
│   │   ├── TvTestPattern/             # NEW
│   │   ├── Vco/
│   │   └── Yggdrasil/
│   ├── tscg-tools/                    # TSCG meta-analytical tools
│   │   ├── TscgExplorer/              # TSCG Explorer (self-analysis)
│   │   ├── TscgPocletExplorer/        # NEW (stub)
│   │   └── TscgPocletGenerator/       # NEW — AI-powered poclet generation
│   ├── systemic-frameworks/Vsm/       # VSM framework integration
│   └── symbolic-system-grammars/      # I-Ching and similar systems
│       └── Iching/
├── src/tscg/                          # Python package
│   ├── engine/                        # Core engine (analysis, RAG, math, reasoner)
│   ├── cli/                           # Command-line interface
│   ├── demos/
│   ├── webapi/
│   ├── ontology_tools/                # jsonld-to-owl converter, migration tools
│   ├── rag/                           # Standalone RAG scripts
│   ├── simulation-engine/             # Shared pygame simulations
│   └── tests/
└── docs/                              # Main documentation
    ├── reboot-kit/                    # Quick-start package
    │   └── SmartPrompts/              # Smart Prompt history
    ├── methodology/                   # Development guides
    ├── Orchestration/                 # Multi-agent coordination
    └── papers/                        # Academic papers & white papers
        ├── inputs/
        ├── preprints/
        │   └── previous/              # Archived v1 & v2
        └── white-paper/
```

---

## 🔄 Version History

### v15.10.0 (2026-03-16) — Current

- New poclets: `TrophicPyramid/` + `TvTestPattern/` (tv_test_pattern_sim.py)
- New TSCG tools: `TscgPocletGenerator/` (AI-powered generation) + `TscgPocletExplorer/` (stub)
- New standalone M2 file: `M2_Calibration.jsonld`
- Reboot-kit enriched: Smart Prompt v15.9.0, M2_GenericConcepts.jsonld copy, M2_FormulasReference_v15.10.0.md

### v15.9.0 (2026-03-01)

- New M1 extension: `economics/` (M1_Economics.jsonld + README)
- New poclet: `KindlebergerMinsky/` (M0 + simulation)
- New section: `instances/tscg-tools/TscgExplorer/` (meta-analytical tool)
- `instances/validation/` directory removed

### v15.8.0 (2026-02-27)

- Smart Prompt v15.8.0 released
- New M1 extensions: `education/`, `physics/`, `electronics/` (VCO domain)
- New poclets: `PhaseTransition/` (simulation) + `Vco/` (first m2:Oscillator instantiation)
- `M1_Electronics.jsonld` — 17 concepts covering analog electronics & modular synthesis
- Preprints reorganized with `previous/` subfolder; v3 is now current

---

**Generated:** 2026-03-16  
**Framework:** TSCG v15.10.0  
**Author:** Echopraxium with the collaboration of Claude AI
