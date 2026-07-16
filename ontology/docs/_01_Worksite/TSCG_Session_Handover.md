# TSCG Session Handover — SC-1 (Functional Grammar Model)

**Session**: 2026-07-12 → 2026-07-14
**Author**: Echopraxium with the collaboration of Claude AI
**Status**: ✅ **SC-1 + SC-1.5 COMPLETE, VALIDATED, COMMITTED, PUSHED**
**Signed off by Michel** (2026-07-14): *`Φ`/`Ψ` = morphisms · `Fm2`/`Fm1m2` = functions*
**Next**: read §1 (the rule), §2 (the model), then §7 (what to do next)

---

## 1. ⛔ THE RULE — read this before editing a single file

> ### The project knowledge snapshot is NOT an authority.
> ### The only authority is `git show HEAD:<file>` and `git ls-files`.

This is not a stylistic preference. On 2026-07-13 the snapshot held **M2 at 16.14.0** while
the repository was at **16.16.0** — **two versions behind, silently**. SC-1's M2 edits were
written on top of live work (`m2:Constraint`, reformulated in 16.16.0) and **would have
erased it**. The snapshot also capitalised `M1_music.jsonld` → `M1_Music.jsonld`, which
produced a *fictitious* "case bug" that was reported as a finding and was not one.

It was caught only by comparing `git diff --numstat` against the **expected** surgical diff,
file by file: `M1_CoreConcepts` came out at exactly 13/13 and `M3_GrammarFoundation` at
39/23 **as predicted** — but M2 came out **57 lines over**, and that discrepancy is what
exposed it.

**Before editing any file, ask Michel to run `git show HEAD:<file> | findstr versionInfo`,
or work in Claude Code, which reads the real repository.** Three other duplicates cost time
the same day: `system_modeling/` vs `systemic_modeling/` (a whole file went unvalidated),
`M1_Schema_shacl.ttl` in three copies, `M1_SystemicModeling.jsonld` in two versions six
weeks apart.

**A duplicate is not a spare file. It is an authority that lies — and it never lies loudly.**

---

## 2. The model, graved and signed

```
Fm2   : GenericConcept²⁺            →  m2:GenericConceptCombo   (≥ 2 concepts)
Fm1m2 : Domain⁺ , GenericConcept⁺   →  m2:DomainConceptCombo    (≥ 1 domain AND ≥ 1 concept)
```

- **A combo's formula IS the signature of the function that produces it.** No monoidal
  formula, **no monoidal expansion**. Monoidal formulas (`×` Gt, `+` Gm, `|` Gs) belong to
  **atoms only**.
- **`Fm2`/`Fm1m2` are FUNCTIONS, not morphisms and not functors.** A morphism/functor must
  *preserve composition*; emergence is **non-compositional** — the arguments are
  **combined, not associated**. *"Functor" stays reserved for M0 evaluation `F_x : System → Score`.*
- **`Φ`/`Ψ` remain genuine morphisms** — they preserve structure and they *do* compose.
  **The family is split, not purged.**
- **Arguments are NAMED CONCEPTS** from `M2_GenericConcepts` or `M1_CoreConcepts` —
  **never primitives**, **never a monoidal expression**, **comma-juxtaposed**.
  *Consequence: **M1 extensions are leaves**.*
- **`Fm1` does not exist.** Multi-domain conjunction = juxtaposed domain arguments.
- **`Fm1m2` is NOT "the function that crosses the M1/M2 boundary."** That was the **root
  error** (§4). What distinguishes it is **DOMAIN QUALIFICATION**, and the domain must be
  **registered in `M1_Domains.jsonld`**.

📖 `ontology/StructuralGrammar/Functional_Grammar_Model.md` (11 decisions, D1–D11)

---

## 3. State of the repository

| File | Version |
|---|---|
| `M3_GrammarFoundation.jsonld` + README | **2.4.0** |
| `M2_GenericConcepts.jsonld` + README | **16.17.0** |
| `M1_CoreConcepts.jsonld` + README | **2.8.0** |
| `M1_Schema_shacl.ttl` | **1.1.0** (lives in `check-M1/`, **one copy only**) |
| `OntologyModeling_Guidelines.md` | **1.5.0** (Guideline 12 rewritten) |
| 14 M1 extensions | renamed + changelog |
| `ontology/cli-tools/` | **NEW** — tooling + acceptance gate |

**All formal gates green**: SHACL ✅ · RDFS ✅ (0/0) · **Pellet OWL DL ✅ on M2, M3, and —
for the first time — M1_CoreConcepts** · acceptance gate ✅ PASS · **Michel's semantic
sign-off ✅**.

### The acceptance gate

```powershell
cd ontology\cli-tools
_run_all_layers.bat
```
```
M1 :  16 files · 163 errors · 3 warnings · 476 SHACL violations
```

**These numbers are the reference.** Not a target — a **thermometer of the debt**.
**163 is GREEN. 162 is RED. 164 is RED.** A count that **drops** is as suspicious as one
that rises: either a deliberate fix (then `--update-golden`, and the drop is recorded under
`_previous` / `_delta` **with its reason**) or **a validator that stopped biting**.

> **A silently shrinking error count is the most dangerous signal in this repo:
> it looks like progress.**

M3 and M2 are **NOT INSTRUMENTED** — and that is not "green". *An un-instrumented layer is
not a passing layer; it is an unmeasured one.*

---

## 4. What SC-1 actually removed: one thesis, four instances

The residue was never stray notation. It was **a single false claim**, propagated:

```
m2:morphism_emergence        "emergence is a category-theoretic MORPHISM (⇒)"
  ├─ ⊗⇒                                        the operator
  ├─ × ⁿ⇒ = lattice_join(dims(parents) ∪ …)    the combo class definition
  ├─ "union of the parent type sets"           the hasComboComponent clause
  └─ m1:structuralGrammarFormulaExpanded       the same claim, stored as DATA
```

A morphism **composes**. An emergence **does not**. All four are retired; the root is
`owl:deprecated`, superseded by `m2:producingFunction`.

*Tell-tale sign, in hindsight: half the `…FormulaExpanded` values were **empty strings**.
There was never anything to compute.*

### The root error, and its propagation

`M3_GrammarFoundation` defined `Fm1m2 : 𝕋₁(M1) × 𝕋₁(M2)ⁿ → 𝕋₁` — *"crosses the M1/M2
boundary"*. `OntologyModeling_Guidelines` v1.4.0 repeated it. `M1_CoreConcepts` v1.4.0 then
applied it **faithfully**, "correcting" `Propagation` and `CascadeAmplification` from `Fm2`
to `Fm1m2` *"because the parent `m1:Cascade` is M1, not an M2 atomic"* — producing
`Fm1m2(Cascade, Duplication, Network)`, an `Fm1m2` **with no domain at all**.

**The corpus was not wrong *despite* the foundation. It was wrong *because of it*.**

### `⊙` was `Fm1m2` before it had a name

`M0_TrophicPyramid_README` wrote `StratifiedDissipation = Biology ⊙ (Layer ⊗ Dissipation)`.
`⊙` was the **disciplinary qualification operator** — exactly `Fm1m2(Biology, Layer,
Dissipation)`. And *"Compiled tensor: S ⊗ I ⊗ A ⊗ R ⊗ F ⊗ D"* was `lattice_join` in prose.
**SC-1 invented nothing: it named what the corpus was already doing, and removed the part
that was false.**

⚠️ **And a warning for SC-9**: a mechanical `⊗ → ×` substitution would have preserved
**five substantive errors** in modern dress (`Homeostasis` claimed 5 dimensions where M2 has
4; `Transducer` was missing `S`; `Entropy` was missing `It` and both poles; `Gradient = ⊗₂F`
is not a formula in any notation). **The stale notation was hiding stale content. Confront
every formula against M2 — never `sed`.**

---

## 5. ⚠️ THE TWELVE SILENT FAILURES — the real result of this session

None of these **crashed**. None **reported failure**. They just… didn't do the work. This is
why M1 accrued debt *while the validators "existed"*.

| # | Failure | What it actually did |
|---|---|---|
| 1 | `m2:morphism_emergence` | a false thesis, never stated as one — the root of everything |
| 2 | `structuralGrammarFormulaExpanded` | half its values **empty strings**: nothing to compute |
| 3 | **SHAPE 2 ↔ SHAPE 3** | `sh:targetClass` follows subclasses → every extension combo validated **twice**, with **mutually exclusive** requirements. **~256 violations of pure noise.** |
| 4 | `fix_imports_genesis()` | **called by `run()`, never defined** → `AttributeError` → **none of the 7 documented auto-fixes had ever run** |
| 5 | `M1_Schema.shacl.ttl` (dot) vs `_shacl.ttl` (underscore) | `--shacl` **never found its grammar, validated nothing, exited 0** |
| 6 | `symbolic-system-grammar` (singular) | the directory is **plural** → the whole SymbolicSystemGrammar category (Iching, TriskeleToolchain) **skipped without a word** |
| 7 | `M1_BusinessModeling` | **absent from `M1_FILES`** → never validated, 20 combos unseen |
| 8 | Wrong path `system_modeling/` | file **not found** = only a *warning* → `M1_SystemicModeling` **never validated** |
| 9 | cp1252 in a pipe | a checker that **works in a terminal and DIES when called** — reports zero errors, which looks exactly like success |
| 10 | `M1_CoreConcepts` `rdfs:subClassOf` as **string literals** | **Pellet ignored all 19 subClassOf axioms**; the class hierarchy was **invisible**; the layer was not "inconsistent", it was **UNANALYSABLE** |
| 11 | `owl:imports` as a bare string | **the TSCG import graph is DECORATIVE.** `M1_CoreConcepts` has declared importing M2 forever — **and never has.** Every layer is reasoned **in isolation**. |
| 12 | `_previous` captured 3 counters of 4 | **the gate's own anti-silent-failure mechanism silently failed**: the 502→476 drop was recorded **nowhere** |

**#12 is the one to remember.** The mechanism whose entire purpose is to make a lowered
reference *reviewable* quietly failed to review it. **Found because Michel ran
`findstr /C:"_previous"` to check that it had worked.** It hadn't.

### Two errors of mine that Michel caught

- **M3 changelog truncated to 3 entries** — M3's window is **7** (rollback safety on the
  foundational layer). I automated without discriminating the layer.
- **M2 overwritten by two versions** (§1). The expensive one.

### And one claim of mine that was simply false

I asserted, repeatedly, that *"one `@context` line dissolves ~500 SHACL violations"* —
**taken from the 2026-07-03 handover without verifying it**. Measured truth: **26**. Only
`M1_CoreConcepts` had the defect; the 15 extensions already used `{"@id": …}`. The gain was
real but **existential, not quantitative**: Pellet can now reason on M1.

---

## 6. Findings for downstream worksites

### → **SC-5** · ~256 of the 476 SHACL violations are a **validator bug**, not data defects

`sh:targetClass` **follows subclasses**. Since `DomainConceptCombo ⊆ GenericConceptCombo`,
every extension combo is validated **twice**:

| | demands | verdict on `Fm1m2(Optics, …)` |
|---|---|---|
| SHAPE 2 (`GenericConceptCombo`) | formula starts with `Fm2(` | ❌ |
| SHAPE 3 (`DomainConceptCombo`) | formula starts with `Fm1m2(` | ✅ |

**No extension combo can satisfy both.** **SHAPE 2 must exclude the subclass.**

> **THIS IS THE REAL GOLDMINE — not the `@context` line I kept advertising.** ~256 violations
> that **describe no defect at all**. While they scream, the SHACL is unreadable, so it is
> not read. **That is the root cause of six months of invisible debt.**

Also for SC-5: **~77 violations** from the phantom `m2:knowledgeField`; the new
`KnowledgeFieldMetaCombo` form (1 occurrence, missing from the SC-5 inventory); and the
**four phantom domains** below.

### → **SC-6** · The 163, by code

| Code | Count | |
|---|---|---|
| `DCC006` | **127** | monoidal operator inside a signature — **the bulk** |
| `DCC010` | **18** | `Fm1m2`'s first argument is **not a registered Domain** |
| `EXP001` | **12** | retired `structuralGrammarFormulaExpanded` (D8) |
| `GCC009`/`DCC009` | **5** | guards |
| `DCC008` | **1** | `Fm1m2(Electronics, S × (Ft × D × It) × F)` — nested parens **and `Ft`, which is not a TSCG primitive at all** |

**Four phantom domains** (`DCC010`), invisible to regex and SHACL alike — only a lookup
against `M1_Domains.jsonld` can see them:

```
Fm1m2(Music, …)             →  the registry says  MusicTheory
Fm1m2(SystemicModeling, …)  →  the registry says  SystemsTheory
Fm1m2(EnergyGenerators, …)  →  absent from the registry
Fm1m2(Cascade, …)           →  not a domain at all → this is an Fm2
```

**Guards are not one thing.** *Scalar* guards (`| gain_per_stage > 1`, `| λ > 0`) are **M0
measurements that leaked a layer** — M1 describes structure, not values. **Delete them.**
*Qualitative* guards (`| trajectoryShape=Circular`) carry **real semantics** (the
*differentia specifica*). **DO NOT DELETE** — pending D11.

### → **SC-3** · D11: the options slot (deferred **on purpose**)

Michel proposed an **options argument**: `Fm2(Component, Process, Trajectory,
trajectoryShape=Circular)`. Structurally clean — it ends the `|` overload.

**Deferred, deliberately.** (1) After purging the scalars, **2 occurrences, 1 axis** — below
TSCG's own admission threshold (the reasoning that killed `StateFacet`). (2) **An "option"
IS a facet**: orthogonal axis + controlled value-set = the SC-3 definition, verbatim.
Graving it now would build, *in parallel*, what SC-3 is about to formalise — a second
`Domain`/`KnowledgeField` duplicate. **Do not invent grammar under pressure.**

### → **SC-4 / SC-6** · D10: arguments are text, not IRIs

`m2:hasComboComponent` is **absent from all of M1**. A formula's arguments exist only as a
**substring**. So D6 (argument provenance) is **not SHACL-checkable** — hence `DCC010`'s
registry lookup, which is the closest approximation without reifying the arguments.

### → New chantier · **the `owl:imports` graph is decorative**

`M1_CoreConcepts` declares `owl:imports` → M2 **as a bare string**, so it is ignored. Every
layer is reasoned **in isolation, never with its foundation**. Coercing it to an IRI makes
Owlready try to **resolve it over the network** (it fetches the raw.githubusercontent URL,
gets JSON-LD, tries to parse N-Triples, and dies). Making it live requires a **local
catalog**. Left inert on purpose.

### → Script debt

`check_M1.py` still needs: a `--layer` flag on `--update-golden` (it currently rewrites **all
layers at once** — it once froze `149` as the reference, enshrining a *missing file* as
progress). M0's golden counts were frozen **without the review the script itself asks for**.

---

---

## 6-bis. ⚠️ README DEBT — the docs are not in sync with the data

A stale README is not untidiness. **It is an authority that lies**, and this project has now
paid for that three times in one session:

- `TO_DO.txt` was **a week behind** and I edited the stale copy;
- `OntologyModeling_Guidelines` v1.4.0 still taught `Fm1m2 = "crosses the M1/M2 boundary"` —
  **the very error SC-1 spent two days extirpating**, sitting in the document a future session
  reads *before* it ever opens M3;
- `M0_TrophicPyramid_README` hid **five substantive formula errors** under retired notation
  (`Homeostasis` claimed 5 dimensions where M2 has 4; `Transducer` was missing `S`;
  `Entropy` was missing `It` and both poles; `Gradient = ⊗₂F` is not a formula in any notation).
  A mechanical `⊗ → ×` substitution would have **preserved every one of them, in modern dress**.

### Known state, 2026-07-14

| | Status |
|---|---|
| `M2_GenericConcepts_README` · `M3_GrammarFoundation_README` · `M1_CoreConcepts_README` | ✅ synced (16.17.0 / 2.4.0 / 2.8.0) |
| `OntologyModeling_Guidelines` | ✅ **1.5.0** — Guideline 12 rewritten |
| `M0_TrophicPyramid_README` | ✅ **2.2.0** — fully purged and **re-synchronised against M2**, not merely transliterated |
| `M0_PlateTectonics_README` | ✅ **NEW** — an *ontology* README (the file of that name was in fact the *simulation* README; it now lives at `_static/M0_PlateTectonics_Simulation_README.md`) |
| **`M0_TrophicPyramid.jsonld` vs its README** | ❌ **DIVERGENT** — the README is purged, the **data still carries `⊙` and `⊗`** in `m0:synergyPrinciple` and `m0:m1ContributionSummary`. Same for `M0_PlateTectonics.jsonld`. **→ SC-9** (flagged, not fixed: SC-1's mandate was the combo class, not the global `⊗` purge). |
| **The 14 M1 extension READMEs** | ❓ **UNKNOWN** — not all present, not all synced. **None was audited in this session.** |
| The M0 poclet READMEs (~25) | ❓ **UNKNOWN** — likewise |

### The rule this earns

> **A README is part of the deliverable, not a courtesy.** When a `.jsonld` is edited, its
> README is edited in the same breath — or it is *explicitly* recorded as divergent, with the
> worksite that will close the gap (as `M0_TrophicPyramid.jsonld` → SC-9 above).
>
> **And never transliterate a stale README.** Confront every formula against
> `M2_GenericConcepts.jsonld` first. The old notation was hiding old content; a mechanical
> substitution would have made the errors *look current*, and therefore **undetectable**.

### Proposed worksite — **SC-1.7: README audit**

Cheap, mechanical, high value. For each `M1_*.jsonld` and `M0_*.jsonld`:

1. does a README exist?
2. does its declared version match the `.jsonld`'s `owl:versionInfo`?
3. does it still contain `⊗`, `⊙`, `⊗⇒`, `KnowledgeFieldConceptCombo`, `morphism` (applied to
   `Fm2`/`Fm1m2`), or a monoidal formula on a combo?
4. do its formulas match what M2 **actually** says today?

Steps 1–3 are scriptable and belong in `ontology/cli-tools/` — **as a gate counter**, so that
README drift becomes a number that moves, like everything else. **Step 4 is semantic and needs
Michel.**


## 7. What to do next — the order has changed

| | Worksite | Why |
|---|---|---|
| **1** | **SC-5** (partial): SHAPE 2 ↔ SHAPE 3 | **~256 of 476 violations are pure noise.** Best effort/debt ratio in the whole project. Until it's fixed, the SHACL is unreadable — therefore unread. |
| **2** | **SC-2**: monoid qualification (`St`/`Ss`, `It`/`Im`) | **Shrunk by SC-1** — only *atoms* carry monoidal formulas now, so the perimeter is the atom set. ⚠️ SC-2's `FormulaShape` must **not** target `m2:GenericConceptCombo`: `DCC006` already forbids *any* operator there. Open question: does `M3_EagleEye`'s `typeSymbol` move `S→St`, or is qualification enforced only in formulas? |
| **3** | **SC-6**: the 163 | The heaviest. Malformed `Fm1m2` are the **normal regime** of the extension layer, not exceptions. |
| **4** | **SC-1.6**: instrument M2 and M3 | The gate says it at every run: *"an un-instrumented layer is not a passing layer — it is an UNMEASURED one."* `M3_Schema.shacl.ttl` exists (2026-07-03) and **no script runs it**. The `tscg-generate-mn-grammars` skill can produce both. **This is the gate's last blind spot** — and we have just spent two days learning what blind spots cost. |
| **5** | **SC-1.7**: README audit (§6-bis) | Cheap, mechanical, high value. A stale README is an authority that lies. |
| **6** | **SC-3**: rule D11 | "option or facet?" — asked in the right place |
| **7** | SC-8, SC-9, SC-4, SC-7 | SC-9: **no `sed`** (§4 and §6-bis) |
| — | **SC-0** | The 2026-07-03 staging (`Milestone`, `EpistemicMorphism`) is **still uncommitted**. Verified: it was never applied to the working tree, so nothing was lost. |

Also pending: **985 MB of Rust `target/` in git history** (now untracked; `git filter-repo`
would remove it, but it rewrites every hash — back up the folder first, not with `git clone`).
And **`cli_tools/` (underscore, root) vs `ontology/cli-tools/` (hyphen)** — a one-character
difference that has already caused a stumble. Rename or document.

---

## 8. Conventions (unchanged, plus two new ones)

`dcterms:creator` = "Echopraxium with the collaboration of Claude AI" · files in **English**,
conversation in **French** · `@base` = `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`
· changelogs **3 entries** (**M3: up to 7** — rollback safety) · **surgical `str_replace`
edits**, never rewrites · **honest negative results** over enthusiastic validation.

**NEW — `_` prefix = hidden from the gallery.** `_static/` = prototype (**not published**);
`static/` = finished (**published** by the index generator). **Renaming `_static/` → `static/`
publishes the prototype.** Each poclet carries **two distinct READMEs**: `M0_<Name>_README.md`
(the ontology) and `_static/M0_<Name>_Simulation_README.md` (the simulation). Do not merge them.

**NEW — reference locations.** `docs/reboot-kit/` is the single source for `TO_DO.txt`,
`TSCG_Reference_Corpus.md`, `TSCG_Smart_Prompt_*.md`, `TSCG_File_Tree.md`.
`ontology/docs/` holds `OntologyModeling_Guidelines.md`. **No copies elsewhere.**

---

## 9. The methodological lesson

Every serious defect found in this session failed **silently**. Not one crashed. Not one
reported an error. They stayed quiet — and that is precisely why they survived for months
inside a project that *had* validators.

SC-1's deepest contribution is not the rename. It is that **these silences are now loud**:
a crashed checker fails the gate; a missing compartment blocks it; a dropping counter is as
red as a rising one; and a lowered reference must be justified, recorded, and committed.

And the human gate held where the machine could not. **Michel caught the two worst errors of
the session — both mine, both late in the day, when my error rate rises.** The Ouroboros
thesis is not a slogan: execution accelerates, judgement does not delegate.

📖 `ontology/docs/_01_Worksite/SC-1_Completion_Report.md` ·
`ontology/StructuralGrammar/Functional_Grammar_Model.md`
