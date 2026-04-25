#!/usr/bin/env python3
"""
Fix M0_BloodPressureControl.jsonld - Replace tscg: namespace with m0:
Author: Echopraxium with the collaboration of Claude AI
"""
import json
import re
from pathlib import Path

def fix_bloodpressure(input_file, output_file):
    """Replace all tscg: namespace violations with m0:"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modifications = []
    
    # Count tscg: occurrences before
    tscg_count_before = len(re.findall(r'"tscg:', content))
    
    # Fix 1: Global replace "tscg: → "m0: in entire file
    content_fixed = re.sub(r'"tscg:', '"m0:', content)
    
    tscg_count_after = len(re.findall(r'"tscg:', content_fixed))
    
    if tscg_count_before > 0:
        modifications.append(f"Replaced {tscg_count_before - tscg_count_after} tscg: → m0:")
    
    # Parse JSON
    data = json.loads(content_fixed)
    
    # Get @graph
    if "@graph" not in data or len(data["@graph"]) == 0:
        print("❌ ERROR: No @graph found")
        return False
    
    # Fix ontology (@graph[0])
    ontology = data["@graph"][0]
    
    # Fix 2: Remove m2:ontologyCategory if present (m3:ontologyType already exists)
    if "m2:ontologyCategory" in ontology:
        del ontology["m2:ontologyCategory"]
        modifications.append("Removed m2:ontologyCategory (m3:ontologyType already present)")
    
    # Fix 3: Add m1:domain if not present
    if "m1:domain" not in ontology and "m0:domain" in ontology:
        # Extract domain from m0:domain
        domain_value = ontology.pop("m0:domain")
        # Parse "Physiology / Cardiovascular System" → "Physiology"
        if "/" in domain_value:
            domain_value = domain_value.split("/")[0].strip()
        ontology["m1:domain"] = domain_value
        modifications.append(f"m0:domain → m1:domain ('{domain_value}')")
    elif "m1:domain" not in ontology:
        ontology["m1:domain"] = "Physiology"
        modifications.append("Added m1:domain: 'Physiology'")
    
    # Fix 4: Fix @type in all @graph objects
    fixed_types = 0
    for i, obj in enumerate(data["@graph"]):
        obj_type = obj.get("@type", None)
        
        # Fix @type: "m0:Poclet" → "owl:NamedIndividual" (for @graph[1+])
        if i > 0:  # Skip @graph[0] which should be owl:Ontology
            if obj_type == "m0:Poclet":
                obj["@type"] = "owl:NamedIndividual"
                fixed_types += 1
            elif obj_type == "m0:EffectorSystem":
                obj["@type"] = "owl:NamedIndividual"
                fixed_types += 1
    
    if fixed_types > 0:
        modifications.append(f"Fixed {fixed_types} custom @type (m0:Poclet, m0:EffectorSystem → owl:NamedIndividual)")
    
    # Fix 5: Rename ORIVE properties (ORIVE is obsolete, should be REVOI)
    # But scores are already calculated, so just rename the property names
    orive_renamed = 0
    for obj in data["@graph"]:
        if "m0:oriveScore" in obj:
            # Rename m0:oriveScore → m0:revoiScore
            obj["m0:revoiScore"] = obj.pop("m0:oriveScore")
            orive_renamed += 1
            
            # Also rename nested properties
            revoi_score = obj["m0:revoiScore"]
            if isinstance(revoi_score, dict):
                if "m0:oriveTotal" in revoi_score:
                    revoi_score["m0:revoiTotal"] = revoi_score.pop("m0:oriveTotal")
                
                # Rename ORIVE dimension names → REVOI
                renames = {
                    "m0:observabilityScore": "m0:observabilityScore",  # O → O (no change)
                    "m0:reproducibilityScore": "m0:representabilityScore",  # R → R (but different R!)
                    "m0:interoperabilityScore": "m0:interoperabilityScore",  # I → I (no change)
                    "m0:validityScore": "m0:verifiabilityScore",  # V → V (different V!)
                    "m0:expressivenessScore": "m0:evolvabilityScore"  # E → E (different E!)
                }
                
                for old_key, new_key in renames.items():
                    if old_key in revoi_score and old_key != new_key:
                        revoi_score[new_key] = revoi_score.pop(old_key)
    
    if orive_renamed > 0:
        modifications.append(f"Renamed {orive_renamed} m0:oriveScore → m0:revoiScore (ORIVE→REVOI terminology)")
    
    # Fix 6: Update version
    ontology["owl:versionInfo"] = "1.1.0"
    if "m0:dateCreated" in ontology:
        ontology["dcterms:modified"] = "2026-04-20"
    elif "dcterms:created" in ontology:
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
    print(f"   - tscg: occurrences before: {tscg_count_before}")
    print(f"   - tscg: occurrences after: {tscg_count_after}")
    print(f"   - @graph objects: {len(data['@graph'])}")
    
    return True

if __name__ == "__main__":
    input_file = Path("/mnt/user-data/uploads/M0_BloodPressureControl.jsonld")
    output_file = Path("/home/claude/M0_BloodPressureControl_FIXED.jsonld")
    
    print("="*70)
    print("FIXING M0_BloodPressureControl.jsonld")
    print("="*70)
    
    fix_bloodpressure(input_file, output_file)
