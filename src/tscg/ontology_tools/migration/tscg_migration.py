# tscg_migration.py
"""
Script de migration complet pour le framework TSCG
Gestion des chemins depuis la racine du repository
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
import pyshacl

# ============================================================
# CONFIGURATION DES CHEMINS
# ============================================================

class TSCGPaths:
    """Gestionnaire des chemins du repository TSCG"""
    
    def __init__(self, root_dir: Optional[str] = None):
        """
        Initialise les chemins depuis la racine du repository
        
        Args:
            root_dir: Racine du repository (auto-détectée si None)
        """
        if root_dir is None:
            # Auto-détection : remonter jusqu'à trouver le dossier ontology
            self.root_dir = self._find_repo_root()
        else:
            self.root_dir = Path(root_dir)
        
        self.root_dir = Path(self.root_dir)
        self.ontology_dir = self.root_dir / "ontology"
        
        # Vérifier que les dossiers existent
        self._check_directories()
    
    def _find_repo_root(self) -> Path:
        """Trouve la racine du repository en remontant l'arborescence"""
        current = Path.cwd()
        
        while current != current.parent:
            # Cherche un dossier 'ontology' ou un fichier .git
            if (current / "ontology").exists() or (current / ".git").exists():
                return current
            current = current.parent
        
        # Fallback : répertoire courant
        print("⚠️  Racine du repository non trouvée, utilisation du répertoire courant")
        return Path.cwd()
    
    def _check_directories(self):
        """Vérifie que les dossiers nécessaires existent"""
        if not self.ontology_dir.exists():
            print(f"⚠️  Dossier ontology non trouvé: {self.ontology_dir}")
            print("   Création du dossier...")
            self.ontology_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def m3_file(self) -> Path:
        """Chemin vers M3_GenesisSpace.jsonld"""
        # Chercher d'abord dans ontology, puis à la racine
        candidates = [
            self.ontology_dir / "M3_GenesisSpace.jsonld",
            self.root_dir / "M3_GenesisSpace.jsonld"
        ]
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        
        # Si aucun trouvé, utiliser le chemin ontology par défaut
        return self.ontology_dir / "M3_GenesisSpace.jsonld"
    
    @property
    def m2_file(self) -> Path:
        """Chemin vers M2_MetaConcepts.jsonld (ontologie par défaut)"""
        # Chercher d'abord dans ontology, puis à la racine
        candidates = [
            self.ontology_dir / "M2_MetaConcepts.jsonld",
            self.root_dir / "M2_MetaConcepts.jsonld"
        ]
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        
        # Par défaut, utiliser ontology/M2_MetaConcepts.jsonld
        return self.ontology_dir / "M2_MetaConcepts.jsonld"
    
    @property
    def m2_ttl_file(self) -> Path:
        """Chemin vers M2_MetaConcepts.ttl (export Protégé)"""
        return self.ontology_dir / "M2_MetaConcepts.ttl"
    
    @property
    def shapes_file(self) -> Path:
        """Chemin vers shacl_shapes.ttl"""
        return self.ontology_dir / "shacl_shapes.ttl"
    
    @property
    def docs_dir(self) -> Path:
        """Dossier de documentation"""
        docs = self.root_dir / "docs"
        docs.mkdir(exist_ok=True)
        return docs
    
    def get_absolute_iri(self, local_name: str, namespace: str = "m2") -> str:
        """
        Génère l'IRI absolu pour un concept
        
        Args:
            local_name: Nom local du concept
            namespace: m2, m3, etc.
        """
        base = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology"
        return f"{base}/{namespace}_{local_name}.jsonld#{local_name}"
    
    def __str__(self) -> str:
        return f"""
TSCG Paths:
  Root: {self.root_dir}
  Ontology: {self.ontology_dir}
  M3: {self.m3_file}
  M2: {self.m2_file} (DEFAULT)
  Export TTL: {self.m2_ttl_file}
  SHACL: {self.shapes_file}
  Docs: {self.docs_dir}
"""


# ============================================================
# PARSEUR DE FORMULES
# ============================================================

class TSCGFormulaParser:
    """Parseur pour les formules de l'ontologie TSCG"""
    
    def __init__(self, paths: TSCGPaths):
        self.paths = paths
        self.dimensions = {'A', 'D', 'F', 'I', 'S'}
        self.metaconcepts = self._load_metaconcepts()
        
        # Patterns regex
        self.patterns = {
            'tensor_product': re.compile(
                r'([ADFIS]\s*⊗\s*)+[ADFIS]|'
                r'([A-Z][a-zA-Z]*\s*⊗\s*)+[A-Z][a-zA-Z]*'
            ),
            'derivative': re.compile(
                r'∂([A-Z]+)/∂([A-Z]+)|'
                r'∂([A-Za-z]+)/∂([A-Za-z]+)'
            ),
            'divergence': re.compile(
                r'([+-]?)∇·([A-Z]+)'
            ),
            'integral': re.compile(
                r'∫\(([^)]+)\)dτ'
            ),
            'sign_polarity': re.compile(
                r'\(-1\)\^{p}\s*\((.+)\)'
            ),
            'equation': re.compile(
                r'(.+)=(.+)'
            ),
            'emergence_combo': re.compile(
                r'⊗⇒\(([^,]+(?:,\s*[^,]+)*)\)'
            ),
            'hybrid_combo': re.compile(
                r'⊗⇒_Territory\(([^)]+)\)\s*×\s*⊗⇒_Map\(([^)]+)\)'
            ),
            'range_constraint': re.compile(
                r'range\(F_A\)\s*<<\s*range\(F_R\)'
            ),
            'svd': re.compile(
                r'∑ᵢ\s*σᵢ\s*\|uᵢ⟩\s*⊗\s*\|vᵢ⟩'
            )
        }
    
    def _load_metaconcepts(self) -> set:
        """Charge la liste des métaconcepts existants"""
        concepts = {'Process', 'Alignment', 'Homeostasis', 'Step', 
                   'Trajectory', 'Amplification', 'Regulation'}
        
        if self.paths.m2_file.exists():
            try:
                with open(self.paths.m2_file) as f:
                    data = json.load(f)
                    for item in data.get('@graph', []):
                        if item.get('@type') == 'm2:MetaConcept':
                            name = item.get('@id', '').split(':')[-1]
                            concepts.add(name)
            except:
                pass
        
        return concepts
    
    def parse_tensor_product(self, formula: str) -> Dict:
        """Parse D ⊗ I ou Process ⊗ Alignment"""
        formula = formula.replace('⊗', '⊗').strip()
        factors = [f.strip() for f in formula.split('⊗')]
        
        typed_factors = []
        for f in factors:
            if f in self.dimensions:
                typed_factors.append({
                    "@type": "m3:Dimension",
                    "@id": self.paths.get_absolute_iri(f, "m3"),
                    "math:symbol": f
                })
            elif f in self.metaconcepts:
                typed_factors.append({
                    "@type": "m2:MetaConcept",
                    "@id": self.paths.get_absolute_iri(f, "m2"),
                    "math:name": f
                })
            else:
                typed_factors.append({
                    "@type": "math:Unknown",
                    "math:name": f
                })
        
        return {
            "@type": "math:TensorProduct",
            "math:factors": typed_factors,
            "math:arity": len(factors),
            "math:latex": formula.replace('⊗', '\\otimes '),
            "math:ascii": formula.replace('⊗', '(x)')
        }
    
    def parse_derivative(self, formula: str) -> Dict:
        """Parse ∂D/∂F"""
        match = self.patterns['derivative'].match(formula)
        if match:
            groups = match.groups()
            num = groups[0] or groups[2]
            den = groups[1] or groups[3]
            
            return {
                "@type": "math:Derivative",
                "math:numerator": {
                    "@type": "m3:Dimension" if num in self.dimensions else "math:Expression",
                    "math:symbol": num
                },
                "math:denominator": {
                    "@type": "m3:Dimension" if den in self.dimensions else "math:Expression",
                    "math:symbol": den
                },
                "math:latex": f"\\frac{{\\partial {num}}}{{\\partial {den}}}",
                "math:order": 1
            }
        return None
    
    def parse_emergence_combo(self, formula: str) -> Dict:
        """Parse ⊗⇒(Process, Step, Trajectory)"""
        match = self.patterns['emergence_combo'].match(formula)
        if match:
            factors_str = match.group(1)
            factors = [f.strip() for f in factors_str.split(',')]
            
            return {
                "@type": "math:EmergentCombo",
                "math:type": "metaconcept_combo",
                "math:factors": factors,
                "math:arity": len(factors),
                "math:semantics": "synergistic_combination",
                "math:emergence": True,
                "math:latex": f"\\otimes\\Rightarrow({', '.join(factors)})"
            }
        return None
    
    def parse_hybrid_combo(self, formula: str) -> Dict:
        """Parse ⊗⇒_Territory(X,Y) × ⊗⇒_Map(A,B)"""
        match = self.patterns['hybrid_combo'].match(formula)
        if match:
            territory_factors = [f.strip() for f in match.group(1).split(',')]
            map_factors = [f.strip() for f in match.group(2).split(',')]
            
            return {
                "@type": "math:HybridCombo",
                "math:type": "territory_map_coupling",
                "math:territory": {
                    "@type": "math:EmergentCombo",
                    "math:factors": territory_factors,
                    "math:domain": "territory"
                },
                "math:map": {
                    "@type": "math:EmergentCombo",
                    "math:factors": map_factors,
                    "math:domain": "map"
                },
                "math:coupling": "bidirectional_feedback",
                "math:latex": f"\\otimes\\Rightarrow_\\text{{Territory}}({match.group(1)}) \\times \\otimes\\Rightarrow_\\text{{Map}}({match.group(2)})"
            }
        return None
    
    def parse_range_constraint(self, formula: str) -> Dict:
        """Parse range(F_A) << range(F_R)"""
        if self.patterns['range_constraint'].match(formula):
            return {
                "@type": "math:Constraint",
                "math:type": "range_asymmetry",
                "math:left": {
                    "@type": "math:Range",
                    "math:of": "F_A",
                    "math:symbol": "range(F_A)"
                },
                "math:operator": "<<",
                "math:right": {
                    "@type": "math:Range",
                    "math:of": "F_R",
                    "math:symbol": "range(F_R)"
                },
                "math:meaning": "short_range_activation × long_range_inhibition",
                "math:latex": "\\|\\text{range}(F_A)\\| \\ll \\|\\text{range}(F_R)\\|"
            }
        return None
    
    def parse_svd(self, formula: str) -> Dict:
        """Parse ∑ᵢ σᵢ |uᵢ⟩ ⊗ |vᵢ⟩"""
        if self.patterns['svd'].search(formula):
            return {
                "@type": "math:SVD",
                "math:full_name": "Singular Value Decomposition",
                "math:components": {
                    "singular_values": "σᵢ",
                    "left_vectors": "|uᵢ⟩",
                    "right_vectors": "|vᵢ⟩"
                },
                "math:dimensions": {
                    "original": 25,
                    "reduced": 5
                },
                "math:spaces": {
                    "left": "ASFID (Territory)",
                    "right": "REVOI (Map)"
                },
                "math:latex": "\\sum_{i=1}^{5} \\sigma_i |u_i\\rangle \\otimes |v_i\\rangle"
            }
        return None
    
    def parse_formula(self, formula: str) -> Dict:
        """Point d'entrée principal"""
        if not formula or not isinstance(formula, str):
            return {"@type": "math:Null", "math:value": str(formula)}
        
        # Nettoyer
        formula = formula.strip()
        
        # Cas spéciaux (ordre important)
        special_parsers = [
            ('svd', self.parse_svd),
            ('range_constraint', self.parse_range_constraint),
            ('hybrid_combo', self.parse_hybrid_combo),
            ('emergence_combo', self.parse_emergence_combo),
            ('equation', lambda f: self._parse_equation(f) if '=' in f and not f.startswith('(-1)') else None),
            ('sign_polarity', lambda f: self._parse_sign_polarity(f) if '(-1)^{p}' in f else None),
            ('derivative', lambda f: self.parse_derivative(f) if '∂' in f and '/' in f else None),
            ('divergence', lambda f: self._parse_divergence(f) if '∇·' in f else None),
            ('integral', lambda f: self._parse_integral(f) if f.startswith('∫') else None)
        ]
        
        for name, parser in special_parsers:
            result = parser(formula)
            if result:
                return result
        
        # Par défaut : produit tensoriel
        if '⊗' in formula:
            return self.parse_tensor_product(formula)
        
        # Formule simple
        if formula in self.dimensions or formula in self.metaconcepts:
            ns = "m3" if formula in self.dimensions else "m2"
            return {
                "@type": "math:Variable",
                "math:symbol": formula,
                "math:reference": self.paths.get_absolute_iri(formula, ns)
            }
        
        # Fallback
        return {
            "@type": "math:RawString",
            "math:value": formula,
            "math:latex": formula
        }
    
    def _parse_equation(self, formula: str) -> Dict:
        """Parse une équation"""
        left, right = formula.split('=', 1)
        return {
            "@type": "math:Equation",
            "math:left": self.parse_formula(left.strip()),
            "math:right": self.parse_formula(right.strip()),
            "math:latex": formula.replace('=', '=').strip()
        }
    
    def _parse_sign_polarity(self, formula: str) -> Dict:
        """Parse (-1)^{p} (A ⊗ D)"""
        match = re.search(r'\(-1\)\^{p}\s*\((.+)\)', formula)
        if match:
            inner = match.group(1)
            return {
                "@type": "math:SignPolarity",
                "math:base": self.parse_formula(inner),
                "math:parameter": "p",
                "math:latex": f"(-1)^{{p}} ({inner})"
            }
        return None
    
    def _parse_divergence(self, formula: str) -> Dict:
        """Parse -∇·D"""
        match = self.patterns['divergence'].match(formula)
        if match:
            sign, operand = match.groups()
            return {
                "@type": "math:Divergence",
                "math:operand": self.parse_formula(operand),
                "math:sign": sign if sign else "+",
                "math:latex": f"{sign}\\nabla \\cdot {operand}"
            }
        return None
    
    def _parse_integral(self, formula: str) -> Dict:
        """Parse ∫(D−F)dτ"""
        match = self.patterns['integral'].match(formula)
        if match:
            inner = match.group(1)
            return {
                "@type": "math:Integral",
                "math:integrand": self.parse_formula(inner),
                "math:variable": "τ",
                "math:latex": f"\\int ({inner})\\,d\\tau"
            }
        return None


# ============================================================
# EXTRACTEUR DEPUIS TURTLE
# ============================================================

class TSCGExtractor:
    """Extrait les métaconcepts depuis le fichier Turtle"""
    
    def __init__(self, paths: TSCGPaths):
        self.paths = paths
        self.parser = TSCGFormulaParser(paths)
        self.graph = Graph()
        self.results = []
        
        # Charger le fichier Turtle s'il existe
        if paths.m2_ttl_file.exists():
            self.graph.parse(str(paths.m2_ttl_file), format='turtle')
            print(f"✅ Fichier Turtle chargé: {paths.m2_ttl_file}")
        else:
            print(f"⚠️  Fichier Turtle non trouvé: {paths.m2_ttl_file}")
    
    def extract_from_text(self, text: str) -> List[Dict]:
        """Extrait les formules depuis un texte (utilisation manuelle)"""
        formulas = []
        
        # Pattern pour trouver les formules dans le texte
        pattern = r'([A-Za-z\s⊗∂∫∇·(){}[\]|⟩⟨,]+)'
        
        for line in text.split('\n'):
            if '⊗' in line or '∂' in line or '∫' in line or '=' in line:
                # Nettoyer la ligne
                clean = re.sub(r'[#"].*$', '', line).strip()
                if clean:
                    formulas.append({
                        'original': clean,
                        'parsed': self.parser.parse_formula(clean)
                    })
        
        return formulas
    
    def extract_from_graph(self) -> List[Dict]:
        """Extrait les formules depuis le graphe RDF"""
        # Requête SPARQL pour trouver les propriétés de formule
        query = """
        SELECT ?concept ?formula ?ascii ?tex WHERE {
            ?concept ?p ?formula .
            FILTER(CONTAINS(STR(?p), "hasTensorFormula") || 
                   CONTAINS(STR(?p), "expression") ||
                   CONTAINS(STR(?p), "Formula"))
            OPTIONAL { ?concept <http://example.org/m2#hasTensorFormulaASCII> ?ascii }
            OPTIONAL { ?concept <http://example.org/m2#hasTensorFormulaTeX> ?tex }
        }
        """
        
        for row in self.graph.query(query):
            concept = str(row.concept).split('#')[-1].split('/')[-1]
            formula = str(row.formula)
            
            # Parser la formule
            parsed = self.parser.parse_formula(formula)
            
            self.results.append({
                "concept": concept,
                "original": formula,
                "ascii": str(row.ascii) if row.ascii else None,
                "tex": str(row.tex) if row.tex else None,
                "parsed": parsed
            })
        
        return self.results


# ============================================================
# GÉNÉRATEUR JSON-LD
# ============================================================

class TSCGJSONLDGenerator:
    """Génère le fichier JSON-LD M2_MetaConcepts.jsonld"""
    
    def __init__(self, paths: TSCGPaths):
        self.paths = paths
        self.extractor = TSCGExtractor(paths)
        self.parser = TSCGFormulaParser(paths)
    
    def generate_m3(self) -> Dict:
        """Génère le fichier M3 Genesis Space"""
        m3 = {
            "@context": {
                "@version": 1.1,
                "@vocab": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3#",
                "math": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/math#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
            },
            "@graph": [
                {
                    "@id": "m3:Attractor",
                    "@type": "math:BasisVector",
                    "math:symbol": "A",
                    "math:index": 0,
                    "math:latex": "A",
                    "rdfs:comment": "Basin of attraction, equilibrium state"
                },
                {
                    "@id": "m3:Dynamics",
                    "@type": "math:BasisVector",
                    "math:symbol": "D",
                    "math:index": 1,
                    "math:latex": "D",
                    "rdfs:comment": "Temporal evolution, change"
                },
                {
                    "@id": "m3:Flow",
                    "@type": "math:BasisVector",
                    "math:symbol": "F",
                    "math:index": 2,
                    "math:latex": "F",
                    "rdfs:comment": "Material, energy, or information transfer"
                },
                {
                    "@id": "m3:Information",
                    "@type": "math:BasisVector",
                    "math:symbol": "I",
                    "math:index": 3,
                    "math:latex": "I",
                    "rdfs:comment": "Data, meaning, or representation"
                },
                {
                    "@id": "m3:Structure",
                    "@type": "math:BasisVector",
                    "math:symbol": "S",
                    "math:index": 4,
                    "math:latex": "S",
                    "rdfs:comment": "Topology, organization, spatial arrangement"
                }
            ]
        }
        
        return m3
    
    def generate_m2(self) -> Dict:
        """Génère le fichier M2 MetaConcepts"""
        
        # Extraire les formules du Turtle
        formulas = self.extractor.extract_from_graph()
        
        m2 = {
            "@context": {
                "@version": 1.1,
                "@vocab": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m2#",
                "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3#",
                "math": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/math#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "owl": "http://www.w3.org/2002/07/owl#",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "@graph": []
        }
        
        # Ajouter la définition de MetaConcept
        m2["@graph"].append({
            "@id": "m2:MetaConcept",
            "@type": "owl:Class",
            "rdfs:comment": "Pattern émergeant du produit tensoriel des dimensions M3"
        })
        
        # Ajouter les métaconcepts extraits
        concept_names = set()
        for item in formulas:
            if item['concept'] not in concept_names:
                concept_names.add(item['concept'])
                
                node = {
                    "@id": f"m2:{item['concept']}",
                    "@type": "m2:MetaConcept",
                    "math:expression": item['parsed'],
                    "rdfs:comment": self._get_comment(item['concept'])
                }
                
                # Ajouter les propriétés additionnelles
                props = self._get_properties(item['concept'])
                if props:
                    node.update(props)
                
                m2["@graph"].append(node)
        
        # Ajouter les métaconcepts manuels (ceux qui ne sont pas dans le Turtle)
        self._add_manual_concepts(m2)
        
        return m2
    
    def _get_comment(self, concept: str) -> str:
        """Récupère le commentaire RDFS pour un concept"""
        query = f"""
        SELECT ?comment WHERE {{
            ?concept rdfs:comment ?comment .
            FILTER(CONTAINS(STR(?concept), "{concept}"))
        }}
        """
        
        for row in self.extractor.graph.query(query):
            return str(row.comment)
        
        return ""
    
    def _get_properties(self, concept: str) -> Dict:
        """Récupère les propriétés additionnelles pour un concept"""
        props = {}
        
        query = f"""
        SELECT ?p ?o WHERE {{
            ?concept ?p ?o .
            FILTER(CONTAINS(STR(?concept), "{concept}"))
            FILTER(!CONTAINS(STR(?p), "formula") && 
                   !CONTAINS(STR(?p), "Tensor") &&
                   !CONTAINS(STR(?p), "comment"))
        }}
        """
        
        for row in self.extractor.graph.query(query):
            prop = str(row.p).split('#')[-1].split('/')[-1]
            val = str(row.o)
            
            if prop == 'hasPolarity':
                props["m2:polarity"] = val
            elif prop == 'hasEpistemicGap':
                try:
                    props["m2:epistemicGap"] = float(val)
                except:
                    pass
            elif prop == 'hasFamily':
                family = val.split('#')[-1].split('/')[-1]
                props["m2:family"] = family
            elif 'example' in prop.lower():
                if "m2:examples" not in props:
                    props["m2:examples"] = []
                props["m2:examples"].append(val)
        
        return props
    
    def _add_manual_concepts(self, m2: Dict):
        """Ajoute les concepts qui ne sont pas dans le Turtle"""
        
        # FeedbackLoop (exemple spécifique)
        feedback_exists = any(
            item.get('@id') == 'm2:FeedbackLoop' 
            for item in m2['@graph']
        )
        
        if not feedback_exists:
            m2['@graph'].append({
                "@id": "m2:FeedbackLoop",
                "@type": "m2:MetaConcept",
                "math:expression": {
                    "@type": "math:Equation",
                    "math:left": {
                        "@type": "math:TensorProduct",
                        "math:factors": [
                            {"@type": "m2:MetaConcept", "math:name": "Process"},
                            {"@type": "m2:MetaConcept", "math:name": "Alignment"},
                            {"@type": "m2:MetaConcept", "math:name": "Homeostasis"}
                        ]
                    },
                    "math:right": {
                        "@type": "math:TensorProduct",
                        "math:factors": [
                            {"@type": "m3:Dimension", "math:symbol": "A"},
                            {"@type": "m3:Dimension", "math:symbol": "S"},
                            {"@type": "m3:Dimension", "math:symbol": "F"},
                            {"@type": "m3:Dimension", "math:symbol": "I"},
                            {"@type": "m3:Dimension", "math:symbol": "D"}
                        ]
                    },
                    "math:latex": "Process \\otimes Alignment \\otimes Homeostasis = A \\otimes S \\otimes F \\otimes I \\otimes D"
                },
                "m2:polarity": "dual",
                "m2:epistemicGap": 0.2,
                "m2:family": "Dynamic",
                "m2:examples": [
                    "Thermostat",
                    "Insulin-glucose regulation",
                    "RAAS blood pressure control"
                ],
                "rdfs:comment": "Cyclic regulatory process where a system compares its current state to a target, reduces the discrepancy, and evolves over time."
            })
    
    def save(self):
        """Sauvegarde les fichiers générés"""
        
        # Générer M3
        m3 = self.generate_m3()
        with open(self.paths.m3_file, 'w', encoding='utf-8') as f:
            json.dump(m3, f, indent=2, ensure_ascii=False)
        print(f"✅ M3 généré: {self.paths.m3_file}")
        
        # Générer M2
        m2 = self.generate_m2()
        with open(self.paths.m2_file, 'w', encoding='utf-8') as f:
            json.dump(m2, f, indent=2, ensure_ascii=False)
        print(f"✅ M2 généré: {self.paths.m2_file} (DEFAULT)")
        
        return m2


# ============================================================
# GÉNÉRATEUR TURTLE POUR PROTÉGÉ
# ============================================================

class TSCGTurtleGenerator:
    """Génère le fichier Turtle pour Protégé"""
    
    def __init__(self, paths: TSCGPaths):
        self.paths = paths
        self.graph = Graph()
        
        # Namespaces
        self.M2 = Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m2#")
        self.M3 = Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3#")
        self.MATH = Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/math#")
        
    def generate(self, m2_data: Dict):
        """Génère le graphe Turtle à partir des données JSON-LD"""
        
        # Définir l'ontologie
        ontology_uri = URIRef("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts")
        self.graph.add((ontology_uri, RDF.type, OWL.Ontology))
        self.graph.add((ontology_uri, OWL.imports, 
                       URIRef("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace")))
        self.graph.add((ontology_uri, RDFS.label, Literal("TSCG M2 MetaConcepts Ontology")))
        
        # Ajouter les métaconcepts
        for item in m2_data.get('@graph', []):
            if item.get('@type') == 'm2:MetaConcept':
                concept_id = item.get('@id', '').split(':')[-1]
                concept = self.M2[concept_id]
                
                self.graph.add((concept, RDF.type, OWL.Class))
                self.graph.add((concept, RDFS.label, Literal(concept_id)))
                
                # Ajouter le commentaire
                if 'rdfs:comment' in item:
                    self.graph.add((concept, RDFS.comment, Literal(item['rdfs:comment'])))
                
                # Ajouter l'expression mathématique comme annotation
                if 'math:expression' in item:
                    expr_json = json.dumps(item['math:expression'], ensure_ascii=False)
                    self.graph.add((concept, self.MATH.expression, Literal(expr_json)))
                
                # Ajouter les propriétés
                if 'm2:polarity' in item:
                    self.graph.add((concept, self.M2.polarity, Literal(item['m2:polarity'])))
                
                if 'm2:epistemicGap' in item:
                    self.graph.add((concept, self.M2.epistemicGap, 
                                   Literal(item['m2:epistemicGap'], datatype=XSD.decimal)))
                
                if 'm2:family' in item:
                    family = self.M2[item['m2:family']]
                    self.graph.add((concept, self.M2.family, family))
                
                if 'm2:examples' in item:
                    for ex in item['m2:examples']:
                        self.graph.add((concept, self.M2.example, Literal(ex)))
        
        # Sauvegarder
        self.graph.serialize(destination=str(self.paths.m2_ttl_file), 
                            format='turtle', encoding='utf-8')
        print(f"✅ Turtle généré: {self.paths.m2_ttl_file}")


# ============================================================
# VALIDATEUR SHACL
# ============================================================

class TSCGValidator:
    """Valide le framework avec SHACL"""
    
    def __init__(self, paths: TSCGPaths):
        self.paths = paths
    
    def generate_shacl(self):
        """Génère les contraintes SHACL"""
        
        shapes = {
            "@context": {
                "sh": "http://www.w3.org/ns/shacl#",
                "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m2#",
                "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3#",
                "math": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/math#",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "@graph": [
                {
                    "@id": "m2:MetaConceptShape",
                    "@type": "sh:NodeShape",
                    "sh:targetClass": "m2:MetaConcept",
                    "sh:property": [
                        {
                            "sh:path": "math:expression",
                            "sh:minCount": 1,
                            "sh:maxCount": 1,
                            "sh:datatype": "xsd:string"
                        },
                        {
                            "sh:path": "m2:polarity",
                            "sh:minCount": 0,
                            "sh:maxCount": 1,
                            "sh:in": ["dual", "neutral", "hybrid", "nary"]
                        },
                        {
                            "sh:path": "m2:epistemicGap",
                            "sh:minCount": 0,
                            "sh:maxCount": 1,
                            "sh:datatype": "xsd:decimal",
                            "sh:minInclusive": 0.0,
                            "sh:maxInclusive": 1.0
                        }
                    ]
                }
            ]
        }
        
        with open(self.paths.shapes_file, 'w', encoding='utf-8') as f:
            json.dump(shapes, f, indent=2, ensure_ascii=False)
        print(f"✅ SHACL shapes générées: {self.paths.shapes_file}")
    
    def validate(self, m2_data: Dict) -> bool:
        """Valide les données avec SHACL"""
        
        # Convertir en graphe RDF
        data_graph = Graph()
        data_graph.parse(data=json.dumps(m2_data), format='json-ld')
        
        # Charger les shapes
        if not self.paths.shapes_file.exists():
            self.generate_shacl()
        
        shapes_graph = Graph()
        shapes_graph.parse(str(self.paths.shapes_file), format='json-ld')
        
        # Valider
        conforms, results_graph, results_text = pyshacl.validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference='rdfs',
            abort_on_first=False
        )
        
        if not conforms:
            print("\n❌ Validation SHACL échouée:")
            print(results_text)
        else:
            print("\n✅ Validation SHACL réussie")
        
        return conforms


# ============================================================
# GÉNÉRATEUR DE DOCUMENTATION
# ============================================================

class TSCGDocumentation:
    """Génère la documentation du framework"""
    
    def __init__(self, paths: TSCGPaths):
        self.paths = paths
    
    def generate_readme(self, m2_data: Dict):
        """Génère un README.md pour le framework"""
        
        doc = [
            "# TSCG M2 MetaConcepts Framework\n",
            "Framework de modélisation systémique basé sur une algèbre tensorielle à 5 dimensions.\n",
            "## Structure du Framework\n",
            "### M3 - Genesis Space (Dimensions fondamentales)",
            "- **A** (Attractor): Bassin d'attraction, état d'équilibre",
            "- **D** (Dynamics): Évolution temporelle, changement",
            "- **F** (Flow): Transfert de matière, énergie, information",
            "- **I** (Information): Donnée, sens, représentation",
            "- **S** (Structure): Topologie, organisation, arrangement spatial\n",
            "### M2 - MetaConcepts (Tenseurs)\n"
        ]
        
        # Grouper par famille
        families = {}
        for item in m2_data.get('@graph', []):
            if item.get('@type') == 'm2:MetaConcept':
                family = item.get('m2:family', 'Other')
                if family not in families:
                    families[family] = []
                families[family].append(item)
        
        for family, concepts in families.items():
            doc.append(f"\n#### Famille {family}\n")
            for concept in concepts:
                name = concept.get('@id', '').split(':')[-1]
                doc.append(f"**{name}**")
                
                if 'math:expression' in concept:
                    expr = concept['math:expression']
                    if 'math:latex' in expr:
                        doc.append(f"- Formule: ${expr['math:latex']}$")
                
                if 'rdfs:comment' in concept:
                    doc.append(f"- Description: {concept['rdfs:comment']}")
                
                if 'm2:examples' in concept:
                    doc.append("- Exemples:")
                    for ex in concept['m2:examples'][:3]:
                        doc.append(f"  - {ex}")
                
                doc.append("")
        
        # Sauvegarder
        readme_path = self.paths.docs_dir / "M2_MetaConcepts_README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(doc))
        print(f"✅ Documentation générée: {readme_path}")


# ============================================================
# SCRIPT PRINCIPAL
# ============================================================

def main():
    """Point d'entrée principal"""
    
    print("=" * 60)
    print("🚀 TSCG Framework Migration Tool")
    print("=" * 60)
    
    # Initialiser les chemins
    paths = TSCGPaths()
    print(paths)
    
    # Générer le JSON-LD
    print("\n📦 Génération des fichiers JSON-LD...")
    generator = TSCGJSONLDGenerator(paths)
    m2_data = generator.save()
    
    # Générer le Turtle pour Protégé
    print("\n🦉 Génération du fichier Turtle pour Protégé...")
    turtle_gen = TSCGTurtleGenerator(paths)
    turtle_gen.generate(m2_data)
    
    # Valider avec SHACL
    print("\n🔍 Validation du framework...")
    validator = TSCGValidator(paths)
    validator.generate_shacl()
    validator.validate(m2_data)
    
    # Générer la documentation
    print("\n📚 Génération de la documentation...")
    docs = TSCGDocumentation(paths)
    docs.generate_readme(m2_data)
    
    print("\n" + "=" * 60)
    print("✅ Migration terminée avec succès!")
    print("=" * 60)
    print(f"\nFichiers générés dans {paths.ontology_dir}:")
    print(f"  - M3_GenesisSpace.jsonld")
    print(f"  - M2_MetaConcepts.jsonld (DEFAULT)")
    print(f"  - M2_MetaConcepts.ttl (pour Protégé)")
    print(f"  - shacl_shapes.jsonld")
    print(f"\nDocumentation: {paths.docs_dir}/M2_MetaConcepts_README.md")


if __name__ == "__main__":
    main()