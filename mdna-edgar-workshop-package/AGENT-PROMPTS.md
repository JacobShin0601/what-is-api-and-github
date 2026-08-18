# 단계별 Agent 프롬프트

아래 프롬프트에서 `AAPL`을 실습 ticker로 바꾼다. 한 번에 전체를 실행하지 않고 Turn별로 결과를 확인한다.

## Turn 0 — 입력·경계 점검

```text
AGENTS.md를 읽고 workspace/AAPL을 대상으로 작업해.

아직 분석 파일을 만들거나 기존 파일을 수정하지 마.
다음 입력만 점검해서 표로 보고해:
- filing_manifest.json 존재 및 JSON 파싱 가능 여부
- current와 prior의 form, filing_date, period_of_report, accession_number
- mdna_current.md와 mdna_prior.md의 크기와 첫 소제목
- extraction_check.md의 최종 상태
- Item 7A 또는 Item 8 혼입 징후
- 분석 시작 가능 여부

PASS가 아니면 원인과 안전한 해결 방법만 제시하고 멈춰.
PASS이면 “Turn 1 진행 가능”이라고 쓰고 멈춰.
```

## Turn 1 — 전년 대비 서술 변화

```text
workspace/AAPL의 mdna_current.md와 mdna_prior.md를 비교해.
원본 파일은 수정하지 마.

단순 문장 diff가 아니라 경제적 의미의 변화를 다음 유형으로 분류해:
- added: 새로 등장
- removed: 사라짐
- stronger: 강조 강화
- weaker: 강조 완화
- quantified_change: 숫자 변화
- causal_change: 원인 설명 변화
- outlook_change: 전망·불확실성 변화

주제는 revenue, margin, segment, geography, working_capital,
liquidity, debt, capex, critical_estimates, one_offs, outlook로 분류해.

각 변화에 change_id, topic, change_type, current_evidence,
prior_evidence, analyst_note, confidence를 붙여
workspace/AAPL/mdna_diff.md를 만들어.

경영진이 말하지 않은 원인은 추론하지 마.
파일을 만든 뒤 주요 변화 5개만 화면에 보고하고 멈춰.
```

## Turn 2 — 경영진 주장 register

```text
workspace/AAPL/mdna_current.md에서 검증 가능한 경영진의 주장을 추출해.
mdna_diff.md는 변화의 우선순위를 정하는 데만 사용해.

특히 다음 표현을 찾되 단어 검색에만 의존하지 마:
- 증가·감소의 원인
- 가격·판매량·제품 구성·환율 효과
- 비용 또는 마진의 원인
- 유동성이 충분하다는 판단
- Capex·투자·자금조달 계획
- 중요한 회계 추정
- 미래 전망과 불확실성

templates/mdna_claims.csv의 열 순서를 그대로 사용해
workspace/AAPL/mdna_claims.csv를 만들어.

규칙:
- management_claim과 analyst_interpretation을 분리
- historical_or_forward_looking을 표시
- 아직 숫자를 확인하지 않았다면 verification_status=needs_source
- evidence_excerpt는 짧게 기록하고 source_heading을 함께 기록
- 확인되지 않은 숫자를 만들지 않음
- 모든 행에 claim_id와 accession_number를 연결

작성 후 상태별 행 개수만 보고하고 멈춰.
```

## Turn 3 — 재무 숫자 교차검증

```text
workspace/AAPL/mdna_claims.csv의 각 주장을 검토해.
filing_manifest.json의 공시와 EdgarTools 재무제표 객체 또는 SEC Item 8을 사용해
검증 가능한 숫자를 확인해.

각 숫자에 다음을 기록해:
- metric
- current_value
- prior_value
- unit와 currency
- period
- financial_statement_source

verification_status는 다음 중 하나만 사용해:
- verified
- partial
- needs_source
- conflict
- not_applicable

다음 경우 verified를 사용하지 마:
- 기간 또는 단위가 불명확
- MD&A 숫자와 재무제표 개념이 정확히 일치하지 않음
- 경영진의 인과관계까지는 숫자로 확인할 수 없음
- non-GAAP 조정의 원문 표를 확인하지 않음

mdna_claims.csv를 갱신하되 행을 조용히 삭제하지 마.
변경 후 verified, partial, needs_source, conflict 개수를 보고하고 멈춰.
```

## Turn 4 — Tavily·FRED 외부 근거 분류와 통합

먼저 `scripts/search_external_news.py`를 사용해 선택한 핵심 claim 1–3개와 관련된 최신 사건을 수집한다. FRED 트랙을 선택한 경우에만 `scripts/fetch_fred_context.py`를 실행한다. 키 값은 Agent에게 전달하지 않고 사용자가 터미널 환경 변수로 설정한다.

```text
workspace/AAPL의 mdna_claims.csv, tavily_evidence.json을 읽어.
fred_context.json이 있으면 함께 읽고, 없어도 오류로 보지 마.

templates/external_evidence.csv 형식으로 external_evidence.csv를 만들고
templates/integrated_claim_register.csv 형식으로 integrated_claim_register.csv를 만들어.

Tavily 각 결과는 URL의 원문을 열 수 있고 회사·규제기관·신뢰할 수 있는 보도인지 확인한 뒤
corroboration, contradiction, unresolved 중 하나로 분류해.
검색 snippet만으로 primary_verification을 부여하지 마.

FRED 시계열은 반드시 context_only로 분류해.
금리·물가·고용과 회사 지표의 동행만으로 인과관계를 단정하지 마.

각 claim에 다음을 연결해:
- SEC MD&A 원문과 accession
- 재무 숫자 검증 상태
- 관련 Tavily external_id
- 관련 FRED series_id
- 서로 충돌하는 근거
- 여전히 답하지 못한 질문

완료 후 evidence_role별 개수와 contradiction 목록을 보고하고 멈춰.
```

## Turn 5 — 세 직군 검토

```text
workspace/AAPL/mdna_diff.md, mdna_claims.csv,
external_evidence.csv와 integrated_claim_register.csv를 읽고
templates/role_review.md 형식으로 workspace/AAPL/role_review.md를 만들어.

투자 관점:
- 성장의 질과 지속 가능성
- 가격·판매량·mix·환율 구분
- 마진과 현금흐름
- Capex와 유동성

회계 관점:
- 중요한 회계 추정
- 반복되는 일회성·조정 항목
- 운전자본과 현금흐름
- 손상·충당금·매출인식

법무 관점:
- 역사적 사실과 미래예측 진술 구분
- 불확실성 표현의 강화·완화
- Item 1A와 교차 확인할 항목
- 규제·소송·계약상 의무 관련 공백

각 항목에 관련 claim_id를 붙여.
공시 후 사건과 거시맥락을 회사의 원래 MD&A 주장과 구분해.
투자 추천, 법률 의견, 감사 결론을 작성하지 마.
완료 후 각 관점의 최우선 검토 항목 하나씩만 보고하고 멈춰.
```

## Turn 6 — 최종 1페이지 DD 메모

```text
workspace/AAPL의 mdna_diff.md, mdna_claims.csv, external_evidence.csv,
integrated_claim_register.csv, role_review.md를 사용해
templates/mdna_review.md 형식으로 workspace/AAPL/mdna_review.md를 만들어.

다섯 블록으로 제한해:
1. 경영진이 가장 강조한 변화
2. 실제 숫자로 확인된 주장
3. 부분적으로만 확인된 주장
4. 전년 대비 새로 등장한 우려
5. 공시 후 corroboration·contradiction과 context_only
6. 추가 원문 검토가 필요한 항목

본문의 핵심 주장마다 claim_id를 붙여.
verified가 아닌 주장을 확정적 사실처럼 쓰지 마.
마지막에 Human Gate 표본 3개를 제안하되 승인 처리하지 마.
투자 추천과 목표가격은 포함하지 마.
```

## Turn 7 — Human Gate 반영

사람이 SEC 원문을 확인한 뒤에만 사용한다.

```text
내가 확인한 claim_id와 결과는 다음과 같아:
[여기에 사람이 확인한 claim_id, 원문 위치, 결과 입력]

이 확인 결과만 mdna_claims.csv, integrated_claim_register.csv와 mdna_review.md에 반영해.
확인하지 않은 다른 claim의 상태는 바꾸지 마.
변경 내역을 별도 목록으로 보고해.
```
