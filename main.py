import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 모바일 최적화 페이지 설정
st.set_page_config(
    page_title="후쿠오카 모바일 가이드",
    page_icon="⛩️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS (모바일 가독성 증대)
st.markdown("""
<style>
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: bold; padding: 8px 12px; }
    .warning-card { background-color: #fff2f2; border-left: 5px solid #ff4d4d; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .info-card { background-color: #f0f7ff; border-left: 5px solid #0066cc; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .food-card { background-color: #f6fff5; border-left: 5px solid #28a745; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
</style>
""", unsafe_allow_allow_html=True)

st.title("⛩️ 후쿠오카 스마트 가이드")
st.caption("📱 폰에서 한눈에 보는 현지 맛집 · 교통 · 주의지역")

# 데이터 정의
LOCATIONS = [
    # 맛집 (Green)
    {"name": "신신라멘 본점", "cat": "Gourmet", "lat": 33.5915, "lng": 130.3989, "desc": "돈코츠 라멘 대표맛집. 추천: 신신라멘+교자세트", "icon": "cutlery", "color": "green"},
    {"name": "이치란 라멘 본점", "cat": "Gourmet", "lat": 33.5932, "lng": 130.4045, "desc": "24시간 운영하는 독서실형 라멘집", "icon": "cutlery", "color": "green"},
    {"name": "모츠나베 오오야마 (하카타)", "cat": "Gourmet", "lat": 33.5898, "lng": 130.4207, "desc": "미소(된장) 맛 모츠나베 강추", "icon": "cutlery", "color": "green"},
    {"name": "나카스 야타이 거리", "cat": "Gourmet", "lat": 33.5905, "lng": 130.4061, "desc": "강변 포장마차 거리 (바가지 가격 주의)", "icon": "cutlery", "color": "green"},
    
    # 위험/주의지역 (Red)
    {"name": "나카스 유흥가 밤거리", "cat": "Caution", "lat": 33.5895, "lng": 130.4075, "desc": "⚠️ 야간 삐끼(호객행위) 주의 / 무료안내소 접근 금지", "icon": "warning", "color": "red"},
    {"name": "텐진 오야불루바드 야간구역", "cat": "Caution", "lat": 33.5880, "lng": 130.3990, "desc": "⚠️ 늦은 밤 과도한 호객행위 주의", "icon": "warning", "color": "red"},
    
    # 공항 & 교통 (Blue)
    {"name": "후쿠오카 공항 (FUK)", "cat": "Transport", "lat": 33.5859, "lng": 130.4507, "desc": "✈️ 도심까지 지하철로 5분 거리 (국제선-국내선 셔틀버스 탑승 필요)", "icon": "plane", "color": "blue"},
    {"name": "하카타역 (교통 거점)", "cat": "Transport", "lat": 33.5897, "lng": 130.4207, "desc": "🚆 신칸센, JR, 버스터미널 결집지", "icon": "subway", "color": "blue"},
    {"name": "텐진역 (쇼핑 거점)", "cat": "Transport", "lat": 33.5916, "lng": 130.3989, "desc": "🛍️ 지하상가 및 백화점 중심지", "icon": "subway", "color": "blue"},
]

# 탭 메뉴
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📍 지도", "🍜 맛집", "⚠️ 위험지역", "✈️ 공항/교통", "🗓️ 추천코스"])

with tab1:
    st.subheader("🗺️ 통합 인터랙티브 지도")
    
    # 카테고리 필터
    selected_cat = st.radio("카테고리 필터:", ["전체", "🍜 맛집", "⚠️ 위험/주의", "✈️ 공항/교통"], horizontal=True)
    
    # Folium 지도 생성 (후쿠오카 중심)
    m = folium.Map(location=[33.5902, 130.4017], zoom_start=13, tiles="OpenStreetMap")
    
    for loc in LOCATIONS:
        # 필터링 로직
        if selected_cat == "🍜 맛집" and loc["cat"] != "Gourmet": continue
        if selected_cat == "⚠️ 위험/주의" and loc["cat"] != "Caution": continue
        if selected_cat == "✈️ 공항/교통" and loc["cat"] != "Transport": continue
        
        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=folium.Popup(f"<b>{loc['name']}</b><br>{loc['desc']}", max_width=250),
            tooltip=loc["name"],
            icon=folium.Icon(color=loc["color"], icon=loc["icon"], prefix="fa")
        ).add_to(m)
        
    # 모바일용 지도 크기 설정
    st_folium(m, width="100%", height=380)

with tab2:
    st.subheader("🍜 필수 추천 맛집")
    for loc in [l for l in LOCATIONS if l["cat"] == "Gourmet"]:
        st.markdown(f"""
        <div class="food-card">
            <h4>{loc['name']}</h4>
            <p>{loc['desc']}</p>
            <a href="https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}" target="_blank">📍 구글맵에서 열기</a>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("⚠️ 야간 주의 & 위험 지역")
    st.warning("후쿠오카는 치안이 좋은 편이지만, 야간 유흥가에서는 아래 사항을 주의하세요!")
    for loc in [l for l in LOCATIONS if l["cat"] == "Caution"]:
        st.markdown(f"""
        <div class="warning-card">
            <h4>🚨 {loc['name']}</h4>
            <p>{loc['desc']}</p>
            <small>💡 팁: 길거리에서 '무료 안내소(無料案内所)'나 '스낵바 호객'은 절대로 따라가지 마세요.</small>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("✈️ 공항 및 교통 가이드")
    st.info("💡 **후쿠오카 공항 → 도심 이동법**\n1. 국제선 도착 후 **무료 셔틀버스** 타고 국내선 이동 (약 10~15분)\n2. 국내선 연결 **지하철 탑승** → 하카타역(5분), 텐진역(11분)")
    for loc in [l for l in LOCATIONS if l["cat"] == "Transport"]:
        st.markdown(f"""
        <div class="info-card">
            <h4>{loc['name']}</h4>
            <p>{loc['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.subheader("🗓️ 2박 3일 퀵 알짜 코스")
    with st.expander("1일차: 공항 도착 & 하카타/나카스"):
        st.write("・ 공항 도착 후 지하철로 하카타 이동\n・ 호텔 체크인 후 신신라멘 점심\n・ 캐널시티 쇼핑 & 분수쇼\n・ 저녁: 모츠나베 오오야마 & 나카스 야경 산책")
    with st.expander("2일차: 텐진 쇼핑 & 오호리 공원"):
        st.write("・ 오호리 공원 & 스타벅스에서 아침 산책\n・ 텐진 지하상가 및 파르코 백화점 쇼핑\n・ 저녁: 야키토리 맛집 탐방")
    with st.expander("3일차: 다자이후 후시미 & 귀국"):
        st.write("・ 버스/전철로 다자이후 천만궁 관광 (우메가에 모찌 맛보기)\n・ 공항 이동 후 면세점 쇼핑 및 귀국")