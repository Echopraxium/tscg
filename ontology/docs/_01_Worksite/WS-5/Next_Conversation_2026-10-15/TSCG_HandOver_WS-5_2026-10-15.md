# TSCG HandOver — WS-5, 2026-10-15: SC-5b fully prepared → implement it

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-15
**Follows**: `../Next_Conversation_2026-10-13/TSCG_HandOver_WS-5_2026-10-13.md` (superseded
for "what next"; keep it for the decision history) and, through it, the 2026-10-12 HandOver
(working method, push path).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — SC-5b writes M1 classes.
3. **`tscg-generate-mn-grammars`** — only if a SHACL grammar is touched (SC-5b should not).
4. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-5/SC-5b/SC-5b_Subdomains_Decision_Table.xlsx` — **the
     authority for SC-5b**: sheet 1 column "Michel: decision" (28/28 decided) and the block
     "New domain classes" under the summary.
   - `ontology/docs/_01_Worksite/WS-5/SC-5b/SC-5c_DomainModel_DesignNote.md` — §0 evaluation
     criterion first; §12–§13 for what SC-5b deletes.

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of the "SC-5b preparation complete"
  docs commit, on top of `76e2943`. Ontologies unchanged since `e9beb47` (Lot SC-5).
- **Gate**: `GATE: PASS`, counts unchanged since 2026-10-12 (M1 17 / 133 / 1 / 296).
- Three evenings (10-12 → 10-14) were **design and review only**: no ontology change.

## 2. Next goal — implement SC-5b (diagnosis pipeline, one lot)

Phase 1 baseline (gate) → Phase 2 change → Phase 3 gate → Phase 4 Michel → patches `1_…`.

**Create** (label + `rdfs:subClassOf` + `skos:closeMatch` OpenAlex when the table gives one;
no definitions — Q7; IRIs in the *current* convention — Q6, NS-SEP comes after):
- the 26 KEEP lines of sheet 1, with the parents of the "Proposed parent(s)" column
  (e.g. Endocrinology ⊑ Physiology ⊑ Biology; Signal Processing ⊑ Electronics + Computer
  Science; Geophysics ⊑ Geology + Physics; Pharmacology ⊑ `m1:Domain`; Trading Card Games
  becomes **Collectible Card Game** ⊑ Card Game);
- the parent classes they need: **Mathematics**, **Game**, **Card Game**, **Vision Science**
  (closeMatch OpenAlex 2809), **Condensed Matter Physics** (OpenAlex 3104),
  **ElectronicMusic** (⊑ Music). **Finance is NOT created** (no M0 cites it — Q10).

**Relink** existing domains: Blockchain ⊑ Computer Science; Optics ⊑ Physics;
Game Theory ⊑ Mathematics; MusicTheory ⊑ Music (Q1).

**Delete**: `m1:subdomains` (22 domain classes); `m1:extension:physics:subdomains`
(6 physics combos, which stay `m1:domain` Physics); the classes
`business_modeling:Strategic`, `economics:Financial`, `geology:Geological` (Q4); the
leftover string `m1:domain` on `optics:Optics_Domain` (M1_Optics).

**Update**: registry README / Debt Overview (record SC-5b); expected gate: M1 counts
unchanged unless a new class trips SHAPE 5/11 — show any move before `--update-golden`.

**One decision still open** (ask before writing that line): **Decision Theory** — parent
Mathematics (proposed) or a root aligned on OpenAlex field 18 "Decision Sciences".

## 3. Then, in order

1. **Lot NS-SEP** — one prefix per defining file: `m1:domain:X` → `m1.domains:X`,
   `m1:extension:<ext>:X` → `m1.<ext>:X` (prefix = layer + `.` + file name in lower case;
   M1_CoreConcepts keeps `m1`). Measured on HEAD `76e2943`: 45 + 1,536 occurrences in
   29 files. Mechanical, gate-verified.
2. **Lot M0** — `m1:domain` → **`m1:belongsToDomain`** with IRIs in the 44 M0 files (+8 M1
   files, M0 template); delete `m0:subdomains` (7 poclets) and `m0.vco:subdomains`; M0
   checks apply the same rule as M1 (in `check_m0_instances.py`, which can see the M1
   hierarchy).
3. **SC-5c** (domain model) — **usefulness test first** (§0): model FireTriangle,
   RGB_Additive and Transistor on paper with the full apparatus (requires, contracts,
   facets) and keep only what serves. Nothing of SC-5c is implemented before that.

Unchanged queue from 2026-10-12: Protocol, Part (a) M2, engine `advanced=False`,
KnowledgeField leftovers in tools, lot R2, etc.

## 4. Housekeeping

- The SC-5c design note ends with one extra blank line (git am whitespace warning) — fix
  in the next patch.
- Project Knowledge: reload `TSCG_ReferenceCorpus_Bootstrap.md` and `TSCG_FileTree.md`
  (new folder `WS-5/SC-5b/`).
