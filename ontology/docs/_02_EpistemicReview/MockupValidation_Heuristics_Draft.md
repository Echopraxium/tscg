# Validating a mock-up — three facets and their heuristics (draft for reflection)

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 0.2.0 (draft) · **Date**: 2026-11-15
**Status**: **DRAFT** — meant to start a reflection, not to be graved. No ontology,
tool or check is proposed for implementation here.
**Measured at**: HEAD `e2e80d2` (the facts in §5).
**Context**: the retirement of the scores and of the epistemic gap
(`ontology/docs/_01_Worksite/WS-15/`, note ≥ 0.5.0).

---

## 1. Starting points (Michel, 2026-11-15)

- The three monoids and the Layer Cake are **not a model of reality**: an architecture
  "until further notice" for the internal coherence of TSCG, whose goal is to build
  **mock-ups of models**. M2 concepts are **proxies**, as the gear in a Lego box is a
  very simplified object next to an industrial gear.
- **No scores.** Evaluation is **subjective** and the responsibility of the user and of
  the observers of the mock-up. It needs **at least one human observer**. TSCG computes
  no evaluation.
- **Evaluation is outside the model.** An M0 model is never legitimate to evaluate
  itself; the principle is now stated in `docs/CoreHypotheses/LayerCake_Models_The_Kit.md`
  §6.
- What can already be defined: three **validation facets**.
- What must be proposed (§6): heuristics of **validation and refutation**, for the
  mock-ups and also for the **Toolkit** itself — a source of improvement leads.

## 2. The three facets

| # | facet | the question | looks at | example |
|---|---|---|---|---|
| 1 | **Learning** | What did I learn by building or observing the mock-up? | the **observer** | building the thermostat mock-up made the negative loop visible: the setpoint, the comparison, the correction |
| 2 | **Realism** | How far is the mock-up *convincing* — which properties or functions of the original does it reproduce? | mock-up → original | the engine sound of a sports-car model |
| 3 | **Reality Check** | Which things, stated plainly, does the mock-up **not** reproduce? | original → mock-up | the specific structural constraints of the real Eiffel Tower (wind load, thermal expansion, riveted wrought iron) |

A reading of how they fit together (proposal): facet 1 is about the person, facets 2 and
3 are about the relation between the mock-up and its original, seen from both sides.
Facets 2 and 3 are Korzybski's principle put to work on one mock-up: the Map is not the
Territory — here is what this Map keeps (2), here is what it leaves out (3). The
Learning facet is why one builds a mock-up at all.

## 3. Heuristics — questions an observer can ask (proposal, open list)

These are prompts, not a checklist to pass. No answer is graded; an empty answer is an
answer too.

**Learning**
- What do I understand now that I did not understand before building or watching it?
- What surprised me? (A surprise is the best sign that the mock-up taught something.)
- What did I get wrong first, and what made me notice?
- What would I build differently next time?
- Could I explain the original to someone else with this mock-up in hand?

**Realism**
- Which properties of the original did I *choose* to reproduce, and why those?
- Does an observer who knows the original recognise them? (The "bluff" test: is it
  convincing to someone who did not build it?)
- Does a behaviour of the original appear that I did not put in explicitly?
  (An emergent match is stronger than a programmed one.)
- Which reproduced property only *looks* right — same appearance, different mechanism?
  (The engine sound played from a recording versus produced by the model.)

**Reality Check**
- What does the original have that the mock-up lacks: scale, materials, forces,
  constraints, context, history, the people who use it?
- What does the mock-up show that the original does **not** have — artefacts of the kit
  (discrete pieces, a simplified time step, a missing friction)? *(A possible second
  direction of the Reality Check; see Q3.)*
- Where does the analogy break first if one pushes it?
- What must **not** be concluded from this mock-up?
- Is each statement checkable by someone else (a source, a measurement, a drawing)?
  This facet is the one that aims at objective statements.

## 4. Who, and how it is recorded (proposal, minimal)

- **Who**: at least one human observer — the builder, a user, a third party. The
  observer is named, with the context in which they looked (a workshop, a review, a
  demo). Several observers can disagree; nothing is averaged.
- **What is kept**: free-text statements under one of the three facets, with the
  observer and the date. No score, no class, no aggregate, no "validated" status.
- **Where**: open (Q4). Close to the mock-up (its README or the instance itself) keeps
  it discoverable; outside the ontology keeps the method out of the grammar of systems
  (the reflexive-modelling trap: the evaluation of a mock-up is not a TSCG system
  concept).

## 5. What already exists at HEAD (facts)

- **An `observer` field** is the embryo of "who looks" (`ContextSwitching.md` §3.5
  already says so). It is written in several forms: `"observer"` (22 occurrences, a bare
  key — dropped on JSON-LD expansion), `m0:observer` (5), and local forms
  (`m0.bmc:`, `m0.fireTriangle:`, `m0.ptoe:`, `m0.thermostat:`,
  `m0.world2DProjection:observer`) — 18 instance files in all
  (`git grep -l -I -E '"(m0:|m0\.[a-zA-Z0-9]+:)?observer"\s*:' -- 'instances/**/M0_*.jsonld'`).
- **The name "RealityCheck" was already used — for something else.**
  `ontology/docs/_01_Worksite/WS-0/SC-3b_RealityCheck_ChangeRequest.md` (2026-10-19)
  proposed a facet labelling the *kind of paradigm* (Experimentable, Myth, Dream…); it
  was **withdrawn** the same day ("classifies without explaining, and quietly ranks")
  and replaced by **declared criteria** (`ContextSwitching.md` §3.4–§3.5). The Reality
  Check of this draft is not that facet: it states what a mock-up leaves out, which is
  close to what replaced it — "a switch should say what it loses" (`ContextSwitching.md`
  §11) and the *epistemic residue* (`The_Epistemic_Residue.md`). Keeping the name
  without saying so would invite confusion (Q2).
- **"Facet" already has a precise meaning in M3** (SC-3): an orthogonal classificatory
  axis with a controlled set of values (`m3:Facet`, `m3:FacetValue`,
  `m3:hasFacetValue`; one axis, `m3:Audience`). The three validation facets are not
  classificatory axes: they hold free statements by an observer, not values from a
  vocabulary (Q1).

## 6. Validation *and refutation*, for mock-ups and for the Toolkit (need recorded)

Recorded need (Michel, 2026-11-15): TSCG should **propose heuristics of validation and
of refutation** of its mock-ups, and possibly of the **Toolkit** itself; failures found
this way are a source of improvement leads.

First observations (proposal):
- **Refutation is not the negative of Realism.** A refutation heuristic looks for the
  case where the mock-up *misleads*: it behaves like the original for the wrong reason,
  or it suggests a conclusion the original contradicts. The Reality Check lists what is
  missing; a refutation shows that what is there is wrong.
- **Turned on the Toolkit**, the same questions read: which piece of the kit (an M2
  concept, a combo, a primitive, a simulation template) did the builder have to bend,
  stretch or work around? Where did several mock-ups of different domains hit the same
  wall? A recurring failure across mock-ups points at the kit, not at the mock-up — an
  improvement lead.
- **Who decides stays the same**: a human observer states the failure; the kit's
  maintainers decide whether it calls for a change. Nothing is computed, and the
  ontology-diagnosis pipeline remains the way a change gets into the kit.
- **Existing seeds**: the Ontological Overfitting filter (Decomposability,
  Transdisciplinarity, Atomicity) is already a refutation heuristic for candidate M2
  concepts; `ContextSwitching.md` §11 ("a switch should say what it loses", "a switch
  can manufacture a correspondence") gives two more.

## 7. Open questions (for Michel)

- **Q1 — The word "facet".** Keep "validation facets" as a working name in prose only,
  or choose another word (aspects, lenses, viewpoints) so that it is never read as an
  `m3:Facet`?
- **Q2 — The name "Reality Check".** Keep it (with a note on the withdrawn SC-3b facet),
  or rename it (e.g. "Residue", "What it leaves out")?
- **Q3 — Two directions?** Should the Reality Check also cover what the mock-up shows
  that the original does not (kit artefacts), or is that a fourth facet?
- **Q4 — Where are the statements kept?** In the instance README, in the instance file,
  in a separate observation file next to it, or nowhere in the repository (the observer's
  own notes)?
- **Q5 — The `observer` field.** Is it the seed of "who looks" (then its many forms are
  a small repair), or is it retired with the scores?
- **Q6 — The Kit.** A Kit workshop is a natural moment for the three questions (after
  building, before leaving). Should the Kit ask them, without storing anything?
- **Q7 — Refutation.** Is refutation a fourth facet, or a way of asking each of the three
  (can this learning be wrong? can this realism be a bluff for the wrong reason? is this
  Reality Check complete)?
- **Q8 — Toolkit feedback.** Where are kit-level failures collected, so that they become
  improvement leads (the Debt Overview, a worksite, `_03_SerendipCrates`)?

## Changelog

| version | date | change |
|---|---|---|
| 0.2.0 | 2026-11-15 | Evaluation outside the model (now in CH4 §6); §6 validation *and refutation* heuristics for mock-ups and for the Toolkit (need recorded); Q7, Q8. |
| 0.1.0 | 2026-11-15 | First draft: starting points, the three facets (Learning, Realism, Reality Check), heuristic questions, a minimal recording proposal, facts at HEAD (observer field, withdrawn SC-3b "RealityCheck", the M3 meaning of "facet"), six open questions. |
