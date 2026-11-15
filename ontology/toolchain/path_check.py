#!/usr/bin/env python3
"""
path_check.py — PATH_CHECK: the file paths of the repository, and the paths it cites.

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0 (2026-11-15)
Home   : ontology/toolchain/path_check.py

WHY
---
Windows does not distinguish the case of file names; Linux, GitHub (raw URLs) and
GitHub Pages do. A wrong case is therefore invisible on Michel's machine and broken
online. On 2026-11-15 six instance folders were tracked in lowercase by git while the
disk had them capitalised: the M0 reasoner sweep (which listed the DISK) reported one
ERROR twice under two names, and nothing said why. This check says why, before it
breaks anything.

CHECKS (codes frozen in golden_values.json, section PATH_CHECK)
------
  PC1  Naming norm (Michel, 2026-11-15): an instance folder
       (instances/<compartment>/<Folder>/) starts with a capital letter. Folders whose
       name starts with "_" (templates, worksite notes) are exempt.
  PC2  Disk vs git case: a tracked path exists on the disk only under another case
       (one finding per mismatching path component). Always 0 on a case-sensitive
       file system; it is the Windows guard.
  PC3  Case collisions in git: two tracked paths that differ only by case (they cannot
       both exist on Windows).
  PC4  A live text file cites a repository path (repo-relative, raw.githubusercontent,
       github.io Pages or github.com blob/tree URL) whose case matches no tracked file
       or folder, while a case-insensitive match exists. A path that matches nothing at
       all is NOT reported (it may be planned, generic or external): this is a case
       check, not a link checker.

HISTORY IS NOT A DEFECT
-----------------------
PC4 skips history: backups, the ontology/Ref snapshots, docs/papers, the old Smart
Prompts, the dated housekeeping notes, test reports, and files that pin a commit in
their name (e.g. *_5a26560.md). The list is HISTORY_RE below; extend it only with a
reason.

USAGE
-----
    python ontology/toolchain/path_check.py            # counts + findings
    (the gate calls run() and compares with golden_values.json)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tscg_paths import REPO_ROOT, INSTANCE_DIRS  # noqa: E402

COMPARTMENTS = tuple(sorted(d.name for d, _ in INSTANCE_DIRS.values()))

TEXT_EXT = (".md", ".json", ".jsonld", ".js", ".mjs", ".py", ".html", ".htm", ".ttl",
            ".yaml", ".yml", ".bat", ".cmd", ".sh", ".txt", ".css", ".ebnf")

HISTORY_RE = re.compile(
    r"(^|/)[^/]*backups?/"
    r"|^ontology/Ref/"
    r"|^docs/papers/"
    r"|^docs/reboot-kit/SmartPrompts/"
    r"|^_02_housekeeping/"
    r"|/_00_test_reports/"
    r"|_[0-9a-f]{7}\.md$"
)

ROOTS = ("instances", "ontology", "docs", "kit", "src", "cli_tools", "_00_UserGuide",
         "_03_SerendipCrates")
_PATH = r"((?:%s)/[A-Za-z0-9_\-./%%]+)" % "|".join(re.escape(r) for r in ROOTS)
REF_RES = (
    re.compile(r"raw\.githubusercontent\.com/echopraxium/tscg/main/([A-Za-z0-9_\-./%]+)", re.I),
    re.compile(r"echopraxium\.github\.io/tscg/([A-Za-z0-9_\-./%]+)", re.I),
    re.compile(r"github\.com/echopraxium/tscg/(?:blob|tree)/main/([A-Za-z0-9_\-./%]+)", re.I),
    re.compile(r"(?<![A-Za-z0-9_\-./])" + _PATH),
)


# ---------------------------------------------------------------------------
def git_files(root: Path = REPO_ROOT) -> list:
    """Tracked paths, as git spells them. Raises when git cannot answer: a check that
    cannot read its input must not look like a pass."""
    p = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("git ls-files failed: " + p.stderr.decode("utf-8", "replace"))
    return [f for f in p.stdout.decode("utf-8", "replace").split("\0") if f]


def all_dirs(files) -> set:
    out = set()
    for f in files:
        parts = f.split("/")
        for i in range(1, len(parts)):
            out.add("/".join(parts[:i]))
    return out


# ---------------------------------------------------------------------------
def pc1_naming(files) -> list:
    bad = set()
    for f in files:
        parts = f.split("/")
        if len(parts) >= 4 and parts[0] == "instances" and parts[1] in COMPARTMENTS:
            name = parts[2]
            if not name.startswith("_") and not name[:1].isupper():
                bad.add("/".join(parts[:3]))
    return [("PC1", d, "instance folder must start with a capital letter") for d in sorted(bad)]


def pc2_disk_case(files, root: Path = REPO_ROOT) -> list:
    listing = {}

    def names(d: Path):
        if d not in listing:
            try:
                listing[d] = set(os.listdir(d))
            except OSError:
                listing[d] = None
        return listing[d]

    found = {}
    for f in files:
        cur = root
        parts = f.split("/")
        for i, part in enumerate(parts):
            entries = names(cur)
            if entries is None:
                break
            if part in entries:
                cur = cur / part
                continue
            twins = [e for e in entries if e.lower() == part.lower()]
            if twins:
                git_path = "/".join(parts[:i + 1])
                found.setdefault(git_path, "/".join(parts[:i] + [twins[0]]))
            break          # missing (deleted locally) or mismatched: stop here
    return [("PC2", g, f"on disk as {d}") for g, d in sorted(found.items())]


def pc3_collisions(files) -> list:
    groups = defaultdict(set)
    for p in list(files) + sorted(all_dirs(files)):
        groups[p.lower()].add(p)
    return [("PC3", " | ".join(sorted(v)), "paths differ only by case")
            for k, v in sorted(groups.items()) if len(v) > 1]


def _clean(ref: str) -> str:
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    return ref.rstrip(".,;:/)")


def pc4_refs(files, root: Path = REPO_ROOT) -> list:
    exact = set(files) | all_dirs(files)
    lower = {}
    for p in sorted(exact):
        lower.setdefault(p.lower(), p)
    out = []
    for f in files:
        if not f.lower().endswith(TEXT_EXT) or HISTORY_RE.search(f):
            continue
        try:
            text = (root / f).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        seen = set()
        for rx in REF_RES:
            for m in rx.finditer(text):
                ref = _clean(m.group(1))
                if not ref or ref in exact or ref in seen:
                    continue
                twin = lower.get(ref.lower())
                if twin and twin != ref:
                    seen.add(ref)
                    line = text.count("\n", 0, m.start()) + 1
                    out.append(("PC4", f"{f}:{line}", f"cites {ref} — tracked as {twin}"))
    return out


# ---------------------------------------------------------------------------
def findings(root: Path = REPO_ROOT) -> list:
    files = git_files(root)
    return (pc1_naming(files) + pc2_disk_case(files, root) + pc3_collisions(files)
            + pc4_refs(files, root))


def run(root: Path = REPO_ROOT) -> dict:
    """Gate entry point: errors + non-zero by_code (the shape compare() expects)."""
    try:
        fs = findings(root)
    except Exception as e:      # a crashed checker reports, never passes
        return {"_error": f"path_check crashed: {e}"}
    by_code = Counter(code for code, _, _ in fs)
    return {"errors": len(fs), "by_code": dict(sorted(by_code.items())), "_findings": fs}


def main() -> int:
    res = run()
    if "_error" in res:
        print("[XX]", res["_error"])
        return 2
    print(f"PATH_CHECK: {res['errors']} finding(s) {res['by_code']}")
    for code, where, what in res["_findings"]:
        print(f"  [{code}] {where}: {what}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
