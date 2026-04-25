#!/usr/bin/env python3
"""
Fix M0_ButterflyMetamorphosis.jsonld - Remove custom classes, fix @type
Author: Echopraxium with the collaboration of Claude AI
"""
import json
from pathlib import Path

def fix_butterfly(input_file, output_file):
    """Remove custom m0:Poclet and m0:DevelopmentalPole classes"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modifications = []
    
    # Get @graph
    if "@graph" not in data or len(data["@graph"]) == 0:
        print("❌ ERROR: No @graph found")
        return False
    
    ontology = data["@graph"][0]
    
    # Fix 1: m2:ontologyCategory → m3:ontologyType
    if "m2:ontologyCategory" in ontology:
        ontology["m3:ontologyType"] = {"@id": "m3:Poclet"}
        del ontology["m2:ontologyCategory"]
        modifications.append("m2:ontologyCategory → m3:ontologyType")
    
    # Fix 2: m0:domain → m1:domain
    if "m0:domain" in ontology:
        ontology["m1:domain"] = ontology.pop("m0:domain")
        modifications.append("m0:domain → m1:domain")
    
    # Fix 3: Remove custom class definitions (@graph[1] and @graph[2])
    # Look for m0:Poclet and m0:DevelopmentalPole class definitions
    new_graph = [ontology]  # Keep @graph[0] (the ontology metadata)
    
    removed_classes = []
    converted_instances = 0
    
    for obj in data["@graph"][1:]:
        obj_id = obj.get("@id", "")
        obj_type = obj.get("@type", "")
        
        # Skip class definitions (m0:Poclet, m0:DevelopmentalPole)
        if obj_id in ["m0:Poclet", "m0:DevelopmentalPole"]:
            removed_classes.append(obj_id)
            continue
        
        # Convert instances using m0:DevelopmentalPole as @type
        if isinstance(obj_type, list) and "m0:DevelopmentalPole" in obj_type:
            obj["@type"] = "owl:NamedIndividual"
            converted_instances += 1
        elif obj_type == "m0:DevelopmentalPole":
            obj["@type"] = "owl:NamedIndividual"
            converted_instances += 1
        
        new_graph.append(obj)
    
    data["@graph"] = new_graph
    
    if removed_classes:
        modifications.append(f"Removed custom class definitions: {', '.join(removed_classes)}")
    
    if converted_instances > 0:
        modifications.append(f"Converted {converted_instances} instances to owl:NamedIndividual")
    
    # Fix 4: Update version
    ontology["owl:versionInfo"] = "1.1.0"
    if "dcterms:created" in ontology:
        ontology["dcterms:modified"] = "2026-04-20"
    modifications.append("Updated version to 1.1.0")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print(f"\n✅ SUCCESS: {output_file}")
    print(f"   Applied {len(modifications)} modifications:")
    for mod in modifications:
        print(f"   - {mod}")
    
    print(f"\n📊 STATS:")
    print(f"   - Original @graph objects: {len(data['@graph']) + len(removed_classes)}")
    print(f"   - Removed class definitions: {len(removed_classes)}")
    print(f"   - Final @graph objects: {len(data['@graph'])}")
    
    return True

if __name__ == "__main__":
    input_file = Path("/mnt/user-data/uploads/M0_ButterflyMetamorphosis.jsonld")
    output_file = Path("/home/claude/M0_ButterflyMetamorphosis_FIXED.jsonld")
    
    print("="*70)
    print("FIXING M0_ButterflyMetamorphosis.jsonld")
    print("="*70)
    
    fix_butterfly(input_file, output_file)
