# 공식 참고자료

## SEC

- [Form 10-K 원문 양식](https://www.sec.gov/files/form10-k.pdf) — Item 7 MD&A, Item 7A 시장위험, Item 8 재무제표 구분
- [SEC EDGAR Company Filings](https://www.sec.gov/edgar/searchedgar/companysearch) — 회사별 원문 공시 검색
- [SEC Developer Resources](https://www.sec.gov/about/developer-resources) — EDGAR 데이터와 개발자 자료
- [SEC Privacy and Security Policy](https://www.sec.gov/privacy.htm) — 자동 요청과 접근 정책 확인

## EdgarTools

- [EdgarTools GitHub 저장소](https://github.com/dgunning/edgartools)
- [Business Overview Data Sources Guide](https://edgartools.readthedocs.io/en/latest/guides/business-overview-data-sources-guide/) — `TenK.management_discussion`과 Item 7 접근
- [Common Pitfalls](https://edgartools.readthedocs.io/en/stable/common-pitfalls/) — filing item key와 결측 섹션 처리
- [Changelog](https://github.com/dgunning/edgartools/blob/main/CHANGELOG.md) — 10-K Item 7·7A 경계 수정 기록

## Tavily

- [Tavily Python SDK quickstart](https://docs.tavily.com/sdk/python/quick-start) — `TavilyClient`와 환경 변수
- [Search API reference](https://docs.tavily.com/documentation/api-reference/endpoint/search) — `topic=news`, 날짜 범위, 도메인 필터와 결과 필드

## FRED

- [FRED API overview](https://fred.stlouisfed.org/docs/api/fred/overview.html) — API 구조와 key
- [Series observations](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) — 관측값·기간·빈도 파라미터
- [Series search](https://fred.stlouisfed.org/docs/api/fred/series_search.html) — 관련 series ID 찾기
- [Vintage dates](https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html) — 당시 이용 가능했던 데이터 재현

## 환경 설정

- [python-dotenv documentation](https://bbc2.github.io/python-dotenv/) — `.env` 로드, 기존 운영체제 환경변수 우선, Git 제외 원칙

## 적용 원칙

- 라이브러리 결과보다 SEC 원문을 최종 근거로 사용한다.
- 수업 환경에서는 `requirements.txt`의 검증 버전을 유지한다.
- 다른 버전으로 변경하면 `scripts/extract_mdna.py`를 대표 종목으로 다시 검증한다.
- SEC identity와 API key는 Git에서 제외된 `.env`로 전달하고 산출물에는 저장하지 않는다.
- Tavily는 최신 근거 후보를 찾는 탐색 도구이며 원 출처를 다시 연다.
- FRED는 공식 거시맥락이지만 개별 기업의 인과관계 증거로 사용하지 않는다.
