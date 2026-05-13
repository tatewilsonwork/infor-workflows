#!/usr/bin/env bash
# Resolve an INFOR template by filename and print its absolute path on stdout.
# Exits 1 with a message on stderr if the template is not found.
#
# Usage:
#   bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Comps Template.xlsx"
#
# Searches, in priority order:
#   1. $CLAUDE_PLUGIN_ROOT/templates         (set by Claude Code at runtime)
#   2. <script-dir>/../templates             (script's own plugin tree)
#   3. <repo-root>/infor-workflows/templates (dev clone, marketplace layout)
#   4. <repo-root>/templates                 (dev clone, flat layout)
#   5. $HOME/.claude/plugins/infor-workflows/templates       (macOS/Linux install)
#   6. $HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates  (Windows install)

set -u

TEMPLATE_NAME="${1:-}"
if [ -z "$TEMPLATE_NAME" ]; then
  echo "usage: find_template.sh <template-filename>" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"

CANDIDATES=()
[ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && CANDIDATES+=("$CLAUDE_PLUGIN_ROOT/templates")
CANDIDATES+=("$SCRIPT_DIR/../templates")
[ -n "$REPO_ROOT" ] && CANDIDATES+=("$REPO_ROOT/infor-workflows/templates" "$REPO_ROOT/templates")
CANDIDATES+=(
  "$HOME/.claude/plugins/infor-workflows/templates"
  "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates"
)

for dir in "${CANDIDATES[@]}"; do
  if [ -f "$dir/$TEMPLATE_NAME" ]; then
    # Resolve to absolute path for downstream cp robustness.
    (cd "$dir" && printf '%s/%s\n' "$(pwd)" "$TEMPLATE_NAME")
    exit 0
  fi
done

echo "ERROR: template '$TEMPLATE_NAME' not found in any known location." >&2
echo "Searched:" >&2
for dir in "${CANDIDATES[@]}"; do
  echo "  - $dir" >&2
done
exit 1
