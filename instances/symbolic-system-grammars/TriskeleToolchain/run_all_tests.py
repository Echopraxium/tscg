#!/usr/bin/env python3
# run_all_tests.py — TriskeleToolchain full validation suite
# Author: Echopraxium with the collaboration of Claude AI
# Version: 0.3.11
#
# Usage:
#   python run_all_tests.py              # run all 12 projects
#   python run_all_tests.py --clean      # with cargo clean first
#   python run_all_tests.py --keep-going # continue on failure (default)
#   python run_all_tests.py --stop       # stop on first failure
#
# Exit: 0 if all pass, 1 if any fail.

import subprocess
import sys
import os

# ── Validation suite ─────────────────────────────────────────────────────────
# Each entry: (project_path, expected_exit_code)

PROJECTS = [
    # Toolchain base tests
    ("toolchain-tests/c89/test_main",              31),
    ("toolchain-tests/c89/test_patterns",          15),
    ("toolchain-tests/c89/test_select",             9),
    ("toolchain-tests/c89/test_variadic",         255),
    ("toolchain-tests/c89/test_doom_libc",        511),
    # Wolf3D
    ("wolfenstein3D/wolf3d",                       15),
    # DoomGeneric modules
    ("Doom-Generic/vm-porting/tests/doom_fixed",  127),
    ("Doom-Generic/vm-porting/tests/doom_alloc",  255),
    ("Doom-Generic/vm-porting/tests/doom_zzone",  255),
    ("Doom-Generic/vm-porting/tests/doom_math",   127),
    ("Doom-Generic/vm-porting/tests/doom_argv",    63),
    ("Doom-Generic/vm-porting/tests/doom_wad",    255),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"

def run_project(path, expected_exit, clean=False):
    cmd = [sys.executable, "run_pipeline.py", path]
    if clean:
        cmd.append("--clean")
    result = subprocess.run(cmd, capture_output=False)
    # run_pipeline.py already validates the VM's exit code against
    # expected_exit internally (see its run_vm()/main()) and translates
    # the result to 0 (pass) / 1 (fail) — NOT the raw VM exit code.
    # So here we just check for that pass/fail signal; the raw VM exit
    # code and the detailed per-test breakdown are visible in
    # run_pipeline.py's own printed report / pipeline_report.txt.
    ok = (result.returncode == 0)
    status = f"{GREEN}✅{RESET}" if ok else f"{RED}❌{RESET}"
    print(f"  {status}  {path:<55}  pipeline_exit={result.returncode}"
          + ("" if ok else f"  (expected VM exit {expected_exit} — see report above)"))
    return ok

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    clean     = "--clean"     in sys.argv
    stop_fail = "--stop"      in sys.argv

    print(f"\n{'='*70}")
    print(f"  TriskeleToolchain — Full Validation Suite v0.3.11")
    print(f"  Projects root : {os.path.abspath('projects')}")
    if clean:
        print(f"  Mode          : --clean")
    print(f"{'='*70}\n")

    passed = 0
    failed = 0

    for path, expected in PROJECTS:
        ok = run_project(path, expected, clean=clean)
        if ok:
            passed += 1
        else:
            failed += 1
            if stop_fail:
                print(f"\n{RED}Stopped on first failure.{RESET}")
                break

    total = passed + failed
    print(f"\n{'='*70}")
    if failed == 0:
        print(f"  {GREEN}✅ ALL {total}/{total} PASSED{RESET}")
    else:
        print(f"  {RED}❌ {failed}/{total} FAILED  ({passed} passed){RESET}")
    print(f"{'='*70}\n")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
