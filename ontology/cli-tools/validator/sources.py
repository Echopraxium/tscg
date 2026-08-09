"""
sources.py — source switch for TscgOntologyValidator (WS-5, lot 1).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/cli-tools/validator/sources.py

WHY THIS EXISTS
---------------
The corpus authority is `git show HEAD:<file>`, repeated all through the
2026-07/08 sessions. A validator that reads a stale on-disk snapshot re-introduces
exactly the defect class the whole worksite is trying to kill. So the source is
selected ONCE, before any check runs:

    local   working copy on disk           -> pre-commit self-check
    head    git show HEAD:<path>           -> THE AUTHORITY (default)
    github  raw.githubusercontent.com/...  -> validate the published state

`head` and `github` mean the validator never validates a stale snapshot; snapshot
staleness stops being a defect class.

SCOPE NOTE (lot 1)
------------------
File DISCOVERY reuses the git manifest (`git ls-files`) even in github mode: the
manifest comes from the local checkout, the CONTENT is fetched from raw GitHub.
Pure API-based discovery (api.github.com) is a follow-up and is deliberately not
built here (60/h unauthenticated rate limit; head mode is the default authority).
"""

from __future__ import annotations

import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # ontology/cli-tools/
from tscg_paths import REPO_ROOT  # noqa: E402

RAW_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/"

# Directories whose *.jsonld are NOT live corpus (backups, archives, docs, mirrors).
# Kept identical to the deprecated-term cleanup scoping so "in-scope" means one thing
# repo-wide.
_OUT_OF_SCOPE = (
    "migration_backups/",
    "domain_format_fix_backups/",
    "_archives/",
    "docs/",
    "/static/",
    "reboot-kit/",
)


def _in_scope(relpath: str) -> bool:
    return not any(marker in relpath for marker in _OUT_OF_SCOPE)


class Source:
    """Resolves file text and the in-scope manifest for one selected source."""

    def __init__(self, mode: str) -> None:
        if mode not in ("local", "head", "github"):
            raise ValueError(f"unknown source mode: {mode!r}")
        self.mode = mode

    # -- content -------------------------------------------------------------
    def read(self, relpath: str) -> str:
        if self.mode == "local":
            return (REPO_ROOT / relpath).read_text(encoding="utf-8")
        if self.mode == "head":
            out = subprocess.run(
                ["git", "show", f"HEAD:{relpath}"],
                cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
            )
            if out.returncode != 0:
                raise FileNotFoundError(f"HEAD:{relpath} -> {out.stderr.strip()}")
            return out.stdout
        # github
        with urllib.request.urlopen(RAW_BASE + relpath, timeout=30) as resp:
            return resp.read().decode("utf-8")

    # -- discovery -----------------------------------------------------------
    def manifest(self) -> List[str]:
        """All in-scope *.jsonld relpaths, tracked by git (from the local checkout)."""
        out = subprocess.run(
            ["git", "ls-files", "*.jsonld"],
            cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        if out.returncode != 0:
            raise RuntimeError(f"git ls-files failed: {out.stderr.strip()}")
        files = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
        return [f for f in files if _in_scope(f)]


def classify_layer(relpath: str) -> str | None:
    """Bucket an in-scope jsonld relpath into a GOVERNED layer, or None.

    Governed = the canonical layer corpus only, NOT sidecar dirs. Concretely:
      * M3/M2/M1 canonical files sit DIRECTLY under ontology/ (one segment).
      * M1 extensions sit under ontology/M1_extensions/<domain>/.
      * M0 = live instances under instances/.
    This deliberately drops ontology/Ref, ontology/sparql, ontology/tools,
    ontology/docs, ontology/TSCG_InstanceGrammar (template) — reference/tooling
    sidecars that are not part of the governed layer stack.
    """
    name = relpath.rsplit("/", 1)[-1]
    # canonical layer files: exactly ontology/<Name>.jsonld (no intermediate dir)
    if relpath.count("/") == 1 and relpath.startswith("ontology/"):
        if name.startswith("M3_"):
            return "M3"
        if name.startswith("M2_"):
            return "M2"
        if name.startswith("M1_"):
            return "M1"
    # M1 extensions: ontology/M1_extensions/<domain>/M1_*.jsonld
    if relpath.startswith("ontology/M1_extensions/") and name.startswith("M1_"):
        return "M1"
    # M0 live instances
    if name.startswith("M0_") and relpath.startswith("instances/"):
        return "M0"
    return None
