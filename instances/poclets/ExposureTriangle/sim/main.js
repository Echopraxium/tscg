/**
 * TSCG Simulation Template — Electron Main Process
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 2.2.0
 *
 * Reusable main.js for all TSCG system-model simulations.
 * Customise per poclet: index.html + renderer.js + metadata.js only.
 */

'use strict';

const { app, BrowserWindow, ipcMain, Menu, shell } = require('electron');
const path  = require('path');
const fs    = require('fs');
const { spawn } = require('child_process');

let mainWindow = null;

// ── Path constants ────────────────────────────────────────────────
// tscg / instances / poclets / <poclet-name> / sim   ← __dirname
// 4 levels up = tscg/
const REPO_ROOT = path.resolve(__dirname, '..', '..', '..', '..');

// Explicit path to the Poclet Explorer app folder
const EXPLORER_DIR = path.join(
  REPO_ROOT, 'instances', 'tscg-tools', 'TscgPocletExplorer'
);

// Log at startup — visible in DevTools console (npm run sim:trophic --dev)
console.log('[main.js] __dirname    :', __dirname);
console.log('[main.js] REPO_ROOT    :', REPO_ROOT);
console.log('[main.js] EXPLORER_DIR :', EXPLORER_DIR);
console.log('[main.js] Explorer OK  :', fs.existsSync(EXPLORER_DIR));

// ── Launch Poclet Explorer, close this sim window ─────────────────
function goHome() {
  if (!fs.existsSync(EXPLORER_DIR)) {
    const { dialog } = require('electron');
    dialog.showErrorBox(
      'Poclet Explorer — folder not found',
      'Expected at:\n' + EXPLORER_DIR +
      '\n\nCreate the folder and run npm install first.'
    );
    return;
  }

  // Use the electron binary already installed at repo root
  const bin = path.join(
    REPO_ROOT, 'node_modules', '.bin',
    process.platform === 'win32' ? 'electron.cmd' : 'electron'
  );

  const child = spawn(`"${bin}"`, [`"${EXPLORER_DIR}"`], {
    cwd:      REPO_ROOT,
    shell:    true,
    detached: true,   // Explorer lives independently
    stdio:    'ignore'
  });
  child.unref();

  if (mainWindow) mainWindow.close();
}

// ── Main window ───────────────────────────────────────────────────
function createMainWindow() {
  // Show the sim folder path in the title bar for easy debugging
  // e.g. "TSCG — trophic-pyramid  [E:\...\sim]"
  const pocletName = path.basename(path.dirname(__dirname));
  const titleBar   = 'TSCG \u2014 ' + pocletName + '  [' + __dirname + ']';

  mainWindow = new BrowserWindow({
    width: 1280, height: 780,
    minWidth: 960, minHeight: 620,
    backgroundColor: '#0d1117',
    title: titleBar,
    webPreferences: { nodeIntegration: true, contextIsolation: false }
  });

  mainWindow.loadFile('index.html');

  if (process.argv.includes('--dev'))
    mainWindow.webContents.openDevTools({ mode: 'detach' });

  mainWindow.on('closed', () => { mainWindow = null; });
}

// ── Application menu ──────────────────────────────────────────────
function buildMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        { label: 'Poclet Explorer',
          accelerator: 'CmdOrCtrl+Shift+E',
          click: goHome },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    { label: 'Edit', submenu: [
        { role: 'undo' }, { role: 'redo' }, { type: 'separator' },
        { role: 'cut' }, { role: 'copy' }, { role: 'paste' }
    ]},
    { label: 'View', submenu: [
        { role: 'reload' }, { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
    ]},
    { label: 'Help', submenu: [
        { label: 'TSCG Repository',
          click: () => shell.openExternal('https://github.com/Echopraxium/tscg') }
    ]}
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// ── IPC ───────────────────────────────────────────────────────────
// Renderer can update the title dynamically
ipcMain.on('set-title', (_e, t) => { if (mainWindow) mainWindow.setTitle(t); });

// All three entry-points send 'go-home':
//   ⌂ Home button (header), File > Poclet Explorer, ⊞ footer button
ipcMain.on('go-home', () => goHome());

// ── Lifecycle ─────────────────────────────────────────────────────
app.whenReady().then(() => {
  buildMenu();
  createMainWindow();
  app.on('activate', () => {
    if (!BrowserWindow.getAllWindows().length) createMainWindow();
  });
});
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
