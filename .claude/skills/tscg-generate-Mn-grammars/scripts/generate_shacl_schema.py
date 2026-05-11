#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TSCG Generate SHACL Schema Script
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-05-11
Version: 1.0.0

Generates SHACL validation schemas for TSCG meta-levels M1, M2, and M3.
Interactive script that prompts for the target level and generates comprehensive
SHACL constraints with absolute URLs, forbidden patterns, and validation messages.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import Counter

# Base URL for TSCG ontologies
BASE_URL = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}\n")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def select_level() -> int:
    """
    Interactive level selection (M1, M2, or M3).
    Returns the selected level as integer (1, 2, or 3).
    """
    print_header("TSCG SHACL Schema Generator")
    
    print("Pour quel niveau méta voulez-vous générer la grammaire SHACL ?\n")
    print(f"{Colors.BOLD}1{Colors.END} - M1 (CoreConcepts & Extensions - Domaine)")
    print(f"{Colors.BOLD}2{Colors.END} - M2 (GenericConcepts - Transdisciplinaire)")
    print(f"{Colors.BOLD}3{Colors.END} - M3 (GenesisSpace - Méta-Ontologie)")
    
    while True:
        choice = input(f"\n{Colors.CYAN}Votre choix (1-3): {Colors.END}").strip()
        if choice in ['1', '2', '3']:
            return int(choice)
        print_error("Choix invalide. Veuillez entrer 1, 2 ou 3.")


def select_m1_target() -> Tuple[str, str]:
    """
    If M1 is selected, ask if user wants CoreConcepts or a specific extension.
    Returns (filename, description) tuple.
    """
    print("\nVoulez-vous générer la grammaire pour :\n")
    print(f"{Colors.BOLD}1{Colors.END} - M1_CoreConcepts (base)")
    print(f"{Colors.BOLD}2{Colors.END} - Extension spécifique (Biology, Physics, Chemistry, etc.)")
    
    while True:
        choice = input(f"\n{Colors.CYAN}Votre choix (1-2): {Colors.END}").strip()
        if choice == '1':
            return ("M1_CoreConcepts.jsonld", "M1 CoreConcepts")
        elif choice == '2':
            extension = input(f"{Colors.CYAN}Nom de l'extension (ex: Biology, Physics): {Colors.END}").strip()
            if extension:
                filename = f"M1_{extension}.jsonld"
                return (filename, f"M1 {extension}")
            print_error("Nom d'extension invalide.")
        else:
            print_error("Choix invalide. Veuillez entrer 1 ou 2.")


def load_ontology(filepath: str) -> Dict:
    """
    Load and parse a JSON-LD ontology file.
    Returns the parsed JSON structure.
    """
    print_info(f"Lecture de l'ontologie : {filepath}")
    
    if not os.path.exists(filepath):
        print_error(f"Fichier non trouvé : {filepath}")
        sys.exit(1)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print_success(f"Ontologie chargée avec succès")
        return data
    except json.JSONDecodeError as e:
        print_error(f"Erreur de parsing JSON : {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erreur lors de la lecture : {e}")
        sys.exit(1)


def analyze_properties(data: Dict) -> Dict[str, any]:
    """
    Analyze the ontology structure and catalog all properties.
    Returns a dictionary with property statistics and patterns.
    """
    print_info("Analyse de la structure de l'ontologie...")
    
    stats = {
        'total_nodes': 0,
        'properties': Counter(),
        'types': Counter(),
        'namespaces': set(),
        'required_properties': set(),
        'optional_properties': set(),
        'datatypes': Counter()
    }
    
    graph = data.get('@graph', [])
    if isinstance(graph, dict):
        graph = [graph]
    
    stats['total_nodes'] = len(graph)
    
    for node in graph:
        if not isinstance(node, dict):
            continue
        
        # Catalog node types
        node_type = node.get('@type')
        if node_type:
            if isinstance(node_type, list):
                for t in node_type:
                    stats['types'][t] += 1
            else:
                stats['types'][node_type] += 1
        
        # Catalog properties
        for key, value in node.items():
            if key.startswith('@'):
                continue
            
            stats['properties'][key] += 1
            
            # Extract namespace
            if ':' in key:
                namespace = key.split(':')[0]
                stats['namespaces'].add(namespace)
            
            # Detect datatypes
            if isinstance(value, dict) and '@type' in value:
                stats['datatypes'][value['@type']] += 1
    
    # Determine required vs optional based on frequency
    total_concepts = stats['types'].get('owl:Class', 1)
    for prop, count in stats['properties'].items():
        if count >= total_concepts * 0.9:  # 90% threshold for required
            stats['required_properties'].add(prop)
        else:
            stats['optional_properties'].add(prop)
    
    print_success(f"Analyse terminée : {stats['total_nodes']} nœuds, "
                  f"{len(stats['properties'])} propriétés distinctes")
    
    return stats


def generate_shacl_header(level: int, target_file: str, stats: Dict) -> str:
    """
    Generate SHACL file header with namespace declarations and metadata.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    header = f"""# TSCG M{level} - SHACL Schema v1.0.0
# Author: Echopraxium with the collaboration of Claude AI
# Date: {today}
# Target: {target_file}
# Status: Production
#
# This schema validates the structural and semantic integrity of {target_file}.
# Generated by generate_shacl_schema.py

@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix m0: <{BASE_URL}M0_Poclet#> .
@prefix m1: <{BASE_URL}M1_CoreConcepts.jsonld#> .
@prefix m2: <{BASE_URL}M2_GenericConcepts.jsonld#> .
@prefix m3: <{BASE_URL}M3_GenesisSpace.jsonld#> .

# ============================================
# NAMESPACE POLICY (CRITICAL)
# ============================================
# TSCG uses a strict namespace hierarchy:
# - m3: Meta-ontology (GenesisSpace, EagleEye, SphinxEye)
# - m2: Generic transdisciplinary concepts (GenericConcepts)
# - m1: Domain-specific concepts (CoreConcepts + extensions)
# - m0: Instances (Poclets, SystemicFrameworks, etc.)
#
# The namespace "tscg:" is FORBIDDEN and must never be used.
# Properties must use the appropriate level namespace.

"""
    return header


def generate_m3_constraints() -> str:
    """
    Generate SHACL constraints specific to M3 (GenesisSpace).
    """
    constraints = """
# ============================================
# M3 - GENESISSPACE CONSTRAINTS
# ============================================

# M3 Dimension Shape - Validates ASFID/REVOI dimensions
m3:DimensionShape
    a sh:NodeShape ;
    sh:targetClass owl:ObjectProperty ;
    sh:property [
        sh:path rdfs:label ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "M3 dimensions MUST have exactly one rdfs:label" ;
    ] ;
    sh:property [
        sh:path rdfs:comment ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:message "M3 dimensions MUST have an rdfs:comment explaining their role" ;
    ] .

# Grammar Properties Shape - Validates structural grammar properties
m3:GrammarPropertiesShape
    a sh:NodeShape ;
    sh:targetSubjectsOf m3:grammar_properties ;
    sh:property [
        sh:path m3:hasStructuralGrammarFormula ;
        sh:minCount 0 ;
        sh:message "M3 may optionally have structural grammar formulas" ;
    ] ;
    sh:not [
        sh:property [
            sh:path m2:hasTensorFormula ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:message "FORBIDDEN: hasTensorFormula is obsolete. Use hasStructuralGrammarFormula instead." .

# Ontology Type Shape - Validates m3:ontologyType values
m3:OntologyTypeShape
    a sh:NodeShape ;
    sh:targetSubjectsOf m3:ontologyType ;
    sh:property [
        sh:path m3:ontologyType ;
        sh:in ( 
            m3:Poclet 
            m3:SystemicFramework 
            m3:SymbolicSystemGrammar 
            m3:TransDisclet 
            m3:TscgTool 
            m3:Enigma 
        ) ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "m3:ontologyType MUST be one of: Poclet, SystemicFramework, SymbolicSystemGrammar, TransDisclet, TscgTool, Enigma" ;
    ] .
"""
    return constraints


def generate_m2_constraints() -> str:
    """
    Generate SHACL constraints specific to M2 (GenericConcepts).
    """
    constraints = """
# ============================================
# M2 - GENERICCONCEPTS CONSTRAINTS
# ============================================

# Generic Concept Shape - Validates all GenericConcepts
m2:GenericConceptShape
    a sh:NodeShape ;
    sh:targetClass m2:GenericConcept ;
    sh:property [
        sh:path rdf:type ;
        sh:hasValue owl:Class ;
        sh:minCount 1 ;
        sh:message "GenericConcept MUST be declared as owl:Class" ;
    ] ;
    sh:property [
        sh:path rdfs:label ;
        sh:datatype xsd:string ;
        sh:pattern "^[A-Z][a-zA-Z]*$" ;  # PascalCase
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "GenericConcept MUST have exactly one PascalCase rdfs:label" ;
    ] ;
    sh:property [
        sh:path m2:conceptFamily ;
        sh:in ( 
            m2:Agent m2:Boundary m2:Cycle m2:Flow 
            m2:Gradient m2:Hierarchy m2:Pattern 
            m2:Resonance m2:Transformation 
        ) ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "GenericConcept MUST belong to exactly one of 9 concept families" ;
    ] ;
    sh:property [
        sh:path m2:hasM3Origin ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:message "GenericConcept MUST reference at least one M3 dimension via m2:hasM3Origin" ;
    ] ;
    sh:property [
        sh:path rdfs:comment ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:message "GenericConcept MUST have a transdisciplinary definition in rdfs:comment" ;
    ] .

# Structural Formula Shape - Validates structural grammar formulas
m2:StructuralFormulaShape
    a sh:NodeShape ;
    sh:targetSubjectsOf m2:hasStructuralGrammarFormula ;
    sh:property [
        sh:path m2:hasStructuralGrammarFormula ;
        sh:minCount 0 ;
        sh:message "Optional: hasStructuralGrammarFormula contains Lambek calculus notation" ;
    ] ;
    sh:not [
        sh:property [
            sh:path m2:hasTensorFormula ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:message "FORBIDDEN: hasTensorFormula is obsolete after structural grammar migration." .

# ASFID/REVOI Scores Shape - Validates dimension scores
m2:ScoresShape
    a sh:NodeShape ;
    sh:targetSubjectsOf m2:asfidScores ;
    sh:property [
        sh:path m2:asfidScores ;
        sh:minCount 0 ;  # Optional but recommended
        sh:message "GenericConcept SHOULD have ASFID scores for dimensional analysis" ;
    ] ;
    sh:property [
        sh:path m2:revoiScores ;
        sh:minCount 0 ;  # Optional but recommended
        sh:message "GenericConcept SHOULD have REVOI scores for epistemic quality" ;
    ] .
"""
    return constraints


def generate_m1_constraints() -> str:
    """
    Generate SHACL constraints specific to M1 (CoreConcepts and extensions).
    """
    constraints = """
# ============================================
# M1 - CORECONCEPTS & EXTENSIONS CONSTRAINTS
# ============================================

# Domain Concept Shape - Validates M1 domain-specific concepts
m1:DomainConceptShape
    a sh:NodeShape ;
    sh:targetClass owl:Class ;
    sh:property [
        sh:path rdfs:label ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "M1 concepts MUST have exactly one rdfs:label with domain-specific terminology" ;
    ] ;
    sh:property [
        sh:path m1:domain ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:message "M1 concepts MUST declare their domain" ;
    ] ;
    sh:property [
        sh:path m1:extendsGenericConcept ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:message "M1 concepts SHOULD reference parent M2 GenericConcept via m1:extendsGenericConcept" ;
    ] ;
    sh:property [
        sh:path rdfs:comment ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:message "M1 concepts MUST have a domain-specific definition in rdfs:comment" ;
    ] .

# Domain Reference Integrity - Validates domain declarations
m1:DomainReferenceShape
    a sh:NodeShape ;
    sh:targetSubjectsOf m1:domain ;
    sh:property [
        sh:path m1:domain ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "M1 concepts MUST have exactly one domain declaration" ;
    ] .

# Generic Concept Extension Shape - Validates M2 references
m1:GenericConceptExtensionShape
    a sh:NodeShape ;
    sh:targetSubjectsOf m1:extendsGenericConcept ;
    sh:property [
        sh:path m1:extendsGenericConcept ;
        sh:nodeKind sh:IRI ;
        sh:pattern "^.*M2_GenericConcepts\\.jsonld#.*$" ;
        sh:message "m1:extendsGenericConcept MUST reference a valid M2 GenericConcept IRI" ;
    ] .
"""
    return constraints


def generate_forbidden_patterns(level: int) -> str:
    """
    Generate constraints for forbidden patterns based on level.
    """
    forbidden = f"""
# ============================================
# FORBIDDEN PATTERNS (CRITICAL)
# ============================================

# Forbidden Namespace - tscg: namespace is FORBIDDEN
sh:ForbiddenTscgNamespace
    a sh:NodeShape ;
    sh:targetNode rdf:Property ;
    sh:not [
        sh:property [
            sh:path rdf:type ;
            sh:pattern "^tscg:.*" ;
        ]
    ] ;
    sh:message "CRITICAL VIOLATION: The 'tscg:' namespace is FORBIDDEN. Use m{level}: namespace instead." .

# Forbidden Tensor Properties - After structural grammar migration
sh:ForbiddenTensorProperties
    a sh:NodeShape ;
    sh:targetNode rdf:Property ;
    sh:not [
        sh:property [
            sh:path m2:hasTensorFormula ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:not [
        sh:property [
            sh:path m2:hasTensorFormulaTeX ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:not [
        sh:property [
            sh:path m2:hasTensorFormulaASCII ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:message "FORBIDDEN: Tensor properties are obsolete. Use hasStructuralGrammarFormula instead." .
"""
    
    if level == 3:
        forbidden += """
# Forbidden Hilbert Space References - M3 specific
sh:ForbiddenHilbertReferences
    a sh:NodeShape ;
    sh:targetNode rdf:Property ;
    sh:not [
        sh:property [
            sh:path m3:hilbert_space ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:not [
        sh:property [
            sh:path m3:orthonormality ;
            sh:minCount 1 ;
        ]
    ] ;
    sh:message "FORBIDDEN: Hilbert space and orthonormality references removed after structural grammar migration." .
"""
    
    return forbidden


def generate_statistics_section(stats: Dict, level: int) -> str:
    """
    Generate statistics and changelog section.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    stats_section = f"""
# ============================================
# STATISTICS & CHANGELOG
# ============================================

# Property Coverage Statistics:
# - Total nodes analyzed: {stats['total_nodes']}
# - Distinct properties: {len(stats['properties'])}
# - Required properties: {len(stats['required_properties'])}
# - Optional properties: {len(stats['optional_properties'])}
# - Namespaces detected: {', '.join(sorted(stats['namespaces']))}
# - Most common node type: {stats['types'].most_common(1)[0] if stats['types'] else 'N/A'}
#
# Top 10 Most Frequent Properties:
"""
    
    for prop, count in stats['properties'].most_common(10):
        coverage = (count / stats['total_nodes'] * 100) if stats['total_nodes'] > 0 else 0
        stats_section += f"# - {prop}: {count}/{stats['total_nodes']} ({coverage:.1f}%)\n"
    
    stats_section += f"""#
# CHANGELOG:
# v1.0.0 ({today}): Initial M{level} grammar generation
#   - Generated from {stats['total_nodes']} ontology nodes
#   - {len(stats['required_properties'])} required property constraints
#   - {len(stats['optional_properties'])} optional property constraints
#   - Forbidden patterns enforced (tscg: namespace, tensor properties)
#   - Level-specific validation rules for M{level}
"""
    
    return stats_section


def generate_shacl_schema(level: int, target_file: str, data: Dict, stats: Dict) -> str:
    """
    Generate the complete SHACL schema based on the target level.
    """
    print_info(f"Génération du schéma SHACL pour M{level}...")
    
    schema = generate_shacl_header(level, target_file, stats)
    
    if level == 3:
        schema += generate_m3_constraints()
    elif level == 2:
        schema += generate_m2_constraints()
    elif level == 1:
        schema += generate_m1_constraints()
    
    schema += generate_forbidden_patterns(level)
    schema += generate_statistics_section(stats, level)
    
    print_success("Schéma SHACL généré avec succès")
    return schema


def validate_shacl_syntax(schema: str) -> bool:
    """
    Validate the generated SHACL schema syntax using rdflib if available.
    """
    try:
        from rdflib import Graph
        
        print_info("Validation de la syntaxe SHACL...")
        g = Graph()
        g.parse(data=schema, format="turtle")
        print_success(f"✓ Syntaxe Turtle valide ({len(g)} triples)")
        return True
    except ImportError:
        print_warning("rdflib non disponible - validation syntaxique ignorée")
        return True
    except Exception as e:
        print_error(f"Erreur de validation syntaxique : {e}")
        return False


def save_shacl_schema(schema: str, output_file: str):
    """
    Save the generated SHACL schema to a .ttl file.
    """
    print_info(f"Sauvegarde du schéma : {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(schema)
        print_success(f"Schéma SHACL sauvegardé : {output_file}")
    except Exception as e:
        print_error(f"Erreur lors de la sauvegarde : {e}")
        sys.exit(1)


def generate_readme(level: int, target_file: str, output_file: str, stats: Dict):
    """
    Generate a companion README file for the SHACL schema.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    readme_file = output_file.replace('.shacl.ttl', '_Schema_README.md')
    
    readme_content = f"""# M{level} SHACL Schema - README

**Generated**: {today}  
**Target Ontology**: {target_file}  
**Schema File**: {output_file}  
**Author**: Echopraxium with the collaboration of Claude AI

## Purpose

Validates the structural and semantic integrity of `{target_file}`.

## Usage

### Validation Command (pyshacl)

```bash
pyshacl -s {output_file} \\
        -f human \\
        {target_file}
```

### Expected Output

- **✓ CONFORMS**: All concepts pass validation
- **✗ VIOLATIONS**: Shows which concepts fail which constraints

## Constraint Categories

### Level-Specific Constraints (M{level})

"""
    
    if level == 3:
        readme_content += """1. **M3 Dimension Validation**
   - ASFID/REVOI dimension structure
   - Grammar properties (Territory/Map)
   - Ontology type declarations

2. **Structural Grammar Properties**
   - hasStructuralGrammarFormula validation
   - Forbidden tensor properties

"""
    elif level == 2:
        readme_content += """1. **GenericConcept Structure**
   - 80 atomic transdisciplinary concepts
   - 9 concept families validation
   - M3 origin references

2. **Formula Validation**
   - Structural grammar formulas (Lambek notation)
   - ASFID/REVOI scores

"""
    elif level == 1:
        readme_content += """1. **Domain Concept Structure**
   - Domain-specific terminology
   - M2 GenericConcept extensions
   - Domain declarations

2. **Reference Integrity**
   - Valid M2 references
   - Domain namespace validation

"""
    
    readme_content += f"""### Forbidden Patterns

- **tscg: namespace** (FORBIDDEN - use m{level}: instead)
- **Tensor properties** (obsolete after structural grammar migration)
"""
    
    if level == 3:
        readme_content += "- **Hilbert space references** (removed in structural grammar reform)\n"
    
    readme_content += f"""
## Statistics

- **Total nodes analyzed**: {stats['total_nodes']}
- **Distinct properties**: {len(stats['properties'])}
- **Required properties**: {len(stats['required_properties'])}
- **Optional properties**: {len(stats['optional_properties'])}
- **Namespaces**: {', '.join(sorted(stats['namespaces']))}

## Maintenance

- Update when M{level} structure changes
- Re-run validation after ontology modifications
- Keep changelog synchronized with ontology versions

## Common Validation Errors

### Error: Missing rdfs:label
**Solution**: Add a label to the concept/property

### Error: Invalid m{level}:ontologyType value
**Solution**: Use one of the allowed values (Poclet, SystemicFramework, etc.)

### Error: Forbidden tscg: namespace detected
**Solution**: Replace with appropriate m{level}: namespace

### Error: hasTensorFormula found (obsolete)
**Solution**: Replace with hasStructuralGrammarFormula

## Integration with TSCG Tools

- **tscg-instance-pipeline**: Validates M0 instances reference valid M{level} concepts
- **tscg-tensor-to-structural-grammar-migration**: Update this schema after Phase 1 (M3)
- **generate_shacl_schema.py**: Re-run to regenerate after major changes

## References

- TSCG Repository: https://github.com/Echopraxium/tscg
- SHACL Specification: https://www.w3.org/TR/shacl/
- Structural Grammar Foundation: `references/Structural_Grammar_Foundation.md`
"""
    
    try:
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print_success(f"README généré : {readme_file}")
    except Exception as e:
        print_warning(f"Erreur lors de la génération du README : {e}")


def main():
    """Main execution flow"""
    try:
        # Step 0: Interactive level selection
        level = select_level()
        
        # Determine target file(s)
        if level == 1:
            target_file, description = select_m1_target()
        elif level == 2:
            target_file = "M2_GenericConcepts.jsonld"
            description = "M2 GenericConcepts"
        else:  # level == 3
            target_file = "M3_GenesisSpace.jsonld"
            description = "M3 GenesisSpace"
        
        print_info(f"\nCible sélectionnée : {description}")
        print_info(f"Fichier : {target_file}")
        
        # Step 1: Load ontology
        data = load_ontology(target_file)
        
        # Step 2: Analyze structure
        stats = analyze_properties(data)
        
        # Step 3: Generate SHACL schema
        schema = generate_shacl_schema(level, target_file, data, stats)
        
        # Step 4: Validate syntax
        if not validate_shacl_syntax(schema):
            print_error("La validation syntaxique a échoué. Schéma non sauvegardé.")
            sys.exit(1)
        
        # Generate output filename
        base_name = target_file.replace('.jsonld', '')
        output_file = f"{base_name}_Schema.shacl.ttl"
        
        # Save schema
        save_shacl_schema(schema, output_file)
        
        # Generate README
        generate_readme(level, target_file, output_file, stats)
        
        # Final summary
        print_header("Génération terminée avec succès !")
        print(f"{Colors.BOLD}Fichiers générés :{Colors.END}")
        print(f"  • {output_file}")
        print(f"  • {output_file.replace('.shacl.ttl', '_Schema_README.md')}")
        print(f"\n{Colors.BOLD}Prochaines étapes :{Colors.END}")
        print(f"  1. Valider : pyshacl -s {output_file} -f human {target_file}")
        print(f"  2. Lire : {output_file.replace('.shacl.ttl', '_Schema_README.md')}")
        print(f"  3. Intégrer : Ajouter au repository TSCG\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interruption utilisateur. Arrêt du script.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
