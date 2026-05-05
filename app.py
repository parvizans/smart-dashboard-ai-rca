import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

# 🔥 DARK THEME (ADD HERE)
st.markdown("""
<style>
    .stApp {
        background-color: #0b1220;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .stMetric {
        background: #1f2937;
        padding: 15px;
        border-radius: 10px;
    }

    h1, h2, h3 {
        color: #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")
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

if len(numeric_cols) == 0:
    st.error("❌ No numeric columns found")
    st.stop()

kpi1 = st.sidebar.selectbox("📌 KPI 1", numeric_cols)
kpi2 = st.sidebar.selectbox("📌 KPI 2 (optional)", ["None"] + numeric_cols)

# =========================
# CHART CONTROLS
# =========================
trend_chart_type = st.sidebar.selectbox(
    "📊 Trend Chart Type",
    ["Line", "Bar", "Scatter", "Area", "Stacked Bar", "Heatmap", "Treemap"]
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
# KPI DASHBOARD
# =========================
st.subheader("📊 KPI Dashboard")

colA, colB = st.columns(2)

# =========================
# 📈 TREND
# =========================
with colA:

    st.markdown("### Trend / Analysis")
    st.caption(f"Primary KPI: {kpi1} | Secondary KPI: {kpi2 if kpi2 != 'None' else 'None'}")

    df_plot = df.copy()
    x_axis = np.arange(len(df_plot))

    # ===== CHART TYPES =====
    if trend_chart_type == "Line":
        y = df_plot[kpi1].rolling(window=smooth).mean()
        fig1 = px.line(df_plot, x=x_axis, y=y, line_shape="spline")

    elif trend_chart_type == "Bar":
        fig1 = px.bar(df_plot, x=x_axis, y=df_plot[kpi1])

    elif trend_chart_type == "Scatter":
        if show_trend:
            fig1 = px.scatter(df_plot, x=x_axis, y=kpi1, trendline="ols")
        else:
            fig1 = px.scatter(df_plot, x=x_axis, y=kpi1)

    elif trend_chart_type == "Area":
        y = df_plot[kpi1].rolling(window=smooth).mean()
        fig1 = px.area(df_plot, x=x_axis, y=y)

    elif trend_chart_type == "Stacked Bar":
        if kpi2 != "None":
            fig1 = px.bar(
                df_plot,
                x=x_axis,
                y=[kpi1, kpi2],
                barmode="stack"
            )
        else:
            fig1 = px.bar(df_plot, x=x_axis, y=df_plot[kpi1])

    elif trend_chart_type == "Heatmap":
        df_plot["bin"] = pd.cut(df_plot[kpi1], bins=20)
        heat = df_plot.groupby("bin").size().reset_index(name="count")

        fig1 = px.bar(
            heat,
            x="bin",
            y="count"
        )

    elif trend_chart_type == "Treemap":
        df_plot["group"] = pd.qcut(df_plot[kpi1], q=5, duplicates="drop")

        fig1 = px.treemap(
            df_plot,
            path=["group"],
            values=kpi1
        )

    # ===== KPI2 OVERLAY (GLOBAL) =====
    if kpi2 != "None" and trend_chart_type in ["Line", "Area"]:
        fig1.add_trace(
            go.Scatter(
                x=x_axis,
                y=df_plot[kpi2],
                mode="lines",
                name=kpi2,
                yaxis="y2",
                line=dict(width=3, dash="dot")
            )
        )

        fig1.update_layout(
            yaxis2=dict(
                title=kpi2,
                overlaying="y",
                side="right"
            )
        )

    # ===== FINAL LAYOUT (GLOBAL) =====
    
    fig1.update_layout(
    title=f"{trend_chart_type} Trend of {kpi1}",
    hovermode="x unified",
    template="plotly_dark",   # 🔥 ADD THIS LINE
    xaxis_title="Time Index",
    yaxis_title=kpi1,
    legend=dict(
        title="KPIs",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

    st.plotly_chart(fig1, width="stretch")

# =========================
# 📊 DISTRIBUTION
# =========================
with colB:
    st.markdown("### Distribution")

    if dist_chart_type == "Histogram":
        fig2 = px.histogram(df, x=kpi1)

    elif dist_chart_type == "Pie":
        fig2 = px.pie(df, names=kpi1)

    elif dist_chart_type == "Donut":
        fig2 = px.pie(df, names=kpi1, hole=0.4)

    fig2.update_layout(title=f"{dist_chart_type} of {kpi1}")

    st.plotly_chart(fig2, width="stretch")

# =========================
# HISTOGRAM & CORRELATION
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown("### Histogram")
    fig3 = px.histogram(df, x=kpi1, nbins=40)
    st.plotly_chart(fig3, width="stretch")

with colD:
    if kpi2 != "None":
        st.markdown("### Correlation")
        fig4 = px.scatter(df, x=kpi1, y=kpi2)
        st.plotly_chart(fig4, width="stretch")

# =========================
# KPI HEALTH
# =========================
st.subheader("🧠 KPI Health")

mean_val = kpi_series.mean()
std_val = kpi_series.std()

if std_val / (mean_val + 0.001) > 0.4:
    st.error("🔴 Degraded")
elif std_val / (mean_val + 0.001) > 0.25:
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
    actions.append("Check RSRP / coverage thresholds")

if std_val > mean_val * 0.3:
    issues.append("Mobility instability")
    actions.append("Tune A3/A5 / neighbor relations")

if kpi_series.max() > mean_val * 2:
    issues.append("Possible congestion")
    actions.append("Check load / PRB utilization")

if issues:
    st.error("⚠️ Issues Detected")
    for i in issues:
        st.write(f"• {i}")

    st.warning("🛠 Recommendations")
    for a in actions:
        st.write(f"👉 {a}")
else:
    st.success("✅ Network looks stable")
