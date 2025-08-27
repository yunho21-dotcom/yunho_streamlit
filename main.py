# Streamlit 예제 실습
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

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

# 레이아웃 구성

st.title("레이아웃 구성")

# 사이드바에 요소 배치
sidebar_selection = st.sidebar.selectbox(
    "사이드바 옵션 선택",
    ["옵션 A", "옵션 B", "옵션 C"]
)
st.sidebar.write(f"선택된 항목: {sidebar_selection}")

# 컬럼 생성 및 콘텐츠 배치
col1, col2 = st.columns(2) # 화면을 2개의 컬럼으로 분할

with col1:
    st.header("컬럼 1")
    st.write("이 영역은 첫 번째 컬럼에 해당합니다.")
    # 체크박스 위젯
    if st.checkbox("메시지 표시"):
        st.write("체크박스가 선택되었습니다.")

with col2:
    st.header("컬럼 2")
    st.write("이 영역은 두 번째 컬럼에 해당합니다.")
    # 이미지 표시
    st.image("https://static.streamlit.io/examples/cat.jpg", caption="샘플 이미지")

# Pandas 데이터프레임 및 차트 시각화
st.title("데이터 시각화")

# Pandas 데이터프레임 생성
data = {
    '첫 번째 컬럼': [1, 2, 3, 4],
    '두 번째 컬럼': [10, 20, 30, 40]
}
df = pd.DataFrame(data)

st.write("Pandas 데이터프레임 표시:")
st.dataframe(df) # 스크롤 가능한 테이블 형식으로 표시

st.write("라인 차트:")
# 랜덤 시계열 데이터 생성
chart_data = pd.DataFrame(
    np.random.randn(20, 3), # 20행 3열의 랜덤 데이터
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

st.write("막대 차트:")
st.bar_chart(chart_data)

# MES 대시보드
st.set_page_config(
    page_title="MES Dashboard",
    page_icon="🏭",
    layout="wide"
)

# 애플리케이션 제목
st.title("🏭 MES 생산 현황 대시보드")
st.markdown("---")

# 가상 생산 데이터
PRODUCTION_TARGET = 3000
current_production = 2350
achievement_rate = (current_production / PRODUCTION_TARGET) * 100

# 생산 현황 시각화
st.header("📊 생산 현황 모니터링")

# 화면을 3개의 컬럼으로 분할
col1, col2, col3 = st.columns(3)

with col1:
    # st.metric: 주요 지표 표시
    st.metric(label="일일 생산 목표", value=f"{PRODUCTION_TARGET} 개")
with col2:
    st.metric(label="현재 생산량", value=f"{current_production} 개", delta=f"{current_production - 2300} 개")
with col3:
    st.metric(label="달성률", value=f"{achievement_rate:.2f} %", delta=f"{achievement_rate - 75:.2f} %")

# 진행률 바 표시 (0.0 ~ 1.0 범위)
st.progress(achievement_rate / 100)
st.markdown("---")

# 품질/특이사항 보고 폼
st.header("📝 품질/특이사항 보고")

# 입력 폼을 위한 컬럼 분할
form_col1, form_col2 = st.columns(2)

with form_col1:
    line_option = st.selectbox("생산 라인", ("1번 라인", "2번 라인", "3번 라인"))
    issue_type = st.selectbox("문제 유형", ("단순 불량", "설비 고장", "원료 부족", "기타"))

with form_col2:
    # 여러 줄 텍스트 입력
    issue_details = st.text_area("상세 내용 입력", placeholder="문제 상황을 구체적으로 기술하십시오...")

# 제출 버튼 배치
_, center_col, _ = st.columns([2, 1, 2])
with center_col:
    submit_button = st.button("보고서 제출", use_container_width=True)

# 보고서 제출 로직
if submit_button:
    if not issue_details:
        st.warning("상세 내용을 입력해야 합니다.")
    else:
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 성공 메시지 표시
        st.success(f"[{report_time}] 보고서가 성공적으로 제출되었습니다!")
        # 정보 메시지 표시
        st.info(f"**라인:** {line_option}")
        st.info(f"**문제 유형:** {issue_type}")
        st.info(f"**상세 내용:** {issue_details}")