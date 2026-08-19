# 문제 해결

## `ModuleNotFoundError: No module named 'edgar'`

가상환경이 활성화됐는지 확인하고 패키지 루트에서 설치한다.

```text
python -m pip install -r requirements.txt
```

같은 명령은 Tavily SDK가 없을 때 발생하는 `No module named 'tavily'`도 해결한다.

## Tavily 또는 FRED 키 오류

- 패키지 루트에 `.env`가 없으면 `python scripts/setup_env.py`를 실행한다.
- `.env`의 변수 이름은 각각 `TAVILY_API_KEY`, `FRED_API_KEY`다. 등호 오른쪽에 실제 값을 넣고 저장한다.
- 키 값을 확인하기 위해 화면에 출력하지 않는다. `python scripts/check_environment.py --require-tavily`로 존재 여부만 확인한다.
- 401은 보통 인증, 429는 사용량·속도 한도를 확인한다.
- Tavily 검색이 비어 있으면 회사명·ticker·기간·사건 유형을 포함해 query를 좁힌다.
- FRED series ID가 틀리면 FRED 공식 series search에서 확인한다.
- 키가 없는 참가자는 강사가 제공한 sample JSON으로 Evidence Register 분류를 연습한다.

## PowerShell에서 `.venv` 활성화가 차단됨

현재 PowerShell 창에만 적용한다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

회사 정책이 실행 정책 변경을 금지하면 활성화 없이 가상환경 Python을 직접 사용한다.

```powershell
.\.venv\Scripts\python.exe scripts\extract_mdna.py --ticker AAPL
```

## `SEC_IDENTITY`가 없다고 나옴

SEC 요청에는 이름과 연락 가능한 이메일이 필요하다. `.env`를 열어 다음 줄의 예시를 실제 정보로 바꾸고 저장한다.

```text
SEC_IDENTITY="Your Name your-email@example.com"
```

공유 화면이나 제출 파일에 개인 이메일을 복사하지 않는다. identity는 manifest에 저장되지 않는다.

## `.env`를 수정했는데 반영되지 않음

- 명령을 패키지 폴더에서 실행했는지 확인한다.
- `.env.txt`가 아니라 정확히 `.env`인지 확인한다. Windows 메모장에서는 파일 확장자가 숨겨질 수 있다.
- 운영체제에 이미 같은 이름의 환경 변수가 있으면 그 값이 우선한다. 기존 세션 변수를 제거하거나 새 터미널에서 다시 실행한다.
- `.env`의 따옴표가 짝이 맞는지, 변수명 앞에 공백이 없는지 확인한다.
- 키 값은 출력하지 말고 환경 점검표의 PASS/FAIL만 확인한다.

## SEC 요청 오류 또는 속도 제한

- 짧은 시간에 반복 실행하지 않는다.
- 여러 참가자가 동시에 같은 네트워크를 사용할 때 조별로 순차 실행한다.
- 잠시 기다린 뒤 한 번만 다시 시도한다.
- 무한 재시도 코드를 만들지 않는다.
- 강사가 준비한 sample 또는 사전 추출 파일로 실습을 계속한다.

## MD&A가 비어 있음

일부 문서는 최신 section parser가 섹션을 감지했어도 텍스트가 비어 있을 수 있다. `extract_mdna.py`는 다음 순서로 안전하게 fallback한다.

1. `TenK.management_discussion`
2. `TenK['Item 7']`
3. 현재 버전의 legacy chunked document
4. filing 전체 텍스트의 Item 7–7A 경계 탐색

fallback이 사용되면 manifest와 extraction check에 기록된다. 결과가 PASS가 아니면 분석하지 않는다.

## Item 7A 또는 Item 8이 섞임

- `extraction_check.md`의 경고를 확인한다.
- SEC 원문에서 Item 7의 시작과 Item 7A의 시작을 찾는다.
- Agent에게 잘못 섞인 텍스트를 요약시키지 않는다.
- 수동 수정 시 원본 파일을 덮어쓰지 말고 `mdna_current_reviewed.md`처럼 별도 파일을 만든다.
- 수동 경계와 검토자를 manifest 또는 별도 메모에 기록한다.

## 최신 문서가 10-K/A임

스크립트는 기본적으로 amendment를 제외한다. 수정공시 자체를 연구할 목적이면 별도 실습으로 진행하고, 원 10-K와 10-K/A의 관계를 명확히 기록한다.

## 회사가 20-F를 제출함

외국기업은 10-K가 아니라 20-F를 제출할 수 있다. 20-F에서 운영·재무 검토는 일반적으로 Item 5에 있으며 이 패키지의 자동 추출 대상이 아니다. 다른 미국 국내 발행인을 선택하거나 별도 20-F 실습을 설계한다.

## 분기 MD&A를 보고 싶음

10-Q에서는 MD&A가 일반적으로 Part I, Item 2다. 이 패키지의 `extract_mdna.py`는 10-K Item 7 전용이다. 파일명과 경계 검증 기준을 그대로 사용하지 않는다.

## 숫자가 MD&A와 재무제표에서 다름

다음을 확인한다.

- 연간·분기·누적 기간 차이
- GAAP·non-GAAP 차이
- 보고 단위: 달러, 천, 백만
- 계속영업·중단영업 범위
- 환율 고정 기준 또는 organic growth
- segment와 consolidated 기준

일치 이유를 확인할 때까지 `partial` 또는 `conflict`를 유지한다.
