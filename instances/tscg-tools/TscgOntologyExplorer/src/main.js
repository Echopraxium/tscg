// =============================================================
// TscgOntologyExplorer — src/main.js   (CJS)
// Electron main process.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const { app, BrowserWindow, Menu, ipcMain, protocol, net, dialog } = require('electron')
const path              = require('path')
const os                = require('os')
const { pathToFileURL } = require('url')

const PluginManager     = require('./core/PluginManager')
const ServerPluginApi   = require('./core/ServerPluginApi')
const config            = require('./config/ConfigManager')

const LOCAL_APP_DATA = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local')
const PLUGINS_PATH   = path.join(LOCAL_APP_DATA, 'TscgOntologyExplorer', 'plugins')


  function openMarkdownViewer (mdPath, title) {
    const viewerPath = path.join(__dirname, '..', 'docs', 'markdown-viewer.html')
    const encodedPath = encodeURIComponent(mdPath)
    const win = new BrowserWindow({
      width: 980, height: 760,
      title,
      webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true }
    })
    win.loadFile(viewerPath, { query: { file: mdPath } })
    win.setMenu(null)
  }

// ── Register plugin:// scheme before app.whenReady() ──────────
protocol.registerSchemesAsPrivileged([{
  scheme: 'plugin',
  privileges: { standard: true, secure: true, supportFetchAPI: true, corsEnabled: true }
}])

// ── Singletons ─────────────────────────────────────────────────
let mainWindow        = null
let prefsWindow       = null
const pluginMgr       = new PluginManager(PLUGINS_PATH)
const serverApi       = new ServerPluginApi()
let serverMenuItems   = []
let rendererMenuItems = []

// =============================================================
// WINDOW
// =============================================================
function createWindow () {
  const bounds = config.get('windowBounds') || {}
  mainWindow = new BrowserWindow({
    width:  bounds.width  || 1400,
    height: bounds.height || 900,
    x:      bounds.x      || undefined,
    y:      bounds.y      || undefined,
    title:  'TscgOntologyExplorer',
    webPreferences: {
      preload:          path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration:  false
    }
  })

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'))
  // mainWindow.webContents.openDevTools()

  mainWindow.webContents.on('did-finish-load', () => {
    // Send initial theme
    const theme = config.get('theme') || 'night'
    mainWindow.webContents.send('theme-init', theme)

    // Read preconfigured layer paths from M0_TscgOntologyExplorer.jsonld.
    // Cached in config.json — M0 re-read only if its mtime has changed.
    const m0Path     = path.join(__dirname, '..', 'M0_TscgOntologyExplorer.jsonld')
    const layerPaths = config.getLayerPaths(m0Path)
    mainWindow.webContents.send('layer-paths', layerPaths)

    // Send renderer plugin list
    const rendererPluginList = pluginMgr.rendererPlugins.map(p => ({
      name: p.name, rendererEntry: p.rendererEntry, meta: p.meta
    }))
    mainWindow.webContents.send('renderer-plugins-list', rendererPluginList)

    // Send repo root
    const repoRoot = path.join(__dirname, '..', '..', '..', '..')
    mainWindow.webContents.send('plugin:repo-root', { root: repoRoot })

    // Send ontology root path from config (if set)
    const ontRoot = config.get('ontologyRootPath')
    if (ontRoot) mainWindow.webContents.send('ontology-root', ontRoot)

    // Auto-load default ontology on startup (local path or URL)
    const defaultOntology = config.get('defaultLoadedOntology')
    if (defaultOntology) {
      mainWindow.webContents.send('auto-load-ontology', defaultOntology)
      console.log('[main] Auto-loading default ontology:', defaultOntology)
    }
  })

  // Save window bounds on close
  mainWindow.on('close', () => {
    const b = mainWindow.getBounds()
    config.set('windowBounds', { width: b.width, height: b.height, x: b.x, y: b.y })
  })

  return mainWindow
}

// =============================================================
// PREFERENCES WINDOW
// =============================================================
function openPreferencesWindow () {
  if (prefsWindow && !prefsWindow.isDestroyed()) {
    prefsWindow.focus()
    return
  }

  prefsWindow = new BrowserWindow({
    parent:         mainWindow,
    modal:          true,
    width:          740,
    height:         520,
    title:          'Preferences',
    resizable:      false,
    minimizable:    false,
    maximizable:    false,
    webPreferences: {
      preload:          path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration:  false
    }
  })

  prefsWindow.setMenu(null)
  prefsWindow.loadFile(path.join(__dirname, 'preferences', 'preferences.html'))
  prefsWindow.on('closed', () => { prefsWindow = null })
}

// =============================================================
// MENU BUILDER
// =============================================================
function buildAppMenu () {
  const allItems = [...serverMenuItems, ...rendererMenuItems]

  const groups = {}
  for (const item of allItems) {
    const g = item.group || 'General'
    if (!groups[g]) groups[g] = []
    groups[g].push(item)
  }

  let pluginsSubmenu = []
  if (allItems.length === 0) {
    pluginsSubmenu = [{ label: '(no plugins loaded)', enabled: false }]
  } else {
    for (const [, items] of Object.entries(groups)) {
      if (pluginsSubmenu.length > 0) pluginsSubmenu.push({ type: 'separator' })
      for (const item of items) {
        pluginsSubmenu.push({
          label: item.label,
          click: () => {
            if (!mainWindow) return
            if (item.type === 'server') serverApi.triggerAction(item.id)
            else mainWindow.webContents.send('trigger-renderer-action', item.id)
          }
        })
      }
    }
  }

  const template = [
    // ── File ──────────────────────────────────────────────────
    {
      label: 'File',
      submenu: [
        {
          label: 'Open M3 (GenesisSpace)…', accelerator: 'CmdOrCtrl+3',
          click: () => mainWindow?.webContents.send('load-layer', 'M3')
        },
        {
          label: 'Open M2 (GenericConcepts)…', accelerator: 'CmdOrCtrl+2',
          click: () => mainWindow?.webContents.send('load-layer', 'M2')
        },
        {
          label: 'Open M1 (CoreConcepts)…', accelerator: 'CmdOrCtrl+1',
          click: () => mainWindow?.webContents.send('load-layer', 'M1')
        },
        { type: 'separator' },
        {
          label: 'Open File…', accelerator: 'CmdOrCtrl+O',
          click: async () => {
            if (!mainWindow) return
            const result = await dialog.showOpenDialog(mainWindow, {
              title: 'Open TSCG ontology',
              filters: [{ name: 'JSON-LD', extensions: ['jsonld', 'json'] }],
              properties: ['openFile']
            })
            if (!result.canceled && result.filePaths[0])
              mainWindow.webContents.send('load-file', result.filePaths[0])
          }
        },
        { type: 'separator' },
        {
          label: 'Export As…', accelerator: 'CmdOrCtrl+Shift+E', 
          click: () => mainWindow?.webContents.send('export-as')
          // stub — enabled when an ontology is loaded
        },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },

    // ── Edit ──────────────────────────────────────────────────
    {
      label: 'Edit',
      submenu: [
        {
          label: 'Find in Ontology…', accelerator: 'CmdOrCtrl+F',
          click: () => mainWindow?.webContents.send('find-in-ontology')
        },
        { type: 'separator' },
        {
          label: 'Preferences…', accelerator: 'CmdOrCtrl+,',
          click: () => openPreferencesWindow()
        }
      ]
    },

    // ── Tools ─────────────────────────────────────────────────
    {
      label: 'Tools',
      submenu: [
        { label: 'Plugins', submenu: pluginsSubmenu },
        { type: 'separator' },
        {
          label: 'Command Palette…', accelerator: 'CmdOrCtrl+Shift+P',
          click: () => mainWindow?.webContents.send('open-command-palette')
          // stub — implemented later
        },
        { type: 'separator' },
        {
          label: 'Install Plugin from file…',
          click: async () => {
            if (!mainWindow) return
            const result = await dialog.showOpenDialog(mainWindow, {
              title: 'Select plugin package (.tgz)',
              filters: [{ name: 'NPM package', extensions: ['tgz'] }],
              properties: ['openFile']
            })
            if (!result.canceled && result.filePaths[0]) installPlugin(result.filePaths[0])
          }
        },
        {
          label: 'Manage Plugins…',
          click: () => mainWindow?.webContents.send('open-plugin-manager')
        }
      ]
    },

    // ── View ──────────────────────────────────────────────────
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' }
      ]
    },

    // ── Help ──────────────────────────────────────────────────
    {
      label: 'Help',
      submenu: [
        {
          label: "User's Manual",
          accelerator: 'F1',
          click: () => {
            const mdPath = path.join(__dirname, '..', 'docs', 'UserManual.md')
            const fs = require('fs')
            if (fs.existsSync(mdPath)) {
              openMarkdownViewer(mdPath, "TscgOntologyExplorer — User's Manual")
            } else {
              dialog.showMessageBox(mainWindow, {
                type:    'warning',
                title:   "User's Manual not found",
                message: "User's Manual not found",
                detail:  `Expected at:\n${mdPath}\n\nPlease copy UserManual.md to the docs/ folder.`
              })
            }
          }
        },
        { type: 'separator' },
        {
          label: 'TSCG Repository…',
          click: () => require('electron').shell.openExternal('https://github.com/Echopraxium/tscg')
        },
        {
          label: "TSCG's README",
          click: () => {
            const cfg    = config.get('ontologyRootPath', '')
            const repoRoot = cfg.replace(/[\\/]ontology$/, '')
            const readmePath = path.join(repoRoot, 'README.md')
            openMarkdownViewer(readmePath, "TSCG's README")
          }
        },
        { type: 'separator' },
        {
          label: 'About TscgOntologyExplorer',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type:    'info',
              title:   'About TscgOntologyExplorer',
              message: 'TscgOntologyExplorer',
              detail:  'TSCG-dedicated ontology browser and editor.\n' +
                       'Built with ElectronJS.\n\n' +
                       'Author: Echopraxium with the collaboration of Claude AI',
              buttons: ['OK']
            })
          }
        }
      ]
    }
  ]

  Menu.setApplicationMenu(Menu.buildFromTemplate(template))
}

// =============================================================
// PLUGIN INSTALL
// =============================================================
async function installPlugin (tgzPath) {
  try {
    const name = pluginMgr.installFromTgz(tgzPath)
    await dialog.showMessageBox(mainWindow, {
      type: 'info', title: 'Plugin installed',
      message: `Plugin "${name}" installed successfully.`,
      detail: 'Restart the application to activate the new plugin.', buttons: ['OK']
    })
  } catch (err) {
    await dialog.showMessageBox(mainWindow, {
      type: 'error', title: 'Installation failed',
      message: String(err.message), buttons: ['OK']
    })
  }
}

// =============================================================
// LOAD SERVER PLUGINS
// =============================================================
function loadServerPlugins () {
  for (const plugin of pluginMgr.serverPlugins) {
    try {
      delete require.cache[require.resolve(plugin.mainPath)]
      const PluginFactory = require(plugin.mainPath)
      if (typeof PluginFactory !== 'function') continue
      const api = serverApi.createFor(plugin.name)
      api.pluginMeta = plugin.meta
      PluginFactory(api)
      console.log(`[main] Server plugin loaded: ${plugin.name}`)
    } catch (err) {
      console.error(`[main] Failed to load server plugin ${plugin.name}:`, err.message)
    }
  }
}

// =============================================================
// APP LIFECYCLE
// =============================================================
app.whenReady().then(() => {

  // Load config first
  config.load()

  // plugin:// protocol
  protocol.handle('plugin', (request) => {
    try {
      const url        = new URL(request.url)
      const pluginName = url.hostname
      const filePath   = url.pathname.replace(/^\//, '')
      const fullPath   = path.join(PLUGINS_PATH, pluginName, filePath)
      return net.fetch(pathToFileURL(fullPath).href)
    } catch (err) {
      console.error('[main] plugin:// error:', err.message)
      return new Response('Plugin file not found', { status: 404 })
    }
  })

  // Scan + load plugins
  pluginMgr.scan()
  serverApi.setupIpc()
  serverApi.onMenuChanged((items) => { serverMenuItems = items; buildAppMenu() })
  loadServerPlugins()

  // Window + menu
  createWindow()
  serverApi.setWindow(mainWindow)   // CRITICAL: allows server plugins to sendToRenderer
  console.log("[main] Window created, serverApi window set")
  buildAppMenu()

  // ── IPC handlers ────────────────────────────────────────────
  ipcMain.on('renderer-plugin-menu-items', (_e, items) => {
    rendererMenuItems = items.map(i => ({ ...i, type: 'renderer' }))
    buildAppMenu()
  })

  // Config IPC
  ipcMain.handle('config-get',     (_e, key)   => config.get(key))
  ipcMain.handle('config-set',     (_e, k, v)  => config.set(k, v))
  ipcMain.handle('config-set-many',(_e, patch) => config.setMany(patch))
  ipcMain.handle('config-get-all', ()          => config.getAll())

  // Theme change from preferences → push to main renderer
  ipcMain.on('theme-changed', (_e, theme) => {
    config.set('theme', theme)
    mainWindow?.webContents.send('theme-changed', theme)
  })

  // Plugin lifecycle
  ipcMain.handle('install-plugin',   async (_e, tgzPath) => {
    try   { return { success: true,  name:  pluginMgr.installFromTgz(tgzPath) } }
    catch (err) { return { success: false, error: err.message } }
  })
  ipcMain.handle('list-plugins',     ()          => pluginMgr.listInstalled())
  ipcMain.handle('uninstall-plugin', (_e, name)  => ({ success: pluginMgr.uninstall(name) }))

  // Open preferences from renderer (e.g. keyboard shortcut)
  ipcMain.on('open-preferences', () => openPreferencesWindow())


  // Scan ontology/M1_extensions/ for all .jsonld files
  ipcMain.handle('read-text-file', async (_, filePath) => {
    const fs = require('fs')
    try { return fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf-8') : null }
    catch { return null }
  })

  ipcMain.handle('list-m1-extensions', async () => {
    const fs   = require('fs')
    const root = config.get('ontologyRootPath', '')
    const extDir = path.join(root, 'M1_extensions')
    if (!fs.existsSync(extDir)) return []
    const results = []
    for (const sub of fs.readdirSync(extDir)) {
      const subPath = path.join(extDir, sub)
      if (!fs.statSync(subPath).isDirectory()) continue
      for (const file of fs.readdirSync(subPath)) {
        if (!file.endsWith('.jsonld')) continue
        const fullPath = path.join(subPath, file)
        const name = file.replace(/\.jsonld$/i, '')   // e.g. "M1_Biology"
        results.push({ name, file, path: fullPath, subfolder: sub })
      }
    }
    return results.sort((a, b) => a.name.localeCompare(b.name))
  })

  // Save SPARQL results as CSV to output/ folder
  ipcMain.handle('save-sparql-output', async (_event, { filename, content: csv }) => {
    const repoRoot  = config.get('ontologyRootPath', '').replace(/[/\\]ontology$/, '')
    const outputDir = path.join(repoRoot, 'instances', 'tscg-tools',
                                'TscgOntologyExplorer', 'output')
    try {
      const fs = require('fs')
      fs.mkdirSync(outputDir, { recursive: true })
      const filePath = path.join(outputDir, filename)
      fs.writeFileSync(filePath, csv, 'utf-8')
      // Show info dialog
      await dialog.showMessageBox(mainWindow, {
        type:    'info',
        title:   'SPARQL Results Saved',
        message: `File saved successfully`,
        detail:  `File: ${filename}\nFolder: ${outputDir}`,
        buttons: ['OK']
      })
      return { ok: true, filePath }
    } catch (err) {
      await dialog.showMessageBox(mainWindow, {
        type: 'error', title: 'Save Failed',
        message: err.message, buttons: ['OK']
      })
      return { ok: false, error: err.message }
    }
  })

  // Export format picker — shows a native list dialog
  ipcMain.handle('show-export-format-dialog', async () => {
    const FORMATS = [
      { id: 'turtle',   label: 'Turtle (.ttl)  — OWL/RDF, Protégé compatible',  extension: '.ttl' },
      { id: 'rdfxml',   label: 'RDF/XML (.rdf) — OWL standard, broad compatibility', extension: '.rdf' },
      { id: 'ntriples', label: 'N-Triples (.nt) — simple line-by-line RDF',      extension: '.nt'  },
      { id: 'jsonld',   label: 'JSON-LD (.jsonld) — re-export with absolute URIs', extension: '.jsonld' },
    ]
    const { response } = await dialog.showMessageBox(mainWindow, {
      type:        'question',
      title:       'Export As…',
      message:     'Choose export format:',
      buttons:     [...FORMATS.map(f => f.label), 'Cancel'],
      cancelId:    FORMATS.length,
      defaultId:   0,
    })
    if (response === FORMATS.length) return null   // cancelled
    return FORMATS[response]
  })

  // File/folder picker invoked from Preferences Browse buttons
  ipcMain.handle('show-open-dialog', async (_event, opts = {}) => {
    const result = await dialog.showOpenDialog({
      properties: [opts.isDirectory ? 'openDirectory' : 'openFile'],
      filters:    opts.filters || [{ name: 'All files', extensions: ['*'] }]
    })
    return result.canceled ? null : result.filePaths[0]
  })


  // Export As — show format picker then save dialog
  ipcMain.on('export-as', async (_event, { filePath, format, content, extension }) => {
    if (!mainWindow) return
    const result = await dialog.showSaveDialog(mainWindow, {
      title:       'Export As',
      defaultPath: filePath
        ? require('path').basename(filePath, '.jsonld') + extension
        : 'export' + extension,
      filters: [
        { name: 'Turtle',    extensions: ['ttl']    },
        { name: 'RDF/XML',   extensions: ['rdf']    },
        { name: 'N-Triples', extensions: ['nt']     },
        { name: 'JSON-LD',   extensions: ['jsonld'] },
      ]
    })
    if (result.canceled || !result.filePath) return
    require('fs').writeFileSync(result.filePath, content, 'utf-8')
    dialog.showMessageBox(mainWindow, {
      type:    'info',
      title:   'Export complete',
      message: `Exported to ${require('path').basename(result.filePath)}`,
      buttons: ['OK']
    })
  })

  // Open external URI in system browser (double-click on URI in Property Inspector)
  ipcMain.on('open-external', (_event, url) => {
    require('electron').shell.openExternal(url)
  })
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
