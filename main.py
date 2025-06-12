import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# 폰트 문제 방지를 위해 기본 설정 (영문 폰트)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="Industrial GHG Visualization", layout="wide")
st.title("📊 Industrial Energy Use and GHG Emissions Visualization")

# 자동으로 포함된 CSV 파일 경로
file_path = "한국에너지공단_산업부문 에너지사용 및 온실가스배출량 통계_20231231.csv"
df = pd.read_csv(file_path)

# 숫자형 컬럼 처리
value_cols = ['합계'] + list(df.columns[5:])
for col in value_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Sidebar filters
st.sidebar.header("🔍 Visualization Filters")
industries = sorted(df['업종'].dropna().unique())
selected_industries = st.sidebar.multiselect("Select Industries", industries, default=industries)

categories = sorted(df['구분'].dropna().unique())
selected_categories = st.sidebar.multiselect("Select Fuel Categories", categories, default=categories)

fuels = sorted(df['연료명'].dropna().unique())
selected_fuels = st.sidebar.multiselect("Select Fuels", fuels, default=fuels)

viz_type = st.sidebar.selectbox("📈 Select Visualization Type", [
    "Total GHG by Industry", 
    "Regional Heatmap", 
    "Fuel Category Pie Chart", 
    "Industry-Fuel Bar Chart"
])

# Apply filters
filtered_df = df[
    df['업종'].isin(selected_industries) &
    df['구분'].isin(selected_categories) &
    df['연료명'].isin(selected_fuels)
]

# Visualization: Total GHG by Industry
if viz_type == "Total GHG by Industry":
    grouped = filtered_df.groupby('업종')['합계'].sum().sort_values(ascending=False)

    st.subheader("🏭 Total GHG Emissions by Industry")
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='bar', ax=ax, color='cornflowerblue')
    ax.set_title("Total GHG Emissions by Industry", fontsize=15)
    ax.set_xlabel("Industry")
    ax.set_ylabel("kTon CO₂")
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y')
    st.pyplot(fig)

# Visualization: Regional Heatmap
elif viz_type == "Regional Heatmap":
    region_cols = df.columns[5:]
    grouped = filtered_df.groupby('업종')[region_cols].sum()

    st.subheader("🗺️ Regional Emissions by Industry")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(grouped, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, ax=ax)
    ax.set_title("GHG Emissions by Industry and Region", fontsize=15)
    st.pyplot(fig)

# Visualization: Fuel Category Pie Chart
elif viz_type == "Fuel Category Pie Chart":
    grouped = filtered_df.groupby('구분')['합계'].sum()

    st.subheader("🔥 Emissions Share by Fuel Category")
    fig, ax = plt.subplots()
    grouped.plot.pie(autopct='%1.1f%%', ax=ax, startangle=90, counterclock=False)
    ax.set_title("Fuel Category Share", fontsize=15)
    ax.set_ylabel("")
    st.pyplot(fig)

# Visualization: Industry-Fuel Bar Chart
elif viz_type == "Industry-Fuel Bar Chart":
    grouped = filtered_df.groupby(['업종', '연료명'])['합계'].sum().reset_index()

    st.subheader("🏭 GHG Emissions by Industry and Fuel")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=grouped, x='업종', y='합계', hue='연료명', ax=ax)
    ax.set_title("GHG Emissions by Industry and Fuel", fontsize=15)
    ax.set_xlabel("Industry")
    ax.set_ylabel("kTon CO₂")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)


st.markdown(f"""
### 🔮 미래 전망 해설

현재 한국 산업 부문의 온실가스 배출 추세에 따르면:

- 별도의 감축 조치가 없는 경우, **2035년까지 배출량이 꾸준히 증가**할 것으로 예측됩니다.  
- 현재의 패턴이 계속된다면, **2035년 총 온실가스 배출량은 약6300 kTon CO₂**에 이를 수 있어, 탄소중립 목표 달성에 큰 도전이 될 수 있습니다.  
- 이는 산업 부문에서의 **에너지 효율 개선**, **탄소 저감 기술 도입**, **강력한 기후 정책 시행**이 절실하다는 점을 시사합니다.
""")
