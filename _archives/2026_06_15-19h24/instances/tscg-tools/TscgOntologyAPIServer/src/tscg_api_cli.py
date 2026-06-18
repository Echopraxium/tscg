#!/usr/bin/env python3
# =============================================================
# TscgOntologyAPIServer — tscg_api_cli.py
# Standalone CLI controller: start / stop / restart / status /
# reload / export.  Works independently of Electron.
#
# Usage:
#   python tscg_api_cli.py start [options]
#   python tscg_api_cli.py stop
#   python tscg_api_cli.py restart [options]
#   python tscg_api_cli.py status
#   python tscg_api_cli.py reload [--file path]
#   python tscg_api_cli.py export [--format ntriples] [--output file]
#
# Author: Echopraxium with the collaboration of Claude AI
# Version: 1.1.0
# =============================================================

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import requests

# ─────────────────────────────────────────────────────────────
# Paths & defaults
# ─────────────────────────────────────────────────────────────
_HERE       = Path(__file__).resolve().parent          # …/src/
_SERVER_PY  = _HERE / 'tscg_api_server.py'
_PID_FILE   = _HERE.parent / 'tscg_api_server.pid'    # …/TscgOntologyAPIServer/

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8000
POLL_TIMEOUT = 20      # seconds to wait for server ready / gone
POLL_STEP    = 0.4


# ─────────────────────────────────────────────────────────────
# PID file helpers
# ─────────────────────────────────────────────────────────────
def _write_pid(pid: int, host: str, port: int):
    _PID_FILE.write_text(json.dumps({'pid': pid, 'host': host, 'port': port}))

def _read_pid() -> dict | None:
    if not _PID_FILE.exists():
        return None
    try:
        return json.loads(_PID_FILE.read_text())
    except Exception:
        return None

def _clear_pid():
    if _PID_FILE.exists():
        _PID_FILE.unlink()

def _base_url(host: str, port: int) -> str:
    return f'http://{host}:{port}'


# ─────────────────────────────────────────────────────────────
# Health helpers
# ─────────────────────────────────────────────────────────────
def _is_running(host: str, port: int) -> bool:
    try:
        r = requests.get(f'{_base_url(host, port)}/health', timeout=2)
        return r.ok
    except Exception:
        return False

def _wait_ready(host: str, port: int) -> bool:
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        if _is_running(host, port):
            return True
        time.sleep(POLL_STEP)
    return False

def _wait_gone(host: str, port: int) -> bool:
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        if not _is_running(host, port):
            return True
        time.sleep(POLL_STEP)
    return False


# ─────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────
def cmd_start(args):
    info = _read_pid()
    if info and _is_running(info['host'], info['port']):
        print(f'⚠  Server already running on port {info["port"]}. '
              'Use "restart" to restart it.')
        return 0

    if not _SERVER_PY.exists():
        print(f'✗  Server script not found: {_SERVER_PY}')
        return 1

    python = args.python or sys.executable
    cmd    = [python, str(_SERVER_PY),
              '--host', args.host, '--port', str(args.port),
              '--log-level', args.log_level]
    if args.store_path:
        cmd += ['--store-path',   args.store_path]
    if args.ontology_dir:
        cmd += ['--ontology-dir', args.ontology_dir]

    print(f'▶  Starting TscgOntologyAPIServer on {args.host}:{args.port} …')
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL if not args.verbose else None,
        stderr=subprocess.DEVNULL if not args.verbose else None,
        # Detach from parent so the CLI can exit while server keeps running
        start_new_session=True,
    )
    _write_pid(proc.pid, args.host, args.port)

    if _wait_ready(args.host, args.port):
        print(f'✔  Server ready  →  http://{args.host}:{args.port}')
        print(f'   Swagger UI    →  http://{args.host}:{args.port}/docs')
        print(f'   PID           : {proc.pid}  ({_PID_FILE})')
        return 0
    else:
        print('✗  Server did not become ready within timeout.')
        _clear_pid()
        return 1


def cmd_stop(args):
    info = _read_pid()
    if not info:
        print('⚠  No PID file found — server may not be running.')
        return 0

    host, port, pid = info['host'], info['port'], info['pid']

    if not _is_running(host, port):
        print(f'⚠  Server on port {port} is not responding. Cleaning up PID file.')
        _clear_pid()
        return 0

    print(f'■  Stopping server (PID {pid}) …')
    try:
        if sys.platform == 'win32':
            subprocess.call(['taskkill', '/PID', str(pid), '/F'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except PermissionError:
        print(f'✗  Permission denied to kill PID {pid}.')
        return 1

    if _wait_gone(host, port):
        _clear_pid()
        print('✔  Server stopped.')
        return 0
    else:
        print('⚠  Server did not stop within timeout — may need manual kill.')
        return 1


def cmd_restart(args):
    print('↺  Restarting server …')
    rc = cmd_stop(args)
    if rc != 0:
        return rc
    time.sleep(0.5)
    return cmd_start(args)


def cmd_status(args):
    info = _read_pid()
    if not info:
        print('○  No PID file — server is not managed by this CLI.')
        return 0

    host, port, pid = info['host'], info['port'], info['pid']
    url = _base_url(host, port)

    if not _is_running(host, port):
        print(f'✗  Server not responding on {url}  (PID {pid} from PID file)')
        return 1

    try:
        h    = requests.get(f'{url}/health', timeout=5).json()
        meta = requests.get(f'{url}/info',   timeout=5).json()
    except Exception as e:
        print(f'✗  Could not fetch server info: {e}')
        return 1

    sep = '─' * 48
    print(sep)
    print('  TscgOntologyAPIServer — STATUS')
    print(sep)
    print(f'  URL       : {url}')
    print(f'  PID       : {pid}')
    print(f'  Uptime    : {h.get("uptime", "?")} s')
    print(f'  Graphs    : {h.get("graph_count", "?")}')
    print(f'  Triples   : {h.get("triple_count", "?")}')
    print(f'  Persistent: {h.get("persistent", False)}')
    print(f'  rdflib    : {meta.get("rdflib_version", "?")}')
    print(f'  pyoxigraph: {meta.get("pyoxigraph_version", "?")}')
    print(f'  Swagger   : {url}/docs')
    print(sep)
    return 0


def cmd_reload(args):
    info = _read_pid()
    if not info:
        print('✗  No PID file — cannot determine server address.')
        return 1

    host, port = info['host'], info['port']
    url = _base_url(host, port)

    if args.file:
        print(f'↺  Reloading file: {args.file}')
        try:
            r = requests.post(f'{url}/corpus/reload',
                              json={'file_path': args.file}, timeout=30)
            r.raise_for_status()
            d = r.json()
            print(f'✔  Reloaded: {d["file"]}  ({d["triples_loaded"]} triples)')
        except Exception as e:
            print(f'✗  Reload failed: {e}')
            return 1
    else:
        print('↺  Reloading all ontology files …')
        try:
            r = requests.post(f'{url}/corpus/reload-all', timeout=120)
            r.raise_for_status()
            d = r.json()
            print(f'✔  Reloaded: {d["reloaded"]} files  '
                  f'({d["total_triples"]} triples total)')
            if d.get('errors'):
                for err in d['errors']:
                    print(f'   ⚠ {err["file"]}: {err["error"]}')
        except Exception as e:
            print(f'✗  Reload-all failed: {e}')
            return 1
    return 0


def cmd_export(args):
    info = _read_pid()
    if not info:
        print('✗  No PID file — cannot determine server address.')
        return 1

    host, port = info['host'], info['port']
    url = _base_url(host, port)

    print(f'⬇  Exporting store as {args.format} …')
    try:
        r = requests.get(f'{url}/corpus/export',
                         params={'format': args.format}, timeout=120)
        r.raise_for_status()
        d       = r.json()
        content = d.get('content', '')
    except Exception as e:
        print(f'✗  Export failed: {e}')
        return 1

    if args.output:
        Path(args.output).write_text(content, encoding='utf-8')
        print(f'✔  Exported {d.get("triple_count", "?")} triples → {args.output}')
    else:
        print(content)
    return 0


# ─────────────────────────────────────────────────────────────
# Shared options builder
# ─────────────────────────────────────────────────────────────

def cmd_test(args):
    """Run the TscgOntologyAPIServer test suite via pytest."""
    import subprocess

    tests_dir = _HERE.parent / 'tests'
    if not tests_dir.exists():
        print(f'✗  Tests directory not found: {tests_dir}')
        return 1

    # Build pytest command
    cmd = [sys.executable, '-m', 'pytest']

    if args.module:
        module_map = {
            'iri':       'test_expand_iri.py',
            'store':     'test_tscg_store.py',
            'endpoints': 'test_endpoints.py',
        }
        if args.module not in module_map:
            print(f'✗  Unknown module: {args.module}. '
                  f'Choose from: {", ".join(module_map)}')
            return 1
        cmd.append(str(tests_dir / module_map[args.module]))
    else:
        cmd.append(str(tests_dir))

    if args.verbose:
        cmd.append('-v')
    if args.tb:
        cmd += ['--tb', args.tb]
    if args.keyword:
        cmd += ['-k', args.keyword]

    sep = '═' * 56
    print(sep)
    print('  TscgOntologyAPIServer — Test Suite')
    print(f'  Module : {args.module or "all"}')
    print(f'  Path   : {tests_dir}')
    print(sep)

    result = subprocess.run(cmd, check=False)

    print(sep)
    if result.returncode == 0:
        print('  ✔  ALL TESTS PASSED')
    else:
        print('  ✗  SOME TESTS FAILED (see above)')
    print(sep)
    return result.returncode


def _add_server_args(p: argparse.ArgumentParser):
    p.add_argument('--host',          default=DEFAULT_HOST)
    p.add_argument('--port',          type=int, default=DEFAULT_PORT)
    p.add_argument('--store-path',    default=None,
                   help='Persistent pyoxigraph store (.oxg)')
    p.add_argument('--ontology-dir',  default=None,
                   help='Ontology root to auto-load on startup')
    p.add_argument('--log-level',     default='warning',
                   choices=['critical', 'error', 'warning', 'info', 'debug'])
    p.add_argument('--python',        default=None,
                   help='Python executable (default: current interpreter)')
    p.add_argument('--verbose', '-v', action='store_true',
                   help='Show server stdout/stderr in this terminal')


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog='tscg_api_cli',
        description='CLI controller for TscgOntologyAPIServer',
    )
    sub = parser.add_subparsers(dest='command', required=True)

    # start
    p_start = sub.add_parser('start', help='Start the API server')
    _add_server_args(p_start)

    # stop
    sub.add_parser('stop', help='Stop the running API server')

    # restart
    p_restart = sub.add_parser('restart', help='Restart the API server')
    _add_server_args(p_restart)

    # status
    sub.add_parser('status', help='Show server status')

    # reload
    p_reload = sub.add_parser('reload', help='Hot-reload ontology files')
    p_reload.add_argument('--file', default=None,
                          help='Reload a single file (default: reload all)')

    # export
    p_export = sub.add_parser('export', help='Export the triple store')
    p_export.add_argument('--format', default='ntriples',
                          choices=['ntriples'], help='Export format')
    p_export.add_argument('--output', '-o', default=None,
                          help='Output file (default: stdout)')

    # test
    p_test = sub.add_parser('test', help='Run the test suite (pytest)')
    p_test.add_argument('--module', '-m', default=None,
                        choices=['iri', 'store', 'endpoints'],
                        help='Run a single module: iri | store | endpoints (default: all)')
    p_test.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose pytest output (-v)')
    p_test.add_argument('--tb', default='short',
                        choices=['short', 'long', 'no', 'line'],
                        help='Traceback style (default: short)')
    p_test.add_argument('--keyword', '-k', default=None,
                        help='Only run tests matching this keyword expression')

    args = parser.parse_args()

    dispatch = {
        'start':   cmd_start,
        'stop':    cmd_stop,
        'restart': cmd_restart,
        'status':  cmd_status,
        'reload':  cmd_reload,
        'export':  cmd_export,
        'test':    cmd_test,
    }
    sys.exit(dispatch[args.command](args))


if __name__ == '__main__':
    main()
