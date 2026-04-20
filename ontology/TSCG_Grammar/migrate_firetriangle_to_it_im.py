#!/usr/bin/env python3
"""
Migrate FireTriangle from I_asfid/I_revoi to It/Im
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18
"""

import json
from pathlib import Path

FIRE_TRIANGLE_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle.jsonld")

def main():
    """Migrate FireTriangle to use It/Im instead of I_asfid/I_revoi."""
    
    print("="*70)
    print("Migrating FireTriangle: I_asfid → It, I_revoi → Im")
    print("="*70)
    
    if not FIRE_TRIANGLE_PATH.exists():
        print(f"❌ File not found: {FIRE_TRIANGLE_PATH}")
        return 1
    
    print(f"📂 Reading: {FIRE_TRIANGLE_PATH}\n")
    
    # Read JSON-LD
    with open(FIRE_TRIANGLE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modifications = []
    
    # Update @context
    context = data.get("@context", {})
    
    if "I_asfid" in context:
        context["It"] = context.pop("I_asfid")
        modifications.append("@context: Renamed I_asfid → It")
    
    if "I_revoi" in context:
        context["Im"] = context.pop("I_revoi")
        modifications.append("@context: Renamed I_revoi → Im")
    
    # Update scores in @graph
    if "@graph" in data and len(data["@graph"]) > 0:
        ontology = data["@graph"][0]
        
        # Update ASFID scores
        if "m0:asfidScores" in ontology:
            asfid = ontology["m0:asfidScores"]
            if "I_asfid" in asfid:
                asfid["It"] = asfid.pop("I_asfid")
                modifications.append("m0:asfidScores: Renamed I_asfid → It")
        
        # Update REVOI scores
        if "m0:revoiScores" in ontology:
            revoi = ontology["m0:revoiScores"]
            if "I_revoi" in revoi:
                revoi["Im"] = revoi.pop("I_revoi")
                modifications.append("m0:revoiScores: Renamed I_revoi → Im")
    
    # Summary
    print("="*70)
    print("MODIFICATIONS")
    print("="*70)
    
    if modifications:
        for mod in modifications:
            print(f"  ✓ {mod}")
        
        # Write back
        print(f"\n💾 Writing changes...")
        with open(FIRE_TRIANGLE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        
        print("✅ Migration complete!")
        print("\n" + "="*70)
        print("Next step: Validate with SHACL")
        print("="*70)
        print("cd E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\ontology")
        print("pyshacl -s TSCG_Grammar\\M0_Instances_Schema.shacl.ttl -df json-ld ..\\instances\\poclets\\FireTriangle\\M0_FireTriangle.jsonld")
        return 0
    else:
        print("  ℹ Already using It/Im - no changes needed")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
