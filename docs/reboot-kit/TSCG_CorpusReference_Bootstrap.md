# TSCG — Corpus Reference (Bootstrap)

> Minimal orientation file. If this is the only TSCG document in context, it is
> enough to avoid silent corruption. For anything operational (paths, tools,
> procedures), see **`TSCG_CorpusReference.md`** (the complete index/router).

---

## What TSCG is

**TSCG (Transdisciplinary System Construction Game)** — a transdisciplinary,
systemic modeling *construction kit* (LEGO Technic metaphor, not a universal
theory). Organized as a 4-layer "Layer Cake" of ontologies:

```
M3  Structural Grammar   (M3_GenesisGrammar.jsonld)
M2  GenericConcepts      (M2_GenericConcepts.jsonld)
M1  Domain Adaptation    (M1_CoreConcepts.jsonld + M1_extensions/)
M0  Instances            (poclets, TscgTools, systemic frameworks, SSGs)
```

---

## Hard invariants (must never drift)

**Bicephalous basis.**
`ASFID` (Territory / Eagle Eye — what a system *is*) = Attractor, Structure,
Flow, Information, Dynamics.
`REVOI` (Map / Sphinx Eye — how a system is *known*) = **R**epresentability,
Evolvability, Verifiability, Observability, Interoperability.
**R is Representability — NEVER Reproducibility.**

**Notation (2026-07-06, supersedes all prior).**
The operator `⊗` must **never** appear in any TSCG file or formula.
Structural formulas use only:
- `×` — Territory / ASFID product (monoid **Gt**)
- `+` — Map / REVOI sum (monoid **Gm**)
- `|` — Stereopsis (monoid **Gs**; its Base16 alphabet is defined in
  `M3_BicephalousPerspective.jsonld` — read it from HEAD, do not enumerate here)

Atom-level subscripts disambiguate: `St`/`Ss` (Structure vs Symbol),
`It`/`Im` (Information vs Interoperability).

**File conventions (all `.jsonld`).**
- `dcterms:creator` = `"Echopraxium with the collaboration of Claude AI"`
- Generated files in **English**; conversation in **French**
- Base URI: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`
  (source sometimes writes `ttps` — always read `https`)
- Short IRIs via `"@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"`
- M1 extension IRIs in M0 files: `M1_extensions/biology/M1_Biology.jsonld` style
- `m2:changelog`: keep the **3 most recent** entries — everywhere **except M3**
  files (up to **7**, rollback safety; documented in the M3 SHACL shape — not a violation)

**M0 namespace.**
- `m0:` MUST resolve to `M0_Common.jsonld#` (shared, joinable)
- Local concepts use `m0.<instance>:` — **DOT** separator
  (the colon form `m0:instance:` crashes the pyld parser — empirically proven)

**Live vs dead / structure.**
- `M3_GenesisGrammar.jsonld` is the **live** M3 file.
  `M3_GenesisSpace.jsonld` is a **dead vestige** — do not use.
- `instances/` replaces the old `system-models/`. Correct roots:
  `instances/{poclets, tscg-tools, transdisclet, systemic-frameworks, symbolic-system-grammars}/`

---

## HEAD is the only authority

`git show HEAD:<file>` is the sole source of truth for any live file
(`.jsonld`, `.ttl`, code). **Never** trust stale snapshots, session uploads,
or project-knowledge copies for current structure.

- Refresh the clone: `git fetch --depth 1 origin main && git reset --hard origin/main`
- Raw CDN is **unrestricted**: `https://raw.githubusercontent.com/Echopraxium/tscg/main/...`
- The GitHub **API is rate-limited** — prefer the raw CDN; use `git show HEAD`
  (not the API) to read the exact committed content.

Corpus `.md` files hold durable *rationale* only. When rationale and a live
file disagree on a structural fact, **the live file on HEAD wins.**
