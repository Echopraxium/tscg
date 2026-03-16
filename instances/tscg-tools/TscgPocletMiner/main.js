// main.js — TscgPocletMiner Electron Main Process
// Author: Echopraxium with the collaboration of Claude AI
// v1.1.0 — RAG JS-native via @xenova/transformers (Option C)

'use strict';

const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const fs   = require('fs');
const { ragEngine } = require('./rag_engine');
const { registerRestoreHandlers } = require('./restore_rag');

// ─── Window ───────────────────────────────────────────────────────────────────

let mainWin = null;

function createWindow() {
  mainWin = new BrowserWindow({
    width:  980,
    height: 760,
    minWidth:  860,
    minHeight: 640,
    title: 'TscgPocletMiner',
    backgroundColor: '#0c0c12',
    webPreferences: {
      preload:          path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration:  false
    }
  });
  mainWin.loadFile('index.html');
  // mainWin.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();
  registerRestoreHandlers(ipcMain);
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// ─── IPC: Load corpus ─────────────────────────────────────────────────────────

ipcMain.handle('load-corpus', () => {
  const corpusPath = path.join(__dirname, 'poclet_corpus_profile.json');
  try {
    return { ok: true, data: JSON.parse(fs.readFileSync(corpusPath, 'utf-8')) };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

// ─── IPC: Open URL ────────────────────────────────────────────────────────────

ipcMain.handle('open-url', (_e, url) => {
  shell.openExternal(url);
  return { ok: true };
});

// ─── IPC: Export candidate JSON ───────────────────────────────────────────────

ipcMain.handle('export-candidate', (_e, data) => {
  const filename = `tscg_candidate_${data.system_slug}_${Date.now()}.json`;
  const outPath  = path.join(app.getPath('downloads'), filename);
  try {
    fs.writeFileSync(outPath, JSON.stringify(data, null, 2), 'utf-8');
    return { ok: true, path: outPath };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

// ─── IPC: RAG init (called once by renderer after startup) ───────────────────

ipcMain.handle('rag-init', async () => {
  try {
    await ragEngine.init((progress) => {
      // Forward progress to renderer
      if (mainWin && !mainWin.isDestroyed()) {
        mainWin.webContents.send('rag-progress', progress);
      }
    });
    return { ok: true };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

// ─── IPC: RAG query — similar poclets ────────────────────────────────────────
//
//  mode: "similar_poclets"  → search validated M0 corpus
//  mode: "suggest_concepts" → search M2 GenericConcepts corpus
//
ipcMain.handle('rag-query', async (_e, { query, mode, topK }) => {
  try {
    let results;
    if (mode === 'suggest_concepts') {
      results = await ragEngine.suggestGenericConcepts(query, topK || 6);
    } else {
      results = await ragEngine.querySimilarPoclets(query, topK || 5);
    }
    return { ok: true, results };
  } catch (err) {
    return { ok: false, error: err.message, results: [] };
  }
});

// ─── IPC: Rebuild corpus from instances/poclets/ ──────────────────────────────

const { rebuildCorpus } = require('./rebuild_corpus');

ipcMain.handle('rebuild-corpus', async () => {
  try {
    const result = rebuildCorpus({ startDir: __dirname });
    // Signal rag_engine to re-embed if hash changed
    ragEngine.markCorpusDirty();
    return { ok: true, ...result };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});
