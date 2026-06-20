#!/usr/bin/env python3
# update_toolchain.py
# Author: Echopraxium with the collaboration of Claude AI
# Version: 0.3.4
# Extracts Cargo.toml, crates/, lib/, projects/ and run_pipeline.py
# from a TriskeleToolchain zip.
# Usage: python update_toolchain.py <path_to_zip> [dest_dir]

import sys, os, zipfile, shutil, datetime, glob, time

def log(msg=""): print(msg)

def usage():
    print("Usage: python update_toolchain.py <path_to_zip> [dest_dir]")
    sys.exit(1)

if len(sys.argv) < 2: usage()

zip_path = sys.argv[1]
dest_dir = sys.argv[2] if len(sys.argv) >= 3 else os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(zip_path):
    log(f"❌ File not found: {zip_path}"); sys.exit(1)
if not zipfile.is_zipfile(zip_path):
    log(f"❌ Not a valid zip: {zip_path}"); sys.exit(1)

log()
log("TriskeleToolchain Update")
log(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Zip      : {zip_path}")
log(f"Dest     : {dest_dir}")

# ── Detect zip root prefix ─────────────────────────────────────────────────────
# A zip may have a wrapping root folder (e.g. "tscg_v031/crates/...").
# BUT if the root prefix is itself a target (e.g. "projects/"), do NOT strip it.
#
# v0.3.3 fix: 'crates/' and 'lib/' moved from TARGETS_CLEAN to TARGETS_MERGE.
# Rationale: patch zips typically contain only a subset of crates (e.g. 2 of 10).
# Cleaning the entire crates/ directory before extraction would delete the crates
# NOT present in the zip — causing the workspace to lose triskele-common, tsk-cc,
# etc. on every patch apply. The merge strategy (used for projects/) is correct:
# remove only the specific sub-directories present in the zip, then extract.
TARGETS_CLEAN = ['Cargo.toml', 'run_pipeline.py']
TARGETS_MERGE = ['crates/', 'lib/', 'projects/']
ALL_TARGETS   = TARGETS_CLEAN + TARGETS_MERGE

with zipfile.ZipFile(zip_path, 'r') as z:
    all_names = z.namelist()

top_dirs = set(name.split('/')[0] + '/' for name in all_names if '/' in name)
# Strip zip_root only if it's NOT itself a target
single_top = top_dirs.pop() if len(top_dirs) == 1 else None
if single_top and single_top not in ALL_TARGETS and single_top + '/' not in ALL_TARGETS:
    zip_root = single_top
else:
    zip_root = ''

log(f"Zip root : '{zip_root}' ({len(all_names)} entries)")

# ── Detect which targets are actually present in this zip ─────────────────────
zip_has = set()
for entry in all_names:
    rel = entry[len(zip_root):] if zip_root and entry.startswith(zip_root) else entry
    if not rel: continue
    for t in ALL_TARGETS:
        if rel == t or rel.startswith(t):
            zip_has.add(t)
            break

log(f"Zip has  : {sorted(zip_has)}")

# ── Clean targets (only those present in the zip) ─────────────────────────────
for target in TARGETS_CLEAN:
    if target not in zip_has:
        log(f"   Skipping (not in zip): {target}")
        continue
    full = os.path.join(dest_dir, target.rstrip('/'))
    if os.path.isdir(full):
        log(f"   Removing dir  : {target}"); shutil.rmtree(full)
    elif os.path.isfile(full):
        log(f"   Removing file : {target}"); os.remove(full)

# ── Merge targets: overwrite only the individual files present in the zip ──────
# v0.3.4 fix: previously removed entire sub-directories (e.g. crates/triskele-vm/)
# before extraction, which deleted files NOT in the zip (main.rs, build.rs,
# decode.rs, etc.). Now we only remove the specific files that will be
# overwritten — preserving everything else in the directory.
for merge_target in TARGETS_MERGE:
    for entry in all_names:
        rel = entry[len(zip_root):] if zip_root and entry.startswith(zip_root) else entry
        if not rel.startswith(merge_target) or entry.endswith('/'):
            continue
        full = os.path.join(dest_dir, rel)
        if os.path.isfile(full):
            log(f"   Updating file : {rel}")
            os.remove(full)

# ── Extract ────────────────────────────────────────────────────────────────────
extracted = skipped = 0

with zipfile.ZipFile(zip_path, 'r') as z:
    for entry in all_names:
        rel = entry[len(zip_root):] if zip_root and entry.startswith(zip_root) else entry
        if not rel:
            continue
        # Handle run_pipeline_new.py → run_pipeline.py rename
        if os.path.basename(rel) == 'run_pipeline_new.py':
            rel = os.path.join(os.path.dirname(rel), 'run_pipeline.py').replace('\\','/')

        matched = any(rel == t or rel.startswith(t) for t in ALL_TARGETS)
        if not matched:
            skipped += 1; continue

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

# Touch .rs files
rs_files = glob.glob(os.path.join(dest_dir, "crates/**/*.rs"), recursive=True)
now = time.time()
for f in rs_files: os.utime(f, (now, now))
log(f"   Touched  : {len(rs_files)} .rs files")
log()
log("Ready — run: python run_pipeline.py --list")
log("             python run_pipeline.py test_main")
