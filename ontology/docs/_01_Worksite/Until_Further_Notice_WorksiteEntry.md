# Worksite Entry — "Until Further Notice" as Self-Improvement Commitment

**Version**: 0.1.0 (entry only — NOT a graved note)
**Date**: 2026-07-16
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Kind**: Epistemological positioning — **NOT an SC** (no ontology file, no formal gate)
**Home**: `docs/CoreHypotheses/` (guardrail corpus), not `ontology/`
**Status**: SCOPED — awaiting Michel's go to draft; nothing sealed
**Sibling notes it must not merely restate**: `_00_TSCG_as_StereoscopicGlasses.md`,
`TerritoryMap_Dichotomy.md`, `MultisubjectiveScoreEvaluationProtocol.md`,
`FitnessRazor.md`, `_01_Narcissus_and_Icarus_as_Safeguards.md`

---

## 0. Why this is a separate worksite (and not an SC)

The SC tree is **ontology engineering** (edits files, passes linter/Pellet/SHACL).
This is **positioning**: a guardrail the framework holds itself to. Filing it as an
SC would re-create the facet/grammar confusion the 2026-07-16 session spent its
time dissolving. It lives beside "Domain-algebra rejected" and "TSCG vs faceted
documentary classification" on the *why* side, not the *what* side.

---

## 1. Thesis

A framework whose central axiom is *"the Map is never the Territory"* cannot place
its value in a **final state** without contradicting itself — a Map taking itself
for the Territory is Narcissus. Its value is therefore in the **disciplined process
of revision**: the Milestone trajectory, residues catalogued then resorbed,
overfittings turned away at the door. *"Until further notice"* is the name of that
commitment — not an epistemic observation, but a **promise of revisability** the
project makes to itself.

Lakatos register: TSCG is not judged by a final theorem but by whether it stays a
**progressive** research programme (each adjustment opens new content) rather than a
**degenerating** one (each adjustment only patches). The judge of progressive vs
degenerating is the debt-vs-overfitting razor (§4).

---

## 2. Opening metaphor — the good specialised map

The same territory yields the hydrologist's map, the wind-farm siting map, the GSM
coverage map, the rail-network map. **None is less true than the others.** What
separates them is not fidelity to the territory but the **audience-use** each serves.
Quality shifts from *correspondence* to *fitness for a purpose*.

Two honesties define a good map, and they are the two axes of this worksite:

- **Perimeter honesty (space)** — it declares the audience it serves *and, by
  complementarity, the audience it does not*. The GSM map is not a bad hydrological
  map; it is not a hydrological map at all, and a good map says so. Silence about
  what it does not cover is a **virtue**, not a gap. A map claiming to serve every
  audience serves none well — the frog-that-would-be-an-ox of Risk 1.
- **Revision honesty (time)** — *"accurate until further notice"*: coastlines move,
  networks extend, the map is re-issued. This is the ModelSupersession discipline
  applied to the framework itself.

*Same figure, two angles: perimeter (for whom / not for whom) and revision (current
until further notice).*

**Guard against self-serving misreads.** Declaring an audience does NOT excuse
mediocrity for that audience ("I only meant it for hydrologists" is no cover for
being poor *for hydrologists*). Perimeter selectivity is a licence to **focus**,
never to be lax. Focus without quality = a lazy map; quality without focus = a
pretentious map (all audiences, good nowhere). The domain declaration and the
FitnessRazor must travel together.

Mapping of the metaphor onto TSCG's own architecture:
- common **territory** = the real system;
- **maps-per-audience** = `ontologyType` and the M1 extensions (the generic concept
  declined for a domain-audience);
- **declared audience** = `appliesToDomains` (SC-3), its *complementarity* = the
  multi-valued form (where it applies, and in negative, where it does not);
- **quality for the audience** = FitnessRazor (best attainable tool for the end, not
  correspondence to the territory).

---

## 3. TSCG's declared audience (Michel, 2026-07-16 — the core of the note)

TSCG's target public is **neither** the general public, **nor** systems scientists,
**nor** the domain experts of any single field (to validate / invalidate) — but the
**intermediate fringe**: engineers, artists, researchers who are drawn to a systemic
approach yet **intimidated** by it as an "elitist discipline".

The offer, stated plainly:

> *"Here is a toolkit to explore a systemic approach to your project or subject of
> interest."*

And, just as plainly, what it is **not**:

> The output is **not a predictive model**. It is a **structured laying-out of your
> own understanding, fed by a state of the art appropriate to your level of
> expertise.**

This is the perimeter declaration the opening metaphor demands. It sets, by
complementarity, what TSCG does *not* promise: no prediction, no expert-grade
authority in any single domain, no substitute for domain science. The value is
**democratising access to systemic thinking**, not adjudicating systems science.
(Note the direct tie to the `roleGrounding` / Democratization facet already in the
corpus — this is that facet stated as the project's own mission.)

Consequence for TscgTools: they should be built as **on-ramps for this fringe**
(explore, lay out, learn), not as authority engines. That is also the concrete
answer to Risk 2 — a tool a newcomer can actually pick up is a tool they can also
find wanting, i.e. a graspable handle for critique.

---

## 4. The debt-vs-overfitting razor (from EpistemicResidue)

Residue = the fraction of the Territory a Map does not absorb. Applied to the two
pathologies:

- **Technical debt** = a residue the Map *recognises but has not yet processed*
  (SHAPE 2↔3 noise, the `E:\` IRI bug, desynced READMEs). Catalogued, **reducible**;
  the remedy is work. → *"the Map is behind the Territory."*
- **OntologicalOverfitting** = the inverse: a Map claiming to have absorbed a residue
  *that did not exist* — an axis/facet/operator added to "cover" a case the Territory
  never presented (the one-member micro-facet, `Fm1`, the rejected domain-algebra). →
  *"the Map has overrun the Territory."* Fabricated residue; the frog swelling.

**Razor**: *an addition is good engineering if it reduces an attested residue; it is
overfitting if it claims to reduce a non-attested one.* Debt and overfitting are the
two sides of the same δ₁ frontier. Sibling of FitnessRazor (which discriminates the
thermodynamically untenable); admission test = is it irreducible to FitnessRazor and
to the Narcissus/Icarus pair? Provisional verdict: yes, it adds the *residue-
attestation* criterion neither carries — **to confirm externally, not by decree.**

This razor also supplies the **stopping criterion** for Risk 1: *the perimeter is
correctly addressed when the next addition no longer reduces any attested residue.*

---

## 5. The two risks (asymmetric — this matters)

- **Risk 1 — not knowing when the perimeter is correctly addressed** (the ox). This
  is **internal**, and TSCG already has the organs to hold it: ≥6-domain admission,
  the Triple Filter, Narcissus/Icarus, and now the residue razor's stopping
  criterion. The real danger is not "growing too big" but *lacking an arrest
  criterion* — which §4 supplies.
- **Risk 2 — presenting the project as "finalised / a reference"** when it should
  above all offer as many implementation paths (e.g. TscgTools) as invitations to
  critique, refutation, or perimeter redefinition. This is **external**, and *no
  internal mechanism neutralises it* — it is the very posture dark-matter / string
  theory occupy in the ModelSupersession seed-sort (a model rendering its own verdict
  the world has not rendered). Remedy is **social**, not internal: publish *to be
  refuted*, ship usable-therefore-falsifiable tools, invite the orthogonal judge
  (the "non-Cook"). "As many implementation paths as invitations to critique" should
  be a **publication rule**, not an intention.

---

## 6. TSCG as a ModelSupersession meta-instance of itself

If ModelSupersession has been running since **SDAP** (System Design Atomic
Principles, the first paper), then SDAP → … → v16.x is not a version log but a real
**Milestone trajectory** in the SC-7 sense: each step *bounds* the previous one
(`⊗` bounding the Hilbert tensor; `Fm2`/`Fm1m2`-functions bounding
`morphism_emergence`; `DomainConceptCombo` bounding `KnowledgeField`). TSCG would be
its own **seed instance** of `m3:ModelSupersession` — not a metaphor, a regular
instantiation, and a non-decorativity test of the type by self-application.

*Open, not decided here*: whether to actually grave TSCG-on-itself as a
ModelSupersession instance (SC-7 territory) or keep it as prose in this note only.

---

## 7. The guard that keeps this note from becoming its own overfitting

*"The value is in the process"* must **never** become an excuse to ship nothing
falsifiable. The process has value only if, at each Milestone, it produces something
an outsider can **grasp and break**. A history of consolidation is precious only if
studded with **handles** offered to critique — otherwise it is a private diary, not a
research programme. This is Risk 2 met from another direction, and it must be the
note's first line, not its footnote.

---

## 8. When drafted (not now)

- Pull the **real text** of the sibling notes from the repo (`git HEAD`), not from
  memory, before writing — to run the irreducibility test against
  `StereoscopicGlasses` / `TerritoryMap_Dichotomy` / `MultisubjectiveScoreEvaluationProtocol`.
- Draft `docs/CoreHypotheses/Until_Further_Notice_SelfImprovement_Commitment.md`
  under the standard admission discipline (irreducible · transdisciplinary · survives
  external test before sealing).
- Author field, English file, conventions per the worksite map §5.

---

## 9. Suggested TO_DO line (separate from the SC list)

```
** [CoreHypotheses / positioning — NOT an SC] "Until Further Notice" as self-improvement commitment
   - Opening metaphor: the good specialised map (perimeter honesty + revision honesty)
   - Declared audience: the intimidated intermediate fringe (engineers/artists/researchers),
     NOT general public / systems scientists / single-domain experts
   - Offer = "a toolkit to explore a systemic approach", output = structured lay-out of
     one's understanding + level-appropriate state of the art, NOT a predictive model
   - Debt-vs-Overfitting razor (from EpistemicResidue) = attested vs fabricated residue
   - TSCG as ModelSupersession meta-instance of itself (SDAP → v16.x = Milestone trajectory)
   - GUARD: process-value must still ship falsifiable handles (Risk 2)
   - Admission test before sealing: irreducible vs StereoscopicGlasses / TerritoryMap /
     MultisubjectiveScoreEvaluationProtocol — confirm EXTERNALLY
```
