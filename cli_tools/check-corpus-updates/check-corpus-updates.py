"""
check-corpus-updates.py — TSCG Corpus Version Checker
======================================================
Compares file versions declared in TSCG_Reference_Corpus.md
against actual versions found in local repo files.

Location : cli-tools/check-corpus-updates/
Usage    : python check-corpus-updates.py [--verbose] [--json] [--fix-corpus]

Author   : Echopraxium with the collaboration of Claude AI
Version  : 1.0.0
"""

import re
import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── Repo root (2 levels up from cli-tools/check-corpus-updates/) ─────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT  = SCRIPT_DIR.parent.parent.resolve()

CORPUS_FILE = REPO_ROOT / "docs" / "reboot-kit" / "TSCG_Reference_Corpus.md"
if not CORPUS_FILE.exists():
    # Fallback — project knowledge location
    CORPUS_FILE = REPO_ROOT / "ontology" / "TSCG_Reference_Corpus.md"

# ── Search paths for each file category ──────────────────────────────────────
SEARCH_PATHS = [
    REPO_ROOT / "ontology",
    REPO_ROOT / "instances",
    REPO_ROOT / "docs",
    REPO_ROOT,
]


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CorpusEntry:
    filename:        str
    corpus_version:  Optional[str]   # version declared in corpus
    status:          str              # "active", "archived", "obsolete"
    notes:           str = ""


@dataclass
class CheckResult:
    filename:        str
    corpus_version:  Optional[str]
    actual_version:  Optional[str]
    local_path:      Optional[Path]
    status:          str              # ok | mismatch | missing | no_version | archived
    message:         str = ""


# =============================================================================
# CORPUS PARSER
# =============================================================================

def parse_corpus(corpus_path: Path) -> list[CorpusEntry]:
    """
    Parse TSCG_Reference_Corpus.md and extract (filename, version, status).

    Handles three formats:
      1. Inline bullet:  **`File.jsonld`** ✅ v2.8.0
      2. Table row:      | `File.jsonld` | 2.8.0 | ...
      3. No version:     **`File.md`** ✅ — description text
    """
    entries: list[CorpusEntry] = []
    seen: set[str] = set()

    with open(corpus_path, encoding="utf-8") as f:
        lines = f.readlines()

    # ── Pattern 1: bullet line  **`filename`** [status] [vX.Y.Z] ─────────────
    # e.g. - **`M3_GenesisGrammar.jsonld`** ✅ v4.2.0
    # e.g. - **`TerritoryMap_Dichotomy.md`** ✅ v16.0+ (2026-05-23)
    # e.g. - **`M3_BicephalousPerspective.jsonld`** ⚠️ `[ARCHIVED]`
    bullet_re = re.compile(
        r'^\s*[-*]?\s*\*\*`([^`]+)`\*\*'           # **`filename`**
        r'(?:\s*(✅|⚠️|❌))?'                        # optional status emoji
        r'(?:\s*`\[ARCHIVED\]`)?'                   # optional [ARCHIVED]
        r'(?:[^v\n]*v(\d+[\d.+]+))?',               # optional vX.Y.Z
        re.UNICODE
    )

    # ── Pattern 2: markdown table row  | `filename` | version | ... ──────────
    # e.g. | `M3_EagleEye.jsonld` | 2.8.0 | ...
    table_re = re.compile(
        r'^\|\s*`([^`]+)`\s*\|\s*([^\|]+?)\s*\|'
    )

    # ── Pattern 3: table row with **bold** name | **Name** | version | ... ───
    # e.g. | **TscgOntologyExplorer** | 1.0 | ...
    bold_table_re = re.compile(
        r'^\|\s*\*\*([^*]+)\*\*\s*\|\s*([^\|]+?)\s*\|'
    )

    def _add(filename: str, version_str: str, status: str):
        filename = filename.strip()
        if not filename or filename in seen:
            return
        # Normalize version string
        v = version_str.strip() if version_str else None
        if v and re.match(r'^\d', v):
            # Keep only the semver part (strip trailing text)
            v = re.split(r'[\s(]', v)[0].rstrip('+')
        else:
            v = None
        seen.add(filename)
        entries.append(CorpusEntry(filename=filename, corpus_version=v, status=status))

    for line in lines:
        # Bullet pattern
        m = bullet_re.search(line)
        if m:
            filename   = m.group(1)
            emoji      = m.group(2) or ""
            version    = m.group(3)
            archived   = "[ARCHIVED]" in line or "⚠️" in emoji
            obsolete   = "❌" in emoji
            status     = "archived" if archived else ("obsolete" if obsolete else "active")
            _add(filename, version, status)
            continue

        # Table pattern with backtick name
        m = table_re.search(line)
        if m:
            filename = m.group(1)
            version  = m.group(2).strip()
            # Skip header rows and separator rows
            if version in ("Version", "---", "v", ""):
                continue
            _add(filename, version, "active")
            continue

        # Table pattern with bold name (TscgTools, SystemicFrameworks…)
        m = bold_table_re.search(line)
        if m:
            name    = m.group(1).strip()
            version = m.group(2).strip()
            if version in ("Version", "v", "---", ""):
                continue
            # Construct likely filename
            filename = f"M0_{name}.jsonld"
            _add(filename, version, "active")

    return entries


# =============================================================================
# VERSION EXTRACTOR (local files)
# =============================================================================

def find_local_file(filename: str) -> Optional[Path]:
    """Search for a file across all known repo directories."""
    for base in SEARCH_PATHS:
        for path in base.rglob(filename):
            # Skip _archives and backup directories
            parts = path.parts
            if any(p.startswith("_") or "backup" in p.lower() or "archive" in p.lower()
                   for p in parts):
                continue
            return path
    return None


def extract_version_jsonld(path: Path) -> Optional[str]:
    """Extract owl:versionInfo from a JSON-LD file."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None

    # Search in @graph nodes
    for node in data.get("@graph", [data]):
        v = node.get("owl:versionInfo")
        if v:
            return str(v).strip()

    # Root level
    v = data.get("owl:versionInfo")
    if v:
        return str(v).strip()

    return None


def extract_version_md(path: Path) -> Optional[str]:
    """Extract version from a Markdown file.

    Looks for patterns like:
      **Version**: 2.8.0
      Version: 2.8.0
      # Title v2.8.0
      v2.8.0
    """
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    patterns = [
        r'\*\*[Vv]ersion\*\*\s*[:\-]\s*v?([\d]+\.[\d.]+)',
        r'^[Vv]ersion\s*[:\-]\s*v?([\d]+\.[\d.]+)',
        r'^\s*#[^#].*v([\d]+\.[\d.]+)\b',
        r'\bv([\d]+\.[\d]+\.[\d]+)\b',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.MULTILINE)
        if m:
            return m.group(1)
    return None


def extract_version_ttl(path: Path) -> Optional[str]:
    """Extract version from a Turtle SHACL file."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    m = re.search(r'#.*[Vv]ersion\s+v?([\d]+\.[\d.]+)', content)
    if m:
        return m.group(1)
    return None


def get_local_version(path: Path) -> Optional[str]:
    suffix = path.suffix.lower()
    if suffix in (".jsonld", ".json"):
        return extract_version_jsonld(path)
    elif suffix == ".md":
        return extract_version_md(path)
    elif suffix == ".ttl":
        return extract_version_ttl(path)
    return None


# =============================================================================
# VERSION COMPARISON
# =============================================================================

def parse_semver(v: str) -> tuple:
    """Parse a version string into a comparable tuple."""
    try:
        parts = re.split(r'[.\-]', v.strip())
        return tuple(int(p) for p in parts if p.isdigit())
    except Exception:
        return (0,)


def compare_versions(corpus_v: str, actual_v: str) -> str:
    """Returns 'ok', 'ahead', or 'behind'."""
    c = parse_semver(corpus_v)
    a = parse_semver(actual_v)
    if a == c:
        return "ok"
    if a > c:
        return "ahead"   # local is newer → corpus is outdated
    return "behind"      # local is older → file may be outdated


# =============================================================================
# MAIN CHECK LOGIC
# =============================================================================

def check_corpus(corpus_path: Path, verbose: bool = False) -> list[CheckResult]:
    entries = parse_corpus(corpus_path)
    results = []

    for entry in entries:
        local_path = find_local_file(entry.filename)

        if entry.status in ("archived", "obsolete"):
            if verbose:
                results.append(CheckResult(
                    filename=entry.filename,
                    corpus_version=entry.corpus_version,
                    actual_version=None,
                    local_path=local_path,
                    status="archived",
                    message="Marked as archived/obsolete in corpus — skipped"
                ))
            continue

        if not local_path:
            results.append(CheckResult(
                filename=entry.filename,
                corpus_version=entry.corpus_version,
                actual_version=None,
                local_path=None,
                status="missing",
                message="File not found in repo"
            ))
            continue

        actual_v = get_local_version(local_path)

        if not entry.corpus_version:
            # No version declared in corpus — just report presence
            results.append(CheckResult(
                filename=entry.filename,
                corpus_version=None,
                actual_version=actual_v,
                local_path=local_path,
                status="no_version",
                message=f"No version in corpus — local: {actual_v or '(none)'}"
            ))
            continue

        if not actual_v:
            results.append(CheckResult(
                filename=entry.filename,
                corpus_version=entry.corpus_version,
                actual_version=None,
                local_path=local_path,
                status="no_version",
                message=f"Corpus: {entry.corpus_version} — cannot read local version"
            ))
            continue

        cmp = compare_versions(entry.corpus_version, actual_v)
        if cmp == "ok":
            results.append(CheckResult(
                filename=entry.filename,
                corpus_version=entry.corpus_version,
                actual_version=actual_v,
                local_path=local_path,
                status="ok",
                message="✅ In sync"
            ))
        elif cmp == "ahead":
            results.append(CheckResult(
                filename=entry.filename,
                corpus_version=entry.corpus_version,
                actual_version=actual_v,
                local_path=local_path,
                status="mismatch",
                message=f"⚠️  Local is NEWER than corpus: local={actual_v}  corpus={entry.corpus_version} → update corpus"
            ))
        else:
            results.append(CheckResult(
                filename=entry.filename,
                corpus_version=entry.corpus_version,
                actual_version=actual_v,
                local_path=local_path,
                status="mismatch",
                message=f"❌ Local is OLDER than corpus: local={actual_v}  corpus={entry.corpus_version} → file may need update"
            ))

    return results


# =============================================================================
# REPORT
# =============================================================================

def print_report(results: list[CheckResult], verbose: bool = False):
    ok        = [r for r in results if r.status == "ok"]
    mismatch  = [r for r in results if r.status == "mismatch"]
    missing   = [r for r in results if r.status == "missing"]
    no_ver    = [r for r in results if r.status == "no_version"]
    archived  = [r for r in results if r.status == "archived"]

    print()
    print("=" * 70)
    print(" TSCG Corpus Version Check")
    print("=" * 70)
    print(f"  Corpus file : {CORPUS_FILE}")
    print(f"  Repo root   : {REPO_ROOT}")
    print(f"  Entries     : {len(results)+len(archived)} parsed")
    print()

    if mismatch:
        print(f"── MISMATCHES ({len(mismatch)}) " + "─" * 40)
        for r in mismatch:
            print(f"  {r.filename}")
            print(f"    {r.message}")
            if r.local_path:
                print(f"    Path: {r.local_path}")
        print()

    if missing:
        print(f"── MISSING FILES ({len(missing)}) " + "─" * 38)
        for r in missing:
            print(f"  {r.filename}  (corpus says: v{r.corpus_version or '?'})")
        print()

    if no_ver:
        print(f"── NO VERSION DECLARED ({len(no_ver)}) " + "─" * 33)
        for r in no_ver:
            print(f"  {r.filename}  — {r.message}")
        print()

    if verbose and ok:
        print(f"── IN SYNC ({len(ok)}) " + "─" * 47)
        for r in ok:
            print(f"  ✅  {r.filename:45s} v{r.corpus_version}")
        print()

    print("=" * 70)
    print(f"  ✅ In sync    : {len(ok)}")
    print(f"  ⚠️  Mismatch  : {len(mismatch)}")
    print(f"  ❌ Missing    : {len(missing)}")
    print(f"  ℹ️  No version : {len(no_ver)}")
    if archived:
        print(f"  📦 Archived   : {len(archived)} (skipped)")
    print("=" * 70)
    print()

    if not mismatch and not missing:
        print("  🎉 All active corpus entries are in sync with local repo!")
    else:
        print("  Action required — see mismatches and missing files above.")
    print()


def print_json(results: list[CheckResult]):
    out = []
    for r in results:
        out.append({
            "filename":       r.filename,
            "status":         r.status,
            "corpus_version": r.corpus_version,
            "actual_version": r.actual_version,
            "local_path":     str(r.local_path) if r.local_path else None,
            "message":        r.message,
        })
    print(json.dumps(out, indent=2, ensure_ascii=False))


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Check TSCG corpus file versions against local repo."
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Also show files that are in sync"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--corpus", default=None,
        help=f"Path to TSCG_Reference_Corpus.md (default: {CORPUS_FILE})"
    )
    args = parser.parse_args()

    corpus_path = Path(args.corpus) if args.corpus else CORPUS_FILE
    if not corpus_path.exists():
        print(f"ERROR: Corpus file not found: {corpus_path}", file=sys.stderr)
        print(f"  Expected at: {CORPUS_FILE}", file=sys.stderr)
        sys.exit(1)

    results = check_corpus(corpus_path, verbose=args.verbose)

    if args.json:
        print_json(results)
    else:
        print_report(results, verbose=args.verbose)

    # Exit code: 0 = all good, 1 = mismatches/missing
    issues = [r for r in results if r.status in ("mismatch", "missing")]
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
