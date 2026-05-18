/**
 * TSCG Poclet Explorer — Electron Main Process
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 2.0.0
 *
 * Location: instances/tscg-tools/tscg-poclet-explorer/main.js
 * Launch  : npm run tscg-poclet-explorer   (from tscg/ root)
 */

'use strict';

const { app, BrowserWindow, ipcMain, Menu, shell } = require('electron');
const path  = require('path');
const fs    = require('fs');
const { spawn } = require('child_process');

let win = null;

// tscg / instances / tscg-tools / tscg-poclet-explorer  -> 3 levels up
const REPO_ROOT   = path.resolve(__dirname, '..', '..', '..');
const POCLETS_DIR = path.join(REPO_ROOT, 'instances', 'poclets');

console.log('[explorer/main.js] REPO_ROOT   :', REPO_ROOT);
console.log('[explorer/main.js] POCLETS_DIR :', POCLETS_DIR);
console.log('[explorer/main.js] Poclets dir exists:', fs.existsSync(POCLETS_DIR));

// ── Window ────────────────────────────────────────────────────────
function createWindow() {
  win = new BrowserWindow({
    width: 1100, height: 680,
    minWidth: 700, minHeight: 460,
    backgroundColor: '#0d1117',
    title: 'TSCG — Poclet Explorer',
    webPreferences: { nodeIntegration: true, contextIsolation: false }
  });
  win.loadFile(path.join(__dirname, 'index.html'));
  if (process.argv.includes('--dev'))
    win.webContents.openDevTools({ mode: 'detach' });
  win.on('closed', () => { win = null; });
}

// ── Menu ──────────────────────────────────────────────────────────
function buildMenu() {
  Menu.setApplicationMenu(Menu.buildFromTemplate([
    { label: 'File', submenu: [{ role: 'quit' }] },
    { label: 'View', submenu: [
        { role: 'reload' }, { role: 'forceReload' },
        { role: 'toggleDevTools' }, { type: 'separator' },
        { role: 'togglefullscreen' }
    ]},
    { label: 'Help', submenu: [
        { label: 'TSCG Repository',
          click: () => shell.openExternal('https://github.com/Echopraxium/tscg') }
    ]}
  ]));
}

// ── IPC ───────────────────────────────────────────────────────────

// Return the list of poclets (sub-folders of instances/poclets)
// Each entry includes sim type detection:
//   hasElectron : sim/main.js exists
//   hasPython   : _00_Run_Simulation.bat or _00_Run.bat exists
//   batFile     : absolute path to the .bat launcher (if found)
//   readmePath  : absolute path to M0_*_README.md or README.md
ipcMain.handle('get-poclets', () => {
  if (!fs.existsSync(POCLETS_DIR)) return [];

  return fs.readdirSync(POCLETS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.endsWith('docs'))
    .map(d => {
      const pocletDir = path.join(POCLETS_DIR, d.name);
      const simDir    = path.join(pocletDir, 'sim');
      const simPath   = path.join('instances', 'poclets', d.name, 'sim');

      // ── README detection ──────────────────────────────────────
      // Priority 1: M0_*_README.md pattern (canonical TSCG naming)
      // Priority 2: README.md / readme.md fallbacks
      let readmeAbs = null;

      // Scan for M0_*_README.md in pocletDir and simDir
      for (const dir of [pocletDir, simDir]) {
        if (!fs.existsSync(dir)) continue;
        const found = fs.readdirSync(dir)
          .find(f => /^M0_.+_README\.md$/i.test(f));
        if (found) { readmeAbs = path.join(dir, found); break; }
      }

      // Fallback to generic README names
      if (!readmeAbs) {
        const fallbacks = ['README.md', 'readme.md', 'Readme.md', 'README.txt'];
        for (const dir of [pocletDir, simDir]) {
          if (!fs.existsSync(dir)) continue;
          for (const c of fallbacks) {
            const p = path.join(dir, c);
            if (fs.existsSync(p)) { readmeAbs = p; break; }
          }
          if (readmeAbs) break;
        }
      }

      // ── Sim type detection ────────────────────────────────────
      const hasElectron = fs.existsSync(path.join(simDir, 'main.js'));

      // Accept _00_Run_Simulation.bat or _00_Run.bat
      let batFile = null;
      for (const name of ['_00_Run_Simulation.bat', '_00_Run.bat']) {
        const p = path.join(pocletDir, name);
        if (fs.existsSync(p)) { batFile = p; break; }
      }
      const hasPython = batFile !== null;

      // Human-readable label: kebab-case → Title Case
      const label = d.name
        .split('-')
        .map(w => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' ');

      return {
        id:          d.name,
        label,
        simPath,
        readmePath:  readmeAbs,
        hasReadme:   readmeAbs !== null,
        hasElectron,
        hasPython,
        batFile,
        hasSim:      hasElectron || hasPython   // at least one sim available
      };
    });
});

// Return README content for a given absolute path
ipcMain.handle('get-readme', (_e, absPath) => {
  if (!absPath || !fs.existsSync(absPath)) return null;
  try { return fs.readFileSync(absPath, 'utf-8'); }
  catch (e) { return null; }
});

// Launch an Electron poclet simulation
ipcMain.on('launch-poclet', (_e, simPath) => {
  const full = path.join(REPO_ROOT, simPath);
  const bin  = path.join(
    REPO_ROOT, 'node_modules', '.bin',
    process.platform === 'win32' ? 'electron.cmd' : 'electron'
  );
  const child = spawn(`"${bin}"`, [`"${full}"`], {
    shell: true, detached: true, stdio: 'ignore', cwd: REPO_ROOT
  });
  child.unref();
  if (win) win.close();
});

// Launch a Python/Pygame simulation via .bat file
ipcMain.on('launch-python', (_e, batAbsPath) => {
  if (!batAbsPath || !fs.existsSync(batAbsPath)) {
    const { dialog } = require('electron');
    dialog.showErrorBox('Launcher not found', 'Expected:\n' + batAbsPath);
    return;
  }
  // Run the .bat from its own directory so relative paths inside it work
  const child = spawn(`"${batAbsPath}"`, [], {
    shell:    true,
    detached: true,
    stdio:    'ignore',
    cwd:      path.dirname(batAbsPath)
  });
  child.unref();
  if (win) win.close();
});

// Renderer ready signal
ipcMain.on('renderer-ready', () => {
  console.log('[explorer/main.js] renderer ready');
});

// ── Lifecycle ─────────────────────────────────────────────────────
app.whenReady().then(() => {
  buildMenu();
  createWindow();
  app.on('activate', () => { if (!BrowserWindow.getAllWindows().length) createWindow(); });
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
