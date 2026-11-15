# TSCG HandOver — end of 2026-11-15: WS-15 (scoring retirement) and WS-16 (sub-projects)

**Date**: 2026-11-15 (evening) · **Author**: Echopraxium with the collaboration of Claude AI
**Kind**: HandOver (Smart Prompt v17 §4). It only loads and points; it holds no authoritative
framework content. It follows the day's HandOver
`ontology/docs/_01_Worksite/WS-15/Next_Conversation_2026-11-15/TSCG_HandOver_EpistemicGap_2026-11-15.md`,
which stays valid for the detail of WS-15 (decisions, next lots, guardrails).

---

## 1. Load first — by name

- **`head-over-memory`**: every verifiable fact below is a *pointer to check at HEAD*.
- **`tscg-ontology-diagnosis-pipeline`**: for any lot that changes an ontology file.
- For a WS-16 sub-project, the skill that goes with it (listed in its item, e.g.
  `tscg-rust-vm` / `tscg-triskelevm-debug` for TriskeleVM).

Then read at HEAD:
1. `ontology/docs/_01_Worksite/WS-15/worksite.yaml` — state of the scoring retirement
   (SF-0 … SF-6).
2. `ontology/docs/_01_Worksite/WS-16/worksite.yaml` — the sub-projects in progress
   (SP-1 … SP-8): path and where to start reading for each.
3. The WS-15 HandOver named above, then the files it lists (decision record, Debt
   Overview §8.0h, `docs/CoreHypotheses/LayerCake_Models_The_Kit.md` §6).

---

## 2. Session state (perishable — verify, do not trust)

- Last four commits of the day, on top of "Naming: references after the M0_VCO / RAAS /
  TPACK README renames": the two HandOver commits, then "WS-15: the scoring-retirement
  worksite gets its id (was WS-TBD_EpistemicGap)", then "WS-16: Sub-projects in progress
  (registry, 8 sub-projects)". *Check with `git log --oneline -6` that they are pushed.*
- Michel's machine after applying them: `GATE: PASS`, `PATH_CHECK: 0 finding(s)`.
  Docs only: no reasoner run was needed.
- WS-14 belongs to another conversation (Michel's), not to this work.

---

## 3. What Michel decided today (non-verifiable)

- D1: the scoring-retirement worksite is **WS-15**; its priority is still open.
- A worksite for the **sub-projects in progress** that no worksite registered: **WS-16**,
  with TriskeleVM/TriskeleToolchain, CanopyGraphVizProto, World2DProjection, Kit,
  Compendium, TscgPocletMiner, TscgOntologyExplorer, TscgOntologyAPIServer. Its priority
  is open too.
- Everything else of the day (no scores, no gap, evaluation outside the model, naming
  norm, method) is in the WS-15 HandOver §3.

---

## 4. Next steps (choose with Michel)

1. **WS-15** — the lots listed in its HandOver §4 (M3/M2 prose after D4/D14/D20; M0
   step 2 after a rule on the qualitative text; producers outside the gate; narrative).
   Their state is `WS-15/worksite.yaml`.
2. **WS-16** — Michel picks which sub-project to resume and sets the priorities. Start
   from the item's `start` files and read the sub-project's own history
   (`git log -- <path>`) before proposing anything.
3. **Smaller items**: priorities of WS-15 and WS-16; other acronyms in file names
   (`M0_Bmc`, `M0_Triz`, `M0_Ptoe`… — each rename changes the instance IRI); a
   `pre-commit` hook calling `path_check.py`.

---

## 5. Guardrails

- **Michel decides** wording, modelling and priorities; Claude brings inventory, impact,
  patches (`git am`); Claude never pushes.
- **Debt honesty**: a counter falls only when the defect disappears.
- **Windows**: a case-only rename goes through a `.bat` (two-step `git mv`) plus a
  content-only patch.
- **No count recited**: every number comes from a command run in the session.
