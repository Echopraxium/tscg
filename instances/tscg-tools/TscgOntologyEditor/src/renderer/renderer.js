// =============================================================
// TscgOntologyEditor — src/renderer/renderer.js   (ESM)
// Main renderer: theme + commands + MDI + plugins + ontology.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

import { createRendererApiFor, dispatchAction,
         getMenuItems, getTabs, notifyOntologyChanged } from './RendererPluginApi.js'
import { initSplitters }                                from './Splitter.js'
import { setBridgeUrl, getBridgeUrl, getOntologyRoot, setRepoRoot, setLayerPaths, setBridgeButtonsEnabled,
         setExplorerRenderer, onDocumentLoaded, activateDocument, loadLayer, loadFile, onObjectSelected } from './OntologyLoader.js'
import { renderObjectExplorer }                                     from './ObjectExplorer.js'
import { registry }                                     from '../commands/CommandRegistry.js'
import { docManager, renderTabBar }                     from './DocumentManager.js'

// =============================================================
// 1. THEME
// =============================================================
function applyTheme (name) {
  const link = document.getElementById('theme-stylesheet')
  if (link) link.href = `themes/${name}.css`
  console.log('[renderer] Theme applied:', name)
}

window.tscgAPI.onThemeInit(applyTheme)
window.tscgAPI.onThemeChanged(applyTheme)

// =============================================================
// 2. SPLITTERS
// =============================================================
initSplitters()

// Wire ObjectExplorer — OntologyLoader injects filePath into onSelect automatically
setExplorerRenderer(({ objects, pairs, onSelect }) => {
  renderObjectExplorer({ objects, pairs, onSelect })
})

// Wire document tab creation + populate Imports tab after each ontology load
onDocumentLoaded(({ filePath, label }) => {
  const nameNoExt  = label.replace(/\.jsonld$/i, '')
  const layerMatch = nameNoExt.match(/^(M[0-9]+)_(.+)$/)
  const layerName  = layerMatch ? layerMatch[1] : null

  docManager.open({ filePath, label: nameNoExt, layerName })
  renderTabBar()

  // Populate Imports tab for the newly loaded ontology
  populateImportsTab(filePath)
})


// =============================================================
// 3. BRIDGE BUTTONS — disabled until bridge ready
// =============================================================
setBridgeButtonsEnabled(false)

window.tscgAPI.onFromServer('bridge-ready', ({ url }) => {
  console.log('[renderer] Python bridge ready:', url)
  setBridgeUrl(url)
  document.getElementById('status-msg').textContent = `Python bridge ready — ${url}`
})

// =============================================================
// 4. REPO ROOT + ONTOLOGY ROOT
// =============================================================
window.tscgAPI.onFromServer('repo-root', ({ root }) => {
  setRepoRoot(root)
  console.log('[renderer] Repo root:', root)
})

window.tscgAPI.onOntologyRoot((root) => {
  setRepoRoot(root)
  console.log('[renderer] Ontology root (from config):', root)
})

// Auto-load default ontology on startup (local path or URL)
window.tscgAPI.onAutoLoadOntology(async (pathOrUrl) => {
  console.log('[renderer] Auto-loading default ontology:', pathOrUrl)
  const label = pathOrUrl.split(/[/\\]/).pop()
  setLabel(`${label} loading…`)
  await loadFile(pathOrUrl)
  setLabel(label.replace(/\.jsonld$/i, ''))
})

// Layer paths from M0_TscgOntologyEditor.jsonld (single source of truth)
window.tscgAPI.onLayerPaths((paths) => setLayerPaths(paths))

// =============================================================
// 5. COMMAND REGISTRY — wire execute functions
// =============================================================
registry.get('file.openM3').execute = () => { setLabel('M3 loading…'); loadLayer('M3').then(() => setLabel('M3')) }
registry.get('file.openM2').execute = () => { setLabel('M2 loading…'); loadLayer('M2').then(() => setLabel('M2')) }
registry.get('file.openM1').execute = () => { setLabel('M1 loading…'); loadLayer('M1').then(() => setLabel('M1')) }
registry.get('edit.preferences').execute = () => window.tscgAPI.openPreferences()
registry.get('help.about').execute = () => {} // handled by main menu

// Undo/Redo from Edit menu

// Command palette (stub)
window.tscgAPI.onOpenCommandPalette(() => {
  console.log('[renderer] Command palette — stub (coming soon)')
  // TODO: open command palette overlay
})

// Export As — native format picker then bridge export + save dialog
window.tscgAPI.onExportAs(async () => {
  const activeDoc = docManager.active
  if (!activeDoc?.filePath) { alert('No ontology loaded.'); return }
  const bridgeUrl = getBridgeUrl()
  if (!bridgeUrl) { alert('Python bridge not ready.'); return }

  const fmt = await window.tscgAPI.showExportFormatDialog()
  if (!fmt) return

  try {
    setStatus(`Exporting as ${fmt.extension}\u2026`)
    const res = await fetch(`${bridgeUrl}/export`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ file_path: activeDoc.filePath, format: fmt.id })
    })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
    const data = await res.json()
    window.tscgAPI.saveExport({
      filePath:  activeDoc.filePath,
      format:    fmt.id,
      content:   data.content,
      extension: data.extension
    })
    setStatus(`Exported ${data.triples} triples as ${fmt.extension}`)
  } catch (err) {
    setStatus(`Export failed: ${err.message}`)
  }
})

// =============================================================
// 6. LAYER NAVIGATION BUTTONS
// =============================================================
document.getElementById('btn-m3').addEventListener('click', () => registry.execute('file.openM3'))
document.getElementById('btn-m2').addEventListener('click', () => registry.execute('file.openM2'))
document.getElementById('btn-m1').addEventListener('click', () => registry.execute('file.openM1'))

window.tscgAPI.onLoadLayer(async (layerName) => {
  setLabel(`${layerName} loading…`)
  await loadLayer(layerName)
  setLabel(layerName)
})
window.tscgAPI.onLoadFile(async (filePath) => {
  setLabel(filePath.split(/[/\\]/).pop())
  await loadFile(filePath)
})

function setLabel (text) {
  const el = document.getElementById('active-ontology-label')
  if (el) el.textContent = text
}

// =============================================================
// 7. DOCUMENT MANAGER (MDI tabs)
// =============================================================
docManager.onChange((type, doc) => {
  renderTabBar()
  if (type === 'activate' && doc) {
    const name = (doc.layerName ? `${doc.layerName}:` : '') + doc.label.replace(/^M[0-9]+_/, '')
    setLabel(name)
    // Reset Property Inspector and Description tab
    const drawers = document.getElementById('property-drawers')
    if (drawers) drawers.innerHTML = '<p class="placeholder">Select an object to inspect its properties.</p>'
    const descPane = document.getElementById('tab-description')
    if (descPane) descPane.innerHTML = '<p class="placeholder">Select an object.</p>'
    // Restore Object Explorer from cache (or reload from bridge)
    activateDocument(doc.filePath)
    // Refresh Imports tab for the activated document
    populateImportsTab(doc.filePath)
  }
})

// =============================================================
// 8. OBJECT SELECTION
// =============================================================
onObjectSelected(async (obj) => {
  // Show basic info immediately
  populatePropertyInspector(obj, null)
  populateDescriptionTab(obj)
  docManager.updateActive({ selectedObjectId: obj.id, selectedObject: obj })
  notifyOntologyChanged({ layer: null, filePath: obj.filePath, label: obj.label })

  // Fetch real property values from bridge
  const bridgeUrl = getBridgeUrl()
  console.log('[renderer] Properties fetch: bridgeUrl=', !!bridgeUrl, 'filePath=', !!obj.filePath, 'id=', !!obj.id)
  if (bridgeUrl && obj.filePath && obj.id) {
    try {
      const url = `${bridgeUrl}/properties?file_path=${encodeURIComponent(obj.filePath)}&subject_uri=${encodeURIComponent(obj.id)}`
      const res = await fetch(url)
      if (res.ok) {
        const data = await res.json()
        populatePropertyInspector(obj, data.properties)
      }
    } catch (err) {
      console.warn('[renderer] Could not fetch properties:', err.message)
    }
  }
})

// properties: array of { predicate: {type, value}, object: {type, value} } from bridge
// or null for initial display (shows … placeholders)
function populatePropertyInspector (obj, properties) {
  const drawers = document.getElementById('property-drawers')
  if (!drawers) return
  drawers.innerHTML = ''

  // Identity drawer — always from obj
  drawers.appendChild(createDrawer('Identity', {
    '@id':   obj.id,
    '@type': obj.type
  }))

  if (!properties) {
    // Initial placeholder — real values loading
    const placeholder = { 'rdfs:label': obj.label || '…' }
    for (const k of (obj.keys || [])) placeholder[k] = '⟳ loading…'
    drawers.appendChild(createDrawer('Properties', placeholder))
    return
  }

  // Group properties by predicate namespace for separate drawers
  const groups = { Label: {}, Metadata: {}, Other: {} }
  for (const { predicate, object } of properties) {
    const pred  = predicate.value
    const short = pred.split('#').pop().split('/').pop()
    const val   = object.type === 'literal'
      ? object.value
      : `<${object.value}>`

    if (pred.includes('label') || pred.includes('comment')) {
      groups.Label[short] = val
    } else if (pred.includes('type') || pred.includes('version') || pred.includes('creator') || pred.includes('created')) {
      groups.Metadata[short] = val
    } else {
      groups.Other[short] = val
    }
  }

  for (const [title, props] of Object.entries(groups)) {
    if (Object.keys(props).length === 0) continue
    drawers.appendChild(createDrawer(title, props))
  }
}

function isUri (val) {
  return typeof val === 'string' && (val.startsWith('http://') || val.startsWith('https://'))
}

function createDrawer (title, props) {
  const wrap   = document.createElement('div')
  wrap.className = 'drawer'
  const header = document.createElement('div')
  header.className   = 'drawer-header'
  header.textContent = `▾ ${title}`
  const body   = document.createElement('div')
  body.className = 'drawer-body'

  for (const [k, v] of Object.entries(props)) {
    const row = document.createElement('div')
    row.className = 'drawer-row'

    const keyEl = document.createElement('span')
    keyEl.className   = 'drawer-key'
    keyEl.textContent = k

    const valEl = document.createElement('span')
    valEl.className = 'drawer-val'

    const strVal = v ?? '—'

    if (isUri(strVal)) {
      // URI value — render as clickable link, double-click opens browser
      valEl.textContent = strVal
      valEl.classList.add('drawer-val-uri')
      valEl.title = 'Double-click to open in browser'
      valEl.addEventListener('dblclick', () => {
        window.tscgAPI.openExternal(strVal)
      })
    } else {
      valEl.textContent = strVal
    }

    row.appendChild(keyEl)
    row.appendChild(valEl)
    body.appendChild(row)
  }

  header.addEventListener('click', () => {
    const open = body.style.display !== 'none'
    body.style.display  = open ? 'none' : ''
    header.textContent  = `${open ? '▸' : '▾'} ${title}`
  })
  wrap.appendChild(header)
  wrap.appendChild(body)
  return wrap
}

function populateDescriptionTab (obj) {
  const pane = document.getElementById('tab-description')
  if (!pane) return

  // IRI chip: compact "prefix:LocalName" label, full IRI in tooltip
  const iriStr = obj.id || ''
  const sep    = Math.max(iriStr.lastIndexOf('#'), iriStr.lastIndexOf('/'))
  const local  = sep >= 0 ? iriStr.slice(sep + 1) : iriStr
  const ns     = sep >= 0 ? iriStr.slice(0, sep + 1) : ''
  // Derive short prefix from filename stem (M2_GenericConcepts → M2, M1_CoreConcepts → M1, etc.)
  const stem   = ns.replace(/[#/]+$/, '').split('/').pop().replace(/\.jsonld$/i, '')
  const prefix = stem
    .replace(/^M(\\d+)_.*/, (_, n) => 'M' + n)
    .replace(/M3_([A-Za-z]+)/, 'M3')

  pane.innerHTML = `
    <div class="desc-block"><div class="desc-label">Label</div><div class="desc-value">${obj.label || '\u2014'}</div></div>
    <div class="desc-block"><div class="desc-label">Type</div><div class="desc-value">${obj.type || '\u2014'}</div></div>
    <div class="desc-block"><div class="desc-label">IRI</div><div id="desc-iri-chip"></div></div>`

  const chipWrap = pane.querySelector('#desc-iri-chip')
  if (iriStr && chipWrap) {
    const chip = document.createElement('span')
    chip.className    = 'imports-chip imports-chip-local'
    chip.textContent  = prefix ? `${prefix}:${local}` : local
    chip.title        = iriStr    // full IRI visible on hover
    chip.style.cursor = 'pointer'
    chip.style.margin = '4px 12px'
    chip.addEventListener('click', () => window.tscgAPI.openExternal(iriStr))
    chipWrap.appendChild(chip)
  } else if (chipWrap) {
    chipWrap.textContent = '\u2014'
  }
}

// ── Imports tab ────────────────────────────────────────────────
async function populateImportsTab (filePath) {
  const pane = document.getElementById('tab-imports')
  if (!pane) return
  const bridgeUrl = getBridgeUrl()
  if (!bridgeUrl || !filePath) {
    pane.innerHTML = '<p class="placeholder">Load an ontology to see its imports.</p>'
    return
  }
  pane.innerHTML = '<p class="placeholder">Loading imports…</p>'
  try {
    const res  = await fetch(`${bridgeUrl}/imports?file_path=${encodeURIComponent(filePath)}`)
    if (!res.ok) throw new Error(res.statusText)
    const data = await res.json()
    pane.innerHTML = ''

    // Helper: create a clickable chip (prefix or suffix)
    // Label is displayed; full URI shown only in tooltip on hover
    const makeChip = (label, uri, isLocal, localPath) => {
      const chip = document.createElement('span')
      chip.className    = isLocal ? 'imports-chip imports-chip-local' : 'imports-chip'
      chip.textContent  = label
      chip.title        = uri    // full URI as bubble info (tooltip)
      chip.style.cursor = 'pointer'
      chip.addEventListener('click', () => {
        if (isLocal && localPath) {
          loadFile(localPath)
        } else if (isLocal) {
          const ontRoot  = getOntologyRoot()
          const filename = uri.split('#')[0].replace(/\/$/, '').split('/').pop()
          if (ontRoot && filename.endsWith('.jsonld')) loadFile(ontRoot + '/' + filename)
          else window.tscgAPI.openExternal(uri)
        } else {
          window.tscgAPI.openExternal(uri)
        }
      })
      return chip
    }

    // ── @context Namespaces — show PREFIX key as chip ───────────
    if (data.namespaces.length > 0) {
      const h = document.createElement('div')
      h.className = 'desc-block'
      h.innerHTML = '<div class="desc-label">@context Namespaces</div>'
      pane.appendChild(h)
      const wrap = document.createElement('div')
      wrap.className = 'imports-chips'
      for (const ns of data.namespaces) {
        wrap.appendChild(makeChip(ns.prefix + ':', ns.uri, ns.is_local, ns.local_path))
      }
      pane.appendChild(wrap)
    }

    // ── owl:imports — show filename SUFFIX as chip ───────────────
    if (data.owl_imports.length > 0) {
      const h = document.createElement('div')
      h.className = 'desc-block'
      h.style.marginTop = '8px'
      h.innerHTML = '<div class="desc-label">owl:imports</div>'
      pane.appendChild(h)
      const wrap = document.createElement('div')
      wrap.className = 'imports-chips'
      for (const imp of data.owl_imports) {
        const suffix = imp.uri.split('/').pop().replace(/\.jsonld$/i, '').replace(/#.*$/, '')
        wrap.appendChild(makeChip(suffix, imp.uri, imp.is_local, imp.local_path))
      }
      pane.appendChild(wrap)
    }

    if (!data.namespaces.length && !data.owl_imports.length) {
      pane.innerHTML = '<p class="placeholder">No imports found.</p>'
    }
  } catch (err) {
    pane.innerHTML = `<p class="placeholder" style="color:var(--danger)">Error: ${err.message}</p>`
  }
}

// =============================================================
// 9. RENDERER PLUGINS
// =============================================================
async function loadRendererPlugins (pluginList) {
  for (const plugin of pluginList) {
    try {
      const mod = await import(`plugin://${plugin.name}/${plugin.rendererEntry}`)
      if (typeof mod.init !== 'function') continue
      mod.init(createRendererApiFor(plugin.name))
      console.log('[renderer] Renderer plugin loaded:', plugin.name)
    } catch (err) {
      console.error(`[renderer] Failed to load ${plugin.name}:`, err)
    }
  }
  window.tscgAPI.sendRendererPluginMenuItems(getMenuItems())
  injectPluginTabs()
}

window.tscgAPI.onRendererPluginsList(async (list) => {
  if (list.length > 0) await loadRendererPlugins(list)
  else window.tscgAPI.sendRendererPluginMenuItems([])
})
window.tscgAPI.onTriggerRendererAction((id) => dispatchAction(id))

// =============================================================
// 10. PLUGIN TABS
// =============================================================
function injectPluginTabs () {
  const tabBar = document.getElementById('tab-bar')
  const tabContent = document.getElementById('tab-content')
  if (!tabBar || !tabContent) return
  for (const tab of getTabs()) {
    const btn = document.createElement('button')
    btn.className = 'tab-btn'; btn.dataset.tab = tab.id
    btn.dataset.plugin = tab.pluginName; btn.textContent = tab.label
    tabBar.appendChild(btn)
    const pane = document.createElement('div')
    pane.id = `tab-${tab.id}`; pane.className = 'tab-pane plugin-tab'
    tabContent.appendChild(pane)
  }
  rebindTabHandlers()
}

function rebindTabHandlers () {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'))
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'))
      btn.classList.add('active')
      document.getElementById(`tab-${btn.dataset.tab}`)?.classList.add('active')
    }
  })
}
rebindTabHandlers()

// =============================================================
// 11. POPUP + MODE TOGGLE + MISC
// =============================================================
window.tscgAPI.onShowPopup((message, from) => {
  document.getElementById('popup-message').textContent = message
  const fromEl = document.getElementById('popup-from')
  if (fromEl) fromEl.textContent = from ? `— ${from}` : ''
  document.getElementById('popup-overlay').hidden = false
})
document.getElementById('popup-close').addEventListener('click', () => {
  document.getElementById('popup-overlay').hidden = true
})

document.body.dataset.mode = 'browse'

// =============================================================
// SPARQL PANEL
// =============================================================
document.getElementById('btn-sparql-run')?.addEventListener('click', async () => {
  const query   = document.getElementById('sparql-query')?.value?.trim()
  const results = document.getElementById('sparql-results')
  const status  = document.getElementById('sparql-status')
  const activeDoc = docManager.active

  if (!query)           { if (status) status.textContent = 'Enter a query.'; return }
  if (!activeDoc?.filePath) { if (status) status.textContent = 'Load an ontology first.'; return }

  const bridgeUrl = getBridgeUrl()
  if (!bridgeUrl)       { if (status) status.textContent = 'Bridge not ready.'; return }

  if (status) status.textContent = 'Running…'
  if (results) results.innerHTML = ''

  try {
    const res  = await fetch(`${bridgeUrl}/sparql`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ file_path: activeDoc.filePath, query })
    })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
    const data = await res.json()

    if (!data.results?.length) {
      if (status)  status.textContent = '0 results'
      if (results) results.innerHTML  = '<p class="placeholder">No results.</p>'
      return
    }

    // Build results table
    const vars = data.vars || Object.keys(data.results[0])
    const table = document.createElement('table')
    table.className = 'sparql-table'
    const head = document.createElement('tr')
    vars.forEach(v => { const th = document.createElement('th'); th.textContent = v; head.appendChild(th) })
    table.appendChild(document.createElement('thead')).appendChild(head)
    const tbody = document.createElement('tbody')
    for (const row of data.results) {
      const tr = document.createElement('tr')
      vars.forEach(v => {
        const td = document.createElement('td')
        const val = row[v] || ''
        td.textContent = val
        td.title       = val
        tr.appendChild(td)
      })
      tbody.appendChild(tr)
    }
    table.appendChild(tbody)
    if (results) results.appendChild(table)
    if (status)  status.textContent = `${data.results.length} row(s)`
  } catch (err) {
    if (status)  status.textContent = `Error: ${err.message}`
    if (results) results.innerHTML  = `<p class="placeholder" style="color:var(--danger)">${err.message}</p>`
  }
})

document.getElementById('btn-sparql-clear')?.addEventListener('click', () => {
  const q = document.getElementById('sparql-query')
  const r = document.getElementById('sparql-results')
  const s = document.getElementById('sparql-status')
  if (q) q.value = ''
  if (r) r.innerHTML = ''
  if (s) s.textContent = ''
})

window.tscgAPI.onOpenPluginManager(async () => {
  const list = await window.tscgAPI.listPlugins()
  alert(`Installed plugins:\n${list.map(p => `• ${p.name}`).join('\n') || '(none)'}`)
})

console.log('[renderer] Initialised.')

// ── Global click diagnostic (temporary) ──────────────────────
document.addEventListener('click', (e) => {
  const t = e.target
  console.log('[GLOBAL CLICK] tag:', t.tagName,
    'class:', t.className || '—',
    'text:', t.textContent?.trim().slice(0, 50) || '—')
}, true)  // capture phase — fires before any other handler
