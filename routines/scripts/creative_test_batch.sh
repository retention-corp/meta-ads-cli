#!/usr/bin/env bash
# Weekly creative test batch — generates combinations from vault.
# Default: dry-run. Pass EXECUTE=1 to actually create ads (all PAUSED).
# Cron (dry-run only): 0 10 * * 1 /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/scripts/creative_test_batch.sh
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"
LOG="$ROUTINES/logs/creative_$(date +%Y%m%d).log"
PREFIX="${PREFIX:-week$(date +%V)}"

mkdir -p "$ROUTINES/logs" "$ROUTINES/reports"
exec > >(tee -a "$LOG") 2>&1

echo "=== 크리에이티브 테스트 배치 $(date) prefix=$PREFIX ==="
source "$CLI_VENV/bin/activate"
cd "$ROUTINES/lib"

if [[ "${EXECUTE:-0}" == "1" ]]; then
  : "${CREATIVE_TEST_ADSET_ID:?must export CREATIVE_TEST_ADSET_ID before EXECUTE=1}"
  python creative_pipeline.py --prefix "$PREFIX" --execute
else
  python creative_pipeline.py --prefix "$PREFIX"
fi
echo "=== 완료 $(date) ==="
