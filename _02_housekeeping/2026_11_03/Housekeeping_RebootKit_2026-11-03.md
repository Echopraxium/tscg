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
