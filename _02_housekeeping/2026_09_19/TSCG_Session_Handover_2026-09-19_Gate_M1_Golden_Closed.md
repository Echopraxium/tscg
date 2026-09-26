# TSCG Session HandOver — Gate / M1 golden — CLOSED (2026-09-19)

**Author**: Echopraxium with the collaboration of Claude AI
**This session did**: resolved the red M1 gate cleanly. Localised and **proved** the SHACL −16, classified it (belt-and-suspenders), and committed the two decisions from the 2026-09-18 HandOver. **The M1 gate is now GREEN, legitimately.**
**HEAD at close**: **`3b81112`** — *"fix(gate): refresh M1 golden 680->664 + add Cartography to gate (files 16->17)"*.

> **head-over-memory**: every number below was measured this session against HEAD `3b81112` (and its ancestors). HEAD may move. Re-verify (see §6) before acting.

---

## 0. Bootstrap (do this first)
1. Load skills: `head-over-memory`, `tscg-ontology-diagnosis-pipeline`.
2. Fetch the Smart Prompt from HEAD and follow it.
3. **HEAD is the only authority.** `git fetch --depth 1 origin main && git reset --hard origin/main`.

---

## 1. What shipped (two SEPARATE commits, in order)
```
3b81112  fix(gate): refresh M1 golden 680->664 + add Cartography to gate (files 16->17)   [Decision 2]
c80625c  fix(ontology): drop M2_MetaConcepts_Ref vestiges, rename tools -> ref_tool_links  [Decision 1 / PEPITE-RT-008]
c5fdefa  fix(World2DProjection): hue legend moved into left panel (CSS follow-up to A+B)     (previous)
```
- **Decision 1 (`c80625c`)** — the PEPITE-RT-008 cleanup: removed pre-migration `M2_MetaConcepts_Ref.{jsonld,ttl}` from `ontology/tools/` and `ontology/Ref/`; renamed `ontology/tools/ → ontology/ref_tool_links/` (tool-link `.url`s only); updated scope markers in `tscg_metrics.py` / `verify_migration.py`; added `test_ontology_identity_regression.py`; updated `CLAUDE.md`. Count-neutral on the gate.
- **Decision 2 (`3b81112`)** — the golden refresh + coverage fix: added `M1_Cartography.jsonld` to `check_M1.py` `M1_FILES` (files 16→17), and `--update-golden` (shacl 680→664) with a documented `_delta_reason`.

Untracked and deliberately left OUT of both commits: `CODE_OF_CONDUCT.md`, `instances/_01_Worksite/2026_09_16/`, `instances/poclets/World2DProjection/static/_docs/`, `.../static/src/W2P_COASTLINE.js`.

---

## 2. Gate state at close (verified GREEN)
```
── M1 ──  [OK] files 17 · [OK] errors 151 · [OK] warnings 3 · [OK] shacl_violations 664
── M0 ──  check_m0 runs; golden NOT captured
── M2 / M3 ──  NOT INSTRUMENTED
GATE: PASS — counts match the reference.
```
Golden `M1` block: `files 17`, `errors 151`, `warnings 3`, `shacl_violations 664`, `_previous.shacl_violations 680`, `_delta {files:"16->17", shacl_violations:"680->664"}`, `_updated 2026-09-19`, `_delta_reason` present.

---

## 3. The −16 — localised and PROVEN (corrects the 2026-09-18 hypothesis)
The prior HandOver guessed `aac3a05` (SHAPE 9 retarget). **That was wrong** — measurement shows the SHAPE-9 retarget is already baked into the golden 680. The real cause is **`c49386c`** (2026-08-05, WS-2/CTX-4): it absolutised the `m1`/`m2`/`m3` `@context` prefixes (relative → canonical `https://…/ontology/…#`) in 10 M1 extensions. **Data-only; no SHACL shape touched.**

Proof (check_M1 `--shacl` totals):
```
c49386c^ (ef06a01) = 680   (== old golden)
c49386c            = 664
HEAD               = 664    (fed2621 Cartography SHACL is +91/-0, count-neutral on the 16 gated files)
```

## 4. Classification — reclassification, NOT a loosening (belt-and-suspenders)
Per-message histogram (IRIs neutralised), 680 → 664:

| Constraint message | 680 | 664 | Δ |
|---|---|---|---|
| `m3:ontologyType must be declared exactly once` | 9 | 0 | −9 (false positives removed — property now resolves to canonical `m3:`) |
| `must use Fm1m2(<Domain>) notation` (combos) | 17 | 0 | −17 |
| `FORBIDDEN monoidal operator inside a combo formula` | 109 | 126 | +17 (same nodes, now correctly typed as `m2:DomainConceptCombo` → correct SC-1 constraint fires) |
| `well-formed signature ≥ 2 args` | 5 | 6 | +1 |

**26 message-lines removed, 18 added → NET −16 gate units.** No shape weakened; the validator bites *more* correctly. Verdict: `--update-golden` was the correct action, and the reason is recorded in the golden `_delta_reason` and in the `3b81112` commit body.

> Metric note for the future: `shacl_violations` counts **Message-lines + Focus-Node-lines** = **2× actual violations** (so 664 ≡ 332 real violations; the −16 ≡ −8 violations). This is how `check_M1.run_shacl` builds its list — keep it in mind when reasoning about counts.

> The `+17` "monoidal operator inside a combo formula" are **real SC-1 defects**, now correctly surfaced (previously masked under the wrong message). They are part of the existing SC-6 / SHACL debt — baselined, not fixed.

---

## 5. Remaining debts (SEPARATE lots — NOT this session)
- **M0 golden not captured** — `check_m0_instances.py` runs; run `--update-golden` once, REVIEW, then trust. (process/coverage debt)
- **M2 / M3 NOT INSTRUMENTED** — no runner wraps their SHACL. Un-instrumented ≠ passing. (coverage debt; `tscg-generate-mn-grammars` can produce the SHACL)
- **SC-6 backlog** — `errors 151` + the SHACL debt (476-subset) are EXPECTED non-zero; lower them ONLY by repairing data or fixing a SHACL bug, never by loosening a shape.

---

## 6. Re-verification commands (run FIRST next session)
```
git clone --depth 1 https://github.com/Echopraxium/tscg.git /tmp/tscg && cd /tmp/tscg
git rev-parse --short HEAD                                   # still 3b81112? else re-measure
pip install -q --break-system-packages pyshacl rdflib pyld pyoxigraph
python ontology/cli-tools/run_all_layers.py                  # expect GATE: PASS, M1 17 / 664
# (to re-confirm the -16 localisation, checkout c49386c^ and c49386c and diff check_M1 --shacl totals)
```

---

## 7. Doctrine reminders
- HEAD is the only authority; §2–§4 figures are dated `3b81112`.
- Never `--update-golden` to turn a red gate green — only to record an understood change (as done here).
- Keep independent changesets in separate commits.
- A shrinking SHACL count is either a real repair (→ refresh golden + reason) or a validator that stopped biting (→ fix, don't refresh). This −16 was proven to be the former.

---

## 8. Unrelated open thread (different HandOver)
The **World2DProjection poclet** is a separate workstream — see `TSCG_Session_Handover_2026-09-16_World2DProjection_ThematicMap.md`. Passes A (per-zone choropleth) + B (blue geographic globe) are committed; **Pass C** (zone selection + globe↔map linking, TRIZ-style), **Pass D** (layout redesign), the **Antarctica pole-polygon fix**, and **Pass E** (20–40 projections) are pending. That thread touches only the simulation (client of M0) — no gate impact.
