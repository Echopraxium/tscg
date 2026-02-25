# 📁 TSCG Framework - Complete File Tree

**Date:** 2026-02-25  
**Framework Version:** TSCG v15.7.0  
**Total Files:** 415

---

## 📊 Project Statistics

**Ontology Files:**
- M3 Layer: 5 files (+ .ttl twins + Ref/ copies)
- M2 Layer: 1 file (M2_GenericConcepts) + archived versions in docs/
- M1 Layer: 1 core file + 6 domain extensions (+ .ttl twins)
- M0 Layer: 16 validated poclets + experimental poclets + 1 VSM systemic framework + 1 symbolic grammar

**Documentation:** ~100 files  
**Source Code:** extensive `src/tscg/` Python package  
**Scripts & Tools:** 20+ files  
**Root & Config:** 7 files

**Total:** 415 files

---

## 🆕 What's New (vs v14.3.3)

### Repository
- 🔄 Moved from `Echopraxium/tscg` (main) to `aladas-org/cryptocalc` (master)

### Ontology Layer Updates
- 🔄 `M2_MetaConcepts.jsonld` at ontology root replaced by `M2_GenericConcepts.jsonld`
- ✅ `M3_GenesisSpace_Ref.jsonld/ttl` added
- ✅ New `ontology/Ref/` subdirectory with reference copies
- ✅ All ontology files now have `.ttl` (Turtle) twin files
- ✅ New `ontology/sparql/` subdirectory with SPARQL tools
- ✅ New `ontology/tools/` subdirectory

### M1 Layer Updates
- ✅ New domain extension: `energy_generators` (M1_EnergyGenerators)
- ✅ `M1_CoreConcepts_NuclearUpdate.jsonld/ttl` added at M1_extensions root
- ✅ `M2_MetaConcepts_Alignment.jsonld/ttl` added in biology extension

### M0 Layer Updates
- ✅ VSM reorganized to `system-models/systemic-frameworks/vsm/` with dedicated subfolder
- ✅ New `M0_VSM_Metaconcepts.jsonld/ttl` and `M0_VSM_README_Metaconcepts.md`
- ✅ New category: `symbolic-system-grammars/` with I-Ching poclet
- ✅ New `poclets/00_to_be_fixed/` triage subfolder
- ✅ New poclets: `kidneys`, `nuclear_reactors_typology`, `raas`, `transistor`, `yggdrasil` (with dedicated folders)

### Source Code Updates
- ✅ Full `src/tscg/` Python package: engine, CLI, RAG, web API, ontology tools
- ✅ JSON-LD to OWL/Turtle converter (`src/tscg/ontology_tools/jsonld-to-owl/`)
- ✅ Migration tools (`src/tscg/ontology_tools/migration/`)
- ✅ Simulation engines: color synthesis, exposure triangle, fire triangle, four-stroke engine, transistor

### Documentation Updates
- ✅ Reboot-kit: new `SmartPrompts/` subfolder
- ✅ Smart Prompts: v15.1.0, v15.7.0
- ✅ Many new analysis and summary documents

---

## 🏛️ M3 Layer - Genesis Space

Core foundation defining the bicephalous architecture (Territory/Map distinction).

### Main ontology/
- [M3_EagleEye.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_EagleEye.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_EagleEye.ttl) - Territory perspective (ASFID dimensions)
- [M3_GenesisSpace.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_GenesisSpace.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_GenesisSpace.ttl) - Foundational ontology
- [M3_GenesisSpace_Ref.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_GenesisSpace_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_GenesisSpace_Ref.ttl) - Reference copy
- [M3_SphinxEye.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_SphinxEye.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M3_SphinxEye.ttl) - Map perspective (REVOI dimensions)

### ontology/Ref/ (reference copies)
- [M2_MetaConcepts_Ref.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/Ref/M2_MetaConcepts_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/Ref/M2_MetaConcepts_Ref.ttl)
- [M3_GenesisSpace_Ref.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/Ref/M3_GenesisSpace_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/Ref/M3_GenesisSpace_Ref.ttl)

---

## 🌐 M2 Layer - Universal Metaconcepts

### Main ontology/ file
- [M2_GenericConcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M2_GenericConcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M2_GenericConcepts.ttl) - Generic/universal metaconcepts

### ontology/sparql/ (SPARQL tools)
- [M2_MetaConcepts_2026_02_08_encoding_lint_ok.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_MetaConcepts_2026_02_08_encoding_lint_ok.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_MetaConcepts_2026_02_08_encoding_lint_ok.ttl)
- [M2_MetaConcepts_v15_0_0_WITH_Processor.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_MetaConcepts_v15_0_0_WITH_Processor.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_MetaConcepts_v15_0_0_WITH_Processor.ttl)
- [M2_Processor.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_Processor.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_Processor.ttl)
- [M2_MetaConcepts_SPARQL_Querie_README.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/M2_MetaConcepts_SPARQL_Querie_README.txt)
- [SPARQL_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/SPARQL_README.md)
- [m2_sparql_analysis.py](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/sparql/m2_sparql_analysis.py)

### ontology/tools/
- [M2_MetaConcepts_Ref.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/tools/M2_MetaConcepts_Ref.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/tools/M2_MetaConcepts_Ref.ttl)

### M2 Documentation (ontology/docs/)
- [M2_Architecture_Specification_v9.1.0.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Architecture_Specification_v9.1.0.md)
- [M2_Behavioral_Sequential_Metaconcepts_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Behavioral_Sequential_Metaconcepts_README.md)
- [M2_Behavioral_Visual_Guide.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Behavioral_Visual_Guide.md)
- [M2_Candidates_Analysis_Layer_Switch_Mode (1).md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Candidates_Analysis_Layer_Switch_Mode%20(1).md)
- [M2_Coherence_Analysis.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Coherence_Analysis.md)
- [M2_Component_Channel_Addition_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Component_Channel_Addition_Summary.md)
- [M2_Dual_ORIVE_Proposals.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Dual_ORIVE_Proposals.md)
- [M2_GenericConcepts_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_GenericConcepts_README.md)
- [M2_Generation_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Generation_Summary.md)
- [M2_Imbrication_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Imbrication_README.md)
- [M2_KnowledgeField_Integration_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_KnowledgeField_Integration_Summary.md)
- [M2_KnowledgeField_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_KnowledgeField_README.md)
- [M2_MetaConcepts_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts_README.md)
- [M2_OntologyCategory_Proposal (1).md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_OntologyCategory_Proposal%20(1).md)
- [M2_Scope_Metaconcept_Proposal.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Scope_Metaconcept_Proposal.md)
- [MetaconceptPair_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/MetaconceptPair_README.md)

**M2 Archived Ontology Files (ontology/docs/):**
- [M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.ttl)
- [M2_MetaConcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts.ttl) *(archived)*
- [M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts_2026_02_06_encoding_lint_checked.ttl)
- [M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.ttl)
- [M2_MetaconceptCombo.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaconceptCombo.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_MetaconceptCombo.ttl)
- [M2_Metaconcepts_v13.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Metaconcepts_v13.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Metaconcepts_v13.ttl)
- [M2_New_5_Metaconcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_New_5_Metaconcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_New_5_Metaconcepts.ttl)
- [M2_Pattern_metaconcept.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Pattern_metaconcept.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/M2_Pattern_metaconcept.ttl)
- [m2_Imbrication_entry.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/m2_Imbrication_entry.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/docs/m2_Imbrication_entry.ttl)

---

## 🎯 M1 Layer - Domain Extensions

### Core Concepts (ontology/)
- [M1_CoreConcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_CoreConcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_CoreConcepts.ttl) - Core domain-agnostic concepts

### M1 Extensions Root (ontology/M1_extensions/)
- [M1_CoreConcepts_NuclearUpdate.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/M1_CoreConcepts_NuclearUpdate.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/M1_CoreConcepts_NuclearUpdate.ttl)
- [M1_Extensions_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/M1_Extensions_Summary.md)

### Domain Extensions

**Biology (M1_extensions/biology/):**
- [M1_Biology.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/biology/M1_Biology.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/biology/M1_Biology.ttl)
- [M2_MetaConcepts_Alignment.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/biology/M2_MetaConcepts_Alignment.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/biology/M2_MetaConcepts_Alignment.ttl)

**Chemistry (M1_extensions/chemistry/):**
- [M1_Chemistry.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/chemistry/M1_Chemistry.ttl)

**Energy Generators (M1_extensions/energy_generators/) — NEW:**
- [M1_EnergyGenerators.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/energy_generators/M1_EnergyGenerators.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/energy_generators/M1_EnergyGenerators.ttl)

**Mythology (M1_extensions/mythology/):**
- [M1_Mythology.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/mythology/M1_Mythology.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/mythology/M1_Mythology.ttl)
- [M1_Mythology_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/mythology/M1_Mythology_README.md)

**Optics (M1_extensions/optics/):**
- [M1_Optics.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/optics/M1_Optics.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/optics/M1_Optics.ttl)

**Photography (M1_extensions/photography/):**
- [M1_Photography.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/photography/M1_Photography.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/M1_extensions/photography/M1_Photography.ttl)

---

## 🔬 M0 Layer - System Models

### Systemic Frameworks (system-models/systemic-frameworks/vsm/)

- [M0_VSM.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/M0_VSM.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/M0_VSM.ttl) - Viable System Model (Stafford Beer)
- [M0_VSM_Metaconcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/M0_VSM_Metaconcepts.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/M0_VSM_Metaconcepts.ttl) — **NEW**
- [M0_VSM_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/M0_VSM_README.md)
- [M0_VSM_README_Metaconcepts.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/M0_VSM_README_Metaconcepts.md) — **NEW**
- [Session_VSM_Capacity_Evaluation.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/systemic-frameworks/vsm/Session_VSM_Capacity_Evaluation.md)

### Symbolic System Grammars (system-models/symbolic-system-grammars/) — NEW CATEGORY

**I-Ching (symbolic-system-grammars/iching/):**
- [M0_IChing.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/symbolic-system-grammars/iching/M0_IChing.jsonld) / [.ttl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/symbolic-system-grammars/iching/M0_IChing.ttl)
- [M0_IChing_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/symbolic-system-grammars/iching/M0_IChing_README.md)

### Validated Poclets (system-models/validation/)

Each poclet has `.jsonld` and `.ttl` files:

- [M0_AdaptiveImmuneResponse](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_AdaptiveImmuneResponse.jsonld)
- [M0_BloodPressureControl](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_BloodPressureControl.jsonld)
- [M0_ButterflyMetamorphosis](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_ButterflyMetamorphosis.jsonld)
- [M0_CellSignalingModes](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_CellSignalingModes.jsonld)
- [M0_CMYK_Subtractive](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_CMYK_Subtractive.jsonld)
- [M0_CMY_Subtractive](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_CMY_Subtractive.jsonld)
- [M0_ColorSynthesis_Federated](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_ColorSynthesis_Federated.jsonld)
- [M0_ComplexChemicalSynapse](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_ComplexChemicalSynapse.jsonld)
- [M0_ExposureTriangle](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_ExposureTriangle.jsonld)
- [M0_FireTriangle](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_FireTriangle.jsonld)
- [M0_FourStrokeEngine](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_FourStrokeEngine.jsonld)
- [M0_HSL_Additive](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_HSL_Additive.jsonld)
- [M0_MTG_ColorWheel](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_MTG_ColorWheel.jsonld)
- [M0_RGB_Additive](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_RGB_Additive.jsonld)
- [M0_TPACK](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_TPACK.jsonld)
- [M0_Yggdrasil](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/validation/M0_Yggdrasil.jsonld)

### Experimental Poclets (system-models/poclets/)

Each poclet folder contains `.jsonld`, `.ttl`, `_README.md` and sometimes simulation scripts.

**Active poclets:**
- `adaptative_immune_response/` — M0_AdaptiveImmuneResponse + README
- `blood_pressure_control/` — M0_BloodPressureControl + README
- `butterfly_metamorphosis/` — M0_ButterflyMetamorphosis + README + executive summary
- `cell_signaling_modes/` — M0_CellSignalingModes + README
- `exposure_triangle/` — M0_ExposureTriangle + README + Metaconcepts_List.py
- `fire_triangle/` — M0_FireTriangle + README
- `four-stroke-engine/` — M0_FourStrokeEngine + README + four_stroke_engine_sim.py + poclet_parser.py
- `kidneys/` — M0_Kidneys + README — **NEW**
- `nuclear_reactors_typology/` — M0_NuclearReactorTypology + README — **NEW**
- `raas/` — M0_RAAS + RAAS_Complete_README — **NEW**
- `transistor/` — M0_Transistor + README + transistor_sim.py + poclet_parser.py — **NEW**
- `yggdrasil/` — M0_Yggdrasil + README + analysis docs — **NEW**

**Yggdrasil companion documents:**
- [Heimdall_Interface_Constraint_Analysis.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/yggdrasil/Heimdall_Interface_Constraint_Analysis.md)
- [Loki_As_Representation_Transformer.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/yggdrasil/Loki_As_Representation_Transformer.md)
- [Yggdrasil_7_vs_9_Analysis.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/yggdrasil/Yggdrasil_7_vs_9_Analysis.md)
- [Yggdrasil_Discussion_Points.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/yggdrasil/Yggdrasil_Discussion_Points.md)
- [Yggdrasil_Reformulation_Analysis.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/yggdrasil/Yggdrasil_Reformulation_Analysis.md)

**Poclets under revision (system-models/poclets/00_to_be_fixed/):**
- `color_synthesis/` — CMYK, CMY, ColorSynthesis_Federated, ComplexChemicalSynapse, HSL, RGB + docs
- `complex_chemical_synapse/` — M0_ComplexChemicalSynapse + README
- `mtg_color_wheel/` — M0_MTG_ColorWheel
- `tpack/` — M0_TPACK + TPACK_ORIVE_Validation_Analysis + TPACK_README

**Poclets documentation:**
- [poclet_terminology.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/docs/poclet_terminology.md)
- [minimal_systems_engineering_frameworks.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/system-models/poclets/docs/minimal_systems_engineering_frameworks.md)

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
- [jsonld_to_turtle.py](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/ontology_tools/jsonld-to-owl/jsonld_to_turtle.py)
- [GUIDE_FR.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/ontology_tools/jsonld-to-owl/GUIDE_FR.md), [README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/ontology_tools/jsonld-to-owl/README.md), [CHANGELOG.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/ontology_tools/jsonld-to-owl/CHANGELOG.md)
- test_converter.py, requirements.txt

**Migration tools (migration/):**
- [tscg_migration.py](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/ontology_tools/migration/tscg_migration.py)
- [TSCG_migration_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/ontology_tools/migration/TSCG_migration_README.md)

### RAG (src/tscg/rag/)
- [create_tscg_rag.py](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/rag/create_tscg_rag.py)
- [query_tscg_rag.py](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/rag/query_tscg_rag.py)
- [TSCG_RAG_Segmentation_Guide.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/rag/TSCG_RAG_Segmentation_Guide.md)
- [TSCG_RAG_Standalone_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/src/tscg/rag/TSCG_RAG_Standalone_README.md)

### Simulation Engine (src/tscg/simulation-engine/)
- color_synthesis_sim.py, exposure_triangle_sim.py, fire_triangle_sim.py
- four_stroke_engine_sim.py, transistor_sim.py
- poclet_parser.py, requirements.txt

### Tests (src/tscg/tests/)
- test_facades.py

---

## 📚 Documentation

### Reboot Kit (docs/reboot-kit/)

**Essential Quick-Start Package** - Complete framework context in one directory.

**Core Documentation:**
- [00_TSCG_M3_Bicephalous_Architecture.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/00_TSCG_M3_Bicephalous_Architecture.md)
- [00_TSCG_Map_Territory_Theoretical_Foundation.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/00_TSCG_Map_Territory_Theoretical_Foundation.md)
- [00_Map_Territory_v1.2_Update_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/00_Map_Territory_v1.2_Update_Summary.md)
- [00_M3_Cyclops_Correction_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/00_M3_Cyclops_Correction_Summary.md)
- [Cascade_Modeling_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/Cascade_Modeling_README.md)
- [ENCODING_CORRESPONDANCES.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/ENCODING_CORRESPONDANCES.txt)
- [TSCG_ValueSpace_Quick_Reference.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/TSCG_ValueSpace_Quick_Reference.md)
- [TSCG_ValueSpace_User_Guide.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/TSCG_ValueSpace_User_Guide.md)

**M2 Metaconcepts Documentation:**
- [Domain_Hybrid_Tensor_Product_5D_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/Domain_Hybrid_Tensor_Product_5D_README.md)
- [HYBRID_FORMULAS_NOTATION_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/HYBRID_FORMULAS_NOTATION_README.md)
- [Amplification_Integration_Summary (1).md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/Amplification_Integration_Summary%20(1).md)
- [ValueSpace_Integration_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/ValueSpace_Integration_Summary.md)
- [M2_OntologyCategory_Proposal.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M2_OntologyCategory_Proposal.md)

**M0 VSM Documentation:**
- [M0_VSM_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M0_VSM_README.md)

**Project Management:**
- [TSCG_File_Tree.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/TSCG_File_Tree.md) - **This file (v15.7.0)**
- [TO_DO.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/TO_DO.txt)
- [poclet_terminology.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/poclet_terminology.md)
- [Namespace_Refactoring_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/Namespace_Refactoring_Summary.md)
- [Session_Summary_TSCG_v14.2.0.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/Session_Summary_TSCG_v14.2.0.md)
- [check_encoding_issues.py](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/check_encoding_issues.py)
- [files.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/files.txt)
- [macros.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/macros.txt)

**Smart Prompts (docs/reboot-kit/SmartPrompts/) — NEW SUBFOLDER:**
- [TSCG_Smart_Prompt_v15_1_0.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/TSCG_Smart_Prompt_v15_1_0.md)
- [TSCG_Smart_Prompt_v15_7_0.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/TSCG_Smart_Prompt_v15_7_0.md)
- [SmartPrompts/Smart_Prompt_2026_01_17.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/SmartPrompts/Smart_Prompt_2026_01_17.md)
- [SmartPrompts/TSCG_Smart_Prompt_11_0_0.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_11_0_0.md)
- [SmartPrompts/TSCG_Smart_Prompt_v14.2_Step.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_v14.2_Step.md)
- [SmartPrompts/TSCG_Smart_Prompt_v14_Domain.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_v14_Domain.md)
- [SmartPrompts/macros.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/SmartPrompts/macros.txt)
- [SmartPrompts/macros_extended.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/SmartPrompts/macros_extended.txt)

**Ontology Files (Reboot Kit Copies):**
- [00_M3_Philosophical_Basis_Sketch.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/00_M3_Philosophical_Basis_Sketch.jsonld)
- [M0_VSM.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M0_VSM.jsonld)
- [M1_CoreConcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M1_CoreConcepts.jsonld)
- [M2_MetaConcepts.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M2_MetaConcepts.jsonld)
- [M2_MetaconceptCombo.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M2_MetaconceptCombo.jsonld)
- [M2_OntologyCategory_Proposal.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M2_OntologyCategory_Proposal.md)
- [M2_Pattern_metaconcept.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M2_Pattern_metaconcept.jsonld)
- [M3_EagleEye.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M3_EagleEye.jsonld)
- [M3_GenesisSpace.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M3_GenesisSpace.jsonld)
- [M3_SphinxEye.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/reboot-kit/M3_SphinxEye.jsonld)

### Methodology (docs/methodology/)
- [Bicephalous_Integration_Guide.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/methodology/Bicephalous_Integration_Guide.md)
- [M2_Completeness_and_3D_Visualization_Strategy.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/methodology/M2_Completeness_and_3D_Visualization_Strategy.md)
- [M2_Component_Addition.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/methodology/M2_Component_Addition.jsonld)
- [Standard_Referencing_Pattern.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/methodology/Standard_Referencing_Pattern.md)

### Orchestration (docs/Orchestration/)
- [Multi-Conversation_Orchestration_Guide.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/Orchestration/Multi-Conversation_Orchestration_Guide.md)

### Papers (docs/papers/)

**Preprints (docs/papers/preprints/):**
- [TSCG_Research_Paper_Draft_v1.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/preprints/TSCG_Research_Paper_Draft_v1.md)
- [TSCG_Research_Paper_Draft_v2.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/preprints/TSCG_Research_Paper_Draft_v2.md)
- [new draft specification.txt](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/preprints/new%20draft%20specification.txt)

**White Paper:**
- [TSCG_WhitePaper.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/white-paper/TSCG_WhitePaper.md)

**Input Sources (docs/papers/inputs/):**
- [00_M3_Cyclops_Correction_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/00_M3_Cyclops_Correction_Summary.md)
- [00_M3_Philosophical_Basis_Sketch.jsonld](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/00_M3_Philosophical_Basis_Sketch.jsonld)
- [00_Map_Territory_v1.2_Update_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/00_Map_Territory_v1.2_Update_Summary.md)
- [00_TSCG_M3_Bicephalous_Architecture.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/00_TSCG_M3_Bicephalous_Architecture.md)
- [00_TSCG_Map_Territory_Theoretical_Foundation.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/00_TSCG_Map_Territory_Theoretical_Foundation.md)
- [TSCG-M3_Ontology_Documentation.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/TSCG-M3_Ontology_Documentation.md)
- [TSCG_Session_Complete_Summary_Claude_2025_01_14.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/TSCG_Session_Complete_Summary_Claude_2025_01_14.md)
- [Network_Decomposition_Report.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/papers/inputs/Network_Decomposition_Report.md)

### Other Documentation
- [docs/M2_MetaConcepts_README.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/M2_MetaConcepts_README.md)
- [docs/TSCG_M2_Category_Taxonomy.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/TSCG_M2_Category_Taxonomy.md)
- [docs/TSCG_Session_Complete_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/TSCG_Session_Complete_Summary.md)
- [docs/TSCG_Update_v11_Summary.md](https://raw.githubusercontent.com/aladas-org/cryptocalc/master/docs/TSCG_Update_v11_Summary.md)

---

## 📈 Repository Structure

```
aladas-org/cryptocalc/                 # Repository root
├── CLAUDE.md                          # Claude AI instructions
├── README.md
├── files.txt                          # Complete file list
├── create_files_URIS.py
├── diagnostic_models.py
├── ontology/                          # Reference ontologies (M3, M2, M1)
│   ├── M1_CoreConcepts.jsonld/ttl
│   ├── M2_GenericConcepts.jsonld/ttl  # ← was M2_MetaConcepts
│   ├── M3_EagleEye.jsonld/ttl
│   ├── M3_GenesisSpace.jsonld/ttl
│   ├── M3_GenesisSpace_Ref.jsonld/ttl
│   ├── M3_SphinxEye.jsonld/ttl
│   ├── shacl_shapes.ttl
│   ├── M1_extensions/                 # Domain-specific extensions
│   │   ├── M1_CoreConcepts_NuclearUpdate.jsonld/ttl
│   │   ├── biology/
│   │   ├── chemistry/
│   │   ├── energy_generators/         # NEW
│   │   ├── mythology/
│   │   ├── optics/
│   │   └── photography/
│   ├── Ref/                           # Reference copies
│   ├── docs/                          # Ontology documentation & archives
│   ├── sparql/                        # SPARQL queries & SPARQL-enriched ontologies
│   └── tools/                         # Reference tool files
├── system-models/                     # System instances (M0 layer)
│   ├── poclets/                       # Experimental models (by subfolder)
│   │   ├── 00_to_be_fixed/            # Poclets under revision
│   │   ├── docs/
│   │   └── [domain folders]
│   ├── validation/                    # Validated models (.jsonld + .ttl)
│   ├── systemic-frameworks/vsm/       # VSM framework integration
│   └── symbolic-system-grammars/     # NEW: I-Ching and similar systems
│       └── iching/
├── src/tscg/                          # Python package
│   ├── engine/                        # Core engine (analysis, RAG, math, reasoner)
│   ├── cli/                           # Command-line interface
│   ├── demos/
│   ├── webapi/
│   ├── ontology_tools/                # jsonld-to-owl converter, migration tools
│   ├── rag/                           # Standalone RAG scripts
│   ├── simulation-engine/             # Pygame simulations
│   └── tests/
└── docs/                              # Main documentation
    ├── reboot-kit/                    # Quick-start package
    │   └── SmartPrompts/              # Smart Prompt history
    ├── methodology/                   # Development guides
    ├── Orchestration/                 # Multi-agent coordination
    └── papers/                        # Academic papers & white papers
        ├── inputs/
        ├── preprints/
        └── white-paper/
```

---

## 🔄 Version History

### v15.7.0 (2026-02-25) - Current

- Smart Prompt v15.7.0 released
- Full src/tscg/ Python engine package
- symbolic-system-grammars/ category with I-Ching
- JSON-LD to OWL/Turtle converter operational

### v15.1.0 (2026-02-XX)

- REVOI canonical notation consolidated (deprecated ORIVE removed)
- M1_CoreConcepts expanded from 3 to 9 concepts
- All ontology files converted to dual format (.jsonld + .ttl)
- M1_EnergyGenerators extension added

### v14.3.3 (2026-02-03)

- New metaconcept: `m2:Scope` (S⊗I⊗A⊗R)
- M0_VSM v1.1.0 - MetaconceptCombo patterns for VSM
- Autonomy = Agent ⊗ Scope pattern

---

**Generated:** 2026-02-25  
**Framework:** TSCG v15.7.0  
**Author:** Echopraxium with the collaboration of Claude AI
