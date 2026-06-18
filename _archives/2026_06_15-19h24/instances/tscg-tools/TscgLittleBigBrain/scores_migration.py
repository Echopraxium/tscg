#!/usr/bin/env python3
"""
migrate_scores_to_shacl.py

Renames score properties in M0 instances to match the SHACL grammar:
- A_score → m0:scoreA
- S_score → m0:scoreS
- F_score → m0:scoreF
- It_score → m0:scoreIt
- D_score → m0:scoreD
- R_score → m0:scoreR
- E_score → m0:scoreE
- V_score → m0:scoreV
- O_score → m0:scoreO
- Im_score → m0:scoreIm

Also moves any direct score keys (A, S, F, I, D, R, E, V, O, Im) into the respective objects.

Usage:
    python migrate_scores_to_shacl.py           # apply changes
    python migrate_scores_to_shacl.py --dry-run # preview only
"""

import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, Any

# Mapping from old keys (inside asfidScores/revoiScores) to new SHACL keys
ASFID_MAP = {
    'A_score': 'm0:scoreA',
    'S_score': 'm0:scoreS',
    'F_score': 'm0:scoreF',
    'It_score': 'm0:scoreIt',
    'D_score': 'm0:scoreD',
}
REVOI_MAP = {
    'R_score': 'm0:scoreR',
    'E_score': 'm0:scoreE',
    'V_score': 'm0:scoreV',
    'O_score': 'm0:scoreO',
    'Im_score': 'm0:scoreIm',
}

# Direct keys that should be moved into asfidScores/revoiScores
DIRECT_ASFID = {'A', 'S', 'F', 'I', 'D', 'A_score', 'S_score', 'F_score', 'It_score', 'D_score'}
DIRECT_REVOI = {'R', 'E', 'V', 'O', 'Im', 'R_score', 'E_score', 'V_score', 'O_score', 'Im_score'}


def normalize_score_value(value: Any) -> Any:
    """Ensure score is a number or JSON-LD @value object."""
    if isinstance(value, dict):
        if '@value' in value:
            return value
        try:
            num = float(value.get('value', 0.0))
        except:
            num = 0.0
        return {'@value': num, '@type': 'xsd:float'}
    else:
        try:
            num = float(value)
        except:
            num = 0.0
        return {'@value': num, '@type': 'xsd:float'}


def process_node(node: Dict, path: str) -> bool:
    """
    Transform score structures in a node (root or @graph element).
    Returns True if modified.
    """
    modified = False

    # 1. Collect direct score keys (old root-level scores)
    asfid_direct = {}
    revoi_direct = {}
    for k in list(node.keys()):
        if k in DIRECT_ASFID:
            asfid_direct[k] = node.pop(k)
            modified = True
        elif k in DIRECT_REVOI:
            revoi_direct[k] = node.pop(k)
            modified = True

    # 2. Get existing asfid/revoi objects
    asfid_obj = node.get('m0:asfidScores', {})
    revoi_obj = node.get('m0:revoiScores', {})

    # 3. Merge direct scores into those objects (if any)
    if asfid_direct:
        asfid_obj.update(asfid_direct)
        modified = True
    if revoi_direct:
        revoi_obj.update(revoi_direct)
        modified = True

    # 4. Rename keys inside objects
    new_asfid = {}
    for old_key, value in asfid_obj.items():
        if old_key in ASFID_MAP:
            new_key = ASFID_MAP[old_key]
            new_asfid[new_key] = normalize_score_value(value)
            modified = True
        else:
            # keep as is (e.g., 'mean', 'justification', etc.)
            new_asfid[old_key] = value
    if new_asfid:
        node['m0:asfidScores'] = new_asfid
    elif asfid_obj and not new_asfid:
        # No valid keys left? remove empty dict
        del node['m0:asfidScores']
        modified = True

    new_revoi = {}
    for old_key, value in revoi_obj.items():
        if old_key in REVOI_MAP:
            new_key = REVOI_MAP[old_key]
            new_revoi[new_key] = normalize_score_value(value)
            modified = True
        else:
            new_revoi[old_key] = value
    if new_revoi:
        node['m0:revoiScores'] = new_revoi
    elif revoi_obj and not new_revoi:
        del node['m0:revoiScores']
        modified = True

    return modified


def migrate_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single JSON-LD file. Returns True if changes would be made."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Cannot read {filepath.name}: {e}")
        return False

    modified = False

    # Process root node
    if process_node(data, 'root'):
        modified = True

    # Process @graph nodes
    if '@graph' in data and isinstance(data['@graph'], list):
        for idx, node in enumerate(data['@graph']):
            if process_node(node, f'@graph[{idx}]'):
                modified = True

    if not modified:
        return False

    if dry_run:
        try:
            rel_path = filepath.relative_to(Path.cwd())
        except ValueError:
            rel_path = filepath
        print(f"  🔄 Would modify: {rel_path}")
        return True

    # Apply changes
    backup = filepath.with_suffix(filepath.suffix + '.bak')
    shutil.copy2(filepath, backup)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    try:
        rel_path = filepath.relative_to(Path.cwd())
    except ValueError:
        rel_path = filepath
    print(f"  ✅ Migrated: {rel_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Migrate score properties to SHACL grammar.")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without writing.")
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

    print(f"🔍 Scanning M0 files in: {instances_root}")
    print(f"   Dry-run mode: {args.dry_run}")
    print("=" * 80)

    excluded_dirs = {'_archives', '__pycache__', '.git', '.idea', 'venv', 'env', 'static'}
    total = 0
    modified = 0

    for filepath in instances_root.rglob("*.jsonld"):
        if any(part in excluded_dirs for part in filepath.parts):
            continue
        total += 1
        if migrate_file(filepath, dry_run=args.dry_run):
            modified += 1

    print("=" * 80)
    print(f"📊 Summary: {modified} file(s) would be modified (or were modified) out of {total} JSON-LD files.")
    if args.dry_run:
        print("⚠️  Dry-run mode – no files were actually changed. Remove --dry-run to apply.")
    else:
        print("✅ Migration complete. Backups (.bak) created alongside original files.")


if __name__ == "__main__":
    main()