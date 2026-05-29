// =============================================================
// TscgOntologyExplorer — src/renderer/ObjectExplorer.js  (ESM)
//
// Hierarchical class tree built from rdfs:subClassOf pairs.
// Only owl:Class nodes are shown (not properties/annotations).
//
// owl:Thing arrives from the bridge as a real object (no virtual node).
//
// Level 0 : owl:Thing
// Level 1 : ConceptContract, GenericConcept, GenericConceptFamily…
// Level 2 : GenericConceptCombo, GenericConceptPair, leaf classes
// Level 3 : Tropism←Behavior, Context←Environment…
//
// Filter combobox = Level-1 groups (pills, TSCG gallery style)
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

const OWL_THING = 'http://www.w3.org/2002/07/owl#Thing'

let _onSelectCb     = null
let _onNavigateTo   = null   // (filePath, iri) → navigate cross-file
let _selectedGroups = new Set()
let _expanded       = new Set()

function shortLabel (uri) {
  if (!uri) return ''
  return uri.split('#').pop().split('/').pop()
}

function nodeLabel (iri) {
  if (iri === OWL_THING) return 'owl:Thing'
  return shortLabel(iri)
}

// ── Build hierarchy ────────────────────────────────────────────
function buildHierarchy (objects, pairs) {
  const OWL_CLASS_TYPES = new Set(['owl:Class', 'owl:Thing'])

  // ── Classes only → class tree ──────────────────────────────────
  const byIri = new Map()
  for (const obj of objects) {
    const t = Array.isArray(obj.type) ? obj.type[0] : (obj.type || '')
    if (t === 'owl:Class' || t.endsWith('Class') || t === 'owl:Thing') {
      byIri.set(obj.id, obj)
    }
  }

  // ── Non-class nodes → property/individual mode ─────────────────
  const nonClassByIri = new Map()
  for (const obj of objects) {
    const t = Array.isArray(obj.type) ? obj.type[0] : (obj.type || '')
    if (!OWL_CLASS_TYPES.has(t) && !t.endsWith('Class') && t !== 'owl:Ontology') {
      nonClassByIri.set(obj.id, obj)
    }
  }

  // ── rdfs:subClassOf hierarchy (classes only) ───────────────────
  const children = new Map()
  const hasParent = new Set()
  for (const { child, parent } of pairs) {
    if (!byIri.has(child)) continue   // skip non-class children
    if (!children.has(parent)) children.set(parent, [])
    children.get(parent).push(child)
    hasParent.add(child)
  }
  for (const [, kids] of children)
    kids.sort((a, b) => nodeLabel(a).localeCompare(nodeLabel(b)))

  // ── Level-1 = direct class children of owl:Thing ───────────────
  // Explicit (rdfs:subClassOf owl:Thing) + implicit (no parent)
  const explicitL1 = (children.get(OWL_THING) || []).filter(iri => byIri.has(iri))
  const implicitL1 = []
  for (const iri of byIri.keys()) {
    if (iri === OWL_THING || explicitL1.includes(iri)) continue
    // Include if: no parent at all, OR all parents are external (not in byIri)
    const hasLocalParent = hasParent.has(iri) &&
      [...children.entries()].some(([p, kids]) => kids.includes(iri) && byIri.has(p))
    if (!hasLocalParent) {
      implicitL1.push(iri)
      if (!children.has(OWL_THING)) children.set(OWL_THING, [])
      if (!children.get(OWL_THING).includes(iri)) children.get(OWL_THING).push(iri)
    }
  }
  const level1 = [...explicitL1, ...implicitL1]
    .sort((a, b) => nodeLabel(a).localeCompare(nodeLabel(b)))

  // ── Non-class type groups ──────────────────────────────────────
  const typeGroups = {}
  for (const [iri, obj] of nonClassByIri) {
    const t = shortLabel(Array.isArray(obj.type) ? obj.type[0] : (obj.type || 'Other'))
    if (!typeGroups[t]) typeGroups[t] = []
    typeGroups[t].push(iri)
  }

  return { byIri, nonClassByIri, children, hasParent, level1, typeGroups }
}



// ── Group map: for each class, which Level-1 ancestor owns it ──
function buildGroupMap (level1, children, byIri) {
  const map = new Map()

  const assign = (iri, groupLabel) => {
    map.set(iri, groupLabel)
    for (const child of (children.get(iri) || [])) {
      if (byIri.has(child)) assign(child, groupLabel)
    }
  }

  for (const iri of level1) assign(iri, nodeLabel(iri))
  return map
}

// ── Public API ─────────────────────────────────────────────────
export function renderObjectExplorer ({ objects, pairs, externalParents, onSelect, onNavigateTo }) {
  _onSelectCb     = onSelect
  _onNavigateTo   = onNavigateTo || null
  const treeEl = document.getElementById('object-tree')
  if (!treeEl) return

  // Build ghost-node map: parent IRI → { label, filePath }
  const ghostMap = new Map()
  for (const ep of (externalParents || [])) {
    if (ep.file_path_hint) ghostMap.set(ep.id, { label: ep.label, filePath: ep.file_path_hint })
  }

  const { byIri, nonClassByIri, children, level1, typeGroups } = buildHierarchy(objects, pairs)
  const groupMap   = buildGroupMap(level1, children, byIri)
  const typeNames  = Object.keys(typeGroups).sort()
  const classCount = byIri.size

  treeEl.innerHTML = ''
  _expanded.add(OWL_THING)
  for (const iri of level1) _expanded.add(iri)
  // Also expand ghost nodes by default
  for (const iri of ghostMap.keys()) _expanded.add(iri)

  // ── Mode selector ─────────────────────────────────────────────
  const modeRow = document.createElement('div')
  modeRow.className = 'oe-mode-row'
  const modeSel = document.createElement('select')
  modeSel.className = 'oe-mode-select'
  const clsOpt = document.createElement('option')
  clsOpt.value = 'classes'; clsOpt.textContent = '⬡ Classes'
  modeSel.appendChild(clsOpt)
  // Auto-select first mode with content if Classes is empty
  const hasClasses = level1.length > 0
  if (!hasClasses && typeNames.length > 0) {
    clsOpt.disabled = true
    modeSel.value = ''  // will be set after options added
  }
  for (const t of typeNames) {
    const opt = document.createElement('option')
    opt.value = t; opt.textContent = '⬡ ' + t
    modeSel.appendChild(opt)
  }
  // If Classes empty, auto-select first property/individual type
  if (!hasClasses && typeNames.length > 0) {
    modeSel.value = typeNames[0]
  }
  modeRow.appendChild(modeSel)
  treeEl.appendChild(modeRow)

  // ── Filter bar (Classes mode only) ────────────────────────────
  const filterBar = document.createElement('div')
  filterBar.className = 'oe-filter-bar'
  const selectRow = document.createElement('div')
  selectRow.className = 'oe-select-row'
  const groupSel = document.createElement('select')
  groupSel.className = 'oe-type-select'
  groupSel.innerHTML = '<option value="">Show group…</option>'
  for (const lbl of level1.map(iri => nodeLabel(iri))) {
    const opt = document.createElement('option')
    opt.value = lbl; opt.textContent = lbl; groupSel.appendChild(opt)
  }
  const clearBtn = document.createElement('button')
  clearBtn.className = 'oe-clear-btn'; clearBtn.textContent = '✕ All'; clearBtn.disabled = true
  selectRow.appendChild(groupSel); selectRow.appendChild(clearBtn)
  const pillsEl = document.createElement('div')
  pillsEl.className = 'oe-pills'
  filterBar.appendChild(selectRow); filterBar.appendChild(pillsEl)
  treeEl.appendChild(filterBar)

  // ── Tree body ─────────────────────────────────────────────────
  const treeBody = document.createElement('div')
  treeBody.className = 'oe-tree-body'
  treeEl.appendChild(treeBody)

  // Store context for selectObjectByIri re-render
  _currentRenderCtx = { treeBody, byIri, children, classCount, groupMap, level1, ghostMap }

  const redraw = () => {
    const mode = modeSel.value
    filterBar.style.display = (mode === 'classes') ? '' : 'none'
    _selectedGroups.clear()
    pillsEl.innerHTML = '<span class="oe-pills-empty">All groups visible</span>'
    clearBtn.disabled = true
    if (mode === 'classes') {
      _currentRenderCtx = { treeBody, byIri, children, classCount, groupMap, level1, ghostMap }
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
    } else {
      _renderFlatList(treeBody, typeGroups[mode] || [], nonClassByIri, mode)
    }
  }

  redraw()

  modeSel.addEventListener('change', () => redraw())

  groupSel.addEventListener('change', () => {
    const val = groupSel.value
    if (val && !_selectedGroups.has(val)) {
      _selectedGroups.add(val); groupSel.value = ''
      _renderPills(pillsEl, clearBtn, () => {
        _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
      })
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
    }
  })
  clearBtn.addEventListener('click', () => {
    _selectedGroups.clear()
    _renderPills(pillsEl, clearBtn, () => {
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
    })
    _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
  })
}

// ── Navigate to object by IRI ─────────────────────────────────
// Stored by renderObjectExplorer for re-render capability
let _currentRenderCtx = null   // { treeBody, byIri, children, classCount, groupMap, level1 }
// Called from Property Inspector when user clicks an internal URI
// Pending cross-document navigation: set before loadFile(), consumed on render
let _pendingSelectIri = null
export function setPendingSelectIri (iri) { _pendingSelectIri = iri }

export function selectObjectByIri (iri) {
  const treeBody = document.querySelector('.oe-tree-body')
  if (!treeBody) return false

  const safeIri = iri.replace(/"/g, '\\"')

  // Try to find node directly (might already be visible)
  let nodeEl = treeBody.querySelector(`[data-iri="${safeIri}"]`)

  if (!nodeEl && _currentRenderCtx) {
    // Node is collapsed — find all ancestors and expand them, then re-render
    const { byIri, children, classCount, groupMap, level1 } = _currentRenderCtx

    // Build parent map from children map
    const parentOf = new Map()
    for (const [parent, kids] of children)
      for (const kid of kids) parentOf.set(kid, parent)

    // Walk ancestors and add to _expanded
    let current = iri
    let safety  = 0
    while (current && safety++ < 20) {
      _expanded.add(current)
      current = parentOf.get(current)
    }

    // Re-render the tree with expanded ancestors
    _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
    nodeEl = treeBody.querySelector(`[data-iri="${safeIri}"]`)
  }

  if (!nodeEl) {
    console.warn('[OE] selectObjectByIri: node not found after expand, IRI:', iri.slice(-60))
    return false
  }

  treeBody.querySelectorAll('.oe-node.selected').forEach(n => n.classList.remove('selected'))
  nodeEl.classList.add('selected')
  nodeEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
  nodeEl.click()
  return true
}

// Called after Object Explorer renders — apply pending cross-doc navigation
export function applyPendingSelect () {
  if (!_pendingSelectIri) return
  const iri = _pendingSelectIri
  _pendingSelectIri = null
  setTimeout(() => selectObjectByIri(iri), 100)
}

// ── Search / filter ───────────────────────────────────────────
export function filterObjectTree (query) {
  const treeBody = document.querySelector('.oe-tree-body')
  if (!treeBody) return 0

  const raw = query.trim()  // keep original casing for regex

  // ── 1. Expand ALL nodes before filtering ──────────────────────
  // So collapsed subtrees (e.g. Process→Duplication) are in the DOM
  if (raw && _currentRenderCtx) {
    const { byIri, children, classCount, groupMap, level1 } = _currentRenderCtx
    for (const iri of byIri.keys()) _expanded.add(iri)
    _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
  }

  // ── 2. Build regex ────────────────────────────────────────────
  // Do NOT toLowerCase the query — the 'i' flag handles case
  let rx = null
  if (raw) {
    try {
      if (raw.startsWith('/') && raw.lastIndexOf('/') > 0) {
        const last = raw.lastIndexOf('/')
        rx = new RegExp(raw.slice(1, last), raw.slice(last + 1) || 'i')
      } else {
        rx = new RegExp(raw, 'i')
      }
    } catch {
      // Invalid regex → fall back to literal string
      rx = new RegExp(raw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i')
    }
  }

  // ── 3. Filter nodes ───────────────────────────────────────────
  const nodes = [...treeBody.querySelectorAll('.oe-node')]
  let matches = 0
  let firstMatch = null

  nodes.forEach(nodeEl => {
    const lblEl = nodeEl.querySelector('.oe-lbl')
    if (!lblEl) return

    const orig  = lblEl.textContent
    const local = (nodeEl.dataset.iri || '').split('#').pop()

    if (!rx) {
      // Empty query — clear all
      nodeEl.classList.remove('oe-node-dimmed')
      lblEl.textContent = orig
      return
    }

    const hit = rx.test(orig) || rx.test(local)

    if (hit) {
      matches++
      nodeEl.classList.remove('oe-node-dimmed')
      if (!firstMatch) firstMatch = nodeEl

      // Highlight match
      const m = rx.exec(orig)
      if (m) {
        lblEl.innerHTML =
          escHtml(orig.slice(0, m.index)) +
          `<span class="oe-match">${escHtml(m[0])}</span>` +
          escHtml(orig.slice(m.index + m[0].length))
      }

      // Un-dim ancestors
      let p = nodeEl.parentElement
      while (p && p !== treeBody) {
        if (p.classList.contains('oe-node')) p.classList.remove('oe-node-dimmed')
        p = p.parentElement
      }
    } else {
      nodeEl.classList.add('oe-node-dimmed')
      lblEl.textContent = orig
    }
  })

  // ── 4. Scroll + select first match ───────────────────────────
  if (firstMatch) {
    firstMatch.scrollIntoView({ behavior: 'smooth', block: 'start' })
    treeBody.querySelectorAll('.oe-node.selected').forEach(n => n.classList.remove('selected'))
    firstMatch.classList.add('selected')
    firstMatch.click()
  }

  return matches
}


function escHtml (s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
}

// ── Flat list for Properties / Individuals ─────────────────────
function _renderFlatList (treeBody, iris, byIri, typeName) {
  treeBody.innerHTML = ''
  const sorted = [...iris].sort((a,b) => nodeLabel(a).localeCompare(nodeLabel(b)))
  for (const iri of sorted) {
    const obj = byIri.get(iri); if (!obj) continue
    const item = document.createElement('div')
    item.className = 'oe-node'; item.style.paddingLeft = '12px'
    const tri = document.createElement('span')
    tri.className = 'oe-tri'; tri.textContent = '–'
    tri.style.opacity = '0.2'; tri.style.cursor = 'default'
    const lbl = document.createElement('span')
    lbl.className = 'oe-lbl'
    lbl.textContent = obj.label || shortLabel(obj.id); lbl.title = obj.id
    item.appendChild(tri); item.appendChild(lbl)
    item.addEventListener('click', () => {
      treeBody.querySelectorAll('.oe-node.selected').forEach(n => n.classList.remove('selected'))
      item.classList.add('selected')
      if (_onSelectCb) _onSelectCb(obj)
    })
    treeBody.appendChild(item)
  }
  const badge = document.createElement('div')
  badge.className = 'oe-count'
  badge.textContent = `${sorted.length} ${typeName}s`
  treeBody.appendChild(badge)
}


// ── Navigate to object by IRI ─────────────────────────────────
// Stored by renderObjectExplorer for re-render capability
// Called from Property Inspector when user clicks an internal URI

// ── Search / filter ───────────────────────────────────────────


// ── Flat list for Properties / Individuals ─────────────────────



// ── Pills ───────────────────────────────────────────────────────
const COLORS = ['#7c6af0','#4ecdc4','#f6b93b','#ee5a6f','#6c5ce7','#fd79a8','#00b894','#e17055']

function _renderPills (pillsEl, clearBtn, redraw) {
  pillsEl.innerHTML  = ''
  clearBtn.disabled  = _selectedGroups.size === 0

  if (_selectedGroups.size === 0) {
    const empty = document.createElement('span')
    empty.className   = 'oe-pills-empty'
    empty.textContent = 'All groups visible'
    pillsEl.appendChild(empty)
    return
  }

  let ci = 0
  for (const grp of _selectedGroups) {
    const pill = document.createElement('span')
    pill.className = 'oe-pill'
    pill.style.background = COLORS[ci++ % COLORS.length]
    pill.innerHTML = `${grp} <span class="oe-pill-x">✕</span>`
    pill.querySelector('.oe-pill-x').addEventListener('click', () => {
      _selectedGroups.delete(grp)
      redraw()
    })
    pillsEl.appendChild(pill)
  }
}

// ── Tree ────────────────────────────────────────────────────────
function _isVisible (iri, groupMap) {
  if (iri === OWL_THING) return true           // root always visible
  if (_selectedGroups.size === 0) return true  // no filter = all visible
  return _selectedGroups.has(groupMap.get(iri))
}

function _renderTree (treeBody, byIri, children, classCount, groupMap, level1, ghostMap) {
  ghostMap = ghostMap || new Map()
  treeBody.innerHTML = ''
  let visibleCount   = 0

  const isVisible = (iri) => {
    if (iri === OWL_THING) return true
    if (_selectedGroups.size === 0) return true
    return _selectedGroups.has(groupMap.get(iri))
  }

  // ── Ghost node renderer (external parent, cross-file link) ────
  const renderGhostNode = (parentIri, ghost, depth) => {
    const localKids = (children.get(parentIri) || []).filter(c => byIri.has(c))
    if (localKids.length === 0) return   // no local children — no point showing

    const expanded  = _expanded.has(parentIri)
    const nodeEl    = document.createElement('div')
    nodeEl.className = 'oe-node oe-ghost'
    nodeEl.style.paddingLeft = `${6 + depth * 18}px`
    nodeEl.dataset.iri = parentIri
    nodeEl.title = `External class — click to open ${ghost.filePath?.split(/[/\\]/).pop() || 'file'}`

    const tri = document.createElement('span')
    tri.className = 'oe-tri'
    tri.textContent = expanded ? '▼' : '▶'
    tri.addEventListener('click', e => {
      e.stopPropagation()
      if (_expanded.has(parentIri)) _expanded.delete(parentIri)
      else                           _expanded.add(parentIri)
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
    })

    const lbl = document.createElement('span')
    lbl.className   = 'oe-lbl oe-ghost-lbl'
    lbl.textContent = `↗ ${ghost.label}`

    const badge = document.createElement('span')
    badge.className   = 'oe-ghost-badge'
    badge.textContent = ghost.filePath ? ghost.filePath.split(/[/\\]/).pop() : '(external)'

    nodeEl.appendChild(tri); nodeEl.appendChild(lbl); nodeEl.appendChild(badge)

    // Click → navigate to external file and select the class
    nodeEl.addEventListener('click', () => {
      treeBody.querySelectorAll('.oe-node.selected').forEach(n => n.classList.remove('selected'))
      nodeEl.classList.add('selected')
      if (_onNavigateTo && ghost.filePath) {
        _onNavigateTo(ghost.filePath, parentIri)
      }
    })

    treeBody.appendChild(nodeEl)
    if (expanded) {
      for (const c of localKids.sort((a,b) => nodeLabel(a).localeCompare(nodeLabel(b))))
        renderNode(c, depth + 1)
    }
    visibleCount++
  }

  const renderNode = (iri, depth) => {
    const obj = byIri.get(iri)
    if (!obj) return
    const nodeKids  = (children.get(iri) || []).filter(c => byIri.has(c))
    const selfVis   = isVisible(iri)
    const anyKidVis = nodeKids.some(c => isVisible(c))
    if (!selfVis && !anyKidVis) return
    if (selfVis) visibleCount++

    const hasKids  = nodeKids.length > 0
    const expanded = _expanded.has(iri)
    const nodeEl   = document.createElement('div')
    nodeEl.className = 'oe-node'
    nodeEl.style.paddingLeft = `${6 + depth * 18}px`
    nodeEl.dataset.iri = iri

    const tri = document.createElement('span')
    tri.className = 'oe-tri'
    if (hasKids) {
      tri.textContent = expanded ? '▼' : '▶'
      tri.title = expanded ? 'Collapse' : 'Expand'
      tri.addEventListener('click', e => {
        e.stopPropagation()
        if (_expanded.has(iri)) _expanded.delete(iri)
        else                    _expanded.add(iri)
        _renderTree(treeBody, byIri, children, classCount, groupMap, level1, ghostMap)
      })
    } else {
      tri.textContent = '–'; tri.style.opacity = '0.2'; tri.style.cursor = 'default'
    }

    const lbl = document.createElement('span')
    lbl.className   = 'oe-lbl'
    lbl.textContent = obj.label || shortLabel(obj.id)
    lbl.title       = obj.id
    if (!selfVis) { lbl.style.opacity = '0.35'; lbl.style.fontStyle = 'italic' }

    nodeEl.appendChild(tri); nodeEl.appendChild(lbl)
    nodeEl.addEventListener('click', () => {
      treeBody.querySelectorAll('.oe-node.selected').forEach(n => n.classList.remove('selected'))
      nodeEl.classList.add('selected')
      if (_onSelectCb && selfVis && iri !== OWL_THING) _onSelectCb(byIri.get(iri))
    })
    treeBody.appendChild(nodeEl)
    if (hasKids && expanded) for (const c of nodeKids) renderNode(c, depth + 1)
  }

  renderNode(OWL_THING, 0)

  // ── Ghost nodes — external parents with local children ────────
  // Rendered after the local tree, grouped under a separator
  const ghostEntries = [...ghostMap.entries()]
    .filter(([iri]) => (children.get(iri) || []).some(c => byIri.has(c)))
    .sort(([,a],[,b]) => a.label.localeCompare(b.label))
  if (ghostEntries.length > 0) {
    const sep = document.createElement('div')
    sep.className   = 'oe-ghost-sep'
    sep.textContent = '↑ Superclasses (external files)'
    treeBody.appendChild(sep)
    for (const [iri, ghost] of ghostEntries) renderGhostNode(iri, ghost, 0)
  }

  const badge = document.createElement('div')
  badge.className   = 'oe-count'
  badge.textContent = `${visibleCount} / ${classCount} classes`
  treeBody.appendChild(badge)
}


