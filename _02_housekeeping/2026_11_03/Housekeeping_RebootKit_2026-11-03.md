# Housekeeping — docs/reboot-kit/ (and the same era in docs/), 2026-11-03

**Author**: Echopraxium with the collaboration of Claude AI
**Follows**: `_02_housekeeping/2026_11_01/Housekeeping_OntologyDocs_2026-11-01.md`
("Next worksite — docs/reboot-kit/") and HandOver WS-5 2026-11-01 session 2, §3.

**Origin** (Michel, 2026-11-01): debt partly left by the era before lazy loading — copies
and summaries placed in `docs/reboot-kit/` to be loaded into Project Knowledge.

**Before the triage** (same day series):
- `2e0b332` — root `CLAUDE.md` rewritten as a thin guide (573 → ~120 lines).
- `0cb6b62` — skills `tscg-instance-pipeline` (2.2.2), `tscg-article-pipeline` and
  `ontology/TSCG_InstanceGrammar/DEPLOYMENT_GUIDE.md` repointed from reboot-kit copies to HEAD.

**Triage**: `RebootKit_Cleanup_Triage.xlsx` (this folder), measured on HEAD `0cb6b62`:
52 files (43 in `docs/reboot-kit/`, 9 in `docs/` outside `papers/` and `CoreHypotheses/`).
Method as in round 2 of `ontology/docs`: one lot at a time, Michel decides, one commit per
lot, every live citing line fixed in the same commit. Nothing lost:
`git show <commit>^:<path>`.

No lot touches an ontology file: no gate change, no reasoner run.

## Lots

### Lot 1 — identical copies (5) — removed
Byte-for-byte copies; the originals stay where they are. No live citer of the copies.
- `00_M3_Cyclops_Correction_Summary.md`, `00_Map_Territory_v1.2_Update_Summary.md`,
  `00_TSCG_M3_Bicephalous_Architecture.md`, `00_TSCG_Map_Territory_Theoretical_Foundation.md`
  → originals in `docs/papers/inputs/` (historical raw material for the article, untouched).
- `TSCG_Validation_Handoff_M1_M0.md` → original in `ontology/toolchain/owl_reasoning_test/`.

### Lot 2 — tensor era, no live citer (14) — removed
Summaries and references of retired eras (`⊗` products, MetaConcepts, M2 v11–v14). Remaining
mentions are only in `files.txt` (lot 4), archived Smart Prompts, archives, or the files
themselves.
- `docs/reboot-kit/`: `Amplification_Integration_Summary (1).md`,
  `ValueSpace_Integration_Summary.md`, `Namespace_Refactoring_Summary.md`,
  `Domain_Hybrid_Tensor_Product_5D_README.md`, `HYBRID_FORMULAS_NOTATION_README.md`,
  `Session_Summary_TSCG_v14.2.0.md`, `M0_VSM_README.md` (an old copy, different from the
  live `instances/systemic-frameworks/vsm/M0_VSM_README.md`, which is authoritative),
  `M2_OntologyCategory_Proposal.md` (proposed `m2:ontologyCategory`, since forbidden).
- `docs/`: `M2_MetaConcepts_README.md`, `TSCG_M2_Category_Taxonomy.md`,
  `TSCG_Session_Complete_Summary.md`, `TSCG_Update_v11_Summary.md`.
- `docs/methodology/`: `M2_Completeness_and_3D_Visualization_Strategy.md`,
  `M2_Component_Addition.jsonld` (an ontology fragment outside the gate's scope).
- Debt recorded (Debt Overview §5, tooling): `tscg_migration.py` writes
  `docs/M2_MetaConcepts_README.md`; running it would recreate the retired document.
