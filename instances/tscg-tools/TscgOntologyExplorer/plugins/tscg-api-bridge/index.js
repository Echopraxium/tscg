// =============================================================
// tscg-api-bridge — index.js   (CJS, server plugin)
// Replaces tscg-python-bridge. Spawns TscgOntologyAPIServer
// (instances/tscg-tools/TscgOntologyAPIServer/src/tscg_api_server.py)
// and exposes a control-panel dialog via Tools/Plugins menu.
//
// Plugin meta keys (set in TscgOntologyExplorer plugin config):
//   tscg-python-executable   Python binary (default: python)
//   tscg-api-host            Bind host      (default: 127.0.0.1)
//   tscg-api-port            Bind port      (default: 8000)
//   tscg-api-store-path      .oxg file path (default: app.getPath('userData')/tscg_store.oxg)
//   tscg-api-ontology-dir    Auto-load dir  (default: none)
//   tscg-api-log-level       uvicorn level  (default: warning)
//
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const { app, ipcMain, BrowserWindow } = require('electron')
const { spawn } = require('child_process')
const net       = require('net')
const path      = require('path')
const fs        = require('fs')

// ── Server script location ────────────────────────────────────
// Resolution order:
//   1. pluginMeta['tscg-api-server-script'] — absolute path (recommended)
//   2. pluginMeta['tscg-repo-root'] + relative path
//   3. Relative from __dirname (only works when plugin runs from repo, not AppData)
//
// Since the plugin is installed in AppData, option 1 or 2 must be set
// in package.json > meta > tscg-api-server-script or tscg-repo-root.
const _SERVER_SCRIPT_REL = path.join(
  'instances', 'tscg-tools', 'TscgOntologyAPIServer', 'src', 'tscg_api_server.py'
)
// ── Read meta directly from local package.json ───────────────
function _readLocalMeta () {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf-8'))
    return pkg.meta || pkg['tscg-plugin']?.meta || {}
  } catch (e) {
    console.warn('[tscg-api-bridge] _readLocalMeta failed:', e.message)
    return {}
  }
}

function _resolveServerScript (meta) {
  // Option 1: explicit absolute path
  if (meta['tscg-api-server-script'] && fs.existsSync(meta['tscg-api-server-script']))
    return meta['tscg-api-server-script']
  // Option 2: repo root provided
  if (meta['tscg-repo-root']) {
    const p = path.join(meta['tscg-repo-root'], _SERVER_SCRIPT_REL)
    if (fs.existsSync(p)) return p
  }
  // Option 3: fallback relative from __dirname (works only from repo)
  return path.resolve(__dirname, '..', '..', '..', '..', _SERVER_SCRIPT_REL)
}
// SERVER_SCRIPT resolved lazily in startServer() after meta is available
const SERVER_SCRIPT = null   // placeholder — resolved in startServer()
const DIALOG_HTML = path.join(__dirname, 'api-server-dialog.html')

const HEALTH_TIMEOUT = 20000
const HEALTH_POLL_MS = 400

// ── Module state ──────────────────────────────────────────────
let _proc      = null
let _port      = null
let _baseUrl   = null
let _startedAt = null
let _logLines  = []          // circular buffer (last 500 lines)
const LOG_MAX  = 500

// ── Port detection ────────────────────────────────────────────
function findFreePort (preferred) {
  return new Promise((resolve, reject) => {
    const srv = net.createServer()
    srv.listen(preferred, '127.0.0.1', () => {
      const p = srv.address().port
      srv.close(() => resolve(p))
    })
    srv.on('error', () => {
      if (preferred < 8020) resolve(findFreePort(preferred + 1))
      else reject(new Error('No free port found in range 8000-8020'))
    })
  })
}

// ── Health polling ────────────────────────────────────────────
function waitForReady (port) {
  const start = Date.now()
  return new Promise((resolve, reject) => {
    const poll = () => {
      if (Date.now() - start > HEALTH_TIMEOUT)
        return reject(new Error(`TscgOntologyAPIServer did not start within ${HEALTH_TIMEOUT}ms`))
      fetch(`http://127.0.0.1:${port}/health`)
        .then(r => r.ok ? resolve() : setTimeout(poll, HEALTH_POLL_MS))
        .catch(()  => setTimeout(poll, HEALTH_POLL_MS))
    }
    poll()
  })
}

// ── Log capture ───────────────────────────────────────────────
function _pushLog (line, api) {
  _logLines.push(line)
  if (_logLines.length > LOG_MAX) _logLines.shift()
  // Forward to all open dialog windows
  for (const win of BrowserWindow.getAllWindows()) {
    if (!win.isDestroyed())
      win.webContents.executeJavaScript(
        `window.dispatchEvent(new CustomEvent('tscg-api-log',
           { detail: ${JSON.stringify(line)} }))`, true
      ).catch(() => {})
  }
  api.log(line)
}

// ── Server lifecycle ──────────────────────────────────────────
async function startServer (api) {
  if (_proc) { api.warn('[tscg-api-bridge] Already running'); return }

  // Merge api.pluginMeta (may be empty) with local package.json meta
  const localMeta  = _readLocalMeta()
  const meta       = Object.assign({}, localMeta, api.pluginMeta || {})
  console.log('[tscg-api-bridge] meta tscg-repo-root:', meta['tscg-repo-root'])
  const pythonExe  = meta['tscg-python-executable'] || 'python'
  const host       = meta['tscg-api-host']          || '127.0.0.1'
  const wantedPort = parseInt(meta['tscg-api-port'] || '8000', 10)
  const ontDir     = meta['tscg-api-ontology-dir']  || null
  const logLevel   = meta['tscg-api-log-level']     || 'warning'

  // ── Store path: pluginMeta override → userData default ───────
  const _userDataDir = app.getPath('userData')
  if (!fs.existsSync(_userDataDir)) fs.mkdirSync(_userDataDir, { recursive: true })
  const storePath = meta['tscg-api-store-path'] || path.join(_userDataDir, 'tscg_store.oxg')
  api.log(`[tscg-api-bridge] Store path: ${storePath}`)

  const SERVER_SCRIPT = _resolveServerScript(meta)
  if (!fs.existsSync(SERVER_SCRIPT))
    throw new Error(`Server script not found:\n${SERVER_SCRIPT}`)

  const port = await findFreePort(wantedPort)
  if (port !== wantedPort)
    api.log(`[tscg-api-bridge] Port ${wantedPort} busy — using ${port}`)

  const pyArgs = [SERVER_SCRIPT, '--host', host, '--port', String(port),
                  '--log-level', logLevel, '--store-path', storePath]
  if (ontDir) pyArgs.push('--ontology-dir', ontDir)

  api.log(`[tscg-api-bridge] Spawning: ${pythonExe} ${pyArgs.join(' ')}`)
  _pushLog(`▶ Starting TscgOntologyAPIServer on ${host}:${port}`, api)

  _proc = spawn(pythonExe, pyArgs, {
    stdio: ['ignore', 'pipe', 'pipe'],
    windowsHide: true,
  })

  _proc.stdout.on('data', d => _pushLog(d.toString().trim(), api))
  _proc.stderr.on('data', d => {
    const msg = d.toString().trim()
    if (!msg.includes('INFO') && !msg.includes('WARNING'))
      _pushLog('[err] ' + msg, api)
  })
  _proc.on('error', err => {
    _pushLog('[proc error] ' + err.message, api)
    _proc = null
  })
  _proc.on('exit', (code, signal) => {
    _pushLog(`■ Server exited (code=${code}, signal=${signal})`, api)
    _proc = null; _port = null; _baseUrl = null; _startedAt = null
    api.sendToRenderer('api-server-stopped', { code, signal })
    _refreshMenu(api)
  })

  await waitForReady(port)

  _port = port; _baseUrl = `http://${host}:${port}`; _startedAt = Date.now()
  global.tscgApiServerUrl  = _baseUrl
  global.tscgApiServerPort = _port

  _pushLog(`✔ Server ready → ${_baseUrl}`, api)
  _pushLog(`  Swagger UI  → ${_baseUrl}/docs`, api)
  api.sendToRenderer('api-server-ready', { url: _baseUrl, port })
}

function stopServer (api) {
  if (!_proc) return Promise.resolve()
  _pushLog('■ Stopping server…', api)
  return new Promise(resolve => {
    _proc.once('exit', () => resolve())
    _proc.kill('SIGTERM')
  })
}

async function restartServer (api) {
  _pushLog('↺ Restarting server…', api)
  await stopServer(api)
  await startServer(api)
}

// ── Status fetch (used by dialog) ─────────────────────────────
async function _fetchStatus () {
  if (!_proc || !_baseUrl) return { running: false }
  try {
    const [health, info, layers] = await Promise.all([
      fetch(`${_baseUrl}/health`).then(r => r.json()),
      fetch(`${_baseUrl}/info`).then(r => r.json()),
      fetch(`${_baseUrl}/corpus/layers`).then(r => r.json()),
    ])
    return { running: true, url: _baseUrl, health, info, layers }
  } catch {
    return { running: false }
  }
}

// ── Dialog window ─────────────────────────────────────────────
let _dialogWin = null

function openDialog (api) {
  // If already open, just focus it
  if (_dialogWin && !_dialogWin.isDestroyed()) {
    _dialogWin.focus()
    return
  }

  const mainWin = BrowserWindow.getFocusedWindow() ||
                  BrowserWindow.getAllWindows()[0]

  _dialogWin = new BrowserWindow({
    width:          820,
    height:         640,
    title:          'TscgOntologyAPIServer — Control Panel',
    parent:         mainWin || undefined,
    modal:          false,
    resizable:      true,
    minimizable:    true,
    maximizable:    false,
    webPreferences: {
      nodeIntegration:  true,
      contextIsolation: false,
    }
  })

  _dialogWin.setMenu(null)
  _dialogWin.loadFile(DIALOG_HTML)

  // Once loaded — inject bridge functions and initial data
  _dialogWin.webContents.on('did-finish-load', () => {
    const logsJson    = JSON.stringify(_logLines.join('\n'))
    const localMeta   = _readLocalMeta()
    const _userDataDir = app.getPath('userData')
    const configJson  = JSON.stringify({
      ...localMeta,
      __defaultStorePath: path.join(_userDataDir, 'tscg_store.oxg')
    })

    _dialogWin.webContents.executeJavaScript(`
      // Bridge functions — nodeIntegration=true so ipcRenderer is available
      const { ipcRenderer } = require('electron')
      window.__tscgApiBridge = {
        action:      (a)  => ipcRenderer.invoke('tscg-api-bridge-dialog', { type: a }),
        getStatus:   ()   => ipcRenderer.invoke('tscg-api-bridge-dialog', { type: 'status' }),
        getConfig:   ()   => ipcRenderer.invoke('tscg-api-bridge-dialog', { type: 'config' }),
        openSwagger: ()   => ipcRenderer.invoke('tscg-api-bridge-dialog', { type: 'swagger' }),
        closeDialog: ()   => ipcRenderer.invoke('tscg-api-bridge-dialog', { type: 'close' }),
      }
      // Replay buffered logs
      const buffered = ${logsJson}
      if (buffered) {
        const el = document.getElementById('log-area')
        if (el) { el.textContent = buffered; el.scrollTop = el.scrollHeight }
      }
      // Pre-populate config tab
      if (typeof renderConfig === 'function') renderConfig(${configJson})
      if (typeof refreshStatus === 'function') refreshStatus()
    `, true).catch(e => console.warn('[tscg-api-bridge] dialog init error:', e.message))
  })

  // Forward log lines to dialog window
  const _logForward = (line) => {
    if (_dialogWin && !_dialogWin.isDestroyed())
      _dialogWin.webContents.executeJavaScript(
        `window.dispatchEvent(new CustomEvent('tscg-api-log',{ detail: ${JSON.stringify('__placeholder__')} }))`.replace('__placeholder__', line.replace(/\\/g,'\\\\').replace(/'/g,"\\'")), true
      ).catch(() => {})
  }

  // IPC handler for dialog commands
  const IPC_CH = 'tscg-api-bridge-dialog'
  // ipcMain.handle throws if channel already registered — remove first
  try { ipcMain.removeHandler(IPC_CH) } catch (_) {}
  ipcMain.handle(IPC_CH, async (_evt, msg) => {
      switch (msg.type) {
        case 'start':   await startServer(api);   _refreshMenu(api); return { ok: true }
        case 'stop':    await stopServer(api);    _refreshMenu(api); return { ok: true }
        case 'restart': await restartServer(api); _refreshMenu(api); return { ok: true }
        case 'status':  return _fetchStatus()
        case 'config': {
          const _ud  = app.getPath('userData')
          const lm   = _readLocalMeta()
          return { ...lm, __defaultStorePath: path.join(_ud, 'tscg_store.oxg') }
        }
        case 'swagger':
          if (_baseUrl) require('electron').shell.openExternal(`${_baseUrl}/docs`)
          return {}
        case 'close':
          if (_dialogWin && !_dialogWin.isDestroyed()) _dialogWin.close()
          return {}
        default: return {}
      }
    })

  _dialogWin.on('closed', () => { _dialogWin = null })
}

// ── Menu refresh ──────────────────────────────────────────────
function _refreshMenu (api) {
  const running = !!_proc
  api.updateMenuItem('api-dialog', {
    label: running
      ? `⚙️  API Server Control Panel  ✅  port ${_port}`
      : '⚙️  API Server Control Panel  ❌  (stopped)'
  })
}

// ── Plugin entry point ────────────────────────────────────────
module.exports = function TscgApiBridge (api) {
  initPlugin(api).catch(err => {
    api.warn('[tscg-api-bridge] Init failed:', err.message)
    api.showPopup(
      `TscgOntologyAPIServer failed to start:\n${err.message}\n\n` +
      `Check:\n• Python in PATH\n• pip install -r requirements.txt\n` +
      `• tscg_api_server.py at:\n  ${SERVER_SCRIPT}`,
      'tscg-api-bridge Error'
    )
  })
}

async function initPlugin (api) {
  api.log('[tscg-api-bridge] Initialising…')

  // Single menu entry — opens the control panel dialog
  api.registerMenuItem({
    label: '⚙️  API Server Control Panel  ❌  (stopped)',
    id:    'api-dialog',
    group: 'TSCG API Server',
  })

  api.onAction('api-dialog', () => openDialog(api))

  // ── IPC via plugin-to-server (contextIsolation safe) ─────────
  api.onFromRenderer('tscg-api-bridge-cmd', async (msg) => {
    const mainWin = require('electron').BrowserWindow.getAllWindows()[0]
    const send = (data) => {
      if (mainWin && !mainWin.isDestroyed())
        mainWin.webContents.send('plugin:tscg-api-bridge-result', data)
    }
    switch (msg.type) {
      case 'start':   await startServer(api);   _refreshMenu(api); break
      case 'stop':    await stopServer(api);    _refreshMenu(api); break
      case 'restart': await restartServer(api); _refreshMenu(api); break
      case 'status':  send({ id: msg.id, result: await _fetchStatus() }); break
      case 'config': {
        const _userDataDir = require('electron').app.getPath('userData')
        const localMeta    = _readLocalMeta()
        send({ id: msg.id, result: {
          ...localMeta,
          __defaultStorePath: require('path').join(_userDataDir, 'tscg_store.oxg')
        }}); break
      }
      case 'swagger':
        if (_baseUrl) require('electron').shell.openExternal(`${_baseUrl}/docs`); break
      case 'close':
        const win = require('electron').BrowserWindow.getAllWindows()[0]
        if (win) win.webContents.executeJavaScript(
          `(function(){ const el=document.getElementById('tscg-api-dialog-overlay'); if(el) el.remove() })()`, true
        ).catch(()=>{}); break
    }
  })

  // Auto-start
  await startServer(api)
  _refreshMenu(api)

  // Kill on quit
  app.on('before-quit', async () => {
    api.log('[tscg-api-bridge] Shutting down…')
    await stopServer(api)
  })
}
