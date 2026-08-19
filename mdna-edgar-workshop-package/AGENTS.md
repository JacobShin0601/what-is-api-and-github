# Agent Instructions — MD&A Evidence-to-Claim Lab

이 프로젝트에서 Agent는 SEC 10-K MD&A 분석을 보조한다. 최종 판단자는 사람이다.

## 시작 순서

1. `README.md`, `PARTICIPANT-WORKBOOK.md`, `AGENT-PROMPTS.md`를 읽는다.
2. `.env` 파일의 존재와 필요한 변수의 설정 여부만 확인한다. 값은 읽어 화면에 표시하거나 프롬프트로 요청하지 않는다.
3. 사용자가 지정한 `workspace/<TICKER>/filing_manifest.json`을 연다.
4. `extraction_check.md`가 `PASS`인지 확인한다.
5. PASS가 아니면 분석하지 말고 문제와 해결 후보만 보고한다.
6. PASS이면 `AGENT-PROMPTS.md`의 Turn 순서대로 진행한다.

## 변경 범위

- 원본인 `mdna_current.md`, `mdna_prior.md`, `filing_manifest.json`은 수정하지 않는다.
- 분석 결과는 같은 ticker 폴더의 새 파일에만 기록한다.
- 한 Turn에서 요청된 산출물만 만든 뒤 멈춘다.
- 파일을 덮어쓰기 전에 기존 파일의 목적과 사용자 변경 여부를 확인한다.

## 근거 규칙

- 회사 경영진의 서술, 재무제표 숫자, Agent의 해석을 명확히 분리한다.
- 주장에는 `claim_id`, 공시연도, source section, accession number를 연결한다.
- 짧은 evidence excerpt만 사용하고 가능하면 소제목과 문단 위치를 함께 기록한다.
- 숫자에는 기간, 단위, 통화, 부호를 기록한다.
- 검증하지 못한 값은 만들지 않고 `needs_source`로 표시한다.
- 전년 비교에서 단순 문장 변화와 경제적 의미의 변화를 구분한다.
- Tavily 결과는 원문을 연 뒤 `corroboration`, `contradiction`, `unresolved` 중 하나로 분류한다.
- FRED 시계열은 `context_only`로만 사용하며 기업별 인과관계를 증명한다고 쓰지 않는다.
- 분석의 기준일(as-of date)과 외부 근거의 발행일·관측일을 기록한다.

## 금지사항

- 투자 매수·매도 추천 또는 목표가격 생성
- 실제 거래·주문 실행
- 법률 의견, 감사 의견 또는 세무 결론으로 표현
- API key, 토큰, 계좌번호, 개인 연락처 출력
- API key를 결과 JSON, 로그, 프롬프트 또는 Git에 저장
- `.env` 내용을 읽어 출력·요약·복사하거나 Git에 추가
- SEC 원문을 확인하지 않은 상태에서 `verified` 사용
- 추출 실패를 무시하고 분석 계속

## 상태값

- `verified`: 원문과 숫자를 사람이 또는 명시된 절차로 확인
- `partial`: 일부 근거만 확인
- `needs_source`: 필요한 원문이나 숫자 없음
- `conflict`: 경영진 설명과 확인된 데이터가 충돌
- `not_applicable`: 해당 없음

외부 근거 역할은 다음 다섯 값만 사용한다.

- `primary_verification`: SEC·회사 원문이나 공식 통계로 사실을 직접 확인
- `corroboration`: 다른 출처가 주장과 같은 방향의 정보를 제공
- `contradiction`: 다른 출처가 주장과 충돌하는 정보를 제공
- `context_only`: 배경 환경만 설명하며 회사별 인과관계는 확인하지 못함
- `unresolved`: 원문·기간·범위가 부족해 역할을 결정하지 못함
