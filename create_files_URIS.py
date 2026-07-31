import subprocess
import sys

def generate_github_urls():
    """
    Génère files.txt avec les URLs raw GitHub des fichiers versionnés.

    Source = `git ls-files` (et NON un os.walk du disque local).
    Pourquoi : le disque local Windows peut diverger en CASSE de ce qui est
    réellement versionné (ex. local `Kidneys/` vs repo `kidneys/`,
    `M0_Vco.jsonld` vs `M0_VCO.jsonld`). GitHub raw est sensible à la casse,
    donc lire le disque produit des URLs en 404. `git ls-files` donne les
    chemins EXACTS du repo (casse comprise) et exclut automatiquement tout ce
    qui est gitignoré (node_modules, _protos/private, etc.).
    """

    # ATTENTION à la casse du compte : GitHub raw est aussi sensible ici.
    REPO_URL = "https://raw.githubusercontent.com/Echopraxium/tscg/main/"
    OUTPUT_FILE = "files.txt"

    INCLUDED_EXTENSIONS = {'.jsonld', '.ttl', '.txt', '.md', '.bat', '.py'}

    # Segments de chemin à exclure malgré tout (au cas où ils seraient versionnés).
    # node_modules / _protos/private ne sont normalement PAS versionnés -> git
    # les exclut déjà ; ceci n'est qu'une ceinture supplémentaire.
    EXCLUDED_PATH_SEGMENTS = {'.git', '_archives', 'api_key'}
    EXCLUDED_EXTENSIONS = {'.api_key'}
    EXCLUDED_NAME_PATTERNS = ['apik']

    print("=" * 60)
    print("Génération de files.txt depuis git ls-files (casse repo exacte)")
    print("=" * 60)

    # 1. Récupérer les fichiers versionnés (chemins en '/' et casse du repo)
    try:
        raw = subprocess.check_output(
            ["git", "ls-files"], text=True, encoding="utf-8"
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\n❌ Échec de `git ls-files` : {e}")
        print("   Lance ce script depuis la racine du dépôt git.")
        return
    tracked = [p for p in raw.splitlines() if p.strip()]

    # 2. Filtrer
    urls = []
    skipped_ext, skipped_seg, skipped_name = 0, 0, 0
    for path in tracked:
        segments = path.split("/")
        fname = segments[-1]

        ext = "." + fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
        if ext in EXCLUDED_EXTENSIONS:
            skipped_ext += 1
            continue
        if any(pat in fname.lower() for pat in EXCLUDED_NAME_PATTERNS):
            skipped_name += 1
            continue
        if ext not in INCLUDED_EXTENSIONS:
            skipped_ext += 1
            continue
        if any(seg in EXCLUDED_PATH_SEGMENTS for seg in segments[:-1]):
            skipped_seg += 1
            continue

        urls.append(REPO_URL + path.replace(" ", "%20"))

    urls = sorted(set(urls))

    # 3. Écrire en LF (jamais CRLF) pour des URLs propres et portables
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        for u in urls:
            f.write(u + "\n")

    # 4. Rapport
    print(f"\n✅ {len(urls)} URLs écrites dans {OUTPUT_FILE}")
    ext_counts = {}
    for u in urls:
        e = "." + u.rsplit(".", 1)[-1].lower()
        ext_counts[e] = ext_counts.get(e, 0) + 1
    print("\n📊 Répartition par extension :")
    for e in sorted(INCLUDED_EXTENSIONS):
        print(f"  {e}: {ext_counts.get(e, 0)}")
    print(f"\n(ignorés : {skipped_ext} hors extension, "
          f"{skipped_seg} segment exclu, {skipped_name} nom sensible)")

    # 5. Garde-fou : casse du compte GitHub
    print("\n🔎 Rappel : GitHub raw est sensible à la casse — pour le chemin ET")
    print("   pour le nom du compte. Vérifie que 'Echopraxium' est la bonne casse.")
    print("   Un échantillon à tester dans un navigateur :")
    for u in urls[:3]:
        print(f"     {u}")


if __name__ == "__main__":
    generate_github_urls()
    if sys.stdin and sys.stdin.isatty():
        input("\nAppuyez sur Entrée pour quitter...")
