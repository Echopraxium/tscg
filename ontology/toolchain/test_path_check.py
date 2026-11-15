#!/usr/bin/env python3
"""
test_path_check.py — negative tests for PATH_CHECK (PC1–PC4).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0 (2026-11-15)
Home   : ontology/toolchain/test_path_check.py

Every check must be able to FAIL. Each test feeds a small synthetic tree (a list of
tracked paths, and for PC2/PC4 a temporary folder) and asserts the exact number of
findings, then the clean counterpart (0).

Run:  python ontology/toolchain/test_path_check.py   (exit 0 iff all pass)
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import path_check as pc  # noqa: E402

FAILURES = []

# The wrong-case fixtures are assembled at run time: written out literally, they would
# be wrong-case references in a tracked file, and PC4 would (rightly) count them.
LOW, LOW_Y, UP = "z" + "eta", "y" + "ggdrasil", "M0_" + "ZETA"


def check(name, got, exp):
    ok = got == exp
    print(f"  [{'OK' if ok else 'XX'}] {name}: {got}" + ("" if ok else f" (expected {exp})"))
    if not ok:
        FAILURES.append(name)


def make(root: Path, paths, text=None):
    for p in paths:
        f = root / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text((text or {}).get(p, ""), encoding="utf-8")


def main() -> int:
    # PC1 — naming norm
    files = [f"instances/poclets/{LOW}/M0_Zeta.jsonld", "instances/poclets/Zeta2/M0_Zeta2.jsonld",
             "instances/poclets/_00_template/x.md", "instances/tscg-tools/tool/a.py",
             "instances/_01_Worksite/note.md", "docs/lower/x.md"]
    check("PC1 lowercase instance folders", len(pc.pc1_naming(files)), 2)
    check("PC1 clean", len(pc.pc1_naming(["instances/poclets/Zeta/M0_Zeta.jsonld"])), 0)

    # PC3 — case collisions (a file pair and a folder pair)
    check("PC3 file + folder collisions",
          len(pc.pc3_collisions(["a/B.md", "a/b.md", "X/1.md", "x/2.md"])), 2)
    check("PC3 clean", len(pc.pc3_collisions(["a/B.md", "a/C.md"])), 0)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        # PC2 — disk vs git case. os.listdir returns the names as stored, so the test
        # behaves the same on a case-sensitive (Linux) and a case-insensitive (Windows) disk.
        make(root, ["instances/poclets/Yggdrasil/M0_Yggdrasil.jsonld"])
        got = len(pc.pc2_disk_case([f"instances/poclets/{LOW_Y}/M0_Yggdrasil.jsonld"], root))
        check("PC2 git lowercase, disk capitalised", got, 1)
        check("PC2 clean", len(pc.pc2_disk_case(
            ["instances/poclets/Yggdrasil/M0_Yggdrasil.jsonld"], root)), 0)
        check("PC2 file missing on disk is not a case finding", len(pc.pc2_disk_case(
            ["instances/poclets/Gone/M0_Gone.jsonld"], root)), 0)

        # PC4 — references with a wrong case
        tracked = ["instances/poclets/Zeta/sim/index.html", "instances/poclets/Zeta/M0_Zeta.jsonld",
                   "docs/a.md", "ontology/Ref/old.md", "instances/x_backups/b.md"]
        texts = {
            "docs/a.md": (f"see instances/poclets/{LOW}/sim and "
                          f"https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/Zeta/{UP}.jsonld#x "
                          f"and https://echopraxium.github.io/tscg/instances/poclets/{LOW}/sim/index.html "
                          "and instances/poclets/Zeta/sim (ok) and instances/poclets/Nowhere/x.md (unknown)"),
            "ontology/Ref/old.md": f"instances/poclets/{LOW}/sim",       # history: skipped
            "instances/x_backups/b.md": f"instances/poclets/{LOW}/sim",  # backup: skipped
        }
        make(root, tracked, texts)
        check("PC4 three wrong-case references, history skipped", len(pc.pc4_refs(tracked, root)), 3)
        (root / "docs/a.md").write_text("instances/poclets/Zeta/sim and instances/poclets/Zeta/M0_Zeta.jsonld",
                                        encoding="utf-8")
        check("PC4 clean", len(pc.pc4_refs(tracked, root)), 0)

    res = pc.run()
    check("run() on the repository returns counts, not an error", "_error" in res, False)

    print(f"\n{'PASS' if not FAILURES else 'FAIL'}: {len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
