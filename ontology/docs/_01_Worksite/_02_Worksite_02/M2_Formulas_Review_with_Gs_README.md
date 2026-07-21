# M2 Formulas Review with Gs — Worksite README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 1.0.0
**Date**: 2026-07-18
**Status**: OPEN — decisions recorded, execution pending
**Layer**: M2 (`M2_GenericConcepts.jsonld`, v16.17.0 at time of audit)
**Pipeline phase**: Phase 0 (change request) + Phase 4 (semantic decisions) of
`tscg-ontology-diagnosis-pipeline`. Phases 2/3/5 not yet run.

---

## 1. Purpose

The Stereopsis monoid **Gs** (`𝕋₀(|) = {T, _^, _$, K, Ss, L}`, plus the derived
element `_0`) was introduced *after* most M2 canonical formulas were written.
Those formulas have **never been systematically re-examined** in its light.

This worksite is that re-examination: a full review of the **97 canonical formulas**
carried by `m2:hasStructuralGrammarFormula`, asking of each one whether it is
under-specified because Gs was not available when it was authored.

**Trigger**: audit session 2026-07-18 (Michel + Claude), during SC-2 preparation.
Two atoms — `State` and `Symmetry` — were found to carry single-primitive formulas
that Michel judged "too basic on a systemic level". Investigation confirmed
attested residue in both. See §5.

---

## 2. Baseline measurements (M2 v16.17.0, audited 2026-07-18)

| Metric | Value |
|---|---|
| Canonical formulas (`m2:hasStructuralGrammarFormula`) | **97** |
| …already SC-2 conformant (no bare `S`/`I`) | 54 |
| …carrying bare `S` or `I` (SC-2 perimeter) | 43 |
| …using **any** Gs primitive (`T`, `K`, `Ss`, `L`) | **18** (≈19 %) |
| …using an oriented pole (`_^` / `_$`) | 11 concepts |
| …using the equilibrium element `_0` | 2 (`Balance`, `TriadicBalance`) |
| …using `T` | **1**, and it is malformed (`Gradient`, see F3) |
| …using `\| T` (correct stereopsic form) | **0** |
| Distinct formula-collision groups | 14 |

**The headline figure is 18/97.** Roughly four fifths of the M2 corpus predates any
serious use of Gs. That is the quantitative justification for this worksite: it is
not a suspicion, it is measurable.

---

## 3. Scope boundary — this worksite is NOT SC-2

The two must not be merged. They differ in nature, risk, and validation gate.

| | **SC-2** (notation) | **This worksite** (semantics) |
|---|---|---|
| Nature | Mechanical substitution | Conceptual revision |
| Content | `S → St`, `I → It` on 43 formulas | Formula redesign, definition rewrite |
| Risk | Nil (no semantics touched) | Requires domain validation |
| Golden impact | Predictable | Must be assessed per decision |
| Authority | LLM may execute | **Michel only** (semantic architecture) |

**Consequence for `State` and `Symmetry`**: both are inside the SC-2 perimeter
(they carry bare `I` and `S`). SC-2 ships them as the plain migration
`State = It`, `Symmetry = St` — *mandatory*, since SC-2 introduces a SHACL shape
forbidding bare `S`/`I` in atom formulas. Their semantic revisions (§5) ship here,
later, as separate commits.

Cost: the formula field of both concepts is edited twice. This is accepted
deliberately, to buy a readable validation gate — if the golden moves, one can tell
whether it came from notation or from semantics.

---

## 4. Attested rules confirmed during the audit

These are not new rules. They were already in the corpus, and the audit surfaced
them. They are recorded here because they *ground* the decisions in §5 — no formula
below is improvised.

**R1 — Poles are orientation; `_0` is non-orientation.**
All 11 concepts carrying `_^`/`_$` are **directed pairs**: Encoding/Decoding,
Recognition/Reuse, Positive/Negative Synergy, Fusion/Fission,
Activation/Inhibition, Convergence/Divergence, Composition/Decomposition,
Amplification/Attenuation, Entropy/Negentropy, Coherence/Incoherence,
Potentialization/Depotentialization. `_^` marks the onset/amplifying/constructive
direction, `_$` the terminus/attenuating/destructive one. Therefore
`_0 = _^ | _$` is the fusion of both directions — i.e. **the absence of a
privileged direction**.

**R2 — Absence of `D` encodes reversibility by construction.**
Stated explicitly in `m2:Stase`: *"Stase is NECESSARILY REVERSIBLE — this
reversibility is structurally encoded by the ABSENCE of D in the structural formula
(a-temporal state)"*, and in its `m2:m3Note`: *"Absence of D in structural formula
guarantees reversibility by construction — no temporal sealing possible."*

**R3 — Formulas are commutative.** Confirmed by Michel, 2026-07-18. The Territory
segment is a multiset: `D × It ≡ It × D`. Collision tests in this worksite normalise
accordingly.

**R4 — A formula is not an identifier.** 14 collision groups already exist
(e.g. `It × St × D` is shared by Emergence, Path, Segmentation, Step,
Transformation; `A × St` by Hierarchy, Invariant, Resilience, Stase). Formula
collision is therefore **not disqualifying**. Precedent for discrimination resting
entirely on the Gs suffix: `Synergy = It × D | _^ / _$` shares its Territory core
with Event, Trigger and Action.

**R5 — Gs primitives are irreducible.** Each Gs primitive carries an explicit
anti-reductionist clause (`T`: *"irreducible — not derivable from F, D, or Im"*;
same pattern for `K`, `Ss`, `L`). A Gs primitive is **never** a composition of Gt/Gm
primitives, whatever the prose of its definition may suggest. See F1.

---

## 5. Decision records

### GS-1 — `m2:State` : `I` → `It × D | T`

**Status**: DECIDED by Michel (2026-07-18). Execution pending.

**Attested residue.** `State` was defined as `I` alone, with the comment
*"Instantaneous configuration of system variables"*. M3 defines the primitive `I`
(Information) as *"Encoded content distinguishing this system **state** from
alternatives"* — the primitive's own definition already contains the notion of
state. `State = It` was therefore **near-tautological**: the concept added nothing
to its own primitive. This is a real defect, not a fabricated one.

**Michel's reading (the resolving argument).** A State is a **state variable**:
it changes dynamically and can be *measured at each instant t*. This dissolves the
apparent tension between "instantaneous" and "dynamic" — in control theory the state
is the minimal information at instant *t* that determines future evolution (Markov
property). Instantaneity is not the absence of dynamics; it is the *support* of
dynamics.

**Component justification.**

| Component | Role |
|---|---|
| `It` | the configurational content |
| `D` | the state determines the evolution (state-variable semantics) |
| `\| T` | measurable at each instant *t*; the temporal cut is a Territory/Map correspondence |

**Why `T` and not more `D`.** M3 states that `T` captures *"what is relational in
time — **not what a system does in time (F, D)**, nor how a model qualifies time
(Im), but how Territory and Map correspond temporally"*. `T` therefore does **not**
carry the dynamic aspect; `D` must be present explicitly for it. Conversely `T` is
what makes the "instant" observer-relative (a market's state per second, a star's
per millennium).

**Collision check**: no exact collision, verified across 17 files (M2 +
M1_CoreConcepts + all M1 extensions). Territory-core neighbours sharing `{D, It}`:
Event, Trigger, Action (`D × It`) and Synergy (`It × D | _^/_$`). Discrimination
rests on `| T`, which is legitimate per R4.

**First correct use of `T` in the corpus** — see F3.

**Remaining work when executed**: rewrite `rdfs:comment` (the current wording stops
at "instantaneous configuration" and must carry the state-variable reading); set
`m2:isStereopsic` to `true` (currently absent); decide on the missing `sphinxView`
(open it or declare it empty).

---

### GS-2 — `m2:Symmetry` : `S` → `St | _0`

**Status**: DECIDED by Michel (2026-07-18). Execution pending.

**Attested residue.** `Symmetry = S`, comment *"Invariance under transformation."*
`Invariant = S × A`, comment *"Property unchanged under specific transformations or
operations."* The two definitions were **near-identical**, and Symmetry's formula
was strictly the poorer. Left as-is, this is an OntologicalOverfitting signature
(two concepts for one phenomenon) — or, at minimum, an under-differentiation defect.

**Michel's reading.** Symmetry is **reversible** and **non-oriented**. Both criteria
map onto rules already attested in the corpus:

| Criterion | Formal encoding | Source |
|---|---|---|
| non-oriented | `\| _0` (fusion of `_^` and `_$` = no privileged direction) | R1 |
| reversible | **absence of `D`** in the formula | R2 (Stase) |

`St | _0` satisfies both — the second one *by construction*, with nothing to add.

**Resolution of the Symmetry/Invariant duplication.** The pair becomes crisply
distinct on the orientation axis:

- `Invariant = St × A` — **oriented** (preserved *toward* an attractor)
- `Symmetry = St | _0` — **non-oriented**

And the equilibrium family reads cleanly:

- `Symmetry = St | _0` — static **structural** equilibrium
- `Balance = A × St × F | _0` — **dynamic** equilibrium (attractor + flow)

**On the missing "transformation".** An objection was raised during the audit: the
formula says nothing about transformation, yet "invariance under transformation" is
the classical definition. Michel's position resolves it — the transformation is the
**means of revealing** the symmetry, not what the symmetry *is*. What it is: a
structure with no privileged direction, hence reversible. The formula states exactly
that. **The `rdfs:comment` must be rewritten accordingly** — otherwise formula and
definition describe two different things.

**Collision check**: no exact collision (17 files). Third use of `_0` after Balance
and TriadicBalance — an attested pattern, not a new construct.

**Remaining work when executed**: rewrite `rdfs:comment` (reversibility +
non-orientation); remove or redo the `sphinxView` (see F4).

---

## 6. Flagged findings (not decisions — inputs to the review)

**F1 — `T`'s definition invites a compositional misreading.**
`skos:definition` says `T` *"emerges from the fusion of Territory time (as
flow/evolution: F, D) and Map time"*, while `rdfs:comment` two lines below says
*"T is irreducible — not derivable from F, D, or Im"*. The first wording caused an
actual misreading during this very audit (Claude argued `It × D | T` double-counted
`D`; Michel corrected it). The other Gs primitives use an "interface" phrasing that
does not invite this. **Wording to harden in M3.**

**F2 — `_0` carries two readings in the corpus.**
Its `rdfs:comment` gives the general one — *"the optimal central state in a triadic
balance: neither excess (`_^`) nor deficit (`_$`)"* — which supports "structure at
equilibrium". Its `m3:semantics` gives a narrower one — *"Territory excess and
Territory deficit fuse into Map-Territory correspondence […] optimal Territory/Map
calibration"* — which is about model/reality fit. This ambivalence produced a
disagreement during the audit. **To harmonise in M3.**

**F3 — `Gradient` is malformed.**
Formula: `F × T  or  I × T`. Two defects: (a) prose inside a formula (the `or`);
(b) `×` (Territory operator) applied to `T`, a Gs primitive — a violation of the
operator reservation rule (`×` = Gt, `+` = Gm, `|` = Gs). This is the *only*
occurrence of `T` in the corpus, and it is wrong. Consequence: GS-1 would be the
first correct use of the primitive.

**F4 — `Symmetry`'s `sphinxView` is non-discriminating.**
`formulaPrimary = "O + V"`, marked *"PROPOSITION (validation in progress)"*. `O` =
*"the phenomenon can be detected and measured"*, `V` = *"model predictions can be
tested against Territory observations"* — true of nearly every M2 concept. The
PROPOSITION marking was lucid; do not grave as-is.

**F5 — `m2:eagleView.formula` is a fossil duplicate.** *(separate decision, pending)*
66 atoms carry it; **38 are identical** to the canonical formula and **28 have
diverged**, always with the canonical being the up-to-date one (e.g. `Layer`: canon
`St × It × A | R` vs eagle `S × I × A × R`; `Code`: canon `It × Ss` vs eagle
`I × S`). **0 atoms** carry an `eagleView.formula` without a canonical formula — it
holds no information of its own. This is structurally the same anti-pattern as the
retired D8 triad in M1 (`…FormulaExpanded/TeX/RawText`): one claim stored twice, one
copy drifting. Note the interaction: **migrating the 43 SC-2 formulas without
resolving this will widen the divergence from 28 to ~50.** Decision required —
synchronise (treats the symptom) or delete (extinguishes the debt).

**F6 — `sphinxView` coverage is thin overall.** Only 7 atoms carry one, and several
use ASFID letters with the `+` operator (e.g. `Behavior: S + D + F`), which is
inconsistent with the REVOI-based Map notation. Needs its own pass.

---

## 7. Method & discipline

Applied throughout the audit, and binding on the rest of the worksite:

1. **Anti-overfitting razor.** An addition is legitimate only if it reduces an
   **attested** residue. Both GS-1 and GS-2 point at a documented defect
   (tautology with `It`; near-duplication with `Invariant`). "The formula looks too
   basic" is a *trigger for investigation*, never a justification on its own.
2. **No formula improvisation.** Claude supplies measurements, collision checks,
   corpus evidence and objections. The formula itself is Michel's — semantic
   architecture is the human's role (`tscg-ontology-diagnosis-pipeline`).
3. **Systematic collision check** before any proposal, over M2 + M1_CoreConcepts +
   all M1 extensions, with commutative normalisation (R3).
4. **Formula and definition must agree.** Every formula revision in this worksite
   carries a `rdfs:comment` rewrite. A formula that outruns its definition is new
   technical debt.
5. **Minimality.** A "too basic" formula is not automatically wrong — some concepts
   are legitimately primitive-adjacent. Requiring every atom to be hybrid would be
   OntologicalOverfitting in reverse.

---

## 8. Next candidates

Not yet examined; listed so the worksite has a work front rather than a wish.

- The **invariance cluster**: `Topology` (`St | L`), `Stase` (`St × A`),
  `Invariant` (`St × A`) — GS-2 settled Symmetry vs Invariant, but Stase and
  Invariant still share a formula.
- The **79 formulas with no Gs component** — systematic pass, concept by concept.
- `Gradient` (F3) — repair required regardless of the Gs question.
- The `sphinxView` layer as a whole (F6).

---

## 9. Changelog

| Version | Date | Changes |
|---|---|---|
| **1.0.0** | 2026-07-18 | Worksite opened. Baseline measured on M2 v16.17.0 (97 canonical formulas, 18 using Gs). Scope boundary with SC-2 fixed. Attested rules R1–R5 recorded. Decisions GS-1 (`State = It × D \| T`) and GS-2 (`Symmetry = St \| _0`) recorded with justification and collision checks. Findings F1–F6 flagged. |

---

## 10. Status summary

| Item | State |
|---|---|
| GS-1 `State` | DECIDED — execution pending |
| GS-2 `Symmetry` | DECIDED — execution pending |
| F5 `eagleView.formula` | **DECISION REQUIRED** (blocks/interacts with SC-2) |
| F1, F2 | M3 wording repairs — open |
| F3 `Gradient` | Repair — open |
| F4, F6 `sphinxView` | Open |
| Remaining 79 formulas | Not started |

**Authority reminder**: the only authority is `git show HEAD:<file>`. All figures
in this document were measured on files supplied during the 2026-07-18 session and
must be re-verified against HEAD before execution.
