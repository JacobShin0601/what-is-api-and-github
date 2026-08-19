# API × MCP × GitHub × AI Agent Workshop

투자·법무·회계 전문직을 위한 60분 실습 자료입니다. API와 MCP의 차이, GitHub 저장소 재사용, 공식 데이터 기반 10-K 분석을 Claude Code 또는 Codex와 함께 진행합니다.

## 수업 흐름

1. Windows PowerShell 또는 macOS Terminal 환경 준비
2. API·MCP의 역할과 증권사 주문 API 흐름 이해
3. Tavily·SerpAPI·FRED 등 대표 API 연결
4. `git clone`으로 공개 저장소와 실습 패키지 재사용
5. EdgarTools로 최신·직전 10-K MD&A 추출
6. EDGAR·Tavily·FRED 근거를 Evidence Register로 통합
7. 투자·법무·회계 관점 검토와 Human Gate

## 시작은 `.env` 한 파일만

저장소를 받은 뒤 실습 패키지 폴더에서 다음 순서로 시작합니다.

```text
cd mdna-edgar-workshop-package
python scripts/setup_env.py
```

Windows는 `notepad .env`, macOS는 `open -e .env`로 파일을 열어 `SEC_IDENTITY`와 사용할 API key만 채웁니다. 이후 모든 실습 스크립트가 같은 `.env`를 자동으로 읽습니다. 실제 `.env`는 Git에서 제외되고, 공유되는 `.env.example`에는 변수명과 빈 자리만 있습니다.

## 바로 열기

- [전체 워크숍 교안](API-GitHub-AI-Agent-60min-workshop.md)
- [수업용 HTML 슬라이드](api-github-ai-agent-classroom.html)
- [MD&A 실행 패키지](mdna-edgar-workshop-package/README.md)
- [Windows·macOS 배포용 ZIP](mdna-edgar-workshop-package.zip)

## Evidence 구조

```text
SEC / EdgarTools ── 공식 공시·재무 숫자 ── primary verification
Tavily ─────────── 공시 후 최신 사건 ───── corroboration / contradiction
FRED ───────────── 공식 거시지표 ───────── context_only
                                      ↓
                         Integrated Evidence Register
                                      ↓
                                 Human Gate
```

## 주의사항

- 실제 API key는 로컬 `.env` 한 파일에만 저장하고 코드·프롬프트·Git에는 넣지 않습니다.
- Tavily 검색 결과는 원문 후보이며 공식 공시를 대체하지 않습니다.
- FRED의 거시 추세는 개별 기업의 인과관계를 자동으로 증명하지 않습니다.
- 이 자료는 교육용이며 투자 추천, 법률 의견, 회계감사 결론 또는 자동매매 지시를 생성하지 않습니다.
