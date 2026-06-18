// =============================================================
// TscgOntologyExplorer — src/preferences/preferences.js
// Builds the Preferences UI dynamically from preferences-schema.json.
// Adding a new preference = adding one JSON entry in the schema.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

'use strict'

let _schema        = null
let _config        = {}
let _originalTheme = 'night'

// ── Init ─────────────────────────────────────────────────────────
async function init () {
  const [schema, config] = await Promise.all([
    fetch('./preferences-schema.json').then(r => r.json()),
    window.tscgAPI.config.getAll()
  ])
  _schema        = schema
  _config        = config
  _originalTheme = config.theme || 'night'

  applyTheme(_originalTheme)
  buildNav()
  activateSection(_schema.sections[0].id)
  bindFooter()
}

// ── Theme ─────────────────────────────────────────────────────────
function applyTheme (name) {
  const link = document.getElementById('theme-stylesheet')
  if (link) link.href = `../renderer/themes/${name}.css`
}

// ── Nav ───────────────────────────────────────────────────────────
function buildNav () {
  const nav = document.getElementById('pref-nav')
  nav.innerHTML = ''
  for (const section of _schema.sections) {
    const item = document.createElement('div')
    item.className  = 'pref-nav-item'
    item.dataset.id = section.id
    item.innerHTML  = `<span class="pref-nav-icon">${section.icon || '⚙️'}</span> ${section.label}`
    item.addEventListener('click', () => activateSection(section.id))
    nav.appendChild(item)
  }
}

// ── Section ───────────────────────────────────────────────────────
function activateSection (sectionId) {
  document.querySelectorAll('.pref-nav-item').forEach(el =>
    el.classList.toggle('active', el.dataset.id === sectionId))

  const section = _schema.sections.find(s => s.id === sectionId)
  if (!section) return

  const content = document.getElementById('pref-content')
  content.innerHTML = ''

  const h2 = document.createElement('h2')
  h2.textContent = section.label
  content.appendChild(h2)

  for (const setting of section.settings) {
    const group = buildGroup(setting)
    if (group) content.appendChild(group)
  }
}

// ── Group ─────────────────────────────────────────────────────────
function buildGroup (setting) {
  const group = document.createElement('div')
  group.className       = 'pref-group'
  group.dataset.setting = setting.id

  const label = document.createElement('label')
  label.className   = 'pref-label'
  label.textContent = setting.label
  group.appendChild(label)

  if (setting.description) {
    const desc = document.createElement('div')
    desc.className = 'pref-description'
    desc.innerHTML = setting.description.replace(/`([^`]+)`/g, '<code>$1</code>')
    group.appendChild(desc)
  }

  const control = buildControl(setting)
  if (control) group.appendChild(control)
  return group
}

// ── Control builder ───────────────────────────────────────────────
function buildControl (setting) {
  const ctrlId = `pref-ctrl-${setting.id}`
  const value  = _config[setting.id] ?? setting.default ?? ''

  switch (setting.type) {

    case 'enum': {
      const values = setting.values || []
      const labels = setting.labels || values
      // Radio for ≤4 values, select otherwise
      if (values.length <= 4) {
        const grp = document.createElement('div')
        grp.className = 'pref-radio-group'
        values.forEach((val, i) => {
          const lbl = document.createElement('label')
          lbl.className = 'pref-radio'
          const inp = document.createElement('input')
          inp.type = 'radio'; inp.name = `pref-${setting.id}`
          inp.value = val; inp.checked = (val === value); inp.id = `${ctrlId}-${val}`
          const preview = document.createElement('span')
          preview.className   = `pref-radio-preview ${val}-preview`
          preview.textContent = labels[i]
          if (setting.livePreview && setting.id === 'theme') {
            inp.addEventListener('change', () => applyTheme(val))
          }
          lbl.appendChild(inp); lbl.appendChild(preview); grp.appendChild(lbl)
        })
        return grp
      } else {
        const sel = document.createElement('select')
        sel.className = 'pref-input'; sel.id = ctrlId
        values.forEach((val, i) => {
          const opt = document.createElement('option')
          opt.value = val; opt.textContent = labels[i] || val
          if (val === value) opt.selected = true
          sel.appendChild(opt)
        })
        return sel
      }
    }

    case 'string': {
      const inp = document.createElement('input')
      inp.type = 'text'; inp.className = 'pref-input'; inp.id = ctrlId
      inp.value = value; inp.placeholder = setting.placeholder || ''
      inp.readOnly = !!setting.readonly
      return inp
    }

    case 'file-or-url':
    case 'file':
    case 'directory': {
      const row = document.createElement('div')
      row.className = 'pref-input-row'
      const inp = document.createElement('input')
      inp.type = 'text'; inp.className = 'pref-input'; inp.id = ctrlId
      inp.value = value; inp.placeholder = setting.placeholder || ''
      inp.readOnly = !!setting.readonly
      row.appendChild(inp)
      if (setting.browse && !setting.readonly) {
        const btn = document.createElement('button')
        btn.className = 'pref-btn'; btn.textContent = 'Browse…'
        btn.addEventListener('click', async () => {
          const result = await window.tscgAPI.showOpenDialog?.({
            isDirectory: setting.type === 'directory',
            filters: setting.filters || [{ name: 'All files', extensions: ['*'] }]
          })
          if (result) inp.value = result
        })
        row.appendChild(btn)
      }
      return row
    }

    case 'number': {
      const inp = document.createElement('input')
      inp.type = 'number'; inp.className = 'pref-input pref-input-number'; inp.id = ctrlId
      inp.value = value
      if (setting.min !== undefined) inp.min = setting.min
      if (setting.max !== undefined) inp.max = setting.max
      return inp
    }

    case 'boolean': {
      const lbl = document.createElement('label')
      lbl.className = 'pref-checkbox-row'
      const inp = document.createElement('input')
      inp.type = 'checkbox'; inp.id = ctrlId; inp.checked = !!value
      const span = document.createElement('span'); span.textContent = setting.label
      lbl.appendChild(inp); lbl.appendChild(span)
      return lbl
    }

    case 'action': {
      const wrap = document.createElement('div')
      const statusEl = document.createElement('div')
      statusEl.className = 'pref-status'
      statusEl.id        = `pref-status-${setting.id}`
      statusEl.textContent = '—'
      wrap.appendChild(statusEl)
      if (setting.actionLabel) {
        const btn = document.createElement('button')
        btn.className = 'pref-btn pref-btn-action'; btn.textContent = setting.actionLabel
        btn.addEventListener('click', () => handleAction(setting.actionId, statusEl))
        wrap.appendChild(btn)
      }
      populateActionStatus(setting, statusEl)
      return wrap
    }

    case 'info-list': {
      const list = document.createElement('div')
      list.className = 'pref-list'; list.id = `pref-list-${setting.id}`
      list.innerHTML = '<p class="pref-empty">Loading…</p>'
      populateInfoList(setting, list)
      return list
    }

    default: return null
  }
}

// ── Async data ────────────────────────────────────────────────────
async function populateActionStatus (setting, el) {
  if (setting.actionId === 'restartBridge') {
    try {
      const cfg = await window.tscgAPI.config.getAll()
      el.textContent = cfg.bridgeUrl ? `Running on ${cfg.bridgeUrl}` : 'Not running'
    } catch { el.textContent = 'Unknown' }
  }
}

async function populateInfoList (setting, listEl) {
  if (setting.dataSource === 'listPlugins') {
    const plugins = await window.tscgAPI.listPlugins()
    if (!plugins.length) { listEl.innerHTML = '<p class="pref-empty">No plugins installed.</p>'; return }
    listEl.innerHTML = ''
    for (const p of plugins) {
      const item = document.createElement('div')
      item.className = 'pref-list-item'
      item.innerHTML = `<span>${p.name} <span style="opacity:.5">v${p.version || '—'}</span></span>
                        <span style="font-size:10px;opacity:.6">${p['tscg-plugin-type'] || 'server'}</span>`
      listEl.appendChild(item)
    }
  }
}

function handleAction (actionId, statusEl) {
  if (actionId === 'restartBridge') {
    window.tscgAPI.config.restartBridge()
    if (statusEl) statusEl.textContent = 'Restarting…'
  }
}

// ── Collect values ────────────────────────────────────────────────
function collectValues () {
  const result = {}
  for (const section of _schema.sections) {
    for (const setting of section.settings) {
      if (setting.type === 'action' || setting.type === 'info-list') continue
      const ctrlId = `pref-ctrl-${setting.id}`
      switch (setting.type) {
        case 'enum':
          if ((setting.values || []).length <= 4) {
            const checked = document.querySelector(`input[name="pref-${setting.id}"]:checked`)
            if (checked) result[setting.id] = checked.value
          } else {
            const sel = document.getElementById(ctrlId)
            if (sel) result[setting.id] = sel.value
          }
          break
        case 'boolean': {
          const cb = document.getElementById(ctrlId)
          if (cb) result[setting.id] = cb.checked
          break
        }
        case 'number': {
          const inp = document.getElementById(ctrlId)
          if (inp) result[setting.id] = Number(inp.value)
          break
        }
        default: {
          const inp = document.getElementById(ctrlId)
          if (inp) result[setting.id] = inp.value
        }
      }
    }
  }
  return result
}

// ── Footer ────────────────────────────────────────────────────────
async function applyChanges () {
  const values = collectValues()
  await window.tscgAPI.config.setMany(values)
  if (values.theme && values.theme !== _originalTheme) {
    window.tscgAPI.config.notifyThemeChanged(values.theme)
    _originalTheme = values.theme
  }
  _config = { ..._config, ...values }
}

function bindFooter () {
  document.getElementById('btn-pref-cancel')?.addEventListener('click', () => {
    applyTheme(_originalTheme)
    window.close()
  })
  document.getElementById('btn-pref-apply')?.addEventListener('click', async () => {
    await applyChanges()
  })
  document.getElementById('btn-pref-ok')?.addEventListener('click', async () => {
    await applyChanges()
    window.close()
  })
}

// ── Start ─────────────────────────────────────────────────────────
init().catch(console.error)
