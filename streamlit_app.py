from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Naver Real Estate Listings", layout="wide")
st.title("네이버 부동산 아파트 매물/시세 뷰어")

csv_path = st.text_input("CSV 경로", value="output/listings.csv")
path = Path(csv_path)

if not path.exists():
    st.warning("CSV 파일이 없습니다. 먼저 수집기를 실행해 주세요.")
    st.stop()


df = pd.read_csv(path)
st.caption(f"총 {len(df)}건")

region_options = ["전체"] + sorted(df["region"].dropna().unique().tolist())
region = st.selectbox("지역 필터", options=region_options, index=0)

if region != "전체":
    df = df[df["region"] == region]

keyword = st.text_input("단지명 검색")
if keyword:
    df = df[df["complex_name"].str.contains(keyword, na=False)]

st.dataframe(df, use_container_width=True)
