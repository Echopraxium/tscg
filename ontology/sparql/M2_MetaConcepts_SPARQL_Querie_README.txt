# ============================================================================
# M2_MetaConcepts SPARQL Queries
# TSCG Framework v15.0.0
# Author: Echopraxium with the collaboration of Claude AI
# Date: 2026-02-08
# ============================================================================
# 
# Ce fichier contient des requêtes SPARQL pour interroger M2_MetaConcepts.jsonld
# en tant que triplestore RDF/OWL
#
# Instructions d'utilisation:
#   1. Charger M2_MetaConcepts_v15_0_0.jsonld dans un triplestore (Apache Jena, RDF4J, GraphDB)
#   2. Exécuter les requêtes SPARQL ci-dessous
#
# Préfixes utilisés:
#   - m2: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#
#   - m3eagle: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#
#   - m3sphinx: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#
#   - owl: http://www.w3.org/2002/07/owl#
#   - rdfs: http://www.w3.org/2000/01/rdf-schema#
#   - dcterms: http://purl.org/dc/terms/
# ============================================================================
# prérequis:
# pip install rdflib
# ============================================================================

# ----------------------------------------------------------------------------
# SECTION 1: REQUÊTES DE BASE
# ----------------------------------------------------------------------------

# 1.1 Liste complète des metaconcepts (avec label et catégorie)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?metaconcept ?label ?category ?polarity
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
}
ORDER BY ?label


# 1.2 Compter le nombre total de metaconcepts
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT (COUNT(?metaconcept) AS ?total)
WHERE {
  ?metaconcept a m2:MetaConcept .
}


# 1.3 Liste des metaconcepts avec leurs formules tensorielles
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?formula ?formulaExpanded
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label .
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
  OPTIONAL { ?metaconcept m2:hasTensorFormulaExpanded ?formulaExpanded }
}
ORDER BY ?label


# 1.4 Liste des metaconcepts avec epistemic gap
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?epistemicGap ?category ?polarity
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasEpistemicGap ?epistemicGap .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
}
ORDER BY ?epistemicGap


# ----------------------------------------------------------------------------
# SECTION 2: REQUÊTES PAR CATÉGORIE
# ----------------------------------------------------------------------------

# 2.1 Tous les metaconcepts Ontologiques
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?polarity ?epistemicGap ?formula
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasCategory m2:Ontological .
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
}
ORDER BY ?label


# 2.2 Tous les metaconcepts Dynamiques
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?polarity ?epistemicGap ?formula
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasCategory m2:Dynamic .
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
}
ORDER BY ?label


# 2.3 Tous les metaconcepts Structurels
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?polarity ?epistemicGap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasCategory m2:Structural .
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
}
ORDER BY ?label


# 2.4 Tous les metaconcepts Régulateurs
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?polarity ?epistemicGap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasCategory m2:Regulatory .
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
}
ORDER BY ?label


# 2.5 Distribution par catégorie (compte et gap moyen)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT ?category (COUNT(?metaconcept) AS ?count) (AVG(?gap) AS ?avgGap)
WHERE {
  ?metaconcept a m2:MetaConcept ;
               m2:hasCategory ?category .
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?gap }
}
GROUP BY ?category
ORDER BY DESC(?count)


# ----------------------------------------------------------------------------
# SECTION 3: REQUÊTES PAR POLARITÉ
# ----------------------------------------------------------------------------

# 3.1 Tous les metaconcepts Dual (Bicephalous)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap ?formula
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasPolarity "dual" .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
}
ORDER BY ?epistemicGap


# 3.2 Tous les metaconcepts Territory
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasPolarity "territory" .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
}
ORDER BY ?label


# 3.3 Tous les metaconcepts Map
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasPolarity "map" .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
}
ORDER BY ?label


# 3.4 Tous les metaconcepts Neutral
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasPolarity "neutral" .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
}
ORDER BY ?label


# 3.5 Distribution par polarité (compte et gap moyen)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT ?polarity (COUNT(?metaconcept) AS ?count) (AVG(?gap) AS ?avgGap)
WHERE {
  ?metaconcept a m2:MetaConcept ;
               m2:hasPolarity ?polarity .
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?gap }
}
GROUP BY ?polarity
ORDER BY DESC(?count)


# ----------------------------------------------------------------------------
# SECTION 4: METACONCEPTCOMBOS
# ----------------------------------------------------------------------------

# 4.1 Tous les MetaconceptCombos
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


# 4.2 MetaconceptCombos avec leurs parents
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?comboLabel ?parentLabel ?parentFormula
WHERE {
  ?combo a m2:MetaconceptCombo ;
         rdfs:label ?comboLabel ;
         m2:parentMetaconcepts ?parent .
  ?parent rdfs:label ?parentLabel .
  OPTIONAL { ?parent m2:hasTensorFormula ?parentFormula }
}
ORDER BY ?comboLabel


# 4.3 Compter les MetaconceptCombos
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT (COUNT(?combo) AS ?totalCombos)
WHERE {
  ?combo a m2:MetaconceptCombo .
}


# ----------------------------------------------------------------------------
# SECTION 5: EPISTEMIC GAP
# ----------------------------------------------------------------------------

# 5.1 Top 10 metaconcepts avec gap minimal (best understood)
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


# 5.2 Top 10 metaconcepts avec gap maximal (need refinement)
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
ORDER BY DESC(?epistemicGap)
LIMIT 10


# 5.3 Metaconcepts bien validés (gap < 0.15)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap ?formula
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasEpistemicGap ?epistemicGap .
  FILTER (?epistemicGap < 0.15)
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
}
ORDER BY ?epistemicGap


# 5.4 Metaconcepts nécessitant validation (gap > 0.3)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasEpistemicGap ?epistemicGap .
  FILTER (?epistemicGap > 0.3)
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
}
ORDER BY DESC(?epistemicGap)


# 5.5 Statistiques gap par catégorie
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT ?category 
       (COUNT(?mc) AS ?count) 
       (AVG(?gap) AS ?avgGap) 
       (MIN(?gap) AS ?minGap) 
       (MAX(?gap) AS ?maxGap)
WHERE {
  ?mc a m2:MetaConcept ;
      m2:hasCategory ?category ;
      m2:hasEpistemicGap ?gap .
}
GROUP BY ?category
ORDER BY ?avgGap


# ----------------------------------------------------------------------------
# SECTION 6: NOUVEAU METACONCEPT PROCESSOR (v15.0.0)
# ----------------------------------------------------------------------------

# 6.1 Détails complets de Processor
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?label ?category ?polarity ?epistemicGap ?formula ?created ?comment
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label "Processor" ;
               rdfs:label ?label .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
  OPTIONAL { ?metaconcept dcterms:created ?created }
  OPTIONAL { ?metaconcept rdfs:comment ?comment }
}


# 6.2 Vérifier que Processor est un MetaconceptCombo
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

ASK {
  ?processor a m2:MetaconceptCombo ;
             rdfs:label "Processor" .
}


# 6.3 Exemples de Processor
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?example
WHERE {
  ?processor rdfs:label "Processor" ;
             m2:hasExample ?example .
}


# ----------------------------------------------------------------------------
# SECTION 7: FORMULES HYBRIDES
# ----------------------------------------------------------------------------

# 7.1 Tous les metaconcepts avec formules hybrides (Territory + Map)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?formulaTerritory ?formulaMap
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label .
  OPTIONAL { ?metaconcept m2:hasTensorFormulaExpanded_Territory ?formulaTerritory }
  OPTIONAL { ?metaconcept m2:hasTensorFormulaExpanded_Map ?formulaMap }
  FILTER (BOUND(?formulaTerritory) && BOUND(?formulaMap))
}
ORDER BY ?label


# 7.2 Cascade et Processor (les 2 hybrides ternaires)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?formula ?formulaExpanded
WHERE {
  VALUES ?label { "Cascade" "Processor" }
  ?metaconcept rdfs:label ?label ;
               m2:hasTensorFormula ?formula .
  OPTIONAL { ?metaconcept m2:hasTensorFormulaExpanded ?formulaExpanded }
}


# ----------------------------------------------------------------------------
# SECTION 8: REQUÊTES TEMPORELLES
# ----------------------------------------------------------------------------

# 8.1 Metaconcepts par année de création
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?created (COUNT(?mc) AS ?count)
WHERE {
  ?mc a m2:MetaConcept ;
      dcterms:created ?created .
}
GROUP BY ?created
ORDER BY DESC(?created)


# 8.2 Metaconcepts créés en 2026 (derniers ajouts)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?label ?category ?created
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               dcterms:created ?created .
  FILTER (YEAR(?created) = 2026)
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
}
ORDER BY DESC(?created)


# ----------------------------------------------------------------------------
# SECTION 9: REQUÊTES DE RECHERCHE TEXTUELLE
# ----------------------------------------------------------------------------

# 9.1 Recherche par mot-clé dans label (REGEX)
# Exemple: tous les metaconcepts contenant "Process"
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


# 9.2 Recherche dans les commentaires
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?comment
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               rdfs:comment ?comment .
  FILTER REGEX(?comment, "input.*output", "i")
}


# 9.3 Metaconcepts utilisant dimension Structure (S) dans formule
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?formulaExpanded
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               m2:hasTensorFormulaExpanded ?formulaExpanded .
  FILTER REGEX(?formulaExpanded, "S⊗", "i")
}


# ----------------------------------------------------------------------------
# SECTION 10: REQUÊTES STATISTIQUES AVANCÉES
# ----------------------------------------------------------------------------

# 10.1 Matrice catégorie × polarité (crosstab)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT ?category ?polarity (COUNT(?mc) AS ?count)
WHERE {
  ?mc a m2:MetaConcept ;
      m2:hasCategory ?category ;
      m2:hasPolarity ?polarity .
}
GROUP BY ?category ?polarity
ORDER BY ?category ?polarity


# 10.2 Densité de formalisation (combien ont des formules)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>

SELECT 
  (COUNT(?mc) AS ?total)
  (COUNT(?formula) AS ?withFormula)
  ((COUNT(?formula) * 100.0 / COUNT(?mc)) AS ?percentage)
WHERE {
  ?mc a m2:MetaConcept .
  OPTIONAL { ?mc m2:hasTensorFormula ?formula }
}


# 10.3 Score de qualité global du framework
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


# ----------------------------------------------------------------------------
# SECTION 11: REQUÊTES HIÉRARCHIQUES (rdfs:subClassOf)
# ----------------------------------------------------------------------------

# 11.1 Metaconcepts avec leurs superclasses
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?superClass
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               rdfs:subClassOf ?superClass .
}
ORDER BY ?label


# 11.2 Processor et sa superclasse (System)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?superClass
WHERE {
  ?metaconcept rdfs:label "Processor" ;
               rdfs:subClassOf ?superClass .
  BIND("Processor" AS ?label)
}


# ----------------------------------------------------------------------------
# SECTION 12: REQUÊTES DE VALIDATION
# ----------------------------------------------------------------------------

# 12.1 Vérifier l'intégrité: tous les metaconcepts ont-ils un label?
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?metaconcept
WHERE {
  ?metaconcept a m2:MetaConcept .
  FILTER NOT EXISTS { ?metaconcept rdfs:label ?label }
}


# 12.2 Vérifier la cohérence: metaconcepts sans catégorie
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label .
  FILTER NOT EXISTS { ?metaconcept m2:hasCategory ?category }
}


# 12.3 Vérifier la cohérence: metaconcepts sans epistemic gap
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label .
  FILTER NOT EXISTS { ?metaconcept m2:hasEpistemicGap ?gap }
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
}


# ----------------------------------------------------------------------------
# SECTION 13: REQUÊTES D'EXPORT
# ----------------------------------------------------------------------------

# 13.1 Export CSV complet (tous les champs principaux)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?label ?category ?polarity ?epistemicGap ?formula ?created
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
  OPTIONAL { ?metaconcept m2:hasPolarity ?polarity }
  OPTIONAL { ?metaconcept m2:hasEpistemicGap ?epistemicGap }
  OPTIONAL { ?metaconcept m2:hasTensorFormula ?formula }
  OPTIONAL { ?metaconcept dcterms:created ?created }
}
ORDER BY ?category ?label


# 13.2 Export pour documentation (avec commentaires)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?comment
WHERE {
  ?metaconcept a m2:MetaConcept ;
               rdfs:label ?label ;
               rdfs:comment ?comment .
  OPTIONAL { ?metaconcept m2:hasCategory ?category }
}
ORDER BY ?label


# ----------------------------------------------------------------------------
# SECTION 14: REQUÊTES DESCRIBE ET CONSTRUCT
# ----------------------------------------------------------------------------

# 14.1 DESCRIBE Processor (tous les triplets)
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

DESCRIBE ?processor
WHERE {
  ?processor rdfs:label "Processor" .
}


# 14.2 CONSTRUCT - Créer un sous-graphe des metaconcepts dual
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
  ?mc rdfs:label ?label ;
      m2:hasCategory ?category ;
      m2:hasPolarity "dual" ;
      m2:hasEpistemicGap ?gap .
}
WHERE {
  ?mc a m2:MetaConcept ;
      rdfs:label ?label ;
      m2:hasPolarity "dual" .
  OPTIONAL { ?mc m2:hasCategory ?category }
  OPTIONAL { ?mc m2:hasEpistemicGap ?gap }
}


# 14.3 CONSTRUCT - Graph de tous les MetaconceptCombos avec parents
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
  ?combo a m2:MetaconceptCombo ;
         rdfs:label ?comboLabel ;
         m2:parentMetaconcepts ?parent .
  ?parent rdfs:label ?parentLabel .
}
WHERE {
  ?combo a m2:MetaconceptCombo ;
         rdfs:label ?comboLabel ;
         m2:parentMetaconcepts ?parent .
  ?parent rdfs:label ?parentLabel .
}


# ============================================================================
# FIN DES REQUÊTES SPARQL
# ============================================================================

# NOTES D'UTILISATION:
# 
# 1. Avec Apache Jena ARQ:
#    sparql --data=M2_MetaConcepts_v15_0_0.jsonld --query=query.sparql
#
# 2. Avec RDF4J Workbench:
#    - Créer un repository
#    - Uploader M2_MetaConcepts_v15_0_0.jsonld
#    - Exécuter les requêtes dans l'interface web
#
# 3. Avec GraphDB:
#    - Import M2_MetaConcepts_v15_0_0.jsonld
#    - Query → SPARQL → Coller la requête
#
# 4. Avec Python rdflib:
#    from rdflib import Graph
#    g = Graph()
#    g.parse("M2_MetaConcepts_v15_0_0.jsonld", format="json-ld")
#    results = g.query(sparql_query)
#
# ============================================================================
