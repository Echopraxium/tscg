// =============================================================
// TscgOntologyExplorer — src/core/ServerPluginApi.js   (CJS)
// API injected into server plugins at load time (main process).
// Location: instances/tscg-tools/TscgOntologyExplorer/src/core/
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const { ipcMain } = require('electron')

class ServerPluginApi {
  constructor () {
    this._window          = null
    this._menuItems       = []
    this._actionHandlers  = new Map()
    this._onMenuChangedCb = null
  }

  setWindow (win)              { this._window = win }
  onMenuChanged (callback)     { this._onMenuChangedCb = callback }
  get menuItems ()             { return this._menuItems }

  triggerAction (id) {
    const fn = this._actionHandlers.get(id)
    if (typeof fn === 'function') fn()
    else console.warn(`[ServerPluginApi] No handler for action: ${id}`)
  }

  setupIpc () {
    ipcMain.on('trigger-server-action', (_event, id) => this.triggerAction(id))
  }

  // ── Per-plugin scoped API ─────────────────────────────────────
  createFor (pluginName) {
    const self = this

    return {
      pluginName,

      registerMenuItem (options) {
        self._menuItems.push({ ...options, pluginName, type: 'server' })
        console.log(`[ServerPlugin:${pluginName}] Menu item: ${options.label}`)
        if (self._onMenuChangedCb) self._onMenuChangedCb(self._menuItems)
      },

      onAction (id, fn) {
        self._actionHandlers.set(id, fn)
      },

      sendToRenderer (eventName, data) {
        console.log(`[ServerPlugin:${pluginName}] sendToRenderer: ${eventName}, window set: ${!!self._window}`)
        if (self._window && !self._window.isDestroyed()) {
          self._window.webContents.send(`plugin:${eventName}`, data)
          console.log(`[ServerPlugin:${pluginName}] sent plugin:${eventName} to renderer`)
        } else {
          console.warn(`[ServerPlugin:${pluginName}] sendToRenderer FAILED — window not set!`)
        }
      },

      onFromRenderer (eventName, fn) {
        ipcMain.on(`plugin-to-server:${eventName}`, (_event, data) => fn(data))
      },

      // Native OS dialog popup (runs in main process)
      showPopup (message, title = pluginName) {
        const { dialog, BrowserWindow } = require('electron')
        const win = BrowserWindow.getFocusedWindow()
        dialog.showMessageBox(win || undefined, {
          type: 'info', title, message, buttons: ['OK']
        })
      },

      // HTML overlay popup in renderer
      showRendererPopup (message) {
        if (self._window && !self._window.isDestroyed())
          self._window.webContents.send('show-popup', { message, from: pluginName })
      },

      log  (...args) { console.log(`[Plugin:${pluginName}]`,  ...args) },
      warn (...args) { console.warn(`[Plugin:${pluginName}]`, ...args) }
    }
  }
}

module.exports = ServerPluginApi
