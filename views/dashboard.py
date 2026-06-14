from utils.style_loader import load_css
load_css()
from utils.ui import page_container

import streamlit as st
import pandas as pd
from utils.storage import get_history
import plotly.express as px

def show_dashboard():

    # =====================================
    # HEADER
    # =====================================
    page_container(
        "🎓 Dashboard Clustering Akademik (Ringkasan performa mahasiswa & hasil clustering)"
    )
    st.markdown("---")

    st.markdown("""
    <div class="card">
        <div class="badge badge-info">ℹ️ System Overview</div>
        <p style="margin-top:10px; text-align: justify;">
            Platform ini dirancang untuk membantu Program Studi dalam melakukan analisis performa akademik mahasiswa secara otomatis menggunakan metode clustering.
            Sistem akan mengelompokkan mahasiswa berdasarkan indikator IPK dan IPS untuk menghasilkan insight yang dapat digunakan sebagai dasar pengambilan keputusan akademik seperti mentoring, monitoring, hingga rekomendasi program pengembangan mahasiswa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # DATA
    # =====================================
    histories = get_history()

    if len(histories) == 0:
        st.warning("Belum ada data clustering yang tersimpan.")
        st.stop()

    # =====================================
    # STATISTIK
    # =====================================
    total_proses = len(histories)
    total_data = sum(i["jumlah_data"] for i in histories)
    total_prestasi = sum(i["cluster_prestasi"] for i in histories)
    total_pendampingan = sum(i["cluster_pendampingan"] for i in histories)

    st.markdown("### 📊 Ringkasan Statistik")

    col1, col2, col3, col4 = st.columns(4)

    def card(title, value, color=""):
        st.markdown(f"""
        <div style="
            padding:16px;
            border-radius:14px;
            border:1px solid rgba(255,255,255,0.08);
            background:rgba(255,255,255,0.03);
            box-shadow:0 4px 14px rgba(0,0,0,0.15);
            transition:0.2s;
        ">
            <div style="font-size:13px; opacity:0.7;">{title}</div>
            <div style="font-size:22px; font-weight:700; color:{color};">
                {value}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        card("Total Proses", total_proses)

    with col2:
        card("Total Mahasiswa", total_data)

    with col3:
        card("🟢 Berprestasi", total_prestasi, "#22c55e")

    with col4:
        card("🔴 Pendampingan", total_pendampingan, "#ef4444")

    st.markdown("---")

    # =====================================
    # DATA CHART
    # =====================================
    pie_df = pd.DataFrame({
        "Kategori": ["Berprestasi", "Pendampingan"],
        "Jumlah": [total_prestasi, total_pendampingan]
    })

    color_map = {
        "Berprestasi": "#22c55e",
        "Pendampingan": "#ef4444"
    }

    st.subheader("📈 Visualisasi Clustering")

    col1, col2 = st.columns(2)

    def style_chart(fig):
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=30, b=10),
            font=dict(color="white"),
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False
        )
        return fig

    with col1:
        fig_pie = px.pie(
            pie_df,
            names="Kategori",
            values="Jumlah",
            hole=0.55,
            color="Kategori",
            color_discrete_map=color_map
        )
        st.plotly_chart(style_chart(fig_pie), use_container_width=True)

    with col2:
        fig_bar = px.bar(
            pie_df,
            x="Kategori",
            y="Jumlah",
            text="Jumlah",
            color="Kategori",
            color_discrete_map=color_map
        )
        st.plotly_chart(style_chart(fig_bar), use_container_width=True)

    st.markdown("---")

    # =====================================
    # HISTORY
    # =====================================
    st.subheader("🕒 Riwayat Clustering Terbaru")

    history_df = pd.DataFrame(histories)[
        [
            "tanggal",
            "angkatan",
            "jurusan",
            "semester",
            "jumlah_data",
            "cluster_prestasi",
            "cluster_pendampingan"
        ]
    ]

    st.dataframe(history_df, use_container_width=True, height=320)

    st.markdown("---")

    # =====================================
    # ANALISIS
    # =====================================
    st.subheader("🏫 Aktivitas Berdasarkan Jurusan")

    jurusan_df = pd.DataFrame(histories)
    jurusan_count = jurusan_df["jurusan"].value_counts().reset_index()
    jurusan_count.columns = ["Jurusan", "Jumlah"]

    fig_jurusan = px.bar(
        jurusan_count,
        x="Jurusan",
        y="Jumlah",
        text="Jumlah",
        color="Jumlah",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(style_chart(fig_jurusan), use_container_width=True)

    st.markdown("---")

    st.subheader("🎓 Aktivitas Berdasarkan Angkatan")

    angkatan_df = pd.DataFrame(histories)
    angkatan_count = angkatan_df["angkatan"].value_counts().reset_index()
    angkatan_count.columns = ["Angkatan", "Jumlah"]

    fig_angkatan = px.bar(
        angkatan_count,
        x="Angkatan",
        y="Jumlah",
        text="Jumlah",
        color="Jumlah",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(style_chart(fig_angkatan), use_container_width=True)

    st.markdown("---")

    # =====================================
    # INTERPRETASI
    # =====================================
    st.markdown("---")
    st.subheader("🧠 Interpestasi Cluster")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card" style="border-left: 5px solid #22c55e;">
                <h4 style="margin-bottom:8px; color:#16a34a;">Mahasiswa Berprestasi</h4>
                <ul style="margin:0; padding-left:18px;">
                    <li>IPK & IPS berada pada kategori tinggi</li>
                    <li>Memiliki potensi beasiswa dan prestasi akademik</li>
                    <li>Direkomendasikan untuk lomba & riset</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card" style="border-left: 5px solid #ef4444;">
                <h4 style="margin-bottom:8px; color:#dc2626;">Mahasiswa Perlu Pendampingan</h4>
                <ul style="margin:0; padding-left:18px;">
                    <li>IPK & IPS di bawah standar optimal</li>
                    <li>Perlu monitoring akademik berkelanjutan</li>
                    <li>Direkomendasikan program mentoring</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )