# M2_GenericConcepts SPARQL Queries - Guide d'Utilisation
## TSCG Framework v15.0.0

**Auteur**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-02-08  
**Version**: 15.0.0

---

## 📚 Vue d'Ensemble

Ce package contient **80+ requêtes SPARQL** pour interroger l'ontologie M2_GenericConcepts.jsonld en tant que triplestore RDF/OWL sémantique.

### Fichiers Fournis

1. **M2_GenericConcepts_SPARQL_Queries.rq** - 80+ requêtes SPARQL organisées en 14 sections
2. **m2_sparql_analysis.py** - Script Python pour exécution automatique avec rdflib
3. **SPARQL_README.md** - Ce guide d'utilisation

---

## 🎯 Pourquoi SPARQL (et pas SQL) ?

### JSON-LD = RDF Sémantique

M2_GenericConcepts.jsonld est un fichier **JSON-LD** (JSON for Linking Data) qui représente :
- Des **triplets RDF** (sujet-prédicat-objet)
- Une **ontologie OWL** (Web Ontology Language)
- Des **relations sémantiques** (rdfs:subClassOf, owl:sameAs, etc.)

### SQL vs SPARQL

| Aspect | SQL | SPARQL |
|--------|-----|--------|
| **Modèle de données** | Tables relationnelles | Graphe RDF (triplets) |
| **Structure** | Schéma fixe | Schéma flexible (ontologie) |
| **Requêtes** | Jointures sur clés | Patterns de graphe |
| **Sémantique** | Aucune | Inférence OWL/RDFS |
| **Idéal pour** | Données tabulaires | Données liées sémantiques |

### Exemple Concret

**Triplet RDF dans M2_GenericConcepts.jsonld** :
```turtle
m2:Processor rdfs:subClassOf m2:System .
m2:Processor m2:hasCategory m2:Ontological .
m2:Processor m2:hasPolarity "dual" .
```

**En SQL** (nécessite table plate avec perte sémantique) :
```sql
SELECT * FROM GenericConcepts WHERE label = 'Processor';
```

**En SPARQL** (navigation de graphe sémantique) :
```sparql
SELECT ?label ?superClass ?category ?polarity
WHERE {
  ?GenericConcept rdfs:label "Processor" ;
               rdfs:subClassOf ?superClass ;
               m2:hasCategory ?category ;
               m2:hasPolarity ?polarity .
}
```

---

## 🔧 Configuration Requise

### Option 1 : Apache Jena ARQ (Ligne de commande)

```bash
# Installation
wget https://dlcdn.apache.org/jena/binaries/apache-jena-4.10.0.tar.gz
tar -xzf apache-jena-4.10.0.tar.gz
export PATH=$PATH:$PWD/apache-jena-4.10.0/bin

# Exécution d'une requête
sparql --data=M2_GenericConcepts_v15_0_0.jsonld --query=query.sparql
```

### Option 2 : Python rdflib

```bash
# Installation
pip install rdflib

# Utilisation
python3 m2_sparql_analysis.py
```

### Option 3 : GraphDB (Interface Web)

1. Télécharger GraphDB Free : https://graphdb.ontotext.com/
2. Créer un repository
3. Importer M2_GenericConcepts_v15_0_0.jsonld
4. Onglet SPARQL → Exécuter les requêtes

### Option 4 : RDF4J Workbench (Interface Web)

1. Télécharger RDF4J : https://rdf4j.org/
2. Déployer workbench.war dans Tomcat
3. Créer repository → Upload M2_GenericConcepts_v15_0_0.jsonld
4. Query → SPARQL

---

## 📊 Structure des Requêtes (14 Sections)

### Section 1 : Requêtes de Base (4 requêtes)
- Liste complète des GenericConcepts
- Compte total
- Formules tensorielles
- Epistemic gap

### Section 2 : Requêtes par Catégorie (5 requêtes)
- Ontological, Dynamic, Structural, Regulatory
- Distribution par catégorie

### Section 3 : Requêtes par Polarité (5 requêtes)
- Dual, Territory, Map, Neutral
- Distribution par polarité

### Section 4 : GenericConceptCombos (3 requêtes)
- Tous les combos
- Combos avec leurs parents
- Compte des combos

### Section 5 : Epistemic Gap (5 requêtes)
- Top 10 gap minimal (best understood)
- Top 10 gap maximal (need refinement)
- Well validated (gap < 0.15)
- Needs validation (gap > 0.3)
- Statistiques par catégorie

### Section 6 : Processor (v15.0.0) (3 requêtes)
- Détails complets
- Vérification GenericConceptCombo
- Exemples

### Section 7 : Formules Hybrides (2 requêtes)
- Tous les hybrides Territory+Map
- Cascade et Processor

### Section 8 : Requêtes Temporelles (2 requêtes)
- Par année de création
- Créés en 2026

### Section 9 : Recherche Textuelle (3 requêtes)
- Par mot-clé dans label (REGEX)
- Dans commentaires
- Par dimension dans formule

### Section 10 : Statistiques Avancées (3 requêtes)
- Matrice catégorie × polarité
- Densité de formalisation
- Score de qualité global

### Section 11 : Hiérarchie (2 requêtes)
- GenericConcepts avec superclasses
- Processor rdfs:subClassOf System

### Section 12 : Validation (3 requêtes)
- Intégrité : tous ont label ?
- Cohérence : tous ont catégorie ?
- Cohérence : tous ont gap ?

### Section 13 : Export (2 requêtes)
- Export CSV complet
- Export documentation

### Section 14 : DESCRIBE et CONSTRUCT (3 requêtes)
- DESCRIBE Processor (tous triplets)
- CONSTRUCT sous-graphe GenericConcepts dual
- CONSTRUCT graphe GenericConceptCombos

---

## 💡 Exemples d'Utilisation

### Exemple 1 : Liste Complète des GenericConcepts

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?GenericConcept ?label ?category ?polarity
WHERE {
  ?GenericConcept a m2:GenericConcept ;
               rdfs:label ?label .
  OPTIONAL { ?GenericConcept m2:hasCategory ?category }
  OPTIONAL { ?GenericConcept m2:hasPolarity ?polarity }
}
ORDER BY ?label
```

**Résultat attendu** : 72 GenericConcepts avec leurs propriétés

---

### Exemple 2 : Vérification Processor (v15.0.0)

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?label ?category ?polarity ?epistemicGap ?created
WHERE {
  ?GenericConcept a m2:GenericConcept ;
               rdfs:label "Processor" ;
               rdfs:label ?label .
  OPTIONAL { ?GenericConcept m2:hasCategory ?category }
  OPTIONAL { ?GenericConcept m2:hasPolarity ?polarity }
  OPTIONAL { ?GenericConcept m2:hasEpistemicGap ?epistemicGap }
  OPTIONAL { ?GenericConcept dcterms:created ?created }
}
```

**Résultat attendu** :
```
label      | category        | polarity | epistemicGap | created
-----------|-----------------|----------|--------------|------------
Processor  | m2:Ontological  | dual     | 0.15         | 2026-02-07
```

---

### Exemple 3 : GenericConcepts Dual (Bicephalous)

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?epistemicGap
WHERE {
  ?GenericConcept a m2:GenericConcept ;
               rdfs:label ?label ;
               m2:hasPolarity "dual" .
  OPTIONAL { ?GenericConcept m2:hasCategory ?category }
  OPTIONAL { ?GenericConcept m2:hasEpistemicGap ?epistemicGap }
}
ORDER BY ?epistemicGap
```

**Résultat attendu** : 16 GenericConcepts dual, triés par gap croissant

---

### Exemple 4 : Distribution par Catégorie

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>

SELECT ?category (COUNT(?GenericConcept) AS ?count) (AVG(?gap) AS ?avgGap)
WHERE {
  ?GenericConcept a m2:GenericConcept ;
               m2:hasCategory ?category .
  OPTIONAL { ?GenericConcept m2:hasEpistemicGap ?gap }
}
GROUP BY ?category
ORDER BY DESC(?count)
```

**Résultat attendu** :
```
category          | count | avgGap
------------------|-------|--------
m2:Structural     | 19    | 0.233
m2:Dynamic        | 13    | 0.237
m2:Ontological    | 11    | 0.268
...
```

---

### Exemple 5 : Recherche par Mot-Clé

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category ?polarity
WHERE {
  ?GenericConcept a m2:GenericConcept ;
               rdfs:label ?label .
  FILTER REGEX(?label, "Process", "i")
  OPTIONAL { ?GenericConcept m2:hasCategory ?category }
  OPTIONAL { ?GenericConcept m2:hasPolarity ?polarity }
}
ORDER BY ?label
```

**Résultat attendu** : Process, Processor (tous les GenericConcepts contenant "Process")

---

### Exemple 6 : ASK - Processor est-il un GenericConceptCombo ?

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

ASK {
  ?processor a m2:GenericConceptCombo ;
             rdfs:label "Processor" .
}
```

**Résultat attendu** : `true` (Processor est bien un GenericConceptCombo)

---

### Exemple 7 : DESCRIBE - Tous les triplets de Processor

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

DESCRIBE ?processor
WHERE {
  ?processor rdfs:label "Processor" .
}
```

**Résultat attendu** : Graphe complet RDF de Processor (tous les triplets)

---

### Exemple 8 : CONSTRUCT - Sous-graphe GenericConcepts Dual

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
  ?mc rdfs:label ?label ;
      m2:hasCategory ?category ;
      m2:hasPolarity "dual" ;
      m2:hasEpistemicGap ?gap .
}
WHERE {
  ?mc a m2:GenericConcept ;
      rdfs:label ?label ;
      m2:hasPolarity "dual" .
  OPTIONAL { ?mc m2:hasCategory ?category }
  OPTIONAL { ?mc m2:hasEpistemicGap ?gap }
}
```

**Résultat attendu** : Nouveau graphe RDF contenant uniquement les GenericConcepts dual

---

## 🚀 Utilisation avec Python rdflib

```python
from rdflib import Graph

# Charger le graphe
g = Graph()
g.parse("M2_GenericConcepts_v15_0_0.jsonld", format="json-ld")

# Exécuter une requête SPARQL
query = """
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?category
WHERE {
  ?mc a m2:GenericConcept ;
      rdfs:label ?label ;
      m2:hasCategory ?category .
}
ORDER BY ?label
LIMIT 10
"""

results = g.query(query)

# Afficher les résultats
for row in results:
    print(f"{row.label} - {row.category}")
```

---

## 🔍 Requêtes les Plus Utiles

### Top 5 Requêtes Essentielles

1. **Liste complète** (Section 1.1) - Vue d'ensemble de tous les GenericConcepts
2. **Vérification Processor** (Section 6.1) - Validation du nouveau GenericConcept v15.0.0
3. **Distribution par catégorie** (Section 2.5) - Comprendre la structure M2
4. **GenericConcepts Dual** (Section 3.1) - Identifier les patterns bicéphales
5. **Top 10 gap minimal** (Section 5.1) - GenericConcepts les mieux compris

### Top 5 Requêtes Avancées

1. **CONSTRUCT sous-graphe dual** (Section 14.2) - Extraire un sous-graphe sémantique
2. **Matrice catégorie × polarité** (Section 10.1) - Analyse croisée
3. **Statistiques gap par catégorie** (Section 5.5) - Qualité par domaine
4. **GenericConceptCombos avec parents** (Section 4.2) - Relations de composition
5. **Recherche REGEX** (Section 9.1) - Recherche textuelle flexible

---

## 📈 Résultats Attendus (TSCG v15.0.0)

### Statistiques Globales

- **Total GenericConcepts** : 72
- **GenericConceptCombos** : 2 (Cascade, Processor)
- **Catégories** : 9 (Structural, Dynamic, Ontological, etc.)
- **Polarités** : 4 (neutral, dual, hybrid, nary)
- **Gap moyen** : 0.251
- **Gap minimal** : 0.100 (Component)
- **Gap maximal** : 0.500

### Distribution par Polarité

- **neutral** : 52 (72.2%)
- **dual** : 16 (22.2%) ← **Processor ici**
- **hybrid** : 3 (4.2%)
- **nary** : 1 (1.4%)

### Nouveau GenericConcept (v15.0.0)

- **Label** : Processor
- **Catégorie** : m2:Ontological
- **Polarité** : dual
- **Epistemic Gap** : 0.15
- **Type** : m2:GenericConceptCombo
- **Créé** : 2026-02-07

---

## 🎓 Concepts SPARQL Clés

### SELECT - Extraction de données

```sparql
SELECT ?variable1 ?variable2
WHERE { ... }
```
Retourne des lignes de résultats (comme SQL SELECT)

### ASK - Question booléenne

```sparql
ASK { ... }
```
Retourne `true` ou `false`

### DESCRIBE - Description complète

```sparql
DESCRIBE ?resource
```
Retourne tous les triplets concernant ?resource

### CONSTRUCT - Construction de graphe

```sparql
CONSTRUCT { triplets_à_créer }
WHERE { pattern_de_recherche }
```
Crée un nouveau graphe RDF

### FILTER - Filtrage

```sparql
FILTER (?gap < 0.15)
FILTER REGEX(?label, "Process", "i")
```
Filtre les résultats (comme WHERE en SQL)

### OPTIONAL - Jointure optionnelle

```sparql
OPTIONAL { ?mc m2:hasCategory ?category }
```
Inclut ?category si présent, sinon NULL

### GROUP BY / AVG / COUNT - Agrégation

```sparql
SELECT ?category (COUNT(?mc) AS ?count) (AVG(?gap) AS ?avgGap)
WHERE { ... }
GROUP BY ?category
```
Agrégation comme en SQL

---

## 🔗 Ressources

### Spécifications W3C

- **SPARQL 1.1 Query Language** : https://www.w3.org/TR/sparql11-query/
- **RDF 1.1 Primer** : https://www.w3.org/TR/rdf11-primer/
- **JSON-LD 1.1** : https://www.w3.org/TR/json-ld11/
- **OWL 2 Web Ontology Language** : https://www.w3.org/TR/owl2-overview/

### Outils

- **Apache Jena** : https://jena.apache.org/
- **RDF4J** : https://rdf4j.org/
- **GraphDB** : https://graphdb.ontotext.com/
- **Python rdflib** : https://rdflib.readthedocs.io/

### Tutoriels

- **SPARQL by Example** : https://www.w3.org/2009/Talks/0615-qbe/
- **Linked Data Patterns** : http://patterns.dataincubator.org/

---

## 💾 Fichiers Inclus

1. **M2_GenericConcepts_SPARQL_Queries.rq** (20 KB)
   - 80+ requêtes SPARQL complètes
   - 14 sections organisées
   - Commentaires détaillés

2. **m2_sparql_analysis.py** (8 KB)
   - Script Python avec rdflib
   - 12 analyses prédéfinies
   - Affichage formaté

3. **SPARQL_README.md** (ce fichier)
   - Guide complet d'utilisation
   - Exemples commentés
   - Résultats attendus

---

## 🎯 Cas d'Usage

### Recherche

- Trouver tous les GenericConcepts d'une catégorie
- Identifier les patterns bicéphales (dual)
- Chercher par mot-clé dans labels/commentaires

### Analyse

- Distribution statistique (catégories, polarités, gaps)
- Qualité du framework (formalisation, validation)
- Évolution temporelle (par année de création)

### Validation

- Vérifier intégrité (tous ont label/catégorie/gap ?)
- Valider nouveau GenericConcept (Processor)
- Cohérence ontologique (rdfs:subClassOf)

### Export

- Extraire sous-graphes (CONSTRUCT)
- Générer CSV pour Excel
- Documentation automatique

---

## ✅ Checklist d'Utilisation

- [ ] Choisir un outil SPARQL (Jena / rdflib / GraphDB / RDF4J)
- [ ] Installer et configurer l'outil
- [ ] Charger M2_GenericConcepts_v15_0_0.jsonld dans le triplestore
- [ ] Exécuter requête de test (Section 1.1 - Liste complète)
- [ ] Vérifier Processor (Section 6.1)
- [ ] Exécuter les analyses qui vous intéressent
- [ ] Adapter les requêtes à vos besoins spécifiques

---

**Bon requêtage SPARQL ! 🚀**

*Echopraxium with the collaboration of Claude AI - TSCG v15.0.0*
