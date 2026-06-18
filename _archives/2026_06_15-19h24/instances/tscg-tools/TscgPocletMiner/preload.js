'use strict';

/**
 * preload.js — Electron contextBridge.
 *
 * Exposes a clean, typed API to the renderer process.
 * The renderer never accesses Node.js directly.
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('tscgMiner', {

  // ── Config ────────────────────────────────────────────────────────────────
  config: {
    load:          ()       => ipcRenderer.invoke('config:load'),
    save:          (cfg)    => ipcRenderer.invoke('config:save', cfg),
    listProviders: ()       => ipcRenderer.invoke('config:listProviders'),
    checkAll:      (cfg)    => ipcRenderer.invoke('config:checkAll', cfg),
  },

  // ── TSCG repo ─────────────────────────────────────────────────────────────
  repo: {
    browse: () => ipcRenderer.invoke('repo:browse'),
  },

  // ── RAG ───────────────────────────────────────────────────────────────────
  rag: {
    build:  (repoRoot) => ipcRenderer.invoke('rag:build', repoRoot),
    status: ()         => ipcRenderer.invoke('rag:status'),
    // Listen to build progress messages
    onProgress: (cb) => {
      ipcRenderer.on('rag:progress', (_evt, msg) => cb(msg));
    },
  },

  // ── Pipeline ──────────────────────────────────────────────────────────────
  pipeline: {
    reset:    ()                         => ipcRenderer.invoke('pipeline:reset'),
    runRound: (round, userInput, cfg)    => ipcRenderer.invoke('pipeline:runRound', { round, userInput, configOverride: cfg }),
    getData:  ()                         => ipcRenderer.invoke('pipeline:getData'),
  },

  // ── File ──────────────────────────────────────────────────────────────────
  file: {
    saveJsonLd: (content, suggestedName) => ipcRenderer.invoke('file:saveJsonLd', { content, suggestedName }),
  },
});
