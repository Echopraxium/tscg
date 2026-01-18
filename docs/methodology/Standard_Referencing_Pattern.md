# Mécanisme de Référencement Standard - Ontologies TSCG

**Date**: 2026-01-17  
**Correction**: Architecture de référencement  
**Pattern**: rdfs:seeAlso + dcterms:documentation

---

## ❌ Problème Identifié

Utilisation d'une propriété custom `m0:file` pour référencer les ontologies spécialisées :

```json
{
  "@id": "m0:RGB_Additive",
  "rdfs:label": "RGB Additive Color Synthesis",
  "m0:file": "./M0_RGB_Additive.jsonld",  // ❌ Propriété non-standard
  ...
}
```

**Problèmes** :
- Propriété custom (pas standard Linked Data)
- Inconsistent avec le reste du framework TSCG
- Pas de métadonnées sur le type de ressource

---

## ✅ Solution : Pattern Standard M2→M3

Utiliser le **même mécanisme** que M2 utilise pour référencer M3 :

### Pattern M2→M3 (référence)

```json
{
  "@id": "m2:Synergy",
  "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/docs/TSCG_M2_MetaConcepts_Ontology_README.md",
  "dcterms:documentation": {
    "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/docs/TSCG_M2_MetaConcepts_Ontology_README.md",
    "dcterms:format": "text/markdown",
    "dcterms:type": "Documentation"
  }
}
```

### Pattern ColorSynthesis (corrigé)

```json
{
  "@id": "m0:RGB_Additive",
  "rdfs:label": "RGB Additive Color Synthesis",
  "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld",
  "dcterms:documentation": {
    "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld",
    "dcterms:format": "application/ld+json",
    "dcterms:type": "Ontology"
  },
  "m0:principle": "Additive (light-based)",
  "m0:components": 3,
  ...
}
```

---

## Avantages du Pattern Standard

### 1. Cohérence

✅ Même mécanisme partout dans TSCG :
- M2 → M3 : `rdfs:seeAlso`
- M0_Federated → M0_Specialized : `rdfs:seeAlso`
- Fire Triangle → RGB (cross-poclets) : `rdfs:seeAlso`

### 2. Standards Linked Data

✅ Utilise vocabulaires RDF/OWL standards :
- `rdfs:seeAlso` : Propriété standard RDF Schema
- `dcterms:documentation` : Dublin Core Terms
- `dcterms:format` : Type MIME standard
- `dcterms:type` : Type de ressource

### 3. Métadonnées Riches

✅ Plus d'information sur la ressource :
```json
"dcterms:documentation": {
  "@id": "https://...",           // URL complète
  "dcterms:format": "application/ld+json",  // Type MIME
  "dcterms:type": "Ontology"      // Nature de la ressource
}
```

### 4. URLs Absolues

✅ URLs complètes (pas relatives) :
- ✅ `https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld`
- ❌ `./M0_RGB_Additive.jsonld`

**Avantage** : Liens fonctionnent partout (même hors contexte du repository)

---

## Application au Poclet ColorSynthesis

### Ontologie Fédératrice Corrigée

`M0_ColorSynthesis_Federated.jsonld` :

```json
{
  "@id": "m0:ColorSynthesisFederated",
  "m0:federatedInstances": [
    {
      "@id": "m0:RGB_Additive",
      "rdfs:label": "RGB Additive Color Synthesis",
      "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld",
      "dcterms:documentation": {
        "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld",
        "dcterms:format": "application/ld+json",
        "dcterms:type": "Ontology"
      },
      "m0:principle": "Additive (light-based)",
      "m0:components": 3,
      "m0:medium": "Light emission (screens, projectors)",
      "m0:primaries": ["Red", "Green", "Blue"]
    },
    {
      "@id": "m0:HSL_Additive",
      "rdfs:label": "HSL Additive Color Synthesis",
      "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_HSL_Additive.jsonld",
      "dcterms:documentation": {
        "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_HSL_Additive.jsonld",
        "dcterms:format": "application/ld+json",
        "dcterms:type": "Ontology"
      },
      "m0:principle": "Additive (light-based, perceptual)",
      "m0:components": 3,
      "m0:medium": "Light emission (alternative representation)",
      "m0:primaries": ["Hue", "Saturation", "Lightness"]
    },
    {
      "@id": "m0:CMY_Subtractive",
      "rdfs:label": "CMY Subtractive Color Synthesis",
      "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_CMY_Subtractive.jsonld",
      "dcterms:documentation": {
        "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_CMY_Subtractive.jsonld",
        "dcterms:format": "application/ld+json",
        "dcterms:type": "Ontology"
      },
      "m0:principle": "Subtractive (pigment-based)",
      "m0:components": 3,
      "m0:medium": "Pigments (theoretical model)",
      "m0:primaries": ["Cyan", "Magenta", "Yellow"]
    },
    {
      "@id": "m0:CMYK_Subtractive",
      "rdfs:label": "CMYK Subtractive Color Synthesis",
      "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_CMYK_Subtractive.jsonld",
      "dcterms:documentation": {
        "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_CMYK_Subtractive.jsonld",
        "dcterms:format": "application/ld+json",
        "dcterms:type": "Ontology"
      },
      "m0:principle": "Subtractive (pigment-based, practical)",
      "m0:components": 4,
      "m0:medium": "Inks (printing industry)",
      "m0:primaries": ["Cyan", "Magenta", "Yellow", "Key (Black)"]
    }
  ]
}
```

---

## Pattern Général pour Poclets Fédératifs

### Template Ontologie Fédératrice

```json
{
  "@id": "m0:{PocletName}Federated",
  "@type": "owl:Ontology",
  "dcterms:title": "{Poclet Name} - Federated Ontology",
  "m0:pocletType": "Federated",
  "m0:federatedInstances": [
    {
      "@id": "m0:{Variant1}",
      "rdfs:label": "{Variant 1 Label}",
      "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet_name}/M0_{Variant1}.jsonld",
      "dcterms:documentation": {
        "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet_name}/M0_{Variant1}.jsonld",
        "dcterms:format": "application/ld+json",
        "dcterms:type": "Ontology"
      },
      "m0:{property1}": "...",
      "m0:{property2}": "..."
    },
    {
      "@id": "m0:{Variant2}",
      ...
    }
  ]
}
```

### Template Ontologie Spécialisée (référence arrière)

```json
{
  "@id": "m0:{Variant1}",
  "@type": "owl:NamedIndividual",
  "rdfs:label": "{Variant 1 Label}",
  "m0:partOfFederation": {
    "@id": "m0:{PocletName}Federated",
    "rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet_name}/M0_{PocletName}_Federated.jsonld",
    "dcterms:documentation": {
      "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet_name}/M0_{PocletName}_Federated.jsonld",
      "dcterms:format": "application/ld+json",
      "dcterms:type": "Ontology"
    }
  },
  ...
}
```

---

## Autres Types de Références

### Documentation (Markdown, HTML)

```json
"rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet}/docs/README.md",
"dcterms:documentation": {
  "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet}/docs/README.md",
  "dcterms:format": "text/markdown",
  "dcterms:type": "Documentation"
}
```

### Ontologies (JSON-LD, RDF/XML, Turtle)

```json
"rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/{path}/{file}.jsonld",
"dcterms:documentation": {
  "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/{path}/{file}.jsonld",
  "dcterms:format": "application/ld+json",
  "dcterms:type": "Ontology"
}
```

### Images, Diagrammes

```json
"rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet}/diagrams/{image}.png",
"dcterms:documentation": {
  "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/{poclet}/diagrams/{image}.png",
  "dcterms:format": "image/png",
  "dcterms:type": "Image"
}
```

---

## Corrections Appliquées

### Fichier : M0_ColorSynthesis_Federated.jsonld

✅ **AVANT** (propriété custom) :
```json
"m0:file": "./M0_RGB_Additive.jsonld"
```

✅ **APRÈS** (standard Linked Data) :
```json
"rdfs:seeAlso": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld",
"dcterms:documentation": {
  "@id": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/color_synthesis/M0_RGB_Additive.jsonld",
  "dcterms:format": "application/ld+json",
  "dcterms:type": "Ontology"
}
```

**Appliqué aux 4 variants** :
- ✅ RGB_Additive
- ✅ HSL_Additive
- ✅ CMY_Subtractive
- ✅ CMYK_Subtractive

---

## Bénéfices Architecturaux

### 1. Interopérabilité Linked Data

Les URLs sont **déréférençables** :
- Clic sur l'URL → Accès direct au fichier
- Parsers RDF peuvent suivre les liens automatiquement
- Intégration avec d'autres ontologies facilitée

### 2. Cohérence Framework

**Un seul pattern** pour toutes les références :
- M3 → M2 : `rdfs:seeAlso`
- M2 → M1 : `rdfs:seeAlso`
- M1 → M0 : `rdfs:seeAlso`
- M0_Federated → M0_Variants : `rdfs:seeAlso`

### 3. Machine-Readable

Les métadonnées sont **structurées** :
```json
"dcterms:format": "application/ld+json"  // → Parser sait que c'est du JSON-LD
"dcterms:type": "Ontology"               // → Nature de la ressource
```

### 4. Extensibilité

Facile d'ajouter métadonnées :
```json
"dcterms:documentation": {
  "@id": "...",
  "dcterms:format": "application/ld+json",
  "dcterms:type": "Ontology",
  "dcterms:creator": "TSCG Project",      // Créateur
  "dcterms:created": "2026-01-17",        // Date de création
  "dcterms:version": "1.0.0"              // Version
}
```

---

## Recommandation Générale

**Pour TOUS les futurs poclets et ontologies TSCG** :

1. ✅ Toujours utiliser `rdfs:seeAlso` pour les références
2. ✅ Toujours ajouter `dcterms:documentation` avec métadonnées
3. ✅ Toujours utiliser URLs **absolues** (pas relatives)
4. ✅ Toujours spécifier `dcterms:format` (type MIME)
5. ✅ Toujours spécifier `dcterms:type` (nature ressource)

---

## Validation

### Checklist Référencement

- ✅ `rdfs:seeAlso` présent (propriété standard)
- ✅ URL absolue (commence par `https://`)
- ✅ `dcterms:documentation` présent
- ✅ `dcterms:format` correct (application/ld+json, text/markdown, etc.)
- ✅ `dcterms:type` correct (Ontology, Documentation, Image, etc.)
- ❌ Pas de propriété custom (m0:file, m0:link, etc.)

### Exemple Validation Ontologie Fédératrice

```json
{
  "m0:federatedInstances": [
    {
      "@id": "m0:Variant1",
      "rdfs:seeAlso": "https://...",              // ✅
      "dcterms:documentation": {                  // ✅
        "@id": "https://...",                     // ✅ URL absolue
        "dcterms:format": "application/ld+json",  // ✅
        "dcterms:type": "Ontology"                // ✅
      }
    }
  ]
}
```

---

**END OF DOCUMENTATION**

**Pattern Standard de Référencement** : ✅ Validé et appliqué

**Cohérence avec M2→M3** : ✅ Garantie

**Tous futurs poclets** : Doivent utiliser ce pattern ✅
