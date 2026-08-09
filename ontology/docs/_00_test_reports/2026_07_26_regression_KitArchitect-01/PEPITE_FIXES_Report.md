# TscgOntologyAPIServer — PEPITE fixes lot (KitArchitect-01 regression, 2026-07)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-08-09
**Base**: server v1.1.0 at repo HEAD `d5e81a7`
**Tested in a Linux VM**: existing suite 72 → **77 passed** (5 regression tests added).

## What this lot fixes

Closes **4 of KitArchitect-01's 5 confirmed/design pépites** in pure server code — no corpus
change, no ORIVE discipline needed.

### PEPITE-001 — `<IRI>` serialization (CONFIRMED bug)
`_ox_to_value()` returned `str(term)` for a `NamedNode`, which pyoxigraph renders in
N-Triples form `<...>` (angle brackets). `Path(g).name` then kept the trailing `>`
(`M0_VSM.jsonld>`). The Literal branch right below already used `.value`; the NamedNode
branch did not. **Fix**: NamedNode returns `term.value` (bare IRI). Same fix applied to
`graph_list()` and the `/corpus/list` name derivation. Reproduced before/after; the
end-to-end store now returns bare IRIs and clean names.

### PEPITE-003 / 005 / 011 — archive amplification & compact IRIs (scope)
`load_pattern()` used `rglob` with NO exclusion filter, so `Ref/`, `_archives/`,
`docs/`, `/static/`, `migration_backups/` were all loaded and amplified. This is KitArchitect-01's
root cause #1 (uncontrolled recursive discovery) and #2 (no canonical active-corpus
manifest). **Fix**: a module-level `_in_active_corpus()` filter — **identical to the
WS-5 validator's `_OUT_OF_SCOPE`** — applied in the loader. "Active corpus" now means
ONE thing across the toolchain: the validator measures it, the API loads it.

This single scope fix resolves:
- **PEPITE-003 / 011** — archives no longer loaded (verified end-to-end: a corpus with
  an `_archives/` copy loads 1 graph, not 2).
- **PEPITE-005** — the un-expanded `owl:inverseOf` values were ALL in `Ref/`/`_archives/`
  graphs. The governed `M2_GenericConcepts.jsonld` uses `{"@id": "m2:..."}` with `m2`
  declared absolute → expands correctly. Excluding archives removes the finding with no
  governed-corpus residue.

## Not in this lot

- **PEPITE-013** (xsd:float on prose, 29 M0 files) — CORPUS defect, tied to the
  `M0_Poclet#` → `M0_Common` refactor. Larger, needs ORIVE-safe local scripting.
  Next chantier; the WS-5 validator will get a datatype family to gauge it.
- **`ontology/ontology/` double segment** in some IRIs — NOT a code bug: it comes from
  mounting `--ontology-dir` at the repo root instead of `.../ontology`. This is KitArchitect-01's
  §9 Q1 (which roots for default startup). Recommendation: mount at the repo root and
  keep `ontology/`-prefixed patterns, OR mount at `.../ontology` with bare patterns —
  pick one canonical launch and document it.

## Files
    src/tscg_api_server.py                  (4 lines changed + 16-line scope block)
    tests/test_pepites_regression.py        (NEW — 5 regression tests)

## Commit & re-test
Additive to server code + tests. After commit + push, give KitArchitect-01 the commit hash; he can
re-run his suite against PEPITE-001/003/005/011 (expected: all cleared) and confirm
013 remains the only open corpus item.
