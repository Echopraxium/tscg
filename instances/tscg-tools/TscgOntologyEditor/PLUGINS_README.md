# TscgOntologyEditor — Plugin System

## Architecture duale

```
Plugin type  │ Process    │ Format │ Chargement
─────────────┼────────────┼────────┼─────────────────────────────────────────
server       │ main       │ CJS    │ require(pluginPath) dans main.js
renderer     │ renderer   │ ESM    │ import('plugin://<name>/renderer.js')
both         │ les deux   │ CJS+ESM│ un fichier par process
```

### Pourquoi cette séparation ?

| Capacité | Server plugin | Renderer plugin |
|----------|--------------|-----------------|
| Node.js (fs, child_process…) | ✅ | ❌ |
| DOM / UI | ❌ | ✅ |
| Onglets dans le panneau droit | ❌ | ✅ |
| Menu Tools > Plugins | ✅ | ✅ |
| Popup native (dialog) | ✅ | ❌ |
| Popup HTML overlay | via IPC | ✅ |
| SHACL validation (pyshacl) | ✅ | ❌ |
| Accès ontologie active | via IPC | ✅ |

### Sécurité

Le protocole `plugin://` est enregistré via `protocol.registerSchemesAsPrivileged()`
avec les privilèges `standard + secure + supportFetchAPI + corsEnabled`.
Cela permet d'importer des modules ES depuis un répertoire local **sans** désactiver
`webSecurity`. Ni `nodeIntegration` ni `webSecurity: false` ne sont requis.

---

## Structure d'un plugin

### Server plugin (CJS)

```
my-server-plugin/
├── package.json
│   ├── "tscg-plugin-type": "server"
│   └── "main": "index.js"
└── index.js      ← module.exports = function(api) { ... }
```

```js
// index.js
'use strict'
module.exports = function MyPlugin(api) {
  api.registerMenuItem({ label: 'My Feature', id: 'my-feature', group: 'Tools' })
  api.onAction('my-feature', () => {
    // Ici: Node.js complet (fs, child_process, etc.)
    api.showPopup('Hello from server plugin!')
  })
}
```

### Renderer plugin (ESM)

```
my-renderer-plugin/
├── package.json
│   ├── "tscg-plugin-type": "renderer"
│   └── "renderer-main": "renderer.js"
└── renderer.js   ← export function init(api) { ... }
```

```js
// renderer.js
export function init(api) {
  api.registerMenuItem({ label: 'My Panel', id: 'my-panel' })
  api.onAction('my-panel', () => {
    api.showPopup('Hello from renderer plugin!')
  })
  api.registerTab({ label: 'My Tab', id: 'my-tab' })
  api.onTabActivated('my-tab', (container) => {
    container.innerHTML = '<p>Custom content here</p>'
  })
  api.onOntologyChanged((info) => {
    console.log('Active ontology:', info.label)
  })
}
```

### Plugin hybride (both)

```
my-hybrid-plugin/
├── package.json
│   ├── "tscg-plugin-type": "both"
│   ├── "main": "index.js"          ← server entry (CJS)
│   └── "renderer-main": "renderer.js"  ← renderer entry (ESM)
├── index.js
└── renderer.js
```

---

## Installation

### Méthode 1 — dossier direct (développement)

Copier le dossier du plugin dans :
```
C:\Users\%USERNAME%\AppData\Local\TscgOntologyEditor\plugins\<plugin-name>\
```
Redémarrer l'application.

### Méthode 2 — depuis un .tgz

```bash
cd my-plugin
npm pack
# → my-plugin-1.0.0.tgz
```

Dans l'application : `Tools > Install Plugin from file…` → sélectionner le `.tgz`.

---

## Test des dummy plugins

```bash
# 1. Copier les dummy plugins dans le répertoire plugins
set PLUGINS=%LOCALAPPDATA%\TscgOntologyEditor\plugins
mkdir %PLUGINS%

xcopy /E /I dummy-plugin-server %PLUGINS%\tscg-dummy-server
xcopy /E /I dummy-plugin-renderer %PLUGINS%\tscg-dummy-renderer

# 2. Lancer l'application
npm start

# 3. Vérifier dans la console (DevTools → View > Toggle DevTools) :
#    [main] Server plugin loaded: tscg-dummy-server
#    [renderer] Renderer plugin loaded: tscg-dummy-renderer

# 4. Tester :
#    Tools > Plugins > Dummy Server Plugin   → dialog natif
#    Tools > Plugins > Dummy Renderer Plugin → popup HTML
#    Onglet "Plugin Info" dans le panneau droit → contenu injecté
```

---

## API Server Plugin

```js
module.exports = function(api) {
  api.pluginName                          // nom du plugin
  api.registerMenuItem({ label, id, group? })  // ajoute au menu
  api.onAction(id, fn)                    // handler clic menu
  api.sendToRenderer(eventName, data)     // IPC → renderer
  api.onFromRenderer(eventName, fn)       // écoute depuis renderer
  api.showPopup(message, title?)          // dialog natif (main)
  api.showRendererPopup(message)          // overlay HTML (renderer)
  api.log(...args)                        // log préfixé
  api.warn(...args)
}
```

## API Renderer Plugin

```js
export function init(api) {
  api.pluginName
  api.registerMenuItem({ label, id, group? })
  api.onAction(id, fn)
  api.registerTab({ label, id })
  api.onTabActivated(id, fn)             // fn(container: HTMLElement)
  api.onOntologyChanged(fn)             // fn({ layer, filePath, label })
  api.showPopup(message)                // overlay HTML
  api.appendToRightPanel(htmlOrElement) // injecte sous les onglets
  api.sendToServer(eventName, data)     // IPC → server plugin
  api.onFromServer(eventName, fn)       // écoute depuis server plugin
  api.log(...args)
  api.warn(...args)
}
```
