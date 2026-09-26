# Housekeeping — Archive purge, 2026-09-27

**Author**: Echopraxium with the collaboration of Claude AI
**Nature**: trace of a completed housekeeping operation. Every figure below was
read from `git log` / `git show` on `origin/main` when this note was written. The
commits are the authority; this note only reads them back.

---

## 1. What was done

Every `_archives/` folder tracked in the repo was removed from `main`, in
8 commits, one per zone (groups A–H). They were pushed directly, fast-forward,
on the night of 2026-09-26/27.

| Group | Commit | Zone | Files | Lines removed |
|---|---|---|---:|---:|
| A | `fa118dd` | root `_archives/` (+ gallery-folder rename, see §3) | 10 deleted, 8 renamed | 3 840 |
| B | `da1a24d` | `docs/reboot-kit/_archives/` + `SmartPrompts/_archives/` (incl. dead `M3_GenesisSpace`) | 23 | 14 347 |
| C | `35050c3` | `docs/papers/**/_archives/` | 14 | 193 572 |
| D | `f645886` | `ontology/StructuralGrammar/` + `ontology/TSCG_InstanceGrammar/` `_archives/` | 23 | 5 457 |
| E | `343707b` | `instances/tscg-tools/_archives/` + `TscgOntologyExplorer/plugins/_archives/` (incl. a committed `.pytest_cache/`) | 46 | 6 252 |
| F | `89375cd` | `src/tscg/rag/_archives/` (incl. the leaked `.api_key`, see §2) | 13 | 2 580 |
| G | `ce8abb9` | instance `_archives/`: 13 poclets, 3 systemic frameworks, 1 symbolic system grammar | 112 | 77 712 |
| H | `83b9ad5` | stray `cli_tools/regenerate_simulation_gallery/_archives/` | 1 | 824 |

**Total**: 242 files deleted, about 305 000 lines. More than half of that is
group C, the old paper drafts.

**Checks after the purge**:
- `git ls-tree -r --name-only origin/main | grep -c "_archives/"` returns **0**.
- The live simulations are still there. For example,
  `instances/poclets/FireTriangle/static/M0_FireTriangle.html` is still tracked.
  Only the `_archives/` subfolders next to them were removed.
- Nothing is lost: every deleted file can still be recovered from history
  (`git show fa118dd^:<path>`, and so on).

## 2. Security incident — leaked `.api_key`

A Gemini API key file was tracked at
`src/tscg/rag/_archives/RAG-prev/.api_key`. Commit F removed it from `main`.
The commit message itself says the key had to be rotated separately.

- **Status**: Michel reported the key **revoked** on 2026-09-27. From that point
  the key is dead.
- **It is still in git history**, which removing a file never rewrites. Since
  the key is revoked, this is no longer a risk. A history rewrite
  (`git filter-repo` / BFG) is **optional cleanup** only. It rewrites every SHA,
  so do it only if there is a separate reason to.
- **Prevention**, `.gitignore` hardened in `f44c33d`: `*.api_key`, `.api_key`,
  `api_keys/`, `.pytest_cache/`, `**/_archives/`. With `**/_archives/` in
  place, a local archive folder can no longer be committed by accident.
  Cosmetic: `.pytest_cache/` now appears twice in `.gitignore` (lines 95 and 157).

## 3. Rename done alongside the purge

In commit A, git detected 8 renames at 100%:
`cli_tools/generate_index-html/` → `cli_tools/regenerate_simulation_gallery/`.
The references in living docs were then fixed:
- `CLAUDE.md` gallery commands and the underscore-prefix note, in `b0d0546`;
- `README.md` tree, in `b0d0546`;
- `docs/reboot-kit/TSCG_FileTree.md`, regenerated with `tscg_generate_filetree.py`.

Mentions of `generate_index-html` are still left in recorded debug logs under
`instances/tscg-tools/TscgPocletMiner/src/rag/` and `src/tscg/rag/`. Those are
historical records and are deliberately **not** rewritten.

## 4. Doctrine going forward

- **Archives live in git history, not in the tree.** To keep an old version,
  commit it before replacing it. Do not copy it into an `_archives/` folder.
- A local `_archives/` folder is fine as a scratch space. `.gitignore` now keeps
  it out of the repo.
- Secrets never go in the repo, archived or not.
