'use strict';

/**
 * main.js — Electron main process for TscgPocletMiner.
 *
 * Responsibilities:
 *   - Create the BrowserWindow
 *   - Expose IPC handlers for LLM calls, RAG, config management
 *   - Run Node.js-side code (fs, fetch, provider instantiation)
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs   = require('fs');

const { ProviderFactory  } = require('./src/llm/ProviderFactory');
const { RagBuilder       } = require('./src/rag/RagBuilder');
const { PocletPipeline   } = require('./src/tscg/PocletPipeline');

// ── App state ─────────────────────────────────────────────────────────────────

let mainWindow  = null;
let ragBuilder  = null;
let pipeline    = null;

// ── Config persistence ────────────────────────────────────────────────────────

function configPath() {
  return path.join(app.getPath('userData'), 'tscg_miner_config.json');
}

function loadConfig() {
  try {
    const raw = fs.readFileSync(configPath(), 'utf-8');
    return JSON.parse(raw);
  } catch {
    return ProviderFactory.defaultConfig();
  }
}

function saveConfig(config) {
  fs.mkdirSync(path.dirname(configPath()), { recursive: true });
  fs.writeFileSync(configPath(), JSON.stringify(config, null, 2), 'utf-8');
}

// ── Window ────────────────────────────────────────────────────────────────────

function createWindow() {
  mainWindow = new BrowserWindow({
    width:  1100,
    height: 750,
    minWidth:  800,
    minHeight: 600,
    title: 'TSCG Poclet Miner',
    webPreferences: {
      preload:           path.join(__dirname, 'preload.js'),
      contextIsolation:  true,
      nodeIntegration:   false,
      sandbox:           false,
    },
  });

  mainWindow.loadFile('renderer/index.html');

  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });

// ── IPC: Config ───────────────────────────────────────────────────────────────

ipcMain.handle('config:load', () => loadConfig());

ipcMain.handle('config:save', (_evt, config) => {
  saveConfig(config);
  return { ok: true };
});

ipcMain.handle('config:listProviders', () => ProviderFactory.listProviders());

ipcMain.handle('config:checkAll', async (_evt, config) => {
  return ProviderFactory.checkAll(config);
});

// ── IPC: TSCG repo path ───────────────────────────────────────────────────────

ipcMain.handle('repo:browse', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    title:       'Select TSCG repository root',
    properties:  ['openDirectory'],
  });
  return result.canceled ? null : result.filePaths[0];
});

// ── IPC: RAG ──────────────────────────────────────────────────────────────────

ipcMain.handle('rag:build', async (_evt, repoRoot) => {
  try {
    ragBuilder = new RagBuilder(repoRoot);
    const stats = await ragBuilder.build(msg => {
      mainWindow?.webContents.send('rag:progress', msg);
    });
    return { ok: true, ...stats };
  } catch (err) {
    return { ok: false, message: err.message };
  }
});

ipcMain.handle('rag:status', () => ({
  built:    ragBuilder?.isBuilt  ?? false,
  docCount: ragBuilder?.docCount ?? 0,
  stats:    ragBuilder?.stats    ?? {},
}));

// ── IPC: Pipeline ─────────────────────────────────────────────────────────────

ipcMain.handle('pipeline:reset', () => {
  pipeline = null;
  return { ok: true };
});

ipcMain.handle('pipeline:runRound', async (_evt, { round, userInput, configOverride }) => {
  try {
    // Load config (or use override from renderer)
    const config   = configOverride ?? loadConfig();
    const provider = ProviderFactory.create(config);

    // Create/reuse pipeline
    if (!pipeline || round === 1) {
      pipeline = new PocletPipeline(provider, ragBuilder);
    } else {
      // Swap provider if config changed
      pipeline._provider = provider;
    }

    const result = await pipeline.runRound(round, userInput);
    return {
      ok:        true,
      round,
      result,
      roundData: pipeline.roundData,
    };
  } catch (err) {
    return { ok: false, round, message: err.message };
  }
});

ipcMain.handle('pipeline:getData', () => ({
  roundData:    pipeline?.roundData    ?? {},
  currentRound: pipeline?.currentRound ?? 0,
  isComplete:   pipeline?.isComplete   ?? false,
}));

// ── IPC: File save ────────────────────────────────────────────────────────────

ipcMain.handle('file:saveJsonLd', async (_evt, { content, suggestedName }) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    title:       'Save M0 JSON-LD poclet',
    defaultPath: suggestedName ?? 'M0_Poclet.jsonld',
    filters:     [{ name: 'JSON-LD', extensions: ['jsonld'] }],
  });
  if (result.canceled) return { ok: false, canceled: true };
  try {
    fs.writeFileSync(result.filePath, content, 'utf-8');
    return { ok: true, filePath: result.filePath };
  } catch (err) {
    return { ok: false, message: err.message };
  }
});
