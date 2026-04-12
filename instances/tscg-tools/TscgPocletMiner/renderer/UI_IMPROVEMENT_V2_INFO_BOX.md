# UI Improvement v2: SELECT + Info Box

**Date:** 2026-04-06  
**Version:** 2.0 (with info box)  
**Author:** Echopraxium with the collaboration of Claude AI

## 🎯 Interface finale

```
Settings Tab
├── LLM Backend
│   ├── Provider: [🔥 DeepSeek ▼]     ← SELECT simple (nom seulement)
│   │
│   └── ┌──────────────────────────┐
│       │ 🔥 DeepSeek              │  ← Boîte d'info détaillée
│       │ Fast & affordable        │
│       │ Quality: ★★★★ · Instant  │
│       └──────────────────────────┘
│
└── (Bloc de configuration du provider sélectionné)
    ├── DeepSeek API Key
    ├── Model
    └── Test connection
```

## ✅ Caractéristiques

### 1. **SELECT simplifié**
- Contenu : `${icon} ${label}` uniquement
- Exemples :
  - `🔥 DeepSeek`
  - `🌟 Gemini`
  - `🏠 Ollama`
  - `🤖 Anthropic`

### 2. **Boîte d'info dynamique**
Affiche les détails du provider sélectionné :
- **Icône** + **Nom** (en gras)
- **Description** (texte secondaire)
- **Métadonnées** : Quality + Speed (petit texte)

### 3. **Affichage réactif**
Changement de provider dans le SELECT → mise à jour instantanée de :
1. La boîte d'info
2. Le bloc de configuration (API key, model, etc.)
3. Le chip dans le header

## 📋 Détails techniques

### **index.html** — Ajout de la boîte d'info

```html
<div class="sb-section">
  <div class="sb-section-title">LLM Backend</div>
  
  <!-- SELECT simple -->
  <div class="form-group">
    <label class="form-label">Provider</label>
    <select class="form-select" id="provider-select">
      <!-- Options: juste icône + nom -->
    </select>
  </div>
  
  <!-- Boîte d'info détaillée -->
  <div id="provider-info-box" style="...">
    <div style="display:flex; align-items:center; gap:8px;">
      <span id="provider-info-icon"></span>
      <span id="provider-info-name"></span>
    </div>
    <div id="provider-info-desc"></div>
    <div id="provider-info-meta"></div>
  </div>
</div>
```

### **renderer.js** — Logique de mise à jour

#### Nouvelles références DOM :
```javascript
providerInfoIcon:   $('provider-info-icon'),
providerInfoName:   $('provider-info-name'),
providerInfoDesc:   $('provider-info-desc'),
providerInfoMeta:   $('provider-info-meta'),
```

#### Cache des providers :
```javascript
let providersCache = null; // Store for info display
```

#### Fonction `updateProviderInfo()` :
```javascript
function updateProviderInfo(pid) {
  if (!providersCache) return;
  const provider = providersCache.find(p => p.id === pid);
  if (!provider) return;
  
  ui.providerInfoIcon.textContent = provider.icon;
  ui.providerInfoName.textContent = provider.label;
  ui.providerInfoDesc.textContent = provider.description;
  ui.providerInfoMeta.textContent = `Quality: ${provider.quality} · ${provider.speed}`;
}
```

#### Fonction `selectProvider()` mise à jour :
```javascript
function selectProvider(pid) {
  if (!state.config) return;
  state.config.active = pid;
  updateProviderInfo(pid);  // ← Nouvelle ligne
  showKeySection(pid);
  updateChips();
}
```

## 🎨 Styling de la boîte d'info

Styles inline dans `index.html` (peuvent être externalisés dans `style.css`) :

```css
#provider-info-box {
  margin-top: 8px;
  padding: 10px;
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 11px;
  line-height: 1.6;
}

/* Icône + Nom */
#provider-info-icon {
  font-size: 18px;
}

#provider-info-name {
  font-weight: 600;
  color: var(--fg);
}

/* Description */
#provider-info-desc {
  color: var(--muted);
}

/* Métadonnées */
#provider-info-meta {
  margin-top: 4px;
  color: var(--sphinx);
  font-size: 10px;
}
```

## 📊 Exemple visuel complet

### DeepSeek sélectionné :

```
┌─────────────────────────────────────┐
│ Provider                            │
│ [🔥 DeepSeek ▼]                     │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🔥 DeepSeek                     │ │
│ │ Fast & affordable               │ │
│ │ Quality: ★★★★ · Instant         │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ DeepSeek API Key                    │
│ [sk-...                          ]  │
│ 🔗 platform.deepseek.com            │
│                                     │
│ Model                               │
│ [DeepSeek V3 (recommandé)        ▼] │
│                                     │
│ [Test connection]                   │
└─────────────────────────────────────┘
```

### Gemini sélectionné :

```
┌─────────────────────────────────────┐
│ Provider                            │
│ [🌟 Gemini ▼]                       │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🌟 Gemini                       │ │
│ │ Free tier with limits           │ │
│ │ Quality: ★★★★★ · Fast           │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Google AI Studio API Key            │
│ [AIzaSy...                       ]  │
│ 🆓 Gratuit sur aistudio.google.com  │
│                                     │
│ Model                               │
│ [Gemini 2.5 Flash               ▼]  │
│                                     │
│ [Test connection]                   │
│                                     │
│ ⚠ Tier gratuit: données utilisées  │
│ par Google pour amélioration        │
└─────────────────────────────────────┘
```

## ✅ Avantages de cette v2

### UX optimale
- ✅ **SELECT ultra-compact** : Juste le nom, pas de descriptions longues
- ✅ **Info visible en permanence** : Pas besoin de hover ou tooltip
- ✅ **Contexte toujours clair** : On voit immédiatement les caractéristiques
- ✅ **Cohérence visuelle** : La boîte d'info rappelle l'ancien style "provider-row"

### Lisibilité améliorée
- ✅ **Séparation claire** : Sélection ≠ Information
- ✅ **Hiérarchie visuelle** : Nom en gras, description en secondaire, meta en petit
- ✅ **Pas de surcharge** : Le SELECT reste léger et rapide à scanner

### Maintenance
- ✅ **Cache intelligent** : Les providers sont stockés pour éviter les appels répétés
- ✅ **Fonction dédiée** : `updateProviderInfo()` gère la mise à jour
- ✅ **Extensible** : Facile d'ajouter d'autres infos (pricing, status, etc.)

## 🔧 Intégration

1. Remplacer `renderer/index.html`
2. Remplacer `renderer/renderer.js`
3. Redémarrer l'application
4. Vérifier le rendu dans Settings

## 📦 Livrables

- [x] `index.html` — SELECT + boîte d'info
- [x] `renderer.js` — Logique de mise à jour
- [x] Documentation complète

---

**Version history:**
- v1.0: SELECT simple avec descriptions dans les options
- v2.0: SELECT + boîte d'info séparée (cette version) ✅
