# TSCG — Session Handover 2026-07-30

**Author**: Echopraxium with the collaboration of Claude AI
**Companion**: `_00_TSCG_Worksite_Map.md` v2.2.1 — the durable index. Read it first.
This handover is the SNAPSHOT of this session.

**Authority**: `git show HEAD:<file>` only. HEAD at close = **`72487e1`** (origin/main).
Figures below were measured 2026-07-30; re-measure at the next session's start.

---

## 1. WHAT WAS GRAVED THIS SESSION (pushed to origin/main)

Two commits, both clean (`working tree clean`, up to date with origin/main):

- **`d92ded2`** — WS-n worksite reorganization (folders `_00_Worksite_00_SC1-9`→`WS-0`,
  `_01`→`WS-8`, `_02`→`WS-3`); Canopy `_protos/`→`instances/poclets/CanopyGraphVizProto/`
  (typed `m3:Poclet`); `TscgLayerCakeMCPServer` added; SC-2 recorded complete; SC-3
  Decision Record + worksite map v2.2.0; empty stray files removed.
- **`72487e1`** — docs refresh: worksite map **v2.2.1**, reference corpus **v3.0.1**,
  file tree **v17.0.1**, smart prompt **v16.3.0** (v16.2.0 archived under
  `SmartPrompts/`); `create_files_URIS.py` fixed to read `git ls-files` (not local
  disk); case-divergence debt recorded.

---

## 2. SC-3 (FACET) — DESIGN DECIDED, **NOT GRAVED**

Full record: `SC-3_Facet_Decision_Record.md` v1.0.0 (committed under
`WS-0/Next Conversation_2026_07_30/`).

**Decided**: four-axis model **SCALE / NATURE / AUDIENCE / DOMAIN** (decomposes the
overloaded `ontologyType`); A1 (`m3:Facet`=axis, `m3:Focus`=value); Conferred/Derived
sub-typing **retracted**; `m3:Facet` to be **lifted** from the existing `m0:Facet`.

**When it gets applied — read this, it answers "when are the Facet decisions taken
into account":** the decisions are *recorded*, not *applied*. Nothing changed in the
ontology files this session — `m3:Facet` does not exist yet, `ontologyType` is still
the single instance-type property. Graving happens in a **dedicated SC-3 session,
AFTER WS-5** (the validator engine), because it is a wide `ontologyType` migration
across M3/M2/M0 that must be measured per-decision, not hand-adjudicated. Decision now,
graving later — deliberately separated.

**Owed at graving** (Decision Record §7-8): OWL 2 punning check on Pellet; §3 admission
contract (likely a WS-5 executable check, not frozen M3 SHACL); layer-role residue;
DOMAIN axis typed WITH SC-5. Names → WS-4.

---

## 3. NEXT WORKSITE — chosen: **WS-2 / CTX-4**

Michel elected to continue with CTX-4 (distinct from SC-2, which is complete — SC-2
only fixed CTX-4 on the M2 file; the M1/M3 remainder is WS-2).

- **Scope**: normalise relative `mN` prefixes → absolute (relative prefixes leave
  `m3:*` predicates silently unresolved). Map cites ~19 occ (2026-07-24), ~15 across
  ~10 M1 extensions + some clean M3 files.
- **First action next session — re-measure CTX-4 on HEAD.** The ~19 count predates
  many commits since; do NOT trust it. Re-fetch HEAD, recount per file, THEN edit.
- **Lot discipline**: measure each file before/after; unexplained golden delta blocks
  the commit; isolated lots to keep golden interpretable (like SC-2's "Commit 1 — CTX").
- **Tool caveat** (map §5): `tscg_metrics.py` wires its SHACL pass to `check-M1` and
  ignores `--shacl-path`. Harmless for CTX-4 (prefix normalisation, not an arbitrary
  SHACL pass), but relevant if verifying a SHACL effect mid-lot — hence WS-5 is
  recommended before heavy lots. CTX-4 is still fine to do alone.

Recommended order otherwise (map §9): WS-5 → CTX-4 → SC-6 → … → SC-3 graving.

---

## 4. OWED OUTSIDE GIT — Cyclop v0 corpus hygiene

The project ("TSCG Cyclop v0") corpus still carried stale/obsolete files. Before the
next conversation:

- **Remove (genuinely obsolete — teach ORIVE/Hilbert)**:
  `00_TSCG_Map_Territory_Theoretical_Foundation.md`,
  `00_M3_Philosophical_Basis_Sketch.jsonld`,
  `TSCG_Smart_Prompt_v16_2_0.md`.
- **Refresh to HEAD/session versions**: worksite map v2.2.1, reference corpus v3.0.1,
  file tree v17.0.1, smart prompt v16.3.0; and the 3 stale ontologies
  (M2 16.19.0, M3_BicephalousPerspective 1.5.1, M3_GrammarFoundation 2.5.0).
- **Leave alone**: ~22 M0 instances carrying residual `⊗`/`ORIVE` — these are current
  files with a *notation debt* (a future corpus-wide migration), NOT obsolete files.

---

## 5. OPENING PACKET FOR NEXT CONVERSATION

- Announce the worksite: **"WS-2 / CTX-4"**.
- Attach (or ensure present in the project corpus): **`_00_TSCG_Worksite_Map.md` v2.2.1**.
  Confirm the corpus carries 2.2.1, not a residual 2.1.0/2.2.0.
- Do NOT attach the SC-3 Decision Record for CTX-4 — it belongs to the SC-3 graving
  session (post-WS-5), not this lot.
- The corpus is fetched from HEAD by the assistant; no ontology files to upload.

---

## 6. CROSS-CUTTING DEBTS CARRIED (map §8)

- **Case divergence** local vs versioned (Windows `core.ignorecase`): `Kidneys`↔`kidneys`,
  `Vsm`↔`vsm`, `M0_Vco`↔`M0_VCO`, etc. `git ls-files` gives correct case; disk
  realignment (fresh clone) deferred to a multi-platform need.
- **SC-5 identifier collision** in `M1_Schema_shacl.ttl` (two referents).
- **Stale "163"** note in `golden_values.json` (should read 151).
- **M0 notation debt**: residual `⊗`/`ORIVE` in ~22 instances — future migration.
