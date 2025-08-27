# Streamlit 예제 실습
import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('streamlit 예제 실습')

# 데이터 로드
DATE_COLUMN = 'date/time'
DATA_URL = ('./uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# 원시 데이터 검사
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 히스토그램 그리기
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# 지도에 데이터 표시
st.subheader('뉴욕시 픽업 및 하차 현황')
st.map(data)
hour_to_filter = st.slider('hour', 0, 23, 17) # 슬라이더로 결과 필터링
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'뉴욕시 픽업 및 하차 현황 {hour_to_filter}:00')
st.map(filtered_data)

# 드롭다운 메뉴 (Selectbox)
favorite_fruit = st.selectbox(
    '좋아하는 과일을 선택하십시오:',
    ('사과', '바나나', '딸기', '오렌지')
)
st.write(f"선택된 과일: {favorite_fruit}")

# 버튼 입력처리
st.title("버튼 위젯")
# 버튼 생성 및 클릭 이벤트 처리
if st.button("클릭"):
    st.write("버튼이 클릭되었습니다.")
    
    # 작업 진행 상태 표시
    with st.spinner('처리 중...'):
        time.sleep(2) # 2초 대기 (작업 시뮬레이션)
    st.success("처리가 완료되었습니다.")
else:
    st.write("버튼 클릭 대기 중입니다.")