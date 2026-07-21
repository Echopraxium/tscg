# M0_TscgOntologyValidator — Design Specification

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 0.1.0 (DESIGN — not implemented)
**Type**: TSCG tool instance (`M0`, sibling of `M0_TscgPocletMiner`,
`M0_TscgOntologyExplorer`, `M0_TscgOntologyAPIServer`)
**Status**: specification captured 2026-07-18 for implementation in a **dedicated
fresh session**. This document is the hand-off; do not implement here.

---

## 0. Why this exists (the problem it kills)

The session of 2026-07-18 spent most of its context budget **re-discovering, by
hand, defects that belong to a small closed set of recurring families**. Each check
cost 3–4 bash calls plus a file in the context window. The work is tedious,
error-prone, and offers **no non-regression guarantee** — every fix risks silently
breaking something a manual pass won't catch.

The defects are not open-ended. They are **deterministic, finite, and already
enumerated** (see §2). None requires semantic judgement. Therefore they are
automatable **without dispossessing the human of any architecture decision** — this
is exactly the *technical validation* band of `tscg-ontology-diagnosis-pipeline`,
which the human's *semantic validation* sits above and is untouched.

**Primary goal: invert the context economy.** Replace "make the LLM re-derive known
defects, burning the window" with "run the validator, read one report, spend the
window on decisions."

**Secondary goal (equally important): dissolve the golden-rule problem.** The whole
session repeated *"the snapshot is not authority, paste me HEAD"*. A validator that
can read **`git HEAD` or the public GitHub raw** validates the authority directly and
removes snapshot-staleness as a class of error (see §3).

---

## 1. Scope and non-scope (hard boundaries)

**IN scope**
- Read ontology files from a selectable source (§3).
- Run the closed set of deterministic checks (§2).
- Emit a single structured report + a golden diff (§5).
- Absorb and extend `run_all_layers` — cover **all four layers M3→M0**, not just
  M1/M0 (`run_all_layers` is `NOT_INSTRUMENTED` on M2 and M3).

**OUT of scope — non-negotiable guards**
1. **Detection only, never auto-correction.** The validator emits *proposed diffs*;
   the human applies them through the normal pipeline. An auto-fixer over a corpus
   whose authority is `git HEAD` is a mass silent-regression engine — the exact
   opposite of the goal. Strict read/write separation.
2. **No semantic judgement.** It never decides whether a formula is *right*, only
   whether it is *well-formed / consistent / resolvable*. "Is `State = It × D | T`
   correct?" stays with the human. "Does `m3:ontologyType` resolve to a real IRI?"
   is the validator's.
3. **It is modelled inside TSCG.** As an `M0_*` instance, not a free-floating script.
   The tool that guards the framework must live in the framework — otherwise it is an
   ungoverned meta-level.

---

## 2. The five check families (each = one deterministic module)

Derived from what was **actually hit** on 2026-07-18. Each check has an ID, a
severity, and a machine-readable output. None needs a human in the loop.

### CTX — `@context` / IRI resolution hygiene
The highest-value family; today it has the worst coverage.
- **CTX-1** prefix used but **not declared** → resolves as a bogus URI scheme.
  *Attested*: `M1_CoreConcepts`, `M1_Domains` use `m3:` with no `m3` prefix →
  `m3:ontologyType` becomes an opaque IRI, invisible to any reasoner/SHACL.
- **CTX-2** relative prefix + `@vocab` present → resolves against `owl#`.
  *Attested*: `M3_BicephalousPerspective`, `M3_GrammarFoundation`.
- **CTX-3** `@base` malformed (missing `ontology/` segment).
  *Attested*: `M3_GrammarFoundation` (`.../main/` instead of `.../main/ontology/`).
- **CTX-4** relative prefix depending on `@base` (fragile, resolves today but one
  bad edit from breaking). *Attested*: 14 files.
- **CTX-5** JSON-LD term whose **name contains `:`** (e.g. `m3:eagle_eye`,
  `m1.ext:biology`, `m0:xxx`) → unusable as a prefix. *Attested*: ~30 files.
- **Canonical rule** (the reference the corpus already converged on): every `mN`
  prefix is **absolute**, hosted on `M3_GenesisGrammar.jsonld#` for `m3`, and the
  respective canonical file for `m2`/`m1`. This is SC-1.5 generalised to all layers.

**Cross-cutting mechanism** (learned twice this session — Fix B, then SHAPE 10/11):
a check that targets a class caught only via a `rdfs:subClassOf` axiom **misses in
per-file mode**. The validator must report **per-file AND merged** resolution and
flag divergence, never a single number.

### FRB — forbidden / retired formalism traces
- **FRB-1** tensor operator `⊗` (retired 2026-07-06).
- **FRB-2** old arrow `×⇒` / `(x)=>`.
- **FRB-3** Hilbert / tensor / SVD / ket vocabulary in live nodes.
- **FRB-4** dead references: `GenesisSpace`, `morphism_emergence`, `KnowledgeField*`.
- **Must distinguish live data from changelog prose** — a mention inside a
  `changes` string is history, not a defect (learned on the M2 cleanup).

### DUP — retired properties surviving as duplicates
- **DUP-1** D8 triad `structuralGrammarFormula{Expanded,TeX,RawText}`.
  *Attested*: 12 in `M1_CoreConcepts` (fixed v2.9.0), **8 still in `M1_Geology`**.
- **DUP-2** M0 scalar leaking into M1/M2 (`hasEpistemicGap` on a TYPE).
- **DUP-3** fossil mirror fields (`m2:eagleView.formula` vs canonical;
  `formulaComposition`/`formulaDecomposition`).
- **Guard-before-delete invariant**: never propose removing a field unless the
  surviving canonical is present and well-formed (the check that saved us on the 12
  combos).

### NOT — notation normalisation
- **NOT-1** bare `S`/`I` in an **atom** formula (must be `St`/`It`/`Ss`/`Im`) — the
  SC-2 rule. *Attested*: 43 canonical M2 formulas.
- **NOT-2** operator/monoid mismatch: `×` with a Gs primitive, `+` with ASFID, etc.
  *Attested*: `Gradient = F × T` (× on a Gs primitive).
- **NOT-3** `S`/`I` correctly bare inside a pure single-monoid context vs a `|`/`+`
  segment — the validator must know **which segment** a token sits in before
  flagging (a `+`-segment `I` is Interoperability→`Im`, not `It`).

### STR — structural / cross-file consistency
- **STR-1** a class/property **defined in two files** (e.g. `m3:MonoidalType` in both
  `GrammarFoundation` and `GenesisGrammar`).
- **STR-2** primitives declared with **incompatible shapes** across grammars
  (Gt/Gm as `owl:DatatypeProperty` vs Gs as `owl:Class`+`MonoidalType`) — so a
  class-targeting shape sees only 6 of 16 primitives.
- **STR-3** `owl:imports` target missing / unresolved.
- **STR-4** changelog length policy (≤3 everywhere, ≤7 for M3) — a lint, not an error.

---

## 3. Source switch (the golden-rule solver)

A single `--source` selector, resolved **before** any check:

| Source | Meaning | Use |
|---|---|---|
| `local` | working copy on disk | pre-commit self-check |
| `head` | `git show HEAD:<path>` | **the authority** — default for any "is the repo OK?" question |
| `github` | `raw.githubusercontent.com/Echopraxium/tscg/main/…` | validate the *published* state, no clone needed |

Rationale: the corpus authority is `git HEAD` (repeated all session). Making the
validator read HEAD/GitHub directly means it **never validates a stale snapshot** —
snapshot-staleness stops being a defect class. `local` exists only for the author's
own pre-commit pass.

`github` mode also lets a third party (Aki, a reviewer) validate the public repo
with zero setup — supports the ICC / non-autarkic-validation principle.

---

## 4. Architecture (implementation notes for the fresh session)

- **Language**: Python (reuses `rdflib`, `pyshacl`, `pyoxigraph`, Pellet already in
  the stack). No new heavy dependency.
- **Absorbs** `check_M1.py`, `check_m0_instances.py`, `run_all_layers.py` as the M1/M0
  back-ends; adds M2 and M3 front-ends (the missing instrumentation). Generate the
  M2/M3 SHACL grammars via the `tscg-generate-mn-grammars` skill — **but only after
  CTX defects are fixed**, else the grammar validates a broken IRI space.
- **Report** = machine-readable (JSON) + human summary. Per check: ID, severity,
  file, node, `git`-authority flag, and — where safe — a **proposed diff** (never
  applied).
- **Golden integration**: one unified `golden_values.json` across all four layers.
  Deliberate changes (a fix that lowers/raises a count) require an explicit
  `--update-golden` with a recorded reason — the discipline already in
  `run_all_layers`, extended corpus-wide. The validator must clearly separate
  *expected* (golden) from *new* (regression) violations.
- **CTX / STR checks run on the raw JSON-LD `@context` AND on the expanded graph** —
  because the whole point is that expansion is where relative-IRI bugs surface.

---

## 5. Output contract

```
TscgOntologyValidator  --source head  --layers M3,M2,M1,M0  --report report.json

=> per family: PASS / n findings (expected e / new n-e)
=> per finding: {id, severity, file, node, message, authority, proposed_diff?}
=> golden delta: {resolved:[...], new:[...], deliberate:[...]}
=> exit code: 0 iff no NEW findings above WARNING
```

---

## 6. What this replaces / relates to

- **Replaces** the ad-hoc bash+pyshacl passes done manually this session.
- **Absorbs** `run_all_layers` (which covers only M1/M0).
- **Feeds** the *technical validation* phase of `tscg-ontology-diagnosis-pipeline`;
  the human's *semantic validation* is unchanged and still required.
- **Is a peer of** the existing `M0_Tscg*` tool instances — same modelling treatment.

---

## 7. Immediate backlog this tool would have caught automatically

Snapshot of the live debt as of 2026-07-18, i.e. the tool's first expected report:

| Family | Finding | Count |
|---|---|---|
| CTX-1 | `m3:` prefix undeclared | 2 (`M1_CoreConcepts`, `M1_Domains`) |
| CTX-2/3 | relative + `@vocab` / bad `@base` | 2 (`M3_BicephalousPerspective`, `M3_GrammarFoundation`) |
| CTX-4 | fragile relative prefix | 14 |
| CTX-5 | term name contains `:` | ~30 |
| DUP-1 | residual D8 triad | 8 (`M1_Geology`) |
| NOT-1 | bare `S`/`I` in atom formula | 43 (M2, = SC-2 perimeter) |
| STR-1 | `m3:MonoidalType` double-defined | 1 |
| STR-2 | Gs primitives shaped differently from Gt/Gm | 6 |

The NOT-1 line is the most telling: the tool would turn the SC-2 perimeter into a
**progress counter** that must reach 0 when SC-2 ships — a gauge, not a manual audit.

---

## 8. Hand-off instruction for the fresh session

Start from this document. First implementation target: **CTX family + `--source`
switch** (highest value, unblocks the M3 SHACL grammar). Then FRB/DUP/NOT/STR.
Do NOT begin by generating the M2/M3 SHACL grammars — fix CTX first, otherwise the
grammar targets a broken IRI space (the trap found on 2026-07-18).

**Authority reminder**: the only authority is `git show HEAD:<file>`. Every count in
§7 was measured on session snapshots and must be re-confirmed against HEAD by the
tool itself on first run.
