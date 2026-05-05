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
# FULL DARK UI + CARDS
# =========================
st.markdown("""
<style>
html, body, .stApp, .main, .block-container {
    background-color: #020617 !important;
    color: #e2e8f0 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
    padding: 15px;
}
section[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* Sidebar spacing */
.stSelectbox, .stSlider, .stFileUploader {
    margin-bottom: 15px;
}

/* KPI cards */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 28px !important;
    font-weight: bold;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* Card feel */
.element-container {
    background: rgba(30, 41, 59, 0.4);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

/* Remove plot background */
.js-plotly-plot .plotly {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

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

df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

kpi1 = st.sidebar.selectbox("📌 KPI 1", numeric_cols)
kpi2 = st.sidebar.selectbox("📌 KPI 2 (optional)", ["None"] + numeric_cols)

smooth = st.sidebar.slider("Smoothing Level", 1, 20, 5)

# =========================
# KPI OVERVIEW
# =========================
st.markdown("<h3>📊 KPI Overview</h3>", unsafe_allow_html=True)

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

# ===== TREND =====
with colA:
    st.markdown("### 📈 Trend Analysis")

    x_axis = np.arange(len(df))
    fig1 = go.Figure()

    y1 = df[kpi1].rolling(window=smooth).mean()

    fig1.add_trace(go.Scatter(
        x=x_axis,
        y=y1,
        mode="lines",
        name=kpi1,
        line=dict(color="#00eaff", width=3)
    ))

    if kpi2 != "None":
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=df[kpi2].rolling(window=smooth).mean(),
            mode="lines",
            name=kpi2,
            yaxis="y2",
            line=dict(color="#ff2da3", width=3, dash="dot")
        ))

    fig1.update_layout(
    title=dict(
        text=f"{kpi1} vs {kpi2}" if kpi2 != "None" else f"{kpi1} Trend",
        x=0.5,                 # ✅ PERFECT CENTER
        y=0.92,                # ✅ slightly lower (inside chart nicely)
        xanchor="center",
        yanchor="top",
        font=dict(size=20, color="#ffffff")
    ),

    template="plotly_dark",
    plot_bgcolor="#020617",
    paper_bgcolor="#020617",

xaxis=dict(
    title=kpi1,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
),

yaxis=dict(
    title=kpi2,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
)

    legend=dict(
        orientation="h",
        x=0.5,                 # ✅ center horizontally
        y=-0.2,                # ✅ move BELOW chart
        xanchor="center",
        yanchor="top",
        font=dict(color="#e2e8f0", size=12),
        bgcolor="rgba(0,0,0,0)"  # transparent
    ),

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=80   # ✅ IMPORTANT → space for legend
    ),

    yaxis2=dict(overlaying="y", side="right") if kpi2 != "None" else None
)

    st.plotly_chart(fig1, use_container_width=True, key="trend")

# ===== DISTRIBUTION =====
with colB:
    st.markdown(f"### 📊 Distribution of {kpi1}")

    fig2 = px.histogram(
        df,
        x=kpi1,
        nbins=40,
        color_discrete_sequence=["#00eaff"]
    )

    fig2.update_layout(
        template="plotly_dark",
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="white"),

xaxis=dict(
        title=kpi1,
        titlefont=dict(size=14, color="#ffffff"),
        tickfont=dict(color="#cbd5f5")
),

yaxis=dict(
    title=kpi2,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
)
    )

    st.plotly_chart(fig2, use_container_width=True, key="dist")

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

    fig3.update_layout(
        template="plotly_dark",
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="white"),

xaxis=dict(
    title=kpi1,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
),

yaxis=dict(
    title=kpi2,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
)
    )

    st.plotly_chart(fig3, use_container_width=True, key="hist")

with colD:
    if kpi2 != "None":
        st.markdown(f"### 🔗 Correlation: {kpi1} vs {kpi2}")

        fig4 = px.scatter(
            df,
            x=kpi1,
            y=kpi2,
            color_discrete_sequence=["#00eaff"]
        )

        fig4.update_layout(
            template="plotly_dark",
            plot_bgcolor="#020617",
            paper_bgcolor="#020617",
            font=dict(color="white"),
          
xaxis=dict(
    title=kpi1,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
),

yaxis=dict(
    title=kpi2,
    titlefont=dict(size=14, color="#ffffff"),
    tickfont=dict(color="#cbd5f5")
)
        )

        st.plotly_chart(fig4, use_container_width=True, key="corr")

# =========================
# KPI HEALTH
# =========================
st.markdown("### 🧠 KPI Health")

mean_val = kpi_series.mean()
std_val = kpi_series.std()

ratio = std_val / (mean_val + 0.001)

if ratio > 0.4:
    st.error("🔴 Degraded")
elif ratio > 0.25:
    st.warning("🟡 Unstable")
else:
    st.success("🟢 Healthy")
