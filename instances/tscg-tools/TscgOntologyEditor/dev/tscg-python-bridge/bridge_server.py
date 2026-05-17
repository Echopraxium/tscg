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
import warnings
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
        return {'type': 'bnode', 'value': str(term), '_bnode_id': str(term)}
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
    # ── Support local path OR http(s):// URL ──────────────────────
    is_url = req.file_path.startswith(('http://', 'https://'))

    if not is_url:
        p = Path(req.file_path)
        if not p.exists():
            raise HTTPException(status_code=404, detail=f'File not found: {req.file_path}')
    
    fmt = _detect_format(req.file_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        g   = ConjunctiveGraph()
    try:
        source = req.file_path  # rdflib accepts both file paths and URLs
        g.parse(source, format=fmt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Parse error: {e}')

    ontology_store[req.file_path] = g

    # ── Build object list from JSON-LD @graph ──────────────────
    # IRIs expanded via @context so they match rdflib expanded IRIs
    # (e.g. "m2:ConceptContract" → "https://...#ConceptContract")
    objects = []
    if fmt == 'json-ld':
        try:
            with open(p, encoding='utf-8') as f:
                raw = json.load(f)
            ctx         = raw.get('@context', {})
            base        = ctx.get('@base', '') if isinstance(ctx, dict) else ''
            graph_nodes = raw.get('@graph', [raw])

            def expand_id(node_id):
                """Expand compact IRI using @context and @base.
                Handles both absolute and relative prefix URIs.
                e.g. m2:ConceptContract where m2=M2_GenericConcepts.jsonld# (relative)
                resolves against @base to produce the full absolute IRI.
                """
                if not node_id or node_id.startswith(("http://", "https://")):
                    return node_id
                # Try prefix expansion: "m2:Foo" -> look up "m2" in @context
                if isinstance(ctx, dict) and ":" in node_id:
                    prefix, local = node_id.split(":", 1)
                    prefix_uri = ctx.get(prefix, "")
                    if isinstance(prefix_uri, str) and prefix_uri:
                        if prefix_uri.startswith(("http://", "https://")):
                            return prefix_uri + local   # already absolute
                        elif base:
                            # Relative prefix -> resolve against @base
                            abs_prefix = base.rstrip("/") + "/" + prefix_uri.lstrip("./")
                            print(f"[bridge expand_id] {node_id} -> {abs_prefix + local}", flush=True)
                            return abs_prefix + local
                # @base fallback
                if base:
                    return base.rstrip("/") + "/" + node_id.lstrip("./")
                return node_id

            for node in graph_nodes:
                node_id   = expand_id(node.get('@id', ''))
                # @type can be a string or a list — normalize to first value for display
                raw_type  = node.get('@type', '')
                node_type = raw_type[0] if isinstance(raw_type, list) else raw_type
                label_val = node.get('rdfs:label', '')
                if isinstance(label_val, dict):
                    label_val = label_val.get('@value', str(label_val))
                objects.append({
                    'id':    node_id,
                    'type':  node_type,
                    'label': label_val or node_id.split('#')[-1].split('/')[-1],
                    'keys':  [k for k in node.keys() if not k.startswith('@')]
                })
        except Exception as e:
            print(f'[bridge] Warning building objects: {e}', flush=True)

    # ── Add owl:Thing if it appears as a parent in rdfs:subClassOf ──
    # owl:Thing is a real OWL built-in class — include it as root node
    # when any class in this ontology is a direct subclass of it.
    OWL_THING_IRI = 'http://www.w3.org/2002/07/owl#Thing'
    RDFS_SUBCLASSOF = rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')
    OWL_THING_REF   = rdflib.URIRef(OWL_THING_IRI)

    has_thing_children = any(
        o == OWL_THING_REF
        for _, _, o in g.triples((None, RDFS_SUBCLASSOF, None))
    )
    if has_thing_children:
        objects.insert(0, {
            'id':    OWL_THING_IRI,
            'type':  'owl:Class',
            'label': 'owl:Thing',
            'keys':  []
        })

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

# ── JSON-LD direct property reader ──────────────────────────────
def _short_key(uri: str, ctx: dict) -> str:
    """Resolve a full URI to its shortest prefix:local form using @context."""
    # Try reverse-lookup in context
    for prefix, expansion in ctx.items():
        if prefix.startswith('@') or not isinstance(expansion, str): continue
        if uri.startswith(expansion):
            local = uri[len(expansion):]
            if local and '/' not in local and '#' not in local:
                return f'{prefix}:{local}'
    # Fallback: just the local name after last # or /
    sep = max(uri.rfind('#'), uri.rfind('/'))
    return uri[sep+1:] if sep >= 0 else uri

def _expand_value(val, ctx: dict, base: str):
    """Recursively expand a JSON-LD value to a human-readable string."""
    if val is None:
        return None
    if isinstance(val, str):
        return val
    if isinstance(val, (int, float, bool)):
        return str(val)
    if isinstance(val, list):
        items = [_expand_value(v, ctx, base) for v in val]
        items = [i for i in items if i is not None]
        return items if len(items) > 1 else (items[0] if items else None)
    if isinstance(val, dict):
        if '@value' in val:
            return str(val['@value'])
        if '@id' in val and len(val) == 1:
            full = val['@id']
            if ':' in full and not full.startswith('http'):
                pfx, local = full.split(':', 1)
                if pfx in ctx and isinstance(ctx[pfx], str):
                    full = ctx[pfx] + local
                    # Resolve against @base if prefix expansion still relative
                    if not full.startswith('http') and base:
                        full = base.rstrip('/') + '/' + full.lstrip('./ ')
            return full
        # Anonymous node → flatten to readable key: value pairs
        parts = {}
        for k, v in val.items():
            if k.startswith('@'): continue
            # Short key: strip prefix
            short_k = k.split(':')[-1] if ':' in k else k
            parts[short_k] = _expand_value(v, ctx, base)
        return parts
    return str(val)

def _get_properties_from_json(file_path: str, subject_uri: str) -> list:
    """Read properties directly from JSON-LD — bypasses rdflib blank node issues."""
    import json as _json
    with open(file_path, encoding='utf-8') as f:
        data = _json.load(f)

    ctx  = data.get('@context', {})
    base = ctx.get('@base', '') if isinstance(ctx, dict) else ''

    def compact_to_full(ciri: str) -> str:
        if ciri.startswith('http'): return ciri
        if ':' in ciri:
            pfx, local = ciri.split(':', 1)
            expansion = ctx.get(pfx, '') if isinstance(ctx, dict) else ''
            if expansion:
                full = expansion + local
                # Expansion may itself be relative — resolve against @base
                if not full.startswith('http') and base:
                    full = base.rstrip('/') + '/' + full.lstrip('./')
                return full
        # Bare name — resolve against @base
        return (base.rstrip('/') + '/' + ciri) if base else ciri

    props = []
    seen  = set()
    for node in data.get('@graph', []):
        node_id = compact_to_full(node.get('@id', ''))
        if node_id != subject_uri: continue

        for raw_key, raw_val in node.items():
            if raw_key.startswith('@'): continue
            # Expand key to full URI then compact for display
            full_key = compact_to_full(raw_key)
            short_key = _short_key(full_key, ctx if isinstance(ctx, dict) else {})
            expanded  = _expand_value(raw_val, ctx if isinstance(ctx, dict) else {}, base)
            if expanded is None: continue

            if isinstance(expanded, list):
                for item in expanded:
                    entry_key = (short_key, str(item))
                    if entry_key in seen: continue
                    seen.add(entry_key)
                    props.append({
                        'predicate': {'type': 'uri', 'value': full_key, 'short': short_key},
                        'object':    {'type': 'literal' if not str(item).startswith('http') else 'uri',
                                      'value': str(item)}
                    })
            elif isinstance(expanded, dict):
                # Inline anonymous object — flatten top-level keys only
                def _fmt(v):
                    if isinstance(v, dict): return '{…}'
                    if isinstance(v, list): return f'[{len(v)} items]'
                    s = str(v)
                    return s[:60] + '…' if len(s) > 60 else s
                obj_str = '  |  '.join(f'{k}: {_fmt(v)}' for k,v in expanded.items())
                entry_key = (short_key, obj_str)
                if entry_key not in seen:
                    seen.add(entry_key)
                    props.append({
                        'predicate': {'type': 'uri', 'value': full_key, 'short': short_key},
                        'object':    {'type': 'bnode_resolved', 'value': obj_str}
                    })
            else:
                entry_key = (short_key, str(expanded))
                if entry_key in seen: continue
                seen.add(entry_key)
                props.append({
                    'predicate': {'type': 'uri', 'value': full_key, 'short': short_key},
                    'object':    {'type': 'literal' if not str(expanded).startswith('http') else 'uri',
                                  'value': str(expanded)}
                })
        break  # found our node

    props.sort(key=lambda x: x['predicate']['short'].lower())
    return props

# ── Get properties of a subject ────────────────────────────────
def _resolve_bnode_in_ctx(ctx, bnode, depth=0):
    """Resolve a blank node WITHIN its own named graph context.
    Blank nodes are graph-scoped in JSON-LD — must resolve in same ctx."""
    if depth > 3:
        return {'type': 'bnode', 'value': '…'}
    parts = []
    seen  = set()
    for p, o in ctx.predicate_objects(bnode):
        pred_label = str(p).split('#')[-1].split('/')[-1]
        if isinstance(o, BNode):
            inner   = _resolve_bnode_in_ctx(ctx, o, depth + 1)
            obj_val = inner.get('value', '…')
        elif isinstance(o, Literal):
            obj_val = str(o)
        else:
            obj_val = str(o).split('#')[-1].split('/')[-1]
        entry = f'{pred_label}: {obj_val}'
        if entry not in seen:
            seen.add(entry)
            parts.append(entry)
    if parts:
        return {'type': 'bnode_resolved', 'value': ' | '.join(sorted(parts))}
    return {'type': 'bnode', 'value': '(unresolved)'}

@app.get('/properties')
def get_properties(file_path: str, subject_uri: str):
    """Return all predicate-object pairs for a given subject URI.
    Uses direct JSON-LD parsing for reliable blank node resolution."""
    # Use JSON-LD direct reader (bypasses rdflib blank node scoping issues)
    if file_path.endswith('.jsonld') or file_path.endswith('.json'):
        try:
            props = _get_properties_from_json(file_path, subject_uri)
            if props:
                return {'subject': subject_uri, 'properties': props, 'count': len(props)}
        except Exception as e:
            print(f'[bridge] JSON-LD reader failed, falling back to rdflib: {e}')

    # Fallback: rdflib SPARQL (for non-JSON-LD files)
    g       = _get_graph(file_path)
    subject = URIRef(subject_uri)
    props   = []
    seen_po = set()
    for ctx in g.contexts():
        for pred, obj in ctx.predicate_objects(subject):
            po_key = (str(pred), str(obj))
            if po_key in seen_po: continue
            seen_po.add(po_key)
            if isinstance(obj, BNode):
                obj_val = _resolve_bnode_in_ctx(ctx, obj)
            else:
                obj_val = _term_to_value(obj)
            props.append({'predicate': _term_to_value(pred), 'object': obj_val})
    props.sort(key=lambda x: x['predicate']['value'].split('#')[-1].split('/')[-1].lower())
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
        return {'query_type': 'ASK', 'result': bool(results)}

    if query_type == 'SELECT':
        vars_  = [str(v) for v in results.vars]
        rows   = []
        for row in results:
            rows.append({v: _term_to_value(row[v]) if row[v] is not None else None
                         for v in vars_})
        return {'query_type': 'SELECT', 'vars': vars_, 'results': rows, 'count': len(rows)}

    if query_type in ('CONSTRUCT', 'DESCRIBE'):
        triples = [
            {
                's': _term_to_value(s),
                'p': _term_to_value(p),
                'o': _term_to_value(o)
            }
            for s, p, o in results
        ]
        # CONSTRUCT: return triples as results rows for Save As .ttl
        triple_rows = [{'s': str(s), 'p': str(p), 'o': str(o)} for s, p, o in triples]
        return {'query_type': query_type, 'vars': ['s','p','o'], 'results': triple_rows, 'count': len(triples)}

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





# ── List layer files ───────────────────────────────────────────
@app.get('/list-layer-files')
def list_layer_files(ontology_root: str, layer: str):
    """
    Scan ontology_root for files matching a layer prefix (M3_, M1_ etc.)
    Returns a list of { filename, label } for the file picker dialog.
    """
    import pathlib, re
    p = pathlib.Path(ontology_root)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'Ontology root not found: {ontology_root}')
    
    prefix = layer.upper() + '_'
    files  = sorted([
        { 'filename': f.name,
          'label':    f.stem,        # e.g. "M3_GenesisGrammar"
          'path':     str(f)
        }
        for f in p.glob(f'{prefix}*.jsonld')
    ], key=lambda x: x['label'])
    
    return { 'layer': layer, 'files': files }

# ── Imports endpoint ───────────────────────────────────────────
@app.get('/imports')
def get_imports(file_path: str):
    """
    Return @context namespaces and owl:imports from a JSON-LD file.
    Used to populate the Imports tab in TscgOntologyEditor.
    """
    import pathlib
    p = pathlib.Path(file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'File not found: {file_path}')
    
    result = { 'namespaces': [], 'owl_imports': [] }
    
    try:
        with open(p, encoding='utf-8') as f:
            raw = json.load(f)
        
        ctx  = raw.get('@context', {})
        base = ctx.get('@base', '') if isinstance(ctx, dict) else ''
        
        # ── @context namespaces ──────────────────────────────────
        if isinstance(ctx, dict):
            for prefix, uri in ctx.items():
                if prefix.startswith('@') or not isinstance(uri, str):
                    continue
                # Resolve relative URI against @base
                if not uri.startswith(('http://', 'https://')):
                    if base:
                        uri = base.rstrip('/') + '/' + uri.lstrip('./')
                    else:
                        continue
                # Classify: external (w3.org, schema.org etc.) or local (GitHub/tscg)
                is_local = 'echopraxium' in uri.lower() or 'tscg' in uri.lower()
                # For local ontologies: resolve the local file path alongside the IRI
                local_path = None
                if is_local:
                    uri_base   = uri.split('#')[0].rstrip('/')
                    filename   = uri_base.split('/')[-1]
                    candidate  = str(p.parent / filename)
                    if pathlib.Path(candidate).exists():
                        local_path = candidate.replace('\\', '/')
                result['namespaces'].append({
                    'prefix':     prefix,
                    'uri':        uri,
                    'is_local':   is_local,
                    'local_path': local_path
                })
        
        # ── owl:imports ──────────────────────────────────────────
        graph_nodes = raw.get('@graph', [raw])
        for node in graph_nodes:
            imports = node.get('owl:imports', [])
            if isinstance(imports, str):
                imports = [imports]
            for imp in imports:
                uri = imp.get('@id', imp) if isinstance(imp, dict) else imp
                # Resolve relative IRIs against @base (standard JSON-LD behaviour)
                # e.g. "M3_GenesisGrammar.jsonld" + base → canonical absolute IRI
                if not uri.startswith(('http://', 'https://')):
                    uri = base.rstrip('/') + '/' + uri.lstrip('./')

                # Now uri is always absolute — classify and resolve local path
                is_local   = 'echopraxium' in uri.lower() or 'tscg' in uri.lower()
                local_path = None

                if is_local:
                    filename  = uri.split('#')[0].rstrip('/').split('/')[-1]
                    candidate = str(p.parent / filename)
                    if pathlib.Path(candidate).exists():
                        local_path = str(pathlib.Path(candidate).resolve()).replace('\\', '/')

                result['owl_imports'].append({
                    'uri':        uri,       # canonical absolute IRI
                    'is_local':   is_local,
                    'local_path': local_path # Windows path for loadFile()
                })
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error reading imports: {e}')
    
    return result

# ── Hierarchy endpoint ─────────────────────────────────────────
@app.get('/hierarchy')
def get_hierarchy(file_path: str):
    """
    Returns rdfs:subClassOf parent-child pairs for building
    a hierarchical tree in the Object Explorer.
    """
    g = _get_graph(file_path)
    q = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        SELECT ?child ?parent WHERE {
            ?child rdfs:subClassOf ?parent .
            FILTER (!isBlank(?parent))
            FILTER (!isBlank(?child))
        }
    """
    pairs = []
    for row in g.query(q):
        pairs.append({ 'child': str(row.child), 'parent': str(row.parent) })
    return { 'pairs': pairs, 'count': len(pairs) }

# ── Export endpoint ────────────────────────────────────────────

class ExportRequest(BaseModel):
    file_path: str
    format:    str = 'turtle'   # 'turtle' | 'rdfxml' | 'ntriples' | 'jsonld'

# Format config: { rdflib_fmt, mime_type, extension }
EXPORT_FORMATS = {
    'turtle':   ('turtle',  'text/turtle',             '.ttl'),
    'rdfxml':   ('xml',     'application/rdf+xml',     '.rdf'),
    'ntriples': ('nt',      'application/n-triples',   '.nt'),
    'jsonld':   ('json-ld', 'application/ld+json',     '.jsonld'),
}

def _bind_absolute_namespaces(g: ConjunctiveGraph, file_path: str):
    """
    For JSON-LD files, resolve relative namespace prefixes to absolute URIs
    using the @base and @context from the source file.
    This ensures exported Turtle has correct absolute URIs for Protégé.
    """
    if not file_path.lower().endswith(('.jsonld', '.json')):
        return
    try:
        with open(file_path, encoding='utf-8') as f:
            raw = json.load(f)
        ctx  = raw.get('@context', {})
        base = ctx.get('@base', '')
        for prefix, uri in ctx.items():
            if prefix.startswith('@') or not isinstance(uri, str):
                continue
            # Resolve relative URI against @base
            if uri.startswith('http://') or uri.startswith('https://'):
                abs_uri = uri
            elif base:
                abs_uri = base.rstrip('/') + '/' + uri.lstrip('./')
            else:
                continue
            try:
                g.bind(prefix, abs_uri, override=True)
            except Exception:
                pass
    except Exception as e:
        print(f'[bridge] Warning: could not bind namespaces: {e}', flush=True)

@app.post('/export')
def export_ontology(req: ExportRequest):
    """
    Export a loaded ontology to a semantic web format.
    Supported formats: turtle, rdfxml, ntriples, jsonld.
    Resolves relative URIs to absolute URIs before serialization.
    """
    p = Path(req.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f'File not found: {req.file_path}')

    fmt_info = EXPORT_FORMATS.get(req.format)
    if not fmt_info:
        raise HTTPException(status_code=400,
            detail=f'Unknown format: {req.format}. Use: {list(EXPORT_FORMATS.keys())}')

    rdflib_fmt, mime_type, extension = fmt_info

    # Use stored graph or parse fresh
    g = ontology_store.get(req.file_path)
    if g is None:
        g = ConjunctiveGraph()
        g.parse(str(p), format=_detect_format(req.file_path))

    # Bind absolute namespace URIs (critical for Protégé compatibility)
    _bind_absolute_namespaces(g, req.file_path)

    try:
        content = g.serialize(format=rdflib_fmt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serialization error: {e}')

    return {
        'content':   content,
        'format':    req.format,
        'extension': extension,
        'mime_type': mime_type,
        'triples':   len(g)
    }

@app.get('/export/formats')
def list_export_formats():
    """List available export formats."""
    return {
        'formats': [
            { 'id': k, 'label': v[0], 'mime': v[1], 'extension': v[2] }
            for k, v in EXPORT_FORMATS.items()
        ]
    }

# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == '__main__':
    print(f'[bridge] Starting on port {args.port}', flush=True)
    uvicorn.run(app, host='127.0.0.1', port=args.port, log_level='warning')
