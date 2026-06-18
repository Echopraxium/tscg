# UI Improvement: SELECT Dropdown for LLM Provider

**Date:** 2026-04-06  
**Changes:** Provider selection UI modernization  
**Author:** Echopraxium with the collaboration of Claude AI

## 🎯 Modifications apportées

### 1. **DeepSeek en premier** ✅

L'ordre des providers est maintenant :
```
1. 🔥 DeepSeek  (opérationnel)
2. 🌟 Gemini
3. 🏠 Ollama
4. 🤖 Anthropic
```

### 2. **SELECT dropdown au lieu de radio buttons** ✅

**Avant (radio buttons)** :
```html
<div id="provider-list">
  <!-- Multiple provider-row divs with click handlers -->
</div>
```

**Après (SELECT)** :
```html
<div class="form-group">
  <label class="form-label">Provider</label>
  <select class="form-select" id="provider-select">
    <!-- Populated dynamically -->
  </select>
</div>
```

### 3. **Affichage dynamique d'un seul bloc** ✅

Le SELECT déclenche l'affichage du bloc d'informations correspondant :
- Selection "DeepSeek" → affiche `#key-section-deepseek` uniquement
- Selection "Gemini" → affiche `#key-section-gemini` uniquement
- etc.

## 📋 Détails des changements

### **index.html**

**Ligne 115-119** — Remplacement de la section provider :
```html
<!-- AVANT -->
<div class="sb-section">
  <div class="sb-section-title">LLM Backend</div>
  <div id="provider-list"></div>
</div>

<!-- APRÈS -->
<div class="sb-section">
  <div class="sb-section-title">LLM Backend</div>
  <div class="form-group">
    <label class="form-label">Provider</label>
    <select class="form-select" id="provider-select">
      <!-- Populated dynamically by renderer.js -->
    </select>
  </div>
</div>
```

### **renderer.js**

#### Ligne 87 — Nouvelle référence DOM :
```javascript
// AVANT
providerList: $('provider-list'),

// APRÈS
providerSelect: $('provider-select'),
```

#### Lignes 209-244 — Fonction `renderProviderList()` réécrite :
```javascript
async function renderProviderList() {
  let providers = await window.tscgMiner.config.listProviders();
  
  // Reorder: DeepSeek first
  const providerOrder = ['deepseek', 'gemini', 'ollama', 'anthropic'];
  providers.sort((a, b) => {
    const ia = providerOrder.indexOf(a.id);
    const ib = providerOrder.indexOf(b.id);
    return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
  });
  
  ui.providerSelect.innerHTML = '';
  
  for (const p of providers) {
    const option = document.createElement('option');
    option.value = p.id;
    option.textContent = `${p.icon} ${p.label} — ${p.description}`;
    ui.providerSelect.appendChild(option);
  }
  
  // Set current selection
  ui.providerSelect.value = state.config?.active ?? 'deepseek';
  
  // Show key section for active
  showKeySection(state.config?.active ?? 'deepseek');
  
  // Handle change event
  ui.providerSelect.addEventListener('change', (e) => {
    selectProvider(e.target.value);
  }, { once: false });
}

function selectProvider(pid) {
  if (!state.config) return;
  state.config.active = pid;
  showKeySection(pid);
  updateChips();
}
```

**Changements clés** :
1. Tri personnalisé pour mettre DeepSeek en premier
2. Création d'options `<option>` au lieu de `<div class="provider-row">`
3. Valeur par défaut : `'deepseek'` au lieu de `'gemini'`
4. Event listener sur `change` au lieu de `click` sur chaque row
5. Fonction `selectProvider()` simplifiée (pas de manipulation de classes)

## 🎨 Avantages de la nouvelle interface

### UX améliorée
- ✅ **Plus compact** : Un seul SELECT au lieu de 4 blocs cliquables
- ✅ **Plus clair** : Un seul bloc d'informations visible à la fois
- ✅ **Standard** : Pattern UI familier (dropdown)
- ✅ **Keyboard-friendly** : Navigation clavier native du SELECT

### Maintenance simplifiée
- ✅ **Moins de CSS** : Plus besoin de styles pour `.provider-row`, `.selected`, etc.
- ✅ **Moins de DOM** : Une seule balise SELECT au lieu de N divs
- ✅ **Code plus simple** : Pas de gestion de classes `.selected`

### Ordre logique
- ✅ **DeepSeek en premier** : Le seul provider actuellement opérationnel
- ✅ **Ordre configurable** : Facile à modifier via le tableau `providerOrder`

## 🔧 Comment tester

1. Remplacer `renderer/index.html` et `renderer/renderer.js` dans TscgPocletMiner
2. Lancer l'application
3. Aller dans Settings
4. Vérifier que le SELECT affiche "🔥 DeepSeek" en premier
5. Changer de provider → le bloc d'informations doit s'adapter

## 📊 Résultat visuel attendu

```
Settings Tab
├── LLM Backend
│   └── [Provider ▼]
│       ├── 🔥 DeepSeek — Fast & affordable
│       ├── 🌟 Gemini — Free tier with limits
│       ├── 🏠 Ollama — Local, private
│       └── 🤖 Anthropic — Premium quality
│
└── (Bloc d'infos du provider sélectionné)
    ├── DeepSeek API Key
    ├── Model
    └── Test connection
```

**Un seul bloc visible** au lieu de 4 sections empilées.

## ✅ Validation

- [x] DeepSeek en premier dans le SELECT
- [x] Affichage dynamique d'un seul bloc d'informations
- [x] Code simplifié et plus maintenable
- [x] Compatibilité avec le reste du code (updateChips, showKeySection, etc.)

---

**Note technique** : Le CSS existant pour `.form-select` sera réutilisé automatiquement. Si des ajustements de style sont nécessaires pour le SELECT, ils peuvent être ajoutés dans `style.css`.
