#!/usr/bin/env python3
"""
Diagnostic Script - Show ASFID/REVOI Scores Structure
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18
"""

import json
from pathlib import Path

FIRE_TRIANGLE_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle.jsonld")

def show_value_detail(value, indent=0):
    """Show detailed value information."""
    prefix = "  " * indent
    
    if isinstance(value, dict):
        if "@value" in value and "@type" in value:
            print(f"{prefix}TYPED: @value={value['@value']}, @type={value['@type']}")
        elif "@id" in value:
            print(f"{prefix}REFERENCE: @id={value['@id']}")
        else:
            print(f"{prefix}OBJECT:")
            for k, v in value.items():
                print(f"{prefix}  {k}:")
                show_value_detail(v, indent + 2)
    elif isinstance(value, (int, float)):
        print(f"{prefix}NUMERIC: {value} (type: {type(value).__name__})")
    elif isinstance(value, str):
        print(f"{prefix}STRING: {value}")
    elif isinstance(value, list):
        print(f"{prefix}ARRAY ({len(value)} items):")
        for i, item in enumerate(value[:3]):
            print(f"{prefix}  [{i}]:")
            show_value_detail(item, indent + 2)
    else:
        print(f"{prefix}{type(value).__name__}: {value}")

def main():
    """Main entry point."""
    print("="*70)
    print("ASFID/REVOI Scores Diagnostic")
    print("="*70)
    
    if not FIRE_TRIANGLE_PATH.exists():
        print(f"❌ File not found: {FIRE_TRIANGLE_PATH}")
        return 1
    
    print(f"📂 Reading: {FIRE_TRIANGLE_PATH}\n")
    
    with open(FIRE_TRIANGLE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Navigate to the ontology in @graph
    if "@graph" in data and len(data["@graph"]) > 0:
        ontology = data["@graph"][0]
        print("✓ Found ontology in @graph[0]\n")
    else:
        ontology = data
        print("⚠ No @graph structure, using root level\n")
    
    # Check epistemicGap
    print("="*70)
    print("1. m0:epistemicGap")
    print("="*70)
    if "m0:epistemicGap" in ontology:
        show_value_detail(ontology["m0:epistemicGap"])
    else:
        print("✗ Not found")
    
    # Check ASFID scores
    print("\n" + "="*70)
    print("2. m0:asfidScores")
    print("="*70)
    if "m0:asfidScores" in ontology:
        scores = ontology["m0:asfidScores"]
        print(f"Type: {type(scores).__name__}")
        print("\nContents:")
        show_value_detail(scores)
    else:
        print("✗ Not found")
    
    # Check REVOI scores
    print("\n" + "="*70)
    print("3. m0:revoiScores")
    print("="*70)
    if "m0:revoiScores" in ontology:
        scores = ontology["m0:revoiScores"]
        print(f"Type: {type(scores).__name__}")
        print("\nContents:")
        show_value_detail(scores)
    else:
        print("✗ Not found")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if "m0:asfidScores" in ontology:
        asfid = ontology["m0:asfidScores"]
        print("\nASFID Properties:")
        for key in ["eagle_eye:Attractor", "eagle_eye:Structure", "eagle_eye:Flow", 
                    "eagle_eye:Information", "eagle_eye:Dynamics", "m0:mean"]:
            if key in asfid:
                val = asfid[key]
                if isinstance(val, dict) and "@type" in val:
                    print(f"  ✓ {key}: {val['@type']}")
                elif isinstance(val, (int, float)):
                    print(f"  ✗ {key}: NUMERIC (not typed) = {val}")
                else:
                    print(f"  ? {key}: {type(val).__name__}")
    
    if "m0:revoiScores" in ontology:
        revoi = ontology["m0:revoiScores"]
        print("\nREVOI Properties:")
        for key in ["sphinx_eye:Representable", "sphinx_eye:Evolvable", "sphinx_eye:Verifiable",
                    "sphinx_eye:Observable", "sphinx_eye:Interoperable", "m0:mean"]:
            if key in revoi:
                val = revoi[key]
                if isinstance(val, dict) and "@type" in val:
                    print(f"  ✓ {key}: {val['@type']}")
                elif isinstance(val, (int, float)):
                    print(f"  ✗ {key}: NUMERIC (not typed) = {val}")
                else:
                    print(f"  ? {key}: {type(val).__name__}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
