import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (맑은 고딕, 나눔고딕 등 설치된 폰트로 자동 적용 시도)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 깨짐 방지

st.set_page_config(page_title="산업부문 온실가스 시각화", layout="wide")
st.title("📊 산업부문 에너지사용 및 온실가스배출 시각화")

# CSV 파일 불러오기 (업로드 없이 자동 포함된 경로 사용)
file_path = "한국에너지공단_산업부문 에너지사용 및 온실가스배출량 통계_20231231.csv"
df = pd.read_csv(file_path)

# '합계'와 지역별 열을 숫자형으로 변환
value_cols = ['합계'] + list(df.columns[5:])
for col in value_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

st.sidebar.header("🔍 시각화 옵션")

# 필터
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

# 필터링된 데이터
필터링된_df = df[
    df['업종'].isin(선택_업종) &
    df['구분'].isin(선택_구분) &
    df['연료명'].isin(선택_연료)
]

# 시각화 1
if 시각화_종류 == "업종별 온실가스 합계":
    grouped = 필터링된_df.groupby('업종')['합계'].sum().sort_values(ascending=False)

    st.subheader("🏭 업종별 온실가스 배출량 합계")
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='bar', ax=ax, color='cornflowerblue')
    ax.set_ylabel("천tCO₂")
    ax.set_xlabel("업종")
    ax.set_title("업종별 온실가스 배출량 합계", fontsize=15)
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y')
    st.pyplot(fig)

# 시각화 2
elif 시각화_종류 == "지역별 배출량 히트맵":
    지역컬럼 = df.columns[5:]
    grouped = 필터링된_df.groupby('업종')[지역컬럼].sum()

    st.subheader("🗺️ 업종별 지역 배출량 히트맵")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(grouped, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, ax=ax)
    ax.set_title("업종별 지역 온실가스 배출량", fontsize=15)
    st.pyplot(fig)

# 시각화 3
elif 시각화_종류 == "연료 구분별 비율 (파이 차트)":
    grouped = 필터링된_df.groupby('구분')['합계'].sum()

    st.subheader("🔥 연료 구분별 온실가스 배출 비율")
    fig, ax = plt.subplots()
    grouped.plot.pie(autopct='%1.1f%%', ax=ax, startangle=90, counterclock=False)
    ax.set_ylabel("")
    ax.set_title("연료 구분별 비율", fontsize=15)
    st.pyplot(fig)

# 시각화 4
elif 시각화_종류 == "업종-연료별 막대그래프":
    grouped = 필터링된_df.groupby(['업종', '연료명'])['합계'].sum().reset_index()

    st.subheader("🏭 업종-연료별 배출량")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=grouped, x='업종', y='합계', hue='연료명', ax=ax)
    ax.set_ylabel("천tCO₂")
    ax.set_title("업종-연료별 온실가스 배출량", fontsize=15)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
