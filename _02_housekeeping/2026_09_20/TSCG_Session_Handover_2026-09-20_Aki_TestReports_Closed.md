# TSCG Session HandOver — Aki test-report thread CLOSED (2026-09-20)

**Author**: Echopraxium with the collaboration of Claude AI
**This thread did**: took Aki's 2026-08-14 retest (`TSCG_RETEST_2026-08-14`, 8800 vs
fresh 8801), separated the deployment-artifact noise from the real defects, and
**resolved every real defect**. Each fix was measured before/after, guarded by a test,
and shipped as its own commit.
**HEAD at close**: **`d22306f`** — *fix(api): graph IRI = raw-CDN URL (remove
/ontology/ontology/ doubling)*, on `origin/main`.

> **head-over-memory**: every number below was measured this session on HEAD (54318ee +
> the two new commits). HEAD may move; re-verify (§5) before acting.

---

## 0. Bootstrap (do this first)
1. Load skills: `head-over-memory`, `tscg-ontology-diagnosis-pipeline`.
2. Fetch the Smart Prompt from HEAD and follow it.
3. **HEAD is the only authority.** `git fetch --depth 1 origin main && git reset --hard origin/main`.

---

## 1. What shipped for the Aki thread (three commits)
```
d22306f  fix(api): graph IRI = raw-CDN URL (remove /ontology/ontology/ doubling)
7534bdc  fix(api): exclude test dirs from recursive corpus discovery (Aki tests/fixtures gap)
c80625c  fix(ontology): drop M2_MetaConcepts_Ref vestiges, rename tools -> ref_tool_links   [PEPITE-RT-008]
```
(The M1-golden refresh `3b81112` and the M0 instrumentation commit `54318ee` that sit
between `c80625c` and the two new ones are the *gate* workstream — separate HandOvers, not Aki.)

- **PEPITE-RT-008** (`c80625c`) — removed the pre-migration `M2_MetaConcepts_Ref.{jsonld,ttl}`
  copies (`ontology/tools/` + `ontology/Ref/`) that re-declared the canonical
  `m2:M2_GenericConcepts` `owl:Ontology` subject; renamed `ontology/tools/ →
  ontology/ref_tool_links/`; updated the `tscg_metrics` / `verify_migration` scope markers;
  added `test_ontology_identity_regression.py` (one active graph per governed subject).
- **tests/fixtures** — `load_pattern` now skips `tests/` dirs **in the recursive
  (broad-discovery) branch only**; an explicit non-recursive load (the test-suite loading
  `tests/fixtures/` on purpose) is untouched. Guard: `test_recursive_discovery_excludes_test_dirs`.
- **graph-IRI** — `_file_to_iri` now builds the named-graph IRI from the raw-CDN **root**
  (`.../main/`), not from `BASE_IRI` (the ontology *namespace* base `.../main/ontology/`).
  `BASE_IRI` is left intact (still used for content-IRI expansion + the `base_iri` field).
  Guard: `test_graph_iri_is_cdn_url_no_doubled_segment`.

Test suite: **80 passed** (was 78 at the base; +1 per new guard).

---

## 2. The Aki ledger — final
| Item (Aki 2026-08-14) | Resolution |
|---|---|
| PEPITE-RT-008 — duplicate `owl:Ontology` subject (8801=2) | ✅ resolved (`c80625c`); measured 2→1 |
| PEPITE-001/003/005/011/013, `M0_Poclet#` legacy, archives/Ref/docs/static | ✅ were **8800 deployment-mismatch artifacts** — already clean on a repo-root mount |
| tests/fixtures coverage gap (8801=1) | ✅ resolved — recursive discovery no longer sweeps `tests/` |
| double `/ontology/ontology/` (8801=28) | ✅ resolved — store re-measured **28→0**; graph IRIs now equal the files' CDN URLs |
| `M0_Poclet` non-IRI string note (8801=1) | ⚪ marginal, not treated (cosmetic notation note) |

**The Aki thread is closed** but for that one marginal note.

---

## 3. The double-segment — root cause on record
`_file_to_iri` returned `BASE_IRI + rel` where `BASE_IRI` already ends in `.../ontology/`
and, for the `ontology` anchor, `rel` restarts with `ontology/` → `.../ontology/ontology/…`
(28 canonical graphs: all M3, M2_GenericConcepts, etc.). The `instances` anchor got a
spurious `ontology/` prefix by the same bug. Only the **graph name** was malformed — all
subjects/predicates/objects were clean (0). The 2026-08-05 `@context` absolutisation
(`c49386c`) fixed content IRIs but not the graph-name construction, which is why a **static
grep read 0 while the loaded store still had 28** — the doubling happens at load time. Fix:
derive the raw-CDN root inside `_file_to_iri`.

---

## 4. Residual debt uncovered (NOT Aki, separate lot)
While verifying the graph-IRI fix, the graph list revealed **non-corpus `.jsonld` still
loaded into the active corpus** — the same scope-hygiene family as tests/fixtures:
- exercise samples: `_00_UserGuide/exercises/*/workflow_run_sample/*.jsonld`
  (e.g. StroboscopicYinYang, PokerHand3D) — they hit the filename-only fallback in
  `_file_to_iri`, a tell that they don't belong in the corpus;
- `ontology/` scratch/tool/template dirs: `ontology/sparql/`, `ontology/TSCG_InstanceGrammar/`,
  `ontology/InstanceSimulations/`, `ontology/StructuralGrammar/`, `ontology/rebuild M2/`.

None is an Aki item and none is a duplicate-identity or double-segment defect. Treat as a
separate **corpus-scope-hygiene lot**: decide which `.jsonld` under `ontology/` and
`_00_UserGuide/` are truly production corpus, then extend `_OUT_OF_SCOPE` (or the auto-load
patterns) accordingly — never by loosening a check. Measure before/after, as always.

---

## 5. Re-verification commands (run FIRST next session)
```
git clone --depth 1 https://github.com/Echopraxium/tscg.git /tmp/tscg && cd /tmp/tscg
git rev-parse --short HEAD
pip install -q --break-system-packages pyshacl rdflib pyld pyoxigraph fastapi httpx uvicorn pytest
pytest instances/tscg-tools/TscgOntologyAPIServer/tests -q        # expect 80 passed
# double-segment must stay 0 on the loaded store:
cd instances/tscg-tools/TscgOntologyAPIServer/src && python - <<'PY'
import sys, pathlib; sys.path.insert(0, ".")
from tscg_api_server import TscgStore
s = TscgStore(); s.load_pattern(str(pathlib.Path("/tmp/tscg")),
    ['M3_*.jsonld','M2_*.jsonld','M1_*.jsonld','instances/**/*.jsonld'])
q = 'SELECT (COUNT(DISTINCT ?g) AS ?n) WHERE { GRAPH ?g {?s ?p ?o} FILTER(CONTAINS(STR(?g),"/ontology/ontology/")) }'
print("doubled graphs:", next(iter(s.query(q)))['n'].value)   # expect 0
PY
```

---

## 6. Doctrine reminders
- HEAD is the only authority; a **static grep can lie** where the defect is born at load time
  (the double-segment) — re-measure on the store.
- Separate the deployment-artifact noise from real defects before acting (Aki 8800 vs 8801).
- One filter, two meanings is a smell: `_in_active_corpus`/`load_pattern` served both broad
  discovery and explicit loads — that is why the naive `tests/` exclusion first broke 4 tests.
- Keep independent fixes in separate commits; guard each so it cannot silently regress.
