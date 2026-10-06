---
name: tscg-m2-candidate-filter
description: >
  Filter skill for evaluating M2 and M1_CoreConcepts candidates — guards against
  Ontological Overfitting (adding one M2 concept per phenomenon instead of composing
  existing ones). Use this skill whenever a session proposes a new M2 GenericConcept
  or M1_CoreConcepts combo, or whenever a concept is described as "missing" from M2.
  Applies three sequential filter tests: Decomposability, Transdisciplinarity, Atomicity.
  Produces a placement decision: M2 / M1_CoreConcepts / M1_Domain / Rejected.
  See also: docs/CoreHypotheses/OntologicalOverfitting.md
---

# TSCG M2 Candidate Filter Skill

Guard against **Ontological Overfitting** when proposing new M2 or M1_CoreConcepts.

**Formal definition**: Ontological Overfitting = m1:ConstraintBalance | _$
applied to m2:Modelisation — adding one M2 concept per observed phenomenon,
sacrificing E (Evolvability) and V (Verifiability) for local R (Representability).

**Load first, by name: `head-over-memory`.** The primitive alphabet, the M2 concept
count, formulas and property names are read from HEAD, never recited from this skill.

**Architectural reminder** before starting (counts: read them at HEAD):
```
M3  — the Base16 primitives    HARD LIMIT
M2  — atomic concepts          GUARDED — this skill is the guard
M1  — unlimited combos         SAFETY VALVE — preferred landing zone
M0  — unlimited instances      OPEN
```

---

## Pipeline Overview

```
CANDIDATE NAMED
      ↓
  STEP 1 — Clarify definition and formula
      ↓
  STEP 2 — Test 1: Decomposability
      ↓ (fails → M1_CoreConcepts)
  STEP 3 — Test 2: Transdisciplinarity
      ↓ (fails → M1_Domain or Reject)
  STEP 4 — Test 3: Atomicity
      ↓ (fails → Reject or reformulate)
  STEP 5 — Placement decision
      ↓
  STEP 6 — Fiche JSON-LD (if admitted)
```

Each step has a **⏸ synchronization point** — wait for Michel's validation
before proceeding.

---

## STEP 1 — Clarify the Candidate

### 1.1 Name and definition

Ask (or propose) a precise definition in domain-neutral language:

```
Name        : <candidate name>
Definition  : <one sentence, no domain-specific vocabulary>
Motivation  : <which phenomenon triggered this proposal?>
Session context : <brief note on the session that produced this candidate>
```

### 1.2 Proposed formula

Attempt a structural grammar formula using ASFID × REVOI | Gs primitives:

```
Proposed formula  : <e.g. A × F × D | _0>
Dimensions used   : <list each and justify>
```

**Check**: Does the formula use only the Base16 primitives (read the alphabet in the
M3 files at HEAD: Gt `×`, Gm `+`, Gs `|`) and their products? `⊗` is forbidden.

### 1.3 Related existing M2 concepts

List the 3-5 most similar existing M2 concepts and their formulas:

```
Related concept 1 : m2:XXX = <formula>  — <how it differs>
Related concept 2 : m2:YYY = <formula>  — <how it differs>
...
```

⏸ **Validate definition and formula with Michel before proceeding.**

---

## STEP 2 — Test 1: Decomposability

> *Can this concept be expressed as Fm2(C1, C2, ...) where C1, C2 are
> existing M2 concepts?*

### 2.1 Decomposition attempt

Try to express the candidate as a GenericConceptCombo:

```
Attempt 1: Fm2(<M2_parent_1>, <M2_parent_2>)
  Shared dimensions  : <list>
  Unique dimensions  : <list>
  Emergent property  : <what the combo produces that neither parent has alone>

Attempt 2: Fm2(<M2_parent_A>, <M2_parent_B>, <M2_parent_C>)
  ...
```

### 2.2 Decomposability verdict

```
IF a clean Fm2 decomposition exists with a genuine emergent property
  → PLACEMENT: M1_CoreConcepts as GenericConceptCombo
  → Formula: Fm2(C1, C2) = <expanded formula>
  → Proceed to STEP 5 (skip Steps 3 and 4)

IF no clean decomposition
  → Proceed to STEP 3
```

**Anti-pattern warning**: If the decomposition feels forced (parents share
no natural dimensions, emergent property is trivial), the candidate may be
poorly defined. Reformulate the definition before continuing.

⏸ **Validate decomposability verdict with Michel.**

---

## STEP 3 — Test 2: Transdisciplinarity

> *Is the concept validated in ≥6 genuinely unrelated domains,
> accessible without domain expertise?*

### 3.1 Domain validation table

For each domain, provide a concrete instance:

```
Domain 1 (Physics/Chemistry)    : <instance name> — <1 sentence>
Domain 2 (Biology/Medicine)     : <instance name> — <1 sentence>
Domain 3 (Social/Economics)     : <instance name> — <1 sentence>
Domain 4 (Computing/Engineering): <instance name> — <1 sentence>
Domain 5 (Arts/Cognition)       : <instance name> — <1 sentence>
Domain 6 (Other)                : <instance name> — <1 sentence>
Domain 7+ (bonus)               : <instance name> — <1 sentence>
```

**Unrelated domains rule**: Physics + Chemistry + Materials + Engineering
counts as 1 domain cluster, not 4. The 6 domains must span at least
4 distinct epistemic families (natural sciences / social sciences /
formal sciences / arts & humanities).

### 3.2 Accessibility test

Can a non-specialist understand the concept from the definition alone,
without domain background?

```
□ Yes — universally accessible → proceed
□ No, requires <domain> expertise → M1_CoreConcepts at most
```

### 3.3 Transdisciplinarity verdict

```
IF < 6 unrelated domains validated
  → PLACEMENT: M1_Domain extension (appropriate domain)
  → Proceed to STEP 5

IF domain expertise required
  → PLACEMENT: M1_CoreConcepts (not M2)
  → Proceed to STEP 5

IF ≥ 6 domains AND universally accessible
  → Proceed to STEP 4
```

⏸ **Validate domain table and verdict with Michel.**

---

## STEP 4 — Test 3: Atomicity

> *Does the concept's formula add at least one genuinely new dimensional
> combination absent from all related M2 concepts?*

### 4.1 Dimensional comparison matrix

Build a comparison table:

```
Dimension  | Candidate | Related_1 | Related_2 | Related_3
-----------+-----------+-----------+-----------+-----------
A          |     ✓     |     ✓     |           |     ✓
S          |           |     ✓     |     ✓     |
F          |     ✓     |     ✓     |     ✓     |     ✓
I          |     ✓     |           |     ✓     |
D          |     ✓     |           |           |     ✓
_0         |     ✓     |           |           |
```

### 4.2 Unique dimensional combination

Identify what the candidate adds that no existing M2 concept has:

```
Unique combination : <e.g. "A × F × D | _0 — no existing M2 encodes
                      3-state topology with qualitative central optimum">
Absent from        : <list related concepts and why they don't capture it>
```

### 4.3 Atomicity verdict

```
IF formula is a recombination of dimensions already present in related M2
  → Not atomic — REJECT or reformulate
  → Consider: is there a more fundamental concept to be extracted?

IF formula introduces genuinely new dimensional combination
  → Atomic — ADMIT to M2
  → Proceed to STEP 5
```

**Special case — Stereopsic concepts**: If the candidate is functionally
stereopsic (its purpose IS the Territory→Map traversal, like m2:Modelisation),
document this explicitly. Functional stereopsic nature is an additional
admission criterion.

⏸ **Validate atomicity verdict and placement with Michel.**

---

## STEP 5 — Placement Decision

### Decision matrix

```
Test 1 (Decomposable)  | Test 2 (Transdisciplinary) | Test 3 (Atomic) | Placement
-----------------------+---------------------------+-----------------+------------------
YES (clean Fm2)        | —                         | —               | M1_CoreConcepts
NO                     | < 6 domains               | —               | M1_Domain
NO                     | Requires expertise        | —               | M1_CoreConcepts
NO                     | ≥ 6 domains, accessible   | NO (reducible)  | Reject / Reformulate
NO                     | ≥ 6 domains, accessible   | YES (new combo) | M2 ✓
```

### Placement summary card

```
Candidate       : <name>
Final placement : <M2 / M1_CoreConcepts / M1_Domain:<domain> / Rejected>
Formula         : <structural grammar formula>
Rationale       : <1-2 sentences>
Session date    : <YYYY-MM-DD>
```

⏸ **Final validation with Michel before generating JSON-LD.**

---

## STEP 6 — JSON-LD Fiche

> **Vocabulary rule (WS-1, ZERO NEW BARE KEYS).** The templates below show the
> property NAMES in use at HEAD (checked 2026-10-06), not a licence to copy their
> nested sub-fields. Existing M2/M1 nodes carry unprefixed sub-keys
> (`vs_<X>`, `validated`, `actualDomains`, `domains`, `formula`, `contribution`…):
> they are bare keys, dropped on JSON-LD expansion — frozen debt owned by WS-1, not a
> pattern. Before writing a fiche:
> 1. check every property at HEAD in a neighbouring node (do not trust this list);
> 2. for a nested sub-field, use a declared term (standard term from the apex, or a
>    TSCG term that exists at HEAD); if none exists, **stop and ask Michel** — never
>    invent a bare key, never copy one;
> 3. after the edit, the gate's D1 count for the layer must not rise
>    (`cd ontology/toolchain && python run_all_layers.py`; the validator
>    `validator/tscg_validator.py --layers M2 --doc` shows the D1 findings).
>
> Write IRIs as IRIs: `{"@id": "m2:X"}`, never the string `"m2:X"`.

### 6.1 If M2 — add to M2_GenericConcepts.jsonld

Minimum required fields:

```json
{
  "@id": "m2:<ConceptName>",
  "@type": "owl:Class",
  "rdfs:subClassOf": {"@id": "m2:GenericConcept"},
  "rdfs:label": "<ConceptName>",
  "rdfs:comment": "<definition, distinctions from related concepts>",
  "m2:hasFamily": "m2:<Family>",
  "m2:hasStructuralGrammarFormula": "<formula>",
  "m2:isStereopsic": <true|false>,
  "m2:hasPolarity": "<neutral|dual|ternary>",
  "m2:perspective": "<territory|map|dual>",
  "m2:distinctFrom": "<distinctions — sub-keys only with declared terms, see the rule above>",
  "m2:transdisciplinaryValidation": "<same rule: no bare sub-keys>",
  "m2:hasExample": ["<domain> — <instance>", "..."],
  "dcterms:created": "<YYYY-MM-DD>",
  "dcterms:creator": "Echopraxium with the collaboration of Claude AI"
}
```

Update ontology node:
- `owl:versionInfo` → bump minor version
- `m3:changelog` → add an entry `{owl:versionInfo, dcterms:date, adms:versionNotes}`
  (the ONLY changelog, decision D5(a); retention 3). `m2:changelog` is forbidden.
- `m2:progress` counters (if still present at HEAD)

### 6.2 If M1_CoreConcepts — add to M1_CoreConcepts.jsonld

Minimum required fields:

```json
{
  "@id": "m1:<ConceptName>",
  "@type": ["owl:Class", "m2:GenericConceptCombo"],
  "rdfs:subClassOf": {"@id": "m2:GenericConceptCombo"},
  "rdfs:label": "<ConceptName>",
  "rdfs:comment": "<definition>",
  "m1:comboOf": [{"@id": "m2:<Parent1>"}, {"@id": "m2:<Parent2>"}],
  "m1:structuralGrammarFormula": "Fm2(<Parent1>, <Parent2>)",
  "m1:parentGenericConcepts": [{"@id": "m2:<Parent1>"}, {"@id": "m2:<Parent2>"}],
  "m1:emergentProperty": "<what the combo produces that parents don't>",
  "m1:transdisciplinaryValidation": "<no bare sub-keys, see the rule above>",
  "dcterms:created": "<YYYY-MM-DD>",
  "dcterms:creator": "Echopraxium with the collaboration of Claude AI"
}
```

Update ontology node:
- `owl:versionInfo` → bump minor version
- `m3:changelog` → add an entry `{owl:versionInfo, dcterms:date, adms:versionNotes}`
  (retention 3). Never `m2:changelog`, never a new `m1:changelog` entry (legacy, D5).
- `m1:validationStatus` counters

The M1 combo formula is a function signature (`Fm2(...)`, SC-1): no monoidal operator
inside, and no `…FormulaExpanded` property (it does not exist at HEAD).

Then validate (`tscg-ontology-diagnosis-pipeline`, Phase 3): the gate must PASS, or a
moved count is shown to Michel before any `--update-golden`.

---

## Quick Reference — Warning Signs of Ontological Overfitting

```
⚠  Proposed immediately after observing ONE specific phenomenon
⚠  Validated in < 4 distinct epistemic families
⚠  Formula = recombination of dimensions in a single related concept
⚠  Definition requires domain vocabulary
⚠  "This is like m2:XXX but more specific" → likely M1, not M2
⚠  Proposed to model a domain law (Fick, Fourier, Newton) → M1_Domain
⚠  No emergent property — combo adds nothing to its parts
```

## Quick Reference — Healthy M2 Addition Signs

```
✓  Validated in ≥ 6 genuinely unrelated epistemic domains
✓  Definition is domain-neutral and immediately understood
✓  Formula introduces a dimensional combination absent from all neighbors
✓  Concept enables modelling of phenomena not yet in M0 corpus
✓  Stereopsic nature is constitutive, not incidental
✓  Emerged from comparison of MULTIPLE phenomena, not one
✓  M1 decomposition was attempted and failed cleanly
```

---

## Session Log Format

At the end of each candidate evaluation session, produce a log entry:

```markdown
## Filter Session — <YYYY-MM-DD>

**Context**: <topic that triggered the analysis>

| Candidate | Test 1 | Test 2 | Test 3 | Placement | Notes |
|---|---|---|---|---|---|
| m2:XXX | PASS | PASS | PASS | M2 ✓ | |
| m1:YYY | FAIL (Fm2) | — | — | M1_Core | Fm2(A,B) |
| m2:ZZZ | PASS | FAIL (<4) | — | M1_Domain | Only in physics |
| Rejected | PASS | PASS | FAIL | Rejected | Reduces to m2:W |

**M2 net change**: +N atomic, +M combos migrated
**Anti-Overfitting ratio**: <rejected+M1> / <total candidates> = X%
```

### Example — Session 2026-06-23 (transport phenomena)

```markdown
## Filter Session — 2026-06-23

**Context**: Transport phenomena (viscosity/conductivity/diffusion) +
  capillarity/permeability + Ontological Overfitting identification

| Candidate | Test 1 | Test 2 | Test 3 | Placement | Notes |
|---|---|---|---|---|---|
| EntropicDrive | — | — | — | Rejected | Causal loop confusion |
| SpontaneousEquilibration | FAIL | — | — | Rejected | = Convergence+Balance |
| Cohesion | FAIL | — | — | Rejected | Reduces to Resilience |
| Permeability | FAIL→M1 | ≥7 | — | M1_Core | Fm2(Channel,Interface,Gradient) |
| TopologicalDefect | FAIL | — | — | M1_Core (migrated from M2) | Too specialized |
| TriadicBalance | PASS | ≥7 | PASS | M2 ✓ | _0=_^|_$ as DerivedGsElement |
| Modelisation | PASS | ≥7 | PASS | M2 ✓ | Functionally stereopsic |

**M2 net change**: +2 atomic (TriadicBalance, Modelisation), -1 combo (TopologicalDefect migrated)
**Anti-Overfitting ratio**: 5/7 = 71% — healthy filtering
```

---

*Skill version: 1.1.0 — 2026-10-06 (aligned with HEAD: m3:changelog per D5(a); IRIs as
`{"@id"}`; zero new bare keys; nonexistent `m1:structuralGrammarFormulaExpanded` removed;
counts and alphabet read from HEAD; loads head-over-memory).*
*1.0.0 — 2026-06-23*
*Author: Echopraxium with the collaboration of Claude AI*
*Generated from transport phenomena analysis session*
