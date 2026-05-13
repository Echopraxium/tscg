#!/usr/bin/env python3
"""
TSCG Migration Diagnostic Script
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19
Version: 1.0.0

Analyzes failed migration instances to understand what went wrong.
"""

import json
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
INSTANCES_DIR = REPO_ROOT / "instances/poclets"

# Instances that failed SHACL validation (from migration log)
FAILED_SHACL = [
    "ComplexChemicalSynapse",
    "KindlebergerMinsky",
    "MtgColorWheel",
    "PhaseTransition",
    "PlateTectonics",
    "TrophicPyramid",
    "TvTestPattern",
    "Vco",
    "Yggdrasil"
]

# Instances that succeeded
SUCCEEDED = [
    "CounterPoint",
    "ExposureTriangle",
    "FireTriangle",
    "FourStrokeEngine",
    "Kidneys",
    "Raas",
    "Tpack",
    "Transistor"
]

# ============================================================================
# DIAGNOSTIC FUNCTIONS
# ============================================================================

def diagnose_instance(instance_name):
    """Diagnose a single instance."""
    
    # Find JSON-LD file
    instance_dir = INSTANCES_DIR / instance_name
    jsonld_path = instance_dir / f"M0_{instance_name}.jsonld"
    
    if not jsonld_path.exists():
        return {
            'status': 'file_not_found',
            'path': str(jsonld_path)
        }
    
    # Read JSON-LD
    try:
        with open(jsonld_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {
            'status': 'read_error',
            'error': str(e)
        }
    
    # Analyze properties
    diagnosis = {
        'status': 'analyzed',
        'properties': {}
    }
    
    # Check title/label
    diagnosis['properties']['dcterms:title'] = 'dcterms:title' in data
    diagnosis['properties']['rdfs:label'] = 'rdfs:label' in data
    
    # Check description/comment
    diagnosis['properties']['dcterms:description'] = 'dcterms:description' in data
    diagnosis['properties']['rdfs:comment'] = 'rdfs:comment' in data
    
    # Check ontologyType
    if 'm3:ontologyType' in data:
        diagnosis['properties']['m3:ontologyType'] = data['m3:ontologyType']
    else:
        diagnosis['properties']['m3:ontologyType'] = None
    
    # Check domain
    if 'm1:domain' in data:
        diagnosis['properties']['m1:domain'] = data['m1:domain']
    elif 'm0:domain' in data:
        diagnosis['properties']['m0:domain'] = data['m0:domain']
    else:
        diagnosis['properties']['m1:domain'] = None
        diagnosis['properties']['m0:domain'] = None
    
    # Check @type
    if '@type' in data:
        diagnosis['properties']['@type'] = data['@type']
    
    # Check for old properties
    diagnosis['properties']['m2:ontologyCategory'] = 'm2:ontologyCategory' in data
    diagnosis['properties']['rdf:type'] = 'rdf:type' in data
    diagnosis['properties']['m2:ontologyType'] = 'm2:ontologyType' in data
    
    return diagnosis

def generate_comparison_report(failed_instances, succeeded_instances):
    """Generate comparative analysis report."""
    
    print("="*70)
    print("TSCG MIGRATION DIAGNOSTIC REPORT")
    print("="*70)
    
    # Analyze failed instances
    print("\n" + "="*70)
    print("FAILED INSTANCES (SHACL Validation)")
    print("="*70)
    
    failed_diagnoses = {}
    for instance in failed_instances:
        print(f"\n### {instance}")
        diagnosis = diagnose_instance(instance)
        failed_diagnoses[instance] = diagnosis
        
        if diagnosis['status'] == 'file_not_found':
            print(f"   ❌ FILE NOT FOUND: {diagnosis['path']}")
            continue
        elif diagnosis['status'] == 'read_error':
            print(f"   ❌ READ ERROR: {diagnosis['error']}")
            continue
        
        props = diagnosis['properties']
        
        # Title/Label
        print(f"\n   📝 TITLE/LABEL:")
        print(f"      dcterms:title present: {props['dcterms:title']}")
        print(f"      rdfs:label present:    {props['rdfs:label']}")
        if props['dcterms:title'] and not props['rdfs:label']:
            print(f"      🔴 PROBLEM: title not converted to label")
        elif props['dcterms:title'] and props['rdfs:label']:
            print(f"      ⚠️  PROBLEM: Both present (dcterms:title should be removed)")
        
        # Description/Comment
        print(f"\n   📋 DESCRIPTION/COMMENT:")
        print(f"      dcterms:description present: {props['dcterms:description']}")
        print(f"      rdfs:comment present:        {props['rdfs:comment']}")
        if props['dcterms:description'] and not props['rdfs:comment']:
            print(f"      🔴 PROBLEM: description not converted to comment")
        elif props['dcterms:description'] and props['rdfs:comment']:
            print(f"      ⚠️  PROBLEM: Both present (dcterms:description should be removed)")
        
        # OntologyType
        print(f"\n   🏷️  ONTOLOGY TYPE:")
        if props['m3:ontologyType']:
            print(f"      m3:ontologyType: {props['m3:ontologyType']}")
            # Check if it's an IRI object
            if isinstance(props['m3:ontologyType'], dict):
                if '@id' in props['m3:ontologyType']:
                    value = props['m3:ontologyType']['@id']
                    if value == "m3:Poclet":
                        print(f"      ⚠️  PROBLEM: Short form 'm3:Poclet' - may need full IRI")
                    elif "M3_GenesisSpace.jsonld#m3:Poclet" in value:
                        print(f"      ✅ Format looks correct")
                    else:
                        print(f"      ⚠️  Unknown format")
        else:
            print(f"      ❌ m3:ontologyType: MISSING")
        
        # Domain
        print(f"\n   🌍 DOMAIN:")
        if props.get('m1:domain'):
            print(f"      m1:domain: {props['m1:domain']}")
        elif props.get('m0:domain'):
            print(f"      ⚠️  m0:domain present (should be m1:domain): {props['m0:domain']}")
        else:
            print(f"      ❌ m1:domain: MISSING")
        
        # Old properties
        print(f"\n   🚫 OBSOLETE PROPERTIES:")
        if props['m2:ontologyCategory']:
            print(f"      ⚠️  m2:ontologyCategory still present")
        if props['rdf:type']:
            print(f"      ⚠️  rdf:type still present")
        if props['m2:ontologyType']:
            print(f"      ⚠️  m2:ontologyType still present")
    
    # Analyze succeeded instances
    print("\n\n" + "="*70)
    print("SUCCEEDED INSTANCES (Reference)")
    print("="*70)
    
    succeeded_diagnoses = {}
    for instance in succeeded_instances:
        print(f"\n### {instance}")
        diagnosis = diagnose_instance(instance)
        succeeded_diagnoses[instance] = diagnosis
        
        if diagnosis['status'] != 'analyzed':
            print(f"   ⚠️  Could not analyze")
            continue
        
        props = diagnosis['properties']
        
        print(f"   dcterms:title: {props['dcterms:title']}, rdfs:label: {props['rdfs:label']}")
        print(f"   dcterms:description: {props['dcterms:description']}, rdfs:comment: {props['rdfs:comment']}")
        print(f"   m3:ontologyType: {props.get('m3:ontologyType')}")
        print(f"   m1:domain: {props.get('m1:domain')}")
    
    # Pattern analysis
    print("\n\n" + "="*70)
    print("PATTERN ANALYSIS")
    print("="*70)
    
    print("\n📊 FAILED INSTANCES - Common Patterns:")
    
    # Count patterns in failed instances
    patterns = defaultdict(int)
    for instance, diag in failed_diagnoses.items():
        if diag['status'] != 'analyzed':
            continue
        props = diag['properties']
        
        if props['dcterms:title'] and not props['rdfs:label']:
            patterns['title_not_converted'] += 1
        if props['dcterms:title'] and props['rdfs:label']:
            patterns['both_title_label'] += 1
        if props['dcterms:description'] and not props['rdfs:comment']:
            patterns['description_not_converted'] += 1
        if props['dcterms:description'] and props['rdfs:comment']:
            patterns['both_description_comment'] += 1
        if not props.get('m1:domain') and not props.get('m0:domain'):
            patterns['no_domain'] += 1
        if props.get('m3:ontologyType') and isinstance(props['m3:ontologyType'], dict):
            if props['m3:ontologyType'].get('@id') == 'm3:Poclet':
                patterns['short_ontologyType'] += 1
    
    for pattern, count in sorted(patterns.items(), key=lambda x: -x[1]):
        print(f"   • {pattern}: {count}/{len([d for d in failed_diagnoses.values() if d['status'] == 'analyzed'])}")
    
    print("\n📊 SUCCEEDED INSTANCES - Common Patterns:")
    
    # Check what succeeded instances have
    success_patterns = defaultdict(int)
    for instance, diag in succeeded_diagnoses.items():
        if diag['status'] != 'analyzed':
            continue
        props = diag['properties']
        
        if props['rdfs:label']:
            success_patterns['has_rdfs_label'] += 1
        if props['rdfs:comment']:
            success_patterns['has_rdfs_comment'] += 1
        if props.get('m1:domain'):
            success_patterns['has_m1_domain'] += 1
        if props.get('m3:ontologyType'):
            success_patterns['has_ontologyType'] += 1
            if isinstance(props['m3:ontologyType'], dict):
                if props['m3:ontologyType'].get('@id') == 'm3:Poclet':
                    success_patterns['short_ontologyType'] += 1
    
    for pattern, count in sorted(success_patterns.items(), key=lambda x: -x[1]):
        print(f"   • {pattern}: {count}/{len([d for d in succeeded_diagnoses.values() if d['status'] == 'analyzed'])}")
    
    # Root cause analysis
    print("\n\n" + "="*70)
    print("ROOT CAUSE ANALYSIS")
    print("="*70)
    
    print("\n🔍 Why did transformations fail?")
    
    print("\n1. dcterms:title → rdfs:label:")
    title_not_converted = patterns.get('title_not_converted', 0)
    both_title_label = patterns.get('both_title_label', 0)
    if title_not_converted > 0:
        print(f"   ❌ {title_not_converted} instances: title NOT converted to label")
        print(f"      → Script's fix_title_to_label() did NOT execute correctly")
    if both_title_label > 0:
        print(f"   ⚠️  {both_title_label} instances: Both title AND label present")
        print(f"      → Script added label but did NOT remove title")
    
    print("\n2. dcterms:description → rdfs:comment:")
    desc_not_converted = patterns.get('description_not_converted', 0)
    both_desc_comment = patterns.get('both_description_comment', 0)
    if desc_not_converted > 0:
        print(f"   ❌ {desc_not_converted} instances: description NOT converted to comment")
        print(f"      → Script's fix_description_to_comment() did NOT execute correctly")
    if both_desc_comment > 0:
        print(f"   ⚠️  {both_desc_comment} instances: Both description AND comment present")
        print(f"      → Script added comment but did NOT remove description")
    
    print("\n3. m3:ontologyType format:")
    short_format = patterns.get('short_ontologyType', 0)
    if short_format > 0:
        print(f"   ⚠️  {short_format} instances: Using short form 'm3:Poclet'")
        print(f"      → SHACL may expect full IRI in @id value")
        print(f"      → Needs investigation: Is this actually the problem?")
    
    print("\n4. m1:domain:")
    no_domain = patterns.get('no_domain', 0)
    if no_domain > 0:
        print(f"   ❌ {no_domain} instances: m1:domain completely missing")
        print(f"      → Script does NOT add m1:domain (expected - requires domain knowledge)")
        print(f"      → This is a MANUAL fix required")
    
    # Recommendations
    print("\n\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    print("\n🔧 Script Fixes Needed:")
    
    if title_not_converted > 0 or desc_not_converted > 0:
        print("\n1. ❌ CRITICAL BUG: Conversion functions not working")
        print("   Problem: fix_title_to_label() and fix_description_to_comment()")
        print("   Likely cause: Function logic error or data structure mismatch")
        print("   Fix: Debug these functions - they claim success but don't modify data")
    
    if both_title_label > 0 or both_desc_comment > 0:
        print("\n2. ⚠️  BUG: Incomplete removal of old properties")
        print("   Problem: Old dcterms properties not deleted")
        print("   Fix: Ensure functions DELETE old property after adding new one")
    
    if short_format > 0:
        print("\n3. ⚠️  POSSIBLE ISSUE: m3:ontologyType format")
        print("   Current: {'@id': 'm3:Poclet'}")
        print("   SHACL may expect: Full IRI or different format")
        print("   Action: Check SHACL schema expectations")
    
    if no_domain > 0:
        print("\n4. ℹ️  MANUAL FIX REQUIRED: m1:domain")
        print(f"   {no_domain} instances need m1:domain added manually")
        print("   Script cannot auto-add (requires domain knowledge)")
    
    print("\n\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    
    print("\n1. Review this diagnostic report")
    print("2. Fix identified bugs in migration script")
    print("3. Test fixes on 1-2 failed instances")
    print("4. Re-run migration on remaining instances")
    print("5. Manually add m1:domain to all instances")

def main():
    """Main execution."""
    generate_comparison_report(FAILED_SHACL, SUCCEEDED)

if __name__ == "__main__":
    main()
