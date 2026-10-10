#!/usr/bin/env bash
# install.sh — install the Claude Code Bootcamp Skills Pack.
#
# Usage:
#   ./install.sh project <path> [--with-agents] [--with-hooks] [--force] [--dry-run]
#   ./install.sh user           [--with-agents] [--with-hooks] [--force] [--dry-run]
#
#   project <path>  copy into <path>/.claude/{skills,agents,hooks}
#   user            copy into ~/.claude/{skills,agents,hooks} (all your projects)
#   --with-agents   also copy agents/*.md (security-reviewer, test-verifier)
#   --with-hooks    also copy hooks/*.sh and print the settings.json snippet
#   --force         overwrite existing files that differ from the pack
#   --dry-run       show what would happen; change nothing
#
# Safe to re-run: identical files are skipped. If any destination file exists
# with different content, nothing is copied unless you pass --force.
# This script never edits settings.json; it prints the snippet for you to paste.

set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-1}"
}

[ $# -ge 1 ] || usage 1

MODE="$1"; shift
TARGET_ROOT=""
case "$MODE" in
  project)
    [ $# -ge 1 ] && [ "${1#--}" = "$1" ] || { echo "error: 'project' needs a path, e.g. ./install.sh project ~/src/shipyard" >&2; exit 1; }
    [ -d "$1" ] || { echo "error: project path '$1' does not exist" >&2; exit 1; }
    TARGET_ROOT="$(cd "$1" && pwd)/.claude"
    shift
    ;;
  user)
    TARGET_ROOT="${HOME}/.claude"
    ;;
  -h|--help|help)
    usage 0
    ;;
  *)
    echo "error: unknown mode '$MODE' (expected 'project' or 'user')" >&2
    usage 1
    ;;
esac

WITH_AGENTS=0; WITH_HOOKS=0; FORCE=0; DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --with-agents) WITH_AGENTS=1 ;;
    --with-hooks)  WITH_HOOKS=1 ;;
    --force)       FORCE=1 ;;
    --dry-run)     DRY_RUN=1 ;;
    -h|--help)     usage 0 ;;
    *) echo "error: unknown option '$arg'" >&2; usage 1 ;;
  esac
done

# Build the list of "source<TAB>destination" pairs.
PLAN="$(mktemp)"
trap 'rm -f "$PLAN"' EXIT

( cd "$PACK_DIR/skills" && find . -type f ! -name '.DS_Store' | LC_ALL=C sort ) | while IFS= read -r rel; do
  rel="${rel#./}"
  printf '%s\t%s\n' "$PACK_DIR/skills/$rel" "$TARGET_ROOT/skills/$rel"
done >> "$PLAN"

if [ "$WITH_AGENTS" -eq 1 ]; then
  for f in "$PACK_DIR"/agents/*.md; do
    printf '%s\t%s\n' "$f" "$TARGET_ROOT/agents/$(basename "$f")"
  done >> "$PLAN"
fi

if [ "$WITH_HOOKS" -eq 1 ]; then
  for f in "$PACK_DIR"/hooks/*.sh; do
    printf '%s\t%s\n' "$f" "$TARGET_ROOT/hooks/$(basename "$f")"
  done >> "$PLAN"
fi

# Pass 1: detect conflicts.
conflicts=0
while IFS="$(printf '\t')" read -r src dst; do
  if [ -e "$dst" ] && ! cmp -s "$src" "$dst"; then
    conflicts=$((conflicts + 1))
    echo "conflict: $dst differs from the pack version" >&2
  fi
done < "$PLAN"

if [ "$conflicts" -gt 0 ] && [ "$FORCE" -eq 0 ]; then
  echo "" >&2
  echo "Nothing was copied: $conflicts file(s) already exist with different content." >&2
  echo "Review them (diff -u <pack file> <installed file>), then re-run with --force to overwrite." >&2
  exit 1
fi

# Pass 2: copy.
copied=0; unchanged=0; overwritten=0
while IFS="$(printf '\t')" read -r src dst; do
  if [ -e "$dst" ] && cmp -s "$src" "$dst"; then
    unchanged=$((unchanged + 1))
    continue
  fi
  action="copy"
  [ -e "$dst" ] && action="overwrite"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $action $dst"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    case "$dst" in *.sh) chmod +x "$dst" ;; esac
    echo "$action $dst"
  fi
  if [ "$action" = "overwrite" ]; then overwritten=$((overwritten + 1)); else copied=$((copied + 1)); fi
done < "$PLAN"

echo ""
echo "Target:   $TARGET_ROOT"
echo "Copied:   $copied   Overwritten: $overwritten   Unchanged: $unchanged"
[ "$DRY_RUN" -eq 1 ] && echo "(dry run: no files were written)"

echo ""
echo "Skills installed: $(ls "$PACK_DIR/skills" | tr '\n' ' ')"
echo "Try one in Claude Code:  /change-review   or   /feature-brief add an --owner filter"
echo "Note: the pack's security-review skill replaces Claude Code's bundled /security-review command; see README > Caveats."

if [ "$WITH_HOOKS" -eq 1 ]; then
  echo ""
  echo "Hooks copied but NOT active yet. Add this to the \"hooks\" key of"
  if [ "$MODE" = "project" ]; then
    echo "  $(dirname "$TARGET_ROOT")/.claude/settings.json"
    echo "(merge with any existing \"hooks\" entries):"
    echo ""
    cat "$PACK_DIR/hooks/settings-snippet.json"
  else
    echo "  ~/.claude/settings.json"
    echo "(merge with any existing \"hooks\" entries):"
    echo ""
    sed 's#"\$CLAUDE_PROJECT_DIR\\"/\.claude/hooks#"$HOME\\"/.claude/hooks#g' "$PACK_DIR/hooks/settings-snippet.json"
  fi
  echo ""
  echo "Then run /hooks in Claude Code to confirm they are registered."
  echo "Requirements: bash and python3 (jq is not needed)."
fi
