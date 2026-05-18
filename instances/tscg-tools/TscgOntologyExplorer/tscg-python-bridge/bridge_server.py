# =============================================================
# tscg-python-bridge — bridge_server.py
# Persistent FastAPI server for TscgOntologyEditor.
# Provides RDF parsing, SPARQL queries and SHACL validation.
# Author: Echopraxium with the collaboration of Claude AI
# =============================================================

import sys
import json
import argparse
import importlib.metadata
from pathlib import Path
from typing import Optional

import rdflib
from rdflib import Graph, ConjunctiveGraph, URIRef, Literal, BNode, Namespace
from rdflib.plugins.sparql import prepareQuery
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── CLI args ───────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=7432)
args = parser.parse_args()

# ── App ────────────────────────────────────────────────────────
app = FastAPI(title='TscgOntologyEditor Python Bridge', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# ── In-memory ontology store ───────────────────────────────────
# key: absolute file path (str)  value: rdflib.ConjunctiveGraph
ontology_store: dict[str, ConjunctiveGraph] = {}

# ── Request models ─────────────────────────────────────────────
class LoadRequest(BaseModel):
    file_path: str

class PropertiesRequest(BaseModel):
    file_path: str
    subject_uri: str

class SparqlRequest(BaseModel):
    file_path: str
    query: str

class ValidateRequest(BaseModel):
    data_file_path: str
    shacl_file_path: Optional[str] = None

# ── Helpers ────────────────────────────────────────────────────
def _get_graph(file_path: str) -> ConjunctiveGraph:
    """Return loaded graph or raise 404."""
    g = ontology_store.get(file_path)
    if g is None:
        raise HTTPException(status_code=404,
            detail=f'Ontology not loaded: {file_path}. Call /load first.')
    return g

def _term_to_value(term) -> dict:
    """Serialize an rdflib term to a JSON-friendly dict."""
    if isinstance(term, URIRef):
        return {'type': 'uri',     'value': str(term)}
    if isinstance(term, Literal):
        d = {'type': 'literal', 'value': str(term)}
        if term.language: d['lang']     = term.language
        if term.datatype: d['datatype'] = str(term.datatype)
        return d
    if isinstance(term, BNode):
        return {'type': 'bnode', 'value': str(term)}
    return {'type': 'unknown', 'value': str(term)}

def _detect_format(file_path: str) -> str:
    """Detect RDF format from file extension."""
    ext = Path(file_path).suffix.lower()
    return {
        '.jsonld': 'json-ld',
        '.json':   'json-ld',
        '.ttl':    'turtle',
        '.n3':     'n3',
        '.nt':     'nt',
        '.xml':    'xml',
        '.rdf':    'xml',
        '.owl':    'xml',
    }.get(ext, 'json-ld')

# =============================================================
# ENDPOINTS
# =============================================================

# ── Health ─────────────────────────────────────────────────────
@app.get('/health')
def health():
    try:
        rdflib_ver  = importlib.metadata.version('rdflib')
    except Exception:
        rdflib_ver  = rdflib.__version__
    try:
        import pyshacl
        pyshacl_ver = importlib.metadata.version('pyshacl')
    except Exception:
        pyshacl_ver = 'not installed'

    return {
        'status':            'ok',
        'rdflib_version':    rdflib_ver,
        'pyshacl_version':   pyshacl_ver,
        'ontologies_loaded': len(ontology_store),
    }

# ── Load ontology ──────────────────────────────────────────────
@app.post('/load')
def load_ontology(req: LoadRequest):
    """
    Load a JSON-LD (or any RDF) file into the in-memory store.
    Also returns the raw @graph for the Object Explorer.
    """
    p = Path(req.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'File not found: {req.file_path}')

    fmt = _detect_format(req.file_path)
    g   = ConjunctiveGraph()
    try:
        g.parse(str(p), format=fmt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Parse error: {e}')

    ontology_store[req.file_path] = g

    # ── Build object list from JSON-LD @graph ──────────────────
    # Direct JSON parse preserves @graph structure for the Object Explorer
    objects = []
    if fmt == 'json-ld':
        try:
            with open(p, encoding='utf-8') as f:
                raw = json.load(f)
            graph_nodes = raw.get('@graph', [raw])  # single node or array
            for node in graph_nodes:
                node_id    = node.get('@id', '')
                node_type  = node.get('@type', '')
                label_val  = node.get('rdfs:label', '')
                if isinstance(label_val, dict):
                    label_val = label_val.get('@value', str(label_val))
                objects.append({
                    'id':    node_id,
                    'type':  node_type,
                    'label': label_val or node_id.split('#')[-1].split('/')[-1],
                    'keys':  [k for k in node.keys() if not k.startswith('@')]
                })
        except Exception:
            pass  # fall back to empty objects list

    return {
        'loaded':    True,
        'triples':   len(g),
        'format':    fmt,
        'file_path': req.file_path,
        'objects':   objects,
    }

# ── List loaded ontologies ─────────────────────────────────────
@app.get('/loaded')
def list_loaded():
    return {
        'ontologies': [
            {'file_path': k, 'triples': len(v)}
            for k, v in ontology_store.items()
        ]
    }

# ── Get all objects (subjects) in a graph ──────────────────────
@app.get('/objects')
def get_objects(file_path: str):
    """Return distinct subjects with type and label via SPARQL."""
    g = _get_graph(file_path)
    q = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?s ?type ?label WHERE {
            ?s a ?type .
            OPTIONAL { ?s rdfs:label ?label }
        }
        ORDER BY ?type ?label
    """
    results = []
    for row in g.query(q):
        results.append({
            'id':    str(row.s),
            'type':  str(row.type)  if row.type  else '',
            'label': str(row.label) if row.label else str(row.s).split('#')[-1].split('/')[-1],
        })
    return {'objects': results, 'count': len(results)}

# ── Get properties of a subject ────────────────────────────────
@app.get('/properties')
def get_properties(file_path: str, subject_uri: str):
    """Return all predicate-object pairs for a given subject URI."""
    g = _get_graph(file_path)
    subject = URIRef(subject_uri)
    props   = []
    for pred, obj in g.predicate_objects(subject):
        props.append({
            'predicate': _term_to_value(pred),
            'object':    _term_to_value(obj),
        })
    # Sort by predicate URI for consistent display
    props.sort(key=lambda x: x['predicate']['value'])
    return {'subject': subject_uri, 'properties': props, 'count': len(props)}

# ── SPARQL query ───────────────────────────────────────────────
@app.post('/sparql')
def sparql_query(req: SparqlRequest):
    """
    Execute a SPARQL SELECT, CONSTRUCT, ASK, or DESCRIBE query.
    Returns results in a JSON-friendly format.
    """
    g = _get_graph(req.file_path)
    try:
        results = g.query(req.query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'SPARQL error: {e}')

    query_type = results.type  # 'SELECT', 'CONSTRUCT', 'ASK', 'DESCRIBE'

    if query_type == 'ASK':
        return {'type': 'ASK', 'result': bool(results)}

    if query_type == 'SELECT':
        vars_  = [str(v) for v in results.vars]
        rows   = []
        for row in results:
            rows.append({v: _term_to_value(row[v]) if row[v] is not None else None
                         for v in vars_})
        return {'type': 'SELECT', 'vars': vars_, 'results': rows, 'count': len(rows)}

    if query_type in ('CONSTRUCT', 'DESCRIBE'):
        triples = [
            {
                's': _term_to_value(s),
                'p': _term_to_value(p),
                'o': _term_to_value(o)
            }
            for s, p, o in results
        ]
        return {'type': query_type, 'triples': triples, 'count': len(triples)}

    return {'type': query_type, 'raw': str(results)}

# ── SHACL validation ───────────────────────────────────────────
@app.post('/validate')
def validate(req: ValidateRequest):
    """
    Validate data_file_path against a SHACL shapes graph.
    If shacl_file_path is omitted, uses pyshacl's built-in OWL-RL inference.
    """
    try:
        import pyshacl
    except ImportError:
        raise HTTPException(status_code=501,
            detail='pyshacl not installed. Run: pip install pyshacl')

    data_path = Path(req.data_file_path)
    if not data_path.exists():
        raise HTTPException(status_code=404, detail=f'Data file not found: {req.data_file_path}')

    shacl_graph = None
    if req.shacl_file_path:
        shacl_path = Path(req.shacl_file_path)
        if not shacl_path.exists():
            raise HTTPException(status_code=404,
                detail=f'SHACL file not found: {req.shacl_file_path}')
        shacl_graph = str(shacl_path)

    try:
        conforms, results_graph, results_text = pyshacl.validate(
            str(data_path),
            shacl_graph=shacl_graph,
            data_graph_format=_detect_format(str(data_path)),
            inference='rdfs',
            serialize_report_graph=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Validation error: {e}')

    return {
        'conforms':      conforms,
        'results_text':  results_text,
        'data_file':     req.data_file_path,
        'shacl_file':    req.shacl_file_path or '(none)',
    }

# ── Unload ontology ────────────────────────────────────────────
@app.delete('/unload')
def unload_ontology(file_path: str):
    if file_path in ontology_store:
        del ontology_store[file_path]
        return {'unloaded': True}
    return {'unloaded': False}

# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == '__main__':
    print(f'[bridge] Starting on port {args.port}', flush=True)
    uvicorn.run(app, host='127.0.0.1', port=args.port, log_level='warning')
