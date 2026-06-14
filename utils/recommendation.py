def get_recommendation(label):

    if label == "Mahasiswa Berprestasi":
        return (
            "Direkomendasikan mengikuti program "
            "beasiswa, penelitian, lomba akademik, "
            "dan kegiatan pengembangan prestasi."
        )

    return (
        "Perlu pendampingan akademik, "
        "monitoring dosen wali, "
        "serta program mentoring belajar."
    )


def add_recommendations(df):

    df["Rekomendasi"] = (
        df["Label"]
        .apply(get_recommendation)
    )

    return df