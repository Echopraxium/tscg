#!/usr/bin/env python3
"""
TSCG M0 Instance SHACL Validator (v1.0.0)
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-20
Version: 1.0.0

Simple standalone script to validate a single M0 instance JSON-LD file
against the TSCG SHACL grammar schema.

Usage:
    python validate_m0_instance.py <path-to-m0-jsonld-file> [--schema <shacl-schema-path>]

Examples:
    python validate_m0_instance.py instances/poclets/FireTriangle/M0_FireTriangle.jsonld
    python validate_m0_instance.py M0_MyNewPoclet.jsonld --schema ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl
"""

import sys
import subprocess
from pathlib import Path
import argparse


def validate_m0_instance(jsonld_path: Path, schema_path: Path) -> tuple[bool, str]:
    """
    Validate a single M0 instance JSON-LD file against the SHACL schema.
    
    Args:
        jsonld_path: Path to the M0 JSON-LD file to validate
        schema_path: Path to the SHACL schema file (*.ttl)
    
    Returns:
        Tuple of (is_valid, message)
        - is_valid: True if validation passed, False otherwise
        - message: Detailed validation results or error message
    """
    # Check if files exist
    if not jsonld_path.exists():
        return False, f"ERROR: JSON-LD file not found: {jsonld_path}"
    
    if not schema_path.exists():
        return False, f"ERROR: SHACL schema file not found: {schema_path}"
    
    # Check file extensions
    if jsonld_path.suffix.lower() != '.jsonld':
        return False, f"ERROR: Input file must be a .jsonld file, got: {jsonld_path.suffix}"
    
    if schema_path.suffix.lower() != '.ttl':
        return False, f"ERROR: Schema file must be a .ttl file, got: {schema_path.suffix}"
    
    print(f"\n{'='*70}")
    print(f"TSCG M0 INSTANCE SHACL VALIDATION")
    print(f"{'='*70}")
    print(f"\n📄 Instance file: {jsonld_path}")
    print(f"📋 Schema file:   {schema_path}")
    print(f"\n{'='*70}\n")
    
    try:
        # Run pyshacl validation
        result = subprocess.run(
            [
                "pyshacl",
                "-s", str(schema_path),
                "-df", "json-ld",
                str(jsonld_path)
            ],
            capture_output=True,
            text=True,
            cwd=str(jsonld_path.parent)
        )
        
        # Check result
        if "Conforms: True" in result.stdout:
            success_msg = "✅ VALIDATION PASSED - Instance conforms to TSCG SHACL grammar"
            print(success_msg)
            print(f"\n{'='*70}\n")
            return True, success_msg
        else:
            # Parse and display violations
            failure_msg = "❌ VALIDATION FAILED - SHACL constraint violations detected"
            print(failure_msg)
            print("\n" + "="*70)
            print("VALIDATION REPORT:")
            print("="*70)
            print(result.stdout)
            if result.stderr:
                print("\nERROR OUTPUT:")
                print(result.stderr)
            print("="*70 + "\n")
            return False, f"{failure_msg}\n\n{result.stdout}"
    
    except FileNotFoundError:
        error_msg = (
            "ERROR: pyshacl command not found.\n"
            "Please install it with: pip install pyshacl\n"
            "For more info: https://github.com/RDFLib/pySHACL"
        )
        print(error_msg)
        return False, error_msg
    
    except Exception as e:
        error_msg = f"ERROR: Validation failed with exception: {str(e)}"
        print(error_msg)
        return False, error_msg


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(
        description="Validate a TSCG M0 instance JSON-LD file against SHACL grammar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_m0_instance.py M0_MyPoclet.jsonld
  python validate_m0_instance.py instances/poclets/FireTriangle/M0_FireTriangle.jsonld
  python validate_m0_instance.py M0_MyPoclet.jsonld --schema custom_schema.ttl
        """
    )
    
    parser.add_argument(
        "jsonld_file",
        type=Path,
        help="Path to the M0 instance JSON-LD file to validate"
    )
    
    parser.add_argument(
        "--schema", "-s",
        type=Path,
        default=None,
        help="Path to the SHACL schema file (default: auto-detect in ontology/TSCG_Grammar/)"
    )
    
    args = parser.parse_args()
    
    # Resolve schema path
    if args.schema:
        schema_path = args.schema.resolve()
    else:
        # Try common locations
        possible_schemas = [
            Path("ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl"),
            Path("../ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl"),
            Path("../../ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl"),
        ]
        
        schema_path = None
        for candidate in possible_schemas:
            if candidate.exists():
                schema_path = candidate.resolve()
                break
        
        if not schema_path:
            print("ERROR: Could not auto-detect SHACL schema file.")
            print("Please specify it explicitly with --schema option.")
            print("\nExpected location: ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl")
            return 1
    
    # Validate
    jsonld_path = args.jsonld_file.resolve()
    is_valid, message = validate_m0_instance(jsonld_path, schema_path)
    
    # Return appropriate exit code
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
