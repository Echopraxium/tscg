# check-M1 — TSCG M1 Layer Validation & Correction Tool

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 1.0.0  
**Date**: 2026-05-26  
**Location**: `cli_tools/check-M1/`

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

### KnowledgeFieldConceptCombo (Extensions)
| Code | Severity | Description |
|---|---|---|
| KFCC001 | ERROR | Missing rdfs:subClassOf m2:KnowledgeFieldConceptCombo |
| KFCC002 | ERROR | Missing m2:knowledgeField |
| KFCC003 | WARNING | Missing m1:structuralGrammarFormula |
| KFCC004 | WARNING | Formula not Fm1m2(...) pattern |
| KFCC005 | ERROR | ⊗ tensor notation in formula (partial auto-fix) |

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
cli_tools/
└── check-M1/
    ├── check_M1.py           ← this script
    ├── M1_Schema.shacl.ttl   ← SHACL grammar (required for --shacl)
    ├── README.md             ← this file
    └── check_M1_report.txt   ← generated by --report (git-ignored)
```

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

### Formula Patterns
```
Fm2(A, B, C)              → GenericConceptCombo (M1_CoreConcepts)
Fm2²(A, B)                → Second-order combo (valid)
Fm1m2(Domain, A × B | C) → KnowledgeFieldConceptCombo (extensions)
```

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

**v1.0.0 (2026-05-26)**
- Initial release
- 7 check categories, 20+ check codes
- 7 auto-fixable issues
- SHACL integration (optional)
- Report generation
- Auto-discovery of M1 files
