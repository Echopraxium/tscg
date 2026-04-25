#!/usr/bin/env python3
"""
Fix XSD Float Typing in TSCG JSON-LD Files
===========================================
Adds explicit "@type": "xsd:float" declarations in @context
to ensure scores are typed as xsd:float instead of xsd:double.

Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

# Properties that need xsd:float typing
FLOAT_PROPERTIES = {
    # M0 level properties
    "m0:epistemicGap",
    "m0:mean",
    
    # ASFID dimensions (M3 EagleEye)
    "eagle_eye:Attractor",
    "eagle_eye:Structure", 
    "eagle_eye:Flow",
    "eagle_eye:Information",
    "eagle_eye:Dynamics",
    
    # REVOI dimensions (M3 SphinxEye)
    "sphinx_eye:Representable",
    "sphinx_eye:Evolvable",
    "sphinx_eye:Verifiable",
    "sphinx_eye:Observable",
    "sphinx_eye:Interoperable"
}

def add_float_typing_to_context(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add explicit xsd:float typing to @context for all score properties.
    
    Args:
        data: Parsed JSON-LD document
        
    Returns:
        Modified JSON-LD document with float typing in @context
    """
    if "@context" not in data:
        print("Warning: No @context found in JSON-LD file", file=sys.stderr)
        return data
    
    context = data["@context"]
    
    # Ensure xsd namespace is declared
    if "xsd" not in context:
        context["xsd"] = "http://www.w3.org/2001/XMLSchema#"
    
    # Add type declarations for all float properties
    modifications_made = []
    
    for prop in FLOAT_PROPERTIES:
        if prop in context:
            # Property exists - check if it needs typing
            if isinstance(context[prop], str):
                # Simple string mapping - convert to typed definition
                context[prop] = {
                    "@id": context[prop],
                    "@type": "xsd:float"
                }
                modifications_made.append(f"Converted {prop} to typed definition")
            elif isinstance(context[prop], dict):
                # Already a dict - add/update @type
                if context[prop].get("@type") != "xsd:float":
                    context[prop]["@type"] = "xsd:float"
                    modifications_made.append(f"Updated @type for {prop}")
        else:
            # Property not in context - add it with typing
            # Extract namespace and local name
            if ":" in prop:
                prefix, local = prop.split(":", 1)
                if prefix in context:
                    # Add typed definition
                    context[prop] = {
                        "@id": f"{context[prefix]}{local}",
                        "@type": "xsd:float"
                    }
                    modifications_made.append(f"Added typed definition for {prop}")
    
    if modifications_made:
        print(f"Made {len(modifications_made)} modifications to @context:")
        for mod in modifications_made:
            print(f"  - {mod}")
    else:
        print("No modifications needed in @context")
    
    data["@context"] = context
    return data

def process_jsonld_file(filepath: Path, dry_run: bool = False) -> bool:
    """
    Process a single JSON-LD file to add float typing.
    
    Args:
        filepath: Path to JSON-LD file
        dry_run: If True, don't write changes
        
    Returns:
        True if file was modified, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"Processing: {filepath}")
    print(f"{'='*70}")
    
    try:
        # Read and parse JSON-LD
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add float typing
        original_context = json.dumps(data.get("@context", {}), sort_keys=True)
        data = add_float_typing_to_context(data)
        modified_context = json.dumps(data.get("@context", {}), sort_keys=True)
        
        # Check if actually modified
        if original_context == modified_context:
            print("✓ File already has correct float typing")
            return False
        
        if not dry_run:
            # Write back with UTF-8 encoding and ensure_ascii=False
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add final newline
            
            print(f"✓ File updated successfully")
            return True
        else:
            print(f"✓ Would update file (dry run)")
            return True
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fix xsd:float typing in TSCG JSON-LD files"
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="JSON-LD files to process"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    files_modified = 0
    files_processed = 0
    
    for filepath in args.files:
        if not filepath.exists():
            print(f"✗ File not found: {filepath}", file=sys.stderr)
            continue
        
        if not filepath.suffix == ".jsonld":
            print(f"✗ Skipping non-JSON-LD file: {filepath}", file=sys.stderr)
            continue
        
        files_processed += 1
        if process_jsonld_file(filepath, args.dry_run):
            files_modified += 1
    
    print(f"\n{'='*70}")
    print(f"Summary: {files_modified}/{files_processed} files modified")
    print(f"{'='*70}")
    
    return 0 if files_modified > 0 or args.dry_run else 1

if __name__ == "__main__":
    sys.exit(main())
