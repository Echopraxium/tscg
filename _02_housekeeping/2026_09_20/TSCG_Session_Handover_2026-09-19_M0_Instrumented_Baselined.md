# TSCG Session HandOver — M0 gate INSTRUMENTED + baselined (2026-09-19)

**Author**: Echopraxium with the collaboration of Claude AI
**This session did**: found that **M0 was never actually measured** (the gate's `run_m0()`
ran the checker but discarded its numbers), instrumented it, **reviewed** the real M0 state,
and **captured the first M0 golden baseline**. The M0 gate now measures and guards M0. Gate
is GREEN, legitimately.
**HEAD at close**: the M0-instrumentation commit on top of **`3b81112`** — fill the SHA after
`git commit` (message: *"feat(gate): instrument M0 (parse check_m0 metrics) + baseline the M0
migration backlog"*).

> **head-over-memory**: every number below was measured this session on HEAD `3b81112` (and
> re-measured on Michel's machine — identical). HEAD may move; re-verify (§6) before acting.

---

## 0. Bootstrap (do this first)
1. Load skills: `head-over-memory`, `tscg-ontology-diagnosis-pipeline`.
2. Fetch the Smart Prompt from HEAD and follow it.
3. **HEAD is the only authority.** `git fetch --depth 1 origin main && git reset --hard origin/main`.

---

## 1. What shipped (one commit)
```
<new>    feat(gate): instrument M0 (parse check_m0 metrics) + baseline the M0 migration backlog
3b81112  fix(gate): refresh M1 golden 680->664 + add Cartography to gate (files 16->17)   (previous)
```
Two files:
- **`ontology/cli-tools/run_all_layers.py`** — `run_m0()` rewritten: it now parses
  `check_m0_instances.py` output (the `RESULTS` line + per-check `[Cxx] … N FAIL(s)` lines)
  into `{files, errors, warnings, shacl_violations, pass, fail, by_code}`, mirroring
  `run_m1()`. Traceback still fails loudly (a crashed checker reports no failures, which
  looks like success).
- **`ontology/cli-tools/golden_values.json`** — M0 block: note replaced with an SC-6-style
  baseline warning, then numbers captured via `--update-golden`.

Untracked and deliberately OUT of the commit: `CODE_OF_CONDUCT.md`,
`_02_housekeeping/2026_09_19/`, `instances/_01_Worksite/2026_09_16/`,
`instances/poclets/World2DProjection/static/_docs/`, `.../static/src/W2P_COASTLINE.js`.

---

## 2. Gate state at close (verified GREEN)
```
── M1 ──  [OK] files 17 · [OK] errors 151 · [OK] warnings 3 · [OK] shacl_violations 664
── M0 ──  [OK] files 43 · [OK] errors 125 · [OK] warnings 0 · [OK] shacl_violations 22
── M2 / M3 ──  NOT INSTRUMENTED
GATE: PASS — counts match the reference.
```
Golden `M0` block now holds: `files 43`, `errors 125`, `warnings 0`, `shacl_violations 22`,
`pass 18`, `fail 25`, and `by_code {C02:22, C03:22, C07:22, C08:6, C09:22, C10:2, C11:3,
C12:25, C13:1, C15:22}`. `compare()` guards all four TRACKED keys **and** the `by_code`
breakdown, so any per-check regression will now trip the gate.

---

## 3. The finding — M0 was UNMEASURED despite the label
Before this session, `run_m0()` returned only `{_raw_exit, _captured}` — no metric keys. So:
- `--update-golden` copied nothing (`new` was empty); the M0 golden stayed number-less.
- `compare()` had no M0 keys to check → M0 passed **trivially**. The `status: INSTRUMENTED`
  label was aspirational. This is exactly the *"un-instrumented ≠ passing, it is unmeasured"*
  trap — hidden behind a green-looking label. Fixed now.

---

## 4. The M0 baseline = a measured MIGRATION BACKLOG (reviewed, not blessed)
`check_m0_instances.py v1.5.1`: **43 instances, 18 PASS / 25 FAIL.** Per-check failures:

| Check | Meaning | FAILs |
|---|---|---|
| C12 | **tensor remnants** — the banned `⊗` operator still in M0 instances | **25** |
| C02 · C03 · C07 · C09 · C15 | v1.5 cluster: `m0:`=M0_Common#, `m0.<inst>:` alias, no obsolete aliases, `owl:imports M0_Common`, SHACL v1.5 | **22** each |
| C08 | `m1.extensions.` pattern | 6 |
| C11 | enum values as IRIs | 3 |
| C10 | score bare numerics | 2 |
| C13 | `ontologyType` only in `@graph[0]` | 1 |

**Metric mapping chosen** (mirrors M1; SHACL tracked separately): `errors` = sum of
**non-SHACL** check failures = **125**; `shacl_violations` = C15 = **22**; `files` = 43;
`warnings` = 0. (Alternative considered and rejected: `errors` = failing-instance count = 25;
the per-check sum is more sensitive to regressions.)

This capture **MEASURES the debt; it does not bless it.** The 25 failures are baselined so the
gate can catch *new* regressions — they are not fixed.

---

## 5. Remaining debts (SEPARATE lots — NOT this session)
- **M0 repair campaign** — lower C12 (25× `⊗` remnants) and the v1.5 cluster (22×) by
  **repairing instances**, never by loosening a check. A campaign HandOver already exists:
  `_02_housekeeping/2026_08_23/TSCG_HandOver_CheckM0_Campaign.md`. Each real drop → a
  documented `--update-golden` (same discipline as the M1 −16).
- **Cosmetic note fix** — the golden M0 `note` still opens with *"FIRST-CAPTURE BASELINE (run
  --update-golden to fill the numbers…)"*, wording written **before** capture and now stale
  (numbers are in). Trim the bootstrap parenthesis; does not affect the gate.
- **M0 `_delta` reads "no change"** — a first-capture artifact (there were no previous
  values), not a real "nothing moved". Harmless.
- **M2 / M3 still NOT INSTRUMENTED** — no runner wraps their SHACL. The real remaining
  frontier: the gate now measures M1 + M0, not the whole cake. `tscg-generate-mn-grammars`
  can produce the M2/M3 SHACL; a runner must then wrap it (mirror `run_m1`/`run_m0`).
- **M1 SC-6 backlog** — `errors 151` + SHACL debt (476-subset) remain EXPECTED non-zero;
  lower only by repairing data / fixing a SHACL bug.

---

## 6. Re-verification commands (run FIRST next session)
```
git clone --depth 1 https://github.com/Echopraxium/tscg.git /tmp/tscg && cd /tmp/tscg
git rev-parse --short HEAD                                   # the M0 commit? else re-measure
pip install -q --break-system-packages pyshacl rdflib pyld pyoxigraph
python ontology/cli-tools/run_all_layers.py                  # expect GATE: PASS, M0 43/125/0/22
# review the M0 detail directly:
cd ontology/cli-tools && python check-M0/check_m0_instances.py && cd ../..   # expect 18 PASS / 25 FAIL
```

---

## 7. Doctrine reminders
- HEAD is the only authority; §2–§4 figures are dated `3b81112` + the M0 commit.
- A checker whose numbers are discarded is a layer that is **unmeasured**, not passing — even
  with `status: INSTRUMENTED`. Instrument = parse + compare, not just "run".
- Baselining a backlog is legitimate (it guards regressions) but must be **loud**: the note
  says it measures, not blesses. Lower it only by repairing instances, never by loosening a
  check.
- Keep independent changesets in separate commits.

---

## 8. Unrelated open thread (different HandOver)
The **World2DProjection poclet** remains a separate workstream (see its own HandOver). It is
the only M0 poclet at C12-clean + full PASS alongside the reference set — it touches only the
simulation (client of M0); no further gate impact.
