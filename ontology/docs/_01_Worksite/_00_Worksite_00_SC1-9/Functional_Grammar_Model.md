# The Functional Grammar Model (`Fm2` / `Fm1m2`)

**Version**: 2.1.0
**Date**: 2026-07-13
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Sub-worksite**: SC-1 (root — see `_00_TSCG_Worksite_Map.md` §1.1)
**Change type**: Foundational — names an existing mechanism and closes an ambiguity
**Status**: GRAVED (SC-1 executed 2026-07-12/13 — M2 **v16.17.0**, M3_GrammarFoundation v2.4.0, M1_CoreConcepts v2.7.0, SHACL v1.1.0, 26 files renamed; acceptance gate PASS at 163)

---

## 1. Summary

TSCG has two ways of writing a concept's structure, and until now they were
conflated under one property (`m1:structuralGrammarFormula`):

- **Atoms** are *constructed* out of primitive types by the three monoidal
  grammars: `Process = D × F`. This is a **monoidal formula**.
- **Combos** are *produced* by combining named concepts with emergence:
  `Fm2(Process, Alignment)`. This is a **function signature**, not a formula.

This note fixes the second reading, names the two producing functions, states why
they are **functions and not functors**, removes the never-existing `Fm1`, and
renames `KnowledgeFieldConceptCombo` to `DomainConceptCombo` — with the semantic
consequence that this rename actually carries (§6).

It edits nothing. It is the citable rationale for the SC-1 edits that follow.

---

## 2. The two signatures

```
Fm2   : GenericConcept²⁺             →  GenericConceptCombo   (⊆ GenericConcept)
Fm1m2 : Domain⁺ , GenericConcept⁺    →  DomainConceptCombo    (⊆ GenericConceptCombo)
```

- `Fm2` combines named concepts into a new named concept.
- `Fm1m2` produces a **hybrid**: **at least one `Domain` and at least one
  `GenericConcept`**. This hybridisation *is* the emergence — hence a single
  concept argument suffices (`Fm1m2(Optics, Refraction)` is well-formed).
- Both are **closed under `GenericConcept`**: their output is itself a
  `GenericConcept`, which is what makes §5 (free recursion) work with no special
  case.

### 2.1 Cardinality (Decision D5)

| Function | Domain slot | Concept slot |
|---|---|---|
| `Fm2` | — (none; a domain argument makes it an `Fm1m2`) | **≥ 2** |
| `Fm1m2` | **≥ 1** | **≥ 1** |

The asymmetry is deliberate. `Fm2` emerges from the *combination of concepts*, so
it needs at least two ingredients — `Fm2(X)` would be an identity, not an
emergence. (This also preserves the `N ≥ 2` already asserted by the `m2:Combo`
family.) `Fm1m2` emerges from the *domain × concept* hybridisation, so `1 + 1` is
already an emergence.

Both slots of `Fm1m2` are **non-empty**: a domain-less `Fm1m2` is an `Fm2` that
mislabelled itself (§4.3, defect class C).

### 2.2 What may appear in the concept slot (Decision D6)

Every concept argument must be a **named concept declared in `M2_GenericConcepts.jsonld`
or in `M1_CoreConcepts.jsonld`**. Nothing else.

This excludes, and SHACL can check it:

- **primitive types** (`A`, `St`, `F`, `It`, `D`, `R`, `O`, …) — generative
  dimensions of the grammars, not concepts (§4.2);
- **concepts local to an M1 extension** — consequence: **M1 extensions are
  leaves**. There is no combo-of-a-combo *inside* `M1_Optics`. The pool of legal
  arguments is the transdisciplinary core (M2 + M1_Core), which is the Map/Territory
  discipline applied to the grammar itself.

### 2.3 Naming note (Decision D1)

`m2:GenericConceptCombo` **keeps its name**. Where the prose of this note and of
the Worksite Map writes *ConceptCombo*, it denotes exactly `m2:GenericConceptCombo`.

> **No class named `m2:ConceptCombo` exists or is to be created.** This sentence
> exists to stop a future session from inventing one from the shorthand.

`m2:DomainConceptCombo` is the only new class name, and it is a **rename**, not an
addition (§6).

---

## 3. Functions, not functors

A functor preserves composition: `F(g ∘ f) = F(g) ∘ F(f)`. It transports a
structure without creating anything that was not already there.

`Fm2` and `Fm1m2` do the opposite. Their essence is **combination with emergence**
— *combinés, pas associés*. The output concept carries semantics **irreducible to
any subset of its arguments**; there is no composition law over the arguments for
a functor to preserve. An emergence operation is therefore **non-compositional and
non-functorial**, by definition and not by accident.

Two consequences, both binding:

1. **The word *functor* stays reserved** for M0 dimension evaluation
   `F_x : System → Score`, where it is used correctly. Applying it to `Fm2` would
   destroy that distinction.
2. **Any compositional definition of a combo is residue and must go.** The current
   `rdfs:comment` of `m2:GenericConceptCombo` still reads:

   > `× ⁿ⇒(M₁,…,Mₙ) = lattice_join(dims(M₁) ∪ … ∪ dims(Mₙ))`, shared dimensions
   > contracted (`Fᵢ ⊔ Fⱼ = F`).

   That is a **compositional** definition — the output is fully computed from the
   union of the inputs' dimensions. It says, in symbols, that no emergence occurs.
   It is the Hilbert/tensor-era `⊗ⁿ⇒` transcribed with `×`, and it contradicts the
   very class it defines. **Purge on sight** (§8, Step 2).

---

## 4. A combo's formula *is* its signature

There is **no monoidal expansion of a combo**. Nothing to develop *bout-à-bout*.

| | Carries a monoidal formula (`× + |`) | Carries a function signature |
|---|---|---|
| **Atom** | ✅ `Process = D × F` | ❌ |
| **Combo** | ❌ | ✅ `Fm2(Process, Alignment)` |

Because the arguments are *combined*, not *associated*, expanding a combo into the
monoidal product of its parents' formulas would assert exactly the compositional
claim §3 rejects. This is why **M1 needs no expanded form** ("pas besoin de la
forme expansée en M1, en tout cas pas jusqu'à nouvel ordre").

### 4.1 Arguments are juxtaposed, never operated on

Function arguments are separated by a **comma**. Never by `×`, `+` or `|`.

`×` is reserved to the **Gt** monoid and is not overloaded — not in signatures,
not for domain conjunction, not anywhere else.

```
✅  Fm1m2(Biology, Chemistry, Catalysis)
❌  Fm1m2(Biology × Chemistry, Catalysis)     ← × overloaded as conjunction
❌  Fm1m2(Biology, S × I × F)                 ← primitives in the argument slot
```

### 4.2 Arguments are **named concepts**, never primitives

An argument must be an entity that `IsA GenericConcept`. A primitive type
(`A`, `S`, `F`, `D`, `I`, …) is **not** a `GenericConcept` — it is a generative
dimension of a grammar. Writing `Fm1m2(Biology, S × I × F)` therefore commits two
violations at once: a monoidal expression where a signature belongs, and
primitives where named concepts belong.

### 4.3 The three defect classes in the corpus (measured 2026-07-12)

The rule above is not academic. Scanning the real formulas:

| Class | Example | Diagnosis |
|---|---|---|
| **A** — primitives as arguments | `Fm1m2(Optics, A × St × F × It \| R + O)` | monoidal expression where a signature belongs |
| **B** — unqualified `S`/`I` | `Fm1m2(Music, S × I × F)` | class A **+** the SC-2 monoid-qualification defect |
| **C** — wrong function | `Fm1m2(Cascade, Duplication, Network)` (`M1_CoreConcepts`) | three valid M2 concepts, **zero domain** → this is an `Fm2` that mislabelled itself |
| **D** — scalar guard | `Fm1m2(Cascade, Amplification) \| gain_per_stage > 1` | a **scalar** appended to the signature. Scalars are M0 measurements; **M1 describes structure, not values**. Same residue class as the `k·` coefficients purged in SC-8. Also overloads `\|`, which is reserved to the Gs monoid. |
| **E** — qualitative guard | `Fm2(Component, Process, Trajectory) \| trajectoryShape=Circular` | **not** a scalar and **not** residue — a controlled enumerated value, i.e. real semantics (the *differentia specifica*). But it still overloads `\|`. **2 occurrences, 1 axis** → below TSCG's own admission threshold. **Do not delete; do not grave a mechanism either** — see D11. |

Class A/B is **not a handful of entries: it is the normal regime of the M1
extension layer** (`M1_Optics`, `M1_Music`, `M1_Economics`, … — every `Fm1m2`
scanned so far). The `M1_Biology` bug was never an exception; it was the rule.
This is an honest negative result and it **resizes SC-6 substantially**.

**Measured on the real repository (2026-07-13): 163 errors, 16 files.**

| Code | Count | |
|---|---|---|
| `DCC006` | **127** | monoidal operator inside a signature — the bulk |
| `DCC010` | **18** | `Fm1m2`'s first argument is not a registered `Domain` |
| `EXP001` | **12** | retired `structuralGrammarFormulaExpanded` (D8) |
| `GCC009`/`DCC009` | **5** | guards |
| `DCC008` | **1** | `Fm1m2(Electronics, S × (Ft × D × It) × F)` — nested parens **and `Ft`, which is not a TSCG primitive at all** |

⚠️ An earlier figure of **126** was measured on a *partial sandbox reconstruction* and was
**wrong** (it lacked `BusinessModeling`, `Music`, `MapTerritory_Optics`). **Only the repository
counts.** The same class of error — trusting a stale copy that *looked* authoritative — later
caused `M2` to be overwritten by two versions. See §12.

### 4.4 Four phantom domains (`DCC010`, found 2026-07-13)

`DCC010` compares an `Fm1m2`'s first argument against the `M1_Domains.jsonld` registry — the
only check that can see this class of defect, since a formula's arguments live **only as text**
(D10). It found that **four "domains" used in formulas are registered nowhere**:

| In the formula | The registry actually says |
|---|---|
| `Fm1m2(Music, …)` | **MusicTheory** |
| `Fm1m2(SystemicModeling, …)` | **SystemsTheory** |
| `Fm1m2(EnergyGenerators, …)` | *absent* |
| `Fm1m2(Cascade, …)` | not a domain at all — this is an `Fm2` |

This is the `Domain`/`KnowledgeField` duplicate (SC-5) surfacing in the data. Neither regex nor
SHACL could catch it: both see a well-formed string.

Class C was not listed in the SC-1 handover — it surfaced from the corpus, not
from the model.

**SC-1 repairs none of them.** Repair means recovering the correct named M2
concepts = *semantic* work = **SC-6** (Michel, 2026-07-12: class C goes to SC-6
with the rest of the backlog, despite being mechanically trivial — one backlog,
one gate). SC-1 states the rule and builds the validator that **flags** them, and
**records the exact count**. Making the backlog visible is the deliverable; hiding
it would be the bug.

---

## 5. Free recursion

Any argument satisfying `IsA GenericConcept` is valid. **No special cases.**

Since the subclass chain

```
m2:DomainConceptCombo ⊆ m2:GenericConceptCombo ⊆ m2:GenericConcept
```

already holds in the corpus, atoms, combos and domain-combos are **all** legal
arguments to `Fm2` and `Fm1m2` with **no structural change required**. Recursion
is a consequence of the existing hierarchy, not a mechanism to be added.

---

## 6. `Fm1` does not exist — and what the rename really changes

### 6.1 No `Fm1`

There is **no reification of composite domains**. "Biochemistry" is not an entity
to be constructed by some `Fm1(Biology, Chemistry)`. Multi-domain conjunction is
carried by **juxtaposed domain arguments** in the `Fm1m2` domain slot:

```
Fm1m2(Biology, Chemistry, Catalysis)
```

Reifying `Fm1` was examined and **rejected as decorative complexity**: it would
create a class of entities whose only content is the tuple already present in the
signature.

### 6.2 The rename is a re-definition (⚠ read before graving)

`m2:KnowledgeFieldConceptCombo` → **`m2:DomainConceptCombo`** (hard rename,
Decision D2 — no `owl:deprecated` alias).

The name change is trivial. **The membership criterion changes, and that is not
trivial.** Current definition:

> *"restricted to combinations that span knowledge field boundaries — i.e. whose
> parent GenericConcepts originate from **distinct epistemological domains**
> (e.g. physical + semiotic). Transdisciplinary by construction."*

That criterion is about the **heterogeneity of the parents**. The functional model
says something different and simpler:

> **`DomainConceptCombo` = the codomain of `Fm1m2`**, i.e. a combo carrying one or
> more `Domain` arguments — a combo **qualified by domain**. Whether its parent
> concepts come from one field or several is *not* the criterion.

Both readings happen to cover most existing instances (a combo declared inside
`M1_Optics` is domain-qualified *and* usually mixes registers), which is why the
drift is easy to miss. But they are not the same predicate, and the corpus has
**304 occurrences** typed under the old one. Graving the rename without stating
the new criterion would silently re-interpret every one of them.

**Resolution (Michel, 2026-07-12 — Decision D4)**: the codomain-of-`Fm1m2`
criterion is adopted. Canonical wording:

> **`DomainConceptCombo` is defined by an `Fm1m2` formula — i.e. a hybrid of at
> least one `Domain` and at least one `GenericConcept`.**

Heterogeneity of the parents is **no longer** the membership condition; **domain
qualification** is. The re-definition is recorded explicitly in the class comment
and in the changelog, so that the 304 re-typed occurrences are not silently
re-interpreted.

---

## 7. The `⊗` / `⊗⇒` residue

`⊗` was retired on 2026-07-06. Its **function-arrow companion `⊗⇒`** — glossed in
the foundation docs as *"function type (emergence)"* — is the same residue class,
and it is precisely what `Fm2` / `Fm1m2` **replace**: there is no operator symbol
between the arguments of a function; there is a **name** in front of them.

SC-1 purges `⊗⇒` (and its `× ⁿ⇒` transcription) **only where it must rewrite
anyway**:

- the `rdfs:comment` of `m2:GenericConceptCombo` (§3);
- `Structural_Grammar_Foundation.md` and
  `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`, which still
  *define* `⊗⇒`.

The rest — **39 files still carrying `⊗`** — is **SC-9**, and the `× ⁿ⇒` in the
`m2:Combo` **family** comment goes with it (Decision D3: the family is not touched
in SC-1; it belongs to SC-4/SC-9).

---

## 8. What SC-1 will grave (informative — full plan in the handover)

1. **M2** (`M2_GenericConcepts.jsonld`): hard rename to `m2:DomainConceptCombo`;
   state each combo class's **producing function** and signature contract in
   `rdfs:comment`; purge the compositional `× ⁿ⇒ = lattice_join(…)` definition;
   re-definition per §6.2. Changelog: 3 entries.
2. **SHACL first, data second** ("validation d'abord sinon c'est une rustine"):
   - `ComboFormulaShape` — a combo's formula must match `Fm2(…)` / `Fm1m2(…)`;
     **forbid** `×`, `+`, `|` inside the argument list; **forbid** primitives as
     arguments; enforce the D5 cardinalities (`Fm2` ≥ 2 concepts; `Fm1m2` ≥ 1
     domain **and** ≥ 1 concept); enforce D6 (arguments resolve to M2 or
     M1_CoreConcepts named concepts).
   - `AtomFormulaShape` — only atoms carry monoidal formulas.
   - `M1_Schema_shacl.ttl` SHAPE 3 `sh:targetClass` → `m2:DomainConceptCombo`.
   - **Expected**: the malformed M1 signatures now **FAIL**. Count them, record
     them, hand them to SC-6. Do not fix.
3. **Mechanical rename** across the 26 files / 304 occurrences.
   > ⚠ **Substring trap**: `KnowledgeFieldConceptCombo` *contains*
   > `KnowledgeField`. The **class** is renamed here (SC-1). The **phantom class
   > and property** `m2:KnowledgeField` / `m2:knowledgeField` are absorbed into
   > `Domain` in **SC-5** and must **not** be touched now. Rename the **longest
   > string first**, then verify no `KnowledgeField*` was collaterally rewritten.
   > `sed s/KnowledgeField/Domain/` would corrupt both at once.
4. **Docs**: CLAUDE.md, OntologyModeling_Guidelines, TSCG_Reference_Corpus,
   TSCG_Smart_Prompt, M1_CoreConcepts_README, TO_DO.txt, README.md.

---

## 9. Explicitly out of scope

- **SC-6** — rewriting malformed M1 signatures into named arguments (semantic).
- **SC-5** — Domain fusion; the `m2:knowledgeField` phantom property; the
  `Domain` / `KnowledgeField` duplicate. SC-1 renames the **combo class only**.
- **SC-2** — monoid qualification (`St`/`Ss`/`It`/`Im`) inside atom formulas.
- **SC-4** — the `m2:Combo` **family** (Decision D3: untouched).
- **SC-9** — the global `⊗` purge (39 files).
- **SC-3** — the options/guards slot (D11).
- **The M1 SHACL SHAPE 2 ↔ SHAPE 3 contradiction** (see the completion report): `sh:targetClass`
  follows subclasses, so every `DomainConceptCombo` is validated **twice**, by SHAPE 2 (which
  demands `Fm2(`) *and* SHAPE 3 (which demands `Fm1m2(`) — mutually exclusive. ~256 of the 479
  pre-existing violations are this SHACL bug, not data defects. Repair belongs to **SC-5**,
  which already reworks SHAPE 3 and SHAPE 7.

---

## 10. Decisions recorded (2026-07-12, Michel)

| | Decision | Outcome |
|---|---|---|
| **D1** | Rename `m2:GenericConceptCombo` → `m2:ConceptCombo`? | **No.** Name kept; "ConceptCombo" is prose shorthand only. |
| **D2** | Soft or hard rename of `KnowledgeFieldConceptCombo`? | **Hard rename**, no deprecation alias. |
| **D3** | Touch the `m2:Combo` family? | **No.** Deferred to SC-4 / SC-9. |
| **D4** | Membership criterion for `DomainConceptCombo`? | **Codomain of `Fm1m2`**: a combo whose formula is an `Fm1m2`, i.e. a **hybrid of ≥ 1 `Domain` and ≥ 1 `GenericConcept`**. Supersedes "parents from distinct epistemological domains". |
| **D5** | Cardinality? | **`Fm2` ≥ 2 concepts**; **`Fm1m2` ≥ 1 domain + ≥ 1 concept** (§2.1). |
| **D6** | Provenance of concept arguments? | **M2 or M1_CoreConcepts only.** M1 extensions are leaves (§2.2). |
| **D7** | Where to fix the mistyped `Fm1m2(Cascade, …)`? | **SC-6**, with the rest of the backlog. |
| **D8** | `m1:structuralGrammarFormulaExpanded`? | **Retired.** It stored `lattice_join(dims(parents))` — the compositional thesis as data. No monoidal expansion exists. 12 occurrences in `M1_CoreConcepts` (half already empty), removal = SC-6. |
| **D9** | `m2:morphism_emergence`? | **`owl:deprecated true` + `m2:supersededBy m2:producingFunction`.** It declared emergence to be a category-theoretic *morphism* — the ROOT from which `⊗⇒`, `lattice_join` and `…FormulaExpanded` all descend. A morphism composes; an emergence does not. |
| **D10** | `m2:hasComboComponent` absent from all of M1 — reify arguments as IRIs? | **Raised, deferred** (SC-4/SC-6). Consequence: D6 (argument provenance) is **not SHACL-checkable** — arguments exist only as text inside a string. SC-1 validates the *syntax*, not that `Refraction` really exists in M2. |
| **D11** | Guards (`\| trajectoryShape=Circular`) — options slot? | **Deferred to SC-3.** An "option" (orthogonal axis + controlled value-set) is the *definition of a facet*. Graving an options mechanism in SC-1 would create, in parallel, what SC-3 is about to formalise — the `Domain`/`KnowledgeField` duplicate all over again. **Do not invent grammar under pressure.** |

---

## 12. The `/mnt/project/` incident (2026-07-13) — read this before editing anything

SC-1 was first executed against `/mnt/project/` (the "project knowledge" snapshot), on the
assumption — stated in the 2026-07-03 handover — that *"the repo's M2 is the current one"*.

**It was not.** The snapshot held `M2` at **16.14.0** while the repository was at **16.16.0**:
**two versions behind**, silently. SC-1's M2 edits were therefore written on top of live work
(`m2:Constraint`, reformulated in 16.16.0) and would have **erased it**. The snapshot also
capitalised `M1_music.jsonld` → `M1_Music.jsonld`, which produced a *fictitious* "case bug" that
was reported as a finding and was not one.

It was caught by comparing `git diff --numstat` against the **expected** surgical diff per file:
`M1_CoreConcepts` came out at exactly 13/13 and `M3_GrammarFoundation` at 39/23, as predicted —
but `M2` came out **57 lines over**, and that discrepancy is what exposed it.

> ### The rule
>
> **`/mnt/project/` is not an authority. It is a partial, silently stale snapshot.**
> The only authority is **`git show HEAD:<file>`**. Check the version **before** editing,
> never after.

---

## 11. References

- `_00_TSCG_Worksite_Map.md` §1.1 — the locked model.
- `SC-1_FunctionalGrammar_Handover.md` — the execution plan.
- `M2_GenericConcepts.jsonld` — `m2:GenericConceptCombo`, `m2:KnowledgeFieldConceptCombo`,
  `m2:Combo`, `m2:hasComboComponent`.
- `M1_Schema_shacl.ttl` — SHAPE 3 (`m1:KnowledgeFieldConceptComboShape`).
- `Structural_Grammar_Foundation.md`, `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
  — the two docs still defining `⊗⇒`.
- `OntologicalOverfitting.md` — admission discipline (why `Fm1` was rejected).
- Base URI (all ontology IRIs): `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/` (via `@base`).
