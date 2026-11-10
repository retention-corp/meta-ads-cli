# 슬라이드 17개 — 디자인 디테일

> 영상 대본 v3 (`youtube-script-ko.md`)에 1:1 매핑.
> 추천 도구: Keynote (16:9, 1920×1080) 또는 Figma 슬라이드 템플릿.
> 공통 톤: 다크 배경 (#0b0d10), 한 슬라이드당 텍스트 최대 30단어. SF Pro / Pretendard.

---

## 슬라이드 1 — 후킹 (0:00)

**용도:** 첫 5초 hook. 시청자 이탈 막음.
**자료:** 본인이 이미 만들어둔 *"똑똑하고 게으른 사람이 가장 멀리 간다"* 이미지 풀스크린.
**스타일:** 그대로 사용.

---

## 슬라이드 2 — 4분할 라이브 (0:30)

**용도:** *"이게 자동으로 돌아감"* 증명.
**자료:** 라이브 캡처 4분할.
- 좌상: Slack `#ads-routines` 채널 — 4개 routine 메시지 도착 모습
- 우상: 터미널 (Ghostty) — `claude routines fired` 로그 흐름
- 좌하: 브라우저 — `dashboard.html` 자동 갱신
- 우하: Finder — `vault/` 폴더, `creative_plan_*.json` 떨어지는 모습

**셋업:** `bash routines/scripts/arrange_4pane.sh` 실행.
**대안 (라이브 안 될 시):** 정적 캡처 4장을 합성한 PNG.

---

## 슬라이드 3 — 학습 공동체 (1:00)

**용도:** thesis 강조 + 본인 자기 소개.
**자료:**
- 큰 텍스트: *"이 영상은 강의가 아닙니다"*
- 작은 텍스트 아래: *"학습 공동체를 같이 만들어요"*
- 본인 사진 작게 우측 하단

**스타일:** 텍스트 위주, 이미지는 보조.

---

## 슬라이드 4 — UI/CLI/MCP 비교표 (2:00)

**용도:** 도구 차이 한 장에 압축.
**자료:** 6열 비교표:

| | Ads Manager (UI) | Ads CLI | Ads MCP |
|---|---|---|---|
| 무엇 | 웹 + 마우스 | 터미널 + 명령 | 에이전트 + 자연어 |
| 속도 | 가장 느림 | 가장 빠름 | 빠름 |
| 반복 | 매번 클릭 | 한 번 짜면 영원 | 매번 자연어 |
| 재현성 | 사람마다 다름 | 100% 동일 | 비결정적 |
| 장점 | 학습 / 탐색 | 자동화 | ad-hoc 분석 |
| 진입 장벽 | 낮음 (누구나) | 중간 (엔지니어 친화) | 낮음 (자연어) |

**스타일:** 다크 배경. UI=보라, CLI=시안, MCP=오렌지 컬럼 헤더.

---

## 슬라이드 5 — OpenClaw 한 줄 (3:30)

**용도:** Claude Code 외 사용자 포용.
**자료:**
```
openclaw mcp set meta-ads '{"type":"http","url":"https://mcp.facebook.com/ads"}'
```

**스타일:** 큰 코드 블록 가운데. 하단에 작은 글씨 *"MCP는 표준 — Cursor, ChatGPT, OpenClaw 모두 작동"*.

---

## 슬라이드 6 — 시스템 아키텍처 (4:00)

**용도:** 전체 흐름 한 장.
**자료:** `routines/assets/architecture.png` (gpt-image-1로 생성됨).
**스타일:** 풀스크린.

---

## 슬라이드 7 — Claude Routines 등록 화면 (5:00)

**용도:** *"진짜 등록됨"* 증명.
**자료:** `https://claude.ai/code/routines` 페이지 캡처. 4개 routine 보임:
- meta-ads-morning-signal-daily
- meta-ads-fatigue-scan-daily
- meta-ads-incrementality-weekly
- meta-ads-creative-flywheel-weekly

**스타일:** 페이지 캡처 + 4개 라인 빨간 박스 강조.

---

## 슬라이드 8 — Routine 1 Slack 메시지 (6:30)

**용도:** 진짜 메시지 보여주기.
**자료:** Slack 캡처:

```
🌅 아침 시그널 브리핑 — get.ship.done-campaign
baseline 30일 일평균 $41.92

✅ 오디언스 연령 누수 — 18-24세 3.5% (baseline 3.9%)
✅ Placement 분포 — 릴스 64% / 스토리 22% / 피드 14%. 정상 분포
✅ 일일 spend — 어제 $51.95 (z=+0.68σ)
```

**스타일:** Slack 다크모드 그대로.

---

## 슬라이드 9 — Fatigue 시그널 4종 (7:30)

**용도:** Routine 2 로직 시각화.
**자료:** 표:

| 시그널 | 경고 임계 | Critical 임계 |
|---|---|---|
| frequency | ≥ 2.0 | ≥ 2.5 |
| CTR decay (오늘/7일전) | < 0.85 | < 0.75 |
| CPM inflation (오늘/7일전) | > 1.20 | > 1.40 |
| reach 일평균 성장률 | < 5% | (saturation) |

**스타일:** 빨강/노랑 신호등 컬러로 임계치 강조.

---

## 슬라이드 10 — Routine 2 Slack + HITL 메뉴 (8:30)

**용도:** *"AI가 자동으로 안 끔"* 증명.
**자료:** Slack 캡처:

```
🚨 Fatigue 경고 — 1개 광고 검토 필요

• meta-reel-compilation-G-v5 (주의)
  freq 1.14, CTR 0%→0%, CPM $35→$17
    - A. 광고 일시정지 (오디언스 saturate)
      `meta ads ad update 120241700755610025 --status PAUSED`
    - Skip — false positive 판단 시 오늘 건너뛰기
```

**스타일:** 명령어 부분 빨간 박스 강조.
**보이스오버:** *"이거 자동 실행 안 합니다. 사람이 paste해서 직접 실행."*

---

## 슬라이드 11 — Attribution Setting 비교 (9:30)

**용도:** Routine 3 핵심 개념.
**자료:** 다이어그램:

```
[ 7d_click + 1d_view ]   ← 전통적 default
        ↕
       gap (보고 방식 차이)
        ↕
[ incremental ]           ← Meta 권장 setting
```

**스타일:** 두 박스 위아래 비교, 중앙에 ↕ 화살표 + *"gap"* 라벨.

---

## 슬라이드 12 — Routine 3 Slack 메시지 (11:00)

**자료:**

```
📊 주간 Incrementality Gap — 최근 30일
attribution setting 비교. 진짜 incrementality는 Conversion Lift 연구 필요.

캠페인: get.ship.done-campaign
• 7d_c + 1d_v ROAS: 7.46배 (전통적 리포팅)
• incremental ROAS: 9.72배 (Meta 권장 setting)
• gap ratio: 0.77 → ✅ true_winner

해석: 두 setting 차이가 크지 않음. click-driven 가능성 높음.
attribution setting 검토 권장.
```

**스타일:** Slack 다크모드.

---

## 슬라이드 13 — Admiral 5단계 Flywheel (11:30)

**자료:** 원형 다이어그램 5단계:
```
   1. Hypothesis
        ↓
   2. AI Production at Volume
        ↓
   3. Balanced Deployment
        ↓
   4. Signal Interpretation
        ↓
   5. Brief Development
        ↓
   (back to 1, compounding)
```

**스타일:** 5각형 또는 원형 사이클 다이어그램. 각 단계마다 1줄 설명.

---

## 슬라이드 14 — Admiral 핵심 원칙 4개 (12:30)

**자료:**
1. **한 번에 한 변수만** — 훅/바디/CTA 동시 변경 금지
2. **1,000 imp 도달 전 판정 금지** — 5,000+ 권장
3. **하위 전환 우선** — purchase CVR > CTR
4. **알고리즘 편향 차단** — Advantage+ 자동 우승자 그대로 믿지 마라

**스타일:** 4개 카드 2×2 그리드.

---

## 슬라이드 15 — Routine 4 Slack 메시지 (13:00)

**자료:**

```
🎨 주간 Creative Flywheel — Admiral framework

테스트 자격 (imp ≥ 1,000): 3개
⏳ Still learning (imp < 1,000): 2개

✅ Winner candidates (하위 전환 상위 30%):
  • ad_postit_winner_260427 — purchase CVR 4.2%, imp 12,300
    핵심: 손글씨 hook + 검은 배경 + 12초 길이

⛔ Loser candidates:
  • jinny-capcut-260420 — purchase CVR 1.1%, imp 8,400

다음 사이클 가설:
검은 배경 + 손글씨 hook이 잔존. 다음 batch에서 손글씨 변형 4개 추가 테스트.
```

---

## 슬라이드 16 — 글로벌 마스터 3명 (13:30)

**자료:** 3장 카드:

| 카드 | 이름 | 한 줄 |
|---|---|---|
| 1 | Thomas Petit | *signal engineering*의 창시자 — 광고 시그널 설계 |
| 2 | Marcus Burke | Meta 광고의 살아있는 백과사전 |
| 3 | Admiral Media | €500M+ ad spend, AI Creative Factory |

**스타일:** 3명 사진 (트위터 프로필 사진) + 트위터 핸들 + 한 줄. 다크 배경.

---

## 슬라이드 17 — 마무리 콜링 (14:30)

**자료:**
- 큰 텍스트: *"직접 만들어보세요"*
- 아래 작은 텍스트: *"막히면 댓글로. 만들면 결과 공유."*
- 댓글창 일러스트

**스타일:** 화이트 텍스트 위 다크 배경. 가운데 정렬.

---

## 영상 캡처용 추가 (사이사이)

- **Slide A (cutaway):** routine ID 4개 표시 — `https://claude.ai/code/routines/{trig_*}`
- **Slide B (cutaway):** baseline.json 컴퓨팅 화면 (실 30일 데이터)
- **Slide C (cutaway):** vault 폴더 hooks 3개 + bodies 4개 + ctas 3개 트리

---

## 슬라이드 17개 만들 때 빠른 방법

### A. Keynote 템플릿 (추천)

1. Apple Keynote 켜고 16:9 다크 테마 선택
2. 마스터 슬라이드 1개 만듦 — 다크 배경, SF Pro 폰트, 흰색 텍스트
3. 17개 슬라이드 복제하면서 위 가이드대로 채움
4. PNG 일괄 export (File → Export As → Images)
5. 영상 편집 시 PNG를 cutaway로 삽입

### B. Figma Slides

1. Figma 새 파일 → Slides 템플릿
2. 같은 방식

### C. 빠른 Markdown → PDF

1. 위 17개 슬라이드를 1슬라이드당 1마크다운 페이지로 작성
2. Marp 또는 reveal.js로 PNG export
3. 다크 테마 자동 적용

### D. AI 생성

이미지 슬라이드 (예: 다이어그램 슬라이드 6, 13)는 `/imagen` 또는 `/gpt-image`로 생성.

```
bash /Users/gyusupsim/.claude/skills/gpt-image/scripts/ima2.sh gen \
  "Slide design: dark background, [내용 설명]..." \
  -o /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/assets/slide_NN.png
```

---

## 자산 위치

```
routines/
├── assets/
│   ├── architecture.png     ← 슬라이드 6 (생성됨)
│   ├── slide_01.png         ← 본인 이미지 (이미 있음)
│   ├── slide_02_4pane.png   ← 라이브 캡처 또는 합성
│   ├── ...
│   └── slide_17.png
├── youtube-script-ko.md     ← 대본 v3
└── slides.md                ← 이 파일
```
