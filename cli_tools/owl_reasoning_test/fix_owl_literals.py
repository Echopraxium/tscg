#!/usr/bin/env python3
"""
Automatic OWL Literal → URI Reference Fixer for TSCG Ontologies
Fixes the 172 errors detected by rdfs_diagnostic.py
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import shutil

print("=" * 70)
print("TSCG OWL LITERAL → URI FIXER")
print("=" * 70)

# Parse arguments
parser = argparse.ArgumentParser(
    description='Fix OWL literal values to URI references in TSCG ontologies'
)
parser.add_argument('--dry-run', action='store_true',
                   help='Show what would be changed without modifying files')
parser.add_argument('--file', default='ontology/M2_GenericConcepts.jsonld',
                   help='Path to ontology file (default: M2_GenericConcepts.jsonld)')
parser.add_argument('--no-backup', action='store_true',
                   help='Skip creating backup file')

args = parser.parse_args()

# Auto-detect TSCG root
def find_tscg_root():
    current = Path.cwd()
    for _ in range(10):
        if (current / "ontology").exists():
            return current
        if current == current.parent:
            return None
        current = current.parent
    return None

print("\n🔍 Auto-detecting TSCG repository root...")
tscg_root = find_tscg_root()

if tscg_root:
    print(f"✅ Found: {tscg_root}")
    import os
    os.chdir(tscg_root)
else:
    print("❌ Could not find TSCG repository root!")
    sys.exit(1)

ONTOLOGY_PATH = Path(args.file)

if not ONTOLOGY_PATH.exists():
    print(f"❌ File not found: {ONTOLOGY_PATH}")
    sys.exit(1)

print(f"\n📂 Target file: {ONTOLOGY_PATH}")

if args.dry_run:
    print(f"🔍 DRY-RUN MODE: No files will be modified")
else:
    print(f"⚠️  LIVE MODE: File will be modified")

# Load ontology
print(f"\n📥 Loading ontology...")
with open(ONTOLOGY_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✅ Loaded: {len(data.get('@graph', []))} items in @graph")

# Statistics
corrections = {
    'subClassOf': 0,
    'domain': 0,
    'range': 0,
    'inverseOf': 0,
    'functionalProperty': 0
}

changes_preview = []

def fix_literal_to_uri(obj, parent_key='', path=''):
    """Recursively fix literal strings that should be URI references"""
    
    if isinstance(obj, dict):
        fixed = {}
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            
            # Fix rdfs:subClassOf, rdfs:domain, rdfs:range, owl:inverseOf
            if key in ['rdfs:subClassOf', 'rdfs:domain', 'rdfs:range', 'owl:inverseOf']:
                if isinstance(value, str):
                    # Convert string to URI reference
                    corrections[key.split(':')[1]] += 1
                    fixed[key] = {"@id": value}
                    
                    changes_preview.append({
                        'path': new_path,
                        'property': key,
                        'old': f'"{value}"',
                        'new': f'{{"@id": "{value}"}}'
                    })
                elif isinstance(value, list):
                    # Handle list of values
                    fixed_list = []
                    for item in value:
                        if isinstance(item, str):
                            corrections[key.split(':')[1]] += 1
                            fixed_list.append({"@id": item})
                            
                            changes_preview.append({
                                'path': new_path,
                                'property': key,
                                'old': f'"{item}"',
                                'new': f'{{"@id": "{item}"}}'
                            })
                        else:
                            fixed_list.append(fix_literal_to_uri(item, key, new_path))
                    fixed[key] = fixed_list
                else:
                    fixed[key] = fix_literal_to_uri(value, key, new_path)
            
            # Remove @owl:functionalProperty annotations (wrong syntax)
            elif '@owl:functionalProperty' in key or 'owl:functionalProperty' in key:
                corrections['functionalProperty'] += 1
                changes_preview.append({
                    'path': new_path,
                    'property': key,
                    'old': f'{key}: "{value}"',
                    'new': 'REMOVED (use rdf:type owl:FunctionalProperty instead)'
                })
                # Don't add to fixed dict (removed)
                continue
            
            else:
                fixed[key] = fix_literal_to_uri(value, key, new_path)
        
        return fixed
    
    elif isinstance(obj, list):
        return [fix_literal_to_uri(item, parent_key, f"{path}[{i}]") 
                for i, item in enumerate(obj)]
    
    else:
        return obj

# Apply fixes
print(f"\n🔧 Analyzing and fixing...")
fixed_data = fix_literal_to_uri(data)

# Report
print(f"\n" + "=" * 70)
print(f"CORRECTION REPORT")
print(f"=" * 70)

print(f"\n📊 Corrections found:")
total_corrections = sum(corrections.values())
print(f"   Total: {total_corrections}")
print(f"   - rdfs:subClassOf:        {corrections['subClassOf']}")
print(f"   - rdfs:domain:            {corrections['domain']}")
print(f"   - rdfs:range:             {corrections['range']}")
print(f"   - owl:inverseOf:          {corrections['inverseOf']}")
print(f"   - @owl:functionalProperty: {corrections['functionalProperty']} (removed)")

if args.dry_run:
    print(f"\n🔍 DRY-RUN: Showing first 10 changes that WOULD be applied:")
    print(f"=" * 70)
    
    for i, change in enumerate(changes_preview[:10]):
        print(f"\n  Change #{i+1}:")
        print(f"    Location: {change['path'][:60]}...")
        print(f"    Property: {change['property']}")
        print(f"    Old: {change['old'][:50]}...")
        print(f"    New: {change['new'][:50]}...")
    
    if len(changes_preview) > 10:
        print(f"\n  ... and {len(changes_preview) - 10} more changes")
    
    print(f"\n" + "=" * 70)
    print(f"🔍 DRY-RUN SUMMARY")
    print(f"=" * 70)
    print(f"   File: {ONTOLOGY_PATH}")
    print(f"   Total corrections: {total_corrections}")
    print(f"   Status: NOT MODIFIED (dry-run mode)")
    print(f"\n   To apply changes, run without --dry-run:")
    print(f"   python {Path(__file__).name} --file {ONTOLOGY_PATH}")

else:
    # Create backup
    if not args.no_backup:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = ONTOLOGY_PATH.with_suffix(f'.backup_{timestamp}.jsonld')
        
        print(f"\n💾 Creating backup...")
        shutil.copy2(ONTOLOGY_PATH, backup_path)
        print(f"✅ Backup: {backup_path}")
    
    # Save fixed file
    print(f"\n💾 Saving corrected ontology...")
    with open(ONTOLOGY_PATH, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved: {ONTOLOGY_PATH}")
    
    # Validate JSON
    print(f"\n🔍 Validating JSON syntax...")
    try:
        with open(ONTOLOGY_PATH, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ JSON valid")
    except json.JSONDecodeError as e:
        print(f"❌ JSON validation failed: {e}")
        print(f"   Restoring from backup...")
        if not args.no_backup:
            shutil.copy2(backup_path, ONTOLOGY_PATH)
            print(f"✅ Restored from backup")
        sys.exit(1)
    
    print(f"\n" + "=" * 70)
    print(f"✅ CORRECTIONS APPLIED")
    print(f"=" * 70)
    print(f"   File: {ONTOLOGY_PATH}")
    print(f"   Total corrections: {total_corrections}")
    print(f"   Backup: {backup_path if not args.no_backup else 'None (--no-backup)'}")
    
    # Suggest next step
    print(f"\n" + "=" * 70)
    print(f"NEXT STEP: RE-VALIDATE")
    print(f"=" * 70)
    print(f"\n   Run RDFS diagnostic to verify fixes:")
    print(f"   python cli-tools/owl_reasoning_test/rdfs_diagnostic.py")
    print(f"\n   Expected result: 0 errors (from 172)")

print(f"\n{'=' * 70}\n")
