import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("전북특별자치도 일산화탄소 농도 시각화 (그래프 버전)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

@st.cache_data
def load_data(file):
    df = pd.read_csv(file, encoding="cp949")
    df["측정소"] = df["측정소"].str.strip().str.replace(r'\s+', '', regex=True)
    return df

if uploaded_file:
    df = load_data(uploaded_file)

    # 필수 컬럼 체크
    if "측정소" not in df.columns or "일산화탄소" not in df.columns:
        st.error("CSV 파일에 '측정소'와 '일산화탄소' 컬럼이 있어야 합니다.")
    else:
        # 결측치 제거
        df = df.dropna(subset=["측정소", "일산화탄소"])

        # 데이터 미리보기
        st.subheader("데이터 미리보기")
        st.dataframe(df)

        # 시각화
        st.subheader("일산화탄소 농도 막대 그래프")

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("측정소:N", sort="-y", title="측정소"),
            y=alt.Y("일산화탄소:Q", title="일산화탄소 (ppm)"),
            color=alt.Color("일산화탄소:Q", scale=alt.Scale(scheme="redyellowgreen"), legend=None),
            tooltip=["측정소", "일산화탄소"]
        ).properties(width=800, height=500)

        st.altair_chart(chart, use_container_width=True)
else:
    st.info("CSV 파일을 업로드해주세요.")
