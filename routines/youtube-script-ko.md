# 유튜브 영상 대본 v3 — Meta Ads CLI 자동화 시스템

> 2026-05-01 · Growth Practitioner / get.ship.done-campaign 실데이터
> 30일: $1,257.55 spend · 68 purchases · $9,382.44 revenue · ROAS 7.46x
> 100만뷰 목표. 험블, 학습 공동체 톤. 각 섹션 = [대사] + [슬라이드].

---

## 영상 thesis

> "AI 에이전트가 광고를 운영하는 게 아니라, 마케터가 똑똑하고 게으르게 일할 수 있는 인프라를 만든다."

---

## 챕터별 [대사] / [슬라이드] 분리 형식

각 섹션은 **[대사]** = 카메라 앞에서 말하는 내용, **[슬라이드]** = 화면에 띄울 시각자료.

---

### 0:00–0:30 — 후킹 (똑똑하고 게으른)

**[슬라이드 1]** 본인이 만들어둔 *"똑똑하고 게으른 사람이 가장 멀리 간다"* 이미지 풀스크린. 5초.

**[대사]**

> "마케팅 10년 하면서 한 가지 깨달았어요. 똑똑하고 게으른 사람이 가장 멀리 간다.
>
> 부지런한데 멍청하면 일만 만들고, 똑똑한데 부지런하면 본인이 병목, 게으른데 멍청하면 그냥 일 안 함. 똑똑하고 게으른 사람만이 시스템을 만들고, 그 시스템이 본인보다 더 잘 일하게 합니다.
>
> 오늘 보여드릴 건 마케터를 똑똑하고 게으르게 만드는 시스템입니다. 매일 자동으로 돌아가요. 끝까지 보시면 똑같이 만드실 수 있습니다."

---

### 0:30–1:00 — 시스템 한눈에 (4분할)

**[슬라이드 2]** 4분할 화면 (대본 끝의 `arrange_4pane.sh` 결과)
- 좌상: Slack `#ads-routines` 채널 — routine 4개 메시지 도착 모습
- 우상: 터미널 — claude routines fired 로그
- 좌하: `dashboard.html` 자동 갱신
- 우하: `vault/` 폴더 — 다음 주 테스트 plan JSON

**[대사]**

> "이 화면 보시는 거, 제가 아무것도 안 누릅니다. 매일 새벽 0시 2분, 아침 8시 3분, 월요일 9시 7분 — Claude routines가 자동 실행되면서 슬랙으로 분석 결과를 보냅니다.
>
> 어제 spend $51.95. 18-24세 누수 없음. 인스타 placement 분포 정상. ROAS 7.46배. 한 캠페인이 fatigue 진입 단계. 액션 메뉴 텍스트로 옴.
>
> 옛날엔 4시간 걸리던 일을 30분으로 줄였습니다. 그것도 슬랙 보면서 커피 마시는 30분."

---

### 1:00–2:00 — 학습 공동체 콜링 (선생-제자 프레임 깨기)

**[슬라이드 3]** 제목만: *"이 영상은 강의가 아니에요"* + 본인 사진 작게.

**[대사]**

> "본격 시연 들어가기 전에 한 가지만.
>
> 저 강사 아니에요. 매일 광고 운영하는 마케터예요. 5개월째 부트캠프를 운영하고 있는데, 한 가지 신기한 걸 봤어요. 와서 강의 듣는 사람들이 어느 순간부터 builder mode가 되더라고요. 본인이 직접 만들기 시작해요.
>
> 저는 원래 change agent를 갈망했어요. 세상을 바꾸고 싶었어요. 근데 인생 살면서 깨달은 게 있어요 — 나를 바꾸는 것조차 매일 갈고 닦아야 가능하다는 거. 지금도 매일 그 일을 합니다.
>
> 이번에 처음으로 *개개인의 변화를 돕는 경험*을 하고 있어요. 부트캠프에서 사람들이 빌더로 바뀌는 걸 옆에서 봅니다. 솔직하게 말씀드리면 저는 아직 조직을 바꿔본 경험이 없어요. 수신제가치국평천하라는 말 있잖아요. 나, 가족, 그 다음 조직, 그 다음 세상. 저는 두 번째 단계에 있어요. 언젠가 조직을 바꾸는 경험도 꼭 해보고 싶습니다.
>
> 코액티브 코칭에서 *얼라이언스* 라는 개념이 있어요. 함께 만들어가는 관계. 다오랩에서 배운 *학습 커뮤니티* 도 같은 결입니다. 한 명이 100명한테 떠먹여주는 구조가 아니라, 같이 만드는 구조.
>
> 그래서 부탁드려요. 영상 보고 끝내지 마시고 직접 만들어보세요. 막히면 댓글 남기세요. 만든 사람은 결과 공유해주세요. 같이 가는 사람들이 모이면 그게 학습 공동체가 됩니다."

---

### 2:00–4:00 — UI vs CLI vs MCP 도구별 역할

**[슬라이드 4]** 비교표:

| | Ads Manager (UI) | Ads CLI | Ads MCP |
|---|---|---|---|
| 무엇 | 웹 화면 + 마우스 | 터미널 + 명령어 | AI 에이전트 + 자연어 |
| 속도 | 가장 느림 | 가장 빠름 | 빠름 |
| 반복 | 매번 클릭 | 한 번 짜면 영원 | 매번 자연어 |
| 재현성 | 사람마다 다름 | 100% 동일 | 비결정적 |
| 장점 | 학습/탐색 | 자동화 | ad-hoc 분석 |
| 마케터 진입 | 누구나 | 엔지니어 친화 | 누구나 |

**[슬라이드 5]** OpenClaw 대안 한 줄:
```
openclaw mcp set meta-ads '{"type":"http","url":"https://mcp.facebook.com/ads"}'
```

**[대사]**

> "본격적으로 시스템 보기 전에, 도구 3가지부터 정리할게요. 이 셋의 차이를 알면 나머지가 다 보입니다.
>
> Ads Manager는 다 아실 거예요. 웹 화면, 마우스로 클릭. 학습용으로는 좋은데 매일 똑같은 일 반복하기엔 느려요.
>
> Ads CLI는 터미널 명령어예요. 한 줄 짜면 0.5초에 끝나고, 매일 같은 결과 나옵니다. 자동화의 뼈대.
>
> Ads MCP는 AI 에이전트랑 자연어로 대화하는 통로. *'어제 ROAS 왜 떨어졌어?'* 이렇게 물어볼 수 있는 거예요. 분석할 때 강력합니다.
>
> 오늘 시스템은 셋 다 씁니다. CLI가 자동화 뼈대, MCP가 분석 layer, UI는 영상에서 거의 안 보여요. UI는 졸업하는 도구예요.
>
> Claude Code 안 쓰시는 분들 — 오픈클로(OpenClaw) 같은 거 쓰셔도 됩니다. MCP는 표준이라 명령 한 줄만 다릅니다."

---

### 4:00–5:00 — 시스템 아키텍처

**[슬라이드 6]** `routines/assets/architecture.png` 풀스크린.

**[대사]**

> "전체 시스템을 한 장으로 보면 이렇습니다.
>
> 위에서부터 — Claude routines가 4개 등록돼있고, 각각 정해진 시간에 깨어납니다. 깨어나면 Meta Ads MCP 통해서 광고 데이터를 받아요. AI 에이전트가 분석만 하고, 결과를 슬랙으로 보내요. 슬랙에는 명령어가 텍스트로 와요. 사람이 검토하고 직접 paste해서 실행합니다.
>
> 핵심 4 원칙:
>
> 첫째, CLI가 fetch + 실행 다 함. Marketing API 직접 안 침.
> 둘째, AI는 분석/추론만. 광고 상태 직접 안 바꿈.
> 셋째, 모든 의사결정은 Human-in-the-Loop.
> 넷째, Andromeda 관점 분석을 별도 layer로 둠.
>
> 사람이 마지막 클릭자입니다. AI는 마찰만 0으로 만들어요."

---

### 5:00–7:00 — Routine 1: 아침 시그널 헬스 체크

**[슬라이드 7]** Claude routines 등록 화면 (`https://claude.ai/code/routines`) — `meta-ads-morning-signal-daily` 항목 강조

**[슬라이드 8]** Slack 메시지 캡처 (실제 도착한 한국어 메시지)

**[대사]**

> "Routine 1, 아침 시그널 헬스 체크. 매일 KST 8:03에 자동 실행됩니다.
>
> 3가지 체크가 있어요.
>
> 하나, 18-24세 spend 누수. 30일 baseline이 3.9%인데 7.85% 넘으면 alert. Andromeda가 cheap proxy event 쫓는다는 신호예요.
>
> 둘, 인스타 placement 분포. 인스타 릴스, 스토리, 피드 단위로 비중 봅니다. 한 곳에 70% 이상 몰리면 fatigue 리스크 경고.
>
> 셋, 일일 spend 이상치. 30일 평균 $41.92, 표준편차 $14.83. z-score 2.5σ 넘으면 critical. pacing 문제, 결제 이벤트, 승인 보류 등 — 보통 이 셋 중 하나예요.
>
> 한 마디로 어제 시그널 quality가 깨졌으면 알려주는 routine입니다. Andromeda가 잘못된 시그널 학습하면 다음 주 ROAS 망가지거든요. 그 신호를 가장 먼저 잡는 거."

---

### 7:00–9:30 — Routine 2: Fatigue + HITL (영상 하이라이트)

**[슬라이드 9]** 4가지 fatigue 시그널 표:

| 시그널 | 경고 | Critical |
|---|---|---|
| frequency | ≥ 2.0 | ≥ 2.5 |
| CTR decay | < 0.85 | < 0.75 |
| CPM inflation | > 1.20 | > 1.40 |
| reach 성장률 | < 5% | (saturation) |

**[슬라이드 10]** Slack 메시지 — fatigue 경고 + 액션 메뉴 + 명령어 텍스트

**[대사]**

> "Routine 2, 광고별 fatigue 스캔. 매일 자정에 돕니다.
>
> 4가지 시그널 보고 점수 매겨요. frequency가 2.5 넘었나, CTR이 일주일 전 대비 25% 빠졌나, CPM이 40% 부풀었나, reach가 정체됐나.
>
> Critical 시그널 2개 이상이면 critical 라벨, 1개거나 warn 2개면 warn 라벨.
>
> 자, 이 부분이 데모랑 결정적으로 다른 점이에요.
>
> 슬랙에 fatigue 경고 메시지가 오면, **자동으로 광고 끄지 않습니다.** 명령어가 텍스트로 와요. *'meta ads ad update 이 광고 ID --status PAUSED'*. 마케터가 보고, 검토하고, 직접 paste해서 실행해야 돼요.
>
> 왜 이렇게 했냐. AI가 광고 자동으로 끄면 회복 불가능한 일이 생겨요. 어제 시작한 신규 광고인데 데이터 부족으로 fatigue로 잘못 판단? 자동으로 끄면 그 광고 그대로 죽음. 사람이 보면 '아 이건 어제 시작이라 데이터 부족, skip' 가능.
>
> AI는 마찰을 0으로, 통제권은 사람이 가져갑니다."

---

### 9:30–11:30 — Routine 3: Attribution Setting Gap

**[슬라이드 11]** 두 setting 비교 다이어그램:
```
[7d_click + 1d_view]  ←  전통적 default
                       ↕  (gap)
[incremental]         ←  Meta 권장
```

**[슬라이드 12]** Slack 메시지 — Incrementality Gap 리포트

**[대사]**

> "Routine 3, 주간 attribution setting gap. 매주 월요일 9시 7분에 돕니다.
>
> 이 routine 만든 이유부터 말씀드릴게요.
>
> Meta가 default로 주는 attribution은 7d_click + 1d_view 입니다. 클릭 후 7일 + 노출 후 1일 컨버전. 이게 전통적인 보고 방식이에요. 한국에서도 많은 분들이 이걸로 보고 있습니다.
>
> 근데 Meta가 새로 incremental setting을 밀고 있어요. Meta가 자체 시그널로 *진짜로 광고가 만든* 컨버전이라고 판단한 것만 카운트.
>
> 두 setting의 차이가 클수록, *내가 어떻게 보고하느냐* 에 따라 같은 캠페인이 다르게 보입니다.
>
> 솔직하게 말씀드리면 — 이건 진짜 incrementality는 아니에요. 진짜 incrementality는 Conversion Lift 연구나 geo holdout 해야 나옵니다. 이건 그 전 단계의 proxy예요. 검토 권장 수준의 시그널.
>
> 매주 월요일에 두 setting의 ROAS 차이를 슬랙으로 보내드려요. 차이 크면 *attribution setting 검토할 만한 시점이라는 신호*. 그게 이 routine이 하는 일입니다."

---

### 11:30–13:30 — Routine 4: Admiral Creative Flywheel

**[슬라이드 13]** Admiral 5단계 flywheel 다이어그램:
```
1. Hypothesis → 2. AI Production → 3. Balanced Deployment
                                            ↓
5. Brief Development ← 4. Signal Interpretation
              (compounding)
```

**[슬라이드 14]** 핵심 원칙 4개:
- 한 번에 한 변수만
- 1,000 imp 도달 전 판정 금지
- 하위 전환 우선, CTR은 보조
- Advantage+ 편향 차단

**[슬라이드 15]** Slack 메시지 — winner/loser candidates + 다음 사이클 가설

**[대사]**

> "Routine 4, 매주 월요일 10시 12분. Admiral Media의 Creative Testing Flywheel을 한국 마케터용으로 재해석했어요.
>
> Admiral이 mobile app UA 분야에서 €5억+ 운영하는 곳인데, 이 사람들이 정리한 5단계 사이클이 있어요. 가설 설계, AI 양산, 균형 노출, 시그널 해석, 브리프 고도화. 이게 한 사이클 돌면서 다음 사이클의 가설을 만들어요.
>
> 핵심 원칙 4개가 있어요.
>
> 하나, 한 번에 한 변수만 테스트. 훅, 바디, CTA를 동시에 바꾸면 뭐 때문에 이긴 건지 모릅니다.
>
> 둘, 1,000 impression 도달 전엔 우승/패자 판정 금지. 200 imp로 끄면 노이즈에 끌려가요. 5,000+ 권장.
>
> 셋, CTR로 우승자 고르지 마세요. 하위 전환 — 우리 캠페인 기준 purchase CVR — 봐야 합니다. CTR 높지만 구매 안 하는 광고는 잘못된 사람한테 보여주고 있는 거예요.
>
> 넷, Advantage+이 골라준 우승자 그대로 믿지 마세요. 알고리즘이 초기 leader한테 노출 몰아주는 편향이 있어요. 테스트 구간에서는 균형 노출 강제.
>
> Admiral이 일주일에 40~100개 variant를 테스트해요. 한국에서 일주일에 5개 만들면 잘하는 거잖아요. 차이가 8~20배. 인간 디자이너가 100개 못 만들어요. AI가 만들어야 합니다. 이게 2026년 마케터의 working style이에요."

---

### 13:30–14:30 — 누구를 따라가야 하나

**[슬라이드 16]** 글로벌 마스터 3명 카드:
- Thomas Petit (@thomasbcn) — signal engineering
- Marcus Burke — Meta 광고 백과사전
- Admiral Media — €500M+ ad spend

**[대사]**

> "마지막으로 한 가지 말씀드릴게요.
>
> 한국 마케팅 커뮤니티에서 강의 듣고 책 보면서 공부하시는 분들 많아요. 좋은 강사들 있고, 정말 잘 가르치는 분들도 많이 봤어요. 그분들 욕할 생각 없어요.
>
> 다만, 글로벌 탑티어가 어떻게 일하는지 모르는 채로 한국 안에서만 학습하면 천장이 보일 수 있어요. 한국 마케팅 평균이 글로벌에서 어디쯤인지 가늠하기 어렵거든요.
>
> 제가 매일 보는 사람 셋만 추천드립니다.
>
> Thomas Petit. 트위터 @thomasbcn. signal engineering이라는 개념을 만든 사람이에요. 광고 시그널을 어떻게 설계해야 알고리즘이 잘 학습하는지 — 이걸 매주 글로 풀어요.
>
> Marcus Burke. Meta 광고의 살아있는 백과사전이에요. 알고리즘 변화, attribution 변경, beta 기능 — 다 정리해서 트위터에 올립니다.
>
> Admiral Media. €500M+ 광고 운영하면서 AI Creative Factory 만든 곳. 블로그가 진짜 좋아요. 오늘 Routine 4도 이 사람들 framework 가져왔습니다.
>
> 매일 30분만 이 셋 보세요. 1년 안에 본인 운영 능력이 두 단계 올라갑니다."

---

### 14:30–15:00 — 마무리 + 콜링

**[슬라이드 17]** *"직접 만들어보세요"* + 댓글창 캡처

**[대사]**

> "정리하겠습니다.
>
> 오늘 보여드린 시스템 — Claude routines 4개, MCP, Slack, HITL — 다 합치면 *마케터를 똑똑하고 게으르게 만드는 인프라*예요. 매일 4시간 쓰던 거 30분으로 줄이고, 그 30분을 더 깊은 의사결정에 쓰는 구조.
>
> 마지막 부탁 — 영상 보고 끝내지 마세요. 직접 만들어보세요. 막히면 댓글 남기세요. 만든 사람은 결과 공유해주세요. 학습 공동체 같이 만들어요.
>
> 다음 영상에선 routine 하나씩 처음부터 끝까지 따라하는 영상 만들 예정입니다. 어떤 routine부터 보고 싶은지 댓글로 알려주세요.
>
> 좋아요와 구독 부탁드립니다. 다음 영상에서 봐요."

---

## 슬라이드 17개 outline

1. *"똑똑하고 게으른"* 본인 이미지 (이미 있음)
2. 4분할 화면 (live capture)
3. *"이 영상은 강의가 아니에요"*
4. UI / CLI / MCP 비교표
5. OpenClaw 대안 한 줄
6. 시스템 아키텍처 다이어그램 (`routines/assets/architecture.png`)
7. Claude routines 등록 화면
8. Routine 1 Slack 메시지 캡처
9. Fatigue 시그널 4종 표
10. Routine 2 Slack 메시지 (액션 메뉴)
11. 두 attribution setting 비교 다이어그램
12. Routine 3 Slack 메시지
13. Admiral 5단계 flywheel
14. Admiral 핵심 원칙 4개
15. Routine 4 Slack 메시지
16. 글로벌 마스터 3명 카드
17. *"직접 만들어보세요"* + 댓글창

→ 별도 파일 `routines/slides.md`에 슬라이드별 디자인 디테일 정리.

---

## 영상 설명란

```
🚀 Meta Ads CLI 자동화 시스템 — 똑똑하고 게으른 마케터의 working style

✅ 챕터
00:00 후킹 — 똑똑하고 게으른 마케터
00:30 시스템 한눈에
01:00 학습 공동체 콜링
02:00 UI vs CLI vs MCP — 도구별 역할
04:00 시스템 아키텍처
05:00 Routine 1: 아침 시그널 헬스 체크
07:00 Routine 2: Fatigue + HITL
09:30 Routine 3: Attribution Setting Gap
11:30 Routine 4: Admiral Creative Flywheel
13:30 누구를 따라가야 하나
14:30 마무리

🌟 영상에서 추천한 글로벌 마스터
- Thomas Petit (@thomasbcn) — signal engineering
- Marcus Burke (@MrMarcusBurke) — Meta 광고 백과사전
- Admiral Media (admiral.media) — €500M+ ad spend, AI Creative Factory

📡 매일 보는 메타 광고 뉴스 채널
- 제가 follow하는 글로벌 메타 광고 꿀팁 큐레이션 슬랙 채널 (#meta-news, 채널 ID `C0ATU9N1XDK`).
  외부 invite 필요. 가입 희망하시면 댓글 / DM 주세요.

🔗 Reference
- Meta Ads CLI 공식: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview
- Admiral Creative Testing Framework: https://admiral.media/creative-testing-framework-mobile-apps/
- Meta Ads MCP: https://www.facebook.com/business/help/1456422242197840
- Claude Code Routines: https://code.claude.com/docs/en/routines

📚 영상에서 인용한 개념
- 코액티브 코칭의 *얼라이언스*
- 다오랩의 *학습 커뮤니티*
- *똑똑하고 게으른 마케터* (제 부트캠프 운영하면서 만든 프레임)
- Thomas Petit *signal engineering*
- Admiral Media *Creative Testing Flywheel*

#MetaAds #PerformanceMarketing #AdsCLI #ClaudeRoutines #광고자동화 #학습공동체
```

---

## iPad 텔레프롬프터 셋업 — 단계별

너 셋업 시나리오: 듀얼 모니터 + 카메라. 한 모니터엔 스크린 공유, 다른 모니터엔 프롬프트 → 시선 분산 문제.

**해결 방향: 카메라 바로 앞 또는 위에 iPad를 두고 거기서 프롬프트 읽기.** 시선이 카메라 정면이 되도록.

### 옵션 A — Speakflow (추천, 무료 ~ $20/월)

1. **앱 설치:** App Store에서 *Speakflow* 검색, 설치
2. **계정 무료 가입** — 이메일만
3. **대본 입력** — 위 v3 대본을 통째로 paste, 또는 `youtube-script-ko.md` 복사
4. **자동 스크롤 모드 켜기** — Auto-scroll 옵션. WPM 130~150 권장 (한국어 자연스러운 속도)
5. **음성 트리거 모드** (선택) — Voice-Sync 켜면 본인 음성을 따라 스크롤. 끊겨도 안 밀림.
6. **iPad를 카메라 위에 배치** — DSLR / 미러리스 렌즈 바로 위에 iPad 거치. 화면 중앙이 렌즈와 같은 높이.
7. **거치대:**
   - 가난한 자: 책 5권 쌓기 + iPad
   - 표준: Lamicall 거치대 ($15)
   - 프로: Manfrotto Magic Arm + iPad clamp ($80)
8. **시선 정면 확인** — 카메라 옆 5도 안 벗어나야 함. iPad 화면 중앙이 렌즈와 거의 일치해야 됨.

### 옵션 B — PromptSmart Pro ($20 일회성)

장점: voice-tracking 정확도 Speakflow보다 좋음.
단점: 한국어 음성인식 가끔 끊김.
나머지 셋업 동일.

### 옵션 C — 진짜 텔레프롬프터 (가장 자연스러움, $200~$500)

- **Glide Gear TMP100 ($120)** — 카메라 + iPad용 미니 텔레프롬프터. 45도 거울로 프롬프트가 렌즈 앞에 보임. 시선 = 카메라 = 프롬프트.
- **Padcaster Parrot 2 ($349)** — 더 큰 화면, 더 자연스러움.
- 셋업: Glide Gear → 카메라 렌즈 앞에 거울 부착 → iPad를 옆에 거치 → iPad가 거울에 반사돼서 카메라 앞에 글씨 보임 → 카메라는 글씨를 통과해서 본인 얼굴 찍음.

### 옵션 D — OBS PiP (네 셋업에 가장 추천)

**OBS PiP 쓰면 iPad 프롬터 안 사도 됨.** 이유:

1. OBS Studio에 카메라 + 화면 공유 두 source 추가
2. 메인 모니터에 OBS 미리보기 띄우기 — 카메라 PiP가 모니터 한 코너에 작게 떠 있음
3. **같은 모니터에 프롬프트 텍스트 (Speakflow 또는 그냥 마크다운 노트) 같이 띄움**
4. 시선이 모니터 1개에 다 머물게 됨 → 옆 모니터 안 봄 → 시선 분산 0
5. 시청자에게 송출되는 화면에는 *프롬프트는 빠지고 화면 공유 + PiP 카메라만* 노출 (별도 scene 셋업)

**시선 메커니즘:**
- 화면 공유 영상에서 시청자는 본인 얼굴이 PiP로 작게만 봄
- 시선이 정면 카메라가 아니라 *모니터 안*을 향해 있어도 시청자에겐 자연스러움 (왜냐하면 시청자 눈에 보이는 본인 얼굴이 *화면 보고 있는 사람*으로 인식됨, 그게 영상 컨텐츠랑 매칭됨)
- 토킹헤드 정면 컷이 메인인 영상은 iPad 필요. **스크린 공유 + PiP 영상은 iPad 불필요.**

**셋업 단계:**

1. OBS Studio 설치
2. 새 scene 2개:
   - `Recording`: 화면 공유 (전체 모니터) + 카메라 PiP (오른쪽 위 코너, 200×150) → 이게 송출
   - `Studio`: 같은 + 프롬프트 윈도우 → 본인이 보면서 작업, 송출엔 안 들어감
3. 메인 모니터 한쪽에 Speakflow / 마크다운 노트 (큰 글씨 24pt+) 띄움
4. 화면 한가운데 작업 (코드/슬랙/대시보드) — 시선이 자연스럽게 이쪽
5. 프롬프트는 곁눈으로 따라 읽음 (피로 적음 — 같은 모니터)
6. 카메라는 모니터 위 거치 — 시청자가 보는 PiP 본인 얼굴이 모니터 위에서 본인을 응시하는 모습

**필요 자산:**
- OBS Studio (무료)
- 카메라 (기존 사용 중인 거)
- Speakflow 앱 (또는 마크다운 + 다른 모니터 안 켜는 게 진짜 편함)

**iPad 필요한 케이스:**
- 정면 talking head 컷 (콜드 오픈, 마무리 등) — 시청자 눈에 본인 얼굴이 메인일 때
- 이 컷만 카메라 위 iPad 셋업 권장. 나머지 70%는 OBS PiP로 가능.

### 시선 함정

- 옆 모니터 보면 *명백히* 옆을 보는 사람으로 보임
- 카메라 옆 5도 미만이면 시청자가 인식 못함 (자연스러움 유지)
- 카메라 위 또는 카메라 바로 앞이 정답

### 추천 (네 셋업 기준)

너가 듀얼 모니터 쓰면서 한쪽엔 화면 공유 — 메인 모니터를 화면 공유로 두고, 카메라를 메인 모니터 위에 놓고, **iPad를 카메라 위에 놓아라**. 시선 거의 정면. 비용 $15 (거치대) + 무료 앱.

```
┌──────────────────────┐
│      iPad            │  ← 프롬프트 (Speakflow)
│   (대본 스크롤)       │
└──────────────────────┘
       [ 카메라 ]         ← DSLR / iPhone
┌──────────────────────┐
│                      │
│    메인 모니터          │  ← 화면 공유
│  (OBS 송출)           │
│                      │
└──────────────────────┘
       [ 키보드 ]
```

---

## 촬영 체크리스트

- [ ] `bash routines/scripts/setup.sh` — baseline 갱신
- [ ] vault hooks 3개 ✅
- [ ] `routines/scripts/arrange_4pane.sh` 리허설 (macOS Accessibility 권한)
- [ ] iPad에 Speakflow 설치 + 대본 paste
- [ ] iPad 거치대 카메라 위 (Lamicall 또는 책 5권)
- [ ] Slack workspace 분리 (demo 전용 — `#ads-routines` 또는 webhook 채널)
- [ ] 후킹 30초 외움 (똑똑하고 게으른)
- [ ] 슬라이드 17개 별도 파일 (`slides.md`) 보고 디자인
