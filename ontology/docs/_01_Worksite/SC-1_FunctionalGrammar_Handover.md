# SC-1 — Functional Grammar Model · Execution Handover

**Version**: 1.0.0
**Date**: 2026-07-11
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Sub-worksite**: SC-1 (root — see `TSCG_Worksite_Map.md`)
**Status**: SPECIFIED — ready to execute in a fresh session
**Read first**: `TSCG_Worksite_Map.md` §1.1 (locked decisions), then this file.

---

## 0. Purpose

Grave the functional grammar model: `Fm2` and `Fm1m2` are **functions**, a combo's
formula **is** the function signature, `Fm1` does not exist, and
`KnowledgeFieldConceptCombo` is renamed `DomainConceptCombo`.

SC-1 is the **root** of the worksite tree: it redimensions SC-2, SC-4, SC-6 and
SC-8. Nothing downstream should be graved before it.

**Design is closed.** Everything in §1 was settled with Michel on 2026-07-11 and
must not be re-litigated. This handover only specifies *execution*.

---

## 1. The model (locked — do not re-derive)

```
Fm2   : GenericConcept⁺              → ConceptCombo        (⊆ GenericConcept)
Fm1m2 : Domain⁺ , GenericConcept⁺    → DomainConceptCombo  (⊆ GenericConcept)
```

1. **Functions, not functors.** Their essence is *combination with emergence*
   ("combinés, pas associés") — non-compositional, hence non-functorial. The word
   *functor* stays reserved for M0 evaluation `F_x : System → Score`.
2. **`Fm1` does NOT exist.** No reification of composite domains. Multi-domain
   conjunction is carried by **juxtaposed domain arguments**:
   `Fm1m2(Biology, Chemistry, NamedConcept)`. (Rejected as decorative complexity.)
3. **A combo's formula IS the function signature** — `Fm2(Process, Alignment)`.
   There is **no monoidal expansion of a combo**, and nothing to develop
   "bout-à-bout". This is why M1 needs no expanded form (Michel: "pas besoin de la
   forme expansée en M1, en tout cas pas jusqu'à nouvel ordre").
4. **Monoidal formulas (`× + |`) belong to ATOMS only** (e.g. `Process = D × F`).
5. **Arguments are juxtaposed by comma, never joined by a grammar operator.**
   `×` is reserved to the Gt monoid and must not be overloaded — not in
   signatures, not for domain conjunction.
6. **Free recursion**: any argument satisfying `IsA GenericConcept` is valid —
   atoms, `ConceptCombo`, `DomainConceptCombo` alike. No special cases.
7. **`⊗⇒` is Hilbert/tensor-era residue** (like `⊗`) — purge on sight.

---

## 2. Grounded scope (verified against `/mnt/project/`, 2026-07-11)

### 2.1 Existing M2 classes (the anchor)

```
m2:GenericConceptCombo         subClassOf m2:GenericConcept      ← keep (rename? see D1)
m2:KnowledgeFieldConceptCombo  subClassOf m2:GenericConceptCombo ← RENAME → m2:DomainConceptCombo
m2:Combo                       subClassOf m2:GenericConceptFamily ← family tag, distinct — do not touch
m2:hasComboComponent           ObjectProperty                     ← parent link, keep
```

Note the subclass chain is already correct (`…Combo ⊆ GenericConceptCombo ⊆
GenericConcept`), which satisfies the "free recursion" requirement (§1.6) with no
structural change.

### 2.2 `KnowledgeFieldConceptCombo` occurrence map (rename perimeter)

**25 files.** It is a *type of instances*, not merely a declared class — so the
rename touches data, schema and docs.

| File | Occurrences |
|---|---|
| M1_Electronics | 34 |
| M1_Chemistry | 30 |
| M1_Economics | 28 |
| M1_Mythology | 23 |
| M1_Photography | 22 |
| M1_BusinessModeling / M1_Education / M1_Geology | 20 each |
| M1_Optics | 18 |
| M1_Music | 16 |
| M1_SystemicModeling | 14 |
| M1_Physics | 12 |
| M1_CoreConcepts | 6 |
| M0_TrophicPyramid | 5 |
| M2_GenericConcepts | 3 |
| M1_Biology / M1_EnergyGenerators / M0_PlateTectonics | 2 each |
| M3_GrammarFoundation | 1 |
| **M1_Schema_shacl.ttl** | **12** (SHAPE 3 — `sh:targetClass`) |
| CLAUDE.md, M1_CoreConcepts_README, OntologyModeling_Guidelines, TSCG_Reference_Corpus, TSCG_Smart_Prompt | docs |

### 2.3 The defect this model exposes (real example, M1_Optics)

```json
"@type": ["owl:Class", "m2:KnowledgeFieldConceptCombo"],
"m1:structuralGrammarFormula": "Fm1m2(Optics, A × St × F × It | R + O)",
"m2:knowledgeField": {"@id": "m1:extension:optics:Optics"}
```

Two violations of §1: primitives sit in the argument slot (must be **named
concepts**), and a monoidal expression is used where a **signature** belongs.

**IMPORTANT — do NOT fix these here.** Rewriting them requires recovering the
right named M2 concepts = *semantic* work = **SC-6**. SC-1 only establishes the
rule and the validator that will flag them.

*(The `m2:knowledgeField` phantom property is SC-5's problem — Domain fusion.)*

---

## 3. Execution plan

Order is deliberate: **rule → validator → data** ("validation d'abord sinon c'est
une rustine").

### Step 1 — Foundation note (no file edits)
Write `Functional_Grammar_Model.md` (proposition): the two signatures, functions
vs functors and why, formula-as-signature, no `Fm1`, free recursion, the rename
rationale, and the `⊗⇒` purge. This is the citable rationale for the edits.

### Step 2 — M2 edits (`M2_GenericConcepts.jsonld`)
- Rename `m2:KnowledgeFieldConceptCombo` → **`m2:DomainConceptCombo`** (keep
  `owl:deprecated` alias for one cycle if Michel wants a soft migration — **D2**).
- State each combo class's **producing function** and its signature contract in
  `rdfs:comment` (Fm2 → ConceptCombo; Fm1m2 → DomainConceptCombo).
- Ensure no combo carries a monoidal formula (per §1.3).
- Changelog: 3 most recent entries.

### Step 3 — SHACL (the validator, before the data)
Add/extend shapes:
- **`ComboFormulaShape`** — a combo's formula must match a function signature
  `Fm2(...)` / `Fm1m2(...)`; **forbid** monoidal operators (`×`, `+`, `|`) inside
  the argument list; forbid bare primitives as arguments.
- **`AtomFormulaShape`** — only atoms carry monoidal formulas.
- Update `M1_Schema_shacl.ttl` SHAPE 3 `sh:targetClass` →
  `m2:DomainConceptCombo` (12 occurrences).
- **Expected outcome**: the M1 extensions of §2.3 will now FAIL validation. That
  is the point — the validator exposes the SC-6 backlog instead of hiding it.
  Record the count; do not fix.

### Step 4 — Mechanical rename across data (25 files)
`KnowledgeFieldConceptCombo` → `DomainConceptCombo`, in `@type` arrays and class
references. Deterministic, scriptable, on copies. Re-validate JSON parse for each.

> **⚠ Substring trap — read before scripting.** `KnowledgeFieldConceptCombo`
> *contains* `KnowledgeField`. Two distinct things must not be conflated:
> - `m2:KnowledgeFieldConceptCombo` (the **class**) → renamed **here, in SC-1**.
> - `m2:KnowledgeField` / `m2:knowledgeField` (the **phantom class + property**)
>   → deprecated in **SC-5** (Domain fusion). **Do not touch in SC-1.**
>
> Consequence: rename the **longest string first** (`KnowledgeFieldConceptCombo`),
> then verify that no `KnowledgeField*` was collaterally rewritten. A naive
> `sed s/KnowledgeField/Domain/` would corrupt both. Michel's standing reminder:
> the rename is easy to *forget*; the gate in §5 is what catches it.

### Step 5 — Docs
Update CLAUDE.md, OntologyModeling_Guidelines, TSCG_Reference_Corpus,
TSCG_Smart_Prompt, M1_CoreConcepts_README to the new name + the function model.
Purge `⊗⇒` from `Structural_Grammar_Foundation.md` and
`TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md` (they still define
`⊗⇒` as "function type (emergence)" — the very residue being replaced by the
`Fm2`/`Fm1m2` named forms).

---

## 4. Open decisions (for Michel, at session start)

- **D1** — Rename `m2:GenericConceptCombo` → `m2:ConceptCombo` for symmetry with
  `DomainConceptCombo` and the signature vocabulary? *Or* keep the existing name
  and treat "ConceptCombo" as prose shorthand? (Recommendation: rename for
  consistency; cost = ~50 more occurrences.)
- **D2** — Soft migration (`owl:deprecated` alias kept one cycle) or hard rename?
- **D3** — Does the `Combo` **family** (`m2:Combo`, a `GenericConceptFamily`) stay
  as-is? It is orthogonal to the combo *classes* and interacts with SC-4
  (families-as-contracts). Recommendation: do not touch in SC-1.

---

## 5. Validation gates

```
□  JSON parses for every edited file
□  pyshacl CONFORMS on M2 (M2 must not regress)
□  New shapes correctly FLAG the known-bad M1 signatures (positive control:
     M1_Biology `Fm1m2(Biology, S × I × F)` must fail)
□  No `⊗` or `⊗⇒` introduced anywhere
□  Changelogs: 3 entries (M3 files: up to 7 — rollback safety)
□  Zero remaining `KnowledgeFieldConceptCombo` outside deprecation aliases
□  Michel's formal gates (linter, Pellet reasoner, cli-tools) + semantic sign-off
```

---

## 6. Explicitly OUT of scope

- **SC-6** — rewriting the malformed M1 signatures into named arguments
  (semantic, per-extension). SC-1 only makes them *detectable*.
- **SC-5** — Domain fusion (`m2:Domain`, `appliesToDomains`, the phantom
  `m2:knowledgeField`). SC-1 renames the combo class only; it does not resolve the
  Domain/KnowledgeField duplicate.
- **SC-2** — monoid qualification of `S`/`I` in atom formulas.
- **The global `⊗` purge.** *Newly measured*: `⊗` persists in **39 files** (22 M0
  instances, 5 M3, 12 docs — e.g. M0_FourStrokeEngine 34×, M0_ExposureTriangle
  30×, M0_ComplexChemicalSynapse 26×). This far exceeds SC-1 and deserves its own
  sub-worksite (**propose SC-9**). SC-1 purges `⊗⇒` **only in the two foundation
  docs it must rewrite anyway**.

---

## 7. Anti-improvisation notes (session hygiene)

Errors made on 2026-07-11 that this handover pre-empts:

- `St`/`Ss`/`It`/`Im` are **four distinct primitives** (Structure-Gt, Symbol-Gs,
  Information-Gt, Interoperability-Gm) — already defined in
  `M3_BicephalousPerspective`. Do **not** treat them as spelling variants of
  `S`/`I`.
- Any count of "formulas to fix" must be **re-derived against §1** and presented
  as provisional until Michel confirms. Earlier counts (116, 149) were artefacts
  of a wrong reading of the rule.
- Do not invent framework rules and then encode them in a script whose output is
  presented as authoritative. Anchor on M3 files or ask Michel.

---

## 8. First actions in the SC-1 session

1. Read `TSCG_Worksite_Map.md` §1.1, then this file.
2. Settle **D1 / D2 / D3** with Michel.
3. Execute Step 1 (foundation note) → Michel's approval → Steps 2–5 on copies.
4. Run the §5 gates. Hand over to SC-2.
