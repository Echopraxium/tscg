# TSCG Reference Documents
**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-05-26  
**Version**: 2.0.0

## Overview
Comprehensive inventory of reference materials for the TSCG (Transdisciplinary System Construction Game) framework v16.1.0.

**Legend**: ✅ Active | ⚠️ `[ARCHIVED]` | ❌ Obsolete/removed

---

## 1. Theoretical Foundation & Architecture

### 1.1 Core Philosophical Basis
- **`00_M3_Philosophical_Basis_Sketch.jsonld`** ⚠️ `[ARCHIVED]`  
  Historical sketch — ORIVE (not REVOI), Hilbert formalism, UTF-8 corruptions. Superseded by M3_GenesisGrammar.

### 1.2 Map-Territory Framework
- **`TerritoryMap_Dichotomy.md`** ✅ v16.0+ (2026-05-23)  
  Current foundational document for Map/Territory distinction (ASFID/REVOI). Supersedes the older theoretical foundation.
- **`00_TSCG_Map_Territory_Theoretical_Foundation.md`** ⚠️ `[ARCHIVED]`  
  v1.2 (Jan 2026) — ORIVE, Hilbert space ℂ⁵, "not yet implemented". Superseded by TerritoryMap_Dichotomy.md.

### 1.3 Conceptual Foundations (docs/CoreHypotheses/)
- **`_00_TSCG_as_StereoscopicGlasses.md`** ✅ — Primary metaphor: TSCG as epistemic stereopsis
- **`_01_Narcissus_and_Icarus_as_Safeguards.md`** ✅ — Epistemological safeguards
- **`SystemicEsperanto.md`** ✅ — TSCG as transdisciplinary language
- **`LegoTechnic_Modularity.md`** ✅ — Modularity and composability principles
- **`Archetypes_as_CrossCultural_Artifacts.md`** ✅ — Cross-cultural archetype patterns
- **`CredibilityAccretion_Process.md`** ✅ — Intersubjective validation process
- **`MultisubjectiveScoreEvaluationProtocol.md`** ✅ — Score evaluation methodology

---

## 2. Mathematical Formalism & Notation

### 2.1 Structural Grammar Foundation (ontology/StructuralGrammar/)
- **`Structural_Grammar_Foundation.md`** ✅  
  Lambek calculus-based structural grammar. Replaces tensor product formalism.
- **`Structural_Grammar_Foundation_README.md`** ✅
- **`TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`** ✅
- **`TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md`** ✅
- **`Braille_StructuralGrammar.pdf`** ✅ — Structural grammar applied to Braille encoding

### 2.2 Formula References ⚠️ `[ARCHIVED]`
- **`M2_FormulasReference_v15_10_0.md`** ⚠️ `[ARCHIVED]`  
  v15.10.0 — all formulas use deprecated ⊗ notation. TODO: generate from M2_GenericConcepts.jsonld via script.
- **`M2_FormulasReference_v15_10_0.json`** ⚠️ `[ARCHIVED]`  
  Doublon JSON du précédent. Même verdict.

### 2.3 KnowledgeField Documentation ⚠️ Pending rewrite
- **`M2_KnowledgeField_README.md`** ⚠️ `[ARCHIVED]`  
  UTF-8 corruption massive, Hilbert/SVD formalism, références invalides. TODO: réécriture en notation Lambek.

---

## 3. Methodology & Pipelines

### 3.1 Instance Analysis
- **`Poclet_Analysis_Methodology.md`** ✅  
  Step-by-step methodology for analyzing systems as TSCG instances.

### 3.2 Architectural Extensions
- **`TSCG_Architectural_Extensions.md`** ✅  
  Architectural patterns and extension mechanisms.

### 3.3 Concept Documentation
- **`MetaconceptPair_README.md`** ✅
- **`M2_KnowledgeField_README.md`** ⚠️ `[ARCHIVED]` → see §2.3
- **`poclet_terminology.md`** ✅

---

## 4. Ontology Files (JSON-LD)

### 4.0 M3 Apex — Mathematical Foundation
- **`M3_GrammarFoundation.jsonld`** ✅ v2.1.0  
  Apex ontology — Lambek calculus, operators ×/+/|, type system 𝕋₀/𝕋₁/𝕋₂, `m3:grammar_foundation:` namespace
- **`M3_GrammarFoundation_README.md`** ✅ v1.3.0

### 4.1 M3 Meta-Level (Foundation)

| File | Version | Role |
|---|---|---|
| `M3_EagleEye.jsonld` | 2.8.0 | Territory Grammar Gt — ASFID (×), `m3:eagle_eye:` |
| `M3_EagleEye_README.md` | 2.8.0 | |
| `M3_SphinxEye.jsonld` | 3.5.0 | Map Grammar Gm — REVOI (+), `m3:sphinx_eye:` |
| `M3_SphinxEye_README.md` | 3.5.0 | |
| `M3_BicephalousPerspective.jsonld` | 1.1.0 | Stereopsis Grammar Gs — {T,_^,_$} (\|), `m3:bicephalous:` |
| `M3_BicephalousPerspective_README.md` | 1.1.0 | |
| `M3_GenesisGrammar.jsonld` | 4.2.0 | Intégrateur — importe les 4 grammaires |
| `M3_GenesisGrammar_README.md` | 4.2.0 | |

**Import hierarchy:**
```
M3_GrammarFoundation (apex)
  ↑ imported by
  ├── M3_EagleEye      (Gt, ×)
  ├── M3_SphinxEye     (Gm, +)
  ├── M3_BicephalousPerspective (Gs, |)
  └── M3_GenesisGrammar (integrator)
```

**Obsolete:** `M3_GenesisSpace.jsonld` → renommé `M3_GenesisGrammar.jsonld`

### 4.2 M2 Meta-Level (Generic Concepts)
- **`M2_GenericConcepts.jsonld`** ✅ v16.10.8  
  75 atomic GenericConcepts across 9 families. Lambek formalism. `m3:ontologyType: GenericConcepts`.
- **`M2_GenericConcepts_README.md`** ✅ v16.10.8

### 4.3 M1 Meta-Level (Domain Extensions)

#### Core Files
- **`M1_CoreConcepts.jsonld`** ✅ v2.4.0  
  9 GenericConceptCombos (Cascade, Oscillator, Processor, LALI, ButterflyEffect, Propagation, Narration, StratifiedDissipation, CascadeAmplification). Namespace umbrella `m1:`.
- **`M1_CoreConcepts_README.md`** ✅ v2.4.0
- **`M1_Domains.jsonld`** ✅ v1.2.0 — 20 domain entries. Namespace `m1:domain:`.
- **`M1_Domains_README.md`** ✅ v1.2.0

#### M1 Extension Files (namespace: `m1:extension:<domain>:`)

| Extension | File | Version | KFCC | Fm1m2 |
|---|---|---|---|---|
| Biology | `M1_Biology.jsonld` | 1.1.0 | 1 | ✅ |
| Chemistry | `M1_Chemistry.jsonld` | 1.1.0 | 15 | ✅ |
| Economics | `M1_Economics.jsonld` | 1.0.0 | 14 | ✅ |
| Education | `M1_Education.jsonld` | 1.0.0 | 10 | ✅ |
| Electronics | `M1_Electronics.jsonld` | 1.0.1 | 17 | ✅ |
| EnergyGenerators | `M1_EnergyGenerators.jsonld` | 1.0.0 | 1 | ✅ |
| Geology | `M1_Geology.jsonld` | 1.0.0 | 8 | ✅ |
| Music | `M1_music.jsonld` | 1.0.0 | 8 | ✅ |
| Mythology | `M1_Mythology.jsonld` | 1.1.0 | 11 | ✅ |
| Optics | `M1_Optics.jsonld` | 1.1.0 | 9 | ✅ |
| Photography | `M1_Photography.jsonld` | 1.1.0 | 11 | ✅ |
| Physics | `M1_Physics.jsonld` | 1.1.0 | 6 | ✅ |
| SystemicModeling | `M1_SystemicModeling.jsonld` | 1.1.0 | 4+40 | ✅ |

**Template README:** `M1_Extension_README_TEMPLATE.md` — base pour créer les 13 READMEs d'extensions

**Convention KFCC:**
```json
"@type": ["owl:Class", "m2:DomainConceptCombo"],
"rdfs:subClassOf": "m2:DomainConceptCombo",
"m1:structuralGrammarFormula": "Fm1m2(<Domain>, <formula>)"
```

### 4.4 M0 Schema & Grammar
- **`M0_Instances_Schema_shacl.ttl`** ✅  
  SHACL grammar — 9 mandatory constraints. Validates all M0 instance types.
- **`M0_POCLET_TEMPLATE.jsonld`** ✅ — Template for new poclet instances
- **`M0_InstanceSimulations.jsonld`** ✅ — Catalog of simulation instances
- **`M0_InstanceSimulation_UXControls.jsonld`** ✅ — UX controls catalog (mandatory for simulation creation)

---

## 5. M0 Instances

**Score Convention (Option B — MANDATORY):** Scores au niveau racine du nœud `owl:Ontology` :
```json
"A_score": {"@value": "0.85", "@type": "xsd:float"}
```
**SpectralClass** : Coherent (δ₁<0.05) | OnCriticalLine (0.05≤δ₁<0.15) | Incoherent (δ₁≥0.15)
**δ₁ formula** : `|ASFID_mean − REVOI_mean| / √2`

---

### 5.1 Poclets (instances/poclets/) — 26 validated

| Poclet | Domain | δ₁ | SpectralClass | Simulation |
|---|---|---|---|---|
| AdaptativeImmuneResponse | Biology | — | pending | — |
| BloodPressureControl | Physiology | — | pending | — |
| ButterflyMetamorphosis | Biology | — | pending | — |
| CellSignalingModes | Biology | — | pending | — |
| ColorSynthesis (RGB/HSL/CMY/CMYK) | Art | ✓ | pending | static/ |
| ComplexChemicalSynapse | Neuroscience | ✓ | pending | pygame |
| CounterPoint | Music | ✓ | pending | static/ (Tone.js) |
| ExposureTriangle | Photography | ✓ | pending | static/ |
| FireTriangle | Chemistry | ✓ | pending | static/ |
| FourStrokeEngine | Engineering | ✓ | pending | sim/ + static/ |
| Kidneys | Physiology | ✓ | pending | — |
| KindlebergerMinsky | Economics | — | pending | sim/ + static/ |
| MtgColorWheel | Game Theory | — | pending | sim/ + static/ |
| NakamotoConsensus | Blockchain | — | pending | static/ |
| NuclearReactorsTypology | Nuclear Engineering | ✓ | pending | static/ |
| PhaseTransition | Physics/Chemistry | — | pending | sim/ + static/ |
| PlateTectonics | Geology | — | pending | _static/ |
| Ptoe (Periodic Table) | Chemistry | ✓ | pending | static/ (BabylonJS) |
| Raas | Physiology | ✓ | pending | — |
| Theremin | Electronics | — | pending | _static/ (stub) |
| Tpack | Pedagogy | — | pending | pygame |
| Transistor | Electronics | ✓ | pending | sim/ + static/ |
| TrophicPyramid | Ecology | — | pending | sim/ + static/ |
| TvTestPattern | Art/Electronics | — | pygame |
| Vco | Electronics | — | sim/ + static/ |
| Yggdrasil | Mythology | — | — |

### 5.2 SystemicFrameworks (instances/systemic-frameworks/)

| Framework | Domain | A | S | F | It | D | R | E | V | O | Im | δ₁ | SpectralClass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Vsm** | Cybernetics | 0.95 | 0.98 | 0.85 | 0.98 | 0.88 | 0.95 | 0.92 | 0.70 | 0.82 | 0.85 | 0.057 | OnCriticalLine |
| **Triz** | Innovation | 1.0 | 1.0 | 0.80 | 1.0 | 0.60 | 1.0 | 0.80 | 1.0 | 1.0 | 1.0 | 0.057 | OnCriticalLine |

**Notes :**
- TRIZ : scores normalisés depuis l'échelle Altshuller 0-5 (÷5). V=0.60 = F=4/5 (flux unidirectionnel sans boucle)
- VSM : V=0.70 (vérification qualitative uniquement, pas de métriques quantitatives)

### 5.3 SymbolicSystemGrammars (instances/symbolic-system-grammars/)

| Grammar | Domain | A | S | F | It | D | R | E | V | O | Im | δ₁ | SpectralClass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **IChing** | Philosophy/Divination | 0.85 | 0.97 | 0.72 | 0.91 | 0.80 | 0.95 | 0.88 | 0.50 | 0.78 | 0.90 | 0.034 | Coherent |

**Note :** V=0.50 est un trait **constitutif** du SSG (arbitration symbolique, non empirique) — pas un défaut de modélisation.

### 5.4 TscgTools (instances/tscg-tools/)

| Tool | v | Stack | A | S | F | It | D | R | E | V | O | Im | δ₁ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **TscgOntologyExplorer** | 1.0 | ElectronJS+pyoxigraph | 0.85 | 0.90 | 0.80 | 0.85 | 0.70 | 0.80 | 0.90 | 0.85 | 0.80 | 0.75 | 0.022 | Coherent |
| **TscgPocletGenerator** | 1.0 | PySide6+RAG | 0.88 | 0.92 | 0.90 | 0.93 | 0.82 | 0.90 | 0.92 | 0.84 | 0.88 | 0.93 | 0.096 | OnCriticalLine |
| **TscgPocletMiner** | 1.1 | ElectronJS+WASM RAG | 0.75 | 0.90 | 0.88 | 0.85 | 0.75 | 0.90 | 0.88 | 0.92 | 0.90 | 0.82 | 0.042 | Coherent |
| **TscgOntologyAPIServer** | stub | — | — | — | — | — | — | — | — | — | — | — | pending |

---

## 6. Version History & Classification

### 6.1 Version Reports
- **`TSCG_v15_1_0_Final_Classification.md`** ✅
- **`Domain_M2_Update_Analysis_v15_1_0.md`** ✅
- **`TSCG_Session_README_2026-03-23.md`** ✅

---

## 7. Project Management & Corpus

### 7.1 Project Organization
- **`README.md`** ✅ — Main project README
- **`TSCG_File_Tree.md`** ✅ v16.1.0 (2026-05-23) — Complete file tree
- **`TO_DO.txt`** ✅ — Current development tasks
- **`CLAUDE.md`** ✅ — Guidelines for Claude AI collaboration
- **`TSCG_Project_Corpus.md`** ✅ — Artifact inventory

### 7.2 Smart Prompts
- **`TSCG_Smart_Prompt_v16_1_0.md`** ✅ — Current smart prompt for Claude AI

---

## 8. Utilities & Scripts

### 8.1 Migration Tools
- **`automated_migration_easy_instances.py`** ✅ — Automated migration for M0 instances

### 8.2 Gallery Generation
- **`generate_index.js`** ✅ — Node.js gallery index generator

### 8.3 RAG Pipeline
- `create_tscg_rag.py`, `rebuild_corpus.py`, `restore_rag.js` — RAG pipeline for TscgPocletMiner

---

## 9. Pending / TO_DO (from current session 2026-05-26)

| Task | Priority | Notes |
|---|---|---|
| Créer 13 READMEs extensions M1 | High | Template: `M1_Extension_README_TEMPLATE.md` |
| Corpus réalignement 26 poclets | High | Namespaces, scores Option B, GenesisGrammar |
| Analyser docs conceptuels (.md) | Medium | CoreHypotheses, SmartPrompts, méthodologies |
| `generate_formulas_reference.js` | Medium | Script auto depuis M2_GenericConcepts.jsonld |
| Réécrire `M2_KnowledgeField_README.md` | Medium | Lambek, UTF-8 propre |
| Stub `M0_TscgOntologyAPIServer.jsonld` | Low | Phase 3 — créer le M0 quand implémenté |
| Ajouter Mathematics/Anthropology à M1_Domains | Low | Nœuds manquants |

---

## 10. Document Conventions

### 10.1 URI Base
```
@base: "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
```

### 10.2 Namespace Hierarchy
```
m3: → M3_GenesisGrammar.jsonld#           (M3 umbrella)
  m3:eagle_eye:       → M3_EagleEye
  m3:sphinx_eye:      → M3_SphinxEye
  m3:bicephalous:     → M3_BicephalousPerspective
  m3:grammar_foundation: → M3_GrammarFoundation

m1: → M1_CoreConcepts.jsonld#             (M1 umbrella)
  m1:domain:          → M1_Domains
  m1:extension:<domain>: → M1 extensions
```

### 10.3 M1 Extension References
```
"M1_extensions/<extension_name>/M1_<ExtensionName>.jsonld"
```
Example: `"M1_extensions/biology/M1_Biology.jsonld"`

### 10.4 Formula Convention
```
M2 GenericConcepts:       "formula": "S × It × D × F | V + O"
M1 GenericConceptCombos:  "m1:structuralGrammarFormula": "Fm2(Process, Step, Trajectory)"
M1 KFConceptCombos:       "m1:structuralGrammarFormula": "Fm1m2(<Domain>, S × It × D)"
```

### 10.5 Score Aliases (Option B — MANDATORY)
```json
"A_score": {"@id": ".../M0_Poclet#scoreA", "@type": "xsd:float"}
```
Applies to: A_score, S_score, F_score, It_score, D_score, R_score, E_score, V_score, O_score, Im_score

### 10.6 Author Attribution
```
"Author": "Echopraxium with the collaboration of Claude AI"
```

### 10.7 Changelog Policy
Maximum 3 most recent entries in `m2:changelog` fields.

---

## 11. Corpus Statistics

| Category | Count | Status |
|---|---|---|
| M3 Ontologies | 5 .jsonld + 5 README | ✅ Tous corrigés (v2026-05-26) |
| M2 Ontology | 1 .jsonld + 1 README | ✅ Corrigé |
| M1 Extensions | 15 .jsonld + 2 README + 1 template | ✅ Tous migrés |
| M0 Poclets | 26 | ⚠️ Corpus réalignement en attente |
| M0 SystemicFrameworks | 2 (VSM + TRIZ) | ✅ Analysés + corrigés |
| M0 SymbolicSystemGrammars | 1 (IChing) | ✅ Analysé + corrigé |
| M0 TscgTools | 3 actifs + 1 stub | ✅ 3 analysés + corrigés |
| Documents théoriques | 7 | ✅ |
| Documents méthodologie | 5 | ✅ |
| Scripts/outils | 8+ | ⚠️ Non analysés |
| ARCHIVED | 6 | Marqués |
| **TOTAL actifs** | **~85** | |

---

## 12. Related Resources

### 12.1 External Publications
- **Zenodo DOI**: 10.5281/zenodo.18471860 (v3.0)
- **GitHub Repository**: https://github.com/Echopraxium/tscg
- **GitHub Pages**: https://echopraxium.github.io/tscg/

### 12.2 Current Development Version
- **Framework Version**: v16.1.0
- **Research Article**: v5.0 (preprint draft)

---

*TSCG_Reference_Corpus.md v2.0.0 — Updated 2026-05-26 during corpus analysis session with Claude AI*
