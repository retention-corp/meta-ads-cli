# routines

영상에서 보여줄 4개 자동화 루틴. **공식 `meta` CLI 만 사용** (Graph API 직접 호출 없음). HITL 설계, dry-run 기본, Slack 알림은 webhook 기반.

대상 계정: **Growth Practitioner** (`act_250561826369987`)
30일 베이스라인: $1,257.55 spend · 68 purchases · $9,382.44 revenue · ROAS 7.46x

## 루틴 4종 요약

| # | 이름 | 빈도 | 동작 | 출력 |
|---|---|---|---|---|
| 1 | Morning Signal Health Check | 매일 8AM | 어제 데이터 vs 30d 베이스라인 비교. 18-24 leakage / placement drift / spend anomaly 3종 체크 | `reports/morning_signal.json` + Slack |
| 2 | Per-Ad Fatigue Scan | 매일 자정 | 활성 광고별 7일 시계열로 frequency / CTR decay / CPM inflation / reach saturation 점수화. severity별 액션 메뉴 (CLI 명령 포함) | `reports/fatigue.json` + Slack |
| 3 | Weekly Incrementality (proxy) | 매주 월 9AM | 캠페인별 reported ROAS vs click-only proxy ROAS. fake/true winner 라벨링. **진짜 incrementality 아님 — 명시 disclaimer 포함** | `reports/incrementality.json` + Slack |
| 4 | Creative Test Batch | 매주 월 10AM (dry-run) | vault 폴더에서 hooks × bodies × CTAs 조합 매트릭스 생성. 기본 dry-run, `EXECUTE=1` 시에만 실제 광고 PAUSED 상태로 생성 | `reports/creative_plan_*.json` + Slack |

## 설치 / 실행

### 1. 셋업 (1회)

```bash
cd /Users/gyusupsim/Projects/tools/meta-ads-cli/routines
cp .env.example .env
# .env 편집: SLACK_WEBHOOK_URL 입력 (없어도 stdout으로 fallback)
bash scripts/setup.sh   # 30일 데이터로 baseline.json 재계산
```

### 2. 영상 촬영용 데모 1회 실행

```bash
bash scripts/run_demo.sh
open reports/dashboard.html
```

위 한 줄로 4개 routine이 순차 실행되고, 통합 HTML 대시보드가 생성됨. 영상에서 이 대시보드를 카메라에 띄움.

### 3. Claude routines 등록 (실제 운영) — cron 대신

cron 대신 **Claude Code의 CronCreate**로 등록하면, 각 routine이 fire될 때마다 Claude 세션 안에서 결과를 받아 즉석 follow-up 분석 가능. cron보다 좋은 점: 슬랙 + Claude 양쪽에 결과가 들어옴.

이번 세션에서 등록 완료 (job IDs):
- `2f1b995b` — 매일 8:03 (아침 시그널)
- `74ef2cf7` — 매일 0:02 (Fatigue 스캔)
- `3aacd4c4` — 매주 월 9:07 (Incrementality proxy)
- `a220f053` — 매주 월 10:12 (Creative test dry-run)

⚠️ **세션 한정.** CronCreate가 durable=true 요청해도 현재 환경에서는 in-memory로만 저장됨. **Claude Code 세션 종료 시 사라짐.** 7일 내 자동 만료. 영상 촬영처럼 한 세션 안에서만 시연하기엔 충분. 24/7 운영하려면 아래 cron fallback 사용 권장.

해제: `CronDelete <job_id>` 또는 Claude 세션 종료 시 자동 정리.

**Cron fallback (Claude Code 안 쓰는 환경):**

```bash
crontab -l > /tmp/cron-current 2>/dev/null
cat crontab.txt >> /tmp/cron-current
crontab /tmp/cron-current
crontab -l   # 확인
```

해제는 `crontab -e`에서 4줄 삭제.

## 폴더 구조

```
routines/
├── README.md                  # 이 파일
├── crontab.txt                # cron 4줄
├── .env.example               # SLACK_WEBHOOK_URL 등
├── config/
│   └── baseline.json          # 30d 실데이터 기반 threshold
├── lib/
│   ├── cli.py                 # meta CLI subprocess wrapper
│   ├── slack.py               # webhook poster (없으면 stdout)
│   ├── signal_quality.py      # 루틴 1
│   ├── fatigue.py             # 루틴 2
│   ├── incrementality.py      # 루틴 3
│   ├── creative_pipeline.py   # 루틴 4
│   ├── render_html.py         # 4개 합쳐서 dashboard.html 생성
│   └── compute_baseline.py    # setup.sh 가 호출
├── scripts/
│   ├── setup.sh               # baseline 재계산
│   ├── morning_signal.sh      # cron 1
│   ├── fatigue_check.sh       # cron 2
│   ├── weekly_incrementality.sh   # cron 3
│   ├── creative_test_batch.sh # cron 4 (dry-run 기본)
│   └── run_demo.sh            # 영상용 4개 순차 실행 + HTML 렌더
├── vault/
│   ├── hooks/                 # 이미지/영상 파일 (creative pipeline 입력)
│   ├── bodies/                # 본문 텍스트 (.txt)
│   ├── ctas/                  # CTA 종류 (파일명 = CTA, 예: LEARN_MORE)
│   └── queue/                 # 다음 promote 대상
├── reports/                   # JSON 결과 + dashboard.html
└── logs/                      # 실행 로그 (날짜별)
```

## HITL 설계 원칙

1. **Routine 1 (Signal Check)** — 알림만, 액션 없음. 마케터가 read.
2. **Routine 2 (Fatigue)** — 진단 + 추천 명령어 텍스트로 슬랙에 보냄. 마케터가 보고 직접 터미널에 paste/실행. **자동 일시정지 안 함.**
3. **Routine 3 (Incrementality)** — 분석 리포트만. 액션은 별도 회의.
4. **Routine 4 (Creative Pipeline)** — `EXECUTE=1` 명시한 경우에만 실제 광고 생성, 그것도 모두 PAUSED 상태. 마케터가 검토 후 활성화.

→ AI/스크립트가 실수로 광고 끄거나 예산 바꾸지 않음. **사람이 마지막 클릭자.**

## 영상 촬영 체크리스트

- [ ] `.env`에 SLACK_WEBHOOK_URL 입력 (별도 demo workspace 권장)
- [ ] `bash scripts/setup.sh` 한 번 실행해 baseline 신선하게 갱신
- [ ] vault에 데모용 자산 미리 채우기 (hooks 2개, bodies 2개, ctas 2개 → 8개 조합 생성됨)
- [ ] `bash scripts/run_demo.sh` 1회 리허설
- [ ] `open reports/dashboard.html` 로 카메라용 HTML 확인
- [ ] cron 등록은 영상 마지막 부분에 라이브로 (`crontab.txt` 보여주면서)

## 알려진 한계

- **Routine 3은 진짜 incrementality 아님.** Conversion Lift 또는 geo holdout 데이터가 없으면 attribution-window proxy로 대체. 영상에서 솔직하게 disclaim 필요.
- **Slack interactive 버튼 없음.** webhook은 read-only. 버튼 승인 흐름은 Slack 앱 + public endpoint (ngrok / Cloudflare Tunnel) 필요. v2.
- **HITL 액션은 copy/paste.** 슬랙 메시지에 들어있는 명령어를 마케터가 터미널에서 직접 실행. 자동 실행 안 함 (의도된 안전장치).
- **`compute_baseline.py`의 account_id가 하드코딩.** 다른 계정으로 옮길 때 한 줄 수정 필요.

## 다음 단계 (v2)

- Slack 앱 + interactive button → 승인 시 자동 실행
- Conversion Lift study 등록 후 Routine 3을 실 incrementality로 업그레이드
- creative pipeline에 video 파일 처리 추가 (현재는 image only)
- Andromeda audience deepening detection (1d_view / 7d_click 비율 시계열)
