# HandOver — TSCG Kit and Layer Cake frictions (2026-11-07)

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: resume in a fresh conversation. HEAD is the only authority: re-read every
fact below from the repository before relying on it.

## 1. State of `main` (all pushed)

| Commit (title) | Content |
|---|---|
| Kit 0.5.0 → 0.9.2 | four workshops (Thermostat, Larsen, Drinking bird, Sunflower); map of scenarios as home page; dark theme; icons; flow chevrons; triangle connectors; Synoptic zoom; toolbar (clear all, erase, snap); top row tutorial + Maquette/Courbes tabs, bottom row Synoptique/Panneau; time axis in s/min/h/days with midnight lines; scale model fills its compartment |
| WS-13 Phase 0 Addendum A | `m1:Interface = Fm2(Boundary, Mediator, Code)`; `m2:Interoperability` removed (not renamed); Boundary defined first; AQ1–AQ3 open. Change request only: no ontology file modified |
| Thermostat poclet | first Kit workshop through the instance pipeline: `instances/poclets/Thermostat/` (M0 JSON-LD 1.0.0, README, analysis, page in `static/`, sources in `static/src/`); Kit = test airlock; gallery regenerated; Compendium build re-bundles Kit pages of poclets |
| Gate golden | M0 files 42 → 43, everything else unchanged; GATE PASS |

## 2. Design document (Claude Doc)

"TSCG Kit — Articulation des scénarios" (claude.ai artifact GaFMpADk37oodYad6EMiJH):
map of scenarios (F1 pivot; lateral: Larsen, Drinking bird, Sunflower; vertical:
house = zoom out, inside of the thermostat = zoom in), anatomy of an articulation,
layer correspondence, delivery plan, and the **friction log** (gaps found by building
scale models, with anti-overfitting rules).

## 3. Decisions taken by Michel (this conversation)

- Map/Territory is never stated in the Kit: the player rediscovers it.
- An M0 object can be an instance of an M2 or an M1 class.
- An M1 combo may take another M1 combo as argument (regulation of Layer Cake
  overcrowding) — already rule SC-1 at HEAD.
- High priority: no monoidal type inside `Fm2` / `Fm1m2` (would short-circuit M3 → M1);
  already enforced by M1 SHACL SHAPE 9.
- Interface = `Fm2(Boundary, Mediator, Code)` (Addendum A).
- Kits validated by the pipeline move to `instances/poclets/<Name>/` (page in `static/`);
  the Kit catalogue page stays in `kit/`.

## 4. Open questions (not decided)

- Addendum A: AQ1 (Mediator's "third party" wording), AQ2 (where REVOI V+E of
  Interoperability go), AQ3 (Permeability: `Fm2(Boundary, Channel, Gradient)` or
  `Fm2(Interface, Gradient)`).
- Thermostat gaps: G1 Boundary undefined; G2 Hysteresis candidate
  `Fm2(Threshold, Memory)`; G3 `m1:Oscillator` is harmonic, the sawtooth is relaxation.
- Michel's latest idea: Adaptability = `Fm2(FeedbackLoop, Process)`, Tropism derived
  from Adaptability. Claude's counter-proposal (to discuss): with SC-8
  (`m1:FeedbackLoop = Fm2(Process, Alignment)`) Process would appear twice;
  Adaptability = `Fm2(FeedbackLoop, Adaptation)`; Tropism = `Fm2(FeedbackLoop, Gradient)`
  (the Sunflower workshop: tracking needs no learning; anticipation is the adaptive layer).
- FeedbackLoop formula written with concept names (SC-8 reclassification, todo).

## 5. Next steps (proposed order)

1. Decide the open questions above (one at a time).
2. Kit: composite blocks + workshop "inside the thermostat" (zoom in).
3. WS-13 L1a (define Boundary) before the house workshop (zoom out, Frontière block).
4. Pass Larsen, Drinking bird and Sunflower through the instance pipeline.

## 6. Working notes

- Delivery: git patches (`git am`), verified on `origin/main`; tests are headless
  Playwright scripts (kept in the session scratchpad, not in the repo).
- New M0 instances: declare local `m0.<id>:*` predicates in the file
  (`owl:AnnotationProperty`), otherwise the gate's G8 counts phantom predicates;
  show the moved gate counts to Michel before `--update-golden`.
