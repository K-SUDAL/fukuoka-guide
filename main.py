import streamlit as st
import folium
from folium.plugins import LocateControl
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="후쿠오카 모바일 가이드",
    page_icon="⛩️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 안전하게 우측 하단 왕관/프로필 버튼 숨기기 (Root 레이아웃 타격 없음)
st.markdown("""
<style>
    /* 상단 메뉴 숨기기 */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* 하단 왕관 및 계정 아바타 버튼 투명화/숨김 */
    .stAppDeployButton { display: none !important; }
    [data-testid="manage-app-button"] { display: none !important; }
    #ViewerBadge { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    iframe[title="streamlit_sharing_badge"] { display: none !important; }
    
    /* 카드 텍스트 색상 검은색으로 고정 (다크모드에서도 잘 보이도록 설정) */
    .sight-card { background-color: #fcf4ff; border-left: 5px solid #9b59b6; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .sight-card h4 { color: #111111 !important; margin-bottom: 6px; font-weight: bold; }
    
    .food-card { background-color: #f6fff5; border-left: 5px solid #28a745; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .food-card h4 { color: #111111 !important; margin-bottom: 6px; font-weight: bold; }
    
    .warning-card { background-color: #fff2f2; border-left: 5px solid #ff4d4d; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .warning-card h4 { color: #111111 !important; margin-bottom: 6px; font-weight: bold; }
    
    .info-card { background-color: #f0f7ff; border-left: 5px solid #0066cc; padding: 12px; border-radius: 6px; margin-bottom: 12px; }
    .info-card h4 { color: #111111 !important; margin-bottom: 6px; font-weight: bold; }
    
    .card-detail { font-size: 13px; color: #333333 !important; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# 3. 카카오톡 인앱 브라우저 안내
st.warning("⚠️ **카카오톡으로 접속하신 경우**\n지도가 제대로 안 뜨면 우측 상단 `⋮` (또는 하단 `⋯`) 누르고 **'다른 브라우저로 열기'**(Safari/Chrome)를 선택해 주세요!")

st.title("⛩️ 후쿠오카 스마트 가이드")
st.caption("📱 폰에서 한눈에 보는 현지 맛집 · 관광지 · 교통 · 주의지역")

# 4. 데이터 정의
LOCATIONS = [
    # --- 관광지 ---
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

    # --- 맛집 ---
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

    # --- 위험/주의지역 ---
    {"name": "나카스 유흥가 밤거리", "cat": "Caution", "lat": 33.5895, "lng": 130.4075, "desc": "⚠️ 야간 삐끼(호객행위) 주의 / 무료안내소 접근 금지", "icon": "warning", "color": "red"},

    # --- 공항 & 교통 ---
    {"name": "후쿠오카 공항 (FUK)", "cat": "Transport", "lat": 33.5859, "lng": 130.4507, "desc": "✈️ 도심까지 지하철로 5분 거리 (국제선-국내선 셔틀버스 탑승 필요)", "icon": "plane", "color": "blue"},
    {"name": "하카타역 (교통 거점)", "cat": "Transport", "lat": 33.5897, "lng": 130.4207, "desc": "🚆 신칸센, JR, 버스터미널 결집지", "icon": "subway", "color": "blue"},
]

# 5. 탭 메뉴
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📍 지도", "🎡 관광지", "🍜 맛집", "⚠️ 위험지역", "✈️ 공항/교통", "🗓️ 추천코스"])

with tab1:
    st.subheader("🗺️ 통합 인터랙티브 지도")
    selected_cat = st.radio("카테고리 필터:", ["전체", "🎡 관광지", "🍜 맛집", "⚠️ 위험/주의", "✈️ 공항/교통"], horizontal=True)

    google_maps_kr = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=ko"

    m = folium.Map(
        location=[33.5902, 130.4017], 
        zoom_start=12, 
        tiles=google_maps_kr, 
        attr="Google"
    )

    LocateControl(
        auto_start=False,
        flyTo=True,
        keepCurrentZoomLevel=True,
        strings={"title": "내 위치 보기", "popup": "현재 위치"}
    ).add_to(m)

    for loc in LOCATIONS:
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

    st_folium(m, width="100%", height=380)

with tab2:
    st.subheader("🎡 주요 관광지")
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
    st.subheader("🍜 맛집 가이드")
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
    for loc in [l for l in LOCATIONS if l["cat"] == "Caution"]:
        st.markdown(f"""
        <div class="warning-card">
            <h4>🚨 {loc['name']}</h4>
            <p>{loc['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.subheader("✈️ 공항 및 교통")
    for loc in [l for l in LOCATIONS if l["cat"] == "Transport"]:
        st.markdown(f"""
        <div class="info-card">
            <h4>{loc['name']}</h4>
            <p>{loc['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.subheader("🗓️ 추천 코스")
    st.write("1일차: 공항 → 하카타역 → 캐널시티\n2일차: 오호리 공원 → 모모치 해변 → 텐진")

# 하단 왕관/배지 실시간 강제 삭제 스크립트
st.components.v1.html("""
<script>
    function removeBadge() {
        var badges = window.parent.document.querySelectorAll('div[class*="viewerBadge"], [data-testid="stStatusWidget"], #ViewerBadge, iframe[title="streamlit_sharing_badge"], [data-testid="manage-app-button"]');
        badges.forEach(function(el) {
            el.remove();
        });
    }
    setInterval(removeBadge, 200);
</script>
""", height=0)
