import streamlit as st
import folium
from folium.plugins import LocateControl
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
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; font-weight: bold; padding: 6px 10px; }
    .warning-card { background-color: #fff2f2; border-left: 5px solid #ff4d4d; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .info-card { background-color: #f0f7ff; border-left: 5px solid #0066cc; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .food-card { background-color: #f6fff5; border-left: 5px solid #28a745; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .sight-card { background-color: #fcf4ff; border-left: 5px solid #9b59b6; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .card-detail { font-size: 13px; color: #444; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("⛩️ 후쿠오카 스마트 가이드")
st.caption("📱 폰에서 한눈에 보는 현지 맛집 · 관광지 · 교통 · 주의지역")

# 데이터 정의
LOCATIONS = [
    # --- 관광지 (Sightseeing / Purple) ---
    {
        "name": "씨사이드 모모치 해변공원 (해수욕장)",
        "cat": "Sightseeing",
        "lat": 33.5936, "lng": 130.3514,
        "hours": "24시간 열림 (상점가 10:00~20:00)",
        "feature": "후쿠오카 타워 바로 앞 인공 모래사장 해변. 일몰 야경이 아름다우며 리조트 스타일의 마리존 상가가 위치함",
        "desc": "후쿠오카 대표 도심형 해수욕장 & 산책로",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "이토시마 야시마 해변 (이토시마 부부바위)",
        "cat": "Sightseeing",
        "lat": 33.6441, "lng": 130.1983,
        "hours": "24시간 (드라이브 추천)",
        "menu": "해변 카페거리 & 천국 계단 / 에메랄드빛 바다",
        "feature": "후쿠오카 근교 최고 인기의 해변 휴양지. 흰 도리이와 부부바위, 하얀 모래사장이 펼쳐져 인생샷 성지로 불림",
        "desc": "에메랄드빛 바다와 드라이브 코스로 유명한 해수욕장/해변",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "후쿠오카시 동식물원 (동물원)",
        "cat": "Sightseeing",
        "lat": 33.5752, "lng": 130.3881,
        "hours": "09:00 ~ 17:00 (월요일 휴무)",
        "feature": "도심 근교 나비관, 열대 식물원과 함께 코끼리, 레서판다, 호랑이 등 다양한 동물을 만날 수 있는 가족 친화형 동물원",
        "desc": "아기자기하고 조용한 도심형 식물원 & 동물원",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "우미노나카미치 해상공원 & 동물원 (동물의 숲)",
        "cat": "Sightseeing",
        "lat": 33.6664, "lng": 130.3608,
        "hours": "09:30 ~ 17:30 (시즌별 변동)",
        "feature": "넓은 국영공원 내 위치한 체험형 동물원 '동물의 숲'. 카피바라, 캥거루, 람파카 등을 가까이서 직접 교감 가능",
        "desc": "넓은 해상공원 안에서 동물들과 자유롭게 만나는 동물원",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "오호리 공원",
        "cat": "Sightseeing",
        "lat": 33.5859, "lng": 130.3763,
        "hours": "24시간 열림",
        "feature": "성곽의 외호를 활용한 대형 호수공원. 호수 중앙을 가로지르는 산책로와 호수뷰 스타벅스가 인기가 높음",
        "desc": "후쿠오카 시민들이 사랑하는 대표 도심 호수공원",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "후쿠오카 타워",
        "cat": "Sightseeing",
        "lat": 33.5933, "lng": 130.3515,
        "hours": "09:30 ~ 22:00 (입장마감 21:30)",
        "feature": "높이 234m의 해안 타워로, 전망대에서 후쿠오카 시내 전체와 모모치 해변의 야경을 360도로 파노라마 감상 가능",
        "desc": "후쿠오카를 상징하는 시그니처 랜드마크 타워",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "캐널시티 하카타",
        "cat": "Sightseeing",
        "lat": 33.5898, "lng": 130.4108,
        "hours": "10:00 ~ 21:00 (음식점 ~23:00)",
        "feature": "운하를 중심으로 형성된 대형 복합 쇼핑몰. 매시 정각마다 펼쳐지는 화려한 분수 쇼와 건담 프로젝션 맵핑쇼가 볼거리",
        "desc": "쇼핑, 엔터테인먼트, 분수쇼가 어우러진 복합 공간",
        "icon": "camera", "color": "purple"
    },
    {
        "name": "팀랩 포레스트 후쿠오카",
        "cat": "Sightseeing",
        "lat": 33.5928, "lng": 130.3626,
        "hours": "11:00 ~ 20:00 (주말 10:00~)",
        "feature": "스마트폰 앱을 활용해 환상적인 빛의 숲 속 동물을 포획하고 감상하는 몰입형 디지털 아트 전시관",
        "desc": "보스 이조(BOSS E・ZO) 내 미디어아트 전시관",
        "icon": "camera", "color": "purple"
    },

    # --- 맛집 (Gourmet / Green) ---
    {
        "name": "이치란 라멘 본점",
        "cat": "Gourmet",
        "lat": 33.5932, "lng": 130.4045,
        "hours": "24시간 영업 (연중무휴)",
        "menu": "천연 돈코츠 라멘",
        "reason": "독서실 형태의 칸막이 좌석에서 진하고 호불호 적은 시그니처 돈코츠 라멘을 맛볼 수 있음",
        "desc": "후쿠오카 라멘의 상징이자 글로벌 본점",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "신신라멘 본점 (텐진)",
        "cat": "Gourmet",
        "lat": 33.5915, "lng": 130.3989,
        "hours": "11:00 ~ 03:00 (일요일 휴무)",
        "menu": "하카타 신신라멘 + 볶음밥/교자 세트",
        "reason": "잡내 없이 깔끔하고 부드러운 돼지 사골 국물로 현지인과 관광객 모두에게 극찬받는 곳",
        "desc": "현지 유명 연예인 방문 인증샷이 가득한 돈코츠 맛집",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "모츠나베 오오야마 (하카타역)",
        "cat": "Gourmet",
        "lat": 33.5898, "lng": 130.4207,
        "hours": "11:00 ~ 23:00 (라스트오더 22:30)",
        "menu": "모츠나베 (미소 맛)",
        "reason": "깊은 된장 베이스 육수에 통통하고 고소한 소곱창이 들어가 한국인 입맛에 가장 잘 맞음",
        "desc": "하카타역 직결로 접근성이 최고인 대표 곱창전골집",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "키와미야 함바그 (하카타점)",
        "cat": "Gourmet",
        "lat": 33.5899, "lng": 130.4182,
        "hours": "11:00 ~ 22:00",
        "menu": "숯불구이 함바그 스테이크 (M/L) + 세트 메뉴",
        "reason": "정통 수제 함바그를 뜨거운 달궈진 돌판에 직접 익혀 먹는 재미와 풍미",
        "desc": "항상 길게 줄을 서는 후쿠오카 필수 함바그 성지",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "요시즈카 우나기야 (장어덮밥)",
        "cat": "Gourmet",
        "lat": 33.5919, "lng": 130.4072,
        "hours": "10:30 ~ 20:00 (수요일 휴무)",
        "menu": "우나쥬 (Unaju)",
        "reason": "1873년 창업한 150년 전통집으로, 겉은 바삭하고 속은 부드러운 양념 장어구이의 진수",
        "desc": "나카스 강변에 위치한 역사 깊은 장어 전문점",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "하카타 잇키구시 / 잇카쿠 (야키토리)",
        "cat": "Gourmet",
        "lat": 33.5900, "lng": 130.4220,
        "hours": "17:00 ~ 24:00",
        "menu": "삼겹살 팽이버섯 말이, 닭껍질(토리카와)",
        "reason": "숯불 향이 짙게 배어있는 꼬치구이와 시원한 생맥주 조합이 훌륭함",
        "desc": "하루 일과를 마치고 맥주 한잔하기 가장 좋은 곳",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "멘타이주 (원조 하카타 멘타이주)",
        "cat": "Gourmet",
        "lat": 33.5908, "lng": 130.4039,
        "hours": "07:00 ~ 22:30",
        "menu": "한정판 멘타이주 (명란덮밥) & 멘타이 츠케멘",
        "reason": "특제 다시마로 감싼 명란 한 개가 통째로 올라가는 고품격 명란요리",
        "desc": "후쿠오카 특산물 '명란' 요리 전문점",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "스시 타츠쇼 / 나카스 효탄스시",
        "cat": "Gourmet",
        "lat": 33.5892, "lng": 130.3995,
        "hours": "11:30 ~ 14:30, 17:00 ~ 21:00",
        "menu": "오늘의 특선 초밥 세트, 게살 크림 고로케",
        "reason": "가성비와 퀄리티를 모두 잡은 텐진 중심가 가성비 대중 스시집",
        "desc": "현지인과 여행객이 항상 붐비는 텐진 대표 스시집",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "우동 타이라",
        "cat": "Gourmet",
        "lat": 33.5855, "lng": 130.4140,
        "hours": "11:15 ~ 15:00 (재료 소진 시 조기 중단)",
        "menu": "고보텐(우엉튀김) 자루우동 / 고기우동",
        "reason": "바삭한 우엉튀김과 직접 뽑아낸 쫄깃한 하카타식 우동 면발의 조화",
        "desc": "후쿠오카 3대 우동으로 꼽히는 수제 우동 전문점",
        "icon": "cutlery", "color": "green"
    },

    # --- 위험/주의지역 (Red) ---
    {"name": "나카스 유흥가 밤거리", "cat": "Caution", "lat": 33.5895, "lng": 130.4075, "desc": "⚠️ 야간 삐끼(호객행위) 주의 / 무료안내소 접근 금지", "icon": "warning", "color": "red"},
    {"name": "텐진 오야불루바드 야간구역", "cat": "Caution", "lat": 33.5880, "lng": 130.3990, "desc": "⚠️ 늦은 밤 과도한 호객행위 주의", "icon": "warning", "color": "red"},

    # --- 공항 & 교통 (Blue) ---
    {"name": "후쿠오카 공항 (FUK)", "cat": "Transport", "lat": 33.5859, "lng": 130.4507, "desc": "✈️ 도심까지 지하철로 5분 거리 (국제선-국내선 셔틀버스 탑승 필요)", "icon": "plane", "color": "blue"},
    {"name": "하카타역 (교통 거점)", "cat": "Transport", "lat": 33.5897, "lng": 130.4207, "desc": "🚆 신칸센, JR, 버스터미널 결집지", "icon": "subway", "color": "blue"},
    {"name": "텐진역 (쇼핑 거점)", "cat": "Transport", "lat": 33.5916, "lng": 130.3989, "desc": "🛍️ 지하상가 및 백화점 중심지", "icon": "subway", "color": "blue"},
]

# 탭 메뉴
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📍 지도", "🎡 관광지", "🍜 맛집", "⚠️ 위험지역", "✈️ 공항/교통", "🗓️ 추천코스"])

with tab1:
    st.subheader("🗺️ 통합 인터랙티브 지도")

    # 카테고리 필터
    selected_cat = st.radio("카테고리 필터:", ["전체", "🎡 관광지", "🍜 맛집", "⚠️ 위험/주의", "✈️ 공항/교통"], horizontal=True)

    # 구글 지도 한국어 타일 URL (&hl=ko)
    google_maps_kr = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=ko"

    # Folium 지도 생성
    m = folium.Map(
        location=[33.5902, 130.4017], 
        zoom_start=12, 
        tiles=google_maps_kr, 
        attr="Google"
    )

    # 내 위치 표시 버튼 추가 (LocateControl)
    LocateControl(
        auto_start=False,
        flyTo=True,
        keepCurrentZoomLevel=True,
        strings={"title": "내 위치 보기", "popup": "현재 위치"}
    ).add_to(m)

    for loc in LOCATIONS:
        # 필터링 로직
        if selected_cat == "🎡 관광지" and loc["cat"] != "Sightseeing": continue
        if selected_cat == "🍜 맛집" and loc["cat"] != "Gourmet": continue
        if selected_cat == "⚠️ 위험/주의" and loc["cat"] != "Caution": continue
        if selected_cat == "✈️ 공항/교통" and loc["cat"] != "Transport": continue

        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=folium.Popup(f"<b>{loc['name']}</b><br>{loc.get('feature', loc.get('menu', loc['desc']))}", max_width=250),
            tooltip=loc["name"],
            icon=folium.Icon(color=loc["color"], icon=loc["icon"], prefix="fa")
        ).add_to(m)

    # 모바일용 지도 크기 설정
    st_folium(m, width="100%", height=380)

with tab2:
    st.subheader("🎡 주요 관광지 (해수욕장 & 동물원 포함)")
    for loc in [l for l in LOCATIONS if l["cat"] == "Sightseeing"]:
        st.markdown(f"""
        <div class="sight-card">
            <h4>{loc['name']}</h4>
            <div class="card-detail">⏰ <b>운영시간:</b> {loc['hours']}</div>
            <div class="card-detail">💡 <b>특징:</b> {loc['feature']}</div>
            <br>
            <a href="https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}" target="_blank">📍 구글맵에서 위치 및 길찾기</a>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("🍜 구글 리뷰 최상위 후쿠오카 맛집")
    for loc in [l for l in LOCATIONS if l["cat"] == "Gourmet"]:
        st.markdown(f"""
        <div class="food-card">
            <h4>{loc['name']}</h4>
            <div class="card-detail">⏰ <b>영업시간:</b> {loc['hours']}</div>
            <div class="card-detail">🍽️ <b>추천메뉴:</b> {loc['menu']}</div>
            <div class="card-detail">💡 <b>추천이유:</b> {loc['reason']}</div>
            <br>
            <a href="https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}" target="_blank">📍 구글맵에서 길찾기</a>
        </div>
        """, unsafe_allow_html=True)

with tab4:
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

with tab5:
    st.subheader("✈️ 공항 및 교통 가이드")
    st.info("💡 **후쿠오카 공항 → 도심 이동법**\n1. 국제선 도착 후 **무료 셔틀버스** 타고 국내선 이동 (약 10~15분)\n2. 국내선 연결 **지하철 탑승** → 하카타역(5분), 텐진역(11분)")
    for loc in [l for l in LOCATIONS if l["cat"] == "Transport"]:
        st.markdown(f"""
        <div class="info-card">
            <h4>{loc['name']}</h4>
            <p>{loc['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.subheader("🗓️ 2박 3일 퀵 알짜 코스")
    with st.expander("1일차: 공항 도착 & 하카타/나카스"):
        st.write("・ 공항 도착 후 지하철로 하카타 이동\n・ 호텔 체크인 후 신신라멘 점심\n・ 캐널시티 쇼핑 & 분수쇼\n・ 저녁: 모츠나베 오오야마 & 나카스 야경 산책")
    with st.expander("2일차: 모모치 해변, 동물원 & 텐진 쇼핑"):
        st.write("・ 아침: 오호리 공원 및 후쿠오카시 동식물원 구경\n・ 오후: 모모치 해수욕장 & 후쿠오카 타워 일몰\n・ 저녁: 키와미야 함바그 또는 야키토리 탐방")
    with st.expander("3일차: 이토시마 해변 드라이브 또는 다자이후 & 귀국"):
        st.write("・ 이토시마 야시마 해변 드라이브 (사진 촬영)\n・ 공항 이동 후 면세점 쇼핑 및 귀국")
