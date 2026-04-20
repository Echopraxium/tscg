#!/usr/bin/env python3
"""
TSCG M1 Namespace Audit Script
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19
Version: 1.0.0

Analyzes usage of M1 namespaces in TSCG corpus to plan migration:
  m1:core → m1: (remove redundancy)
  m1:biology → m1.ext:biology
  m1:chemistry → m1.ext:chemistry
  etc.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
SEARCH_DIRS = [
    REPO_ROOT / "instances",
    REPO_ROOT / "ontology"
]

# M1 extensions to search for
M1_EXTENSIONS = [
    "core",
    "biology",
    "chemistry", 
    "electronics",
    "optics",
    "music",
    "geology",
    "physics",
    "thermodynamics",
    "photography",
    "mythology",
    "economics"
]

# ============================================================================
# AUDIT ENGINE
# ============================================================================

class M1NamespaceAuditor:
    """Audits M1 namespace usage across TSCG corpus."""
    
    def __init__(self):
        self.results = defaultdict(lambda: {
            'context_definitions': [],  # Files defining this namespace
            'property_usages': [],      # Files using properties with this namespace
            'type_usages': []           # Files using types with this namespace
        })
        self.total_files = 0
        self.processed_files = 0
    
    def audit_file(self, filepath):
        """Audit a single JSON-LD file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            relative_path = filepath.relative_to(REPO_ROOT)
            
            # Check @context for namespace definitions
            context = data.get("@context", {})
            for ext in M1_EXTENSIONS:
                namespace_key = f"m1:{ext}"
                if namespace_key in context:
                    self.results[namespace_key]['context_definitions'].append(str(relative_path))
            
            # Check for property/type usages (in entire JSON structure)
            file_content = json.dumps(data)
            for ext in M1_EXTENSIONS:
                namespace_key = f"m1:{ext}"
                # Look for "m1:ext:" pattern (with colon after)
                pattern = f'"{namespace_key}:'
                if pattern in file_content:
                    # Distinguish between properties and types
                    # Property: "m1:ext:propertyName"
                    # Type: "@type": ["...", "m1:ext:ClassName"]
                    
                    # Extract all matches
                    matches = re.findall(f'"{namespace_key}:([^"]+)"', file_content)
                    if matches:
                        entry = {
                            'file': str(relative_path),
                            'usages': list(set(matches))  # Unique usages
                        }
                        
                        # Heuristic: if used in @type context, it's a type usage
                        if '"@type"' in file_content and any(m in file_content for m in matches):
                            self.results[namespace_key]['type_usages'].append(entry)
                        else:
                            self.results[namespace_key]['property_usages'].append(entry)
            
            self.processed_files += 1
            
        except Exception as e:
            print(f"⚠️  Error processing {filepath}: {e}")
    
    def audit_corpus(self):
        """Audit all .jsonld files in corpus."""
        print("="*70)
        print("TSCG M1 NAMESPACE AUDIT")
        print("="*70)
        
        # Collect all .jsonld files
        all_files = []
        for search_dir in SEARCH_DIRS:
            if search_dir.exists():
                all_files.extend(search_dir.rglob("*.jsonld"))
        
        self.total_files = len(all_files)
        
        print(f"\n📊 Found {self.total_files} .jsonld files to analyze")
        print(f"📂 Search directories: {', '.join(str(d.relative_to(REPO_ROOT)) for d in SEARCH_DIRS)}")
        print(f"🔍 Looking for {len(M1_EXTENSIONS)} M1 extensions: {', '.join(M1_EXTENSIONS)}\n")
        
        # Process each file
        for filepath in all_files:
            self.audit_file(filepath)
        
        print(f"\n✅ Processed {self.processed_files}/{self.total_files} files\n")
    
    def generate_report(self, output_path):
        """Generate detailed audit report."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# TSCG M1 Namespace Audit Report\n\n")
            f.write(f"**Files Analyzed:** {self.processed_files}\n")
            f.write(f"**Extensions Searched:** {len(M1_EXTENSIONS)}\n\n")
            
            # Summary table
            f.write("## Summary\n\n")
            f.write("| Namespace | Context Defs | Property Usages | Type Usages |\n")
            f.write("|-----------|-------------|-----------------|-------------|\n")
            
            for ext in M1_EXTENSIONS:
                namespace_key = f"m1:{ext}"
                ctx_count = len(self.results[namespace_key]['context_definitions'])
                prop_count = len(self.results[namespace_key]['property_usages'])
                type_count = len(self.results[namespace_key]['type_usages'])
                
                if ctx_count > 0 or prop_count > 0 or type_count > 0:
                    f.write(f"| `{namespace_key}` | {ctx_count} | {prop_count} | {type_count} |\n")
            
            f.write("\n---\n\n")
            
            # Detailed breakdown
            f.write("## Detailed Breakdown\n\n")
            
            for ext in M1_EXTENSIONS:
                namespace_key = f"m1:{ext}"
                result = self.results[namespace_key]
                
                if not any(result.values()):
                    continue  # Skip unused namespaces
                
                f.write(f"### `{namespace_key}`\n\n")
                
                # Context definitions
                if result['context_definitions']:
                    f.write(f"**Defined in @context ({len(result['context_definitions'])} files):**\n")
                    for filepath in sorted(set(result['context_definitions'])):
                        f.write(f"- `{filepath}`\n")
                    f.write("\n")
                
                # Property usages
                if result['property_usages']:
                    f.write(f"**Used as properties ({len(result['property_usages'])} files):**\n")
                    for entry in result['property_usages']:
                        f.write(f"- `{entry['file']}`\n")
                        for usage in sorted(entry['usages']):
                            f.write(f"  - `{namespace_key}:{usage}`\n")
                    f.write("\n")
                
                # Type usages
                if result['type_usages']:
                    f.write(f"**Used as types ({len(result['type_usages'])} files):**\n")
                    for entry in result['type_usages']:
                        f.write(f"- `{entry['file']}`\n")
                        for usage in sorted(entry['usages']):
                            f.write(f"  - `{namespace_key}:{usage}`\n")
                    f.write("\n")
                
                f.write("---\n\n")
            
            # Migration recommendations
            f.write("## Migration Plan\n\n")
            f.write("### Phase 1: Update @context Definitions\n\n")
            f.write("For each file that defines M1 extension namespaces:\n\n")
            f.write("**BEFORE:**\n")
            f.write("```json\n")
            f.write('{\n')
            f.write('  "@context": {\n')
            f.write('    "m1:core": "https://.../M1_CoreConcepts.jsonld#",\n')
            f.write('    "m1:biology": "https://.../M1_extensions/biology/M1_Biology.jsonld#"\n')
            f.write('  }\n')
            f.write('}\n')
            f.write("```\n\n")
            f.write("**AFTER:**\n")
            f.write("```json\n")
            f.write('{\n')
            f.write('  "@context": {\n')
            f.write('    "m1": "https://.../M1_CoreConcepts.jsonld#",\n')
            f.write('    "m1.ext:biology": "https://.../M1_extensions/biology/M1_Biology.jsonld#"\n')
            f.write('  }\n')
            f.write('}\n')
            f.write("```\n\n")
            
            f.write("### Phase 2: Update Property/Type References\n\n")
            
            total_files_to_migrate = set()
            for ext in M1_EXTENSIONS:
                if ext == "core":
                    continue  # m1:core gets removed, not renamed
                namespace_key = f"m1:{ext}"
                for entry in self.results[namespace_key]['property_usages']:
                    total_files_to_migrate.add(entry['file'])
                for entry in self.results[namespace_key]['type_usages']:
                    total_files_to_migrate.add(entry['file'])
            
            f.write(f"**Files requiring property/type updates:** {len(total_files_to_migrate)}\n\n")
            
            f.write("**Pattern replacements:**\n")
            for ext in M1_EXTENSIONS:
                if ext == "core":
                    f.write(f"- `m1:core:` → `m1:` (remove redundant namespace)\n")
                else:
                    f.write(f"- `m1:{ext}:` → `m1.ext:{ext}:`\n")
            
            f.write("\n### Phase 3: Validation\n\n")
            f.write("1. Run SHACL validation on all migrated files\n")
            f.write("2. Test HTML simulations\n")
            f.write("3. Verify JSON-LD parsing\n")
        
        print(f"📄 Audit report generated: {output_path}")
        return output_path
    
    def print_summary(self):
        """Print console summary."""
        print("="*70)
        print("AUDIT SUMMARY")
        print("="*70)
        
        for ext in M1_EXTENSIONS:
            namespace_key = f"m1:{ext}"
            result = self.results[namespace_key]
            
            ctx_count = len(result['context_definitions'])
            prop_count = len(result['property_usages'])
            type_count = len(result['type_usages'])
            
            if ctx_count > 0 or prop_count > 0 or type_count > 0:
                print(f"\n📦 {namespace_key}")
                print(f"   Context definitions: {ctx_count}")
                print(f"   Property usages: {prop_count}")
                print(f"   Type usages: {type_count}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution flow."""
    auditor = M1NamespaceAuditor()
    
    # Run audit
    auditor.audit_corpus()
    
    # Print summary
    auditor.print_summary()
    
    # Generate report
    report_path = REPO_ROOT / "ontology" / "TSCG_Grammar" / "M1_NAMESPACE_AUDIT_REPORT.md"
    auditor.generate_report(report_path)
    
    print("\n" + "="*70)
    print("✅ AUDIT COMPLETE")
    print("="*70)
    print(f"\n📄 Full report: {report_path.relative_to(REPO_ROOT)}")
    print("\n🧪 NEXT STEPS:")
    print("1. Review the audit report")
    print("2. Create migration script for Phase 1 (@context updates)")
    print("3. Create migration script for Phase 2 (property/type updates)")
    print("4. Validate with SHACL after migration")

if __name__ == "__main__":
    main()
