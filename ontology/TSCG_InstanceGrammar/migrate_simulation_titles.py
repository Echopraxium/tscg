#!/usr/bin/env python3
"""
migrate_simulation_titles.py
=============================
TSCG Interactive Migration Script — Add m1:simulationTitle to M0 instances

Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-28

This script scans all TSCG instances with static HTML simulations and 
interactively prompts the user to set the m1:simulationTitle property for each.

The m1:simulationTitle is a short, user-friendly display name used in the 
gallery (index.html) and simulation headers, separate from the formal rdfs:label.

Usage:
    python migrate_simulation_titles.py [--root <repo-root>] [--dry-run]

Options:
    --root <path>    Repository root (default: auto-detect from script location)
    --dry-run        Preview changes without modifying files
    --help           Show this help
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Colors for terminal output ───────────────────────────────────────────────
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Print colored header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

# ── Repository detection ──────────────────────────────────────────────────────
def detect_root() -> Path:
    """
    Auto-detect repository root by walking up from script location.
    Looks for .git/ or instances/poclets/ directory.
    """
    candidate = Path(__file__).resolve().parent
    for _ in range(12):
        if (candidate / '.git').exists():
            return candidate
        if (candidate / 'instances' / 'poclets').exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:  # Reached filesystem root
            break
        candidate = parent
    return Path.cwd()

# ── Instance discovery ────────────────────────────────────────────────────────
ONTOLOGY_TYPES = [
    {'id': 'poclets', 'dir': 'poclets', 'label': 'Poclets'},
    {'id': 'systemic-frameworks', 'dir': 'systemic-frameworks', 'label': 'Systemic Frameworks'},
    {'id': 'symbolic-system-grammars', 'dir': 'symbolic-system-grammars', 'label': 'Symbolic System Grammars'},
]

def find_instances_with_simulations(root: Path) -> List[Dict]:
    """
    Scan instances/ directory for instances with static/*.html files.
    Returns list of dicts with instance metadata.
    """
    instances_dir = root / 'instances'
    if not instances_dir.exists():
        print_error(f"instances/ directory not found at: {instances_dir}")
        sys.exit(1)
    
    results = []
    
    for type_config in ONTOLOGY_TYPES:
        type_dir = instances_dir / type_config['dir']
        if not type_dir.exists():
            print_warning(f"Directory not found: {type_config['dir']}")
            continue
        
        for entry in sorted(type_dir.iterdir()):
            if not entry.is_dir():
                continue
            
            static_dir = entry / 'static'
            if not static_dir.exists():
                continue
            
            # Check for .html files
            html_files = list(static_dir.glob('*.html'))
            if not html_files:
                continue
            
            # Find M0_*.jsonld file (prefer file matching folder name)
            jsonld_candidates = list(entry.glob('M0_*.jsonld'))
            if not jsonld_candidates:
                print_warning(f"No M0_*.jsonld found in {entry.name}, skipping")
                continue
            
            # Prefer file matching folder name
            folder_hint = entry.name.lower()
            jsonld_file = next(
                (f for f in jsonld_candidates if folder_hint in f.name.lower()),
                jsonld_candidates[0]
            )
            
            results.append({
                'instance_name': entry.name,
                'jsonld_path': jsonld_file,
                'html_files': html_files,
                'ontology_type': type_config['label'],
            })
    
    return results

# ── JSON-LD parsing and updating ──────────────────────────────────────────────
def load_jsonld(path: Path) -> Tuple[Dict, Dict]:
    """
    Load JSON-LD file and extract main ontology node.
    Returns (full_data, main_node).
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract main ontology node (@graph[0])
    graph = data.get('@graph', [data])
    main_node = graph[0] if graph else {}
    
    return data, main_node

def clean_label(label: str) -> str:
    """
    Clean rdfs:label to suggest a good simulationTitle.
    Removes common prefixes like "TSCG M0", "Poclet", and trailing metadata.
    """
    cleaned = label
    
    # Remove common prefixes
    prefixes_to_remove = [
        'TSCG M0 ',
        'TSCG ',
        'M0 ',
    ]
    for prefix in prefixes_to_remove:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
    
    # Remove trailing " Poclet", " Instance", etc.
    suffixes_to_remove = [
        ' Poclet',
        ' Instance',
        ' System',
    ]
    for suffix in suffixes_to_remove:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
    
    # Remove parenthetical notes
    if '(' in cleaned:
        cleaned = cleaned.split('(')[0].strip()
    
    return cleaned.strip()

def update_jsonld_with_simulation_title(path: Path, simulation_title: str, dry_run: bool = False) -> bool:
    """
    Add m1:simulationTitle to the main ontology node in a JSON-LD file.
    Preserves all existing content and UTF-8 encoding.
    """
    try:
        data, main_node = load_jsonld(path)
        
        # Add m1:simulationTitle to main node
        main_node['m1core:simulationTitle'] = simulation_title
        
        if dry_run:
            print_info(f"[DRY RUN] Would add: m1core:simulationTitle = '{simulation_title}'")
            return True
        
        # Write back with UTF-8 encoding and proper JSON formatting
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print_error(f"Failed to update {path.name}: {e}")
        return False

# ── Interactive prompting ─────────────────────────────────────────────────────
def prompt_simulation_title(instance: Dict) -> Optional[str]:
    """
    Interactively prompt user for simulation title.
    Returns the title or None if user wants to skip.
    """
    jsonld_path = instance['jsonld_path']
    instance_name = instance['instance_name']
    
    # Load current metadata
    try:
        _, main_node = load_jsonld(jsonld_path)
    except Exception as e:
        print_error(f"Failed to load {jsonld_path.name}: {e}")
        return None
    
    rdfs_label = main_node.get('rdfs:label', instance_name)
    current_sim_title = main_node.get('m1core:simulationTitle', None)
    
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}Instance: {instance_name}{Colors.ENDC}")
    print(f"  Type:        {instance['ontology_type']}")
    print(f"  File:        {jsonld_path.name}")
    print(f"  rdfs:label:  {Colors.BOLD}{rdfs_label}{Colors.ENDC}")
    
    if current_sim_title:
        print(f"  {Colors.WARNING}m1:simulationTitle already set: {current_sim_title}{Colors.ENDC}")
        overwrite = input(f"  Overwrite? [y/N]: ").strip().lower()
        if overwrite != 'y':
            print_info("Skipping (keeping existing title)")
            return None
    
    # Suggest cleaned title
    suggested = clean_label(rdfs_label)
    print(f"\n  {Colors.OKGREEN}Suggested: {suggested}{Colors.ENDC}")
    
    # Prompt for user input
    user_input = input(f"  Enter simulation title [Enter = use suggestion, 's' = skip]: ").strip()
    
    if user_input.lower() == 's':
        print_info("Skipping this instance")
        return None
    
    return user_input if user_input else suggested

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    """Main migration workflow."""
    # Parse arguments
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    
    if '--help' in args or '-h' in args:
        print(__doc__)
        sys.exit(0)
    
    # Detect root
    root_override = None
    if '--root' in args:
        idx = args.index('--root')
        if idx + 1 < len(args):
            root_override = Path(args[idx + 1])
    
    root = Path(root_override) if root_override else detect_root()
    
    # Header
    print_header("TSCG Simulation Title Migration")
    print_info(f"Repository root: {root}")
    if dry_run:
        print_warning("DRY RUN MODE — no files will be modified")
    print()
    
    # Discover instances
    print_info("Scanning for instances with static HTML simulations...")
    instances = find_instances_with_simulations(root)
    
    if not instances:
        print_warning("No instances with static/*.html found")
        sys.exit(0)
    
    print_success(f"Found {len(instances)} instance(s) with simulations\n")
    
    # Group by ontology type
    by_type = {}
    for inst in instances:
        otype = inst['ontology_type']
        if otype not in by_type:
            by_type[otype] = []
        by_type[otype].append(inst)
    
    # Show summary
    for otype in sorted(by_type.keys()):
        print(f"  {Colors.BOLD}{otype}:{Colors.ENDC} {len(by_type[otype])} instance(s)")
    
    # Interactive loop
    print(f"\n{Colors.BOLD}Starting interactive migration...{Colors.ENDC}")
    print("(Press Ctrl+C to abort at any time)\n")
    
    updated_count = 0
    skipped_count = 0
    
    try:
        for instance in instances:
            simulation_title = prompt_simulation_title(instance)
            
            if simulation_title:
                if update_jsonld_with_simulation_title(
                    instance['jsonld_path'], 
                    simulation_title, 
                    dry_run=dry_run
                ):
                    updated_count += 1
                    if not dry_run:
                        print_success(f"Updated: m1core:simulationTitle = '{simulation_title}'")
            else:
                skipped_count += 1
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Migration aborted by user{Colors.ENDC}")
        sys.exit(1)
    
    # Summary
    print_header("Migration Complete")
    print(f"  Updated:  {Colors.OKGREEN}{updated_count}{Colors.ENDC} instance(s)")
    print(f"  Skipped:  {Colors.WARNING}{skipped_count}{Colors.ENDC} instance(s)")
    
    if dry_run:
        print(f"\n  {Colors.WARNING}DRY RUN — no files were modified{Colors.ENDC}")
        print(f"  Run without --dry-run to apply changes\n")
    else:
        print(f"\n  {Colors.OKGREEN}Files have been updated successfully{Colors.ENDC}")
        print(f"  Run 'node generate_index.js' to regenerate the gallery\n")

if __name__ == '__main__':
    main()
