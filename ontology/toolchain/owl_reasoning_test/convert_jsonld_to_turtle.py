#!/usr/bin/env python3
"""
JSON-LD to Turtle Converter for TSCG Ontologies
Converts .jsonld files to .ttl format for use in Protégé
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from rdflib import Graph
except ImportError:
    print("❌ Error: rdflib not installed")
    print("Install with: pip install rdflib")
    sys.exit(1)

print("=" * 70)
print("TSCG JSON-LD → TURTLE CONVERTER")
print("=" * 70)

# Parse arguments
parser = argparse.ArgumentParser(
    description='Convert JSON-LD ontology to Turtle format'
)
parser.add_argument('--file', required=True,
                   help='Path to JSON-LD file (e.g., ontology/M2_GenericConcepts.jsonld)')
args = parser.parse_args()

# Auto-detect TSCG repository root
def find_tscg_root():
    """Find TSCG repository root by looking for 'ontology' directory"""
    current = Path.cwd()
    max_depth = 10
    
    for _ in range(max_depth):
        if (current / "ontology").exists() and (current / "ontology").is_dir():
            return current
        if current == current.parent:
            return None
        current = current.parent
    return None

print("\n🔍 Auto-detecting TSCG repository root...")
tscg_root = find_tscg_root()

if tscg_root:
    print(f"✅ Found: {tscg_root}")
    os.chdir(tscg_root)
else:
    print("❌ Could not find TSCG repository root!")
    print("   (Optional - will use current directory)")

# Resolve file paths
input_path = Path(args.file)
print(f"\n📂 Input file: {input_path}")

if not input_path.exists():
    print(f"❌ File not found: {input_path}")
    sys.exit(1)

# Generate output path (same location, .ttl extension)
output_path = input_path.with_suffix('.ttl')
print(f"📄 Output file: {output_path}")

if output_path.exists():
    print(f"⚠️  Output file already exists - will be overwritten")

try:
    # Load JSON-LD
    print(f"\n📥 Loading JSON-LD...")
    g = Graph()
    g.parse(str(input_path), format='json-ld')
    
    print(f"✅ Loaded: {len(g)} triples")
    
    # Convert to Turtle
    print(f"\n🔄 Converting to Turtle...")
    g.serialize(destination=str(output_path), format='turtle')
    
    print(f"✅ Saved: {output_path}")
    
    # Report
    print(f"\n" + "=" * 70)
    print(f"CONVERSION COMPLETE")
    print(f"=" * 70)
    
    print(f"\n📊 Summary:")
    print(f"   Input:  {input_path.name}")
    print(f"   Output: {output_path.name}")
    print(f"   Triples: {len(g)}")
    print(f"   Location: {output_path.parent}")
    
    print(f"\n✅ Ready for Protégé!")
    print(f"   File → Open → {output_path}")
    
    print(f"\n" + "=" * 70 + "\n")

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
