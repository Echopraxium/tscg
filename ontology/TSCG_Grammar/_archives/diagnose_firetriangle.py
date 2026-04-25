#!/usr/bin/env python3
"""
Diagnostic Script - Show JSON-LD Structure
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18
"""

import json
from pathlib import Path

FIRE_TRIANGLE_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle.jsonld")

def show_structure(obj, indent=0, max_depth=10):
    """Display JSON structure with types."""
    prefix = "  " * indent
    
    if indent > max_depth:
        print(f"{prefix}... (max depth)")
        return
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (int, float)):
                print(f"{prefix}{key}: {value} (numeric)")
            elif isinstance(value, str):
                if len(value) > 50:
                    print(f"{prefix}{key}: \"{value[:50]}...\" (string)")
                else:
                    print(f"{prefix}{key}: \"{value}\" (string)")
            elif isinstance(value, dict):
                # Check if it's a typed value
                if "@value" in value and "@type" in value:
                    print(f"{prefix}{key}: TYPED {{ @value: {value['@value']}, @type: {value['@type']} }}")
                elif "@id" in value:
                    print(f"{prefix}{key}: REFERENCE {{ @id: {value['@id']} }}")
                else:
                    print(f"{prefix}{key}: OBJECT {{")
                    show_structure(value, indent + 1, max_depth)
                    print(f"{prefix}}}")
            elif isinstance(value, list):
                print(f"{prefix}{key}: ARRAY [")
                for i, item in enumerate(value[:3]):  # Show first 3 items
                    print(f"{prefix}  [{i}]:")
                    show_structure(item, indent + 2, max_depth)
                if len(value) > 3:
                    print(f"{prefix}  ... and {len(value) - 3} more items")
                print(f"{prefix}]")
            else:
                print(f"{prefix}{key}: {type(value).__name__}")
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            print(f"{prefix}[{i}]:")
            show_structure(item, indent + 1, max_depth)
    
    else:
        print(f"{prefix}{obj} ({type(obj).__name__})")

def main():
    """Main entry point."""
    print("="*70)
    print("M0_FireTriangle.jsonld - Structure Diagnostic")
    print("="*70)
    
    if not FIRE_TRIANGLE_PATH.exists():
        print(f"❌ Error: File not found at {FIRE_TRIANGLE_PATH}")
        return 1
    
    print(f"📂 Reading: {FIRE_TRIANGLE_PATH}\n")
    
    with open(FIRE_TRIANGLE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Top-level keys:")
    print("-" * 70)
    for key in data.keys():
        print(f"  • {key}")
    
    print("\n" + "="*70)
    print("Searching for score properties...")
    print("="*70)
    
    # Look for specific score properties
    score_props = [
        "m0:epistemicGap",
        "m0:asfidScores",
        "m0:revoiScores"
    ]
    
    for prop in score_props:
        if prop in data:
            print(f"\n✓ Found: {prop}")
            print("-" * 70)
            show_structure({prop: data[prop]}, indent=0, max_depth=3)
        else:
            print(f"\n✗ Not found: {prop}")
    
    print("\n" + "="*70)
    print("Full structure (first 2 levels):")
    print("="*70)
    show_structure(data, max_depth=2)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
