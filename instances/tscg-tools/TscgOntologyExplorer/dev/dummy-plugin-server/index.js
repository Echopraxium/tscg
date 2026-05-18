// =============================================================
// tscg-dummy-server — index.js   (CJS, main process)
// Dummy SERVER plugin for TscgOntologyEditor.
// Demonstrates: menu item registration + native dialog popup.
// =============================================================

'use strict'

/**
 * Plugin factory function — called by main.js with the ServerPluginApi.
 * Runs in the Electron main process: full Node.js access available.
 *
 * @param {object} api  ServerPluginApi scoped to this plugin
 */
module.exports = function DummyServerPlugin (api) {
  api.log('Server plugin activated')

  // ── Register a menu item under Tools > Plugins ──────────────
  api.registerMenuItem({
    label: 'Dummy Server Plugin',
    id:    'dummy-server-popup',
    group: 'Demo'
  })

  // ── Handle the menu item click ──────────────────────────────
  // Runs in the main process → uses native Electron dialog.
  api.onAction('dummy-server-popup', () => {
    api.log('Action triggered — showing native dialog')

    // Option 1: native OS dialog (main process)
    api.showPopup(
      'Dummy Server Plugin\n\nThis is a SERVER plugin running in the main process.\nFull Node.js access is available here.',
      'Server Plugin Demo'
    )

    // Option 2: HTML overlay in renderer (uncomment to use instead)
    // api.showRendererPopup('Dummy Server Plugin — running in main process')
  })
}
