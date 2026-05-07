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
# STYLE
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #050505 !important;
    color: #ffffff !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

.element-container {
    background: #0b0f14 !important;
    border: 1px solid rgba(0, 234, 255, 0.25) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    margin-bottom: 16px !important;
}

section[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid rgba(0,234,255,0.35) !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stFileUploader {
    background: #0b0f14 !important;
    border: 1px solid rgba(0,234,255,0.35) !important;
    border-radius: 12px !important;
    padding: 12px !important;
    margin-bottom: 18px !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 36px !important;
    font-weight: 900 !important;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

h1 {
    font-size: 42px !important;
    font-weight: 900 !important;
}

h2, h3 {
    color: #ffffff !important;
    font-weight: 850 !important;
}

.js-plotly-plot .plotly text {
    fill: #ffffff !important;
    font-size: 14px !important;
    font-weight: 600 !important;
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


def style_fig(fig, title, x_title="", y_title="", legend_bottom=False):
    layout = dict(
        template="plotly_dark",
        plot_bgcolor="#060b16",
        paper_bgcolor="#060b16",
        font=dict(color="#ffffff"),
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=20, color="#ffffff")
        ),
                xaxis=dict(
            title=dict(text=x_title, font=dict(size=15, color="#ffffff")),
            tickfont=dict(color="#cbd5e1"),

            showgrid=False,

            showline=True,
            linewidth=1.5,
            linecolor="#00eaff",

            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.15)"
        ),

        yaxis=dict(
            title=dict(text=y_title, font=dict(size=15, color="#ffffff")),
            tickfont=dict(color="#cbd5e1"),

            showgrid=False,

            showline=True,
            linewidth=1.5,
            linecolor="#00eaff",

            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.15)"
        ),
        margin=dict(l=50, r=50, t=80, b=85)
    )

    if legend_bottom:
        layout["legend"] = dict(
            orientation="h",
            x=0.5,
            y=-0.22,
            xanchor="center",
            yanchor="top",
            font=dict(size=13, color="#ffffff")
        )

    fig.update_layout(**layout)
    fig.update_traces(
        hovertemplate=
        "<b>%{fullData.name}</b><br>" +
        "X: %{x}<br>" +
        "Y: %{y:.2f}<extra></extra>"
    )
    return fig


# =========================
# HEADER
# =========================
st.title("🚀 Smart Telecom Dashboard")
st.markdown(
    "<h3 style='color:#00eaff;'>AI-powered KPI Analysis & Root Cause Intelligence</h3>",
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

df = pd.read_csv(uploaded_file, sep=None, engine="python")
df = clean_columns(df)

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

if not numeric_cols:
    st.error("❌ No numeric columns found in this report.")
    st.stop()

# =========================
# SIDEBAR CHART CONTROLS
# =========================
smooth = st.sidebar.slider("Smoothing Level", 1, 20, 5)

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

relationship_chart_type = st.sidebar.selectbox(
    "Relationship Chart Type",
    ["Scatter", "Line", "Bar"]
)

# =========================
# TOP FILTER BAR
# =========================
st.markdown("### 🔎 Quick Filters")

f1, f2, f3, f4 = st.columns([2, 2, 2, 2])

with f1:
    kpi1 = st.selectbox("Primary KPI", numeric_cols, key="primary_kpi")

with f2:
    kpi2 = st.selectbox("Secondary KPI", ["None"] + numeric_cols, key="secondary_kpi")

with f3:
    filter_col = st.selectbox("Filter Column", ["None"] + cat_cols, key="filter_col")

with f4:
    if filter_col != "None":
        filter_values = st.multiselect(
            "Filter Values",
            sorted(df[filter_col].dropna().unique().tolist()),
            default=sorted(df[filter_col].dropna().unique().tolist())[:5],
            key="filter_values"
        )
    else:
        filter_values = []

filtered_df = df.copy()

if filter_col != "None" and filter_values:
    filtered_df = filtered_df[filtered_df[filter_col].isin(filter_values)]

if filtered_df.empty:
    st.warning("No data after filtering.")
    st.stop()

# =========================
# KPI OVERVIEW
# =========================
st.markdown("### 📊 KPI Overview")

kpi_series = filtered_df[kpi1].dropna()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Avg", round(kpi_series.mean(), 2))
m2.metric("Max", round(kpi_series.max(), 2))
m3.metric("Min", round(kpi_series.min(), 2))
m4.metric("Count", len(kpi_series))

# =========================
# MAIN CHARTS
# =========================
colA, colB = st.columns(2)

with colA:
    st.markdown("### 📈 Trend Analysis")

    chart_df = filtered_df.copy()
    x_axis = np.arange(len(chart_df))

    y1 = chart_df[kpi1].rolling(window=smooth, min_periods=1).mean()

    fig1 = go.Figure()

    if trend_chart_type == "Line":
        fig1.add_trace(go.Scatter(x=x_axis, y=y1, mode="lines", name=kpi1,
                                  line=dict(color="#00eaff", width=3)))
    elif trend_chart_type == "Area":
        fig1.add_trace(go.Scatter(x=x_axis, y=y1, mode="lines", fill="tozeroy", name=kpi1,
                                  line=dict(color="#00eaff", width=3)))
    elif trend_chart_type == "Bar":
        fig1.add_trace(go.Bar(x=x_axis, y=y1, name=kpi1, marker_color="#00eaff"))
    else:
        fig1.add_trace(go.Scatter(x=x_axis, y=y1, mode="markers", name=kpi1,
                                  marker=dict(color="#00eaff", size=5)))

    if kpi2 != "None":
        y2 = chart_df[kpi2].rolling(window=smooth, min_periods=1).mean()
        fig1.add_trace(go.Scatter(
            x=x_axis,
            y=y2,
            mode="lines",
            name=kpi2,
            yaxis="y2",
            line=dict(color="#ff2da3", width=3, dash="dot")
        ))

    fig1 = style_fig(
        fig1,
        f"{kpi1} vs {kpi2}" if kpi2 != "None" else f"{kpi1} Trend",
        "Index",
        kpi1,
        True
    )

    if kpi2 != "None":
        fig1.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showgrid=False,
                title=dict(text=kpi2, font=dict(size=15, color="#ffffff")),
                tickfont=dict(color="#cbd5e1")
            )
        )

    st.plotly_chart(fig1, use_container_width=True, key="trend_chart")

with colB:
    st.markdown(f"### 📊 Distribution of {kpi1}")

    if distribution_chart_type == "Histogram":
        fig2 = px.histogram(filtered_df, x=kpi1, nbins=40,
                            color_discrete_sequence=["#00eaff"])
        y_title = "Count"
        x_title = kpi1
    elif distribution_chart_type == "Box":
        fig2 = px.box(filtered_df, y=kpi1, color_discrete_sequence=["#00eaff"])
        y_title = kpi1
        x_title = ""
    else:
        fig2 = px.violin(filtered_df, y=kpi1, box=True,
                         color_discrete_sequence=["#00eaff"])
        y_title = kpi1
        x_title = ""

    fig2 = style_fig(fig2, f"{distribution_chart_type} of {kpi1}", x_title, y_title)
    st.plotly_chart(fig2, use_container_width=True, key="distribution_chart")

# =========================
# EXTRA + RELATIONSHIP
# =========================
colC, colD = st.columns(2)

with colC:
    st.markdown(f"### 📊 Extra Chart: {extra_chart_type} of {kpi1}")

    if extra_chart_type == "Histogram":
        fig3 = px.histogram(filtered_df, x=kpi1, nbins=40,
                            color_discrete_sequence=["#00eaff"])
        x_title, y_title = kpi1, "Count"
    elif extra_chart_type == "Box":
        fig3 = px.box(filtered_df, y=kpi1, color_discrete_sequence=["#00eaff"])
        x_title, y_title = "", kpi1
    elif extra_chart_type == "Violin":
        fig3 = px.violin(filtered_df, y=kpi1, box=True,
                         color_discrete_sequence=["#00eaff"])
        x_title, y_title = "", kpi1
    else:
        fig3 = px.bar(filtered_df, x=np.arange(len(filtered_df)), y=kpi1,
                      color_discrete_sequence=["#00eaff"])
        x_title, y_title = "Index", kpi1

    fig3 = style_fig(fig3, f"{extra_chart_type} of {kpi1}", x_title, y_title)
    st.plotly_chart(fig3, use_container_width=True, key="extra_chart")

with colD:
    if kpi2 != "None":
        st.markdown(f"### 🔗 Relationship: {kpi1} vs {kpi2}")

        if relationship_chart_type == "Scatter":
            fig4 = px.scatter(filtered_df, x=kpi1, y=kpi2,
                              color_discrete_sequence=["#00eaff"])
        elif relationship_chart_type == "Line":
            fig4 = px.line(filtered_df, x=kpi1, y=kpi2,
                           color_discrete_sequence=["#00eaff"])
        else:
            fig4 = px.bar(filtered_df, x=kpi1, y=kpi2,
                          color_discrete_sequence=["#00eaff"])

        fig4 = style_fig(fig4, f"{relationship_chart_type}: {kpi1} vs {kpi2}", kpi1, kpi2)
        st.plotly_chart(fig4, use_container_width=True, key="relationship_chart")
    else:
        st.info("Select Secondary KPI to show relationship chart.")

# =========================
# DATA TABLE - TRUST LAYER
# =========================
st.markdown("### 📋 Data Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    height=350
)

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
