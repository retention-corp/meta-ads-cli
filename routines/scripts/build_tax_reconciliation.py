import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests


ROOT = Path('/Users/gyusupsim/Projects/tools/meta-ads')
ENV_PATH = ROOT / 'meta-ads-official-cli' / '.env'
BASE = 'https://graph.facebook.com/v21.0'
ACCOUNT_ACTIVITY_SINCE = '2024-11-01'
LIFETIME_SINCE = '2023-07-12'
REPORT_UNTIL = '2026-08-11'
KST = ZoneInfo('Asia/Seoul')


def load_env(path):
    values = {}
    for raw in path.read_text().splitlines():
        raw = raw.strip()
        if not raw or raw.startswith('#') or '=' not in raw:
            continue
        key, value = raw.split('=', 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


env = load_env(ENV_PATH)
token = env['ACCESS_TOKEN']
account = env['AD_ACCOUNT_ID']
if not account.startswith('act_'):
    account = 'act_' + account
session = requests.Session()


def get(path, params):
    request_params = dict(params)
    request_params['access_token'] = token
    response = session.get(BASE + path, params=request_params, timeout=60)
    data = response.json()
    if response.status_code >= 400 or 'error' in data:
        raise RuntimeError(f'{path}: {data}')
    return data


def paginate(path, params):
    rows = []
    data = get(path, params)
    while True:
        rows.extend(data.get('data', []))
        next_url = data.get('paging', {}).get('next')
        if not next_url:
            break
        response = session.get(next_url, timeout=60)
        data = response.json()
        if response.status_code >= 400 or 'error' in data:
            raise RuntimeError(f'pagination: {data}')
    return rows


def money(value):
    return f'${value:,.2f}'


account_info = get('/' + account, {
    'fields': 'id,name,account_status,currency,amount_spent,balance,spend_cap,funding_source_details,timezone_name'
})
activities = paginate('/' + account + '/activities', {
    'fields': 'event_time,event_type,extra_data,object_name,object_type',
    'since': ACCOUNT_ACTIVITY_SINCE,
    'until': '2026-08-12',
    'limit': 100,
})

charge_rows = []
funding_rows = []
for row in activities:
    event_type = row.get('event_type')
    extra_raw = row.get('extra_data') or '{}'
    try:
        extra = json.loads(extra_raw) if isinstance(extra_raw, str) else extra_raw
    except Exception:
        extra = {'_raw': extra_raw}
    timestamp = row.get('event_time')
    dt_utc = datetime.fromisoformat(timestamp.replace('Z', '+00:00')) if timestamp else None
    dt_kst = dt_utc.astimezone(KST) if dt_utc else None
    common = {
        'event_time_utc': timestamp or '',
        'event_time_kst': dt_kst.isoformat() if dt_kst else '',
        'date_kst': dt_kst.date().isoformat() if dt_kst else '',
        'event_type': event_type or '',
        'currency': extra.get('currency') or extra.get('provider_currency') or 'USD',
        'transaction_id': extra.get('transaction_id', ''),
    }
    if event_type == 'ad_account_billing_charge':
        cents = extra.get('new_value')
        if isinstance(cents, (int, float)):
            charge_rows.append({
                **common,
                'amount': round(float(cents) / 100, 2),
                'raw_amount_minor': cents,
                'action': extra.get('action', ''),
                'value_type': extra.get('type', ''),
            })
    elif event_type == 'funding_event_successful':
        minor = extra.get('amount')
        provider_minor = extra.get('provider_amount')
        if isinstance(minor, (int, float)):
            funding_rows.append({
                **common,
                'amount': round(float(minor) / 100, 2),
                'provider_amount': round(float(provider_minor) / 100, 2) if isinstance(provider_minor, (int, float)) else '',
                'fee': round(float(extra.get('fee', 0)) / 100, 2) if isinstance(extra.get('fee'), (int, float)) else '',
                'raw_amount_minor': minor,
                'payment_method_id': extra.get('payment_method_id', ''),
                'funding_source_id': extra.get('funding_source_id', ''),
            })


def insights(params):
    return paginate('/' + account + '/insights', params)


monthly = insights({
    'fields': 'date_start,date_stop,spend,account_currency,impressions,clicks',
    'time_range': json.dumps({'since': ACCOUNT_ACTIVITY_SINCE, 'until': REPORT_UNTIL}, separators=(',', ':')),
    'level': 'account',
    'time_increment': 'monthly',
    'limit': 500,
})
campaigns = insights({
    'fields': 'campaign_id,campaign_name,spend,account_currency,impressions,clicks',
    'time_range': json.dumps({'since': ACCOUNT_ACTIVITY_SINCE, 'until': REPORT_UNTIL}, separators=(',', ':')),
    'level': 'campaign',
    'limit': 500,
})
lifetime = insights({
    'fields': 'date_start,date_stop,spend,account_currency,impressions,clicks',
    'time_range': json.dumps({'since': LIFETIME_SINCE, 'until': REPORT_UNTIL}, separators=(',', ':')),
    'level': 'account',
    'time_increment': 'all_days',
    'limit': 500,
})

out = ROOT / 'routines' / 'reports'
out.mkdir(parents=True, exist_ok=True)

billing_csv = out / 'meta_ads_billing_events_20260811.csv'
with billing_csv.open('w', newline='', encoding='utf-8-sig') as handle:
    fields = ['event_time_kst', 'date_kst', 'event_type', 'amount', 'currency', 'transaction_id', 'payment_method', 'status', 'note']
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for item in sorted(charge_rows + funding_rows, key=lambda value: value['event_time_kst'], reverse=True):
        is_charge = item['event_type'] == 'ad_account_billing_charge'
        writer.writerow({
            'event_time_kst': item['event_time_kst'],
            'date_kst': item['date_kst'],
            'event_type': '광고비 자동청구' if is_charge else '광고잔액 충전',
            'amount': f"{item['amount']:.2f}",
            'currency': item['currency'],
            'transaction_id': item['transaction_id'],
            'payment_method': 'API 미제공',
            'status': '성공 이벤트',
            'note': 'Meta API 활동내역 기준; 카드 브랜드/끝 4자리는 API 미제공',
        })

monthly_csv = out / 'meta_ads_monthly_spend_20260811.csv'
with monthly_csv.open('w', newline='', encoding='utf-8-sig') as handle:
    fields = ['date_start', 'date_stop', 'spend', 'currency', 'impressions', 'clicks']
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for item in monthly:
        writer.writerow({key: item.get(key, '') for key in fields} | {'currency': item.get('account_currency', '')})

campaign_csv = out / 'meta_ads_campaign_spend_20260811.csv'
with campaign_csv.open('w', newline='', encoding='utf-8-sig') as handle:
    fields = ['campaign_id', 'campaign_name', 'spend', 'currency', 'impressions', 'clicks']
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for item in sorted(campaigns, key=lambda value: float(value.get('spend') or 0), reverse=True):
        writer.writerow({key: item.get(key, '') for key in fields} | {'currency': item.get('account_currency', '')})

charges_total = sum(item['amount'] for item in charge_rows)
funding_total = sum(item['amount'] for item in funding_rows)
monthly_total = sum(float(item.get('spend') or 0) for item in monthly)
lifetime_total = float(lifetime[0].get('spend') or 0) if lifetime else 0
account_amount_spent = float(account_info.get('amount_spent') or 0) / 100
account_balance = float(account_info.get('balance') or 0) / 100
funding_source = account_info.get('funding_source_details') or {}

lines = [
    '# Meta 광고비·충전·청구 내역 정리',
    '',
    '- 기준일: 2026-08-11 (Asia/Seoul)',
    f"- 광고계정: {account_info.get('name', '')} ({account_info.get('id', '')})",
    f"- 통화: {account_info.get('currency', '')}",
    f'- 광고 사용액 조회기간: {LIFETIME_SINCE} ~ {REPORT_UNTIL} (Meta Insights; Meta 37개월 제한)',
    f'- 결제/충전 활동 조회기간: {ACCOUNT_ACTIVITY_SINCE} ~ {REPORT_UNTIL}; API가 반환한 최초 활동일은 2024-11-05',
    '',
    '## 핵심 요약',
    '',
    f'- 광고 실제 사용액(Insights, {LIFETIME_SINCE}~{REPORT_UNTIL}): **{money(lifetime_total)}**',
    f'- 광고 실제 사용액(Insights, {ACCOUNT_ACTIVITY_SINCE}~{REPORT_UNTIL}): **{money(monthly_total)}**',
    f'- 광고비 자동청구 성공 이벤트: **{len(charge_rows)}건 / {money(charges_total)}**',
    f'- 광고잔액 충전 성공 이벤트: **{len(funding_rows)}건 / {money(funding_total)}**',
    f'- 계정 현재 잔액 API 표시: **{money(account_balance)}**',
    f'- 계정 amount_spent API 표시: **{money(account_amount_spent)}**',
    '',
    '## 세무사 전달용 해석',
    '',
    'Meta의 광고비 사용액은 Insights의 spend를 기준으로 보며, 결제/충전은 Billing activity의 성공 이벤트를 별도로 집계했습니다. 충전액은 광고 사용액과 동일한 개념이 아니므로, 충전만으로 광고 집행 증빙을 대체하지 않고 Insights 및 캠페인별 사용내역을 함께 제출해야 합니다.',
    '',
    '현재 결제수단 화면에서는 Visa 끝 4자리 8109와 MasterCard 끝 4자리 3071이 확인됩니다. 다만 Meta Graph API의 과거 활동 응답에는 카드 브랜드/끝 4자리 필드가 없어 2024-11-05 이후 전체 청구 이벤트를 카드별로 자동 매칭할 수 없습니다. 따라서 CSV의 카드 열은 API 기준으로 미제공 처리했고, Meta 결제 활동 화면/다운로드 영수증에서 거래번호별 카드 매칭이 추가로 필요합니다.',
    '',
    '## 파일',
    '',
    f'- [청구·충전 이벤트 CSV]({billing_csv})',
    f'- [월별 광고 사용액 CSV]({monthly_csv})',
    f'- [캠페인별 광고 사용액 CSV]({campaign_csv})',
    '',
    '## 월별 광고 사용액',
    '',
    '| 기간 | 사용액 | 노출 | 클릭 |',
    '|---|---:|---:|---:|',
]
for item in monthly:
    lines.append(f"| {item.get('date_start', '')}~{item.get('date_stop', '')} | {money(float(item.get('spend') or 0))} | {int(float(item.get('impressions') or 0)):,} | {int(float(item.get('clicks') or 0)):,} |")
lines += [
    '',
    '## 검증 메모',
    '',
    f'- API 활동내역은 {len(charge_rows)}건의 ad_account_billing_charge와 {len(funding_rows)}건의 funding_event_successful을 반환했습니다.',
    '- 결제/충전 이벤트 합계와 광고 사용액 합계는 잔액 이월, 청구 시점, 실패 결제, 환불/조정, 조회기간 차이로 일치하지 않을 수 있습니다.',
    '- 계정의 amount_spent 표시액과 Insights 합계도 서로 달라, 세무 신고용 금액은 카드명세서·Meta 영수증·Insights를 같은 기간으로 맞춰 최종 대조해야 합니다.',
]
report = out / 'meta_ads_tax_reconciliation_20260811.md'
report.write_text('\n'.join(lines) + '\n', encoding='utf-8')

summary = {
    'account': account_info,
    'activity_coverage': {
        'requested_since': ACCOUNT_ACTIVITY_SINCE,
        'requested_until': REPORT_UNTIL,
        'rows': len(activities),
        'charges': len(charge_rows),
        'fundings': len(funding_rows),
        'earliest_returned_event': min((item['event_time_utc'] for item in charge_rows + funding_rows), default=''),
    },
    'totals': {
        'charges': round(charges_total, 2),
        'fundings': round(funding_total, 2),
        'monthly_insights': round(monthly_total, 2),
        'lifetime_insights': round(lifetime_total, 2),
    },
    'files': [str(report), str(billing_csv), str(monthly_csv), str(campaign_csv)],
}
(out / 'meta_ads_tax_reconciliation_20260811.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

print(json.dumps({
    'account': account_info.get('name'),
    'currency': account_info.get('currency'),
    'funding_source': funding_source,
    'activity_rows': len(activities),
    'charges': {'count': len(charge_rows), 'total': round(charges_total, 2)},
    'fundings': {'count': len(funding_rows), 'total': round(funding_total, 2)},
    'insights_period': {'since': ACCOUNT_ACTIVITY_SINCE, 'until': REPORT_UNTIL, 'total': round(monthly_total, 2), 'months': len(monthly)},
    'insights_lifetime': round(lifetime_total, 2),
    'account_amount_spent': round(account_amount_spent, 2),
    'account_balance': round(account_balance, 2),
    'campaign_count': len(campaigns),
    'files': [str(report), str(billing_csv), str(monthly_csv), str(campaign_csv)],
}, ensure_ascii=False, indent=2))
