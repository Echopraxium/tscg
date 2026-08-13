# TSCG — Reference Corpus (Complete)

**Author**: Echopraxium with the collaboration of Claude AI · **Date**: 2026-08-11

> **This file is a router, not a content store.** It maps *where authority lives*
> so that live facts are read from HEAD, never recited from the corpus. It carries
> no versions, counts, or golden values — those go dirty. For the hard invariants
> (notation, REVOI, namespaces, conventions), see the companion
> **`TSCG_ReferenceCorpus_Bootstrap.md`**.
>
> Paths below are tagged **[✓ HEAD 2026-08-11]** when confirmed live (HTTP 200 on
> the raw CDN today) or **[⚠ unconfirmed]** when known only from memory — the
> latter must be checked with `git ls-tree -r HEAD` before being trusted.

---

## How to read HEAD

- Raw CDN (unrestricted): `https://raw.githubusercontent.com/Echopraxium/tscg/main/<path>`
- Exact committed content: `git show HEAD:<path>` in a freshly-fetched clone
  (`git fetch --depth 1 origin main && git reset --hard origin/main`)
- The GitHub **API is rate-limited** — do not rely on it for tree/SHA; use the CDN or a clone.

---

## The 16 primitive types — 3 grammars, 3 source files

Verified against HEAD on 2026-08-11. `M3_GenesisGrammar.jsonld` is the **aggregator**
(`owl:imports` the three below + `M3_GrammarFoundation.jsonld`); the **truth lives in
the three specialised files**, not the aggregator.

| Grammar | Source file `[✓ HEAD]` | Op. | Primitives |
|---|---|---|---|
| **Gt** — Territory / Eagle Eye | `ontology/M3_EagleEye.jsonld` | `×` | A, St, F, It, D — ASFID (5) |
| **Gm** — Map / Sphinx Eye | `ontology/M3_SphinxEye.jsonld` | `+` | R, E, V, O, **Im** — REVOI (5) |
| **Gs** — Stereopsis | `ontology/M3_BicephalousPerspective.jsonld` | `\|` | T, K, Ss, L, _^, _$ (6) |

**= 5 + 5 + 6 = 16.** Notes: Gm's 5th is `Im`, never a bare `I` (the `{R,E,V,O,I}`
form was a corrected defect). Gs's 6 = 4 nominal (TKSL) + 2 poles (`_^`/`_$`, polarity
modifiers); `_0` (EquilibriumPole) `= _^ | _$` is a **derived** element, not a primitive.

---

## Layer routing — where each layer's authority lives

| Layer | Path `[✓ HEAD 2026-08-11]` |
|---|---|
| M3 aggregator | `ontology/M3_GenesisGrammar.jsonld` |
| M3 grammars | `ontology/M3_EagleEye.jsonld`, `M3_SphinxEye.jsonld`, `M3_BicephalousPerspective.jsonld`, `M3_GrammarFoundation.jsonld` |
| M2 | `ontology/M2_GenericConcepts.jsonld` |
| M1 core | `ontology/M1_CoreConcepts.jsonld` |
| M1 extensions | `ontology/M1_extensions/<domain>/M1_<Domain>.jsonld` (e.g. `M1_extensions/biology/M1_Biology.jsonld`) |
| M0 shared | `ontology/M0_Common.jsonld` (`m0:` resolves here) |

## Tooling routing

| Purpose | Path `[✓ HEAD 2026-08-11]` |
|---|---|
| Acceptance gate | `ontology/cli-tools/run_all_layers.py` |
| Golden values | `ontology/cli-tools/golden_values.json` |
| Metrics gauge | `ontology/cli-tools/tscg_metrics.py` |
| M1 checker | `ontology/cli-tools/check-M1/check_M1.py` |
| M1 SHACL | `ontology/cli-tools/check-M1/M1_Schema_shacl.ttl` |
| M0 SHACL | `ontology/cli-tools/check-M0/M0_Instances_Schema_shacl.ttl` |

*Reminder: `check_M1.py` runs from `ontology/cli-tools/`, not the repo root.
Watch the separator — the **folder** is `check-M1` (hyphen), the **file** is
`check_M1.py` (underscore); mixing them gives a 404.*

## M0 instances routing

**Confirmed convention** `[✓ HEAD]`: `instances/<Category>/<InstanceCamelCase>/M0_<Instance>.jsonld`
— one sub-folder per instance (this differs from the flat layout in older notes).

| Category | Status | Example confirmed |
|---|---|---|
| `instances/poclets/` | `[✓ HEAD]` | `instances/poclets/FireTriangle/M0_FireTriangle.jsonld` |
| `instances/systemic-frameworks/` | `[✓ HEAD]` | `instances/systemic-frameworks/Triz/M0_Triz.jsonld` |
| `instances/tscg-tools/` | `[✓ HEAD]` | `instances/tscg-tools/TscgOntologyAPIServer/M0_TscgOntologyAPIServer.jsonld` |
| `instances/symbolic-system-grammars/` | `[✓ HEAD]` | `instances/symbolic-system-grammars/TriskeleToolchain/M0_TriskeleToolchain.jsonld` |
| `instances/transdisclet/` | `[· absent]` | not in the tree (empty/reserved — git tracks no empty dir) |

**Casing is inconsistent across the repo — verify per instance, don't assume.**
Some folders are CamelCase (`FireTriangle`, `Triz`), others lowercase (`vsm`,
`iching`), and a folder's case need not match its file's (`vsm/M0_VSM.jsonld`).

## Other key folders — `[✓ HEAD 2026-08-12]`

- `ontology/docs/_01_Worksite/` — worksite READMEs, `WS-n/` sub-folders, and dated
  session HandOvers (e.g. `WS-0/.../TSCG_Session_Handover_2026-08-11.md`). This is
  where HandOvers are archived.
- `docs/CoreHypotheses/` — core-hypothesis essays.
- `cli_tools/` at repo root — **underscore**, root-level tools (linter, reasoning
  test, migration). Distinct from `ontology/cli-tools/` (**hyphen**), the gate/checker tools.

---

## Durable corpus index (the 27 kept `.md`)

What remains in project knowledge after cleanup — durable *rationale*, no live structure.

**Foundations & method**: `Structural_Grammar_Foundation.md` (+ its 2 READMEs),
`Functional_Grammar_Model.md`, `OntologyModeling_Guidelines.md`, `OntologicalOverfitting.md`,
`Poclet_Analysis_Methodology.md`, `poclet_terminology.md`, `TSCG_Architectural_Extensions.md`.

**Epistemology & philosophy**: `TerritoryMap_Dichotomy.md`, `_00_TSCG_as_StereoscopicGlasses.md`,
`_01_Narcissus_and_Icarus_as_Safeguards.md`, `CredibilityAccretion_Process.md`,
`Archetypes_as_CrossCultural_Artifacts.md`, `LegoTechnic_Modularity.md`, `SystemicEsperanto.md`,
`MultisubjectiveScoreEvaluationProtocol.md`, `TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md`.

**Ontology READMEs (rationale kept — read HEAD for structure)**: `M3_GrammarFoundation_README.md`,
`M2_GenericConcepts_README.md`, `M1_CoreConcepts_README.md`, `M3_GenesisGrammar_README.md`,
`M3_EagleEye_README.md`, `M3_SphinxEye_README.md`, `M3_BicephalousPerspective_README.md`,
`tscg_metrics_README.md`.

**Live design note (deferred worksite)**: `_01_Facet_as_M3_Principle_ArchitectureNote.md`.

---

*Companion: `TSCG_ReferenceCorpus_Bootstrap.md` (invariants). Governing discipline:
the `head-over-memory` skill.*
