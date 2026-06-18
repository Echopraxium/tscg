"""
_run_tests.py — Interactive test runner for tscg-python-bridge.
Place this file under: dev/tscg-python-bridge/

Usage:
    python _run_tests.py

Author: Echopraxium with the collaboration of Claude AI
"""
import subprocess
import sys
import os

# ── Ensure we run from bridge dir ─────────────────────────────────
os.chdir(os.path.dirname(os.path.abspath(__file__)))

MENU = """
╔══════════════════════════════════════════════════════╗
║       TscgOntologyExplorer — Test Runner             ║
╠══════════════════════════════════════════════════════╣
║  1. test_expand_iri    — IRI expansion (18 tests)    ║
║  2. test_tscg_store    — TscgStore / pyoxigraph       ║
║                          (20 tests)                  ║
║  3. test_endpoints     — FastAPI integration          ║
║                          (20 tests)                  ║
║  4. All tests          — Full suite (58 tests)        ║
╠══════════════════════════════════════════════════════╣
║  Q. Quit                                             ║
╚══════════════════════════════════════════════════════╝
"""

TEST_MODULES = {
    '1': ('test_expand_iri',  'tests/test_expand_iri.py'),
    '2': ('test_tscg_store',  'tests/test_tscg_store.py'),
    '3': ('test_endpoints',   'tests/test_endpoints.py'),
    '4': ('All tests',        'tests/'),
}

def run(label, path):
    print(f"\n{'═'*54}")
    print(f"  Running: {label}")
    print(f"{'═'*54}\n")
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', path, '-v', '--tb=short'],
        check=False
    )
    print(f"\n{'═'*54}")
    if result.returncode == 0:
        print(f"  ✓  {label} — ALL PASSED")
    else:
        print(f"  ✗  {label} — SOME FAILED (see above)")
    print(f"{'═'*54}")
    return result.returncode

def main():
    while True:
        print(MENU)
        choice = input("Choice [1-4 / Q]: ").strip().upper()

        if choice == 'Q':
            print("\nBye.\n")
            break
        elif choice in TEST_MODULES:
            label, path = TEST_MODULES[choice]
            run(label, path)
            input("\nPress Enter to return to menu...")
        else:
            print("\n  Invalid choice — please enter 1, 2, 3, 4 or Q.\n")

if __name__ == '__main__':
    main()
