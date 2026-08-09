# TSCG — Session Handover 2026-08-08

**Author**: Echopraxium with the collaboration of Claude AI
**Companion**: `_00_TSCG_Worksite_Map.md` **v2.3.0** — the durable index, already graved
this session and current. Read it first.
This handover is the SNAPSHOT of this session.

**Authority**: `git show HEAD:<file>` only. HEAD at close = **`f0daa1a`** (origin/main).
Re-measure any figure at the next session's start; the map's non-CTX-4 numbers are stale.

---

## 1. WHAT WAS GRAVED THIS SESSION (7 lots, all isolated, HEAD-verified, pushed)

Each lot was measured before/after, staged scoped (never `git add -A` except the
housekeeping lot), and committed alone.

- **`c49386c`** — **WS-2 / CTX-4**: absolutised the relative `m1/m2/m3` `@context`
  prefixes in the **10 M1 extensions** (15 occ). Golden-stable (`check_M1` = 151
  before and after), linter 0 errors, Pellet consistent (electronics + optics).
- **`ce94045`** — **Template → instance rename**: `M0_POCLET_TEMPLATE.jsonld` →
  `M0_INSTANCE_TEMPLATE.jsonld` (absolute IRIs, `GenesisGrammar`, token
  `POCLET_NAME`→`INSTANCE_NAME`); PowerShell generator **ported to Python**
  (`create_new_instance.py`, auto-detects repo root, validates JSON, fixes the old
  script's hard-coded path + wrong template location); `create_new_poclet.ps1` retired.
- **`5dfb488`** — **Docs alignment**: 5 usage docs + the preprint aligned to the new
  name/token/script; fixed pre-existing stale `_v2` references and the wrong
  `TSCG_Grammar/` path; `files.txt` regenerated via `create_files_URIS.py`. Done with
  a one-shot Python script (`align_docs.py`, run on the user's machine) + manual
  preprint prose edits.
- **`63b6cdf`** — **Housekeeping**: `_open_cmd_window.bat` → `_00_open_cmd_window.bat`
  (root + ontology-linter); removed the empty stray file `owl_reasoning_test/python`.
- **`16c8ace`** — **CTX-4-bis / InstanceSimulations**: the 2 `ontology/InstanceSimulations/*`
  M0 files — `m3` absolutised (+ `GenesisGrammar`), `m0` self-path corrected to the real
  `.../ontology/InstanceSimulations/…` location.
- **`0bb062c`** — **CTX-4-bis / 11 poclet m0**: absolutised the `m0` self-prefix of 11
  live M0 instances to their correct git path — fixing Canopy (`Tscg…` folder),
  TvTestPattern (`tv_test_pattern` case), Vco (`M0_Vco`→`M0_VCO`), iching (`Iching` case),
  and Nakamoto (pointed at the wrong file `M0_Poclets.jsonld`). Done with `align_m0.py`
  (Python, on the user's machine — Nakamoto contains `ORIVE`).
- **`f0daa1a`** — **Worksite map v2.3.0**: closed WS-2/CTX-4 + CTX-4-bis (§2, §5),
  anchored `Current HEAD: 0bb062c`, logged the M0_Common refactor backlog (§8), added
  the 2.3.0 changelog entry with the ORIVE lesson.

**Net result**: **CTX-4 and CTX-4-bis are closed** — no relative `mN` prefix remains
anywhere in the live corpus.

---

## 2. WS-2 STATUS — essentially done

- CTX-1 fixed (Lot A). CTX-4 + CTX-4-bis closed this session.
- **Only CTX-5 remains** (~31, from a stale measurement — re-measure when opened):
  `@context` terms *defined* with a colon in their name (e.g. a term literally named
  `"m3:eagle_eye":`), distinct from normal prefixed-property usage. **Low priority** —
  not in the recommended order. WS-2 needs no more work to unblock anything.

---

## 3. NEXT WORKSITE — recommended: **WS-5 (Validator engine)**

Rank 1 in the map (§2). Rationale:
1. every remaining lot needs the same measurement primitives; today they were
   hand-scripted (`align_docs.py`, `align_m0.py`) — WS-5 builds them once, reusable,
   which is exactly what makes the step-by-step discipline less tedious;
2. the SC-3 graving (wide `ontologyType` migration across M3/M2/M0) must NOT be
   hand-adjudicated — it needs per-decision measurement from the engine;
3. tooling gap to close: `tscg_metrics.py` hard-wires the SHACL pass to `check-M1` and
   ignores `--shacl-path`; a runner for an arbitrary shape file is job one.
Build it in a FRESH session from `M0_TscgOntologyValidator_README.md` v0.1.0.

**Alternative if a focused non-engine lot is wanted**: the M0_Common refactor (§4).

---

## 4. NEW BACKLOG LOGGED THIS SESSION — `M0_Poclet#` → `M0_Common.jsonld`

Measured 2026-08-08: **29 poclets, ~293 `@id`** point score/gap/mean properties at the
non-existent namespace `.../ontology/M0_Poclet#` (`scoreA…scoreIm`, `epistemicGap`,
`mean`) — a leftover from the old template. The canonical vocabulary **already exists**
in `ontology/M0_Common.jsonld` (`.../M0_Common.jsonld#scoreA…`, `epistemicGap`), already
referenced by ~10 poclets. Target = rebrand the 293 IRIs onto `M0_Common.jsonld#`.

**NOT mechanical — two open sub-questions for the lot**:
1. the poclets' `mean` has no 1:1 in M0_Common, which defines `asfidMean`/`revoiMean`
   — decide the mapping, or add a `mean` term to M0_Common;
2. align on how the ~10 already-wired poclets reference M0_Common (owl:imports vs
   explicit IRI) before rebranding the rest.

Full entry in worksite map §8.

---

## 5. OTHER DEBTS CARRIED (map §8)

- **Case divergence, disk vs versioned** (Windows `core.ignorecase`): the *m0 IRIs*
  were corrected in content this session, but disk-vs-git dir/file case divergence
  (`Kidneys`↔`kidneys`, etc.) remains; disk realignment (fresh clone) still deferred.
- **CTX-5** (~31) — see §2.
- **δ₁ provenance**: ~17 scalar `m0:epistemicGap` measured but under-provenanced.
- **SC-3 graving**: design decided (`SC-3_Facet_Decision_Record.md` v1.0.0); grave only
  AFTER WS-5. Do NOT start it before the engine.
- Stale "163" golden note; SC-5 identifier collision; README↔jsonld drift — unchanged.

- **ORIVE → REVOI cleanup — VERIFICATION STEP for a dedicated lot** (measured 2026-08-08):
  residual `ORIVE` in **~16 live `.jsonld` data files** (~38 occ), plus many
  doc/analysis/archive files that are OUT of scope. **NOT mechanical** — three natures:
  * **KEEP**: `MIGRATION: ORIVE -> REVOI` changelog lines (legitimate history).
  * **MIGRATE**: live-term usages (`ORIVE_mean`, "using ORIVE basis", "ORIVE Map-Space").
  * **RE-DERIVE, don't swap**: the ColorSynthesis quartet (RGB/CMY/CMYK/HSL) and
    CellSignalingModes carry ORIVE tangled with the **retired `⊗`/ket formalism**
    (`R⊗V⊗E`, `|M⟩_ORIVE = 0.90|O⟩ + …`) — this overlaps the tensor→structural-grammar
    migration; their Sphinx-Eye blocks must be re-derived in REVOI order with `×`/`|`,
    not string-swapped.
  Verification procedure for the lot: `git grep -c ORIVE` per file → classify each line
  (history / live-term / retired-formalism) → migrate via a **script on the user's
  machine** → confirm with `git diff` that no `ORIVE -> REVOI` history line was flattened
  and no `ORIVE` was silently corrupted to `REVOI`. Needs Michel's per-file semantic
  ruling on reorder-vs-swap and on the ColorSynthesis re-derivation.

---

## 6. TERMINOLOGY — REVOI is canonical, ORIVE is deprecated

**REVOI** (Representability, Evolvability, Verifiability, Observability, Interoperability)
is the canonical Map / Sphinx-Eye acronym. **ORIVE** is the OLD ordering of the SAME five
dimensions (O, R, I, V, E) and is **deprecated**. Residual `ORIVE` in the corpus is stale
and should be migrated to `REVOI` where it is used as a live term — see the cleanup step
in §5.

**Two cautions when doing that cleanup** (this is why it must be careful, not blind):
1. It is NOT a blind find-replace. ORIVE→REVOI is a *reordering* of the same dimensions,
   so dimension lists and formulas may need re-ordering, not just an acronym swap; and
   `ORIVE -> REVOI` changelog lines are legitimate *history* — keep those.
2. The assistant's file-write path silently corrupts the literal `ORIVE` (writes `REVOI`
   instead) and masks it on re-read — `git diff`, not grep, is the authority. So run the
   cleanup as a **Python script on the user's machine** (as with `align_m0.py`) or as
   **manual edits**, never as whole files delivered by the assistant, and verify every
   changed line with `git diff`.

---

## 7. OPENING PACKET FOR NEXT CONVERSATION

- Anchor on **HEAD `f0daa1a`** (re-measure at start).
- Announce the worksite: **WS-5** (or the M0_Common refactor).
- The corpus is fetched from HEAD by the assistant; the worksite map is already v2.3.0
  and current — no upload needed unless the project corpus carries an older copy
  (confirm it reads 2.3.0).
- Working tree is clean at close.
