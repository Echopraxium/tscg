#!/usr/bin/env python3
"""
TSCG Ontology Validator
Validates namespaces, IRIs, and identifiers in JSON-LD ontology files

Author: Echopraxium with the collaboration of Claude AI
Version: 1.0.0
Date: 2026-01-25
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse
from collections import defaultdict


class TSCGOntologyValidator:
    """Validator for TSCG JSON-LD ontology files"""
    
    # Valid TSCG namespace patterns
    VALID_NAMESPACE_PATTERNS = {
        'w3c': r'^(rdf|rdfs|owl|xsd|dcterms|skos)$',
        'm3': r'^m3(:(genesis|eagle_eye|sphinx_eye))?$',
        'm2': r'^m2$',
        'm1': r'^m1:(core|biology|chemistry|mythology|optics|photography|education|[a-z_]+)$',
        'm0': r'^m0:[a-z_]+$'
    }
    
    # Expected URI base
    EXPECTED_URI_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology"
    
    # Required W3C namespaces in @context
    REQUIRED_W3C = {'dcterms', 'owl', 'rdf', 'rdfs', 'xsd'}
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = None
        self.errors = []
        self.warnings = []
        self.context_namespaces = {}
        self.used_prefixes = set()
        self.defined_ids = set()
        self.referenced_ids = set()
        
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Main validation entry point
        Returns: (is_valid, errors, warnings)
        """
        print(f"\n{'='*80}")
        print(f"🔍 Validating: {self.filepath.name}")
        print(f"{'='*80}\n")
        
        # Load JSON
        if not self._load_json():
            return False, self.errors, self.warnings
        
        # Run all validations
        self._validate_structure()
        self._validate_context()
        self._validate_namespace_order()
        self._validate_namespace_format()
        self._validate_uris()
        self._validate_imports()
        self._validate_graph()
        self._validate_prefix_usage()
        self._validate_id_references()
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _load_json(self) -> bool:
        """Load and parse JSON file"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"❌ Invalid JSON: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"❌ File not found: {self.filepath}")
            return False
        except Exception as e:
            self.errors.append(f"❌ Error loading file: {e}")
            return False
    
    def _validate_structure(self):
        """Validate basic JSON-LD structure"""
        if '@context' not in self.data:
            self.errors.append("❌ Missing @context")
        
        if '@graph' not in self.data and '@id' not in self.data:
            self.errors.append("❌ Missing both @graph and @id (need at least one)")
    
    def _validate_context(self):
        """Validate @context structure"""
        if '@context' not in self.data:
            return
        
        context = self.data['@context']
        if not isinstance(context, dict):
            self.errors.append("❌ @context must be a JSON object")
            return
        
        # Extract namespaces (ignore _comment fields)
        for key, value in context.items():
            if not key.startswith('_comment'):
                if isinstance(value, str):
                    self.context_namespaces[key] = value
        
        # Check for required W3C namespaces
        defined_w3c = set(self.context_namespaces.keys()) & self.REQUIRED_W3C
        missing_w3c = self.REQUIRED_W3C - defined_w3c
        
        if missing_w3c:
            self.errors.append(f"❌ Missing required W3C namespaces: {', '.join(sorted(missing_w3c))}")
    
    def _validate_namespace_order(self):
        """Validate namespace ordering in @context"""
        if '@context' not in self.data:
            return
        
        context = self.data['@context']
        keys = [k for k in context.keys() if not k.startswith('_comment')]
        
        # Categorize keys
        w3c_keys = []
        tscg_keys = []
        
        for key in keys:
            if key in self.REQUIRED_W3C or key == 'skos':
                w3c_keys.append(key)
            elif key.startswith('m'):
                tscg_keys.append(key)
        
        # Check W3C alphabetical order
        sorted_w3c = sorted(w3c_keys)
        if w3c_keys != sorted_w3c:
            self.warnings.append(f"⚠️  W3C namespaces not alphabetical: {w3c_keys} (expected: {sorted_w3c})")
        
        # Check TSCG hierarchical order (m3 before m2 before m1 before m0)
        if not self._is_tscg_hierarchical(tscg_keys):
            self.warnings.append(f"⚠️  TSCG namespaces not hierarchical (M3→M2→M1→M0): {tscg_keys}")
    
    def _is_tscg_hierarchical(self, keys: List[str]) -> bool:
        """Check if TSCG keys follow M3→M2→M1→M0 order"""
        m3_keys = [k for k in keys if k.startswith('m3')]
        m2_keys = [k for k in keys if k.startswith('m2')]
        m1_keys = [k for k in keys if k.startswith('m1')]
        m0_keys = [k for k in keys if k.startswith('m0')]
        
        expected = m3_keys + m2_keys + m1_keys + m0_keys
        return keys == expected
    
    def _validate_namespace_format(self):
        """Validate namespace format against TSCG patterns"""
        for prefix in self.context_namespaces.keys():
            # Skip W3C namespaces
            if prefix in self.REQUIRED_W3C or prefix == 'skos':
                continue
            
            # Check for invalid separators
            if '.' in prefix:
                self.errors.append(f"❌ Invalid namespace '{prefix}': contains POINT (.) - must use COLON (:)")
                continue
            
            if '-' in prefix and not prefix.startswith('m'):
                self.errors.append(f"❌ Invalid namespace '{prefix}': contains HYPHEN (-)")
                continue
            
            # Validate against TSCG patterns
            valid = False
            for pattern_type, pattern in self.VALID_NAMESPACE_PATTERNS.items():
                if re.match(pattern, prefix):
                    valid = True
                    break
            
            if not valid:
                self.errors.append(f"❌ Invalid namespace format '{prefix}': doesn't match TSCG patterns")
    
    def _validate_uris(self):
        """Validate URI formats"""
        for prefix, uri in self.context_namespaces.items():
            # Skip W3C namespaces
            if prefix in self.REQUIRED_W3C or prefix == 'skos':
                continue
            
            # Check URI structure
            if not uri.startswith('http://') and not uri.startswith('https://'):
                self.errors.append(f"❌ Invalid URI for '{prefix}': must start with http:// or https://")
                continue
            
            # Check for TSCG base URI
            if prefix.startswith('m') and self.EXPECTED_URI_BASE not in uri:
                self.warnings.append(f"⚠️  URI for '{prefix}' doesn't contain expected base: {self.EXPECTED_URI_BASE}")
            
            # Check for wrong GitHub domain
            if 'github.com' in uri and 'raw.githubusercontent.com' not in uri:
                self.errors.append(f"❌ URI for '{prefix}' uses github.com instead of raw.githubusercontent.com")
            
            # Check URI ends with #
            if not uri.endswith('#'):
                self.warnings.append(f"⚠️  URI for '{prefix}' doesn't end with # (fragment identifier)")
            
            # Validate path structure for TSCG namespaces
            if prefix.startswith('m3'):
                if '/M3_' not in uri:
                    self.errors.append(f"❌ M3 URI for '{prefix}' should contain /M3_...")
            elif prefix.startswith('m2'):
                if '/M2_' not in uri:
                    self.errors.append(f"❌ M2 URI for '{prefix}' should contain /M2_...")
            elif prefix.startswith('m1'):
                if prefix == 'm1:core':
                    if '/M1_CoreConcepts.jsonld' not in uri:
                        self.errors.append(f"❌ m1:core should reference M1_CoreConcepts.jsonld")
                else:
                    if '/M1_extensions/' not in uri:
                        self.errors.append(f"❌ M1 extension '{prefix}' should be in /M1_extensions/")
            elif prefix.startswith('m0'):
                if '/poclets/' not in uri:
                    self.errors.append(f"❌ M0 URI for '{prefix}' should contain /poclets/")
    
    def _validate_imports(self):
        """Validate owl:imports"""
        graph = self._get_graph()
        if not graph:
            return
        
        # Find ontology node
        ontology_node = None
        for item in graph:
            if isinstance(item, dict) and item.get('@type') == 'owl:Ontology':
                ontology_node = item
                break
        
        if not ontology_node:
            self.warnings.append("⚠️  No owl:Ontology node found")
            return
        
        imports = ontology_node.get('owl:imports', [])
        if not isinstance(imports, list):
            imports = [imports]
        
        for import_uri in imports:
            # Check URI format
            if not import_uri.startswith('https://'):
                self.errors.append(f"❌ Invalid import URI: {import_uri}")
                continue
            
            # Check for wrong GitHub domain
            if 'github.com' in import_uri and 'raw.githubusercontent.com' not in import_uri:
                self.errors.append(f"❌ Import URI uses github.com instead of raw.githubusercontent.com: {import_uri}")
            
            # Check file extension
            if not import_uri.endswith('.jsonld'):
                self.errors.append(f"❌ Import URI should end with .jsonld: {import_uri}")
    
    def _validate_graph(self):
        """Validate @graph structure and collect IDs"""
        graph = self._get_graph()
        if not graph:
            return
        
        if not isinstance(graph, list):
            self.errors.append("❌ @graph must be an array")
            return
        
        # Collect all defined IDs
        self._collect_ids(graph)
    
    def _get_graph(self):
        """Get @graph or create single-item list from @id"""
        if '@graph' in self.data:
            return self.data['@graph']
        elif '@id' in self.data:
            return [self.data]
        return None
    
    def _collect_ids(self, obj, path=""):
        """Recursively collect all @id and referenced IDs"""
        if isinstance(obj, dict):
            # Collect defined ID
            if '@id' in obj:
                id_val = obj['@id']
                self.defined_ids.add(id_val)
                
                # Extract prefix used
                if ':' in id_val:
                    prefix = id_val.split(':')[0]
                    self.used_prefixes.add(prefix)
            
            # Collect references in property values
            for key, value in obj.items():
                if key == '@id':
                    continue
                
                # Check if value is a reference (compact IRI)
                if isinstance(value, str) and ':' in value and not value.startswith('http'):
                    self.referenced_ids.add(value)
                    prefix = value.split(':')[0]
                    self.used_prefixes.add(prefix)
                
                # Recurse
                self._collect_ids(value, f"{path}.{key}")
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._collect_ids(item, f"{path}[{i}]")
    
    def _validate_prefix_usage(self):
        """Validate that all used prefixes are declared"""
        undefined_prefixes = self.used_prefixes - set(self.context_namespaces.keys())
        
        for prefix in undefined_prefixes:
            self.errors.append(f"❌ Prefix '{prefix}' used but not defined in @context")
        
        # Warn about unused declarations
        declared_prefixes = set(self.context_namespaces.keys()) - self.REQUIRED_W3C - {'skos'}
        unused_prefixes = declared_prefixes - self.used_prefixes
        
        for prefix in unused_prefixes:
            self.warnings.append(f"⚠️  Prefix '{prefix}' declared but never used")
    
    def _validate_id_references(self):
        """Validate that referenced IDs could be resolved"""
        # Note: We can't fully validate cross-file references without loading all files
        # But we can check for obvious errors
        
        for ref_id in self.referenced_ids:
            # Check format
            if not ':' in ref_id:
                continue
            
            prefix = ref_id.split(':')[0]
            
            # Check if prefix is defined
            if prefix not in self.context_namespaces:
                self.errors.append(f"❌ Reference '{ref_id}' uses undefined prefix '{prefix}'")
            
            # Check for invalid characters in local part
            local_part = ':'.join(ref_id.split(':')[1:])
            if ' ' in local_part:
                self.errors.append(f"❌ Invalid ID '{ref_id}': contains spaces in local part")
    
    def print_report(self):
        """Print validation report"""
        print(f"\n{'='*80}")
        print(f"📊 VALIDATION REPORT - {self.filepath.name}")
        print(f"{'='*80}\n")
        
        # Summary
        total_issues = len(self.errors) + len(self.warnings)
        
        if total_issues == 0:
            print("✅ VALIDATION PASSED - No issues found!\n")
        else:
            print(f"Issues found: {len(self.errors)} errors, {len(self.warnings)} warnings\n")
        
        # Errors
        if self.errors:
            print(f"{'─'*80}")
            print("❌ ERRORS (must fix)")
            print(f"{'─'*80}")
            for i, error in enumerate(self.errors, 1):
                print(f"{i:2}. {error}")
            print()
        
        # Warnings
        if self.warnings:
            print(f"{'─'*80}")
            print("⚠️  WARNINGS (should fix)")
            print(f"{'─'*80}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i:2}. {warning}")
            print()
        
        # Statistics
        print(f"{'─'*80}")
        print("📈 STATISTICS")
        print(f"{'─'*80}")
        print(f"Namespaces defined: {len(self.context_namespaces)}")
        print(f"Prefixes used: {len(self.used_prefixes)}")
        print(f"IDs defined: {len(self.defined_ids)}")
        print(f"IDs referenced: {len(self.referenced_ids)}")
        print()


def validate_file(filepath: str) -> bool:
    """Validate a single file and return success status"""
    validator = TSCGOntologyValidator(filepath)
    is_valid, errors, warnings = validator.validate()
    validator.print_report()
    return is_valid


def validate_directory(dirpath: str, pattern: str = "*.jsonld") -> Tuple[int, int]:
    """
    Validate all JSON-LD files in a directory
    Returns: (passed_count, failed_count)
    """
    directory = Path(dirpath)
    files = list(directory.glob(pattern))
    
    if not files:
        print(f"❌ No files matching '{pattern}' found in {dirpath}")
        return 0, 0
    
    print(f"\n{'='*80}")
    print(f"🔍 BATCH VALIDATION - {len(files)} files in {dirpath}")
    print(f"{'='*80}")
    
    passed = 0
    failed = 0
    
    for filepath in sorted(files):
        is_valid = validate_file(str(filepath))
        if is_valid:
            passed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 BATCH SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Passed: {passed}/{len(files)}")
    print(f"❌ Failed: {failed}/{len(files)}")
    print(f"{'='*80}\n")
    
    return passed, failed


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TSCG Ontology Validator - Validates namespaces, IRIs, and identifiers in JSON-LD files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single file
  python tscg_ontology_validator.py M0_TPACK.jsonld
  
  # Validate all files in directory
  python tscg_ontology_validator.py --dir ./ontology
  
  # Validate specific pattern
  python tscg_ontology_validator.py --dir ./ontology --pattern "M1_*.jsonld"
        """
    )
    
    parser.add_argument('file', nargs='?', help='JSON-LD file to validate')
    parser.add_argument('--dir', '-d', help='Directory containing JSON-LD files')
    parser.add_argument('--pattern', '-p', default='*.jsonld', help='File pattern (default: *.jsonld)')
    
    args = parser.parse_args()
    
    if args.dir:
        passed, failed = validate_directory(args.dir, args.pattern)
        sys.exit(0 if failed == 0 else 1)
    elif args.file:
        is_valid = validate_file(args.file)
        sys.exit(0 if is_valid else 1)
    else:
        parser.print_help()
        sys.exit(1)
