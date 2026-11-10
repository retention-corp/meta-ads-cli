#!/usr/bin/env bash
# Daily midnight — per-ad fatigue scan + HITL action menu.
# Cron: 0 0 * * * /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/scripts/fatigue_check.sh
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"
LOG="$ROUTINES/logs/fatigue_$(date +%Y%m%d).log"

mkdir -p "$ROUTINES/logs" "$ROUTINES/reports"
exec > >(tee -a "$LOG") 2>&1

echo "=== Fatigue 스캔 $(date) ==="
source "$CLI_VENV/bin/activate"
cd "$ROUTINES/lib"
python fatigue.py
echo "=== 완료 $(date) ==="
