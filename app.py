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
# FULL DARK UI
# =========================
st.markdown("""
<style>

/* ===== FULL BACKGROUND ===== */
html, body, .stApp, .main, .block-container {
    background-color: #020617 !important;
    color: #e2e8f0 !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
}
section[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
    font-weight: 500;
}

/* ===== INPUTS ===== */
.stSelectbox div[data-baseweb="select"],
.stFileUploader {
    background-color: #1e293b !important;
    border-radius: 8px !important;
}

/* ===== KPI CARDS ===== */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 28px !important;
    font-weight: bold;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* REMOVE WHITE PLOT BACKGROUND */
.js-plotly-plot .plotly {
    background: transparent !important;
}
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stFileUploader {
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🚀 Smart Telecom Dashboard")
st.caption("AI-powered KPI Analysis & Root Cause Intelligence")

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
df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# =========================
# KPI SELECTION
# =========================
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

kpi1 = st.sidebar.selectbox("📌 KPI 1", numeric_cols)
kpi2 = st.sidebar.selectbox("📌 KPI 2 (optional)", ["None"] + numeric_cols)

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
colA, colB = st.columns(2)

# ===== TREND =====
with colA:
    st.markdown("### 📈 Trend Analysis")

    x_axis = np.arange(len(df))
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=x_axis,
        y=df[kpi1],
        mode="lines",
        name=kpi1,
        line=dict(color="#00eaff", width=3)   # main line

    ))

    if kpi2 != "None":
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=df[kpi2],
            mode="lines",
            name=kpi2,
            yaxis="y2",
            line=dict(color="#ff2da3", width=3, dash="dot")  # second KPI
        ))

    fig1.update_layout(
    title=dict(
        text=f"{kpi1} vs {kpi2}" if kpi2 != "None" else f"{kpi1} Trend",
        x=0.45,   # 👈 slightly left (your request)
        font=dict(size=20, color="#ffffff")
    ),

    template="plotly_dark",
    plot_bgcolor="#020617",
    paper_bgcolor="#020617",

    legend=dict(
        font=dict(color="#ffffff"),
        orientation="h",
        x=0.45,   # 👈 move left (important fix)
        xanchor="center",
        y=1.05
    ),

    yaxis2=dict(overlaying="y", side="right") if kpi2 != "None" else None
)
    st.plotly_chart(fig1, use_container_width=True, key="trend")

# ===== DISTRIBUTION =====
with colB:
    st.markdown(f"### 📊 Distribution of {kpi1}")

    fig2 = px.histogram(df, x=kpi1, nbins=40,
                        color_discrete_sequence=["#00e5ff"])

    fig2.update_layout(
        template="plotly_dark",
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="white")
    )

    st.plotly_chart(fig2, use_container_width=True, key="dist")

# =========================
# EXTRA CHARTS
# =========================
colC, colD = st.columns(2)

# ===== HISTOGRAM =====
with colC:
    st.markdown(f"### 📊 Histogram of {kpi1}")

    fig3 = px.histogram(
        df,
        x=kpi1,
        nbins=40,
        color_discrete_sequence=["#00e5ff"]
    )

    fig3.update_layout(
        template="plotly_dark",
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="white")
    )

    st.plotly_chart(fig3, use_container_width=True, key="hist")


# ===== CORRELATION =====
with colD:
    if kpi2 != "None":
        st.markdown(f"### 🔗 Correlation: {kpi1} vs {kpi2}")

        fig4 = px.scatter(
            df,
            x=kpi1,
            y=kpi2,
            color_discrete_sequence=["#00e5ff"]
        )

        fig4.update_layout(
            template="plotly_dark",
            plot_bgcolor="#020617",
            paper_bgcolor="#020617",
            font=dict(color="white")
        )

        st.plotly_chart(fig4, use_container_width=True, key="corr")

# =========================
# KPI HEALTH
# =========================
st.subheader("🧠 KPI Health")

mean_val = kpi_series.mean()
std_val = kpi_series.std()

ratio = std_val / (mean_val + 0.001)

if ratio > 0.4:
    st.error("🔴 Degraded")
elif ratio > 0.25:
    st.warning("🟡 Unstable")
else:
    st.success("🟢 Healthy")

# =========================
# TELECOM INTELLIGENCE
# =========================
st.subheader("📡 Telecom Intelligence")

issues = []
actions = []

if mean_val < kpi_series.max() * 0.5:
    issues.append("Coverage issue detected")
    actions.append("Check RSRP")

if std_val > mean_val * 0.3:
    issues.append("Mobility instability")
    actions.append("Tune Handover")

if kpi_series.max() > mean_val * 2:
    issues.append("Possible congestion")
    actions.append("Check PRB")

if issues:
    st.error("⚠️ Issues Detected")
    for i in issues:
        st.write(f"• {i}")

    st.warning("🛠 Recommendations")
    for a in actions:
        st.write(f"👉 {a}")
else:
    st.success("✅ Network looks stable")
