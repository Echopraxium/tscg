/**
 * serve.js — TSCG minimal static HTTP server
 * Author: Echopraxium with the collaboration of Claude AI
 * Usage: node serve.js [port] [root]
 */
'use strict';
const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT = parseInt(process.argv[2]) || 8080;
const ROOT = path.resolve(process.argv[3] || process.cwd());

console.log('[TSCG] ROOT : ' + ROOT);
console.log('[TSCG] index: ' + path.join(ROOT, 'index.html') + ' — exists: ' + fs.existsSync(path.join(ROOT, 'index.html')));

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js':   'application/javascript',
  '.css':  'text/css',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
};

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  if (urlPath === '/' || urlPath === '') urlPath = '/index.html';

  const filePath = path.join(ROOT, urlPath);

  if (!filePath.startsWith(ROOT)) {
    res.writeHead(403); res.end('Forbidden'); return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      console.log('[TSCG] 404  ' + filePath);
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not found: ' + filePath);
      return;
    }
    const ext  = path.extname(filePath).toLowerCase();
    const mime = MIME[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
  });
});

server.on('error', err => {
  if (err.code === 'EADDRINUSE') {
    console.error('[TSCG] ERROR: Port ' + PORT + ' already in use.');
    console.error('[TSCG] Fix : close the other server window, or run:');
    console.error('[TSCG]       netstat -ano | findstr :' + PORT);
    console.error('[TSCG]       taskkill /PID <pid> /F');
  } else {
    console.error('[TSCG] ERROR:', err.message);
  }
  process.exit(1);
});

server.listen(PORT, '127.0.0.1', () => {
  console.log('[TSCG] Server: http://127.0.0.1:' + PORT + '/');
  console.log('[TSCG] Stop  : Ctrl+C');
});
