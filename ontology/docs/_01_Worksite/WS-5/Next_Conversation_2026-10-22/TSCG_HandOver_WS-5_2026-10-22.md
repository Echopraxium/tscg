# TSCG HandOver — WS-5, 2026-10-22: SC-5b done → implement lot NS-SEP

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-22
**Follows**: `../Next_Conversation_2026-10-15/TSCG_HandOver_WS-5_2026-10-15.md` (superseded
for "what next"; keep it for the SC-5b scope) and, through it, the 2026-10-12 HandOver
(working method, push path).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — NS-SEP rewrites IRIs in M1 and M0 files.
3. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-5/SC-5b/SC-5c_DomainModel_DesignNote.md` — **§13** (lot
     NS-SEP, prefix rule) and **§14** (rule "a domain and a combo never share a local name").
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` §8.0f — "Lot SC-5b (done)" and
     "Open after SC-5b".

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of the SC-5b commit ("Lot SC-5b:
  subdomains become domain classes; gate M1 133/1/296 -> 132/1/294"), on top of `6f7cd5a`.
- **Gate**: `GATE: PASS` with M1 132 / 1 / 294 (`--update-golden` done in the SC-5b commit,
  reason written under `M1._delta_reason`).
- **Pellet reasoner**: PASSED on the 6 key SC-5b files (M1_Domains, Biology, Physics,
  Education, Optics, music), run locally by Michel 2026-10-22 (needs Java 25 — the session
  VM had 21, so it could not run there). SC-5b is fully validated.

## 2. Next goal — lot NS-SEP (diagnosis pipeline, one lot, mechanical)

Rule (Michel, 2026-10-14; SC-5c note §13): **one `:` per CURIE, one prefix per defining
file**; prefix = layer + `.` + the defining file's name in lower case.
- `m1:domain:X` → `m1.domains:X`, prefix `m1.domains` → `…/ontology/M1_Domains.jsonld#`
- `m1:extension:<ext>:X` → `m1.<file>:X`, prefix → that extension file's `#`
  (`M1_Physics` → `m1.physics`, `M1_BusinessModeling` → `m1.businessmodeling`,
  `M1_music` → `m1.music`)
- M1_CoreConcepts **keeps `m1`** (HandOver 2026-10-15).
- Each file that uses a prefix declares it in its `@context`.

Why: today `m1` → `M1_CoreConcepts.jsonld#`, so `m1:extension:physics:Physics` expands into
CoreConcepts although the class is defined in M1_Physics — a hidden defect.

Measured at handover (post-SC-5b tree, `git grep` on `*.jsonld`, **re-measure**):
`m1:domain:X` 68 occurrences in 9 files; `m1:extension:<ext>:X` 1,334 in 24 files.
Tools that also carry these strings: `check_M1.py`, `tscg_layercake_health_map.py`,
`test_m1_domains.py`, `check-M0/M0_Instances_Schema_shacl.ttl`, the TscgLayerCake MCP server.

**Ask Michel before writing** (both change the scope):
1. **Archives**: `migration_backups/` and `domain_format_fix_backups/` hold old copies with
   these strings. Proposed: leave archives untouched (they document the past).
2. **Extension-local property names** (`m1:extension:education:asfidBasis`,
   `…:instanceEvidence`, …) are the same pattern on properties, not classes. Proposed:
   rename them too (`m1.education:asfidBasis`), so that one convention exists.

Expected gate: counts unchanged (a pure rename). Any move = a check that reads the old
string; show it before `--update-golden`. Add a negative test: an `m1:extension:` CURIE in an
M1 file must be flagged once the lot is in.

## 3. Then, in order

1. **Lot M0** — `m1:domain` → `m1:belongsToDomain` with domain IRIs in the M0 files (+ M1
   files, M0 template); delete `m0:subdomains` (7 poclets) and `m0.vco:subdomains`; M0
   checks apply the M1 rule (in `check_m0_instances.py`, which sees the M1 hierarchy).
   The stale `m1:edu:InstructionalDesign` in M0_TPACK (a dangling old prefix) goes there.
2. **SC-5c** — usefulness test first (§0): FireTriangle, RGB_Additive, Transistor on paper.

## 4. Found during SC-5b (not fixed — recorded for later lots)

- **`check_M1` counts every SHACL result twice** (one "Focus Node" + one "Message" line):
  the M1 `shacl_violations` golden value is 2 × the real number of results (already noted
  in `golden_values.json` for lot C1). A fix would halve the frozen value — its own lot.
- **LayerCake Health Map, same tool on both trees**: M1 green 98/297 (2026-10-06,
  `ffa6206`) → 167/324 (after SC-5b). M3 red rose 79 → 94: the `@vocab` defect (D2) moved
  from `M3_BicephalousPerspective` to its larger successor `M3_OdinsWisdom` (and
  `M3_GrammarFoundation` still has it); the four D5 of M3 are gone. Biggest levers left:
  `@vocab` out of those two M3 files (≈94 cells), the M0 lot (30/43 red), M2 bare keys.
- **Worksite map** (`WS-0/_00_TSCG_Worksite_Map.md`, ~line 356) still uses "SC-5b" for
  "SHACL-hardening" — the name is now taken by the subdomain lot; disambiguate.

## 5. Housekeeping

- Project Knowledge: reload `TSCG_ReferenceCorpus_Bootstrap.md` and `TSCG_FileTree.md`
  (new folder `WS-5/Next_Conversation_2026-10-22/`).
