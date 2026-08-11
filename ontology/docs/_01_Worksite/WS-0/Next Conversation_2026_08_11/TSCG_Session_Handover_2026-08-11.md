# TSCG — Session Handover 2026-08-11

**Author**: Echopraxium with the collaboration of Claude AI
**HEAD at close**: `9cc3868`

---

## 1. Pushed this session (HEAD chain)

```
9cc3868  worksite_report.py: aggregate central + distributed WS-n; add WS-9 + WS-10
f353943  Rebrand step 1-bis: fix template + SHACL that re-injected M0_Poclet#
c80361f  Rebrand step 1/3: M0_Poclet# -> M0_Common.jsonld# + remove orphan m0:mean
485dcad  KitArchitect-01 report obfuscation
fb34b3b  Archive KitArchitect-01 regression cycle
83abd58  Fix PEPITE-013: xsd:float coercion off prose
0e496ea  Stop tracking pytest cache
dbde7df  APIServer: fix PEPITE-001 + scope filter (003/005/011)
```

## 2. Delivered but NOT yet applied/committed (in outputs/)

- **WS-5 distributed** — `WS-5_worksite.yaml` (place at `WS-5/worksite.yaml`) +
  `migrate_ws5_to_distributed.py` (removes WS-5 from central). Enriched with 7 validator
  improvement pistes (see §5).
- **WS-11** — `WS-11_worksite.yaml` (place at `WS-11/worksite.yaml`).
- **KitArchitect-01 retest guide** — `KitArchitect-01_retest_guide.md`, updated to HEAD
  `9cc3868` + a "Known / in progress" section. Replaces the committed copy under
  `ontology/docs/_00_test_reports/2026_07_26_regression_KitArchitect-01/`.

## 3. Corpus state

- **KitArchitect-01 (Aki): 5 pépites CLOSED** — 001 (bare IRI), 003/011 (scope filter),
  005 (inverseOf via scope), 013 (xsd:float off prose). API suite 72→77.
- **Rebrand M0_Poclet# -> M0_Common: CLOSED** (effect + cause). Gauge `git grep
  M0_Poclet#` in live corpus = 0. Template + SHACL fixed so it can't re-inject.
- **Corpus is functionally correct** for single-poclet use. Cross-poclet comparability
  is NOT yet there — that's WS-10.

## 4. Locked decisions

- **M0 namespace convention** (from SHACL, proven with pyld):
  - `m0:` ALWAYS = `M0_Common.jsonld#` (shared, joinable — enables inter-poclet pattern
    queries; the whole point of transdisciplinarity).
  - `m0.<instance>:` (DOT) = the poclet's local file. The colon form `m0:instance:` is a
    JSON-LD parser ERROR (proven), i.e. the CTX-5 defect.
  - Same by analogy: `m1:` shared, `m1.extension.<domain>:` local.
- **M0 subsidiarity rule** (answers Aki §9 Q4): a new M0 property is allowed only via 3
  gates — no duplication of M3-M1; else factor into a domain (M1 extension); else define
  locally but TYPED. Prevents PEPITE-013 recurrence.

## 5. Backlog (worksites)

- **WS-1 (VOC)** — BLOCKS GR-M2. Measured on HEAD: **1693 bare keys / 3476 pairs** in
  M2_GenericConcepts (398 distinct: role×124, basis×114, status×111, examples, formula,
  description, value…). A SHACL M2 grammar now would validate only the RDF half and pass
  green — misleading. First rentable step: a validator **BARE** family (gauge 1693->0)
  to make WS-1 pilotable, then decide per key: promote to RDF / assume non-RDF / merge
  (changeLog vs changelog).
- **WS-10 (M0 namespace harmonisation)** — the real next structural chantier. Validator
  gauge: **CTX-CANON(m0) = 25->0** (25 poclets still have m0=local), CTX-5 for colon-name.
  Prerequisite lot: elevate CTX-CANON INFO->ERROR (hard gate). Approach: ~5 poclets/lot.
- **WS-9 (archaeological poclets)** — FireTriangle, ColorSynthesis, ExposureTriangle,
  Transistor, and AP-5 the template M0_CONTEXT_TEMPLATE.json (dead GenesisSpace +
  eagle_eye colon-name + xsd:float). Re-model via instance pipeline, anti-overfitting.
- **WS-11 (Mn SHACL grammars)** — GR-M2 (blocked by WS-1), GR-M3-a (structural, moderate,
  skill-generable once adapted off dead GenesisSpace), GR-M3-b (monoid/axiom constraints;
  HEAVY + risky, defer until M3 stabilises: WS-3 Gs, WS-7 F-axiom).
- **WS-5 validator pistes** (now logged in WS-5): CANON-ERR, CTX5-split, TYP (013 guard),
  NSRESOLVE (anti-phantom), ADDR (double ontology/), GOLDEN (unified thresholds), FEED
  (validator populates worksite gauges -> LIVE dashboard — most ambitious).

## 6. Recommended next steps

1. Apply the 3 pending deliverables (§2): WS-5 distributed, WS-11, Aki guide.
2. Open WS-10 with the **CTX-CANON -> ERROR** validator lot (hard gate), then NS-1 in
   lots of ~5 poclets.
3. GR-M2 stays blocked until WS-1; consider the BARE validator family first.

## 7. Cosmetic / carried

- `worksite.yaml` central `meta.head` still `f0daa1a` -> bump to real HEAD.
- Double `ontology/ontology/` in graph IRIs (`_file_to_iri`) — addressing decision (Aki
  §9 Q1), not a bug.
- Aki §9 Q1-Q3 still to answer (Q4 done via subsidiarity rule).
- Deprecated-term (ORIVE->REVOI) cleanup lot still pending.
- Discipline reminder: files containing the ORIVE literal -> LOCAL script only (server
  write-path corrupts it).

## 8. Tools state

- Validator (`ontology/cli-tools/validator/`): CTX family + --source switch. Measures
  M0 now (CTX-CANON=25, CTX-5=42). Pending families: FRB/DUP/NOT/STR/TYP/BARE.
- `worksite_report.py`: aggregates central + distributed WS-n/worksite.yaml (11 worksites).
- APIServer: 77 tests, scope filter active.
