# Housekeeping — ontology/docs cleanup, round 1 (2026-11-01)

**Author**: Echopraxium with the collaboration of Claude AI
**Nature**: trace of a housekeeping operation, same method as
`../2026_09_27/Housekeeping_ArchivePurge_2026-09-27.md`: files removed from `main`,
nothing lost — every file stays recoverable from history
(`git show <this commit>^:<path>`).

## Why

Michel, 2026-11-01: `ontology/docs/` holds many obsolete files. Finding that makes it
more than tidying: `src/tscg/rag/create_tscg_rag.py` (and its high-compress twin) tag
every file under `ontology/docs` as **authoritative ontology documentation**, so retired
vocabulary (tensor/⊗, KnowledgeField, MetaConcept, GenesisSpace, Bicephalous, ORIVE) was
served as authority by the RAG; the Compendium publishes them too.

## Triage

`OntologyDocs_Cleanup_Triage.xlsx` (this folder) — 88 files (outside `_01_Worksite`
and `_00_test_reports`), measured on HEAD `55497d4`: last commit, live references
(index files excluded; `docs/` path required when a name is ambiguous), retired-vocabulary
markers, Claude's proposal, **Michel's decision** (yellow column). No tool reads a
specific file of `ontology/docs` by path.

## Round 1 — removed (19 files, Michel's decision)

- `Domain_M2_Update_Analysis_v15_1_0.md`
- `MetaconceptPair_README.md`
- `M2_GenericConcepts_README.md`
- `M2_MetaConcepts.jsonld`
- `MetaconceptCombo_corrected.json`
- `M1_CoreConcepts.jsonld`
- `M2_KnowledgeField_Integration_Summary.md`
- `M3_SphinxEye_ORIVE_Correction_v2.2.0.md`
- `M3_TransdisciplinaryMetaConcepts_Renaming.md`
- `Namespace_Collision_Fix_Summary.md`
- `Namespace_Refactoring_Summary.md`
- `README_v13_Delivery.md`
- `TSCG-M3_Ontology_Documentation.md`
- `TSCG_M2_MetaConcepts_README.md`
- `TSCG_Smart_Prompt_v15_7_0.md`
- `UPDATE_SUMMARY_v14_3_1.md`
- `M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld`
- `M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.jsonld`
- `UserManual.html`

Live references fixed: `CLAUDE.md` — the two "Ontology Management" lines pointing at
`Domain_M2_Update_Analysis_v15_1_0.md` and `MetaconceptPair_README.md`.
Not touched on purpose: `ontology/Ref/` (archive snapshot) still cites
`docs/M2_GenericConcepts_README.md`; all LIVE references to `M2_GenericConcepts_README.md`
point at the live `ontology/M2_GenericConcepts_README.md`. The article skill's
`TSCG-M3_Ontology_Documentation.md` is the `docs/papers/inputs/` copy (a different file).

## Still open — 69 files undecided

Rows of the table with an empty decision column: 53 with no live reference (proposal:
delete), 9 cited only by documents that are obsolete themselves (proposal: delete and
remove the citing line), 6 to decide (`Poclet_Analysis_Methodology.md`,
`TSCG_Architectural_Extensions.md`, `TSCG_M1_Architecture.md`, the two analyses cited by
the Yggdrasil README, the VSM prerequisites analysis), 1 to keep
(`OntologyModeling_Guidelines.md`). Resume from the table: fill the yellow column.

Gate: not concerned (it reads no file of `ontology/docs`).
