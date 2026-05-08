# =========================
# STYLE - FINAL GOLDEN VERSION
# =========================
st.markdown("""
<style>

/* =========================================================
   🌑 GLOBAL BACKGROUND
========================================================= */
html, body, .stApp {
    background-color: #050505 !important;
    color: #ffffff !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* =========================================================
   📦 MAIN CARDS / SECTIONS
========================================================= */
.element-container {
    background: #0b0f14 !important;
    border: 1px solid rgba(0, 234, 255, 0.25) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    margin-bottom: 16px !important;
}

.element-container:hover {
    border: 1px solid rgba(0, 234, 255, 0.45) !important;
    transition: 0.2s ease-in-out;
}

/* =========================================================
   🎛️ SIDEBAR / CONTROL PANEL
========================================================= */
section[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid rgba(0, 234, 255, 0.35) !important;
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
    border: 1px solid rgba(0, 234, 255, 0.35) !important;
    border-radius: 12px !important;
    padding: 12px !important;
    margin-bottom: 18px !important;
}

/* =========================================================
   🔽 INPUTS / DROPDOWNS
========================================================= */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #050505 !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 234, 255, 0.35) !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* =========================================================
   📂 FILE UPLOADER FIX
========================================================= */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background-color: #050505 !important;
    border: 1px dashed rgba(0, 234, 255, 0.45) !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
    background-color: #111827 !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 234, 255, 0.25) !important;
    border-radius: 8px !important;
}

/* =========================================================
   📊 KPI NUMBERS
========================================================= */
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

/* =========================================================
   📝 HEADINGS
========================================================= */
h1 {
    color: #ffffff !important;
    font-size: 42px !important;
    font-weight: 900 !important;
}

h2, h3 {
    color: #ffffff !important;
    font-weight: 850 !important;
}

/* =========================================================
   📈 PLOTLY TEXT / AXIS / LEGEND
========================================================= */
.js-plotly-plot .plotly text {
    fill: #ffffff !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

.js-plotly-plot .plotly .xtitle,
.js-plotly-plot .plotly .ytitle {
    font-size: 16px !important;
    font-weight: 700 !important;
}

.js-plotly-plot .plotly .gtitle {
    font-size: 20px !important;
    font-weight: 800 !important;
}

.js-plotly-plot .plotly .legend text {
    font-size: 14px !important;
    font-weight: 700 !important;
}

/* =========================================================
   🖱️ PLOTLY HOVER TOOLTIP FIX
========================================================= */
.js-plotly-plot .hoverlayer .hovertext {
    fill: #ffffff !important;
}

.js-plotly-plot .hoverlayer path {
    fill: #0b1220 !important;
    stroke: #00eaff !important;
}

/* =========================================================
   📈 PLOTLY BACKGROUND CLEANUP
========================================================= */
.js-plotly-plot .plotly {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)S
