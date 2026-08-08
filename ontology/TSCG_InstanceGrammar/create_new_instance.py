#!/usr/bin/env python3
"""
Create a new TSCG instance (poclet) from M0_INSTANCE_TEMPLATE.jsonld.

Author: Echopraxium with the collaboration of Claude AI

Python port of create_new_poclet.ps1, with three fixes/improvements:
  - auto-detects the repository root (no hard-coded absolute path),
  - reads the template from ontology/TSCG_InstanceGrammar/ (correct location),
  - validates the generated JSON after writing.

Usage:
  python create_new_instance.py --name FireTriangle --domain Physics
  python create_new_instance.py --name FireTriangle --domain Physics \
      --label "Fire Triangle - combustion prerequisites" \
      --description "Models the three prerequisites of combustion ..."
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

TEMPLATE_REL = Path("ontology") / "TSCG_InstanceGrammar" / "M0_INSTANCE_TEMPLATE.jsonld"
POCLETS_REL = Path("instances") / "poclets"

# Exact placeholder strings carried by the template.
LABEL_PLACEHOLDER = "INSTANCE_NAME - Short Descriptive Title"
DESCRIPTION_PLACEHOLDER = (
    "Detailed description of the poclet and its systemic properties. "
    "Explain what system/phenomenon is modeled and why it's a good TSCG candidate."
)
CHANGELOG_PLACEHOLDER = "Initial M0 poclet ontology with ASFID/REVOI bicephalous modeling"
DATE_PLACEHOLDER = "2026-04-18"


def find_repo_root(start: Path) -> Path:
    """Walk upward until a directory containing the template is found."""
    for d in [start, *start.parents]:
        if (d / TEMPLATE_REL).is_file():
            return d
    sys.exit(
        "ERROR: could not locate the TSCG repository root "
        f"(no '{TEMPLATE_REL.as_posix()}' found above {start})."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new TSCG instance from M0_INSTANCE_TEMPLATE.jsonld."
    )
    parser.add_argument("--name", required=True,
                        help="Instance name in PascalCase, e.g. FireTriangle.")
    parser.add_argument("--domain", required=True,
                        help="Domain, e.g. Physics.")
    parser.add_argument("--label", default="",
                        help="Optional rdfs:label short title.")
    parser.add_argument("--description", default="",
                        help="Optional rdfs:comment description.")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve().parent)
    template_file = repo_root / TEMPLATE_REL
    poclets_dir = repo_root / POCLETS_REL
    today = date.today().isoformat()

    name = args.name
    if not re.match(r"^[A-Z][A-Za-z0-9]*$", name):
        print(f"WARNING: instance name should be PascalCase "
              f"(e.g. FireTriangle, FourStrokeEngine); got '{name}'.")
        if input("Continue anyway? (y/n) ").strip().lower() != "y":
            return 0

    instance_dir = poclets_dir / name
    instance_file = instance_dir / f"M0_{name}.jsonld"
    if instance_dir.exists():
        sys.exit(f"ERROR: instance directory already exists: {instance_dir}")

    label = args.label or f"{name} - TODO: Add Short Descriptive Title"
    description = args.description or (
        f"TODO: Add detailed description of the {name} instance and its systemic "
        f"properties. Explain what system/phenomenon is modeled and why it's a "
        f"good TSCG candidate."
    )

    print("=" * 60)
    print(f"Creating new TSCG instance: {name}")
    print("=" * 60)

    content = template_file.read_text(encoding="utf-8")
    # Order matters: substitute the full placeholder strings before the bare token.
    content = content.replace(LABEL_PLACEHOLDER, label)
    content = content.replace(DESCRIPTION_PLACEHOLDER, description)
    content = content.replace(CHANGELOG_PLACEHOLDER,
                              f"Initial M0 instance ontology for {name}")
    content = content.replace(DATE_PLACEHOLDER, today)
    content = content.replace("INSTANCE_NAME", name)   # m0 self-path IRIs
    content = content.replace("DOMAIN_NAME", args.domain)

    # Validate the generated JSON before writing anything to disk.
    try:
        json.loads(content)
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: generated content is not valid JSON: {exc}")

    instance_dir.mkdir(parents=True, exist_ok=False)
    instance_file.write_text(content, encoding="utf-8")

    print(f"  written: {instance_file.relative_to(repo_root).as_posix()}")
    print("=" * 60)
    print("Next steps:")
    print("  1. Open the file and complete the TODO sections")
    print("     (rdfs:label, rdfs:comment, ASFID + REVOI scores,")
    print("      m0:epistemicGap, m0:components, m0:interactions).")
    print("  2. Validate against SHACL:")
    print("     pyshacl -s ontology/TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl "
          f"-df json-ld {instance_file.relative_to(repo_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
