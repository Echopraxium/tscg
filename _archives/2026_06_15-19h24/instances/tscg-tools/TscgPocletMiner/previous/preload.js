// preload.js — TscgPocletMiner Secure IPC Bridge
// Author: Echopraxium with the collaboration of Claude AI

'use strict';

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('tscgAPI', {
  loadCorpus:      ()           => ipcRenderer.invoke('load-corpus'),
  openURL:         (url)        => ipcRenderer.invoke('open-url', url),
  exportCandidate: (data)       => ipcRenderer.invoke('export-candidate', data),

  // RAG (JS-native, @xenova/transformers in main process)
  ragInit:         ()           => ipcRenderer.invoke('rag-init'),
  ragQuery:        (opts)       => ipcRenderer.invoke('rag-query', opts),
  onRagProgress:   (cb)         => ipcRenderer.on('rag-progress', (_e, p) => cb(p)),
  rebuildCorpus:   ()           => ipcRenderer.invoke('rebuild-corpus'),

  // restore_rag.js — ChromaDB RAG database decompression
  pickArchive:     ()              => ipcRenderer.invoke('dialog:openFile'),
  pickOutDir:      ()              => ipcRenderer.invoke('dialog:openDir'),
  restoreRag:      (file, outDir) => ipcRenderer.invoke('rag:restore', file, outDir),
  onRagDbProgress: (cb)           => ipcRenderer.on('rag:progress', (_, m) => cb(m)),
  offRagDbProgress:()             => ipcRenderer.removeAllListeners('rag:progress')
});
