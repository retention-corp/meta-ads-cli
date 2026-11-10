"""Routine 1: Morning Signal Health Check.

Three checks, all grounded in 30-day baselines stored in config/baseline.json:

1. **Audience age leakage** — share of 18-24 spend vs baseline. Spike means
   Andromeda is chasing cheap proxy events.
2. **Placement concentration drift** — Instagram share. Drop means budget
   leaking into Facebook / Audience Network where this account historically
   underperforms; sharp rise means narrowing risk.
3. **Daily spend anomaly** — z-score of yesterday's spend against the 30-day
   distribution. Catches pacing failures and approval bottlenecks.

This is intentionally short and explainable. The threshold values come from
real account history, not handwave constants.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cli  # type: ignore[import-not-found]

ROUTINES = Path(__file__).resolve().parent.parent
BASELINE = json.loads((ROUTINES / "config" / "baseline.json").read_text())


@dataclass
class Alert:
    code: str
    severity: str  # "ok" | "warn" | "critical"
    message: str
    metric: float
    expected: str


def _age_share_of(rows: list[dict], age: str) -> float:
    total = sum(float(r.get("spend", 0) or 0) for r in rows)
    if total <= 0:
        return 0.0
    target = sum(float(r.get("spend", 0) or 0) for r in rows if r.get("age") == age)
    return target / total


def _platform_share_of(rows: list[dict], platform: str) -> float:
    total = sum(float(r.get("spend", 0) or 0) for r in rows)
    if total <= 0:
        return 0.0
    target = sum(float(r.get("spend", 0) or 0) for r in rows if r.get("publisher_platform") == platform)
    return target / total


def _position_shares(rows: list[dict]) -> list[tuple[str, float]]:
    """Return [(position_name, share)] sorted desc, top 3."""
    total = sum(float(r.get("spend", 0) or 0) for r in rows)
    if total <= 0:
        return []
    by_pos: dict[str, float] = {}
    for r in rows:
        pos = r.get("platform_position", "unknown")
        by_pos[pos] = by_pos.get(pos, 0) + float(r.get("spend", 0) or 0)
    items = sorted(by_pos.items(), key=lambda kv: -kv[1])
    return [(name, spend / total) for name, spend in items[:3]]


def check_placement_granularity() -> Alert:
    """publisher_platform 비중 분포 체크.

    한계 사항: Meta Ads CLI v1.0.1 은 `--breakdown platform_position` 조회 시
    action_type 자동 결합 버그로 (#100) 에러 반환. 현재는 publisher_platform 단위로
    fallback. 인스타 릴스/스토리/피드 단위 세분 보려면 Marketing API 직접 호출 필요.
    """
    rows = cli.insights(
        date_preset="yesterday",
        breakdown="publisher_platform",
        fields=["spend", "impressions"],
    )
    total = sum(float(r.get("spend", 0) or 0) for r in rows)
    if total <= 0:
        return Alert("placement_granularity", "ok", "어제 publisher_platform 데이터 없음.", 0.0, "n/a")
    by_plat: dict[str, float] = {}
    for r in rows:
        plat = r.get("publisher_platform", "unknown")
        by_plat[plat] = by_plat.get(plat, 0) + float(r.get("spend", 0) or 0)
    shares = sorted(by_plat.items(), key=lambda kv: -kv[1])
    label = {"instagram": "인스타", "facebook": "FB", "audience_network": "AN", "threads": "Threads"}
    parts = ", ".join(f"{label.get(k, k)} {v/total*100:.0f}%" for k, v in shares[:4])
    ig_share = by_plat.get("instagram", 0) / total
    if ig_share > 0.96:
        sev = "warn"
        msg = f"단일 platform 과다 집중 — 인스타 {ig_share*100:.0f}%. fatigue 리스크 점검 권장. 분포: {parts}"
    elif ig_share < 0.85:
        sev = "warn"
        msg = f"인스타 비중 {ig_share*100:.0f}% — FB/AN 누수 가능성 검토 권장. 분포: {parts}"
    else:
        sev = "ok"
        msg = f"분포 정상 — {parts}"
    return Alert("placement_granularity", sev, msg, round(ig_share, 4), "인스타 85~96%")


def check_audience_leakage() -> Alert:
    rows = cli.insights(date_preset="yesterday", breakdown="age", fields=["spend", "impressions"])
    share = _age_share_of(rows, "18-24")
    base = BASELINE["thresholds"]["young_age_share_baseline"]
    alert = BASELINE["thresholds"]["young_age_share_alert"]
    if share > alert:
        sev = "critical"
        msg = (
            f"18-24세 spend 비중 {share*100:.1f}% (baseline {base*100:.1f}%, alert >{alert*100:.1f}%). "
            f"Andromeda가 cheap proxy event 쫓는 신호. 크리에이티브 및 제외 타겟 점검 필요."
        )
    elif share > base * 1.5:
        sev = "warn"
        msg = (
            f"18-24세 spend 비중 {share*100:.1f}% — baseline {base*100:.1f}% 대비 상승 추세. "
            f"alert zone 진입 전 모니터링."
        )
    else:
        sev = "ok"
        msg = f"18-24세 spend 비중 {share*100:.1f}% 정상 범위 (baseline {base*100:.1f}%)."
    return Alert("audience_age_leakage", sev, msg, round(share, 4), f"<= {alert:.4f}")


def check_placement_concentration() -> Alert:
    rows = cli.insights(date_preset="yesterday", breakdown="publisher_platform", fields=["spend", "impressions"])
    share = _platform_share_of(rows, "instagram")
    floor = BASELINE["thresholds"]["instagram_share_floor"]
    ceil = BASELINE["thresholds"]["instagram_share_ceil"]
    if share < floor:
        sev = "warn"
        msg = (
            f"Instagram spend 비중 {share*100:.1f}% (floor {floor*100:.1f}%). "
            f"Facebook/Audience Network로 예산 누수 — 이 계정 기준 ROAS 낮은 placement."
        )
    elif share > ceil:
        sev = "warn"
        msg = (
            f"Instagram spend 비중 {share*100:.1f}% (ceil {ceil*100:.1f}%). "
            f"단일 placement 과다 집중 — fatigue 리스크 가중."
        )
    else:
        sev = "ok"
        msg = f"Instagram spend 비중 {share*100:.1f}% 정상 범위 ({floor*100:.0f}-{ceil*100:.0f}%)."
    return Alert("placement_concentration", sev, msg, round(share, 4), f"{floor:.4f} ~ {ceil:.4f}")


def check_daily_spend_anomaly() -> Alert:
    rows = cli.insights(date_preset="yesterday", fields=["spend", "impressions", "clicks"])
    spend = sum(float(r.get("spend", 0) or 0) for r in rows) if rows else 0.0
    mean = BASELINE["daily"]["mean_spend"]
    std = BASELINE["daily"]["std_spend"]
    z = (spend - mean) / std if std > 0 else 0
    lo = BASELINE["thresholds"]["daily_spend_anomaly_low"]
    hi = BASELINE["thresholds"]["daily_spend_anomaly_high"]
    if spend < lo or spend > hi:
        sev = "critical"
        msg = (
            f"어제 spend ${spend:.2f} (z={z:+.2f}σ). Baseline ${mean:.2f}±${std:.2f}. "
            f"pacing / 승인 / 결제 이벤트 가능성."
        )
    elif abs(z) > 1.5:
        sev = "warn"
        msg = f"어제 spend ${spend:.2f} (z={z:+.2f}σ) — baseline ${mean:.2f}±${std:.2f} 대비 drift."
    else:
        sev = "ok"
        msg = f"어제 spend ${spend:.2f} (z={z:+.2f}σ) 정상 범위 ${lo:.2f}~${hi:.2f}."
    return Alert("daily_spend_anomaly", sev, msg, round(spend, 2), f"{lo:.2f} ~ {hi:.2f}")


def run_all() -> list[Alert]:
    return [
        check_audience_leakage(),
        check_placement_granularity(),
        check_daily_spend_anomaly(),
    ]


CODE_LABELS = {
    "audience_age_leakage": "오디언스 연령 누수",
    "placement_concentration": "Placement 집중도 (IG/FB)",
    "placement_granularity": "Placement 분포 (릴스/스토리/피드)",
    "daily_spend_anomaly": "일일 spend 이상치",
}


def to_slack_text(alerts: list[Alert]) -> str:
    icons = {"ok": ":white_check_mark:", "warn": ":warning:", "critical": ":rotating_light:"}
    head = (
        f"*🌅 아침 시그널 브리핑 — {BASELINE['account_name']}*\n"
        f"_baseline {BASELINE['window_start']} → {BASELINE['window_end']} "
        f"({BASELINE['window_days']}일, 일평균 ${BASELINE['daily']['mean_spend']:.2f})_\n"
    )
    body_lines = []
    for a in alerts:
        label = CODE_LABELS.get(a.code, a.code)
        body_lines.append(f"{icons.get(a.severity, '•')} *{label}* — {a.message}")
    return head + "\n" + "\n".join(body_lines)


if __name__ == "__main__":
    alerts = run_all()
    text = to_slack_text(alerts)
    from slack import post  # type: ignore[import-not-found]

    post(text, channel="#ads-morning-brief")
    out = ROUTINES / "reports" / "morning_signal.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps([a.__dict__ for a in alerts], ensure_ascii=False, indent=2))
    print(f"wrote {out}")
