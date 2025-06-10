import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="에너지 사용 및 온실가스 배출량 시각화", layout="wide")
st.title("📊 산업부문 에너지사용 및 온실가스배출 통계 시각화")

uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # '합계'와 지역별 배출량 열을 숫자로 변환
    value_cols = ['합계'] + list(df.columns[5:])
    for col in value_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    st.sidebar.header("🔍 시각화 옵션")

    # 필터 옵션
    업종들 = sorted(df['업종'].dropna().unique())
    선택_업종 = st.sidebar.multiselect("업종 선택", 업종들, default=업종들)

    구분들 = sorted(df['구분'].dropna().unique())
    선택_구분 = st.sidebar.multiselect("연료 구분 선택", 구분들, default=구분들)

    연료들 = sorted(df['연료명'].dropna().unique())
    선택_연료 = st.sidebar.multiselect("연료명 선택", 연료들, default=연료들)

    시각화_종류 = st.sidebar.selectbox("📈 시각화 유형 선택", [
        "업종별 온실가스 합계", 
        "지역별 배출량 히트맵", 
        "연료 구분별 비율 (파이 차트)", 
        "업종-연료별 막대그래프"
    ])

    # 필터링
    필터링된_df = df[
        df['업종'].isin(선택_업종) &
        df['구분'].isin(선택_구분) &
        df['연료명'].isin(선택_연료)
    ]

    # 시각화 1: 업종별 합계
    if 시각화_종류 == "업종별 온실가스 합계":
        grouped = 필터링된_df.groupby('업종')['합계'].sum().sort_values(ascending=False)

        st.subheader("🏭 업종별 온실가스 배출량 합계")
        fig, ax = plt.subplots(figsize=(10, 6))
        grouped.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel("천tCO₂")
        ax.set_title("업종별 온실가스 배출량")
        ax.grid(axis='y')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    # 시각화 2: 지역별 히트맵
    elif 시각화_종류 == "지역별 배출량 히트맵":
        지역컬럼 = df.columns[5:]
        grouped = 필터링된_df.groupby('업종')[지역컬럼].sum()

        st.subheader("🗺️ 업종별 지역 배출량 히트맵")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(grouped, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, ax=ax)
        st.pyplot(fig)

    # 시각화 3: 연료 구분별 파이 차트
    elif 시각화_종류 == "연료 구분별 비율 (파이 차트)":
        grouped = 필터링된_df.groupby('구분')['합계'].sum()
        st.subheader("🔥 연료 구분별 온실가스 배출 비율")
        fig, ax = plt.subplots()
        grouped.plot.pie(autopct='%1.1f%%', ax=ax, startangle=90, counterclock=False)
        ax.set_ylabel("")
        ax.set_title("구분별 배출 비율")
        st.pyplot(fig)

    # 시각화 4: 업종-연료별 막대그래프
    elif 시각화_종류 == "업종-연료별 막대그래프":
        grouped = 필터링된_df.groupby(['업종', '연료명'])['합계'].sum().reset_index()
        st.subheader("🏭 업종-연료별 배출량")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=grouped, x='업종', y='합계', hue='연료명', ax=ax)
        ax.set_ylabel("천tCO₂")
        ax.set_title("업종-연료 조합별 배출량")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
