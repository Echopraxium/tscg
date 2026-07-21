# TSCG — Session Handover (2026-07-18)

**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Context**: session opened on SC-2 preparation; degenerated (productively) into a
corpus-wide `@context` hygiene emergency + two M-layer cleanups + the decision to
build a validator. Almost nothing of the *planned* work (SC-2, the Gs review) was
executed; a lot of *unplanned* debt was surfaced and partially repaired.

**Authority reminder (golden rule)**: `/mnt/project/` snapshots and prior uploads are
**NOT** authorities — the only authority is `git show HEAD:<file>`. Every file below
was produced from **session uploads**, which proved stale more than once this session
(M1_Domains snapshot was 1.3.0 vs real 1.4.0; the ConceptCombo confusion; etc.).
**Re-verify against HEAD before committing anything.**

Conventions unchanged: English files / French conversation; `@base` short IRIs;
base URI `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`;
changelog 3 entries (M3: up to 7); no `⊗`/`×⇒` (× = Gt, + = Gm, | = Gs);
Fm2/Fm1m2 are functions (comma-args), St/It only on collision letters S/I.

---

## 0. Deliverables (in outputs/, PENDING Michel's gates + HEAD re-verification)

12 files modified/created (+3 accompanying diffs):

| # | File | Nature | Version | Worksite |
|---|---|---|---|---|
| 1 | `M1_CoreConcepts.jsonld` | modified | 2.9.1 | SC-6 cleanup + @context fix |
| 2 | `M1_CoreConcepts_README.md` | modified | **2.9.0** ⚠ | (drift — see §6) |
| 3 | `M1_Domains.jsonld` | modified | 1.4.1 | @context fix |
| 4 | `M1_Domains_README.md` | modified | 1.4.1 | @context fix |
| 5 | `M1_Schema_shacl.ttl` | modified | 1.3.0 | SC-5 hardening |
| 6 | `M2_GenericConcepts.jsonld` | modified | 16.18.0 | Gs review (decision 1.B) |
| 7 | `M2_GenericConcepts_README.md` | modified | 16.18.0 | Gs review (1.B) |
| 8 | `M3_BicephalousPerspective.jsonld` | modified | 1.3.1 | @context fix |
| 9 | `M3_BicephalousPerspective_README.md` | modified | 1.3.1 | @context fix |
| 10 | `M3_GrammarFoundation.jsonld` | modified | 2.4.1 | @context fix (+@base) |
| 11 | `M3_GrammarFoundation_README.md` | modified | 2.4.1 | @context fix |
| 12 | `M2_Formulas_Review_with_Gs_README.md` | **created** | 1.0.0 | worksite opened |
| 13 | `M0_TscgOntologyValidator_README.md` | **created** | 0.1.0 | tool design spec |

Diffs: `M1_CoreConcepts_SC6_cleanup.diff`, `M2_eagleView_formula_removal.diff`.

---

## 1. COMMIT DISCIPLINE (read before committing — non-negotiable)

Three independent golden movements, each **deliberate**. Commit them **separately**
so each delta is attributable, and pass `--update-golden` with the reason recorded:

1. **SC-6 cleanup** (`M1_CoreConcepts` 2.9.1): `EXP001` drops **12 → 0** (retired D8
   triad + `hasEpistemicGap` removed from 12 combos). *Lowering.*
2. **SC-5 hardening** (`M1_Schema_shacl.ttl` 1.3.0): **+8** — SHAPE 10 extended to
   TeX/RawText now catches `M1_Geology`'s 8 residual `RawText`. *Raising.* (Geology
   itself left uncleaned — see §4.)
3. **@context fixes** (4 files): golden delta **UNPREDICTABLE** — invisible triples
   become visible; violations may disappear AND appear. **Commit ISOLATED.**

The Gs-review eagleView removal (`M2` 16.18.0) is **not** covered by any automated
gate (`run_all_layers` is `NOT_INSTRUMENTED` on M2) — validate with Pellet manually.

---

## 2. WHAT ACTUALLY HAPPENED (honest ledger)

Planned: SC-2. Executed: almost none of it. The session was ~90 % unplanned debt.

- **SC-6 (partial)** — removed the retired D8 property family
  (`structuralGrammarFormula{Expanded,TeX,RawText}`, 30 fields) + the M0 scalar leak
  `hasEpistemicGap` (12) from 12 GenericConceptCombos in `M1_CoreConcepts`. Live
  `Fm2`/`Fm1m2` signatures preserved (verified: 0 combos left formula-less).
- **SC-5 (hardening)** — `M1_Schema_shacl.ttl` 1.3.0: SHAPE 10 extended to the full
  D8 triad; NEW SHAPE 11 `NoM0MeasurementInM1Shape` forbids `hasEpistemicGap`. Both
  given **dual `sh:targetClass` (GenericConceptCombo + DomainConceptCombo)** — without
  the second, they never fire in per-file mode (the Fix-B trap, caught again).
- **Gs review decision 1.B** — removed 66 fossil `m2:eagleView.formula` (duplicate of
  the canonical formula; 28 had diverged). `role`/`status`/`basis` preserved.
- **@context corpus emergency (the big find)** — the M3 files do not share one IRI
  space (see §3). Fixed the 4 hard-broken; 14 fragile + ~30 term-name-with-`:` remain.

---

## 3. THE @context DEFECT (root cause, generalises SC-1.5)

`m3` prefix `"M3_GenesisGrammar.jsonld#"` is a **relative** IRI. It resolves against
`@vocab` if present, else `@base`. The corpus already converged on the **absolute**
form (all M1 extensions + all M0 use it); the M3 files and a couple of M1 files
lagged. Symptoms fixed this session:

- **CTX-1** prefix used but undeclared → bogus URI scheme. `M1_CoreConcepts`,
  `M1_Domains` (the latter had 4 real `m3:*` terms invisible to reasoners).
- **CTX-2** relative + `@vocab`=owl# → resolves against owl#.
  `M3_BicephalousPerspective`, `M3_GrammarFoundation`.
- **CTX-3** `@base` malformed (`.../main/` missing `ontology/`). `M3_GrammarFoundation`.

**Fix applied**: made `m3` absolute in all 4 (+ repaired GrammarFoundation `@base`).
Verified: the 5 M3 files now resolve `MonoidalType` to the **same** IRI; CoreConcepts
`m3:ontologyType` now resolves to the real M3 namespace. Data graphs unchanged.

**Still open**: 14 "fragile" files (relative, resolve today, `@base`-dependent → make
absolute, golden-stable) and ~30 files with JSON-LD **terms whose name contains `:`**
(`m3:eagle_eye`, etc. — unusable as prefixes). These are CTX-4/CTX-5 for the validator.

---

## 4. BACKLOG (surfaced this session, NOT done)

- **M1_Geology**: 8 residual `structuralGrammarFormulaRawText` (SC-6 slice). SHACL
  1.3.0 will flag them (+8). Same cleanup as CoreConcepts. Michel deferred it.
- **14 fragile @context** + **~30 term-name-with-`:`** (CTX-4/5).
- **Changelog normalisation** — Michel DECIDED the single canonical form is
  `@graph[ontology].metadata.changelog` (nested block). Current corpus has **3
  competing forms** (`metadata.changelog` in M3; `m2:changelog` flat list everywhere —
  most common; `m1:changelog` in M1_Domains & M1_CoreConcepts) **+ intra-file
  duplicates** (M1_CoreConcepts has m1:+m2:; M3_EagleEye has metadata.changelog +
  m2:changelog) **+ the `changelog` property is DEFINED NOWHERE**. Migration NOT done
  (too large/manual for session end) → first canonical job for the validator.
- **Source typo**: `M3_GrammarFoundation.jsonld` changelog 2.3.0 reads
  `DomainConceptCombo → DomainConceptCombo` (should be `KnowledgeFieldConceptCombo →
  DomainConceptCombo`). README transcribes it corrected; the .jsonld still has the typo.
- **README/jsonld version drift**: `M1_CoreConcepts_README` is 2.9.0 vs .jsonld 2.9.1.
  M3_EagleEye/SphinxEye READMEs not touched (files not modified this session).

---

## 5. THE TWO SEMANTIC DECISIONS (instructed, ship in the Gs worksite — NOT SC-2)

Both are inside the SC-2 perimeter, so **SC-2 ships their MECHANICAL migration**
(`State = It`, `Symmetry = St`); the SEMANTIC revision below ships **later** in
`M2_Formulas_Review_with_Gs`. Rationale in that README (§3): keeps the SC-2 golden
delta predictable.

- **GS-1 `State`: `I` → `It × D | T`.** Residue: `State = It` was near-tautological
  (M3 defines `I` via "…this system **state**…"). Reading: state = state-variable
  (Markov). `It`=content, `D`=determines evolution, `| T`=measurable at each instant t.
  `T` does NOT subsume `D` (T is relational time, not dynamics) — `D` is explicit.
  First correct use of `T` in the corpus. No collision (checked, 17 files).
- **GS-2 `Symmetry`: `S` → `St | _0`.** Residue: near-duplicate of `Invariant`
  (`St × A`). Reading: symmetry = **reversible** (absence of `D`, per R2/Stase) +
  **non-oriented** (`_0` = `_^|_$` = no privileged direction, per R1). Distinguishes
  from Invariant (oriented). No collision; 3rd use of `_0`.

Both need `rdfs:comment` rewrite + `isStereopsic` + sphinxView decision when graved.

---

## 6. SC-2 — READY TO EXECUTE (nothing migrated yet)

Base is now sound (IRIs aligned). Execution order (unchanged from prior handover):
1. `notation_disambiguation` convention in `M3_BicephalousPerspective` (revise the
   EXISTING one — it is the stale "hybrid-only, includes O" rule; SC-2 = collision
   pairs S/I only, everywhere, O bare).
2. `typeSymbol` in `M3_EagleEye`: `S→St`, `I→It` **at the source**.
3. SHACL `FormulaShape` forbidding bare `S`/`I` in **atom** formulas
   (`m2:hasStructuralGrammarFormula`, NOT the `Fm2` signatures).
4. Migrate the **43** canonical M2 formulas (measured; 0 in a Map `+` segment; 0
   already-`Ss`/`Im` — fully mechanical). `Balance = A × S × F | _0 → A × St × F | _0`.
5. Update `M2_GenericConcepts_README` §"Notation Convention" (currently states the OLD
   hybrid-only rule) + Key Takeaways + Statistics.

**Perimeter fact**: atom formulas live in `m2:hasStructuralGrammarFormula` (97 total,
43 with bare S/I); combos use `m1:structuralGrammarFormula` (Fm2 signatures — no
subscripts apply).

---

## 7. THE VALIDATOR (agreed remedy — build in a FRESH session)

`M0_TscgOntologyValidator_README.md` (v0.1.0) is the design spec. Why it exists: the
defects are a **closed, deterministic set** (5 families: CTX, FRB, DUP, NOT, STR),
re-discovered by hand each session at high context cost. Key design points:
- **Detection only, never auto-correction** (proposes diffs; human applies).
- **`--source local | head | github`** — validating HEAD/GitHub directly dissolves the
  golden-rule/snapshot-staleness problem.
- **Absorbs `run_all_layers`** (M1/M0 only) and adds M2/M3 instrumentation.
- Modelled as an `M0_*` TSCG instance (peer of PocletMiner/Explorer/APIServer).
- **Start with**: CTX family + the source switch (unblocks the M3 SHACL grammar).
- Do NOT generate M2/M3 SHACL grammars before CTX is fixed (they'd target broken IRIs).

`run_all_layers` coverage confirmed this session: **M2 and M3 are NOT_INSTRUMENTED**;
it wraps `check_M1.py` (per-file) + `check_m0_instances.py` only.

---

## 8. PROGRESS ESTIMATES (honest)

- **SC-2**: ~25 % — unblocked + measured + 2 atoms instructed; **0 formulas migrated**.
- **M2 Gs-review worksite**: ~5 % — opened, 2/97 decisions recorded, none graved.
- **This session's real output**: unplanned hygiene debt (SC-6 partial, SC-5 hardening,
  eagleView removal, @context repair) — which was blocking everything else.

Maturity note (Michel's, endorsed): ontology engineering here lacks the safety nets of
software engineering (compiler/linter/CI). The validator is the missing net. TSCG's own
Map had drifted from its Territory — the validator is δ₁ applied to the corpus.

---

## 9. NEXT ACTIONS (recommended order)

1. Run gates on the 12 deliverables; commit in the 3 isolated groups (§1).
2. Fix the README/jsonld drift (CoreConcepts README → 2.9.1) + the 2.3.0 source typo.
3. Build `M0_TscgOntologyValidator` in a fresh session (CTX + source switch first).
4. Fix M1_Geology (SC-6 slice, +8).
5. Execute SC-2 (§6) on the now-sound base.
6. Grave GS-1/GS-2 in the Gs review worksite; continue the 97-formula review.
7. Changelog normalisation (validator-assisted).
