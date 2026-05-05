import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# DARK UI (STABLE VERSION)
# =========================
st.markdown("""
<style>

/* FULL PAGE */
html, body, .stApp {
    background-color: #0b1220;
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* KPI CARDS */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 26px !important;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
}

/* FIX SIDEBAR BUTTON */
button[kind="header"] {
    color: white !important;
}

/* REMOVE WIDTH LIMIT */
.block-container {
    max-width: 100% !important;
}

/* FIX SCROLL CUT */
.main {
    overflow: auto;
}

</style>
""", unsafe_allow_html=True)
# =========================
# TITLE
# =========================
st.title("🚀 Smart Telecom Dashboard")
st.caption("AI-powered KPI Analysis & Root Cause Intelligence")

# =========================
# SIDEBAR (SAFE VERSION)
# =========================
st.sidebar.header("🎛️ Control Panel")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if st.sidebar.button("🔄 Reset"):
    st.session_state.clear()
    st.rerun()

if uploaded_file is None:
    st.warning("⬅️ Upload CSV to start")
    st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(uploaded_file, sep=None, engine='python')
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

st.success(f"✅ Loaded: {uploaded_file.name}")

# =========================
# KPI SELECTION
# =========================
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

kpi1 = st.sidebar.selectbox("📌 KPI 1", numeric_cols)
kpi2 = st.sidebar.selectbox("📌 KPI 2 (optional)", ["None"] + numeric_cols)

trend_chart_type = st.sidebar.selectbox(
    "📊 Trend Chart Type",
    ["Line", "Bar", "Scatter", "Area"]
)

dist_chart_type = st.sidebar.selectbox(
    "📊 Distribution Type",
    ["Histogram", "Pie", "Donut"]
)

smooth = 1
if trend_chart_type in ["Line", "Area"]:
    smooth = st.sidebar.slider("Smoothing Level", 1, 20, 5)

show_trend = False
if trend_chart_type == "Scatter":
    show_trend = st.sidebar.checkbox("📈 Add Trend Line")

# =========================
# KPI OVERVIEW
# =========================
st.subheader("📊 KPI Overview")

kpi_series = df[kpi1].dropna()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg", round(kpi_series.mean(), 2))
c2.metric("Max", round(kpi_series.max(), 2))
c3.metric("Min", round(kpi_series.min(), 2))
c4.metric("Count", len(kpi_series))

# =========================
# DASHBOARD
# =========================
st.subheader("📊 KPI Dashboard")

colA, colB = st.columns(2)

# =========================
# 📈 TREND
# =========================
with colA:
    st.markdown("### Trend / Analysis")

    df_plot = df.copy()
    x_axis = np.arange(len(df_plot))

    fig1 = go.Figure()

    # KPI1
    y1 = df_plot[kpi1]
    if trend_chart_type in ["Line", "Area"]:
        y1 = y1.rolling(window=smooth).mean()

    fig1.add_trace(
        go.Scatter(
            x=x_axis,
            y=y1,
            mode="lines",
            name=kpi1,
            line=dict(width=3, color="#4cc9f0")
        )
    )

    # KPI2
    if kpi2 != "None":
        fig1.add_trace(
            go.Scatter(
                x=x_axis,
                y=df_plot[kpi2],
                mode="lines",
                name=kpi2,
                yaxis="y2",
                line=dict(width=3, dash="dot", color="#f72585")
            )
        )

    # ===== LAYOUT FIX =====
    fig1.update_layout(
        title=dict(
            text=f"{kpi1} vs {kpi2 if kpi2 != 'None' else ''}",
            x=0.5,
            y=0.92,
            font=dict(color="white")
        ),

        template="plotly_dark",
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",

        xaxis=dict(
            title="Time Index",
            color="white",
            gridcolor="rgba(255,255,255,0.08)"
        ),

        yaxis=dict(
            title=kpi1,
            color="white",
            gridcolor="rgba(255,255,255,0.08)"
        ),

        yaxis2=dict(
            title=kpi2,
            overlaying="y",
            side="right",
            color="white"
        ) if kpi2 != "None" else None,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="white")
        ),

        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig1, use_container_width=True)
# =========================
# DISTRIBUTION (FIXED)
# =========================
with colB:

    st.markdown("### Distribution")

    if dist_chart_type == "Histogram":
        fig2 = px.histogram(df, x=kpi1)

    elif dist_chart_type == "Pie":
        fig2 = px.pie(df, names=kpi1)

    elif dist_chart_type == "Donut":
        fig2 = px.pie(df, names=kpi1, hole=0.4)

    fig2.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)
