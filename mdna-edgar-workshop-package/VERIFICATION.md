# 패키지 검증 기록

## 검증 환경

- 검증일: 2026-08-18
- 운영체제: macOS arm64
- Python: 3.10.2
- EdgarTools: 5.49.0
- Tavily SDK: 0.7.27
- 검증 명령: `scripts/check_environment.py`, `scripts/extract_mdna.py`, hybrid script mock tests

## 라이브 EDGAR 실행 결과

| Ticker | 문서 | 회계연도 말 | MD&A 문자 수 | 추출 방법 | 상태 |
|---|---|---:|---:|---|---|
| AAPL | current 10-K | 2025-09-27 | 21,009 | guarded legacy chunked Item 7 | PASS |
| AAPL | prior 10-K | 2024-09-28 | 18,324 | guarded legacy chunked Item 7 | PASS |
| MSFT | current 10-K | 2026-06-30 | 57,762 | guarded legacy chunked Item 7 | PASS |
| MSFT | prior 10-K | 2025-06-30 | 53,140 | guarded legacy chunked Item 7 | PASS |

## 확인한 통제

- 최신·직전 non-amended 10-K 선택
- accession number·제출일·회계연도 말·SEC URL 기록
- Item 7A heading 혼입 검사
- Item 8 heading 혼입 검사
- 최소·최대 섹션 길이 검사
- 공개 section 결과가 비었을 때 fallback과 warning 기록
- SEC identity가 manifest와 추출 Markdown에 저장되지 않음
- 기존 산출물은 `--force` 없이는 덮어쓰지 않음
- Tavily 요청이 `topic=news`, `include_answer=False`와 날짜 필터를 사용
- Tavily 결과의 초기 역할이 `unresolved`이며 API key가 JSON에 저장되지 않음
- FRED metadata·observations가 series ID와 함께 저장되고 missing value `.`가 null로 변환됨
- FRED 결과의 역할이 `context_only`이며 API key가 JSON에 저장되지 않음
- Tavily·FRED 키가 없을 때 비밀값을 출력하지 않고 명확한 오류로 종료

## Hybrid script 검증 범위

Tavily와 FRED의 호출 형식·응답 변환·스키마·덮어쓰기·비밀값 비저장을 mock 응답으로 실행 검증했다. 참가자 개인 key를 사용한 라이브 호출은 패키지에 포함하거나 기록하지 않았다. 라이브 결과의 내용과 사용량 한도는 수업 당일 각 계정에서 확인한다.

## 알려진 사항

EdgarTools 5.49.0에서 일부 대표 10-K는 `TenK.management_discussion` 또는 `TenK['Item 7']`가 빈 문자열을 반환했지만 내부 chunked document에는 정상 Item 7이 존재했다. 패키지는 이 경우를 감지해 보조 추출을 사용하고 manifest에 방법과 warning을 남긴다. private fallback은 향후 EdgarTools에서 변경될 수 있으므로 버전 변경 시 재검증해야 한다. 모든 경우 최종 근거는 SEC 원문이다.
