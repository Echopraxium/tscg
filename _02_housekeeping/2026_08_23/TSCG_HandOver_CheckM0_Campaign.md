# TSCG — HandOver: check-M0 Conformance Campaign

> Paste this as the **first message** of a fresh conversation in the TSCG project to
> resume this worksite. Two rules, as always: load skills **by name**, and carry
> **no authoritative content** — read every fact (HEAD SHA, PASS/FAIL counts, file
> structure, the schema, the checker, any instance) from HEAD, never from memory or
> from this document. Numbers below are **perishable context**: confirm them, don't
> trust them.

---

## 1. Load first — by name
- **`head-over-memory`** — authority discipline (HEAD > durable corpus > memory; verifiable facts never come from memory).
- **`tscg-ontology-diagnosis-pipeline`** — the 6-phase validation pipeline.
- **`tscg-instance-pipeline`** — M0 instance mechanics.

Naming a skill is a direct instruction, not a heuristic match.

## 2. The one rule
**HEAD is the only authority** (`github.com/Echopraxium/tscg`). Read the checker, the
schema, the modernizer, and any instance from HEAD (raw CDN or a fresh shallow clone:
`git clone --depth 1 https://github.com/Echopraxium/tscg.git`). Do not recite structure
or counts from this document.

## 3. The worksite — repo-wide check-M0 conformance

**Goal.** Most `M0_*.jsonld` instances fail the **check-M0** acceptance gate
(`ontology/cli-tools/check-M0/check_m0_instances.py`, checks C01–C15). We are bringing
them to conformance, instance by instance, in verified batches — without polluting the
shared `M0_Common` namespace.

**The gate** = the `check_*` scripts orchestrated by `run_all_layers.py`:
- M0: `ontology/cli-tools/check-M0/check_m0_instances.py` + `M0_Instances_Schema_shacl.ttl`
- M1: `ontology/cli-tools/check-M1/check_M1.py` + `M1_Schema_shacl.ttl`
- M2/M3: schemas only, no executable checker.
The gate is a **gap-tracker by design** (run_all_layers' own docstring: "M1 has never been
conformant; a binary gate would be red every day"), not a must-be-green precondition.

**Progress (perishable — re-verify with a full `check_m0_instances.py` scan):**
last confirmed ≈ **17 PASS / 25 FAIL / 42 total**. Confirm current HEAD with
`git rev-parse HEAD` (last seen ~ commit `0.1.88`).

**Green so far** (confirm by scan): FireTriangle, QRCodeToPocketCity, Bmc, Triz,
Triz_Examples, TriskeleToolchain, TscgPocletGenerator, BloodPressureControl,
PhaseTransition, Vco, NuclearReactorsTypology, Ptoe, TscgCanopyGraphVizProto,
TscgOntologyExplorer, TscgPocletMiner, TscgOntologyAPIServer. (≈16–17; re-count.)

### The main tool — `ontology/cli-tools/modernize_m0.py` (read its README from HEAD)
Mechanical/semi-mechanical Path-B modernizer. Per instance it: repoints `m0:` →
`M0_Common#`; adds the local alias `m0.<inst>:` (identity = **file stem**, camel like the
gate's `_camel`); reclassifies instance-local `m0:X` props to `m0.<inst>:` **unless** the
first segment is in the schema's shared whitelist (read live from the SHACL); migrates
retired aliases (`m1core:`→`m1:`, `m1<dom>:`→`m1.ext:<dom>:`, root `X_score`→`m0:scoreX`);
adds `owl:imports M0_Common`; de-wraps `{@value}` scores (C10); flattens nested
`asfidScores/revoiScores` (C15) with means/gap; converts enum strings to IRIs
`m0:<prop>.<Pascal>` (C11); dedups `m3:ontologyType` to `@graph[0]` (C13); renames
`m0:tensorFormula`→`m2:hasStructuralGrammarFormula`; ORIVE→REVOI in prose. It **reports,
never guesses** — flags `semantic_gaps` (`m1:domain`, `m3:ontologyType`), `CASING_WARNING`,
`UNRESOLVED_PREFIXES`. Usage: `python ontology/cli-tools/modernize_m0.py <path>` then
**re-gate both** (check-M0 + `ontology/TSCG_InstanceGrammar/validate_m0_instance.py`).

## 4. What's left

- **Group C (~25 instances)** — need the **`⊗`-in-formula-VALUES reform**, which is **NOT
  yet wired into `modernize_m0.py`** (only the `m0:tensorFormula`→`m2:` property rename is).
  Next concrete task: branch the value transform under **Politique 1** — mechanical
  `⊗`→`×`, atoms `S→St` / `I→It` (Territory), Map-segment `I→Im` reviewed case by case —
  and validate it first on the **colour lot (CMY / CMYK / HSL = Group A, C12-only)** before
  generalizing. (`M0_CMY_Subtractive`, `M0_CMYK_Subtractive`, `M0_HSL_Additive` under
  `instances/poclets/ColorSynthesis/`.) Consider the `tscg-tensor-to-structural-grammar-migration`
  skill as reference for the reform.

  **All 25 remaining FAILs carry C12** (re-verify by scan; every one also needs the usual
  mechanical passes the modernizer already does — C02/C03/C07/C09/C15 — except the three
  colour-lot ones which are C12-only):
  - *C12-only (Group A, ideal ⊗-reform pilot):* `CMY_Subtractive`, `CMYK_Subtractive`,
    `HSL_Additive`.
  - *C12 + mechanical (Group C):* `AdaptativeImmuneResponse`, `ButterflyMetamorphosis`,
    `CellSignalingModes`, `ColorSynthesis`, `ComplexChemicalSynapse`, `Counterpoint`,
    `ExposureTriangle`, `FourStrokeEngine`, `IChing`, `Kidneys`, `KindlebergerMinsky`,
    `MtgColorWheel`, `NakamotoConsensus`, `PlateTectonics`, `RAAS`, `RGB_Additive`,
    `TPACK`, `TVTestPattern`, `Transistor`, `TrophicPyramid`, `VSM`, `Yggdrasil`.
  - A few carry extra flags to watch: `IChing` and `VSM` also fail C10+C11; `Counterpoint`
    also C11; `Kidneys`/`KindlebergerMinsky`/`PlateTectonics`/`RAAS`/`Transistor`/
    `TrophicPyramid` also C08; `AdaptativeImmuneResponse` also C13. (Confirm per instance.)
- **Worksite A — Simulation Ontology: classification + grammar** (deferred). Define a
  central `sim:` vocabulary (`SimulationCase`, `TransitionOutcome`, metrics `vp/conv/cross/
  net/cost`, `phaseIndex`…) in `ontology/InstanceSimulations/`; write a SHACL grammar
  (`check-SIM`) + possibly an `m3:SimulationOntology` type; repair the **dead
  `M3_GenesisSpace` references** in `BmcSimulation`, its `.js` wrapper, and the two
  `ontology/InstanceSimulations/M0_InstanceSimulation*` files (all still point to the
  vestige). Anti-overfitting: wait until ≥2 real simulations exist before freezing the grammar.
- **Per-instance semantic gaps** the tool cannot fill (Head Chef decides): missing
  `m1:domain` / `m3:ontologyType`, and any divergent formula content.

## 5. Decisions already made (do not re-litigate — but re-verify against HEAD)
- **D1 (formula content):** an instance cites the **canonical M2 formula** (from
  `m2:hasStructuralGrammarFormula` on HEAD), not an ad-hoc one. (Applied to FireTriangle.)
- **Path B (namespace):** instance-local props go under `m0.<inst>:`; only the schema's
  shared whitelist stays `m0:`. Never dump ad-hoc vocab into `M0_Common#`.
- **Option B (datatype):** the M0 SHACL accepts `xsd:float` **OR** `xsd:double` for
  scores/means/gap/focal (16 constraints relaxed). Single source of truth =
  `ontology/cli-tools/check-M0/M0_Instances_Schema_shacl.ttl`; the standalone validator
  `validate_m0_instance.py` reads that one (its duplicate copy was removed).
- **Politique 1 (⊗ reform):** mechanical `⊗`→`×` + atom subscripting (matches the M2
  reform already done), not per-concept canonical replacement.
- **Formula property:** `m2:hasStructuralGrammarFormula` (m2 prefix, defined in M2), NOT
  `m0:tensorFormula` (retired) nor `m0:hasStructuralGrammarFormula`.
- **BmcSimulation** de-classified: it is sim-config data, renamed off the `M0_` prefix
  (`BmcSimulation.jsonld`), Bmc.js loader path updated — excluded from check-M0. Formal
  classification + grammar is Worksite A.
- **`m1:domain` values** are Title-Case labels with spaces (e.g. "Fire Safety", "Coding
  Theory"), and need no matching M1 extension to be valid.

## 6. Discipline / traps (all learned the hard way this campaign)
- **Gate = check-M0**, not the standalone validator alone. The standalone SHACL and
  check-M0 share the **same schema**, but the checker adds C01–C14 on top. Always run both.
- **Casing (folder vs file).** The gate derives the instance name from the **file stem**;
  a folder `Vco` with file `M0_VCO.jsonld` passes on Windows, fails on Linux/CI (and vice
  versa). Canonical = `M0_<folder>.jsonld`. The modernizer emits `CASING_WARNING` + the
  case-safe two-step `git mv`. Fix the file name, don't just tweak the alias.
- **ORIVE is a vestige** — always `REVOI`. The gate tolerates `ORIVE` inside a prose
  string but the notation rule forbids it; the modernizer rewrites `\bORIVE\b`→`REVOI`.
- **Dangling aliases.** An alias used in the body but absent from `@context` (e.g.
  `m1core:simulationTitle`) yields a non-absolute IRI → C15 fail. The modernizer migrates
  `m1core` unconditionally and reports any other `UNRESOLVED_PREFIXES`.
- **Bare JSON numbers parse as `xsd:double`** — that is why Option B exists. Do not "fix"
  it by forcing `xsd:float` coercion everywhere.
- **Write-path / ORIVE-safety:** deliver rewritten instances as files or local scripts for
  Michel to run; never a server write-path (it can silently corrupt `REVOI→ORIVE`). Grep
  outputs for `orive`.
- **Encoding:** always write with `ensure_ascii=False` (never escape `×` `|` `√` `⊗` or
  chemical subscripts). Never let a literal `⊗` land in any file — not even in a changelog
  or a checker banner (both were caught and fixed this campaign).
- **Surgical git.** `git add` by explicit path only — never `git add -A` / `git add .`.
  Never commit the throwaway vectors (`patch_*.py`, `rewrite_*.py`, `fix_*.py`,
  `modernize_*` outputs left in the repo root) or the `_02_housekeeping/` scratch.
- **`modernize_m0.py` is a keeper** (lives in `ontology/cli-tools/`), unlike the throwaway
  patch scripts.
- **Presence ≠ liveness:** `M3_GenesisSpace.jsonld` is dead — never reference or copy it.

## 7. Definition of done (per instance)
- `check_m0_instances.py --instance <Name>` → **C01–C15 all OK, PASS**, AND
  `validate_m0_instance.py <path>` → **VALIDATION PASSED**.
- Hard scans: `⊗`=0, `⊕`=0, ket `⟩`=0, `orive`=0, valid JSON.
- Any `CASING_WARNING` resolved (file renamed via `git mv`), no `UNRESOLVED_PREFIXES`.
- Commit surgically by path; regenerate `docs/reboot-kit/TSCG_FileTree.md` with
  `tscg_generate_filetree.py` after any rename/structural change, and reload it into
  Project Knowledge.

## 8. Fresh session state (perishable — confirm, never trust)
- **Current HEAD:** `<confirm: git rev-parse HEAD>` (last seen ~ `0.1.88`).
- **Active worksite:** check-M0 campaign — Group C (`⊗`-value reform) is next.
- **In flight:** none committed by this HandOver. If the last batch's commits/pushes
  (`0.1.86`–`0.1.88`: APIServer, modernize_m0 v3, BmcSimulation de-class, FileTree regen)
  are not on HEAD, verify and re-push.
- **Immediate next step:** branch the `⊗`→`×` value reform into `modernize_m0.py`
  (Politique 1) and pilot it on the colour lot (Group A), gate both, deliver, commit.
- **Deferred:** Worksite A (Simulation Ontology grammar + dead-M3 repair).

---

*Context, not authority: this campaign has taken PASS from 3 → ~17. Every green instance
was verified against both gates on HEAD. The next session re-verifies before trusting any
number here.*
