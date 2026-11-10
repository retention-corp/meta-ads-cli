"""Aggregate all routine outputs into a single HTML dashboard.

Reads the JSON dropped by signal_quality.py / fatigue.py / incrementality.py
and renders a static dashboard at reports/dashboard.html. This is what the
camera sees during the YouTube shoot.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROUTINES = Path(__file__).resolve().parent.parent
REPORTS = ROUTINES / "reports"
BASELINE = json.loads((ROUTINES / "config" / "baseline.json").read_text())


def _read(name: str):
    p = REPORTS / name
    if not p.exists():
        return None
    return json.loads(p.read_text())


def render() -> Path:
    signal = _read("morning_signal.json") or []
    fatigue = _read("fatigue.json") or []
    incr = _read("incrementality.json") or []

    sev_color = {"ok": "#22c55e", "warn": "#f59e0b", "critical": "#ef4444", "healthy": "#22c55e"}

    def signal_card(a):
        c = sev_color.get(a.get("severity", "ok"), "#7c8694")
        return (
            f"<div class='card'>"
            f"<div class='dot' style='background:{c}'></div>"
            f"<div class='kicker'>{html.escape(a['code'])}</div>"
            f"<div class='msg'>{html.escape(a['message'])}</div>"
            f"<div class='meta'>metric={a['metric']} · expected {html.escape(a['expected'])}</div>"
            f"</div>"
        )

    def fatigue_row(r):
        c = sev_color.get(r["severity"], "#7c8694")
        opts = "".join(
            f"<li><b>{html.escape(o['label'])}</b>"
            + (f"<pre>{html.escape(o['command'])}</pre>" if o.get("command", "# noop") != "# noop" else "")
            + "</li>"
            for o in r.get("suggestions", [])
        )
        m = r["metrics"]
        return (
            f"<tr>"
            f"<td><span class='pill' style='background:{c}'>{r['severity']}</span> "
            f"<b>{html.escape(r['ad_name'])}</b><br><code>{r['ad_id']}</code></td>"
            f"<td>${m['spend_7d']}</td>"
            f"<td>{m['frequency']}</td>"
            f"<td>{m['ctr_first']}% → {m['ctr_last']}%<br><span class='dim'>×{m['ctr_decay_ratio']}</span></td>"
            f"<td>${m['cpm_first']} → ${m['cpm_last']}<br><span class='dim'>×{m['cpm_inflation_ratio']}</span></td>"
            f"<td><ul class='opts'>{opts or '<li class=dim>healthy — no action</li>'}</ul></td>"
            f"</tr>"
        )

    def incr_row(r):
        labels = {"fake_winner_candidate": "🚩 Fake winner 후보", "true_winner": "✅ True winner",
                  "view_through_dependent": "⚠️ View-through 의존", "neutral": "—"}
        return (
            f"<tr>"
            f"<td><b>{html.escape(r['name'])}</b><br><code>{r['campaign_id']}</code></td>"
            f"<td>${r['spend']}</td>"
            f"<td>${r['revenue_default']}<br>${r['revenue_click_only']} <span class='dim'>(proxy)</span></td>"
            f"<td>{r['roas_default']}x<br>{r['roas_click_only']}x <span class='dim'>(proxy)</span></td>"
            f"<td>{r['proxy_ratio']}</td>"
            f"<td>{labels.get(r['label'], r['label'])}</td>"
            f"</tr>"
        )

    out = REPORTS / "dashboard.html"
    out.write_text(
        f"""<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<title>Routines Dashboard — {BASELINE['account_name']}</title>
<style>
:root{{--bg:#0b0d10;--panel:#14181d;--border:#222831;--text:#e6e9ef;--muted:#7c8694;--dim:#5a6472}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font:14px/1.5 -apple-system,BlinkMacSystemFont,sans-serif;padding:24px}}
h1{{font-size:22px;font-weight:600;margin-bottom:6px;letter-spacing:-.01em}}
h2{{font-size:14px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin:24px 0 10px}}
.sub{{color:var(--muted);font-size:13px;margin-bottom:24px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 16px;position:relative}}
.card .dot{{position:absolute;top:14px;right:14px;width:10px;height:10px;border-radius:50%}}
.kicker{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}}
.msg{{font-size:13px;line-height:1.45}}
.meta{{color:var(--dim);font-size:11px;margin-top:8px;font-family:"SF Mono",Menlo,monospace}}
table{{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-bottom:20px}}
th{{background:#0f1318;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:600;padding:12px 10px;text-align:left;border-bottom:1px solid var(--border)}}
td{{padding:12px 10px;border-bottom:1px solid var(--border);font-size:13px;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.pill{{display:inline-block;padding:1px 7px;border-radius:3px;font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:#0b0d10;font-weight:700;margin-right:6px}}
.dim{{color:var(--dim);font-size:11px}}
code{{font-family:"SF Mono",Menlo,monospace;font-size:11px;color:var(--muted)}}
pre{{background:#0f1318;border:1px solid var(--border);border-radius:6px;padding:8px 10px;font-size:11px;color:#cbd5e1;white-space:pre-wrap;margin-top:6px}}
.opts{{list-style:none;padding-left:0}}
.opts li{{margin-bottom:8px}}
.note{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);color:#f59e0b;padding:10px 14px;border-radius:8px;font-size:12px;margin-bottom:20px}}
</style></head><body>
<h1>Routines 대시보드 — {BASELINE['account_name']}</h1>
<div class="sub">baseline {BASELINE['window_start']} → {BASELINE['window_end']} · {BASELINE['window_days']}일 · 30일 ROAS {BASELINE['totals']['roas']}배</div>

<h2>루틴 1 — 아침 시그널 헬스 체크</h2>
<div class="cards">{''.join(signal_card(a) for a in signal) or '<div class=card><div class=msg>시그널 리포트 없음.</div></div>'}</div>

<h2>루틴 2 — 광고별 Fatigue 스캔 + HITL 액션 메뉴</h2>
<table><thead><tr><th>광고</th><th>7d Spend</th><th>Freq</th><th>CTR</th><th>CPM</th><th>추천 액션</th></tr></thead>
<tbody>{''.join(fatigue_row(r) for r in fatigue) or '<tr><td colspan=6 class=dim>fatigue 리포트 없음.</td></tr>'}</tbody></table>

<h2>루틴 3 — 주간 Incrementality (proxy)</h2>
<div class="note">⚠️ Attribution-window proxy. 진짜 incrementality는 Meta Conversion Lift study 또는 geo holdout 필요. "proxy" 컬럼은 view-through 의존성 높은 placement(Audience Network)를 할인하여 click-only ROAS를 근사함.</div>
<table><thead><tr><th>캠페인</th><th>Spend</th><th>매출 (reported / proxy)</th><th>ROAS (reported / proxy)</th><th>Ratio</th><th>라벨</th></tr></thead>
<tbody>{''.join(incr_row(r) for r in incr) or '<tr><td colspan=6 class=dim>incrementality 리포트 없음.</td></tr>'}</tbody></table>

</body></html>"""
    )
    print(f"wrote {out}")
    return out


if __name__ == "__main__":
    render()
