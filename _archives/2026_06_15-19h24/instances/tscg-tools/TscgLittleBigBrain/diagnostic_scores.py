#!/usr/bin/env python3
"""
diagnostic_scores.py
====================
Parcourt les fichiers JSON‑LD du dossier instances/ et affiche :
- les propriétés de scores ASFID/REVOI trouvées et leurs valeurs
- les fichiers qui ne contiennent aucun score
- les formats de stockage (m0:asfidScores, clés directes, @graph, etc.)

Usage: python diagnostic_scores.py
"""

import json
from pathlib import Path
from collections import defaultdict

def extract_scores_from_node(node):
    """Extrait les dictionnaires asfid et revoi d'un nœud JSON."""
    asfid = {}
    revoi = {}
    if 'm0:asfidScores' in node:
        asfid = node['m0:asfidScores']
    if 'm0:revoiScores' in node:
        revoi = node['m0:revoiScores']
    # Chercher aussi les clés directes (ancien format)
    if not asfid:
        asfid = {k: node.get(k) for k in ['A_score', 'S_score', 'F_score', 'It_score', 'D_score']}
        asfid = {k: v for k, v in asfid.items() if v is not None}
    if not revoi:
        revoi = {k: node.get(k) for k in ['R_score', 'E_score', 'V_score', 'O_score', 'Im_score']}
        revoi = {k: v for k, v in revoi.items() if v is not None}
    return asfid, revoi

def extract_all_scores(data):
    """Parcourt la racine et le @graph pour collecter tous les scores."""
    all_asfid = {}
    all_revoi = {}
    # Racine
    a, r = extract_scores_from_node(data)
    all_asfid.update(a)
    all_revoi.update(r)
    # @graph
    if '@graph' in data and isinstance(data['@graph'], list):
        for node in data['@graph']:
            a, r = extract_scores_from_node(node)
            all_asfid.update(a)
            all_revoi.update(r)
    return all_asfid, all_revoi

def format_value(val):
    """Convertit une valeur JSON‑LD (peut être dict avec @value) en chaîne lisible."""
    if isinstance(val, dict):
        if '@value' in val:
            return f"{val['@value']} (type: {val.get('@type', '?')})"
        return str(val)
    return str(val)

def main():
    # Chemin racine : deux niveaux au‑dessus de l'emplacement du script (supposé dans TscgLittleBigBrain/tests/)
    # Mais on peut aussi demander un chemin en argument.
    # Ici on part du répertoire courant et on cherche "instances" à la racine du dépôt.
    script_dir = Path(__file__).resolve().parent
    # Remonter jusqu'à la racine du dépôt tscg (4 niveaux depuis TscgLittleBigBrain/tests)
    tscg_root = script_dir.parent.parent.parent
    instances_dir = tscg_root / "instances"
    
    if not instances_dir.exists():
        print(f"❌ Dossier instances non trouvé : {instances_dir}")
        print("Veuillez exécuter ce script depuis un endroit où il peut trouver le dépôt tscg.")
        return

    print(f"🔍 Parcours des fichiers JSON‑LD dans : {instances_dir}")
    print("="*80)
    
    excluded_dirs = {'_archives', '__pycache__', '.git', '.idea', 'venv', 'env', 'static'}
    total_files = 0
    files_with_scores = 0
    files_without_scores = []
    
    for filepath in instances_dir.rglob("*.jsonld"):
        if any(part in excluded_dirs for part in filepath.parts):
            continue
        total_files += 1
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            asfid, revoi = extract_all_scores(data)
            if asfid or revoi:
                files_with_scores += 1
                print(f"✅ {filepath.relative_to(instances_dir)}")
                if asfid:
                    print(f"   ASFID scores :")
                    for k, v in asfid.items():
                        print(f"      {k} = {format_value(v)}")
                if revoi:
                    print(f"   REVOI scores :")
                    for k, v in revoi.items():
                        print(f"      {k} = {format_value(v)}")
                print()
            else:
                files_without_scores.append(filepath.relative_to(instances_dir))
        except Exception as e:
            print(f"⚠️  Erreur de lecture {filepath.name} : {e}")
    
    print("="*80)
    print(f"📊 RÉSUMÉ : {files_with_scores} fichiers avec scores sur {total_files} fichiers JSON‑LD.")
    if files_without_scores:
        print(f"\n❌ Fichiers sans scores ({len(files_without_scores)}) :")
        for f in files_without_scores:
            print(f"   - {f}")
    else:
        print("✅ Tous les fichiers JSON‑LD contiennent au moins des scores ASFID ou REVOI.")

if __name__ == "__main__":
    main()