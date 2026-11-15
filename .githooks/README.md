# .githooks — local checks for this repository

**Author:** Echopraxium with the collaboration of Claude AI

Activate once per clone:

    git config core.hooksPath .githooks

| Hook | Runs on | Refuses |
|---|---|---|
| `commit-msg` | `git commit` | a message with a Claude attribution trailer (`Co-Authored-By: Claude…`, `Claude-Session: …`) |
| `applypatch-msg` | `git am` | the same, in a patch: `git am` stops before the commit |
| `pre-commit` | `git commit` | an author that is Claude (`noreply@anthropic.com`) or a noreply address GitHub cannot link to Michel |
| `pre-applypatch` | `git am` | the same author check, on the patch's author |

Message hooks call `check-trailers.sh`, author hooks `check-author.sh`. Rule: CLAUDE.md, Authorship ("Echopraxium with the
collaboration of Claude AI"). The same rule is checked on every push by the `checks` job of
`.github/workflows/pages.yml`, over the whole history of `main`.
