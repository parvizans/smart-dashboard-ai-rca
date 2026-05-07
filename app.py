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
# STYLE (YOUR FINAL DARK)
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #000000 !important;
    color: #ffffff !important;
}
.element-container {
    background: #050505 !important;
    border: 1px solid rgba(0,255,255,0.15);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}
section[data-testid="stSidebar"] {
    background: #000000 !important;
}
[data-testid="stMetricValue"] {
    font-size: 34px !important;
    font-weight: 900 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def apply_style(fig, title):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="white"),
        title=dict(text=title, x=0.5),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.2,
            xanchor="center"
        )
    )
    return fig

# =========================
# HEADER
# =========================
st.title("🚀 Smart Telecom Dashboard")
st.markdown("### AI-powered KPI Analysis & Root Cause Intelligence")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🎛️ Control Panel")

file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if file is None:
    st.warning("Upload CSV to start")
    st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(file)
df = clean_columns(df)

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

# =========================
# TOP FILTER BAR (MASTER CONTROL)
# =========================
st.markdown("### 🔎 Quick Filters")

c1, c2, c3 = st.columns(3)

with c1:
    kpi1 = st.selectbox("Primary KPI", numeric_cols)

with c2:
    kpi2 = st.selectbox("Secondary KPI", ["None"] + numeric_cols)

with c3:
    chart_type = st.selectbox("Chart Type", ["Line", "Area", "Bar", "Scatter"])

# =========================
# SIDEBAR CONTROLS (NO KPI HERE)
# =========================
smooth = st.sidebar.slider("Smoothing", 1, 20, 5)

dist_type = st.sidebar.selectbox("Distribution", ["Histogram", "Box", "Violin"])
extra_type = st.sidebar.selectbox("Extra Chart", ["Histogram", "Box"])
corr_type = st.sidebar.selectbox("Relationship", ["Scatter", "Line", "Bar"])

# =========================
# KPI OVERVIEW
# =========================
st.markdown("### 📊 KPI Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg", round(df[kpi1].mean(),2))
col2.metric("Max", round(df[kpi1].max(),2))
col3.metric("Min", round(df[kpi1].min(),2))
col4.metric("Count", len(df))

# =========================
# TREND + DISTRIBUTION
# =========================
colA, colB = st.columns(2)

with colA:
    st.markdown("### 📈 Trend Analysis")

    if chart_type == "Line":
        fig1 = px.line(df, y=kpi1)
    elif chart_type == "Area":
        fig1 = px.area(df, y=kpi1)
    elif chart_type == "Bar":
        fig1 = px.bar(df, y=kpi1)
    else:
        fig1 = px.scatter(df, y=kpi1)

    if kpi2 != "None":
        fig1.add_trace(go.Scatter(y=df[kpi2], name=kpi2, yaxis="y2"))

    fig1 = apply_style(fig1, f"{kpi1} vs {kpi2}")
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.markdown(f"### 📊 Distribution of {kpi1}")

    if dist_type == "Histogram":
        fig2 = px.histogram(df, x=kpi1)
    elif dist_type == "Box":
        fig2 = px.box(df, y=kpi1)
    else:
        fig2 = px.violin(df, y=kpi1)

    fig2 = apply_style(fig2, dist_type)
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# EXTRA + RELATIONSHIP
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown(f"### 📊 Extra Chart")

    if extra_type == "Histogram":
        fig3 = px.histogram(df, x=kpi1)
    else:
        fig3 = px.box(df, y=kpi1)

    fig3 = apply_style(fig3, extra_type)
    st.plotly_chart(fig3, use_container_width=True)

with colD:
    if kpi2 != "None":
        st.markdown(f"### 🔗 Relationship")

        if corr_type == "Scatter":
            fig4 = px.scatter(df, x=kpi1, y=kpi2)
        elif corr_type == "Line":
            fig4 = px.line(df, x=kpi1, y=kpi2)
        else:
            fig4 = px.bar(df, x=kpi1, y=kpi2)

        fig4 = apply_style(fig4, corr_type)
        st.plotly_chart(fig4, use_container_width=True)

# =========================
# KPI HEALTH
# =========================
st.markdown("### 🧠 KPI Health")

series = df[kpi1]
ratio = series.std() / (abs(series.mean()) + 0.001)

if ratio > 0.4:
    st.error("🔴 Degraded")
elif ratio > 0.25:
    st.warning("🟡 Unstable")
else:
    st.success("🟢 Healthy")
