// =============================================================
// TscgOntologyEditor — src/renderer/renderer.js   (ESM)
// Main renderer: theme + commands + MDI + plugins + ontology.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

import { createRendererApiFor, dispatchAction,
         getMenuItems, getTabs, notifyOntologyChanged } from './RendererPluginApi.js'
import { initSplitters }                                from './Splitter.js'
import { setBridgeUrl, getBridgeUrl, getOntologyRoot, setRepoRoot, setLayerPaths, setBridgeButtonsEnabled,
         setExplorerRenderer, onDocumentLoaded, activateDocument, isDirtyLoad, clearDirtyLoad,
         loadLayer, loadFile, onObjectSelected } from './OntologyLoader.js'
import { renderObjectExplorer, selectObjectByIri, setPendingSelectIri, applyPendingSelect, filterObjectTree } from './ObjectExplorer.js'
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
  activateDocument(filePath)  // ensure Object Explorer shows the new doc
  clearDirtyLoad()              // allow tab-switch activations again
  populateImportsTab(filePath)
})
  setTimeout(() => applyPendingSelect(), 250)  // cross-doc navigation


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
document.getElementById('btn-m1').addEventListener('click', async (e) => {
  // Remove any existing dropdown
  document.getElementById('m1-ext-dropdown')?.remove()
  const btn     = e.currentTarget
  const btnRect = btn.getBoundingClientRect()

  const drop = document.createElement('div')
  drop.id = 'm1-ext-dropdown'
  Object.assign(drop.style, {
    position: 'fixed', top: `${btnRect.bottom + 4}px`, left: `${btnRect.left}px`,
    minWidth: '220px', maxHeight: '320px', overflowY: 'auto',
    background: 'var(--bg-drawer)', border: '1px solid var(--accent)',
    borderRadius: '6px', boxShadow: '0 4px 16px rgba(0,0,0,.4)',
    zIndex: '9999', fontSize: '11px',
  })

  const addSection = (label) => {
    const h = document.createElement('div')
    Object.assign(h.style, { padding: '5px 12px 3px', color: 'var(--text-muted)',
      fontSize: '10px', fontWeight: '700', borderBottom: '1px solid var(--border)' })
    h.textContent = label; drop.appendChild(h)
  }
  const addItem = (label, filePath, accent = false) => {
    const item = document.createElement('div')
    Object.assign(item.style, { padding: '7px 16px', cursor: 'pointer',
      color: accent ? 'var(--accent)' : 'var(--text-primary)',
      fontWeight: accent ? '700' : '400' })
    item.textContent = label
    item.onmouseenter = () => { item.style.background = 'var(--bg-hover)' }
    item.onmouseleave = () => { item.style.background = '' }
    item.addEventListener('click', () => { drop.remove(); loadFile(filePath) })
    drop.appendChild(item)
  }

  addSection('M1 Layer')
  const ontRoot = getOntologyRoot()
  if (ontRoot) addItem('M1_CoreConcepts  ★', ontRoot + '/M1_CoreConcepts.jsonld', true)

  const sep = document.createElement('div')
  sep.style.cssText = 'height:1px;background:var(--border);margin:2px 0'
  drop.appendChild(sep)
  addSection('Extensions')

  try {
    const exts = await window.tscgAPI.listM1Extensions()
    if (!exts?.length) {
      addItem('(no extensions found)', null)
    } else {
      for (const ext of exts)
        addItem(ext.name.replace(/^M1_/, ''), ext.path)
    }
  } catch (err) {
    addItem('Error: ' + err.message, null)
  }

  document.body.appendChild(drop)
  const close = (ev) => {
    if (!drop.contains(ev.target) && ev.target !== btn) {
      drop.remove(); document.removeEventListener('click', close, true)
    }
  }
  setTimeout(() => document.addEventListener('click', close, true), 10)
})

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
    // Restore Object Explorer — skip if just freshly loaded (onDocumentLoaded handles it)
    if (!isDirtyLoad()) {
      activateDocument(doc.filePath)
    }
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
    const val   = (object.type === 'literal' || object.type === 'bnode_resolved' || object.type === 'uri')
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
      const isInternal = strVal.includes('echopraxium') || strVal.includes('raw.githubusercontent')
      const sep    = Math.max(strVal.lastIndexOf('#'), strVal.lastIndexOf('/'))
      const local  = sep >= 0 ? strVal.slice(sep + 1) : strVal
      const stem   = strVal.slice(0, sep).split('/').pop().replace(/\.jsonld$/i, '')
      const prefix = stem.replace(/^M(\d+)_.*/,  (_, n) => 'M' + n)

      // Chip only for same-document URIs (same filename stem)
      const activeDoc    = docManager.active
      const activeFile   = activeDoc?.filePath || ''
      const activeStem   = activeFile.split(/[/\\]/).pop().replace(/\.jsonld$/i, '')
      const isSameDoc    = isInternal && strVal.includes(activeStem)

      if (isSameDoc) {
        valEl.className    = 'imports-chip imports-chip-local'
        valEl.textContent  = prefix ? `${prefix}:${local}` : local
        valEl.title        = strVal + '\nClick: navigate to this object'
        valEl.style.cursor = 'pointer'
        valEl.style.margin = '2px 0'
        valEl.addEventListener('click', (e) => { e.stopPropagation(); selectObjectByIri(strVal) })
        // Also make the whole row clickable (chip may not cover full cell area)
        row.style.cursor = 'pointer'
        row.addEventListener('click', () => selectObjectByIri(strVal))
      } else if (isInternal) {
        // Cross-document internal URI → plain text (no chip, no broken nav)
        valEl.textContent = prefix ? `${prefix}:${local}` : local
        valEl.title       = strVal
        valEl.style.color = 'var(--text-secondary)'
      } else {
        // External URI → open in browser on click
        valEl.textContent = strVal
        valEl.classList.add('drawer-val-uri')
        valEl.title = 'Click to open in browser'
        valEl.addEventListener('click', () => window.tscgAPI.openExternal(strVal))
      }
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

// ── Predefined queries ────────────────────────────────────────
const SPARQL_PRESETS = {
  // Exploration
  all_classes: `SELECT DISTINCT ?class ?label WHERE {
  ?class a owl:Class .
  OPTIONAL { ?class rdfs:label ?label }
} ORDER BY ?label`,

  all_properties: `SELECT DISTINCT ?prop ?type ?label WHERE {
  ?prop a ?type .
  VALUES ?type { owl:ObjectProperty owl:DatatypeProperty }
  OPTIONAL { ?prop rdfs:label ?label }
} ORDER BY ?type ?label`,

  class_hierarchy: `SELECT ?child ?parent WHERE {
  ?child rdfs:subClassOf ?parent .
  FILTER(!isBlank(?child) && !isBlank(?parent))
} ORDER BY ?parent ?child`,

  all_triples: `SELECT ?s ?p ?o WHERE {
  ?s ?p ?o .
  FILTER(!isBlank(?s))
} LIMIT 20`,

  // M2 GenericConcepts
  generic_concepts: `PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?concept ?label ?family WHERE {
  ?concept rdfs:subClassOf+ m2:GenericConcept .
  OPTIONAL { ?concept rdfs:label ?label }
  OPTIONAL { ?concept m2:hasFamily ?family }
} ORDER BY ?family ?label`,

  by_family: `PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?family (COUNT(?concept) AS ?count) WHERE {
  ?concept rdfs:subClassOf+ m2:GenericConcept .
  ?concept m2:hasFamily ?family .
} GROUP BY ?family ORDER BY DESC(?count)`,

  structural_formulas: `PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?concept ?label ?formula WHERE {
  ?concept rdfs:subClassOf+ m2:GenericConcept .
  ?concept m2:hasStructuralGrammarFormula ?formula .
  OPTIONAL { ?concept rdfs:label ?label }
} ORDER BY ?label`,

  dual_polarity: `PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?concept ?label ?formula WHERE {
  ?concept m2:hasPolarity "dual" .
  OPTIONAL { ?concept rdfs:label ?label }
  OPTIONAL { ?concept m2:hasStructuralGrammarFormula ?formula }
} ORDER BY ?label`,

  dominant_m3: `PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dim (GROUP_CONCAT(?label; separator=", ") AS ?concepts) WHERE {
  ?concept m2:hasDominantM3 ?dim .
  OPTIONAL { ?concept rdfs:label ?label }
} GROUP BY ?dim ORDER BY ?dim`,

  // M3 Dimensions
  m3_dimensions: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dim ?label ?symbol WHERE {
  ?dim a m3:M3Dimension .
  OPTIONAL { ?dim rdfs:label ?label }
  OPTIONAL { ?dim m3:dimensionSymbol ?symbol }
} ORDER BY ?symbol`,

  asfid_dims: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dim ?label ?symbol WHERE {
  ?dim a m3:M3Dimension .
  OPTIONAL { ?dim rdfs:label ?label }
  OPTIONAL { ?dim m3:dimensionSymbol ?symbol }
} ORDER BY ?symbol`,

  revoi_dims: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dim ?label ?symbol WHERE {
  ?dim a m3:M3Dimension .
  OPTIONAL { ?dim rdfs:label ?label }
  OPTIONAL { ?dim m3:dimensionSymbol ?symbol }
} ORDER BY ?symbol`,

  // M0 Instances
  poclets: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?poclet ?label WHERE {
  ?poclet a m3:Poclet .
  OPTIONAL { ?poclet rdfs:label ?label }
} ORDER BY ?label`,

  asfid_scores: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#>
SELECT ?attractor ?structure ?flow ?information ?dynamics WHERE {
  ?instance m3:hasAttractor ?attractor ;
            m3:hasStructure ?structure ;
            m3:hasFlow      ?flow ;
            m3:hasInformation ?information ;
            m3:hasDynamics  ?dynamics .
} LIMIT 10`,

  // Utilities
  named_graphs: `SELECT DISTINCT ?g WHERE {
  GRAPH ?g { ?s ?p ?o }
} ORDER BY ?g`,

  owl_imports: `SELECT ?import WHERE {
  ?ont a owl:Ontology .
  ?ont owl:imports ?import .
}`,

  ontology_meta: `PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?version ?creator ?created WHERE {
  ?ont a owl:Ontology .
  OPTIONAL { ?ont owl:versionInfo ?version }
  OPTIONAL { ?ont dcterms:creator ?creator }
  OPTIONAL { ?ont dcterms:created ?created }
}`,
}

document.getElementById('sparql-presets')?.addEventListener('change', (e) => {
  const key = e.target.value
  if (!key || !SPARQL_PRESETS[key]) return
  const ta = document.getElementById('sparql-query')
  if (ta) {
    ta.value = SPARQL_PRESETS[key]
    ta.focus()
  }
  e.target.value = ''  // reset so same query can be re-selected
})
// Last SPARQL results for Save As
let _lastSparqlResults   = null
let _lastSparqlVars      = []
let _lastSparqlQueryType = 'SELECT'

document.getElementById('btn-sparql-save')?.addEventListener('click', async () => {
  if (!_lastSparqlResults?.length) return
  const ts       = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
  const isTurtle = _lastSparqlQueryType === 'CONSTRUCT'
  const ext      = isTurtle ? 'ttl' : 'csv'
  const filename = `SPARQL_OUTPUT_${ts}.${ext}`

  let fileContent
  if (isTurtle) {
    // CONSTRUCT → Turtle (.ttl): results are RDF triples
    fileContent = _lastSparqlResults
      .map(r => {
        const s = typeof r.s === 'object' ? r.s.value : (r.s || '')
        const p = typeof r.p === 'object' ? r.p.value : (r.p || '')
        const o = typeof r.o === 'object' ? r.o.value : (r.o || '')
        return `<${s}> <${p}> <${o}> .`
      }).join('\n')
    fileContent = '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n' + fileContent
  } else {
    // SELECT → CSV (tabular)
    const header = _lastSparqlVars.join(',')
    const rows   = _lastSparqlResults.map(row =>
      _lastSparqlVars.map(v => {
        const raw = row[v]
        const val = raw === null || raw === undefined ? ''
                  : typeof raw === 'object' ? (raw.value || '') : String(raw)
        return `"${val.replace(/"/g, '""')}"`
      }).join(',')
    )
    fileContent = [header, ...rows].join('\n')
  }
  await window.tscgAPI.saveSparqlOutput({ filename, content: fileContent })
})

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
        const td  = document.createElement('td')
        const raw = row[v]
        // SPARQL results come as {type, value} objects from rdflib
        const val = raw === null || raw === undefined ? '—'
                  : typeof raw === 'object' ? (raw.value || JSON.stringify(raw))
                  : String(raw)
        // Shorten long URIs for display, keep full in tooltip
        const display = val.length > 60 && val.startsWith('http')
          ? '…' + val.slice(val.lastIndexOf('/') + 1).slice(0, 50)
          : val
        td.textContent = display
        td.title       = val
        tr.appendChild(td)
      })
      tbody.appendChild(tr)
    }
    table.appendChild(tbody)
    if (results) results.appendChild(table)
    if (status)  status.textContent = `${data.results.length} row(s)`
    // Store for Save As
    _lastSparqlResults   = data.results
    _lastSparqlVars      = vars
    _lastSparqlQueryType = data.query_type || 'SELECT'
    const saveBtn = document.getElementById('btn-sparql-save')
    if (saveBtn) saveBtn.disabled = false
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
  _lastSparqlResults = null; _lastSparqlVars = []
  const saveBtn = document.getElementById('btn-sparql-save')
  if (saveBtn) saveBtn.disabled = true
})

window.tscgAPI.onOpenPluginManager(async () => {
  const list = await window.tscgAPI.listPlugins()
  alert(`Installed plugins:\n${list.map(p => `• ${p.name}`).join('\n') || '(none)'}`)
})

console.log('[renderer] Initialised.')

// ── Object Explorer search (Ctrl+F / Edit > Find) ──────────────
const searchBar   = document.getElementById('oe-search-bar')
const searchInput = document.getElementById('oe-search-input')
const searchCount = document.getElementById('oe-search-count')
const searchClose = document.getElementById('oe-search-close')

function openSearch () {
  if (!searchBar) return
  searchBar.style.display = 'flex'
  searchInput?.focus()
  searchInput?.select()
}
function closeSearch () {
  if (!searchBar) return
  searchBar.style.display = 'none'
  if (searchInput) searchInput.value = ''
  filterObjectTree('')
  searchCount.textContent = ''
}

searchInput?.addEventListener('input', () => {
  const q = searchInput.value
  if (!q.trim()) { filterObjectTree(''); searchCount.textContent = ''; return }
  const n = filterObjectTree(q)
  searchCount.textContent = n ? `${n} match${n > 1 ? 'es' : ''}` : 'no match'
  searchCount.style.color = n ? 'var(--accent)' : 'var(--danger)'
})
searchInput?.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeSearch()
})
searchClose?.addEventListener('click', closeSearch)

// Ctrl+F → open search (global)
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
    e.preventDefault()
    openSearch()
  }
})

// Expose for Edit menu IPC
window.tscgAPI.onFindInOntology?.(() => openSearch())
