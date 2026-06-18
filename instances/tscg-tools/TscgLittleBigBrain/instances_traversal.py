import json
from pathlib import Path

def inspect_m0_files(root_dir: str = r"E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances"):
    root = Path(root_dir)
    if not root.exists():
        print(f"❌ Directory not found: {root}")
        return

    total_files = 0
    files_with_scores = 0

    for filepath in root.rglob("*.jsonld"):
        # Ignorer les dossiers d'archive
        if any(part in filepath.parts for part in ['_archives', '__pycache__', '.git', '.idea']):
            continue

        total_files += 1
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extraire les scores depuis la racine ou @graph
            asfid_found = False
            revoi_found = False

            # Vérifier dans la racine
            if 'm0:asfidScores' in data:
                asfid_found = True
            if 'm0:revoiScores' in data:
                revoi_found = True

            # Vérifier dans @graph
            if not asfid_found or not revoi_found:
                for node in data.get('@graph', []):
                    if 'm0:asfidScores' in node:
                        asfid_found = True
                    if 'm0:revoiScores' in node:
                        revoi_found = True

            # Vérifier les clés directes (ancien format)
            if not asfid_found:
                if any(data.get(f'm0:score{k.upper()}') for k in ['a','s','f','it','d']):
                    asfid_found = True
            if not revoi_found:
                if any(data.get(f'm0:score{k.upper()}') for k in ['r','e','v','o','im']):
                    revoi_found = True

            if asfid_found or revoi_found:
                files_with_scores += 1
                status = "✅ HAS SCORES"
                print(f"{status:15} {filepath.relative_to(root)}")
            else:
                # Optionnel : afficher les fichiers sans scores (silencieux pour ne pas polluer)
                # print(f"❌ NO SCORES    {filepath.relative_to(root)}")
                pass

        except Exception as e:
            print(f"⚠️ ERROR reading {filepath.name}: {e}")

    print(f"\n📊 Summary: {files_with_scores}/{total_files} JSON-LD files contain ASFID/REVOI scores.")

if __name__ == "__main__":
    inspect_m0_files()