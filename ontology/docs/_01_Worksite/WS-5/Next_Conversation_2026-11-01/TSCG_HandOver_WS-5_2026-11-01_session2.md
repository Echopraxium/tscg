# TSCG HandOver — WS-5, 2026-11-01 (session 2): docs/reboot-kit cleanup → then lot K1

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-11-01
**Follows**: `TSCG_HandOver_WS-5_2026-11-01.md` (same folder). Its "FIRST" step — the
`ontology/docs/` cleanup — is **done**; its §0–§4 (lot K1, then NS-SEP, K2, lot M0, SC-5c)
stay the reference for what comes after.

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** (1.3.0) — needed for K1 (M2 data) and for any
   cleanup step that touches an ontology file (gate + Michel runs the reasoner).
3. Then read from HEAD:
   - `_02_housekeeping/2026_11_01/Housekeeping_OntologyDocs_2026-11-01.md` — the method
     that worked (round 1, round 2, its "Next worksite — docs/reboot-kit/" section).
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` §5 (two entries added today) and
     §8.0g (lot K0).

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of `3cd89d1`
  (M1_CoreConcepts 2.24.0) and the five "Housekeeping ontology/docs round 2" commits.
- **Gate**: `GATE: PASS` (Linux and Michel's Windows), counts unchanged by today's work.
  **Reasoner**: `M1_CoreConcepts.jsonld` (7 files merged) PASSED (Michel, 2026-11-01).
- **`ontology/docs/`** (outside `_00_test_reports`, `_01_Worksite`) holds one file:
  `OntologyModeling_Guidelines.md`. 64 files removed, 3 moved next to their instance.
- **Project Knowledge**: `TSCG_FileTree.md` and `TSCG_ReferenceCorpus.md` reloaded from HEAD
  `3cd89d1` — reload `TSCG_FileTree.md` again after this HandOver's commit.

## 2. First question to Michel

Which first: **(A) the `docs/reboot-kit/` cleanup (§3)** or **(B) lot K1** (previous
HandOver §2)? Claude's view: A first — several of those files are pointed at by skills and
by `CLAUDE.md`, so they can still steer a session (see §3 "Why it matters"); K1 does not
depend on them.

## 3. Worksite — `docs/reboot-kit/` (and the same era elsewhere in `docs/`)

**Origin** (Michel, 2026-11-01): debt partly left by the era **before lazy loading** — copies
and summaries placed in `docs/reboot-kit/` to be loaded into Project Knowledge. Today the
Project loads 4 resident files and reads everything else from HEAD on demand.

**Why it matters (measured 2026-11-01, not only the Compendium):**
- **Skills point there** (repo sources under `.claude/skills/`, re-provisioned from the repo):
  `tscg-instance-pipeline` SKILL.md:103–104 → `docs/reboot-kit/M2_FormulasReference_v15.10.0.md`
  (a tensor formula table, 214 `⊗`) and `docs/reboot-kit/SmartPrompts/`;
  `tscg-article-pipeline` SKILL.md:55 and :229 → `TSCG_Smart_Prompt_v15_10_1.md` presented as
  « version courante du framework » (the live loader is `TSCG_SmartPrompt.md`, v17).
  Loading such a skill sends Claude to read those files.
- **Root `CLAUDE.md`** (573 lines) is stale: a section "M3: The Bicephalous Basis",
  MetaConcept/GenesisSpace/tensor vocabulary, a Smart Prompt v16.0.0 URI, and links to the
  reboot-kit copies of `HYBRID_FORMULAS_NOTATION_README.md`, `TSCG_ValueSpace_User_Guide.md`,
  `TSCG_ValueSpace_Quick_Reference.md`. Claude Code loads the root `CLAUDE.md` automatically
  in every session opened in the repository (the reboot-kit one was already replaced on
  2026-10-03). Debt Overview §5 already lists it.
- **`ontology/TSCG_InstanceGrammar/DEPLOYMENT_GUIDE.md`:205–206** → the same formula table and
  a Smart Prompt file that no longer exists.
- **The RAG builder** (`src/tscg/rag/create_tscg_rag.py`) has no folder exclusion: it indexes
  `docs/reboot-kit/` (not tagged "authoritative", but retrievable).
- **The Compendium** shows them under "Guides & templates → Reboot kit".

**Scope (re-measure on HEAD):**
- `docs/reboot-kit/` — 43 tracked files, of which 13 in `SmartPrompts/`.
  **Live — never remove, they are the session loader and the resident corpus:**
  `TSCG_SmartPrompt.md`, `TSCG_ReferenceCorpus_Bootstrap.md`, `TSCG_ReferenceCorpus.md`,
  `TSCG_FileTree.md`, and `CLAUDE.md` (the 2026-10-03 folder guide). Decide with Michel:
  `SmartPrompts/` (archived versions — keep as history or remove; the papers in
  `docs/papers/` cite `TSCG_Smart_Prompt_v15_10_1.md`), `TO_DO.txt`, `macros*.txt`,
  `files.txt`, `_000_TSCG_Context_Files.md`, `check_encoding_issues.py`.
  Old copies already identified: `M0_VSM_README.md`, `Cascade_Modeling_README.md`,
  `Namespace_Refactoring_Summary.md`, `Amplification_Integration_Summary (1).md`,
  `ValueSpace_Integration_Summary.md`, `M2_FormulasReference_v15.10.0.md`,
  `HYBRID_FORMULAS_NOTATION_README.md`, the two ValueSpace guides, the `00_*` bicephalous /
  Map-Territory summaries.
- Same era in `docs/`: `docs/M2_MetaConcepts_README.md`, `TSCG_M2_Category_Taxonomy.md`,
  `TSCG_Session_Complete_Summary.md`, `TSCG_Update_v11_Summary.md`,
  `docs/methodology/Bicephalous_Integration_Guide.md` (cited by
  `M0_AdaptativeImmuneResponse_README.md`:292), and the rest of `docs/methodology/`.
- **Root `CLAUDE.md`**: not a removal — a rewrite (Michel decides its content), or a thin
  version that points to the Smart Prompt and the ReferenceCorpus, like the 2026-10-03
  reboot-kit `CLAUDE.md`.
- **Skill sources** `.claude/skills/tscg-instance-pipeline/SKILL.md`,
  `.claude/skills/tscg-article-pipeline/SKILL.md`: fix the pointers in the repo, then Michel
  re-provisions the skills in the Project.

**Method** (same as `ontology/docs` round 2): a triage table in
`_02_housekeeping/<date>/` (last commit, live references with `file:line`, retired-vocabulary
markers, homonyms, proposal, yellow decision column); **one file at a time** for the files
that need judgement (live citers, skills, `CLAUDE.md`), **thematic lots** for the rest, with
a short summary per lot (Michel asked: say the "buts" briefly). Then one commit per group;
every LIVE citing line is fixed, **even in documents that will be judged later** (Michel's
rule: no dead reference left behind); same-name files elsewhere are checked; a trace note;
`TSCG_FileTree.md` regenerated, and reloaded into the Project after the push (also
`TSCG_ReferenceCorpus.md` if it changed). If a step touches an ontology file: gate, then
Michel runs the reasoner and reports, before the push. Nothing lost: `git show <commit>^:<path>`.

## 4. Debts recorded today (for the lots that own them)

- **Lot M0** — Debt Overview §5: `M0_NuclearReactorsTypology` (`m1:CriticalityRegime`,
  `m1:SelfSustainingReaction`, 3 strings), `M0_PhaseTransition` (`m2:CriticalityRegime`),
  `M0_Yggdrasil` (`m1:CatastrophicBifurcation`) reference concepts declared nowhere; the
  former definitions are reachable with `git show 796583a:<path>` (paths in §5).
- **No owner yet** — Debt Overview §5: retired vocabulary in the narrative `.md` of the
  instances, measured: 75 of 140 files, 1605 markers, 1347 `⊗`. No instrument counts it; a
  `⊗` count over `.md` (health map) is a possible instrumentation lot.

## 5. Then — unchanged

Lot **K1** (bare keys of `m2:eagleView` / `m2:sphinxView`, previous HandOver §2), then
NS-SEP, K2, lot M0, SC-5c (previous HandOver §3).

## 6. Housekeeping

- Project Knowledge: reload `TSCG_FileTree.md` (this HandOver adds a file).
