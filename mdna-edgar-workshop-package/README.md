# EDGAR MD&A Evidence-to-Claim Lab

최신·직전 10-K의 MD&A를 추출하고, 경영진의 설명을 재무 숫자·최신 사건·거시환경과 대조하는 실습 패키지다. 투자·법무·회계 전문직이 Claude Code 또는 Codex와 함께 27분 집중 실습이나 60분 독립 수업으로 사용할 수 있다.

핵심 구조는 “API 키 하나를 EdgarTools에 끼우는 방식”이 아니다. 세 소스의 역할을 분리한다.

```text
EDGAR / EdgarTools ── 회사의 공식 주장·공시 숫자 ── primary verification
Tavily ───────────── 공시 후 최신 사건·반대 근거 ── corroboration / contradiction
FRED(선택) ───────── 금리·물가·고용 등 거시환경 ── context_only
                                      ↓
                          Integrated Evidence Register
                                      ↓
                                 Human Gate
```

Tavily 결과는 원문 후보를 찾는 탐색 근거이고, FRED의 동행성은 개별 기업의 인과관계를 증명하지 않는다.

## 실습 결과물

실습을 마치면 `workspace/<TICKER>/` 아래에 다음 파일이 생긴다.

```text
filing_manifest.json       공시 식별정보와 추출 방법
mdna_current.md            최신 10-K Item 7
mdna_prior.md              직전 10-K Item 7
extraction_check.md        섹션 경계와 품질 점검
mdna_diff.md               전년 대비 서술 변화
mdna_claims.csv            주장–숫자–근거 register
tavily_evidence.json       공시 후 최신 사건 검색 결과
fred_context.json          선택한 공식 거시 시계열
external_evidence.csv      외부 근거의 역할·방향 검토
integrated_claim_register.csv  SEC·뉴스·거시 근거 통합표
role_review.md             투자·법무·회계 관점 검토
mdna_review.md             최종 1페이지 DD 메모
```

## 패키지 구성

```text
README.md                   빠른 시작
INSTRUCTOR-GUIDE.md         강사용 진행안과 시간표
PARTICIPANT-WORKBOOK.md     참가자용 단계별 워크북
AGENT-PROMPTS.md            Claude Code·Codex용 단계별 프롬프트
REVIEW-CHECKLIST.md         제출 전 Human Gate
TROUBLESHOOTING.md          설치·추출 오류 대응
SOURCES.md                  공식 참고자료
VERIFICATION.md             패키지 실행 검증 기록
AGENTS.md                   Codex 등 Agent가 읽는 프로젝트 규칙
CLAUDE.md                   Claude Code 진입 지침
requirements.txt            검증된 Python 의존성
.env.example                참가자가 복사해 한 번만 수정하는 설정 양식
scripts/check_environment.py
scripts/setup_env.py         .env을 안전하게 생성
scripts/env_loader.py        모든 실습 스크립트의 공통 설정 로더
scripts/extract_mdna.py
scripts/search_external_news.py
scripts/fetch_fred_context.py
templates/                  분석 산출물 템플릿
sample-output/              형식 예시
workspace/                  참가자 실행 결과 저장 위치
```

## 준비물

- Windows 10/11 PowerShell 또는 macOS Terminal
- Python 3.10 이상. 수업 환경은 Python 3.12 권장
- Claude Code 또는 Codex 중 하나
- 인터넷 연결
- SEC 요청 식별에 사용할 실제 이름과 이메일
- Tavily API key
- FRED API key(거시환경 선택 트랙)

EDGAR와 EdgarTools는 별도 API key를 요구하지 않으며 SEC 요청에는 연락 가능한 identity가 필요하다. 참가자는 `.env.example`을 복사해 만든 `.env` **한 파일만** 수정한다. 모든 스크립트가 이 파일을 자동으로 읽으며 `.env`는 Git에서 제외된다. `.env.example`에는 변수 이름과 빈 자리만 남긴다. 앱 시크릿·증권사 계좌·개인 API key를 프롬프트·소스 코드·Git에 입력하지 않는다.

## 한 파일 설정 원리

```text
.env.example ── setup_env.py ──→ .env (참가자가 여기만 수정)
                                      ↓ 자동 로드
              EDGAR · Tavily · SerpAPI · FRED 실습 스크립트
```

`.env`에는 `SEC_IDENTITY`, `TAVILY_API_KEY`, 선택형 `SERPAPI_KEY`, `FRED_API_KEY`를 적는다. 운영체제에 이미 같은 이름의 환경 변수가 있으면 그 값이 우선하며 `.env` 값으로 덮어쓰지 않는다. 키 값은 화면에 출력하거나 제출 파일에 복사하지 않는다.

## Windows PowerShell 빠른 시작

패키지 폴더에서 실행한다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\setup_env.py
notepad .env
python scripts\check_environment.py --require-tavily
python scripts\extract_mdna.py --ticker AAPL
python scripts\search_external_news.py --ticker AAPL --company "Apple Inc." --claim-id C001 --query "demand pricing margin supply regulation latest developments"
# 선택: python scripts\fetch_fred_context.py --ticker AAPL --claim-id C001 --series FEDFUNDS,CPIAUCSL,UNRATE --observation-start 2024-01-01
```

PowerShell이 가상환경 활성화를 차단할 때만 현재 창에 한해 다음을 먼저 실행한다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## macOS Terminal 빠른 시작

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/setup_env.py
open -e .env
python scripts/check_environment.py --require-tavily
python scripts/extract_mdna.py --ticker AAPL
python scripts/search_external_news.py --ticker AAPL --company "Apple Inc." --claim-id C001 --query "demand pricing margin supply regulation latest developments"
# 선택: python scripts/fetch_fred_context.py --ticker AAPL --claim-id C001 --series FEDFUNDS,CPIAUCSL,UNRATE --observation-start 2024-01-01
```

## Agent 시작

추출이 끝난 뒤 패키지 루트에서 Claude Code 또는 Codex를 실행한다.

```text
Codex:       codex
Claude Code: claude
```

첫 지시는 다음과 같이 한다.

```text
AGENTS.md와 AGENT-PROMPTS.md를 읽어.
workspace/AAPL의 filing_manifest.json과 extraction_check.md를 먼저 검사하고,
PASS가 아니면 분석을 시작하지 마.
PASS이면 AGENT-PROMPTS.md의 Turn 1부터 순서대로 진행해.
```

## 실습 원칙

1. 최신 10-K와 직전 10-K를 함께 본다.
2. 10-K의 MD&A는 일반적으로 Part II, Item 7이다.
3. Item 7 추출 결과에 Item 7A·Item 8이 섞였는지 먼저 확인한다.
4. 경영진의 주장과 Agent의 해석을 분리한다.
5. 숫자는 재무제표의 기간·단위·부호와 함께 검증한다.
6. 근거가 없으면 추론하지 않고 `needs_source`로 남긴다.
7. 외부 근거에는 `primary_verification`, `corroboration`, `contradiction`, `context_only`, `unresolved` 중 역할을 붙인다.
8. FRED와 기업 성과가 함께 움직여도 회사별 인과관계로 단정하지 않는다.
9. 최종 판단 전에 사람이 중요한 주장 3개를 원 출처에서 확인한다.

## 교육용 안전 범위

이 패키지는 공시 분석 교육용이다. 투자 추천, 법률 의견, 회계감사 결론 또는 자동매매 지시를 생성하지 않는다. SEC 원문과 회사 공시는 최종적으로 사람이 직접 확인한다.

공식 문서와 테스트 환경은 `SOURCES.md`, `VERIFICATION.md`에서 확인한다.
