#!/usr/bin/env python3
"""
restore_m0_bak.py
=================
Restaure les fichiers JSON-LD à partir des sauvegardes .bak créées lors des migrations.
Pour chaque fichier .jsonld.bak trouvé, il remplace le .jsonld correspondant.

Usage:
    python restore_m0_bak.py           # restauration réelle
    python restore_m0_bak.py --dry-run # aperçu sans écrire
"""

import argparse
import shutil
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Restore .bak files to .jsonld")
    parser.add_argument('--dry-run', action='store_true', help="Preview only, do not restore")
    parser.add_argument('--instances-dir', type=str, default=None,
                        help="Path to 'instances' directory (auto-detected if not given)")
    args = parser.parse_args()

    if args.instances_dir:
        instances_root = Path(args.instances_dir)
    else:
        script_dir = Path(__file__).resolve().parent
        for p in [script_dir] + list(script_dir.parents):
            candidate = p / 'instances'
            if candidate.exists() and candidate.is_dir():
                instances_root = candidate
                break
        else:
            print("❌ Could not find 'instances' directory. Please provide --instances-dir.")
            return

    if not instances_root.exists():
        print(f"❌ Directory not found: {instances_root}")
        return

    print(f"🔍 Scanning for .bak files in: {instances_root}")
    print(f"   Dry-run mode: {args.dry_run}")
    print("=" * 80)

    bak_files = list(instances_root.rglob("*.jsonld.bak"))
    restored = 0

    for bak_path in bak_files:
        target_path = bak_path.with_suffix('')  # enlève .bak
        if not target_path.exists():
            print(f"⚠️  Target missing: {target_path.name} — will rename anyway")
        if args.dry_run:
            print(f"🔄 Would restore: {bak_path.relative_to(instances_root)} -> {target_path.relative_to(instances_root)}")
        else:
            shutil.move(str(bak_path), str(target_path))
            print(f"✅ Restored: {target_path.relative_to(instances_root)}")
        restored += 1

    if restored == 0:
        print("No .bak files found.")
    else:
        print("=" * 80)
        print(f"📊 Summary: {restored} file(s) restored.")
        if args.dry_run:
            print("⚠️  Dry-run mode – no files were actually changed. Remove --dry-run to apply.")

if __name__ == "__main__":
    main()