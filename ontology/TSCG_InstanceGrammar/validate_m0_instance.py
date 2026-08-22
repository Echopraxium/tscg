#!/usr/bin/env python3
"""
TSCG M0 Instance SHACL Validator (v1.1.0)
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-08-21
Version: 1.1.0

Standalone script to validate a single M0 instance JSON-LD file against the TSCG
SHACL grammar schema.

Single source of truth: the schema lives ONLY at
    ontology/cli-tools/check-M0/M0_Instances_Schema_shacl.ttl
(the same file the check-M0 acceptance gate uses). This validator reads that file
so its SHACL verdict always matches the gate. The former duplicate at
ontology/TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl has been removed.

Usage:
    python validate_m0_instance.py <path-to-m0-jsonld-file> [--schema <shacl-schema-path>]

Examples:
    python validate_m0_instance.py instances/poclets/FireTriangle/M0_FireTriangle.jsonld
    python validate_m0_instance.py M0_MyNewPoclet.jsonld   # uses the check-M0 reference schema
"""

import sys
import subprocess
from pathlib import Path
import argparse


# The single-source reference schema, resolved relative to THIS script's location
# (robust to the current working directory). This script lives at
# ontology/TSCG_InstanceGrammar/ ; the schema lives at ontology/cli-tools/check-M0/.
REFERENCE_SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "cli-tools" / "check-M0" / "M0_Instances_Schema_shacl.ttl"
)


def validate_m0_instance(jsonld_path: Path, schema_path: Path) -> tuple[bool, str]:
    """Validate a single M0 instance JSON-LD file against the SHACL schema."""
    if not jsonld_path.exists():
        return False, f"ERROR: JSON-LD file not found: {jsonld_path}"

    if not schema_path.exists():
        return False, f"ERROR: SHACL schema file not found: {schema_path}"

    if jsonld_path.suffix.lower() != '.jsonld':
        return False, f"ERROR: Input file must be a .jsonld file, got: {jsonld_path.suffix}"

    if schema_path.suffix.lower() != '.ttl':
        return False, f"ERROR: Schema file must be a .ttl file, got: {schema_path.suffix}"

    print(f"\n{'='*70}")
    print("TSCG M0 INSTANCE SHACL VALIDATION")
    print(f"{'='*70}")
    print(f"\nInstance file: {jsonld_path}")
    print(f"Schema file:   {schema_path}")
    print(f"\n{'='*70}\n")

    try:
        result = subprocess.run(
            ["pyshacl", "-s", str(schema_path), "-df", "json-ld", str(jsonld_path)],
            capture_output=True,
            text=True,
            cwd=str(jsonld_path.parent),
        )

        if "Conforms: True" in result.stdout:
            success_msg = "VALIDATION PASSED - Instance conforms to TSCG SHACL grammar"
            print(success_msg)
            print(f"\n{'='*70}\n")
            return True, success_msg
        else:
            failure_msg = "VALIDATION FAILED - SHACL constraint violations detected"
            print(failure_msg)
            print("\n" + "=" * 70)
            print("VALIDATION REPORT:")
            print("=" * 70)
            print(result.stdout)
            if result.stderr:
                print("\nERROR OUTPUT:")
                print(result.stderr)
            print("=" * 70 + "\n")
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
    parser = argparse.ArgumentParser(
        description="Validate a TSCG M0 instance JSON-LD file against the check-M0 SHACL grammar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_m0_instance.py M0_MyPoclet.jsonld
  python validate_m0_instance.py instances/poclets/FireTriangle/M0_FireTriangle.jsonld
  python validate_m0_instance.py M0_MyPoclet.jsonld --schema custom_schema.ttl

By default the schema is the single-source reference used by the check-M0 gate:
  ontology/cli-tools/check-M0/M0_Instances_Schema_shacl.ttl
        """,
    )

    parser.add_argument(
        "jsonld_file",
        type=Path,
        help="Path to the M0 instance JSON-LD file to validate",
    )

    parser.add_argument(
        "--schema", "-s",
        type=Path,
        default=None,
        help="Override the SHACL schema (default: the check-M0 reference schema)",
    )

    args = parser.parse_args()

    if args.schema:
        schema_path = args.schema.resolve()
    else:
        schema_path = REFERENCE_SCHEMA
        if not schema_path.exists():
            print("ERROR: Could not find the reference SHACL schema.")
            print(f"Expected at: {schema_path}")
            print("Specify one explicitly with --schema, or check the repo layout.")
            return 1

    jsonld_path = args.jsonld_file.resolve()
    is_valid, _ = validate_m0_instance(jsonld_path, schema_path)
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
