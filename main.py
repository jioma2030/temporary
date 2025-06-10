import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(layout="wide")
st.title("전북특별자치도 일산화탄소 농도 시각화")

# CSV 파일 경로 (수정 가능)
csv_path = "전북특별자치도_대기오염정보.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, encoding="cp949")
    df["측정소"] = df["측정소"].str.strip().str.replace(r'\s+', '', regex=True)
    return df

try:
    df = load_data(csv_path)

    # 필수 컬럼 확인
    if "측정소" not in df.columns or "일산화탄소" not in df.columns:
        st.error("CSV 파일에 '측정소'와 '일산화탄소' 컬럼이 있어야 합니다.")
    else:
        df = df.dropna(subset=["측정소", "일산화탄소"])

        st.subheader("일산화탄소 농도 막대 그래프")

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("측정소:N", sort="-y", title="측정소"),
            y=alt.Y("일산화탄소:Q", title="일산화탄소 (ppm)"),
            tooltip=["측정소", "일산화탄소"],
            color=alt.value("#1f77b4")  # 고정된 파란색
        ).properties(width=800, height=500)

        st.altair_chart(chart, use_container_width=True)

except FileNotFoundError:
    st.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
except Exception as e:
    st.error(f"오류 발생: {e}")
