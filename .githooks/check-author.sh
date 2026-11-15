#!/bin/sh
# TSCG — Claude is never the author of a commit (CLAUDE.md, Authorship). Also refuses the
# noreply addresses that GitHub cannot link to Michel's account.
# Usage: check-author.sh "<Name> <email>"
case "$1" in
  *noreply@anthropic.com*|Claude\ \<*|*noreply@users.noreply.github.com*|*noreply@example.invalid*)
    echo "TSCG: commit author refused: $1" >&2
    echo "CLAUDE.md, Authorship: the author is Echopraxium <echopraxium@gmail.com>." >&2
    echo "git am: --abort, and ask for the patch to be authored Echopraxium <echopraxium@gmail.com>." >&2
    echo "git commit: git config user.name Echopraxium; git config user.email echopraxium@gmail.com" >&2
    exit 1 ;;
esac
exit 0
