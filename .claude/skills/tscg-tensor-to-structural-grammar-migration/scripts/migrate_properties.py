"""
TSCG Migration Script — Phase 2
Renames tensor product property family to structural formula family.

Usage:
    python migrate_properties.py [--dry-run] [--root PATH]

Options:
    --dry-run   Preview changes without writing files
    --root      Repository root (default: current directory)

Author: Echopraxium with the collaboration of Claude AI
"""

import argparse
import json
import shutil
from pathlib import Path

# ── Property renames ──────────────────────────────────────────────────────────
RENAMES = [
    ('"m2:hasTensorFormula"',      '"m2:hasStructuralFormula"'),
    ('"m2:hasTensorFormulaTeX"',   '"m2:hasStructuralFormulaTeX"'),
    ('"m2:hasTensorFormulaASCII"', '"m2:hasStructuralFormulaASCII"'),
    # Also rename any key-only occurrences (no leading quote from property name)
    ("m2:hasTensorFormula ",       "m2:hasStructuralFormula "),
]

# ── Patterns that should NOT be renamed (false-positive guards) ───────────────
SAFEGUARD_PATTERNS = [
    "hasTensorFormulaTeX",    # handled separately above
    "hasTensorFormulaASCII",  # handled separately above
]


def rename_in_content(content: str) -> tuple[str, int]:
    """Apply all renames. Returns (modified_content, change_count)."""
    modified = content
    total_changes = 0
    for old, new in RENAMES:
        count = modified.count(old)
        if count:
            modified = modified.replace(old, new)
            total_changes += count
    return modified, total_changes


def validate_json(content: str, path: Path) -> bool:
    """Return True if content is valid JSON."""
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON validation failed: {e}")
        return False


def migrate_file(path: Path, dry_run: bool) -> tuple[bool, int]:
    """
    Migrate a single file.
    Returns (was_modified, change_count).
    """
    content = path.read_text(encoding="utf-8")
    modified, changes = rename_in_content(content)

    if changes == 0:
        return False, 0

    if dry_run:
        print(f"  📝 {changes} rename(s) would be applied")
        return True, changes

    # Validate before writing
    if not validate_json(modified, path):
        print(f"  ⚠️  Skipped (JSON validation failed after rename)")
        return False, 0

    # Backup original
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)

    # Write migrated file
    path.write_text(modified, encoding="utf-8")
    print(f"  ✅ {changes} rename(s) applied  (backup: {backup.name})")
    return True, changes


def run(root: Path, dry_run: bool) -> None:
    mode = "DRY RUN — " if dry_run else ""
    print(f"\n{'=' * 60}")
    print(f"  TSCG Migration — {mode}Tensor → Structural Grammar")
    print(f"  Root: {root}")
    print(f"{'=' * 60}\n")

    jsonld_files = sorted(root.rglob("*.jsonld"))
    if not jsonld_files:
        print("⚠️  No .jsonld files found. Check --root path.")
        return

    total_files_modified = 0
    total_renames = 0

    for path in jsonld_files:
        rel = path.relative_to(root)
        print(f"📄 {rel}")
        modified, count = migrate_file(path, dry_run)
        if modified:
            total_files_modified += 1
            total_renames += count
        else:
            print(f"  — unchanged")

    print(f"\n{'─' * 60}")
    print(f"  {'Would modify' if dry_run else 'Modified'}: "
          f"{total_files_modified} file(s), {total_renames} rename(s) total")
    if not dry_run and total_files_modified:
        print(f"  Backups: .jsonld.bak files alongside each modified file")
        print(f"\n  ➡️  Next: run verify_migration.py to confirm 0 violations")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename m2:hasTensorFormula → m2:hasStructuralFormula in all TSCG .jsonld files"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without writing files"
    )
    parser.add_argument(
        "--root", type=Path, default=Path("."),
        help="Repository root directory (default: current directory)"
    )
    args = parser.parse_args()

    run(root=args.root.resolve(), dry_run=args.dry_run)
