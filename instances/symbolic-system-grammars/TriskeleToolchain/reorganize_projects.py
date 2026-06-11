#!/usr/bin/env python3
"""
reorganize_projects.py — TriskeleToolchain v0.3.10
Author: Echopraxium with the collaboration of Claude AI

Reorganises projects/ into a hierarchical structure.
Run from workspace root. Use --dry-run to preview.
"""
import os, sys, shutil

DRY  = "--dry-run" in sys.argv
BASE = os.path.dirname(os.path.abspath(__file__))
P    = os.path.join(BASE, "projects")

def mv(src, dst):
    src_full = os.path.join(P, src)
    dst_full = os.path.join(P, dst)
    if not os.path.exists(src_full):
        print(f"  [SKIP] {src}  (not found)")
        return
    if DRY:
        print(f"  [DRY]  {src}  →  {dst}")
        return
    os.makedirs(os.path.dirname(dst_full), exist_ok=True)
    shutil.move(src_full, dst_full)
    print(f"  [MOVE] {src}  →  {dst}")

print("=== Reorganising projects/ ===\n")

# ── toolchain-tests/c89 ───────────────────────────────────────────────────────
print("-- toolchain-tests/c89 --")
for name in ["test_main", "test_patterns", "test_select",
             "test_variadic", "test_doom_libc", "test-lib-dos"]:
    mv(name, f"toolchain-tests/c89/{name}")

# ── toolchain-tests/asm ───────────────────────────────────────────────────────
print("\n-- toolchain-tests/asm --")
for name in ["hello", "test_div", "test_shr", "sdl_test"]:
    mv(name, f"toolchain-tests/asm/{name}")

# ── wolf3d ────────────────────────────────────────────────────────────────────
print("\n-- wolf3d --")
# Rename wolf3d → wolfenstein3D to avoid self-move conflict
mv("wolf3d", "wolfenstein3D/wolf3d")
for name in ["wolf3d_drawtest", "wolf3d_raycaster", "wolf3d_raycaster_debug",
             "wolf3d_v2", "wolf3d_v2_clean"]:
    mv(name, f"wolfenstein3D/tests/{name}")

# ── doom-generic ──────────────────────────────────────────────────────────────
print("\n-- doom-generic --")
mv("Doom-Generic", "doom-generic/src/Doom-Generic")
for name in ["doom_fixed", "doom_alloc", "doom_zzone", "doom_math"]:
    mv(name, f"doom-generic/vm-porting/tests/{name}")

# ── references ────────────────────────────────────────────────────────────────
print("\n-- references --")
for name in [
    "wolf3D_4DSL",
    "wolfenstein3d-opensource",
    "lazd-wolf4sdl- Wolf4SDL is an open-source port of id Software's classic first-person shooter Wolfenstein 3D to the cross-plat.url",
    "ozkl-doomgeneric- Easily portable doom.url",
    "_00_open_cmd_window.bat",
]:
    mv(name, f"references/{name}")

print(f"\n{'='*50}")
print("Done." if not DRY else "Dry-run complete — rerun without --dry-run to apply.")
