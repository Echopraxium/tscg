#!/usr/bin/env python3
"""
Fix XSD Float Typing by Converting Values to Typed Objects
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18
"""

import json
from pathlib import Path

# Path to M0_FireTriangle.jsonld
FIRE_TRIANGLE_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle.jsonld")

# Properties that need xsd:float values
FLOAT_PROPERTIES = [
    "m0:epistemicGap",
    "m0:mean",
    "eagle_eye:Attractor",
    "eagle_eye:Structure", 
    "eagle_eye:Flow",
    "eagle_eye:Information",
    "eagle_eye:Dynamics",
    "sphinx_eye:Representable",
    "sphinx_eye:Evolvable",
    "sphinx_eye:Verifiable",
    "sphinx_eye:Observable",
    "sphinx_eye:Interoperable"
]

def convert_to_typed_float(value):
    """Convert a numeric value to a typed xsd:float object."""
    if isinstance(value, (int, float)):
        return {
            "@value": str(float(value)),
            "@type": "xsd:float"
        }
    elif isinstance(value, dict) and "@value" in value:
        # Already typed - ensure it's xsd:float
        return {
            "@value": str(float(value["@value"])),
            "@type": "xsd:float"
        }
    return value

def fix_scores_recursive(obj, depth=0):
    """Recursively fix float values in the JSON structure."""
    modifications = []
    
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            # Check if this key needs float typing
            if key in FLOAT_PROPERTIES:
                original = obj[key]
                if isinstance(original, (int, float)):
                    obj[key] = convert_to_typed_float(original)
                    modifications.append(f"Converted {key}: {original} → typed float")
            
            # Recurse into nested objects
            if isinstance(obj[key], (dict, list)):
                nested_mods = fix_scores_recursive(obj[key], depth + 1)
                modifications.extend(nested_mods)
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                nested_mods = fix_scores_recursive(item, depth + 1)
                modifications.extend(nested_mods)
    
    return modifications

def fix_fire_triangle():
    """Fix float typing in M0_FireTriangle.jsonld by converting values."""
    
    print("="*70)
    print("Fixing XSD Float Values in M0_FireTriangle.jsonld")
    print("="*70)
    
    if not FIRE_TRIANGLE_PATH.exists():
        print(f"❌ Error: File not found at {FIRE_TRIANGLE_PATH}")
        return False
    
    print(f"📂 Reading: {FIRE_TRIANGLE_PATH}")
    
    # Read JSON-LD
    with open(FIRE_TRIANGLE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fix all score values recursively
    print(f"\n🔧 Converting numeric values to typed xsd:float objects...")
    modifications = fix_scores_recursive(data)
    
    if modifications:
        print(f"\n✓ Made {len(modifications)} value conversions:")
        for mod in modifications[:10]:  # Show first 10
            print(f"  • {mod}")
        if len(modifications) > 10:
            print(f"  ... and {len(modifications) - 10} more")
        
        # Write back
        print(f"\n💾 Writing changes...")
        with open(FIRE_TRIANGLE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        
        print(f"✅ File updated successfully!")
        print("\n" + "="*70)
        print("Next step: Run SHACL validation to verify:")
        print("cd E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\ontology")
        print("pyshacl -s TSCG_Grammar\\M0_Instances_Schema.shacl.ttl -df json-ld ..\\instances\\poclets\\FireTriangle\\M0_FireTriangle.jsonld")
        print("="*70)
        return True
    else:
        print("\n✓ No numeric values found to convert")
        return False

if __name__ == "__main__":
    import sys
    success = fix_fire_triangle()
    sys.exit(0 if success else 1)
