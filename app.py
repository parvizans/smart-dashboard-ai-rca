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
# DARK UI
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #0b1220;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 26px !important;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
}

.block-container {
    max-width: 100% !important;
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

if not numeric_cols:
    st.error("❌ No numeric columns found")
    st.stop()

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
# TREND CHART
# =========================
with colA:
    st.markdown("### 📈 Trend / Analysis")

    x_axis = np.arange(len(df))
    fig1 = go.Figure()

    y1 = df[kpi1]
    if trend_chart_type in ["Line", "Area"]:
        y1 = y1.rolling(window=smooth).mean()

    # KPI1
    if trend_chart_type == "Bar":
        fig1.add_trace(go.Bar(x=x_axis, y=y1, name=kpi1, marker_color="#4cc9f0"))
    elif trend_chart_type == "Scatter":
        fig1.add_trace(go.Scatter(x=x_axis, y=y1, mode="markers", name=kpi1, marker_color="#4cc9f0"))
    else:
        fig1.add_trace(go.Scatter(x=x_axis, y=y1, mode="lines", name=kpi1,
                                 line=dict(color="#4cc9f0", width=3)))

    # KPI2
    if kpi2 != "None":
        fig1.add_trace(
            go.Scatter(
                x=x_axis,
                y=df[kpi2],
                mode="lines",
                name=kpi2,
                yaxis="y2",
                line=dict(color="#f72585", width=3, dash="dot")
            )
        )

    fig1.update_layout(
        title=dict(
            text=f"{kpi1} Trend Analysis",
            x=0.5,
            font=dict(color="white", size=20)
        ),
        template="plotly_dark",
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",

        xaxis=dict(color="#d1d5db"),
        yaxis=dict(color="#d1d5db"),

        yaxis2=dict(
            overlaying="y",
            side="right",
            color="#d1d5db"
        ) if kpi2 != "None" else None,

        legend=dict(
            orientation="h",
            y=1.02,
            x=0.5,
            xanchor="center",
            font=dict(color="white")
        ),

        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig1, use_container_width=True)

# =========================
# DISTRIBUTION
# =========================
with colB:
    st.markdown("### 📊 Distribution")

    if dist_chart_type == "Histogram":
        fig2 = px.histogram(df, x=kpi1, nbins=40,
                            color_discrete_sequence=["#4cc9f0"])
    elif dist_chart_type == "Pie":
        fig2 = px.pie(df, names=kpi1)
    else:
        fig2 = px.pie(df, names=kpi1, hole=0.4)

    fig2.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        font=dict(color="white")
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# EXTRA CHARTS
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown("### Histogram")
    fig3 = px.histogram(df, x=kpi1, nbins=40,
                        color_discrete_sequence=["#4cc9f0"])
    fig3.update_layout(template="plotly_dark", font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)

with colD:
    if kpi2 != "None":
        st.markdown("### Correlation")
        fig4 = px.scatter(df, x=kpi1, y=kpi2,
                          color_discrete_sequence=["#4cc9f0"])
        fig4.update_layout(template="plotly_dark", font=dict(color="white"))
        st.plotly_chart(fig4, use_container_width=True)

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
    actions.append("Check RSRP / Coverage")

if std_val > mean_val * 0.3:
    issues.append("Mobility instability")
    actions.append("Tune Handover A3/A5")

if kpi_series.max() > mean_val * 2:
    issues.append("Possible congestion")
    actions.append("Check PRB Utilization")

if issues:
    st.error("⚠️ Issues Detected")
    for i in issues:
        st.write(f"• {i}")

    st.warning("🛠 Recommendations")
    for a in actions:
        st.write(f"👉 {a}")
else:
    st.success("✅ Network looks stable")
