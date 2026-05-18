// =============================================================
// TscgOntologyEditor — src/renderer/OntologyLoader.js   (ESM)
// Loads TSCG ontology files via the Python bridge and populates
// the Object Explorer (left panel).
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

// ── State ──────────────────────────────────────────────────────
let _bridgeUrl    = null    // set by setBridgeUrl() once bridge is ready
let _activeFile   = null    // currently loaded file path
let _onSelectCb   = null    // callback when an object is selected

// ── Preconfigured layer paths (absolute, filled by main via IPC) ──
// Populated by setRepoRoot() from the main process __dirname chain
let _repoRoot = null

const LAYER_FILES = {
  M3: 'M3_GenesisSpace.jsonld',
  M2: 'M2_GenericConcepts.jsonld',
  M1: 'M1_CoreConcepts.jsonld',
}

// ── API ─────────────────────────────────────────────────────────

export function setBridgeUrl (url) {
  _bridgeUrl = url
  console.log('[OntologyLoader] Bridge URL set:', url)
}

export function setRepoRoot (root) {
  _repoRoot = root
}

export function onObjectSelected (callback) {
  _onSelectCb = callback
}

// Load a layer by name (M3/M2/M1)
export async function loadLayer (layerName) {
  if (!_repoRoot) {
    showError('Repository root not set. Cannot resolve layer paths.')
    return
  }
  const relPath = LAYER_FILES[layerName]
  if (!relPath) { showError(`Unknown layer: ${layerName}`); return }

  // Build absolute path — repo root is TscgOntologyEditor's parent×3
  // e.g. .../tscg/instances/tscg-tools/TscgOntologyEditor → .../tscg/ontology/
  const ontologyRoot = _repoRoot
    .replace(/\\/g, '/')
    .replace(/instances\/tscg-tools\/TscgOntologyEditor.*$/, 'ontology')

  const absPath = ontologyRoot + '/' + relPath
  await loadFile(absPath)
}

// Load any .jsonld file by absolute path
export async function loadFile (absPath) {
  if (!_bridgeUrl) {
    showError('Python bridge not ready yet. Please wait a moment.')
    return
  }

  setStatus(`Loading ${absPath.split('/').pop()}…`)
  showLoading()

  try {
    const res  = await fetch(`${_bridgeUrl}/load`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ file_path: absPath })
    })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || res.statusText)
    }

    const data = await res.json()
    _activeFile = absPath

    setStatus(`${data.objects.length} objects — ${data.triples} triples`)
    populateObjectExplorer(data.objects)

  } catch (err) {
    showError(`Load failed: ${err.message}`)
    setStatus('Load error.')
  }
}

// ── Object Explorer population ──────────────────────────────────
function populateObjectExplorer (objects) {
  const tree = document.getElementById('object-tree')
  if (!tree) return

  if (objects.length === 0) {
    tree.innerHTML = '<p class="placeholder">No objects found in this ontology.</p>'
    return
  }

  // Group by @type
  const groups = {}
  for (const obj of objects) {
    const typeName = shortLabel(obj.type) || 'Untyped'
    if (!groups[typeName]) groups[typeName] = []
    groups[typeName].push(obj)
  }

  tree.innerHTML = ''

  for (const [typeName, items] of Object.entries(groups)) {
    // Group header (collapsible)
    const header = document.createElement('div')
    header.className   = 'tree-group-header'
    header.textContent = `▾ ${typeName} (${items.length})`
    tree.appendChild(header)

    const list = document.createElement('div')
    list.className = 'tree-group-items'
    tree.appendChild(list)

    // Toggle collapse
    header.addEventListener('click', () => {
      const collapsed = list.style.display === 'none'
      list.style.display  = collapsed ? '' : 'none'
      header.textContent  = `${collapsed ? '▾' : '▸'} ${typeName} (${items.length})`
    })

    for (const obj of items) {
      const item = document.createElement('div')
      item.className   = 'tree-item'
      item.textContent = obj.label || shortLabel(obj.id) || obj.id
      item.title       = obj.id
      item.dataset.id  = obj.id

      item.addEventListener('click', () => {
        // Highlight
        document.querySelectorAll('.tree-item').forEach(el => el.classList.remove('selected'))
        item.classList.add('selected')
        // Callback → PropertyInspector + right panel
        if (_onSelectCb) _onSelectCb({ ...obj, filePath: _activeFile })
      })

      list.appendChild(item)
    }
  }
}

// ── Helpers ─────────────────────────────────────────────────────
function shortLabel (uri) {
  if (!uri) return ''
  return uri.split('#').pop().split('/').pop()
}

function showLoading () {
  const tree = document.getElementById('object-tree')
  if (tree) tree.innerHTML = '<p class="placeholder">Loading…</p>'
}

function showError (msg) {
  const tree = document.getElementById('object-tree')
  if (tree) tree.innerHTML = `<p class="placeholder" style="color:#f38ba8">${msg}</p>`
  console.error('[OntologyLoader]', msg)
}

function setStatus (msg) {
  const el = document.getElementById('status-msg')
  if (el) el.textContent = msg
}
