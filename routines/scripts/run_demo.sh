#!/usr/bin/env bash
# Sequential run of all 4 routines for the YouTube demo.
# Run this on camera. Generates HTML reports + posts to Slack (if configured).
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"

mkdir -p "$ROUTINES/logs" "$ROUTINES/reports"

print_block() {
  echo
  echo "============================================================"
  echo "  $1"
  echo "============================================================"
  sleep 0.4
}

print_block "[1/4] 루틴 1 — 아침 시그널 헬스 체크"
bash "$ROUTINES/scripts/morning_signal.sh" 2>&1 | tail -40

print_block "[2/4] 루틴 2 — 광고별 Fatigue 스캔 + HITL 액션 메뉴"
bash "$ROUTINES/scripts/fatigue_check.sh" 2>&1 | tail -40

print_block "[3/4] 루틴 3 — 주간 Incrementality (proxy)"
bash "$ROUTINES/scripts/weekly_incrementality.sh" 2>&1 | tail -40

print_block "[4/4] 루틴 4 — 크리에이티브 테스트 배치 (dry-run)"
PREFIX="demo_$(date +%Y%m%d_%H%M)" bash "$ROUTINES/scripts/creative_test_batch.sh" 2>&1 | tail -40

print_block "HTML 대시보드 렌더"
source "$CLI_VENV/bin/activate"
python "$ROUTINES/lib/render_html.py"

echo
echo "완료. 리포트 출력:"
ls -la "$ROUTINES/reports" | tail -10
