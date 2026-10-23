# Crate — EpistemologyMaquette

| Field | Value |
|---|---|
| **Opened** | 2026-10-22 |
| **Status** | `sealed` (resealed 2026-10-22 after the first analysis session) |
| **Idea** | Build an *existing, external* epistemology as a TSCG M0 maquette — never "epistemology" as a whole |
| **Goal** (Michel, 2026-10-22) | Model an external epistemology **without proving or refuting it**. The maquette makes explicit **what validated or challenged it in the history of epistemology** — who, when, with which argument, under which criterion, and with which reply. History arbitrates, not TSCG |
| **Main risks** | Ontological Overfitting; Narcissus/Icarus; tautological Grand Unifying Framework (the M3 grammar is itself an epistemological stance); selection bias in which reception history is followed |
| **Possible destination** | M0 instance, category `m3:SystemicFramework` (checked on HEAD 2026-10-22: "established methodologies (TRIZ, VSD)") |
| **Next step** | Michel's two pending decisions (below), then pipeline step 2 (Analysis). No `.jsonld` before then |
| **Contents** | `TSCG_HandOver_EpistemologyMaquette_2026-10-22.md` · `Note_InvariantsWithoutMetric_2026-10-22.md` |

---

## 1. Line-up (agreed 2026-10-22)

| Role | Who | Why |
|---|---|---|
| **Subject** | Lakatos — *Falsification and the Methodology of Scientific Research Programmes* (1970) | External epistemology with a documented reception |
| **Historical interlocutors** | Popper, Kuhn, Feyerabend | Not rivals chosen by us: the people who **actually** discussed Lakatos (London colloquium 1965, published as *Criticism and the Growth of Knowledge*, 1970). Objections are selected by the record, not by taste |
| **Adversary of TSCG** | Descartes — *Discours de la méthode* (1637), *Méditations* with the *Objections and Replies* (1641) | Separate maquette. Tests whether the kit can model, **without judging**, a stance opposed to its own (a self-certifying foundation vs "every paradigm has its turtle"). Its reception record is built in: the *Objections and Replies* (Hobbes, Arnauld, Gassendi…). The Cartesian circle is recorded as **Arnauld's objection with Descartes's reply**, never as a TSCG verdict |
| *Optional, later* | Kuhn's incommensurability | Targets TSCG's transdisciplinary claim itself, not one epistemology |

Rejected as adversaries (already absorbed or aligned with TSCG): Popper (wired into the
pipeline — "Refutation (Popper)"; his "piles driven into a swamp" is TSCG's turtle),
Kuhn (the vocabulary of `ModelSupersession.md`), Montaigne (aligned with "until further
notice"). Plato kept as an alternative adversary (not a methodology).

**Framing caveat — Descartes.** He is adversarial by his *endpoint*: doubt is a means
to reach a certainty that ends doubt (the cogito, then divine veracity). Doubt itself
aligns with TSCG. A maquette keeping only "Descartes the doubter" would be a mirror.

**Declared alignment — Lakatos.** His own meta-criterion (*History of Science and Its
Rational Reconstructions*, 1971) is that a methodology is judged by how well it
rationally reconstructs the history of science — the same move as this crate's goal.
A strength (he can be judged on his own ground) and a point to declare. The corpus also
already maps the protective belt to `E` (`ContextSwitching.md` §9) and the degenerating
programme to dogma (`ModelSupersession.md` §4.6): those correspondences do not count as
success.

## 2. What each pair preserves and sacrifices

**Lakatos / Popper — a genuine trade-off, within one criterion (experiment).**

| | Preserves | Sacrifices |
|---|---|---|
| **Popper** | Sharpness: an accepted refutation brings the theory down; no theory can immunise itself | Patience: Newton rejected over Uranus in 1845, one year before Neptune |
| **Lakatos** | Patience and history: a programme gets time to answer its anomalies | Real-time verdict: Neptune and Vulcan are the same move; only the future tells which was progressive. No deadline for abandoning a degenerating programme (Feyerabend's objection) |

Read as two opposite errors: Popper risks **killing a good theory too early**; Lakatos
(and Kuhn, further still) risks **keeping an exhausted one too long**. No rule avoids both.

Shared test case: Newtonian mechanics — Uranus → Neptune (1846, progressive);
Mercury's perihelion (1859) → Vulcan never found → general relativity (1915).

**Lakatos / Descartes — not a trade-off: two different goals.**

| | Preserves | Sacrifices |
|---|---|---|
| **Descartes** | Certainty: an indubitable foundation, knowledge deduced from it step by step | Revisability: nothing in the method provides for revising what was deduced; the foundation did not protect his vortex physics from error |
| **Lakatos** | Revisability: everything, the core included, falls if the programme degenerates | Certainty: the core is held only by decision |

This is reading **(b)** in concrete form: rules within one criterion are comparable on
one scale; across criteria there is no common scale, only a declared context switch
(`ContextSwitching.md` §11: a switch says what it loses).

## 3. Failure criteria (proposed)

1. **Decorative** — the maquette only lists objections, like a table of contents. It
   succeeds only if it shows what prose blurs: **the same objection bites under one
   criterion and not under another, and it targets a specific piece** (core, belt,
   heuristic, appraisal rule).
2. **Forcing** — a piece requires a new M2 concept that fails the candidate filter.
3. **Mirror** — only correspondences the corpus had already written are found.
4. **Adversarial** — Descartes can only be modelled by judging him.
5. **Out-of-sample** (Michel, 2026-10-23) — the maquette must be tested on at least one
   historical episode chosen **before** the analysis and **not** among the canonical
   examples of the modelled epistemology. Success only on those canonical examples does
   not count: it is a backtest on training data. For Lakatos, Uranus/Neptune and
   Mercury/Vulcan are canonical (in-sample); a candidate out-of-sample episode is
   continental drift (already a `ModelSupersession.md` seed).

   Rationale: overfitting (backtesting of trading strategies — Bailey, Borwein,
   López de Prado & Zhu, "Pseudo-Mathematics and Financial Charlatanism", *Notices of
   the AMS*, 2014) and the researcher's confirmation bias (Wason's 2-4-6 task, 1960).
   Lakatos's own criterion is close to an anti-overfitting rule: a degenerating
   programme fits known data after the fact (in-sample); a progressive one predicts a
   novel fact (out-of-sample). Criteria 1–5 stated before building act as a
   pre-registration; the adversary acts as an adversarial collaboration. The same
   caution applies to this crate's own analysis sessions: convergence of every idea
   with TSCG is itself an alarm signal.

## 4. Pending decisions (Michel)

- Accept the five failure criteria (as they stand or amended).
- Domain: option a — `m1:domain:Philosophy` now (a class on HEAD); option b — wait for
  SC-5b ("Epistemology" is only a string in `m1:subdomains`).

## 5. Seeds for other crates

Discoveries made here that may open other crates. Recorded as pointers only — a seed
becomes a crate only when Michel opens it, with a possible destination and a failure test.

| Seed | Where | Note |
|---|---|---|
| Invariants without a metric (prism / relativity / Erlangen / structural grammar) | `Note_InvariantsWithoutMetric_2026-10-22.md` | Candidate subject #3; external parents Cassirer, Nozick |
| Kuhn's incommensurability vs TSCG's transdisciplinary claim | §1 above | Does a shared M2 signature survive a change of meaning? |
| Utility as the adequacy of a map to a need (Michel, 2026-10-23) | §6 below | The need justifies the criterion; the criterion makes the map judgeable |
| Bachelard — epistemological obstacles and breaks | §6 below | External subject, and a possible adversary of the utility seed |
| Pragmatism ennobled by cybernetics (Michel, 2026-10-23) | §6 below | Black box, good regulator; tension with Bachelard |
| Form as a reference frame — knots, π with a string, Möbius strip (Michel, 2026-10-23) | `Note_InvariantsWithoutMetric_2026-10-22.md` §9–10 | Structural invariants survive the imprecision of the hand; boundary objects. Beware of epistemic dogfooding |
| "Epistemic pivot" (first named "epistemic interface") — one object, many modes of access (Michel, 2026-10-23) | `Note_InvariantsWithoutMetric_2026-10-22.md` §11 | Parents: boundary object, trading zone, epistemic thing. REVOI fit flagged as dogfooding risk; out-of-sample test on Star & Griesemer's case. **Graduated (seed only) 2026-10-23** → `docs/CoreHypotheses/EpistemicPivot.md`, section "Exploratory" (Michel's decision; no innovation claimed, sources cited; still to be paid by use). Renamed after a name collision (Marin, *Topoi*, 2024) |

## 6. Seed notes (2026-10-23)

**Utility as adequacy of a map to a need.** A bat keeps not one map of "the" cave but
several, each indexed by a need (drink, hunt, rest, mate). The idea refines reading (b):
it says **where a criterion comes from** — from a need. `ContextSwitching.md` §3.2
already shows it (*Maurice v. Judd*, 1818): the merchants' need (taxing sea oil) gave
the habitat criterion, the naturalist's need gave the anatomical one. It also reads
bounding by morphism: Newton is kept for the need it still serves best (building a
bridge); relativity is needed for others (GPS clocks).

- External parents: pragmatism — C. S. Peirce, "How to Make Our Ideas Clear" (1878);
  W. James, *Pragmatism* (1907); J. Dewey. G. E. P. Box, "all models are wrong, but
  some are useful".
- Classic objection: a false belief can be useful (a comforting myth). The bat answers
  it only for utility **tested by the Territory** (a wrong water map means thirst), not
  utility as comfort. That is closer to Peirce than to James.
- Limit: a map optimised for one need is blind to others — the epistemic residue.
- Concrete proposal (not graved): the open question of `ContextSwitching.md` §13 (how
  to declare criteria) could take the form of a triple —
  **who** looks (the existing `observer` field) · **for what** (the need) ·
  **by which criteria**.
- Caution: pragmatism is closely aligned with TSCG's own stance (the Bootstrap judges
  TSCG by "usefulness as a toolkit"). Never inject it into a maquette as TSCG's
  stance; modelled only as an external subject, with its reception (e.g. Russell's
  criticism of James).

**Bachelard.** Gaston Bachelard (1884–1962), central to the French tradition of
historical epistemology (later Canguilhem; the "epistemological break" taken up by
Althusser). *Le Nouvel Esprit scientifique* (1934); *La Formation de l'esprit
scientifique* (1938) — **epistemological obstacles** (first experience, verbal habits,
substantialism, animism…) that knowledge must overcome; science advances by
**breaks** with common sense and by rectified errors; *La Philosophie du non* (1940) —
a new theory generalises the old one (non-Euclidean, non-Newtonian), close to
"bounding by morphism". *La Psychanalyse du feu* (1938) analyses fire reveries as
obstacles to chemistry — a link to the FireTriangle poclet and to the phlogiston seed
of `ModelSupersession.md`.

- Why it matters here: Bachelard counts **utilitarian, pragmatic knowledge among the
  obstacles** to scientific knowledge. He is therefore a natural **adversary of the
  utility seed** — the bat's need-indexed maps are exactly the first-hand knowledge he
  says science must break with. Verified 2026-10-23: *La Formation de l'esprit
  scientifique* (1938), chapter V, « La connaissance unitaire et pragmatique comme
  obstacle à la connaissance scientifique ».
- Also a candidate subject in his own right: a published, dated epistemology with a
  documented reception, and his "obstacles" answer the bat question directly (how does
  one avoid obstacles and dead ends?).

**Pragmatism ennobled by cybernetics (Michel).** Bachelard's objection to pragmatic
knowledge — "we know it works, not why or how" — can be met, at least in part, by
cybernetics, which made "knowing without opening the box" a rigorous level of knowledge.

- W. R. Ashby, *An Introduction to Cybernetics* (1956) — the **black box**: a system
  studied through its inputs and outputs, predictable and controllable without its
  mechanism.
- R. C. Conant & W. R. Ashby, "Every Good Regulator of a System Must Be a Model of
  That System" (1970) — successful regulation **implies** a model, even an implicit one.
  This is what turns "utility tested by the Territory" into more than convenience.
- Living example: **sea turtles** (K. Lohmann and colleagues) use the geomagnetic field
  as a map and return to nest on their natal beach — a need-indexed map (breeding),
  tested by success. Whales: magnetic orientation is a hypothesis with suggestive
  evidence only (e.g. strandings vs geomagnetic anomalies, Kirschvink 1986) — not to be
  cited as established. The sensing mechanism itself is still not settled: scientists
  are, here, in the "it works, we don't know how" position too.
- **Bachelard is not refuted by this.** The two positions bear on different properties
  of a map: the turtle's map is effective and verified by success, but neither
  representable nor shareable — no one can read or criticise it. What Bachelard calls
  scientific is the passage to an **explicit, communicable, rectifiable** map. In TSCG
  terms, one *possible* reading is that science mainly adds `R` (Representable) and
  `Im` (Interoperable) to a map that already worked.
- Caution: that reading is TSCG reading Bachelard and Ashby with its own pieces — a
  modelling lead, not an arbitration. In a maquette it would appear as one reading
  beside their positions on their own criteria.

**Author**: Echopraxium with the collaboration of Claude AI
