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

/* =========================================================
   🌑 GLOBAL BACKGROUND (DEEP BLACK)
========================================================= */
html, body, .stApp {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* =========================================================
   📦 MAIN CARDS (CLEAR SEPARATION)
========================================================= */
.block-container {
    padding-top: 1rem !important;
}

.element-container {
    background: #050505 !important;
    border: 1px solid rgba(0, 255, 255, 0.18) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 14px !important;
}

/* =========================================================
   🎛️ SIDEBAR (STRONG + READABLE)
========================================================= */
section[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid rgba(0,255,255,0.25) !important;
}

/* Sidebar titles */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 800 !important;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

/* Sidebar boxes */
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stFileUploader {
    background: #050505 !important;
    border: 1px solid rgba(0,255,255,0.25) !important;
    border-radius: 10px !important;
    padding: 10px !important;
    margin-bottom: 16px !important;
}

/* Inputs */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background: #000000 !important;
    color: #ffffff !important;
    border: 1px solid rgba(0,255,255,0.35) !important;
}

/* =========================================================
   📊 KPI NUMBERS (BIG + BOLD)
========================================================= */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 34px !important;
    font-weight: 900 !important;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* =========================================================
   📈 PLOTLY FIXES (THIS IS THE KEY 🔥)
========================================================= */
.js-plotly-plot .plotly text {
    fill: #ffffff !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Axis titles */
.js-plotly-plot .plotly .xtitle,
.js-plotly-plot .plotly .ytitle {
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* Chart titles */
.js-plotly-plot .plotly .gtitle {
    font-size: 20px !important;
    font-weight: 800 !important;
}

/* Legend */
.js-plotly-plot .plotly .legend text {
    font-size: 14px !important;
    font-weight: 700 !important;
}

/* =========================================================
   ✨ HOVER EFFECT
========================================================= */
.element-container:hover {
    border: 1px solid rgba(0,255,255,0.4) !important;
    transition: 0.2s ease-in-out;
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


def build_single_kpi_chart(df, x_axis, kpi, chart_type, title):
    y = df[kpi]

    if chart_type == "Line":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=y,
            mode="lines",
            name=kpi,
            line=dict(color="#00eaff", width=3)
        ))

    elif chart_type == "Area":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=y,
            mode="lines",
            fill="tozeroy",
            name=kpi,
            line=dict(color="#00eaff", width=3)
        ))

    elif chart_type == "Bar":
        fig = px.bar(
            df,
            x=x_axis,
            y=kpi,
            color_discrete_sequence=["#00eaff"]
        )

    else:
        fig = px.scatter(
            df,
            x=x_axis,
            y=kpi,
            color_discrete_sequence=["#00eaff"]
        )

    fig = apply_chart_style(
        fig,
        x_title="Index",
        y_title=kpi,
        title_text=title,
        bottom_legend=True
    )

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

kpi1 = st.sidebar.selectbox("📌 Primary KPI", numeric_cols)
kpi2 = st.sidebar.selectbox("📌 Secondary KPI", ["None"] + numeric_cols)

smooth = st.sidebar.slider("Smoothing Level", 1, 20, 5)

st.sidebar.markdown("### 📊 Chart Controls")

trend_chart_type = st.sidebar.selectbox(
    "Trend Chart Type",
    ["Line", "Area", "Bar", "Scatter"]
)

distribution_chart_type = st.sidebar.selectbox(
    "Distribution Chart Type",
    ["Histogram", "Box", "Violin"]
)

extra_chart_type = st.sidebar.selectbox(
    "Extra Chart Type",
    ["Histogram", "Box", "Violin", "Bar"]
)

correlation_chart_type = st.sidebar.selectbox(
    "Correlation Chart Type",
    ["Scatter", "Line", "Bar"]
)
# =========================================================
# 📊 DETECT NUMERIC COLUMNS
# =========================================================
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# =========================================================
# 🚀 TOP FILTER BAR (MAIN CONTROL - SOURCE OF TRUTH)
# =========================================================
st.markdown("### 🔎 Quick Filters")

top1, top2, top3 = st.columns([2, 2, 2])

with top1:
    kpi1 = st.selectbox(
        "Primary KPI",
        numeric_cols,
        index=0,
        key="top_kpi1"
    )

with top2:
    kpi2 = st.selectbox(
        "Secondary KPI",
        ["None"] + numeric_cols,
        key="top_kpi2"
    )

with top3:
    chart_type = st.selectbox(
        "Trend Chart Type",
        ["Line", "Area", "Bar", "Scatter"],
        key="top_chart"
    )

# =========================================================
# 🎛️ SIDEBAR (SECONDARY CONTROLS ONLY)
# =========================================================
st.sidebar.markdown("## ⚙️ Chart Controls")

smooth = st.sidebar.slider(
    "Smoothing Level",
    min_value=1,
    max_value=20,
    value=5
)

dist_chart_type = st.sidebar.selectbox(
    "Distribution Chart",
    ["Histogram", "Violin"]
)

extra_chart_type = st.sidebar.selectbox(
    "Extra Chart",
    ["Histogram", "Box"]
)

corr_chart_type = st.sidebar.selectbox(
    "Relationship Chart",
    ["Scatter", "Line", "Bar"]
)

# =========================================================
# 📈 TREND CHART (USES TOP BAR ONLY)
# =========================================================
st.markdown("### 📈 Trend Analysis")

df["smooth"] = df[kpi1].rolling(window=smooth).mean()

if chart_type == "Line":
    fig1 = px.line(df, y=kpi1)

elif chart_type == "Area":
    fig1 = px.area(df, y=kpi1)

elif chart_type == "Bar":
    fig1 = px.bar(df, y=kpi1)

else:
    fig1 = px.scatter(df, y=kpi1)

# Secondary KPI overlay
if kpi2 != "None":
    fig1.add_trace(
        go.Scatter(
            y=df[kpi2],
            mode="lines",
            name=kpi2,
            yaxis="y2"
        )
    )

# =========================================================
# 🎨 STYLE (YOUR DARK THEME)
# =========================================================
fig1.update_layout(
    title=dict(
        text=f"{kpi1} vs {kpi2}" if kpi2 != "None" else f"{kpi1} Trend",
        x=0.5,
        y=0.92,
        xanchor="center",
        yanchor="top",
        font=dict(size=20, color="#ffffff")
    ),
    template="plotly_dark",
    plot_bgcolor="#020617",
    paper_bgcolor="#020617",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(
        orientation="h",
        x=0.5,
        y=-0.2,
        xanchor="center",
        yanchor="top",
        font=dict(color="#e2e8f0", size=12),
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=40, r=40, t=80, b=80),
    yaxis2=dict(overlaying="y", side="right") if kpi2 != "None" else None
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# DISTRIBUTION
# =========================
with colB:
    st.markdown(f"### 📊 Distribution of {kpi1}")

    if distribution_chart_type == "Histogram":
        fig2 = px.histogram(
            df,
            x=kpi1,
            nbins=40,
            color_discrete_sequence=["#00eaff"]
        )
        y_title = "Count"

    elif distribution_chart_type == "Box":
        fig2 = px.box(
            df,
            y=kpi1,
            color_discrete_sequence=["#00eaff"]
        )
        y_title = kpi1

    else:
        fig2 = px.violin(
            df,
            y=kpi1,
            box=True,
            color_discrete_sequence=["#00eaff"]
        )
        y_title = kpi1

    fig2 = apply_chart_style(
        fig2,
        x_title=kpi1,
        y_title=y_title,
        title_text=f"{distribution_chart_type} of {kpi1}"
    )

    st.plotly_chart(fig2, use_container_width=True, key="distribution_chart")

# =========================
# EXTRA CHARTS
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown(f"### 📊 Extra Chart: {extra_chart_type} of {kpi1}")

    if extra_chart_type == "Histogram":
        fig3 = px.histogram(
            df,
            x=kpi1,
            nbins=40,
            color_discrete_sequence=["#00eaff"]
        )
        x_title = kpi1
        y_title = "Count"

    elif extra_chart_type == "Box":
        fig3 = px.box(
            df,
            y=kpi1,
            color_discrete_sequence=["#00eaff"]
        )
        x_title = ""
        y_title = kpi1

    elif extra_chart_type == "Violin":
        fig3 = px.violin(
            df,
            y=kpi1,
            box=True,
            color_discrete_sequence=["#00eaff"]
        )
        x_title = ""
        y_title = kpi1

    else:
        fig3 = px.bar(
            df,
            x=np.arange(len(df)),
            y=kpi1,
            color_discrete_sequence=["#00eaff"]
        )
        x_title = "Index"
        y_title = kpi1

    fig3 = apply_chart_style(
        fig3,
        x_title=x_title,
        y_title=y_title,
        title_text=f"{extra_chart_type} of {kpi1}"
    )

    st.plotly_chart(fig3, use_container_width=True, key="extra_chart")

with colD:
    if kpi2 != "None":
        st.markdown(f"### 🔗 Relationship: {kpi1} vs {kpi2}")

        if correlation_chart_type == "Scatter":
            fig4 = px.scatter(
                df,
                x=kpi1,
                y=kpi2,
                color_discrete_sequence=["#00eaff"]
            )

        elif correlation_chart_type == "Line":
            fig4 = px.line(
                df,
                x=kpi1,
                y=kpi2,
                color_discrete_sequence=["#00eaff"]
            )

        else:
            fig4 = px.bar(
                df,
                x=kpi1,
                y=kpi2,
                color_discrete_sequence=["#00eaff"]
            )

        fig4 = apply_chart_style(
            fig4,
            x_title=kpi1,
            y_title=kpi2,
            title_text=f"{correlation_chart_type}: {kpi1} vs {kpi2}"
        )

        st.plotly_chart(fig4, use_container_width=True, key="relationship_chart")
    else:
        st.info("Select Secondary KPI to show relationship chart.")

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
