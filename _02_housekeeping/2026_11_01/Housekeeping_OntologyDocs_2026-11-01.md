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
(`OntologyModeling_Guidelines.md`). Resume from the table: fill the yellow column. The 15 rows whose proposal said "to
confirm / to verify / to decide" were verified on 2026-11-01 — column J gives the exact
citing line (file:line) and a revised proposal. Notable: the live links in `CLAUDE.md` and
`README.md` to `docs/methodology/Poclet_Analysis_Methodology.md` are BROKEN (that path never
existed; the only copy is in `ontology/docs`) — moving it there would repair them;
`TSCG_M1_Architecture.md` is cited by an ontology (`M1_CoreConcepts.jsonld` rdfs:seeAlso), so
removing it is an ontology change (gate + reasoner); three analyses belong next to their
instances (Yggdrasil ×2, VSM).

Gate: not concerned (it reads no file of `ontology/docs`).

---

# Round 2 (2026-11-01) — the 69 remaining files

**Method** (Michel, 2026-11-01): one file at a time, in the conversation, for the 15 files
that needed his judgement (6 "À DÉCIDER" + 9 "to confirm"), each re-verified on HEAD
`796583a` (title, date, citing lines `file:line`, retired-vocabulary markers, options);
then the 53 with no live reference in five thematic lots. Decisions are in the yellow
column of `OntologyDocs_Cleanup_Triage.xlsx` (column I: why and which lines).

## Result — `ontology/docs/` (outside `_00_test_reports`, `_01_Worksite`) now holds 2 files

| Commit | Content |
|---|---|
| 1/5 | 55 removals, no live citation (dead M3; MetaConcept-era JSON-LD fragments; tensor formula tables and ORIVE notes; version/delivery summaries; old M2/M1 analyses and guides; `M3_Philosophical_Eye.jsonld`; `M2_FormulasReference_v15.10.0.json`) |
| 2/5 | 7 removals + their live citations (Poclet_Analysis_Methodology, TSCG_Architectural_Extensions, M2_KnowledgeField_README, M2_Scope_Metaconcept_Proposal, TSCG_Documentation_Index, ValueSpace_Enrichment_Final_Report, ontology_analysis) — rule chosen by Michel: no dead reference left behind, even in `docs/reboot-kit/` |
| 3/5 | 2 removals of unmerged M1 patches (NuclearUpdate, M1_CoreConcepts_updated) + Debt Overview 1.16.2: the M0 references they alone defined are recorded for lot M0 |
| 4/5 | 3 moves next to their instance (Yggdrasil ×2, VSM) + Debt Overview 1.16.3: the retired vocabulary of instance docs measured |
| 5/5 | this note, the table, `TSCG_FileTree.md` regenerated |

**Kept**: `OntologyModeling_Guidelines.md` (live, cited by `M3_GrammarFoundation` and the
ReferenceCorpus). **Still in place, decided**: `TSCG_M1_Architecture.md` — remove, but in a
separate ontology lot, because `M1_CoreConcepts.jsonld:208` cites it (`rdfs:seeAlso`, a plain
string): repoint to `{"@id": …/ontology/M1_CoreConcepts_README.md}`, M1 changelog, gate,
reasoner run by Michel.

## Findings worth keeping

- **Dangling M0 references** (Debt Overview §5): `M0_NuclearReactorsTypology` and
  `M0_PhaseTransition` (CriticalityRegime, SelfSustainingReaction…), `M0_Yggdrasil`
  (CatastrophicBifurcation) point at M1 concepts declared nowhere; the only definitions were
  the two unmerged patches. Owner: lot M0.
- **Broken links repaired by removal**: `CLAUDE.md` and `README.md` pointed at
  `docs/methodology/Poclet_Analysis_Methodology.md` (never existed); the live VSM README at
  `M2_Scope_GenericConcept_Proposal.md` (never existed).
- **Moves are not repairs**: the three moved analyses keep their `⊗`. Measured for all
  instance docs (Debt Overview §5): 75 of 140 `.md`, 1605 markers, 1347 `⊗`. No counter moved.
- **Effects**: the RAG builder no longer tags this material as authoritative ontology
  documentation; the Compendium's "M3–M0 layers → Historical notes" folder drops from ~70
  documents to 2.
- Not touched on purpose: `ontology/Ref/` (archive), archived Smart Prompts, `index.html`
  (embedded copy of a README, refreshed by the gallery generator), dated reports and
  journals whose lines narrate what existed (`_000_TSCG_Context_Files.md`,
  `M1_NAMESPACE_AUDIT_REPORT.md`, `Session_VSM_Capacity_Evaluation.md`, `docs/papers/inputs/`).

Gate: `GATE: PASS` before and after (it reads no file of `ontology/docs`, only `*.jsonld`).
Reasoner: no ontology file changed. Nothing lost: `git show <commit>^:<path>`.

## Next worksite — `docs/reboot-kit/` housekeeping

Michel (2026-11-01): debt partly left by the era before lazy loading (copies placed there
to be loaded into Project Knowledge). Found during round 2:
- `tscg-instance-pipeline` SKILL.md:103 and `TSCG_InstanceGrammar/DEPLOYMENT_GUIDE.md:205`
  point at `docs/reboot-kit/M2_FormulasReference_v15.10.0.md` — a tensor formula table
  (214 `⊗`). The skill is re-provisioned from the repo: fix the source, then re-provision.
- `CLAUDE.md` (Instance Development list, URI table) points at the reboot-kit copies of
  `HYBRID_FORMULAS_NOTATION_README.md`, `TSCG_ValueSpace_User_Guide.md`,
  `TSCG_ValueSpace_Quick_Reference.md`; `CLAUDE.md` itself is stale (Debt Overview §5).
- Old copies: `M0_VSM_README.md`, `Cascade_Modeling_README.md`,
  `Namespace_Refactoring_Summary.md`, `Amplification_Integration_Summary (1).md`,
  `ValueSpace_Integration_Summary.md`, the `00_*` bicephalous / Map-Territory summaries,
  `TO_DO.txt`.
- Same era elsewhere: `docs/methodology/Bicephalous_Integration_Guide.md` (cited by the
  AdaptativeImmuneResponse README:292), `docs/M2_MetaConcepts_README.md`.
