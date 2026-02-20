# SearchRealEstateWithCodex

네이버 부동산 웹에서 아파트 매물 정보를 수집하고 CSV/웹으로 확인하는 Python MVP입니다.

## 기능
- 지역 선택(예: `gangnam`, `songpa`, `bundang`)
- 네이버 부동산 페이지 로딩 후 매물 리스트 추출
- CSV 저장(`utf-8-sig`)
- Streamlit으로 결과 조회

## 빠른 시작
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## 수집 실행
```bash
PYTHONPATH=src python -m realestate.app --region gangnam --max-items 100 --csv output/listings.csv
```

옵션:
- `--json`: 결과를 JSON으로 출력
- `--headed`: 브라우저 UI를 보면서 실행

## 웹 조회
```bash
streamlit run streamlit_app.py
```

## 테스트
```bash
PYTHONPATH=src pytest -q
```

## 주의
- 실제 웹 구조 변경에 따라 CSS selector는 조정이 필요할 수 있습니다.
- 운영 전, 대상 서비스의 이용약관과 robots 정책을 반드시 확인하세요.
