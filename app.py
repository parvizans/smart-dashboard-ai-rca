import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("🚀 Smart Dashboard (AI + RCA Engine)")

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

kpi1 = st.selectbox("KPI 1", numeric_cols)
kpi2 = st.selectbox("KPI 2 (optional)", ["None"] + numeric_cols)

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
# 📈 TREND (LEFT)
# =========================
with colA:

    st.markdown("### Trend / Analysis")

    chart_type = st.selectbox(
        "Chart Type",
        ["Line", "Bar", "Scatter", "Area"],
        key="trend_chart"
    )

    smooth = 1
    if chart_type in ["Line", "Area"]:
        smooth = st.slider("Smoothing Level", 1, 20, 5)

    show_trend = False
    if chart_type == "Scatter":
        show_trend = st.checkbox("📈 Add Trend Line")

    df_plot = df.copy()
    x_axis = np.arange(len(df_plot))

    if chart_type == "Line":
        y = df_plot[kpi1].rolling(window=smooth).mean()
        fig1 = px.line(df_plot, x=x_axis, y=y)

    elif chart_type == "Bar":
        fig1 = px.bar(df_plot, x=x_axis, y=df_plot[kpi1])

    elif chart_type == "Scatter":
        if show_trend:
            fig1 = px.scatter(df_plot, x=x_axis, y=kpi1, trendline="ols")
        else:
            fig1 = px.scatter(df_plot, x=x_axis, y=kpi1)

    elif chart_type == "Area":
        y = df_plot[kpi1].rolling(window=smooth).mean()
        fig1 = px.area(df_plot, x=x_axis, y=y)

    # KPI2 overlay
    if kpi2 != "None":
        fig1.add_trace(
            go.Scatter(
                x=x_axis,
                y=df_plot[kpi2],
                mode="lines",
                name=kpi2,
                yaxis="y2"
            )
        )

        fig1.update_layout(
            yaxis2=dict(
                title=kpi2,
                overlaying="y",
                side="right"
            )
        )

    fig1.update_layout(hovermode="x unified")

    st.plotly_chart(fig1, use_container_width=True)

# =========================
# 📊 DISTRIBUTION (RIGHT)
# =========================
with colB:

    st.markdown("### Distribution")

    dist_type = st.selectbox(
        "Distribution Type",
        ["Histogram", "Box", "Violin"]
    )

    if dist_type == "Histogram":
        fig2 = px.histogram(df, x=kpi1)
    elif dist_type == "Box":
        fig2 = px.box(df, y=kpi1)
    elif dist_type == "Violin":
        fig2 = px.violin(df, y=kpi1, box=True)

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# HISTOGRAM & CORRELATION
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown("### Histogram")
    fig3 = px.histogram(df[kpi1], nbins=40)
    st.plotly_chart(fig3, use_container_width=True)

with colD:
    if kpi2 != "None":
        st.markdown("### Correlation")
        fig4 = px.scatter(df, x=kpi1, y=kpi2)
        st.plotly_chart(fig4, use_container_width=True)

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
# TELECOM INTELLIGENCE V2
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
