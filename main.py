import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import CircleMarker

# 앱 제목
st.title("전북특별자치도 이산화탄소(CO) 농도 지도 시각화")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    # 인코딩 지정하여 CSV 읽기
    df = pd.read_csv("전북특별자치도_대기오염정보(이산화질소_일산화탄소)_20200331.csv", encoding='cp949')
    df = df.dropna(subset=["위도", "경도", "일산화탄소농도"])
    df["일산화탄소농도"] = pd.to_numeric(df["일산화탄소농도"], errors="coerce")
    return df

# 데이터 로딩
data = load_data()

# 지도 중심 설정
center_lat = data["위도"].mean()
center_lon = data["경도"].mean()

# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

# 색상 함수 정의
def get_color(co_value):
    if co_value < 0.5:
        return "green"
    elif co_value < 1.0:
        return "yellow"
    elif co_value < 2.0:
        return "orange"
    else:
        return "red"

# 마커 추가
for _, row in data.iterrows():
    CircleMarker(
        location=[row["위도"], row["경도"]],
        radius=7,
        color=get_color(row["일산화탄소농도"]),
        fill=True,
        fill_color=get_color(row["일산화탄소농도"]),
        fill_opacity=0.7,
        popup=folium.Popup(f"{row['측정소명']}<br>CO: {row['일산화탄소농도']}ppm", max_width=200)
    ).add_to(m)

# 지도 출력
st_folium(m, width=700, height=500)
