# HandOver — TSCG, FeedbackLoop to the M0 reasoner sweep (2026-11-08 → 09)

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: resume in a fresh conversation. HEAD is the only authority: re-read every
fact below from the repository before relying on it. Supersedes the HandOver of
2026-11-07 (Kit frictions) for everything listed here.

## 1. State of `main` (all pushed, HEAD `5423635`)

| Commit (title) | Content |
|---|---|
| M2: Adaptation dcterms:requires FeedbackLoop | M2 16.37.0; `dcterms:requires` declared in the apex (M3_GrammarFoundation 2.17.0) |
| M1: Hysteresis = Fm2(Threshold, Memory) | M1_CoreConcepts 2.25.0; M0_Thermostat 1.1.0 typed `m1:Hysteresis`; gap G2 closed |
| M0_Common 1.7.0 / Thermostat 1.2.0 | `owl:oneOf` as `{"@list": …}` (root cause of every M0 inconsistency); Thermostat scores coerced to xsd:float |
| M0 reasoner campaign | 23 instance files; 41/43 consistent; gate C09 −6, C15 −3, C12 −1 (golden updated) |
| Fm2 notation (D11 resolved) | `grammars/Fm2_notation.ebnf` + `fm2_notation.py`; check_M1 1.9.0 (GCC011/012/013); M1 SHACL 1.9.0 (SHAPE 9 reads blocks, NEW SHAPE 14); M1 2.26.0; apex 2.18.0; Functional_Grammar_Model 2.2.0 §13; GCC009 5 → 1, M1 SHACL 294 → 280 |
| Gate 1.7.0 | `run_all_layers.py --reasoner`: OWL reasoner on all M0, golden section `M0_REASONER` (2/43 not PASSED, names frozen) |
| Skill 1.4.0 (repo copy) | `tscg-ontology-diagnosis-pipeline` 1.4.0 also saved on the account |

Reasoner results confirmed by Michel on his machine for every lot.

## 2. Decisions taken by Michel

- **FeedbackLoop is atomic, stays in M2** (a primitive of cybernetics). SC-8 is reframed:
  reformulate its formula, do NOT migrate it to M1. Its current formula
  (`Process × Alignment × Homeostasis`) is still wrong (circular via Homeostasis, unsigned).
- **Adaptation stays in M2.** Adaptation *requires* a feedback loop (the loop is a means,
  not a part): `m2:Adaptation dcterms:requires m2:FeedbackLoop` — a necessary-condition
  link, never a factor inside a formula.
- **Hysteresis = `Fm2(Threshold, Memory)`**, dual polarity, no restriction on Threshold
  (its value `threshold_behavior: Hysteretic` already means "memory effect": counting it
  twice would presuppose the result).
- **Argument block notation** (OOP-inspired), attached to the argument it follows:
  `Arg { properties: [name: value, final: true|false], constraints: [expr, …] }`;
  absent `final` = `false` = a default value; several properties = a list of tuples;
  in a constraint `F` = dimension of the carrying argument, `Other.F` = of another one.
  LALI's constraint is carried by Regulation.
- **One grammar, many tools**: the EBNF is the single source ("ontology compiler").
- Instrument before reducing: the M0 reasoner enters the gate (`--reasoner`).

## 3. Open questions (not decided)

- **FeedbackLoop formula** (closure of SC-8): an atomic formula that encodes causal
  closure; `It × F × D` rejected (it is Adaptation's formula).
- **G3**: relaxation oscillator = `Fm2(Hysteresis, FeedbackLoop)`? (to pass the filter;
  maybe the way to found Oscillator without a restriction).
- Regulation and Homeostasis share `A × St × F` (Homeostasis only adds `| L`): debt noted.
- Addendum A: AQ1–AQ3 (Interface).
- M1 has no declared polarity property (`m1:hasPolarity` is a phantom): Hysteresis states
  its dual polarity in `rdfs:comment`.

## 4. Debt found and recorded (Debt Overview 1.20.0 §5)

- 22 M0 instances bind `m0:` to their own namespace (= check_m0 C02, frozen at 22).
- `M0_Bmc`: score predicates reused with text justifications (FAILED).
- `M0_Yggdrasil`: string `rdfs:range`, double-colon names (ERROR; S5-3).
- `m0:epistemicGap` holds an object in 9 instances (xsd:float property).
- `m2:possibleValues` stores values under a bare key `value` (WS-1): blocks the structured
  RDF form of the Fm2 signature (so the meaning checks read raw JSON for now).
- `m1:Processor` keeps `| V + R` (monoidal suffix, SC-6).

## 5. In progress — Kit ergonomics (mock-up shown, awaiting Michel's OK)

Transport bar of every workshop (`kit/lib/app.js`, `tscg-kit.css`, `i18n.js`):
fast-rewind / fast-forward icons instead of ▼ ▲; a space between "Lancer" and the speed
control; label "Vitesse 100 %" (percent of `S.speed`, steps 25…1600 %, 100 % default);
the old "ralenti ×4" ratio moves to the tooltip. Then: the Thermostat page in
`instances/poclets/Thermostat/static/` must be rebuilt from the Kit.

## 6. Next steps (proposed order)

1. Kit ergonomics lot (above), after the mock-up is validated.
2. FeedbackLoop formula (SC-8), then G3.
3. Namespace lot for the 22 misbound `m0:` (WS-1 / WS-10).
4. Kit: composite blocks + workshop "inside the thermostat"; WS-13 L1a (Boundary).

## 7. Working notes

- Delivery: git patches (`git am`), verified on `origin/main` before sending.
- Reasoner in the VM: Java 25 from GitHub releases (recipe in the skill 1.4.0); baseline
  at HEAD before blaming a lot; `pellet explain` for the minimal explanation.
- `tscg_validator.py` reads HEAD by default: use `--source local` for the working copy.
- Gate moves are shown to Michel before any `--update-golden`.
