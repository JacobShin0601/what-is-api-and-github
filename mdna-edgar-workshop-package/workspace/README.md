# Workspace

`scripts/extract_mdna.py --ticker <TICKER>`를 실행하면 이 폴더 아래에 ticker별 디렉터리가 생성된다. `search_external_news.py`와 선택형 `fetch_fred_context.py`도 같은 ticker 폴더에 외부 근거 JSON을 저장한다. 원본 추출 파일과 원시 JSON은 수정하지 않고 Agent 분석 결과를 같은 ticker 폴더의 CSV·Markdown 새 파일로 저장한다.
