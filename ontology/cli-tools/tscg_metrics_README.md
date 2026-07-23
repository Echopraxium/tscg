# TSCG Metric Board — `tscg_metrics.py`

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 1.0.0
**Date**: 2026-07-23
**Location**: `ontology/cli-tools/tscg_metrics.py`
**Project**: TSCG (Transdisciplinary System Construction Game)

---

## 0. Why this exists

Three manual censuses of the same defect produced **three different numbers**
(1661, 6444, 4263 bare keys) because each applied a different notion of "canonical
file". That is the real problem this tool solves: not the counting itself, but the
fact that **hand-counting is not reproducible**, so no worksite could ever prove it
had made progress.

A gauge is only useful if the same corpus always yields the same number. This
script fixes the file-selection rule (§2), fixes the detection patterns, and emits
a stable board. **Every count produced by hand before 2026-07-23 is superseded.**

Second purpose: turn worksites into **progress counters**. `NOT-1 = 43` is not a
report, it is the SC-2 perimeter; it must read `0` when SC-2 ships. Same for
`DUP-1` (Geology cleanup), `SC-1` (SC-6), `VOC` (vocabulary consolidation).

---

## 1. Scope — what it is, and what it is NOT

**IS**: a read-only measuring instrument. It counts. It never edits, never
proposes a diff, never emits a conformance verdict.

**IS NOT**:
- not a validator — no golden gate, no exit-code contract, no SHACL verdict;
- not a fixer — strict read-only;
- not a semantic judge. It answers *"how many?"*, never *"is it right?"*.
  "Is `State = It × D | T` correct?" stays with Michel. "How many atom formulas
  still carry a bare `S`/`I`?" is the gauge's business.

It is the **metric front-end** that `M0_TscgOntologyValidator` will absorb
(families CTX / FRB / DUP / NOT / STR, plus **VOC** added 2026-07-22).

**Authority**: run it against a checkout of `git HEAD`. A count taken from a
working copy is provisional by construction.

---

## 2. Canonical file selection (the reproducibility rule)

A file is counted iff it ends in `.jsonld` **and** its path contains none of:

```
/_archives/   /docs/   /tools/   _protos   /static/
migration_backups   domain_format_fix   POCLET_TEMPLATE   _Ref   /Ref/
```

Rationale: these hold copies, historical snapshots, private prototypes and
per-instance duplicates. Counting them inflates every gauge and makes runs
incomparable. Current result: **26 canonical files**.

> The `_archives/` anti-pattern (a live file tracked twice, destined to drift) was
> already retired from Git tracking on 2026-07-18. The exclusion list encodes the
> same lesson for measurement.

---

## 3. The gauges

### VOC — vocabulary hygiene (added 2026-07-22)

| Gauge | Meaning | Target |
|---|---|---|
| `VOC_bare_keys_occurrences` | JSON keys declared in **no** `@context` | 0 |
| `VOC_bare_keys_distinct` | distinct such names | 0 |
| `VOC_bare_standard_replaceable` | subset with a standard equivalent (family A) | — |
| `VOC_bare_false_friends` | subset that only *looks* standard (§4) | — |
| `VOC_prefixed_but_undefined` | `mN:` keys that resolve but are declared nowhere (family B1) | 0 |

**Why it matters**: a bare key is not a badly-named property — it is JSON that
never crosses into RDF. In files without `@vocab` it is **dropped on expansion**
(the data is *absent*, not mistyped); in files with `@vocab` it is worse, mapping
onto a namespace it does not belong to (two M3 files mint bogus `owl:role`,
`owl:status`). Either way it is invisible to any reasoner or SHACL shape. This is
δ₁ applied to the files: the gap between what the file *displays* and what the
graph *contains*.

### CTX — `@context` / IRI resolution

| Gauge | Meaning | Target |
|---|---|---|
| `CTX1_undeclared_prefix` | prefix used, absent from `@context` | 0 |
| `CTX4_relative_mN_prefix_files` | `mN` prefix is relative, not absolute | 0 |
| `CTX5_term_name_with_colon` | JSON-LD term whose *name* contains `:` | 0 |

**CTX-4 is not cosmetic** (established 2026-07-22): a relative prefix resolves
against `@base` in **identifier** position but **not** in **predicate** position.
So `m3:MonoidalType` (a class) expanded correctly while every `m3:*` *property* in
the same file expanded to an unresolved IRI. Measured impact on repair:
`M3_GenesisGrammar` went from **52 unresolved predicates to 0**. The 2026-07-18
verification compared an identifier and concluded "aligned" — an alignment that did
not hold for properties.

### FRB — retired formalism

| Gauge | Meaning | Target |
|---|---|---|
| `FRB1_tensor_operator` | `⊗` in live nodes (retired 2026-07-06) | 0 |
| `FRB2_legacy_arrow` | `⊗⇒` / `(x)=>` | 0 |

Lines belonging to a changelog are skipped: a mention inside `"changes"` is
**history, not a defect**.

### DUP — retired duplicates

| Gauge | Meaning | Target |
|---|---|---|
| `DUP1_D8_triad` | `structuralGrammarFormula{Expanded,TeX,RawText}` | 0 |

Matched **with or without** an `mN:` prefix. A prefix-blind pattern reported `0`
while 8 occurrences sat in `M1_Geology` — a false negative caught on 2026-07-22 by
cross-checking the gauge against the backlog. Any new detector must be validated
the same way: **a gauge reading 0 is a claim, and claims get tested.**

### NOT — notation

| Gauge | Meaning | Target |
|---|---|---|
| `NOT1_bare_SI_in_atom_formula` | bare `S`/`I` in `m2:hasStructuralGrammarFormula` | 0 |

**Scope is atoms only.** Combo signatures (`m1:structuralGrammarFormula`) are
excluded: subscripts qualify monoidal primitives, and a function argument is a
named concept, not a primitive. This gauge **is** the SC-2 perimeter.

### STR — structural / cross-file

| Gauge | Meaning | Target |
|---|---|---|
| `STR_layer_inversion` | `m<j>:` key inside an `M<k>` file with `j < k` | 0 |
| `STR_changelog_forms` | census of competing changelog spellings | 1 form |

Layer inversion = the foundational layer referencing a derived one (e.g. an M3
file using `m2:changelog`). Only **keys** count; a `m2:Stase` appearing as a *string
value* is a documentary citation, not a triple, and is not flagged.

### SC-1 — combo signature conformance (optional, `--shacl`)

| Gauge | Meaning | Target |
|---|---|---|
| `SC1_combo_violations` | violations of the three SC-1 rules | 0 |

The three rules, as graved in `M1_Schema_shacl.ttl` SHAPE 9 `ComboFormulaShape`:

1. **no monoidal operator** (`× + | ⊗`) inside a signature — arguments are
   juxtaposed by comma, never joined by a grammar operator;
2. **no bare primitive as an argument** — arguments are NAMED CONCEPTS;
3. **arity** — `Fm2` ≥ 2 GenericConcepts; `Fm1m2` ≥ 1 Domain AND ≥ 1 GenericConcept.

> **Requires `M1_Schema_shacl.ttl` ≥ 1.4.0.** Until 1.4.0 SHAPE 9 carried a single
> `sh:targetClass m2:GenericConceptCombo` with an "inherited by DomainConceptCombo"
> comment. That inheritance assumption was **false in practice**: every M1 extension
> combo is typed `m2:DomainConceptCombo`, so the shape fired on `M1_CoreConcepts`
> **only** — the three rules were enforced on **no extension at all**. Verified
> empirically on `M1_Geology`: 17 violations reported, **zero** from SHAPE 9,
> against formulas that plainly violate rule 1. Fixed by a dual `sh:targetClass`.

---

## 4. False friends — do not map these

Standard reuse is the anti-overfitting discipline applied to vocabulary, but
reuse is decided **by semantics and typing, never by name**:

| Bare key | Tempting standard | Why it is rejected |
|---|---|---|
| `status` | `adms:status` | `adms:status` is an `owl:ObjectProperty`, range `skos:Concept`, for **workflow** state (accepted/deprecated). TSCG `status` is an **epistemic** string ("PROPOSITION"/"VALIDATED"). |
| `role` | `prov:hadRole` | PROV-O means the role of an **agent in an activity**. TSCG `role` is the role of a **primitive in a formula**. |

Both are therefore **authentically TSCG-native** — established by verification,
not assumed by default. The gauge counts them separately so the distinction stays
visible.

---

## 5. Usage

```bash
# from the repo root, on a checkout of git HEAD
python ontology/cli-tools/tscg_metrics.py

# explicit root
python ontology/cli-tools/tscg_metrics.py --root ontology

# add the SC-1 gauge (needs rdflib + pyshacl)
python ontology/cli-tools/tscg_metrics.py --shacl

# machine-readable
python ontology/cli-tools/tscg_metrics.py --json

# snapshot / compare (delta column appears)
python ontology/cli-tools/tscg_metrics.py --save baseline.json
python ontology/cli-tools/tscg_metrics.py --baseline baseline.json
```

Dependencies: **none** for the core gauges (standard library only).
`rdflib` + `pyshacl` only for `--shacl`.

---

## 6. Baseline — HEAD `5dcd8e9`, 2026-07-23

26 canonical files.

| Family | Gauge | Value | Target | Owning worksite |
|---|---|---:|---:|---|
| VOC | bare keys (occurrences) | 4263 | 0 | vocabulary consolidation |
| VOC | bare keys (distinct) | 1301 | 0 | " |
| VOC | of which standard-replaceable | 681 | — | family A |
| VOC | of which false friends | 303 | — | (native, keep) |
| VOC | prefixed but undefined | 873 | 0 | family B1 |
| CTX | undeclared prefix | 1 | 0 | CTX |
| CTX | relative `mN` prefix | 24 | 0 | CTX-4 |
| CTX | term name with `:` | 31 | 0 | CTX-5 |
| FRB | tensor operator (live) | 89 | 0 | SC-9 |
| FRB | legacy arrow | 5 | 0 | SC-9 |
| DUP | retired D8 triad | 8 | 0 | SC-6 slice (Geology) |
| NOT | bare S/I in atom formula | 43 | 0 | **SC-2** |
| STR | layer inversion | 5 | 0 | changelog migration |
| SC-1 | combo signature violations | 114 | 0 | **SC-6** |

Bare keys by layer: **M2 1781, M1 1572, M3 738, M0 172**.
Changelog forms: `m2:changelog` 22, `m1:changelog` 3, bare `metadata.changelog` 4.
SC-1 worst files: Chemistry 15, Economics 14, Mythology 11, Photography 11,
CoreConcepts 10, Education 10. **`M1_Physics` and `M1_Electronics` are already
clean** — useful conformance references.

---

## 7. Known limits (honest)

- `VOC_prefixed_but_undefined` is **per-file and deliberately conservative**: a
  property defined in another file counts as undefined here. Cross-file resolution
  belongs to the validator. Read it as an upper bound.
- The SC-1 gauge counts **violation messages**, not distinct offending nodes; one
  formula breaking two rules counts twice. Direct file counting gives **155
  formulas** carrying a monoidal operator against **114** messages — the two
  numbers measure different things and both are correct.
- `STR_layer_inversion` catches keys only, by design (§3).
- No `--source local|head|github` switch yet: that is the validator's contract
  (see `M0_TscgOntologyValidator_README.md` §3). Until then, **check out HEAD
  yourself before measuring**.

---

## 8. Discipline

- A gauge moving is a **claim**; cross-check it against an independent count
  before believing it. Two detector bugs were found exactly this way.
- Gauges do not authorise edits. Lowering a gauge by deleting data is trivially
  possible and always wrong: the guard-before-delete invariant (never remove a
  field unless the surviving canonical is present and well-formed) still applies.
- Deliberate movements — a fix that raises or lowers a count — belong in
  **isolated commits** with the reason recorded, exactly as for `golden_values`.
  Making previously invisible triples visible produces an **unpredictable** delta:
  violations may both disappear and appear.
