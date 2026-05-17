// =============================================================
// TscgOntologyEditor — src/core/PluginManager.js   (CJS)
// Scans the plugins directory, classifies and manages plugins.
// Location: instances/tscg-tools/TscgOntologyEditor/src/core/
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const fs   = require('fs')
const path = require('path')

class PluginManager {
  /**
   * @param {string} pluginsPath  Absolute path to the plugins root directory.
   *
   * Expected layout:
   *   pluginsPath/
   *     my-server-plugin/
   *       package.json          "tscg-plugin-type": "server"
   *       index.js              CJS entry (module.exports = fn)
   *     my-renderer-plugin/
   *       package.json          "tscg-plugin-type": "renderer"
   *       renderer.js           ESM entry (export function init)
   *     my-hybrid-plugin/
   *       package.json          "tscg-plugin-type": "both"
   *       index.js              CJS server entry
   *       renderer.js           ESM renderer entry
   */
  constructor (pluginsPath) {
    this.pluginsPath     = pluginsPath
    this.serverPlugins   = []   // { name, dir, mainPath, meta }
    this.rendererPlugins = []   // { name, dir, rendererEntry, meta }
  }

  // ── Scan ─────────────────────────────────────────────────────
  scan () {
    this.serverPlugins   = []
    this.rendererPlugins = []

    if (!fs.existsSync(this.pluginsPath)) {
      console.log(`[PluginManager] Creating plugins directory: ${this.pluginsPath}`)
      fs.mkdirSync(this.pluginsPath, { recursive: true })
      return
    }

    for (const entry of fs.readdirSync(this.pluginsPath, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue

      const pluginDir = path.join(this.pluginsPath, entry.name)
      const pkgPath   = path.join(pluginDir, 'package.json')
      if (!fs.existsSync(pkgPath)) continue

      let meta
      try { meta = JSON.parse(fs.readFileSync(pkgPath, 'utf-8')) }
      catch { console.warn(`[PluginManager] Invalid package.json in ${entry.name}`); continue }

      const pluginType = meta['tscg-plugin-type'] || 'server'
      const pluginName = meta.name || entry.name

      if (pluginType === 'server' || pluginType === 'both') {
        const mainFile = meta.main || 'index.js'
        const mainPath = path.join(pluginDir, mainFile)
        if (fs.existsSync(mainPath)) {
          this.serverPlugins.push({ name: pluginName, dir: pluginDir, mainPath, meta })
          console.log(`[PluginManager] Server plugin: ${pluginName}`)
        } else {
          console.warn(`[PluginManager] ${pluginName}: server entry not found (${mainPath})`)
        }
      }

      if (pluginType === 'renderer' || pluginType === 'both') {
        const rendererEntry = meta['renderer-main'] || 'renderer.js'
        const rendererPath  = path.join(pluginDir, rendererEntry)
        if (fs.existsSync(rendererPath)) {
          this.rendererPlugins.push({ name: pluginName, dir: pluginDir, rendererEntry, meta })
          console.log(`[PluginManager] Renderer plugin: ${pluginName}`)
        } else {
          console.warn(`[PluginManager] ${pluginName}: renderer entry not found (${rendererPath})`)
        }
      }
    }

    console.log(
      `[PluginManager] ${this.serverPlugins.length} server, ` +
      `${this.rendererPlugins.length} renderer plugin(s) found`
    )
  }

  // ── Install from .tgz ─────────────────────────────────────────
  // npm pack generates a .tgz with a 'package/' subdirectory inside.
  installFromTgz (tgzPath) {
    const { execSync } = require('child_process')
    const os    = require('os')
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tscg-plugin-'))

    try {
      execSync(`tar -xzf "${tgzPath}" -C "${tmpDir}"`, { stdio: 'pipe' })
      const extractedDir = path.join(tmpDir, 'package')
      if (!fs.existsSync(extractedDir))
        throw new Error('Unexpected .tgz structure: "package" subdirectory not found')

      const meta       = JSON.parse(fs.readFileSync(path.join(extractedDir, 'package.json'), 'utf-8'))
      const pluginName = meta.name || path.basename(tgzPath, '.tgz')
      const destDir    = path.join(this.pluginsPath, pluginName)

      if (fs.existsSync(destDir)) fs.rmSync(destDir, { recursive: true })
      fs.cpSync(extractedDir, destDir, { recursive: true })

      console.log(`[PluginManager] Installed: ${pluginName}`)
      return pluginName
    } finally {
      fs.rmSync(tmpDir, { recursive: true, force: true })
    }
  }

  // ── Uninstall ─────────────────────────────────────────────────
  uninstall (pluginName) {
    const dir = path.join(this.pluginsPath, pluginName)
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true })
      console.log(`[PluginManager] Uninstalled: ${pluginName}`)
      return true
    }
    return false
  }

  // ── List all installed plugin metadata ────────────────────────
  listInstalled () {
    if (!fs.existsSync(this.pluginsPath)) return []
    const result = []
    for (const entry of fs.readdirSync(this.pluginsPath, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue
      const pkgPath = path.join(this.pluginsPath, entry.name, 'package.json')
      if (!fs.existsSync(pkgPath)) continue
      try { result.push(JSON.parse(fs.readFileSync(pkgPath, 'utf-8'))) } catch { /* skip */ }
    }
    return result
  }
}

module.exports = PluginManager
