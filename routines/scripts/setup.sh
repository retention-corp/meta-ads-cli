#!/usr/bin/env bash
# Recompute config/baseline.json from the last 30 days of account data.
# Run this once on first install, and again any time the account's spend
# pattern shifts materially (new campaigns, geo expansion, big budget change).
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"

source "$CLI_VENV/bin/activate"
mkdir -p /tmp/baselines

cd "$ROUTINES/../meta-ads-official-cli"

echo "Pulling 30-day account daily baseline..."
meta --output json ads insights get --date-preset last_30d --time-increment daily \
  --fields spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,actions,action_values \
  > /tmp/baselines/account_30d_daily.json

echo "Pulling 30-day age breakdown..."
meta --output json ads insights get --date-preset last_30d --breakdown age \
  --fields spend,impressions,clicks,actions \
  > /tmp/baselines/age_30d.json

echo "Pulling 30-day publisher_platform breakdown..."
meta --output json ads insights get --date-preset last_30d --breakdown publisher_platform \
  --fields spend,impressions,clicks \
  > /tmp/baselines/platform_30d.json

echo "Computing baseline.json..."
python "$ROUTINES/lib/compute_baseline.py" \
  /tmp/baselines/account_30d_daily.json \
  /tmp/baselines/age_30d.json \
  /tmp/baselines/platform_30d.json \
  "$ROUTINES/config/baseline.json"

echo "✅ baseline.json updated. Review:"
python -c "import json; d=json.load(open('$ROUTINES/config/baseline.json')); print(f\"  account: {d['account_name']}\"); print(f\"  window: {d['window_start']} → {d['window_end']} ({d['window_days']}d)\"); t=d['totals']; print(f\"  totals: \\${t['spend']} spend, {t['purchases']} purchases, \\${t['revenue']} revenue, ROAS {t['roas']}x\"); print(f\"  daily: mean \\${d['daily']['mean_spend']} ± \\${d['daily']['std_spend']}\")"
