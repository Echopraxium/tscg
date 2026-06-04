#!/usr/bin/env python3
# update_toolchain.py
# Author: Echopraxium with the collaboration of Claude AI
# Extracts Cargo.toml, crates/ and lib/ from a TriskeleToolchain zip.
# Usage: python update_toolchain.py <path_to_zip> [dest_dir]
#   dest_dir defaults to the directory containing this script.

import sys
import os
import zipfile
import shutil
import datetime

def log(msg=""):
    print(msg)

def usage():
    print("Usage: python update_toolchain.py <path_to_zip> [dest_dir]")
    print("   Ex: python update_toolchain.py C:\\Downloads\\crates_v030_sb.zip")
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

zip_path = sys.argv[1]
dest_dir = sys.argv[2] if len(sys.argv) >= 3 else os.path.dirname(os.path.abspath(__file__))

# ── Validation ─────────────────────────────────────────────────────────────────
if not os.path.isfile(zip_path):
    log(f"❌ File not found: {zip_path}")
    sys.exit(1)

if not zipfile.is_zipfile(zip_path):
    log(f"❌ Not a valid zip file: {zip_path}")
    sys.exit(1)

log()
log("TriskeleToolchain Update")
log(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Zip      : {zip_path}")
log(f"Dest     : {dest_dir}")

# ── Detect zip root prefix ─────────────────────────────────────────────────────
with zipfile.ZipFile(zip_path, 'r') as z:
    all_names = z.namelist()

prefixes = set(name.split('/')[0] for name in all_names if '/' in name)
zip_root = (prefixes.pop() + '/') if len(prefixes) == 1 else ''
log(f"Zip root : '{zip_root}' ({len(all_names)} entries)")

# ── Targets to replace ─────────────────────────────────────────────────────────
TARGETS = ['crates/', 'lib/', 'Cargo.toml']

# Delete existing targets before extraction (clean replace)
for target in TARGETS:
    full = os.path.join(dest_dir, target.rstrip('/'))
    if os.path.isdir(full):
        log(f"   Removing dir  : {target}")
        shutil.rmtree(full)
    elif os.path.isfile(full):
        log(f"   Removing file : {target}")
        os.remove(full)

# ── Extract ────────────────────────────────────────────────────────────────────
extracted = 0
skipped   = 0

with zipfile.ZipFile(zip_path, 'r') as z:
    for entry in z.namelist():
        rel = entry[len(zip_root):] if zip_root and entry.startswith(zip_root) else entry
        if not rel:
            continue

        matched = any(rel == t or rel.startswith(t) for t in TARGETS)
        if not matched:
            skipped += 1
            continue

        dest = os.path.join(dest_dir, rel)

        if entry.endswith('/'):
            os.makedirs(dest, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(entry) as src, open(dest, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            extracted += 1

log()
log(f"✅ Extracted : {extracted} files")
log(f"   Skipped  : {skipped} entries (outside targets)")

# Touch all modified .rs files to ensure cargo detects changes
import glob, time
rs_files = glob.glob(os.path.join(dest_dir, "crates/**/*.rs"), recursive=True)
now = time.time()
for f in rs_files:
    os.utime(f, (now, now))
log(f"   Touched  : {len(rs_files)} .rs files (force cargo rebuild)")

log()
log("Ready — run: python run_pipeline.py")
