from utils.style_loader import load_css
load_css()
from utils.ui import page_container

import streamlit as st


def card_block(content):
    st.markdown(
        f"""
        <div class="card">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


def show_panduan():

    page_container(
        "📖 Panduan Sistem (Petunjuk penggunaan aplikasi clustering akademik)"
    )

    st.markdown("""
    <div class="card">
        <div class="badge badge-info">ℹ️ System Overview</div>
        <p style="margin-top:10px; text-align: justify;">    
            Sistem ini dirancang untuk membantu Program Studi dalam melakukan analisis data mahasiswa berbasis clustering.
            Panduan ini menjelaskan alur penggunaan mulai dari input dataset, proses clustering, hingga interpretasi hasil.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # DATASET
    # ==================================================
    with st.expander("1️⃣ Data Preparation", expanded=True):

        st.write("""
        Dataset yang digunakan harus mengikuti struktur standar agar dapat diproses oleh sistem clustering secara optimal.
        """)

        contoh = {
            "NIM": ["221001", "221002", "221003"],
            "Nama": ["Ahmad", "Siti", "Budi"],
            "Gender": ["L", "P", "L"],
            "IPK": [3.85, 3.60, 2.75],
            "IPS": [3.90, 3.55, 2.80]
        }

        st.dataframe(contoh, use_container_width=True)

        card_block("""
        <div class="badge badge-success">Required Fields</div>
        <ul>
            <li>NIM (Unique Identifier)</li>
            <li>Nama Mahasiswa</li>
            <li>Gender</li>
            <li>IPK (0.00 - 4.00)</li>
            <li>IPS (0.00 - 4.00)</li>
        </ul>
        """)

        card_block("""
        <div class="badge badge-warning">Data Validation Rules</div>
        <ul>
            <li>Tidak boleh terdapat nilai kosong (NULL)</li>
            <li>IPK harus berada pada rentang 0 - 4</li>
            <li>IPS harus berada pada rentang 0 - 4</li>
            <li>Format file yang didukung: CSV & XLSX</li>
        </ul>
        """)

    # ==================================================
    # UPLOAD
    # ==================================================
    with st.expander("2️⃣ Data Upload"):

        card_block("""
        <p>Untuk memulai proses analisis, silakan masuk ke menu Clustering dan lakukan konfigurasi berikut:</p>
        <ul>
            <li>Pilih Angkatan</li>
            <li>Pilih Program Studi</li>
            <li>Pilih Semester</li>
            <li>Upload dataset mahasiswa</li>
        </ul>
        """)

        card_block("""
        <div class="badge badge-info">Supported Format</div>
        <ul>
            <li>CSV (.csv)</li>
            <li>Excel (.xlsx)</li>
        </ul>
        """)

    # ==================================================
    # CLUSTERING
    # ==================================================
    with st.expander("3️⃣ Clustering Execution"):

        card_block("""
        <ol>
            <li>Dataset akan ditampilkan dalam preview table</li>
            <li>Sistem melakukan validasi data otomatis</li>
            <li>Klik tombol <b>Mulai Clustering</b></li>
            <li>Hasil analisis ditampilkan secara real-time</li>
        </ol>
        """)

        card_block("""
        <div class="badge badge-success">System Output</div>
        <ul>
            <li>Hasil clustering mahasiswa</li>
            <li>Statistik akademik</li>
            <li>Visualisasi interaktif</li>
            <li>Rekomendasi tindak lanjut</li>
        </ul>
        """)

    # ==================================================
    # VISUALIZATION
    # ==================================================
    with st.expander("4️⃣ Insight & Visualization"):

        card_block("""
        <div class="badge badge-info">Analytics Dashboard</div>
        <ul>
            <li>Scatter Plot (IPK vs IPS)</li>
            <li>Pie Chart Distribusi Cluster</li>
            <li>Bar Chart Perbandingan Cluster</li>
            <li>Histogram IPK & IPS</li>
            <li>Boxplot Analisis Sebaran</li>
            <li>Heatmap Korelasi Akademik</li>
        </ul>
        """)

    # ==================================================
    # DOWNLOAD
    # ==================================================
    with st.expander("5️⃣ Export Results"):

        card_block("""
        <ul>
            <li>CSV (Data mentah hasil clustering)</li>
            <li>Excel (.xlsx format report)</li>
            <li>JSON (API-ready format)</li>
        </ul>
        """)

    # ==================================================
    # HISTORY
    # ==================================================
    with st.expander("6️⃣ History & Tracking"):

        card_block("""
        <ul>
            <li>Melihat hasil clustering sebelumnya</li>
            <li>Pencarian berdasarkan dataset</li>
            <li>Download ulang hasil analisis</li>
            <li>Hapus riwayat tertentu</li>
        </ul>
        """)

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
