# WS-5 — Lot 1: TscgOntologyValidator engine (CTX family + source switch)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-08-08
**Spec**: `ontology/docs/_01_Worksite/TSCG_OntologyValidator_Worksite_README.md` v0.1.0, §8
**Authority**: measured against `git show HEAD:<file>`, HEAD = `f0daa1a`
**Golden gate**: `check_M1.py` = **16 files | 151 errors | 3 warnings** before and after
(this lot adds files only; no corpus file is touched).

---

## 1. What was built

A new package `ontology/cli-tools/validator/`, sibling of `check-M1/`, reusing
`tscg_paths` for relocatable repo-root resolution:

```
validator/
  tscg_validator.py     CLI + orchestration + JSON/human report + exit code
  sources.py            --source local|head|github + in-scope git manifest + layer bucketing
  checks/
    __init__.py
    ctx.py              CTX-1..CTX-5 + CTX-CANON advisory
  WS-5_LOT1_Report.md   this file
```

Delivered in this lot (spec §8 first target): **CTX family + `--source` switch**.
`FRB / DUP / NOT / STR` are declared in the family roster and print
`not yet implemented (later lot)`. **No SHACL grammar generation** (the §8 trap:
fix CTX first, else the grammar targets a broken IRI space).

**Hard guard honoured (spec §1)**: DETECTION ONLY. The engine never writes to the
corpus. `git status` after every run shows only the untracked `validator/` dir.

## 2. First-run report against HEAD (the spec's §7 re-confirmation)

`python tscg_validator.py --source head --layers M3,M2,M1` → **22 governed files**:

```
TOTAL: 0 ERROR | 28 WARNING | 3 INFO
  CTX-5   28   (m3:eagle_eye / m3:sphinx_eye colon-named terms, 14 files x 2)
  CTX-5i   3   (rdfs:subClassOf/domain/range coercion in M1_CoreConcepts — benign)
```

**The §7 snapshot counts are confirmed stale**, exactly as the spec required the
tool to check on first run:

| §7 (2026-07-18 snapshot) | HEAD (this tool, f0daa1a) |
|---|---|
| CTX-1 = 2 (undeclared m3:) | **0** — fixed (Lot A) |
| CTX-2/3 = 2 (rel+@vocab / bad @base) | **0** — fixed this session |
| CTX-4 = 14 (fragile relative prefix) | **0** — CTX-4 + CTX-4-bis closed this session |
| CTX-5 ≈ 30 (term name has `:`) | **28** defects + **3** benign coercions |

The only live CTX debt on HEAD is **CTX-5 = 28**: `m3:eagle_eye` / `m3:sphinx_eye`
declared as colon-named `@context` terms mapped to IRI strings across 14 files.
JSON-LD will not use a colon-named term as a prefix, so these are inert aliases.

## 3. Design decisions taken inside the deterministic band (for your confirmation)

These are technical choices; the *policy* is yours to ratify. Each is reversible.

1. **CTX-1 fires only in IRI-expansion position** (a prefixed KEY, or a value under
   `@id`/`@type`), never on a prefixed string inside prose (`changes`,
   `rdfs:comment`, `skos:definition`, an arbitrary property, a plain list item).
   *Why*: the naive all-string scan reported 5 "defects" that were **all** changelog
   prose or literals — including a `changes` line that itself documents the CTX-1 fix.
   Re-flagging documented history is the false-positive class the spec warns about
   for FRB; it generalises to CTX-1. Full JSON-LD expansion (spec §4) is the exact
   version and is deferred to a hardening pass; this key/@id/@type proxy is its
   deterministic lower bound.

2. **CTX-1 restricted to structural prefixes** (`m0..m3` + standard vocab prefixes
   rdf/rdfs/owl/xsd/dcterms/skos/…). An arbitrary capitalised data string like
   `"Mythology:"` in a reference table is data, not a namespace defect. The naive
   version cried wolf 407 times on `ontology/tools/M2_MetaConcepts_Ref.jsonld`.

3. **Governed scope = canonical layer files + M1 extensions only.** Dropped
   `ontology/Ref`, `ontology/sparql`, `ontology/tools`, `ontology/docs`,
   `ontology/TSCG_InstanceGrammar` (template) — reference/tooling sidecars, not the
   governed layer stack. Same in-scope filter as the deprecated-ORIVE→REVOI cleanup
   scoping, so "in-scope"
   means one thing repo-wide.

4. **CTX-5 split by value shape**: a colon-named term mapped to an **IRI string** is
   a defect (`CTX-5`, WARNING); mapped to a **coercion object** (`{"@type":"@id"}`)
   is the standard JSON-LD idiom (`CTX-5i`, INFO, **not** counted as a defect). The
   3 CTX-5i are exactly the `rdfs:subClassOf/domain/range` coercions that made
   M1_CoreConcepts SHACL-conformant (golden note, SC-1.5). Confirm this stays benign.

## 4. Rulings (status)

- **R1** — RATIFIED (2026-08-08, Michel): the CTX-1 prose/IRI-position rule (§3.1)
  stands. A prefix counts as *used* only in a KEY or `@id`/`@type` value, never in
  prose. This is the difference between a 5-false-positive report and a 0-ERROR one.
- **R2** — RATIFIED (2026-08-08, Michel): CTX-5i (coercion idiom `{"@type":"@id"}`)
  is **benign, not a defect** (§3.4); the 3 `rdfs:subClassOf/domain/range` stay INFO.
- **CANON** — RATIFIED (2026-08-08, Michel) and verified against HEAD: the four layer
  roots are `m3→M3_GenesisGrammar`, `m2→M2_GenericConcepts`, `m1→M1_CoreConcepts`,
  `m0→M0_Common` (all `.jsonld#`, absolute). The governed corpus declares exactly one
  target per prefix (m3×24, m2×18, m1×18, m0×2), zero divergence. `m0` was ADDED to
  the CTX-CANON table this lot; it arms the check to flag the `M0_Poclet#` backlog
  (~293 phantom @id) once the M0 layer is scanned.
- **R3** — OPEN: schedule the **CTX-5 = 28** fix as its own worksite (rename/
  restructure `m3:eagle_eye` / `m3:sphinx_eye`). A *fix* lot, distinct from this
  *engine* lot; the engine now gives it an exact gauge (28 → 0 when it ships).
- **R4** — RESOLVED (2026-08-08, Michel): **no M0 modelling.** The validator stays a
  pure CLI sibling of `check-M1/` under `ontology/cli-tools/`, with NO
  `M0_TscgOntologyValidator.jsonld`. Rationale: its real peers — the validation
  scripts `check_M1.py`, `run_all_layers.py`, `tscg_metrics.py` — carry no M0 either;
  only projected *product* tools (`TscgPocletMiner`, `TscgOntologyExplorer`,
  `TscgOntologyAPIServer`) do. Spec §1.3 ("modelled inside TSCG") is **amended** for
  validation scripts: their governance is git (versioned, HEAD-authoritative, golden-
  gated, lot-reported), not a poclet. An M0 would be created only if a future TSCG
  tool needs to reference the validator as a queryable instance — not by principle.

## 5. Next lots (recommended order)

1. **FRB** family — retired formalism traces (⊗, ket, GenesisSpace, KnowledgeField),
   with the same live-vs-changelog discrimination proven here. This is where the
   deprecated-ORIVE (→REVOI) / tensor residue surfaces as a gauge.
2. **DUP** (D8 triad, 8 in M1_Geology), **NOT** (SC-2 gauge, 43 M2 formulas), **STR**
   (cross-file double-definitions), then unified `golden_values.json` across layers.

## 6. Commit note

Adds files only under `ontology/cli-tools/validator/`. Golden gate unaffected
(16 | 151 | 3 both sides). Stage scoped to the new dir; isolated commit.
