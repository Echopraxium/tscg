// =============================================================
// TscgOntologyEditor — src/renderer/OntologyLoader.js   (ESM)
// Loads TSCG ontology files via the Python bridge.
// Queues requests made before the bridge is ready.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

let _bridgeUrl   = null
let _activeFile  = null
let _onSelectCb  = null
let _pendingLoad = null   // { type: 'layer'|'file', value: string }
let _repoRoot    = null

// Layer filenames — loaded from M0_TscgOntologyEditor.jsonld via main.js IPC.
// Do NOT hardcode here: the M0 ontology is the single source of truth.
let LAYER_FILES = {}

export function setLayerPaths (paths) {
  LAYER_FILES = paths
  console.log('[OntologyLoader] Layer paths set from M0:', paths)
}

// ── API ─────────────────────────────────────────────────────────

export function setBridgeUrl (url) {
  _bridgeUrl = url
  setBridgeButtonsEnabled(true)
  setBridgeIndicator(true)
  console.log('[OntologyLoader] Bridge URL set:', url)

  // Execute any queued request
  if (_pendingLoad) {
    const pending = _pendingLoad
    _pendingLoad  = null
    console.log('[OntologyLoader] Executing queued load:', pending)
    if (pending.type === 'layer') loadLayer(pending.value)
    else                          loadFile(pending.value)
  }
}

export function getBridgeUrl ()       { return _bridgeUrl }

export function getOntologyRoot () {
  // Returns the local ontology directory path (normalized, no trailing slash)
  if (!_repoRoot) return null
  const normalized = _repoRoot.replace(/\\/g, '/')
  return /\/ontology\/?$/.test(normalized)
    ? normalized.replace(/\/$/, '')
    : normalized + '/ontology'
}
export function setRepoRoot (root)  { _repoRoot = root }

export function onObjectSelected (callback) { _onSelectCb = callback }

// ── Disable/enable M1/M2/M3 buttons ──────────────────────────
export function setBridgeButtonsEnabled (enabled) {
  for (const id of ['btn-m3', 'btn-m2', 'btn-m1']) {
    const btn = document.getElementById(id)
    if (!btn) continue
    btn.disabled = !enabled
    btn.title    = enabled ? '' : 'Python bridge starting… please wait'
  }
  if (!enabled) setStatus('Python bridge starting…')
}

// ── Load a layer ──────────────────────────────────────────────
export async function loadLayer (layerName) {
  if (!_repoRoot) { showError('Repository root not set.'); return }

  if (!_bridgeUrl) {
    _pendingLoad = { type: 'layer', value: layerName }
    setStatus(`Bridge starting… "${layerName}" queued`)
    showPending()
    return
  }

  // Normalize ontology root (avoid double /ontology/)
  const normalized = _repoRoot.replace(/\\/g, '/')
  const ontRoot    = /\/ontology\/?$/.test(normalized)
    ? normalized.replace(/\/$/, '')
    : normalized + '/ontology'

  // For layers with multiple files (M3, M1), show a picker dialog
  // M2 has only one file — load directly
  const defaultFile = LAYER_FILES[layerName]
  if (!defaultFile) { showError(`Unknown layer: ${layerName}`); return }

  if (layerName === 'M2') {
    await loadFile(ontRoot + '/' + defaultFile)
    return
  }

  // Fetch available files for this layer
  try {
    const res   = await fetch(`${_bridgeUrl}/list-layer-files?ontology_root=${encodeURIComponent(ontRoot)}&layer=${layerName}`)
    const data  = await res.json()
    const files = data.files || []

    if (files.length === 0) {
      showError(`No ${layerName} files found in ${ontRoot}`)
      return
    }
    if (files.length === 1) {
      await loadFile(files[0].path)
      return
    }

    // Multiple files → show picker
    const chosen = await showLayerPicker(layerName, files)
    if (chosen) await loadFile(chosen)

  } catch (err) {
    showError(`Could not list ${layerName} files: ${err.message}`)
  }
}

// ── Layer file picker (inline HTML dialog) ─────────────────────
function showLayerPicker (layerName, files) {
  return new Promise(resolve => {
    // Remove existing picker if any
    document.getElementById('layer-picker-overlay')?.remove()

    const overlay = document.createElement('div')
    overlay.id        = 'layer-picker-overlay'
    overlay.className = 'popup-overlay'  // reuse popup CSS
    overlay.style.display = 'flex'

    const box = document.createElement('div')
    box.className = 'popup-box'
    box.style.minWidth = '340px'
    box.style.textAlign = 'left'

    const title = document.createElement('p')
    title.style.fontWeight = '600'
    title.style.marginBottom = '12px'
    title.style.fontSize = '14px'
    title.textContent = `Open ${layerName} ontology`
    box.appendChild(title)

    for (const f of files) {
      const btn = document.createElement('button')
      btn.style.cssText = 'display:block;width:100%;text-align:left;margin-bottom:8px;padding:8px 12px'
      btn.textContent = f.label
      btn.addEventListener('click', () => {
        overlay.remove()
        resolve(f.path)
      })
      box.appendChild(btn)
    }

    const cancel = document.createElement('button')
    cancel.style.cssText = 'display:block;width:100%;text-align:center;margin-top:4px;opacity:.6'
    cancel.textContent = 'Cancel'
    cancel.addEventListener('click', () => { overlay.remove(); resolve(null) })
    box.appendChild(cancel)

    overlay.appendChild(box)
    document.body.appendChild(overlay)
  })
}

// ── Load a file ───────────────────────────────────────────────
export async function loadFile (absPath) {
  if (!_bridgeUrl) {
    _pendingLoad = { type: 'file', value: absPath }
    setStatus(`Bridge starting… "${absPath.split(/[/\\]/).pop()}" queued`)
    showPending()
    return
  }

  setStatus(`Loading ${absPath.split(/[/\\]/).pop()}…`)
  showLoading()

  try {
    const res = await fetch(`${_bridgeUrl}/load`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_path: absPath })
    })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail || res.statusText) }

    const data = await res.json()
    _activeFile = absPath

    // Fetch hierarchy (rdfs:subClassOf pairs) for tree view
    let pairs = []
    try {
      const hRes = await fetch(`${_bridgeUrl}/hierarchy?file_path=${encodeURIComponent(absPath)}`)
      if (hRes.ok) { const hData = await hRes.json(); pairs = hData.pairs || [] }
    } catch { /* hierarchy optional */ }

    setStatus(`${data.objects.length} objects — ${data.triples} triples`)
    populateObjectExplorer(data.objects, pairs)

    // Cache the loaded data for fast tab switching
    _isDirty = true  // mark as fresh load in progress
    console.log('[OntologyLoader] Caching:', absPath.split(/[/\\]/).pop(),
      '| objects:', data.objects?.length,
      '| sample:', data.objects?.[1]?.id?.slice(-35))
    _docCache.set(absPath, { objects: data.objects, pairs })

    // Notify renderer to create/activate a document tab
    if (_onDocumentLoadedCb) {
      _onDocumentLoadedCb({
        filePath: absPath,
        label:    absPath.split(/[/\\]/).pop()
      })
    }

  } catch (err) {
    showError(`Load failed: ${err.message}`)
    setStatus('Load error.')
  }
}

// ── Object Explorer — delegates to ObjectExplorer.js module ─────
let _explorerRender      = null
let _onDocumentLoadedCb  = null

// ── Document cache ─────────────────────────────────────────────
// Stores { objects, pairs } per filePath so switching tabs
// doesn't require a full bridge round-trip.
const _docCache        = new Map()
let   _isDirty         = false  // true during fresh load — prevents double activate in onChange

export function setExplorerRenderer (fn) { _explorerRender = fn }
export function onDocumentLoaded (cb)    { _onDocumentLoadedCb = cb }
export function isDirtyLoad ()           { return _isDirty }
export function clearDirtyLoad ()        { _isDirty = false }

// Activate a document from the cache (called when switching tabs)
export async function activateDocument (filePath) {
  if (!filePath) return

  if (_docCache.has(filePath)) {
    // Fast path: restore from cache
    const { objects, pairs } = _docCache.get(filePath)
    _activeFile = filePath
    setStatus(`${objects.length} objects — cached`)
    populateObjectExplorer(objects, pairs)
    const stem = filePath.split(/[/\\]/).pop()
    console.log('[OntologyLoader] Activated from cache:', stem,
      '| objects:', objects.length,
      '| sample IRI:', objects[1]?.id?.slice(-35) || '?')
  } else {
    // Cache miss: load from bridge
    console.log('[OntologyLoader] Cache miss — loading from bridge:', filePath.split(/[/\\]/).pop())
    await loadFile(filePath)
  }
}

function populateObjectExplorer (objects, pairs) {
  if (_explorerRender) {
    // OntologyLoader injects _activeFile so downstream callbacks have the correct path
    _explorerRender({
      objects,
      pairs: pairs || [],
      onSelect: (obj) => {
        if (_onSelectCb) _onSelectCb({ ...obj, filePath: _activeFile })
      }
    })
    return
  }
  // Fallback: simple flat list
  const tree = document.getElementById('object-tree')
  if (!tree) return

  if (objects.length === 0) {
    tree.innerHTML = '<p class="placeholder">No objects found.</p>'
    return
  }

  const groups = {}
  for (const obj of objects) {
    const t = shortLabel(obj.type) || 'Untyped'
    if (!groups[t]) groups[t] = []
    groups[t].push(obj)
  }

  tree.innerHTML = ''

  for (const [typeName, items] of Object.entries(groups)) {
    const header = document.createElement('div')
    header.className   = 'tree-group-header'
    header.textContent = `▾ ${typeName} (${items.length})`
    tree.appendChild(header)

    const list = document.createElement('div')
    list.className = 'tree-group-items'
    tree.appendChild(list)

    header.addEventListener('click', () => {
      const collapsed    = list.style.display === 'none'
      list.style.display = collapsed ? '' : 'none'
      header.textContent = `${collapsed ? '▾' : '▸'} ${typeName} (${items.length})`
    })

    for (const obj of items) {
      const item = document.createElement('div')
      item.className   = 'tree-item'
      item.textContent = obj.label || shortLabel(obj.id) || obj.id
      item.title       = obj.id
      item.dataset.id  = obj.id
      item.addEventListener('click', () => {
        document.querySelectorAll('.tree-item').forEach(el => el.classList.remove('selected'))
        item.classList.add('selected')
        if (_onSelectCb) _onSelectCb({ ...obj, filePath: _activeFile })
      })
      list.appendChild(item)
    }
  }
}

// ── Helpers ────────────────────────────────────────────────────
function shortLabel (uri) {
  if (!uri) return ''
  return uri.split('#').pop().split('/').pop()
}

function showLoading () {
  const tree = document.getElementById('object-tree')
  if (tree) tree.innerHTML = '<p class="placeholder">Loading…</p>'
}

function showPending () {
  const tree = document.getElementById('object-tree')
  if (tree) tree.innerHTML = '<p class="placeholder">Bridge starting — load queued…</p>'
}

function showError (msg) {
  const tree = document.getElementById('object-tree')
  if (tree) tree.innerHTML = `<p class="placeholder" style="color:var(--danger)">${msg}</p>`
  console.error('[OntologyLoader]', msg)
}

function setStatus (msg) {
  const el = document.getElementById('status-msg')
  if (el) el.textContent = msg
}

function setBridgeIndicator (online) {
  const el = document.getElementById('bridge-indicator')
  if (!el) return
  el.textContent = online ? '● Bridge' : '○ Bridge'
  el.style.color = online ? 'var(--success)' : 'var(--danger)'
}
