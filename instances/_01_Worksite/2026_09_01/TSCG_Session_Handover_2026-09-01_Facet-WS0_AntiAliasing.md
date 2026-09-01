# TSCG — Session Handover 2026-09-01 — Finalize the Facet-M3 principle

**Author**: Echopraxium with the collaboration of Claude AI
**HEAD at close**: `7da58af` — *nothing was pushed this session (exploration only); treat as unverified, confirm with `git show HEAD`.*
**Suggested archive path**: `ontology/docs/_01_Worksite/WS-0/`

> This is a **HandOver**: a thin loader to resume an in-progress worksite. It carries
> no authoritative framework content — only pointers to HEAD and fresh session state.
> Paste it as the first message of a new conversation.

---

## 0. Load first — by name

- **`head-over-memory`** — authority discipline (verify at source; never recite a
  verifiable fact from memory or corpus).
- **`tscg-ontology-diagnosis-pipeline`** — the 6-phase pipeline; this session's goal is
  an M3/M1 ontology change, so it governs.

**Governing rule**: HEAD is the only authority. Read every framework fact from HEAD
(raw CDN `https://raw.githubusercontent.com/Echopraxium/tscg/main/…` or `git show HEAD:<file>`),
never from memory.

---

## 1. Session goal

**Finalize (grave) the Facet-M3 architectural principle.**
Worksite **WS-0** (confirmed by the note's HEAD path). Sub-worksite **SC-3** per Michel —
*reconfirm on HEAD* (a `SC-3_Facet_Decision_Record.md` appears under `WS-0/` in the tree;
verify it is live, not a vestige).

---

## 2. Established this session (read from HEAD — re-verify, don't trust this list)

- The Facet architecture note **exists**:
  `ontology/docs/_01_Worksite/WS-0/_01_Facet_as_M3_Principle_ArchitectureNote.md`.
- The principle is **NOT graved**: `m3:Facet` / `Facet` = **0 occurrences** across all live
  M3 files (`M3_GenesisGrammar`, `M3_GrammarFoundation`, `M3_EagleEye`, `M3_SphinxEye`,
  `M3_BicephalousPerspective`); `M1_Domains.jsonld` uses **no SKOS** (no ConceptScheme/Concept).
- Note terminology **(HEAD, corrects a likely memory drift)**: **Facet = the axis**,
  **Focus = the value** on the axis — *not* "FacetValue". The disciplinary **domain is a
  facet** (type *conferred*).
- Note **§7** states it explicitly: the **Facet-M3 principle and the Domain-fusion Phase 0
  are the same idea from two ends**. `M1_Domains` is therefore already, structurally, an
  instance of the *domain* facet (axis = domain; Focus = Biology, Optics, …).
- Note **§9** lists **three open, unsigned decisions**:
  - (A) `m3:Facet` = axis (A1, recommended) **vs** value-registry (A2)
  - (B) Derived **vs** Conferred facets (sub-typing, not exclusion)
  - (Sequencing) Facet-M3 **before / with / after** the Domain-fusion Phase 0

---

## 3. Working copy in flight — NOT graved (reconsider UNDER Facet; do not grave as-is)

This session drifted into an *ad hoc* mechanism that the Facet principle very likely
**subsumes**. Michel caught this. Do not commit these in their local form — re-express
them as Facet/Focus if the sequencing decision keeps them:

- `DisplayTechnology` — proposed new top-level domain entry for `M1_Domains`
  (label deliberately "Display Technology", disambiguated from *display = shop stand*;
  `@id: m1:domain:DisplayTechnology`). Deliberately abstracted **above** implementation
  means so it also covers a **refreshable Braille display** (tactile matrix, no optics).
- `enablingDomains` — proposed **directional** domain property (means → domain),
  to coexist with the flat `relatedDomains`. `applicationDomains` was noted as its *inverse*
  (not a synonym), held in reserve.
- `domainCandidates` / `m1:DomainCandidate` — proposed table + distinct type + distinct IRI
  segment (`m1:candidate:`) so a not-yet-defined domain is registered but **not referenceable**.
  → This is exactly the "candidate vs defined" *facet* — reframe under Facet, don't hand-roll.
- `ElectroMechanics` — surfaced by the Braille case; **not defined** in the registry.
  Parked as a *candidate*, not referenced.

Two **M1_Core candidates** semantically accepted by Michel this session, **NOT graved**
(re-verify the M2 ingredient formulas against `M2_GenericConcepts.jsonld` on HEAD before graving):

- `Sampling = Fm2(Process, Signal, Space)` — discretizes **position** (the resolution axis).
- `Quantization = Fm2(Process, Representation)` — discretizes **value** (the PWM-step axis).
- Both are transverse (hence M1_Core, not a domain extension); orthogonal siblings of
  signal processing. **Do not** create a `Discretization` parent yet (overfitting — wait
  for a second, non-display case).

---

## 4. Pilot poclet — PAUSED

`PwmAntialiasing` (provisional name) — emulating antialiasing on an LED matrix via PWM
(time→intensity→space; per-LED PWM restores the intermediate-intensity primitive that
antialiasing spends to smooth edges). Proposition done (verdict: **valid instance**,
Alignment). Paused at its sync-point: it only awaits its **M1 domain**, which is now
suspended on the Facet sequencing decision below. This poclet is the **concrete pilot case**
that surfaced the Facet convergence — its params: resolution slider (Sampling),
PWM-step slider (Quantization), LED shape square/round (reconstruction filter),
AA on/off, monochrome-on-black channel.

---

## 5. Open gate — Michel's decision (start here)

**Sequencing** (the real blocker; the note leaves it open at §9):

- **(a)** advance an "M1_Domains v1.5" in the current registry style but *Facet-pre-aligned*,
  grave Facet later → risk: double work + vestige at migration.
- **(b)** grave **Facet-M3 first**, then place `DisplayTechnology` directly as a Focus →
  cleaner, but depends on the note's still-open decisions.
- **(c)** recognize "M1_Domains v1.5" ≡ a slice of the Facet / Domain-fusion worksite, and
  make `DisplayTechnology` + the *candidate* status the pilot case that unblocks Facet
  (commis preference — the note says it's the same idea; a "proposed-not-graved" principle
  needs exactly one concrete case).

Then the note's three open decisions (A / B / sequencing) for sign-off.

---

## 6. Recommended first actions on resume

1. Read the **full** Facet note (`_01_Facet_as_M3_Principle_ArchitectureNote.md`) — the three
   open decisions in their exact HEAD wording.
2. Locate on HEAD (verify live vs vestige): `SC-3_Facet_Decision_Record.md` and the
   `M2_DomainFusion_ChangeRequest.md` (+ the planned `m2:appliesToDomains` property) the note
   references at §11.
3. Confirm WS-0 / SC-3 numbering against the worksite map.
4. Present the sequencing choice (a/b/c) to Michel, then A/B, for sign-off. Grave nothing
   before sign-off; run the diagnosis pipeline + SHACL on any M3/M1 edit.

---

## 7. HEAD pointers (verified this session unless marked)

- Facet note — `ontology/docs/_01_Worksite/WS-0/_01_Facet_as_M3_Principle_ArchitectureNote.md`
- Domain registry — `ontology/M1_Domains.jsonld` (+ `ontology/M1_Domains_README.md`);
  entries are `@type m1:Domain`, `@id m1:domain:X`; `m1:ext` present **only** when an
  extension exists (14 of 21 domains have none — domain≠extension is already first-class).
  Note the drift: **Electronics/Physics lack `m1:ext`** though `M1_Electronics/Physics.jsonld` exist.
- M1 core — `ontology/M1_CoreConcepts.jsonld` (combo pattern `Fm2(...)`, `Fm1m2(...)`; base for extensions)
- M2 — `ontology/M2_GenericConcepts.jsonld` (ingredients for the two candidates)
- M3 live — `ontology/M3_GenesisGrammar.jsonld` + `M3_EagleEye/SphinxEye/GrammarFoundation/BicephalousPerspective.jsonld`
- `SC-3_Facet_Decision_Record.md`, `M2_DomainFusion_ChangeRequest.md` — **to locate on HEAD** (from tree/memory; unverified)

---

*Instrument type: HandOver (resumes a worksite). Not a content snapshot — HEAD wins on every
structural fact. Governing skill: `head-over-memory`.*
