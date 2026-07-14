#!/usr/bin/env python3
"""
run_all_layers — TSCG ontology acceptance gate (M3 → M0).

Author : Echopraxium with the collaboration of Claude AI
Version: 1.1.0
Date   : 2026-07-13
Home   : ontology/cli-tools/run_all_layers.py

WHY GOLDEN VALUES AND NOT PASS/FAIL
-----------------------------------
M1 has NEVER been conformant. A binary CONFORMS gate would have been red every day
for six months — so it would have been ignored, so it would have been useless. That
is exactly how the debt grew *while* the checkers "existed".

So this gate borrows the TriskeleToolchain discipline: SEPTUPLE VALIDATION with EXACT
reference values.

    163 is GREEN.  162 is RED.  164 is RED.

- **164 (or more) = REGRESSION.** Someone introduced a new defect.
- **162 (or fewer) = ALSO RED.** Either a real fix landed — in which case you LOWER the
  golden value on purpose, with `--update-golden`, and the drop is recorded — or, far
  more likely, **a validator stopped biting**: a shape lost its target, a schema was not
  found, a file was skipped. A silently shrinking error count is the most dangerous
  signal in this codebase, because it looks like progress.

The count is therefore a THERMOMETER OF THE DEBT, not a traffic light. It is allowed to
be non-zero. It is not allowed to move by accident.

THE FAILURE MODE THIS EXISTS TO CATCH
-------------------------------------
Every serious defect found on 2026-07-12/13 failed SILENTLY:

  - `m2:morphism_emergence` — a false thesis, never stated as one
  - `structuralGrammarFormulaExpanded` — half its values were empty strings, because
    there was never anything to compute
  - SHAPE 2 ↔ SHAPE 3 — 256 violations of pure noise drowning the real signal
  - `fix_imports_genesis()` — called by run(), never defined
  - `M1_Schema.shacl.ttl` (dot) vs `M1_Schema_shacl.ttl` (underscore) — --shacl found
    no grammar, validated nothing, and exited 0
  - `symbolic-system-grammar` (singular) — a whole instance category skipped
  - `M1_music` listed twice — its errors double-counted
  - a checker that WORKS in a terminal and DIES when called from this launcher, because
    a pipe flips Windows from UTF-8 to cp1252 (caught by this gate on 2026-07-13 — see
    `_utf8_env()`)

None of them crashed. None of them reported failure. They just… didn't do the work.
This script's job is to make that impossible: if a number moves, you hear about it.

USAGE
-----
    python run_all_layers.py                 # the gate
    python run_all_layers.py --verbose       # per-code breakdown
    python run_all_layers.py --update-golden # accept the current counts as the new reference
                                             # (use ONLY after a deliberate fix — it rewrites
                                             #  golden_values.json and records the delta)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tscg_paths import REPO_ROOT, ONTOLOGY_DIR, CLI_TOOLS_DIR, verify_layout  # noqa: E402

__version__ = "1.3.0"

GOLDEN_FILE = CLI_TOOLS_DIR / "golden_values.json"

# ---------------------------------------------------------------------------
# Reference values — measured on the real repository, 2026-07-13, after SC-1.
#
# NOT measured on a sandbox reconstruction: an earlier estimate of 126 was made on a
# partial corpus and was WRONG (it lacked BusinessModeling, Music, MapTerritory_Optics).
# Only the repo counts.
# ---------------------------------------------------------------------------
DEFAULT_GOLDEN = {
    "_measured": "2026-07-13, real repository, after SC-1",
    "M3": {
        "status": "NOT_INSTRUMENTED",
        "note": "No M3 checker exists. M3_Schema.shacl.ttl was produced 2026-07-03 "
                "(CONFORMS: True, 13 shapes) but is not wired into a script. TODO.",
    },
    "M2": {
        "status": "NOT_INSTRUMENTED",
        "note": "No M2 checker exists. The tscg-generate-mn-grammars skill can produce "
                "the SHACL grammar; no runner wraps it yet. TODO.",
    },
    "M1": {
        "status": "INSTRUMENTED",
        "files": 16,
        "errors": 163,
        "warnings": 3,
        "shacl_violations": 502,
        "by_code": {
            "DCC006": 127,   # monoidal operator inside a signature  → SC-6 (the bulk)
            "DCC010": 18,    # Fm1m2's first argument is not a registered Domain
            "EXP001": 12,    # retired m1:structuralGrammarFormulaExpanded (D8)
            "GCC009": 4,     # guard after an Fm2 signature
            "DCC009": 1,     # guard after an Fm1m2 signature
            "DCC008": 1,     # wrong arity  (Amplifier: nested parens + the invented `Ft`)
            "CTX001": 3,     # WARNINGS, not errors — by_code counts every code emitted,
                             # warnings included. Leaving them out of the golden set made
                             # the gate fail against a reference that was itself incomplete.
        },
        "note": "This is the SC-6 BACKLOG, measured. It is expected to be non-zero. "
                "Lower it only by actually repairing formulas — never by loosening a shape.",
    },
    "M0": {
        "status": "INSTRUMENTED",
        "note": "check_m0_instances.py runs; golden counts not yet captured. "
                "Run --update-golden once, review the numbers, then trust them.",
    },
}


def load_golden() -> dict:
    if GOLDEN_FILE.exists():
        return json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))
    return DEFAULT_GOLDEN


def save_golden(g: dict) -> None:
    GOLDEN_FILE.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Runners
# ---------------------------------------------------------------------------


def _utf8_env() -> dict:
    """
    Force UTF-8 on the CHILD process's stdout.

    Windows only: when a script writes to a TERMINAL, Python uses the console encoding
    (UTF-8 on a modern terminal). When it writes to a PIPE — which is exactly what
    subprocess.run(capture_output=True) creates — Python falls back to the ANSI code page,
    cp1252. The checkers print '⊗', 'ℹ️', '≥'… none of which exist in cp1252, so they die
    with UnicodeEncodeError.

    The perverse consequence: `python check_M1.py` works perfectly, and the SAME command
    called from this launcher crashes. A checker that works alone and dies when invoked is
    a checker that reports zero errors inside a gate — which is precisely the class of
    silent failure this gate exists to catch. (It DID catch it, on 2026-07-13, which is the
    only reason you are reading this comment.)
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def run_m1() -> dict | None:
    """Run check_M1 in dry-run and parse its output. Never let a crash pass as a pass."""
    script = CLI_TOOLS_DIR / "check-M1" / "check_M1.py"
    if not script.exists():
        return {"_error": f"check_M1.py not found at {script}"}

    proc = subprocess.run(
        [sys.executable, str(script), "--dry-run", "--shacl", "--no-color"],
        capture_output=True, text=True, cwd=script.parent,
        env=_utf8_env(), encoding="utf-8", errors="replace",
    )
    out = proc.stdout + proc.stderr

    # A traceback means the checker died. A dead checker reports zero errors, which
    # would otherwise look like a clean run. Fail loudly.
    if "Traceback" in out:
        return {"_error": "check_M1.py CRASHED — a crashed validator reports no errors, "
                          "which looks exactly like success.\n" + out[-800:]}

    import re
    files = errors = warnings = None
    for line in out.splitlines():
        if "SUMMARY:" not in line:
            continue
        m = re.search(r"(\d+)\s+files?\s*\|\s*(\d+)\s+errors?\s*\|\s*(\d+)\s+warnings?", line)
        if m:
            files, errors, warnings = (int(m.group(i)) for i in (1, 2, 3))

    if errors is None:
        return {"_error": "could not parse check_M1 SUMMARY line — the format changed, "
                          "or the run produced no summary at all."}

    by_code = Counter(re.findall(r"\[((?:GCC|DCC|EXP|CTX|ONT|FRBDN|NS|ENC|JSON)\d+[a-z]?)\]", out))

    # SHACL violations are reported PER FILE ("SHACL: 46 violations") and are NOT part
    # of check_M1's own error count. Tracking only `errors` left the gate blind to half
    # the signal: on 2026-07-14, M1_CoreConcepts went from UNREASONABLE to Pellet-clean,
    # and the dashboard said "nothing changed". A counter blind to half its subject is
    # exactly the failure mode this gate exists to prevent — so count them separately.
    shacl = sum(int(m) for m in re.findall(r"SHACL:\s*(\d+)\s+violations?", out))

    return {"files": files, "errors": errors, "warnings": warnings,
            "shacl_violations": shacl, "by_code": dict(by_code)}


def run_m0() -> dict | None:
    script = CLI_TOOLS_DIR / "check-M0" / "check_m0_instances.py"
    if not script.exists():
        return {"_error": f"check_m0_instances.py not found at {script}"}
    proc = subprocess.run([sys.executable, str(script)],
                          capture_output=True, text=True, cwd=script.parent,
                          env=_utf8_env(), encoding="utf-8", errors="replace")
    out = proc.stdout + proc.stderr
    if "Traceback" in out:
        return {"_error": "check_m0_instances.py CRASHED.\n" + out[-800:]}
    return {"_raw_exit": proc.returncode, "_captured": True}


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def _enable_ansi() -> bool:
    """
    Return True if ANSI colour codes will actually RENDER.

    On Windows, cmd.exe only interprets ANSI escapes when "Virtual Terminal
    processing" is enabled on the console handle — which it is not, by default, in
    older cmd.exe. Emitting escapes anyway prints literal garbage:

        ←[31m≠←[0m CTX001   3   0

    …which is strictly WORSE than no colour: the marker column becomes unreadable
    exactly where the eye is supposed to land. So: try to switch VT on; if that
    fails, or if stdout is a pipe/file rather than a terminal, fall back to plain
    ASCII markers. A gate whose output cannot be read is a gate that will not be run.
    """
    if not sys.stdout.isatty():
        return False
    if os.name != "nt":
        return True
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-11)                     # STD_OUTPUT_HANDLE
        mode = ctypes.c_ulong()
        if not k.GetConsoleMode(h, ctypes.byref(mode)):
            return False
        # 0x0004 = ENABLE_VIRTUAL_TERMINAL_PROCESSING
        return bool(k.SetConsoleMode(h, mode.value | 0x0004))
    except Exception:
        return False


_COLOR = _enable_ansi() and "--no-color" not in sys.argv

if _COLOR:
    C_OK, C_BAD, C_WARN, C_DIM, C_END = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
    M_OK, M_BAD = "OK", "!!"
else:
    C_OK = C_BAD = C_WARN = C_DIM = C_END = ""
    M_OK, M_BAD = "OK", "!!"


def compare(layer: str, actual: dict, golden: dict, verbose: bool) -> bool:
    print(f"\n── {layer} " + "─" * (50 - len(layer)))

    g = golden.get(layer, {})
    if g.get("status") == "NOT_INSTRUMENTED":
        print(f"  {C_WARN}[--] NOT INSTRUMENTED{C_END} — {g.get('note', '')}")
        print(f"  {C_DIM}   An un-instrumented layer is not a passing layer. It is an "
              f"unmeasured one.{C_END}")
        return True  # not a failure, but never reported as a success either

    if actual is None or "_error" in (actual or {}):
        print(f"  {C_BAD}[{M_BAD}] RUNNER FAILED{C_END}")
        print("   " + (actual or {}).get("_error", "unknown"))
        return False

    ok = True
    for key in ("files", "errors", "warnings", "shacl_violations"):
        exp, got = g.get(key), actual.get(key)
        if exp is None or got is None:
            continue
        if got == exp:
            print(f"  {C_OK}[{M_OK}] {key:<9} {got:>4}{C_END}")
        elif got > exp:
            print(f"  {C_BAD}[{M_BAD}] {key:<9} {got:>4}   expected {exp}   "
                  f"(+{got - exp}) — REGRESSION: a new defect was introduced.{C_END}")
            ok = False
        else:
            print(f"  {C_BAD}[{M_BAD}] {key:<9} {got:>4}   expected {exp}   "
                  f"({got - exp}) — the count DROPPED.{C_END}")
            print(f"     {C_WARN}Either you repaired something on purpose (then run "
                  f"--update-golden), or a validator STOPPED BITING.{C_END}")
            print(f"     {C_DIM}A silently shrinking error count is the most dangerous "
                  f"signal in this repo: it looks like progress.{C_END}")
            ok = False

    exp_codes = g.get("by_code", {})
    got_codes = actual.get("by_code", {})
    if exp_codes and (verbose or exp_codes != got_codes):
        print(f"\n       {'code':<9} {'got':>5} {'golden':>7}")
        for code in sorted(set(exp_codes) | set(got_codes)):
            e, a = exp_codes.get(code, 0), got_codes.get(code, 0)
            if e == a:
                print(f"  {C_OK}[{M_OK}]{C_END} {code:<9} {a:>5} {e:>7}")
            else:
                print(f"  {C_BAD}[{M_BAD}]{C_END} {code:<9} {a:>5} {e:>7}"
                      f"   <-- MISMATCH ({a - e:+d})")
        if exp_codes != got_codes:
            ok = False

    if g.get("note"):
        print(f"\n  {C_DIM}{g['note']}{C_END}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="TSCG ontology acceptance gate (M3 → M0)")
    ap.add_argument("--verbose", "-v", action="store_true", help="per-code breakdown")
    ap.add_argument("--no-color", action="store_true",
                    help="plain output (auto-detected, but forceable — e.g. for CI logs)")
    ap.add_argument("--update-golden", action="store_true",
                    help="accept the CURRENT counts as the new reference (deliberate fixes only)")
    args = ap.parse_args()

    print("=" * 62)
    print(f"  TSCG — run_all_layers v{__version__}   ({date.today()})")
    print(f"  repo: {REPO_ROOT}")
    print("=" * 62)

    # A missing REQUIRED compartment silently removes a whole populated category from
    # the counts — fatal. A missing OPTIONAL one (planned, never populated) skips nothing.
    # Blocking on the latter would make the gate cry wolf, and a gate that cries wolf is a
    # gate people learn to ignore.
    layout = verify_layout()
    if layout["blocking"]:
        print(f"\n{C_BAD}[!!] A REQUIRED instance compartment is missing — the totals below "
              f"would NOT be comprehensive. Fix the layout before trusting any number.{C_END}")
        return 2

    golden = load_golden()
    results = {"M1": run_m1(), "M0": run_m0()}

    ok = True
    for layer in ("M3", "M2", "M1", "M0"):
        ok &= compare(layer, results.get(layer), golden, args.verbose)

    if args.update_golden:
        # ⚠ Capture EVERY tracked counter, not a hand-written subset. On 2026-07-14 this
        # list read ("files", "errors", "warnings") — it omitted `shacl_violations`, so
        # the 502 → 476 drop was NOT recorded anywhere. The one mechanism whose entire
        # purpose is to make a lowered reference REVIEWABLE quietly failed to review it.
        # A gate that forgets why a number went down is a gate that has stopped working.
        TRACKED = ("files", "errors", "warnings", "shacl_violations")
        for layer, res in results.items():
            if res and "_error" not in res and golden.get(layer, {}).get("status") == "INSTRUMENTED":
                old = {k: golden[layer].get(k) for k in TRACKED if k in golden[layer]}
                new = {k: v for k, v in res.items() if not k.startswith("_")}
                deltas = {k: f"{old[k]} -> {new[k]}" for k in TRACKED
                          if k in old and k in new and old[k] != new[k]}
                golden[layer].update(new)
                golden[layer]["_previous"] = old
                golden[layer]["_delta"] = deltas or "no change"
                golden[layer]["_updated"] = str(date.today())
                if deltas:
                    print(f"\n  {C_WARN}[!!] {layer}: {deltas}{C_END}")
                    print(f"     {C_DIM}Recorded under '_previous' and '_delta'. WRITE DOWN WHY, "
                          f"in the commit message.{C_END}")
        golden["_measured"] = f"{date.today()}, real repository (--update-golden)"
        save_golden(golden)
        print(f"\n{C_WARN}[!!] Golden values REWRITTEN → {GOLDEN_FILE}{C_END}")
        print(f"   {C_DIM}The previous values are kept under '_previous'. Commit this file: "
              f"a lowered reference must be a reviewable, deliberate act — never a side "
              f"effect.{C_END}")
        return 0

    print("\n" + "=" * 62)
    if ok:
        print(f"  {C_OK}GATE: PASS{C_END} — counts match the reference.")
        print(f"  {C_DIM}Non-zero errors are EXPECTED: that is the measured SC-6 backlog, "
              f"not a failure.{C_END}")
    else:
        print(f"  {C_BAD}GATE: FAIL{C_END} — a count moved. Read the direction of the move:")
        print(f"  {C_DIM}up = new defect · down = a fix (then --update-golden) OR a "
              f"validator that stopped working.{C_END}")
    print("=" * 62)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
