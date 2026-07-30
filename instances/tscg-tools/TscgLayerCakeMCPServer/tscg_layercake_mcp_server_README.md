# TscgLayerCakeMCPServer

A **local-first MCP server** that exposes the TSCG ontology corpus to an MCP
client (e.g. Claude Desktop) as a small set of task-shaped tools. The client
pulls only what a query needs, instead of loading the whole corpus into its
context window.

**Author:** Echopraxium with the collaboration of Claude AI

---

## Why this design

- **Stateless on the corpus.** By default every read fetches **live from git
  HEAD** (`raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`). Nothing
  is stored on disk, so nothing can go stale relative to HEAD. "Run it locally"
  is therefore a valid distribution model — every user runs the same server
  against the same authoritative source, with no central hosting bill.
- **Two sources.** `head` (authoritative, default) or `local` (your working
  copy while editing — set `TSCG_LOCAL_REPO`).
- **Task-shaped over raw SPARQL.** `get_file` / `search` / `get_concept` /
  `list_*` / `resolve_iri` keep each call short and reliable. `sparql` is an
  optional last-resort escape hatch.

---

## Tools

| Tool | Purpose |
|------|---------|
| `tscg_get_file(path, source)` | Raw text of one file, path relative to `ontology/` (e.g. `M1_extensions/biology/M1_Biology.jsonld`). |
| `tscg_search(query, layer, max_results, source)` | Full-text search → **paths + snippets**, never whole files. Optional `layer` filter `M0..M3`. |
| `tscg_get_concept(name, source)` | Compact record for one M2 GenericConcept (formula, definition, family, examples). |
| `tscg_list_extensions(source)` | The M1 domain extension files. |
| `tscg_list_poclets(source)` | The M0 instance / poclet files. |
| `tscg_resolve_iri(compact, source)` | Expand a compact IRI (`m3:eagle_eye:Attractor`, `m1:extension:biology:CellularCommunication`) to a full URI. |
| `tscg_sparql(query, graphs, source)` | **Optional** SPARQL over named JSON-LD files. Prefer the tools above. |

---

## Install

Requires **Python 3.10+**.

```bash
pip install mcp          # the MCP SDK (FastMCP)
pip install rdflib       # OPTIONAL — only for the tscg_sparql tool
```

Verify the core works before wiring it into any client (no client needed):

```bash
python tscg_layercake_mcp_server.py --selftest
```

---

## Corpus listing: the manifest

Listing/searching needs to know which files exist. The server resolves the file
list in this order:

1. **`ontology/_manifest.json`** on the raw CDN — a committed JSON array of
   ontology-relative paths. Not rate-limited, zero config, works everywhere.
   **Recommended.**
2. **GitHub tree API** — live, but limited to 60 requests/hour when
   unauthenticated (set `GITHUB_TOKEN` to lift it).

Generate the manifest once from your working copy and commit it:

```bash
export TSCG_LOCAL_REPO=/path/to/tscg          # repo root (contains ontology/)
python tscg_layercake_mcp_server.py --emit-manifest > /path/to/tscg/ontology/_manifest.json
git add ontology/_manifest.json && git commit -m "Add corpus manifest for MCP server"
```

Regenerate whenever files are added or removed. (`get_file`, `get_concept` and
`resolve_iri` do **not** need the manifest — only listing and search do.)

---

## Claude Desktop configuration

Edit the Claude Desktop MCP config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "tscg-layercake": {
      "command": "python3",
      "args": ["/absolute/path/to/tscg_layercake_mcp_server.py"],
      "env": {
        "TSCG_SOURCE": "head"
      }
    }
  }
}
```

Restart Claude Desktop. The `tscg_*` tools then appear and are called on demand.

To query your **local working copy** instead of HEAD, set the source per call
(`source: "local"`) or switch the default:

```json
"env": {
  "TSCG_SOURCE": "local",
  "TSCG_LOCAL_REPO": "/path/to/tscg"
}
```

> **Note:** stdio MCP (this server) works with the **desktop** client only.
> Mobile clients require a *remote* (hosted, URL-based) MCP server — a later
> step if/when hosting is available. The code is written so the same core
> functions can back an HTTP transport without change.

---

## Environment variables

| Variable | Default | Meaning |
|----------|---------|---------|
| `TSCG_SOURCE` | `head` | `head` (live from GitHub) or `local`. |
| `TSCG_LOCAL_REPO` | *(empty)* | Repo root, required when source is `local`. |
| `TSCG_REF` | `main` | Git ref to read from. |
| `GITHUB_TOKEN` | *(empty)* | Optional; lifts the GitHub API rate limit for tree listing. |

---

## Status

Prototype. Validated against live HEAD: file fetch + JSON-LD parse,
`get_concept` (returns the real structural-grammar formula, e.g.
`St × It × A | R`), `resolve_iri` (all prefix strategies), and the
listing/search filtering + ranking logic. To be modelled as an `m3:TscgTool`
poclet (`M0_TscgLayerCakeMCPServer.jsonld`) in a following step.
