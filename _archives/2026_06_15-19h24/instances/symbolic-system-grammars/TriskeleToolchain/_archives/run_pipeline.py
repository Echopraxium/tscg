#!/usr/bin/env python3
# run_pipeline.py
# Author: Echopraxium with the collaboration of Claude AI
# Version: 0.3.2
#
# Generic pipeline runner for TriskeleToolchain projects.
# Reads projects/<name>/pipeline.toml and runs the appropriate steps.
#
# Usage:
#   python run_pipeline.py test_main          # run test_main project
#   python run_pipeline.py wolf3d_v2_clean    # run a .tasm project
#   python run_pipeline.py --list             # list available projects

import subprocess
import sys
import os
import datetime
import tomllib   # Python 3.11+ built-in; fallback to tomli below
import argparse

# ── tomllib fallback for Python < 3.11 ───────────────────────────────────────
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: requires Python 3.11+ or 'pip install tomli'")
        sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
WORKSPACE   = os.path.dirname(os.path.abspath(__file__))
PROJECTS    = os.path.join(WORKSPACE, "projects")
LIB_DIR     = os.path.join(WORKSPACE, "lib")
REPORT_FILE = os.path.join(WORKSPACE, "pipeline_report.txt")

# ── Logging ───────────────────────────────────────────────────────────────────
lines = []

def log(msg=""):
    print(msg)
    lines.append(msg)

def save_report():
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n📄 Report: {REPORT_FILE}")

def section(label, cmd_str):
    log(f"\n{'='*60}")
    log(f"[{label}] {cmd_str}")
    log(f"{'='*60}")

# ── Command runner ────────────────────────────────────────────────────────────
def run(cmd, label, cwd=None, allow_fail=False):
    section(label, " ".join(cmd))
    r = subprocess.run(cmd, cwd=cwd or WORKSPACE,
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.stdout: log(r.stdout.rstrip())
    if r.stderr: log(r.stderr.rstrip())
    if r.returncode != 0 and not allow_fail:
        log(f"\n❌ STEP FAILED: [{label}] exit code {r.returncode}")
        log(f"   Aborting pipeline.")
        save_report()
        sys.exit(r.returncode)
    log(f"✅ [{label}] OK")
    return r.returncode

def run_vm(cmd, label, cfg):
    section(label, " ".join(cmd))
    r = subprocess.run(cmd, cwd=WORKSPACE,
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.stdout: log(r.stdout.rstrip())
    if r.stderr: log(r.stderr.rstrip())
    code = r.returncode

    # Validation for C projects with expected_exit
    val = cfg.get("validation", {})
    expected = val.get("expected_exit")
    if expected is not None:
        log(f"\n── VM Exit Code: {code} (0x{code:02X}) ──")
        if code == expected:
            log(f"✅ ALL TESTS PASSED (0x{expected:02X} = {expected})")
        else:
            log(f"❌ expected {expected} (0x{expected:02X})")
            tests = val.get("tests", [])
            for i, t in enumerate(tests):
                bit = 1 << i
                status = "✅" if (code & bit) else "❌"
                log(f"   {status} Test {i+1}: {t}")
    else:
        log(f"\n── VM Exit Code: {code} (0x{code:02X}) ──")
        if code == 0:
            log("✅ Exit 0")
        else:
            log(f"⚠️  Exit {code}")
    return code

# ── Pipeline types ────────────────────────────────────────────────────────────

def pipeline_tasm(cfg, proj_dir, target_dir):
    """Pipeline for .tasm projects: tsk-asm → .tobj → tsk-link → .tvmx → VM"""
    name    = cfg["name"]
    sources = cfg["sources"]
    entry   = cfg.get("entry", "main")
    libs    = cfg.get("libs", [])

    tobj_files = []
    for src in sources:
        src_path  = os.path.join(proj_dir, src)
        stem      = os.path.splitext(os.path.basename(src))[0]
        tobj_path = os.path.join(target_dir, stem + ".tobj")
        run(["cargo", "run", "-p", "tsk-asm", "--",
             src_path, "-o", tobj_path],
            f"tsk-asm {stem}")
        tobj_files.append(tobj_path)

    tvmx_path = os.path.join(target_dir, name + ".tvmx")
    lib_paths = [os.path.join(LIB_DIR, l) for l in libs]
    run(["cargo", "run", "-p", "tsk-link", "--"] +
        tobj_files + lib_paths +
        ["-o", tvmx_path, "--entry", entry, "--verbose", "--dump-symbols"],
        "tsk-link")

    return tvmx_path

def pipeline_c(cfg, proj_dir, target_dir):
    """Pipeline for .c projects: clang → .ll → tsk-cc → .tobj → tsk-link → .tvmx"""
    name         = cfg["name"]
    sources      = cfg["sources"]
    entry        = cfg.get("entry", "main")
    libs         = cfg.get("libs", [])
    include_dirs = cfg.get("include_dirs", [])

    tobj_files = []
    for src in sources:
        src_path = os.path.join(proj_dir, src)
        stem     = os.path.splitext(os.path.basename(src))[0]
        ll_path  = os.path.join(target_dir, stem + ".ll")
        tobj_path= os.path.join(target_dir, stem + ".tobj")

        # clang -O0 → .ll
        clang_cmd = ["clang", "-O0", "-S", "-emit-llvm", "-o", ll_path, src_path]
        for inc in include_dirs:
            clang_cmd += ["-I", os.path.join(proj_dir, inc)]
        run(clang_cmd, f"clang {stem}")

        # tsk-cc → .tobj
        run(["cargo", "run", "-p", "tsk-cc", "--",
             ll_path, "-o", tobj_path, "--verbose"],
            f"tsk-cc {stem}")
        tobj_files.append(tobj_path)

    # tsk-link → .tvmx
    tvmx_path = os.path.join(target_dir, name + ".tvmx")
    lib_paths = [os.path.join(LIB_DIR, l) for l in libs
                 if os.path.exists(os.path.join(LIB_DIR, l))]
    run(["cargo", "run", "-p", "tsk-link", "--"] +
        tobj_files + lib_paths +
        ["-o", tvmx_path, "--entry", entry, "--verbose", "--dump-symbols"],
        "tsk-link")

    return tvmx_path

# ── Main ──────────────────────────────────────────────────────────────────────

def list_projects():
    print("Available projects:")
    for p in sorted(os.listdir(PROJECTS)):
        toml_path = os.path.join(PROJECTS, p, "pipeline.toml")
        if os.path.isfile(toml_path):
            with open(toml_path, "rb") as f:
                cfg = tomllib.load(f)
            ptype = cfg.get("type", "?")
            print(f"  {p:<30} [{ptype}]")

def main():
    parser = argparse.ArgumentParser(
        description="TriskeleToolchain pipeline runner v0.3.2")
    parser.add_argument("project", nargs="?",
                        help="Project name (subfolder of projects/)")
    parser.add_argument("--list", action="store_true",
                        help="List available projects")
    parser.add_argument("--no-clean", action="store_true",
                        help="Skip cargo clean steps")
    args = parser.parse_args()

    if args.list or not args.project:
        list_projects()
        return

    # Load pipeline.toml
    proj_dir  = os.path.join(PROJECTS, args.project)
    toml_path = os.path.join(proj_dir, "pipeline.toml")
    if not os.path.isfile(toml_path):
        print(f"ERROR: project '{args.project}' not found or missing pipeline.toml")
        print(f"       Expected: {toml_path}")
        list_projects()
        sys.exit(1)

    with open(toml_path, "rb") as f:
        cfg = tomllib.load(f)

    target_dir = os.path.join(proj_dir, "target")
    os.makedirs(target_dir, exist_ok=True)

    # Header
    log(f"TriskeleToolchain Pipeline Report")
    log(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Workspace: {WORKSPACE}")
    log(f"Project  : {args.project}  [{cfg.get('type','?')}]")

    # Optional clean
    if not args.no_clean:
        run(["cargo", "clean", "-p", "tsk-cc"],   "  clean tsk-cc",   allow_fail=True)
        run(["cargo", "clean", "-p", "tsk-link"],  "  clean tsk-link", allow_fail=True)

    # Run pipeline by type
    ptype = cfg.get("type", "tasm")
    if ptype == "tasm":
        tvmx = pipeline_tasm(cfg, proj_dir, target_dir)
    elif ptype == "c":
        tvmx = pipeline_c(cfg, proj_dir, target_dir)
    else:
        print(f"ERROR: unknown pipeline type '{ptype}'")
        sys.exit(1)

    # Run VM
    code = run_vm(["cargo", "run", "-p", "triskele-vm", "--", tvmx, "--trace"],
                  "tskvm", cfg)

    save_report()
    val = cfg.get("validation", {})
    expected = val.get("expected_exit")
    if expected is not None:
        sys.exit(0 if code == expected else 1)
    else:
        sys.exit(0 if code == 0 else code)

if __name__ == "__main__":
    main()
