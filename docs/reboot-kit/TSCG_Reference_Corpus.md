# TSCG Reference Corpus

**Version**: 3.0.1
**Date**: 2026-07-30
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Anchor**: repo HEAD `d92ded2` (origin/main). Every version below was read from the
actual file at HEAD on 2026-07-30 — not carried over from the v2.0.0 (2026-05-26)
inventory, which was pre-SC-1/SC-2 and is fully superseded.

**Legend**: ✅ Active · ⚠️ archived/pending · ❌ obsolete

---

## 1. M3 — Foundation (Structural Grammar)

| File | Version | Role |
|---|---|---|
| `M3_GrammarFoundation.jsonld` | 2.5.0 | Apex — Lambek calculus; operators `×` / `+` / `\|`; type system 𝕋₀/𝕋₁/𝕋₂ |
| `M3_EagleEye.jsonld` | 2.10.0 | Territory grammar Gt — ASFID, operator `×` |
| `M3_SphinxEye.jsonld` | 3.6.0 | Map grammar Gm — REVOI, operator `+` |
| `M3_BicephalousPerspective.jsonld` | 1.5.1 | Stereopsis grammar Gs — TKSL, operator `\|` |
| `M3_GenesisGrammar.jsonld` | 4.5.0 | Integrator — imports the four grammars; `m3:ontologyType` scheme |

**Retired**: `⊗` operator (permanently — 0 occurrences in M2 at HEAD); `M3_GenesisSpace`
(renamed `M3_GenesisGrammar`); Hilbert/tensor formalism.

## 2. M2 — Generic Concepts

- **`M2_GenericConcepts.jsonld`** ✅ **16.19.0** — SC-2 complete (monoidal formulas,
  St/It subscripting, no `⊗`).

Family distribution measured at HEAD (`m2:hasFamily`):

| Family | Count | Family | Count |
|---|---|---|---|
| Structural | 23 | Informational | 8 |
| Dynamic | 17 | Combo | 6 |
| Ontological | 10 | Relational | 5 |
| Regulatory | 10 | Adaptive | 4 |
| Energetic | 4 | Teleonomic | 1 |

(88 nodes carry a family; 10 families incl. the Combo umbrella.)

## 3. M1 — Core + Domain Extensions

| File | Version | | Extension | Version |
|---|---|---|---|---|
| `M1_CoreConcepts.jsonld` | 2.9.1 | | Biology | 1.2.0 |
| `M1_Domains.jsonld` | 1.4.1 | | BusinessModeling | 1.1.0 |
| `M0_Common.jsonld` | 1.1.0 | | Chemistry | 1.2.0 |
| | | | Economics | 1.1.0 |
| | | | Education | 1.1.0 |
| | | | Electronics | 1.1.0 |
| | | | EnergyGenerators | 1.1.0 |
| | | | Geology | 1.1.0 |
| | | | music | 1.1.0 |
| | | | Mythology | 1.2.0 |
| | | | Optics | 1.2.0 |
| | | | Photography | 1.2.0 |
| | | | Physics | 1.2.0 |
| | | | SystemicModeling | 1.2.0 |

**14 extensions** under `ontology/M1_extensions/<domain>/`.
`M0_Common.jsonld` hosts the shared M0 vocabulary incl. `m0:Facet`/`m0:hasFacet`
(the faceting mechanism — see §7, SC-3).

## 4. M0 — Instances

### 4.1 Poclets (`instances/poclets/`) — 27 dirs, 42 M0 files
AdaptativeImmuneResponse · BloodPressureControl · ButterflyMetamorphosis ·
**CanopyGraphVizProto** (typed `m3:Poclet`, moved from `_protos/`) · CellSignalingModes ·
ColorSynthesis (RGB/HSL/CMY/CMYK variants) · ComplexChemicalSynapse · CounterPoint ·
ExposureTriangle · FireTriangle · FourStrokeEngine · KindlebergerMinsky · MtgColorWheel ·
NakamotoConsensus · NuclearReactorsTypology · PhaseTransition · PlateTectonics · Ptoe ·
Theremin (stub) · Transistor · TrophicPyramid · TvTestPattern · Vco · Kidneys · RAAS ·
TPACK · Yggdrasil.

### 4.2 SystemicFrameworks (`instances/systemic-frameworks/`) — 3
Bmc (Business Model Canvas — new) · Triz · VSM.

### 4.3 SymbolicSystemGrammars (`instances/symbolic-system-grammars/`) — 3
IChing · TriskeleToolchain (new) · TscgFoundationGrammar (dir).

### 4.4 TscgTools (`instances/tscg-tools/`) — 7 dirs
TscgOntologyExplorer · TscgPocletGenerator · TscgPocletMiner · TscgOntologyAPIServer
(stub) · **TscgLayerCakeMCPServer** (new, Python MCP) · **TscgLittleBigBrain** (new) ·
`_archives`.

## 5. Tooling (`cli_tools/`)

`ontology-linter/` (`ontology_linter.py`) · `owl_reasoning_test/` (Pellet/OWL DL harness) ·
`migrate_properties/` · `verify_migration/` · `check-corpus-updates/` ·
`generate_index-html/` · `flexible-graphRAG/`.
Validation pipeline referenced by the worksite map: `run_all_layers.py`,
`tscg_metrics.py` v1.1.0, `check_M1.py` (confirm the canonical `cli_tools/` vs `cli-tools/`
path before scripting — a known SC-1 hazard).

## 6. Worksite documents (`ontology/docs/_01_Worksite/`)

- **`WS-0/`** (Structural Cleanup): `_00_TSCG_Worksite_Map.md` **v2.2.0** (the durable
  index), `TSCG_Session_Handover_2026-07-25.md`, `_01_Facet_as_M3_Principle_ArchitectureNote.md`,
  `M2_FeedbackLoop_Reclassification_README.md`, `SC-1/`, and dated opening packets
  `Next Conversation_YYYY_MM_DD/` (the 2026-07-30 packet holds `SC-3_Facet_Decision_Record.md` v1.0.0).
- **`WS-3/`**: `M2_Formulas_Review_with_Gs_README.md`.
- **`WS-8/`**: `Until_Further_Notice_WorksiteEntry.md`.
- Root: `TSCG_OntologyValidator_Worksite_README.md`, `TSCG_VocabularyConsolidation_Worksite_README.md`.

## 7. Live design state (not yet graved)

- **SC-2** ✅ complete (M2 16.19.0, pushed).
- **SC-3** — DESIGN DECIDED (`SC-3_Facet_Decision_Record.md` v1.0.0): four-axis model
  SCALE/NATURE/AUDIENCE/DOMAIN; `m3:Facet` to be lifted from the existing `m0:Facet`;
  Conferred/Derived sub-typing retracted. **NOT graved** — `m3:ontologyType` remains the
  single instance-type property at HEAD until the SC-3 graving session (after WS-5).
- Recommended next: **WS-5** (validator engine), then WS-2/CTX-4, then SC-3 graving.

---

## 7bis. Known corpus-hygiene debt

- **Case divergence (Windows `core.ignorecase`)**: several instance dirs/files differ
  in case between the local working tree and the versioned state — `Kidneys`↔`kidneys`,
  `Vsm`↔`vsm`, `Raas`↔`raas`, `Tpack`↔`tpack`, `Yggdrasil`↔`yggdrasil`,
  `Iching`↔`iching`, `M0_Vco`↔`M0_VCO`, `M1_Music`↔`M1_music`. Raw GitHub is
  case-sensitive, so tooling must read repo case (`git ls-files`), not local disk.
  Repo case itself is sometimes mixed (e.g. `raas/M0_RAAS.jsonld` + `M0_raas_README.md`).
  Deferred; full normalisation is a small separate worksite. (See worksite map §8.)

## 8. Conventions (HEAD)

- **URI base**: `@base: "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"`
- **M1 extension reference**: `"M1_extensions/<domain>/M1_<Name>.jsonld"`
- **Operators**: `×` (Territory/ASFID) · `+` (Map/REVOI) · `\|` (Stereopsis/Gs). `⊗` retired.
- **Subscripting**: S/I always monoid-subscripted in atom formulas (St/Ss, It/Im); A/F/D bare.
- **Author attribution**: `"Echopraxium with the collaboration of Claude AI"`.
- **Changelog**: rolling 3 most recent entries — except M3 files (up to 7).

## 9. External

- Zenodo DOI (preprint active) · GitHub: https://github.com/Echopraxium/tscg ·
  Pages: https://echopraxium.github.io/tscg/

---

## CHANGELOG

- **3.0.1** (2026-07-30) — Added §7bis: case-divergence corpus-hygiene debt (local vs versioned).
- **3.0.0** (2026-07-30) — Full rebuild from HEAD `d92ded2`. All ontology versions
  re-read (M2 16.19.0, M3 GenesisGrammar 4.5.0, GrammarFoundation 2.5.0, EagleEye 2.10.0,
  SphinxEye 3.6.0, Bicephalous 1.5.1, M1_CoreConcepts 2.9.1, 14 M1 extensions). Added
  M0_Common, BusinessModeling, Bmc, TriskeleToolchain, MCP server, LittleBigBrain,
  CanopyGraphVizProto. Recorded WS-n reorganization, SC-2 completion and SC-3 decision.
  Removed all pre-SC-1 artefacts (⊗, GenesisSpace, Option-B-as-novelty, KnowledgeField-as-current).
