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
│   ├── project_ref_documents/
│   │   ├── poclet_terminology.md
│   │   ├── TSCG_File_Tree.md
│   │   ├── M1_CoreConcepts.jsonld
│   │   ├── M2_MetaConcepts.jsonld
│   │   ├── M3_EagleEye.jsonld
│   │   ├── M3_GenesisSpace.jsonld
│   │   ├── M3_SphinxEye.jsonld
│   │   └── files.txt
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
│   ├── Namespace_Refactoring_Summary.md
│   ├── M1_CoreConcepts.jsonld
│   ├── M2_MetaConcepts.jsonld
│   ├── M3_EagleEye.jsonld
│   ├── M3_GenesisSpace.jsonld
│   ├── M3_SphinxEye.jsonld
│   │
│   ├── docs/
│   │   ├── Bicephalous_Integration_Guide.md
│   │   ├── Bicephalous_Refactoring_Summary.md
│   │   ├── Final_Corrections_Summary.md
│   │   ├── Fusion_vs_Composition_Correction.md
│   │   ├── HOWTO_Create_M1_Extension.md
│   │   ├── M2_Architecture_Specification_v9.1.0.md
│   │   ├── M2_Candidates_Analysis_Layer_Switch_Mode (1).md
│   │   ├── M2_Coherence_Analysis.md
│   │   ├── M2_Component_Channel_Addition_Summary.md
│   │   ├── M2_Dual_ORIVE_Proposals.md
│   │   ├── M2_Generation_Summary.md
│   │   ├── M3_Genesis_Space_README.md
│   │   ├── Namespace_Collision_Fix_Summary.md
│   │   ├── ontology_analysis.md
│   │   ├── README_v13_Delivery.md
│   │   ├── TSCG-M3_Ontology_Documentation.md
│   │   ├── TSCG_M1_Architecture.md
│   │   ├── TSCG_M2_MetaConcepts_Ontology_README.md
│   │   ├── TSCG_Nary_Polarity_Paradigm_Shift.md
│   │   ├── TSCG_Update_v12_Summary.md
│   │   ├── M1_CoreConcepts.jsonld
│   │   ├── M2_Metaconcepts_v13.jsonld
│   │   └── M3_Philosophical_Eye.jsonld
│   │
│   ├── M1_extensions/
│   │   ├── biology/
│   │   │   └── M1_Biology.jsonld
│   │   │
│   │   ├── chemistry/
│   │   │   └── M1_Chemistry.jsonld
│   │   │
│   │   ├── optics/
│   │   │   └── M1_Optics.jsonld
│   │   │
│   │   └── photography/
│   │       └── M1_Photography.jsonld
│   │
│   └── poclets/
│       │
│       ├── docs/
│       │   ├── minimal_systems_engineering_frameworks.md
│       │   └── poclet_terminology.md
│       │
│       ├── cell_signaling/
│       │   ├── M0_CellSignalingModes.jsonld
│       │   └── M0_CellSignalingModes_README.md
│       │
│       ├── color_synthesis/
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
│       │   └── M0_ComplexChemicalSynapse_README.md
│       │
│       ├── exposition_triangle/
│       │   ├── M0_ExposureTriangle.jsonld
│       │   └── Balance_Tradeoff_ExposureTriangle_Summary.md
│       │
│       ├── fire_triangle/
│       │   ├── M0_FireTriangle.jsonld
│       │   └── M0_FireTriangle_README.md
│       │
│       ├── four_stroke_engine/
│       │   ├── M0_FourStrokeEngine.jsonld
│       │   └── M0_FourStrokeEngine_README.md
│       │
│       ├── mtg_color_wheel/
│       │   └── M0_MTG_ColorWheel.jsonld
│       │
│       └── tpack/
│           ├── M0_TPACK.jsonld
│           ├── TPACK_ORIVE_Validation_Analysis.md
│           └── TPACK_README.md
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
- **generate_file_list_URIs.bat**: Script to generate file list with GitHub URIs

### `/cli_tools/`
Command-line interface utilities and PowerShell scripts for project operations.

### `/docs/`
Complete project documentation organized by domain:
- **methodology/**: Framework methodologies and integration guides
- **Orchestration/**: Multi-conversation orchestration documentation
- **project_ref_documents/**: Core reference documents (ontology copies, file tree, terminology)
- **reboot-kit/**: Core theoretical foundations and smart prompts
- **research-paper/**: Academic paper drafts and supporting materials

### `/ontology/`
Core TSCG ontological framework:
- **M1_CoreConcepts.jsonld**: Base layer for domain-specific concepts
- **M2_MetaConcepts.jsonld**: Fundamental metaconcepts (59 validated)
- **M3_*.jsonld**: Bicephalous architecture components (EagleEye, SphinxEye, GenesisSpace)
- **M1_extensions/**: Domain-specific concept extensions (biology, chemistry, optics, photography)
- **poclets/**: Practical examples across multiple domains (8 poclets)
- **docs/**: Technical specifications and architectural documentation

### `/src/`
Source code for the TSCG Orchestrator application (C# .NET 10.0):
- **Program.cs**: Main orchestrator logic
- **role-prompts/**: AI role definition prompts for various architectural roles

---

## Key File Categories

### Ontology Files (`.jsonld`)
- **M0_*.jsonld**: Poclet instances (practical examples - 8 poclets)
- **M1_*.jsonld**: Domain-specific concept extensions (4 domains)
- **M2_MetaConcepts.jsonld**: Fundamental metaconcepts layer (59 metaconcepts)
- **M3_*.jsonld**: Bicephalous architecture components (Genesis Space, Eagle Eye, Sphinx Eye)

### Documentation Files (`.md`)
- Methodology guides and integration specifications
- Poclet analysis and validation reports
- Architecture specifications and update summaries
- Smart prompts for framework application
- Namespace refactoring documentation

### Automation Scripts (`.bat`)
- Build and test automation
- Orchestrator execution scripts
- Command-line tool launchers
- File list generation utilities

---

## M1 Extensions Summary

The TSCG framework now includes **4 domain-specific M1 extensions**:

1. **M1_Biology.jsonld** (`m1:biology:`)
   - Cell signaling patterns (Autocrine, Paracrine, Endocrine, Juxtacrine)
   - Communication modes and biological signaling

2. **M1_Chemistry.jsonld** (`m1:chemistry:`)
   - Chemical reaction patterns
   - Combustion, catalysis, equilibrium concepts
   - Activation energy, reactants, products

3. **M1_Optics.jsonld** (`m1:optics:`)
   - 8 optical patterns
   - Additive/Subtractive color synthesis
   - Channel multiplexing
   - Spectral decomposition

4. **M1_Photography.jsonld** (`m1:photography:`)
   - 10 photography patterns
   - Compensatory triplet (exposure triangle)
   - Logarithmic scaling (stops system)
   - Side effect coupling (aperture depth-of-field)

---

## Poclet Portfolio (8 validated)

1. **Fire Triangle** - Combustion fundamentals
2. **RGB/HSL/CMY/CMYK** - Color synthesis (federated)
3. **Exposure Triangle** - Photography exposure control
4. **Cell Signaling Modes** - Biological communication
5. **Complex Chemical Synapse** - Neuronal signaling
6. **TPACK** - Educational technology framework
7. **Four-Stroke Engine** - Mechanical engineering cycles
8. **MTG Color Wheel** - Game design value system (pentagonal N-ary polarity)

---

## Complete File List (URIs)

All files are accessible via GitHub raw URLs:

### Root Level Files
- https://raw.githubusercontent.com/Echopraxium/tscg/main/README.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/files.txt
- https://raw.githubusercontent.com/Echopraxium/tscg/main/generate_file_list_URIs.bat
- https://raw.githubusercontent.com/Echopraxium/tscg/main/_00_run_Orchestrator.bat
- https://raw.githubusercontent.com/Echopraxium/tscg/main/_01_Rebuild_Solution.bat
- https://raw.githubusercontent.com/Echopraxium/tscg/main/_02_Test_Solution.bat
- https://raw.githubusercontent.com/Echopraxium/tscg/main/_open_cmd_window.bat

### CLI Tools
- https://raw.githubusercontent.com/Echopraxium/tscg/main/cli_tools/_00_run_Doc2B64z.bat
- https://raw.githubusercontent.com/Echopraxium/tscg/main/cli_tools/_open_powershell.bat
- https://raw.githubusercontent.com/Echopraxium/tscg/main/cli_tools/files_list_ps.txt

### Documentation - Main
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/TSCG_M2_Category_Taxonomy.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/TSCG_Session_Complete_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/TSCG_Update_v11_Summary.md

### Documentation - Methodology
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/methodology/Bicephalous_Integration_Guide.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/methodology/M2_Completeness_and_3D_Visualization_Strategy.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/methodology/Standard_Referencing_Pattern.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/methodology/M2_Component_Addition.jsonld

### Documentation - Orchestration
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/Orchestration/Multi-Conversation_Orchestration_Guide.md

### Documentation - Project Reference Documents
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/poclet_terminology.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/TSCG_File_Tree.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/M1_CoreConcepts.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/M2_MetaConcepts.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/M3_EagleEye.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/M3_GenesisSpace.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/M3_SphinxEye.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/project_ref_documents/files.txt

### Documentation - Reboot Kit
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/00_M3_Cyclops_Correction_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/00_Map_Territory_v1.2_Update_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/00_TSCG_M3_Bicephalous_Architecture.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/00_TSCG_Map_Territory_Theoretical_Foundation.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/poclet_terminology.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/00_M3_Philosophical_Basis_Sketch.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/macros.txt

### Documentation - Reboot Kit Smart Prompts
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/Smart_Prompt_2026_01_17.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/TSCG_Smart_Prompt_11_0_0.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/macros.txt
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/macros_extended.txt

### Documentation - Research Paper
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/tscg-draft-v0.md

### Documentation - Research Paper Inputs
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/00_M3_Cyclops_Correction_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/00_Map_Territory_v1.2_Update_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/00_TSCG_M3_Bicephalous_Architecture.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/00_TSCG_Map_Territory_Theoretical_Foundation.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/M2_v7.2.0_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/M2_v8.0.0_Update_Guide.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/Network_Decomposition_Report.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/TSCG-M3_Ontology_Documentation.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/TSCG_Session_Complete_Summary_Claude_2025_01_14.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/research-paper/inputs/00_M3_Philosophical_Basis_Sketch.jsonld

### Ontology - Root Level
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/Namespace_Refactoring_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld

### Ontology - Documentation
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/Bicephalous_Integration_Guide.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/Bicephalous_Refactoring_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/Final_Corrections_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/Fusion_vs_Composition_Correction.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/HOWTO_Create_M1_Extension.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Architecture_Specification_v9.1.0.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Candidates_Analysis_Layer_Switch_Mode%20(1).md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Coherence_Analysis.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Component_Channel_Addition_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Dual_ORIVE_Proposals.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Generation_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M3_Genesis_Space_README.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/Namespace_Collision_Fix_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/ontology_analysis.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/README_v13_Delivery.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/TSCG-M3_Ontology_Documentation.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/TSCG_M1_Architecture.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/TSCG_M2_MetaConcepts_Ontology_README.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/TSCG_Nary_Polarity_Paradigm_Shift.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/TSCG_Update_v12_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M1_CoreConcepts.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M2_Metaconcepts_v13.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/docs/M3_Philosophical_Eye.jsonld

### Ontology - M1 Extensions
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/optics/M1_Optics.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/photography/M1_Photography.jsonld

### Ontology - Poclets Documentation
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/docs/minimal_systems_engineering_frameworks.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/docs/poclet_terminology.md

### Ontology - Poclets: Cell Signaling
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/cell_signaling/M0_CellSignalingModes.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/cell_signaling/M0_CellSignalingModes_README.md

### Ontology - Poclets: Color Synthesis
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/ORIVE_Poclets_Application_Summary.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/M0_CMYK_Subtractive.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/M0_CMY_Subtractive.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/M0_ColorSynthesis_Federated.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/M0_HSL_Additive.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/docs/ColorSynthesis_Final_Summary.md

### Ontology - Poclets: Complex Chemical Synapse
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/complex_chemical_synapse/M0_ComplexChemicalSynapse.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/complex_chemical_synapse/M0_ComplexChemicalSynapse_README.md

### Ontology - Poclets: Exposure Triangle
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/exposition_triangle/M0_ExposureTriangle.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/exposition_triangle/Balance_Tradeoff_ExposureTriangle_Summary.md

### Ontology - Poclets: Fire Triangle
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/fire_triangle/M0_FireTriangle.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/fire_triangle/M0_FireTriangle_README.md

### Ontology - Poclets: Four-Stroke Engine
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/four_stroke_engine/M0_FourStrokeEngine.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/four_stroke_engine/M0_FourStrokeEngine_README.md

### Ontology - Poclets: MTG Color Wheel
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/mtg_color_wheel/M0_MTG_ColorWheel.jsonld

### Ontology - Poclets: TPACK
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/tpack/M0_TPACK.jsonld
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/tpack/TPACK_ORIVE_Validation_Analysis.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/tpack/TPACK_README.md

### Source Code - Orchestrator
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/Program.cs
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/TSCG.Orchestrator.csproj

### Source Code - Build Artifacts
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/obj/Debug/net10.0/.NETCoreApp,Version=v10.0.AssemblyAttributes.cs
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/obj/Debug/net10.0/TSCG.Orchestrator.AssemblyInfo.cs
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/obj/Debug/net10.0/TSCG.Orchestrator.GlobalUsings.g.cs
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/obj/Debug/net10.0/TSCG.Orchestrator.csproj.FileListAbsolute.txt

### Source Code - Role Prompts
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-Backend_Software_Architect.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-Compilation_Errors_Analyser.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-Frontend_Software_Architect.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-Orchestrator_Software_Architect.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-QA%20Officer.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-Reboot_Kit_Manager.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role-Simulation_Game_Engine_Architect.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Role_Reference_Documentation_Writer.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Step_1_System%20Prompt.md
- https://raw.githubusercontent.com/Echopraxium/tscg/main/src/TSCG.Orchestrator/role-prompts/Step_2_System%20Prompt.md

---

## URI Base Reference

All ontology URIs use the base:
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology
```

---

## Project Statistics

- **Total Files**: 127 files tracked
- **Ontology Files**: 
  - M3 Layer: 3 files (Genesis Space, Eagle Eye, Sphinx Eye)
  - M2 Layer: 1 file (59 metaconcepts)
  - M1 Layer: 5 files (Core + 4 domain extensions)
  - M0 Layer: 14 files (8 poclet families)
- **Documentation Files**: 67 markdown files
- **Source Code Files**: 14 files (C# .NET 10.0)
- **Automation Scripts**: 10 batch scripts

---

**Last Updated**: January 22, 2026  
**Framework Version**: TSCG v13.0.1  
**Document Version**: 2.0
