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

# 2. 커스텀 CSS (카드 스타일 & 다크모드 글자색 고정)
st.markdown("""
<style>
    /* 상단 메뉴 및 하단 툴바 기본 숨김 */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* 레이아웃 여백 조정 */
    .main .block-container { padding-top: 0.5rem; padding-bottom: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; font-weight: bold; padding: 6px 8px; }
    
    /* 카드 텍스트 색상 검은색 고정 */
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

# 4. 전체 장소 데이터 (구글 리뷰 최상위 맛집 9곳 복구)
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
        "feature": "운하를 중심으로 형성된 대형 복합 쇼핑몰. 매시 정각마다 펼쳐지는 화려한 분수 쇼와 건담
