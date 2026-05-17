// =============================================================
// tscg-python-bridge — index.js   (CJS, main process)
// Server plugin: spawns a persistent FastAPI/Python process,
// exposes it as global.pythonBridgeUrl for other server plugins.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

const { app }    = require('electron')
const { spawn }  = require('child_process')
const net        = require('net')
const path       = require('path')
const fs         = require('fs')

const BRIDGE_SCRIPT  = path.join(__dirname, 'bridge_server.py')
const DEFAULT_PORT   = 7432
const HEALTH_TIMEOUT = 15000   // ms to wait for server ready
const HEALTH_POLL_MS = 300     // polling interval

// ── Port detection ─────────────────────────────────────────────
function findFreePort (start) {
  return new Promise((resolve, reject) => {
    const srv = net.createServer()
    srv.listen(start, '127.0.0.1', () => {
      const port = srv.address().port
      srv.close(() => resolve(port))
    })
    srv.on('error', () => {
      if (start < DEFAULT_PORT + 20) resolve(findFreePort(start + 1))
      else reject(new Error('No free port found in range'))
    })
  })
}

// ── Health check ───────────────────────────────────────────────
function waitForReady (port) {
  const start = Date.now()
  return new Promise((resolve, reject) => {
    const poll = () => {
      if (Date.now() - start > HEALTH_TIMEOUT) {
        return reject(new Error(`Python bridge did not start within ${HEALTH_TIMEOUT}ms`))
      }
      fetch(`http://127.0.0.1:${port}/health`)
        .then(r => r.ok ? resolve() : setTimeout(poll, HEALTH_POLL_MS))
        .catch(() => setTimeout(poll, HEALTH_POLL_MS))
    }
    poll()
  })
}

// ── Plugin factory ─────────────────────────────────────────────
module.exports = function TscgPythonBridge (api) {
  initBridge(api).catch(err => {
    api.warn('Bridge initialisation failed:', err.message)
    api.showPopup(
      `Python Bridge failed to start:\n${err.message}\n\nCheck that Python is in PATH and run:\npip install -r requirements.txt`,
      'TscgPythonBridge Error'
    )
  })
}

async function initBridge (api) {
  api.log('Starting Python bridge…')

  // ── 1. Find free port ────────────────────────────────────────
  const port = await findFreePort(DEFAULT_PORT)
  if (port !== DEFAULT_PORT) {
    api.log(`Port ${DEFAULT_PORT} busy — using port ${port}`)
  }

  // ── 2. Spawn Python server ───────────────────────────────────
  const pythonExe = api.pluginMeta?.['tscg-python-executable'] || 'python'
  const proc = spawn(pythonExe, [BRIDGE_SCRIPT, '--port', String(port)], {
    stdio: ['ignore', 'pipe', 'pipe'],
    windowsHide: true
  })

  proc.stdout.on('data', d => api.log('[py]', d.toString().trim()))
  proc.stderr.on('data', d => {
    const msg = d.toString().trim()
    // uvicorn writes INFO logs to stderr — filter real errors
    if (!msg.includes('INFO') && !msg.includes('WARNING')) {
      api.warn('[py-err]', msg)
    }
  })
  proc.on('error', err => api.warn('Python process error:', err.message))
  proc.on('exit', (code, signal) => {
    if (code !== 0 && signal !== 'SIGTERM') {
      api.warn(`Python bridge exited unexpectedly (code=${code})`)
    }
  })

  // ── 3. Wait until server is ready ────────────────────────────
  await waitForReady(port)
  api.log(`Python bridge ready → http://127.0.0.1:${port}`)

  // ── 4. Expose URL globally for other server plugins ──────────
  global.pythonBridgeUrl  = `http://127.0.0.1:${port}`
  global.pythonBridgePort = port

  // ── 5. Register menu item ────────────────────────────────────
  api.registerMenuItem({
    label: `Python Bridge — port ${port}`,
    id:    'bridge-status',
    group: 'Python Bridge'
  })
  api.onAction('bridge-status', async () => {
    try {
      const res  = await fetch(`${global.pythonBridgeUrl}/health`)
      const data = await res.json()
      api.showPopup(
        `Python Bridge status: ${data.status}\n` +
        `Port: ${port}\n` +
        `rdflib: ${data.rdflib_version}\n` +
        `pyshacl: ${data.pyshacl_version}\n` +
        `Ontologies loaded: ${data.ontologies_loaded}`,
        'Python Bridge Status'
      )
    } catch (e) {
      api.showPopup(`Bridge unreachable:\n${e.message}`, 'Python Bridge Error')
    }
  })

  // ── 6. Notify renderer of bridge URL via IPC ─────────────────
  api.sendToRenderer('bridge-ready', { url: global.pythonBridgeUrl, port })

  // ── 7. Kill Python on app quit ────────────────────────────────
  app.on('before-quit', () => {
    api.log('Shutting down Python bridge…')
    proc.kill('SIGTERM')
  })
}
