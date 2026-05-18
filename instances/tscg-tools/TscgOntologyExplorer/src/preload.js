// =============================================================
// TscgOntologyExplorer — src/preload.js   (CJS)
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('tscgAPI', {

  // ── Plugin menu ───────────────────────────────────────────
  sendRendererPluginMenuItems: (items) => ipcRenderer.send('renderer-plugin-menu-items', items),
  onRendererPluginsList:  (cb) => ipcRenderer.on('renderer-plugins-list', (_e, list) => cb(list)),
  onTriggerRendererAction:(cb) => ipcRenderer.on('trigger-renderer-action', (_e, id) => cb(id)),

  // ── Popup ─────────────────────────────────────────────────
  onShowPopup: (cb) => ipcRenderer.on('show-popup', (_e, { message, from }) => cb(message, from)),

  // ── Layer / file navigation ───────────────────────────────
  onLoadLayer: (cb) => ipcRenderer.on('load-layer', (_e, name)     => cb(name)),
  onLoadFile:  (cb) => ipcRenderer.on('load-file',  (_e, filePath) => cb(filePath)),

  // ── Ontology root (custom path from config) ───────────────
  onOntologyRoot:      (cb) => ipcRenderer.on('ontology-root',      (_e, root) => cb(root)),
  onAutoLoadOntology:  (cb) => ipcRenderer.on('auto-load-ontology', (_e, path) => cb(path)),
  onLayerPaths:   (cb) => ipcRenderer.on('layer-paths', (_e, paths) => cb(paths)),

  // ── Theme ─────────────────────────────────────────────────
  onThemeInit:    (cb) => ipcRenderer.on('theme-init',    (_e, theme) => cb(theme)),
  onThemeChanged: (cb) => ipcRenderer.on('theme-changed', (_e, theme) => cb(theme)),

  // ── Undo / Redo (from Edit menu) ──────────────────────────
  onUndo: (cb) => ipcRenderer.on('menu-undo', () => cb()),
  onRedo: (cb) => ipcRenderer.on('menu-redo', () => cb()),

  // ── Command Palette ───────────────────────────────────────
  onOpenCommandPalette: (cb) => ipcRenderer.on('open-command-palette', () => cb()),

  // ── Export As ─────────────────────────────────────────────
  onExportAs: (cb) => ipcRenderer.on('export-as', () => cb()),
  saveExport:             (data) => ipcRenderer.send('export-as', data),
  showExportFormatDialog: ()     => ipcRenderer.invoke('show-export-format-dialog'),
  saveSparqlOutput:       (data) => ipcRenderer.invoke('save-sparql-output', data),
  onFindInOntology:       (cb)   => ipcRenderer.on('find-in-ontology', cb),
  listM1Extensions:       ()     => ipcRenderer.invoke('list-m1-extensions'),
  readTextFile:           (path) => ipcRenderer.invoke('read-text-file', path),

  // ── Open external URI in system browser ──────────────────
  openExternal: (url) => ipcRenderer.send('open-external', url),

  // ── Preferences ───────────────────────────────────────────
  onOpenPluginManager: (cb) => ipcRenderer.on('open-plugin-manager', () => cb()),
  openPreferences:      ()   => ipcRenderer.send('open-preferences'),

  // ── File/folder picker for Preferences Browse buttons ────────
  showOpenDialog: (opts) => ipcRenderer.invoke('show-open-dialog', opts),

  // ── Config (invoke = async request/response) ──────────────
  config: {
    get:       (key)        => ipcRenderer.invoke('config-get', key),
    set:       (key, value) => ipcRenderer.invoke('config-set', key, value),
    setMany:   (patch)      => ipcRenderer.invoke('config-set-many', patch),
    getAll:    ()           => ipcRenderer.invoke('config-get-all'),
    notifyThemeChanged: (theme) => ipcRenderer.send('theme-changed', theme),
    restartBridge: ()       => ipcRenderer.send('restart-bridge')
  },

  // ── Plugin lifecycle ──────────────────────────────────────
  installPlugin:   (tgzPath) => ipcRenderer.invoke('install-plugin', tgzPath),
  listPlugins:     ()        => ipcRenderer.invoke('list-plugins'),
  uninstallPlugin: (name)    => ipcRenderer.invoke('uninstall-plugin', name),

  // ── Cross-process custom events ───────────────────────────
  sendToServer: (eventName, data) => ipcRenderer.send(`plugin-to-server:${eventName}`, data),
  onFromServer: (eventName, cb)   => ipcRenderer.on(`plugin:${eventName}`, (_e, data) => cb(data))
})
