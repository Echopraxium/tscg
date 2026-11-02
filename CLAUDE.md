# CLAUDE.md — TSCG repository root

TSCG (Transdisciplinary System Construction Game): a layered ontology framework
(M3 structural grammar → M2 generic concepts → M1 domain adaptations → M0 instances),
with its Python toolchain, its instance pipeline and its BabylonJS simulations.

This file is a **thin guide**. It carries rules and pointers, not framework content:
no versions, counts, concept lists or formulas. Those go stale the moment the repo moves.

---

## 1. Authority — read these, in this order

1. **HEAD** — the committed state of `main` (`git show HEAD:<file>`, or
   `https://raw.githubusercontent.com/Echopraxium/tscg/main/…`). HEAD is the only
   authority on live structure, versions and counts.
2. **`docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md`** — the hard invariants
   (notation, namespaces, conventions, the debt-honesty rule).
3. **`docs/reboot-kit/TSCG_ReferenceCorpus.md`** — which file owns which authority.
4. **`docs/reboot-kit/TSCG_SmartPrompt.md`** — the session loader (skills to load first).

Never state a verifiable fact (version, count, SHA, file structure) from memory or from
an old document: read it at the source. Skills under `.claude/skills/` (start with
`head-over-memory` and `tscg-ontology-diagnosis-pipeline`) carry the working disciplines.

Where the work stands: `ontology/docs/_01_Worksite/` (Debt Overview, worksite map) and the
latest HandOver. Modeling guidance: `ontology/docs/OntologyModeling_Guidelines.md`.

**Historical material is not an authority.** `docs/reboot-kit/` (except its live files,
listed in its own `CLAUDE.md`), `docs/methodology/`, `docs/papers/` and old READMEs
describe the framework as it was when they were written; vocabulary such as tensor
products (`⊗`), GenesisSpace, MetaConcepts or the "bicephalous basis" belongs to retired
eras.

---

## 2. The acceptance gate — nothing is committed without it

```bash
cd ontology/toolchain
python -m pip install -r requirements.txt   # once
python run_all_layers.py                    # must end with GATE: PASS
```

- Exact frozen counts per layer (`golden_values.json`). A count that goes **up** is a new
  defect — or deliberately revealed debt, frozen with a written reason. A count that goes
  **down** is checked against the debt-honesty rule (did the defect disappear, or move out
  of sight?) before `--update-golden`. Never loosen a check to pass.
- Every change to an ontology file (M3/M2/M1, M1 extensions, M0 instances): run the
  **OWL reasoner** on each changed file (`owl_reasoning_test/owl_reasoning_test.py --file
  <file>`, needs Java 25) and record the result before pushing. The gate lists the files.
- The full 6-phase procedure: skill `tscg-ontology-diagnosis-pipeline`.

---

## 3. File conventions

### Ontology files
- Layer prefix in file names: `M3_`, `M2_`, `M1_`, `M0_`.
- No comments in `.jsonld` files.
- Authorship: `"Echopraxium with the collaboration of Claude AI"`.
- Changelog: `m3:changelog` on the `owl:Ontology` node (never `m2:changelog`), entries
  `{owl:versionInfo, dcterms:date, adms:versionNotes}`, newest first.
- Ontology type: `m3:ontologyType` only.
- SHACL files: dot before the extension (`<Name>.shacl.ttl`). SPARQL queries:
  `ontology/sparql/`.
- For namespaces, `@base`, notation and anything else normative: the Bootstrap (§1).

### Simulations
- BabylonJS 6.26.0, from `unpkg.com/babylonjs@6.26.0/babylon.js`.
- UI patterns: consult `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld`.
- Skill: `tscg-create-instance-simulation`.

### Underscore prefix = hidden from the gallery
A leading `_` on a folder is **functional**: the gallery generator
(`cli_tools/regenerate_simulation_gallery/`) skips it.

| Folder | Meaning |
|---|---|
| `_static/` | prototype simulation — not published |
| `static/` | finished simulation — published |
| `_archives/` | superseded copies — not published |

Renaming `_static/` → `static/` **publishes** the prototype: never as a "cleanup".
Each poclet keeps two distinct READMEs, never merged: `M0_<Name>_README.md` (ontology)
and `_static/M0_<Name>_Simulation_README.md` (simulation).

### Never copy a live ontology elsewhere
A frozen `.jsonld`/`.ttl` copy that looks like a source is how stale content gets mistaken
for the real thing. Point to the file on HEAD instead. Nothing is lost by removing a file:
`git show <commit>^:<path>`.

---

## 4. Nested CLAUDE.md — scoped contexts

Claude Code loads this file **and** the nearest `CLAUDE.md` up the tree from the working
directory. They compose; keep them separate.

| Scope | File | Owns |
|---|---|---|
| Repository root | `CLAUDE.md` (this file) | the ontology, the toolchain, the instance pipelines |
| TriskeleToolchain | `instances/symbolic-system-grammars/TriskeleToolchain/CLAUDE.md` | the Rust toolchain and VM; its gate is `python run_all_tests.py --clean` |
| Reboot kit | `docs/reboot-kit/CLAUDE.md` | which files of that folder are live, which are history |

In `TriskeleToolchain/`, its file wins on toolchain matters and ontology work is out of
scope; on the ontology, the toolchain rules do not apply.

---

## 5. Working rules (shared)

- Generated files in **English**; conversation with Michel in **French**.
- **Surgical edits** over rewrites; one lot at a time, one commit per group.
- No dead reference left behind: when a file moves or goes, every live citer is fixed.
- **Honest negative results** over enthusiastic validation.
- Semantics (what a concept means, whether a structure is right) is Michel's decision —
  never improvise it.

---

*Rewritten 2026-11-02 (thin guide). The previous version (573 lines: GenesisSpace,
bicephalous M3, tensor formulas, Smart Prompt v16 URI, links to reboot-kit copies) is
recoverable with `git show <this commit>^:CLAUDE.md`.*
