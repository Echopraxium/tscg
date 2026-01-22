# TSCG Project File Tree Documentation

**Author**: Echopraxium with the collaboration of Claude AI  
**Project**: Transdisciplinary System Construction Game (TSCG)  
**Repository**: https://github.com/Echopraxium/tscg

---

## Project Root Structure

```
tscg/
├── README.md
├── files.txt
├── generate_file_list_URIs.bat
├── _00_run_Orchestrator.bat
├── _01_Rebuild_Solution.bat
├── _02_Test_Solution.bat
├── _open_cmd_window.bat
│
├── cli_tools/
│   ├── _00_run_Doc2B64z.bat
│   ├── _open_powershell.bat
│   └── files_list_ps.txt
│
├── docs/
│   ├── TSCG_M2_Category_Taxonomy.md
│   ├── TSCG_Session_Complete_Summary.md
│   ├── TSCG_Update_v11_Summary.md
│   │
│   ├── methodology/
│   │   ├── Bicephalous_Integration_Guide.md
│   │   ├── M2_Completeness_and_3D_Visualization_Strategy.md
│   │   ├── Standard_Referencing_Pattern.md
│   │   └── M2_Component_Addition.jsonld
│   │
│   ├── Orchestration/
│   │   └── Multi-Conversation_Orchestration_Guide.md
│   │
│   ├── reboot-kit/
│   │   ├── 00_M3_Cyclops_Correction_Summary.md
│   │   ├── 00_Map_Territory_v1.2_Update_Summary.md
│   │   ├── 00_TSCG_M3_Bicephalous_Architecture.md
│   │   ├── 00_TSCG_Map_Territory_Theoretical_Foundation.md
│   │   ├── poclet_terminology.md
│   │   ├── 00_M3_Philosophical_Basis_Sketch.jsonld
│   │   ├── macros.txt
│   │   │
│   │   └── SmartPrompts/
│   │       ├── Smart_Prompt_2026_01_17.md
│   │       ├── TSCG_Smart_Prompt_11_0_0.md
│   │       ├── macros.txt
│   │       └── macros_extended.txt
│   │
│   └── research-paper/
│       ├── tscg-draft-v0.md
│       │
│       └── inputs/
│           ├── 00_M3_Cyclops_Correction_Summary.md
│           ├── 00_Map_Territory_v1.2_Update_Summary.md
│           ├── 00_TSCG_M3_Bicephalous_Architecture.md
│           ├── 00_TSCG_Map_Territory_Theoretical_Foundation.md
│           ├── M2_v7.2.0_Summary.md
│           ├── M2_v8.0.0_Update_Guide.md
│           ├── Network_Decomposition_Report.md
│           ├── TSCG-M3_Ontology_Documentation.md
│           ├── TSCG_Session_Complete_Summary_Claude_2025_01_14.md
│           └── 00_M3_Philosophical_Basis_Sketch.jsonld
│
├── ontology/
│   ├── M2_MetaConcepts.jsonld
│   ├── M3_EagleEye.jsonld
│   ├── M3_GenesisSpace.jsonld
│   ├── M3_SphinxEye.jsonld
│   ├── M1_CoreConcepts.jsonld
│   │
│   ├── docs/
│   │   ├── Bicephalous_Integration_Guide.md
│   │   ├── Bicephalous_Refactoring_Summary.md
│   │   ├── Final_Corrections_Summary.md
│   │   ├── HOWTO_Create_M1_Extension.md
│   │   ├── M2_Architecture_Specification_v9.1.0.md
│   │   ├── M2_Candidates_Analysis_Layer_Switch_Mode (1).md
│   │   ├── M2_Coherence_Analysis.md
│   │   ├── M2_Component_Channel_Addition_Summary.md
│   │   ├── M2_Dual_ORIVE_Proposals (1).md
│   │   ├── M2_Dual_ORIVE_Proposals.md
│   │   ├── M2_Generation_Summary.md
│   │   ├── M3_Genesis_Space_README.md
│   │   ├── ontology_analysis.md
│   │   ├── PAPAT.md
│   │   ├── TSCG-M3_Ontology_Documentation.md
│   │   ├── TSCG_M2_MetaConcepts_Ontology_README.md
│   │   ├── TSCG_Update_v12_Summary.md
│   │   └── M3_Philosophical_Eye.jsonld
│   │
│   ├── M1_extensions/
│   │   ├── chemistry/
│   │   │   └── M1_Chemistry.jsonld
│   │   │
│   │   └── optics/
│   │       └── M1_Optics.jsonld
│   │
│   └── poclets/
│       │
│       ├── docs/
│       │   ├── minimal_systems_engineering_frameworks.md
│       │   └── poclet_terminology.md
│       │
│       ├── cell_signaling/
│       │   ├── M0_CellSignalingModes.jsonld
│       │   │
│       │   └── docs/
│       │       └── M0_CellSignalingModes_README.md
│       │
│       ├── color_synthesis/
│       │   ├── Fusion_vs_Composition_Correction.md
│       │   ├── ORIVE_Poclets_Application_Summary.md
│       │   ├── M0_CMYK_Subtractive.jsonld
│       │   ├── M0_CMY_Subtractive.jsonld
│       │   ├── M0_ColorSynthesis_Federated.jsonld
│       │   ├── M0_HSL_Additive.jsonld
│       │   ├── M0_RGB_Additive.jsonld
│       │   │
│       │   └── docs/
│       │       └── ColorSynthesis_Final_Summary.md
│       │
│       ├── complex_chemical_synapse/
│       │   ├── M0_ComplexChemicalSynapse.jsonld
│       │   ├── M0_ComplexChemicalSynapse_README.md
│       │
│       ├── exposition_triangle/
│       │   ├── M0_ExposureTriangle.jsonld
│       │   │
│       │   └── docs/
│       │       └── Balance_Tradeoff_ExposureTriangle_Summary.md
│       │
│       ├── fire_triangle/
│       │   └── M0_FireTriangle.jsonld
│       │
│       └── tpack/
│           ├── TPACK_ORIVE_Validation_Analysis.md
│           ├── TPACK_README.md
│           └── M0_TPACK.jsonld
│
└── src/
    └── TSCG.Orchestrator/
        ├── Program.cs
        ├── TSCG.Orchestrator.csproj
        │
        ├── obj/Debug/net10.0/
        │   ├── .NETCoreApp,Version=v10.0.AssemblyAttributes.cs
        │   ├── TSCG.Orchestrator.AssemblyInfo.cs
        │   ├── TSCG.Orchestrator.GlobalUsings.g.cs
        │   └── TSCG.Orchestrator.csproj.FileListAbsolute.txt
        │
        └── role-prompts/
            ├── Role-Backend_Software_Architect.md
            ├── Role-Compilation_Errors_Analyser.md
            ├── Role-Frontend_Software_Architect.md
            ├── Role-Orchestrator_Software_Architect.md
            ├── Role-QA Officer.md
            ├── Role-Reboot_Kit_Manager.md
            ├── Role-Simulation_Game_Engine_Architect.md
            ├── Role_Reference_Documentation_Writer.md
            ├── Step_1_System Prompt.md
            └── Step_2_System Prompt.md
```

---

## Directory Structure Overview

### Root Level
- **Batch scripts** for project automation and orchestration
- **README.md**: Main project documentation
- **files.txt**: File listing utilities

### `/cli_tools/`
Command-line interface utilities and PowerShell scripts for project operations.

### `/docs/`
Complete project documentation organized by domain:
- **methodology/**: Framework methodologies and integration guides
- **Orchestration/**: Multi-conversation orchestration documentation
- **reboot-kit/**: Core theoretical foundations and smart prompts
- **research-paper/**: Academic paper drafts and supporting materials

### `/ontology/`
Core TSCG ontological framework:
- **M2_MetaConcepts.jsonld**: Fundamental metaconcepts (56 validated)
- **M3_*.jsonld**: Bicephalous architecture components (EagleEye, SphinxEye, GenesisSpace)
- **M1-extension/**: Domain-specific concept extensions (chemistry, optics)
- **poclets/**: Practical examples across multiple domains
- **docs/**: Technical specifications and architectural documentation

### `/src/`
Source code for the TSCG Orchestrator application (C# .NET 10.0):
- **Program.cs**: Main orchestrator logic
- **role-prompts/**: AI role definition prompts for various architectural roles

---

## Key File Categories

### Ontology Files (`.jsonld`)
- **M0_*.jsonld**: Poclet instances (practical examples)
- **M1_*.jsonld**: Domain-specific concept extensions
- **M2_MetaConcepts.jsonld**: Fundamental metaconcepts layer
- **M3_*.jsonld**: Bicephalous architecture components

### Documentation Files (`.md`)
- Methodology guides and integration specifications
- Poclet analysis and validation reports
- Architecture specifications and update summaries
- Smart prompts for framework application

### Automation Scripts (`.bat`)
- Build and test automation
- Orchestrator execution scripts
- Command-line tool launchers

---

## URI Base Reference

All ontology URIs use the base:
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology
```

---

**Last Updated**: January 2026  
**Framework Version**: TSCG 12.0.0
