# HandOver — post-SC-3 (WS-0) — 2026-09-02

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: resume TSCG work after SC-3 was graved, committed, pushed and verified.
Paste this as the opening message of a new conversation in the TSCG project.
**Nature**: a thin *loader* (Smart Prompt v17 §4) — it names skills, points to HEAD,
and carries fresh state only. It is NOT a content snapshot; read live facts from HEAD.

---

## 1. Load first — by name

- **`head-over-memory`** — authority discipline (verify at source; never recite a
  verifiable fact from memory or corpus).
- **`tscg-ontology-diagnosis-pipeline`** — the 6-phase validation pipeline.
- Add the task-specific skill when the session's topic is chosen (see §4):
  `tscg-instance-pipeline` (oscillator poclet) etc.

## 2. The one rule

**HEAD is the only authority.** Read versions, structure, counts from HEAD
(raw CDN `https://raw.githubusercontent.com/Echopraxium/tscg/main/…` or
`git show HEAD:<file>` in a fresh clone). Do not trust the numbers below without
re-measuring — they are perishable.

---

## 3. Fresh session state (perishable — re-verify)

- **HEAD**: `dfac73b` on `main` (measured 2026-09-02) — *treat as unverified; confirm
  with `git rev-parse HEAD` on a fresh fetch.*
- **SC-3 "Facet as an M3 principle" is DONE** — graved, committed, pushed, and
  independently verified on remote HEAD. The Facet mechanism lives in M3; the
  `m0:facet.*` apparatus is gone. What landed (re-verify versions at HEAD):
  - `M3_GenesisGrammar.jsonld` → 4.6.0 — `m3:Facet` (owl:Class = skos:ConceptScheme
    per individual), `m3:FacetValue` (owl:Class = skos:Concept), `m3:valueOf`
    (⊑ skos:inScheme), `m3:hasFacetValue` (carrier→value, IRI-only, no domain),
    axis `m3:Audience` + `m3:audience.{KitArchitect,KitCrafter,KitUser}`.
  - `M0_Common.jsonld` → 1.3.0 — entire `m0:facet.*` apparatus removed. (owl:versionInfo
    had been stale at 1.1.0 vs a 1.2.0 changelog head; 1.3.0 corrects the lag.)
  - `check-M0/M0_Instances_Schema_shacl.ttl` → v1.7 — 3 facet shapes removed; the
    survivor renamed+repointed `ForbidStringHasFacetShape` → `ForbidStringHasFacetValueShape`
    (guards `m3:hasFacetValue`).
  - `QRCodeToPocketCity/M0_*.jsonld` → 1.1.0 — Democratization migrated to
    `m3:hasFacetValue m3:audience.KitUser` (the only carrier; gauge X=1).
  - `validator/checks/axis.py` (new) + 2-line registration in `tscg_validator.py` —
    the WS-5 **AXIS** check family that gates SC-3.
  - Gates passed: linter (0 new warning), AXIS (0 finding, proven live), **Pellet OWL DL
    consistent** (Audience class/individual punning confirmed), SHACL CONFORMS:True,
    `run_all_layers` (SC-3 exonerated).
- **Companion commits also pushed**: `.gitattributes` pins `*.jsonld`/`*.ttl` to
  `eol=lf` (kills the Windows autocrlf ENC001 artifact); `TSCG_FileTree.md` regenerated;
  housekeeping (TODO, PokerHand3D screenshot, `instances/_01_Worksite/`).
- **Canonical SC-3 docs on HEAD** (read them, don't recite):
  - Decision Record **v2.0.0** (the re-scope; supersedes the v1.0.0 four-axis model):
    `ontology/docs/_01_Worksite/WS-0/2026_09_02/SC-3_Facet_Decision_Record.md`
  - Frozen model spec: `ontology/docs/_01_Worksite/WS-0/SC-3_M3_Facet_Draft_v2.md`
  - HandOvers of this crafting session:
    `instances/_01_Worksite/2026_09_01/` (Head Chef's chosen layout: HandOvers under the
    *crafting* tree; Record+spec under the *ontology* tree).

---

## 4. On the shelf — pick one to resume (NONE started)

1. **Phase-shift oscillator poclet** — the original topic that spawned SC-3. Reading **C**:
   round-trip as a fidelity test (encode → decode → redraw; the un-redrawable part = the
   epistemic residue). Support circuit = transistor + 3×RC, chosen sinusoidal. Pipeline
   Étape 2 (analysis) never started — it was paused when SC-3 opened. → load
   `tscg-instance-pipeline`.
2. **EpistemicResidue / Sieve** — now UNBLOCKED. Diagnosed as a `m3:FacetValue` **with a
   contract** (round-trip + residue delta), NOT a new `ontologyType`. The Facet mechanism
   is now graved, so the contract-on-value hook exists (Record v2.0.0 §1).
3. **Golden `shacl_violations` re-baseline** (M1 / SC-6 hygiene, NOT SC-3) — golden
   expects 680, current pyshacl reports 664 (a −16 that reproduces on pristine HEAD; the
   M1 SHACL schema is byte-identical to HEAD, so no shape was loosened). Confirm the 16
   are benign, then either pin the pyshacl version that produced 680 or `--update-golden`
   to 664 with a recorded note.

## 5. Loose ends / governance (not blocking)

- **`main` is a protected branch**; direct pushes succeed via owner bypass but log a rule
  violation each time. If external contributors (e.g. Aki) join, switch to branch → PR.
- **Doc layout**: HandOvers now live under `instances/_01_Worksite/` (crafting), Record +
  spec under `ontology/docs/_01_Worksite/WS-0/` (ontology). A v1.0.0 Record copy still
  sits in `WS-0/Next Conversation_2026_07_30/` — two versions, not a faulty duplicate;
  prune the old one only if you want a single live copy.
- **Reload `TSCG_FileTree.md` into Project Knowledge** if not already done (owner
  maintenance; the resident copy drifts after structural changes).

---

*State: SC-3 closed and verified on remote HEAD. Repo clean. Nothing in flight.
Resume from §4.*
