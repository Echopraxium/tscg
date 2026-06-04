#!/usr/bin/env python3
# run_pipeline.py
# Author: Echopraxium with the collaboration of Claude AI
# Pipeline: test_main.c -> .ll -> .tobj -> .tvmx -> VM

import subprocess
import sys
import os
import datetime

# ── Configuration ─────────────────────────────────────────────────────────────
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
C    = "lib/samples/test_main.c"
LL   = "lib/samples/test_main.ll"
TOBJ = "lib/samples/test_main.tobj"
TVMX = "lib/samples/test_main.tvmx"
REPORT = "pipeline_report.txt"

lines = []  # accumulate report lines

def log(msg=""):
    print(msg)
    lines.append(msg)

def save_report(final_status):
    report_path = os.path.join(WORKSPACE, REPORT)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n📄 Report saved: {report_path}")

def run(cmd, label):
    log(f"\n{'='*60}")
    log(f"[{label}] {' '.join(cmd)}")
    log(f"{'='*60}")
    r = subprocess.run(cmd, cwd=WORKSPACE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "RUST_LOG": "warn"})
    if r.stdout: log(r.stdout.rstrip())
    if r.stderr: log(r.stderr.rstrip())
    if r.returncode != 0:
        log(f"\n❌ STEP FAILED: [{label}] exit code {r.returncode}")
        log(f"   Aborting pipeline.")
        save_report("FAILED")
        sys.exit(r.returncode)
    log(f"✅ [{label}] OK")

def run_vm(cmd, label):
    log(f"\n{'='*60}")
    log(f"[{label}] {' '.join(cmd)}")
    log(f"{'='*60}")
    r = subprocess.run(cmd, cwd=WORKSPACE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.stdout: log(r.stdout.rstrip())
    if r.stderr: log(r.stderr.rstrip())
    code = r.returncode
    log(f"\n── VM Exit Code: {code} (0x{code:02X}) ──")
    if code == 31:
        log(f"✅ ALL TESTS PASSED (0x1F = 31)")
    else:
        log(f"❌ expected 31 (0x1F)")
        passed = [i+1 for i in range(5) if code & (1 << i)]
        failed = [i+1 for i in range(5) if not (code & (1 << i))]
        log(f"   Tests passed : {passed}")
        log(f"   Tests failed : {failed}")
        log(f"   Test legend  : 1=ScaleDiv(10,2) 2=ScaleDiv(7,0) 3=IsSolid(3,5) 4=IsSolid(0,0) 5=SumTiles")
    return code

# ── Pipeline ───────────────────────────────────────────────────────────────────
log(f"TriskeleToolchain Pipeline Report")
log(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Workspace: {WORKSPACE}")

run(["clang", "-O0", "-S", "-emit-llvm", "-o", LL, C],           "1/4 clang")
run(["cargo", "clean", "-p", "tsk-cc"],                               "  clean tsk-cc")
run(["cargo", "clean", "-p", "tsk-link"],                              "  clean tsk-link")
run(["cargo", "run", "-p", "tsk-cc",   "--", LL,   "-o", TOBJ, "--verbose", "--dump-asm"],  "2/4 tsk-cc")
run(["cargo", "run", "-p", "tsk-link", "--", TOBJ, "-o", TVMX,
     "--entry", "main"],                                           "3/4 tsk-link")
code = run_vm(["cargo", "run", "-p", "triskele-vm", "--", TVMX],  "4/4 tskvm")

save_report("PASSED" if code == 31 else "FAILED")
sys.exit(0 if code == 31 else 1)
