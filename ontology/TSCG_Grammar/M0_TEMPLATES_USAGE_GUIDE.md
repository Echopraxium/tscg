# Guide d'Utilisation des Templates M0 TSCG

**Auteur:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-04-18  
**Version:** 1.0.0

## 📦 Templates Disponibles

1. **`M0_CONTEXT_TEMPLATE.json`** - Template de `@context` standard avec tous les namespaces et typages float
2. **`M0_POCLET_TEMPLATE.jsonld`** - Template complet de poclet M0 prêt à l'emploi

## 🎯 Utilisation pour Créer un Nouveau Poclet

### Étape 1 : Copier le Template

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\poclets

# Créer le répertoire du nouveau poclet (PascalCase, 1-4 mots)
mkdir NewPocletName

# Copier le template
copy ..\..\..\..\M0_POCLET_TEMPLATE.jsonld NewPocletName\M0_NewPocletName.jsonld
```

### Étape 2 : Personnaliser les Métadonnées

Ouvre `M0_NewPocletName.jsonld` et modifie :

#### A. Identité du Poclet
```json
"@id": "",  // Laisser vide (utilise @base)
"rdfs:label": "NewPocletName - Short Descriptive Title",
"rdfs:comment": "Detailed description explaining the system modeled...",
"dcterms:created": "2026-04-18",  // Date du jour
```

#### B. Domaine
```json
"m1:domain": "DomainName",  // Ex: "Chemistry", "Physics", "Biology"
```

Pour multi-domaine :
```json
"m1:domain": ["Domain1", "Domain2"],
```

#### C. Extensions M1 (si nécessaire)

Si ton poclet utilise des concepts spécifiques à un domaine, ajoute le namespace dans `@context` :

```json
"@context": {
  // ... namespaces existants ...
  "m1bio": "M1_extensions/biology/M1_Biology.jsonld#",
  "m1chem": "M1_extensions/chemistry/M1_Chemistry.jsonld#"
}
```

Et dans `owl:imports` :
```json
"owl:imports": [
  "M3_GenesisSpace.jsonld",
  "M2_GenericConcepts.jsonld",
  "M1_CoreConcepts.jsonld",
  "M1_extensions/biology/M1_Biology.jsonld"
]
```

### Étape 3 : Scores ASFID/REVOI

#### A. Calcul des Scores (voir méthodologie TSCG)

Évalue chaque dimension sur [0.0, 1.0] selon les critères TSCG.

#### B. Remplir les Scores
```json
"m0:asfidScores": {
  "eagle_eye:Attractor": 0.75,     // [0.0-1.0]
  "eagle_eye:Structure": 0.90,     // [0.0-1.0]
  "eagle_eye:Flow": 0.60,           // [0.0-1.0] (0=Stase OK)
  "eagle_eye:Information": 0.80,   // [0.0-1.0]
  "eagle_eye:Dynamics": 0.50,      // [0.0-1.0]
  "m0:mean": 0.71,                  // Moyenne calculée
  "m0:justification": "Justification détaillée..."
}
```

**IMPORTANT:** Les scores sont automatiquement typés `xsd:float` grâce au `@context` !

#### C. Calcul de l'Epistemic Gap

Utilise la formule δ₁ (voir documentation TSCG) :

```json
"m0:epistemicGap": 0.474  // Résultat de δ₁
```

### Étape 4 : Modéliser les Composants

```json
"m0:components": [
  {
    "@id": "m0:Oxygen",
    "@type": "m0:PocletComponent",
    "rdfs:label": "Oxygen (O₂)",
    "rdfs:comment": "Comburant - enables combustion",
    "m2:genericConcept": { "@id": "m2:Reagent" }
  },
  {
    "@id": "m0:Fuel",
    "@type": "m0:PocletComponent",
    "rdfs:label": "Fuel",
    "rdfs:comment": "Combustible material",
    "m2:genericConcept": { "@id": "m2:Reagent" }
  }
]
```

**Concepts Génériques M2 :** Utilise les 75 GenericConcepts de `M2_GenericConcepts.jsonld`

### Étape 5 : Modéliser les Interactions

```json
"m0:interactions": [
  {
    "@id": "m0:CombustionReaction",
    "@type": "m0:PocletInteraction",
    "rdfs:label": "Combustion Reaction",
    "rdfs:comment": "Exothermic oxidation reaction",
    "m0:source": { "@id": "m0:Oxygen" },
    "m0:target": { "@id": "m0:Fuel" },
    "m2:genericConcept": { "@id": "m2:Reaction" }
  }
]
```

### Étape 6 : Validation SHACL

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg

pyshacl -s ontology/M0_Instances_Schema.shacl.ttl ^
        -df json-ld ^
        instances/poclets/NewPocletName/M0_NewPocletName.jsonld
```

**Résultat attendu:** `Conforms: True`

## ✅ Checklist de Validation

Avant de considérer le poclet comme terminé :

- [ ] `@context` contient tous les namespaces nécessaires
- [ ] Toutes les propriétés float ont `"@type": "xsd:float"` dans le @context
- [ ] `@type: owl:Ontology` (jamais `owl:NamedIndividual`)
- [ ] `m3:ontologyType: m3:Poclet` (jamais `m2:ontologyCategory`)
- [ ] `rdfs:label` et `rdfs:comment` (pas `dcterms:title/description`)
- [ ] `owl:versionInfo` en semver (pas `m0:version`)
- [ ] `dcterms:creator` = "Echopraxium with the collaboration of Claude AI"
- [ ] `m1:domain` défini (pas `m0:domain`)
- [ ] Scores ASFID/REVOI entre 0.0 et 1.0
- [ ] REVOI suit l'ordre R-E-V-O-I (pas ORIVE)
- [ ] Changelog au format array (max 3 entrées)
- [ ] Validation SHACL passe sans erreur

## 🔧 Dépannage

### Erreur : "Value Node: xsd:double"
→ Le `@context` n'a pas les définitions `@type: xsd:float`. Utilise `M0_CONTEXT_TEMPLATE.json` comme référence.

### Erreur : "FORBIDDEN: Use rdfs:label instead of dcterms:title"
→ Utilise `rdfs:label` et `rdfs:comment`, pas les propriétés `dcterms:`.

### Erreur : "m3:ontologyType MUST be one of..."
→ Utilise `"m3:ontologyType": {"@id": "m3:Poclet"}`, pas `m2:ontologyCategory`.

## 📚 Ressources

- **M3_GenesisSpace.jsonld** - Définitions ASFID/REVOI
- **M2_GenericConcepts.jsonld** - 75 concepts génériques (9 familles)
- **M1_CoreConcepts.jsonld** - Combos de concepts
- **M0_Instances_Schema.shacl.ttl** - Schéma de validation
- **M0_FireTriangle.jsonld** - Poclet de référence canonique

## 💡 Bonnes Pratiques

1. **Nommage :** PascalCase, 1-4 mots, descriptif (ex: `FireTriangle`, `FourStrokeEngine`)

2. **Structure de fichiers :**
   ```
   instances/poclets/PocletName/
   ├── M0_PocletName.jsonld
   ├── M0_PocletName.html (simulation)
   └── README.md (optionnel)
   ```

3. **Versionning :** Semantic versioning (1.0.0 → 1.1.0 → 2.0.0)

4. **Changelog :** Maximum 3 entrées, la plus récente en premier

5. **Encodage :** UTF-8 obligatoire, `ensure_ascii=False` en Python

6. **Justifications :** Sois précis et technique, cite les sources si applicable

## 🚀 Raccourci

Pour créer rapidement un nouveau poclet :

```bash
# Script PowerShell (à créer)
.\create_new_poclet.ps1 -Name "NewPocletName" -Domain "Physics"
```

Ce script pourrait automatiquement :
- Créer le répertoire
- Copier le template
- Remplacer les placeholders
- Ouvrir le fichier dans l'éditeur
