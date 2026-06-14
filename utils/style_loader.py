import streamlit as st
import os


def load_css():

    css_path = os.path.join("assets", "style.css")

    if not os.path.exists(css_path):
        st.warning("style.css tidak ditemukan")
        return

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
        
        