#!/usr/bin/env python3
"""
Clean Poclet @id and add m2:ontologyCategory property
VERSION 2.0 - Recursive search in subdirectories

Removes suffixes like _Poclet, _Ontology, M0_ from @id
Adds m2:ontologyCategory: "Poclet" property

Author: Echopraxium with the collaboration of Claude AI
Date: 2026-01-25
"""

import json
import re
from pathlib import Path

def clean_ontology_id(id_string: str, namespace: str) -> str:
    """
    Nettoie l'@id en supprimant les suffixes redondants
    
    Args:
        id_string: L'@id actuel (ex: "m0:yggdrasil:Yggdrasil_Poclet")
        namespace: Le namespace du poclet (ex: "m0:yggdrasil")
    
    Returns:
        L'@id nettoyé (ex: "m0:yggdrasil:Yggdrasil")
    """
    # Extraire la partie locale (après le dernier :)
    parts = id_string.split(":")
    if len(parts) < 3:
        return id_string
    
    local_part = parts[-1]
    
    # Supprimer les suffixes redondants
    local_part = re.sub(r'_Poclet$', '', local_part)
    local_part = re.sub(r'_Ontology$', '', local_part)
    local_part = re.sub(r'^M0_', '', local_part)
    
    # Reconstruire l'@id
    return f"{namespace}:{local_part}"

def process_poclet(filepath: Path) -> bool:
    """Traite un fichier poclet"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraire le namespace M0
        context = data.get("@context", {})
        m0_namespaces = [k for k in context.keys() if k.startswith("m0:")]
        
        if not m0_namespaces:
            print(f"⚠️  No M0 namespace found")
            return False
        
        namespace = m0_namespaces[0]
        
        # Traiter @graph si présent
        modified = False
        if "@graph" in data:
            for item in data["@graph"]:
                if isinstance(item, dict) and item.get("@type") == "owl:Ontology":
                    old_id = item.get("@id", "")
                    new_id = clean_ontology_id(old_id, namespace)
                    
                    if old_id != new_id:
                        item["@id"] = new_id
                        print(f"  ✓ @id: {old_id} → {new_id}")
                        modified = True
                    
                    # Ajouter m2:ontologyCategory si absent
                    if "m2:ontologyCategory" not in item:
                        item["m2:ontologyCategory"] = "Poclet"
                        print(f"  ✓ Added m2:ontologyCategory: Poclet")
                        modified = True
        
        # Traiter niveau racine si pas de @graph
        elif data.get("@type") == "owl:Ontology":
            old_id = data.get("@id", "")
            new_id = clean_ontology_id(old_id, namespace)
            
            if old_id != new_id:
                data["@id"] = new_id
                print(f"  ✓ @id: {old_id} → {new_id}")
                modified = True
            
            if "m2:ontologyCategory" not in data:
                data["m2:ontologyCategory"] = "Poclet"
                print(f"  ✓ Added m2:ontologyCategory: Poclet")
                modified = True
        
        if modified:
            # Sauvegarder
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        else:
            print(f"  - No changes needed")
            return False
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python clean_poclet_ids.py <poclets_dir>")
        print()
        print("Examples:")
        print("  python clean_poclet_ids.py .")
        print("  python clean_poclet_ids.py E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\system-models\\poclets")
        sys.exit(1)
    
    poclets_dir = Path(sys.argv[1])
    
    if not poclets_dir.exists():
        print(f"❌ Directory not found: {poclets_dir}")
        sys.exit(1)
    
    print("=" * 80)
    print("🧹 CLEANING POCLET @id AND ADDING ontologyCategory (Recursive)")
    print("=" * 80)
    print()
    print(f"Searching in: {poclets_dir.absolute()}")
    print()
    
    # Chercher récursivement tous les fichiers M0_*.jsonld
    files = sorted(poclets_dir.rglob("M0_*.jsonld"))
    
    if not files:
        print("⚠️  No M0_*.jsonld files found!")
        print()
        print("Listing directory contents:")
        print("-" * 80)
        
        # Afficher la structure
        subdirs = [d for d in poclets_dir.iterdir() if d.is_dir()]
        if subdirs:
            print("Subdirectories found:")
            for d in sorted(subdirs):
                jsonld_files = list(d.glob("*.jsonld"))
                print(f"  {d.name}/ ({len(jsonld_files)} files)")
                for f in jsonld_files:
                    print(f"    - {f.name}")
        else:
            print("No subdirectories found")
        
        all_jsonld = list(poclets_dir.rglob("*.jsonld"))
        if all_jsonld:
            print()
            print(f"All .jsonld files found ({len(all_jsonld)}):")
            for f in sorted(all_jsonld):
                rel = f.relative_to(poclets_dir)
                print(f"  {rel}")
        
        sys.exit(1)
    
    print(f"Found {len(files)} file(s) to process:")
    for f in files:
        rel = f.relative_to(poclets_dir)
        print(f"  - {rel}")
    print()
    print("-" * 80)
    print()
    
    modified_count = 0
    total_count = 0
    
    for filepath in files:
        rel_path = filepath.relative_to(poclets_dir)
        print(f"📄 {rel_path}:")
        total_count += 1
        if process_poclet(filepath):
            modified_count += 1
        print()
    
    print("=" * 80)
    print(f"✅ Modified: {modified_count}/{total_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()
