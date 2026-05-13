#!/usr/bin/env python3
"""
TSCG M1 Namespace Migration Script
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19
Version: 1.0.0

Migrates M1 namespace architecture:
  - m1:core → m1 (remove redundancy)
  - m1:biology → m1.ext:biology
  - m1:chemistry → m1.ext:chemistry
  - etc.

Applies to both @context definitions AND type/property references.
"""

import json
import re
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
SEARCH_DIRS = [
    REPO_ROOT / "instances",
    REPO_ROOT / "ontology"
]
BACKUP_DIR = REPO_ROOT / "migration_backups" / f"m1_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
SHACL_SCHEMA = REPO_ROOT / "ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl"

# M1 extensions to migrate
M1_EXTENSIONS = {
    "biology": "m1.ext:biology",
    "chemistry": "m1.ext:chemistry",
    "electronics": "m1.ext:electronics",
    "optics": "m1.ext:optics",
    "music": "m1.ext:music",
    "geology": "m1.ext:geology",
    "physics": "m1.ext:physics",
    "thermodynamics": "m1.ext:thermodynamics",
    "photography": "m1.ext:photography",
    "mythology": "m1.ext:mythology",
    "economics": "m1.ext:economics",
    "education": "m1.ext:education"
}

# ============================================================================
# MIGRATION ENGINE
# ============================================================================

class M1NamespaceMigrator:
    """Migrates M1 namespaces in a single file."""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.relative_path = filepath.relative_to(REPO_ROOT)
        self.modifications = []
        self.errors = []
        self.backup_path = None
    
    def backup(self):
        """Create backup of file."""
        backup_file_dir = BACKUP_DIR / self.relative_path.parent
        backup_file_dir.mkdir(parents=True, exist_ok=True)
        
        self.backup_path = backup_file_dir / self.filepath.name
        shutil.copy2(self.filepath, self.backup_path)
    
    def migrate(self, dry_run=False):
        """Apply M1 namespace migration."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Phase 1: Migrate @context definitions
            context_modified = self._migrate_context(data.get("@context", {}))
            
            # Phase 2: Migrate type/property references throughout file
            # Convert to JSON string for regex-based replacement
            file_content = json.dumps(data, indent=2, ensure_ascii=False)
            content_modified, file_content = self._migrate_references(file_content)
            
            # Parse back to JSON
            if content_modified:
                data = json.loads(file_content)
            
            # Write back if any modifications (unless dry run)
            if context_modified or content_modified:
                if not dry_run:
                    with open(self.filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        f.write('\n')
                
                return True
            else:
                self.modifications.append("No modifications needed")
                return True
                
        except Exception as e:
            self.errors.append(f"Migration failed: {str(e)}")
            return False
    
    def _migrate_context(self, context):
        """Migrate @context namespace definitions."""
        modified = False
        
        # 1. Migrate m1:core → m1
        if "m1:core" in context:
            context["m1"] = context.pop("m1:core")
            self.modifications.append("@context: m1:core → m1")
            modified = True
        
        # 2. Migrate m1:extension → m1.ext:extension
        for old_ext, new_ext in M1_EXTENSIONS.items():
            old_key = f"m1:{old_ext}"
            if old_key in context:
                context[new_ext] = context.pop(old_key)
                self.modifications.append(f"@context: {old_key} → {new_ext}")
                modified = True
        
        return modified
    
    def _migrate_references(self, file_content):
        """Migrate all m1:* references in file content."""
        modified = False
        original_content = file_content
        
        # 1. Migrate m1:core: → m1:
        # Pattern: "m1:core:Something" → "m1:Something"
        pattern_core = r'"m1:core:([^"]+)"'
        replacement_core = r'"m1:\1"'
        
        new_content = re.sub(pattern_core, replacement_core, file_content)
        if new_content != file_content:
            count = len(re.findall(pattern_core, file_content))
            self.modifications.append(f"References: m1:core: → m1: ({count} occurrences)")
            file_content = new_content
            modified = True
        
        # 2. Migrate m1:extension: → m1.ext:extension:
        for old_ext, new_ext in M1_EXTENSIONS.items():
            pattern = f'"m1:{old_ext}:([^"]+)"'
            replacement = f'"{new_ext}:\\1"'
            
            new_content = re.sub(pattern, replacement, file_content)
            if new_content != file_content:
                count = len(re.findall(pattern, file_content))
                self.modifications.append(f"References: m1:{old_ext}: → {new_ext}: ({count} occurrences)")
                file_content = new_content
                modified = True
        
        return modified, file_content
    
    def validate_shacl(self):
        """Validate file with SHACL (only for M0 poclet instances)."""
        # Only validate M0 poclet instances
        if not str(self.filepath).startswith(str(REPO_ROOT / "instances/poclets")):
            return True, "Not a poclet instance (skipped SHACL)"
        
        if not self.filepath.name.startswith("M0_"):
            return True, "Not an M0 file (skipped SHACL)"
        
        if not SHACL_SCHEMA.exists():
            return True, f"SHACL schema not found (skipped): {SHACL_SCHEMA}"
        
        try:
            result = subprocess.run(
                [
                    "pyshacl",
                    "-s", str(SHACL_SCHEMA),
                    "-df", "json-ld",
                    str(self.filepath)
                ],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT / "ontology")
            )
            
            if "Conforms: True" in result.stdout:
                return True, "SHACL validation passed"
            else:
                # Extract first violation for readability
                lines = result.stdout.split('\n')
                violation_summary = '\n'.join(lines[:30])  # First 30 lines
                return False, f"SHACL validation failed:\n{violation_summary}\n..."
                
        except Exception as e:
            return False, f"SHACL validation error: {str(e)}"
    
    def rollback(self):
        """Restore from backup."""
        if self.backup_path and self.backup_path.exists():
            shutil.copy2(self.backup_path, self.filepath)
            return True
        return False

# ============================================================================
# BATCH PROCESSOR
# ============================================================================

class BatchMigrator:
    """Processes multiple files with migration pipeline."""
    
    def __init__(self, dry_run=False, stop_on_error=True, skip_shacl=False):
        self.dry_run = dry_run
        self.stop_on_error = stop_on_error
        self.skip_shacl = skip_shacl
        self.results = {}
        self.total_files = 0
        self.processed = 0
        self.succeeded = 0
        self.failed = 0
    
    def collect_files(self):
        """Collect all .jsonld files to migrate."""
        all_files = []
        for search_dir in SEARCH_DIRS:
            if search_dir.exists():
                all_files.extend(search_dir.rglob("*.jsonld"))
        
        # Filter out archives and backups
        filtered_files = [
            f for f in all_files 
            if "_archives" not in str(f) and "backup" not in str(f).lower()
        ]
        
        return filtered_files
    
    def migrate_file(self, filepath):
        """Migrate a single file with full pipeline."""
        migrator = M1NamespaceMigrator(filepath)
        
        print(f"\n{'='*70}")
        print(f"MIGRATING: {migrator.relative_path}")
        print(f"{'='*70}")
        
        # Checkpoint 1: Backup
        print("\n📦 Checkpoint 1: Creating backup...")
        migrator.backup()
        print(f"   ✓ Backup created")
        
        # Checkpoint 2: Migrate
        print("\n🔧 Checkpoint 2: Applying M1 namespace migration...")
        
        if self.dry_run:
            print("   [DRY RUN MODE - analyzing without writing]")
        
        if not migrator.migrate(dry_run=self.dry_run):
            print(f"   ❌ Migration failed: {migrator.errors}")
            self.results[str(migrator.relative_path)] = {
                'status': 'failed',
                'modifications': migrator.modifications,
                'errors': migrator.errors
            }
            return False
        
        if migrator.modifications:
            if self.dry_run:
                print("   [DRY RUN] Would apply:")
            for mod in migrator.modifications:
                print(f"   • {mod}")
        else:
            print("   ℹ️  No modifications needed")
        
        # Checkpoint 3: Validate (if not dry run and not skip_shacl)
        if not self.dry_run:
            if self.skip_shacl:
                print("\n⏭️ Checkpoint 3: SHACL validation skipped (--skip-shacl-validation)")
            else:
                print("\n✅ Checkpoint 3: Validating with SHACL...")
                valid, message = migrator.validate_shacl()
                
                if not valid:
                    print(f"   ❌ {message}")
                    print("\n⚠️  ROLLBACK: Restoring from backup...")
                    if migrator.rollback():
                        print("   ✓ Rollback complete")
                    else:
                        print("   ❌ Rollback failed!")
                    
                    self.results[str(migrator.relative_path)] = {
                        'status': 'failed',
                        'modifications': migrator.modifications,
                        'errors': [message]
                    }
                    return False
                else:
                    print(f"   ✓ {message}")
        
        print(f"\n{'='*70}")
        print(f"✅ MIGRATION COMPLETE: {migrator.relative_path}")
        print(f"{'='*70}")
        
        self.results[str(migrator.relative_path)] = {
            'status': 'success',
            'modifications': migrator.modifications,
            'errors': []
        }
        return True
    
    def migrate_all(self):
        """Migrate all collected files."""
        files = self.collect_files()
        self.total_files = len(files)
        
        print("="*70)
        print("TSCG M1 NAMESPACE MIGRATION")
        print("="*70)
        print(f"\n📊 Found {self.total_files} .jsonld files to process")
        
        if self.dry_run:
            print("⚠️  DRY RUN MODE - No files will be modified")
        
        # Confirm unless dry run
        if not self.dry_run:
            print(f"\n⚠️  This will modify {self.total_files} files.")
            print(f"   Backups will be created in: {BACKUP_DIR}")
            
            response = input("\nProceed? [y/N]: ")
            if response.lower() != 'y':
                print("❌ Migration cancelled")
                return 1
        
        # Create backup directory
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Process each file
        for filepath in files:
            self.processed += 1
            success = self.migrate_file(filepath)
            
            if success:
                self.succeeded += 1
            else:
                self.failed += 1
                if self.stop_on_error and not self.dry_run:
                    print("\n❌ STOPPING: Error encountered and --stop-on-error is enabled")
                    break
        
        # Generate report
        self._generate_report()
        
        # Summary
        print("\n" + "="*70)
        print("MIGRATION COMPLETE")
        print("="*70)
        print(f"\n✅ Successfully migrated: {self.succeeded}/{self.total_files} files")
        print(f"❌ Failed: {self.failed}/{self.total_files} files")
        print(f"\n📁 Backups: {BACKUP_DIR}")
        
        return 0 if self.failed == 0 else 1
    
    def _generate_report(self):
        """Generate migration report."""
        report_path = BACKUP_DIR / "M1_MIGRATION_REPORT.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# TSCG M1 Namespace Migration Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Backup Location:** {BACKUP_DIR}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE'}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- ✅ **Successful:** {self.succeeded}\n")
            f.write(f"- ❌ **Failed:** {self.failed}\n")
            f.write(f"- 📊 **Total:** {self.total_files}\n\n")
            
            f.write("## Migration Rules Applied\n\n")
            f.write("### @context Definitions\n")
            f.write("- `m1:core` → `m1`\n")
            for old_ext, new_ext in M1_EXTENSIONS.items():
                f.write(f"- `m1:{old_ext}` → `{new_ext}`\n")
            f.write("\n")
            
            f.write("### Type/Property References\n")
            f.write("- `m1:core:*` → `m1:*`\n")
            for old_ext, new_ext in M1_EXTENSIONS.items():
                f.write(f"- `m1:{old_ext}:*` → `{new_ext}:*`\n")
            f.write("\n---\n\n")
            
            f.write("## Detailed Results\n\n")
            for filepath, result in self.results.items():
                f.write(f"### {filepath}\n")
                f.write(f"**Status:** {'✅ Success' if result['status'] == 'success' else '❌ Failed'}\n\n")
                
                if result['modifications']:
                    f.write("**Modifications:**\n")
                    for mod in result['modifications']:
                        f.write(f"- {mod}\n")
                    f.write("\n")
                
                if result['errors']:
                    f.write("**Errors:**\n")
                    for err in result['errors']:
                        f.write(f"- {err}\n")
                    f.write("\n")
        
        print(f"\n📄 Migration report: {report_path.relative_to(REPO_ROOT)}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution flow."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate TSCG M1 namespace architecture"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue migration even if errors occur (default: stop on error)"
    )
    parser.add_argument(
        "--skip-shacl-validation",
        action="store_true",
        help="Skip SHACL validation (useful when fixing pre-existing violations)"
    )
    
    args = parser.parse_args()
    
    migrator = BatchMigrator(
        dry_run=args.dry_run,
        stop_on_error=not args.continue_on_error,
        skip_shacl=args.skip_shacl_validation
    )
    
    return migrator.migrate_all()

if __name__ == "__main__":
    sys.exit(main())
