/**
 * restore_rag.js — TSCG RAG Database Extraction for Electron
 *
 * Handles two cases automatically:
 *   • Single volume : db_tscg_rag.tar.gz
 *   • Multi-volume  : db_tscg_rag_01.tar.gz, db_tscg_rag_02.tar.gz, …
 *
 * Zero npm dependencies — uses only Node.js built-ins:
 *   zlib  (gunzip)
 *   fs    (file I/O)
 *   path  (path helpers)
 *
 * ─────────────────────────────────────────────────────────────
 * Integration (main.js):
 *   const { registerRestoreHandlers } = require('./restore_rag');
 *   registerRestoreHandlers(ipcMain);
 *
 * Preload (preload.js):
 *   contextBridge.exposeInMainWorld('api', {
 *     pickArchive:    ()             => ipcRenderer.invoke('dialog:openFile'),
 *     pickOutDir:     ()             => ipcRenderer.invoke('dialog:openDir'),
 *     restoreRag:     (file, outDir) => ipcRenderer.invoke('rag:restore', file, outDir),
 *     onRagProgress:  (cb)           => ipcRenderer.on('rag:progress', (_, m) => cb(m)),
 *     offRagProgress: ()             => ipcRenderer.removeAllListeners('rag:progress'),
 *   });
 *
 * Renderer — pass any one volume or the single archive:
 *   await window.api.restoreRag('/path/to/db_tscg_rag_01.tar.gz', '/output/dir');
 *   await window.api.restoreRag('/path/to/db_tscg_rag.tar.gz',    '/output/dir');
 * ─────────────────────────────────────────────────────────────
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const zlib = require('zlib');

// ==============================================================================
// VOLUME DETECTION
// ==============================================================================

/**
 * Given any file path (single archive or one volume of a split set), return
 * the ordered list of files that make up the complete archive.
 *
 * Naming convention:
 *   Single : db_tscg_rag.tar.gz
 *   Split  : db_tscg_rag_01.tar.gz  db_tscg_rag_02.tar.gz  ...
 *
 * @param {string} filePath
 * @returns {{ volumes: string[], isMulti: boolean }}
 */
function detectVolumes(filePath) {
  const dir      = path.dirname(path.resolve(filePath));
  const basename = path.basename(filePath);

  // Multi-volume pattern: ends with _NN.tar.gz
  const multiMatch = basename.match(/^(.+)_(\d{2})\.tar\.gz$/);

  if (!multiMatch) {
    // Single archive — no number suffix
    return { volumes: [path.resolve(filePath)], isMulti: false };
  }

  const prefix   = multiMatch[1];  // e.g. "db_tscg_rag"
  const volumeRe = new RegExp(`^${escapeRegex(prefix)}_(\\d{2})\\.tar\\.gz$`);

  const volumes = fs.readdirSync(dir)
    .filter(f => volumeRe.test(f))
    .sort()                              // lexicographic = numeric for zero-padded NN
    .map(f => path.join(dir, f));

  return { volumes, isMulti: volumes.length > 1 };
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// ==============================================================================
// TAR PARSER  (pure Node.js / Buffer — zero npm)
// ==============================================================================

/**
 * Parse a raw TAR buffer and extract all regular files to outDir.
 *
 * TAR block = 512 bytes.
 * Header layout (POSIX ustar):
 *   [0–99]   filename  (NUL-terminated)
 *   [124–135] file size (octal ASCII)
 *   [156]    type flag  '0'=file  '5'=directory  '\0'=old-style file
 *   [265–499] name prefix (ustar extension — prepended with '/')
 *
 * Security: paths are sanitised — absolute paths and '..' are stripped.
 *
 * @param {Buffer}   tarBuf
 * @param {string}   outDir
 * @param {Function} [onProgress]
 * @returns {string[]} extracted file paths
 */
function extractTarBuffer(tarBuf, outDir, onProgress) {
  fs.mkdirSync(outDir, { recursive: true });

  const extracted = [];
  let offset = 0;

  while (offset + 512 <= tarBuf.length) {
    const header = tarBuf.slice(offset, offset + 512);

    // Two consecutive zero blocks = end-of-archive marker
    if (isZeroBlock(header)) break;

    const name     = readNulString(header, 0,   100);
    const prefix   = readNulString(header, 265, 155);
    const sizeStr  = readNulString(header, 124, 12);
    const typeFlag = String.fromCharCode(header[156]);
    const fileSize = parseInt(sizeStr.trim(), 8) || 0;

    offset += 512;  // advance past header

    const rawPath  = prefix ? `${prefix}/${name}` : name;
    const safePath = sanitizePath(rawPath);

    if (!safePath) {
      offset += Math.ceil(fileSize / 512) * 512;
      continue;
    }

    const destPath = path.join(outDir, safePath);

    if (typeFlag === '5' || rawPath.endsWith('/')) {
      // Directory entry
      fs.mkdirSync(destPath, { recursive: true });
    } else if (typeFlag === '0' || typeFlag === '\0') {
      // Regular file
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      fs.writeFileSync(destPath, tarBuf.slice(offset, offset + fileSize));
      extracted.push(destPath);
      onProgress?.(`  ${safePath}  (${formatBytes(fileSize)})`);
    }

    offset += Math.ceil(fileSize / 512) * 512;
  }

  return extracted;
}

function isZeroBlock(buf) {
  for (let i = 0; i < 512; i++) if (buf[i] !== 0) return false;
  return true;
}

function readNulString(buf, start, maxLen) {
  let end = start;
  while (end < start + maxLen && buf[end] !== 0) end++;
  return buf.slice(start, end).toString('utf8');
}

function sanitizePath(raw) {
  const parts = raw
    .replace(/\\/g, '/')
    .replace(/^\/+/, '')
    .split('/')
    .filter(seg => seg !== '' && seg !== '..');
  return parts.join('/');
}

function formatBytes(n) {
  if (n < 1024)      return `${n} B`;
  if (n < 1024*1024) return `${(n/1024).toFixed(1)} KB`;
  return `${(n/1024/1024).toFixed(2)} MB`;
}

// ==============================================================================
// PUBLIC API
// ==============================================================================

/**
 * Restore a TSCG RAG database from a single or multi-volume archive.
 *
 * Automatically detects volumes from the provided file path:
 *   db_tscg_rag.tar.gz         single archive  → direct extraction
 *   db_tscg_rag_01.tar.gz      finds all _NN siblings → concatenate → extract
 *
 * @param {string}   archiveFile  — path to the archive or any one volume
 * @param {string}   outDir       — destination directory
 * @param {Function} [onProgress] — optional callback(message: string)
 *
 * @returns {Promise<{ dbDir: string, volumeCount: number, filesExtracted: number }>}
 */
async function restoreRagDb(archiveFile, outDir, onProgress) {
  // 1 — detect volumes
  const { volumes, isMulti } = detectVolumes(archiveFile);

  if (isMulti) {
    onProgress?.(`Multi-volume archive: ${volumes.length} volumes`);
    volumes.forEach((v, i) =>
      onProgress?.(`  [${i + 1}/${volumes.length}] ${path.basename(v)}  ${formatBytes(fs.statSync(v).size)}`)
    );
  } else {
    onProgress?.(`Single archive: ${path.basename(volumes[0])}  ${formatBytes(fs.statSync(volumes[0]).size)}`);
  }

  // 2 — read + concatenate
  onProgress?.(isMulti ? 'Joining volumes…' : 'Reading archive…');
  const chunks = volumes.map(v => fs.readFileSync(v));
  const rawGz  = chunks.length === 1 ? chunks[0] : Buffer.concat(chunks);
  onProgress?.(`  Compressed total: ${formatBytes(rawGz.length)}`);

  // 3 — gunzip
  onProgress?.('Decompressing…');
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
  onProgress?.(`Extracting to ${outDir}…`);
  const extracted = extractTarBuffer(tarBuf, outDir, onProgress);

  // 5 — locate ChromaDB root (directory that contains chroma.sqlite3)
  const sqlitePath = extracted.find(f => path.basename(f) === 'chroma.sqlite3');
  const dbDir      = sqlitePath ? path.dirname(sqlitePath) : outDir;

  onProgress?.(`Done — ${extracted.length} file(s) extracted`);
  onProgress?.(`DB directory: ${dbDir}`);

  return { dbDir, volumeCount: volumes.length, filesExtracted: extracted.length };
}

// ==============================================================================
// ELECTRON IPC INTEGRATION
// ==============================================================================

/**
 * Register all IPC handlers on ipcMain.
 *
 *   'rag:restore'      invoke → { ok, dbDir, volumeCount, filesExtracted }
 *                              or { ok: false, error }
 *   'dialog:openFile'  invoke → string | null
 *   'dialog:openDir'   invoke → string | null
 *
 * Progress messages are forwarded to the renderer via 'rag:progress' events.
 *
 * @param {Electron.IpcMain} ipcMain
 */
function registerRestoreHandlers(ipcMain) {
  const { BrowserWindow, dialog } = require('electron');

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

  ipcMain.handle('dialog:openFile', async () => {
    const { filePaths } = await dialog.showOpenDialog({
      title:      'Select RAG archive',
      filters:    [{ name: 'RAG Archives', extensions: ['gz'] }],
      properties: ['openFile'],
    });
    return filePaths[0] ?? null;
  });

  ipcMain.handle('dialog:openDir', async () => {
    const { filePaths } = await dialog.showOpenDialog({
      title:      'Select output directory',
      properties: ['openDirectory', 'createDirectory'],
    });
    return filePaths[0] ?? null;
  });
}

// ==============================================================================
// EXPORTS
// ==============================================================================

module.exports = {
  restoreRagDb,             // programmatic use
  registerRestoreHandlers,  // Electron IPC wiring
  detectVolumes,            // inspect volumes without extracting
};
