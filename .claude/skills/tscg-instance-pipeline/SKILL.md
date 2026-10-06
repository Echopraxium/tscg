---
name: tscg-instance-pipeline
description: >
  Complete pipeline for creating a TSCG Instance in 4 sequential steps: Proposition,
  Analysis, Modeling, and Simulation. Use this skill whenever the user mentions
  an instance, wants to model a system with TSCG, wants to create an M0 JSON-LD ontology,
  or proposes a system/process to analyze through the TSCG lens (ASFID/REVOI dimensions,
  M2 GenericConcepts, M1 extensions). Also applicable when the user asks "what do you
  think?" about a known system, or requests an HTML/Electron simulation of a TSCG system.
  Do NOT use for Case Studies or Real World Systems (too complex) — this pipeline is
  reserved for Instances.
version: 2.2.1
---

<!-- v2.2.1 (2026-10-06) — requirement line: python -m pip install -r ontology/toolchain/requirements.txt. -->
<!-- v2.2.0 (2026-10-01) — Vocabulary hygiene (WS-1). ZERO BARE KEYS rule + mandatory
     bare-key check before delivery (3.3, 3.5); @context example no longer shows
     colon-named terms (CTX-5) — local namespace m0.<instanceId>: (WS-10); m2:changelog
     -> m3:changelog with {owl:versionInfo, dcterms:date, adms:versionNotes};
     owl:imports written as IRIs; SHACL schema path corrected (the TSCG_InstanceGrammar
     copy was removed); check_m0_instances.py added; FireTriangle flagged as a STRUCTURE
     reference only (it carries bare keys, WS-9 AP-1). Loads head-over-memory. -->
<!-- v2.1.1 (2026-08-16) — Fixes on top of v2.1.0:
     path `ontology/TSCG_Grammar/` → `ontology/TSCG_InstanceGrammar/` (old path 404'd)  ·
     corrected self-contradictory dead-vestige line (dead = M3_GenesisSpace, live = M3_GenesisGrammar). -->
<!-- v2.1.0 (2026-08-13) — Notation-reform pass:
     ⊗ → × / + / |  ·  M3_GenesisSpace → M3_GenesisGrammar  ·
     KnowledgeFieldConceptCombo → DomainConceptCombo  ·  echopraxium → Echopraxium  ·
     verified example formulas from HEAD  ·  @context pointer to FireTriangle.
     Structural logic unchanged. -->


# TSCG Instance Pipeline

4-step pipeline for creating a complete TSCG Instance:
**Proposition → Analysis → Modeling → Simulation**

Each step may contain **human synchronization points** (⏸) that suspend
the pipeline until Michel's explicit decision to continue.

**Load first, by name: `head-over-memory`.** Every file path, formula, type name,
version or count used below is read from HEAD, never recited.

> **Notation (current — reformed 2026-08-13).** Structural grammar formulas use
> three operators only: `×` (Territory / ASFID, monoid **Gt**), `+` (Map / REVOI,
> monoid **Gm**), `|` (Stereopsis, monoid **Gs**). The operator **`⊗` is
> forbidden** (superseded 2026-07-06). Atom subscripts disambiguate: `St`/`Ss`
> (Structure vs Symbol), `It`/`Im` (Information vs Interoperability); `A`/`F`/`D`
> stay bare. The live M3 file is **`M3_GenesisGrammar.jsonld`** (the old
> `M3_GenesisSpace.jsonld` is a dead vestige — do not reference it). M1 combos are
> **`DomainConceptCombo`** (ex-`KnowledgeFieldConceptCombo`). Always verify any
> formula, type name or version against **HEAD**, never from memory.

> **Vocabulary rule (WS-1, 2026-10-01) — ZERO BARE KEYS.** A *bare key* is a JSON key
> declared in no `@context` and carrying no prefix. JSON-LD silently DROPS it on
> expansion: the file still opens and feeds the simulation, but that content never
> reaches the RDF graph, so no reasoner and no SHACL shape can see it — and nothing
> reports an error. Previous generations of this pipeline produced thousands of them
> (measured 2026-10-01: 6604 in the 43 M0 instances, 3418 in the canonical corpus).
> Every key you write — **at every nesting depth** — must be one of:
> 1. a standard term declared in the apex `M3_GrammarFoundation` (`rdfs:`, `owl:`,
>    `dcterms:`, `skos:`, `adms:`, `schema:` — see its node
>    `m3:grammar_foundation:ExternalVocabularyPolicy`);
> 2. a TSCG term of the right layer (`m0:` = `M0_Common.jsonld#`, `m1:`, `m2:`, `m3:`),
>    checked at HEAD to exist;
> 3. a **local instance term** under the instance's own prefix `m0.<instanceId>:`
>    (dot form, WS-10 convention) — for sections and sub-fields specific to this
>    instance.
>
> Never invent a bare key "for documentation". If a field has no home, stop and ask
> Michel (duo mode). The check of 3.5 must report 0 before delivery.

---

## GitHub References (raw URLs)

Base: `https://raw.githubusercontent.com/Echopraxium/tscg/main/`

**Ontology:**
- `ontology/M3_GrammarFoundation.jsonld` — apex: external vocabulary declarations and policy
- `ontology/M3_GenesisGrammar.jsonld` — M3 structural grammar (aggregator)
- `ontology/M3_EagleEye.jsonld` — ASFID dimensions
- `ontology/M3_SphinxEye.jsonld` — REVOI dimensions
- `ontology/M2_GenericConcepts.jsonld` — GenericConcepts (count them at HEAD)
- `ontology/M1_CoreConcepts.jsonld` — core concepts
- `ontology/M1_extensions/chemistry/M1_Chemistry.jsonld` — domain extension example
- `ontology/M0_Common.jsonld` — shared M0 vocabulary (`m0:` scores, gap, …)

**Reference instances (2026-10-01 — re-measure with the 3.5 bare-key check):**
- **Structure reference** (sections, README, simulation):
  `instances/poclets/FireTriangle/M0_FireTriangle.jsonld` + `_README.md`.
  ⚠ Do NOT copy its vocabulary: its top-level sections are correctly prefixed
  (`m0.fireTriangle:…`) but their sub-fields are bare keys (262), and its `@context`
  carries archaeological colon-named terms (scheduled re-evaluation: WS-9 AP-1).
- **Vocabulary reference**: `instances/poclets/QRCodeToPocketCity/M0_QRCodeToPocketCity.jsonld`
  — the only instance with 0 bare keys at that date (every key prefixed).

**Other existing instances (for comparison):** list them from HEAD
(`instances/poclets/`, `instances/systemic-frameworks/`,
`instances/symbolic-system-grammars/`, `instances/tscg-tools/`).

**Reference documentation:**
- `docs/reboot-kit/M2_FormulasReference_v15.10.0.md` (verify against M2 at HEAD)
- `docs/reboot-kit/SmartPrompts/`

**Validation (single source of truth for the M0 SHACL schema):**
- `ontology/toolchain/check-M0/M0_Instances_Schema_shacl.ttl` — M0 SHACL schema
- `ontology/TSCG_InstanceGrammar/validate_m0_instance.py` — single-file SHACL validation
  (uses the schema above)
- `ontology/toolchain/check-M0/check_m0_instances.py` — full M0 checker (C01–C15),
  `--instance NAME` for one instance
- `ontology/toolchain/run_all_layers.py` — the acceptance gate (exact reference values)

**This skill (source of truth in repo):**
- `.claude/skills/tscg-instance-pipeline/SKILL.md`

---

## Step 1 — PROPOSITION

### Expected Input from Michel
1. **System name** (e.g., "Color Synthesis", "Fire Triangle")
2. **Brief description + examples** (few sentences, often pre-generated with DeepSeek)
3. **Diagnostic request** (e.g., "what do you think?")

### Expected Response: TSCG Feasibility Diagnostic

Produce a **dual evaluation**:

**A. TSCG Lens**
- Which ASFID dimensions are active? (A/S/F/I/D)
- Which M2 GenericConcepts seem relevant a priori?
- Is the system well-bounded (minimal + complete)?

**B. Experience Perspective**
- Comparison with existing instances (similarities, close domain)
- Anticipated difficulties
- Estimated richness (number of mobilizable GenericConcepts)

### System Classification — MANDATORY DECISION

| Verdict | Criterion | Next Step |
|---------|-----------|-----------|
| 🟡 **Too trivial** | Too few active dimensions, no dynamics, no feedback | ⏸ Stop with explanation |
| 🟢 **Valid instance** | Appropriate complexity, modelable in minimal complete JSON-LD | → Continue to Step 2 |
| 🔵 **Too complex** | LLM, Microprocessor, Mitochondria… → requires different pipeline | ⏸ Stop with orientation |

> If the system is "borderline", propose a reduced scope to make it
> a valid instance (e.g., "simple chemical synapse" instead of "the brain").

⏸ **Sync point if verdict ≠ Valid instance** — wait for Michel's decision.

---

## Step 2 — ANALYSIS

### Objective
Assess the alignment between the proposed system and the TSCG framework.
This is an **epistemic act**, not just a technical verification.

### Three Possible Outcomes

| Result | Description | Behavior |
|--------|-------------|----------|
| ✅ **Alignment** | System models well with existing metaconcepts and dimensions | Continue to Step 3 |
| ⚠️ **Gap** | Modeling reveals a "hole" in the framework | ⏸ Document + discuss with Michel |
| 🔬 **Refutation (Popper)** | System challenges a TSCG axiom or principle | ⏸ Explain, justify in detail |

> A Gap or Refutation has **positive value**: it contributes to TSCG's evolution.
> Refutation has maximum value — it forces framework strengthening or revision.

### Output: `analysis.md`

File structure:
```
# TSCG Analysis — [System Name]

## Verdict: [Alignment | Gap | Refutation]

## ASFID Lens
- A (Attractor): ...
- S (Structure): ...
- F (Flow): ...
- I (Information): ...
- D (Dynamics): ...

## Anticipated M2 GenericConcepts
- [Name] ([structural grammar formula]) — anticipated role

## Comparison with existing instances
- [Similar instance]: [similarities / differences]

## Detailed Verdict
[If Gap: precise description of identified hole]
[If Refutation: complete Popperian argument + justification]

## Recommended Decision
[Continue | Discuss | Revise scope]
```

⏸ **Sync point if Gap or Refutation** — wait for Michel's decision before continuing.

---

## Step 3 — MODELING

### Internal Pipeline (sequential sub-steps)

#### 3.1 — M2 Identification (GenericConcepts)
- List relevant **existing GenericConcepts** with their structural grammar formula
  (e.g., `Process = D × F`, `Trigger = D × It`, `Balance = A × St × F | _0`) —
  verify each against `M2_GenericConcepts.jsonld` at HEAD; do not recite from memory
- Identify **new candidates** if a necessary concept doesn't exist yet
- Response format for new candidate:
  ```
  🆕 M2 Candidate: [Name]
  Structural grammar formula: [e.g., St × It]   # × Gt · + Gm · | Gs  (never ⊗)
  Role: [description]
  Status: "Proposal — to be validated"
  ```

#### 3.2 — M1 Identification (DomainConceptCombos)
- List used DomainConceptCombos (e.g., `m1:chemistry:Combustion`)
- Identify **new M1 candidates** if necessary
- Identify if a **new M1 extension** is required or if an existing extension
  should be enriched (e.g., new class in `M1_Chemistry.jsonld`)
- If a candidate is written into an M1 / M2 file, it follows the same zero-bare-key
  rule, and the canonical VOC gauge must not rise (see 3.5).

#### 3.3 — M0 JSON-LD Generation

Follow the FireTriangle pattern for the **structure** (sections, order), and the
**Vocabulary rule** above for every key.

**`@context` — build it from this shape, verify every IRI at HEAD.** Do not copy an
existing instance's `@context` blindly: most still carry colon-named terms (e.g.
QRCodeToPocketCity, otherwise clean, has `m3:eagle_eye`, `m3:sphinx_eye`,
`m1.ext:electronics`). Required shape:

```json
{
  "@context": {
    "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
    "m0": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Common.jsonld#",
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#",
    "dcterms": "http://purl.org/dc/terms/",
    "adms": "http://www.w3.org/ns/adms#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "m0.<instanceId>": "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/<type>/<InstanceName>/M0_<InstanceName>.jsonld#"
  }
}
```

- All prefixes **absolute**; `m0:` always resolves to `M0_Common.jsonld#` (WS-10).
- **No term name containing `:`** in the `@context` (CTX-5: `m1:core`, `m0:instance`,
  `m3:eagle_eye`, `m1.ext:<domain>`… — strict JSON-LD processors reject some of them,
  and `m3:eagle_eye` points to the wrong IRI). Local terms use the dot-form prefix
  `m0.<instanceId>`.
- **M1 extension prefix**: the dot form `m1.extensions.<domain>` (the form check_m0 C08
  documents), mapped to **the namespace IRI the M1 extension itself uses** — read it in
  that extension's `@context` / `@id` at HEAD; never rebuild it from the folder name.
  The `m1.ext:<domain>` form found in many instances is colon-named: do not copy it
  (harmonisation: WS-10).
- Add `schema` (`https://schema.org/`) only if a `schema:` term is used.

**Mandatory JSON-LD content (owl:Ontology node):**
1. Metadata: `rdfs:label`, `rdfs:comment`, `dcterms:created`, `dcterms:creator`,
   `owl:versionInfo`, and **`m3:changelog`** — a list of entries
   `{ "owl:versionInfo": …, "dcterms:date": …, "adms:versionNotes": … }`
   (newest first, 3 kept). `m2:changelog` is FORBIDDEN (check_m0 C14, SHACL).
2. `owl:imports` as **IRIs**: `[{ "@id": "M3_GenesisGrammar.jsonld" },
   { "@id": "M2_GenericConcepts.jsonld" }, { "@id": "M1_CoreConcepts.jsonld" },
   { "@id": "M0_Common.jsonld" }, { "@id": "M1_extensions/<domain>/M1_<Domain>.jsonld" }]`
   — never plain strings (a string is a literal: nothing is imported).
3. `m3:ontologyType`, `m1:domain`, and the `m0:` scores / means / epistemic gap as
   defined in `M0_Common` at HEAD.
4. Instance sections, each a **local term** with **prefixed sub-fields**:
   `m0.<instanceId>:completeness`, `…:minimality`, `…:pedagogy`, `…:observer`,
   `…:components` (with each component's ASFID contribution), `…:process`,
   `…:territorySpace` (ASFID / Eagle Eye), `…:mapSpace` (REVOI / Sphinx Eye),
   `…:epistemicGap` (ΔΘ, delta vector, norm, interpretation), `…:revoi`,
   `…:GenericConceptsMobilized`, `…:validation`.
   Inside them, reuse a standard term when one fits (`rdfs:label` for a name,
   `dcterms:description` for a description, `skos:note`, `skos:example`,
   `schema:unitText` for a unit text…), otherwise a `m0.<instanceId>:` term.
   ASFID / REVOI letters (`A`, `S`, `F`, `It`, `D`, `R`, `E`, `V`, `O`, `Im`) used as
   **keys** are bare keys too: use the `m0:` score terms or a prefixed term.

> ⏸ **"Duo analysis" mode** if any blocking occurs at any sub-step
> (concept not found, tension between dimensions, namespace doubt, a field with no
> declared home) — suspend and open discussion with Michel.

#### 3.4 — README.md Generation

After JSON-LD validation, generate `M0_[InstanceName]_README.md` with:
```
# [Instance Name] — TSCG Instance

## Overview
## System Description
## TSCG Analysis
### ASFID State (Territory / Eagle Eye)
### REVOI State (Map / Sphinx Eye)
### Epistemic Gap
## Components
## GenericConcepts Mobilized
## Key Insights
## Transdisciplinary Analogies (if relevant)
## References
```

#### 3.5 — Validation — MANDATORY, all must pass

Run from the repository root.

**(a) Zero bare keys** (this check can fail — exit code 1 — and must report 0):

```python
import json, sys
from collections import Counter
doc = json.load(open(sys.argv[1], encoding="utf-8"))
ctx = doc.get("@context", {}); declared = set(ctx) if isinstance(ctx, dict) else set()
bare = Counter()
def walk(n):
    if isinstance(n, dict):
        for k, v in n.items():
            if not k.startswith("@") and ":" not in k and k not in declared:
                bare[k] += 1
            walk(v)
    elif isinstance(n, list):
        for x in n: walk(x)
walk(doc.get("@graph", doc))
print(f"bare keys: {sum(bare.values())}  {dict(bare.most_common(15))}")
sys.exit(1 if bare else 0)
```

**(b) SHACL:**
```bash
python ontology/TSCG_InstanceGrammar/validate_m0_instance.py instances/[type]/[InstanceName]/M0_[InstanceName].jsonld
```

**(c) M0 checker** (namespaces, imports, changelog, tensor remnants, SHACL):
```bash
python ontology/toolchain/check-M0/check_m0_instances.py --instance [InstanceName]
```

**(d) If an M1 / M2 file was modified (3.1 / 3.2):** run
`python ontology/toolchain/tscg_metrics.py` before and after — the VOC bare-key gauge
must not rise — and the gate `cd ontology/toolchain && python run_all_layers.py`
(a new M0 file also changes the gate's M0 file count: show the moved counts to Michel
before any `--update-golden`).

**Deliver with the numbers**: bare keys = 0, SHACL result, check_m0 line, and for
M1/M2 changes the VOC gauge before → after.

**If validation fails:**
1. Review the report
2. Typical causes:
   - Bare keys (fix: prefix them — standard term, TSCG term, or `m0.<instanceId>:`)
   - Missing mandatory properties (`rdfs:label`, `m3:ontologyType`, `m1:domain`, …)
   - Wrong property names or namespaces (`dcterms:title`, `m2:changelog`, …)
   - Relative or colon-named `@context` entries
   - `owl:imports` written as strings
3. Fix the JSON-LD file and re-run until everything passes

| Error | Cause | Fix |
|-------|-------|-----|
| "bare keys: N" (N > 0) | unprefixed, undeclared keys | prefix each key (see Vocabulary rule) |
| "m3:ontologyType MUST be one of..." | Missing or wrong ontologyType | Add `"m3:ontologyType": {"@id": "m3:Poclet"}` |
| "m1:domain is MANDATORY" | Missing domain property | Add `"m1:domain": "Chemistry"` |
| "Use rdfs:label instead of dcterms:title" | Wrong property name | Rename `dcterms:title` → `rdfs:label` |
| "pyshacl cannot resolve relative URLs" | Relative namespace URLs in @context | Use the full `https://raw.githubusercontent.com/...` IRIs |
| "owl:Ontology required" | Wrong @type value | Change `"@type": "owl:NamedIndividual"` → `"owl:Ontology"` |
| m2:changelog present (C14) | old changelog container | `m3:changelog` with `{owl:versionInfo, dcterms:date, adms:versionNotes}` |

> ⏸ **Mandatory sync point if validation fails repeatedly** — discuss structural
> issues with Michel before continuing.

**Only proceed to Step 4 (Simulation) after all checks pass.**

---

## Step 4 — SIMULATION

### Objective
Generate a **standalone HTML application** (Electron and browser compatible)
visualizing the instance in an interactive, pedagogical, and aesthetic way.

### Reference Template
The FireTriangle HTML is the **canonical template**. Conform to it for:
- CSS Grid layout: `header / canvas + splitter + sidebar / controls`
- GitHub-style dark theme (CSS variables for ASFID/REVOI colors)
- Tabbed sidebar: Description | ASFID/REVOI | GenericConcepts | README
- Draggable splitter between canvas and sidebar
- Everything inline in a single `.html` file (no external files except CDN)

### ASFID/REVOI Color Palette (reusable CSS variables)
```css
--col-A: #f78166;  /* Attractor — red-salmon */
--col-S: #56d364;  /* Structure — green */
--col-F: #79c0ff;  /* Flow — light blue */
--col-I: #d2a8ff;  /* Information — purple */
--col-D: #e3b341;  /* Dynamics — amber */
--col-R: #79c0ff;  /* Representability */
--col-E: #56d364;  /* Evolvability */
--col-V: #f78166;  /* Verifiability */
--col-O: #d2a8ff;  /* Observability */
--col-Im: #e3b341; /* Interoperability */
--eagle:  #f78166; /* Eagle Eye accent */
--sphinx: #79c0ff; /* Sphinx Eye accent */
```

### Allowed Libraries (cdnjs.cloudflare.com CDN only)
- **p5.js** — main canvas animation (mandatory)
- Chart.js, D3 — complementary visualizations (optional)

### CSP Header (Electron + standalone compatible)
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self' https://cdnjs.cloudflare.com;
               script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
               style-src  'self' 'unsafe-inline';
               img-src    'self' data: blob:;
               connect-src http://127.0.0.1:* ws://127.0.0.1:*;">
```

### Iterative Process

**First draft**: generate a functional simulation covering:
- p5.js canvas animation representing system dynamics
- Sidebar with ASFID/REVOI scores (colored progress bars)
- List of mobilized GenericConcepts
- README tab with instance description

**Refinement rounds** (successive iterations with Michel):
- Ergonomics round: interactive controls, sliders, buttons
- Pedagogy round: labels, tooltips, annotations, legends
- Aesthetics round: animations, colors, proportions, visual polish

> Michel decides the number of rounds and priorities at each iteration. ⏸ after each round.

> Ontology files live next to the instance, never under `static/` (rule of
> 2026-09-30: no ontology copy under `static/`, except instance data such as a
> simulation's own data module).

---

## File Naming Conventions

```
instances/[type]/[InstanceName]/
├── M0_[InstanceName].jsonld         ← M0 ontology
├── M0_[InstanceName]_README.md      ← documentation
├── M0_[InstanceName]_analysis.md    ← TSCG analysis (step 2)
└── [InstanceName]_sim.html          ← standalone simulation
```

`[InstanceName]` is in PascalCase (e.g., `FireTriangle`, `ColorSynthesis`).
`[type]`: list the categories under `instances/` at HEAD (e.g. `poclets`,
`symbolic-system-grammars`, `systemic-frameworks`, `tscg-tools`).

---

## Pipeline Summary and Sync Points

```
PROPOSITION
  └─ Diagnostic (TSCG lens + experience perspective)
  └─ Classification: Trivial⏸ | Valid instance✅ | Too complex⏸
       ↓ (if Valid instance)
ANALYSIS → analysis.md
  └─ Alignment✅ | Gap⏸ | Refutation⏸
       ↓ (if Alignment)
MODELING
  ├─ 3.1 M2 GenericConcepts (existing + candidates)
  ├─ 3.2 M1 DomainConceptCombos (existing + candidates)
  ├─ 3.3 M0 JSON-LD  ← zero bare keys · duo mode if blocking ⏸
  ├─ 3.4 README.md
  └─ 3.5 Validation ← MANDATORY: bare keys 0 · SHACL · check_m0 (· VOC/gate if M1/M2) ✅⏸
       ↓ (only if all checks pass)
SIMULATION
  └─ First HTML standalone draft
  └─ Iterative rounds (ergonomics / pedagogy / aesthetics) ⏸⏸⏸
```

---

## Validation tools (reference)

- `validate_m0_instance.py` (`ontology/TSCG_InstanceGrammar/`): one JSON-LD file as
  argument, uses `ontology/toolchain/check-M0/M0_Instances_Schema_shacl.ttl` (single
  source of truth; the former `TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl` was
  removed), optional `--schema`, exit code 0 / 1, violation report on failure.
- `check_m0_instances.py` (`ontology/toolchain/check-M0/`): checks C01–C15 on all M0
  instances or one (`--instance NAME`); its totals feed the gate.
- Requirement: `python -m pip install -r ontology/toolchain/requirements.txt` (rdflib,
  pyshacl, pyld). Use `python -m pip`, not a bare `pip` (several Pythons may be installed).
