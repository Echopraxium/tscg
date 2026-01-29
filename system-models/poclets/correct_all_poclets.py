#!/usr/bin/env python3
"""
TSCG Poclet Corrector - Applique les corrections standardisées à tous les poclets M0

Modifications:
1. Base URI: ontology/poclets → system-models/poclets
2. Namespaces standardisés: m0:{poclet_name} en snake_case
3. Ordre @context: W3C (alpha) puis M3→M2→M1→M0
4. M3 simplifié (m3 au lieu de m3:eagle_eye/sphinx_eye)
5. owl:imports standardisés
6. Métadonnées complètes

Author: Echopraxium with the collaboration of Claude AI
Version: 1.0.0
Date: 2026-01-25
"""

import json
import re
from pathlib import Path
from typing import Dict, Any
from collections import OrderedDict

# Mapping des poclets
POCLETS_MAPPING = {
    "M0_AdaptiveImmuneResponse.jsonld": {
        "folder": "adaptive_immune_response",
        "namespace": "m0:adaptive_immune_response"
    },
    "M0_BloodPressureControl.jsonld": {
        "folder": "blood_pressure_control",
        "namespace": "m0:blood_pressure_control"
    },
    "M0_ButterflyMetamorphosis.jsonld": {
        "folder": "butterfly_metamorphosis",
        "namespace": "m0:butterfly_metamorphosis"
    },
    "M0_CellSignalingModes.jsonld": {
        "folder": "cell_signaling_modes",
        "namespace": "m0:cell_signaling_modes"
    },
    "M0_ColorSynthesis_Federated.jsonld": {
        "folder": "color_synthesis",
        "namespace": "m0:color_synthesis"
    },
    "M0_HSL_Additive.jsonld": {
        "folder": "color_synthesis",
        "namespace": "m0:color_synthesis"
    },
    "M0_RGB_Additive.jsonld": {
        "folder": "color_synthesis",
        "namespace": "m0:color_synthesis"
    },
    "M0_CMY_Subtractive.jsonld": {
        "folder": "color_synthesis",
        "namespace": "m0:color_synthesis"
    },
    "M0_CMYK_Subtractive.jsonld": {
        "folder": "color_synthesis",
        "namespace": "m0:color_synthesis"
    },
    "M0_ComplexChemicalSynapse.jsonld": {
        "folder": "complex_chemical_synapse",
        "namespace": "m0:complex_chemical_synapse"
    },
    "M0_ExposureTriangle.jsonld": {
        "folder": "exposure_triangle",
        "namespace": "m0:exposure_triangle"
    },
    "M0_FireTriangle.jsonld": {
        "folder": "fire_triangle",
        "namespace": "m0:fire_triangle"
    },
    "M0_FourStrokeEngine.jsonld": {
        "folder": "four_stroke_engine",
        "namespace": "m0:four_stroke_engine"
    },
    "M0_MTG_ColorWheel.jsonld": {
        "folder": "mtg_color_wheel",
        "namespace": "m0:mtg_color_wheel"
    },
    "M0_TPACK.jsonld": {
        "folder": "tpack",
        "namespace": "m0:tpack"
    },
    "M0_Yggdrasil.jsonld": {
        "folder": "yggdrasil",
        "namespace": "m0:yggdrasil"
    }
}

BASE_URI = "https://raw.githubusercontent.com/Echopraxium/tscg/main"

def create_standard_context(poclet_info: Dict[str, str], m1_domains: list = None) -> OrderedDict:
    """Crée un @context standardisé"""
    context = OrderedDict()
    
    # W3C namespaces (alphabétique)
    context["dcterms"] = "http://purl.org/dc/terms/"
    context["owl"] = "http://www.w3.org/2002/07/owl#"
    context["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    context["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
    context["skos"] = "http://www.w3.org/2004/02/skos/core#"
    context["xsd"] = "http://www.w3.org/2001/XMLSchema#"
    
    # M3 (simplifié - Genesis inclut Eagle + Sphinx)
    context["m3"] = f"{BASE_URI}/ontology/M3_GenesisSpace.jsonld#"
    
    # M2
    context["m2"] = f"{BASE_URI}/ontology/M2_MetaConcepts.jsonld#"
    
    # M1 core (toujours présent)
    context["m1:core"] = f"{BASE_URI}/ontology/M1_CoreConcepts.jsonld#"
    
    # M1 domains (optionnels)
    if m1_domains:
        for domain in sorted(m1_domains):
            context[f"m1:{domain}"] = f"{BASE_URI}/ontology/M1_extensions/M1_{domain.capitalize()}.jsonld#"
    
    # M0 (ce poclet)
    folder = poclet_info["folder"]
    filename = poclet_info["filename"]
    context[poclet_info["namespace"]] = f"{BASE_URI}/system-models/poclets/{folder}/{filename}#"
    
    return context

def detect_m1_domains(data: Dict[str, Any]) -> list:
    """Détecte les domaines M1 utilisés dans le fichier"""
    data_str = json.dumps(data)
    domains = []
    
    # Patterns de domaines connus
    domain_patterns = {
        "biology": r'"m1:biology:|m1bio:',
        "chemistry": r'"m1:chemistry:|m1chem:',
        "mythology": r'"m1:mythology:|m1myth:',
        "optics": r'"m1:optics:|m1optics:',
        "photography": r'"m1:photography:|m1photo:'
    }
    
    for domain, pattern in domain_patterns.items():
        if re.search(pattern, data_str):
            domains.append(domain)
    
    return domains

def fix_namespace_references(obj: Any, old_to_new: Dict[str, str]) -> Any:
    """Corrige récursivement les références de namespace"""
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            # Corriger les clés
            new_key = key
            for old, new in old_to_new.items():
                if key.startswith(old):
                    new_key = key.replace(old, new, 1)
                    break
            
            # Corriger les valeurs
            new_obj[new_key] = fix_namespace_references(value, old_to_new)
        return new_obj
    
    elif isinstance(obj, list):
        return [fix_namespace_references(item, old_to_new) for item in obj]
    
    elif isinstance(obj, str):
        # Corriger les compact IRIs dans les strings
        for old, new in old_to_new.items():
            if obj.startswith(old):
                return obj.replace(old, new, 1)
        return obj
    
    else:
        return obj

def correct_poclet(input_path: str, output_path: str) -> bool:
    """Corrige un fichier poclet"""
    try:
        # Charger le fichier
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        filename = Path(input_path).name
        if filename not in POCLETS_MAPPING:
            print(f"⚠️  {filename} not in mapping, skipping")
            return False
        
        poclet_info = POCLETS_MAPPING[filename].copy()
        poclet_info["filename"] = filename
        
        # Détecter les domaines M1 utilisés
        m1_domains = detect_m1_domains(data)
        
        # Créer le nouveau @context standardisé
        new_context = create_standard_context(poclet_info, m1_domains)
        
        # Mapper les anciens namespaces vers les nouveaux
        old_to_new = {}
        
        # M3: Simplifier
        old_to_new["m3:eagle_eye:"] = "m3:"
        old_to_new["m3:sphinx_eye:"] = "m3:"
        old_to_new["m3:genesis:"] = "m3:"
        
        # M1: Standardiser
        old_to_new["m1optics:"] = "m1:optics:"
        old_to_new["m1photo:"] = "m1:photography:"
        old_to_new["m1bio:"] = "m1:biology:"
        old_to_new["m1chem:"] = "m1:chemistry:"
        old_to_new["m1myth:"] = "m1:mythology:"
        
        # M0: Détecter l'ancien namespace et le remplacer
        if "@context" in data and isinstance(data["@context"], dict):
            for key, value in data["@context"].items():
                if key.startswith("m0:") or key.startswith("m0_"):
                    old_to_new[key + ":"] = poclet_info["namespace"] + ":"
        
        # Corriger les références de namespace dans tout le fichier
        data = fix_namespace_references(data, old_to_new)
        
        # Remplacer @context
        data["@context"] = new_context
        
        # Vérifier/corriger owl:imports
        if "@graph" in data:
            for item in data["@graph"]:
                if isinstance(item, dict) and item.get("@type") == "owl:Ontology":
                    # Standardiser les imports
                    standard_imports = [
                        f"{BASE_URI}/ontology/M1_CoreConcepts.jsonld",
                        f"{BASE_URI}/ontology/M2_MetaConcepts.jsonld"
                    ]
                    
                    # Ajouter imports M1 si nécessaire
                    for domain in m1_domains:
                        import_uri = f"{BASE_URI}/ontology/M1_extensions/M1_{domain.capitalize()}.jsonld"
                        if import_uri not in standard_imports:
                            standard_imports.append(import_uri)
                    
                    item["owl:imports"] = standard_imports
                    
                    # Vérifier métadonnées requises
                    if "dcterms:creator" not in item:
                        item["dcterms:creator"] = "Echopraxium with the collaboration of Claude AI"
        
        # Sauvegarder
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {filename} corrected")
        return True
    
    except Exception as e:
        print(f"❌ Error correcting {input_path}: {e}")
        return False

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python correct_all_poclets.py <input_dir> [output_dir]")
        print("Example: python correct_all_poclets.py /mnt/user-data/uploads ./corrected")
        sys.exit(1)
    
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./corrected_poclets")
    
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*80}")
    print("🔧 TSCG POCLET CORRECTOR")
    print(f"{'='*80}\n")
    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}\n")
    
    success_count = 0
    total_count = 0
    
    for filename in POCLETS_MAPPING.keys():
        input_path = input_dir / filename
        output_path = output_dir / filename
        
        if not input_path.exists():
            print(f"⚠️  {filename} not found, skipping")
            continue
        
        total_count += 1
        if correct_poclet(str(input_path), str(output_path)):
            success_count += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Corrected: {success_count}/{total_count}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
