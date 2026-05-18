// =============================================================
// TscgOntologyEditor — src/renderer/renderer.js   (ESM)
// Main renderer: plugin orchestration + splitters + ontology loading.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

import {
  createRendererApiFor,
  dispatchAction,
  getMenuItems,
  getTabs,
  notifyOntologyChanged
} from './RendererPluginApi.js'

import { initSplitters }                    from './Splitter.js'
import { setBridgeUrl, setRepoRoot,
         loadLayer, loadFile,
         onObjectSelected }                 from './OntologyLoader.js'

// =============================================================
// 1. SPLITTERS
// =============================================================
initSplitters()

// =============================================================
// 2. PYTHON BRIDGE — receive URL from server plugin
// =============================================================
window.tscgAPI.onFromServer('bridge-ready', ({ url }) => {
  console.log('[renderer] Python bridge ready:', url)
  setBridgeUrl(url)
  document.getElementById('status-msg').textContent =
    `Python bridge ready — ${url}`
})

// Expose bridge fetch helper for renderer plugins
window.bridgeFetch = async (endpoint, options = {}) => {
  const baseUrl = window.__bridgeUrl || null
  if (!baseUrl) throw new Error('Python bridge not ready')
  const res = await fetch(`${baseUrl}${endpoint}`, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

// =============================================================
// 3. OBJECT SELECTION → Property Inspector + right panel
// =============================================================
onObjectSelected(async (obj) => {
  populatePropertyInspector(obj)
  populateDescriptionTab(obj)
  notifyOntologyChanged({ layer: null, filePath: obj.filePath, label: obj.label })
})

function populatePropertyInspector (obj) {
  const drawers = document.getElementById('property-drawers')
  if (!drawers) return

  drawers.innerHTML = ''

  const fields = [
    { title: 'Identity', props: { '@id': obj.id, '@type': obj.type } },
    { title: 'Label',    props: { 'rdfs:label': obj.label } },
    { title: 'Properties', props: Object.fromEntries(
        (obj.keys || []).map(k => [k, '…'])
      )
    }
  ]

  for (const { title, props } of fields) {
    if (!Object.keys(props).length) continue
    const drawer = createDrawer(title, props)
    drawers.appendChild(drawer)
  }
}

function createDrawer (title, props) {
  const wrap = document.createElement('div')
  wrap.className = 'drawer'

  const header = document.createElement('div')
  header.className   = 'drawer-header'
  header.textContent = `▾ ${title}`
  wrap.appendChild(header)

  const body = document.createElement('div')
  body.className = 'drawer-body'
  wrap.appendChild(body)

  for (const [k, v] of Object.entries(props)) {
    const row = document.createElement('div')
    row.className = 'drawer-row'
    row.innerHTML = `
      <span class="drawer-key">${k}</span>
      <span class="drawer-val">${v ?? '—'}</span>`
    body.appendChild(row)
  }

  header.addEventListener('click', () => {
    const open = body.style.display !== 'none'
    body.style.display  = open ? 'none' : ''
    header.textContent  = `${open ? '▸' : '▾'} ${title}`
  })

  return wrap
}

function populateDescriptionTab (obj) {
  const pane = document.getElementById('tab-description')
  if (!pane) return
  pane.innerHTML = `
    <div class="desc-block">
      <div class="desc-label">Label</div>
      <div class="desc-value">${obj.label || '—'}</div>
    </div>
    <div class="desc-block">
      <div class="desc-label">Type</div>
      <div class="desc-value">${obj.type || '—'}</div>
    </div>
    <div class="desc-block">
      <div class="desc-label">IRI</div>
      <div class="desc-value desc-iri">${obj.id || '—'}</div>
    </div>`
}

// =============================================================
// 4. LAYER NAVIGATION
// =============================================================
let _repoRoot = null

// Main sends repo root so OntologyLoader can resolve layer paths
window.tscgAPI.onFromServer('repo-root', ({ root }) => {
  _repoRoot = root
  setRepoRoot(root)
  console.log('[renderer] Repo root:', root)
})

window.tscgAPI.onLoadLayer(async (layerName) => {
  setActiveOntologyLabel(`${layerName} loading…`)
  await loadLayer(layerName)
  setActiveOntologyLabel(layerName)
})

window.tscgAPI.onLoadFile(async (filePath) => {
  setActiveOntologyLabel(filePath.split(/[/\\]/).pop())
  await loadFile(filePath)
})

document.getElementById('btn-m3').addEventListener('click', async () => {
  setActiveOntologyLabel('M3 loading…')
  await loadLayer('M3')
  setActiveOntologyLabel('M3')
})
document.getElementById('btn-m2').addEventListener('click', async () => {
  setActiveOntologyLabel('M2 loading…')
  await loadLayer('M2')
  setActiveOntologyLabel('M2')
})
document.getElementById('btn-m1').addEventListener('click', async () => {
  setActiveOntologyLabel('M1 loading…')
  await loadLayer('M1')
  setActiveOntologyLabel('M1')
})

function setActiveOntologyLabel (text) {
  const el = document.getElementById('active-ontology-label')
  if (el) el.textContent = text
}

// =============================================================
// 5. RENDERER PLUGINS
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
// 6. PLUGIN TABS injection
// =============================================================
function injectPluginTabs () {
  const tabBar     = document.getElementById('tab-bar')
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
      const pane = document.getElementById(`tab-${btn.dataset.tab}`)
      if (pane) pane.classList.add('active')
    }
  })
}
rebindTabHandlers()

// =============================================================
// 7. POPUP + MODE TOGGLE + MISC
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

document.getElementById('btn-browse').addEventListener('click', () => {
  document.getElementById('btn-browse').classList.add('active')
  document.getElementById('btn-edit').classList.remove('active')
  document.body.dataset.mode = 'browse'
})
document.getElementById('btn-edit').addEventListener('click', () => {
  document.getElementById('btn-edit').classList.add('active')
  document.getElementById('btn-browse').classList.remove('active')
  document.body.dataset.mode = 'edit'
})
document.body.dataset.mode = 'browse'

window.tscgAPI.onOpenPluginManager(async () => {
  const list = await window.tscgAPI.listPlugins()
  alert(`Installed plugins:\n${list.map(p => `• ${p.name}`).join('\n') || '(none)'}`)
})

console.log('[renderer] Initialised — awaiting plugin list and bridge URL…')
