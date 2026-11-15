#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M2 Metaconcepts SPARQL Analysis Tool
TSCG Framework v15.0.0
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-02-08

Ce script charge M2_MetaConcepts.jsonld et exécute des requêtes SPARQL

* prérequis:
pip install rdflib
"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL
import sys
from pathlib import Path

# Définir les namespaces
M2 = Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#")
M3EAGLE = Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#")
M3SPHINX = Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

def load_jsonld(jsonld_file):
    """
    Charge M2_MetaConcepts.jsonld dans un graphe RDF
    
    Args:
        jsonld_file: Chemin vers M2_MetaConcepts.jsonld
    
    Returns:
        Graph: Graphe RDF chargé
    """
    print(f"📖 Chargement de {jsonld_file}...")
    
    g = Graph()
    g.bind("m2", M2)
    g.bind("m3eagle", M3EAGLE)
    g.bind("m3sphinx", M3SPHINX)
    g.bind("dcterms", DCTERMS)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)
    
    try:
        g.parse(jsonld_file, format="json-ld")
        print(f"✓ {len(g)} triplets chargés")
        return g
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        sys.exit(1)

def execute_query(g, query, title):
    """
    Exécute une requête SPARQL et affiche les résultats
    
    Args:
        g: Graphe RDF
        query: Requête SPARQL
        title: Titre de la requête
    """
    print("\n" + "="*80)
    print(f"📊 {title}")
    print("="*80)
    
    try:
        results = g.query(query)
        
        if not results:
            print("(Aucun résultat)")
            return
        
        # Afficher les résultats
        count = 0
        for row in results:
            count += 1
            formatted_row = []
            for item in row:
                if item is None:
                    formatted_row.append('NULL')
                elif isinstance(item, Literal):
                    formatted_row.append(str(item))
                else:
                    # Extraire juste le fragment de l'URI
                    formatted_row.append(str(item).split('#')[-1] if '#' in str(item) else str(item))
            print(" | ".join(formatted_row))
        
        print(f"\nTotal: {count} résultats")
    
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")

def run_analysis(g):
    """Exécute une série de requêtes SPARQL d'analyse"""
    
    # 1. Statistiques globales
    query1 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    
    SELECT (COUNT(?metaconcept) AS ?total)
    WHERE {
      ?metaconcept a m2:MetaConcept .
    }
    """
    execute_query(g, query1, "1. Nombre Total de Metaconcepts")
    
    # 2. Liste complète avec label et catégorie
    query2 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?category ?polarity
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   rdfs:label ?label .
      OPTIONAL { ?metaconcept m2:hasCategory ?category }
      OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
    }
    ORDER BY ?label
    LIMIT 100
    """
    execute_query(g, query2, "2. Liste des Metaconcepts (100 premiers)")
    
    # 3. Distribution par catégorie
    query3 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    
    SELECT ?category (COUNT(?metaconcept) AS ?count) (AVG(?gap) AS ?avgGap)
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   m2:hasCategory ?category .
      OPTIONAL { ?metaconcept m2:hasEpistemicGap ?gap }
    }
    GROUP BY ?category
    ORDER BY DESC(?count)
    """
    execute_query(g, query3, "3. Distribution par Catégorie")
    
    # 4. Distribution par polarité
    query4 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    
    SELECT ?polarity (COUNT(?metaconcept) AS ?count) (AVG(?gap) AS ?avgGap)
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   m2:hasPolarity ?polarity .
      OPTIONAL { ?metaconcept m2:hasEpistemicGap ?gap }
    }
    GROUP BY ?polarity
    ORDER BY DESC(?count)
    """
    execute_query(g, query4, "4. Distribution par Polarité")
    
    # 5. Top 10 metaconcepts avec gap minimal
    query5 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?category ?polarity ?epistemicGap
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   rdfs:label ?label ;
                   m2:hasEpistemicGap ?epistemicGap .
      OPTIONAL { ?metaconcept m2:hasCategory ?category }
      OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
    }
    ORDER BY ?epistemicGap
    LIMIT 10
    """
    execute_query(g, query5, "5. Top 10 Metaconcepts Mieux Compris (gap minimal)")
    
    # 6. Tous les MetaconceptCombos
    query6 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?label ?category ?polarity ?epistemicGap ?created
    WHERE {
      ?metaconcept a m2:MetaconceptCombo ;
                   rdfs:label ?label .
      OPTIONAL { ?metaconcept m2:hasCategory ?category }
      OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
      OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
      OPTIONAL { ?metaconcept dcterms:created ?created }
    }
    ORDER BY DESC(?created)
    """
    execute_query(g, query6, "6. MetaconceptCombos")
    
    # 7. Metaconcepts Dual (Stereopsic)
    query7 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?category ?epistemicGap
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   rdfs:label ?label ;
                   m2:hasPolarity "dual" .
      OPTIONAL { ?metaconcept m2:hasCategory ?category }
      OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
    }
    ORDER BY ?epistemicGap
    LIMIT 15
    """
    execute_query(g, query7, "7. Metaconcepts Dual (Stereopsic) - 15 premiers")
    
    # 8. Vérification Processor (v15.0.0)
    query8 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?label ?category ?polarity ?epistemicGap ?created
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   rdfs:label "Processor" ;
                   rdfs:label ?label .
      OPTIONAL { ?metaconcept m2:hasCategory ?category }
      OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
      OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
      OPTIONAL { ?metaconcept dcterms:created ?created }
    }
    """
    execute_query(g, query8, "8. Nouveau Metaconcept: Processor (v15.0.0)")
    
    # 9. Processor est-il un MetaconceptCombo?
    query9 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    ASK {
      ?processor a m2:MetaconceptCombo ;
                 rdfs:label "Processor" .
    }
    """
    print("\n" + "="*80)
    print("📊 9. Processor est-il un MetaconceptCombo?")
    print("="*80)
    result = g.query(query9)
    print(f"Résultat: {'✅ OUI' if result.askAnswer else '❌ NON'}")
    
    # 10. Statistiques gap global
    query10 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    
    SELECT 
      (COUNT(?mc) AS ?totalMetaconcepts)
      (AVG(?gap) AS ?avgEpistemicGap)
      (MIN(?gap) AS ?minGap)
      (MAX(?gap) AS ?maxGap)
    WHERE {
      ?mc a m2:MetaConcept ;
          m2:hasEpistemicGap ?gap .
    }
    """
    execute_query(g, query10, "10. Statistiques Epistemic Gap Global")
    
    # 11. Metaconcepts Ontologiques
    query11 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?polarity ?epistemicGap
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   rdfs:label ?label ;
                   m2:hasCategory ?category .
      FILTER (STR(?category) = "m2:Ontological")
      OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
      OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
    }
    ORDER BY ?label
    """
    execute_query(g, query11, "11. Metaconcepts Ontologiques")
    
    # 12. Recherche par mot-clé: "Process"
    query12 = """
    PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?category ?polarity
    WHERE {
      ?metaconcept a m2:MetaConcept ;
                   rdfs:label ?label .
      FILTER REGEX(?label, "Process", "i")
      OPTIONAL { ?metaconcept m2:hasCategory ?category }
      OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
    }
    ORDER BY ?label
    """
    execute_query(g, query12, "12. Recherche: Metaconcepts contenant 'Process'")

def main():
    """Point d'entrée principal"""
    
    # Chemin du fichier JSON-LD
    jsonld_file = '../M2_MetaConcepts.jsonld'
    
    # Vérifier que le fichier existe
    if not Path(jsonld_file).exists():
        print(f"❌ Erreur: Fichier non trouvé: {jsonld_file}")
        sys.exit(1)
    
    # Charger le graphe RDF
    g = load_jsonld(jsonld_file)
    
    # Exécuter les analyses SPARQL
    run_analysis(g)
    
    print("\n" + "="*80)
    print("✅ Analyse SPARQL terminée !")
    print("\nPour exécuter vos propres requêtes:")
    print("  from rdflib import Graph")
    print("  g = Graph()")
    print("  g.parse('M2_MetaConcepts_v15_0_0.jsonld', format='json-ld')")
    print("  results = g.query('SELECT ...')")
    print("="*80)

if __name__ == '__main__':
    main()