#!/usr/bin/env python3
"""
Check number of objects in @graph for successfully migrated poclets
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19
"""

import json
from pathlib import Path

# List of successfully migrated poclets (18 from MIGRATION_REPORT.md)
SUCCESSFUL_POCLETS = [
    "AdaptativeImmuneResponse",
    "ColorSynthesis",
    "ComplexChemicalSynapse",
    "CounterPoint",
    "ExposureTriangle",
    "FireTriangle",
    "FourStrokeEngine",
    "Kidneys",
    "KindlebergerMinsky",
    "MtgColorWheel",
    "NuclearReactorsTypology",
    "PlateTectonics",
    "Raas",
    "Tpack",
    "Transistor",
    "TrophicPyramid",
    "TvTestPattern",
    "Vco"
]

def count_graph_objects(jsonld_path):
    """Count number of objects in @graph array"""
    try:
        with open(jsonld_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if '@graph' in data:
            return len(data['@graph'])
        else:
            # No @graph means single implicit object
            return 1
    except Exception as e:
        return f"ERROR: {e}"

def main():
    base_path = Path(r"E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\poclets")
    
    results = []
    multiple_graph_poclets = []
    
    print("=" * 70)
    print("GRAPH OBJECTS COUNT - SUCCESSFULLY MIGRATED POCLETS")
    print("=" * 70)
    print()
    
    for poclet in SUCCESSFUL_POCLETS:
        poclet_dir = base_path / poclet
        jsonld_file = poclet_dir / f"M0_{poclet}.jsonld"
        
        if not jsonld_file.exists():
            count = "FILE NOT FOUND"
        else:
            count = count_graph_objects(jsonld_file)
        
        results.append((poclet, count))
        
        # Track poclets with multiple objects
        if isinstance(count, int) and count > 1:
            multiple_graph_poclets.append((poclet, count))
        
        status = "✅" if count == 1 else "⚠️" if isinstance(count, int) and count > 1 else "❌"
        print(f"{status} {poclet:30s} : {count} object(s)")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total poclets checked: {len(SUCCESSFUL_POCLETS)}")
    print(f"Single @graph object (✅): {sum(1 for _, c in results if c == 1)}")
    print(f"Multiple @graph objects (⚠️): {len(multiple_graph_poclets)}")
    print(f"Errors (❌): {sum(1 for _, c in results if isinstance(c, str))}")
    print()
    
    if multiple_graph_poclets:
        print("=" * 70)
        print("⚠️  POCLETS WITH MULTIPLE @graph OBJECTS")
        print("=" * 70)
        for poclet, count in multiple_graph_poclets:
            print(f"  - {poclet}: {count} objects")
        print()
        print("🚨 RISK ASSESSMENT:")
        risk_pct = (len(multiple_graph_poclets) / len(SUCCESSFUL_POCLETS)) * 100
        if risk_pct < 10:
            print(f"   ✅ LOW RISK ({risk_pct:.0f}%) - Safe to activate SHACL v1.2 constraint")
        elif risk_pct < 30:
            print(f"   ⚠️  MODERATE RISK ({risk_pct:.0f}%) - Consider fixing before activating")
        else:
            print(f"   🚨 HIGH RISK ({risk_pct:.0f}%) - Revert to SHACL v1.1, fix poclets first")
    else:
        print("✅ ALL POCLETS HAVE SINGLE @graph OBJECT")
        print("   Safe to activate SHACL v1.2 architectural constraint!")
    
    print()

if __name__ == "__main__":
    main()
