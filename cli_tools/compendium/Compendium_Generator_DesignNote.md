# TSCG Compendium — generator design note

**Status:** draft for review (KitArchitect) · **Author:** Echopraxium with the collaboration of Claude AI

## 1. What it is, and the one rule

The Compendium is a **generated, read-mostly** view of the whole toolkit — not a
hand-edited wiki. Its purpose: turn "1764 files nobody can hold in their head"
into a map navigable by *rubric* and filtered by *audience*, so a newcomer meets
only what concerns them.

The governing rule is head-over-memory applied to the interface: **the Compendium
stores no framework facts of its own.** It renders what already lives on HEAD —
the `@tscg` annotation blocks in the files, and the `m3:Audience` facet on the
instances. Regenerate and it is fresh; there is no second copy to rot.

## 2. Two axes (already in the files)

- **section** — the navigation, derived from each file's `tscg-kind`
  (+ path). Michel's rubrics: *Projets en cours · Instances & simulations ·
  Outils Gate & tooling · Couches M3–M0 · Épistémologie · Guides & modèles*.
- **audience** — the filter, the closed set `KitUser / KitCrafter / KitArchitect`.
  For files it comes from the `tscg-audience` annotation; for instances from the
  `m3:hasFacetValue` facet (WS-12), with the type-default as fallback.

An entry is visible to a reader when the reader's level is in the entry's
`audience`. KitUser therefore sees the fewest entries, KitArchitect the most —
that offset *is* the progressive disclosure.

## 3. Data flow

```
   HEAD (the repo)
     ├─ 647 files carrying @tscg blocks   ─┐
     └─ M0 instances carrying m3:Audience ─┤
                                           ▼
            build step  →  compendium_data.json   (path, title, section, kind, audience[], status)
                                           ▼
            static site (index.html + data)  →  GitHub Pages  →  public URL
```

The build step is two small scripts, both already prototyped:
`annotate_compendium.py` (writes/refreshes the `@tscg` blocks) and the
data-collector (walks the blocks + facets → `compendium_data.json`).

## 4. Page structure

- **Header / hero:** the audience *lens* — a three-level control (KitUser →
  KitCrafter → KitArchitect) with a live count ("KitUser voit 238 des 690").
  The lens is the hero because progressive disclosure is the core idea.
- **Rubric rail:** the six sections as filters, each with a live count that
  responds to the lens.
- **Search:** by title / path.
- **Entry rows:** title (links to the file on HEAD), path, `kind` + `status`,
  and a compact who-can-see indicator. Not identical cards — a scannable list.

## 5. Build & deployment

- **Static hosting, dynamic behavior.** The site is plain HTML/CSS/JS served from
  **GitHub Pages** — one public URL, zero install for the KitUser (the whole
  democratization point). The interactivity (filter, lens, search) is client-side
  JS; no server, no runtime fetch of HEAD.
- **Freshness by rebuild, not by runtime.** A **GitHub Action** on push
  regenerates `compendium_data.json` and redeploys. Always fresh, never a stale
  copy — the same discipline as the WS-12 `AUD-template` lot (fix it at the
  source, never re-do by hand).
- The repo already has the seed: `index.html`, `styles.css`, `.nojekyll`,
  `cli_tools/generate_index-html/`, and `echopraxium.github.io/tscg`.

## 6. MVP scope vs deferred

**In the MVP (this pass):** the real 690-entry index, the audience lens, the six
rubrics, search, links to HEAD, light/dark. It reads the actual classification —
it is browsable today.

**Deferred (next passes):**
- Human titles + one-line descriptions per entry (read from each file's README /
  first heading), replacing the filename-derived titles.
- Embedding the playable simulations inline for the KitUser view.
- Vulgarized renderings of the epistemology essays for KitUser (the file stays
  architect-level; the User view is a generated summary).
- The GitHub Action wiring.

## 7. Open questions for the KitArchitect

1. Rubric names — keep these six, or split/rename (e.g. a distinct
   "Simulations" rubric separate from "Instances")?
2. Default audience on first load — KitUser (most inviting) confirmed?
3. Do KitArchitect-only entries stay hidden from lower levels, or shown greyed
   ("exists, not for you yet")?
