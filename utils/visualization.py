import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# =========================================
# COLOR SYSTEM (MATCH SIDEBAR THEME)
# =========================================
COLOR_PRIMARY = "#2563eb"
COLOR_PRESTASI = "#22c55e"
COLOR_PENDAMPINGAN = "#ef4444"

GRID_COLOR = "rgba(37, 99, 235, 0.12)"
FONT_FAMILY = "Inter"


# =========================================
# SCATTER PLOT
# =========================================
def create_cluster_scatter(df):

    fig = px.scatter(
        df,
        x="IPS",
        y="IPK",
        color="Label",
        hover_data=["Nama", "NIM"],
        color_discrete_map={
            "Mahasiswa Berprestasi": COLOR_PRESTASI,
            "Mahasiswa Perlu Pendampingan": COLOR_PENDAMPINGAN
        },
        title="Visualisasi Cluster Mahasiswa"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        title_x=0.02,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        zeroline=False
    )

    return fig


# =========================================
# PIE CHART (DONUT STYLE)
# =========================================
def create_cluster_pie(df):

    cluster_count = df["Label"].value_counts().reset_index()
    cluster_count.columns = ["Label", "Jumlah"]

    fig = px.pie(
        cluster_count,
        names="Label",
        values="Jumlah",
        hole=0.6,
        color="Label",
        color_discrete_map={
            "Mahasiswa Berprestasi": COLOR_PRESTASI,
            "Mahasiswa Perlu Pendampingan": COLOR_PENDAMPINGAN
        },
        title="Persentase Cluster"
    )

    fig.update_layout(
        paper_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        legend_title_text="",
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


# =========================================
# BAR CHART
# =========================================
def create_cluster_bar(df):

    cluster_count = df["Label"].value_counts().reset_index()
    cluster_count.columns = ["Label", "Jumlah"]

    fig = px.bar(
        cluster_count,
        x="Label",
        y="Jumlah",
        text="Jumlah",
        color="Label",
        color_discrete_map={
            "Mahasiswa Berprestasi": COLOR_PRESTASI,
            "Mahasiswa Perlu Pendampingan": COLOR_PENDAMPINGAN
        },
        title="Jumlah Mahasiswa Tiap Cluster"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=False
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR
    )

    return fig


# =========================================
# HISTOGRAM IPK
# =========================================
def create_ipk_histogram(df):

    fig = px.histogram(
        df,
        x="IPK",
        nbins=10,
        color_discrete_sequence=[COLOR_PRIMARY],
        title="Distribusi IPK"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    fig.update_xaxes(gridcolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR)

    return fig


# =========================================
# HISTOGRAM IPS
# =========================================
def create_ips_histogram(df):

    fig = px.histogram(
        df,
        x="IPS",
        nbins=10,
        color_discrete_sequence=["#6366f1"],
        title="Distribusi IPS"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    fig.update_xaxes(gridcolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR)

    return fig


# =========================================
# GENDER CHART (FIXED COLORS)
# =========================================
def create_gender_chart(df):

    gender_count = df["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Jumlah"]

    fig = px.bar(
        gender_count,
        x="Gender",
        y="Jumlah",
        text="Jumlah",
        color="Gender",
        color_discrete_sequence=["#60a5fa", "#f472b6"],
        title="Distribusi Gender"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        showlegend=False
    )

    return fig


# =========================================
# BOXPLOT
# =========================================
def create_boxplot(df):

    fig = px.box(
        df,
        x="Label",
        y="IPK",
        color="Label",
        color_discrete_map={
            "Mahasiswa Berprestasi": COLOR_PRESTASI,
            "Mahasiswa Perlu Pendampingan": COLOR_PENDAMPINGAN
        },
        title="Sebaran IPK Per Cluster"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


# =========================================
# HEATMAP
# =========================================
def create_correlation_heatmap(df):

    corr = df[["IPK", "IPS"]].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            text=corr.round(2),
            texttemplate="%{text}",
            colorscale=[
                [0, "#dbeafe"],
                [1, "#2563eb"]
            ]
        )
    )

    fig.update_layout(
        title="Heatmap Korelasi",
        paper_bgcolor="white",
        font=dict(family=FONT_FAMILY),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


# =========================================
# SUMMARY METRICS
# =========================================
def create_summary_metrics(df):

    return {
        "total_mahasiswa": len(df),
        "rata_ipk": round(df["IPK"].mean(), 2),
        "rata_ips": round(df["IPS"].mean(), 2),
        "jumlah_prestasi": len(
            df[df["Label"] == "Mahasiswa Berprestasi"]
        ),
        "jumlah_pendampingan": len(
            df[df["Label"] == "Mahasiswa Perlu Pendampingan"]
        )
    }