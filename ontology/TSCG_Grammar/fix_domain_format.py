#!/usr/bin/env python3
"""
TSCG Domain Format Fixer (v1.0.0)
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-25
Version: 1.0.0

Converts incorrect domain format from string with "/" separator to array format.

PROBLEM:
  Incorrect: "m1:domain": "Photography / Optics"
  Correct:   "m1:domain": ["Photography", "Optics"]

SOLUTION:
  - Detects strings containing "/" separator
  - Splits on "/" and cleans whitespace
  - Converts to array format

Usage:
    python fix_domain_format.py [--dry-run] [--instance <name>]
    
Examples:
    python fix_domain_format.py --dry-run           # Preview changes only
    python fix_domain_format.py                      # Apply changes to all instances
    python fix_domain_format.py --instance ExposureTriangle  # Fix single instance
"""

import json
import re
from pathlib import Path
from datetime import datetime
import shutil
import argparse


# Repository structure
REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
POCLETS_DIR = REPO_ROOT / "instances/poclets"
SYMBOLIC_GRAMMARS_DIR = REPO_ROOT / "instances/symbolic-system-grammars"
SYSTEMIC_FRAMEWORKS_DIR = REPO_ROOT / "instances/systemic-frameworks"
BACKUP_DIR = REPO_ROOT / "domain_format_fix_backups" / datetime.now().strftime("%Y%m%d_%H%M%S")


def find_m0_jsonld_file(instance_dir: Path) -> Path:
    """Find the M0_*.jsonld file in the instance directory."""
    m0_files = list(instance_dir.glob("M0_*.jsonld"))
    if not m0_files:
        return None
    # Prefer file matching directory name
    dir_name = instance_dir.name
    preferred = instance_dir / f"M0_{dir_name}.jsonld"
    if preferred in m0_files:
        return preferred
    # Otherwise return first found
    return m0_files[0]


def needs_domain_format_fix(data: dict) -> tuple[bool, str, list]:
    """
    Check if instance needs domain format conversion.
    
    Returns:
        (needs_fix, current_value, new_value)
        - needs_fix: True if conversion needed
        - current_value: Current domain value as string
        - new_value: New domain value as array (or None if no fix needed)
    """
    if "@graph" not in data or len(data["@graph"]) == 0:
        return False, None, None
    
    ontology = data["@graph"][0]
    
    # Check if m1:domain exists
    if "m1:domain" not in ontology:
        return False, None, None
    
    domain_value = ontology["m1:domain"]
    
    # Already array format - no fix needed
    if isinstance(domain_value, list):
        return False, str(domain_value), None
    
    # String format - check if contains "/"
    if isinstance(domain_value, str) and "/" in domain_value:
        # Split on "/" and clean whitespace
        domains = [d.strip() for d in domain_value.split("/")]
        return True, domain_value, domains
    
    # Single domain string without "/" - no fix needed
    return False, domain_value, None


def fix_domain_format(data: dict) -> tuple[bool, str, str]:
    """
    Fix domain format in the instance data.
    
    Returns:
        (modified, old_value, new_value)
    """
    needs_fix, current, new_array = needs_domain_format_fix(data)
    
    if not needs_fix:
        return False, None, None
    
    # Apply fix
    data["@graph"][0]["m1:domain"] = new_array
    
    return True, current, new_array


def process_instance(instance_name: str, instance_type: str, dry_run: bool = False) -> dict:
    """
    Process a single instance.
    
    Returns:
        Dictionary with processing results
    """
    # Determine instance directory
    type_config = {
        "poclet": POCLETS_DIR,
        "symbolic_grammar": SYMBOLIC_GRAMMARS_DIR,
        "systemic_framework": SYSTEMIC_FRAMEWORKS_DIR
    }
    
    instance_dir = type_config[instance_type] / instance_name
    
    if not instance_dir.exists():
        return {
            "status": "error",
            "message": f"Directory not found: {instance_dir}"
        }
    
    # Find M0 file
    jsonld_file = find_m0_jsonld_file(instance_dir)
    
    if not jsonld_file:
        return {
            "status": "error",
            "message": f"No M0_*.jsonld file found in {instance_dir}"
        }
    
    # Load JSON-LD
    try:
        with open(jsonld_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to load JSON: {str(e)}"
        }
    
    # Check if fix needed
    needs_fix, current, new_array = needs_domain_format_fix(data)
    
    if not needs_fix:
        return {
            "status": "skip",
            "message": "No fix needed",
            "current_value": current
        }
    
    # Apply fix (or just report if dry-run)
    if dry_run:
        return {
            "status": "would_fix",
            "file": str(jsonld_file.relative_to(REPO_ROOT)),
            "old_value": current,
            "new_value": new_array
        }
    
    # Create backup
    backup_file = BACKUP_DIR / instance_name / jsonld_file.name
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(jsonld_file, backup_file)
    
    # Apply fix
    modified, old_val, new_val = fix_domain_format(data)
    
    # Save modified file
    try:
        with open(jsonld_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save JSON: {str(e)}"
        }
    
    return {
        "status": "fixed",
        "file": str(jsonld_file.relative_to(REPO_ROOT)),
        "old_value": old_val,
        "new_value": new_val,
        "backup": str(backup_file.relative_to(REPO_ROOT))
    }


def scan_all_instances() -> list:
    """Scan all instance directories and return list of (name, type) tuples."""
    instances = []
    
    # Poclets
    if POCLETS_DIR.exists():
        for d in POCLETS_DIR.iterdir():
            if d.is_dir():
                instances.append((d.name, "poclet"))
    
    # Symbolic Grammars
    if SYMBOLIC_GRAMMARS_DIR.exists():
        for d in SYMBOLIC_GRAMMARS_DIR.iterdir():
            if d.is_dir():
                instances.append((d.name, "symbolic_grammar"))
    
    # Systemic Frameworks
    if SYSTEMIC_FRAMEWORKS_DIR.exists():
        for d in SYSTEMIC_FRAMEWORKS_DIR.iterdir():
            if d.is_dir():
                instances.append((d.name, "systemic_framework"))
    
    return instances


def generate_report(results: dict, dry_run: bool):
    """Generate summary report."""
    print("\n" + "="*70)
    print("DOMAIN FORMAT FIX SUMMARY")
    print("="*70 + "\n")
    
    would_fix = [name for name, r in results.items() if r['status'] == 'would_fix']
    fixed = [name for name, r in results.items() if r['status'] == 'fixed']
    skipped = [name for name, r in results.items() if r['status'] == 'skip']
    errors = [name for name, r in results.items() if r['status'] == 'error']
    
    if dry_run:
        print(f"🔍 DRY RUN MODE - No changes applied\n")
        print(f"📊 Would fix: {len(would_fix)}")
        print(f"⏭️  Skip (already correct): {len(skipped)}")
        print(f"❌ Errors: {len(errors)}\n")
        
        if would_fix:
            print("="*70)
            print("INSTANCES THAT WOULD BE FIXED:")
            print("="*70 + "\n")
            for name in would_fix:
                r = results[name]
                print(f"📄 {name}")
                print(f"   File: {r['file']}")
                print(f"   Old:  {repr(r['old_value'])}")
                print(f"   New:  {r['new_value']}\n")
    else:
        print(f"✅ Fixed: {len(fixed)}")
        print(f"⏭️  Skipped (already correct): {len(skipped)}")
        print(f"❌ Errors: {len(errors)}\n")
        
        if fixed:
            print("="*70)
            print("INSTANCES FIXED:")
            print("="*70 + "\n")
            for name in fixed:
                r = results[name]
                print(f"✅ {name}")
                print(f"   File: {r['file']}")
                print(f"   Old:  {repr(r['old_value'])}")
                print(f"   New:  {r['new_value']}")
                print(f"   Backup: {r['backup']}\n")
    
    if errors:
        print("="*70)
        print("ERRORS:")
        print("="*70 + "\n")
        for name in errors:
            r = results[name]
            print(f"❌ {name}: {r['message']}\n")


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(
        description="Fix m1:domain format - convert 'Domain1 / Domain2' to ['Domain1', 'Domain2']",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    
    parser.add_argument(
        "--instance",
        type=str,
        help="Process only a specific instance (e.g., ExposureTriangle)"
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("TSCG Domain Format Fixer v1.0.0")
    print("="*70)
    
    # Get instances to process
    if args.instance:
        # Try to find instance type
        instance_type = None
        for type_name, type_dir in [
            ("poclet", POCLETS_DIR),
            ("symbolic_grammar", SYMBOLIC_GRAMMARS_DIR),
            ("systemic_framework", SYSTEMIC_FRAMEWORKS_DIR)
        ]:
            if (type_dir / args.instance).exists():
                instance_type = type_name
                break
        
        if not instance_type:
            print(f"\n❌ Instance not found: {args.instance}")
            return 1
        
        instances = [(args.instance, instance_type)]
    else:
        instances = scan_all_instances()
    
    print(f"\n📊 Processing {len(instances)} instances")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be applied\n")
    else:
        print(f"💾 Backups will be saved to: {BACKUP_DIR}\n")
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process instances
    results = {}
    for instance_name, instance_type in instances:
        result = process_instance(instance_name, instance_type, args.dry_run)
        results[instance_name] = result
        
        # Show progress
        if result['status'] == 'would_fix':
            print(f"🔍 {instance_name}: Would fix")
        elif result['status'] == 'fixed':
            print(f"✅ {instance_name}: Fixed")
        elif result['status'] == 'skip':
            print(f"⏭️  {instance_name}: Already correct")
        elif result['status'] == 'error':
            print(f"❌ {instance_name}: Error - {result['message']}")
    
    # Generate report
    generate_report(results, args.dry_run)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
