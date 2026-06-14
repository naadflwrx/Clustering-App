import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from config import EPS
from config import MIN_SAMPLES


def validate_dataset(df):

    required_columns = [
        "NIM",
        "Nama",
        "Gender",
        "IPK",
        "IPS"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Kolom tidak ditemukan: {missing}"
        )

    return True


def preprocess_data(df):

    features = df[["IPK", "IPS"]]

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(features)

    return scaled_data


def perform_clustering(df):

    validate_dataset(df)

    scaled_data = preprocess_data(df)

    model = DBSCAN(
        eps=EPS,
        min_samples=MIN_SAMPLES
    )

    cluster_labels = model.fit_predict(
        scaled_data
    )

    df["Cluster"] = cluster_labels

    return df


def assign_cluster_labels(df):

    cluster_summary = (
        df.groupby("Cluster")[["IPK", "IPS"]]
        .mean()
        .reset_index()
    )

    cluster_summary["Score"] = (
        cluster_summary["IPK"] +
        cluster_summary["IPS"]
    )

    cluster_summary = cluster_summary.sort_values(
        by="Score",
        ascending=False
    )

    best_cluster = cluster_summary.iloc[0]["Cluster"]

    label_map = {}

    for cluster in cluster_summary["Cluster"]:

        if cluster == best_cluster:

            label_map[cluster] = (
                "Mahasiswa Berprestasi"
            )

        else:

            label_map[cluster] = (
                "Mahasiswa Perlu Pendampingan"
            )

    df["Label"] = df["Cluster"].map(label_map)

    return df


def add_metadata(
    df,
    angkatan,
    jurusan,
    semester
):

    df["Angkatan"] = angkatan
    df["Jurusan"] = jurusan
    df["Semester"] = semester

    return df


def clustering_pipeline(
    df,
    angkatan,
    jurusan,
    semester
):

    df = perform_clustering(df)

    df = assign_cluster_labels(df)

    df = add_metadata(
        df,
        angkatan,
        jurusan,
        semester
    )

    return df