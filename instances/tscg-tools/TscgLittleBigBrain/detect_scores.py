import json
from pathlib import Path

def has_any_score(node):
    """Vérifie si un nœud contient des scores (sous n'importe quelle forme)."""
    # SHACL
    if 'm0:asfidScores' in node or 'm0:revoiScores' in node:
        return True
    # Legacy dans m0:asfidScores avec A_score etc.
    asfid = node.get('m0:asfidScores', {})
    if any(k in asfid for k in ['A_score','S_score','F_score','It_score','D_score']):
        return True
    # Clés directes
    if any(k in node for k in ['A','S','F','I','D','R','E','V','O','Im']):
        return True
    # m1:asfidScoring
    if 'm1:asfidScoring' in node or 'm1:revoiScoring' in node:
        return True
    return False

def main():
    root = Path(r"E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances")
    if not root.exists():
        print("Instances directory not found")
        return

    excluded = {'_archives', '__pycache__', 'static'}
    total = 0
    with_scores = 0
    files_with_scores = []

    for fp in root.rglob("*.jsonld"):
        if any(p in excluded for p in fp.parts):
            continue
        total += 1
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Vérifier la racine
            found = has_any_score(data)
            if not found and '@graph' in data:
                for node in data['@graph']:
                    if has_any_score(node):
                        found = True
                        break
            if found:
                with_scores += 1
                files_with_scores.append(fp.relative_to(root))
        except Exception as e:
            print(f"Error {fp.name}: {e}")
    print(f"Total JSON-LD files: {total}")
    print(f"Files with scores (any format): {with_scores}")
    print("\nList of files with scores:")
    for f in files_with_scores:
        print(f"  {f}")

if __name__ == "__main__":
    main()