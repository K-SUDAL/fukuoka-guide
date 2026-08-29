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
    .food-detail { font-size: 13px; color: #444; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("⛩️ 후쿠오카 스마트 가이드")
st.caption("📱 폰에서 한눈에 보는 현지 맛집 · 교통 · 주의지역")

# 데이터 정의
LOCATIONS = [
    # --- 맛집 (Gourmet) : 구글 리뷰 최상위권 13곳 ---
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
        "reason": "잡내 없이 깔끔하고 잡곡 육수처럼 부드러운 돼지 사골 국물로 현지인과 관광객 모두에게 극찬받는 곳",
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
        "reason": "겉만 살짝 익혀 나온 정통 수제 함바그를 뜨거운 개인 달궈진 돌판에 직접 익혀 먹는 재미와 풍미",
        "desc": "항상 길게 줄을 서는 후쿠오카 필수 함바그 성지",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "요시즈카 우나기야 (장어덮밥)",
        "cat": "Gourmet",
        "lat": 33.5919, "lng": 130.4072,
        "hours": "10:30 ~ 20:00 (수요일 휴무)",
        "menu": "우나쥬 (Unaju)",
        "reason": "1873년 창업한 150년 전통집으로, 겉은 바삭하고 속은 부드러운 특제 타레 소스 양념 장어구이의 진수",
        "desc": "나카스 강변에 위치한 역사 깊은 장어 전문점",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "하카타 잇키구시 / 잇카쿠 (야키토리)",
        "cat": "Gourmet",
        "lat": 33.5900, "lng": 130.4220,
        "hours": "17:00 ~ 24:00",
        "menu": "삼겹살 팽이버섯 말이, 닭껍질(토리카와)",
        "reason": "숯불 향이 짙게 배어있는 꼬치구이와 시원한 생맥주 조합이 훌륭한 하카타 대표 이자카야",
        "desc": "하루 일과를 마치고 맥주 한잔하기 가장 좋은 곳",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "멘타이주 (원조 하카타 멘타이주)",
        "cat": "Gourmet",
        "lat": 33.5908, "lng": 130.4039,
        "hours": "07:00 ~ 22:30",
        "menu": "한정판 멘타이주 (명란덮밥) & 멘타이 츠케멘",
        "reason": "특제 콤부(다시마)로 감싼 명란 한 개가 통째로 올라가는 고품격 명란요리로 아침 식사로도 인기",
        "desc": "후쿠오카 특산물 '명란' 요리 전문점",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "스시 타츠쇼 / 나카스 효탄스시",
        "cat": "Gourmet",
        "lat": 33.5892, "lng": 130.3995,
        "hours": "11:30 ~ 14:30, 17:00 ~ 21:00",
        "menu": "오늘의 특선 초밥 세트, 게살 크림 고로케",
        "reason": "시장直送 가성비와 퀄리티를 모두 잡은 텐진 중심가 가성비 대중 스시집",
        "desc": "현지인과 여행객이 항상 붐비는 텐진 대표 스시집",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "타이치 (스미요시 모츠나베)",
        "cat": "Gourmet",
        "lat": 33.5867, "lng": 130.4125,
        "hours": "17:00 ~ 23:30",
        "menu": "간장(쇼유) 베이스 모츠나베",
        "reason": "오오야마보다 담백하고 깔끔한 맛을 선호하는 이들에게 강력 추천하는 로컬 모츠나베 숨은 맛집",
        "desc": "진한 현지인 비율 높고 단골이 많은 전골집",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "우동 타이라",
        "cat": "Gourmet",
        "lat": 33.5855, "lng": 130.4140,
        "hours": "11:15 ~ 15:00 (재료 소진 시 조기 중단)",
        "menu": "고보텐(우엉튀김) 자루우동 / 고기우동",
        "reason": "갓 튀겨낸 큼직하고 바삭한 우엉튀김과 직접 뽑아낸 쫄깃·부드러운 하카타식 우동 면발의 조화",
        "desc": "후쿠오카 3대 우동으로 꼽히는 수제 우동 전문점",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "하카타 잇샤도 (돈카츠)",
        "cat": "Gourmet",
        "lat": 33.5885, "lng": 130.4210,
        "hours": "11:00 ~ 21:00",
        "menu": "상로스카츠 (특 등심돈카츠)",
        "reason": "두꺼운 육즙을 품은 프리미엄 흑돼지 돈카츠로 소금만 살짝 찍어 먹어도 뛰어난 풍미를 전달함",
        "desc": "겉바속촉 육즙 가득한 두툼한 일식 돈카츠",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "하카타 잇푸도 본점",
        "cat": "Gourmet",
        "lat": 33.5858, "lng": 130.3967,
        "hours": "11:00 ~ 22:00",
        "menu": "시로마루 원조 / 아카마루 신아지",
        "reason": "전 세계적으로 유명한 잇푸도의 총본산으로, 깔끔하면서 묵직한 오리지널 돈코츠 풍미를 고수함",
        "desc": "이치란과 더불어 라멘계를 이끄는 대중적 라멘 명가",
        "icon": "cutlery", "color": "green"
    },
    {
        "name": "만체키 (돈카츠)",
        "cat": "Gourmet",
        "lat": 33.5925, "lng": 130.4010,
        "hours": "11:30 ~ 15:00, 17:00 ~ 20:30",
        "menu": "안심(히레) 카츠 정식",
        "reason": "저온 구이 방식으로 튀겨내 분홍빛 육즙과 연하고 부드러운 안심 고기 식감이 일품",
        "desc": "줄 서서 먹는 후쿠오카 돈카츠 최상위 맛집",
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📍 지도", "🍜 맛집", "⚠️ 위험지역", "✈️ 공항/교통", "🗓️ 추천코스"])

with tab1:
    st.subheader("🗺️ 통합 인터랙티브 지도")

    # 카테고리 필터
    selected_cat = st.radio("카테고리 필터:", ["전체", "🍜 맛집", "⚠️ 위험/주의", "✈️ 공항/교통"], horizontal=True)

    # 구글 지도 한국어 타일 URL (&hl=ko)
    google_maps_kr = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=ko"

    # Folium 지도 생성
    m = folium.Map(
        location=[33.5902, 130.4017], 
        zoom_start=13, 
        tiles=google_maps_kr, 
        attr="Google"
    )

    for loc in LOCATIONS:
        # 필터링 로직
        if selected_cat == "🍜 맛집" and loc["cat"] != "Gourmet": continue
        if selected_cat == "⚠️ 위험/주의" and loc["cat"] != "Caution": continue
        if selected_cat == "✈️ 공항/교통" and loc["cat"] != "Transport": continue

        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=folium.Popup(f"<b>{loc['name']}</b><br>{loc.get('menu', loc['desc'])}", max_width=250),
            tooltip=loc["name"],
            icon=folium.Icon(color=loc["color"], icon=loc["icon"], prefix="fa")
        ).add_to(m)

    # 모바일용 지도 크기 설정
    st_folium(m, width="100%", height=380)

with tab2:
    st.subheader("🍜 구글 리뷰 최상위 후쿠오카 맛집")
    for loc in [l for l in LOCATIONS if l["cat"] == "Gourmet"]:
        st.markdown(f"""
        <div class="food-card">
            <h4>{loc['name']}</h4>
            <div class="food-detail">⏰ <b>영업시간:</b> {loc['hours']}</div>
            <div class="food-detail">🍽️ <b>추천메뉴:</b> {loc['menu']}</div>
            <div class="food-detail">💡 <b>추천이유:</b> {loc['reason']}</div>
            <br>
            <a href="https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}" target="_blank">📍 구글맵에서 길찾기</a>
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
        st.write("・ 오호리 공원 & 스타벅스에서 아침 산책\n・ 텐진 지하상가 및 파르코 백화점 쇼핑\n・ 저녁: 키와미야 함바그 또는 야키토리 탐방")
    with st.expander("3일차: 다자이후 후시미 & 귀국"):
        st.write("・ 버스/전철로 다자이후 천만궁 관광 (우메가에 모찌 맛보기)\n・ 공항 이동 후 면세점 쇼핑 및 귀국")
