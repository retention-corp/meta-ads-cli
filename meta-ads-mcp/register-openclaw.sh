#!/usr/bin/env bash
# Register the Meta Ads remote MCP server with OpenClaw.
#
# Source for the URL: https://www.facebook.com/business/help/1456422242197840
# OpenClaw stores MCP config at ~/.openclaw/openclaw.json (servers key).
# Auth: OAuth on first tool call (browser pop-up, Meta login + consent).
#
# Usage:
#   bash register-openclaw.sh
#
# Remove later with:
#   openclaw mcp unset meta-ads

set -euo pipefail

NAME="${NAME:-meta-ads}"
URL="${URL:-https://mcp.facebook.com/ads}"

if ! command -v openclaw >/dev/null 2>&1; then
  echo "openclaw CLI not found in PATH. Install OpenClaw first." >&2
  exit 1
fi

echo "Registering MCP server '$NAME' -> $URL in OpenClaw"
openclaw mcp set "$NAME" "{\"type\":\"http\",\"url\":\"$URL\"}"

echo
echo "Verify: openclaw mcp show $NAME"
echo "First tool call from OpenClaw triggers Meta OAuth in your browser."
echo "Remove: openclaw mcp unset $NAME"
