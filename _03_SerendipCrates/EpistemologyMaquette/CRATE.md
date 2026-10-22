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

## 4. Pending decisions (Michel)

- Accept the four failure criteria (as they stand or amended).
- Domain: option a — `m1:domain:Philosophy` now (a class on HEAD); option b — wait for
  SC-5b ("Epistemology" is only a string in `m1:subdomains`).

## 5. Seeds for other crates

Discoveries made here that may open other crates. Recorded as pointers only — a seed
becomes a crate only when Michel opens it, with a possible destination and a failure test.

| Seed | Where | Note |
|---|---|---|
| Invariants without a metric (prism / relativity / Erlangen / structural grammar) | `Note_InvariantsWithoutMetric_2026-10-22.md` | Candidate subject #3; external parents Cassirer, Nozick |
| Kuhn's incommensurability vs TSCG's transdisciplinary claim | §1 above | Does a shared M2 signature survive a change of meaning? |

**Author**: Echopraxium with the collaboration of Claude AI
