// =============================================================
// TscgOntologyExplorer — renderer/RendererPluginApi.js   (ESM)
// API factory for renderer plugins.
// Each renderer plugin receives a scoped instance of this API.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

// ── Shared registries (module-level singletons) ───────────────
const _menuItems      = []            // { label, id, group, pluginName }
const _actionHandlers = new Map()     // id → fn
const _tabs           = []            // { label, id, pluginName }
const _tabHandlers    = new Map()     // id → fn(container)
const _ontologyListeners = []         // fn(ontologyInfo)

// ── Internal dispatcher ───────────────────────────────────────
// Called by renderer.js when main sends 'trigger-renderer-action'
export function dispatchAction (id) {
  const fn = _actionHandlers.get(id)
  if (typeof fn === 'function') {
    fn()
  } else {
    console.warn(`[RendererPluginApi] No handler for action: ${id}`)
  }
}

// Called by renderer.js to get all registered menu items
export function getMenuItems () {
  return [..._menuItems]
}

// Called by renderer.js to get all registered tabs
export function getTabs () {
  return [..._tabs]
}

// Called when the active ontology changes (from renderer.js)
export function notifyOntologyChanged (info) {
  for (const fn of _ontologyListeners) {
    try { fn(info) } catch (e) { console.error(e) }
  }
}

// =============================================================
// PER-PLUGIN API FACTORY
// =============================================================
export function createRendererApiFor (pluginName) {
  return {
    pluginName,

    // ── Register a menu item under Tools > Plugins ──────────────
    // options: { label: string, id: string, group?: string }
    registerMenuItem (options) {
      _menuItems.push({ ...options, pluginName })
      console.log(`[RendererPluginApi:${pluginName}] Menu item: ${options.label}`)
    },

    // ── Register the click handler for a menu item ──────────────
    onAction (id, fn) {
      _actionHandlers.set(id, fn)
    },

    // ── Register a new tab in the right panel ───────────────────
    // options: { label: string, id: string }
    // The tab's content container is passed to the activation handler.
    registerTab (options) {
      _tabs.push({ ...options, pluginName })
      console.log(`[RendererPluginApi:${pluginName}] Tab registered: ${options.label}`)
    },

    // ── Handle tab activation ───────────────────────────────────
    // fn(container: HTMLElement) — called when the user switches to this tab
    onTabActivated (id, fn) {
      _tabHandlers.set(id, fn)
    },

    // ── Activate a tab programmatically (internal use) ──────────
    activateTab (id, container) {
      const fn = _tabHandlers.get(id)
      if (typeof fn === 'function') fn(container)
    },

    // ── Listen for active ontology changes ──────────────────────
    // info: { layer, filePath, label }
    onOntologyChanged (fn) {
      _ontologyListeners.push(fn)
    },

    // ── Show the renderer popup overlay ─────────────────────────
    showPopup (message) {
      const overlay = document.getElementById('popup-overlay')
      const msg     = document.getElementById('popup-message')
      const from    = document.getElementById('popup-from')
      if (overlay && msg) {
        msg.textContent  = message
        if (from) from.textContent = `— ${pluginName}`
        overlay.hidden = false
      }
    },

    // ── DOM helpers ──────────────────────────────────────────────
    // Insert content into the right panel below the existing tabs
    appendToRightPanel (htmlOrElement) {
      const panel = document.getElementById('right-panel-extra')
      if (!panel) return
      if (typeof htmlOrElement === 'string') {
        panel.insertAdjacentHTML('beforeend', htmlOrElement)
      } else {
        panel.appendChild(htmlOrElement)
      }
    },

    // ── IPC helpers ──────────────────────────────────────────────
    // Send a custom event to a server plugin
    sendToServer (eventName, data) {
      window.tscgAPI.sendToServer(eventName, data)
    },

    // Listen for a custom event from a server plugin
    onFromServer (eventName, fn) {
      window.tscgAPI.onFromServer(eventName, fn)
    },

    // ── Log ──────────────────────────────────────────────────────
    log  (...args) { console.log(`[Plugin:${pluginName}]`,  ...args) },
    warn (...args) { console.warn(`[Plugin:${pluginName}]`, ...args) }
  }
}
