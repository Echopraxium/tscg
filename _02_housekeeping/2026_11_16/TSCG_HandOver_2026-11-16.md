# TSCG HandOver — 2026-11-16: stereopsic vocabulary, Odin's Wisdom, next lot "bicephalous" in the ontologies

**Date**: 2026-11-16 · **Author**: Echopraxium with the collaboration of Claude AI
**Kind**: HandOver (Smart Prompt v17 §4). It only loads and points; it holds no authoritative
framework content. It follows `_02_housekeeping/2026_11_15/TSCG_HandOver_2026-11-15_evening.md`
(WS-15 / WS-16), which stays valid.

---

## 1. Load first — by name

- **`head-over-memory`**: every verifiable fact below is a *pointer to check at HEAD*.
- **`tscg-ontology-diagnosis-pipeline`**: the next lot changes ontology files (Scenario 1,
  renaming; reasoner on every changed file).

Then read at HEAD:
1. `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` — the Gs paragraph (three
   vocabularies; Odin; who evaluates).
2. `ontology/M3_OdinsWisdom_README.md` — §Role and "Why Odin's Wisdom — the observer".
3. `ontology/docs/_01_Worksite/WS-15/worksite.yaml` — state of the scoring retirement.
4. `ontology/docs/_02_EpistemicReview/MockupValidation_Heuristics_Draft.md` §7 — the
   human/AI duo.

---

## 2. Session state (perishable — verify, do not trust)

- The 2026-11-15/16 commits are pushed. *Check with `git log --oneline -12`*: the
  latest should be "Odin is a second-order map, not an observer", above "Two obsolete
  \"bicephalous\" documents deleted", "M3_OdinsWisdom README §Role…", "WS-15: SF-5 and
  SF-6 state updated…", the heuristics draft 0.3.0, the Odin's Wisdom README section,
  the Bootstrap paragraph, "\"bicephalous\" -> \"stereopsic\"…", the README/Narcissus
  rewrite and "CoreHypotheses §4 retired…".
- Every lot of the day: `GATE: PASS`, `PATH_CHECK: 0 finding(s)` on Michel's machine.
  Docs only: no reasoner run was needed.
- Commit identity (repo rule, `CLAUDE.md` §5): author Echopraxium, no Claude trailer.

---

## 3. What Michel decided (non-verifiable)

- **CoreHypotheses §4 deleted** (ScoringSystem, MultisubjectiveScoreEvaluationProtocol,
  CredibilityAccretion_Process). Root README and Narcissus §2 rewritten in his words
  (D18 answered); the author's star self-assessment deleted.
- **"bicephalous" → "stereopsic" everywhere except dated archives.** Done in the live
  text (docs, code, skills); two obsolete documents deleted; the SPARQL query renamed
  `FindStereopsicComponents.sparql`.
- **One meaning, three vocabularies**: monoidal **Gs**, epistemological **Stereopsis /
  stereopsic**, metaphoric **Odin's Wisdom**. Rule applied to the replaced text:
  monoid / alphabet / primitives / `|` formulas → Gs; metaphor → Odin's Wisdom;
  otherwise stereopsic. The label stays **epistemological** (not "cybernetic"); the
  epistemological vocabulary is close to second-order cybernetics.
- **Odin**: one Stereopsis (Gs) is the instrument; inside the model Odin is a
  **second-order map** (a map that holds the place of the observer), acting as a
  co-driver / guide (locates, reads the Map, raises warnings), never an evaluator; the
  **second-order observer proper is the human** outside the model, who decides and
  evaluates. Gs is not a feedback loop (Φ observation, Ψ interpretation).
- **Human/AI duo**: the AI plays Odin's role in practice (a lead for the heuristics,
  draft §7; Q9 open).

---

## 4. Next lot — "bicephalous" in the ontologies and M0 instances

Inventory (run it, do not trust a count written here):

```
git grep -n -i bicephal -- '*.jsonld' '*.ttl' ':(exclude)ontology/Ref/*' ':(exclude)*backups*'
```

Triage each occurrence with Michel:
1. **Prose** (`rdfs:comment`, descriptions, notes) → stereopsic, with the three-vocabulary
   rule of §3.
2. **Keep**: changelog entries (`adms:versionNotes`), the names of things that existed
   (`M3_BicephalousPerspective`, prefix `m3:bicephalous:`, `M3_GenesisSpace`).
3. **Keys / identifiers** (`m2:bicephalousArchitecture`, `bicephalousAnalysis`,
   `triz:bicephalousNature`, `phaseTransition:bicephalousBalance`…): Michel decides per
   key — **rename** (Scenario 1: G8 and D1 must not rise; every user of the key renamed
   with it) or **delete with WS-15 SF-2** when the key holds scores
   (e.g. `REVOI=0.84`). A renamed key keeps its declaration and comment.
4. Reasoner on every changed file (Java 25: see the pipeline skill), and the M0 sweep
   `run_all_layers.py --reasoner` if M0 files change.

Also left for later: `index.html` (generated gallery, regenerate with the producers lot
SF-4); the other WS-15 lots (see its worksite.yaml).

---

## 5. Small items

- **Skills to re-save in Michel's account** from the repo copies changed on 2026-11-16:
  `tscg-article-pipeline`, `tscg-tensor-to-structural-grammar-migration` (incl.
  `references/Structural_Grammar_Foundation.md`).
- Priorities of WS-15 and WS-16 still open.
- Possible formal anchor for Odin as "geolocator": the Gs primitive L (Localizability) —
  Michel's call, not written anywhere yet.

---

## 6. Guardrails

- **Michel decides** wording, modelling and per-key fate; Claude brings inventory,
  impact, patches (`git am`, one mbox when several); Claude never pushes.
- **Debt honesty**: a counter falls only when the defect disappears.
- **Archives untouched**: dated records keep the words they recorded.
- **No count recited**: every number comes from a command run in the session.
