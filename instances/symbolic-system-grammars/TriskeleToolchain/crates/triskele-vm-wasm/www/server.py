#!/usr/bin/env python3
"""
server.py — TriskeleVM WASM dev server
Author: Echopraxium with the collaboration of Claude AI

Serves the www/ directory with COOP/COEP headers required for SharedArrayBuffer.
Use this instead of `python -m http.server`.

Usage (from crates/triskele-vm-wasm/www/):
    python server.py
    python server.py 9000   # custom port
"""

import http.server
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class CoopCoepHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy",   "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

    def log_message(self, fmt, *args):
        try:
            if int(args[1]) >= 400:
                super().log_message(fmt, *args)
        except (IndexError, ValueError):
            pass  # silently ignore non-numeric status args (e.g. 404 text messages)


if __name__ == "__main__":
    addr = ("", PORT)
    httpd = http.server.HTTPServer(addr, CoopCoepHandler)
    print(f"[TriskeleVM] COOP/COEP server on http://localhost:{PORT}")
    print(f"[TriskeleVM] SharedArrayBuffer: enabled")
    print(f"[TriskeleVM] Ctrl-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[TriskeleVM] server stopped")
