// =============================================================
// TscgOntologyExplorer — src/renderer/renderer.js   (ESM)
// Main renderer: theme + commands + MDI + plugins + ontology.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

import { createRendererApiFor, dispatchAction,
         getMenuItems, getTabs, notifyOntologyChanged } from './RendererPluginApi.js'
import { initSplitters }                                from './Splitter.js'
import { setBridgeUrl, getBridgeUrl, getOntologyRoot, setRepoRoot, setLayerPaths, setBridgeButtonsEnabled,
         setExplorerRenderer, onDocumentLoaded, activateDocument, isDirtyLoad, clearDirtyLoad,
         loadLayer, loadFile, onObjectSelected, findFileForIri, getInstanceOfTargets } from './OntologyLoader.js'
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
setExplorerRenderer(({ objects, pairs, externalParents, onSelect, onNavigateTo }) => {
  renderObjectExplorer({ objects, pairs, externalParents, onSelect, onNavigateTo })
})

// Ghost node styles (cross-file superclass links)
;(function injectGhostStyles () {
  if (document.getElementById('ghost-node-styles')) return
  const s = document.createElement('style')
  s.id = 'ghost-node-styles'
  s.textContent = `
    .oe-ghost { opacity: 0.82; cursor: pointer; }
    .oe-ghost:hover { opacity: 1; }
    .oe-ghost-lbl { color: var(--accent, #7eb8f7); font-style: italic; }
    .oe-ghost-badge {
      margin-left: 6px; font-size: 10px; opacity: 0.6;
      background: var(--bg-input, #2a2a2e); border-radius: 3px;
      padding: 1px 5px; vertical-align: middle;
    }
    .oe-ghost-sep {
      padding: 6px 8px 3px 8px; font-size: 10px; font-weight: 600;
      opacity: 0.5; text-transform: uppercase; letter-spacing: .05em;
      border-top: 1px solid var(--border, #3a3a3e); margin-top: 6px;
    }
  `
  document.head.appendChild(s)
})()

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
  // Switch to Imports tab automatically on load
  activateTab('imports')
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

// tscg-api-bridge (replaces tscg-python-bridge)
window.tscgAPI.onFromServer('api-server-ready', ({ url }) => {
  console.log('[renderer] TscgOntologyAPIServer ready:', url)
  setBridgeUrl(url)
  window._bridgeUrl = url
  setBridgeButtonsEnabled(true)
  document.getElementById('status-msg').textContent = `API Server ready — ${url}`
  // Trigger deferred auto-load: read defaultLoadedOntology from config and load it
  window.tscgAPI.config.get('defaultLoadedOntology').then(pathOrUrl => {
    if (pathOrUrl) {
      console.log('[renderer] API server ready — auto-loading:', pathOrUrl)
      const label = pathOrUrl.split(/[/\\]/).pop()
      setLabel(`${label} loading…`)
      loadFile(pathOrUrl).then(() => setLabel(label.replace(/\.jsonld$/i, '')))
    }
  }).catch(e => console.warn('[renderer] auto-load config error:', e))
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

// Layer paths from M0_TscgOntologyExplorer.jsonld (single source of truth)
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

// ── Shared dropdown builder ────────────────────────────────────
function buildDropdown (dropId, anchorEl) {
  document.getElementById(dropId)?.remove()
  const rect = anchorEl.getBoundingClientRect()
  const drop = document.createElement('div')
  drop.id = dropId
  Object.assign(drop.style, {
    position: 'fixed', top: `${rect.bottom + 4}px`, left: `${rect.left}px`,
    minWidth: '220px', maxHeight: '320px', overflowY: 'auto',
    background: 'var(--bg-drawer)', border: '1px solid var(--accent)',
    borderRadius: '6px', boxShadow: '0 4px 16px rgba(0,0,0,.4)',
    zIndex: '9999', fontSize: '11px',
  })

  // ── Section header — label + optional X button on same line ──
  let firstSection = true
  const addSection = (label, withClose = false) => {
    const row = document.createElement('div')
    Object.assign(row.style, {
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '5px 8px 4px 12px',
      borderBottom: '1px solid var(--border)',
      marginTop: firstSection ? '0' : '2px',
    })
    firstSection = false

    const lbl = document.createElement('span')
    Object.assign(lbl.style, {
      color: 'var(--text-secondary, #d0d8e8)',   // light label
      fontSize: '10px', fontWeight: '700', letterSpacing: '0.04em',
      textTransform: 'uppercase',
    })
    lbl.textContent = label
    row.appendChild(lbl)

    if (withClose) {
      const x = document.createElement('button')
      x.textContent = '✕'
      Object.assign(x.style, {
        background: 'none', border: 'none', cursor: 'pointer',
        color: 'var(--text-secondary, #b0b8c8)', fontSize: '11px',
        lineHeight: '1', padding: '1px 4px', borderRadius: '3px',
        flexShrink: '0',
      })
      x.title = 'Close'
      x.onmouseenter = () => { x.style.color = 'var(--text-primary)'; x.style.background = 'var(--bg-hover)' }
      x.onmouseleave = () => { x.style.color = 'var(--text-secondary, #b0b8c8)'; x.style.background = 'none' }
      x.addEventListener('click', (e) => { e.stopPropagation(); drop.remove() })
      row.appendChild(x)
    }
    drop.appendChild(row)
  }

  const addItem = (label, filePath, accent = false) => {
    if (!filePath) return
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
  const addSep = () => {
    const s = document.createElement('div')
    s.style.cssText = 'height:1px;background:var(--border);margin:2px 0'
    drop.appendChild(s)
  }
  return { drop, addSection, addItem, addSep }
}

function attachDropdownClose (drop, btn) {
  document.body.appendChild(drop)
  const close = (ev) => {
    if (!drop.contains(ev.target) && ev.target !== btn) {
      drop.remove()
      document.removeEventListener('click', close, true)
    }
  }
  setTimeout(() => document.addEventListener('click', close, true), 10)
}

// ── btn-m3 — dropdown (same behaviour as btn-m1) ───────────────
document.getElementById('btn-m3').addEventListener('click', async (e) => {
  const btn = e.currentTarget
  const { drop, addSection, addItem, addSep } = buildDropdown('m3-dropdown', btn)
  const ontRoot = getOntologyRoot()

  addSection('M3 Layer', true)
  if (ontRoot) {
    addItem('M3_GenesisGrammar  ★',          ontRoot + '/M3_GenesisGrammar.jsonld', true)
    addSep()
    addSection('Grammars')
    addItem('GrammarFoundation',             ontRoot + '/M3_GrammarFoundation.jsonld')
    addItem('EagleEye  (Gt / ASFID / ×)',    ontRoot + '/M3_EagleEye.jsonld')
    addItem('SphinxEye  (Gm / REVOI / +)',   ontRoot + '/M3_SphinxEye.jsonld')
    addItem('BicephalousPerspective  (Gs / |)', ontRoot + '/M3_BicephalousPerspective.jsonld')
  } else {
    const h = document.createElement('div')
    h.style.cssText = 'padding:10px 16px;color:var(--text-muted);font-size:11px'
    h.textContent = '(ontology root not set)'; drop.appendChild(h)
  }

  attachDropdownClose(drop, btn)
})

// ── btn-m2 — direct load ───────────────────────────────────────
document.getElementById('btn-m2').addEventListener('click', () => registry.execute('file.openM2'))

// ── btn-m1 — dropdown with extensions ─────────────────────────
document.getElementById('btn-m1').addEventListener('click', async (e) => {
  const btn = e.currentTarget
  const { drop, addSection, addItem, addSep } = buildDropdown('m1-ext-dropdown', btn)
  const ontRoot = getOntologyRoot()

  addSection('M1 Layer', true)
  if (ontRoot) {
    addItem('M1_CoreConcepts  ★', ontRoot + '/M1_CoreConcepts.jsonld', true)
    addItem('M1_Domains',         ontRoot + '/M1_Domains.jsonld')
  }
  addSep()
  addSection('Extensions')

  try {
    const exts = await window.tscgAPI.listM1Extensions()
    if (!exts?.length) {
      const h = document.createElement('div')
      h.style.cssText = 'padding:7px 16px;color:var(--text-muted)'
      h.textContent = '(no extensions found)'; drop.appendChild(h)
    } else {
      for (const ext of exts)
        addItem(ext.name.replace(/^M1_/, ''), ext.path)
    }
  } catch (err) {
    const h = document.createElement('div')
    h.style.cssText = 'padding:7px 16px;color:var(--danger)'
    h.textContent = 'Error: ' + err.message; drop.appendChild(h)
  }

  attachDropdownClose(drop, btn)
})

// ── Adjacent Layers panel ─────────────────────────────────────
// One dropdown button per adjacent layer (combolist style)
function renderAdjacentLayers (currentLayer, filePath) {
  const panel = document.getElementById('adjacent-layers-content')
  if (!panel) return
  panel.innerHTML = ''
  const ontRoot = getOntologyRoot()
  if (!ontRoot) { panel.innerHTML = '<p class="placeholder">Ontology root not set.</p>'; return }

  // ── M2 Metaclass section (m3:instanceOf) — M0 instances only ─
  const ioTargets = filePath ? getInstanceOfTargets(filePath) : []
  if (ioTargets.length > 0) {
    const metaSection = document.createElement('div')
    Object.assign(metaSection.style, { padding: '8px 8px 4px 8px' })

    const metaTitle = document.createElement('div')
    metaTitle.textContent = '↑ M2 Metaclass (instanceOf)'
    Object.assign(metaTitle.style, {
      fontSize: '10px', fontWeight: '700', textTransform: 'uppercase',
      letterSpacing: '.05em', opacity: '.55', marginBottom: '5px',
      color: 'var(--text-primary)'
    })
    metaSection.appendChild(metaTitle)

    for (const target of ioTargets) {
      const chip = document.createElement('div')
      chip.textContent = `↗ ${target.label}`
      chip.title = (target.file_path_hint
        ? target.file_path_hint.split(/[/\\]/).pop() + ' — '
        : '') + target.id + '\nClick to open'
      Object.assign(chip.style, {
        display: 'inline-block', margin: '2px 3px',
        padding: '3px 10px', borderRadius: '4px', cursor: 'pointer',
        fontSize: '12px', fontStyle: 'italic',
        background: 'var(--bg-input)', border: '1px solid var(--accent, #7eb8f7)',
        color: 'var(--accent, #7eb8f7)'
      })
      chip.onmouseenter = () => { chip.style.opacity = '1'; chip.style.background = 'var(--bg-hover, #2a2a3a)' }
      chip.onmouseleave = () => { chip.style.opacity = '.9'; chip.style.background = 'var(--bg-input)' }
      chip.addEventListener('click', () => {
        if (target.file_path_hint) {
          setPendingSelectIri(target.id)
          loadFile(target.file_path_hint)
        }
      })
      metaSection.appendChild(chip)
    }

    // Separator between metaclass section and standard layers
    const sep = document.createElement('hr')
    Object.assign(sep.style, { border: 'none', borderTop: '1px solid var(--border)', margin: '8px 0 4px 0' })
    metaSection.appendChild(sep)
    panel.appendChild(metaSection)
  }

  const layers = {
    M3: {
      label: 'M3',
      staticFiles: [
        { name: 'GenesisGrammar ★',                 file: 'M3_GenesisGrammar.jsonld',            accent: true },
        { name: 'GrammarFoundation',                 file: 'M3_GrammarFoundation.jsonld' },
        { name: 'EagleEye  (Gt / ASFID / ×)',        file: 'M3_EagleEye.jsonld' },
        { name: 'SphinxEye  (Gm / REVOI / +)',       file: 'M3_SphinxEye.jsonld' },
        { name: 'BicephalousPerspective  (Gs / |)',  file: 'M3_BicephalousPerspective.jsonld' },
      ]
    },
    M2: {
      label: 'M2',
      staticFiles: [
        { name: 'GenericConcepts ★', file: 'M2_GenericConcepts.jsonld', accent: true },
      ]
    },
    M1: {
      label: 'M1',
      staticFiles: [
        { name: 'CoreConcepts ★', file: 'M1_CoreConcepts.jsonld', accent: true },
        { name: 'Domains',        file: 'M1_Domains.jsonld' },
      ],
      dynamicExtensions: true
    },
  }

  const adjacentMap = {
    M0: ['M1'],
    M1: ['M2'],
    M2: ['M3', 'M1'],
    M3: ['M2'],
  }
  const adjacent = adjacentMap[currentLayer] || []

  if (!adjacent.length) {
    panel.innerHTML = '<p class="placeholder">No adjacent layers.</p>'
    return
  }

  const buttonsRow = document.createElement('div')
  Object.assign(buttonsRow.style, { display: 'flex', flexDirection: 'column', gap: '6px', padding: '8px' })

  for (const layerKey of adjacent) {
    const layer = layers[layerKey]
    if (!layer) continue

    const btn = document.createElement('button')
    btn.textContent = `${layer.label} ▾`
    Object.assign(btn.style, {
      display: 'block', width: '100%', textAlign: 'left',
      padding: '7px 12px', cursor: 'pointer',
      background: 'var(--bg-input)', border: '1px solid var(--border)',
      borderRadius: '5px', color: 'var(--text-primary)',
      fontSize: '12px', fontWeight: '600',
    })
    btn.onmouseenter = () => { btn.style.borderColor = 'var(--accent)' }
    btn.onmouseleave = () => { btn.style.borderColor = 'var(--border)' }

    btn.addEventListener('click', async () => {
      const dropId = `adj-drop-${layerKey}`
      if (document.getElementById(dropId)) {
        document.getElementById(dropId)?.remove()
        btn.textContent = `${layer.label} ▾`
        return
      }
      btn.textContent = `${layer.label} ▴`
      const { drop, addSection, addItem, addSep } = buildDropdown(dropId, btn)

      if (layer.staticFiles.length) {
        addSection(layer.label + ' Layer', true)
        for (const f of layer.staticFiles)
          addItem(f.name, ontRoot + '/' + f.file, f.accent || false)
      }
      if (layer.dynamicExtensions) {
        addSep()
        addSection('Extensions')
        try {
          const exts = await window.tscgAPI.listM1Extensions()
          if (!exts?.length) {
            const h = document.createElement('div')
            h.style.cssText = 'padding:7px 16px;color:var(--text-muted);font-size:11px'
            h.textContent = '(no extensions)'; drop.appendChild(h)
          } else {
            for (const ext of exts) addItem(ext.name.replace(/^M1_/, ''), ext.path)
          }
        } catch (err) {
          const h = document.createElement('div')
          h.style.cssText = 'padding:7px 16px;color:var(--danger)'
          h.textContent = 'Error: ' + err.message; drop.appendChild(h)
        }
      }

      document.body.appendChild(drop)
      const close = (ev) => {
        if (!drop.contains(ev.target) && ev.target !== btn) {
          drop.remove()
          btn.textContent = `${layer.label} ▾`
          document.removeEventListener('click', close, true)
        }
      }
      setTimeout(() => document.addEventListener('click', close, true), 10)
      drop.addEventListener('click', () => setTimeout(() => { btn.textContent = `${layer.label} ▾` }, 50))
    })

    buttonsRow.appendChild(btn)
  }
  panel.appendChild(buttonsRow)
}

// Hook into document activation to update Adjacent Layers
docManager.onChange((type, doc) => {
  if (type === 'activate' && doc?.layerName) {
    renderAdjacentLayers(doc.layerName, doc.filePath)
  }
})

// Rename "Neighbor Layers" → "Adjacent Layers" in DOM if present
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-label="Neighbor Layers"], #neighbor-layers-title').forEach(el => {
    el.textContent = 'Adjacent Layers'
  })
}, { once: true })

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
  const addProp = (group, key, val) => {
    if (group[key] === undefined) {
      group[key] = val
    } else {
      // Second occurrence — promote to array (e.g. polar formula pairs)
      if (!Array.isArray(group[key])) group[key] = [group[key]]
      group[key].push(val)
    }
  }
  for (const { predicate, object } of properties) {
    const pred  = predicate.value
    const short = pred.split('#').pop().split('/').pop()
    const val   = (object.type === 'literal' || object.type === 'bnode_resolved' || object.type === 'uri')
      ? object.value
      : `<${object.value}>`

    if (pred.includes('label') || pred.includes('comment')) {
      addProp(groups.Label, short, val)
    } else if (pred.includes('type') || pred.includes('version') || pred.includes('creator') || pred.includes('created')) {
      addProp(groups.Metadata, short, val)
    } else {
      addProp(groups.Other, short, val)
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

    // ── Array value — polar formula pair (or other multi-value property) ──
    if (Array.isArray(v)) {
      const isPolarFormula = k.toLowerCase().includes('structuralgrammarformula')
        && v.length === 2
        && v.some(f => f.includes('_^') || f.includes('_$') || f.includes('_{+}') || f.includes('_{-}'))

      if (isPolarFormula) {
        // Render as a 2-element array table — full formula on each row
        const table = document.createElement('table')
        table.style.cssText = 'width:100%;border-collapse:collapse;font-size:11px;margin-top:2px'
        for (const [i, formula] of v.entries()) {
          const isPos  = formula.includes('_^') || formula.includes('_{+}')
          const color  = isPos ? 'var(--success, #4caf82)' : 'var(--danger, #e07070)'
          const tr     = document.createElement('tr')
          const tdIdx  = document.createElement('td')
          tdIdx.textContent = `[${i}]`
          tdIdx.style.cssText = `width:24px;color:var(--text-muted);padding:2px 6px 2px 0;font-size:10px;vertical-align:top`
          const tdForm = document.createElement('td')
          tdForm.textContent = formula
          tdForm.style.cssText = `font-family:monospace;color:${color};padding:2px 0`
          tr.appendChild(tdIdx); tr.appendChild(tdForm)
          table.appendChild(tr)
        }
        row.appendChild(keyEl)
        row.appendChild(table)
        body.appendChild(row)
        continue
      }

      // Generic array — join with newlines
      valEl.textContent = v.join('\n')
      valEl.style.whiteSpace = 'pre-wrap'
      row.appendChild(keyEl); row.appendChild(valEl)
      body.appendChild(row)
      continue
    }

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
        // Cross-document internal URI → clickable chip (same style as Imports tab)
        // Derive local file path: extract .jsonld filename from IRI, join with ontology root
        const fileBase  = strVal.split('#')[0].split('/').pop()   // e.g. "M2_GenericConcepts.jsonld"
        const ontRoot   = getOntologyRoot()
        const localPath = (ontRoot && fileBase.endsWith('.jsonld'))
          ? ontRoot + '/' + fileBase
          : null

        valEl.className   = 'imports-chip'
        valEl.textContent = prefix ? `${prefix}:${local}` : local
        valEl.title       = (localPath
          ? `${localPath.split(/[/\\]/).pop()}\nClick to open and navigate`
          : strVal)
        valEl.style.cursor = 'pointer'
        valEl.style.margin = '2px 0'

        if (localPath) {
          const navigate = (e) => {
            e?.stopPropagation()
            // Check if the IRI is already in a loaded document (e.g. m1:extension:biology:Hormone
            // expands to M1_CoreConcepts.jsonld#... but the class lives in M1_Biology.jsonld)
            const cachedFile = findFileForIri(strVal)
            if (cachedFile) {
              // Found in a cached doc — activate it and select the node
              activateDocument(cachedFile).then(() => selectObjectByIri(strVal))
            } else {
              // Not in cache — load the file derived from the IRI
              setPendingSelectIri(strVal)
              loadFile(localPath)
            }
          }
          valEl.addEventListener('click', navigate)
          row.style.cursor = 'pointer'
          row.addEventListener('click', navigate)
        }
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
    btn.onclick = () => activateTab(btn.dataset.tab)
  })
}

function activateTab (tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'))
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'))
  const btn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`)
  if (btn) btn.classList.add('active')
  document.getElementById(`tab-${tabId}`)?.classList.add('active')
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
  ?dim a m3:MonoidalType .
  OPTIONAL { ?dim rdfs:label ?label }
  OPTIONAL { ?dim m3:typeSymbol ?symbol }
} ORDER BY ?symbol`,

  asfid_dims: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dim ?label ?symbol WHERE {
  ?dim a m3:MonoidalType .
  OPTIONAL { ?dim rdfs:label ?label }
  OPTIONAL { ?dim m3:typeSymbol ?symbol }
} ORDER BY ?symbol`,

  revoi_dims: `PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dim ?label ?symbol WHERE {
  ?dim a m3:MonoidalType .
  OPTIONAL { ?dim rdfs:label ?label }
  OPTIONAL { ?dim m3:typeSymbol ?symbol }
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

  // ── Corpus presets (multi-file SPARQL) ────────────────────────
  corpus_m1_classes: `PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?graph ?class ?label WHERE {
  GRAPH ?graph { ?class a owl:Class ; rdfs:label ?label }
} ORDER BY ?graph ?label`,

  corpus_all_formulas: `PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?graph ?label ?formula WHERE {
  GRAPH ?graph {
    ?x rdfs:label ?label .
    ?x ?prop ?formula .
    FILTER(CONTAINS(LCASE(STR(?prop)), 'structuralgrammarformula'))
  }
} ORDER BY ?graph ?label`,

  corpus_shared_formulas: `PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?formula (COUNT(DISTINCT ?graph) AS ?count) WHERE {
  GRAPH ?graph {
    ?x ?prop ?formula .
    FILTER(CONTAINS(LCASE(STR(?prop)), 'structuralgrammarformula'))
  }
} GROUP BY ?formula HAVING(?count > 1) ORDER BY DESC(?count)`,

  corpus_transdisciplinary: `PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label (COUNT(DISTINCT ?graph) AS ?files) WHERE {
  GRAPH ?graph { ?x a owl:Class ; rdfs:label ?label }
} GROUP BY ?label HAVING(?files >= 2) ORDER BY DESC(?files)`,

  corpus_structural_homology: `PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?formula ?label1 ?label2 WHERE {
  GRAPH ?g1 { ?x1 ?p1 ?formula ; rdfs:label ?label1 . FILTER(CONTAINS(LCASE(STR(?p1)),'formula')) }
  GRAPH ?g2 { ?x2 ?p2 ?formula ; rdfs:label ?label2 . FILTER(CONTAINS(LCASE(STR(?p2)),'formula')) }
  FILTER(?g1 < ?g2)
} ORDER BY ?formula`,
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

// ── Corpus UI logic ───────────────────────────────────────────
let _activeCorpus = null   // name of currently loaded corpus

const CORPUS_PRESETS = [
  { id: 'M1_all',  label: 'M1 — All extensions',
    patterns: ['M1_extensions/**/M1_*.jsonld'] },
  { id: 'M0_all',  label: 'M0 — All instances',
    patterns: ['instances/**/*.jsonld', 'system-models/**/*.jsonld'] },
  { id: 'M3_all',  label: 'M3 — All grammar files',
    patterns: ['M3_*.jsonld'] },
  { id: 'full',    label: 'Full corpus (M3+M2+M1+M0)',
    patterns: ['M3_*.jsonld', 'M2_GenericConcepts.jsonld',
               'M1_extensions/**/M1_*.jsonld',
               'instances/**/*.jsonld'] },
]

document.getElementById('btn-corpus-load')?.addEventListener('click', async (e) => {
  const btn    = e.currentTarget
  const dropId = 'corpus-dropdown'
  if (document.getElementById(dropId)) { document.getElementById(dropId)?.remove(); return }

  const { drop, addSection, addItem } = buildDropdown(dropId, btn)
  addSection('Load Corpus', true)

  const ontRoot = getOntologyRoot()
  if (!ontRoot) {
    const h = document.createElement('div')
    h.style.cssText = 'padding:8px 16px;color:var(--text-muted);font-size:11px'
    h.textContent = 'Ontology root not set'; drop.appendChild(h)
  } else {
    for (const preset of CORPUS_PRESETS) {
      const item = document.createElement('div')
      Object.assign(item.style, { padding: '7px 16px', cursor: 'pointer',
        color: _activeCorpus === preset.id ? 'var(--accent)' : 'var(--text-primary)',
        fontWeight: _activeCorpus === preset.id ? '700' : '400' })
      item.textContent = (_activeCorpus === preset.id ? '✓ ' : '') + preset.label
      item.onmouseenter = () => { item.style.background = 'var(--bg-hover)' }
      item.onmouseleave = () => { item.style.background = '' }
      item.addEventListener('click', async () => {
        drop.remove()
        await _loadCorpus(preset.id, preset.label, preset.patterns, ontRoot)
      })
      drop.appendChild(item)
    }
    if (_activeCorpus) {
      const sep = document.createElement('div')
      sep.style.cssText = 'height:1px;background:var(--border);margin:2px 0'
      drop.appendChild(sep)
      const unload = document.createElement('div')
      Object.assign(unload.style, { padding: '7px 16px', cursor: 'pointer',
        color: 'var(--danger, #e06c75)' })
      unload.textContent = '✕ Unload corpus'
      unload.onmouseenter = () => { unload.style.background = 'var(--bg-hover)' }
      unload.onmouseleave = () => { unload.style.background = '' }
      unload.addEventListener('click', async () => {
        drop.remove()
        await _unloadCorpus()
      })
      drop.appendChild(unload)
    }
  }
  attachDropdownClose(drop, btn)
})

async function _loadCorpus (name, label, patterns, ontRoot) {
  const status = document.getElementById('corpus-status')
  status.textContent = `Loading ${label}…`
  try {
    const res = await fetch(`${window._bridgeUrl}/corpus/load`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ corpus_name: name, ontology_root: ontRoot,
                             patterns, recursive: true })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Load failed')
    _activeCorpus = name
    const persist = data.persistent ? ' 💾' : ''
    status.textContent = `📚 ${label} — ${data.files_loaded} files, ${data.triples} triples${persist}`
    status.style.color = 'var(--accent)'
    document.getElementById('btn-corpus-clear').style.display = 'inline-block'
  } catch (e) {
    status.textContent = `Error: ${e.message}`
    status.style.color = 'var(--danger, #e06c75)'
  }
}

async function _unloadCorpus () {
  if (!_activeCorpus) return
  try {
    await fetch(`${window._bridgeUrl}/corpus/${_activeCorpus}`, { method: 'DELETE' })
  } catch (_) {}
  _activeCorpus = null
  const status = document.getElementById('corpus-status')
  status.textContent = 'No corpus loaded'
  status.style.color = 'var(--text-muted)'
  document.getElementById('btn-corpus-clear').style.display = 'none'
}

document.getElementById('btn-corpus-clear')?.addEventListener('click', _unloadCorpus)
async function _reloadCorpusFile (filePath) {
  const bridgeUrl = window._bridgeUrl || getBridgeUrl()
  if (!bridgeUrl || !filePath) return
  try {
    await fetch(`${bridgeUrl}/corpus/reload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_path: filePath })
    })
    console.log('[corpus] reloaded:', filePath)
  } catch (e) { console.warn('[corpus] reload failed:', e) }
}
// Auto-reload corpus when a file is saved/loaded in the editor
window.addEventListener('tscg:file-saved', (e) => {
  if (_activeCorpus && e.detail?.filePath) _reloadCorpusFile(e.detail.filePath)
})


document.getElementById('btn-sparql-run')?.addEventListener('click', async () => {
  const query   = document.getElementById('sparql-query')?.value?.trim()
  const results = document.getElementById('sparql-results')
  const status  = document.getElementById('sparql-status')
  const activeDoc = docManager.active

  if (!query) { if (status) status.textContent = 'Enter a query.'; return }

  const bridgeUrl = getBridgeUrl()
  if (!bridgeUrl) { if (status) status.textContent = 'Bridge not ready.'; return }

  // ── Route to corpus if active ─────────────────────────────────
  if (_activeCorpus) {
    if (status) status.textContent = `Running on corpus "${_activeCorpus}"…`
    if (results) results.innerHTML = ''
    try {
      const res = await fetch(`${bridgeUrl}/corpus/sparql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ corpus_name: _activeCorpus, query })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Query failed')
      renderSparqlResults(data, results)
      if (status) status.textContent =
        `${data.count ?? '?'} result(s) — corpus: ${_activeCorpus}`
    } catch (e) {
      if (status) status.textContent = `Error: ${e.message}`
    }
    return
  }

  // ── Single-file mode (unchanged) ─────────────────────────────
  if (!activeDoc?.filePath) { if (status) status.textContent = 'Load an ontology first.'; return }

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
