#!/usr/bin/env python3
"""
tscg_api_client_example.py
===========================
Example Python client for TscgOntologyAPIServer.

Demonstrates:
  1. Health check
  2. Loading ontology files into the store
  3. Listing loaded graphs
  4. Running SPARQL queries
  5. Filtering by layer (M2, M1, M0)
  6. Exporting results as JSON-LD or Turtle
  7. Hot-reload trigger
  8. IRI resolution helper

Requirements:
    pip install requests

Usage:
    python tscg_api_client_example.py
    python tscg_api_client_example.py --host localhost --port 8000
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional
import requests


# ── Client class ─────────────────────────────────────────────────────────────

class TscgAPIClient:
    """Thin client for TscgOntologyAPIServer REST API."""

    def __init__(self, host: str = "localhost", port: int = 8000, timeout: int = 30):
        self.base_url = f"http://{host}:{port}"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    # ── Connectivity ──────────────────────────────────────────────────────────

    def health(self) -> dict:
        """GET /health — server status, uptime, graph count."""
        r = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def info(self) -> dict:
        """GET /info — server metadata (version, store_path, loaded_graphs)."""
        r = self.session.get(f"{self.base_url}/info", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def is_running(self) -> bool:
        """Quick connectivity check."""
        try:
            self.health()
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    # ── Corpus management ──────────────────────────────────────────────────────

    def load(self, file_path: str) -> dict:
        """POST /corpus/load — load a JSON-LD file into a named graph."""
        r = self.session.post(
            f"{self.base_url}/corpus/load",
            json={"file_path": str(file_path)},
            timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def load_dir(self, directory: str, pattern: str = "**/*.jsonld") -> list[dict]:
        """Load all JSON-LD files matching pattern from a directory."""
        results = []
        for p in Path(directory).glob(pattern):
            try:
                result = self.load(str(p))
                results.append({"file": p.name, "status": "ok", **result})
                print(f"  ✅ Loaded: {p.name}")
            except requests.HTTPError as e:
                results.append({"file": p.name, "status": "error", "error": str(e)})
                print(f"  ❌ Failed: {p.name} — {e}")
        return results

    def list_graphs(self) -> list[dict]:
        """GET /corpus/list — list all named graphs with triple counts."""
        r = self.session.get(f"{self.base_url}/corpus/list", timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        # Response: {"total_triples":..., "graph_count":..., "graphs":[...]}
        return data.get("graphs", data) if isinstance(data, dict) else data

    def list_layers(self) -> dict:
        """GET /corpus/layers — graphs grouped by M3/M2/M1/M0 layer."""
        r = self.session.get(f"{self.base_url}/corpus/layers", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def reload(self) -> dict:
        """POST /corpus/reload — hot-reload all ontology files from disk."""
        r = self.session.post(f"{self.base_url}/corpus/reload", timeout=60)
        r.raise_for_status()
        return r.json()

    def delete_graph(self, graph_iri: str) -> dict:
        """DELETE /corpus/graph — remove a named graph."""
        r = self.session.delete(
            f"{self.base_url}/corpus/graph",
            json={"graph_iri": graph_iri},
            timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def save(self) -> dict:
        """POST /corpus/save — persist current store to .oxg file."""
        r = self.session.post(f"{self.base_url}/corpus/save", timeout=30)
        r.raise_for_status()
        return r.json()

    # ── SPARQL ──────────────────────────────────────────────────────────────────

    def sparql(
        self,
        query: str,
        fmt: str = "json",          # "json" | "turtle" | "jsonld"
        named_graph: Optional[str] = None
    ) -> Any:
        """
        POST /corpus/sparql — execute SPARQL query.

        Args:
            query:       SPARQL query string (SELECT / CONSTRUCT / ASK / DESCRIBE)
            fmt:         response format: "json", "turtle", "jsonld"
            named_graph: restrict query to a specific named graph IRI

        Returns:
            dict for SELECT/ASK (SPARQL JSON results)
            str  for CONSTRUCT/DESCRIBE with fmt="turtle"
        """
        payload = {"query": query, "format": fmt}
        if named_graph:
            payload["named_graph"] = named_graph

        headers = {"Accept": "application/sparql-results+json"}
        if fmt == "turtle":
            headers["Accept"] = "text/turtle"
        elif fmt == "jsonld":
            headers["Accept"] = "application/ld+json"

        r = self.session.post(
            f"{self.base_url}/corpus/sparql",
            json=payload,
            headers=headers,
            timeout=self.timeout
        )
        r.raise_for_status()

        if fmt in ("turtle",):
            return r.text
        return r.json()

    def export(self, fmt: str = "jsonld", output_path: Optional[str] = None) -> str:
        """GET /corpus/export — export full store."""
        r = self.session.get(
            f"{self.base_url}/corpus/export",
            params={"format": fmt},
            timeout=60
        )
        r.raise_for_status()
        content = r.text
        if output_path:
            Path(output_path).write_text(content, encoding="utf-8")
            print(f"  Exported to: {output_path}")
        return content

    # ── Convenience query helpers ──────────────────────────────────────────────

    def get_all_poclets(self) -> list[dict]:
        """Return all Poclet instances with their labels and domains."""
        q = """
        PREFIX m3:    <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#>
        PREFIX m3old: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#>
        PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX m1:    <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#>

        SELECT DISTINCT ?poclet ?label ?domain
        WHERE { GRAPH ?g {
            { ?poclet m3:ontologyType m3:Poclet }
            UNION
            { ?poclet m3old:ontologyType m3old:Poclet }
            OPTIONAL { ?poclet rdfs:label ?label }
            OPTIONAL { ?poclet m1:domain ?domain }
        } }
        ORDER BY ?label
        """
        result = self.sparql(q)
        rows = result.get("results", [])
        if not isinstance(rows, list): rows = rows.get("bindings", [])
        # Deduplicate by poclet IRI
        seen, deduped = set(), []
        for r in rows:
            iri = _val(r, "?poclet", _val(r, "poclet", ""))
            if iri.startswith("_:"): continue  # skip blank nodes
            if iri not in seen:
                seen.add(iri)
                deduped.append(r)
        return deduped

    def get_tscg_tools(self) -> list[dict]:
        """Return all TscgTool instances."""
        q = """
        PREFIX m3:    <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#>
        PREFIX m3old: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#>
        PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?tool ?label ?comment
        WHERE { GRAPH ?g {
            ?tool ?ontTypePred ?ontTypeVal .
            FILTER(CONTAINS(STR(?ontTypePred), "ontologyType"))
            FILTER(CONTAINS(STR(?ontTypeVal), "TscgTool"))
            OPTIONAL { ?tool rdfs:label ?label }
            OPTIONAL { ?tool rdfs:comment ?comment }
        } }
        """
        result = self.sparql(q)
        rows = result.get("results", [])
        if not isinstance(rows, list): rows = rows.get("bindings", [])
        seen, deduped = set(), []
        for r in rows:
            iri = _val(r, "?tool", _val(r, "tool", ""))
            if iri not in seen:
                seen.add(iri)
                deduped.append(r)
        return deduped

    def get_generic_concepts(self) -> list[dict]:
        """Return all M2 GenericConcepts with their structural formulas."""
        q = """
        PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?concept ?label ?formula
        WHERE { GRAPH <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/ontology/M2_GenericConcepts.jsonld> {
            ?concept rdfs:label ?label .
            OPTIONAL { ?concept m2:hasStructuralFormula ?formula }
        } }
        ORDER BY ?label
        LIMIT 100
        """
        result = self.sparql(q)
        rows = result.get("results", [])
        seen, deduped = set(), []
        for r in rows:
            iri = _val(r, "?concept", _val(r, "concept", ""))
            if iri not in seen:
                seen.add(iri)
                deduped.append(r)
        return deduped

    def get_scores(self, instance_iri: Optional[str] = None) -> list[dict]:
        """Return ASFID/REVOI scores for all (or a specific) instance."""
        filter_clause = f"FILTER(?instance = <{instance_iri}>)" if instance_iri else ""
        q = f"""
        PREFIX m0poclet: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?instance ?label ?A ?S ?F ?It ?D ?R ?E ?V ?O ?Im
        WHERE {{ GRAPH ?g {{
            ?instance m0poclet:scoreA ?A ;
                      m0poclet:scoreS ?S ;
                      m0poclet:scoreF ?F ;
                      m0poclet:scoreIt ?It ;
                      m0poclet:scoreD ?D ;
                      m0poclet:scoreR ?R ;
                      m0poclet:scoreE ?E ;
                      m0poclet:scoreV ?V ;
                      m0poclet:scoreO ?O ;
                      m0poclet:scoreIm ?Im .
            OPTIONAL {{ ?instance rdfs:label ?label }}
            {filter_clause}
        }} }}
        ORDER BY ?label
        """
        result = self.sparql(q)
        return result.get("results", [])

    def search_by_domain(self, domain: str) -> list[dict]:
        """Return all instances in a given domain (e.g. 'Biology', 'Physics')."""
        q = f"""
        PREFIX m1: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#>

        SELECT ?instance ?label ?type
        WHERE {{ GRAPH ?g {{
            ?instance m1:domain ?domain ;
                      m3:ontologyType ?type .
            OPTIONAL {{ ?instance rdfs:label ?label }}
            FILTER(CONTAINS(STR(?domain), "{domain}"))
        }} }}
        ORDER BY ?label
        """
        result = self.sparql(q)
        return result.get("results", [])

    def expand_iri(self, compact_iri: str) -> str:
        """GET /iri/expand — expand a compact TSCG IRI to full URI."""
        r = self.session.get(
            f"{self.base_url}/iri/expand",
            params={"iri": compact_iri},
            timeout=self.timeout
        )
        r.raise_for_status()
        return r.json().get("expanded", compact_iri)


# ── Demo ──────────────────────────────────────────────────────────────────────

def _val(row: dict, key: str, default: str = "?") -> str:
    """Extract value from SPARQL result row.
    Handles: direct string, {"value":...} dict, pyoxigraph quoted literals.
    Keys may be returned with or without leading "?" (e.g. "?label" or "label").
    """
    # Try key as-is, then with "?" prefix, then without "?" prefix
    v = row.get(key) or row.get(f"?{key}") or row.get(key.lstrip("?"))
    if v is None: return default
    if isinstance(v, dict): v = v.get("value", default)
    if not v: return default
    # pyoxigraph returns literals with surrounding quotes: '"value"' or '"value"@en'
    s = str(v)
    if s.startswith('"'):
        s = s.split('"')[1] if s.count('"') >= 2 else s.strip('"')
    # Strip IRI angle brackets: <http://...>
    if s.startswith('<') and s.endswith('>'):
        s = s[1:-1]
    return s if s else default


def demo(client: TscgAPIClient, ontology_dir: Optional[str] = None):
    """Run a complete demonstration of the TscgAPIClient capabilities."""

    sep = "─" * 55

    # ── 1. Health check ──────────────────────────────────────────────────────
    print(f"\n{sep}")
    print("1. HEALTH CHECK")
    print(sep)
    health = client.health()
    print(f"  Status   : {health.get('status', '?')}")
    print(f"  Uptime   : {health.get('uptime', '?')} s")
    print(f"  Graphs   : {health.get('graph_count', '?')}")
    print(f"  Triples  : {health.get('triple_count', '?')}")

    # ── 2. Load ontology (if dir provided) ──────────────────────────────────
    if ontology_dir:
        print(f"\n{sep}")
        print(f"2. LOADING ONTOLOGY from {ontology_dir}")
        print(sep)
        # Load M3 first, then M2, M1, M0
        for pattern in ["M3_*.jsonld", "M2_*.jsonld", "M1_*.jsonld", "M0_*.jsonld"]:
            results = client.load_dir(ontology_dir, pattern)
            if results:
                ok = sum(1 for r in results if r.get("status") == "ok")
                print(f"  {pattern}: {ok}/{len(results)} loaded")
        # Also load instances/ (poclets, tscg-tools, etc.) from repo root
        repo_root = str(Path(ontology_dir).parent)
        instances_dir = Path(repo_root) / "instances"
        if instances_dir.exists():
            results = client.load_dir(str(instances_dir), "**/*.jsonld")
            ok = sum(1 for r in results if r.get("status") == "ok")
            print(f"  instances/**/*.jsonld: {ok}/{len(results)} loaded")

    # ── 3. List graphs ───────────────────────────────────────────────────────
    print(f"\n{sep}")
    print("3. LOADED NAMED GRAPHS")
    print(sep)
    graphs = client.list_graphs()
    for g in graphs[:10]:  # Show first 10
        name = g.get("name", g.get("iri","?")).split("/")[-1].rstrip(">")
        print(f"  {name:50s}")
    if len(graphs) > 10:
        print(f"  ... and {len(graphs) - 10} more")

    # ── 4. List by layer ─────────────────────────────────────────────────────
    print(f"\n{sep}")
    print("4. GRAPHS BY LAYER")
    print(sep)
    try:
        layers = client.list_layers()
        for layer, count in layers.items():
            print(f"  {layer:6s}: {count} graph(s)")
    except Exception:
        print("  (endpoint not available)")

    # ── 5. SPARQL — list all Poclets ─────────────────────────────────────────
    print(f"\n{sep}")
    print("5. SPARQL — All Poclets")
    print(sep)
    poclets = client.get_all_poclets()
    for p in poclets[:8]:
        label = _val(p, "label", "")
        if not label or label == "?":
            iri = _val(p, "poclet", "")
            label = iri.split("#")[-1].split("/")[-1] or "?"
        domain = _val(p, "domain", "?")
        print(f"  {label:30s} [{domain}]")
    print(f"  Total: {len(poclets)} poclets")

    # ── 6. SPARQL — list TscgTools ───────────────────────────────────────────
    print(f"\n{sep}")
    print("6. SPARQL — TscgTools")
    print(sep)
    tools = client.get_tscg_tools()
    for t in tools:
        label = _val(t, "label", "?")
        print(f"  {label}")

    # ── 7. SPARQL — GenericConcepts with formulas ────────────────────────────
    print(f"\n{sep}")
    print("7. SPARQL — M2 GenericConcepts (first 5)")
    print(sep)
    concepts = client.get_generic_concepts()
    for c in concepts[:5]:
        label   = _val(c, "label", "?")
        formula = _val(c, "formula", "—")
        print(f"  {label:25s} {formula}")
    print(f"  Total: {len(concepts)} GenericConcepts")

    # ── 8. SPARQL — Scores for all instances ────────────────────────────────
    print(f"\n{sep}")
    print("8. SPARQL — ASFID/REVOI Scores (top 5 by A_score)")
    print(sep)
    scores = client.get_scores()
    def _to_float(row, key):
        try: return float(_val(row, key, "0"))
        except (ValueError, TypeError): return 0.0

    # Filter to rows with numeric A score, then sort
    scores_numeric = [s for s in scores if _to_float(s, "A") > 0.0]
    scores_sorted  = sorted(scores_numeric, key=lambda x: _to_float(x, "A"), reverse=True)
    print(f"  {'Instance':30s} {'A':5s} {'S':5s} {'F':5s} {'It':5s} {'D':5s}")
    for s in scores_sorted[:5]:
        label = _val(s, "label", _val(s, "instance", "?").split("/")[-1])
        vals  = [round(_to_float(s, k), 2) for k in ["A","S","F","It","D"]]
        print(f"  {label[:30]:30s} {vals[0]:5.2f} {vals[1]:5.2f} {vals[2]:5.2f} {vals[3]:5.2f} {vals[4]:5.2f}")

    # ── 9. Search by domain ──────────────────────────────────────────────────
    print(f"\n{sep}")
    print("9. SEARCH — Instances in domain 'Biology'")
    print(sep)
    bio = client.search_by_domain("Biology")
    for b in bio:
        label = _val(b, "label", "?")
        itype = _val(b, "type", "?").split("#")[-1]
        print(f"  {label:30s} [{itype}]")

    # ── 10. Raw SPARQL — custom query ────────────────────────────────────────
    print(f"\n{sep}")
    print("10. RAW SPARQL — Instances with δ₁ (epistemicGap)")
    print(sep)
    q = """
    PREFIX m0: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?inst ?label ?gap ?spectral
    WHERE { GRAPH ?g {
        ?inst ?epistemicPred ?gap .
        FILTER(CONTAINS(STR(?epistemicPred), "epistemicGap"))
        FILTER(datatype(?gap) = <http://www.w3.org/2001/XMLSchema#float> ||
               datatype(?gap) = <http://www.w3.org/2001/XMLSchema#double>)
        OPTIONAL { ?inst rdfs:label ?label }
        OPTIONAL { ?inst ?spectralPred ?spectral .
                   FILTER(CONTAINS(STR(?spectralPred), "spectralClass")) }
    } }
    ORDER BY ASC(?gap)
    LIMIT 8
    """
    result = client.sparql(q)
    rows = result.get("results", [])
    print(f"  {'Label':30s} {'δ₁':8s} {'SpectralClass'}")
    for row in rows:
        label = _val(row, "label", "")
        if not label or label == "?":
            iri = _val(row, "inst", "")
            label = iri.split("#")[-1].split("/")[-1] or "?"
        try: gap = float(_val(row, "gap", "0"))
        except: gap = 0.0
        spectral = _val(row, "spectral", "—")
        print(f"  {label[:30]:30s} {gap:8.4f} {spectral}")

    print(f"\n{'═' * 55}")
    print("  Demo complete ✅")
    print(f"{'═' * 55}\n")


# ── CLI wrapper examples ──────────────────────────────────────────────────────

def show_cli_usage():
    """Print CLI controller usage examples."""
    print("""
─────────────────────────────────────────────────────
CLI Controller (tscg_api_server.py) — Usage Examples
─────────────────────────────────────────────────────

# Start server (default: localhost:8000)
python tscg_api_server.py start

# Start with custom options
python tscg_api_server.py start \\
    --host 0.0.0.0 \\
    --port 9000 \\
    --store-path ./tscg_store.oxg \\
    --ontology-dir ./ontology

# Check server status
python tscg_api_server.py status

# Trigger hot-reload (re-parse all JSON-LD files)
python tscg_api_server.py reload

# Restart (stop + rebuild store + start)
python tscg_api_server.py restart

# Stop server
python tscg_api_server.py stop

# Export full store to JSON-LD
python tscg_api_server.py export --format jsonld --output tscg_export.jsonld

─────────────────────────────────────────────────────
Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
─────────────────────────────────────────────────────
""")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TscgOntologyAPIServer — Python client example"
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--ontology-dir", default=None,
        help="Path to ontology/ directory to load on startup")
    parser.add_argument("--cli-help", action="store_true",
        help="Show CLI controller usage examples")
    args = parser.parse_args()

    if args.cli_help:
        show_cli_usage()
        sys.exit(0)

    client = TscgAPIClient(host=args.host, port=args.port)

    print(f"\nConnecting to TscgOntologyAPIServer at {client.base_url} ...")

    if not client.is_running():
        print(f"❌ Server not reachable at {client.base_url}")
        print("   Start it with: python tscg_api_server.py start")
        sys.exit(1)

    print("✅ Connected\n")

    demo(client, ontology_dir=args.ontology_dir)
