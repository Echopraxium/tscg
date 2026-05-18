// =============================================================
// TscgOntologyExplorer — src/config/ConfigManager.js   (CJS)
// Reads and writes config.json in AppData\Local\TscgOntologyExplorer\.
// Singleton — require() always returns the same instance.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const fs   = require('fs')
const path = require('path')
const os   = require('os')

const CONFIG_DIR  = path.join(
  process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'),
  'TscgOntologyExplorer'
)
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json')

// ── Default configuration ──────────────────────────────────────
// Add new options here — they are merged with existing config on load.
const DEFAULTS = {
  // Appearance
  theme:              'night',        // 'night' | 'day' | custom theme name

  // Paths
  ontologyRootPath:   '',             // absolute path to tscg/ontology/ (empty = auto-detect)
  pluginsDirectory:   path.join(CONFIG_DIR, 'plugins'),

  // Python Bridge
  pythonExecutable:   'python',       // 'python' | 'python3' | absolute path
  bridgePort:         7432,           // default port; tries next ports if busy

  // Window
  windowBounds: {
    width:  1400,
    height: 900,
    x:      null,
    y:      null
  },

  // Editor behaviour
  maxUndoHistory:     100,
  autoLoadLastFile:   false,
  lastOpenedFiles:    [],             // list of recently opened file paths

  // Default ontology loaded on startup (empty = none)
  // Supports local absolute path OR http(s):// URL
  defaultLoadedOntology: '',    // e.g. 'E:\\tscg\\ontology\\M2_GenericConcepts.jsonld'
                                //  or 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld'

  // Cached from M0_TscgOntologyExplorer.jsonld (single source of truth)
  // Re-read only when M0 file modification time changes.
  layerPaths: {},                     // { M3, M2, M1 } filenames
  m0Mtime:    0                       // M0 file mtime (ms) at last read
}

class ConfigManager {
  constructor () {
    this._config = null
  }

  // ── Load (call once at app start) ──────────────────────────
  load () {
    if (!fs.existsSync(CONFIG_DIR)) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true })
    }

    if (!fs.existsSync(CONFIG_FILE)) {
      this._config = structuredClone(DEFAULTS)
      this._save()
      console.log(`[ConfigManager] Created default config: ${CONFIG_FILE}`)
    } else {
      try {
        const raw = fs.readFileSync(CONFIG_FILE, 'utf-8')
        // Deep merge: defaults provide missing keys, saved values override
        this._config = this._merge(DEFAULTS, JSON.parse(raw))
        console.log(`[ConfigManager] Loaded config: ${CONFIG_FILE}`)
      } catch (err) {
        console.warn(`[ConfigManager] Failed to parse config, using defaults: ${err.message}`)
        this._config = structuredClone(DEFAULTS)
      }
    }
    return this._config
  }

  // ── Getters / Setters ───────────────────────────────────────
  get (key) {
    if (!this._config) this.load()
    return this._config[key]
  }

  set (key, value) {
    if (!this._config) this.load()
    this._config[key] = value
    this._save()
  }

  setMany (patch) {
    if (!this._config) this.load()
    Object.assign(this._config, patch)
    this._save()
  }

  getAll () {
    if (!this._config) this.load()
    return structuredClone(this._config)
  }

  // ── Helpers ─────────────────────────────────────────────────
  _save () {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(this._config, null, 2), 'utf-8')
  }

  _merge (defaults, saved) {
    const result = structuredClone(defaults)
    for (const [k, v] of Object.entries(saved)) {
      if (v !== null && typeof v === 'object' && !Array.isArray(v) &&
          typeof result[k] === 'object' && result[k] !== null) {
        result[k] = this._merge(result[k], v)
      } else {
        result[k] = v
      }
    }
    return result
  }
}

// ── Layer paths helper ────────────────────────────────────────
// Reads m0:preconfiguredPaths from M0_TscgOntologyExplorer.jsonld.
// Returns cached value from config.json unless M0 has been modified.
ConfigManager.prototype.getLayerPaths = function (m0FilePath) {
  const fs   = require('fs')
  if (!this._config) this.load()

  let m0Mtime = 0
  try { m0Mtime = fs.statSync(m0FilePath).mtimeMs } catch { /* file missing */ }

  // Use cache if M0 file unchanged
  const cached = this._config.layerPaths
  if (cached && Object.keys(cached).length > 0 && m0Mtime === this._config.m0Mtime) {
    console.log('[ConfigManager] Layer paths from cache:', cached)
    return cached
  }

  // Re-read M0
  try {
    const m0Data  = JSON.parse(fs.readFileSync(m0FilePath, 'utf-8'))
    const m0Node  = m0Data['@graph']?.[0]
    const paths   = m0Node?.['m0:architecture']?.['m0:preconfiguredPaths'] || {}
    this._config.layerPaths = paths
    this._config.m0Mtime    = m0Mtime
    this._save()
    console.log('[ConfigManager] Layer paths read from M0 and cached:', paths)
    return paths
  } catch (err) {
    console.warn('[ConfigManager] Could not read M0 file:', err.message)
    return this._config.layerPaths || {}
  }
}

module.exports = new ConfigManager()
