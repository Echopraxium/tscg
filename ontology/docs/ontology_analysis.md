# Analyse des Ontologies TSCG - Namespaces et Chaînage

**Date**: 21 janvier 2026  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Version**: 1.0.0

---

## 🎯 Objectifs de l'Analyse

1. Vérifier les URI dans les ontologies
2. Vérifier l'autoréférencement avec URI dans @context
3. Vérifier le chaînage des prérequis et inclusions
4. Expliquer la stratégie de cohabitation des namespaces M3 (Eagle/Sphinx)

---

## 📊 État Actuel des Ontologies

### Structure Hiérarchique

```
M3_GenesisSpace.jsonld (Racine M3)
    ├── M3_EagleEye.jsonld (ASFID - Territory)
    ├── M3_SphinxEye.jsonld (ORIVE - Map)
    └── [M2_GenericConcepts.jsonld] (dépend de M3_GenesisSpace)
```

---

## ⚠️ Problèmes Identifiés

### 1. **URI Racine Incohérente**

**Problème**: Les fichiers utilisent `https://tscg.org/` mais la documentation spécifie:
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
```

**Fichiers affectés**: TOUS (M3_GenesisSpace, M3_EagleEye, M3_SphinxEye, M2_GenericConcepts)

**Impact**: Les références croisées ne fonctionneront pas correctement.

---

### 2. **Autoréférencement Absent**

**Problème**: Les ontologies n'incluent pas leur propre namespace dans @context

**Exemple actuel**:
```json
"@context": {
    "@vocab": "https://tscg.org/vocab#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "tscg": "https://tscg.org/"
}
```

**Problème**: Pas de namespace spécifique pour M3_EagleEye, M3_SphinxEye, M2_GenericConcepts.

---

### 3. **Chaînage des Imports Incomplet**

**M3_GenesisSpace.jsonld**:
```json
"eagle_eye": {
    "@id": "M3_EagleEye",
    "@type": "owl:imports",
    // ...
}
```

**Problème**: Utilise `"@type": "owl:imports"` mais devrait utiliser `"owl:imports"` comme propriété, pas comme type.

**Structure OWL correcte**:
```json
"owl:imports": [
    "https://raw.githubusercontent.com/.../M3_EagleEye.jsonld",
    "https://raw.githubusercontent.com/.../M3_SphinxEye.jsonld"
]
```

---

### 4. **Référence Mixte dans M2**

**M2_GenericConcepts.jsonld** ligne 44:
```json
"source": {
    "@id": "https://tscg.org/M3_SphinxEye.jsonld",
    "basis": "ORIVE"
}
```

**Problème**: URI absolue incorrecte, devrait être relative au repository GitHub.

---

## ✅ Solution Proposée: Stratégie de Namespaces

### Principe Fondamental

**Cohabitation Eagle/Sphinx**: Utiliser des **namespaces distincts** dans le même espace M3.

```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
    ├── M3_GenesisSpace.jsonld          [namespace: m3genesis]
    ├── M3_EagleEye.jsonld              [namespace: m3eagle]
    ├── M3_SphinxEye.jsonld             [namespace: m3sphinx]
    └── M2_GenericConcepts.jsonld          [namespace: m2]
```

---

### Architecture des Namespaces

#### **1. M3_GenesisSpace.jsonld** (Ontologie fédératrice)

```json
{
  "@context": {
    "m3genesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "m3eagle": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#",
    "m3sphinx": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "m3genesis:M3_GenesisSpace",
  "@type": "owl:Ontology",
  
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld",
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld"
  ],
  
  "metadata": {
    "layer": "M3",
    "name": "Genesis Space - Complete Bicephalous Basis",
    "version": "2.0.0",
    "architecture": "bicephalous",
    "date_created": "2026-01-21",
    "authors": ["Echopraxium with the collaboration of Claude AI"]
  }
}
```

**Avantages**:
- ✅ Namespace propre pour Genesis Space (`m3genesis`)
- ✅ Références explicites à Eagle (`m3eagle`) et Sphinx (`m3sphinx`)
- ✅ Imports OWL corrects avec URIs absolues

---

#### **2. M3_EagleEye.jsonld** (ASFID - Territory)

```json
{
  "@context": {
    "m3eagle": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#",
    "m3genesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "m3eagle:M3_EagleEye",
  "@type": "owl:Ontology",
  
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld"
  ],
  
  "metadata": {
    "layer": "M3",
    "name": "Eagle Eye - ASFID Basis",
    "version": "2.0.0",
    "date_created": "2026-01-21",
    "authors": ["Echopraxium with the collaboration of Claude AI"]
  },
  
  "rdfs:comment": "ASFID basis (Attractor, Structure, Flow, Information, Dynamics) for Territory measurement"
}
```

**Namespace**: `m3eagle`  
**Autoréférence**: `m3eagle:M3_EagleEye`  
**Référence parent**: `m3genesis:M3_GenesisSpace` via `owl:imports`

---

#### **3. M3_SphinxEye.jsonld** (ORIVE - Map)

```json
{
  "@context": {
    "m3sphinx": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#",
    "m3genesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "m3sphinx:M3_SphinxEye",
  "@type": "owl:Ontology",
  
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld"
  ],
  
  "metadata": {
    "layer": "M3",
    "name": "Sphinx Eye - ORIVE Basis",
    "version": "2.0.0",
    "date_created": "2026-01-21",
    "authors": ["Echopraxium with the collaboration of Claude AI"]
  },
  
  "rdfs:comment": "ORIVE basis (Observer, Recurse, Interact, Vary, Emerge) for Map construction"
}
```

**Namespace**: `m3sphinx`  
**Autoréférence**: `m3sphinx:M3_SphinxEye`  
**Référence parent**: `m3genesis:M3_GenesisSpace` via `owl:imports`

---

#### **4. M2_GenericConcepts.jsonld** (Tensor Space)

```json
{
  "@context": {
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m3genesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "m3eagle": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#",
    "m3sphinx": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "m2:M2_GenericConcepts",
  "@type": "owl:Ontology",
  
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld"
  ],
  
  "metadata": {
    "layer": "M2",
    "name": "Tensor Space - GenericConcept Ontology",
    "version": "1.0.0",
    "date_created": "2026-01-21",
    "authors": ["Echopraxium with the collaboration of Claude AI"]
  },
  
  "foundation_layer": {
    "@id": "m3genesis:M3_GenesisSpace",
    "relationship": "derived_from",
    "description": "M2 tensor space is derived from M3 Genesis Space through dual mechanisms"
  }
}
```

**Namespace**: `m2`  
**Autoréférence**: `m2:M2_GenericConcepts`  
**Référence M3**: `m3genesis:M3_GenesisSpace` via `owl:imports`  
**Accès Eagle**: `m3eagle:Attractor`, `m3eagle:Structure`, etc.  
**Accès Sphinx**: `m3sphinx:Observer`, `m3sphinx:Recurse`, etc.

---

## 🔗 Stratégie de Cohabitation des Namespaces

### Principe de Séparation

**Eagle (ASFID)** et **Sphinx (ORIVE)** cohabitent dans M3 via **namespaces distincts**:

```
m3eagle:  # Namespace pour ASFID (Territory)
    - m3eagle:Attractor
    - m3eagle:Structure
    - m3eagle:Flow
    - m3eagle:Information
    - m3eagle:Dynamics

m3sphinx:  # Namespace pour ORIVE (Map)
    - m3sphinx:Observer
    - m3sphinx:Recurse
    - m3sphinx:Interact
    - m3sphinx:Vary
    - m3sphinx:Emerge
```

### Avantages de cette Stratégie

✅ **Clarté conceptuelle**: 
- `m3eagle:` → Territory (ASFID)
- `m3sphinx:` → Map (ORIVE)

✅ **Pas de collision de noms**: 
- Les dimensions ASFID et ORIVE sont dans des namespaces séparés
- Impossible de confondre `m3eagle:Structure` avec `m3sphinx:Structure` (si existait)

✅ **Imports sélectifs**:
```json
// Une ontologie qui ne veut que ASFID:
"owl:imports": ["...M3_EagleEye.jsonld"]

// Une ontologie qui veut les deux:
"owl:imports": ["...M3_GenesisSpace.jsonld"]  // Inclut Eagle + Sphinx
```

✅ **Extensibilité**:
- Ajouter M3_Hydra.jsonld → namespace `m3hydra:`
- Ajouter M3_Phoenix.jsonld → namespace `m3phoenix:`

---

## 📝 Utilisation dans M2

### Référencer les Dimensions ASFID

```json
{
  "@id": "m2:Homeostasis",
  "@type": "m2:GenericConcept",
  "m2:tensorFormula": "A⊗S⊗F",
  "m2:asfidComponents": [
    {
      "@id": "m3eagle:Attractor",
      "role": "Stability attraction"
    },
    {
      "@id": "m3eagle:Structure",
      "role": "Organized arrangement"
    },
    {
      "@id": "m3eagle:Flow",
      "role": "Exchange with environment"
    }
  ]
}
```

### Référencer les Dimensions ORIVE

```json
{
  "@id": "m2:Representation",
  "@type": "m2:GenericConcept",
  "m2:oriveComponents": [
    {
      "@id": "m3sphinx:Observer",
      "role": "Observer-dependent modeling"
    },
    {
      "@id": "m3sphinx:Vary",
      "role": "Multiple possible representations"
    }
  ]
}
```

---

## 🔄 Graphe de Dépendances Corrigé

```
┌─────────────────────────────────────┐
│   M3_GenesisSpace.jsonld           │
│   namespace: m3genesis              │
│   @id: m3genesis:M3_GenesisSpace   │
│                                     │
│   owl:imports:                      │
│     - M3_EagleEye.jsonld           │
│     - M3_SphinxEye.jsonld          │
└──────────┬─────────────┬────────────┘
           │             │
     ┌─────▼──────┐  ┌──▼──────────┐
     │ M3_EagleEye│  │ M3_SphinxEye│
     │ m3eagle:   │  │ m3sphinx:   │
     │ ASFID (5D) │  │ ORIVE (5D)  │
     └─────┬──────┘  └──┬──────────┘
           │             │
           └──────┬──────┘
                  │
         ┌────────▼────────────┐
         │ M2_GenericConcepts.jsonld│
         │ namespace: m2          │
         │ @id: m2:M2_GenericConcepts│
         │                        │
         │ owl:imports:           │
         │   - M3_GenesisSpace    │
         │                        │
         │ References:            │
         │   - m3eagle:* (ASFID)  │
         │   - m3sphinx:* (ORIVE) │
         └────────────────────────┘
```

---

## 📋 Checklist de Corrections

### M3_GenesisSpace.jsonld
- [ ] Corriger URI racine → `https://raw.githubusercontent.com/.../`
- [ ] Ajouter namespace `m3genesis:` dans @context
- [ ] Ajouter namespaces `m3eagle:` et `m3sphinx:` dans @context
- [ ] Corriger `owl:imports` (propriété, pas type)
- [ ] Utiliser URIs absolues pour imports

### M3_EagleEye.jsonld
- [ ] Corriger URI racine → `https://raw.githubusercontent.com/.../`
- [ ] Ajouter autoréférence `m3eagle:` dans @context
- [ ] Ajouter référence `m3genesis:` dans @context
- [ ] Ajouter `owl:imports` de M3_GenesisSpace
- [ ] Changer `@id` → `m3eagle:M3_EagleEye`

### M3_SphinxEye.jsonld
- [ ] Corriger URI racine → `https://raw.githubusercontent.com/.../`
- [ ] Ajouter autoréférence `m3sphinx:` dans @context
- [ ] Ajouter référence `m3genesis:` dans @context
- [ ] Ajouter `owl:imports` de M3_GenesisSpace
- [ ] Changer `@id` → `m3sphinx:M3_SphinxEye`

### M2_GenericConcepts.jsonld
- [ ] Corriger URI racine → `https://raw.githubusercontent.com/.../`
- [ ] Ajouter autoréférence `m2:` dans @context
- [ ] Ajouter namespaces `m3genesis:`, `m3eagle:`, `m3sphinx:` dans @context
- [ ] Corriger ligne 44 : utiliser `m3sphinx:M3_SphinxEye` au lieu de URI absolue incorrecte
- [ ] Changer `@id` → `m2:M2_GenericConcepts`

---

## ✅ Exemple Complet: M3_EagleEye.jsonld Corrigé

```json
{
  "@context": {
    "m3eagle": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#",
    "m3genesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "m3eagle:M3_EagleEye",
  "@type": "owl:Ontology",
  
  "owl:versionInfo": "2.0.0",
  "dcterms:created": "2026-01-21",
  "dcterms:creator": "Echopraxium with the collaboration of Claude AI",
  
  "owl:imports": [
    "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld"
  ],
  
  "rdfs:label": "Eagle Eye - ASFID Basis for Territory Measurement",
  "rdfs:comment": "Orthonormal basis (Attractor, Structure, Flow, Information, Dynamics) for analytical decomposition of reality-as-territory",
  
  "metadata": {
    "layer": "M3",
    "name": "Eagle Eye - ASFID Basis",
    "version": "2.0.0",
    "date_created": "2026-01-21",
    "authors": ["Echopraxium with the collaboration of Claude AI"],
    "description": "ASFID basis for Territory measurement through analytical decomposition"
  },
  
  "parent_ontology": {
    "@id": "m3genesis:M3_GenesisSpace",
    "relationship": "component_of",
    "description": "Eagle Eye is the ASFID component of M3 Genesis Space"
  },
  
  "basis_properties": {
    "name": "ASFID",
    "expansion": "Attractor, Structure, Flow, Information, Dynamics",
    "dimensions": 5,
    "orthonormality": "verified",
    "completeness": "partial (completes with ORIVE)",
    "role": "Territory measurement"
  },
  
  "dimensions": [
    {
      "@id": "m3eagle:Attractor",
      "@type": "owl:NamedIndividual",
      "rdfs:label": "Attractor",
      "m3eagle:symbol": "|A⟩",
      "m3eagle:index": 1,
      "rdfs:comment": "Asymptotic convergence tendency"
    },
    {
      "@id": "m3eagle:Structure",
      "@type": "owl:NamedIndividual",
      "rdfs:label": "Structure",
      "m3eagle:symbol": "|S⟩",
      "m3eagle:index": 2,
      "rdfs:comment": "Topological organization and connectivity"
    },
    {
      "@id": "m3eagle:Flow",
      "@type": "owl:NamedIndividual",
      "rdfs:label": "Flow",
      "m3eagle:symbol": "|F⟩",
      "m3eagle:index": 3,
      "rdfs:comment": "Exchange rate with environment"
    },
    {
      "@id": "m3eagle:Information",
      "@type": "owl:NamedIndividual",
      "rdfs:label": "Information",
      "m3eagle:symbol": "|I⟩",
      "m3eagle:index": 4,
      "rdfs:comment": "State complexity (synchronic)"
    },
    {
      "@id": "m3eagle:Dynamics",
      "@type": "owl:NamedIndividual",
      "rdfs:label": "Dynamics",
      "m3eagle:symbol": "|D⟩",
      "m3eagle:index": 5,
      "rdfs:comment": "Rate of internal change"
    }
  ]
}
```

---

## 📚 Résumé: Cohabitation des Namespaces

### Question Originale
> "Comment on fait cohabiter le namespace M3 pour Eagle et celui pour Sphinx ?"

### Réponse
Les namespaces **ne cohabitent PAS dans le même namespace M3**.

**Solution adoptée**:

1. **M3_GenesisSpace** (`m3genesis:`) = Ontologie fédératrice
   - Importe Eagle ET Sphinx
   - Déclare les deux namespaces dans @context

2. **M3_EagleEye** (`m3eagle:`) = Namespace ASFID distinct
   - Dimensions Territory: `m3eagle:Attractor`, `m3eagle:Structure`, etc.

3. **M3_SphinxEye** (`m3sphinx:`) = Namespace ORIVE distinct
   - Dimensions Map: `m3sphinx:Observer`, `m3sphinx:Recurse`, etc.

**Principe**:
```
m3genesis: (container)
    ├── m3eagle: (ASFID - Territory)
    └── m3sphinx: (ORIVE - Map)
```

**Analogie**:
- Comme RDF et RDFS cohabitent via namespaces distincts
- Comme OWL et SKOS cohabitent via namespaces distincts
- **Eagle et Sphinx cohabitent via namespaces distincts**

**Avantage majeur**: Clarté conceptuelle immédiate dans les références:
```json
m3eagle:Attractor  → "C'est du Territory (ASFID)"
m3sphinx:Observer  → "C'est du Map (ORIVE)"
```

---

## 🎯 Conclusion

**État actuel**: ❌ URIs incorrects, autoréférencement manquant, imports mal formés

**État cible**: ✅ URIs GitHub corrects, namespaces distincts (m3genesis/m3eagle/m3sphinx/m2), imports OWL standards

**Bénéfices**:
- ✅ Interopérabilité avec outils RDF/OWL
- ✅ Clarté conceptuelle (Eagle vs Sphinx)
- ✅ Extensibilité (ajouter nouvelles perspectives)
- ✅ Standards W3C respectés

---

**FIN DU DOCUMENT D'ANALYSE**
