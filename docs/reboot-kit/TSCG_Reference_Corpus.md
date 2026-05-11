# TSCG Reference Corpus Catalog

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 16.0.0  
**Last Updated**: 2026-05-11

---

## 1. Foundational Architecture Documents

### 1.1 M3 Bicephalous Foundation
- `00_M3_Philosophical_Basis_Sketch.jsonld`
- `00_TSCG_M3_Bicephalous_Architecture.md`
- `00_TSCG_Map_Territory_Theoretical_Foundation.md`
- `00_Map_Territory_v1_2_Update_Summary.md`

### 1.2 Ontology Files (Meta-levels)
- `M3_GenesisSpace.jsonld` - Bicephalous foundation layer
- `M3_EagleEye.jsonld` - ASFID dimension (Territory)
- `M3_SphinxEye.jsonld` - REVOI dimension (Map)
- `M2_GenericConcepts.jsonld` - 80 atomic transdisciplinary concepts
- `M1_CoreConcepts.jsonld` - Domain extensions core concepts
- `M1_Domains.jsonld` - Knowledge field taxonomy

---

## 2. Mathematical & Formal Foundations

### 2.1 Tensor Product & Structural Grammar
- `Domain_Hybrid_Tensor_Product_5D_README.md`
- `HYBRID_FORMULAS_NOTATION_README.md`
- `Structural_Grammar_Foundation.md`
- `TSCG_Mathematical_Legitimacy_Summary.md`

### 2.2 Formula References
- `M2_FormulasReference_v15_10_0.md`
- `M2_FormulasReference_v15_10_0.json`

---

## 3. Methodologies & Pipelines

### 3.1 Analysis & Modeling
- `Poclet_Analysis_Methodology.md`
- `M2_KnowledgeField_README.md`
- `MetaconceptPair_README.md`

### 3.2 Validation & Schema
- `M0_Instances_Schema_shacl.ttl`

---

## 4. ValueSpace & Architectural Extensions

### 4.1 ValueSpace Documentation
- `TSCG_ValueSpace_User_Guide.md`
- `TSCG_ValueSpace_Quick_Reference.md`
- `TSCG_Architectural_Extensions.md`

---

## 5. Version History & Integration Reports

### 5.1 Major Version Updates
- `TSCG_v15_1_0_Integration_Report.md`
- `TSCG_v15_1_0_Final_Classification.md`
- `Domain_M2_Update_Analysis_v15_1_0.md`

### 5.2 Session Summaries
- `TSCG_Session_README_2026-03-23.md`
- `TSCG_Session_Summary_2026-04-18.md`
- `TSCG_Grammar_Extraction_Final_Report.md`

---

## 6. Terminology & Smart Prompts

- `poclet_terminology.md`
- `TSCG_Smart_Prompt_v16_0_0.md`
- `CLAUDE.md` - Collaboration guidelines

---

## 7. Repository Structure & Organization

- `TSCG_File_Tree.md`
- `README.md` - Main repository documentation
- `TO_DO.txt` - Current development backlog

---

## 8. Utility Scripts & Tools

### 8.1 Python Scripts
- `check_encoding_issues.py` - UTF-8 encoding validation
- `create_files_URIS.py` - URI generation utility
- `automated_migration_easy_instances.py` - Ontology migration tool

### 8.2 JavaScript Tools
- `generate_index.js` - Gallery index generator

### 8.3 Data Files
- `encoding_correspondances.json` - Character encoding mappings

---

## Notes

### URI Base Convention
All ontology files use the following `@base` URI:
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
```

### M1 Extensions Referencing Pattern
M1 extensions in M0 instances follow this IRI pattern:
```
M1_extensions/extension_name/M1_ExtensionName.jsonld
```
Example: `M1_extensions/biology/M1_Biology.jsonld`

### Changelog Policy
All ontology files maintain a rolling maximum of 3 most recent entries in `m2:changelog`.

### Language Convention
- **Generated files**: English
- **Conversations**: French
- **Authorship**: "Echopraxium with the collaboration of Claude AI"

---

## Document Categories Summary

| Category | File Count | Description |
|----------|------------|-------------|
| Foundational Architecture | 9 | M3 bicephalous structure, ontology meta-levels |
| Mathematical Foundations | 5 | Tensor products, formulas, structural grammar |
| Methodologies | 3 | Analysis pipelines, validation schemas |
| ValueSpace & Extensions | 3 | Architectural documentation |
| Version History | 5 | Integration reports, session summaries |
| Terminology & Prompts | 3 | Definitions, collaboration guidelines |
| Repository Structure | 3 | File organization, main docs |
| Utility Scripts | 5 | Python/JavaScript tools, data files |

**Total Reference Documents**: 36 files

---

*This corpus catalog serves as the canonical reference for TSCG framework documentation and should be consulted before any ontology modeling or framework extension work.*
