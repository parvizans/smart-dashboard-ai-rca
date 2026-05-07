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
   🌌 GLOBAL BACKGROUND (PURE BLACK)
========================================================= */
html, body, .stApp, .main, .block-container {
    background-color: #000000 !important;
    color: #e5e7eb !important;
}


/* =========================================================
   📦 CARD / CONTAINER (STRONG BLACK GLASS)
========================================================= */
.element-container {
    background: #050505 !important;
    border: 1px solid rgba(0,255,255,0.08);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 14px;
}


/* =========================================================
   📊 KPI METRICS (HIGH CONTRAST)
========================================================= */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 30px !important;
    font-weight: 900 !important;
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
    font-size: 13px !important;
}


/* =========================================================
   🎛️ SIDEBAR (PURE BLACK PANEL)
========================================================= */
section[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid rgba(0,255,255,0.1);
    padding: 20px 12px;
}


/* =========================================================
   📝 SIDEBAR TEXT
========================================================= */
section[data-testid="stSidebar"] * {
    color: #d1d5db !important;
    font-weight: 500 !important;
}


/* =========================================================
   🔲 INPUT BOXES (TRUE DARK)
========================================================= */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 1px solid rgba(0,255,255,0.2) !important;
    border-radius: 10px !important;
}


/* =========================================================
   📂 FILE UPLOADER
========================================================= */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background-color: #000000 !important;
    border: 1px dashed rgba(0,255,255,0.25) !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #d1d5db !important;
}


/* =========================================================
   📏 SPACING
========================================================= */
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stFileUploader {
    margin-bottom: 18px !important;
}


/* =========================================================
   📈 PLOTLY CLEAN BACKGROUND
========================================================= */
.js-plotly-plot .plotly {
    background: transparent !important;
}


/* =========================================================
   ✨ HOVER EFFECT (PREMIUM TOUCH)
========================================================= */
.element-container:hover {
    border: 1px solid rgba(0,255,255,0.35);
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

    chart_df = df.copy()
    x_axis = np.arange(len(chart_df))

    chart_df[kpi1] = chart_df[kpi1].rolling(window=smooth, min_periods=1).mean()

    if kpi2 != "None":
        chart_df[kpi2] = chart_df[kpi2].rolling(window=smooth, min_periods=1).mean()

    fig1 = go.Figure()

    if trend_chart_type == "Line":
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=chart_df[kpi1],
            mode="lines",
            name=kpi1,
            line=dict(color="#00eaff", width=3)
        ))

    elif trend_chart_type == "Area":
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=chart_df[kpi1],
            mode="lines",
            fill="tozeroy",
            name=kpi1,
            line=dict(color="#00eaff", width=3)
        ))

    elif trend_chart_type == "Bar":
        fig1.add_trace(go.Bar(
            x=x_axis,
            y=chart_df[kpi1],
            name=kpi1,
            marker_color="#00eaff"
        ))

    else:
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=chart_df[kpi1],
            mode="markers",
            name=kpi1,
            marker=dict(color="#00eaff", size=5)
        ))

    if kpi2 != "None":
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=chart_df[kpi2],
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
