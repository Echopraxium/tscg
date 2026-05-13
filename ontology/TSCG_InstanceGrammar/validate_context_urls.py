#!/usr/bin/env python3
"""
TSCG @context URL Validator
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19
Version: 1.0.0

Validates that all namespace URLs in JSON-LD @context are ABSOLUTE, not relative.
This is critical for pyshacl compatibility.

Usage:
    python validate_context_urls.py <file.jsonld>
    python validate_context_urls.py --batch <directory>
    python validate_context_urls.py --fix <file.jsonld>  # Auto-fix relative URLs
"""

import json
import sys
from pathlib import Path
import argparse

# Required absolute URL mappings
REQUIRED_ABSOLUTE_URLS = {
    "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
}

# Known relative patterns to detect
RELATIVE_PATTERNS = {
    "m3": "M3_GenesisSpace.jsonld#",
    "m2": "M2_GenericConcepts.jsonld#",
    "m1": "M1_CoreConcepts.jsonld#",
}


class ContextValidator:
    """Validates @context namespace URLs."""
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.errors = []
        self.warnings = []
        
    def validate(self):
        """Validate the @context URLs."""
        if not self.filepath.exists():
            self.errors.append(f"File not found: {self.filepath}")
            return False
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        
        if "@context" not in data:
            self.warnings.append("No @context found in file")
            return True
        
        context = data["@context"]
        has_violations = False
        
        # Check for required absolute URLs
        for ns_key, required_url in REQUIRED_ABSOLUTE_URLS.items():
            if ns_key in context:
                actual_url = context[ns_key]
                
                # Check if it's the correct absolute URL
                if actual_url != required_url:
                    # Check if it's a known relative pattern
                    if actual_url == RELATIVE_PATTERNS.get(ns_key):
                        self.errors.append(
                            f"❌ CRITICAL: '{ns_key}' uses RELATIVE URL: '{actual_url}'\n"
                            f"   Must use ABSOLUTE URL: '{required_url}'\n"
                            f"   Reason: pyshacl cannot resolve relative URLs"
                        )
                        has_violations = True
                    else:
                        self.warnings.append(
                            f"⚠️  '{ns_key}' uses non-standard URL: '{actual_url}'\n"
                            f"   Expected: '{required_url}'"
                        )
        
        return not has_violations
    
    def fix(self):
        """Automatically fix relative URLs to absolute."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        
        if "@context" not in data:
            self.warnings.append("No @context found - nothing to fix")
            return True
        
        context = data["@context"]
        fixed_count = 0
        
        for ns_key, required_url in REQUIRED_ABSOLUTE_URLS.items():
            if ns_key in context:
                actual_url = context[ns_key]
                
                # Fix if it's a relative URL
                if actual_url == RELATIVE_PATTERNS.get(ns_key):
                    context[ns_key] = required_url
                    fixed_count += 1
                    print(f"✅ Fixed '{ns_key}': {actual_url} → {required_url}")
        
        if fixed_count > 0:
            # Write back
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
            
            print(f"\n✅ Fixed {fixed_count} namespace URL(s) in {self.filepath}")
            return True
        else:
            print(f"ℹ️  No fixes needed for {self.filepath}")
            return True
    
    def report(self):
        """Print validation report."""
        print(f"\n{'='*70}")
        print(f"@context URL Validation: {self.filepath.name}")
        print(f"{'='*70}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ All @context URLs are valid (absolute)")
        
        return len(self.errors) == 0


def validate_file(filepath):
    """Validate a single file."""
    validator = ContextValidator(filepath)
    is_valid = validator.validate()
    validator.report()
    return is_valid


def validate_batch(directory):
    """Validate all JSON-LD files in directory."""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return False
    
    jsonld_files = list(directory.rglob("*.jsonld"))
    
    if not jsonld_files:
        print(f"ℹ️  No .jsonld files found in {directory}")
        return True
    
    print(f"Found {len(jsonld_files)} JSON-LD files")
    
    total = len(jsonld_files)
    passed = 0
    failed = 0
    
    for filepath in jsonld_files:
        validator = ContextValidator(filepath)
        if validator.validate():
            passed += 1
        else:
            failed += 1
            validator.report()
    
    print(f"\n{'='*70}")
    print(f"BATCH VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    
    return failed == 0


def fix_file(filepath):
    """Fix relative URLs in a single file."""
    validator = ContextValidator(filepath)
    return validator.fix()


def main():
    parser = argparse.ArgumentParser(
        description="Validate @context namespace URLs are absolute (pyshacl compatible)"
    )
    parser.add_argument("path", nargs="?", help="File or directory to validate")
    parser.add_argument("--batch", action="store_true", help="Batch mode: validate all .jsonld in directory")
    parser.add_argument("--fix", action="store_true", help="Auto-fix relative URLs to absolute")
    
    args = parser.parse_args()
    
    if not args.path:
        parser.print_help()
        return 1
    
    if args.fix:
        return 0 if fix_file(args.path) else 1
    elif args.batch:
        return 0 if validate_batch(args.path) else 1
    else:
        return 0 if validate_file(args.path) else 1


if __name__ == "__main__":
    sys.exit(main())
