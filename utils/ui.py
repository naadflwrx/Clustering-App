import streamlit as st

# ==============================
# PAGE HEADER (SAAS STYLE)
# ==============================
def page_container(title):
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #1e3a8a, #0f172a);
        padding: 18px 20px;
        border-radius: 14px;
        color: white;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 6px;
    ">
        {title}
    </div>
    """, unsafe_allow_html=True)


# ==============================
# CARD COMPONENT (SAFE VERSION)
# ==============================
def card(title, value, color="#0f172a", bg="white"):
    st.markdown(f"""
    <div style="
        background: {bg};
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        transition: 0.2s;
    " onmouseover="this.style.transform='translateY(-4px)'"
      onmouseout="this.style.transform='translateY(0px)'">

        <div style="font-size:12px; color:#64748b; margin-bottom:6px;">
            {title}
        </div>

        <div style="font-size:22px; font-weight:700; color:{color};">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)