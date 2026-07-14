# check-M1 — TSCG M1 Layer Validation & Correction Tool

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 2.0.0  
**Date**: 2026-07-12  
**Location**: `ontology/cli-tools/check-M1/`

---

## Overview

`check_M1.py` validates and auto-corrects TSCG M1 layer files against the
TSCG v16.1.0 conventions. It covers:

- **M1_CoreConcepts.jsonld** — GenericConceptCombos, properties, namespace
- **M1_Domains.jsonld** — domain registry
- **All 13 M1 extensions** — KnowledgeFieldConceptCombos, formulas, namespaces

The tool performs **two levels of validation**:

1. **Python checks** — structural, semantic, and convention checks
2. **SHACL validation** — formal constraint validation via pyshacl (optional)

---

## Installation

```bash
# Required (always)
python >= 3.8

# Optional (for --shacl option)
pip install pyshacl
```

---

## Usage

```bash
# Validate all M1 files (auto-detects location)
python check_M1.py

# Dry-run: show issues without modifying files
python check_M1.py --dry-run

# Validate a single file
python check_M1.py --file M1_Geology.jsonld
python check_M1.py --file /path/to/ontology/M1_Biology.jsonld

# Single file, dry-run
python check_M1.py --file M1_music.jsonld --dry-run

# Include SHACL validation
python check_M1.py --shacl

# Save report to check_M1_report.txt
python check_M1.py --report

# Verbose (show all checks, including passed)
python check_M1.py -v

# No color (for CI/log files)
python check_M1.py --no-color

# Full pipeline: all files + SHACL + report
python check_M1.py --shacl --report
```

---

## File Discovery

The script auto-discovers M1 files by scanning these locations (in order):

1. `../../ontology/` (relative to `cli_tools/check-M1/`)
2. `../../` (repo root)
3. Current working directory
4. Script directory

Use `--file` to specify an explicit path.

---

## Checks Performed

### Structural Checks
| Code | Severity | Description |
|---|---|---|
| ENC001 | ERROR | CRLF line endings (auto-fixed) |
| JSON001 | ERROR | Invalid JSON |

### @context Checks
| Code | Severity | Description |
|---|---|---|
| CTX001 | WARNING | Missing required context key |
| CTX002 | ERROR | @base incorrect URL (auto-fixed) |
| CTX003 | ERROR | m3: points to M3_GenesisSpace (auto-fixed) |

### owl:Ontology Node
| Code | Severity | Description |
|---|---|---|
| ONT002 | ERROR | dcterms:creator incorrect (auto-fixed) |
| ONT003 | WARNING | dcterms:created not ISO 8601 |
| ONT004 | ERROR | owl:versionInfo not semver X.Y.Z |
| ONT005 | ERROR | m3:ontologyType missing |
| ONT006 | ERROR | owl:imports references GenesisSpace (auto-fixed) |
| ONT007 | WARNING | m2:changelog not array format |

### GenericConceptCombo (M1_CoreConcepts)
| Code | Severity | Description |
|---|---|---|
| GCC001 | ERROR | Missing rdfs:subClassOf m2:GenericConceptCombo |
| GCC002 | WARNING | Missing m1:structuralGrammarFormula |
| GCC003 | WARNING | Formula not Fm2(...) pattern |
| GCC004 | ERROR | ⊗ tensor notation in formula (partial auto-fix) |

### DomainConceptCombo (Extensions) — renamed from KnowledgeFieldConceptCombo in SC-1
| Code | Severity | Description |
|---|---|---|
| DCC000 | ERROR | Retired class `m2:KnowledgeFieldConceptCombo` (auto-fixed → `m2:DomainConceptCombo`) |
| DCC001/001b | ERROR | Missing `rdfs:subClassOf m2:DomainConceptCombo` |
| DCC003 | WARNING | Missing `m1:structuralGrammarFormula` |
| DCC004 | WARNING | Formula not `Fm1m2(...)` |
| DCC010 | ERROR | **First argument of `Fm1m2` is not a registered Domain** (checked against `M1_Domains.jsonld`) |

### Signature rules — shared by Fm2 and Fm1m2 (SC-1)
| Code | Severity | Description |
|---|---|---|
| xxx005 | ERROR | Retired `⊗` notation |
| xxx006 | ERROR | **Monoidal operator (`×`/`+`/`\|`) inside a signature** — the bulk of the SC-6 backlog |
| xxx007 | ERROR | **Primitive type used as an argument** |
| xxx008 | ERROR | Wrong arity (`Fm2` ≥ 2 concepts; `Fm1m2` ≥ 1 domain **and** ≥ 1 concept) |
| xxx009 | ERROR | **Guard appended after the signature** (`\| gain > 1`) |
| EXP001 | ERROR | Retired property `m1:structuralGrammarFormulaExpanded` (D8 — no monoidal expansion) |

### Forbidden Patterns
| Code | Severity | Description |
|---|---|---|
| FRBDN001 | ERROR | Deprecated property found (m2:characterizedBy, tensorFormula, etc.) |
| FRBDN002 | ERROR | ORIVE terminology (auto-fixed → REVOI) |
| FRBDN003 | ERROR | m1core: namespace (auto-fixed → m1:) |
| FRBDN004 | ERROR | M3_GenesisSpace reference (auto-fixed → M3_GenesisGrammar) |

### Namespace
| Code | Severity | Description |
|---|---|---|
| NS001 | WARNING | Non-standard prefix key in @context |

---

## Auto-Fixed Issues

The following issues are corrected automatically (unless `--dry-run`):

| Issue | Auto-Fix Applied |
|---|---|
| CRLF endings | → LF |
| M3_GenesisSpace | → M3_GenesisGrammar (all occurrences) |
| ORIVE | → REVOI |
| m1core: namespace | → m1: |
| dcterms:creator wrong | → Echopraxium with the collaboration of Claude AI |
| @base incorrect | → https://raw.githubusercontent.com/.../ontology/ |
| owl:imports GenesisSpace | → M3_GenesisGrammar.jsonld |

Issues **not** auto-fixed (require manual intervention):
- Missing `m3:ontologyType`
- Missing `rdfs:subClassOf`
- Missing `m2:knowledgeField`
- Wrong formula patterns
- Non-semver `owl:versionInfo`

---

## SHACL Grammar

`M1_Schema.shacl.ttl` must be in the same directory as `check_M1.py`.

**8 shapes defined:**

| Shape | Target | Key constraints |
|---|---|---|
| M1OntologyShape | `owl:Ontology` | creator, date, versionInfo, m3:ontologyType |
| GenericConceptComboShape | `m2:GenericConceptCombo` | subClassOf, Fm2() formula |
| KFConceptComboShape | `m2:KnowledgeFieldConceptCombo` | subClassOf, knowledgeField, Fm1m2() formula |
| KnowledgeFieldInstanceShape | `m2:KnowledgeField` | NamedIndividual, label |
| PlainDomainClassShape | `rdfs:subClassOf` subjects | label mandatory |
| NamespacePurityShape | all | forbids deprecated properties |
| StructuralGrammarFormulaShape | formula subjects | Fm2/Fm1m2 pattern, no ⊗ |
| CorePatternShape | `m1:CorePattern` | NamedIndividual, raw formula allowed |

---

## Directory Structure

```
ontology/cli-tools/
├── tscg_paths.py             ← shared repo-root resolution (no hardcoded path)
├── check-M0/
│   ├── check_m0_instances.py
│   ├── migrate_m0_to_v1_5.py
│   └── M0_Instances_Schema_shacl.ttl
└── check-M1/
    ├── check_M1.py           ← this script
    ├── M1_Schema_shacl.ttl   ← SHACL grammar v1.1.0 (note: UNDERSCORE, not dot)
    ├── check_M1_README.md    ← this file
    └── check_M1_report.txt   ← generated by --report (git-ignored)
```

The scripts are **relocatable**: `tscg_paths` discovers the repository root by walking
UP from the script until it finds a directory holding both `ontology/` and `instances/`.
No absolute path is hardcoded. Override with `TSCG_REPO_ROOT` if ever needed.

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | All files clean (no errors) |
| `1` | One or more errors found |

---

## Integration with CI/CD

```yaml
# GitHub Actions example
- name: Validate TSCG M1 layer
  run: |
    cd cli_tools/check-M1
    python check_M1.py --no-color --report
```

---

## Convention Reference (v16.1.0)

### Namespaces
```
m1:                       → M1_CoreConcepts.jsonld# (umbrella)
m1:domain:X               → M1_Domains entities
m1:extension:<domain>:X   → M1 extension entities
```

### Formula Patterns (SC-1 — a combo's formula IS a function signature)
```
Fm2   : GenericConcept²⁺            → GenericConceptCombo   (≥ 2 named concepts)
Fm1m2 : Domain⁺ , GenericConcept⁺   → DomainConceptCombo    (≥ 1 domain AND ≥ 1 concept)

GOOD  Fm2(Cascade, Duplication, Network)
GOOD  Fm1m2(Optics, Refraction)

BAD   Fm1m2(Optics, A × St × F × It | R + O)   monoidal expression as argument
BAD   Fm1m2(Cascade, Duplication, Network)     no Domain → this is an Fm2
BAD   Fm2(Cascade, Amplification) | gain > 1   scalar guard = an M0 measurement in M1
BAD   Fm2²(A, B)                               RETIRED — there is no "second order"
```

⚠️ **v1.0.0 of this README documented `Fm1m2(Domain, A × B | C)` and `Fm2²(A, B)` as
VALID.** Both are now forbidden. `Fm2`/`Fm1m2` are **functions, not functors**:
emergence is non-compositional (arguments are *combined, not associated*), so a combo
has **no monoidal expansion** and its arguments are **named concepts**, comma-juxtaposed,
never joined by a grammar operator. `Fm2²` never appeared in a single real formula —
only in prose, as an *infix operator* between two monoidal expressions, which is the
retired `⊗⇒` structure. See `StructuralGrammar/Functional_Grammar_Model.md`.

### Forbidden
```
⊗                         → Use × (product) / + (sum) / | (bridge)
m2:characterizedBy        → Use m1:structuralGrammarFormula
asfidSignature            → Use m1:structuralGrammarFormula
tensorFormula             → Use m1:structuralGrammarFormula
hasTensorFormula          → Use m1:structuralGrammarFormula
M3_GenesisSpace           → Use M3_GenesisGrammar
ORIVE                     → Use REVOI
m1core:                   → Use m1:
```

---

## Changelog

**v2.0.0 (2026-07-12)** — SC-1 + three pre-existing bugs fixed
- **BUG**: `run()` called `fix_imports_genesis()`, **which was never defined** → the
  script raised `AttributeError` on the first file, in the auto-fix path. **None of the
  seven documented auto-fixes had ever run.** Method now implemented.
- **BUG**: the script looked for `M1_Schema.shacl.ttl` (DOT) while the file on disk is
  `M1_Schema_shacl.ttl` (UNDERSCORE) → `--shacl` never found its grammar and validated
  nothing, while still exiting 0. Both spellings are now tried.
- **BUG**: hardcoded discovery paths assumed `cli_tools/check-M1/` at repo root.
  Replaced by `tscg_paths` (relocatable).
- **SC-1**: `KnowledgeFieldConceptCombo` → `DomainConceptCombo`; the signature rules
  (no monoidal operator, no primitive argument, arity, guards); `Fm2²` retired;
  `m1:structuralGrammarFormulaExpanded` retired (D8); **DCC010** — `Fm1m2`'s first
  argument is checked against the `M1_Domains.jsonld` registry.

**v1.0.0 (2026-05-26)**
- Initial release
- 7 check categories, 20+ check codes
- 7 auto-fixable issues
- SHACL integration (optional)
- Report generation
- Auto-discovery of M1 files
