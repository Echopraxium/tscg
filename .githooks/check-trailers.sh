#!/bin/sh
# TSCG — no Claude attribution trailer in a commit message.
# CLAUDE.md (Authorship): "Echopraxium with the collaboration of Claude AI"; Claude is not a
# co-author. Called by commit-msg (git commit) and applypatch-msg (git am) with the message file.
if grep -qiE '^(Co-Authored-By:.*(claude|anthropic)|Claude-Session:)' "$1"; then
  echo "TSCG: this commit message carries a Claude attribution trailer:" >&2
  grep -iE '^(Co-Authored-By:.*(claude|anthropic)|Claude-Session:)' "$1" | sed 's/^/    /' >&2
  echo "CLAUDE.md, Authorship: remove these lines (git am --abort, or edit the message)." >&2
  exit 1
fi
exit 0
