import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide", page_title="Smart Telecom Dashboard")

# =========================
# FINAL DARK UI + CONTROL PANEL FIX
# =========================
st.markdown("""
<style>
html, body, .stApp, .main, .block-container {
    background-color: #020617 !important;
    color: #e2e8f0 !important;
}

/* CONTROL PANEL */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
    border-right: 1px solid rgba(56,189,248,0.25);
    padding: 18px 10px;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
    font-weight: 600 !important;
}

/* Sidebar boxes */
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stFileUploader {
    background: #111827 !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
    border-radius: 14px !important;
    padding: 12px !important;
    margin-bottom: 18px !important;
}

/* Dropdown/input white boxes text */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #f8fafc !important;
    color: #020617 !important;
    border-radius: 8px !important;
}

/* File uploader */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background-color: #f8fafc !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #020617 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* Cards */
.element-container {
    background: rgba(30, 41, 59, 0.42);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

/* Plotly transparent */
.js-plotly-plot .plotly {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def clean_columns(dataframe):
    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return dataframe

def apply_chart_style(fig, x_title="", y_title="", title_text=None, bottom_legend=False):
    layout = dict(
        template="plotly_dark",
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e2e8f0"),
        xaxis=dict(
            showgrid=False,
            title=dict(text=x_title, font=dict(size=14, color="#ffffff")),
            tickfont=dict(color="#cbd5f5")
        ),
        yaxis=dict(
            showgrid=False,
            title=dict(text=y_title, font=dict(size=14, color="#ffffff")),
            tickfont=dict(color="#cbd5f5")
        ),
        margin=dict(l=45, r=45, t=75, b=85)
    )

    if title_text:
        layout["title"] = dict(
            text=title_text,
            x=0.5,
            y=0.93,
            xanchor="center",
            yanchor="top",
            font=dict(size=20, color="#ffffff")
        )

    if bottom_legend:
        layout["legend"] = dict(
            orientation="h",
            x=0.5,
            y=-0.22,
            xanchor="center",
            yanchor="top",
            font=dict(color="#e2e8f0", size=12),
            bgcolor="rgba(0,0,0,0)"
        )

    fig.update_layout(**layout)
    return fig

# =========================
# HEADER
# =========================
st.title("🚀 Smart Telecom Dashboard")
st.markdown(
    "<h3 style='color:#38bdf8;'>AI-powered KPI Analysis & Root Cause Intelligence</h3>",
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🎛️ Control Panel")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is None:
    st.warning("⬅️ Upload CSV to start")
    st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(uploaded_file, sep=None, engine="python")
df = clean_columns(df)

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

if len(numeric_cols) == 0:
    st.error("❌ No numeric columns found in this CSV.")
    st.stop()

kpi1 = st.sidebar.selectbox("📌 KPI 1", numeric_cols)
kpi2 = st.sidebar.selectbox("📌 KPI 2 (optional)", ["None"] + numeric_cols)

smooth = st.sidebar.slider("Smoothing Level", 1, 20, 5)

# =========================
# KPI OVERVIEW
# =========================
st.markdown("### 📊 KPI Overview")

kpi_series = df[kpi1].dropna()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg", round(kpi_series.mean(), 2))
c2.metric("Max", round(kpi_series.max(), 2))
c3.metric("Min", round(kpi_series.min(), 2))
c4.metric("Count", len(kpi_series))

# =========================
# MAIN CHARTS
# =========================
colA, colB = st.columns(2)

# =========================
# TREND ANALYSIS
# =========================
with colA:
    st.markdown("### 📈 Trend Analysis")

    x_axis = np.arange(len(df))
    fig1 = go.Figure()

    y1 = df[kpi1].rolling(window=smooth, min_periods=1).mean()

    fig1.add_trace(go.Scatter(
        x=x_axis,
        y=y1,
        mode="lines",
        name=kpi1,
        line=dict(color="#00eaff", width=3)
    ))

    if kpi2 != "None":
        y2 = df[kpi2].rolling(window=smooth, min_periods=1).mean()

        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=y2,
            mode="lines",
            name=kpi2,
            yaxis="y2",
            line=dict(color="#ff2da3", width=3, dash="dot")
        ))

    trend_title = f"{kpi1} vs {kpi2}" if kpi2 != "None" else f"{kpi1} Trend"

    fig1 = apply_chart_style(
        fig1,
        x_title="Index",
        y_title=kpi1,
        title_text=trend_title,
        bottom_legend=True
    )

    if kpi2 != "None":
        fig1.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showgrid=False,
                title=dict(text=kpi2, font=dict(size=14, color="#ffffff")),
                tickfont=dict(color="#cbd5f5")
            )
        )

    st.plotly_chart(fig1, use_container_width=True, key="trend_chart")

# =========================
# DISTRIBUTION
# =========================
with colB:
    st.markdown(f"### 📊 Distribution of {kpi1}")

    fig2 = px.histogram(
        df,
        x=kpi1,
        nbins=40,
        color_discrete_sequence=["#00eaff"]
    )

    fig2 = apply_chart_style(
        fig2,
        x_title=kpi1,
        y_title="Count",
        title_text=f"Distribution of {kpi1}"
    )

    st.plotly_chart(fig2, use_container_width=True, key="distribution_chart")

# =========================
# EXTRA CHARTS
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown(f"### 📊 Histogram of {kpi1}")

    fig3 = px.histogram(
        df,
        x=kpi1,
        nbins=40,
        color_discrete_sequence=["#00eaff"]
    )

    fig3 = apply_chart_style(
        fig3,
        x_title=kpi1,
        y_title="Count",
        title_text=f"Histogram of {kpi1}"
    )

    st.plotly_chart(fig3, use_container_width=True, key="histogram_chart")

with colD:
    if kpi2 != "None":
        st.markdown(f"### 🔗 Correlation: {kpi1} vs {kpi2}")

        fig4 = px.scatter(
            df,
            x=kpi1,
            y=kpi2,
            color_discrete_sequence=["#00eaff"]
        )

        fig4 = apply_chart_style(
            fig4,
            x_title=kpi1,
            y_title=kpi2,
            title_text=f"Correlation: {kpi1} vs {kpi2}"
        )

        st.plotly_chart(fig4, use_container_width=True, key="correlation_chart")
    else:
        st.info("Select KPI 2 to show correlation chart.")

# =========================
# KPI HEALTH
# =========================
st.markdown("### 🧠 KPI Health")

mean_val = kpi_series.mean()
std_val = kpi_series.std()
ratio = std_val / (abs(mean_val) + 0.001)

if ratio > 0.4:
    st.error("🔴 Degraded")
elif ratio > 0.25:
    st.warning("🟡 Unstable")
else:
    st.success("🟢 Healthy")
