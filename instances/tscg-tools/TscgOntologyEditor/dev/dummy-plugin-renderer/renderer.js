// =============================================================
// tscg-dummy-renderer — renderer.js   (ESM, renderer process)
// Dummy RENDERER plugin for TscgOntologyEditor.
// Loaded via: import('plugin://tscg-dummy-renderer/renderer.js')
// Demonstrates: menu item + HTML popup + custom tab + ontology listener.
// =============================================================

/**
 * Plugin entry point — called by renderer.js with the RendererPluginApi.
 * Runs in the Electron renderer process: full DOM access available.
 *
 * @param {object} api  RendererPluginApi scoped to this plugin
 */
export function init (api) {
  api.log('Renderer plugin activated')

  // ── 1. Register a menu item under Tools > Plugins ───────────
  api.registerMenuItem({
    label: 'Dummy Renderer Plugin',
    id:    'dummy-renderer-popup',
    group: 'Demo'
  })

  // ── 2. Handle the menu item click ───────────────────────────
  // Runs in the renderer → shows the HTML overlay popup.
  api.onAction('dummy-renderer-popup', () => {
    api.log('Action triggered — showing renderer popup')
    api.showPopup(
      'Dummy Renderer Plugin\n\nThis is a RENDERER plugin running in the renderer process.\nFull DOM access is available here.'
    )
  })

  // ── 3. React to ontology changes ────────────────────────────
  api.onOntologyChanged((info) => {
    api.log('Active ontology changed:', info?.label || '—')
  })

  api.log('Init complete — menu item and ontology listener registered')
}
