import os
import json
import pandas as pd

from datetime import datetime
from config import HISTORY_FOLDER


# ==========================================
# SIMPAN RIWAYAT
# ==========================================
def save_history(
    df,
    filename,
    angkatan,
    jurusan,
    semester
):

    timestamp = datetime.now()

    # pastikan folder ada
    os.makedirs(HISTORY_FOLDER, exist_ok=True)

    existing_files = [
        f for f in os.listdir(HISTORY_FOLDER)
        if f.endswith(".csv") and f.startswith("cluster_")
    ]

    cluster_number = len(existing_files) + 1

    csv_name = f"cluster_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"

    csv_path = os.path.join(
        HISTORY_FOLDER,
        csv_name
    )

    # simpan hasil clustering (CSV)
    df.to_csv(
        csv_path,
        index=False
    )

    # hitung cluster
    prestasi = len(
        df[df["Label"] == "Mahasiswa Berprestasi"]
    )

    pendampingan = len(
        df[df["Label"] == "Mahasiswa Perlu Pendampingan"]
    )

    # metadata (DIRAPIKAN tapi TIDAK menghapus field penting)
    metadata = {

        # FIX: sebelumnya "NAMA FILE" -> sekarang konsisten
        "filename": csv_name,

        # tetap support display name
        "display_name": f"Clustering {cluster_number}",

        "tanggal": timestamp.strftime("%d-%m-%Y %H:%M:%S"),

        "timestamp": timestamp.strftime("%Y%m%d_%H%M%S"),

        "angkatan": angkatan,
        "jurusan": jurusan,
        "semester": semester,

        "jumlah_data": len(df),

        "cluster_prestasi": prestasi,
        "cluster_pendampingan": pendampingan
    }

    # ==========================================
    # FIX BUG UTAMA: file_id tidak ada
    # ==========================================
    json_name = f"cluster_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

    json_path = os.path.join(
        HISTORY_FOLDER,
        json_name
    )

    try:
        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:
        # jangan crash aplikasi kalau JSON gagal
        print("Error saving history JSON:", e)

    return csv_path


# ==========================================
# AMBIL RIWAYAT
# ==========================================
def get_history():

    histories = []

    if not os.path.exists(HISTORY_FOLDER):
        return histories

    for file in os.listdir(HISTORY_FOLDER):

        if file.endswith(".json"):

            filepath = os.path.join(
                HISTORY_FOLDER,
                file
            )

            try:
                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                    # ==========================
                    # FIX COMPATIBILITY SAFETY
                    # ==========================
                    if "display_name" not in data:
                        data["display_name"] = data.get("tanggal", file)

                    if "filename" not in data:
                        data["filename"] = file.replace(".json", ".csv")

                    histories.append(data)

            except Exception:
                continue

    histories.sort(
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )

    return histories


# ==========================================
# HAPUS SATU RIWAYAT
# ==========================================
def delete_history(filename):

    csv_file = os.path.join(
        HISTORY_FOLDER,
        filename
    )

    json_file = csv_file.replace(".csv", ".json")

    if os.path.exists(csv_file):
        os.remove(csv_file)

    if os.path.exists(json_file):
        os.remove(json_file)


# ==========================================
# HAPUS SEMUA RIWAYAT
# ==========================================
def clear_history():

    if not os.path.exists(HISTORY_FOLDER):
        return

    for file in os.listdir(HISTORY_FOLDER):

        filepath = os.path.join(
            HISTORY_FOLDER,
            file
        )

        try:
            os.remove(filepath)

        except Exception:
            pass