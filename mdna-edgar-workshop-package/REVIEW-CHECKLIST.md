# Human Review Checklist

## A. 공시 식별

- [ ] 회사명과 ticker가 맞다.
- [ ] 최신·직전 문서가 모두 10-K이며 10-K/A가 섞이지 않았다.
- [ ] 두 문서의 회계연도 말과 제출일을 구분했다.
- [ ] accession number와 SEC URL이 기록돼 있다.
- [ ] EdgarTools 버전과 추출 방법이 manifest에 기록돼 있다.

## B. MD&A 추출 경계

- [ ] 실제 Part II, Item 7 제목에서 시작한다.
- [ ] 목차만 추출된 것이 아니다.
- [ ] MD&A의 주요 소제목과 본문이 존재한다.
- [ ] Item 7A 전체가 포함되지 않았다.
- [ ] Item 8 재무제표 전체가 포함되지 않았다.
- [ ] parser warning과 fallback 사용 여부를 확인했다.

## C. 전년 비교

- [ ] 비교 대상 기간이 연속된 회계연도다.
- [ ] 문장 변화와 경제적 의미의 변화를 구분했다.
- [ ] added·removed·stronger·weaker를 근거와 함께 기록했다.
- [ ] 단순 표기 변경을 중요한 변화로 과장하지 않았다.
- [ ] 삭제된 설명도 검토했다.

## D. Claim register

- [ ] 경영진 주장과 Agent 해석이 분리돼 있다.
- [ ] 역사적 사실과 미래예측 진술이 구분돼 있다.
- [ ] 숫자에 기간·단위·통화·부호가 있다.
- [ ] 인과관계가 숫자로 완전히 증명되지 않는 경우 partial로 표시했다.
- [ ] non-GAAP 숫자의 조정표를 확인했다.
- [ ] 근거 없는 값은 needs_source로 남겼다.
- [ ] 모든 핵심 주장에 claim_id와 accession number가 있다.

## E. 직군별 검토

- [ ] 투자: 성장, 마진, 현금흐름, Capex, 유동성을 확인했다.
- [ ] 회계: 회계 추정, 일회성 항목, 운전자본, 인식·손상을 확인했다.
- [ ] 법무: 미래예측, 불확실성, Risk Factors 연결을 확인했다.
- [ ] 투자 추천·법률 의견·감사 결론으로 과장하지 않았다.

## F. 외부 근거와 기준일

- [ ] Tavily 결과의 원문 URL·발행일·발행기관을 열어 확인했다.
- [ ] 검색 snippet만으로 `primary_verification`을 부여하지 않았다.
- [ ] 지지 근거와 반대 근거를 모두 찾고 `corroboration`·`contradiction`을 구분했다.
- [ ] FRED series ID·단위·빈도·관측 기간·last updated를 기록했다.
- [ ] FRED는 `context_only`로 두고 기업별 인과관계를 단정하지 않았다.
- [ ] 분석 기준일(as-of date) 이후 자료를 당시 이용 가능했던 근거처럼 쓰지 않았다.

## G. 최종 승인

- [ ] 중요한 숫자 주장 하나를 SEC 원문에서 확인했다.
- [ ] 유동성·Capex·차입 주장 하나를 확인했다.
- [ ] partial·needs_source·conflict 주장 하나를 확인했다.
- [ ] verified가 아닌 주장을 확정적으로 쓰지 않았다.
- [ ] 메모에 사용된 claim_id가 register에 존재한다.
- [ ] 사람이 확인한 시각과 검토자를 기록했다.
- [ ] 가장 중요한 contradiction 하나를 원문에서 확인했다.
