#!/usr/bin/env python3
"""
Fix M0_CellSignalingModes.jsonld - Extract inline components to @graph objects
Author: Echopraxium with the collaboration of Claude AI
"""
import json
from pathlib import Path

def fix_cellsignaling(input_file, output_file):
    """Extract inline components from m0:components array to separate @graph objects"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modifications = []
    
    # Get ontology (should be @graph[0])
    if "@graph" not in data or len(data["@graph"]) == 0:
        print("❌ ERROR: No @graph found")
        return False
    
    ontology = data["@graph"][0]
    
    # Fix 1: Remove redundant rdf:type
    if "rdf:type" in ontology:
        del ontology["rdf:type"]
        modifications.append("Removed redundant rdf:type")
    
    # Fix 2: m2:ontologyCategory → m3:ontologyType
    if "m2:ontologyCategory" in ontology:
        ontology["m3:ontologyType"] = {"@id": "m3:Poclet"}
        del ontology["m2:ontologyCategory"]
        modifications.append("m2:ontologyCategory → m3:ontologyType")
    
    # Fix 3: m0:domain → m1:domain
    if "m0:domain" in ontology:
        ontology["m1:domain"] = ontology.pop("m0:domain")
        modifications.append("m0:domain → m1:domain")
    
    # Fix 4: Extract inline components to separate @graph objects
    if "m0:components" in ontology:
        components = ontology.pop("m0:components")
        
        if isinstance(components, list):
            # Add each component as a separate @graph object
            for component in components:
                # Change @type from m2:Component to owl:NamedIndividual
                if "@type" in component:
                    component["@type"] = "owl:NamedIndividual"
                
                # Add to @graph
                data["@graph"].append(component)
            
            modifications.append(f"Extracted {len(components)} inline components to @graph objects")
            
            # Add reference to components in ontology
            component_ids = [comp["@id"] for comp in components if "@id" in comp]
            ontology["m0:hasComponent"] = component_ids
            modifications.append(f"Added m0:hasComponent references")
    
    # Fix 5: Update version
    ontology["owl:versionInfo"] = "1.1.0"
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
    
    return True

if __name__ == "__main__":
    input_file = Path("/mnt/user-data/uploads/M0_CellSignalingModes.jsonld")
    output_file = Path("/home/claude/M0_CellSignalingModes_FIXED.jsonld")
    
    print("="*70)
    print("FIXING M0_CellSignalingModes.jsonld")
    print("="*70)
    
    fix_cellsignaling(input_file, output_file)
