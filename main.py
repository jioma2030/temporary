import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("전북특별자치도 CO 농도 지도 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file, encoding='cp949')

        st.write("CSV 데이터 미리보기:", df.head())
        st.write("측정소 고유 값:", df["측정소"].unique())
        st.write("전체 데이터 행 수:", len(df))

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

        df["측정소"] = df["측정소"].str.strip().str.replace(r'\s+', '', regex=True)
        st.write("정규화 후 측정소 고유 값:", df["측정소"].unique())

        df["위도"] = df["측정소"].map(lambda x: station_coords.get(x, [None, None])[0])
        df["경도"] = df["측정소"].map(lambda x: station_coords.get(x, [None, None])[1])

        st.write("결측치 수 (위도, 경도, 일산화탄소):", df[["위도", "경도", "일산화탄소"]].isna().sum())

        df = df.dropna(subset=["위도", "경도", "일산화탄소"])

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

if uploaded_file:
    data = load_data(uploaded_file)

    if data.empty:
        st.error("데이터가 비어 있습니다.")
    else:
        m = folium.Map(location=[35.8, 127.1], zoom_start=9)

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

        st.write(f"지도에 추가된 마커 수: {len(data)}")
        st_folium(m, width=1000, height=700)
else:
    st.info("CSV 파일을 업로드해주세요.")
