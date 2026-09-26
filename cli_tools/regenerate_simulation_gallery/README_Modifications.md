# Script generate_index.js — Version Finale avec Double Filtrage

## 🎯 Objectif

Combiner **deux systèmes de filtrage** qui fonctionnent ensemble (logique AND) :
1. **Ontology Type** : Sélecteur pour Poclets / Systemic Frameworks / Symbolic System Grammars
2. **Tags** : Sélection multiple de tags basée sur les domaines (existant)

## ✅ Modifications Appliquées

### 1. **Structure de Découverte Multi-Dossiers**

Le script scanne maintenant **3 dossiers** :
```
instances/
├── poclets/                      → Poclets
├── systemic-frameworks/          → Systemic Frameworks  
└── symbolic-system-grammars/     → Symbolic System Grammars
```

Chaque instance reçoit automatiquement :
- `ontologyType` : `'poclets'`, `'systemic-frameworks'`, ou `'symbolic-system-grammars'`
- `ontologyTypeLabel` : `'Poclets'`, `'Systemic Frameworks'`, ou `'Symbolic System Grammars'`

### 2. **Parsing JSON-LD Corrigé**

**Problème résolu** : Le domaine (`m1:domain`) est dans le nœud `owl:Ontology`, pas dans le nœud instance !

```javascript
// Structure typique
{
  "@graph": [
    {
      "@type": "owl:Ontology",           // ← Métadonnées ici
      "m1:domain": ["Economics"],         // ← DOMAINE ICI !
      "rdfs:label": "...",
      "m3:ontologyType": { "@id": "m3:Poclet" }
    },
    {
      "@type": "owl:NamedIndividual",    // ← Instance ici
      "m0:asfidScores": { ... },          // ← Scores ici
      "m0:revoiScores": { ... }
    }
  ]
}
```

**Nouvelle logique** :
1. Cherche `owl:Ontology` → lit `m1:domain` (tableau) → joint avec "/"
2. Cherche le nœud instance → scores ASFID/REVOI, gap, label
3. Fallback : si pas de domaine dans ontology, cherche dans instance
4. Support aussi `m0:domain` (compatibilité)

### 3. **Interface HTML Modifiée**

**Section de filtrage** (sans le label "Filter by Tags") :

```html
<!-- Ontology Type (nouveau) -->
<div class="type-filter-section">
  <div class="type-filter-label">📂 Ontology Type</div>
  <select id="ontology-type-select">
    <option value="">— All Types —</option>
    <option value="poclets">Poclets</option>
    <option value="systemic-frameworks">Systemic Frameworks</option>
    <option value="symbolic-system-grammars">Symbolic System Grammars</option>
  </select>
</div>

<!-- Tags (existant, SANS le label "🏷️ Filter by Tags") -->
<div class="tag-filter-section">
  <select id="tag-select">
    <option value="">— Select a tag —</option>
  </select>
  <button id="clear-tags-btn">✕</button>
  <div id="selected-tags">
    <!-- Pilules de tags colorées -->
  </div>
</div>
```

### 4. **Logique de Filtrage Combinée (AND)**

Les deux filtres fonctionnent ensemble avec une **logique AND** :

```javascript
function filterPoclets() {
  items.forEach(item => {
    const poclet = POCLETS.find(p => p.id === item.dataset.id);
    
    // Filtre 1 : Type d'ontologie
    let matchesType = true;
    if (selectedOntologyType !== '') {
      matchesType = (poclet.ontologyType === selectedOntologyType);
    }
    
    // Filtre 2 : Tags
    let matchesTags = true;
    if (selectedTags.size > 0) {
      matchesTags = Array.from(selectedTags).some(tag => 
        poclet.domain.toLowerCase().includes(tag.toLowerCase())
      );
    }
    
    // Visible si TOUS LES DEUX correspondent
    if (matchesType && matchesTags) {
      item.classList.remove('filtered');
      visibleCount++;
    } else {
      item.classList.add('filtered');
    }
  });
}
```

### 5. **Navigation Clavier Mise à Jour**

Les touches ↑↓ et Entrée tiennent compte des **deux filtres actifs**.

## 📊 Exemples d'Usage

### Exemple 1 : Voir tous les Poclets
- **Ontology Type** : `Poclets`
- **Tags** : aucun
- **Résultat** : 24 poclets affichés

### Exemple 2 : Poclets de chimie/physique
- **Ontology Type** : `Poclets`
- **Tags** : `Chemistry`, `Physics`
- **Résultat** : FireTriangle, PhaseTransition

### Exemple 3 : Tout ce qui concerne l'électronique
- **Ontology Type** : `All Types`
- **Tags** : `Electronics`
- **Résultat** : Transistor, Vco (poclets) + potentiellement d'autres types

### Exemple 4 : Systemic Frameworks uniquement
- **Ontology Type** : `Systemic Frameworks`
- **Tags** : aucun
- **Résultat** : Triz, VSM (si disponibles)

## 🔧 Fichiers Livrés

### 1. `generate_index_final.js`
Script complet avec :
- ✅ Découverte multi-dossiers (3 types d'ontologie)
- ✅ Parsing JSON-LD corrigé (`m1:domain` depuis `owl:Ontology`)
- ✅ Double filtrage (Type + Tags, logique AND)
- ✅ Interface sans label "Filter by Tags"
- ✅ Navigation clavier adaptée
- ✅ CSS pour les deux sections de filtrage

### 2. `M0_Vco.jsonld`
Fichier corrigé avec :
- ✅ Virgule finale supprimée (erreur JSON critique)
- ✅ Référence du contexte mise à jour (`M0_Vco.jsonld#`)
- ✅ Domaine détectable : `Music/Electronics/Modular Synthesis`

## 🎨 Interface Générée

```
┌─────────────────────────────────────────┐
│ TSCG — Instance Gallery                 │
├─────────────────────────────────────────┤
│ 📂 Ontology Type                        │
│ [— All Types —         ▼]               │
├─────────────────────────────────────────┤
│ [— Select a tag — ▼] [✕]                │
│ ┌─────────────────────────────────────┐ │
│ │ No tags selected                    │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ Showing 26 of 26 instances              │
├─────────────────────────────────────────┤
│ ▸ Color Synthesis                       │
│ ▸ Counterpoint                          │
│ ▸ Exposure Triangle                     │
│ ...                                     │
└─────────────────────────────────────────┘
```

## 📝 Domaines Maintenant Trouvés

Tous les domaines sont maintenant correctement détectés :

| Instance | Domaine |
|----------|---------|
| **KindlebergerMinsky** | `Economics` |
| **MtgColorWheel** | `Game Theory/Trading Card Games/Strategic Games` |
| **PhaseTransition** | `Chemistry/Physics` |
| **TrophicPyramid** | `Ecology/Biology/Trophodynamics/Population Dynamics/Thermodynamics of Ecosystems` |
| **Vco** | `Music/Electronics/Modular Synthesis` |
| **Triz** | `Systems Theory/Systems Thinking` |
| **ExposureTriangle** | `Photography/Optics/Image Formation` |
| **Transistor** | `Electronics/Semiconductor Physics/Analog Electronics/Signal Processing/Circuit Theory` |

Plus aucun `[?]` ne devrait apparaître ! ✅

## 🚀 Utilisation

```bash
# Génération
node generate_index_final.js

# Avec URL de site
node generate_index_final.js --site-url https://echopraxium.github.io/tscg

# Sortie personnalisée
node generate_index_final.js --output /tmp/gallery.html
```

## 🎯 Points Clés

1. **Double filtrage** : Type d'ontologie ET tags (logique AND)
2. **Pas de label "Filter by Tags"** : section épurée
3. **Parsing robuste** : lit `m1:domain` depuis le bon nœud (`owl:Ontology`)
4. **Compatible** : supporte aussi `m0:domain` (ancien format)
5. **Navigation fluide** : clavier adapté aux filtres actifs
6. **Affichage groupé** : console log groupé par type d'ontologie

---

**Auteur** : Echopraxium with the collaboration of Claude AI  
**Date** : 2026-04-24  
**Version** : 2.0.0 (Double Filtrage)
