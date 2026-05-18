// =============================================================
// TscgOntologyEditor — src/renderer/DocumentManager.js  (ESM)
// Multi-Document Interface: manages open ontology tabs.
// Each Document holds its own state (objects, selection, scroll).
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

// ── Document class ─────────────────────────────────────────────
export class Document {
  /**
   * @param {object} opts
   *   filePath  {string}   absolute path to the .jsonld file
   *   label     {string?}  display name (defaults to filename)
   *   layerName {string?}  'M3' | 'M2' | 'M1' | null
   */
  constructor ({ filePath, label, layerName = null }) {
    this.id               = `doc-${Date.now()}-${Math.random().toString(36).slice(2)}`
    this.filePath         = filePath
    this.label            = label || filePath.split(/[/\\]/).pop()
    this.layerName        = layerName
    this.isModified       = false

    // Object Explorer state
    this.objects          = []           // loaded from bridge /load
    this.selectedObjectId = null
    this.treeScrollTop    = 0

    // Property Inspector state
    this.selectedObject   = null         // full object data

    // Status
    this.isLoading        = false
    this.loadError        = null
    this.tripleCount      = 0
  }
}

// ── DocumentManager class ──────────────────────────────────────
class DocumentManager {
  constructor () {
    this._documents = []
    this._activeId  = null
    this._listeners = []
  }

  // ── Open ──────────────────────────────────────────────────
  // Opens a document. If already open, activates it instead.
  open ({ filePath, label, layerName }) {
    const existing = this._documents.find(d => d.filePath === filePath)
    if (existing) {
      this.setActive(existing.id)
      return existing
    }
    const doc = new Document({ filePath, label, layerName })
    this._documents.push(doc)
    this.setActive(doc.id)
    this._notify('open', doc)
    return doc
  }

  // ── Close ─────────────────────────────────────────────────
  close (id) {
    const idx = this._documents.findIndex(d => d.id === id)
    if (idx === -1) return
    const [removed] = this._documents.splice(idx, 1)

    // Activate adjacent tab
    if (this._activeId === id) {
      const next = this._documents[Math.min(idx, this._documents.length - 1)]
      this._activeId = next?.id || null
    }
    this._notify('close', removed)
  }

  // ── Activate ─────────────────────────────────────────────
  setActive (id) {
    if (this._activeId === id) return
    this._activeId = id
    this._notify('activate', this.active)
  }

  // ── Update active document's state ───────────────────────
  updateActive (patch) {
    const doc = this.active
    if (doc) {
      Object.assign(doc, patch)
      this._notify('update', doc)
    }
  }

  // ── Accessors ────────────────────────────────────────────
  get active ()    { return this._documents.find(d => d.id === this._activeId) || null }
  get documents () { return [...this._documents] }
  get count ()     { return this._documents.length }
  get hasAny ()    { return this._documents.length > 0 }

  // ── Events ───────────────────────────────────────────────
  // cb(eventType: 'open'|'close'|'activate'|'update', document)
  onChange (cb)           { this._listeners.push(cb) }
  _notify  (type, doc)   { this._listeners.forEach(cb => cb(type, doc)) }
}

// ── Singleton export ──────────────────────────────────────────
export const docManager = new DocumentManager()

// ── Tab bar renderer ──────────────────────────────────────────
// Renders the document tab bar in the DOM.
// Called by renderer.js whenever the document list changes.
export function renderTabBar () {
  const bar = document.getElementById('doc-tab-bar')
  if (!bar) return

  // Keep the '+' button, rebuild the rest
  const addBtn = document.getElementById('doc-tab-add')
  bar.innerHTML = ''

  for (const doc of docManager.documents) {
    const tab = document.createElement('div')
    tab.className  = `doc-tab${doc.id === docManager.active?.id ? ' active' : ''}`
    tab.dataset.id = doc.id
    tab.title      = doc.filePath

    const lbl = document.createElement('span')
    lbl.className   = 'doc-tab-label'
    const nameNoExt  = doc.label.replace(/\.jsonld$/i, '')
    const shortName  = nameNoExt.replace(/^M[0-9]+_/, '')  // strip M2_ prefix
    lbl.textContent  = (doc.layerName ? `${doc.layerName}:` : '') + shortName

    const closeBtn = document.createElement('button')
    closeBtn.className   = 'doc-tab-close'
    closeBtn.textContent = '×'
    closeBtn.title       = 'Close'
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation()
      docManager.close(doc.id)
    })

    tab.appendChild(lbl)
    tab.appendChild(closeBtn)
    tab.addEventListener('click', () => docManager.setActive(doc.id))

    bar.appendChild(tab)
  }

  // Re-append the '+' button
  if (addBtn) bar.appendChild(addBtn)
}
