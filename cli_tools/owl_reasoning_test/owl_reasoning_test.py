#!/usr/bin/env python3
"""
Quick OWL Reasoning Test for TSCG Ontologies
Test Owlready2 + Pellet reasoner on TSCG ontologies
"""

import os
import sys
import argparse
from owlready2 import *
from pathlib import Path

# Parse arguments
parser = argparse.ArgumentParser(
    description='OWL reasoning validation for TSCG ontologies'
)
parser.add_argument('--file', default='ontology/M2_GenericConcepts.jsonld',
                   help='Path to ontology file (default: M2_GenericConcepts.jsonld)')
args = parser.parse_args()

print("=" * 70)
print("TSCG OWL REASONING - QUICK TEST")
print("=" * 70)

# Auto-detect TSCG repository root
def find_tscg_root():
    """Find TSCG repository root by looking for 'ontology' directory"""
    current = Path.cwd()
    max_depth = 10  # Safety limit
    
    for _ in range(max_depth):
        if (current / "ontology").exists() and (current / "ontology").is_dir():
            return current
        
        # Reached filesystem root
        if current == current.parent:
            return None
        
        current = current.parent
    
    return None

# Find and change to TSCG root
print("\n🔍 Auto-detecting TSCG repository root...")
tscg_root = find_tscg_root()

if tscg_root:
    print(f"✅ Found: {tscg_root}")
    os.chdir(tscg_root)
else:
    print("❌ Could not find TSCG repository root!")
    print("   Looking for 'ontology/' directory")
    print(f"   Started from: {Path.cwd()}")
    print("\n   Make sure you're inside the TSCG repository")
    sys.exit(1)

# Use file from argument or default to M2
ONTOLOGY_PATH = args.file

try:
    # 1. Check file exists
    print(f"\n📂 Looking for: {ONTOLOGY_PATH}")
    if not Path(ONTOLOGY_PATH).exists():
        print(f"❌ File not found!")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Make sure you're in the TSCG repository root")
        exit(1)
    
    print(f"✅ File found")
    
    # 2. Load ontology (convert JSON-LD to RDF/XML first)
    print(f"\n📥 Loading ontology...")
    print(f"   Converting JSON-LD to RDF/XML (Owlready2 requirement)...")
    
    # Convert JSON-LD to RDF/XML using rdflib
    try:
        from rdflib import Graph as RDFGraph
        
        # Load JSON-LD with rdflib
        temp_graph = RDFGraph()
        temp_graph.parse(ONTOLOGY_PATH, format='json-ld')
        
        # Save as temporary RDF/XML file
        temp_rdf = Path("temp_ontology.rdf")
        temp_graph.serialize(destination=str(temp_rdf), format='xml')
        
        print(f"   ✅ Converted to RDF/XML")
        
        # Now load with Owlready2
        onto = get_ontology(f"file://{temp_rdf.absolute()}").load()
        
        # Clean up temp file
        temp_rdf.unlink()
        
    except ImportError:
        print(f"❌ rdflib not installed!")
        print(f"   Install with: pip install rdflib")
        exit(1)
    
    print(f"✅ Loaded: {onto.name}")
    
    # 3. Count elements
    classes = list(onto.classes())
    properties = list(onto.properties())
    individuals = list(onto.individuals())
    
    print(f"\n📊 Ontology statistics:")
    print(f"   Classes: {len(classes)}")
    print(f"   Properties: {len(properties)}")
    print(f"   Individuals: {len(individuals)}")
    
    # 4. Display sample classes
    print(f"\n🔍 Sample classes (first 5):")
    for cls in classes[:5]:
        print(f"   • {cls.name}")
    
    # 5. Run reasoner
    print(f"\n🧠 Running OWL Reasoner (Pellet)...")
    print(f"   This may take 10-30 seconds...")
    
    with onto:
        sync_reasoner_pellet(infer_property_values=True, debug=1)
    
    print(f"✅ Reasoning completed successfully!")
    
    # 6. Check for inconsistencies
    print(f"\n🔍 Checking logical consistency...")
    inconsistent = list(onto.inconsistent_classes())
    
    if inconsistent:
        print(f"❌ INCONSISTENT CLASSES FOUND: {len(inconsistent)}")
        print(f"\n   Inconsistent classes:")
        for cls in inconsistent:
            print(f"   • {cls.name}")
        print(f"\n⚠️  Your ontology has logical inconsistencies!")
        print(f"   This needs to be fixed before production use.")
    else:
        print(f"✅ NO INCONSISTENCIES FOUND")
        print(f"   Ontology is logically consistent!")
    
    # 7. Summary
    print(f"\n" + "=" * 70)
    print(f"TEST SUMMARY")
    print(f"=" * 70)
    print(f"File: {ONTOLOGY_PATH}")
    print(f"Classes: {len(classes)}")
    print(f"Properties: {len(properties)}")
    print(f"Reasoner: Pellet (via Owlready2)")
    print(f"Status: {'✅ PASSED' if not inconsistent else '❌ FAILED'}")
    print(f"=" * 70)
    
    if not inconsistent:
        print(f"\n🎉 SUCCESS! Your ontology passed OWL reasoning validation!")
    else:
        print(f"\n⚠️  ATTENTION: Fix inconsistencies before proceeding.")
        exit(1)

except FileNotFoundError as e:
    print(f"\n❌ ERROR: File not found")
    print(f"   {e}")
    print(f"\n   Make sure you're running from TSCG repository root:")
    print(f"   cd /path/to/tscg")
    print(f"   python test_owl_reasoning.py")
    exit(1)

except Exception as e:
    print(f"\n❌ ERROR during reasoning:")
    print(f"   {type(e).__name__}: {e}")
    print(f"\n   Common issues:")
    print(f"   1. Java not installed: run 'java -version'")
    print(f"   2. JAVA_HOME not set: check environment variables")
    print(f"   3. Owlready2 not installed: pip install owlready2")
    print(f"\n   See TSCG_Prerequisites_Installation.md for setup guide")
    exit(1)
