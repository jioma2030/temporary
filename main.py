import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="지역별 이산화탄소 & 기온 분석", layout="wide")

st.title("📊 지역별 이산화탄소 농도 및 기온 변화")

# 데이터 불러오기
@st.cache_data
def load_data():
    # 실제로는 로컬 파일 또는 웹에서 불러올 수 있음
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/co2_temperature.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# 지역 선택
regions = df['지역'].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 필터링
region_data = df[df['지역'] == selected_region]

# 날짜 형식 추가
region_data['날짜'] = pd.to_datetime(region_data[['년도', '월']].assign(day=1))

# 시각화
tab1, tab2 = st.tabs(["🌿 이산화탄소 농도", "🌡️ 평균기온"])

with tab1:
    fig_co2 = px.line(region_data, x='날짜', y='이산화탄소(ppm)',
                      title=f"{selected_region} - 월별 이산화탄소 농도 추이",
                      markers=True)
    st.plotly_chart(fig_co2, use_container_width=True)

with tab2:
    fig_temp = px.line(region_data, x='날짜', y='평균기온(℃)',
                       title=f"{selected_region} - 월별 평균기온 추이",
                       markers=True)
    st.plotly_chart(fig_temp, use_container_width=True)
