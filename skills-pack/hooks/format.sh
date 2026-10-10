#!/usr/bin/env bash
# format.sh — optional PostToolUse formatter for Edit|Write.
#
# Formats the edited file ONLY if a formatter is already installed:
#   *.py                                   -> black   (if `black` is on PATH)
#   *.js *.mjs *.css *.html *.json *.md    -> prettier (if `prettier` is on PATH)
# Nothing is downloaded or installed (no npx, no pip). If no formatter is
# available, or the file is outside the project, this is a no-op.
#
# Always exits 0: formatting is a convenience, not a gate. Problems are reported
# on stderr so you can see them with Ctrl+O / verbose mode.

set -u

command -v python3 >/dev/null 2>&1 || exit 0

file="$(python3 -c '
import json, os, sys
try:
    event = json.load(sys.stdin)
except Exception:
    sys.exit(0)
root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
path = (event.get("tool_input") or {}).get("file_path") or ""
if path:
    full = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
    if full.startswith(root + os.sep) and os.path.isfile(full):
        print(full)
')"

[ -n "$file" ] || exit 0

case "$file" in
  *.py)
    if command -v black >/dev/null 2>&1; then
      black --quiet "$file" || echo "format.sh: black could not format $file" >&2
    fi
    ;;
  *.js|*.mjs|*.css|*.html|*.json|*.md)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write --log-level warn "$file" >/dev/null || echo "format.sh: prettier could not format $file" >&2
    fi
    ;;
esac

exit 0
