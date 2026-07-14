"""
tscg_paths — repository-root resolution for TSCG cli-tools.

Author : Echopraxium with the collaboration of Claude AI
Version: 1.2.0
Date   : 2026-07-13
Home   : ontology/cli-tools/tscg_paths.py

WHY THIS EXISTS
---------------
The M0/M1 scripts used to hardcode an absolute path:

    REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")

Which meant they never used their own location to find the repository. They
worked on exactly one machine, one OS, one clone. Moving them anywhere was a
no-op (they still pointed at E:/), and running them from a CI box, a Linux
sandbox, or a second clone silently operated on the wrong tree — or on nothing.

This module resolves the repository root by walking UP from the script's own
location until it finds the structural marker of the TSCG repo: a directory that
contains BOTH `ontology/` and `instances/`. Scripts become relocatable: they work
from ontology/cli-tools/, from cli_tools/, from a subfolder of either, unchanged.

USAGE
-----
Scripts live one level down (ontology/cli-tools/check-M0/, .../check-M1/), so they
bootstrap the import by putting this module's directory on sys.path first:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # ontology/cli-tools/

    from tscg_paths import REPO_ROOT, ONTOLOGY_DIR, INSTANCES_ROOT, find_schema

    shacl = find_schema("M0_Instances_Schema_shacl.ttl", script_dir=Path(__file__).parent)

An explicit override remains available for the odd case (CI, a detached checkout):

    TSCG_REPO_ROOT=/path/to/tscg  python check_m0_instances.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Sequence

__version__ = "1.2.0"

# The structural signature of the TSCG repository root.
# Both must be present — `ontology/` alone would also match a nested checkout.
_MARKERS = ("ontology", "instances")


class RepoRootNotFound(RuntimeError):
    """Raised when the TSCG repository root cannot be located."""


def _is_repo_root(path: Path) -> bool:
    return all((path / m).is_dir() for m in _MARKERS)


def find_repo_root(start: Optional[Path] = None) -> Path:
    """
    Walk up from `start` (default: this file) until a directory containing both
    `ontology/` and `instances/` is found.

    Honours the TSCG_REPO_ROOT environment variable, which wins over discovery.
    """
    env = os.environ.get("TSCG_REPO_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if not _is_repo_root(p):
            raise RepoRootNotFound(
                f"TSCG_REPO_ROOT={p} does not look like the TSCG repo "
                f"(expected sub-directories: {', '.join(_MARKERS)})."
            )
        return p

    here = (start or Path(__file__)).resolve()
    for candidate in (here, *here.parents):
        if candidate.is_dir() and _is_repo_root(candidate):
            return candidate

    raise RepoRootNotFound(
        f"Could not locate the TSCG repository root by walking up from {here}.\n"
        f"Expected an ancestor directory containing both {' and '.join(_MARKERS)}/.\n"
        f"Set TSCG_REPO_ROOT explicitly if the layout is non-standard."
    )


REPO_ROOT: Path = find_repo_root()
ONTOLOGY_DIR: Path = REPO_ROOT / "ontology"
INSTANCES_ROOT: Path = REPO_ROOT / "instances"
CLI_TOOLS_DIR: Path = Path(__file__).parent.resolve()

# Canonical base URIs (single source of truth — do not re-declare in scripts).
BASE_ONTOLOGY = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
BASE_INSTANCES = "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/"

# ---------------------------------------------------------------------------
# Instance compartments.
#
# ⚠ `symbolic-system-grammars` is PLURAL. The previous scripts wrote it in the
# singular, so `base_dir.exists()` was False and the whole SymbolicSystemGrammar
# category was skipped IN SILENCE — Iching and TriskeleToolchain were never
# checked and never migrated. `verify_layout()` below exists so that this class
# of typo is reported instead of swallowed.
# ---------------------------------------------------------------------------
INSTANCE_DIRS = {
    "poclet":             (INSTANCES_ROOT / "poclets",                   "m3:Poclet"),
    "systemic_framework": (INSTANCES_ROOT / "systemic-frameworks",       "m3:SystemicFramework"),
    "symbolic_grammar":   (INSTANCES_ROOT / "symbolic-system-grammars",  "m3:SymbolicSystemGrammar"),
    "tscg_tool":          (INSTANCES_ROOT / "tscg-tools",                "m3:TscgTool"),
    "transdisclet":       (INSTANCES_ROOT / "transdisclet",              "m3:TransDisclet"),
}

# ---------------------------------------------------------------------------
# A missing compartment is NOT one thing. Two very different cases hide behind it,
# and conflating them is itself a bug:
#
#   PLANNED-BUT-EMPTY  — `transdisclet/` has never been populated. Its absence skips
#                        nothing, because there is nothing to skip. → WARN.
#   MISSPELLED         — `symbolic-system-grammar` (singular) vs the real
#                        `symbolic-system-grammars`. The directory "does not exist",
#                        so an entire populated category (Iching, TriskeleToolchain)
#                        was silently dropped from every run. → BLOCK.
#
# Only REQUIRED compartments block. Treating both as fatal would make the gate cry wolf
# on an empty folder — and a gate that cries wolf is a gate people learn to ignore, which
# is exactly how the 479 violations stayed invisible for six months.
# ---------------------------------------------------------------------------
REQUIRED_COMPARTMENTS = {"poclet", "systemic_framework", "symbolic_grammar", "tscg_tool"}
OPTIONAL_COMPARTMENTS = {"transdisclet"}   # planned; empty is legitimate


def verify_layout(warn=print) -> dict:
    """
    Check every instance compartment. Returns {"blocking": [...], "optional": [...]}.

    `blocking` is non-empty only when a REQUIRED compartment is absent — which means a
    populated category is being silently dropped from the totals. That is fatal: a total
    computed over a silently skipped category is worse than no total at all.

    `optional` compartments (planned, never populated) are reported but do not block.
    """
    blocking, optional = [], []
    for name, (path, _) in INSTANCE_DIRS.items():
        if path.is_dir():
            continue
        if name in REQUIRED_COMPARTMENTS:
            blocking.append((name, path))
            warn(
                f"[layout] ERROR: REQUIRED compartment '{name}' not found at {path}.\n"
                f"          Every instance it holds is being SKIPPED — SILENTLY. Check the\n"
                f"          directory name first (the M0 scripts used to spell\n"
                f"          'symbolic-system-grammar' in the SINGULAR while the directory is\n"
                f"          PLURAL, and the whole category vanished from every run without a\n"
                f"          word). Do not trust any total until this is resolved."
            )
        else:
            optional.append((name, path))
            warn(
                f"[layout] note: optional compartment '{name}' is absent ({path.name}/). "
                f"Planned but never populated — nothing is being skipped."
            )
    return {"blocking": blocking, "optional": optional}


def find_schema(*names: str,
                script_dir: Optional[Path] = None,
                extra_dirs: Sequence[Path] = ()) -> Optional[Path]:
    """
    Locate a SHACL schema, trying each name in each search directory, in order:

        1. `script_dir`   — the CALLING script's own folder (a local copy wins)
        2. CLI_TOOLS_DIR  — ontology/cli-tools/
        3. ONTOLOGY_DIR   — ontology/  (where the canonical schemas live)
        4. `extra_dirs`

    Pass EVERY spelling you have ever used. The M1 checker used to look for
    "M1_Schema.shacl.ttl" (dot) while the file on disk is "M1_Schema_shacl.ttl"
    (underscore), so `--shacl` silently found nothing and validated nothing. A
    validator that cannot find its grammar must not look like a validator that
    passed.
    """
    search_dirs = [d for d in (script_dir, CLI_TOOLS_DIR, ONTOLOGY_DIR, *extra_dirs) if d]
    for directory in search_dirs:
        for name in names:
            candidate = Path(directory) / name
            if candidate.exists():
                return candidate
    return None


if __name__ == "__main__":
    print(f"tscg_paths v{__version__}")
    print(f"  REPO_ROOT      : {REPO_ROOT}")
    print(f"  ONTOLOGY_DIR   : {ONTOLOGY_DIR}")
    print(f"  INSTANCES_ROOT : {INSTANCES_ROOT}")
    print(f"  CLI_TOOLS_DIR  : {CLI_TOOLS_DIR}")
    print()
    layout = verify_layout()
    if not layout["blocking"] and not layout["optional"]:
        print("  [layout] all instance compartments present.")
    elif not layout["blocking"]:
        print("  [layout] all REQUIRED compartments present.")
