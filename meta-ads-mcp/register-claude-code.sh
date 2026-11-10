#!/usr/bin/env bash
# Register the Meta Ads remote MCP server with Claude Code.
#
# Source for the URL: https://www.facebook.com/business/help/1456422242197840
#   "The remote MCP server URL for our ads MCP server across all currently
#    supported AI agents is: https://mcp.facebook.com/ads"
#
# Auth: OAuth. The first MCP tool call from Claude Code will pop a browser
# window for Meta login + consent. The bearer token is stored locally by
# Claude Code; revoke at any time via Meta Business Suite > Connected Apps.
#
# Usage:
#   bash register-claude-code.sh           # default: user scope (all projects)
#   SCOPE=local bash register-claude-code.sh   # current project only
#   SCOPE=project bash register-claude-code.sh # writes to ./.mcp.json (committable)

set -euo pipefail

NAME="${NAME:-meta-ads}"
URL="${URL:-https://mcp.facebook.com/ads}"
SCOPE="${SCOPE:-user}"

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found in PATH. Install Claude Code first." >&2
  exit 1
fi

echo "Registering MCP server '$NAME' -> $URL (scope=$SCOPE)"
claude mcp add --transport http --scope "$SCOPE" "$NAME" "$URL"

echo
echo "Registered. Verify with: claude mcp get $NAME"
echo "First tool call from Claude Code will trigger Meta OAuth in your browser."
echo "To remove: claude mcp remove $NAME"
