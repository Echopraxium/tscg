#!/usr/bin/env python3
"""
TSCG Poclet Namespace Fixer
Automatically fixes namespaces in M0 poclet ontology files

Author: Echopraxium with the collaboration of Claude AI
Date: 2026-01-22
Version: 1.0
"""

import os
import re
import sys
from pathlib import Path

def get_poclet_folder_name(file_path):
    """Extract poclet folder name from file path"""
    # Example: /path/to/poclets/color_synthesis/M0_RGB.jsonld → color_synthesis
    parts = Path(file_path).parts
    for i, part in enumerate(parts):
        if part == 'poclets' and i + 1 < len(parts):
            return parts[i + 1]
    return None

def fix_m0_poclet(input_file, output_file=None, folder_name=None):
    """
    Fix M0 poclet namespace
    
    Args:
        input_file: Path to input .jsonld file
        output_file: Path to output file (if None, will use input_file name in current dir)
        folder_name: Poclet folder name (if None, will auto-detect)
    """
    if output_file is None:
        output_file = os.path.basename(input_file)
    
    if folder_name is None:
        folder_name = get_poclet_folder_name(input_file)
        if folder_name is None:
            print(f"❌ Could not determine folder name for {input_file}")
            return False
    
    namespace = f"m0:{folder_name}"
    
    print(f"📄 Processing: {input_file}")
    print(f"   Folder: {folder_name}")
    print(f"   Namespace: {namespace}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix @context - replace generic m0: with specific namespace
    old_m0_pattern = r'"m0": "https://github\.com/Echopraxium/tscg/blob/main/ontology/poclets/[^"]+/M0_[^"]+\.jsonld#"'
    new_m0 = f'"{namespace}": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/{folder_name}/M0_{Path(input_file).stem.replace("M0_", "")}.jsonld#"'
    content = re.sub(old_m0_pattern, new_m0, content)
    
    # Also handle if it was already using raw.githubusercontent
    old_m0_pattern2 = r'"m0": "https://raw\.githubusercontent\.com/Echopraxium/tscg/main/ontology/poclets/[^"]+/M0_[^"]+\.jsonld#"'
    content = re.sub(old_m0_pattern2, new_m0, content)
    
    # 2. Add m1:core reference if not present
    if '"m1:core"' not in content:
        # Find m2 reference and add m1:core before it
        content = re.sub(
            r'("m2": ")',
            r'"m1:core": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",\n    \1',
            content
        )
    
    # 3. Fix github.com → raw.githubusercontent.com
    content = content.replace(
        'https://github.com/Echopraxium/tscg/blob/main/',
        'https://raw.githubusercontent.com/Echopraxium/tscg/main/'
    )
    
    # 4. Fix M3 namespaces
    content = content.replace('"m3eagle":', '"m3:eagle_eye":')
    content = content.replace('"m3sphinx":', '"m3:sphinx_eye":')
    content = re.sub(r'([^"])m3eagle:', r'\1m3:eagle_eye:', content)
    content = re.sub(r'([^"])m3sphinx:', r'\1m3:sphinx_eye:', content)
    
    # 5. Add owl:imports for M1_CoreConcepts if not present
    if '"owl:imports"' not in content:
        # Find a good place to add it (after @type)
        content = re.sub(
            r'("@type": "owl:(?:NamedIndividual|Ontology)",)',
            r'\1\n      "owl:imports": ["https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld"],',
            content,
            count=1
        )
    
    # 6. Fix all m0: references within the document
    # Replace "m0:Something" with "m0:folder_name:Something"
    content = re.sub(r'"@id": "m0:([A-Z])', rf'"@id": "{namespace}:\1', content)
    
    # Fix properties like "m0:property": → "m0:folder_name:property":
    content = re.sub(r'"m0:([a-z][a-zA-Z0-9_]*)":', rf'"{namespace}:\1":', content)
    
    # 7. Fix m1 references to use proper domain namespaces
    # This is domain-specific, so we'll keep generic m1: for now unless we can detect the domain
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed → {output_file}\n")
    return True

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python fix_m0_poclet.py <input_file> [output_file] [folder_name]")
        print("\nExample:")
        print("  python fix_m0_poclet.py /path/to/M0_RGB_Additive.jsonld")
        print("  python fix_m0_poclet.py /path/to/M0_RGB_Additive.jsonld ./M0_RGB_Additive_fixed.jsonld")
        print("  python fix_m0_poclet.py ./M0_TPACK.jsonld ./M0_TPACK_fixed.jsonld tpack")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    folder_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    success = fix_m0_poclet(input_file, output_file, folder_name)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
