"""
TSCG Migration Verifier -- Phase 3
Scans all .jsonld files for residual tensor product formalism references.

Usage:
    python verify_migration.py [--root PATH] [--strict]

Author: Echopraxium with the collaboration of Claude AI
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

# Windows UTF-8 fix: force UTF-8 for stdout AND stderr
# This covers both terminal output and file redirection (> file.txt)
import os
os.environ.setdefault('PYTHONUTF8', '1')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

VIOLATIONS = {
    "hasTensorFormula":  "Property not renamed -> m2:hasStructuralFormula",
    "hilbert_space":     "Hilbert space reference (M3 remnant)",
    "orthonormality":    "Orthonormality claim (Hilbert remnant)",
    "H_ASFID":          "Hilbert space H_ASFID",
    "H_REVOI":          "Hilbert space H_REVOI",
    "Hilbert space":     "Explicit Hilbert space mention (reframe)",
    "svdDecomposition":  "SVD block (remove from Domain/KF)",
    "couplingMatrix":    "Coupling matrix Sigma (remove)",
}

EXPECTED_CONTEXTS = [
    # Changelog entries documenting the reform (legitimate historical mentions)
    "FORMALISM REFORM",
    "FORMAT CORRECTION",
    "migrate_properties",
    # Operator disclaimer in GrammarFoundation
    "disclaimer",
    "NOT an algebraic",
    "shares notation",
]


@dataclass
class Violation:
    file: Path
    line: int
    pattern: str
    reason: str
    context: str


def is_expected(line: str) -> bool:
    return any(ctx in line for ctx in EXPECTED_CONTEXTS)


# Directories to exclude from scan (archives, backups, references)
EXCLUDE_DIRS = {
    "Ref", "docs", "sparql", "tools", "_protos", "reboot-kit",
}


def is_excluded(path: Path, root: Path) -> bool:
    """Return True if path is inside an excluded directory."""
    try:
        parts = path.relative_to(root).parts
        for part in parts:
            # Explicit exclusion list
            if part in EXCLUDE_DIRS:
                return True
            # Generic patterns: backup dirs, archive dirs, hidden dirs
            p = part.lower()
            if ("backup" in p or "_archive" in p or p.startswith("_back")
                    or p.startswith("_archive") or p.startswith("archive")):
                return True
        return False
    except ValueError:
        return False


def scan_file(path: Path) -> list:
    violations = []
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except Exception as e:
        print(f"  [WARN] Cannot read {path}: {e}")
        return violations
    for i, line in enumerate(lines, 1):
        if is_expected(line):
            continue
        for pattern, reason in VIOLATIONS.items():
            if pattern in line:
                violations.append(Violation(path, i, pattern, reason, line.strip()[:120]))
    return violations


def run(root: Path, strict: bool) -> int:
    print(f"\n{'='*60}")
    print(f"  TSCG Migration Verifier")
    print(f"  Root: {root}")
    print(f"{'='*60}\n")

    files = sorted(
        f for f in root.rglob("*.jsonld")
        if not is_excluded(f, root)
    )
    if not files:
        print("[WARN] No .jsonld files found.")
        return 1

    all_violations = []
    for path in files:
        v = scan_file(path)
        if v:
            print(f"[FAIL] {path.relative_to(root)}")
            for x in v:
                print(f"   line {x.line:4d}  [{x.pattern}]  {x.reason}")
                print(f"          -> {x.context}")
            all_violations.extend(v)

    print(f"\n-- JSON Validation {'-'*42}")
    bad = []
    for path in files:
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            bad.append((path, str(e)))
            print(f"  [FAIL] {path.relative_to(root)}: {e}")
    if not bad:
        print(f"  [ OK ] All {len(files)} .jsonld files are valid JSON")

    print(f"\n{'-'*60}")
    if not all_violations and not bad:
        print(f"  [ OK ] MIGRATION COMPLETE -- 0 violations, {len(files)} files clean")
        print(f"\n  Tensor formalism replaced by Structural Grammar.")
        return 0
    total = len(all_violations) + len(bad)
    print(f"  [FAIL] {total} issue(s) found -- migration incomplete")
    print(f"         Violations : {len(all_violations)}")
    print(f"         JSON errors: {len(bad)}")
    return 1 if strict else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    sys.exit(run(root=args.root.resolve(), strict=args.strict))
