// =============================================================
// TscgOntologyEditor — src/commands/CommandRegistry.js  (ESM)
// Command Pattern: every user action is a Command registered here.
// Enables: Undo/Redo, Command Palette, plugin-defined commands,
//          keyboard shortcut mapping.
// Author: Echopraxium with the collaboration of Claude AI
// =============================================================

// ── Command class ─────────────────────────────────────────────
class Command {
  /**
   * @param {object} def
   *   id         {string}    unique identifier  e.g. 'file.openM2'
   *   label      {string}    human-readable     e.g. 'Open M2 GenericConcepts'
   *   keybinding {string?}   e.g. 'Ctrl+2'
   *   icon       {string?}   emoji or CSS class
   *   execute    {function}  (...args) → any
   *   undo       {function?} () → void  (omit if not undoable)
   *   canExecute {function?} () → bool  (for enabling/disabling menu items)
   */
  constructor (def) {
    this.id         = def.id
    this.label      = def.label
    this.keybinding = def.keybinding || null
    this.icon       = def.icon       || null
    this._execute   = def.execute
    this._undo      = def.undo       || null
    this.canExecute = def.canExecute || (() => true)
    this.isUndoable = !!def.undo
  }

  execute (...args) { return this._execute(...args) }
  undo ()           { if (this._undo) return this._undo() }
}

// ── CommandRegistry class ─────────────────────────────────────
class CommandRegistry {
  constructor () {
    this._commands  = new Map()   // id → Command
    this._history   = []          // executed undoable commands (for undo)
    this._redoStack = []          // undone commands (for redo)
    this._maxHistory = 100
    this._listeners = []          // onChange callbacks
  }

  // ── Register ───────────────────────────────────────────────
  // Called by app init and by plugins to add their commands.
  register (def) {
    const cmd = new Command(def)
    if (this._commands.has(cmd.id)) {
      console.warn(`[CommandRegistry] Overwriting command: ${cmd.id}`)
    }
    this._commands.set(cmd.id, cmd)
    this._notify()
    return cmd
  }

  // ── Execute ────────────────────────────────────────────────
  execute (id, ...args) {
    const cmd = this._commands.get(id)
    if (!cmd) {
      console.warn(`[CommandRegistry] Unknown command: ${id}`)
      return
    }
    if (!cmd.canExecute()) {
      console.log(`[CommandRegistry] Command not available: ${id}`)
      return
    }
    const result = cmd.execute(...args)
    if (cmd.isUndoable) {
      this._history.push(cmd)
      this._redoStack = []
      if (this._history.length > this._maxHistory) this._history.shift()
    }
    return result
  }

  // ── Undo / Redo ────────────────────────────────────────────
  undo () {
    const cmd = this._history.pop()
    if (!cmd) return false
    cmd.undo()
    this._redoStack.push(cmd)
    this._notify()
    return true
  }

  redo () {
    const cmd = this._redoStack.pop()
    if (!cmd) return false
    cmd.execute()
    this._history.push(cmd)
    this._notify()
    return true
  }

  canUndo () { return this._history.length > 0 }
  canRedo () { return this._redoStack.length > 0 }

  // ── Query ──────────────────────────────────────────────────
  get (id)  { return this._commands.get(id) || null }
  getAll () { return [...this._commands.values()] }

  // Find commands matching a search string (for Command Palette)
  search (query) {
    const q = query.toLowerCase()
    return this.getAll().filter(cmd =>
      cmd.label.toLowerCase().includes(q) ||
      cmd.id.toLowerCase().includes(q)
    )
  }

  // ── Change notification ────────────────────────────────────
  onChange (cb)  { this._listeners.push(cb) }
  _notify ()     { this._listeners.forEach(cb => cb()) }
}

// ── Singleton export ──────────────────────────────────────────
export const registry = new CommandRegistry()

// ── Built-in commands registration ───────────────────────────
// Registered here as stubs; execute functions are wired in renderer.js
// after the DOM and modules are ready.
// Plugins can register additional commands via registry.register().

registry.register({
  id:         'file.openM3',
  label:      'Open M3 GenesisSpace',
  keybinding: 'Ctrl+3',
  execute:    () => {}   // wired in renderer.js
})
registry.register({
  id:         'file.openM2',
  label:      'Open M2 GenericConcepts',
  keybinding: 'Ctrl+2',
  execute:    () => {}
})
registry.register({
  id:         'file.openM1',
  label:      'Open M1 CoreConcepts',
  keybinding: 'Ctrl+1',
  execute:    () => {}
})
registry.register({
  id:         'file.open',
  label:      'Open File…',
  keybinding: 'Ctrl+O',
  execute:    () => {}
})
registry.register({
  id:         'file.exportAs',
  label:      'Export As…',
  keybinding: 'Ctrl+Shift+E',
  execute:    () => {}   // stub — implemented later
})
registry.register({
  id:         'edit.undo',
  label:      'Undo',
  keybinding: 'Ctrl+Z',
  execute:    () => registry.undo(),
  canExecute: () => registry.canUndo()
})
registry.register({
  id:         'edit.redo',
  label:      'Redo',
  keybinding: 'Ctrl+Y',
  execute:    () => registry.redo(),
  canExecute: () => registry.canRedo()
})
registry.register({
  id:         'edit.preferences',
  label:      'Preferences…',
  keybinding: 'Ctrl+,',
  execute:    () => {}   // wired in renderer.js
})
registry.register({
  id:         'view.commandPalette',
  label:      'Command Palette…',
  keybinding: 'Ctrl+Shift+P',
  execute:    () => {}   // stub — implemented later
})
registry.register({
  id:         'help.about',
  label:      'About TscgOntologyEditor',
  execute:    () => {}
})
