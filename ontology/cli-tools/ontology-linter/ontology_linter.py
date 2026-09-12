#!/usr/bin/env python3
"""
TSCG Ontology Linter
====================
Validates JSON-LD ontology files for syntax, semantics, and consistency.

Usage:
    python ontology_linter.py <file_or_directory> [options]
    
Options:
    --strict        Fail on warnings (default: errors only)
    --format json   Output format: text (default) or json
    --fix-imports   Attempt to resolve import paths
    
Examples:
    python ontology_linter.py M2_GenericConcepts.jsonld
    python ontology_linter.py ontology/ --strict
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict

try:
    from rdflib import Graph, URIRef, Namespace
    from rdflib.namespace import RDF, RDFS, OWL
except ImportError:
    print("❌ Error: rdflib not installed")
    print("Install with: pip install rdflib --break-system-packages")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class OntologyLinter:
    """Lints JSON-LD ontology files for TSCG"""
    
    def __init__(self, strict=False):
        self.strict = strict
        self.errors = []
        self.warnings = []
        self.info = []
        self.stats = defaultdict(int)
        
    def lint_file(self, filepath: Path) -> Dict:
        """Lint a single ontology file"""
        self.errors = []
        self.warnings = []
        self.info = []
        self.stats = defaultdict(int)
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}Linting: {filepath.name}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        # 1. JSON Syntax Check
        print(f"{Colors.CYAN}[1/7] JSON Syntax...{Colors.RESET}")
        data = self._check_json_syntax(filepath)
        if not data:
            return self._build_report(filepath)
        
        # 2. JSON-LD Structure
        print(f"{Colors.CYAN}[2/7] JSON-LD Structure...{Colors.RESET}")
        self._check_jsonld_structure(data, filepath)
        
        # 3. RDF Parsing
        print(f"{Colors.CYAN}[3/7] RDF Parsing...{Colors.RESET}")
        graph = self._check_rdf_parsing(filepath)
        if not graph:
            return self._build_report(filepath)
        
        # 4. OWL Semantics
        print(f"{Colors.CYAN}[4/7] OWL Semantics...{Colors.RESET}")
        self._check_owl_semantics(graph, data)
        
        # 5. TSCG Conventions
        print(f"{Colors.CYAN}[5/7] TSCG Conventions...{Colors.RESET}")
        self._check_tscg_conventions(data, filepath)
        
        # 6. Import Resolution
        print(f"{Colors.CYAN}[6/7] Import Resolution...{Colors.RESET}")
        self._check_imports(data, filepath)
        
        # 7. Namespace Consistency
        print(f"{Colors.CYAN}[7/7] Namespace Consistency...{Colors.RESET}")
        self._check_namespaces(data)
        
        return self._build_report(filepath)
    
    def _check_json_syntax(self, filepath: Path) -> Dict:
        """Check if file is valid JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.info.append("✓ Valid JSON syntax")
            return data
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON syntax: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Cannot read file: {e}")
            return None
    
    def _check_jsonld_structure(self, data: Dict, filepath: Path):
        """Check JSON-LD required structure"""
        # Check @context
        if '@context' not in data:
            self.errors.append("Missing @context")
        else:
            self.info.append("✓ @context present")
            
            # Check @base placement
            if '@base' in data['@context']:
                self.info.append("✓ @base in @context (correct)")
            elif '@base' in data:
                self.warnings.append("@base at root level (should be in @context)")
        
        # Check @graph
        if '@graph' not in data:
            self.errors.append("Missing @graph")
        else:
            self.stats['graph_items'] = len(data['@graph'])
            self.info.append(f"✓ @graph with {self.stats['graph_items']} items")
        
        # Check ontology metadata
        has_ontology = False
        for item in data.get('@graph', []):
            if item.get('@type') in ['owl:Ontology', 'Ontology']:
                has_ontology = True
                
                # Check version
                if 'owl:versionInfo' not in item and 'versionInfo' not in item:
                    self.warnings.append("Ontology missing version info")
                
                break
        
        if not has_ontology:
            self.warnings.append("No owl:Ontology declaration found")
    
    def _check_rdf_parsing(self, filepath: Path) -> Graph:
        """Parse as RDF graph"""
        try:
            g = Graph()
            g.parse(str(filepath), format='json-ld')
            self.stats['triples'] = len(g)
            self.info.append(f"✓ Parsed as RDF: {self.stats['triples']} triples")
            return g
        except Exception as e:
            self.errors.append(f"RDF parsing failed: {e}")
            return None
    
    def _check_owl_semantics(self, graph: Graph, data: Dict):
        """Check OWL semantic validity"""
        # Count ontology elements
        classes = set(graph.subjects(RDF.type, OWL.Class))
        properties = set(graph.subjects(RDF.type, OWL.ObjectProperty)) | \
                     set(graph.subjects(RDF.type, OWL.DatatypeProperty))
        
        self.stats['classes'] = len(classes)
        self.stats['properties'] = len(properties)
        
        self.info.append(f"✓ OWL Classes: {self.stats['classes']}")
        self.info.append(f"✓ OWL Properties: {self.stats['properties']}")
        
        # Check for undefined references
        defined_terms = classes | properties
        
        # Check domain/range references
        for prop in properties:
            for domain in graph.objects(prop, RDFS.domain):
                if domain not in defined_terms and not str(domain).startswith('http://www.w3.org'):
                    self.warnings.append(f"Property {self._short_uri(prop)} has undefined domain: {self._short_uri(domain)}")
            
            for range_val in graph.objects(prop, RDFS.range):
                if range_val not in defined_terms and not str(range_val).startswith(('http://www.w3.org', 'xsd:')):
                    self.warnings.append(f"Property {self._short_uri(prop)} has undefined range: {self._short_uri(range_val)}")
    
    def _check_tscg_conventions(self, data: Dict, filepath: Path):
        """Check TSCG-specific conventions"""
        filename = filepath.name
        
        # Check naming convention
        if not (filename.startswith('M0_') or filename.startswith('M1_') or 
                filename.startswith('M2_') or filename.startswith('M3_')):
            self.warnings.append(f"Filename doesn't follow TSCG naming (M0_/M1_/M2_/M3_): {filename}")
        
        # Check for legacy "tensor" terminology
        json_str = json.dumps(data)
        if 'tensor' in json_str.lower():
            tensor_count = json_str.lower().count('tensor')
            self.warnings.append(f"Found {tensor_count} occurrences of 'tensor' (should use 'monoidal product' or 'structural grammar')")
        
        # Check for ambiguous "I" in formulas (M2 specific)
        if filename.startswith('M2_'):
            # Look for bare I (not It or Im)
            import re
            for item in data.get('@graph', []):
                for key, value in item.items():
                    if 'formula' in key.lower() and isinstance(value, str):
                        if re.search(r'\bI\b(?!t|m)', value):
                            self.warnings.append(f"Ambiguous 'I' in formula (use It or Im): {value}")
        
        # Check @base suffix
        if '@context' in data and '@base' in data['@context']:
            base = data['@context']['@base']
            if '/ontology/' in base:
                self.warnings.append("@base has /ontology/ suffix (should be: .../main/)")
    
    def _check_imports(self, data: Dict, filepath: Path):
        """Check owl:imports resolution"""
        imports = []
        
        for item in data.get('@graph', []):
            if 'owl:imports' in item:
                imports_val = item['owl:imports']
                if isinstance(imports_val, str):
                    imports = [imports_val]
                elif isinstance(imports_val, list):
                    imports = imports_val
        
        if imports:
            self.info.append(f"✓ Imports declared: {len(imports)}")
            
            # Check if imports exist
            for imp in imports:
                imp_path = filepath.parent / imp
                if not imp_path.exists():
                    self.warnings.append(f"Import not found: {imp}")
                else:
                    self.info.append(f"  ✓ {imp}")
        else:
            self.info.append("No imports declared")
    
    def _check_namespaces(self, data: Dict):
        """Check namespace consistency"""
        if '@context' not in data:
            return
        
        context = data['@context']
        namespaces = {k: v for k, v in context.items() 
                     if isinstance(v, str) and (v.startswith('http') or v.endswith('.jsonld#'))}
        
        self.stats['namespaces'] = len(namespaces)
        self.info.append(f"✓ Namespaces defined: {self.stats['namespaces']}")
        
        # Check for common issues
        for prefix, uri in namespaces.items():
            if prefix in ['@base', '@vocab']:
                continue
            
            # Check if namespace URI ends properly
            if not (uri.endswith('#') or uri.endswith('/')):
                self.warnings.append(f"Namespace '{prefix}' doesn't end with # or /: {uri}")
    
    def _short_uri(self, uri) -> str:
        """Shorten URI for display"""
        uri_str = str(uri)
        if '#' in uri_str:
            return uri_str.split('#')[-1]
        return uri_str.split('/')[-1]
    
    def _build_report(self, filepath: Path) -> Dict:
        """Build final report"""
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}REPORT: {filepath.name}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        # Errors
        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}❌ ERRORS ({len(self.errors)}):{Colors.RESET}")
            for err in self.errors:
                print(f"{Colors.RED}   • {err}{Colors.RESET}")
            print()
        
        # Warnings
        if self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  WARNINGS ({len(self.warnings)}):{Colors.RESET}")
            for warn in self.warnings:
                print(f"{Colors.YELLOW}   • {warn}{Colors.RESET}")
            print()
        
        # Info (only if verbose or no errors/warnings)
        if not self.errors and not self.warnings:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ INFO:{Colors.RESET}")
            for info in self.info:
                print(f"{Colors.GREEN}   {info}{Colors.RESET}")
            print()
        
        # Stats
        if self.stats:
            print(f"{Colors.CYAN}{Colors.BOLD}📊 STATISTICS:{Colors.RESET}")
            for key, value in self.stats.items():
                print(f"{Colors.CYAN}   {key}: {value}{Colors.RESET}")
            print()
        
        # Verdict
        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}❌ FAILED{Colors.RESET}\n")
            status = 'FAILED'
        elif self.warnings and self.strict:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  FAILED (strict mode){Colors.RESET}\n")
            status = 'FAILED'
        elif self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  PASSED WITH WARNINGS{Colors.RESET}\n")
            status = 'WARNING'
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ PASSED{Colors.RESET}\n")
            status = 'PASSED'
        
        return {
            'file': str(filepath),
            'status': status,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'stats': dict(self.stats)
        }


def generate_markdown_report(reports: List[Dict], output_path: Path):
    """Generate markdown report"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# TSCG Ontology Lint Report\n\n")
        f.write(f"**Generated:** {Path.cwd()}\n\n")
        
        # Summary
        passed = sum(1 for r in reports if r['status'] == 'PASSED')
        warnings = sum(1 for r in reports if r['status'] == 'WARNING')
        failed = sum(1 for r in reports if r['status'] == 'FAILED')
        
        f.write("## Summary\n\n")
        f.write(f"- ✅ **Passed:** {passed}\n")
        f.write(f"- ⚠️  **Warnings:** {warnings}\n")
        f.write(f"- ❌ **Failed:** {failed}\n")
        f.write(f"- 📁 **Total files:** {len(reports)}\n\n")
        
        # Per file
        f.write("## Files\n\n")
        for report in reports:
            filename = Path(report['file']).name
            status_icon = {'PASSED': '✅', 'WARNING': '⚠️', 'FAILED': '❌'}
            
            f.write(f"### {status_icon.get(report['status'], '❓')} {filename}\n\n")
            
            if report['errors']:
                f.write("**Errors:**\n")
                for err in report['errors']:
                    f.write(f"- ❌ {err}\n")
                f.write("\n")
            
            if report['warnings']:
                f.write("**Warnings:**\n")
                for warn in report['warnings'][:10]:  # Limit to 10
                    f.write(f"- ⚠️  {warn}\n")
                if len(report['warnings']) > 10:
                    f.write(f"- ... and {len(report['warnings']) - 10} more\n")
                f.write("\n")
            
            if report['stats']:
                f.write("**Statistics:**\n")
                for key, value in report['stats'].items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n")
    
    print(f"{Colors.GREEN}✅ Markdown report: {output_path}{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description='TSCG Ontology Linter - Validate JSON-LD ontology files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('path', help='File or directory to lint')
    parser.add_argument('--strict', action='store_true', 
                       help='Fail on warnings (default: errors only)')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text',
                       help='Output format (text, json, or markdown report)')
    parser.add_argument('--layer', choices=['M0', 'M1', 'M2', 'M3'], 
                       help='Lint only specific layer (M0, M1, M2, or M3)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be checked without running full analysis')
    parser.add_argument('--output', type=str,
                       help='Output file for markdown/json report')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"{Colors.RED}❌ Error: Path not found: {path}{Colors.RESET}")
        sys.exit(1)
    
    # Collect files
    if path.is_file():
        files = [path]
    else:
        files = sorted(path.glob('*.jsonld'))
    
    # Filter by layer
    if args.layer:
        files = [f for f in files if f.name.startswith(f'{args.layer}_')]
        print(f"{Colors.CYAN}🔍 Filtering layer: {args.layer}{Colors.RESET}")
    
    if not files:
        print(f"{Colors.RED}❌ No .jsonld files found{Colors.RESET}")
        sys.exit(1)
    
    # Dry run
    if args.dry_run:
        print(f"{Colors.CYAN}{Colors.BOLD}DRY RUN MODE{Colors.RESET}")
        print(f"{Colors.CYAN}Would lint {len(files)} file(s):{Colors.RESET}\n")
        for f in files:
            print(f"  • {f.name}")
        print(f"\n{Colors.CYAN}Run without --dry-run to execute{Colors.RESET}")
        sys.exit(0)
    
    linter = OntologyLinter(strict=args.strict)
    
    # Lint all files
    reports = []
    for filepath in files:
        report = linter.lint_file(filepath)
        reports.append(report)
    
    # Summary
    if len(files) > 1:
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}SUMMARY ({len(files)} files){Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        passed = sum(1 for r in reports if r['status'] == 'PASSED')
        warnings = sum(1 for r in reports if r['status'] == 'WARNING')
        failed = sum(1 for r in reports if r['status'] == 'FAILED')
        
        print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠️  Warnings: {warnings}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed: {failed}{Colors.RESET}\n")
    
    # Output formats
    if args.format == 'json':
        output_data = json.dumps(reports, indent=2)
        if args.output:
            Path(args.output).write_text(output_data)
            print(f"{Colors.GREEN}✅ JSON report: {args.output}{Colors.RESET}")
        else:
            print(output_data)
    
    elif args.format == 'markdown':
        output_path = Path(args.output) if args.output else Path('lint_report.md')
        generate_markdown_report(reports, output_path)
    
    # Exit code
    if any(r['status'] == 'FAILED' for r in reports):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
