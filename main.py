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
    try:
        # 업로드된 로컬 파일 경로 사용
        csv_url = "/mnt/data/전북특별자치도_대기오염정보(이산화질소_일산화탄소)_20200331.csv"
        df = pd.read_csv(csv_url, encoding='cp949')
        
        ...

        # 디버깅: 데이터 구조 확인
        st.write("CSV 데이터 미리보기:", df.head())
        st.write("측정소 고유 값:", df["측정소"].unique())
        st.write("전체 데이터 행 수:", len(df))

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

        # 측정소 이름 정규화 (공백, 특수문자 제거)
        df["측정소"] = df["측정소"].str.strip().str.replace(r'\s+', '', regex=True)

        # 디버깅: 정규화 후 측정소 값 확인
        st.write("정규화 후 측정소 고유 값:", df["측정소"].unique())

        # 위도, 경도 열 생성
        df["위도"] = df["측정소"].map(lambda x: station_coords.get(x, [None, None])[0])
        df["경도"] = df["측정소"].map(lambda x: station_coords.get(x, [None, None])[1])

        # 결측치 확인
        st.write("결측치 수 (위도, 경도, 일산화탄소):", df[["위도", "경도", "일산화탄소"]].isna().sum())

        # 결측치 제거
        df = df.dropna(subset=["위도", "경도", "일산화탄소"])

        # 유효 데이터 확인
        if df.empty:
            st.warning("유효한 데이터가 없습니다. 측정소 이름이 station_coords와 일치하는지 확인하세요.")
            st.write("사용 가능한 측정소:", list(station_coords.keys()))
        else:
            st.write("유효 데이터 (마커로 표시될 데이터):", df[["측정소", "위도", "경도", "일산화탄소"]])
            st.write("유효 데이터 행 수:", len(df))

        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()

# 데이터 불러오기
data = load_data()

# 데이터 확인 및 지도 생성
if data.empty:
    st.error("데이터가 비어 있습니다. GitHub의 CSV 파일 URL 또는 측정소 이름을 확인하세요.")
else:
    # 지도 생성
    m = folium.Map(location=[35.8, 127.1], zoom_start=9)

    # 색상 결정 함수
    def get_color(value):
        try:
            value = float(value)
            if value < 0.3:
                return "green"
            elif value < 0.6:
                return "orange"
            else:
                return "red"
        except:
            return "gray"

    # 지도에 마커 추가
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row["위도"], row["경도"]],
            radius=10,
            color=get_color(row["일산화탄소"]),
            fill=True,
            fill_color=get_color(row["일산화탄소"]),
            fill_opacity=0.7,
            popup=folium.Popup(f"{row['측정소']}<br>일산화탄소농도: {row['일산화탄소']} ppm", max_width=300)
        ).add_to(m)

    # 디버깅: 마커 추가 확인
    st.write(f"지도에 추가된 마커 수: {len(data)}")

    # 지도 출력
    st_folium(m, width=1000, height=700)
