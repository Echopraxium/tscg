# TSCG — Session Handover 2026-08-09

**Author**: Echopraxium with the collaboration of Claude AI
**Companion**: `_00_TSCG_Worksite_Map.md` v2.3.0 (durable index) + NEW this session
`ontology/docs/_01_Worksite/worksite.yaml` (structured state layer, schema 0.1.0).
This handover is the SNAPSHOT of this session.

**Authority**: `git show HEAD:<file>` only. HEAD at close = **`d5e81a7`** (origin/main,
pushed, working tree clean). Re-measure any figure at the next session's start.

---

## 1. WHAT WAS GRAVED THIS SESSION (2 lots, isolated, pushed)

Both lots are ADDITIVE — no corpus file was modified (every corpus `git status` was
clean throughout; the guard held). Staged scoped, committed alone.

- **`9bdf7c4`** — **WS-5 lot 1: TscgOntologyValidator engine (CTX family + `--source`)**.
  New package `ontology/cli-tools/validator/` (sibling of `check-M1/`, reuses
  `tscg_paths`): `tscg_validator.py` (CLI + JSON/human report + exit code),
  `sources.py` (`--source local|head|github` + in-scope git manifest + layer
  bucketing), `checks/ctx.py` (CTX-1..CTX-5 + CTX-CANON). Lot report at
  `ontology/docs/_01_Worksite/WS-5/WS-5_LOT1_Report.md`. Built strictly from the
  design spec §8 (CTX first; NO SHACL grammar generation).
- **`d5e81a7`** — **Worksite state layer**: `ontology/docs/_01_Worksite/worksite.yaml`
  (source of truth, schema 0.1.0) + `ontology/cli-tools/worksite_report.py`
  (renders the roadmap table, text + `--markdown` derivation).

**Tested on Michel's Windows machine before push** (not just my Linux VM):
validator `--source head` → `0 ERROR | 28 WARNING | 3 INFO` (identical to Linux);
worksite_report → WS-0 table renders. No `UnicodeEncodeError` on `⊗`/`→`/icons.

---

## 2. VALIDATOR — first-run report against HEAD (re-confirmed §7 of the spec)

`tscg_validator.py --source head --layers M3,M2,M1` → 22 governed files:
**`0 ERROR | 28 WARNING | 3 INFO`**.

The 2026-07-18 snapshot counts in the spec's §7 are CONFIRMED STALE:
- CTX-1 (undeclared m3:) = **0** (fixed Lot A) · CTX-2/3 = **0** (fixed) · CTX-4 = **0**
  (closed 2026-08-08).
- Only live CTX debt = **CTX-5 = 28**: `m3:eagle_eye` / `m3:sphinx_eye` colon-named
  `@context` terms across 14 files ×2 (inert aliases). Plus 3 benign CTX-5i
  (`rdfs:subClassOf/domain/range` coercion, INFO, not a defect).

### Ratified rulings (Michel, 2026-08-08), all recorded in the lot report
- **R1** — CTX-1 fires only in IRI-expansion position (a KEY, or `@id`/`@type` value),
  never in prose (`changes`/`rdfs:comment`/`skos:definition`). This is the difference
  between 5 false positives (all changelog/literal) and 0 ERROR. Honest limit: it is a
  deterministic lower bound; full JSON-LD expansion (spec §4) is a later hardening pass.
- **R2** — CTX-5i coercion idiom `{"@type":"@id"}` is benign, not a defect.
- **CANON** — the four layer roots, verified against HEAD (zero divergence):
  `m3→M3_GenesisGrammar`, `m2→M2_GenericConcepts`, `m1→M1_CoreConcepts`,
  `m0→M0_Common` (all `.jsonld#`, absolute). Governed corpus declares exactly one
  target per prefix (m3×24, m2×18, m1×18, m0×2). `m0` was ADDED to the CTX-CANON
  table this lot — it arms the check to flag the `M0_Poclet#` backlog once M0 is scanned.
- **R4** — NO M0 modelling for the validator. It stays a pure CLI sibling of the
  validation scripts (which carry no M0 either); only projected *product* tools
  (Miner/Explorer/APIServer) get an M0. Spec §1.3 amended for validation scripts:
  governance is git, not a poclet.
- **R3** — OPEN: schedule the CTX-5 = 28 fix as its own worksite (28 → 0 gauge).

---

## 3. WORKSITE YAML — schema ratified (Michel, 2026-08-08)

`ontology/docs/_01_Worksite/worksite.yaml` is now the SOURCE OF TRUTH for worksite
STATE; the prose map (`_00_TSCG_Worksite_Map.md`) is the narrative beside it. Ratified:

- **2 levels**: `WS-n → sub-item` (SC-n for WS-0, CTX-n for WS-2, VOC for WS-1…).
  The sub-item taxonomies are per-worksite and NEVER renumbered (map §1). No third
  "step" level for now.
- **status enum**: `done / design-decided / scoped / staged / todo / partial / blocked`.
- **gauge convention**: `current: <n>` only when a disciplined family measured it;
  `current: null` + `measured_by` otherwise. NEVER a raw `git grep` count (the 2310-⊗
  trap). This is the explicit YAML↔validator link.
- **location**: `worksite.yaml` at `_01_Worksite/` root; `worksite_report.py` in
  `cli-tools/`.
- **fill policy**: WS-0 fully modelled (SC-0..SC-11); WS-1..8 skeleton; sub-items
  filled at-the-flow when each worksite opens (anti-overfitting).

`worksite_report.py` usage: `--worksite WS-0`, `--markdown -o roadmap.md`.

---

## 4. IMPORTANT ENVIRONMENT FINDING — golden 151 vs 153 (Windows)

`check_M1.py --dry-run` on Michel's Windows machine returns **153**, not the golden
**151**. VERIFIED NOT A REGRESSION: `git diff --stat f0daa1a..HEAD` shows only the
handover `.md` between the golden-measurement HEAD and now — zero `.jsonld`, the 16 M1
files are byte-identical to the 151 measurement. The +2 is the documented `publicID=`
Windows bug (rdflib mints the base IRI from the Windows path, not `@base`).

Consequence for lot discipline: the golden gate value is OS-dependent. What matters is
STABILITY (153 before = 153 after, since the lots add no M1 file), not 151-vs-153.
**Michel's Windows baseline is 153, stable.** The validator is IMMUNE to this (reads
`git show HEAD:`, not the disk path) — which is exactly why it returned 28 on both OSes.

Backlog (do later): either fix `check_M1.py` `publicID=` (real fix) or record the
Windows baseline in `golden_values.json`. This is precisely the debt WS-5 exists to absorb.

---

## 5. NEXT WORKSITE — recommended: WS-5 lot 2 (FRB) or the CTX-5 fix

- **WS-5 lot 2 = FRB** (retired-formalism traces: ⊗, ket, GenesisSpace, KnowledgeField),
  same live-vs-changelog discrimination proven on CTX. This is what makes SC-9 (⊗) and,
  via DUP/STR, SC-5 (KnowledgeField) measurable — turning worksite.yaml's `current: null`
  gauges into real numbers.
- **or the CTX-5 fix** (R3): rename/restructure `m3:eagle_eye`/`m3:sphinx_eye`, gauge 28→0.
- SC-6 (DCC006=127) remains the heaviest WS-0 item; semantic, needs the validator's
  measurement primitives first.
- SC-3 graving still recommended AFTER WS-5 (wide ontologyType migration; do not
  hand-adjudicate).

---

## 6. BACKLOG CARRIED / LOGGED THIS SESSION

- **Update `meta.head` in worksite.yaml** — frozen at `f0daa1a` at build; real HEAD is
  now `d5e81a7`. Re-sync at next session start (or let a future `--measure` do it).
- **Golden 151-vs-153** (§4) — WS-5 target.
- **CTX-5 = 28** fix (R3).
- **Fill worksite.yaml sub-items** for WS-1/3/4/6/7/8 at-the-flow.
- **Join script** `worksite.yaml + live measures → table` (the `--measure` switch),
  then optionally the **TscgLayerCakeDashboard** (Electron GUI: roadmap + script
  launcher). Assessed PREMATURE this session — build after the validator matures and
  after deciding generated-HTML vs Electron. Depends on the structured worksite (done).
- **Worksite YAML→MD generator** (yaml is source of truth, md derived) — `--markdown`
  already does the table; a full map-regeneration generator is later.
- Carried from before: M0_Common refactor (`M0_Poclet#` → `M0_Common.jsonld#`, ~293 @id);
  ORIVE→REVOI cleanup lot (deprecated term; NOT a blind swap — KEEP changelog history,
  MIGRATE live terms, RE-DERIVE the ColorSynthesis quartet + CellSignalingModes off the
  retired ⊗/ket formalism); CTX-5 (~28) confirmed; SC-5 identifier collision; disk-vs-git
  case divergence.

---

## 7. OPENING PACKET FOR NEXT CONVERSATION

- Anchor on **HEAD `d5e81a7`** (re-measure at start; expect Windows check_M1 = 153).
- The validator and worksite_report are LIVE tools now — use the validator as the
  measurement instrument for the next lot instead of hand-scripting.
- Announce the worksite: **WS-5 lot 2 (FRB)** or the **CTX-5 fix**.
- Corpus is fetched from HEAD by the assistant; worksite.yaml + map v2.3.0 are current
  (worksite.yaml's `meta.head` is the one stale field — re-sync it).
- Working tree clean at close; origin/main synced.
