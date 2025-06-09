import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Streamlit 설정
st.set_page_config(layout="wide")
st.title("전북특별자치도 CO 농도 지도 시각화")

# CSV 파일 로딩 함수
@st.cache_data
def load_data():
    df = pd.read_csv("전북특별자치도_대기오염정보(이산화질소_일산화탄소)_20200331.csv", encoding='cp949')

    # 미리 정의된 측정소 위경도 정보
    station_coords = {
        "전주완산구": [35.8242, 127.1392],
        "전주덕진구": [35.8561, 127.1255],
        "익산시": [35.9483, 126.9577],
        "군산시": [35.9677, 126.7361],
        "정읍시": [35.5693, 126.8555],
        "남원시": [35.4164, 127.3907],
        "김제시": [35.8030, 126.8803],
        "완주군": [35.9040, 127.1662],
        "진안군": [35.7916, 127.4260],
        "무주군": [35.9556, 127.6607],
        "장수군": [35.6474, 127.5211],
        "임실군": [35.6132, 127.2847],
        "순창군": [35.3742, 127.1377],
        "고창군": [35.4353, 126.7014],
        "부안군": [35.7318, 126.7310]
    }

    # 위도, 경도 열 생성
    df["위도"] = df["측정소"].map(lambda x: station_coords.get(x, [None, None])[0])
    df["경도"] = df["측정소"].map(lambda x: station_coords.get(x, [None, None])[1])

    # 결측치 제거
    df = df.dropna(subset=["위도", "경도", "일산화탄소"])

    return df

# 데이터 불러오기
data = load_data()

# 지도 생성
m = folium.Map(location=[35.8, 127.1], zoom_start=9)

# 색상 결정 함수 (농도에 따라)
def get_color(value):
    if value < 0.3:
        return "green"
    elif value < 0.6:
        return "orange"
    else:
        return "red"

# 지도에 마커 추가
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row["위도"], row["경도"]],
        radius=10,
        color=get_color(row["일산화탄소농도"]),
        fill=True,
        fill_color=get_color(row["일산화탄소농도"]),
        fill_opacity=0.7,
        popup=(f"{row['측정소']}<br>일산화탄소농도: {row['일산화탄소']} ppm"),
    ).add_to(m)

# 지도 출력
st_folium(m, width=1000, height=700)
