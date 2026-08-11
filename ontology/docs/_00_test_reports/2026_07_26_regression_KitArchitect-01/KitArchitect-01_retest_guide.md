# KitArchitect-01 — Re-test guide after the PEPITE fixes (2026-08-09)

**From**: Echopraxium (with the collaboration of Claude AI)
**To**: KitArchitect-01 — SEERAVERSE Research Initiative

Thank you for the regression report. It was genuine territory resistance: precise,
with provenance, contre-hypotheses, and honest weakening where the evidence was thin.
Four of the five confirmed/design pépites are now fixed. This guide asks you to
re-test **from a fresh checkout of the latest `main`**, not by patching your local copy.

## Why a fresh checkout (not a patch)

You tested at commit `787d9aa`. Since then the corpus itself advanced several sessions
(CTX-4 absolutisation, template rename, the new WS-5 validator, the worksite YAML) AND
the API server fixes landed. Patching only the server would test new code against an
old corpus — you'd re-see data defects that are already closed. A clean checkout removes
that noise and gives a valid re-test against the reference state.

## Step 1 — Fresh checkout of the latest main

```
git clone https://github.com/Echopraxium/tscg.git tscg-retest
cd tscg-retest
git log -1 --format="%H %s"
```

The HEAD should be at least **`9cc3868`** (or later on `main`). All five confirmed
pépites plus the M0_Poclet# phantom-namespace repair are in by then. If your existing clone is fine, instead:
`git fetch origin && git reset --hard origin/main` — but a fresh clone is cleaner.

## Step 2 — Install and run the server's own test suite

```
cd instances/tscg-tools/TscgOntologyAPIServer/src
python -m pip install -r requirements.txt
python -m pytest ../tests/ -q
```

Expected: **77 passed** (includes 5 new regression tests named `test_pepites_*`).
These are the guard that PEPITE-001 and the scope filter cannot silently come back.

## Step 3 — Launch the server against the active corpus

Mount the **repository root** as the ontology dir (so both `ontology/` layer files and
`instances/` are discovered):

```
python tscg_api_server.py --ontology-dir <path-to>/tscg-retest
```

The loader now applies the canonical **active-corpus filter**: `_archives/`, `Ref/`,
`docs/`, `*/static/`, `migration_backups/` are no longer loaded. This is the same scope
definition the WS-5 validator uses — one notion of "active corpus" across the toolchain.

## Step 4 — Re-check the pépites

| Pépite | What to check | Expected after fix |
|---|---|---|
| **001** | `GET /corpus/list` → each graph `name` and `iri` | names end in `.jsonld` (no trailing `>`); iris have no `<…>` |
| **003 / 011** | `/corpus/list` graph count; search for `_archives`/`Ref` graphs | archive graphs absent; count reflects live corpus only |
| **005** | query `owl:inverseOf` objects | resolve to full IRIs; the previously-compact `m2:…` cases were all in archives, now not loaded |
| **013** | score fields typed `xsd:float` carrying prose | **FIXED** — coercion removed from @context; prose no longer cast |

## Known / in progress (please don't file as new)

**Fixed since your last run (verify these are gone):** PEPITE-001, 003, 005, 011, and 013.
The phantom `M0_Poclet#` namespace is also eradicated from the live corpus, the generation
template, and the SHACL.

**Still in progress — tracked, not bugs:**

- **Cross-poclet comparability (worksite WS-10).** This is the important one for you. The
  25 poclets still declare `m0` as their OWN local namespace, so `m0:scoreA` is a
  DIFFERENT IRI in each poclet. Queries WITHIN a single poclet work; queries ACROSS
  poclets (e.g. "which systems have scoreA > 0.8?") will NOT join yet, because there is
  no shared `m0:` vocabulary. The fix (WS-10) makes `m0:` always resolve to
  M0_Common.jsonld# (shared/joinable) and moves local concepts to `m0.<instance>:` (dot
  form). Until WS-10 ships, treat inter-poclet pattern queries as not-yet-supported —
  it's a planned worksite, not a defect.
- **Double `ontology/ontology/` in some graph IRIs.** An addressing decision
  (`_file_to_iri` + which root to mount), not a code bug. Being decided separately.
- **Colon-named terms** (`m0:instance:...`, `eagle_eye:Attractor`) in un-harmonised
  poclets — these are the CTX-5 defect WS-10 clears.


## Your §9 questions

Your four semantic questions (corpus roots at startup; scores numeric-only; canonical
vs archival naming; which local vocabularies need formal schema) are architecture
decisions that belong to Michel. He will answer them separately — they are taken
seriously as KitArchitect-level input, not treated as mere bug reports.

## If anything diverges

If Step 2 is not `77 passed`, or a pépite you expected closed still appears (other than
the double-`ontology` addressing item), please capture the exact request/response and the commit
hash (`git log -1 --format=%H`) so we can localise it against the reference state.
