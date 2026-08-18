# 참가자 워크북

## 오늘의 과제

한 기업의 최신·직전 10-K MD&A를 비교하고, 경영진 설명 중 중요한 주장을 재무 숫자·최신 사건·거시환경과 대조해 Evidence Register를 만든다.

## 0. 폴더와 환경 확인

패키지 폴더에서 터미널을 연다. Python 가상환경을 만들고 의존성을 설치한 뒤 환경 점검을 실행한다.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SEC_IDENTITY = "Your Name your-email@example.com"
$env:TAVILY_API_KEY = Read-Host "Tavily API key"
# 선택: $env:FRED_API_KEY = Read-Host "FRED API key"
python scripts\check_environment.py --require-tavily
```

### macOS Terminal

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export SEC_IDENTITY="Your Name your-email@example.com"
read -s "TAVILY_API_KEY?Tavily API key: "; export TAVILY_API_KEY; echo
# 선택: read -s "FRED_API_KEY?FRED API key: "; export FRED_API_KEY; echo
python scripts/check_environment.py --require-tavily
```

성공 기준:

- Python 3.10 이상
- EdgarTools 5.49.0
- Tavily SDK 0.7.27과 Tavily key
- SEC identity 설정
- `workspace` 쓰기 가능

## 1. 최신·직전 10-K MD&A 추출

예시 종목은 AAPL이다. 강사가 다른 ticker를 지정하면 바꾼다.

### Windows

```powershell
python scripts\extract_mdna.py --ticker AAPL
```

### macOS

```bash
python scripts/extract_mdna.py --ticker AAPL
```

생성된 파일:

```text
workspace/AAPL/filing_manifest.json
workspace/AAPL/mdna_current.md
workspace/AAPL/mdna_prior.md
workspace/AAPL/extraction_check.md
```

## 2. Gate A — 추출 결과 확인

`extraction_check.md`를 연다.

- `PASS`: 다음 단계로 이동
- `REVIEW`: SEC 원문과 시작·끝을 직접 확인한 뒤 진행 여부 결정
- `FAIL`: 분석하지 않고 강사 또는 Agent와 추출 문제 해결

직접 확인할 질문:

1. 최신과 직전 공시가 같은 회사의 연속된 회계연도인가?
2. 파일 시작 부분에 실제 Item 7 MD&A 제목이 있는가?
3. 파일 끝부분에 Item 7A·Item 8 전체가 붙어 있지 않은가?
4. manifest의 accession number와 SEC URL이 기록되어 있는가?
5. 추출 방법이 무엇인지 기록되어 있는가?

## 3. Agent 실행

패키지 루트에서 Agent를 시작한다.

```text
codex
```

또는:

```text
claude
```

첫 지시:

```text
AGENTS.md와 AGENT-PROMPTS.md를 읽어.
workspace/AAPL의 추출 결과를 대상으로 Turn 0만 실행하고 멈춰.
```

Turn마다 다음 파일을 직접 열어 확인한 후 다음 Turn을 요청한다.

| Turn | 목적 | 결과 파일 |
|---:|---|---|
| 0 | 입력과 추출 품질 점검 | 화면 보고만 수행 |
| 1 | 전년 대비 MD&A 변화 분류 | `mdna_diff.md` |
| 2 | 경영진 주장 추출 | `mdna_claims.csv` |
| 3 | 재무 숫자와 교차검증 | 갱신된 `mdna_claims.csv` |
| 4 | Tavily·FRED 외부 근거 통합 | `external_evidence.csv`, `integrated_claim_register.csv` |
| 5 | 투자·법무·회계 검토 | `role_review.md` |
| 6 | 최종 DD 메모 조립 | `mdna_review.md` |
| 7 | 사람의 원문 확인 반영 | 상태가 갱신된 register와 memo |

## 4. 외부 근거 수집

먼저 `mdna_claims.csv`에서 검증 가치가 큰 claim 하나를 고른다. 아래의 `C001`, 회사명, 날짜는 실제 값으로 바꾼다.

```text
python scripts/search_external_news.py --ticker AAPL --company "Apple Inc." --claim-id C001 --query "demand pricing margin supply regulation latest developments" --time-range month
```

FRED는 선택 트랙이다. MD&A가 금리·물가·고용·소비와 관련된 설명을 포함할 때만 관련 series를 고른다.

```text
python scripts/fetch_fred_context.py --ticker AAPL --claim-id C001 --series FEDFUNDS,CPIAUCSL,UNRATE --observation-start 2024-01-01
```

검색 결과 snippet을 사실로 확정하지 않는다. 원문 URL을 열어 출처와 날짜를 확인한다. FRED는 `context_only`이며 기업 성과의 원인으로 단정하지 않는다.

## 5. 어떤 변화를 찾을 것인가

문장 표현이 달라졌다는 사실보다 경제적 의미가 달라졌는지 본다.

- 매출 변화의 원인: 가격, 판매량, 제품 구성, 환율, M&A
- 매출총이익률과 영업이익률의 변화 원인
- 사업부문 또는 지역별 성과
- 영업현금흐름과 운전자본
- Capex와 투자 계획
- 유동성, 차입금, 만기와 자금조달
- 중요한 회계 추정
- 일회성 비용과 조정 항목
- 새로 강조되거나 사라진 불확실성
- 미래 계획과 forward-looking statement

## 6. Claim register 읽기

`mdna_claims.csv`에서 최소 다음을 확인한다.

- `management_claim`: 회사가 실제로 한 주장인가?
- `analyst_interpretation`: Agent의 해석이 분리됐는가?
- `historical_or_forward_looking`: 과거 사실과 전망이 구분됐는가?
- `current_value`, `prior_value`, `unit`: 기간과 단위가 맞는가?
- `verification_status`: 근거 수준이 과장되지 않았는가?
- `accession_number`, `source_section`: 원문으로 돌아갈 수 있는가?

## 7. Gate B — 사람이 확인할 세 주장

다음 세 종류에서 하나씩 고른다.

1. 매출·마진 등 가장 중요한 숫자 주장
2. 유동성·Capex·차입 관련 주장
3. `partial`, `needs_source` 또는 `conflict` 상태의 주장

추가로 `contradiction`이 있으면 그 원문을 우선 확인한다. Tavily 결과 URL과 FRED series의 관측 기준일도 확인한다.

manifest의 SEC URL을 열어 해당 문장과 숫자를 직접 확인한다. 확인 전에는 `verified`로 바꾸지 않는다.

## 8. 제출 기준

최종 `mdna_review.md`에는 다음 여섯 블록만 사용한다.

1. 경영진이 가장 강조한 변화
2. 실제 숫자로 확인된 주장
3. 부분적으로만 확인된 주장
4. 전년 대비 새롭게 등장한 우려
5. 공시 후 corroboration·contradiction과 context_only
6. 추가 원문 검토가 필요한 항목

투자 추천이나 목표가격은 작성하지 않는다.
