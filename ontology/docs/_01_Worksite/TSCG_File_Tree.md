# 📁 TSCG Framework - Complete File Tree

**Date:** 2026-07-13
**Framework Version:** TSCG v16.17.0 (M2) — SC-1 Functional Grammar Model
**Total Files:** ~964

---

## 📊 Project Statistics

**Ontology Files:**
- M3 Layer: 6 files (M3_GrammarFoundation apex, M3_EagleEye, M3_GenesisGrammar, M3_SphinxEye, **M3_BicephalousPerspective NEW**) + README files + StructuralGrammar/ documentation folder
- M2 Layer: 1 main file (M2_GenericConcepts) + 1 standalone (M2_Calibration) + archived versions in docs/
- M1 Layer: 2 root files (M1_CoreConcepts, M1_Domains) + 13 domain extensions (biology, chemistry, economics, education, electronics, energy_generators, geology, music, mythology, optics, photography, physics, system_modeling) — @base factorised in all files
- M0 Layer: **26 poclets** (instances/poclets/) + **3 TscgTools active + 1 stub** (instances/tscg-tools/) + **2 systemic frameworks** (Vsm, Triz) + 1 symbolic grammar (IChing)

**Documentation:** ~150 files (+ docs/CoreHypotheses/ NEW)
**Source Code:** extensive `src/tscg/` Python package
**Scripts & Tools:** 40+ files
**Root & Config:** 10 files

**Total:** ~964 files

---

## 🆕 What's New

### v16.17.0 (2026-07-13) — Current — **SC-1 · FUNCTIONAL GRAMMAR MODEL**

**A combo's formula IS a function signature.**

```
Fm2   : GenericConcept²⁺            →  m2:GenericConceptCombo   (≥ 2 concepts)
Fm1m2 : Domain⁺ , GenericConcept⁺   →  m2:DomainConceptCombo    (≥ 1 domain AND ≥ 1 concept)
```

`Fm2`/`Fm1m2` are **functions, not functors**: emergence is *non-compositional* (the
arguments are **combined, not associated**), and a functor must *preserve* composition.
A combo therefore has **no monoidal formula and no monoidal expansion**. Monoidal
formulas (`×` Gt, `+` Gm, `|` Gs) belong to **atoms only**.

- 🆕 **`ontology/StructuralGrammar/Functional_Grammar_Model.md`** — the foundation note (11 decisions)
- 🆕 **`ontology/docs/_01_Worksite/`** — worksite maps and sub-worksite handovers (SC-0 … SC-9)
- 🆕 **`ontology/cli-tools/`** — check/migrate tooling **relocated** here from `cli_tools/`, plus the
  **acceptance gate** (`run_all_layers.py` + `golden_values.json`). Each SHACL grammar lives **next to
  the script that uses it** (`check-M0/`, `check-M1/`) — **one copy, never two**: `find_schema()` returns
  the first match, so a stray duplicate would silently shadow the real one.
- ✅ **RENAME (hard)** `m2:KnowledgeFieldConceptCombo` → **`m2:DomainConceptCombo`** (26 files, 304 occurrences)
  — and **re-defined**: membership is now **domain qualification** (an `Fm1m2` formula), not "parents from distinct epistemological domains"
- ✅ **`m2:producingFunction`** (new M2 property) declares each combo class's function
- ✅ **DEPRECATED `m2:morphism_emergence`** — it declared emergence to be a category-theoretic *morphism*, and was the **root** from which `⊗⇒`, `lattice_join(dims(parents))`, the "union of the parent type sets" clause and `m1:structuralGrammarFormulaExpanded` all descended. A morphism composes; an emergence does not.
- ✅ **M3 correction** (`M3_GrammarFoundation` v2.4.0) — `Fm1m2` was defined as *"crossing the M1/M2 boundary"*. **That was the root error**: it propagated into `M1_CoreConcepts` v1.4.0, which "corrected" `Propagation`/`CascadeAmplification` `Fm2`→`Fm1m2` *"because parent m1:Cascade is M1"*. `Φ`/`Ψ` remain **genuine morphisms** — the family is **split, not purged**.
- ✅ **SHACL v1.1.0** — `ComboFormulaShape`, `NoMonoidalExpansionShape`; SHAPE 3 retargeted
- 📊 **163 M1 errors exposed** — the SC-6 backlog, **measured on the real repository**
  (`DCC006`=127 monoidal operator in a signature · `DCC010`=18 unregistered Domain ·
  `EXP001`=12 retired expansion · guards=5 · `DCC008`=1). ⚠️ An earlier estimate of **126**
  came from a partial sandbox reconstruction and was **wrong** — only the repo counts.
- 🔍 **Four PHANTOM DOMAINS** found by `DCC010`: `Music` (the registry says *MusicTheory*),
  `SystemicModeling` (*SystemsTheory*), `EnergyGenerators` (absent), `Cascade` (not a domain at
  all). Formulas were qualifying concepts by domains registered nowhere — structurally
  invisible until a validator compared the formula against `M1_Domains.jsonld`.
- 🚦 **Acceptance gate**: `ontology/cli-tools/run_all_layers.py` + `golden_values.json`.
  **163 is GREEN. 162 is RED. 164 is RED.** A count that *drops* is as suspicious as one that
  rises: either a deliberate fix (`--update-golden`, and the drop is recorded) or a validator
  that stopped biting. A silently shrinking error count is the most dangerous signal here —
  **it looks like progress**.
- ⚠️ **Finding for SC-5**: ~256 of the 479 pre-existing violations are a **SHACL bug**, not data defects — `sh:targetClass` follows subclasses, so SHAPE 2 and SHAPE 3 validate every extension combo **twice**, with mutually exclusive requirements

**Version bumps**: M3_GrammarFoundation 2.2.0→**2.4.0** · M2_GenericConcepts 16.16.0→**16.17.0** ·
M1_CoreConcepts 2.6.1→**2.7.0** · M1_Schema_shacl 1.0.0→**1.1.0** · check_M1 1.0.0→**2.0.0**

---

### v16.1.0 (2026-05-23)

**SCORE CONVENTION REFORM + CORPUS EXPANSION + TOOLING**

- ✅ **Convention Option B** — Score alias disambiguation across ALL 36 M0 instances:
  - `A`, `S`, `F`, `It`, `D`, `R`, `E`, `V`, `O`, `Im` (short aliases → MonoidalTypes) replaced by
  - `A_score`, `S_score`, `F_score`, `It_score`, `D_score`, `R_score`, `E_score`, `V_score`, `O_score`, `Im_score` (→ `m0:score*` DatatypeProperties, distinct from MonoidalTypes)
  - TRIZ scores normalized from 0–5 scale to 0–1 (÷5); δ₁ recalculated
  - 36 `.jsonld` + 31 `_README.md` migrated (4 lots)
- ✅ **NEW poclets:** `Ptoe/` (Periodic Table), `PlateTectonics/`, `NuclearReactorsTypology/`
- ✅ **NEW poclet stub:** `Theremin/` (`_static/` only)
- ✅ **NEW systemic framework:** `instances/systemic-frameworks/Triz/` (TRIZ icosahedron)
- ✅ **NEW TscgTool stubs:** `instances/tscg-tools/TscgOntologyAPIServer/` (Phase 3 planned)
- ✅ **NEW TscgTools modeled:** TscgOntologyExplorer + TscgPocletGenerator + TscgPocletMiner (m3:TscgTool instances)
- ✅ **NEW `docs/CoreHypotheses/`** — 8 theoretical foundation documents
- ✅ **NEW `ontology/TSCG_InstanceGrammar/`** — SHACL grammar + migration tools (reorganized from `ontology/` root)
- ✅ **NEW `ontology/InstanceSimulations/`** — UX knowledge base (4 files, mandatory for simulation creation)
- ✅ **NEW `ontology/M3_BicephalousPerspective.jsonld`** + README
- ✅ **NEW `ontology/OntologyModeling_Guidelines.md`**
- ✅ **UPDATED `ontology/StructuralGrammar/`** — 2 new files (PotentialRefinements, MonoidalOperators README)
- ✅ **NEW `instances/tscg-tools/TscgOntologyExplorer/dev/tscg-python-bridge/`:**
  - Phase 2: `TscgStore` (pyoxigraph named-graph triple store) in `bridge_server.py`
  - `/corpus/*` endpoints (load, list, sparql, reload)
  - `_run_tests.py` interactive test runner (menu 1–4)
  - `tests/` full test suite (58 tests: test_expand_iri, test_tscg_store, test_endpoints)
  - `requirements.txt` updated with `pyoxigraph>=0.5.0`
  - `_plugins_setup.bat` updated with pyoxigraph install + optional test run
- ✅ **NEW `instances/tscg-tools/TscgOntologyExplorer/docs/UserManual.md`**
- ✅ **NEW `docs/papers/preprints/TSCG_Research_Paper_Draft_v5.md`** (v4.0 on Zenodo DOI:10.5281/zenodo.18471860)
- ✅ **NEW `docs/papers/preprints/HAL/`** folder
- ✅ **NEW `domain_format_fix_backups/`** backup folder
- ✅ Smart Prompt v16.0.0 added to `docs/reboot-kit/SmartPrompts/`

### v16.0.0 (2026-05-13)

**FORMALISM REFORM: Tensor Product → Structural Grammar (Lambek Calculus)**

- ✅ **NEW** `ontology/M3_GrammarFoundation.jsonld` — apex ontology, 6 indexed operators, type system 𝕋₀/𝕋₁/𝕋₂/𝕄₀
- ✅ **RENAMED** `M3_GenesisSpace.jsonld` → `M3_GenesisGrammar.jsonld` (v4.0.0)
- ✅ **UPDATED** `M3_EagleEye.jsonld` (v2.5.0) + `M3_SphinxEye.jsonld` (v3.3.0)
- ✅ **UPDATED** `M2_GenericConcepts.jsonld` (v15.12.0) — `hasTensorFormula` → `hasStructuralFormula`
- ✅ **NEW** `ontology/StructuralGrammar/` — Lambek Calculus documentation
- ✅ **NEW** `.claude/skills/tscg-tensor-to-structural-grammar-migration/`

### v15.10.1 (2026-03-23)
- New poclets: `CounterPoint/` + `NakamotoConsensus/`
- New TSCG tool: `TscgPocletMiner/`; New M1 extension: `music/`
- New CLI tool: `cli_tools/generate_index-html/`

### v15.10.0 (2026-03-16)
- New poclets: `TrophicPyramid/` + `TvTestPattern/`
- New TSCG tools: `TscgPocletGenerator/` + `TscgPocletExplorer/` stub
- New standalone M2 file: `M2_Calibration.jsonld`

### v15.9.0 (2026-03-01)
- New M1 extension: `economics/`; New poclet: `KindlebergerMinsky/`

---

## 🏛️ M3 Layer - Genesis Grammar (Structural Grammar Foundation)

### Main ontology/ — Import hierarchy
```
M3_GrammarFoundation.jsonld  ← APEX (no imports)
        ↓ imported by
M3_EagleEye.jsonld  +  M3_SphinxEye.jsonld
        ↓ imported by
M3_GenesisGrammar.jsonld  +  M3_BicephalousPerspective.jsonld  ← NEW
        ↓ imported by
M2_GenericConcepts.jsonld → M1 → M0
```

- [M3_GrammarFoundation.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GrammarFoundation.jsonld) — APEX, 6 operators, type system 𝕋₀/𝕋₁/𝕋₂/𝕄₀, intersubjectiveBenchmark
- [M3_GrammarFoundation_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GrammarFoundation_README.md)
- [M3_EagleEye.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_EagleEye.jsonld) v2.5.0 — Territory Grammar Gt, primitive types {A,S,F,I,D}
- [M3_EagleEye_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_EagleEye_README.md)
- [M3_SphinxEye.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld) v3.3.0 — Map Grammar Gm, primitive types {R,E,V,O,I}
- [M3_SphinxEye_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_SphinxEye_README.md)
- [M3_GenesisGrammar.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld) v4.0.0 *(renamed from M3_GenesisSpace)* — bicephalous hub
- [M3_GenesisGrammar_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisGrammar_README.md)
- [M3_BicephalousPerspective.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_BicephalousPerspective.jsonld) **NEW** — Eagle Eye ⊕ Sphinx Eye unified perspective
- [M3_BicephalousPerspective_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_BicephalousPerspective_README.md) **NEW**
- [OntologyModeling_Guidelines.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/OntologyModeling_Guidelines.md) **NEW**
- [TSCG_Reference_Corpus.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_Reference_Corpus.md) **NEW**

### ontology/StructuralGrammar/ (updated)
- [Structural_Grammar_Foundation.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/Structural_Grammar_Foundation.md)
- [Structural_Grammar_Foundation_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/Structural_Grammar_Foundation_README.md)
- [TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md)
- [TSCG_Mathematical_Legitimacy_Summary.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/TSCG_Mathematical_Legitimacy_Summary.md)
- [TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md)
- [StructuralGrammar_MonoidalOperators_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/StructuralGrammar_MonoidalOperators_README.md) **NEW**
- [PotentialRefinements_MonoidalOperators.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/PotentialRefinements_MonoidalOperators.md) **NEW**
- [_00_Session_Claude_GrammaireStructurelle.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/_00_Session_Claude_GrammaireStructurelle.md)
- [Functional_Grammar_Model.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/StructuralGrammar/Functional_Grammar_Model.md) **NEW (SC-1)** — `Fm2`/`Fm1m2` as functions; formula-as-signature; the `⊗⇒` purge

### ontology/InstanceSimulations/ **NEW — UX knowledge base for simulations**
- [M0_InstanceSimulations.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/InstanceSimulations/M0_InstanceSimulations.jsonld) — Catalog of all instance simulations
- [M0_InstanceSimulations_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/InstanceSimulations/M0_InstanceSimulations_README.md)
- [M0_InstanceSimulation_UXControls.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld) — UX controls catalog (mandatory consultation during simulation creation)
- [M0_InstanceSimulation_UXControls_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md)

### ontology/TSCG_InstanceGrammar/ **NEW — SHACL grammar + migration tools**
- [M0_Instances_Schema.shacl.ttl](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl) — SHACL grammar v1.0 FINAL (9 mandatory constraints)
- [M0_POCLET_TEMPLATE.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/M0_POCLET_TEMPLATE.jsonld) + [M0_TEMPLATES_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/M0_TEMPLATES_README.md) + [M0_TEMPLATES_USAGE_GUIDE.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/M0_TEMPLATES_USAGE_GUIDE.md)
- [TSCG_Grammar_Extraction_Final_Report.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/TSCG_Grammar_Extraction_Final_Report.md)
- [MIGRATION_GUIDE_It_Im.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/MIGRATION_GUIDE_It_Im.md) — It (Information/Territory) vs Im (Interoperable/Map) disambiguation guide
- [RECAPITULATIF_EXECUTIF.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/TSCG_InstanceGrammar/RECAPITULATIF_EXECUTIF.md)
- **Migration scripts:** `automated_migration_easy_instances.py`, `fix_domain_format.py`, `migrate_m1_namespaces.py`, `migrate_simulation_titles.py`, `audit_m1_namespaces.py`, `diagnose_scores.py`, `validate_m0_instance.py`, `validate_context_urls.py`

### ontology/Ref/ (reference copies)
- M2_GenericConcepts (2026-02-17) / M2_MetaConcepts_Ref / M3_GenesisSpace_Ref (archived)

---

## 🌐 M2 Layer - Universal GenericConcepts

- [M2_GenericConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld) v15.12.0 — 75+ atomic GenericConcepts; `hasStructuralFormula`
- [M2_GenericConcepts_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M2_GenericConcepts_README.md)
- [M2_Calibration.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M2_Calibration.jsonld) — standalone Calibration metaconcept (A ⊗ F ⊗ It ⊗ D)

### ontology/sparql/ + ontology/tools/ + ontology/docs/
*(unchanged from v16.0.0 — see archived documentation)*

---

## 🎯 M1 Layer - Domain Extensions

### Root (ontology/)
- [M1_CoreConcepts.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld) + [M1_CoreConcepts_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_CoreConcepts_README.md)
- [M1_Domains.jsonld](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_Domains.jsonld) + [M1_Domains_README.md](https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_Domains_README.md) — 19 registered domains

### Domain Extensions (ontology/M1_extensions/)

| Extension | File | Notes |
|---|---|---|
| **biology** | M1_Biology.jsonld | |
| **chemistry** | M1_Chemistry.jsonld + .ttl | |
| **economics** | M1_Economics.jsonld + README | |
| **education** | M1_Education.jsonld + README | |
| **electronics** | M1_Electronics.jsonld + README | |
| **energy_generators** | M1_EnergyGenerators.jsonld | |
| **geology** | M1_Geology.jsonld | |
| **music** | M1_Music.jsonld | |
| **mythology** | M1_Mythology.jsonld + README | |
| **optics** | M1_Optics.jsonld | |
| **photography** | M1_Photography.jsonld | |
| **physics** | M1_Physics.jsonld + README | |
| **system_modeling** | M1_SystemicModeling.jsonld | |

---

## 📦 M0 Layer - Instances

### instances/poclets/ — 26 validated poclets

| Folder | Domain | Scores | Simulation |
|---|---|---|---|
| AdaptativeImmuneResponse | Biology | — | — |
| BloodPressureControl | Physiology | — | — |
| ButterflyMetamorphosis | Biology | — | — |
| CellSignalingModes | Biology | — | — |
| ColorSynthesis/ | Art (federated: RGB, HSL, CMY, CMYK) | ✓ | static/ |
| ComplexChemicalSynapse | Neuroscience | ✓ | pygame |
| CounterPoint | Music | ✓ | static/ (Tone.js) |
| ExposureTriangle | Photography | ✓ | static/ |
| FireTriangle | Chemistry | ✓ | static/ |
| FourStrokeEngine | Engineering | ✓ | sim/ + static/ |
| Kidneys | Physiology | ✓ | — |
| KindlebergerMinsky | Economics | — | sim/ + static/ |
| MtgColorWheel | Game Theory | — | sim/ + static/ |
| NakamotoConsensus | Blockchain | — | static/ |
| NuclearReactorsTypology | Nuclear Engineering | ✓ | static/ |
| PhaseTransition | Physics/Chemistry | — | sim/ + static/ |
| PlateTectonics | Geology | — | _static/ |
| Ptoe | Chemistry | ✓ | static/ (BabylonJS) |
| Raas | Physiology | ✓ | — |
| Theremin | Electronics | — | _static/ stub |
| Tpack | Pedagogy | — | pygame |
| Transistor | Electronics | ✓ | sim/ + static/ |
| TrophicPyramid | Ecology | — | sim/ + static/ |
| TvTestPattern | Art/Electronics | — | pygame |
| Vco | Electronics | — | sim/ + static/ |
| Yggdrasil | Mythology | — | — |

### instances/symbolic-system-grammars/
- **Iching/** — M0_IChing.jsonld + README (64 hexagrams, m3:SymbolicSystemGrammar)

### instances/systemic-frameworks/
- **Vsm/** — M0_Vsm.jsonld + README + _sim/ (Viable System Model, m3:SystemicFramework)
- **Triz/** — M0_Triz.jsonld + README + Triz_Description.md + static/ (TRIZ icosahedron, m3:SystemicFramework) **NEW**
  - Scores normalized 0–5 → 0–1: ASFID mean=0.88, REVOI mean=0.96, δ₁=0.057 (OnCriticalLine)

### instances/tscg-tools/

| Tool | Status | Type | Key Files |
|---|---|---|---|
| **TscgOntologyExplorer/** | Active v1.0 | m3:TscgTool | ElectronJS browser/editor |
| **TscgOntologyAPIServer/** | Stub (Phase 3) | m3:TscgTool | `_open_cmd_window.bat` only |
| **TscgPocletGenerator/** | Active v1.0 | m3:TscgTool | PySide6 + RAG pipeline |
| **TscgPocletMiner/** | Active v1.2 | m3:TscgTool | ElectronJS 5-round wizard |

#### TscgOntologyExplorer/ — detail

```
TscgOntologyExplorer/
├── M0_TscgOntologyExplorer.jsonld / _README.md
├── PLUGINS_README.md
├── _00_run.bat / _plugins_setup.bat (updated: pyoxigraph + test runner)
├── docs/
│   └── UserManual.md                        ← NEW
└── dev/tscg-python-bridge/
    ├── bridge_server.py                     ← Phase 2: TscgStore + /corpus/* endpoints
    ├── requirements.txt                     ← + pyoxigraph>=0.5.0
    ├── _run_tests.py                        ← NEW interactive test runner (menu 1–4)
    ├── _00_run_tests.bat
    └── tests/                               ← NEW full test suite (58 tests)
        ├── conftest.py
        ├── test_expand_iri.py               ← 18 tests (_expand_iri strategies 1/2/3)
        ├── test_tscg_store.py               ← 20 tests (TscgStore, pyoxigraph)
        ├── test_endpoints.py                ← 20 tests (FastAPI integration)
        └── fixtures/
            ├── minimal_m2.jsonld
            ├── minimal_m1_edu.jsonld
            └── minimal_m1_chem.jsonld
```

---

## 📚 Documentation

### docs/CoreHypotheses/ **NEW — Theoretical foundations**
- [_00_TSCG_as_StereoscopicGlasses.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/_00_TSCG_as_StereoscopicGlasses.md) — Primary metaphor
- [_01_Narcissus_and_Icarus_as_Safeguards.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/_01_Narcissus_and_Icarus_as_Safeguards.md)
- [TerritoryMap_Dichotomy.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/TerritoryMap_Dichotomy.md)
- [SystemicEsperanto.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/SystemicEsperanto.md)
- [LegoTechnic_Modularity.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/LegoTechnic_Modularity.md)
- [Archetypes_as_CrossCultural_Artifacts.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/Archetypes_as_CrossCultural_Artifacts.md)
- [CredibilityAccretion_Process.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/CredibilityAccretion_Process.md)
- [MultisubjectiveScoreEvaluationProtocol.md](https://raw.githubusercontent.com/echopraxium/tscg/main/docs/CoreHypotheses/MultisubjectiveScoreEvaluationProtocol.md)

### docs/reboot-kit/SmartPrompts/
- Smart_Prompt_2026_01_17.md through TSCG_Smart_Prompt_v16_0_0.md (full history)

### docs/papers/
- `preprints/TSCG_Research_Paper_Draft_v5.md` **NEW**
- `preprints/HAL/` **NEW** — HAL submission materials + TSCG_Research_Paper_Draft_v4.md
- `preprints/Zenodo/` — v3.0 DOI: 10.5281/zenodo.18471860 (published)
- `preprints/previous/` — v1, v2 archived

---

## 📁 Folder Conventions

### Underscore prefix = hidden from the gallery

A leading `_` on a folder is **functional**, not decorative: the poclet-gallery index
generator (`cli_tools/generate_index-html/`) **skips underscore-prefixed folders**.

| Folder | Meaning |
|---|---|
| `_static/` | **prototype** simulation — NOT published in the gallery |
| `static/` | **finished** simulation — published |
| `_archives/` | superseded copies — not published |

**Renaming `_static/` → `static/` publishes the prototype.** Never do it as a "cleanup".
Conversely, a simulation is promoted to the gallery by dropping the underscore — that is the
switch, and it is the only one.

Each poclet therefore carries **two distinct READMEs**, and they must not be merged:
- `M0_<Name>_README.md` — the **ontology** (poles, GenericConcepts, ASFID/REVOI, combos)
- `_static/M0_<Name>_Simulation_README.md` — the **simulation** (engine, controls, visuals)

---

## 🛠️ CLI Tools

### ontology/cli-tools/ **NEW (SC-1)** — layer validation & migration
- `tscg_paths.py` — **shared repo-root resolution**. Walks UP from the script until it finds a
  directory holding both `ontology/` and `instances/`. Replaces the hardcoded
  `REPO_ROOT = Path("E:/_00_Michel/…")`, so the tools are **relocatable and machine-independent**
  (override: `TSCG_REPO_ROOT`).
- `check-M0/` — `check_m0_instances.py` (v1.6.0), `migrate_m0_to_v1_5.py`, `M0_Instances_Schema_shacl.ttl`
- `check-M1/` — `check_M1.py` (**v2.0.0**), `M1_Schema_shacl.ttl` (v1.1.0), `check_M1_README.md`

> ⚠️ **Three pre-existing bugs fixed in SC-1** — all of the *silent failure* kind:
> 1. `check_M1.run()` called `fix_imports_genesis()`, **never defined** → `AttributeError` on the
>    first file, in the auto-fix path. **None of the 7 documented auto-fixes had ever run.**
> 2. `check_M1` looked for `M1_Schema.shacl.ttl` (**dot**) while the file is `M1_Schema_shacl.ttl`
>    (**underscore**) → `--shacl` never found its grammar, validated nothing, and exited 0.
> 3. The M0 scripts looked for `symbolic-system-grammar` (**singular**); the directory is
>    `symbolic-system-grammars` (**plural**) → the whole SymbolicSystemGrammar category
>    (Iching, TriskeleToolchain) was **skipped without a word**.
>
> A validator that cannot find its grammar looks exactly like a validator that passed.
> `verify_layout()` now reports missing compartments instead of swallowing them.

### cli_tools/ (repo root — unchanged)
- `generate_index-html/` — Gallery generator (`_Generate_Index-html.bat`)
- `migrate_properties/` — Property rename CLI (README added)
- `ontology-linter/` — JSON-LD linting
- `owl_reasoning_test/` — OWL reasoning validation
- `verify_migration/` — Post-migration validation

---

## 🌳 Directory Tree (simplified)

```
tscg/
├── .claude/skills/                    # Claude AI skills
│   ├── tscg-article-pipeline/
│   ├── tscg-create-instance-simulation/
│   ├── tscg-generate-Mn-grammars/
│   ├── tscg-instance-pipeline/
│   ├── tscg-ontology-diagnosis-pipeline/
│   └── tscg-tensor-to-structural-grammar-migration/
├── cli_tools/                         # Command-line tools
│   ├── generate_index-html/
│   ├── migrate_properties/
│   ├── ontology-linter/
│   ├── owl_reasoning_test/
│   └── verify_migration/
├── domain_format_fix_backups/         # NEW — domain format fix backups
├── instances/                         # System instances (M0 layer)
│   ├── poclets/                       # 26 validated poclets
│   │   ├── AdaptativeImmuneResponse/
│   │   ├── BloodPressureControl/
│   │   ├── ButterflyMetamorphosis/
│   │   ├── CellSignalingModes/
│   │   ├── ColorSynthesis/            # federated (RGB, HSL, CMY, CMYK)
│   │   ├── ComplexChemicalSynapse/
│   │   ├── CounterPoint/
│   │   ├── ExposureTriangle/
│   │   ├── FireTriangle/
│   │   ├── FourStrokeEngine/
│   │   ├── Kidneys/
│   │   ├── KindlebergerMinsky/
│   │   ├── MtgColorWheel/
│   │   ├── NakamotoConsensus/
│   │   ├── NuclearReactorsTypology/   # NEW
│   │   ├── PhaseTransition/
│   │   ├── PlateTectonics/            # NEW
│   │   ├── Ptoe/                      # NEW — Periodic Table (BabylonJS 3D)
│   │   ├── Raas/
│   │   ├── Theremin/                  # NEW stub
│   │   ├── Tpack/
│   │   ├── Transistor/
│   │   ├── TrophicPyramid/
│   │   ├── TvTestPattern/
│   │   ├── Vco/
│   │   └── Yggdrasil/
│   ├── tscg-tools/
│   │   ├── TscgOntologyAPIServer/     # NEW stub (Phase 3)
│   │   ├── TscgOntologyExplorer/      # ElectronJS browser/editor
│   │   │   ├── dev/tscg-python-bridge/
│   │   │   │   ├── bridge_server.py   # Phase 2: TscgStore + /corpus/*
│   │   │   │   ├── _run_tests.py      # NEW interactive test menu
│   │   │   │   └── tests/             # NEW 58 tests
│   │   │   └── docs/UserManual.md     # NEW
│   │   ├── TscgPocletGenerator/
│   │   └── TscgPocletMiner/
│   ├── systemic-frameworks/
│   │   ├── Triz/                      # NEW — TRIZ icosahedron
│   │   └── Vsm/
│   └── symbolic-system-grammars/
│       └── Iching/
├── migration_backups/                 # Migration history
├── ontology/                          # Core ontologies
│   ├── InstanceSimulations/           # NEW — UX knowledge base
│   ├── M3_GrammarFoundation.jsonld    # APEX
│   ├── M3_EagleEye.jsonld
│   ├── M3_SphinxEye.jsonld
│   ├── M3_GenesisGrammar.jsonld
│   ├── M3_BicephalousPerspective.jsonld  # NEW
│   ├── M2_GenericConcepts.jsonld
│   ├── M2_Calibration.jsonld
│   ├── M1_CoreConcepts.jsonld
│   ├── M1_Domains.jsonld
│   ├── M1_extensions/                 # 13 domain extensions
│   ├── Ref/                           # Reference copies
│   ├── StructuralGrammar/             # Lambek documentation
│   │   └── Functional_Grammar_Model.md   # NEW (SC-1) — Fm2/Fm1m2 as functions
│   ├── cli-tools/                     # NEW (SC-1) — layer validation & migration
│   │   ├── tscg_paths.py              #   shared repo-root resolution
│   │   ├── run_all_layers.py          #   THE acceptance gate (M3 -> M0)
│   │   ├── golden_values.json         #   reference counts — 163 is GREEN
│   │   ├── check-M0/                  #   check + migrate M0 instances (+ its SHACL)
│   │   └── check-M1/                  #   check_M1.py v2.0.0 + M1_Schema_shacl.ttl v1.1.0
│   │                                  #   (the SHACL lives NEXT TO its script — one copy only)
│   ├── TSCG_InstanceGrammar/          # SHACL + migration tools
│   ├── docs/                          # Ontology documentation
│   │   └── _01_Worksite/              # NEW (SC-1) — worksite map + SC-* handovers
│   ├── sparql/                        # SPARQL queries
│   └── tools/
├── src/tscg/                          # Python package
│   ├── engine/                        # Core engine (analysis, RAG, math, reasoner)
│   ├── cli/
│   ├── demos/
│   ├── webapi/
│   ├── ontology_tools/
│   ├── rag/
│   ├── simulation-engine/
│   └── tests/
└── docs/
    ├── CoreHypotheses/                # NEW — 8 theoretical foundation docs
    ├── methodology/
    ├── Orchestration/
    ├── reboot-kit/
    │   └── SmartPrompts/              # Smart Prompt history (v11 → v16.0.0)
    └── papers/
        ├── inputs/
        ├── preprints/
        │   ├── HAL/                   # NEW — HAL submission
        │   ├── Zenodo/                # v3.0 published (DOI: 10.5281/zenodo.18471860)
        │   ├── TSCG_Research_Paper_Draft_v5.md  # NEW
        │   └── previous/              # v1, v2 archived
        └── white-paper/
```

---

## 🔄 Version History (summary)

| Version | Date | Key Changes |
|---|---|---|
| **v16.1.0** | 2026-05-23 | Score convention Option B (A_score/S_score), 26 poclets, Triz, TscgTools modeled, TSCG_InstanceGrammar/, CoreHypotheses/, InstanceSimulations/, BicephalousPerspective, python-bridge Phase 2 |
| v16.0.0 | 2026-05-13 | Structural Grammar reform (Lambek), M3_GrammarFoundation, hasTensorFormula→hasStructuralFormula |
| v15.10.1 | 2026-03-23 | CounterPoint, NakamotoConsensus, TscgPocletMiner, M1_music |
| v15.10.0 | 2026-03-16 | TrophicPyramid, TvTestPattern, TscgPocletGenerator, M2_Calibration |
| v15.9.0 | 2026-03-01 | KindlebergerMinsky, M1_Economics, TscgExplorer |

---

**Generated:** 2026-05-23
**Framework:** TSCG v16.1.0
**Author:** Echopraxium with the collaboration of Claude AI
