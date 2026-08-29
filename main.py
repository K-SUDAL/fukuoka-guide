import streamlit as st
import folium
from folium.plugins import LocateControl
from streamlit_folium import st_folium

# 1. 페이지 설정 (반드시 최상단에 위치)
st.set_page_config(
    page_title="후쿠오카 모바일 가이드",
    page_icon="⛩️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 커스텀 CSS (왕관/계정 버튼 숨김 + 글자색 고정)
st.markdown("""
<style>
    /* 상단 헤더, 툴바 숨기기 */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    
    /* 우측 하단 요소 완전 차단 */
    .stAppDeployButton { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="manage-app-button"] { display: none !important; }
    #ViewerBadge { display: none !important; }
    .viewerBadge_container__1A53K { display: none !important; }
    .viewerBadge_link__1S137 { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    iframe[title="streamlit_sharing_badge"] { display: none !important; }
    
    /* 레이아웃 및 글자 색상 고정 */
    .main .block-container { padding-top: 0.5rem; padding-bottom: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; font-weight: bold; padding: 6px 8px; }
    
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
