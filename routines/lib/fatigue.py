"""Routine 2: Per-ad fatigue detection.

For every active ad with spend in the last 7 days, pull the daily time-series
and score against four fatigue signals:

- frequency >= 2.5 (Andromeda exhaustion threshold for this account class)
- CTR decay: today vs 7d-first ratio < 0.85
- CPM inflation: today vs 7d-first ratio > 1.20
- reach saturation: 7d reach growth rate < 5%

Score 3-4 → critical, 2 → warn, otherwise healthy. Critical/warn ads get a
suggested action menu posted to Slack with the exact CLI commands to execute
(HITL — human runs them, no auto-execute).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import cli  # type: ignore[import-not-found]

ROUTINES = Path(__file__).resolve().parent.parent
BASELINE = json.loads((ROUTINES / "config" / "baseline.json").read_text())
TH = BASELINE["thresholds"]


@dataclass
class FatigueRow:
    ad_id: str
    ad_name: str
    status: str
    score: int
    severity: str
    signals: dict
    metrics: dict
    suggestions: list[dict]


def _series(insights: list[dict], field: str) -> list[float]:
    return [float(r.get(field, 0) or 0) for r in insights]


def _ratio(today: float, first: float) -> float:
    return (today / first) if first > 0 else 1.0


def _reach_growth(reach_series: list[float]) -> float:
    if len(reach_series) < 2 or reach_series[0] <= 0:
        return 0.0
    return (reach_series[-1] - reach_series[0]) / reach_series[0] / max(len(reach_series) - 1, 1)


def score_ad(ad: dict, ts: list[dict]) -> FatigueRow | None:
    if not ts:
        return None
    spend = sum(float(r.get("spend", 0) or 0) for r in ts)
    if spend < 1.0:
        return None
    freq_series = _series(ts, "frequency")
    ctr_series = _series(ts, "ctr")
    cpm_series = _series(ts, "cpm")
    reach_series = _series(ts, "reach")
    if not freq_series or not ctr_series:
        return None
    freq = freq_series[-1]
    ctr_decay = _ratio(ctr_series[-1], ctr_series[0])
    cpm_inflation = _ratio(cpm_series[-1], cpm_series[0])
    reach_growth = _reach_growth(reach_series)
    signals = {
        "frequency_critical": freq >= TH["fatigue_frequency_critical"],
        "frequency_warn": freq >= TH["fatigue_frequency_warn"] and freq < TH["fatigue_frequency_critical"],
        "ctr_decay_critical": ctr_decay < TH["fatigue_ctr_decay_critical"],
        "ctr_decay_warn": (
            ctr_decay < TH["fatigue_ctr_decay_warn"] and ctr_decay >= TH["fatigue_ctr_decay_critical"]
        ),
        "cpm_inflation_critical": cpm_inflation > TH["fatigue_cpm_inflation_critical"],
        "cpm_inflation_warn": (
            cpm_inflation > TH["fatigue_cpm_inflation_warn"] and cpm_inflation <= TH["fatigue_cpm_inflation_critical"]
        ),
        "reach_saturation": reach_growth < TH["fatigue_reach_growth_floor"],
    }
    crit = sum(1 for k, v in signals.items() if v and "critical" in k) + (
        1 if signals["reach_saturation"] else 0
    )
    warn = sum(1 for k, v in signals.items() if v and "warn" in k)
    score = crit * 2 + warn  # 0-8 weight
    if crit >= 2:
        severity = "critical"
    elif crit >= 1 or warn >= 2:
        severity = "warn"
    else:
        severity = "healthy"
    metrics = {
        "spend_7d": round(spend, 2),
        "frequency": round(freq, 2),
        "ctr_first": round(ctr_series[0], 2),
        "ctr_last": round(ctr_series[-1], 2),
        "ctr_decay_ratio": round(ctr_decay, 2),
        "cpm_first": round(cpm_series[0], 2),
        "cpm_last": round(cpm_series[-1], 2),
        "cpm_inflation_ratio": round(cpm_inflation, 2),
        "reach_growth_per_day": round(reach_growth, 4),
    }
    suggestions = _build_suggestions(ad, severity, signals, metrics)
    return FatigueRow(
        ad_id=ad["id"],
        ad_name=ad.get("name", ""),
        status=ad.get("effective_status", ""),
        score=score,
        severity=severity,
        signals=signals,
        metrics=metrics,
        suggestions=suggestions,
    )


def _build_suggestions(ad: dict, severity: str, signals: dict, metrics: dict) -> list[dict]:
    if severity == "healthy":
        return []
    ad_id = ad["id"]
    options = []
    if signals.get("frequency_critical") or signals.get("reach_saturation"):
        options.append(
            {
                "label": "A. 광고 일시정지 (오디언스 saturate)",
                "rationale": f"frequency {metrics['frequency']} ≥ {TH['fatigue_frequency_critical']} 또는 reach 성장 정체",
                "command": f"meta ads ad update {ad_id} --status PAUSED",
                "risk": "low",
            }
        )
    if signals.get("ctr_decay_critical") or signals.get("ctr_decay_warn"):
        options.append(
            {
                "label": "B. 일시정지 + vault 차기 크리에이티브 promote",
                "rationale": f"CTR이 7일 시작 대비 {metrics['ctr_decay_ratio']*100:.0f}%로 감소",
                "command": (
                    f"meta ads ad update {ad_id} --status PAUSED && "
                    f"bash routines/scripts/promote_next_creative.sh {ad['adset_id']}"
                ),
                "risk": "medium",
            }
        )
    if signals.get("cpm_inflation_critical"):
        options.append(
            {
                "label": "C. 광고 세트 일일 예산 50% 감액 (cool-down)",
                "rationale": f"CPM이 7일 시작 대비 {metrics['cpm_inflation_ratio']*100:.0f}%까지 인플레",
                "command": (
                    f"# 현재 daily_budget 가져와서 절반\n"
                    f"meta ads adset get {ad['adset_id']} --output json | "
                    f"jq -r '.daily_budget' | "
                    f"awk '{{print int($1/2)}}' | "
                    f"xargs -I% meta ads adset update {ad['adset_id']} --daily-budget %"
                ),
                "risk": "medium",
            }
        )
    options.append({"label": "Skip — false positive 판단 시 오늘 건너뛰기", "command": "# noop", "risk": "none"})
    return options


def run() -> list[FatigueRow]:
    ads = cli.list_ads(limit=200)
    rows: list[FatigueRow] = []
    for ad in ads:
        if ad.get("effective_status") not in {"ACTIVE", "ADSET_PAUSED", "CAMPAIGN_PAUSED"}:
            continue
        ts = cli.insights(
            ad_id=ad["id"],
            date_preset="last_7d",
            time_increment="daily",
            fields=["spend", "impressions", "clicks", "ctr", "cpc", "cpm", "reach", "frequency"],
        )
        row = score_ad(ad, ts)
        if row:
            rows.append(row)
    rows.sort(key=lambda r: (-r.score, -r.metrics["spend_7d"]))
    return rows


SEV_KO = {"critical": "심각", "warn": "주의", "healthy": "정상"}


def to_slack_text(rows: list[FatigueRow]) -> str:
    needing = [r for r in rows if r.severity != "healthy"]
    if not needing:
        return ":white_check_mark: *Fatigue 스캔 — 전체 정상.* 검토 필요한 광고 없음."
    lines = [f":rotating_light: *Fatigue 경고 — {len(needing)}개 광고 검토 필요*", ""]
    for r in needing:
        lines.append(
            f"• *{r.ad_name}* ({SEV_KO.get(r.severity, r.severity)}) — "
            f"freq {r.metrics['frequency']}, "
            f"CTR {r.metrics['ctr_first']}%→{r.metrics['ctr_last']}%, "
            f"CPM ${r.metrics['cpm_first']}→${r.metrics['cpm_last']}"
        )
        for opt in r.suggestions:
            lines.append(f"    - {opt['label']}")
            if opt.get("command") and opt["command"] != "# noop":
                lines.append(f"      `{opt['command']}`")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    rows = run()
    text = to_slack_text(rows)
    from slack import post  # type: ignore[import-not-found]

    post(text, channel="#ads-fatigue-alerts")
    out = ROUTINES / "reports" / "fatigue.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        json.dumps([{**r.__dict__} for r in rows], ensure_ascii=False, indent=2)
    )
    print(f"wrote {out} — {len(rows)} ads scored, {sum(1 for r in rows if r.severity!='healthy')} need review")
