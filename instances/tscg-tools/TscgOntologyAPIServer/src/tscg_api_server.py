# =============================================================
# TscgOntologyAPIServer — tscg_api_server.py
# Standalone FastAPI/pyoxigraph REST server exposing the TSCG
# ontology corpus via SPARQL 1.1 and corpus management endpoints.
# Extracted and promoted from TscgOntologyExplorer bridge_server.py
# (Phase 2 bridge → Phase 3 standalone server).
#
# Author: Echopraxium with the collaboration of Claude AI
# Version: 1.1.0
# =============================================================

import sys
import json
import time
import argparse
import importlib.metadata
from pathlib import Path
from typing import Optional

import rdflib
import pyoxigraph as ox
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ─────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────
BASE_IRI       = 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/'
SERVER_VERSION = '1.1.0'
_start_time    = time.time()

# Global store — populated in _init_store() called from __main__
_tscg_store: Optional['TscgStore'] = None


# ─────────────────────────────────────────────────────────────
# IRI expansion  (3-strategy, identical to bridge_server.py)
# ─────────────────────────────────────────────────────────────
def _expand_iri(node_id: str, ctx: dict, base: str) -> str:
    """Expand a compact IRI using @context and @base.

    Strategy 1: longest exact prefix match in @context.
    Strategy 2: shared namespace inference for nested prefixes.
    Strategy 3: @base fallback.
    """
    if not node_id or node_id.startswith(('http://', 'https://')):
        return node_id
    if isinstance(ctx, dict) and ':' in node_id:
        for ctx_key in sorted(ctx.keys(), key=len, reverse=True):
            if node_id.startswith(ctx_key + ':'):
                local      = node_id[len(ctx_key) + 1:]
                prefix_uri = ctx[ctx_key]
                if not isinstance(prefix_uri, str) or not prefix_uri:
                    continue
                if prefix_uri.startswith(('http://', 'https://')):
                    return prefix_uri + local
                elif base:
                    return base.rstrip('/') + '/' + prefix_uri.lstrip('./') + local
        # Strategy 2 — shared namespace inference
        node_parts  = node_id.split(':')
        best_uri    = None
        best_shared = 0
        for ctx_key, prefix_uri in ctx.items():
            if not isinstance(prefix_uri, str) or not prefix_uri.startswith('http'):
                continue
            ctx_parts = ctx_key.split(':')
            shared    = 0
            for a, b in zip(node_parts[:-1], ctx_parts[:-1]):
                if a == b: shared += 1
                else:      break
            if shared > best_shared and shared == len(node_parts) - 1:
                best_shared = shared
                best_uri    = prefix_uri
        if best_uri:
            return best_uri.rstrip('#') + '#' + node_parts[-1]
    # Strategy 3 — @base fallback
    if base:
        return base.rstrip('/') + '/' + node_id.lstrip('./')
    return node_id


# ─────────────────────────────────────────────────────────────
# rdflib ↔ pyoxigraph term conversion
# ─────────────────────────────────────────────────────────────
def _rdflib_to_ox(term):
    """Convert an rdflib term to a pyoxigraph term; returns None on failure."""
    try:
        if isinstance(term, rdflib.URIRef):
            s = str(term)
            if not s.startswith(('http://', 'https://', 'urn:')):
                return None
            return ox.NamedNode(s)
        if isinstance(term, rdflib.BNode):
            return ox.BlankNode(str(term))
        if isinstance(term, rdflib.Literal):
            if term.datatype and str(term.datatype).startswith('http'):
                return ox.Literal(str(term), datatype=ox.NamedNode(str(term.datatype)))
            if term.language:
                return ox.Literal(str(term), language=term.language)
            return ox.Literal(str(term))
    except Exception:
        return None
    return None
    return None


def _ox_to_value(term) -> Optional[str]:
    """Convert a pyoxigraph term to a plain Python string.
    - NamedNode: returns bare IRI (no angle brackets)
    - Literal:   returns bare string value (no surrounding quotes)
    - BlankNode: returns _:id
    """
    if term is None:                    return None
    if isinstance(term, ox.NamedNode): return str(term)
    if isinstance(term, ox.BlankNode): return f'_:{term}'
    if isinstance(term, ox.Literal):
        # pyoxigraph str(Literal) includes quotes: '"value"' or '"value"@lang'
        # Use .value attribute for the bare string
        if hasattr(term, 'value'):      return term.value
        s = str(term)
        if s.startswith('"'):
            return s.split('"')[1] if s.count('"') >= 2 else s.strip('"')
        return s
    return str(term)


# ─────────────────────────────────────────────────────────────
# TscgStore
# ─────────────────────────────────────────────────────────────
class TscgStore:
    """Named-graph triple store for the TSCG corpus.

    Each JSON-LD file is loaded as one named graph whose IRI is
    derived from its canonical ontology URL.  Backed by pyoxigraph
    for high-performance SPARQL and optional disk persistence.
    """

    def __init__(self, db_path: str | None = None):
        self._db_path       = db_path
        try:
            self._store = ox.Store(db_path) if db_path else ox.Store()
        except RuntimeError as e:
            if db_path and ('RocksDB' in str(e) or 'lock' in str(e).lower()):
                print(f'', flush=True)
                print(f'[api] ⚠ Store locked: {db_path}', flush=True)
                print(f'[api]   Another instance may already be using this store.', flush=True)
                print(f'[api]   This could mean TscgOntologyExplorer is already running.', flush=True)
                print(f'', flush=True)
                import sys as _sys
                if not _sys.stdin.isatty():
                    # Non-interactive (spawned by Electron) — abort safely
                    print('[api]   Non-interactive mode: aborting.', flush=True)
                    raise SystemExit(1)
                print('[api]   Launch a second in-memory instance on port 8001? [y/N] ',
                      end='', flush=True)
                try:
                    answer = input('').strip().lower()
                except EOFError:
                    answer = 'n'
                if answer == 'y':
                    # Will be picked up in __main__ to restart on port 8001
                    self._db_path          = None
                    self._store            = ox.Store()
                    self._fallback_port    = 8001
                    print('[api]   In-memory store ready — will start on port 8001.',
                          flush=True)
                else:
                    print('[api]   Aborted. Close the other instance first.', flush=True)
                    raise SystemExit(1)
            else:
                raise
        self._loaded_files: dict[str, float] = {}   # absolute path → load timestamp

    # ── IRI derivation ─────────────────────────────────────────
    def _file_to_iri(self, file_path: str) -> str:
        """Derive a canonical named-graph IRI from a filesystem path."""
        p = Path(file_path).resolve()
        for anchor in ('ontology', 'instances'):
            if anchor in p.parts:
                idx = list(p.parts).index(anchor)
                rel = '/'.join(p.parts[idx:])
                return BASE_IRI + rel
        return BASE_IRI + p.name

    # ── File loading ───────────────────────────────────────────
    def load_file(self, file_path: str) -> dict:
        """Parse a JSON-LD file and insert it as a named graph."""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f'Not found: {file_path}')

        graph_iri_str = self._file_to_iri(file_path)
        graph_iri     = ox.NamedNode(graph_iri_str)

        if self._store.contains_named_graph(graph_iri):
            self._store.clear_graph(graph_iri)

        g = rdflib.Graph()
        g.parse(str(p), format='json-ld')

        loaded = skipped = 0
        for s, pred, o in g:
            os_, op_, oo_ = _rdflib_to_ox(s), _rdflib_to_ox(pred), _rdflib_to_ox(o)
            if os_ and op_ and oo_:
                try:
                    self._store.add(ox.Quad(os_, op_, oo_, graph_iri))
                    loaded += 1
                except Exception:
                    skipped += 1
            else:
                skipped += 1

        self._store.flush()
        self._loaded_files[str(p.resolve())] = time.time()
        return {
            'file':           p.name,
            'graph':          graph_iri_str,
            'triples_loaded': loaded,
            'skipped':        skipped,
        }

    def load_pattern(self, root: str, patterns: list[str],
                     recursive: bool = True) -> dict:
        """Load all JSON-LD files matching glob patterns under *root*."""
        root_p = Path(root)
        seen: dict[str, Path] = {}
        for pattern in patterns:
            fname = pattern.split('/')[-1]
            hits  = list(root_p.rglob(fname)) if recursive else list(root_p.glob(pattern))
            for f in hits:
                if f.suffix == '.jsonld':
                    seen[str(f.resolve())] = f

        results, errors = [], []
        for f in sorted(seen.values()):
            try:
                results.append(self.load_file(str(f)))
            except Exception as e:
                errors.append({'file': f.name, 'error': str(e)})

        self._store.flush()
        st = self.stats()
        return {
            'files_loaded':  len(results),
            'total_triples': st['total_triples'],
            'graphs':        st['named_graphs'],
            'files':         [r['file'] for r in results],
            'errors':        errors,
        }

    def reload_file(self, file_path: str) -> dict:
        """Hot-reload a single file (clears its named graph first)."""
        return self.load_file(file_path)

    def reload_all(self) -> dict:
        """Re-parse every previously loaded file from disk."""
        paths = list(self._loaded_files.keys())
        results, errors = [], []
        for fp in paths:
            try:
                results.append(self.load_file(fp))
            except Exception as e:
                errors.append({'file': Path(fp).name, 'error': str(e)})
        self._store.flush()
        return {
            'reloaded':      len(results),
            'errors':        errors,
            'total_triples': len(self._store),
        }

    def clear(self):
        """Remove all named graphs and reset the loaded-files index.
        Uses remove_graph() so pyoxigraph drops the graph from named_graphs()
        entirely, rather than leaving an empty shell (clear_graph behaviour).
        """
        for g in list(self._store.named_graphs()):
            self._store.remove_graph(g)
        self._loaded_files.clear()
        self._store.flush()

    # ── SPARQL ─────────────────────────────────────────────────
    def query(self, sparql_str: str):
        return self._store.query(sparql_str)

    # ── Introspection ──────────────────────────────────────────
    def stats(self) -> dict:
        return {
            'total_triples': len(self._store),
            'named_graphs':  len(list(self._store.named_graphs())),
            'db_path':       self._db_path,
            'persistent':    self._db_path is not None,
        }

    def graph_list(self) -> list[str]:
        return sorted(str(g) for g in self._store.named_graphs())

    def layer_map(self) -> dict:
        """Return {layer: count} grouping named graphs by M3/M2/M1/M0."""
        counts = {'M3': 0, 'M2': 0, 'M1': 0, 'M0': 0, 'other': 0}
        for g in self._store.named_graphs():
            name = Path(str(g)).name
            if   name.startswith('M3_'): counts['M3'] += 1
            elif name.startswith('M2_'): counts['M2'] += 1
            elif name.startswith('M1_'): counts['M1'] += 1
            elif name.startswith('M0_'): counts['M0'] += 1
            else:                        counts['other'] += 1
        return counts

    def export_ntriples(self) -> str:
        """Serialize the full store as N-Triples."""
        def _fmt(t):
            if isinstance(t, ox.NamedNode): return f'<{t}>'
            if isinstance(t, ox.BlankNode): return f'_:{t}'
            if isinstance(t, ox.Literal):
                if t.datatype: return f'"{t}"^^<{t.datatype}>'
                if t.language: return f'"{t}"@{t.language}'
                return f'"{t}"'
            return str(t)
        lines = [
            f'{_fmt(q.subject)} {_fmt(q.predicate)} {_fmt(q.object)} .'
            for q in self._store
        ]
        return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────
def _get_store() -> TscgStore:
    if _tscg_store is None:
        raise HTTPException(status_code=503, detail='TscgStore not initialised')
    return _tscg_store


# ─────────────────────────────────────────────────────────────
# FastAPI application
# ─────────────────────────────────────────────────────────────
app = FastAPI(
    title='TscgOntologyAPIServer',
    version=SERVER_VERSION,
    description=(
        'Standalone REST server exposing the TSCG ontology corpus '
        'via SPARQL 1.1 and corpus management endpoints. '
        'Uses pyoxigraph as a named-graph triple store with optional '
        'disk persistence. Self-documented via Swagger UI (/docs).'
    ),
    docs_url='/docs',
    redoc_url='/redoc',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


# ─────────────────────────────────────────────────────────────
# Request / response models
# ─────────────────────────────────────────────────────────────
class LoadRequest(BaseModel):
    file_path: str

class LoadPatternRequest(BaseModel):
    ontology_root: str
    patterns: list[str] = [
        'M3_*.jsonld', 'M2_*.jsonld', 'M1_*.jsonld',
        'instances/**/*.jsonld',
    ]
    recursive: bool = True

class ReloadFileRequest(BaseModel):
    file_path: str

class DeleteGraphRequest(BaseModel):
    graph_iri: str

class SparqlRequest(BaseModel):
    query:       str
    format:      str           = 'json'   # 'json' | 'ntriples'
    named_graph: Optional[str] = None

class IriExpandRequest(BaseModel):
    compact_iri: str
    context:     Optional[dict] = None


# ─────────────────────────────────────────────────────────────
# GET /health   GET /info
# ─────────────────────────────────────────────────────────────
@app.get('/health', tags=['Server'])
def health():
    """Liveness probe — polled by the tscg-api-bridge Electron plugin."""
    st = _get_store().stats()
    return {
        'status':       'ok',
        'uptime':       round(time.time() - _start_time, 1),
        'graph_count':  st['named_graphs'],
        'triple_count': st['total_triples'],
        'persistent':   st['persistent'],
    }

@app.get('/info', tags=['Server'])
def info():
    """Server metadata: version, store path, library versions."""
    st = _get_store().stats()
    def _ver(pkg):
        try:    return importlib.metadata.version(pkg)
        except: return 'unknown'
    return {
        'server':             'TscgOntologyAPIServer',
        'version':            SERVER_VERSION,
        'base_iri':           BASE_IRI,
        'store_path':         st['db_path'],
        'rdflib_version':     _ver('rdflib'),
        'pyoxigraph_version': _ver('pyoxigraph'),
        'loaded_graphs':      st['named_graphs'],
        'total_triples':      st['total_triples'],
    }


# ─────────────────────────────────────────────────────────────
# /corpus/*  — corpus management
# ─────────────────────────────────────────────────────────────
@app.post('/corpus/load', tags=['Corpus'])
def corpus_load(req: LoadRequest):
    """Load a single JSON-LD file into a named graph."""
    try:
        result = _get_store().load_file(req.file_path)
        print(f'[api] Loaded: {result["file"]} ({result["triples_loaded"]} triples)',
              flush=True)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/corpus/load-pattern', tags=['Corpus'])
def corpus_load_pattern(req: LoadPatternRequest):
    """Load all JSON-LD files matching glob patterns under a root directory."""
    root = Path(req.ontology_root)
    if not root.exists():
        raise HTTPException(status_code=404,
                            detail=f'Root not found: {req.ontology_root}')
    result = _get_store().load_pattern(str(root), req.patterns, req.recursive)
    st     = _get_store().stats()
    print(f'[api] Corpus: {result["files_loaded"]} files, '
          f'{st["total_triples"]} triples, {st["named_graphs"]} graphs', flush=True)
    return {**result, 'persistent': st['persistent'], 'db_path': st['db_path']}

@app.get('/corpus/list', tags=['Corpus'])
def corpus_list():
    """List all named graphs currently in the TscgStore."""
    store  = _get_store()
    graphs = store.graph_list()
    st     = store.stats()
    return {
        'total_triples': st['total_triples'],
        'graph_count':   len(graphs),
        'graphs': [{'iri': g, 'name': Path(g).name} for g in graphs],
    }

@app.get('/corpus/layers', tags=['Corpus'])
def corpus_layers():
    """Return graph counts grouped by M3 / M2 / M1 / M0 layer."""
    return _get_store().layer_map()

@app.post('/corpus/reload', tags=['Corpus'])
def corpus_reload(req: ReloadFileRequest):
    """Hot-reload a single JSON-LD file (clears its named graph first)."""
    try:
        result = _get_store().reload_file(req.file_path)
        print(f'[api] Reloaded: {result["file"]}', flush=True)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/corpus/reload-all', tags=['Corpus'])
def corpus_reload_all():
    """Re-parse all previously loaded JSON-LD files from disk (hot-reload)."""
    result = _get_store().reload_all()
    print(f'[api] Reload-all: {result["reloaded"]} files', flush=True)
    return result

@app.delete('/corpus/graph', tags=['Corpus'])
def corpus_delete_graph(req: DeleteGraphRequest):
    """Remove a specific named graph from the TscgStore."""
    store = _get_store()
    g     = ox.NamedNode(req.graph_iri)
    if not store._store.contains_named_graph(g):
        raise HTTPException(status_code=404,
                            detail=f'Graph not found: {req.graph_iri}')
    store._store.remove_graph(g)
    store._store.flush()
    return {'deleted': req.graph_iri}

@app.delete('/corpus/clear', tags=['Corpus'])
def corpus_clear():
    """Clear the entire TscgStore (removes all named graphs)."""
    _get_store().clear()
    return {'cleared': True}

@app.get('/corpus/export', tags=['Corpus'])
def corpus_export(format: str = 'ntriples'):
    """Export the full store as N-Triples."""
    content = _get_store().export_ntriples()
    lines   = content.count('\n') + 1 if content else 0
    return {'format': 'ntriples', 'triple_count': lines, 'content': content}


# ─────────────────────────────────────────────────────────────
# POST /corpus/sparql  — SPARQL 1.1
# ─────────────────────────────────────────────────────────────
@app.post('/corpus/sparql', tags=['SPARQL'])
def corpus_sparql(req: SparqlRequest):
    """
    Execute SPARQL SELECT / ASK / CONSTRUCT on the full TscgStore corpus.
    Supports GRAPH ?g { ... } patterns for cross-graph queries.
    """
    store = _get_store()
    try:
        results = store.query(req.query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'SPARQL error: {e}')

    # ASK — pyoxigraph returns QueryBoolean, not a Python bool
    if isinstance(results, bool) or type(results).__name__ == 'QueryBoolean':
        return {'query_type': 'ASK', 'result': bool(results)}

    # SELECT
    if hasattr(results, 'variables'):
        vars_ = [str(v) for v in results.variables]
        rows  = [
            {str(v): _ox_to_value(row[i]) for i, v in enumerate(results.variables)}
            for row in results
        ]
        return {'query_type': 'SELECT', 'vars': vars_,
                'results': rows, 'count': len(rows)}

    # CONSTRUCT
    triples = [
        {'s': _ox_to_value(s), 'p': _ox_to_value(p), 'o': _ox_to_value(o)}
        for s, p, o, *_ in results
    ]
    return {'query_type': 'CONSTRUCT', 'vars': ['s', 'p', 'o'],
            'results': triples, 'count': len(triples)}


# ─────────────────────────────────────────────────────────────
# /iri/expand  — compact IRI resolution
# ─────────────────────────────────────────────────────────────
@app.get('/iri/expand', tags=['IRI'])
def iri_expand_get(iri: str, context_file: Optional[str] = None):
    """Expand a compact TSCG IRI. Optionally load @context from a JSON-LD file."""
    ctx = {}
    if context_file:
        try:
            with open(context_file, encoding='utf-8') as f:
                raw = json.load(f)
            ctx = raw.get('@context', {})
        except Exception:
            pass
    return {'compact': iri, 'expanded': _expand_iri(iri, ctx, BASE_IRI)}

@app.post('/iri/expand', tags=['IRI'])
def iri_expand_post(req: IriExpandRequest):
    """Expand a compact TSCG IRI using a supplied @context dict."""
    expanded = _expand_iri(req.compact_iri, req.context or {}, BASE_IRI)
    return {'compact': req.compact_iri, 'expanded': expanded}



# =============================================================
# COMPATIBILITY LAYER — TscgOntologyExplorer renderer API
# Provides the same endpoints as bridge_server.py Phase 2 so
# that OntologyLoader.js works without modification.
# Key endpoints: /load, /properties, /sparql, /hierarchy,
#                /imports, /export, /loaded, /objects, /unload
# =============================================================

import json as _json
import warnings as _warnings
from rdflib import ConjunctiveGraph as _CG, URIRef as _URIRef  # _CG kept for compat
from rdflib import Literal as _Literal, BNode as _BNode

# In-memory store for rdflib graphs (renderer compat layer)
_compat_store: dict[str, _CG] = {}

OWL_THING_IRI = 'http://www.w3.org/2002/07/owl#Thing'

EXPORT_FORMATS = {
    'turtle':   ('turtle',   'text/turtle',               '.ttl'),
    'rdfxml':   ('xml',      'application/rdf+xml',       '.rdf'),
    'ntriples': ('nt',       'application/n-triples',     '.nt'),
    'jsonld':   ('json-ld',  'application/ld+json',       '.jsonld'),
}


def _detect_fmt(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    return {'.jsonld':'json-ld','.json':'json-ld','.ttl':'turtle',
            '.n3':'n3','.nt':'nt','.xml':'xml','.rdf':'xml','.owl':'xml'
            }.get(ext, 'json-ld')


def _get_compat_graph(file_path: str) -> _CG:
    g = _compat_store.get(file_path)
    if g is None:
        raise HTTPException(status_code=404,
            detail=f'Ontology not loaded: {file_path}. Call /load first.')
    return g


def _term_val(term) -> dict:
    if isinstance(term, _URIRef):  return {'type':'uri',     'value':str(term)}
    if isinstance(term, _Literal):
        d = {'type':'literal','value':str(term)}
        if term.language: d['lang']     = term.language
        if term.datatype: d['datatype'] = str(term.datatype)
        return d
    if isinstance(term, _BNode):   return {'type':'bnode',   'value':str(term)}
    return {'type':'unknown','value':str(term)}


def _short_key(uri: str, ctx: dict) -> str:
    for prefix, expansion in ctx.items():
        if prefix.startswith('@') or not isinstance(expansion, str): continue
        if uri.startswith(expansion):
            local = uri[len(expansion):]
            if local and '/' not in local and '#' not in local:
                return f'{prefix}:{local}'
    sep = max(uri.rfind('#'), uri.rfind('/'))
    return uri[sep+1:] if sep >= 0 else uri


def _expand_val(val, ctx: dict, base: str):
    if val is None: return None
    if isinstance(val, str):
        if ':' in val and not val.startswith(('http://','https://')):
            colon = val.index(':')
            pfx   = val[:colon]
            if pfx and pfx.isalnum() and isinstance(ctx, dict) and pfx in ctx:
                return _expand_iri(val, ctx, base)
        return val
    if isinstance(val, (int, float, bool)): return str(val)
    if isinstance(val, list):
        items = [_expand_val(v, ctx, base) for v in val]
        items = [i for i in items if i is not None]
        return items if len(items) > 1 else (items[0] if items else None)
    if isinstance(val, dict):
        if '@value' in val: return str(val['@value'])
        if '@id' in val and len(val) == 1:
            full = val['@id']
            if ':' in full and not full.startswith('http'):
                pfx, local = full.split(':',1)
                if pfx in ctx and isinstance(ctx[pfx], str):
                    full = ctx[pfx] + local
                    if not full.startswith('http') and base:
                        full = base.rstrip('/') + '/' + full.lstrip('./ ')
            return full
        parts = {}
        for k, v in val.items():
            if k.startswith('@'): continue
            sk = k.split(':')[-1] if ':' in k else k
            parts[sk] = _expand_val(v, ctx, base)
        return parts
    return str(val)


def _props_from_json(file_path: str, subject_uri: str) -> list:
    with open(file_path, encoding='utf-8') as f:
        data = _json.load(f)
    ctx  = data.get('@context', {})
    base = ctx.get('@base','') if isinstance(ctx, dict) else ''
    def c2f(c): return _expand_iri(c, ctx if isinstance(ctx,dict) else {}, base)
    props, seen = [], set()
    for node in data.get('@graph',[]):
        if c2f(node.get('@id','')) != subject_uri: continue
        for raw_key, raw_val in node.items():
            if raw_key.startswith('@'): continue
            full_key  = c2f(raw_key)
            short     = _short_key(full_key, ctx if isinstance(ctx,dict) else {})
            expanded  = _expand_val(raw_val, ctx if isinstance(ctx,dict) else {}, base)
            if expanded is None: continue
            items = expanded if isinstance(expanded, list) else [expanded]
            for item in items:
                if isinstance(item, dict):
                    obj_str = '  |  '.join(
                        f'{k}: {str(v)[:60]}' for k,v in item.items())
                    ek = (short, obj_str)
                    if ek not in seen:
                        seen.add(ek)
                        props.append({'predicate':{'type':'uri','value':full_key,'short':short},
                                      'object':{'type':'bnode_resolved','value':obj_str}})
                else:
                    s = str(item)
                    ek = (short, s)
                    if ek not in seen:
                        seen.add(ek)
                        t = 'uri' if s.startswith('http') else 'literal'
                        props.append({'predicate':{'type':'uri','value':full_key,'short':short},
                                      'object':{'type':t,'value':s}})
        break
    props.sort(key=lambda x: x['predicate']['short'].lower())
    return props


# ── Pydantic models (compat) ──────────────────────────────────
class CompatSparqlRequest(BaseModel):
    file_path: str
    query:     str

class ExportRequest(BaseModel):
    file_path: str
    format:    str = 'turtle'

class UnloadRequest(BaseModel):
    file_path: str


# ── POST /load ────────────────────────────────────────────────
@app.post('/load', tags=['Compat'])
def compat_load(req: LoadRequest):
    """Bridge-compatible /load — parses JSON-LD and returns objects for Object Explorer."""
    p = Path(req.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'File not found: {req.file_path}')
    fmt = _detect_fmt(req.file_path)
    with _warnings.catch_warnings():
        _warnings.simplefilter('ignore')
        with _warnings.catch_warnings():
            _warnings.simplefilter('ignore', DeprecationWarning)
            g = _CG()
    try:
        g.parse(str(p), format=fmt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Parse error: {e}')
    _compat_store[req.file_path] = g

    # Also load into TscgStore (named graph)
    try:
        _get_store().load_file(req.file_path)
    except Exception:
        pass

    objects = []
    if fmt == 'json-ld':
        try:
            with open(p, encoding='utf-8') as f:
                raw = _json.load(f)
            ctx  = raw.get('@context', {})
            base = ctx.get('@base','') if isinstance(ctx, dict) else ''
            def eid(nid): return _expand_iri(nid, ctx if isinstance(ctx,dict) else {}, base)
            for node in raw.get('@graph', [raw]):
                nid   = eid(node.get('@id',''))
                rtype = node.get('@type','')
                ntype = rtype[0] if isinstance(rtype, list) else rtype
                lbl   = node.get('rdfs:label','')
                if isinstance(lbl, dict): lbl = lbl.get('@value', str(lbl))
                objects.append({'id':nid,'type':ntype,
                                'label':lbl or nid.split('#')[-1].split('/')[-1],
                                'keys':[k for k in node if not k.startswith('@')]})
        except Exception as e:
            print(f'[api/compat] Warning building objects: {e}', flush=True)

    has_classes   = any(o.get('type')=='owl:Class' for o in objects)
    has_owl_thing = any(o.get('id')==OWL_THING_IRI for o in objects)
    if has_classes and not has_owl_thing:
        objects.insert(0, {'id':OWL_THING_IRI,'type':'owl:Class',
                           'label':'owl:Thing','keys':[]})

    subclass_pairs, external_parents, known_ids = [], [], {o['id'] for o in objects}
    instanceof_targets = []
    if fmt == 'json-ld':
        try:
            with open(p, encoding='utf-8') as f:
                raw2 = _json.load(f)
            ctx2  = raw2.get('@context',{})
            base2 = ctx2.get('@base','') if isinstance(ctx2,dict) else ''
            def eid2(nid): return _expand_iri(nid, ctx2 if isinstance(ctx2,dict) else {}, base2)
            graph_nodes = raw2.get('@graph',[raw2])
            for node in graph_nodes:
                child_iri = eid2(node.get('@id',''))
                sub = node.get('rdfs:subClassOf')
                if sub is not None:
                    for par in (sub if isinstance(sub,list) else [sub]):
                        parent_iri = eid2(par.get('@id',par) if isinstance(par,dict) else par)
                        if child_iri and parent_iri:
                            subclass_pairs.append({'child':child_iri,'parent':parent_iri})
                            if parent_iri not in known_ids and \
                                    not any(ep['id']==parent_iri for ep in external_parents):
                                lbl = parent_iri.split('#')[-1].split('/')[-1]
                                fph = None
                                try:
                                    norm = base2.rstrip('/')
                                    if norm and parent_iri.startswith(norm):
                                        rel = parent_iri[len(norm):].lstrip('/')
                                        fr  = rel.split('#')[0]
                                        if fr: fph = str(Path(req.file_path).parent/fr).replace('\\','/')
                                except Exception: pass
                                external_parents.append({'id':parent_iri,'label':lbl,'file_path_hint':fph})
                # instanceof
                ntypes = node.get('@type','')
                ntypes = ntypes if isinstance(ntypes,list) else [ntypes]
                if 'owl:Ontology' in ntypes:
                    raw_io = node.get('m3:instanceOf')
                    if raw_io:
                        for item in (raw_io if isinstance(raw_io,list) else [raw_io]):
                            tgt = eid2(item.get('@id',item) if isinstance(item,dict) else item)
                            if tgt:
                                lbl = tgt.split('#')[-1].split('/')[-1]
                                fph = None
                                try:
                                    norm = base2.rstrip('/')
                                    if norm and tgt.startswith(norm):
                                        rel = tgt[len(norm):].lstrip('/')
                                        fr  = rel.split('#')[0]
                                        if fr: fph = str(Path(req.file_path).parent/fr).replace('\\','/')
                                except Exception: pass
                                instanceof_targets.append({'id':tgt,'label':lbl,'file_path_hint':fph})
        except Exception as e:
            print(f'[api/compat] Warning extracting pairs: {e}', flush=True)

    return {
        'loaded':True,'triples':len(g),'format':fmt,'file_path':req.file_path,
        'objects':objects,'subclass_pairs':subclass_pairs,
        'external_parents':external_parents,'instanceof_targets':instanceof_targets,
    }


# ── GET /loaded ───────────────────────────────────────────────
@app.get('/loaded', tags=['Compat'])
def compat_loaded():
    return {'ontologies':[{'file_path':k,'triples':len(v)} for k,v in _compat_store.items()]}


# ── GET /objects ──────────────────────────────────────────────
@app.get('/objects', tags=['Compat'])
def compat_objects(file_path: str):
    g = _get_compat_graph(file_path)
    q = ('PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
         'SELECT DISTINCT ?s ?type ?label WHERE { ?s a ?type . '
         'OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?type ?label')
    results = []
    for row in g.query(q):
        results.append({'id':str(row.s),'type':str(row.type) if row.type else '',
                        'label':str(row.label) if row.label else str(row.s).split('#')[-1].split('/')[-1]})
    return {'objects':results,'count':len(results)}


# ── GET /properties ───────────────────────────────────────────
@app.get('/properties', tags=['Compat'])
def compat_properties(file_path: str, subject_uri: str):
    if file_path.endswith(('.jsonld','.json')):
        try:
            props = _props_from_json(file_path, subject_uri)
            if props: return {'subject':subject_uri,'properties':props,'count':len(props)}
        except Exception as e:
            print(f'[api/compat] JSON-LD reader failed, rdflib fallback: {e}', flush=True)
    g = _get_compat_graph(file_path)
    subj = _URIRef(subject_uri)
    props, seen_po = [], set()
    for ctx in g.contexts():
        for pred, obj in ctx.predicate_objects(subj):
            po = (str(pred), str(obj))
            if po in seen_po: continue
            seen_po.add(po)
            props.append({'predicate':_term_val(pred),'object':_term_val(obj)})
    props.sort(key=lambda x: x['predicate']['value'].split('#')[-1].split('/')[-1].lower())
    return {'subject':subject_uri,'properties':props,'count':len(props)}


# ── POST /sparql (single-file) ────────────────────────────────
@app.post('/sparql', tags=['Compat'])
def compat_sparql(req: CompatSparqlRequest):
    g = _get_compat_graph(req.file_path)
    try:
        results = g.query(req.query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'SPARQL error: {e}')
    qt = results.type
    if qt == 'ASK':
        return {'query_type':'ASK','result':bool(results)}
    if qt == 'SELECT':
        vars_ = [str(v) for v in results.vars]
        rows  = [{v:_term_val(row[v]) if row[v] is not None else None for v in vars_} for row in results]
        return {'query_type':'SELECT','vars':vars_,'results':rows,'count':len(rows)}
    triples = [{'s':str(s),'p':str(p),'o':str(o)} for s,p,o in results]
    return {'query_type':qt,'vars':['s','p','o'],'results':triples,'count':len(triples)}


# ── GET /hierarchy ────────────────────────────────────────────
@app.get('/hierarchy', tags=['Compat'])
def compat_hierarchy(file_path: str):
    g = _get_compat_graph(file_path)
    q = ('PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
         'SELECT ?child ?parent WHERE { ?child rdfs:subClassOf ?parent . '
         'FILTER(!isBlank(?parent)) FILTER(!isBlank(?child)) }')
    pairs, ext_parents, local_iris = [], {}, {str(s) for s in g.subjects()}
    for row in g.query(q):
        c, par = str(row.child), str(row.parent)
        pairs.append({'child':c,'parent':par})
        if par not in local_iris and par not in ext_parents:
            ext_parents[par] = par.split('#')[-1].split('/')[-1]
    return {'pairs':pairs,'count':len(pairs),
            'external_parents':[{'id':iri,'label':lbl} for iri,lbl in ext_parents.items()]}


# ── GET /imports ──────────────────────────────────────────────
@app.get('/imports', tags=['Compat'])
def compat_imports(file_path: str):
    p = Path(file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'File not found: {file_path}')
    result = {'namespaces':[],'owl_imports':[]}
    try:
        with open(p, encoding='utf-8') as f:
            raw = _json.load(f)
        ctx  = raw.get('@context',{})
        base = ctx.get('@base','') if isinstance(ctx,dict) else ''
        if isinstance(ctx, dict):
            for prefix, uri in ctx.items():
                if prefix.startswith('@') or not isinstance(uri,str): continue
                if not uri.startswith(('http://','https://')):
                    if base: uri = base.rstrip('/')+'/'+uri.lstrip('./')
                    else: continue
                is_local = 'echopraxium' in uri.lower() or 'tscg' in uri.lower()
                local_path = None
                if is_local:
                    fn = uri.split('#')[0].rstrip('/').split('/')[-1]
                    c  = str(p.parent/fn)
                    if Path(c).exists(): local_path = c.replace('\\','/')
                    else:
                        found = list(p.parent.rglob(fn))
                        if found: local_path = str(found[0]).replace('\\','/')
                result['namespaces'].append({'prefix':prefix,'uri':uri,
                                              'is_local':is_local,'local_path':local_path})
        for node in raw.get('@graph',[raw]):
            imports = node.get('owl:imports',[])
            if isinstance(imports,str): imports = [imports]
            for imp in imports:
                uri = imp.get('@id',imp) if isinstance(imp,dict) else imp
                if not uri.startswith(('http://','https://')):
                    uri = base.rstrip('/')+'/'+uri.lstrip('./')
                is_local = 'echopraxium' in uri.lower() or 'tscg' in uri.lower()
                local_path = None
                if is_local:
                    fn = uri.split('#')[0].rstrip('/').split('/')[-1]
                    c  = str(p.parent/fn)
                    if Path(c).exists(): local_path = str(Path(c).resolve()).replace('\\','/')
                    else:
                        found = list(p.parent.rglob(fn))
                        if found: local_path = str(found[0].resolve()).replace('\\','/')
                result['owl_imports'].append({'uri':uri,'is_local':is_local,'local_path':local_path})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error reading imports: {e}')
    return result


# ── DELETE /unload ────────────────────────────────────────────
@app.delete('/unload', tags=['Compat'])
def compat_unload(file_path: str):
    removed = file_path in _compat_store
    _compat_store.pop(file_path, None)
    return {'unloaded': removed}


# ── POST /export ──────────────────────────────────────────────
@app.post('/export', tags=['Compat'])
def compat_export(req: ExportRequest):
    p = Path(req.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'File not found: {req.file_path}')
    fmt_info = EXPORT_FORMATS.get(req.format)
    if not fmt_info:
        raise HTTPException(status_code=400,
            detail=f'Unknown format: {req.format}. Use: {list(EXPORT_FORMATS)}')
    rdflib_fmt, mime_type, extension = fmt_info
    g = _compat_store.get(req.file_path)
    if g is None:
        with _warnings.catch_warnings():
            _warnings.simplefilter('ignore')
            with _warnings.catch_warnings():
                _warnings.simplefilter('ignore', DeprecationWarning)
                g = _CG()
        g.parse(str(p), format=_detect_fmt(req.file_path))
    try:
        content = g.serialize(format=rdflib_fmt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serialization error: {e}')
    return {'content':content,'format':req.format,'extension':extension,
            'mime_type':mime_type,'triples':len(g)}


# ── GET /export/formats ───────────────────────────────────────
@app.get('/export/formats', tags=['Compat'])
def compat_export_formats():
    return {'formats':[{'id':k,'label':v[0],'mime':v[1],'extension':v[2]}
                       for k,v in EXPORT_FORMATS.items()]}


# ─────────────────────────────────────────────────────────────
# Store init  +  entry point
# ─────────────────────────────────────────────────────────────
def _init_store(store_path: Optional[str], ontology_dir: Optional[str]):
    global _tscg_store
    _tscg_store = TscgStore(db_path=store_path)
    st = _tscg_store.stats()
    if _tscg_store._db_path:   # may differ from store_path if fallback occurred
        print(f'[api] TscgStore: persistent → {_tscg_store._db_path} '
              f'({st["total_triples"]} triples, {st["named_graphs"]} graphs)',
              flush=True)
    else:
        print('[api] TscgStore: in-memory  '
              '(pass --store-path <file.oxg> for persistence)', flush=True)

    if ontology_dir:
        root = Path(ontology_dir)
        if root.exists():
            print(f'[api] Auto-loading ontology from {root} …', flush=True)
            result = _tscg_store.load_pattern(
                str(root),
                ['M3_*.jsonld', 'M2_*.jsonld', 'M1_*.jsonld',
                 'instances/**/*.jsonld'],
            )
            st2 = _tscg_store.stats()
            print(f'[api]   → {result["files_loaded"]} files, '
                  f'{st2["total_triples"]} triples, '
                  f'{st2["named_graphs"]} graphs', flush=True)
            for err in result.get('errors', []):
                print(f'[api]   ⚠ {err["file"]}: {err["error"]}', flush=True)
        else:
            print(f'[api] Warning: --ontology-dir not found: {ontology_dir}',
                  flush=True)


if __name__ == '__main__':
    # Force UTF-8 stdout/stderr on Windows (avoids cp1252 UnicodeEncodeError)
    import sys, io
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(
        description='TscgOntologyAPIServer — standalone SPARQL/REST server'
    )
    parser.add_argument('--host',         default='127.0.0.1',
                        help='Bind address (default: 127.0.0.1)')
    parser.add_argument('--port',         type=int, default=8000,
                        help='Bind port (default: 8000)')
    parser.add_argument('--store-path',   default=None,
                        help='Path to persistent pyoxigraph store (.oxg). '
                             'Omit for in-memory mode.')
    parser.add_argument('--ontology-dir', default=None,
                        help='Ontology root to auto-load on startup.')
    parser.add_argument('--log-level',    default='warning',
                        choices=['critical', 'error', 'warning', 'info', 'debug'],
                        help='uvicorn log level (default: warning)')
    args = parser.parse_args()

    _init_store(args.store_path, args.ontology_dir)

    # Check if store init requested a fallback port (in-memory on 8001)
    effective_port = getattr(_tscg_store, '_fallback_port', None) or args.port

    print(f'[api] TscgOntologyAPIServer v{SERVER_VERSION} '
          f'→ http://{args.host}:{effective_port}', flush=True)
    print(f'[api] Swagger UI → http://{args.host}:{effective_port}/docs', flush=True)

    uvicorn.run(app, host=args.host, port=effective_port, log_level=args.log_level)
