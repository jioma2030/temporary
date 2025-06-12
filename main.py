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


from sklearn.linear_model import LinearRegression
import numpy as np

# 연도별 온실가스 합계 예측
df['연도'] = pd.to_datetime(df['기준년월'], format='%Y-%m').dt.year
yearly = df.groupby('연도')['합계'].sum().reset_index()

# 선형 회귀로 미래 예측
X = yearly[['연도']]
y = yearly['합계']
model = LinearRegression()
model.fit(X, y)

# 2024~2035년 예측
future_years = pd.DataFrame({'연도': list(range(2024, 2036))})
future_preds = model.predict(future_years)

# 시각화
st.subheader("📈 Predicted Total GHG Emissions (2024–2035)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly['연도'], yearly['합계'], label="Actual", marker='o')
ax.plot(future_years['연도'], future_preds, label="Predicted", linestyle='--', marker='x', color='orange')
ax.set_xlabel("Year")
ax.set_ylabel("Total Emissions (kTon CO₂)")
ax.set_title("Future GHG Emissions Prediction")
ax.legend()
ax.grid()
st.pyplot(fig)
