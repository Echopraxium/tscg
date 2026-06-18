# diagnostic_scoring.py
import json
from pathlib import Path

root = Path(r"E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances")
excluded = {'_archives', '__pycache__', '.git', '.idea', 'venv', 'env', 'static'}
found = 0
for fp in root.rglob("*.jsonld"):
    if any(p in excluded for p in fp.parts):
        continue
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Vérifier la présence de m0:asfidScores avec des clés m0:score*
        def has_scores(node):
            asfid = node.get('m0:asfidScores', {})
            revoi = node.get('m0:revoiScores', {})
            return any(k.startswith('m0:score') for k in asfid) or any(k.startswith('m0:score') for k in revoi)
        if has_scores(data):
            found += 1
            print(f"✅ {fp.relative_to(root)}")
        else:
            # chercher dans @graph
            found_in_graph = False
            for node in data.get('@graph', []):
                if has_scores(node):
                    found_in_graph = True
                    break
            if found_in_graph:
                found += 1
                print(f"✅ {fp.relative_to(root)} (dans @graph)")
            else:
                # Affichage des clés pour déboguer
                print(f"❌ {fp.relative_to(root)}")
    except Exception as e:
        print(f"⚠️ {fp.name}: {e}")
print(f"\nTotal with scores: {found}")