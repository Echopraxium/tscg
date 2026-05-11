"""
TSCG Migration Verifier — Phase 3
Scans all .jsonld files for residual tensor product formalism references.

Usage:
    python verify_migration.py [--root PATH] [--strict]

Options:
    --root    Repository root (default: current directory)
    --strict  Exit with code 1 if any violations found (for CI)

Author: Echopraxium with the collaboration of Claude AI
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── Patterns that must NOT appear after migration ────────────────────────────
VIOLATIONS = {
    # Renamed properties still present
    "hasTensorFormula":      "Property not renamed → m2:hasStructuralFormula",
    # Hilbert space / quantum formalism
    "hilbert_space":         "Hilbert space reference (M3 formalism remnant)",
    "orthonormality":        "Orthonormality claim (Hilbert remnant)",
    "ℋ_ASFID":              "Hilbert space ℋ_ASFID (remove or reframe)",
    "ℋ_REVOI":              "Hilbert space ℋ_REVOI (remove or reframe)",
    "ℂ²⁵":                  "25D complex space claim (remove)",
    "Hilbert space":         "Explicit Hilbert space mention (reframe)",
    "svdDecomposition":      "SVD decomposition block (remove from Domain/KF)",
    "couplingMatrix":        "Coupling matrix Σ (remove from Domain/KF)",
    "singularValues":        "SVD singular values (remove from Domain/KF)",
    "|uᵢ⟩":                 "Ket notation (remove)",
    "|vᵢ⟩":                 "Ket notation (remove)",
    "αᵢⱼ":                  "Coupling coefficients αᵢⱼ (remove)",
    "⟨i|j⟩":               "Inner product notation (remove)",
}

# ── Patterns that are EXPECTED (do not flag) ─────────────────────────────────
# The word "tensor" may still appear in:
# - changelog entries documenting the migration
# - the disclaimer node in M3_GenesisSpace
# - this script itself
EXPECTED_CONTEXTS = [
    "FORMALISM REFORM",   # changelog entries
    "disclaimer",         # operator disclaimer in GenesisSpace
    "NOT an algebraic",   # explicit reframing note
    "shares notation",    # disambiguation note
    "migrate_properties", # script references
    # hasTensorFormula in changelog/version entries handled by other patterns
]


@dataclass
class Violation:
    file: Path
    line: int
    pattern: str
    reason: str
    context: str


def is_expected(line_content: str) -> bool:
    """Return True if the line is an expected (allowed) occurrence."""
    return any(ctx in line_content for ctx in EXPECTED_CONTEXTS)


def scan_file(path: Path) -> list[Violation]:
    violations = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"  ⚠️  Cannot read {path}: {e}")
        return violations

    for lineno, line in enumerate(lines, start=1):
        if is_expected(line):
            continue
        for pattern, reason in VIOLATIONS.items():
            if pattern in line:
                violations.append(Violation(
                    file=path,
                    line=lineno,
                    pattern=pattern,
                    reason=reason,
                    context=line.strip()[:120],
                ))

    return violations


def validate_json_all(root: Path) -> list[Path]:
    """Return list of files that fail JSON parsing."""
    bad = []
    for path in root.rglob("*.jsonld"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad.append((path, str(e)))
    return bad


def run(root: Path, strict: bool) -> int:
    print(f"\n{'=' * 60}")
    print(f"  TSCG Migration Verifier")
    print(f"  Root: {root}")
    print(f"{'=' * 60}\n")

    jsonld_files = sorted(root.rglob("*.jsonld"))
    if not jsonld_files:
        print("⚠️  No .jsonld files found. Check --root path.")
        return 1

    all_violations: list[Violation] = []

    for path in jsonld_files:
        violations = scan_file(path)
        if violations:
            rel = path.relative_to(root)
            print(f"❌ {rel}")
            for v in violations:
                print(f"   line {v.line:4d}  [{v.pattern}]  {v.reason}")
                print(f"           └─ {v.context}")
            all_violations.extend(violations)
        # else: silent for clean files

    # JSON validation pass
    print("\n── JSON Validation ──────────────────────────────────")
    bad_json = validate_json_all(root)
    if bad_json:
        for path, err in bad_json:
            print(f"  ❌ {path.relative_to(root)}: {err}")
    else:
        print(f"  ✅ All {len(jsonld_files)} .jsonld files are valid JSON")

    # Summary
    print(f"\n{'─' * 60}")
    if not all_violations and not bad_json:
        print(f"  ✅ MIGRATION COMPLETE — 0 violations, {len(jsonld_files)} files clean")
        print(f"\n  Tensor formalism successfully replaced by Structural Grammar.")
        return 0
    else:
        total = len(all_violations) + len(bad_json)
        print(f"  ❌ {total} issue(s) found — migration incomplete")
        print(f"     Violations: {len(all_violations)}")
        print(f"     JSON errors: {len(bad_json)}")
        print(f"\n  Fix the issues above and re-run this script.")
        return 1 if strict else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify TSCG tensor→structural grammar migration completeness"
    )
    parser.add_argument(
        "--root", type=Path, default=Path("."),
        help="Repository root directory (default: current directory)"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit with code 1 if any violations found"
    )
    args = parser.parse_args()
    sys.exit(run(root=args.root.resolve(), strict=args.strict))
