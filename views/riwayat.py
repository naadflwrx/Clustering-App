from utils.style_loader import load_css
load_css()

import streamlit as st
import pandas as pd
import os

from config import HISTORY_FOLDER

from utils.storage import (
    get_history,
    delete_history,
    clear_history
)

from utils.export import (
    export_csv,
    export_excel,
    export_json,
)

from utils.visualization import (
    create_cluster_pie,
    create_cluster_bar,
    create_cluster_scatter
)

from utils.ui import page_container


# =====================================
# COMPONENT
# =====================================
def card_block(content):
    st.markdown(f"""
    <div class="card">
        {content}
    </div>
    """, unsafe_allow_html=True)


def mini_card(title, value, color="#1e3a8a"):
    st.markdown(f"""
    <div class="card">
        <div style="font-size:12px; opacity:0.7; margin-bottom:6px;">
            {title}
        </div>
        <div style="font-size:22px; font-weight:700; color:{color};">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================
# MAIN PAGE
# =====================================
def show_riwayat():

    page_container(
        "🕒 Riwayat Clustering (Rekam jejak analisis mahasiswa berbasis clustering akademik)"
    )

    st.markdown("---")

    # SYSTEM OVERVIEW
    card_block("""
    <div class="badge badge-info">ℹ️ System Overview</div>
    <p style="margin-top:10px; text-align: justify;">
        Halaman ini menyimpan seluruh hasil proses clustering yang telah dilakukan sebelumnya.
        Data dapat digunakan untuk tracking, evaluasi, dan pengambilan keputusan berbasis histori analitik.
    </p>
    """)

    histories = get_history()

    if len(histories) == 0:
        st.warning("Belum ada riwayat clustering.")
        st.stop()

    # =====================================
    # KPI SECTION
    # =====================================
    total_clustering = len(histories)
    total_data = sum(i["jumlah_data"] for i in histories)

    st.markdown("### 📊 Ringkasan Riwayat")

    col1, col2 = st.columns(2)

    with col1:
        mini_card("Total Riwayat", total_clustering, "#1e3a8a")

    with col2:
        mini_card("Total Data Diproses", total_data, "#0f172a")
        
    # =====================================
    # TABLE + ACTION (SIDE BY SIDE)
    # =====================================
    st.markdown("---")
    st.subheader("📋 Daftar Riwayat")

    history_df = pd.DataFrame(histories)

    col_table, col_action = st.columns([3, 1])

    with col_table:
        st.dataframe(
            history_df,
            use_container_width=True,
            height=380
        )

    with col_action:
        st.markdown("### ⚙️ Action Panel")

        selected_file = st.selectbox(
            "Pilih Riwayat",
            ["-- Pilih --"] + history_df["filename"].tolist()
        )

        if selected_file != "-- Pilih --":

            if st.button("🗑 Hapus Riwayat", use_container_width=True):
                delete_history(selected_file)
                st.success("Riwayat berhasil dihapus.")
                st.rerun()

        st.markdown("---")

        if st.button("🚨 Hapus Semua Riwayat", use_container_width=True):
            clear_history()
            st.success("Semua riwayat berhasil dihapus.")
            st.rerun()

    if selected_file == "-- Pilih --":
        return

    selected_metadata = next(
        item for item in histories if item["filename"] == selected_file
    )

    # =====================================
    # DETAIL INFO
    # =====================================
    st.markdown("---")
    st.subheader("📌 Informasi Dataset")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mini_card("Angkatan", selected_metadata["angkatan"])

    with col2:
        mini_card("Jurusan", selected_metadata["jurusan"])

    with col3:
        mini_card("Semester", selected_metadata["semester"])

    with col4:
        mini_card("Jumlah Data", selected_metadata["jumlah_data"], "#0f172a")
    
    # =====================================
    # LOAD DATA
    # =====================================
    csv_path = os.path.join(HISTORY_FOLDER, selected_file)
    result_df = pd.read_csv(csv_path)

    # =====================================
    # FILTER
    # =====================================
    st.markdown("---")
    st.subheader("🔎 Filter Data")

    col1, col2 = st.columns(2)

    with col1:
        filter_cluster = st.selectbox(
            "Filter Cluster",
            ["Semua", "Mahasiswa Berprestasi", "Mahasiswa Perlu Pendampingan"]
        )

    with col2:
        keyword = st.text_input("Cari NIM / Nama")

    filtered_df = result_df.copy()

    if filter_cluster != "Semua":
        filtered_df = filtered_df[filtered_df["Label"] == filter_cluster]

    if keyword:
        filtered_df = filtered_df[
            filtered_df["Nama"].astype(str).str.contains(keyword, case=False)
            |
            filtered_df["NIM"].astype(str).str.contains(keyword, case=False)
        ]

    # =====================================
    # PREVIEW
    # =====================================
    st.subheader("📄 Preview Hasil")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=360
    )

    # =====================================
    # STATISTIK (1 ROW FIX)
    # =====================================
    st.markdown("---")
    st.subheader("📊 Statistik Cluster")

    prestasi = len(result_df[result_df["Label"] == "Mahasiswa Berprestasi"])
    pendampingan = len(result_df[result_df["Label"] == "Mahasiswa Perlu Pendampingan"])
    total = len(result_df)

    persentase = round((prestasi / total) * 100, 1) if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mini_card("Total Data", total, "#1e3a8a")

    with col2:
        mini_card("Berprestasi", prestasi, "#22c55e")

    with col3:
        mini_card("Pendampingan", pendampingan, "#ef4444")

    with col4:
        mini_card(
            "Persentase Berprestasi",
            f"{persentase}%",
            "#16a34a"
        )
    

    # =====================================
    # VISUALISASI
    # =====================================
    st.markdown("---")
    st.subheader("📊 Visualisasi Cluster")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_cluster_pie(result_df), use_container_width=True)

    with col2:
        st.plotly_chart(create_cluster_bar(result_df), use_container_width=True)

    st.plotly_chart(create_cluster_scatter(result_df), use_container_width=True)

    # =====================================
    # EXPORT
    # =====================================
    st.markdown("---")
    st.subheader("📥 Export Data")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.download_button("CSV", export_csv(result_df), selected_file, "text/csv", use_container_width=True)

    with d2:
        st.download_button("Excel", export_excel(result_df), selected_file.replace(".csv", ".xlsx"), use_container_width=True)

    with d3:
        st.download_button("JSON", export_json(result_df), selected_file.replace(".csv", ".json"), use_container_width=True)
