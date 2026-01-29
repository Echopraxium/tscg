# 🏗️ Proposition: Propriété m2:ontologyCategory

**Version:** 1.0.0  
**Date:** January 25, 2026  
**Author:** Echopraxium with the collaboration of Claude AI  
**Status:** Proposition pour intégration dans M2_MetaConcepts.jsonld

---

## 📋 Problème Identifié

### Situation Actuelle (Incorrecte)

Les identifiants d'ontologies incluent des suffixes redondants qui polluent la sémantique :

```json
"@id": "m0:yggdrasil:Yggdrasil_Poclet"
"@id": "m0:fire_triangle:FireTriangle_Ontology"
"@id": "m0:tpack:M0_TPACK_Ontology"
```

❌ **Problèmes :**
- Le suffixe `_Poclet` / `_Ontology` n'apporte aucune information sémantique
- Pollue l'identifiant qui devrait représenter l'entité, pas sa catégorie
- Mélange identité et métadonnées
- Viole le principe de séparation des préoccupations

---

## ✅ Solution Proposée

### Séparation Identité vs Catégorie

**Identifiant propre :**
```json
"@id": "m0:yggdrasil:Yggdrasil"
```

**Catégorisation explicite :**
```json
"m2:ontologyCategory": "Poclet"
```

✅ **Avantages :**
- Identifiants sémantiquement purs
- Catégorisation formelle et interrogeable
- Extensible (peut évoluer avec le framework)
- Cohérent avec OWL best practices

---

## 🎯 Définition de la Propriété

### Ajout à M2_MetaConcepts.jsonld

```json
{
  "@id": "m2:ontologyCategory",
  "@type": "owl:DatatypeProperty",
  "rdfs:label": "Ontology Category",
  "rdfs:comment": "Categorizes ontologies by their architectural role in the TSCG framework hierarchy. This property provides formal metadata about the layer position and purpose of each ontology, enabling systematic organization and querying of the framework structure.",
  "rdfs:domain": "owl:Ontology",
  "rdfs:range": "xsd:string",
  "owl:functionalProperty": true,
  "skos:note": "This is a framework-level architectural property, not a domain-specific classification. It describes WHERE an ontology sits in the M3→M2→M1→M0 hierarchy, not WHAT domain it covers.",
  
  "m2:allowedValues": [
    {
      "value": "FoundationalBasis",
      "description": "M3 layer - Provides complete orthogonal basis (Genesis Space, Eagle Eye, Sphinx Eye)",
      "examples": ["M3_GenesisSpace", "M3_EagleEye", "M3_SphinxEye"]
    },
    {
      "value": "UniversalPattern",
      "description": "M2 layer - Defines transdisciplinary systemic patterns from M3 tensor products",
      "examples": ["M2_MetaConcepts"]
    },
    {
      "value": "DomainExtension",
      "description": "M1 layer - Domain-specific concept collections bridging M2 and M0",
      "examples": ["M1_CoreConcepts", "M1_Biology", "M1_Optics", "M1_Photography"]
    },
    {
      "value": "Poclet",
      "description": "M0 layer - Proof-of-concept instances validating M2 metaconcepts through minimal complete systems",
      "examples": ["M0_Yggdrasil", "M0_FireTriangle", "M0_TPACK"]
    }
  ],
  
  "m2:usage": {
    "when_to_use": "REQUIRED for all TSCG ontology files (M3, M2, M1, M0)",
    "where_in_file": "Inside the owl:Ontology node metadata section",
    "cardinality": "Exactly one value per ontology (owl:functionalProperty)"
  },
  
  "m2:rationale": {
    "architectural": "Enables systematic queries like 'find all Poclets' or 'list all DomainExtensions'",
    "semantic": "Keeps @id clean and semantically meaningful",
    "extensibility": "Framework can evolve categories without breaking existing ontologies",
    "queryability": "SPARQL queries can filter ontologies by category"
  },
  
  "dcterms:created": "2026-01-25",
  "dcterms:creator": "Echopraxium with the collaboration of Claude AI"
}
```

---

## 📖 Usage dans les Ontologies

### M3 Layer (Foundational Basis)

**M3_GenesisSpace.jsonld:**
```json
{
  "@id": "m3:genesis:GenesisSpace",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "FoundationalBasis",
  "dcterms:title": "TSCG M3 Genesis Space",
  ...
}
```

**M3_EagleEye.jsonld:**
```json
{
  "@id": "m3:eagle_eye:EagleEye",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "FoundationalBasis",
  "dcterms:title": "TSCG M3 Eagle Eye - ASFID Basis",
  ...
}
```

### M2 Layer (Universal Patterns)

**M2_MetaConcepts.jsonld:**
```json
{
  "@id": "m2:MetaConcepts",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "UniversalPattern",
  "dcterms:title": "TSCG M2 Metaconcepts",
  ...
}
```

### M1 Layer (Domain Extensions)

**M1_CoreConcepts.jsonld:**
```json
{
  "@id": "m1:core:CoreConcepts",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "DomainExtension",
  "dcterms:title": "TSCG M1 Core Concepts",
  ...
}
```

**M1_Biology.jsonld:**
```json
{
  "@id": "m1:biology:Biology",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "DomainExtension",
  "dcterms:title": "TSCG M1 Biology Extension",
  ...
}
```

### M0 Layer (Poclets)

**M0_Yggdrasil.jsonld:**
```json
{
  "@id": "m0:yggdrasil:Yggdrasil",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "Poclet",
  "dcterms:title": "Yggdrasil - Norse Cosmological Tree",
  ...
}
```

**M0_FireTriangle.jsonld:**
```json
{
  "@id": "m0:fire_triangle:FireTriangle",
  "@type": "owl:Ontology",
  "m2:ontologyCategory": "Poclet",
  "dcterms:title": "Fire Triangle - Combustion System",
  ...
}
```

---

## 🔍 Exemples de Requêtes SPARQL

### Trouver tous les Poclets

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?ontology ?title
WHERE {
  ?ontology a owl:Ontology ;
            m2:ontologyCategory "Poclet" ;
            dcterms:title ?title .
}
ORDER BY ?title
```

### Compter les ontologies par catégorie

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?category (COUNT(?ontology) AS ?count)
WHERE {
  ?ontology a owl:Ontology ;
            m2:ontologyCategory ?category .
}
GROUP BY ?category
ORDER BY ?category
```

### Lister toutes les extensions de domaine

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?ontology ?title ?created
WHERE {
  ?ontology a owl:Ontology ;
            m2:ontologyCategory "DomainExtension" ;
            dcterms:title ?title ;
            dcterms:created ?created .
}
ORDER BY ?created
```

---

## ✅ Validation et Checklist

### Checklist pour Adoption

- [ ] Ajouter la définition de `m2:ontologyCategory` dans M2_MetaConcepts.jsonld
- [ ] Mettre à jour le validateur TSCG pour vérifier cette propriété
- [ ] Ajouter `m2:ontologyCategory` à tous les fichiers M3 existants
- [ ] Ajouter `m2:ontologyCategory` à M2_MetaConcepts.jsonld
- [ ] Ajouter `m2:ontologyCategory` à tous les fichiers M1 existants
- [ ] Ajouter `m2:ontologyCategory` à tous les poclets M0 (✅ FAIT)
- [ ] Mettre à jour les templates d'ontologies
- [ ] Documenter dans le guide des standards TSCG
- [ ] Ajouter des exemples dans la documentation

---

## 📊 Impact et Bénéfices

### Bénéfices Immédiats

1. **Propreté sémantique** : Identifiants ne contiennent que l'essence de l'entité
2. **Interrogeabilité** : Requêtes SPARQL simples pour filtrer par catégorie
3. **Maintenance** : Catégorie changeable sans modifier l'@id
4. **Documentation** : Auto-documentation du rôle architectural

### Bénéfices Long Terme

1. **Évolutivité** : Nouvelles catégories ajoutables sans casser l'existant
2. **Outillage** : Générateurs de documentation, visualisations, etc.
3. **Validation** : Vérification automatique de la cohérence architecturale
4. **Pédagogie** : Facilite la compréhension de la structure TSCG

---

## 🔄 Migration

### Étape 1 : Ajouter la Propriété à M2

Insérer la définition complète de `m2:ontologyCategory` dans M2_MetaConcepts.jsonld.

### Étape 2 : Mettre à Jour les Ontologies Existantes

- M3 (3 fichiers)
- M2 (1 fichier)
- M1 (6+ fichiers)
- M0 (16 fichiers) ✅ **DÉJÀ FAIT**

### Étape 3 : Mettre à Jour le Validateur

Ajouter une règle de validation :
```python
# Vérifier que owl:Ontology a m2:ontologyCategory
if item.get("@type") == "owl:Ontology":
    if "m2:ontologyCategory" not in item:
        self.errors.append("❌ Missing required m2:ontologyCategory")
```

### Étape 4 : Mettre à Jour les Templates

Tous les templates d'ontologies doivent inclure `m2:ontologyCategory`.

---

## 📝 Conclusion

L'ajout de `m2:ontologyCategory` est une amélioration architecturale majeure qui :

- ✅ Sépare identité et métadonnées
- ✅ Améliore la maintenabilité
- ✅ Facilite l'interrogation et l'analyse
- ✅ Renforce la cohérence du framework
- ✅ Suit les best practices OWL/RDF

**Recommandation : ADOPTER** cette propriété dans M2_MetaConcepts.jsonld.

---

**Document Maintainer:** Echopraxium with the collaboration of Claude AI  
**Last Updated:** January 25, 2026
