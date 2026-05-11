#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script: ontologyCategory -> ontologyType
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-05-11

This script migrates all occurrences of 'ontologyCategory' to 'ontologyType'
in TSCG ontology files (M3, M2, M1, M0 layers).

Replacements performed:
- "m3:ontologyCategory" -> "m3:ontologyType"
- "m2:ontologyCategory" -> "m3:ontologyType" 
- "ontologyCategory" -> "ontologyType" (in @context definitions)

Usage:
    python migrate_ontologyCategory_to_ontologyType.py --dir <ontology_dir> [--dry-run] [--no-backup]
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
import sys
import argparse

class OntologyMigrator:
    def __init__(self, root_dir, dry_run=False, backup=True):
        """
        Initialize the migrator.
        
        Args:
            root_dir: Root directory containing ontology files
            dry_run: If True, only show what would be changed without modifying files
            backup: If True, create backups before modifying files
        """
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.backup = backup and not dry_run  # No backup needed in dry-run mode
        self.backup_dir = None
        self.report = {
            'files_processed': 0,
            'files_modified': 0,
            'replacements': 0,
            'errors': [],
            'modified_files': [],
            'changes_by_file': {}
        }
        
        if self.backup:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.backup_dir = self.root_dir / f"backup_ontologyCategory_{timestamp}"
            self.backup_dir.mkdir(exist_ok=True)
    
    def find_jsonld_files(self):
        """Find all .jsonld files recursively in the directory tree."""
        jsonld_files = []
        
        # Search recursively for all M0, M1, M2, M3 patterns
        # This will cover:
        # - Root level: M3_*.jsonld, M2_*.jsonld, M1_CoreConcepts.jsonld
        # - instances/**: M0_*.jsonld (all poclets, systemic frameworks, etc.)
        # - M1-Extensions/**: M1_*.jsonld (all domain extensions)
        for pattern in ['M3_*.jsonld', 'M2_*.jsonld', 'M1_*.jsonld', 'M0_*.jsonld']:
            jsonld_files.extend(self.root_dir.rglob(pattern))
        
        # Remove duplicates and sort
        jsonld_files = list(set(jsonld_files))
        return sorted(jsonld_files)
    
    def create_backup(self, file_path):
        """Create a backup of the file."""
        if not self.backup:
            return
        
        relative_path = file_path.relative_to(self.root_dir)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        print(f"  ✓ Backup created: {backup_path}")
    
    def migrate_content(self, content):
        """
        Migrate content by replacing ontologyCategory with ontologyType.
        Returns tuple: (modified_content, replacement_count, changes_list)
        """
        changes = []
        replacement_count = 0
        
        # Pattern 1: "m3:ontologyCategory" -> "m3:ontologyType"
        if '"m3:ontologyCategory"' in content:
            count = content.count('"m3:ontologyCategory"')
            content = content.replace('"m3:ontologyCategory"', '"m3:ontologyType"')
            replacement_count += count
            changes.append(f'"m3:ontologyCategory" -> "m3:ontologyType" ({count} times)')
        
        # Pattern 2: "m2:ontologyCategory" -> "m3:ontologyType"
        if '"m2:ontologyCategory"' in content:
            count = content.count('"m2:ontologyCategory"')
            content = content.replace('"m2:ontologyCategory"', '"m3:ontologyType"')
            replacement_count += count
            changes.append(f'"m2:ontologyCategory" -> "m3:ontologyType" ({count} times)')
        
        # Pattern 3: 'm3:ontologyCategory' (single quotes)
        if "'m3:ontologyCategory'" in content:
            count = content.count("'m3:ontologyCategory'")
            content = content.replace("'m3:ontologyCategory'", "'m3:ontologyType'")
            replacement_count += count
            changes.append(f"'m3:ontologyCategory' -> 'm3:ontologyType' ({count} times)")
        
        # Pattern 4: 'm2:ontologyCategory' (single quotes)
        if "'m2:ontologyCategory'" in content:
            count = content.count("'m2:ontologyCategory'")
            content = content.replace("'m2:ontologyCategory'", "'m3:ontologyType'")
            replacement_count += count
            changes.append(f"'m2:ontologyCategory' -> 'm3:ontologyType' ({count} times)")
        
        # Pattern 5: "ontologyCategory": in @context (becomes "ontologyType":)
        if '"ontologyCategory":' in content:
            count = content.count('"ontologyCategory":')
            content = content.replace('"ontologyCategory":', '"ontologyType":')
            replacement_count += count
            changes.append(f'"ontologyCategory": -> "ontologyType": in @context ({count} times)')
        
        return content, replacement_count, changes
    
    def migrate_file(self, file_path):
        """Migrate a single JSON-LD file."""
        self.report['files_processed'] += 1
        
        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Perform migration
            modified_content, replacement_count, changes = self.migrate_content(original_content)
            
            if replacement_count == 0:
                print(f"  ○ No changes needed")
                return
            
            # Record changes
            self.report['files_modified'] += 1
            self.report['replacements'] += replacement_count
            self.report['modified_files'].append(str(file_path.relative_to(self.root_dir)))
            self.report['changes_by_file'][str(file_path.relative_to(self.root_dir))] = changes
            
            if self.dry_run:
                print(f"  ⚠ DRY-RUN: Would modify file ({replacement_count} replacements)")
                for change in changes:
                    print(f"    - {change}")
            else:
                # Create backup
                self.create_backup(file_path)
                
                # Validate JSON before writing
                try:
                    json.loads(modified_content)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Modified content is not valid JSON: {e}")
                
                # Write modified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                
                print(f"  ✓ Modified ({replacement_count} replacements)")
                for change in changes:
                    print(f"    - {change}")
        
        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            self.report['errors'].append(error_msg)
            print(f"  ✗ ERROR: {str(e)}")
    
    def run(self):
        """Run the migration process."""
        print("=" * 80)
        print("TSCG Ontology Migration: ontologyCategory -> ontologyType")
        print("=" * 80)
        print(f"Root directory: {self.root_dir}")
        print(f"Mode: {'DRY-RUN (no files will be modified)' if self.dry_run else 'LIVE (files will be modified)'}")
        print(f"Backup: {'Enabled' if self.backup else 'Disabled'}")
        print()
        
        # Find all JSON-LD files
        jsonld_files = self.find_jsonld_files()
        
        if not jsonld_files:
            print("No JSON-LD files found matching M3_*, M2_*, M1_*, M0_* patterns.")
            return
        
        print(f"Found {len(jsonld_files)} JSON-LD files to process:")
        for f in jsonld_files:
            print(f"  - {f.relative_to(self.root_dir)}")
        print()
        
        # Process each file
        print("Processing files...")
        print("-" * 80)
        for file_path in jsonld_files:
            print(f"\n{file_path.name}:")
            self.migrate_file(file_path)
        
        # Print summary report
        print()
        print("=" * 80)
        print("MIGRATION SUMMARY")
        print("=" * 80)
        print(f"Files processed:    {self.report['files_processed']}")
        print(f"Files modified:     {self.report['files_modified']}")
        print(f"Total replacements: {self.report['replacements']}")
        print(f"Errors:             {len(self.report['errors'])}")
        
        if self.report['modified_files']:
            print("\nModified files:")
            for file_name in self.report['modified_files']:
                print(f"  ✓ {file_name}")
                if file_name in self.report['changes_by_file']:
                    for change in self.report['changes_by_file'][file_name]:
                        print(f"      - {change}")
        
        if self.report['errors']:
            print("\nErrors encountered:")
            for error in self.report['errors']:
                print(f"  ✗ {error}")
        
        if self.backup and self.report['files_modified'] > 0:
            print(f"\nBackup directory: {self.backup_dir}")
        
        if self.dry_run and self.report['files_modified'] > 0:
            print("\n⚠ DRY-RUN MODE: No files were actually modified.")
            print("   Run without --dry-run to apply changes.")
        
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Migrate ontologyCategory to ontologyType in TSCG ontology files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run to see what would be changed (from cli-tools directory)
  cd cli-tools
  python migrate_ontologyCategory_to_ontologyType.py --dir ../ontology --dry-run
  
  # Apply migration with backup
  python migrate_ontologyCategory_to_ontologyType.py --dir ../ontology
  
  # Apply migration without backup
  python migrate_ontologyCategory_to_ontologyType.py --dir ../ontology --no-backup
        """
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        required=True,
        help='Root directory containing ontology files'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files (not recommended unless using version control)'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    ontology_dir = Path(args.dir)
    if not ontology_dir.exists():
        print(f"Error: Directory does not exist: {ontology_dir}")
        sys.exit(1)
    
    if not ontology_dir.is_dir():
        print(f"Error: Path is not a directory: {ontology_dir}")
        sys.exit(1)
    
    # Run migration
    migrator = OntologyMigrator(
        root_dir=ontology_dir,
        dry_run=args.dry_run,
        backup=not args.no_backup
    )
    
    migrator.run()


if __name__ == '__main__':
    main()
