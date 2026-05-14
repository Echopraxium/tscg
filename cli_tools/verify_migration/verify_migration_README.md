# verify_migration — CLI Tool

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-05-13
**Location**: `cli_tools/verify_migration/`
**Part of**: TSCG Structural Grammar Migration (Phase 3)

---

## Purpose

Scans all TSCG `.jsonld` ontology files for residual tensor product formalism
references and validates JSON syntax on every file.

This is **Phase 3** of the Tensor to Structural Grammar migration.
Run after `migrate_properties` to confirm 0 violations.

> **Zero tolerance**: "Hilbert space" must NOT appear anywhere in active
> ontology files. Only changelog entries documenting the reform are exempt.

---

## Patterns Detected

| Pattern | Reason |
|---|---|
| `hasTensorFormula` | Property not renamed to `hasStructuralFormula` |
| `hilbert_space` | Hilbert space reference (M3 remnant) |
| `orthonormality` | Orthonormality claim (Hilbert remnant) |
| `H_ASFID` / `H_REVOI` | Hilbert space notation |
| `Hilbert space` | Any explicit mention -- zero tolerance |
| `svdDecomposition` | SVD block (remove from Domain/KF) |
| `couplingMatrix` | Coupling matrix Sigma (remove) |

---

## Legitimate Exemptions

Only **changelog entries** documenting the reform are automatically exempted:

```python
EXPECTED_CONTEXTS = [
    "FORMALISM REFORM",   # new changelog entries
    "FORMAT CORRECTION",  # old changelog entries
    "migrate_properties", # script references
    "disclaimer",         # operator disambiguation in GrammarFoundation
    "NOT an algebraic",   # explicit reframing note
    "shares notation",    # disambiguation note
]
```

Everything else is flagged -- including QM domain examples and any other
contextual "Hilbert space" mentions. When in doubt: reword, do not exempt.

---

## Excluded Directories

The script automatically excludes these from scanning:

| Pattern | Examples |
|---|---|
| Name contains `backup` | `backup_ontologyCategory_20260512/`, `domain_format_fix_backups/` |
| Name contains `_archive` | `_archives/` |
| Explicit list | `Ref/`, `docs/`, `sparql/`, `tools/`, `_protos/`, `reboot-kit/` |

Active ontology files in `ontology/` root, `M1_extensions/`, and
`instances/` are always scanned.

---

## Usage

```bash
# From repo root

# Standard check
python cli_tools/verify_migration/verify_migration.py --root ontology

# Strict mode -- exit 1 if any violations (for CI)
python cli_tools/verify_migration/verify_migration.py --root ontology --strict

# Redirect output to file (Windows -- UTF-8 handled automatically)
python cli_tools/verify_migration/verify_migration.py --root ontology --strict > verify_output.txt 2>&1
```

> **Windows note**: The script sets `PYTHONUTF8=1` and reconfigures stdout/stderr
> to UTF-8 automatically. No `-X utf8` flag needed.

---

## Options

| Option | Description |
|---|---|
| `--root PATH` | Directory to scan recursively (default: current directory) |
| `--strict` | Exit with code 1 if any violations found |

---

## Output -- Success

```
============================================================
  TSCG Migration Verifier
  Root: ontology/
============================================================

-- JSON Validation ------------------------------------------
  [ OK ] All 24 .jsonld files are valid JSON

------------------------------------------------------------
  [ OK ] MIGRATION COMPLETE -- 0 violations, 24 files clean

  Tensor formalism replaced by Structural Grammar.
```

## Output -- With Violations

```
[FAIL] M2_GenericConcepts.jsonld
   line  209  [hasTensorFormula]  Property not renamed -> m2:hasStructuralFormula
          -> "m2:hasTensorFormula": "D x I x F",
...
------------------------------------------------------------
  [FAIL] 3 issue(s) found -- migration incomplete
         Violations : 3
         JSON errors: 0
```

---

## How to Fix Violations

| Violation | Fix |
|---|---|
| `hasTensorFormula` | Run `migrate_properties.py` on that file |
| `hilbert_space` / `orthonormality` | Remove field entirely |
| `Hilbert space` in text | Replace with grammar/categorical equivalent |
| `couplingMatrix` / `svdDecomposition` | Remove blocks entirely |
| Legacy alignment file | Delete if no longer needed |
| Backup dir still scanned | Check exclusion pattern covers directory name |

---

## Workflow

```
Phase 1  Manual M3 edits         (GrammarFoundation, EagleEye, SphinxEye, GenesisGrammar)
Phase 2  migrate_properties.py   rename hasTensorFormula everywhere
Phase 3  verify_migration.py     confirm 0 violations   <-- THIS TOOL
```

---

## See Also

- `cli_tools/migrate_properties/` -- Phase 2 renaming tool (run before this)
- `ontology/StructuralGrammar/TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
- SKILL: `.claude/skills/tscg-tensor-to-structural-grammar-migration/`

---

*TSCG Framework -- Echopraxium with the collaboration of Claude AI -- May 2026*
