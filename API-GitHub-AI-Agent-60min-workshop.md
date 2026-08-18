# API × MCP × GitHub × AI Agent

## 공식 데이터를 업무 도구로 바꾸는 60분 실습

**대상:** 투자업계·변호사·회계사 등 비개발자 전문직  
**도구:** Claude Code 또는 Codex 중 하나, Git, Python, Tavily, 선택형 FRED, EdgarTools  
**환경:** Windows 10/11 PowerShell 또는 macOS Terminal  
**문서 기준일:** 2026-08-18  
**결과물:** 실제 상장사의 최신 10-K를 바탕으로 한 출처 추적형 DD 메모

> 오늘의 핵심은 코드를 외우는 것이 아니다. 공식 데이터와 오픈소스 도구를 찾아서, AI Agent에게 안전하게 연결하고, 결과의 출처를 검증하는 방법을 익히는 것이다.

---

## 1. 오늘 끝나면 할 수 있는 것

교육 종료 시 참가자는 다음 작업을 직접 수행한다.

1. API가 무엇인지 업무 언어로 설명한다.
2. API와 MCP의 역할 차이와 연결 관계를 설명한다.
3. 증권사 API가 시세·잔고·주문·체결을 어떻게 연결하는지 설명한다.
4. 웹 검색 결과와 공식·구조화 API 데이터를 구분한다.
5. Tavily API key를 안전하게 연결하고, 선택 실습에서 FRED API key로 거시지표를 가져온다.
6. 공개 GitHub 저장소를 `git clone`으로 내려받아 AI Agent에게 설명시킨다.
7. EdgarTools로 실제 기업의 최신 10-K와 재무제표를 가져온다.
8. EDGAR·Tavily·FRED 근거를 하나의 Evidence Register로 통합한다.
9. 투자·법무·회계 관점의 DD 메모를 만들고, 주장마다 원문 근거를 확인한다.

### 60분 시간표

| 시간 | 주제 | 참가자 행동 | 산출물 |
|---:|---|---|---|
| 0–6분 | API란 무엇인가 | 요청·응답 구조 이해 | API 한 문장 정의 |
| 6–9분 | API와 MCP | 코드 연결과 Agent 연결 비교 | API–MCP 관계도 |
| 9–12분 | 증권사 주문 API | 모의투자 주문 흐름과 통제 지점 확인 | 주문 생명주기 도식 |
| 12–16분 | 왜 API인가 | 웹 검색과 공식 데이터 비교 | Source-of-Truth 원칙 |
| 16–25분 | 대표 API와 검색 API | Tavily로 첫 검색, FRED 구조 확인 | 검색 결과 JSON |
| 25–33분 | Git/GitHub | 저장소 clone·상태 확인 | 로컬 저장소 |
| 33–41분 | EdgarTools MD&A pack | 최신·직전 10-K Item 7과 재무 숫자 추출 | MD&A 2종과 manifest |
| 41–49분 | Hybrid evidence | Tavily 최신 사건과 FRED 거시맥락 수집 | 외부근거 JSON 2종 |
| 49–58분 | AI Agent DD sprint | 세 근거를 통합하고 반론·직군 검토 | Evidence Register와 DD 초안 |
| 58–60분 | 사람의 검증 | 표본 원문 대조와 최종 승인 | 검증된 Markdown 보고서 |

> 설치는 본 교육 전에 완료한다. 현장 설치가 필요하면 아래 “사전 준비” 절차를 사용한다.

---

# 2. 사전 준비

## 2.1 준비물과 계정

- 인터넷 연결과 소프트웨어 설치 권한
- Claude Code 또는 Codex를 사용할 수 있는 계정 하나
- 기본 검색 API 계정: [Tavily](https://app.tavily.com)
- 선택 거시경제 API 계정: [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)
- SEC 요청 식별에 사용할 실제 이름과 이메일
- 약 2 GB 이상의 여유 저장공간

GitHub 계정은 **공개 저장소를 clone하는 데 필요하지 않다.** 회사 장비라면 오픈소스 사용, 외부 API 접속, AI 도구 사용에 관한 내부 정책을 먼저 확인한다.

## 2.2 설치 경로 선택

이 교안은 다음 두 경로를 지원한다.

- **Windows:** Windows PowerShell에서 네이티브 실행
- **macOS:** Terminal에서 실행

Claude Code와 Codex를 둘 다 설치할 필요는 없다. 이미 사용할 수 있는 도구 하나만 선택한다. Windows의 WSL은 좋은 대안이지만, 수업 중 경로 혼선을 줄이기 위해 이 교안의 기본 경로에서는 사용하지 않는다.

---

## 2.3 Windows 10/11 — PowerShell 설정

### A. PowerShell 열기

시작 메뉴에서 **PowerShell** 또는 **Windows Terminal**을 연다. 프롬프트가 `PS C:\...>`로 보이면 맞다. 일반적인 사용자 설치에는 관리자 권한이 필요하지 않지만, 회사 정책에 따라 승인이 필요할 수 있다.

### B. 현재 상태 확인

아래 명령은 한 줄씩 실행한다. 오류가 나는 항목만 설치한다.

```powershell
winget --version
git --version
py --version
codex --version
claude --version
```

`codex`와 `claude`는 선택 사항이므로 둘 중 하나만 성공하면 된다.

### C. Git 설치

```powershell
winget install --id Git.Git -e --source winget
```

설치 후 PowerShell을 닫았다가 다시 열고 확인한다.

```powershell
git --version
```

### D. Python 3.12 설치

Python Install Manager를 설치하고 PowerShell을 다시 연다.

```powershell
winget install 9NQ7512CXL7T -e --accept-package-agreements --accept-source-agreements
```

그다음 Python 3.12 런타임을 설치하고 확인한다.

```powershell
py install 3.12
py -V:3.12 --version
py -V:3.12 -m pip --version
```

### E-1. Codex를 선택한 경우

OpenAI의 Windows용 설치 스크립트를 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

PowerShell을 다시 열고 확인한다.

```powershell
codex --version
codex
```

처음 실행하면 화면 안내에 따라 로그인한다. 설치 스크립트 실행이 회사 정책상 제한되면 [Codex 공식 저장소](https://github.com/openai/codex)의 Windows 설치 안내 또는 조직에서 승인한 배포 방식을 사용한다.

### E-2. Claude Code를 선택한 경우

```powershell
winget install Anthropic.ClaudeCode -e
```

PowerShell을 다시 열고 확인한다.

```powershell
claude --version
claude doctor
claude
```

처음 실행하면 화면 안내에 따라 로그인한다.

### F. 실습 폴더와 가상환경 만들기

강사는 배포 전에 `<WORKSHOP_REPOSITORY_URL>`을 패키지를 올린 실제 GitHub URL로 바꾼다. ZIP으로 배포하면 압축을 푼 `mdna-edgar-workshop-package` 폴더로 이동한 뒤 `git clone` 두 줄 다음부터 실행한다.

```powershell
New-Item -ItemType Directory -Force "$HOME\Documents\api-git-ai-workshop" | Out-Null
Set-Location "$HOME\Documents\api-git-ai-workshop"
git clone <WORKSHOP_REPOSITORY_URL> mdna-evidence-lab
Set-Location mdna-evidence-lab
py -V:3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

확인:

```powershell
git log -1 --oneline
python --version
python -c "import edgar, tavily; print('READY')"
```

마지막 줄에 `READY`가 나오면 준비 완료다.

---

## 2.4 macOS — Terminal 설정

### A. Terminal 열기와 현재 상태 확인

Spotlight에서 **Terminal**을 열고 아래 명령을 실행한다.

```bash
git --version
python3 --version
codex --version
claude --version
```

`codex`와 `claude`는 둘 중 하나만 성공하면 된다. Python이 3.10 이상이면 기존 버전을 사용할 수 있지만, 수업 환경을 맞추려면 3.12를 권장한다.

### B. Git 준비

`git`이 없으면 Apple Command Line Tools를 설치한다.

```bash
xcode-select --install
```

설치 창을 완료한 뒤 확인한다.

```bash
git --version
```

### C. Python 3.12 준비

Homebrew가 있으면 다음을 실행한다.

```bash
brew --version
brew install python@3.12
python3.12 --version
```

Homebrew가 없다면 먼저 <https://brew.sh>의 공식 설치 명령을 사용하고 Terminal을 다시 연 뒤 위 명령을 실행한다. 회사 장비에서 Homebrew 설치가 제한되면 <https://www.python.org/downloads/macos/>의 공식 설치 프로그램을 사용한다.

### D-1. Codex를 선택한 경우

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex --version
codex
```

처음 실행하면 화면 안내에 따라 로그인한다.

### D-2. Claude Code를 선택한 경우

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
claude doctor
claude
```

처음 실행하면 화면 안내에 따라 로그인한다.

### E. 실습 폴더와 가상환경 만들기

강사는 배포 전에 `<WORKSHOP_REPOSITORY_URL>`을 패키지를 올린 실제 GitHub URL로 바꾼다. ZIP으로 배포하면 압축을 푼 `mdna-edgar-workshop-package` 폴더로 이동한 뒤 `git clone` 두 줄 다음부터 실행한다.

```bash
mkdir -p ~/Documents/api-git-ai-workshop
cd ~/Documents/api-git-ai-workshop
git clone <WORKSHOP_REPOSITORY_URL> mdna-evidence-lab
cd mdna-evidence-lab
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

확인:

```bash
git log -1 --oneline
python --version
python -c "import edgar, tavily; print('READY')"
```

마지막 줄에 `READY`가 나오면 준비 완료다.

---

## 2.5 AI Agent에게 환경 진단과 설정을 맡기는 프롬프트

Claude Code 또는 Codex를 실습 폴더에서 실행한 뒤 아래 프롬프트를 그대로 붙여 넣는다. Agent 자체 설치 전에는 앞의 수동 절차가 필요하다.

```text
이 컴퓨터를 “API × MCP × GitHub × AI Agent” 교육 실습 환경으로 준비해줘.

먼저 아무것도 설치하거나 수정하지 말고 다음을 진단해서 표로 보고해:
- 운영체제, 버전, CPU 아키텍처, 현재 shell
- Git과 Python의 설치 경로 및 버전
- Python 3.10 이상 여부, pip와 venv 사용 가능 여부
- 현재 폴더가 강사가 배포한 mdna-evidence-lab Git 저장소인지 여부
- .venv 존재 및 활성화 여부
- edgartools와 tavily-python import 가능 여부
- Claude Code 또는 Codex 중 현재 실행 중인 Agent

그 다음, 부족한 항목만 설치·설정하는 명령을 운영체제에 맞게 제안해.
Windows에서는 PowerShell 명령을, macOS에서는 Terminal(zsh) 명령을 사용해.
시스템 수준 설치나 실행 정책 변경은 명령과 영향을 먼저 설명하고 내 승인을 받은 뒤 실행해.
기존 정상 설치는 업그레이드하거나 제거하지 마.
프로젝트 의존성은 반드시 현재 저장소의 .venv 안에만 설치해.

준비가 끝나면 다음 검증을 실제로 실행하고 성공/실패를 표로 정리해:
- git --version
- python --version
- python -m pip --version
- python -c "import edgar, tavily; print('READY')"

API 키를 묻거나 출력하거나 파일에 저장하지 마. 키가 필요하면 내가 별도 터미널에서 세션 환경 변수로 설정하도록 명령만 알려줘.
```

이 프롬프트의 포인트는 **진단 → 변경 제안 → 승인 → 검증** 순서다. Agent가 무엇이든 바로 설치하게 두지 않는다.

---

# 3. Part 1 — API란 무엇인가? (0–6분)

## 한 문장 정의

> **API(Application Programming Interface)는 프로그램끼리 정해진 방식으로 요청과 응답을 주고받는 창구다.**

식당에 비유하면 다음과 같다.

| 식당 | 데이터 업무 |
|---|---|
| 손님 | 사용자 또는 AI Agent |
| 메뉴 | API 문서와 사용 가능한 기능 |
| 주문 | Request: 무엇을 달라는 요청 |
| 직원 | API: 정해진 요청을 전달하는 창구 |
| 주방 | 데이터베이스 또는 서비스 |
| 음식 | Response: JSON 등 정해진 형식의 결과 |

```text
사람의 요구
   ↓
AI Agent가 요청 코드 작성·실행
   ↓
API ──→ 데이터 제공기관
   ↓
구조화된 응답(JSON 등)
   ↓
분석·표·보고서
```

## API가 연결하는 두 종류: 데이터와 서비스

S&P Global·Bloomberg·SEC EDGAR 같은 외부 기관은 **데이터**를 제공하고, Notion·Google Docs·특수 알고리즘 같은 외부 시스템은 문서 생성·저장·계산 같은 **기능**을 제공한다. 우리 코드나 AI Agent는 각 기관의 내부 시스템에 직접 들어가는 대신, 그 기관이 공개한 API의 규칙에 맞춰 요청하고 결과를 받는다.

```text
우리의 업무 도구                  API 연결 규칙                   제3자의 자원

Python · Excel        ── Request: 조회·생성·계산 ──→     [데이터]
사내 앱 · AI Agent             주소(endpoint)              S&P Global
                               인증 방식                    Bloomberg
                               요청 형식                    SEC EDGAR
                               응답 형식
                     ←─ Response: JSON·결과·상태 ──       [서비스]
                                                           Notion
                                                           Google Docs
                                                           특수 알고리즘
```

수업에서는 다음 문장으로 정리한다.

> **API는 제3자의 데이터와 서비스 자체가 아니라, 우리 프로그램이 그것을 요청하고 결과를 받기 위해 서로 약속한 연결 창구다.**

기술적으로 API와 통신 프로토콜은 완전히 같은 말은 아니다. API가 “어떤 요청을 보내고 어떤 결과를 받는가”라는 인터페이스 규칙이라면, 실제 인터넷 통신에는 보통 HTTPS 같은 프로토콜이 사용된다. 입문 단계에서는 **API = 프로그램 사이의 정해진 통신 방법**이라고 기억해도 충분하다.

예를 들어 “AAPL의 최근 10-K를 찾아줘”라는 요구는 다음과 같이 바뀐다.

```text
Request:  회사 식별자 + 공시 유형 10-K
Response: 제출일, accession number, 원문 위치, XBRL 재무 데이터
```

### 꼭 구분할 것

- **API**는 데이터를 전달하는 방식이다.
- **데이터의 신뢰도**는 그 API의 운영 주체와 원천에 달려 있다.
- API로 받았다는 사실만으로 공식 데이터가 되는 것은 아니다.

---

# 4. Part 2 — API와 MCP, 그리고 실제 주문 연결 (6–12분)

## 4.1 수업용 기억법

> **API는 프로그램과 서비스를 연결하고, MCP는 AI Agent와 도구를 연결한다.**

“API는 코드에 넣고, MCP는 Agent에 넣는다”는 설명은 비개발자가 차이를 기억하기에 매우 유용하다. 다만 기술적으로는 다음처럼 조금 더 정확하게 이해한다.

| 구분 | API | MCP |
|---|---|---|
| 핵심 역할 | 특정 서비스의 기능·데이터를 호출하는 인터페이스 | AI 애플리케이션이 도구·데이터를 발견하고 사용하는 표준 프로토콜 |
| 주된 사용자 | 코드, 앱, 자동화 프로그램, Agent | Claude Code·Codex 같은 MCP client를 가진 AI 애플리케이션 |
| 연결 대상 | 웹 서비스, 데이터베이스, 사내 시스템 | MCP server가 공개한 tools·resources·prompts |
| 사용자가 준비할 것 | API 문서, endpoint, 인증 방식, 호출 코드 | MCP server 설정, 권한, 연결할 데이터·도구 |
| 결과 | 서비스별 형식의 응답 | Agent가 이해할 수 있는 공통 방식의 기능·자료 목록과 실행 결과 |

```text
API 방식
사람 → 코드·앱 → 서비스 API → 데이터 또는 기능

MCP 방식
사람 → AI Agent(MCP client) → MCP server → API·파일·DB·업무 도구
```

## 4.2 둘은 경쟁 관계가 아니다

MCP는 기존 API를 없애는 기술이 아니다. 실제로 많은 MCP server는 내부에서 기존 API를 호출하고, 그 기능을 Agent가 발견하고 사용할 수 있는 `tool` 형태로 바꿔 제공한다.

예를 들어 검색 서비스를 연결할 때 다음 두 방식이 모두 가능하다.

```text
직접 API 연결
내 Python 코드 → Tavily 또는 SerpAPI → 검색 결과 JSON

MCP 연결
Claude Code·Codex → 검색 MCP server → Tavily·SerpAPI 등 → Agent가 결과 사용
```

### 꼭 구분할 것

- API도 Agent가 직접 호출할 수 있고, MCP도 결국 코드로 구현된다.
- MCP server가 API 키·권한·보안을 자동으로 해결해 주는 것은 아니다.
- 같은 도구를 여러 Agent에서 일관된 방식으로 쓰고 싶을 때 MCP가 특히 유용하다.
- 단발성 스크립트나 서비스 고유 기능을 세밀하게 제어할 때는 직접 API 호출이 더 단순할 수 있다.

### 강사용 확인 질문

> “MCP server가 SEC API를 감싸서 `get_latest_10k`라는 tool을 제공한다면, 참가자는 endpoint를 외우는 대신 Agent에게 무엇을 요청하면 될까요?”

예상 답: “AAPL의 최신 10-K를 가져오고 원문 위치를 알려줘”처럼 **업무 언어로 tool 사용을 요청한다.**

## 4.3 증권사 API는 실제로 무엇까지 할 수 있나? — 한국투자증권 Open API 예시

한국투자증권의 공식 `open-trading-api` 저장소는 국내·해외 주식 등의 시세와 계좌, 주문·정정·취소, 체결내역, WebSocket 실시간 데이터 예제를 제공한다. LLM용 기능별 샘플과 MCP 예제도 포함되어 있어 “API 호출”과 “Agent 도구 연결”을 한 사례에서 함께 설명하기 좋다.

### 예시: 삼성전자 1주를 지정가로 모의 매수한다면

아래 흐름의 핵심은 **주문 요청, 증권사 접수, 거래소 체결을 서로 다른 사건으로 보는 것**이다.

```text
사용자·Agent        승인·통제        KIS REST API       증권사 주문시스템         KRX
     │                  │                  │                     │                 │
     │─ 주문안 ────────→│                  │                     │                 │
     │  005930·매수 1주 │                  │                     │                 │
     │  승인받은 지정가  │                  │                     │                 │
     │                  │─ 한도·중복 검사 ─→│                     │                 │
     │                  │                  │─ 주문 요청 ─────────→│─ 시장 전달 ────→│
     │                  │                  │← 주문 접수·주문번호 ─│                 │
     │← 접수 결과 ─────────────────────────│                     │                 │
     │                  │                  │                     │← 호가 매칭 ─────│
     │← 체결·부분체결·미체결 조회 ──────────│← 체결 결과 ──────────│                 │
     │─ 현금·보유수량 재조회 및 대사 ──────→│                     │                 │
```

> **HTTP 200 또는 API 성공은 “요청을 받았다”는 뜻이지 전량 체결을 뜻하지 않는다.** 주문번호를 기록한 뒤 체결 수량·가격과 계좌 잔고를 별도로 확인해야 한다.

공식 샘플에서 사용하는 대표 함수와 구분값은 다음과 같다.

| 단계 | 공식 샘플의 예 | 수업에서 강조할 점 |
|---|---|---|
| 인증 | `ka.auth(svr="vps", product="01")` | `vps` 모의투자만 사용하고 실전 `prod`와 설정을 분리 |
| 시세 조회 | `inquire_price(...)` | 주문 전 종목코드·현재가·호가를 확인 |
| 현금 주문 | `order_cash(env_dv="demo", ord_dv="buy", ...)` | `demo` 여부, 계좌·종목·수량·가격을 다시 검증 |
| 사후 확인 | 주문 응답·체결내역·잔고 조회 | 요청 성공과 실제 체결은 다른 상태임을 구분 |

공식 국내주식 현금주문 샘플의 입력을 교육용으로 단순화하면 다음과 같다. 실제 키·토큰·계좌번호와 당시 시장 가격은 교안이나 프롬프트에 넣지 않는다.

| 의미 | 샘플 입력 | 교육용 값 |
|---|---|---|
| 실행 환경 | `env_dv` | `demo` — 모의투자 |
| 주문 방향 | `ord_dv` | `buy` |
| 종목코드 | `PDNO`에 대응 | `005930` |
| 주문 방식 | `ORD_DVSN`에 대응 | `00` — 지정가 |
| 수량 | `ORD_QTY`에 대응 | 문자열 `"1"` |
| 가격 | `ORD_UNPR`에 대응 | 문자열 `"사람이 승인한 지정가"` |
| 거래소 | `EXCG_ID_DVSN_CD`에 대응 | `KRX` |

### 주문의 생명주기

| 상태 | 무엇이 일어났나 | 다음 확인 |
|---|---|---|
| 전송 전 | 토큰·계좌·장 운영시간·입력값을 검증 | 종목·매수/매도·수량·지정가·주문한도·중복 여부 |
| 접수 성공 | 증권사 주문시스템이 요청을 받고 주문번호를 반환 | 주문번호와 원 요청을 함께 기록. 아직 체결로 보지 않음 |
| 거절 | 인증·계좌·한도·입력 오류 등으로 주문이 시장에 가지 않음 | 거절 사유를 고친 뒤 사람의 재승인을 받음 |
| 미체결 | 주문은 유효하지만 지정가와 시장 호가가 만나지 않음 | 대기·정정·취소 중 사전에 정한 정책을 적용 |
| 부분체결 | 주문 수량 중 일부만 거래됨 | 누적 체결수량과 미체결수량을 분리하고 중복 주문 방지 |
| 전량체결 | 전 수량의 체결이 확인됨 | 평균 체결가·수수료·현금·보유수량 대사 |
| 취소 종료 | 미체결 잔량의 취소가 확인됨 | 취소 확인 전 새 주문을 중복 전송하지 않음 |

교육에서는 다음 **의사코드만 읽고 주문을 실행하지 않는다.**

```python
# 교육용 의사코드 — 실제 주문 코드가 아님
mode = "paper"
symbol = "005930"
quantity = 1

quote = get_quote(symbol)
check(symbol=symbol, quantity=quantity, max_amount="교육용 한도")

if mode == "paper" and human_approved and not_duplicate:
    response = send_paper_limit_order(
        symbol=symbol,
        side="buy",
        quantity=quantity,
        price="사람이 승인한 지정가",
    )
    order_id = record_acceptance(response)  # 접수번호는 체결이 아님
    fill = poll_or_subscribe_fill_status(order_id)
    reconcile_cash_and_position(fill)
```

### 실제 매매 자동화 전에 필요한 최소 통제

- **환경 분리:** 모의투자와 실전투자의 앱 키·계좌·base URL·설정을 별도 보관한다.
- **사람의 최종 승인:** Agent가 종목·수량·가격을 제안할 수는 있어도 주문 전송은 별도 승인 단계로 둔다.
- **주문 한도:** 1회 주문금액, 일일 누적금액, 종목별 수량을 코드에서 제한한다.
- **중복 방지:** 재시도와 네트워크 오류가 같은 주문을 두 번 만들지 않도록 고유 요청 ID와 주문 상태를 기록한다.
- **체결 확인:** API 응답 성공, 주문 접수, 일부 체결, 전량 체결, 취소를 서로 다른 상태로 처리한다.
- **비밀정보 보호:** 앱 시크릿·토큰·계좌번호를 프롬프트, 코드, Git, 화면 캡처에 넣지 않는다.
- **감사 가능성:** 요청 시각, 승인자, 입력값, 응답, 주문번호, 체결 결과를 변경하기 어려운 로그로 남긴다.

> 이 예시는 API의 가능성과 통제 구조를 설명하기 위한 것이다. 교육 중에는 실전 계좌를 연결하거나 실제·모의 주문을 전송하지 않는다.

공식 참고: [한국투자증권 Open API 샘플 저장소](https://github.com/koreainvestment/open-trading-api), [국내주식 현금주문 함수 샘플](https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/order_cash/order_cash.py), [KIS Trading MCP 설명](https://github.com/koreainvestment/open-trading-api/blob/main/MCP/Kis%20Trading%20MCP/Readme.md)

---

# 5. Part 3 — 왜 공식·구조화 API 데이터인가? (12–16분)

## 5.1 웹 검색과 API의 차이

| 기준 | 일반 웹 검색·페이지 복사 | 공식·구조화 API |
|---|---|---|
| 구조 | 메뉴·광고·본문이 섞일 수 있음 | 필드와 자료형이 정해짐 |
| 출처 | 2차 기사·재인용이 섞임 | 제공기관을 직접 확인 가능 |
| 반복성 | 같은 작업을 다시 하기 어려움 | 동일 요청을 기록·재실행 가능 |
| 검증 | 숫자의 기준일·단위가 불명확할 수 있음 | 기간·단위·문서 식별자를 함께 보관 가능 |
| 자동화 | 페이지 변경에 취약 | 문서화된 규격에 맞춰 처리 가능 |

## 5.2 전문직의 Source-of-Truth 원칙

```text
탐색: Tavily·SerpAPI·검색엔진·뉴스
                ↓
원천 확인: SEC EDGAR·규제기관·회사 공시
                ↓
구조화: API·XBRL·표준 필드
                ↓
분석: 계산·비교·요약
                ↓
검토: 원문 링크·문서일자·단위·가정 확인
```

투자·법무·회계 업무에서는 “답이 그럴듯한가”보다 다음이 중요하다.

- 어느 문서의 어느 부분에서 나왔는가?
- 공시일과 대상 기간은 언제인가?
- 단위와 통화는 무엇인가?
- 정정 공시 또는 후속 공시가 있는가?
- 원문 사실과 분석자의 추론이 분리되어 있는가?

> Tavily와 SerpAPI는 **탐색**에 유용하지만 SEC 공시의 대체물이 아니다. 오늘 실습의 최종 근거는 SEC EDGAR 원문과 그 XBRL 데이터다.

---

# 6. Part 4 — 대표 API와 검색 API 실습 (16–25분)

## 6.1 업무에서 만나는 API

| 분류 | 예시 | 적합한 용도 | 주의점 |
|---|---|---|---|
| 규제·공시 | SEC EDGAR Data APIs, Open DART | 제출 이력, 공시 원문, XBRL | 문서 유형·수정 공시 확인 |
| 거시경제 | FRED | 금리·물가·고용 시계열 | 빈도·수정치·계절조정 확인 |
| AI 친화형 웹 탐색 | Tavily Search API | 관련 문서와 정제된 snippet 탐색 | 결과의 원 출처를 다시 검증 |
| 검색결과 구조화 | SerpAPI | Google·Scholar·News·Maps 등 검색결과를 JSON으로 수집 | 검색결과이지 공식 원천은 아님 |
| AI 모델 | OpenAI API, Anthropic API | 요약·분류·추출·도구 호출 | 기밀성·비용·환각·접근정책 |
| 사내 시스템 | CRM·DMS·데이터룸 API | 내부 자료 연결과 자동화 | 권한·감사로그·개인정보 |

SEC의 `data.sec.gov` API는 인증 키 없이 공개 JSON 데이터를 제공하며 제출 이력과 XBRL 데이터를 다룬다. 자동 접근 시에는 식별 가능한 User-Agent와 공정 접근 정책을 지켜야 한다.

## 6.2 Tavily와 SerpAPI 중 무엇을 고를까?

하이브리드 실습의 기본 검색 도구는 **Tavily**다. SerpAPI는 검색엔진 결과 구조가 필요한 경우의 대안이다. FRED는 검색 API의 대안이 아니라 거시경제 맥락을 보충하는 선택 트랙이다.

| 기준 | Tavily | SerpAPI |
|---|---|---|
| 주된 역할 | AI Agent가 읽기 좋은 웹 검색·추출 | 실제 검색엔진 결과 페이지를 구조화된 JSON으로 제공 |
| 결과 예 | 제목, URL, relevance score, content snippet | organic results, news, Scholar, Maps 등 엔진별 필드 |
| 도메인 제한 | `include_domains=["sec.gov"]` | 검색어의 `site:sec.gov` 연산자 활용 |
| 잘 맞는 상황 | RAG, 리서치 Agent, 문서 후보 수집 | Google/Scholar/News 결과 재현, 순위·위치·엔진별 조사 |
| 오늘의 공통 원칙 | 발견한 URL을 SEC 원문에서 재확인 | 발견한 URL을 SEC 원문에서 재확인 |

Tavily는 검색 결과를 AI가 소비하기 좋게 정리하는 데 강점이 있고, SerpAPI는 Google을 포함한 여러 검색엔진의 결과 구조를 다룰 수 있다. 어느 쪽도 규제기관이나 회사가 발행한 공식 데이터 자체는 아니다.

## 6.3 계정과 API 키 만들기

### 선택 A — Tavily

1. <https://app.tavily.com>에 접속해 계정을 만들거나 로그인한다.
2. Dashboard의 API Keys에서 키를 생성하거나 기존 키를 복사한다.
3. 키는 일반적으로 `tvly-...` 형태다.
4. 최신 무료 한도와 요금은 [Tavily 공식 문서](https://docs.tavily.com/documentation/quickstart)와 Dashboard에서 확인한다.

### 선택 B — SerpAPI

1. <https://serpapi.com/signup>에서 계정을 만든다.
2. 로그인 후 <https://serpapi.com/manage-api-key>에서 private API key를 확인한다.
3. [SerpAPI Playground](https://serpapi.com/playground)에서 검색엔진과 파라미터를 바꿔볼 수 있다.
4. 최신 무료 한도와 요금은 SerpAPI Dashboard에서 확인한다.

### 선택 C — FRED 거시경제 트랙

1. [FRED API key 안내](https://fred.stlouisfed.org/docs/api/api_key.html)에서 계정을 만들고 API key를 요청한다.
2. [FRED Series Search](https://fred.stlouisfed.org/docs/api/fred/series_search.html)에서 지표의 series ID를 찾는다.
3. 예: 정책금리 `FEDFUNDS`, 소비자물가 `CPIAUCSL`, 실업률 `UNRATE`.
4. 같은 지표도 빈도·단위·계절조정·수정 시점이 다르므로 metadata를 함께 보관한다.

어느 키든 화면 공유, 채팅, 프롬프트, 소스 코드, Git commit에 넣지 않는다.

## 6.4 키를 현재 터미널 세션에만 넣기

### Windows PowerShell

아래 명령을 실행하면 다음 줄에서 키를 입력한다. 명령 기록에는 실제 키가 남지 않는다.

선택한 API에 해당하는 한 줄만 실행한다.

```powershell
# Tavily
$env:TAVILY_API_KEY = Read-Host "Tavily API key"

# 또는 SerpAPI
$env:SERPAPI_KEY = Read-Host "SerpAPI key"

# 선택: FRED 거시경제 트랙
$env:FRED_API_KEY = Read-Host "FRED API key"
```

존재 여부만 확인한다. 키 자체를 출력하지 않는다.

```powershell
if ($env:TAVILY_API_KEY) { "TAVILY_API_KEY is set" }
if ($env:SERPAPI_KEY) { "SERPAPI_KEY is set" }
if ($env:FRED_API_KEY) { "FRED_API_KEY is set" }
```

### macOS Terminal

입력 문자가 화면에 보이지 않도록 설정한다.

선택한 API에 해당하는 블록 하나만 실행한다.

```bash
# Tavily
read -s "TAVILY_API_KEY?Tavily API key: "
export TAVILY_API_KEY
echo
test -n "$TAVILY_API_KEY" && echo "TAVILY_API_KEY is set"

# 또는 SerpAPI
read -s "SERPAPI_KEY?SerpAPI key: "
export SERPAPI_KEY
echo
test -n "$SERPAPI_KEY" && echo "SERPAPI_KEY is set"

# 선택: FRED 거시경제 트랙
read -s "FRED_API_KEY?FRED API key: "
export FRED_API_KEY
echo
test -n "$FRED_API_KEY" && echo "FRED_API_KEY is set"
```

Terminal을 닫으면 이 값은 사라진다. 오늘 실습에는 이것이 더 안전하다.

## 6.5 Agent에게 첫 검색 프로그램 만들게 하기

Claude Code 또는 Codex에 선택한 프롬프트 하나를 입력한다.

### 선택 A — Tavily

```text
workshop/tavily_search.py를 만들어줘.

요구사항:
- TAVILY_API_KEY를 코드에 쓰지 말고 os.environ에서만 읽는다.
- 키가 없으면 비밀값을 출력하지 않고 친절한 오류로 종료한다.
- TavilyClient로 “NVIDIA latest 10-K SEC filing”을 검색한다.
- include_domains=["sec.gov"], max_results=3을 사용한다.
- 결과마다 title, url, score만 출력한다.
- 실행 후 결과 URL의 도메인이 sec.gov인지 확인한다.
- 파일 생성과 실행에 사용한 명령, 성공 여부를 마지막에 알려준다.
```

직접 확인하고 싶다면 생성된 파일의 핵심은 다음과 같아야 한다.

```python
import os
from tavily import TavilyClient

api_key = os.environ.get("TAVILY_API_KEY")
if not api_key:
    raise SystemExit("TAVILY_API_KEY가 설정되지 않았습니다.")

client = TavilyClient(api_key=api_key)
response = client.search(
    query="NVIDIA latest 10-K SEC filing",
    topic="general",
    include_domains=["sec.gov"],
    include_answer=False,
    max_results=3,
)

for result in response["results"]:
    print(f"[{result['score']:.2f}] {result['title']}")
    print(result["url"])
```

실행:

```text
python workshop/tavily_search.py
```

### 선택 B — SerpAPI

SerpAPI의 공식 Python SDK 패키지 이름은 `serpapi`다. 과거 예제에 많이 등장하는 `google-search-results`는 legacy 패키지이므로 새 실습에서는 사용하지 않는다.

```text
workshop/serpapi_search.py를 만들어줘.

요구사항:
- SERPAPI_KEY를 코드에 쓰지 말고 os.environ에서만 읽는다.
- 키가 없으면 비밀값을 출력하지 않고 친절한 오류로 종료한다.
- 공식 serpapi 패키지의 serpapi.Client를 사용한다.
- engine="google", q="site:sec.gov NVIDIA latest 10-K filing"로 검색한다.
- num=3, hl="en", gl="us"를 사용한다.
- organic_results에서 title, link, position만 출력한다.
- link의 도메인이 sec.gov인지 확인하되, 아니면 경고만 표시한다.
- 파일 생성과 실행에 사용한 명령, 성공 여부를 마지막에 알려준다.
```

생성된 파일의 핵심은 다음과 같아야 한다.

```python
import os
from urllib.parse import urlparse
import serpapi

api_key = os.environ.get("SERPAPI_KEY")
if not api_key:
    raise SystemExit("SERPAPI_KEY가 설정되지 않았습니다.")

client = serpapi.Client(api_key=api_key)
results = client.search({
    "engine": "google",
    "q": "site:sec.gov NVIDIA latest 10-K filing",
    "num": 3,
    "hl": "en",
    "gl": "us",
})

for item in results.get("organic_results", [])[:3]:
    link = item.get("link", "")
    domain = urlparse(link).netloc.lower()
    status = "SEC" if domain == "sec.gov" or domain.endswith(".sec.gov") else "CHECK"
    print(f"[{status}] {item.get('position')} | {item.get('title')}")
    print(link)
```

실행:

```text
python workshop/serpapi_search.py
```

### 여기서 배울 점

- API 키는 **인증 수단**이므로 비밀번호처럼 다룬다.
- API 응답은 Tavily의 `title`·`url`·`score`, SerpAPI의 `organic_results`·`link`·`position`처럼 구조화되어 있다.
- `include_domains`나 `site:sec.gov`는 노이즈를 줄이지만 결과의 정확성을 보증하지 않는다.
- 발견한 URL을 열어 원문을 확인해야 한다.

## 6.6 FRED 첫 호출 — “공식 맥락”을 가져오기

FRED는 회사 공시가 말하는 금리·물가·고용 환경을 확인하는 데 유용하다. 아래 프롬프트는 회사 주장을 증명하는 것이 아니라 당시 환경을 구조화한다.

```text
workshop/fred_context.py를 만들어줘.

요구사항:
- FRED_API_KEY를 os.environ에서만 읽고 값은 출력하거나 저장하지 않는다.
- FRED series observations API로 FEDFUNDS, CPIAUCSL, UNRATE를 가져온다.
- observation_start와 observation_end를 명시한다.
- series_id, title, units, frequency, seasonal_adjustment, last_updated와 관측값을 JSON으로 저장한다.
- 각 series의 evidence_role은 context_only로 고정한다.
- “거시지표와 회사 실적의 동행은 회사별 인과관계를 증명하지 않는다”는 warning을 넣는다.
```

FRED의 강점은 공식성과 재현성이다. 다만 최신값은 수정될 수 있다. 당시 이용 가능했던 값이 중요하면 real-time period 또는 vintage date를 별도로 기록한다.

---

# 7. Part 5 — Git과 GitHub는 무엇이며 왜 비개발자도 쓰는가? (25–33분)

## 7.1 한 문장 정의

- **Git:** 파일의 변경 이력과 상태를 기록하는 도구
- **GitHub:** Git 저장소를 공유·검토·협업하는 서비스
- **Repository:** 코드, 문서, 예제, 설정, 변경 이력이 함께 들어 있는 작업 묶음

## 7.2 비개발자에게 Git이 유용한 이유

`git clone` 한 줄로 다른 사람이 공개한 산출물 전체를 가져올 수 있다.

- README와 사용법
- 실행 코드와 예제
- 테스트와 샘플 데이터
- 변경 이력과 이슈
- 라이선스

웹페이지에서 파일 몇 개를 복사하는 것과 달리, 저장소 전체의 맥락과 출처가 남는다. AI Agent는 이 구조를 한 번에 읽고 “무엇을 하는 도구인지”, “어떻게 실행하는지”, “어디를 바꿔야 하는지” 설명할 수 있다.

## 7.3 오늘 사용하는 명령

강사가 이 패키지를 GitHub에 올린 경우 아래 URL을 실제 주소로 바꿔 배포한다. 참가자는 남이 만든 **실행 코드·문서·템플릿 전체**를 clone한다.

```text
git clone <WORKSHOP_REPOSITORY_URL> mdna-evidence-lab
cd mdna-evidence-lab
```

이제 다음을 확인한다.

```text
git status
git log -1 --oneline
```

- `git status`: 내가 바꾼 파일이 있는지 확인
- `git log -1`: 내려받은 버전의 최근 변경 확인
- `--depth 1`: 수업 시간을 위해 최신 이력만 내려받기

공개 저장소 clone에는 GitHub 계정이 필요하지 않다. 다만 push, private repository 접근, 이슈 작성 등에는 계정과 권한이 필요하다.

오늘 구조에서는 `edgartools`를 별도 SDK 의존성으로 설치한다. 공식 소스 자체를 읽고 싶을 때만 다음처럼 다른 폴더에 clone한다.

```text
git clone --depth 1 https://github.com/dgunning/edgartools.git reference-repos/edgartools
```

즉, **저장소를 clone하는 것**과 **그 안에서 사용하는 API/SDK 키를 설정하는 것**은 서로 다른 단계다. EDGAR/EdgarTools에는 API key가 없고 SEC identity가 필요하며, Tavily와 FRED에만 각자의 API key를 연결한다.

## 7.4 저장소를 AI에게 읽히는 첫 프롬프트

```text
이 저장소를 비개발자인 투자자·변호사·회계사에게 설명해줘.

다음을 표로 정리해:
1. 이 저장소가 해결하는 문제
2. 데이터의 원천
3. 최신 10-K를 가져오는 핵심 객체와 메서드
4. SEC 요청 시 identity가 필요한 이유
5. 실행에 필요한 최소 파일과 패키지
6. 투자·법무·회계 관점의 활용 예시
7. 결과를 그대로 믿으면 안 되는 지점

README와 공식 문서를 근거로 답하고, 확인한 파일 경로를 함께 적어줘.
파일은 아직 수정하지 마.
```

## 7.5 업무에 유용한 GitHub 저장소 지도

이 목록은 “유명한 Python 패키지”가 아니라 **투자 리서치의 실제 작업 단계에 바로 연결되는가**를 기준으로 다시 선별했다. README의 기능 범위, 최근 release·commit, 설치 난이도, 데이터 출처와 이용조건을 함께 확인했다. 전부 설치하지 말고 현재 문제에 맞는 하나만 고른다.

### A. 입문 수업에서 먼저 보여줄 4개

| 저장소 | 실제로 해결하는 문제 | 왜 우선인가 | 반드시 말할 주의점 |
|---|---|---|---|
| [dgunning/edgartools](https://github.com/dgunning/edgartools) | 미국 SEC 공시, 10-K/10-Q section, XBRL 재무제표, 13F·insider filing 조회 | 이번 실습과 직접 연결되고 공시 원문까지 추적하기 좋음 | SEC identity·공정 접근 정책, 문서 파싱 오류 가능성 |
| [FinanceData/OpenDartReader](https://github.com/FinanceData/OpenDartReader) | 한국 Open DART 공시·재무제표·주주·사업보고서 조회 | 한국 기업 분석으로 실습을 확장하기 가장 쉬움 | DART API 키, 정정공시와 연결재무제표 여부 확인 |
| [FinanceData/FinanceDataReader](https://github.com/FinanceData/FinanceDataReader) | KRX·미국·글로벌 종목과 지수, 환율·FRED 시계열 조회 | 한국 투자업계 참가자가 가격·지수 비교를 빠르게 시작하기 좋음 | 데이터 제공처가 여러 곳이므로 심볼별 원천·이용조건 확인 |
| [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) | 여러 금융 데이터 제공자를 Python·CLI·REST API·MCP로 연결 | API와 MCP가 투자 리서치 플랫폼에서 함께 쓰이는 모습을 보여주기 좋음 | 제공자별 API 키·비용·라이선스가 다르고 전체 설치는 큼 |
| [koreainvestment/open-trading-api](https://github.com/koreainvestment/open-trading-api) | 한국투자증권 시세·계좌·주문·체결, WebSocket, MCP 샘플 | API가 실제 거래 시스템으로 이어지는 흐름을 설명하기 좋음 | 실습은 읽기 전용으로 진행하고 모의·실전 키와 계좌를 엄격히 분리 |

### B. 분석 산출물을 바로 만드는 실무 도구

| 저장소 | 실제로 해결하는 문제 | 적합한 사용자 | 반드시 말할 주의점 |
|---|---|---|---|
| [ranaroussi/yfinance](https://github.com/ranaroussi/yfinance) | Yahoo Finance 기반 가격·기업·보유자·뉴스 데이터의 빠른 프로토타입 | 아이디어 검토와 개인 리서치 | Yahoo의 공식 SDK가 아니며 프로젝트가 연구·교육 및 개인 용도를 명시함 |
| [ranaroussi/quantstats](https://github.com/ranaroussi/quantstats) | Sharpe, 변동성, drawdown, rolling metric과 HTML tear sheet 생성 | 포트폴리오 매니저·성과분석 | 입력 수익률·benchmark·연율화 가정과 비용 반영 여부 검증 |
| [docling-project/docling](https://github.com/docling-project/docling) | PDF·Office·이미지·XBRL의 layout, 표, OCR을 보존해 Markdown/JSON으로 변환 | 리서치 보고서·IM·복잡한 공시 문서 처리 | 모델 다운로드·처리시간·OCR 오류, 기밀문서 로컬 처리 정책 확인 |
| [jadchaar/sec-edgar-downloader](https://github.com/jadchaar/sec-edgar-downloader) | 10-K·10-Q·8-K·13F 등 SEC 원문을 조건별로 일괄 내려받기 | 공시 아카이브·시계열 비교 | 분석 기능보다 수집에 특화되어 `edgartools`와 역할이 겹칠 수 있음 |

### C. 퀀트·시스템 운용 심화용

| 저장소 | 실제로 해결하는 문제 | 수업에서의 위치 | 진입 장벽 |
|---|---|---|---|
| [QuantConnect/Lean](https://github.com/QuantConnect/Lean) | 주식·옵션·선물·FX·크립토 전략의 event-driven 백테스트와 live trading | “검증 가능한 전략 실행환경”의 대표 사례로만 소개 | Docker, 데이터·broker 설정, 체결·수수료·slippage 모델 이해 필요 |
| [microsoft/qlib](https://github.com/microsoft/qlib) | 데이터 처리, ML 모델, backtest, portfolio·execution을 잇는 AI quant 연구 파이프라인 | AI 기반 factor·model 연구의 심화 참고자료 | 설치와 데이터 준비가 무겁고 기본 샘플 데이터 품질을 별도 검증해야 함 |

### 이번 60분 수업의 추천 순서

1. **미국 공시:** `edgartools`
2. **한국 공시:** `OpenDartReader`
3. **한국·글로벌 가격 비교:** `FinanceDataReader`
4. **API와 MCP 확장 사례:** `OpenBB`
5. **증권사 API와 주문 통제:** `open-trading-api`
6. **포트폴리오 보고서:** `QuantStats`
7. **복잡한 PDF·XBRL:** `Docling`

`yfinance`는 빠른 실험에는 편리하지만 최종 투자 판단의 source of truth로 사용하지 않는다. `LEAN`과 `Qlib`은 강력하지만 이번 입문 수업에서 clone·설치하지 않고 심화 과정으로 분리한다.

## 7.6 새로운 저장소를 안전하게 평가하는 프롬프트

저장소 하나를 고른 뒤 Agent에게 다음처럼 요청한다. 처음에는 설치나 실행 없이 읽기만 한다.

```text
다음 공개 GitHub 저장소를 업무 도입 관점에서 검토해줘:
<여기에 GitHub URL>

아직 설치하거나 코드를 실행하지 마.
README, LICENSE, pyproject.toml/requirements, 최근 release와 주요 issue를 읽고 표로 정리해:
1. 해결하는 문제와 대표 입력/출력
2. 원 데이터 제공자와 공식성
3. 필요한 API 키·계정·네트워크 권한
4. Windows와 macOS 설치 난이도
5. 라이선스와 업무 사용 시 확인할 점
6. 최근 유지보수 상태와 알려진 제한
7. 투자·법무·회계 업무의 구체적 사용 예시
8. 최소한의 안전한 실습 계획

근거가 된 파일 경로와 공식 링크를 붙이고,
확인하지 못한 내용은 추측하지 말고 “미확인”으로 표시해.
```

### clone 전 체크

- 저장소 소유자와 공식 조직인지 확인한다.
- README뿐 아니라 `LICENSE`, 최근 release, issue를 본다.
- clone 자체는 코드를 실행하지 않지만, 설치 스크립트와 패키지는 실행될 수 있으므로 별도 검토한다.
- 별도 폴더와 가상환경을 사용한다. 여러 저장소를 같은 `.venv`에 섞지 않는다.
- 데이터 라이선스와 소프트웨어 라이선스는 서로 다를 수 있다.

---

# 8. Part 6 — EDGAR MD&A + 최신 뉴스 + 거시맥락 (33–49분)

> 바로 실행할 파일과 Turn별 프롬프트는 [MD&A 실습 패키지](mdna-edgar-workshop-package/README.md)에 들어 있다. 본문은 수업 중 흐름을 설명하고, 패키지는 참가자가 그대로 실행하는 작업공간이다.

## 8.1 SEC EDGAR와 EdgarTools

SEC EDGAR는 미국 상장사 등의 공시 원천이다. SEC Data APIs는 제출 이력과 XBRL 데이터를 JSON으로 제공한다. EdgarTools는 이를 Python 객체와 표 형태로 다루기 쉽게 만든 오픈소스 도구다.

중요한 운영 원칙:

- 실제 이름과 이메일을 SEC 요청 identity로 설정한다.
- 필요한 자료만 요청한다.
- SEC의 현재 공정 접근 한도인 초당 10회 이하를 지킨다.
- 공시 원문, 제출일, accession number를 보고서와 함께 보관한다.

## 8.2 SEC identity 설정

이 값은 비밀키가 아니지만 실제 연락 가능한 정보여야 한다.

### Windows PowerShell

```powershell
$env:SEC_IDENTITY = "Your Name your.email@company.com"
```

### macOS Terminal

```bash
export SEC_IDENTITY="Your Name your.email@company.com"
```

## 8.3 분석 기업 선택

수업에서는 한 기업을 선택한다.

- NVIDIA: `NVDA`
- Apple: `AAPL`
- Tesla: `TSLA`

기업마다 회계연도와 공시 시점이 다르므로, 단순히 달력연도만 보고 비교하지 않는다.

## 8.4 개념 시연 — Agent에게 최소 추출 프로그램 만들게 하기

아래는 EdgarTools의 객체 흐름을 설명하는 선택형 시연이다. 실제 수업은 8.7의 패키지 스크립트로 최신·직전 MD&A를 함께 추출한다. 아래 프롬프트의 `AAPL`을 원하는 ticker로 바꾼다.

```text
EdgarTools를 사용해 AAPL의 가장 최근 10-K를 분석할 준비를 해줘.

workshop/analyze_10k.py를 만들고 현재 .venv에서 실행해.
SEC_IDENTITY는 os.environ에서만 읽고, 없으면 친절한 오류로 종료해.

프로그램은 다음을 수행해야 해:
1. Company("AAPL")을 만든다.
2. get_filings(form="10-K").latest()로 최신 10-K filing을 고른다.
3. filing.obj()로 10-K 객체를 만든다.
4. Item 1A Risk Factors와 Item 7 MD&A를 텍스트로 추출한다.
5. company.get_financials()로 income statement, balance sheet, cash flow statement를 가져온다.
6. workshop_outputs 폴더에 다음 파일을 UTF-8로 저장한다.
   - filing_metadata.txt
   - risk_factors.txt
   - mdna.txt
   - financial_statements.txt
   - evidence_index.csv
7. metadata에는 ticker, company name, filing date, accession number, 가능한 경우 SEC filing URL을 기록한다.
8. 오류가 나면 임의로 메서드를 추측하지 말고 설치된 EdgarTools 버전과 저장소 문서를 확인해 수정한다.
9. evidence_index.csv에는 evidence_id, 파일명, section/statement, reporting period, unit, source URL을 기록한다.
10. 실행 후 각 출력 파일의 존재와 크기를 검사하고 결과를 표로 알려준다.

원문 숫자를 계산하거나 해석하지 말고, 이 단계에서는 추출만 해.
```

Agent가 만든 코드는 대략 다음 흐름이어야 한다.

```python
import os
from pathlib import Path
from edgar import Company, set_identity

identity = os.environ.get("SEC_IDENTITY")
if not identity:
    raise SystemExit("SEC_IDENTITY가 설정되지 않았습니다.")

set_identity(identity)
company = Company("AAPL")
filing = company.get_filings(form="10-K").latest()
ten_k = filing.obj()
financials = company.get_financials()

output_dir = Path("workshop_outputs")
output_dir.mkdir(exist_ok=True)

metadata = (
    f"Company: {filing.company}\n"
    f"Form: {filing.form}\n"
    f"Filing date: {filing.filing_date}\n"
    f"Reporting period: {filing.period_of_report}\n"
    f"Accession number: {filing.accession_number}\n"
    f"SEC URL: {filing.homepage_url}\n"
)

(output_dir / "filing_metadata.txt").write_text(
    metadata,
    encoding="utf-8",
)
(output_dir / "risk_factors.txt").write_text(
    str(ten_k["Item 1A"]), encoding="utf-8"
)
(output_dir / "mdna.txt").write_text(
    str(ten_k["Item 7"]), encoding="utf-8"
)
(output_dir / "financial_statements.txt").write_text(
    "INCOME STATEMENT\n"
    + str(financials.income_statement())
    + "\n\nBALANCE SHEET\n"
    + str(financials.balance_sheet())
    + "\n\nCASH FLOW STATEMENT\n"
    + str(financials.cashflow_statement()),
    encoding="utf-8",
)
(output_dir / "evidence_index.csv").write_text(
    "evidence_id,file,section_or_statement,reporting_period,unit,source_url,notes\n"
    f"E001,risk_factors.txt,Item 1A,{filing.period_of_report},text,{filing.homepage_url},\n"
    f"E002,mdna.txt,Item 7,{filing.period_of_report},text,{filing.homepage_url},\n"
    f"E003,financial_statements.txt,Financial Statements,{filing.period_of_report},verify in filing,{filing.homepage_url},\n",
    encoding="utf-8",
)
```

> 위 코드는 개념 확인용 최소 예시다. 설치된 버전에서 속성 이름이나 반환 형태가 바뀌었으면 Agent가 저장소의 현재 문서를 확인해 맞춰야 한다.

## 8.5 개념 시연 결과 확인

### Windows PowerShell

```powershell
Get-ChildItem .\workshop_outputs
Get-Content .\workshop_outputs\filing_metadata.txt
```

### macOS Terminal

```bash
ls -lh workshop_outputs
sed -n '1,20p' workshop_outputs/filing_metadata.txt
```

확인할 것:

- 최신 filing이 정말 `10-K`인가?
- 제출일과 대상 회계연도는 언제인가?
- `10-K/A` 또는 후속 정정·수정 자료가 있는가?
- 회사 ticker가 의도한 법인과 일치하는가?
- 표의 단위가 USD, shares, millions 등 무엇인가?

## 8.6 핵심 도식 — 한 개의 MD&A 주장을 세 방향으로 검증

```text
MD&A claim: “수요 둔화는 고금리와 고객 구매 지연의 영향이다”
        │
        ├── SEC / EdgarTools
        │     최신·직전 Item 7, accession, 재무 숫자
        │     역할: primary_verification
        │
        ├── Tavily
        │     공시 후 회사 IR·규제기관·신뢰할 수 있는 보도
        │     역할: corroboration / contradiction / unresolved
        │
        └── FRED (선택)
              금리·물가·고용·소비·산업생산 시계열
              역할: context_only
                         ↓
              Integrated Evidence Register
                         ↓
                    Human Gate
```

| 소스 | 이 소스가 답하는 질문 | 저장할 것 | 금지하는 추론 |
|---|---|---|---|
| EDGAR·EdgarTools | 회사가 실제로 무엇을 말했고 어떤 숫자를 공시했는가? | form, period, accession, section, 단위 | 경영진의 인과 설명이 자동으로 사실이라는 단정 |
| Tavily | 공시 후 어떤 사건·발표·반대 근거가 나타났는가? | 원문 URL, 발행기관, 발행일, snippet, 검토 상태 | 검색 결과가 SEC 원문을 대체한다는 단정 |
| FRED | 당시 거시 환경은 어떠했는가? | series ID, 단위, 빈도, 관측일, last updated | 거시 추세가 해당 회사 실적의 원인이라는 단정 |

Evidence role은 다음 다섯 값으로 통제한다.

- `primary_verification`: 공식 원문·공식 통계로 직접 확인
- `corroboration`: 같은 방향의 보강 근거
- `contradiction`: 반대되거나 충돌하는 근거
- `context_only`: 배경만 설명하는 근거
- `unresolved`: 원문·날짜·범위가 부족해 아직 분류할 수 없음

## 8.7 패키지로 실행하는 실제 명령

최신·직전 10-K Item 7을 함께 추출한다.

```text
python scripts/extract_mdna.py --ticker AAPL
```

`mdna_claims.csv`에서 검증 가치가 큰 claim 하나를 고르고 Tavily로 공시 후 사건을 찾는다.

```text
python scripts/search_external_news.py --ticker AAPL --company "Apple Inc." --claim-id C001 --query "demand pricing margin supply regulation latest developments" --time-range month
```

FRED는 선택 트랙이다. MD&A의 주장과 관련 있는 series만 고른다.

```text
python scripts/fetch_fred_context.py --ticker AAPL --claim-id C001 --series FEDFUNDS,CPIAUCSL,UNRATE --observation-start 2024-01-01
```

스크립트는 키를 결과 파일에 저장하지 않는다. Tavily 결과는 `unresolved`, FRED 결과는 `context_only`로 시작하며, Agent가 원문을 확인하고 사람이 승인해야 상태가 바뀐다.

---

# 9. Part 7 — Claude Code/Codex로 통합 DD sprint 진행하기 (49–60분)

이 실습은 긴 프롬프트 하나로 보고서를 바로 생성하지 않는다. 참가자는 Agent에게 **한 단계씩 지시하고, 단계 사이의 산출물을 확인한 뒤 다음 단계로 넘어간다.** Claude Code와 Codex 모두 저장소 루트에서 실행하고 같은 파일 구조와 완료 기준을 사용한다.

## 9.1 최종 작업공간

```text
workspace/AAPL/
├── filing_manifest.json            # 최신·직전 공시 식별자와 추출 방법
├── mdna_current.md                  # 최신 10-K Item 7
├── mdna_prior.md                    # 직전 10-K Item 7
├── extraction_check.md              # 섹션 경계 Gate A
├── mdna_diff.md                     # 전년 대비 설명 변화
├── mdna_claims.csv                  # 경영진 주장과 재무 숫자
├── tavily_evidence.json             # 최신 사건 후보
├── fred_context.json                # 선택형 거시 시계열
├── external_evidence.csv            # 외부 근거 역할·방향
├── integrated_claim_register.csv    # SEC·뉴스·거시 통합표
├── role_review.md                   # 투자·법무·회계 검토
└── mdna_review.md                   # 최종 DD 메모
```

Agent가 파일을 만들었다는 사실만으로 완료가 아니다. 각 단계의 **완료 기준**을 충족하고 사람이 지정된 gate를 확인해야 한다.

## 9.2 Turn 0 — 작업공간과 실행계획 확인

첫 지시는 수정이나 분석이 아니라 현재 상태 확인이다.

```text
이 저장소에서 AAPL 최신 10-K DD sprint를 진행할 거야.

지금은 파일을 만들거나 수정하지 말고 다음만 확인해:
1. 현재 작업 디렉터리와 git status
2. 사용 중인 Python과 edgartools 버전
3. SEC_IDENTITY, TAVILY_API_KEY와 선택형 FRED_API_KEY 설정 여부. 값 자체는 출력하지 마.
4. workspace/AAPL의 기존 파일과 덮어쓰기 위험
5. 앞으로 만들 파일 목록과 단계별 실행계획

확인 결과와 위험을 표로 보여준 뒤 멈춰. 내가 승인하기 전에는 실행하지 마.
```

완료 기준:

- 저장소 루트와 현재 변경사항을 확인했다.
- 비밀값을 출력하지 않았다.
- 새로 만들거나 바꿀 파일이 명확하다.
- 기존 사용자 파일을 덮어쓰지 않는다.

## 9.3 Turn 1 — Filing identity 고정

```text
scripts/extract_mdna.py를 실행해 AAPL의 최신·직전 non-amended 10-K를 조회해.

먼저 filing_manifest.json의 다음 항목만 보고해:
- legal company name, ticker, CIK
- current와 prior의 form, filing date, reporting period
- accession number와 SEC URL
- 추출 방법과 parser warning

mdna_current.md, mdna_prior.md, extraction_check.md가 만들어졌는지 확인해.
분석은 시작하지 말고 다시 멈춰. 다음 단계는 내가 identity와 추출 경계를 확인한 뒤 진행한다.
```

### Human Gate A — 30초 확인

사람이 다음 네 항목을 직접 읽는다.

- 회사가 의도한 법인인가?
- form이 `10-K`이며 수정공시 여부가 표시됐는가?
- filing date와 reporting period가 구분됐는가?
- accession number 또는 SEC URL로 원문을 열 수 있는가?

하나라도 불명확하면 추출 단계로 넘어가지 않는다.

## 9.4 Turn 2 — MD&A claim과 재무 숫자 연결

```text
extraction_check.md가 PASS인 경우에만 최신·직전 Item 7을 비교해.

생성할 파일:
- mdna_diff.md: added, removed, stronger, weaker, quantified_change, causal_change
- mdna_claims.csv: management_claim과 analyst_interpretation 분리

각 claim에 claim_id, source heading, accession, historical/forward-looking,
metric, current/prior value, period, unit, verification_status를 붙여.
재무제표나 Item 8에서 확인하지 못한 숫자와 인과관계는 verified로 두지 마.
상태별 행 개수를 보여주고 멈춰.
```

완료 기준:

- 최신·직전 MD&A가 비어 있지 않고 Item 7A·8 경계를 통과했다.
- 모든 claim은 승인된 accession과 source heading으로 돌아간다.
- 숫자의 기간·단위·통화를 추적할 수 있다.
- 경영진의 인과 설명과 숫자로 확인된 사실을 분리했다.

## 9.5 Turn 3 — Tavily 최신 사건과 FRED 거시맥락 수집

```text
mdna_claims.csv에서 검증 가치가 큰 claim 1–3개를 고르고 이유를 보여줘.
내가 승인하면 scripts/search_external_news.py로 회사별 최신 사건을 수집해.
FRED_API_KEY가 있고 주장과 직접 관련된 series를 설명할 수 있을 때만
scripts/fetch_fred_context.py를 실행해.

키 값은 출력·저장하지 마. Tavily 결과는 처음에 unresolved,
FRED 결과는 항상 context_only로 유지해.
원문 URL, 발행일 또는 관측일, 분석 기준일을 보여주고 멈춰.
```

Tavily의 검색 snippet만으로 사실을 확정하지 않는다. 회사 IR, 규제기관, 신뢰할 수 있는 원문을 열어야 한다. FRED와 회사 지표의 동행은 인과관계 증명이 아니다.

## 9.6 Turn 4 — Integrated Evidence Register와 세 직군 검토

```text
mdna_claims.csv, tavily_evidence.json과 선택형 fred_context.json을 통합해.

생성할 파일:
- external_evidence.csv
- integrated_claim_register.csv
- role_review.md

외부 근거 역할은 primary_verification, corroboration, contradiction,
context_only, unresolved 중 하나만 사용해.
각 claim에 SEC 근거, 재무 검증, Tavily external_id, FRED series_id,
충돌과 open_question을 연결해.

투자·법무·회계 관점을 분리해 읽고, contradiction과 unresolved를 우선 보고해.
아직 최종 메모는 만들지 말고 멈춰.
```

### Human Gate B — 표본 원문 대조

참가자는 integrated claim register에서 다음 세 개를 골라 원문과 직접 대조한다.

1. 가장 중요한 숫자 주장 1개
2. 가장 중요한 법적 리스크 주장 1개
3. `contradiction`, `unresolved`, `needs_source` 중 하나

근거가 맞지 않으면 해당 claim을 수정하거나 제외한 뒤에만 최종 조립을 승인한다.

## 9.7 Turn 5 — 검증된 주장만 최종 보고서로 조립

```text
Human Gate B에서 승인한 결과만 사용해 workspace/AAPL/mdna_review.md를 조립해.

verified인 SEC·재무 사실, 원문을 확인한 corroboration·contradiction만 본문에 사용해.
context_only는 배경으로 명시하고, unresolved와 needs_source는 “추가 확인 필요”로 이동해.

보고서 구조:
1. Filing identity
2. Executive summary: 검증된 사실 5개
3. Investment findings
4. Legal and regulatory findings
5. Accounting findings
6. Red flags와 추가 확인 질문
7. 공시 후 최신 사건과 반대 근거
8. 거시환경(context only)
9. Limitations와 Human verification checklist

각 핵심 문장 뒤에 [claim_id | accession/external_id/series_id]를 붙여.
사실과 해석을 분리하고 법률·투자·회계 자문으로 단정하지 마.
완료 후 새로 만든 파일과 변경한 파일만 목록으로 보여줘.
```

## 9.8 Turn 6 — 최종 감사와 handoff

```text
workspace/AAPL/mdna_review.md를 제출 전 감사해.

검사:
- 모든 claim_id가 integrated_claim_register.csv에 존재하는가?
- 모든 accession, external_id, series_id가 원본 파일에 존재하는가?
- 숫자에 기간과 단위가 있는가?
- filing_manifest와 회사·form·기간이 일치하는가?
- 미확인 내용을 사실처럼 쓴 문장이 없는가?
- Tavily snippet을 원문처럼, FRED context를 회사 인과관계처럼 쓰지 않았는가?

문제가 있으면 mdna_review.md를 수정하고 reviewer_note에 수정 이유를 남겨.
마지막에는 git status --short와 최종 파일 목록을 보여줘.
```

> Agent의 자신감은 근거가 아니다. **SEC 원문·최신 원문·공식 거시지표 → evidence role → claim ID → 최종 문장**의 연결이 남아야 DD 결과를 다시 검토할 수 있다.

---

# 10. 실습 성공 기준

아래 항목이 모두 체크되면 완료다.

- [ ] `git --version`이 버전을 출력한다.
- [ ] `python --version`이 3.10 이상을 출력한다.
- [ ] Claude Code 또는 Codex가 저장소 안에서 실행된다.
- [ ] `git status`와 `git log -1`의 의미를 설명할 수 있다.
- [ ] Tavily·FRED API key가 코드, 프롬프트, 결과 JSON 또는 Git에 저장되지 않았다.
- [ ] Tavily에서 회사별 최신 사건 후보를 얻고 원문 URL을 열었다.
- [ ] FRED 선택 트랙에서는 series ID·단위·빈도·기준일을 저장했다.
- [ ] `SEC_IDENTITY`를 설정했다.
- [ ] 최신·직전 10-K의 filing date와 accession number를 확인했다.
- [ ] 최신·직전 MD&A, manifest와 extraction check를 저장했다.
- [ ] `integrated_claim_register.csv`에서 주요 주장의 evidence role을 검토했다.
- [ ] Human Gate A와 B에서 filing identity와 표본 claim을 원문 대조했다.
- [ ] 최종 보고서의 claim ID가 accession, external ID 또는 FRED series ID로 연결된다.
- [ ] 사실, 해석, 미확인 사항과 추가 확인 항목이 구분되어 있다.
- [ ] FRED의 거시맥락을 기업별 인과관계라고 단정하지 않았다.

마지막으로 확인한다.

```text
git status --short
git diff
```

새 파일은 `git status --short`에서 `??`로 보이고, 이미 추적 중인 파일의 수정 내용은 `git diff`에서 보인다. 이것이 “AI가 무엇을 바꿨는지 사람이 검토하는” 가장 기본적인 통제다.

---

# 11. 자주 생기는 문제

## `git`, `codex`, `claude`, `py`가 “인식되지 않는 명령”이라고 나온다

설치 후 Terminal/PowerShell을 완전히 닫고 다시 연다. 그래도 안 되면 Agent에게 실행 파일 경로와 `PATH`를 진단하게 한다. 같은 도구를 여러 방식으로 중복 설치하지 않는다.

## Windows에서 `.venv\Scripts\Activate.ps1` 실행이 차단된다

현재 PowerShell 창에만 적용되는 다음 설정을 사용한다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

회사 정책이 이를 차단하면 활성화 없이 다음처럼 가상환경 Python을 직접 사용한다.

```powershell
.\.venv\Scripts\python.exe -m pip install edgartools tavily-python serpapi
.\.venv\Scripts\python.exe workshop\analyze_10k.py
```

## `python`이 Microsoft Store를 열거나 엉뚱한 버전을 실행한다

Windows에서는 `py -V:3.12`를 사용해 명시적으로 실행한다. 새 Python Install Manager 설치 후에는 PowerShell을 다시 열어야 할 수 있다.

## `ImportError`와 함께 `edgar` 관련 오류가 난다

이름이 비슷한 다른 패키지 `edgar`가 설치됐을 수 있다.

```text
python -m pip uninstall edgar
python -m pip install --upgrade edgartools
```

## SEC에서 403 또는 access denied가 발생한다

- `SEC_IDENTITY`에 실제 이름과 이메일이 있는지 확인한다.
- 반복 요청을 멈추고 잠시 기다린다.
- 초당 10회 이하 정책을 지킨다.
- VPN·회사 프록시의 공용 IP에서 다른 사용자가 과도한 요청을 보내는지 확인한다.

## Tavily 또는 SerpAPI가 인증·한도 오류를 반환한다

- 환경 변수 이름이 각각 `TAVILY_API_KEY`, `SERPAPI_KEY`인지 확인한다.
- 키 자체를 출력하지 말고 존재 여부만 확인한다.
- HTTP 401은 보통 키 문제, 429는 사용량·속도 한도 문제다.
- Dashboard에서 잔여 크레딧과 요청 로그를 확인한다.
- SerpAPI에서는 새 코드에 공식 `serpapi` 패키지를 사용하고 legacy `google-search-results`와 섞지 않는다.

## FRED가 키·series 오류를 반환한다

- 환경 변수 이름이 `FRED_API_KEY`인지 확인한다.
- [FRED series search](https://fred.stlouisfed.org/docs/api/fred/series_search.html)에서 series ID를 다시 찾는다.
- 같은 이름처럼 보여도 단위·빈도·계절조정이 다를 수 있으므로 metadata를 확인한다.
- 최신 관측값이 `.`이면 결측값이며 임의로 0으로 바꾸지 않는다.

## Agent가 외부 접속 또는 명령 실행 승인을 요청한다

요청 대상이 `sec.gov`, `pypi.org`, `github.com`, `tavily.com`, `serpapi.com` 등 수업 범위인지 확인한다. 명령을 읽고 범위가 맞을 때만 승인한다. 광범위한 관리자 권한, 홈 폴더 전체 접근, API 키 출력 요청은 거절한다.

## 수업 시간이 부족하다

검색 API 호출은 강사 시연으로 전환하고, 참가자는 EdgarTools 추출과 DD 메모 검증에 집중한다. 설치는 수업 전 체크리스트로 반드시 분리한다.

---

# 12. 보안·품질 가드레일

1. **API 키를 프롬프트에 붙여 넣지 않는다.** Agent 대화 기록도 기록이다.
2. **키를 코드나 `.env`에 저장해 Git에 올리지 않는다.** 수업은 세션 환경 변수를 사용한다.
3. **고객명·미공개 거래·개인정보를 공개 API나 개인 AI 계정에 입력하지 않는다.**
4. **AI가 제안한 설치 명령을 읽고 승인한다.** 관리자 권한은 꼭 필요한 경우에만 사용한다.
5. **공식 원문으로 돌아간다.** Tavily·SerpAPI 결과나 AI 요약을 최종 증거로 사용하지 않는다.
6. **문서 식별자를 남긴다.** form, filing date, reporting period, accession number, URL을 기록한다.
7. **숫자의 의미를 검증한다.** 단위, 기간, XBRL tag, restatement 여부를 확인한다.
8. **전문가 판단을 대체하지 않는다.** Agent는 조사·추출·초안·체크리스트 도구다.
9. **맥락과 인과를 구분한다.** FRED 추세는 환경 설명이며 해당 기업의 원인을 자동으로 입증하지 않는다.

---

# 13. 수업 후 응용 아이디어

- Watchlist 기업의 새 10-K/10-Q/8-K 감시
- 전년도 10-K와 최신 10-K Risk Factors 변경 비교
- 계약서 조항과 공시된 material agreement 대조
- 회사별 revenue·margin·cash flow 표준 비교표
- 주요 회계정책과 footnote 변화 탐지
- SEC 원문 링크가 달린 Investment Committee 사전 메모

자동화로 확장할 때는 먼저 한 기업·한 공시·한 보고서로 정확성을 검증한 뒤 범위를 늘린다.

---

# 14. 공식 자료

- [OpenAI Codex CLI 공식 문서](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI Codex 공식 GitHub 저장소](https://github.com/openai/codex)
- [Claude Code 설치 공식 문서](https://code.claude.com/docs/en/getting-started)
- [Git for Windows 공식 설치 문서](https://git-scm.com/install/windows.html)
- [Python Install Manager 공식 문서](https://docs.python.org/3/using/windows.html)
- [Tavily Quickstart](https://docs.tavily.com/documentation/quickstart)
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [FRED API Overview](https://fred.stlouisfed.org/docs/api/fred/overview.html)
- [FRED Series Observations](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)
- [FRED Series Search](https://fred.stlouisfed.org/docs/api/fred/series_search.html)
- [SerpAPI Python Integration](https://serpapi.com/integrations/python)
- [SerpAPI Google Search API](https://serpapi.com/search-api)
- [SerpAPI 공식 Python SDK](https://github.com/serpapi/serpapi-python)
- [SEC EDGAR Data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [SEC Developer Resources와 Fair Access](https://www.sec.gov/about/developer-resources)
- [EdgarTools GitHub](https://github.com/dgunning/edgartools)
- [EdgarTools Quickstart](https://github.com/dgunning/edgartools/blob/main/docs/quickstart.md)

> 제품 설치 방법과 요금·무료 한도는 변경될 수 있다. 교육 직전 위 공식 자료에서 명령과 정책을 다시 확인한다.

---

## 한 줄 정리

> **검색으로 후보를 찾고, GitHub에서 도구를 가져오고, 공식 API에서 근거를 확보하고, AI Agent로 반복 작업을 줄이되, 최종 판단은 사람이 원문에서 검증한다.**
