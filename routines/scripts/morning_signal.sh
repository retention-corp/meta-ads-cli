#!/usr/bin/env bash
# Daily 8 AM — signal quality health check.
# Cron: 0 8 * * * /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/scripts/morning_signal.sh
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"
LOG="$ROUTINES/logs/morning_signal_$(date +%Y%m%d).log"

mkdir -p "$ROUTINES/logs" "$ROUTINES/reports"
exec > >(tee -a "$LOG") 2>&1

echo "=== 아침 시그널 헬스 체크 $(date) ==="
source "$CLI_VENV/bin/activate"
cd "$ROUTINES/lib"
python signal_quality.py
echo "=== 완료 $(date) ==="
