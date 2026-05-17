// =============================================================
// TscgOntologyEditor — src/renderer/ObjectExplorer.js  (ESM)
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
    if (iri !== OWL_THING && !hasParent.has(iri) && !explicitL1.includes(iri)) {
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
export function renderObjectExplorer ({ objects, pairs, onSelect }) {
  _onSelectCb = onSelect
  const treeEl = document.getElementById('object-tree')
  if (!treeEl) return

  const { byIri, nonClassByIri, children, level1, typeGroups } = buildHierarchy(objects, pairs)
  const groupMap   = buildGroupMap(level1, children, byIri)
  const typeNames  = Object.keys(typeGroups).sort()
  const classCount = byIri.size

  treeEl.innerHTML = ''
  _expanded.add(OWL_THING)
  for (const iri of level1) _expanded.add(iri)

  // ── Mode selector ─────────────────────────────────────────────
  const modeRow = document.createElement('div')
  modeRow.className = 'oe-mode-row'
  const modeSel = document.createElement('select')
  modeSel.className = 'oe-mode-select'
  const clsOpt = document.createElement('option')
  clsOpt.value = 'classes'; clsOpt.textContent = '⬡ Classes'
  modeSel.appendChild(clsOpt)
  for (const t of typeNames) {
    const opt = document.createElement('option')
    opt.value = t; opt.textContent = '⬡ ' + t
    modeSel.appendChild(opt)
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

  const redraw = () => {
    const mode = modeSel.value
    filterBar.style.display = (mode === 'classes') ? '' : 'none'
    _selectedGroups.clear()
    pillsEl.innerHTML = '<span class="oe-pills-empty">All groups visible</span>'
    clearBtn.disabled = true
    if (mode === 'classes') {
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1)
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
        _renderTree(treeBody, byIri, children, classCount, groupMap, level1)
      })
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1)
    }
  })
  clearBtn.addEventListener('click', () => {
    _selectedGroups.clear()
    _renderPills(pillsEl, clearBtn, () => {
      _renderTree(treeBody, byIri, children, classCount, groupMap, level1)
    })
    _renderTree(treeBody, byIri, children, classCount, groupMap, level1)
  })
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

function _renderTree (treeBody, byIri, children, classCount, groupMap, level1) {
  treeBody.innerHTML = ''
  let visibleCount   = 0

  const isVisible = (iri) => {
    if (iri === OWL_THING) return true
    if (_selectedGroups.size === 0) return true
    return _selectedGroups.has(groupMap.get(iri))
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
        _renderTree(treeBody, byIri, children, classCount, groupMap, level1)
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

  const badge = document.createElement('div')
  badge.className   = 'oe-count'
  badge.textContent = `${visibleCount} / ${classCount} classes`
  treeBody.appendChild(badge)
}


