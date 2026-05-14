#!/usr/bin/env python3
"""
RDFS Reasoning & Diagnostic for TSCG Ontologies
Validates RDF/RDFS structure and generates actionable error reports
"""

import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
    from rdflib.namespace import XSD
except ImportError:
    print("❌ Error: rdflib not installed")
    print("Install with: pip install rdflib")
    sys.exit(1)

# Parse arguments
parser = argparse.ArgumentParser(
    description='RDFS diagnostic validation for TSCG ontologies'
)
parser.add_argument('--file', default='ontology/M2_GenericConcepts.jsonld',
                   help='Path to ontology file (default: M2_GenericConcepts.jsonld)')
args = parser.parse_args()

print("=" * 70)
print("TSCG RDFS REASONING & DIAGNOSTIC")
print("=" * 70)

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
    sys.exit(1)

# Use file from argument or default to M2
ONTOLOGY_PATH = Path(args.file)

try:
    # 1. Load ontology
    print(f"\n📂 Loading: {ONTOLOGY_PATH}")
    if not Path(ONTOLOGY_PATH).exists():
        print(f"❌ File not found!")
        sys.exit(1)
    
    print(f"✅ File found")
    
    print(f"\n📥 Parsing JSON-LD with rdflib...")
    g = Graph()
    g.parse(ONTOLOGY_PATH, format='json-ld')
    
    print(f"✅ Parsed successfully")
    print(f"   Triples: {len(g)}")
    
    # 2. Statistics
    print(f"\n📊 Ontology Statistics:")
    
    classes = set(g.subjects(RDF.type, OWL.Class))
    properties = set(g.subjects(RDF.type, OWL.ObjectProperty)) | \
                 set(g.subjects(RDF.type, OWL.DatatypeProperty))
    
    print(f"   Classes: {len(classes)}")
    print(f"   Properties: {len(properties)}")
    
    # 3. RDFS Validation
    print(f"\n🔍 RDFS Validation:")
    print(f"   Checking domain/range consistency...")
    
    errors = []
    warnings = []
    
    # Check 1: Properties with literal in domain/range
    print(f"\n   [Check 1] Domain/Range types...")
    
    for prop in properties:
        # Check domain
        for domain in g.objects(prop, RDFS.domain):
            if isinstance(domain, Literal):
                errors.append({
                    'type': 'DOMAIN_LITERAL',
                    'property': str(prop),
                    'domain': str(domain),
                    'fix': f'Change domain from literal "{domain}" to URI reference'
                })
        
        # Check range
        for range_val in g.objects(prop, RDFS.range):
            if isinstance(range_val, Literal):
                errors.append({
                    'type': 'RANGE_LITERAL',
                    'property': str(prop),
                    'range': str(range_val),
                    'fix': f'Change range from literal "{range_val}" to URI reference'
                })
    
    # Check 2: Classes with literal in subClassOf
    print(f"   [Check 2] SubClassOf relations...")
    
    for cls in classes:
        for parent in g.objects(cls, RDFS.subClassOf):
            if isinstance(parent, Literal):
                errors.append({
                    'type': 'SUBCLASS_LITERAL',
                    'class': str(cls),
                    'parent': str(parent),
                    'fix': f'Change subClassOf from literal "{parent}" to URI reference'
                })
    
    # Check 3: Functional properties with wrong type
    print(f"   [Check 3] Functional property declarations...")
    
    # Look for @owl:functionalProperty annotations (wrong)
    functional_wrong = []
    for s, p, o in g:
        if 'functionalProperty' in str(p):
            functional_wrong.append(str(s))
    
    for prop_uri in functional_wrong:
        warnings.append({
            'type': 'FUNCTIONAL_WRONG_SYNTAX',
            'property': prop_uri,
            'current': '@owl:functionalProperty "true"',
            'fix': 'Use rdf:type owl:FunctionalProperty instead'
        })
    
    # Check 4: Inverse properties with literals
    print(f"   [Check 4] Inverse property declarations...")
    
    for s in g.subjects(OWL.inverseOf, None):
        for inv in g.objects(s, OWL.inverseOf):
            if isinstance(inv, Literal):
                errors.append({
                    'type': 'INVERSE_LITERAL',
                    'property': str(s),
                    'inverse': str(inv),
                    'fix': f'Change inverseOf from literal "{inv}" to URI reference'
                })
    
    # Check 5: Undefined classes referenced
    print(f"   [Check 5] Undefined class references...")
    
    referenced_classes = set()
    
    # Collect all class references from domain/range
    for prop in properties:
        for domain in g.objects(prop, RDFS.domain):
            if isinstance(domain, URIRef):
                referenced_classes.add(domain)
        for range_val in g.objects(prop, RDFS.range):
            if isinstance(range_val, URIRef) and not str(range_val).startswith(str(XSD)):
                referenced_classes.add(range_val)
    
    # Collect from subClassOf
    for cls in classes:
        for parent in g.objects(cls, RDFS.subClassOf):
            if isinstance(parent, URIRef):
                referenced_classes.add(parent)
    
    # Filter to M2 namespace and check if defined
    m2_namespace = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#"
    
    undefined_classes = set()
    for ref_cls in referenced_classes:
        if str(ref_cls).startswith(m2_namespace):
            # Check if defined as a class
            if ref_cls not in classes and ref_cls != OWL.Thing:
                undefined_classes.add(str(ref_cls))
    
    for undef in undefined_classes:
        warnings.append({
            'type': 'UNDEFINED_CLASS',
            'class': undef,
            'fix': 'Define this class or check if it should reference an existing class'
        })
    
    # 4. Generate Report
    print(f"\n" + "=" * 70)
    print(f"DIAGNOSTIC REPORT")
    print(f"=" * 70)
    
    print(f"\n📈 Summary:")
    print(f"   Triples: {len(g)}")
    print(f"   Classes: {len(classes)}")
    print(f"   Properties: {len(properties)}")
    print(f"   Errors: {len(errors)}")
    print(f"   Warnings: {len(warnings)}")
    
    # Group errors by type
    errors_by_type = defaultdict(list)
    for err in errors:
        errors_by_type[err['type']].append(err)
    
    warnings_by_type = defaultdict(list)
    for warn in warnings:
        warnings_by_type[warn['type']].append(warn)
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)} total):")
        print(f"=" * 70)
        
        for err_type, err_list in errors_by_type.items():
            print(f"\n  {err_type}: {len(err_list)} occurrences")
            print(f"  {'-' * 66}")
            
            # Show first 5 examples
            for err in err_list[:5]:
                if err_type == 'SUBCLASS_LITERAL':
                    print(f"    • Class: .../{err['class'].split('#')[-1]}")
                    print(f"      Parent literal: {err['parent']}")
                    print(f"      Fix: {err['fix']}")
                
                elif err_type == 'DOMAIN_LITERAL':
                    print(f"    • Property: .../{err['property'].split('#')[-1]}")
                    print(f"      Domain literal: {err['domain']}")
                    print(f"      Fix: {err['fix']}")
                
                elif err_type == 'RANGE_LITERAL':
                    print(f"    • Property: .../{err['property'].split('#')[-1]}")
                    print(f"      Range literal: {err['range']}")
                    print(f"      Fix: {err['fix']}")
                
                elif err_type == 'INVERSE_LITERAL':
                    print(f"    • Property: .../{err['property'].split('#')[-1]}")
                    print(f"      Inverse literal: {err['inverse']}")
                    print(f"      Fix: {err['fix']}")
                
                print()
            
            if len(err_list) > 5:
                print(f"    ... and {len(err_list) - 5} more")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)} total):")
        print(f"=" * 70)
        
        for warn_type, warn_list in warnings_by_type.items():
            print(f"\n  {warn_type}: {len(warn_list)} occurrences")
            print(f"  {'-' * 66}")
            
            for warn in warn_list[:3]:
                if warn_type == 'FUNCTIONAL_WRONG_SYNTAX':
                    print(f"    • Property: .../{warn['property'].split('#')[-1]}")
                    print(f"      Current: {warn['current']}")
                    print(f"      Fix: {warn['fix']}")
                
                elif warn_type == 'UNDEFINED_CLASS':
                    print(f"    • Class: .../{warn['class'].split('#')[-1]}")
                    print(f"      Fix: {warn['fix']}")
                
                print()
            
            if len(warn_list) > 3:
                print(f"    ... and {len(warn_list) - 3} more")
    
    # 5. Actionable recommendations
    print(f"\n" + "=" * 70)
    print(f"ACTIONABLE RECOMMENDATIONS")
    print(f"=" * 70)
    
    if errors:
        print(f"\n🔧 Priority 1: Fix ERRORS ({len(errors)} total)")
        print(f"\nThese prevent proper OWL reasoning:")
        
        if 'SUBCLASS_LITERAL' in errors_by_type:
            count = len(errors_by_type['SUBCLASS_LITERAL'])
            print(f"\n  1. Fix {count} rdfs:subClassOf with literal values")
            print(f"     Pattern to replace:")
            print(f'     "rdfs:subClassOf": "m2:GenericConcept"')
            print(f"     →")
            print(f'     "rdfs:subClassOf": {{"@id": "m2:GenericConcept"}}')
        
        if 'INVERSE_LITERAL' in errors_by_type:
            count = len(errors_by_type['INVERSE_LITERAL'])
            print(f"\n  2. Fix {count} owl:inverseOf with literal values")
            print(f"     Same pattern as above")
        
        if 'DOMAIN_LITERAL' in errors_by_type or 'RANGE_LITERAL' in errors_by_type:
            count = len(errors_by_type.get('DOMAIN_LITERAL', [])) + \
                    len(errors_by_type.get('RANGE_LITERAL', []))
            print(f"\n  3. Fix {count} domain/range with literal values")
    
    if warnings:
        print(f"\n⚠️  Priority 2: Fix WARNINGS ({len(warnings)} total)")
        
        if 'FUNCTIONAL_WRONG_SYNTAX' in warnings_by_type:
            count = len(warnings_by_type['FUNCTIONAL_WRONG_SYNTAX'])
            print(f"\n  1. Fix {count} functional property declarations")
            print(f"     Remove: @owl:functionalProperty \"true\"")
            print(f"     Add: \"@type\": [\"owl:DatatypeProperty\", \"owl:FunctionalProperty\"]")
    
    # 6. Next steps
    print(f"\n" + "=" * 70)
    print(f"NEXT STEPS")
    print(f"=" * 70)
    
    print(f"""
1. 📝 Save this report for reference
2. 🔧 Create automated fix script for literal → URI conversions
3. ✅ Test fixes incrementally (fix 10 → validate → repeat)
4. 🎯 Once RDFS clean, enable OWL Pellet reasoning
5. 🚀 Integrate into CI/CD pipeline

Estimated fix time: 2-3 hours with automated script
    """)
    
    # 7. Exit code
    if errors:
        print(f"❌ VALIDATION FAILED: {len(errors)} errors found")
        sys.exit(1)
    elif warnings:
        print(f"⚠️  VALIDATION PASSED WITH WARNINGS: {len(warnings)} warnings")
        sys.exit(0)
    else:
        print(f"✅ VALIDATION PASSED: No errors or warnings")
        sys.exit(0)

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
