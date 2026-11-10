#!/usr/bin/env bash
# Weekly Monday 9 AM — incrementality gap proxy.
# Cron: 0 9 * * 1 /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/scripts/weekly_incrementality.sh
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"
LOG="$ROUTINES/logs/incrementality_$(date +%Y%m%d).log"

mkdir -p "$ROUTINES/logs" "$ROUTINES/reports"
exec > >(tee -a "$LOG") 2>&1

echo "=== 주간 Incrementality $(date) ==="
source "$CLI_VENV/bin/activate"
cd "$ROUTINES/lib"
python incrementality.py
echo "=== 완료 $(date) ==="
