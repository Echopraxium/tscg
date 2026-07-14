# SC-1 — Functional Grammar Model · Completion Report & Handover to SC-2

**Version**: 1.0.0
**Date**: 2026-07-12
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Status**: ✅ **SC-1 EXECUTED** — on copies, in `outputs`. Michel's formal gates
(linter, Pellet, cli-tools) + semantic sign-off remain before commit.
**Reference**: `StructuralGrammar/Functional_Grammar_Model.md` v2.0.0

---

## 1. The model, graved

```
Fm2   : GenericConcept²⁺            →  m2:GenericConceptCombo   (≥ 2 concepts)
Fm1m2 : Domain⁺ , GenericConcept⁺   →  m2:DomainConceptCombo    (≥ 1 domain AND ≥ 1 concept)
```

Arguments are **named concepts** from `M2_GenericConcepts` or `M1_CoreConcepts`,
**juxtaposed by comma**, never primitives, never joined by `×`/`+`/`|`.
`Fm1` does not exist. A combo's formula **is** the signature — **no monoidal
expansion**, because `Fm2`/`Fm1m2` are **functions, not functors** (emergence is
non-compositional). Consequence: **M1 extensions are leaves.**

---

## 2. Deliverables

| File | Change |
|---|---|
| `StructuralGrammar/Functional_Grammar_Model.md` | **NEW** v2.0.0 — the foundation note (11 decisions) |
| `M2_GenericConcepts.jsonld` | v16.14.0 → **v16.15.0** |
| `M2_GenericConcepts_README.md` | v16.14.0 → **v16.15.0** (new §"Atoms vs Combos") |
| `M1_Schema_shacl.ttl` | v1.0.0 → **v1.1.0** (SHAPE 3 retargeted; **SHAPES 9 & 10** added) |
| 19 data files | mechanical rename `KnowledgeFieldConceptCombo` → `DomainConceptCombo` |
| `Structural_Grammar_Foundation.md`, `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md` | `⊗⇒` purged + SUPERSEDED banner |
| `CLAUDE.md`, `OntologyModeling_Guidelines.md`, `TSCG_Reference_Corpus.md`, `TSCG_Smart_Prompt_v16_2_0.md`, `M1_CoreConcepts_README.md`, `TO_DO.txt` | rename + functional grammar rule |

**Placement**: the note → `ontology/StructuralGrammar/`. Worksite docs →
`ontology/docs/_01_Worksite/`.

---

## 3. What SC-1 actually removed: a family, not a notation

The residue was not stray symbols. It was **one thesis, instantiated four times**:

```
m2:morphism_emergence            "emergence is a category-theoretic MORPHISM (⇒)"
  ├─ ⊗⇒                          the operator, "function type (emergence)"
  ├─ × ⁿ⇒ = lattice_join(dims(parents) ∪ …)     the combo class definition
  ├─ "union of the parent type sets"            the hasComboComponent clause
  └─ m1:structuralGrammarFormulaExpanded        the same claim, stored as DATA
```

A morphism **composes**. An emergence **does not**. The whole family asserted
compositionality — i.e. the exact opposite of what a combo is. All four are now
retired, and the root (`m2:morphism_emergence`) is deprecated and superseded by
`m2:producingFunction`.

*Tell-tale sign, in hindsight*: half the `…FormulaExpanded` values were **empty
strings**. There was never anything to compute.

---

## 4. Validation gates (§5 of the handover)

```
✅  JSON parses — 55/55 files
✅  Turtle parses — M1_Schema_shacl.ttl v1.1.0, 253 triples
✅  M2 does not regress
✅  POSITIVE CONTROL — M1_Biology `Fm1m2(Biology, S × I × F)` is FLAGGED
✅  NEGATIVE CONTROL — `Fm2(Cascade, Duplication, Network)` is NOT flagged (0 false positives)
✅  No `⊗` / `⊗⇒` introduced (remaining ones = quotations of the refuted formalism → SC-9)
✅  Changelogs — 3 entries (M2 .jsonld + README)
✅  Zero `KnowledgeFieldConceptCombo` outside the rename record
✅  Anti-collision — all other `KnowledgeField*` forms INTACT (SC-5's perimeter preserved)
⏳  Michel's formal gates (linter, Pellet, cli-tools) + semantic sign-off
```

---

## 5. Measurement — the honest numbers

```
BASELINE (SHACL v1.0.0, repo data, BEFORE SC-1) :  479 violations   CONFORMS = False
AFTER   (SHACL v1.1.0, renamed data)            :  605 violations   CONFORMS = False
                                                   ─────
                                    exposed by SC-1 :  +126
```

**M1 was already non-conformant.** SC-1 fixed none of the 479 and broke none of
them. It **exposes 126**, which are exactly the three new shapes:

| Shape | Count | What it is |
|---|---|---|
| Monoidal operator inside a signature | **109** | `Fm1m2(Optics, A × St × F × It \| R + O)` → **the SC-6 backlog** |
| `structuralGrammarFormulaExpanded` (D8) | **12** | the compositional expansion, retired |
| Malformed signature / arity (D5) | **5** | incl. the domain-less `Fm1m2(Cascade, …)` |

**The SC-6 backlog is 126 entries.** Not 116, not 149 — **126**, derived from the
confirmed rule, measured, reproducible.

> **Honest negative #1**: the "primitive as argument" shape fired **0 times**. Not
> a bug: corpus primitives always sit *inside* a monoidal expression, so the
> operator shape catches them upstream. The primitive shape remains a backstop for
> the operator-less form `Fm1m2(Biology, S)`.

> **Honest negative #2**: the malformed `Fm1m2` formulas are **the normal regime of
> the M1 extension layer**, not a handful of exceptions. The `M1_Biology` bug was
> never an exception — it was the rule. **This resizes SC-6 substantially.**

---

## 6. Findings for downstream worksites (do not lose these)

### 6.1 → **SC-5** · The M1 SHACL is self-contradictory (~256 of the 479 baseline violations are a **validator bug**, not data defects)

`sh:targetClass` **follows subclasses**. Since `DomainConceptCombo ⊆
GenericConceptCombo`, every extension combo is validated **twice**:

| | demands | verdict on `Fm1m2(Optics, …)` |
|---|---|---|
| SHAPE 2 (`GenericConceptCombo`) | formula starts with `Fm2(` | ❌ |
| SHAPE 3 (`DomainConceptCombo`) | formula starts with `Fm1m2(` | ✅ |

**No extension combo can satisfy both.** 133 + 123 = 256 violations are pure noise.
This is the **third** occurrence of the same pattern (after SHAPE 7 ↔ SHAPE 8), and
it explains why nobody was reading the 479: the validator cried wolf, so the real
signal was buried. **SHAPE 2 must exclude the subclass.** SC-5 already reworks
SHAPE 3 and SHAPE 7 — it is the right home.

### 6.2 → **SC-5** · A new `KnowledgeField*` form, missing from the inventory

`KnowledgeFieldMetaCombo` (1 occurrence) — not in the SC-5 change-request table.
Add it. (SC-1 did **not** touch it: the substring trap was avoided, longest string
renamed first, all other `KnowledgeField*` forms verified intact.)

### 6.3 → **SC-6** · Defect classes A–E (see the note §4.3)

- **A/B** primitives + unqualified `S`/`I` as arguments — 109
- **C** wrong function (`Fm1m2` with no domain) — includes `Fm1m2(Cascade, …)`
- **D** **scalar guards** — `| gain_per_stage > 1`, `| λ > 0`, `| range(F_A) << range(F_R)`,
  and `| V + R`. Michel, 2026-07-12: **a scalar in M1 is an M0 measurement that leaked
  a layer.** M1 describes structure, not values. Same class as the `k·` residues purged
  in SC-8. → **delete the guard, restore the pure signature.**
- **E** **qualitative guards** — `| trajectoryShape=Circular` (Oscillator),
  `| trajectoryShape=Chaotic` (ButterflyEffect, once `λ > 0` is stripped).
  ⚠️ **DO NOT DELETE.** Not scalars, not residue: real semantics (the *differentia
  specifica*). Pending **D11** (§6.4).

### 6.4 → **SC-3** · D11, the options/guard slot (deferred, deliberately)

Proposal on the table (Michel): an **options argument**, as functions commonly have —
`Fm2(Component, Process, Trajectory, trajectoryShape=Circular)`. Structurally clean:
it ends the `|` overload and turns the qualification into a *function application*.

**Deferred, on purpose.** Two reasons:

1. **The empirical base is thin**: after purging the scalars, **2 occurrences, 1 axis**
   (`trajectoryShape`). Below TSCG's own admission threshold — the same reasoning that
   killed `StateFacet` ("one-member = micro-overfitting").
2. **An "option" is a facet**: orthogonal axis + controlled value-set = the SC-3
   definition, verbatim. Graving an options mechanism now would build, **in parallel**,
   what SC-3 is about to formalise — a second `Domain`/`KnowledgeField` duplicate, and
   we know that bill.

Rule the question **in SC-3**, where "option or facet?" is asked in the right place with
the right vocabulary. *No inventing grammar under pressure* (handover §7).

### 6.5 → **SC-4 / SC-6** · D10, arguments are text, not IRIs

`m2:hasComboComponent` is **absent from all of M1**. A formula's arguments exist only
as a **substring**. Consequence: **D6 (argument provenance) is not SHACL-checkable** —
SC-1 validates the *syntax* of a signature, never that `Refraction` actually exists in
M2. Making it checkable requires M1 combos to carry `m2:hasComboComponent` (parents as
`@id`), the formula becoming the human-readable projection. **Model decision, not a
patch.**

### 6.6 → **SC-9** · The two foundation docs contradict themselves

`Structural_Grammar_Foundation.md` and its README: the **header** says Phase 2 (2026-05-18)
*replaced* `⊗` with `× + |`; the **body** still says the `⊗` symbol is *kept and
recontextualised*. The header was patched, the body never was.

⚠️ **A blind `⊗` purge would be wrong.** In these two docs `⊗` plays **two roles**:
- **(a)** *citation of the refuted Hilbert/tensor formalism* (`ℋ_ASFID ⊗ ℋ_REVOI = ℂ²⁵`)
  — **must stay**: it is the exhibit. Erasing it would erase the refutation.
- **(b)** *the current TSCG operator* — **stale**, retired 2026-07-06.

SC-1 purged `⊗⇒` only (its mandate) and added a **SUPERSEDED banner** to both. The 92
remaining `⊗` are role (a) + role (b) mixed: **SC-9 must sort them one by one, not by
`sed`.**

---

## 7. Handover to SC-2 (monoid-qualification rule, atoms only)

SC-1 **redimensions SC-2 favourably**:

- Only **atoms** carry monoidal formulas → SC-2's perimeter is the **atom set only**,
  and it is small. Combos are out of scope by construction.
- SC-2's `FormulaShape` (forbidding bare `S`/`I`) must **not** target
  `m2:GenericConceptCombo` — SHAPE 9 already forbids *any* monoidal operator there.
  Composing them would double-flag.
- The **B defect class** (`Fm1m2(Music, S × I × F)`) is a *joint* A+SC-2 defect: SC-6
  will repair it, but only after SC-2 has settled `St`/`Ss`/`It`/`Im`.
- SC-2's open question stands: does `M3_EagleEye`'s `typeSymbol` move `S→St` / `I→It`,
  or stay bare with qualification enforced only in formulas?

**Recommended order unchanged**: SC-2 → SC-8 → SC-9 → SC-3 (rule D11) → SC-4 → SC-5
(repair SHAPE 2!) → SC-7 → SC-6 (the 126). SC-0 at Michel's convenience.

---

## 8. Conventions applied

`dcterms:creator` = "Echopraxium with the collaboration of Claude AI" · files in
English, conversation in French · `@base` =
`https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/` · changelogs 3
entries (M3: up to 7) · surgical `str_replace` edits · everything on copies in
`outputs`; `/mnt/project/` untouched.
