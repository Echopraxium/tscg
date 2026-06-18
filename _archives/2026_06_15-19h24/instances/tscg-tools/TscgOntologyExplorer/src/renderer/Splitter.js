// =============================================================
// TscgOntologyExplorer — src/renderer/Splitter.js   (ESM)
// Drag-to-resize logic for the 3-column layout splitters.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

/**
 * Initialise both splitters.
 * Must be called after DOM is ready.
 */
export function initSplitters () {
  initSplitter({
    splitter:  document.getElementById('splitter-lc'),
    leftPanel: document.getElementById('object-explorer'),
    rightPanel: document.getElementById('property-inspector'),
    minLeft:   120,
    minRight:  200,
    side:      'left'    // dragging moves left panel width
  })

  initSplitter({
    splitter:  document.getElementById('splitter-cr'),
    leftPanel: document.getElementById('property-inspector'),
    rightPanel: document.getElementById('right-panel'),
    minLeft:   200,
    minRight:  200,
    side:      'right'   // dragging moves right panel width
  })
}

/**
 * Wire a single splitter element for drag-to-resize.
 *
 * @param {object} opts
 *   splitter  {HTMLElement}  the splitter div
 *   leftPanel {HTMLElement}  panel to the left of the splitter
 *   rightPanel{HTMLElement}  panel to the right of the splitter
 *   minLeft   {number}       minimum px width of left panel
 *   minRight  {number}       minimum px width of right panel
 *   side      {'left'|'right'}  which panel has a fixed px width
 */
function initSplitter ({ splitter, leftPanel, rightPanel, minLeft, minRight, side }) {
  if (!splitter || !leftPanel || !rightPanel) return

  let dragging  = false
  let startX    = 0
  let startWidth = 0

  splitter.addEventListener('mousedown', (e) => {
    e.preventDefault()
    dragging   = true
    startX     = e.clientX
    startWidth = side === 'left'
      ? leftPanel.offsetWidth
      : rightPanel.offsetWidth

    document.body.style.cursor         = 'col-resize'
    document.body.style.userSelect     = 'none'
    splitter.classList.add('dragging')
  })

  document.addEventListener('mousemove', (e) => {
    if (!dragging) return
    const dx        = e.clientX - startX
    const workspace = document.getElementById('workspace')
    const maxWidth  = workspace.offsetWidth - minLeft - minRight - 10 // 10 = splitter widths

    if (side === 'left') {
      const newWidth = Math.min(maxWidth, Math.max(minLeft, startWidth + dx))
      leftPanel.style.width = newWidth + 'px'
    } else {
      const newWidth = Math.min(maxWidth, Math.max(minRight, startWidth - dx))
      rightPanel.style.width = newWidth + 'px'
    }
  })

  document.addEventListener('mouseup', () => {
    if (!dragging) return
    dragging = false
    document.body.style.cursor     = ''
    document.body.style.userSelect = ''
    splitter.classList.remove('dragging')
  })

  // Prevent text selection during drag
  splitter.addEventListener('dragstart', e => e.preventDefault())
}
