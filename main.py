import streamlit as st
import folium
from streamlit_folium import st_folium

# Streamlit 페이지 설정
st.set_page_config(page_title="서울 지도 시각화", page_icon="🌍")

# 제목
st.title("서울 지도 시각화 예제")

# Folium 지도 생성 (서울 중심)
map = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가 (예: 서울 시청)
folium.Marker(
    location=[37.565804, 126.975147],
    popup="서울 시청",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(map)

# Streamlit에 지도 표시
st_folium(map, width=700, height=500)

# 설명 텍스트
st.write("이 지도는 서울을 중심으로 표시되며, 서울 시청에 마커가 추가되었습니다.")
