import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("산업부문 온실가스 배출량 통계 시각화")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    # 데이터 불러오기
    df = pd.read_csv(uploaded_file)

    # 숫자형으로 변환
    df['합계'] = pd.to_numeric(df['합계'], errors='coerce')

    # '구분'이 '합계'인 항목만 필터링
    filtered_df = df[df['구분'] == '합계']

    # 업종별 합계 계산
    grouped = filtered_df.groupby('업종')['합계'].sum().sort_values(ascending=False)

    # 시각화
    st.subheader("Total greenhouse gas emissions by industry (천tCO₂)")
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_ylabel("1000tCO₂")
    ax.set_xlabel("industry")
    ax.set_title("Total greenhouse gas emissions by industry")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    st.pyplot(fig)
