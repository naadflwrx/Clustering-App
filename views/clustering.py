
from utils.style_loader import load_css
load_css()

import streamlit as st
import pandas as pd

from utils.clustering_dbscan import (
    clustering_pipeline,
    validate_dataset
)

from utils.recommendation import add_recommendations
from utils.storage import save_history

from utils.export import (
    export_csv,
    export_excel,
    export_json
)

from utils.visualization import (
    create_cluster_scatter,
    create_cluster_pie,
    create_cluster_bar,
    create_ipk_histogram,
    create_ips_histogram,
    create_boxplot,
    create_correlation_heatmap,
    create_summary_metrics
)

from utils.ui import page_container


def show_clustering():

    # =====================================
    # HEADER
    # =====================================
    page_container(
        "⚙️ Proses Clustering (Analisis data mahasiswa menggunakan DBSCAN)"
    )
    st.markdown("---")

    st.markdown("""
    <div class="card">
        <div class="badge badge-info">ℹ️ System Overview</div>
        <p style="margin-top:10px; text-align: justify;">
            Halaman ini digunakan untuk melakukan proses clustering mahasiswa menggunakan algoritma DBSCAN.
            Sistem akan menganalisis data IPK dan IPS dari dataset yang diunggah, kemudian mengelompokkan mahasiswa ke dalam kategori performa akademik secara otomatis. 
            Hasil analisis ini dapat digunakan sebagai dasar pengambilan keputusan akademik seperti program mentoring, evaluasi performa, dan rekomendasi pengembangan mahasiswa.            Sistem akan mengelompokkan mahasiswa berdasarkan indikator IPK dan IPS untuk menghasilkan insight yang dapat digunakan sebagai dasar pengambilan keputusan akademik seperti mentoring, monitoring, hingga rekomendasi program pengembangan mahasiswa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # INFO BOX (SAAS STYLE)
    # =====================================
    st.info("""
    Silakan pilih informasi akademik lalu upload dataset mahasiswa untuk memulai clustering.
    """)

    # =====================================
    # INPUT FORM
    # =====================================
    col1, col2, col3 = st.columns(3)

    with col1:
        angkatan = st.selectbox("Angkatan", ["2021", "2022", "2023", "2024"])

    with col2:
        jurusan = st.selectbox(
            "Jurusan",
            ["Teknik Informatika", "Sistem Informasi", "Bisnis Digital"]
        )

    with col3:
        semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8])

    uploaded_file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"])

    # =====================================
    # PREVIEW DATA
    # =====================================
    if uploaded_file:

        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

            validate_dataset(df)

            # ================================
            # DATA PREVIEW CARD
            # ================================
            st.markdown("### 📄 Preview Dataset")
            st.dataframe(df, use_container_width=True)

            # ================================
            # METRICS CARD
            # ================================
            st.markdown("### 📊 Statistik Dataset")

            col = st.columns(5)

            metrics = [
                ("Total", len(df)),
                ("Avg IPK", round(df["IPK"].mean(), 2)),
                ("Avg IPS", round(df["IPS"].mean(), 2)),
                ("Max IPK", round(df["IPK"].max(), 2)),
                ("Max IPS", round(df["IPS"].max(), 2)),
            ]

            for i, (label, value) in enumerate(metrics):
                col[i].markdown(f"""
                <div class="card">
                    <div style="font-size:12px; opacity:0.7;">{label}</div>
                    <div style="font-size:20px; font-weight:700; color:#1e3a8a;">
                        {value}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ================================
            # ACTION BUTTON
            # ================================
            if st.button("🚀 Mulai Clustering", use_container_width=True):

                result = clustering_pipeline(df, angkatan, jurusan, semester)
                result = add_recommendations(result)

                st.session_state["hasil_cluster"] = result

                save_history(
                    result,
                    uploaded_file.name,
                    angkatan,
                    jurusan,
                    semester
                )

                st.success("Clustering berhasil dilakukan.")
                st.rerun()

        except Exception as e:
            st.error(str(e))

    # =====================================
    # RESULT SECTION
    # =====================================
    if "hasil_cluster" not in st.session_state:
        return

    result = st.session_state["hasil_cluster"]

    st.markdown("---")
    st.header("📋 Hasil Clustering")

    # =====================================
    # FILTER
    # =====================================
    col1, col2 = st.columns(2)

    with col1:
        filter_cluster = st.selectbox(
            "Filter Cluster",
            ["Semua", "Mahasiswa Berprestasi", "Mahasiswa Perlu Pendampingan"]
        )

    with col2:
        keyword = st.text_input("🔍 Cari NIM / Nama")

    filtered_df = result.copy()

    if filter_cluster != "Semua":
        filtered_df = filtered_df[filtered_df["Label"] == filter_cluster]

    if keyword:
        filtered_df = filtered_df[
            filtered_df["Nama"].astype(str).str.contains(keyword, case=False)
            |
            filtered_df["NIM"].astype(str).str.contains(keyword, case=False)
        ]

    # =====================================
    # TABLE (CLEAN SAAS STYLE FIX)
    # =====================================
    st.markdown("### 📄 Data Hasil Clustering")

    def highlight_label(val):
        if val == "Mahasiswa Berprestasi":
            return "🟢 Mahasiswa Berprestasi"
        elif val == "Mahasiswa Perlu Pendampingan":
            return "🔴 Mahasiswa Perlu Pendampingan"
        return val

    display_df = filtered_df.copy()
    display_df["Label"] = display_df["Label"].apply(highlight_label)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=420
    )

    # =====================================
    # METRICS
    # =====================================
    metrics = create_summary_metrics(result)

    c = st.columns(5)

    items = [
        ("Total", metrics["total_mahasiswa"]),
        ("Avg IPK", metrics["rata_ipk"]),
        ("Avg IPS", metrics["rata_ips"]),
        ("Prestasi", metrics["jumlah_prestasi"]),
        ("Pendampingan", metrics["jumlah_pendampingan"])
    ]

    for i in range(5):
        c[i].markdown(f"""
        <div class="card">
            <div style="font-size:12px; opacity:0.7;">{items[i][0]}</div>
            <div style="font-size:20px; font-weight:700; color:#1e3a8a;">
                {items[i][1]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # VISUALISASI
    # =====================================
    st.markdown("---")
    st.subheader("📊 Visualisasi")

    st.plotly_chart(create_cluster_scatter(result), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_cluster_pie(result), use_container_width=True)

    with col2:
        st.plotly_chart(create_cluster_bar(result), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(create_ipk_histogram(result), use_container_width=True)

    with col4:
        st.plotly_chart(create_ips_histogram(result), use_container_width=True)

    col5, col6 = st.columns(2)

    with col5:
        st.plotly_chart(create_boxplot(result), use_container_width=True)

    with col6:
        st.plotly_chart(create_correlation_heatmap(result), use_container_width=True)

    # =====================================
    # DOWNLOAD
    # =====================================
    st.markdown("---")
    st.subheader("📥 Download")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.download_button("CSV", export_csv(result), "hasil.csv", "text/csv", use_container_width=True)

    with d2:
        st.download_button("Excel", export_excel(result), "hasil.xlsx", use_container_width=True)

    with d3:
        st.download_button("JSON", export_json(result), "hasil.json", "application/json", use_container_width=True)

    # =====================================
    # RESET
    # =====================================
    st.markdown("---")

    if st.button("🔄 Reset Clustering", use_container_width=True):
        del st.session_state["hasil_cluster"]
        st.rerun()