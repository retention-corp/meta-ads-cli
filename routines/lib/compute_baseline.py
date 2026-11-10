"""Re-derive config/baseline.json from raw CLI output.

Called by scripts/setup.sh. Lives apart from the rest of lib/ so that the
runtime routines can be edited without re-running setup.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def num(v) -> float:
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def sum_action(actions, action_type: str) -> float:
    if not actions:
        return 0.0
    return sum(num(a.get("value")) for a in actions if a.get("action_type") == action_type)


def main(daily_path: str, age_path: str, plat_path: str, out_path: str) -> None:
    daily = json.loads(Path(daily_path).read_text())["data"]
    age = json.loads(Path(age_path).read_text()).get("data", [])
    plat = json.loads(Path(plat_path).read_text()).get("data", [])

    totals = {"spend": 0.0, "imp": 0, "clk": 0, "purchases": 0.0, "pvalue": 0.0}
    daily_spend: list[float] = []
    daily_ctr: list[float] = []
    for r in daily:
        spend = num(r.get("spend"))
        totals["spend"] += spend
        totals["imp"] += int(num(r.get("impressions")))
        totals["clk"] += int(num(r.get("clicks")))
        totals["purchases"] += sum_action(r.get("actions"), "purchase")
        totals["pvalue"] += sum_action(r.get("action_values"), "purchase")
        daily_spend.append(spend)
        daily_ctr.append(num(r.get("ctr")))

    days = len(daily) or 1
    mean_spend = totals["spend"] / days
    std_spend = math.sqrt(sum((v - mean_spend) ** 2 for v in daily_spend) / days)
    mean_ctr = sum(daily_ctr) / days

    age_total = sum(num(r.get("spend")) for r in age) or 1
    age_share = {r.get("age", "Unknown"): num(r.get("spend")) / age_total for r in age}
    plat_total = sum(num(r.get("spend")) for r in plat) or 1
    plat_share = {r.get("publisher_platform", "Unknown"): num(r.get("spend")) / plat_total for r in plat}

    young = age_share.get("18-24", 0.04)
    instagram = plat_share.get("instagram", 0.93)

    baseline = {
        "account_id": "act_250561826369987",
        "account_name": "Growth Practitioner",
        "computed_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "window_days": days,
        "window_start": daily[0]["date_start"],
        "window_end": daily[-1]["date_start"],
        "totals": {
            "spend": round(totals["spend"], 2),
            "impressions": totals["imp"],
            "clicks": totals["clk"],
            "ctr_mean": round(mean_ctr, 4),
            "purchases": int(totals["purchases"]),
            "revenue": round(totals["pvalue"], 2),
            "roas": round(totals["pvalue"] / totals["spend"], 2) if totals["spend"] else 0,
        },
        "daily": {
            "mean_spend": round(mean_spend, 2),
            "std_spend": round(std_spend, 2),
            "spend_z3_floor": round(mean_spend - 3 * std_spend, 2),
            "spend_z3_ceil": round(mean_spend + 3 * std_spend, 2),
        },
        "age_share": {k: round(v, 4) for k, v in age_share.items()},
        "platform_share": {k: round(v, 4) for k, v in plat_share.items()},
        "thresholds": {
            "young_age_share_baseline": round(young, 4),
            "young_age_share_alert": round(young * 2, 4),
            "instagram_share_floor": round(instagram * 0.93, 4),
            "instagram_share_ceil": 0.99,
            "daily_spend_anomaly_low": round(mean_spend - 2.5 * std_spend, 2),
            "daily_spend_anomaly_high": round(mean_spend + 2.5 * std_spend, 2),
            "fatigue_frequency_warn": 2.0,
            "fatigue_frequency_critical": 2.5,
            "fatigue_ctr_decay_warn": 0.85,
            "fatigue_ctr_decay_critical": 0.75,
            "fatigue_cpm_inflation_warn": 1.20,
            "fatigue_cpm_inflation_critical": 1.40,
            "fatigue_reach_growth_floor": 0.05,
            "roas_floor_pause_candidate": 1.0,
            "roas_winner": 3.0,
        },
    }
    Path(out_path).write_text(json.dumps(baseline, ensure_ascii=False, indent=2))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage: compute_baseline.py <daily.json> <age.json> <platform.json> <out.json>")
        raise SystemExit(2)
    main(*sys.argv[1:])
