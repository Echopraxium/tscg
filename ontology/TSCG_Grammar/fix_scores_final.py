#!/usr/bin/env python3
"""
Fix ASFID/REVOI Scores - Final Version
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18

Converts numeric scores to typed xsd:float objects.
"""

import json
from pathlib import Path

FIRE_TRIANGLE_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle.jsonld")

# Score property keys as they appear in the file
ASFID_KEYS = ["A", "S", "F", "I_asfid", "D"]  # I_asfid = Information (Territory)
REVOI_KEYS = ["R", "E", "V", "O", "I_revoi"]  # I_revoi = Interoperability (Map)
OTHER_FLOAT_KEYS = ["m0:mean"]

def convert_to_typed_float(value):
    """Convert a numeric value to a typed xsd:float object."""
    if isinstance(value, (int, float)):
        return {
            "@value": str(float(value)),
            "@type": "xsd:float"
        }
    elif isinstance(value, dict):
        # Already typed or reference
        return value
    return value

def fix_scores_in_object(obj, keys_to_fix):
    """Fix numeric scores in an object by converting to typed floats."""
    modifications = []
    
    for key in keys_to_fix:
        if key in obj:
            original = obj[key]
            if isinstance(original, (int, float)):
                obj[key] = convert_to_typed_float(original)
                modifications.append(f"Converted {key}: {original} → typed float")
            elif isinstance(original, dict) and "@value" in original:
                # Already typed - ensure xsd:float
                if original.get("@type") != "xsd:float":
                    original["@type"] = "xsd:float"
                    modifications.append(f"Updated type for {key}")
    
    return modifications

def main():
    """Main entry point."""
    print("="*70)
    print("Fixing ASFID/REVOI Scores in M0_FireTriangle.jsonld")
    print("="*70)
    
    if not FIRE_TRIANGLE_PATH.exists():
        print(f"❌ File not found: {FIRE_TRIANGLE_PATH}")
        return 1
    
    print(f"📂 Reading: {FIRE_TRIANGLE_PATH}\n")
    
    # Read JSON-LD
    with open(FIRE_TRIANGLE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Navigate to ontology in @graph
    if "@graph" in data and len(data["@graph"]) > 0:
        ontology = data["@graph"][0]
        print("✓ Found ontology in @graph[0]\n")
    else:
        print("❌ No @graph structure found")
        return 1
    
    all_modifications = []
    
    # Fix ASFID scores
    print("🔧 Processing m0:asfidScores...")
    if "m0:asfidScores" in ontology:
        asfid_scores = ontology["m0:asfidScores"]
        mods = fix_scores_in_object(asfid_scores, ASFID_KEYS + OTHER_FLOAT_KEYS)
        all_modifications.extend(mods)
        print(f"  ✓ {len(mods)} modifications in ASFID")
    else:
        print("  ⚠ m0:asfidScores not found")
    
    # Fix REVOI scores
    print("\n🔧 Processing m0:revoiScores...")
    if "m0:revoiScores" in ontology:
        revoi_scores = ontology["m0:revoiScores"]
        mods = fix_scores_in_object(revoi_scores, REVOI_KEYS + OTHER_FLOAT_KEYS)
        all_modifications.extend(mods)
        print(f"  ✓ {len(mods)} modifications in REVOI")
    else:
        print("  ⚠ m0:revoiScores not found")
    
    # Fix epistemicGap (should already be done)
    print("\n🔧 Checking m0:epistemicGap...")
    if "m0:epistemicGap" in ontology:
        original = ontology["m0:epistemicGap"]
        if isinstance(original, (int, float)):
            ontology["m0:epistemicGap"] = convert_to_typed_float(original)
            all_modifications.append("Converted m0:epistemicGap")
            print("  ✓ Converted")
        elif isinstance(original, dict) and "@type" in original:
            print(f"  ✓ Already typed as {original['@type']}")
        else:
            print(f"  ? Unexpected format: {type(original)}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if all_modifications:
        print(f"\n✓ Made {len(all_modifications)} total modifications:")
        for mod in all_modifications:
            print(f"  • {mod}")
        
        # Write back
        print(f"\n💾 Writing changes to {FIRE_TRIANGLE_PATH}...")
        with open(FIRE_TRIANGLE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        
        print("✅ File updated successfully!")
        print("\n" + "="*70)
        print("Next step: Run SHACL validation")
        print("="*70)
        print("cd E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\ontology")
        print("pyshacl -s TSCG_Grammar\\M0_Instances_Schema.shacl.ttl -df json-ld ..\\instances\\poclets\\FireTriangle\\M0_FireTriangle.jsonld")
        print("="*70)
        return 0
    else:
        print("\n⚠ No modifications needed - all scores already typed correctly")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
