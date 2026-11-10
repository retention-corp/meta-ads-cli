# Meta Partnership Ads 운영 에이전트 가이드

이 문서는 워크숍에서 Meta Ads CLI/API로 Partnership Ads(이하 PA)를 집행할 때, 광고 생성이 반복적으로 막히는 상황을 에이전트가 안전하게 진단하고 처리하기 위한 작업 지침이다.

## 0. 결론부터 확인할 것

`PA code`는 광고주 API 토큰이 아니다. 크리에이터가 특정 콘텐츠를 파트너가 Partnership Ads로 사용할 수 있도록 발급하는 콘텐츠 사용 권한 코드다. 따라서 PA code만 있어서는 광고를 만들 수 없다.

광고 집행에는 최소한 아래 두 종류의 권한이 모두 필요하다.

```text
광고주 측
  Business Manager / Ad Account / Page / 앱 / System User token
      └─ Graph API 호출과 광고 생성 권한

크리에이터 측
  Instagram 계정 / 게시물 / Partnership Ads code
      └─ 해당 콘텐츠를 파트너 광고에 사용할 권한
```

현재 이 저장소의 루트 `meta_ads` CLI는 일반적인 Page 기반 이미지·링크 크리에이티브를 생성한다. `meta_ads/api.py`와 `meta_ads/cli.py`에는 PA code, Partnership Ads 전용 크리에이티브, 크리에이터 콘텐츠 연결 로직이 구현되어 있지 않다. 일반 크리에이티브 요청에 PA code를 임의의 필드로 끼워 넣어 해결하려고 하지 않는다.

## 1. 절대 지켜야 하는 운영 규칙

1. 토큰, PA code, 광고 계정 비밀값을 터미널 출력·로그·프롬프트·Git에 남기지 않는다.
2. 진단은 기본적으로 read-only로 시작한다.
3. 캠페인·광고 세트·광고를 만들더라도 기본 상태는 `PAUSED`로 둔다.
4. 사용자의 별도 승인 없이 `ACTIVE` 전환, 예산 변경, 결제 관련 변경을 하지 않는다.
5. 실패하면 같은 요청을 무작정 반복하지 않는다. HTTP 상태, Meta error code/subcode, message, `fbtrace_id` 또는 `x-fb-request-id`를 보존한다.
6. CLI 토큰과 MCP OAuth 세션을 섞지 않는다. 어느 계정과 어느 토큰으로 실행했는지 작업 기록에 남긴다.
7. Ads Manager 화면에서 되는 것과 API에서 되는 것은 동일한 권한·엔드포인트·검증 경로를 보장하지 않는다. 화면 성공만으로 API 성공을 주장하지 않는다.

## 2. 작업 대상과 인증 구조

이 저장소에는 서로 다른 두 CLI 경로가 있다.

| 경로 | 주요 명령 | 인증 환경변수 | 용도 |
|---|---|---|---|
| 루트 독립 CLI | `meta-ads ...` | `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`, `META_PAGE_ID` | 이 저장소의 YAML 기반 Graph API 래퍼 |
| Meta 공식 CLI | `meta ads ...` | `ACCESS_TOKEN`, `AD_ACCOUNT_ID`, 선택적 `BUSINESS_ID` | Meta 공식 Ads CLI |

두 경로의 환경변수 이름과 광고 계정 ID 형식이 다르다.

- 루트 CLI의 `META_AD_ACCOUNT_ID`는 숫자 계정 ID를 기대하고 코드에서 `act_`를 붙인다.
- 공식 CLI의 `AD_ACCOUNT_ID`는 보통 `act_123456789` 형식을 사용한다.
- 한 경로의 `.env`를 다른 경로가 자동으로 읽는다고 가정하지 않는다.

공식 CLI를 쓰는 경우에는 Meta Business Suite에서 System User를 만들고, 광고 계정과 필요한 Page·Instagram 관련 자산을 할당한 뒤, 앱과 System User의 관계 및 필요한 권한을 확인한다. 공식 CLI 설정 문서의 현재 권한·버전 요구사항을 기준으로 확인한다.

참고: [Meta Ads CLI 설정 문서](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started)

## 3. 최초 진단 순서

에이전트는 아래 순서를 지키고, 앞 단계가 실패하면 뒤의 광고 생성 단계로 넘어가지 않는다.

### 3.1 어떤 CLI가 실제로 실행되는지 확인

```bash
pwd
python3 --version
command -v meta
command -v meta-ads
meta --version 2>&1 | head -20
meta auth status 2>&1 | head -40
meta-ads --help 2>&1 | head -40
```

현재 로컬 상태에서는 `/Users/gyusupsim/.local/bin/meta`가 존재하지만, 내부 shebang이 삭제된 `meta-ads-official-cli/.venv/bin/python`을 가리키면 `bad interpreter`가 발생한다. 이 경우 PA 문제로 분류하지 말고 먼저 공식 CLI의 가상환경과 설치 상태를 복구·검증한다.

### 3.2 비밀값을 출력하지 않고 환경변수 형태 확인

```bash
python3 - <<'PY'
import os

for name in (
    "META_ACCESS_TOKEN", "META_AD_ACCOUNT_ID", "META_PAGE_ID", "META_API_VERSION",
    "ACCESS_TOKEN", "AD_ACCOUNT_ID", "BUSINESS_ID",
):
    value = os.getenv(name)
    if value is None:
        print(f"{name}=MISSING")
    elif "TOKEN" in name:
        print(f"{name}=SET(length={len(value)})")
    else:
        print(f"{name}=SET(value-shape={value[:4]}... length={len(value)})")
PY
```

`value-shape`도 실제 비밀값을 드러낼 수 있는 환경에서는 출력하지 않는다. 에이전트가 보고할 때는 `SET`, `MISSING`, `FORMAT_ERROR` 정도로만 요약한다.

확인할 항목:

- 토큰이 비어 있거나 앞뒤 공백·따옴표·줄바꿈을 포함하지 않는가
- 토큰이 해당 앱과 해당 Business/Ad Account의 것인가
- 광고 계정 ID가 올바른 계정인가
- Page ID가 크리에이터의 Instagram ID로 잘못 들어가 있지 않은가
- API 버전이 현재 Meta 지원 버전인가
- 루트 CLI와 공식 CLI의 환경변수를 혼용하고 있지 않은가

### 3.3 토큰으로 광고 계정 접근만 검증

아래는 read-only 확인 예시다. 토큰은 셸 히스토리에 남기지 않으며, 출력 전체를 공유하지 않는다.

```bash
GRAPH_VERSION="v21.0"
AD_ACCOUNT_ID="act_REDACTED_ACCOUNT_ID"

curl -sS -G "https://graph.facebook.com/${GRAPH_VERSION}/${AD_ACCOUNT_ID}" \
  --data-urlencode "fields=id,name,account_status" \
  --data-urlencode "access_token=${META_ACCESS_TOKEN}" \
  | jq 'if .error then {error: .error} else {id: .id, name: .name, account_status: .account_status} end'
```

운영 환경에서는 토큰을 명령행 인자로 직접 넣는 방식도 피하고, 공식 CLI 또는 안전한 환경 주입 방식을 사용한다. 위 예시는 구조 설명용이다.

이 단계에서 실패하면 PA code를 다시 발급받아도 해결되지 않는다. 먼저 아래를 확인한다.

- System User가 Ad Account에 할당됐는가
- 앱이 올바른 Business에 연결됐는가
- 토큰에 광고 관리 권한이 있는가
- 광고 계정이 비활성화·결제 제한·정책 제한 상태가 아닌가
- 앱 모드와 권한의 Advanced Access/App Review 상태가 필요한 경우 충족됐는가

### 3.4 Page와 Instagram 자산을 분리 확인

PA 광고에서 가장 흔한 혼동은 광고주의 Page ID, 크리에이터의 Instagram User ID, 게시물 ID를 같은 값으로 취급하는 것이다. 다음 ID를 별도로 기록한다.

```text
advertiser_business_id
advertiser_ad_account_id
advertiser_page_id
creator_instagram_user_id
creator_media_id 또는 콘텐츠 식별자
campaign_id
adset_id
creative_id
ad_id
```

에이전트는 ID 자체는 기록할 수 있지만, 토큰·PA code·전체 URL의 서명/쿼리 파라미터는 기록하지 않는다.

## 4. PA code 진단

공식 Instagram 도움말 기준으로 크리에이터가 Partnership Ads code를 생성해 파트너에게 공유하면 파트너가 해당 콘텐츠를 Partnership Ads로 부스트할 수 있다. 이 코드는 광고 API access token을 대신하지 않으며, 코드가 있다고 해서 광고주의 모든 계정이나 모든 콘텐츠에 접근할 수 있는 것도 아니다.

참고: [Create a partnership ad code to share with partners](https://www.facebook.com/help/instagram/797201308253238?locale=en_GB)

에이전트는 다음을 확인한다.

1. 코드가 실제로 해당 크리에이터 계정에서 발급됐는가
2. 코드 전달 과정에서 앞뒤 공백, 따옴표, 줄바꿈, 잘림이 생기지 않았는가
3. 코드가 만료·철회되지 않았는가
4. 광고주가 승인된 파트너로 지정됐는가
5. 사용하려는 콘텐츠가 코드가 허용하는 콘텐츠와 일치하는가
6. 크리에이터 계정, 콘텐츠, 광고주 계정이 현재 정책·제품·지역 조건을 충족하는가
7. 동일 코드를 다른 파트너가 이미 사용했거나 파트너 수 제한에 걸리지 않았는가

코드 원문을 에이전트에게 붙여 넣지 않는다. 필요하면 길이, 앞 2자와 뒤 2자만 별도 로컬 화면에서 대조하고, 로그에는 `[PA_CODE_REDACTED]`로 남긴다.

## 5. 이 저장소의 현재 구현 범위

### 지원되는 것

- 광고 이미지 업로드
- 캠페인 생성
- 광고 세트 생성
- Page 기반 표준 광고 크리에이티브 생성
- 광고 생성·조회·상태 변경
- YAML 설정 기반 실행 및 dry-run 흐름

### 지원되지 않는 것

- PA code를 받는 CLI 인자
- Partnership Ads 전용 creative payload
- 크리에이터의 Instagram 콘텐츠를 PA creative로 연결하는 검증
- creator authorization 상태 조회
- Ads Manager의 Partnership Ads 전용 UI 흐름을 API로 재현하는 기능

따라서 현재 루트 CLI에 다음처럼 임의의 인자를 추가해서는 안 된다.

```bash
# 이런 식의 임의 인자는 현재 구현되어 있지 않다.
meta-ads create campaign.yaml --pa-code "..."
```

PA 전용 API 스키마와 현재 API 버전을 공식 Meta 개발자 문서에서 확인한 뒤, 별도 어댑터를 추가하거나 공식 CLI가 지원하는 공식 명령으로 연결해야 한다. 필드명과 엔드포인트를 기억에 의존해 추정하지 않는다. 특히 표준 `object_story_spec`에 PA code를 임의로 합치는 방식은 금지한다.

## 6. 안전한 생성 절차

실제 광고를 만들 때는 다음 단계별로 멈추고 결과를 확인한다.

```text
read-only 계정/권한 확인
        ↓
크리에이터·콘텐츠·PA code 관계 확인
        ↓
PA 전용 endpoint/payload 스키마 확인
        ↓
PAUSED 캠페인 생성
        ↓
PAUSED 광고 세트 생성
        ↓
PAUSED PA creative 생성
        ↓
PAUSED 광고 생성
        ↓
Ads Manager와 API의 ID/검수 상태 대조
        ↓
사용자의 명시적 승인 후에만 ACTIVE
```

각 단계에서 다음을 기록한다.

- 사용한 API 버전
- 실제 사용한 CLI 경로
- 광고 계정·Business·Page·Instagram·콘텐츠 ID
- endpoint 경로와 HTTP method
- 토큰·PA code를 제거한 요청 payload
- HTTP status
- Meta error type, code, subcode, message
- `fbtrace_id` 또는 `x-fb-request-id`
- 생성된 객체 ID와 현재 `effective_status`

실패가 난 상태에서 캠페인이나 광고 세트를 삭제하거나 재생성하지 않는다. 먼저 객체가 부분 생성됐는지 조회한다.

## 7. 오류 분류표

| 증상 | 우선 의심할 원인 | 다음 조치 |
|---|---|---|
| `bad interpreter`, CLI 실행 불가 | 깨진 venv/shebang, PATH 충돌 | 실제 실행 파일과 Python venv 복구 후 버전 확인 |
| Invalid OAuth access token | 만료·철회·잘못된 토큰·환경변수 혼용 | 토큰 출처와 Business/App/System User를 재확인 |
| Permission error, code 200/권한 관련 오류 | 앱 권한·자산 할당·Advanced Access 부족 | `/me`·광고 계정 접근과 Business 자산 할당을 분리 확인 |
| Invalid parameter, code 100 | 잘못된 endpoint·API 버전·payload·ID | PA 전용 현재 스키마와 ID 관계 재검증 |
| Object not found | 크리에이터 콘텐츠가 토큰에 보이지 않음, ID 혼동 | Page ID/Instagram User ID/media ID를 분리 확인 |
| PA code invalid/expired/revoked | 코드 상태나 파트너 승인 문제 | 크리에이터가 새 코드를 발급하고 광고주를 다시 승인 |
| Creative validation/unsupported | 콘텐츠 형식·목표·배치 조합 제한 | 지원 목표·배치와 콘텐츠 유형 확인; 임의 재시도 금지 |
| Rate limit | 호출 과다 또는 병렬 재시도 | exponential backoff; 중복 생성 여부 먼저 조회 |
| Ads Manager는 되지만 API는 실패 | UI와 API의 권한/검증 경로 차이 | 같은 계정·크리에이터·콘텐츠로 request ID 포함 비교 |
| 광고는 생성됐지만 전달 안 됨 | 검수·정책·결제·계정 상태 | `effective_status`, delivery, policy, billing 상태를 따로 확인 |

## 8. 에이전트가 남겨야 하는 실패 보고

아래 형식을 그대로 사용한다.

```text
[Meta PA 진단 결과]
시각(KST): YYYY-MM-DD HH:MM
실행 경로: root meta_ads CLI | official meta CLI | direct Graph API
API version: vX.Y
Business ID: 확인됨/미확인
Ad Account ID: act_... 뒤 4자리만
Advertiser Page ID: 확인됨/미확인
Creator Instagram ID: 확인됨/미확인
Content/Media ID: 확인됨/미확인
PA code: 제공됨/미제공/형식만 확인/검증 실패

요청:
  method: POST/GET
  endpoint: /REDACTED_PATH
  payload: 토큰·PA code 제거본

응답:
  HTTP status:
  Meta error type:
  Meta code:
  Meta subcode:
  message:
  fbtrace_id 또는 x-fb-request-id:

현재 판단:
  - 재현됨/미재현
  - 인증 문제/자산 권한 문제/PA code 문제/payload 문제/정책·결제 문제/CLI 런타임 문제

다음 1개 조치:
  - 예: 크리에이터에게 PA code 재발급 요청
  - 예: System User에 Ad Account와 Page 자산 할당
  - 예: 공식 문서 기준 PA creative payload 확인 후 PAUSED dry-run 추가
```

오류 message를 그대로 공유해야 할 때도 access token, PA code, 쿠키, Authorization header, 서명된 URL은 반드시 마스킹한다.

## 9. 구현을 요청받았을 때의 개발 지침

에이전트가 코드 수정까지 맡게 되면 다음 순서를 따른다.

1. 먼저 정확한 실패 요청과 응답을 확보한다.
2. 현재 Meta 문서에서 PA 전용 endpoint, 필수 필드, 지원 API 버전, 필요한 권한을 확인한다.
3. 표준 크리에이티브 경로와 PA 크리에이티브 경로를 분리한다.
4. `partnership_ad_code` 같은 필드명은 문서에서 확인된 경우에만 사용한다.
5. 기본값은 `PAUSED`와 `dry_run`으로 둔다.
6. 토큰·코드가 예외 메시지와 디버그 로그에 들어가지 않도록 redaction 테스트를 추가한다.
7. 기존 일반 광고 YAML과 CLI 동작을 깨지 않는 회귀 테스트를 추가한다.
8. read-only 조회, dry-run payload 검증, PAUSED 생성 검증 순으로 테스트한다.
9. 실제 활성화는 코드 수정의 완료 조건으로 간주하지 않는다. 별도 승인과 Ads Manager/API 상태 확인이 필요하다.

권장 인터페이스 예시는 다음과 같다. 실제 필드명은 Meta 공식 스키마 확인 후 확정한다.

```python
create_partnership_creative(
    *,
    creator_instagram_user_id: str,
    content_id: str,
    partnership_code: str,
    page_id: str | None = None,
    status: str = "PAUSED",
)
```

이 인터페이스를 바로 구현하지 말고, 먼저 현재 API가 요구하는 creator/content 식별자와 code 전달 방식을 확인한다.

## 10. 에이전트에게 그대로 전달할 작업 지시문

```text
이 문서를 먼저 읽고 Meta Partnership Ads 막힘을 진단하라.

1. root meta_ads CLI와 official meta CLI 중 실제 실행 경로를 식별하라.
2. 토큰·PA code 원문을 출력하지 말고 인증, Business/Ad Account/Page/Instagram 자산 접근을 read-only로 확인하라.
3. PA code는 API access token이 아니라 creator content authorization임을 전제로 진단하라.
4. 현재 저장소의 표준 creative 생성 코드에 PA code가 지원되는지 확인하라. 지원되지 않으면 임의 필드 추가나 표준 payload 변형으로 우회하지 말라.
5. 실패 endpoint, HTTP status, Meta code/subcode/message, fbtrace_id를 마스킹된 형태로 남겨라.
6. 부분 생성된 캠페인·광고 세트·광고가 있는지 조회하라.
7. 해결 전에는 ACTIVE 전환, 예산 변경, 결제 변경을 하지 말라.
8. 마지막에는 원인 분류 1개, 증거, 다음 조치 1개만 명확하게 보고하라.
```

## 로컬 참고 파일

- `meta_ads/api.py`: 루트 CLI가 호출하는 Graph API 래퍼
- `meta_ads/cli.py`: 루트 CLI 명령과 환경변수 로딩
- `README.md`: 기존 독립 CLI 설정 문서
- `cli-vs-mcp.md`: CLI와 MCP의 인증·용도 차이
- `meta-ads-official-cli/README.md`: Meta 공식 CLI 사용법

