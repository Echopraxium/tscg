# migrate_properties — CLI Tool

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-05-13
**Location**: `cli_tools/migrate_properties/`
**Part of**: TSCG Structural Grammar Migration (Phase 2)

---

## Purpose

Automates the renaming of the tensor product property family to the
structural formula family across all TSCG `.jsonld` ontology files.

This is **Phase 2** of the Tensor to Structural Grammar migration.
Run after Phase 1 (manual M3 edits) and before Phase 3 (`verify_migration`).

> In the initial migration (v16.0.0), the renaming was applied manually
> via Python directly on each file. This script is provided for **future
> migrations** — new poclets, new M1 extensions, or any file that still
> carries the old property names.

---

## What It Renames

| Old property | New property |
|---|---|
| `m2:hasTensorFormula` | `m2:hasStructuralFormula` |
| `m2:hasTensorFormulaTeX` | `m2:hasStructuralFormulaTeX` |
| `m2:hasTensorFormulaASCII` | `m2:hasStructuralFormulaASCII` |

Formula **values** are never changed — `"D x I x F"` stays `"D x I x F"`.
Only property **names** are renamed.

---

## Usage

```bash
# From repo root

# 1. Preview changes without writing (recommended first)
python cli_tools/migrate_properties/migrate_properties.py --dry-run --root ontology

# 2. Apply changes
python cli_tools/migrate_properties/migrate_properties.py --root ontology

# 3. Always verify afterwards
python cli_tools/verify_migration/verify_migration.py --root ontology --strict
```

---

## Options

| Option | Description |
|---|---|
| `--root PATH` | Directory to scan recursively (default: current directory) |
| `--dry-run` | Preview changes without writing any file |

---

## Safety Features

- **Dry-run mode** -- preview before applying
- **Automatic backup** -- creates `.jsonld.bak` alongside each modified file
- **JSON validation** -- validates each file after renaming; restores backup on failure
- **Change report** -- shows count of renames per file

---

## Sample Output

```
M2_GenericConcepts.jsonld
  250 rename(s) applied  (backup: M2_GenericConcepts.jsonld.bak)
M1_extensions/economics/M1_Economics.jsonld
  3 rename(s) applied  (backup: M1_Economics.jsonld.bak)
M3_EagleEye.jsonld
  -- unchanged
------------------------------------------------------------
  Modified: 2 file(s), 253 rename(s) total
  Backups: .jsonld.bak files alongside each modified file

  Next: run verify_migration to confirm 0 violations
```

---

## Typical Use Cases

**New M0 poclet** added before migration was complete:
```bash
python cli_tools/migrate_properties/migrate_properties.py \
  --dry-run --root instances/poclets/MyNewPoclet
```

**New M1 extension** created with old property names:
```bash
python cli_tools/migrate_properties/migrate_properties.py \
  --root ontology/M1_extensions/my_new_domain
```

**Full corpus check** after adding multiple files:
```bash
python cli_tools/migrate_properties/migrate_properties.py --dry-run --root ontology
python cli_tools/migrate_properties/migrate_properties.py --root ontology
python cli_tools/verify_migration/verify_migration.py --root ontology --strict
```

---

## See Also

- `cli_tools/verify_migration/` -- post-migration validation (always run after this script)
- `ontology/StructuralGrammar/TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
- SKILL: `.claude/skills/tscg-tensor-to-structural-grammar-migration/`

---

*TSCG Framework -- Echopraxium with the collaboration of Claude AI -- May 2026*
