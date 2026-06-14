import sys
sys.dont_write_bytecode = True

import streamlit as st

from utils.style_loader import load_css
load_css()

from utils.ui import page_container

from views.dashboard import show_dashboard
from views.panduan import show_panduan
from views.clustering import show_clustering
from views.riwayat import show_riwayat


# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Clustering Akademik Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================
# SESSION STATE
# =====================================
if "theme" not in st.session_state:
    st.session_state.theme = "light"


# =====================================
# THEME VARIABLES
# =====================================
theme = st.session_state.theme

if theme == "dark":
    bg = "#0f172a"
    text = "#e2e8f0"
    sidebar_bg = "#111827"
    hover = "rgba(59, 130, 246, 0.15)"
    border = "rgba(255,255,255,0.08)"
    separator = "rgba(255,255,255,0.25)"
else:
    bg = "#ffffff"
    text = "#0f172a"
    sidebar_bg = "#f8fafc"
    hover = "rgba(59, 130, 246, 0.10)"
    border = "rgba(0,0,0,0.08)"
    separator = "rgba(0,0,0,0.15)"


# =====================================
# GLOBAL STYLE
# =====================================
st.markdown(f"""
<style>

/* APP */
.stApp {{
    background: {bg};
    color: {text};
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background: {sidebar_bg};
    border-right: 1px solid {border};
}}

/* SIDEBAR LAYOUT SAFE */
section[data-testid="stSidebar"] > div {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {{
    color: {text};
}}

/* DIVIDER (WORK 100%) */
.sidebar-divider {{
    width: 85%;
    height: 1px;
    margin: 14px auto;
    background: {separator};
    border-radius: 2px;
}}

/* RADIO MENU */
div[data-testid="stRadio"] label {{
    display: flex;
    align-items: center;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: 100%;
    transition: 0.2s;
}}

div[data-testid="stRadio"] label:hover {{
    background: {hover};
    transform: translateX(4px);
    cursor: pointer;
}}

div[data-testid="stRadio"] input {{
    display: none;
}}

/* BUTTON FIX (CENTER + TEXT NORMAL) */
div[data-testid="stButton"] {{
    display: flex;
    justify-content: center;
    width: 100%;
}}

div[data-testid="stButton"] > button {{
    width: 85% !important;
    border-radius: 12px !important;
    font-weight: 600;
    text-align: center !important;
    white-space: nowrap !important;
    transition: 0.2s;
}}

div[data-testid="stButton"] > button:hover {{
    transform: translateY(-2px);
}}

</style>
""", unsafe_allow_html=True)


# =====================================
# SIDEBAR UI
# =====================================
with st.sidebar:

    # LOGO
    st.image("assets/logo.png")

    st.markdown(
        """
        <div style="text-align:center; margin-top:5px;">
            <h4 style="margin:0;">Clustering System</h4>
            <p style="margin:0; font-size:12px; opacity:0.7;">
                Academic Analytics Panel
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # DIVIDER
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # NAVIGATION
    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📖 Panduan",
            "⚙️ Clustering",
            "🕒 Riwayat"
        ],
        label_visibility="collapsed"
    )

    # =====================================
    # THEME TOGGLE (STABLE + CLEAN)
    # =====================================

    def toggle_theme():
        st.session_state.theme = (
            "dark" if st.session_state.theme == "light" else "light"
        )

    btn_label = "☀️ Light Mode" if theme == "dark" else "🌙 Dark Mode"

    st.button(btn_label, on_click=toggle_theme)


# =====================================
# ROUTING
# =====================================
pages = {
    "📊 Dashboard": show_dashboard,
    "📖 Panduan": show_panduan,
    "⚙️ Clustering": show_clustering,
    "🕒 Riwayat": show_riwayat
}

pages[page]()


# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.caption("Sistem Clustering Akademik Mahasiswa © 2026")
