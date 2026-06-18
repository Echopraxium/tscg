// restore_rag.js — TSCG RAG Database Extraction for Electron
// Author: Echopraxium with the collaboration of Claude AI
// v1.0.0
//
// Zero npm dependencies — Node.js built-ins only: fs, path, zlib, crypto
//
// Naming conventions (auto-detected):
//   Single volume : db_tscg_rag.tar.gz
//   Multi-volume  : db_tscg_rag_01.tar.gz, db_tscg_rag_02.tar.gz, …
//
// Integration in main.js:
//   const { registerRestoreHandlers } = require('./restore_rag');
//   registerRestoreHandlers(ipcMain);
//
// Preload bridge (preload.js):
//   pickArchive:    ()             => ipcRenderer.invoke('dialog:openFile')
//   pickOutDir:     ()             => ipcRenderer.invoke('dialog:openDir')
//   restoreRag:     (file, outDir) => ipcRenderer.invoke('rag:restore', file, outDir)
//   detectVolumes:  (file)         => ipcRenderer.invoke('rag:detect-volumes', file)
//   onRagProgress:  cb             => ipcRenderer.on('rag:progress', (_, m) => cb(m))
//   offRagProgress: ()             => ipcRenderer.removeAllListeners('rag:progress')

'use strict';

const fs     = require('fs');
const path   = require('path');
const zlib   = require('zlib');
const crypto = require('crypto');

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatBytes(n) {
  if (n < 1024)        return `${n} B`;
  if (n < 1048576)     return `${(n / 1024).toFixed(1)} KB`;
  if (n < 1073741824)  return `${(n / 1048576).toFixed(1)} MB`;
  return `${(n / 1073741824).toFixed(2)} GB`;
}

function readOctal(buf, off, len) {
  return parseInt(buf.slice(off, off + len).toString('ascii').trim() || '0', 8);
}

// ─── Volume detection ─────────────────────────────────────────────────────────
//
//  Given any of these inputs, returns the full ordered list of volumes:
//    db_tscg_rag.tar.gz        → single, [ db_tscg_rag.tar.gz ]
//    db_tscg_rag_01.tar.gz     → multi,  [ _01.tar.gz, _02.tar.gz, … ]
//    db_tscg_rag_02.tar.gz     → multi,  [ _01.tar.gz, _02.tar.gz, … ]

function detectVolumes(archivePath) {
  const dir      = path.dirname(archivePath);
  const basename = path.basename(archivePath);

  // Multi-volume pattern: ends with _NN.tar.gz  (NN = two or more digits)
  const multiRe = /^(.+?)_(\d{2,})\.tar\.gz$/;
  const match   = basename.match(multiRe);

  if (!match) {
    // Single volume (or unrecognised — treat as single)
    return { isMulti: false, volumes: [archivePath] };
  }

  const stem = match[1]; // e.g. "db_tscg_rag"
  const volumes = [];

  for (let n = 1; n <= 99; n++) {
    const num  = String(n).padStart(2, '0');
    const file = path.join(dir, `${stem}_${num}.tar.gz`);
    if (fs.existsSync(file)) {
      volumes.push(file);
    } else if (n > 1) {
      break; // stop at first gap after the first found
    }
    // If n===1 and not found, try anyway (the user may have passed _02)
  }

  // If detection yielded nothing (caller passed _02 and _01 is missing),
  // fall back to the single provided file so we at least attempt extraction.
  if (volumes.length === 0) {
    return { isMulti: false, volumes: [archivePath] };
  }

  return { isMulti: volumes.length > 1, volumes };
}

// ─── Pure-JS TAR extractor ────────────────────────────────────────────────────
//
//  Reads a TAR buffer (already decompressed) and writes files to outDir.
//  Supports USTAR + GNU long-name headers (type 'L').
//  Returns array of extracted file paths.

function extractTarBuffer(tarBuf, outDir, onProgress) {
  fs.mkdirSync(outDir, { recursive: true });

  const extracted = [];
  let offset = 0;
  let pendingLongName = null; // GNU @LongLink

  while (offset + 512 <= tarBuf.length) {
    const header = tarBuf.slice(offset, offset + 512);
    offset += 512;

    // All-zero block = end-of-archive marker
    if (header.every(b => b === 0)) break;

    const rawName  = header.slice(0, 100).toString('utf8').replace(/\0/g, '');
    const typeFlag = String.fromCharCode(header[156]);
    const size     = readOctal(header, 124, 12);

    // Prefix field (USTAR)
    const prefix   = header.slice(345, 500).toString('utf8').replace(/\0/g, '');
    let name = pendingLongName ||
               (prefix ? `${prefix}/${rawName}` : rawName);
    pendingLongName = null;

    // GNU long-name extension: type 'L' stores the real name as content
    if (typeFlag === 'L') {
      const blocks = Math.ceil(size / 512);
      pendingLongName = tarBuf
        .slice(offset, offset + size)
        .toString('utf8')
        .replace(/\0/g, '');
      offset += blocks * 512;
      continue;
    }

    const blocks = Math.ceil(size / 512);

    if (typeFlag === '0' || typeFlag === '' || typeFlag === '\0') {
      // Regular file
      const safeName  = name.replace(/^\/+/, '').replace(/\.\.\//g, '');
      const dest      = path.join(outDir, safeName);
      const parentDir = path.dirname(dest);

      if (!fs.existsSync(parentDir)) fs.mkdirSync(parentDir, { recursive: true });

      const content = tarBuf.slice(offset, offset + size);
      fs.writeFileSync(dest, content);
      extracted.push(dest);
      onProgress?.(`  + ${safeName}  (${formatBytes(size)})`);

    } else if (typeFlag === '5') {
      // Directory
      const safeName = name.replace(/^\/+/, '').replace(/\.\.\//g, '');
      const dest     = path.join(outDir, safeName);
      fs.mkdirSync(dest, { recursive: true });
    }
    // Symlinks, hard links, etc. — silently skip

    offset += blocks * 512;
  }

  return extracted;
}

// ─── Main restore function ────────────────────────────────────────────────────

/**
 * restoreRagDb(archivePath, outDir, onProgress?)
 *
 * @param  {string}   archivePath  Path to any volume (.tar.gz or _01.tar.gz …)
 * @param  {string}   outDir       Destination directory (created if absent)
 * @param  {Function} [onProgress] Callback(message: string)
 * @returns {Promise<{ dbDir, volumeCount, filesExtracted }>}
 */
async function restoreRagDb(archivePath, outDir, onProgress) {
  // 1 — detect volumes
  const { isMulti, volumes } = detectVolumes(archivePath);

  if (isMulti) {
    onProgress?.(`Multi-volume archive detected — ${volumes.length} part(s):`);
    volumes.forEach((v, i) =>
      onProgress?.(`  [${i + 1}/${volumes.length}] ${path.basename(v)}  (${formatBytes(fs.statSync(v).size)})`)
    );
  } else {
    onProgress?.(`Single archive: ${path.basename(volumes[0])}  (${formatBytes(fs.statSync(volumes[0]).size)})`);
  }

  // 2 — read & concatenate
  onProgress?.(isMulti ? 'Joining volumes…' : 'Reading archive…');
  const chunks = volumes.map(v => fs.readFileSync(v));
  const rawGz  = chunks.length === 1 ? chunks[0] : Buffer.concat(chunks);
  onProgress?.(`  Compressed total: ${formatBytes(rawGz.length)}`);

  // 3 — gunzip
  onProgress?.('Decompressing (gunzip)…');
  let tarBuf;
  try {
    tarBuf = zlib.gunzipSync(rawGz);
  } catch (err) {
    throw new Error(
      `Decompression failed — volumes may be incomplete or corrupted: ${err.message}`
    );
  }
  onProgress?.(`  Decompressed: ${formatBytes(tarBuf.length)}`);

  // 4 — extract TAR
  onProgress?.(`Extracting to: ${outDir}`);
  const extracted = extractTarBuffer(tarBuf, outDir, onProgress);

  // 5 — locate ChromaDB root (directory containing chroma.sqlite3)
  const sqlitePath = extracted.find(f => path.basename(f) === 'chroma.sqlite3');
  const dbDir      = sqlitePath ? path.dirname(sqlitePath) : outDir;

  onProgress?.(`Done — ${extracted.length} file(s) extracted`);
  onProgress?.(`ChromaDB directory: ${dbDir}`);

  return { dbDir, volumeCount: volumes.length, filesExtracted: extracted.length };
}

// ─── Electron IPC integration ─────────────────────────────────────────────────

/**
 * Register IPC handlers on ipcMain.
 *
 *   'rag:restore'         invoke(archiveFile, outDir) → { ok, dbDir, volumeCount, filesExtracted }
 *   'rag:detect-volumes'  invoke(archiveFile)         → { ok, isMulti, volumes, totalSize }
 *   'dialog:openFile'     invoke()                    → string | null
 *   'dialog:openDir'      invoke()                    → string | null
 *
 * Progress forwarded to renderer via 'rag:progress' events.
 *
 * @param {Electron.IpcMain} ipcMain
 */
function registerRestoreHandlers(ipcMain) {
  const { BrowserWindow, dialog } = require('electron');

  // ── Restore ────────────────────────────────────────────────────────────────
  ipcMain.handle('rag:restore', async (event, archiveFile, outDir) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    const onProgress = msg => {
      if (win && !win.isDestroyed()) win.webContents.send('rag:progress', msg);
    };
    try {
      const result = await restoreRagDb(archiveFile, outDir, onProgress);
      return { ok: true, ...result };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  });

  // ── Detect volumes only (no extraction) ───────────────────────────────────
  ipcMain.handle('rag:detect-volumes', (_event, archiveFile) => {
    try {
      const { isMulti, volumes } = detectVolumes(archiveFile);
      const totalSize = volumes.reduce((s, v) => {
        try { return s + fs.statSync(v).size; } catch { return s; }
      }, 0);
      return { ok: true, isMulti, volumes, totalSize };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  });

  // ── File / directory pickers ───────────────────────────────────────────────
  ipcMain.handle('dialog:openFile', async () => {
    const { filePaths } = await dialog.showOpenDialog({
      title:      'Select RAG archive',
      filters:    [{ name: 'RAG Archives', extensions: ['gz'] }],
      properties: ['openFile']
    });
    return filePaths[0] ?? null;
  });

  ipcMain.handle('dialog:openDir', async () => {
    const { filePaths } = await dialog.showOpenDialog({
      title:      'Select output directory',
      properties: ['openDirectory', 'createDirectory']
    });
    return filePaths[0] ?? null;
  });
}

// ─── Exports ──────────────────────────────────────────────────────────────────

module.exports = {
  restoreRagDb,             // programmatic use
  registerRestoreHandlers,  // Electron IPC wiring
  detectVolumes             // inspect volumes without extracting
};
