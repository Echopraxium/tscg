# TSCG Session HandOver — 2026-09-27

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: resume cold in a fresh session. Follows head-over-memory — every
volatile fact below (SHAs, counts, file structure) must be re-verified against
HEAD; this doc is a map, not an authority.
**Where to put this**: commit under a worksite folder
(e.g. `ontology/docs/_01_Worksite/WS-0/Next_Conversation_2026-09-27/`) and/or drop
into Project Knowledge so the next session auto-loads it.

---

## 1. TL;DR — where we are

Two things shipped to `origin/main` this session (direct push, fast-forward —
`main` at `83b9ad5` **at handover time**, re-check with `git log`):
1. **Archive purge** — every `_archives/` folder removed (8 commits, groups A–H).
   Verified: `git ls-files | findstr "_archives/"` returns nothing; live sims
   preserved (`FireTriangle/static/M0_FireTriangle.html` still there).
2. **Gallery-folder rename** — `cli_tools/generate_index-html/` →
   `cli_tools/regenerate_simulation_gallery/` (git-detected renames, 100%).

Security: the leaked Gemini API key (`.api_key`, was in `src/tscg/rag/_archives/`)
was **revoked** on 2026-09-27. It survives in git history but is now dead → history
purge (filter-repo/BFG) is optional cleanup, not a risk.

The **Compendium** (audience-filtered navigable site over the whole toolkit) was
designed and prototyped this session but is **not yet deployed**. Live MVP preview:
https://claude.ai/artifact/K87SSsUzbZnVgpGreoh9FB

## 2. IMMEDIATE next step — regenerate the File Tree

`docs/reboot-kit/TSCG_FileTree.md` is the last resident doc still describing the
OLD structure (old gallery name, and it predates the archive purge + new
`cli_tools/compendium/`). Regenerate, don't hand-edit:
```
python tscg_generate_filetree.py
```
Then reload it into Project Knowledge. Sanity-check afterwards:
`git grep -n "generate_index-html"` should return only historical snapshots
(WS-0) and recorded debug logs — no living doc.

## 3. Deliverables produced this session — TO DEPOSIT in the repo

These were produced as files/artifacts but are **not yet committed** (verify with
`git status` first — some doc fixes below may already be in):

| File | Target repo path | What it is |
|---|---|---|
| `pages.yml` | `.github/workflows/pages.yml` | GitHub Action: build + deploy Compendium |
| `build_compendium.py` | `cli_tools/compendium/` | READ-ONLY site builder (data + sims copy + gallery) |
| `annotate_compendium.py` | `cli_tools/compendium/` | writes `@tscg` blocks (LOCAL step, not CI) |
| `compendium_template.html` | `cli_tools/compendium/` | the page shell (`@@DATA@@` placeholder) |
| `worksite.yaml` | `ontology/docs/_01_Worksite/WS-12/` | WS-12: Audience-facet population campaign |
| `LayerCake_Models_The_Kit.md` | `docs/CoreHypotheses/` | **Core Hypothesis #4** (layer cake models the kit, not the world) |
| `Housekeeping_ArchivePurge_2026-09-27.md` | `_02_housekeeping/2026_09_27/` | trace of the purge + the .api_key incident |
| `Compendium_Generator_DesignNote.md` | `cli_tools/compendium/` (optional) | design rationale |

Also verify these earlier doc fixes are committed (they may already be on main):
CLAUDE.md gallery-path lines (30, 493), README.md, and the hardened `.gitignore`
(`*.api_key`, `.pytest_cache/`, `**/_archives/`).

## 4. Compendium deployment — the next big block (not started)

1. Deposit the `cli_tools/compendium/` files + `pages.yml` (§3).
2. Test the build LOCALLY first (guaranteed green if it passes):
   ```
   python cli_tools/compendium/build_compendium.py . \
     --template cli_tools/compendium/compendium_template.html \
     --gallery-script cli_tools/regenerate_simulation_gallery/generate_index.js \
     --site-url "https://echopraxium.github.io/tscg" --out dist
   ```
   Expect `dist/index.html` + `dist/instances/simulation_gallery.html`.
3. GitHub: Settings → Pages → Source = **GitHub Actions**, then push.
   Note: `main` has a branch-protection rule (PRs expected) — either use a PR or
   bypass as owner.
4. Once live, the "▸ Play" links and gallery become real (they point to Pages URLs).

## 5. Locked design decisions (do NOT relitigate)

- **Compendium = the site**; simulation gallery kept in its current form,
  output to `instances/simulation_gallery.html`, reachable via a shortcut button.
- **Audience lens** (closed set, from `m3:Audience` facet): default **KitUser**,
  choice remembered. Level meanings (Michel's wording):
  KitUser = *experiment & play with assembled kits*;
  KitCrafter = *design & assemble kits*;
  KitArchitect = *design architecture, workflows & tools*.
- **Structure by subject** + run-mode badge **Playable / Local / Under construction**.
  Playability = has a browser-runnable HTML (decoupled from audience, so the
  gallery/deploy copies every runnable sim; the lens controls visibility only).
- **"Understand the kit"** section (KitUser): desiloification → 3 pillars
  (Esperanto / Stereopsis after Korzybski / LEGO-Technic-kit) → concept intros
  (ASFID·REVOI·TKSL, the 4-layer cake, key words instance/poclet/workflow) →
  **"Under the hood"** (light epistemology, honest hypotheses) → full essays.
- Writing discipline: **anti-overfitting** (several/can, never every/all) and
  **anti-"it's easy"** (real learning cost named, not hidden).
- Layer-cake raw internals (M3/M2/M1 jsonld, SHACL) **hidden from KitUser**.

## 6. Deferred chantiers (tracked, not urgent)

- `_02_housekeeping/2026_09_23/Cleanup_Chantier_2026-09-23.md`:
  `m1core`→`m1` vestige, `cli_tools/` vs `ontology/cli-tools/` duplication,
  `ORIVE`→`REVOI` in `poclet_terminology.md`.
- CLAUDE.md still references dead `M3_GenesisSpace.jsonld` (README is already correct).
- WS-12 Audience-facet campaign (only 1/55 instances currently carry the facet;
  wiki filter leans on type-defaults until it fills).
- Optional: purge `.api_key` from git history.

## 7. Authority reminder

The Compendium reads its classification **from HEAD** — the `@tscg` blocks in files
+ the `m3:Audience` facet on M0 instances — never from a stored copy. Same rule for
resuming: re-read HEAD / the resident corpus before asserting any framework fact.
