#!/usr/bin/env python3
"""
migrate_scores_to_shacl.py
Renomme les propriétés de score dans les fichiers M0 pour correspondre à la grammaire SHACL.
Lit les anciens formats (m1:asfidScoring, clés directes, etc.) et les convertit en
m0:asfidScores / m0:revoiScores avec clés m0:scoreA, m0:scoreS, etc.
Ne crée pas de scores artificiels.
"""

import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, List

# Mappings des anciennes clés vers les nouvelles clés SHACL
ASFID_MAP = {
    # m1:asfidScoring textual keys
    'attractor': 'm0:scoreA',
    'structure': 'm0:scoreS',
    'flow': 'm0:scoreF',
    'information': 'm0:scoreIt',
    'dynamics': 'm0:scoreD',
    # Legacy direct keys
    'A': 'm0:scoreA',
    'S': 'm0:scoreS',
    'F': 'm0:scoreF',
    'I': 'm0:scoreIt',
    'D': 'm0:scoreD',
    'A_score': 'm0:scoreA',
    'S_score': 'm0:scoreS',
    'F_score': 'm0:scoreF',
    'It_score': 'm0:scoreIt',
    'D_score': 'm0:scoreD',
}

REVOI_MAP = {
    'representability': 'm0:scoreR',
    'evolvability': 'm0:scoreE',
    'verifiability': 'm0:scoreV',
    'observability': 'm0:scoreO',
    'interoperability': 'm0:scoreIm',
    'R': 'm0:scoreR',
    'E': 'm0:scoreE',
    'V': 'm0:scoreV',
    'O': 'm0:scoreO',
    'Im': 'm0:scoreIm',
    'R_score': 'm0:scoreR',
    'E_score': 'm0:scoreE',
    'V_score': 'm0:scoreV',
    'O_score': 'm0:scoreO',
    'Im_score': 'm0:scoreIm',
}

def get_value(val):
    """Extrait la valeur numérique d'un score (gère les dict @value)."""
    if isinstance(val, dict):
        if '@value' in val:
            try:
                return float(val['@value'])
            except:
                return 0.0
        # Sinon, peut-être d'autres clés
        return 0.0
    try:
        return float(val) if val is not None else 0.0
    except:
        return 0.0

def normalize_score(value):
    """Convertit une valeur en objet JSON-LD @value."""
    num = get_value(value)
    return {'@value': num, '@type': 'xsd:float'}

def convert_node(node: Dict) -> bool:
    """Convertit les scores dans un nœud. Retourne True si modifié."""
    modified = False
    asfid = {}
    revoi = {}

    # 1. m1:asfidScoring / m1:revoiScoring
    if 'm1:asfidScoring' in node:
        for k, v in node['m1:asfidScoring'].items():
            if k in ASFID_MAP:
                asfid[ASFID_MAP[k]] = v
            else:
                # on ignore les champs comme 'overall', 'interpretation'
                pass
        del node['m1:asfidScoring']
        modified = True
    if 'm1:revoiScoring' in node:
        for k, v in node['m1:revoiScoring'].items():
            if k in REVOI_MAP:
                revoi[REVOI_MAP[k]] = v
        del node['m1:revoiScoring']
        modified = True

    # 2. m0:asfidScores / m0:revoiScores legacy (clés A_score, etc.)
    if 'm0:asfidScores' in node:
        for k, v in node['m0:asfidScores'].items():
            if k in ASFID_MAP:
                asfid[ASFID_MAP[k]] = v
            else:
                # préserver les clés non standard (mean, justification)
                asfid[k] = v
        del node['m0:asfidScores']
        modified = True
    if 'm0:revoiScores' in node:
        for k, v in node['m0:revoiScores'].items():
            if k in REVOI_MAP:
                revoi[REVOI_MAP[k]] = v
            else:
                revoi[k] = v
        del node['m0:revoiScores']
        modified = True

    # 3. Clés directes à la racine (A, S, F, I, D, R, E, V, O, Im)
    for k in list(node.keys()):
        if k in ASFID_MAP:
            asfid[ASFID_MAP[k]] = node.pop(k)
            modified = True
        elif k in REVOI_MAP:
            revoi[REVOI_MAP[k]] = node.pop(k)
            modified = True

    # 4. Si on a des scores, on normalise et on ajoute les blocs SHACL
    if asfid:
        # Normaliser chaque valeur
        asfid_norm = {k: normalize_score(v) for k, v in asfid.items()}
        node['m0:asfidScores'] = asfid_norm
        modified = True
    if revoi:
        revoi_norm = {k: normalize_score(v) for k, v in revoi.items()}
        node['m0:revoiScores'] = revoi_norm
        modified = True

    return modified

def migrate_file(filepath: Path, dry_run: bool = False) -> bool:
    """Traite un fichier JSON-LD. Retourne True si modifié."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Cannot read {filepath.name}: {e}")
        return False

    modified = False
    # Traiter la racine
    if convert_node(data):
        modified = True
    # Traiter les nœuds @graph
    if '@graph' in data:
        for node in data['@graph']:
            if convert_node(node):
                modified = True

    if not modified:
        return False

    if dry_run:
        try:
            rel = filepath.relative_to(Path.cwd())
        except ValueError:
            rel = filepath
        print(f"  🔄 Would migrate: {rel}")
        return True

    # Sauvegarde
    backup = filepath.with_suffix(filepath.suffix + '.bak')
    shutil.copy2(filepath, backup)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    try:
        rel = filepath.relative_to(Path.cwd())
    except ValueError:
        rel = filepath
    print(f"  ✅ Migrated: {rel}")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--instances-dir', type=str, default=None)
    args = parser.parse_args()

    if args.instances_dir:
        instances_root = Path(args.instances_dir)
    else:
        # Auto-détection
        script_dir = Path(__file__).resolve().parent
        for p in [script_dir] + list(script_dir.parents):
            candidate = p / 'instances'
            if candidate.exists() and candidate.is_dir():
                instances_root = candidate
                break
        else:
            print("❌ Could not find 'instances' directory.")
            return

    if not instances_root.exists():
        print(f"❌ Directory not found: {instances_root}")
        return

    print(f"🔍 Scanning M0 files in: {instances_root}")
    print(f"   Dry-run mode: {args.dry_run}")
    print("=" * 80)

    excluded = {'_archives', '__pycache__', 'static'}
    total = 0
    migrated = 0
    for fp in instances_root.rglob("*.jsonld"):
        if any(p in excluded for p in fp.parts):
            continue
        total += 1
        if migrate_file(fp, dry_run=args.dry_run):
            migrated += 1

    print("=" * 80)
    print(f"📊 Summary: {migrated} file(s) would be migrated (or were migrated) out of {total} JSON-LD files.")
    if args.dry_run:
        print("⚠️  Dry-run mode – no files were actually changed. Remove --dry-run to apply.")

if __name__ == "__main__":
    main()