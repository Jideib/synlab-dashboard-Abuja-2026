# app.py - SYNLAB Dashboard Cover Page (Landing Page)
import os
import pandas as pd
import streamlit as st
from PIL import Image
from utils import render_hero_logo

# ===== PAGE CONFIGURATION =====

icon = Image.open("assets/synlab_logo.png")

st.set_page_config(
    page_title="SYNLAB Nigeria · Market Intelligence",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===== HIDE DEFAULT STREAMLIT ELEMENTS & GLOBAL STYLES =====
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .st-emotion-cache-1y4p8pa {display: none;}

    .stApp {
        background: linear-gradient(180deg, #F0F7FA 0%, #FFFFFF 100%);
    }

    .main > div {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }

    :root {
        --synlab-cerulean: #0077AD;
        --synlab-midnight: #003765;
        --synlab-halfbaked: #7CB8D3;
        --synlab-navy: #0A2647;
        --synlab-bg-light: #E8F4F8;
    }

    .cover-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 20px 0;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, var(--synlab-midnight) 0%, var(--synlab-cerulean) 100%);
        border-radius: 20px;
        padding: 48px 56px;
        text-align: center;
        color: white;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 55, 101, 0.15);
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: rgba(124, 184, 211, 0.08);
        border-radius: 50%;
    }

    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -40%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: rgba(124, 184, 211, 0.06);
        border-radius: 50%;
    }

    .hero-icon {
        font-size: 56px;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        position: relative;
        z-index: 1;
    }

    .hero-title .highlight {
        color: var(--synlab-halfbaked);
    }

    .hero-subtitle {
        font-size: 20px;
        opacity: 0.9;
        margin: 10px 0 0;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }

    .hero-divider {
        width: 60px;
        height: 4px;
        background: var(--synlab-halfbaked);
        margin: 20px auto 0;
        border-radius: 2px;
        position: relative;
        z-index: 1;
    }

    .hero-meta {
        display: flex;
        justify-content: center;
        gap: 48px;
        margin-top: 28px;
        position: relative;
        z-index: 1;
        flex-wrap: wrap;
    }

    .hero-meta-item {
        text-align: center;
    }

    .hero-meta-value {
        font-size: 26px;
        font-weight: 700;
        display: block;
    }

    .hero-meta-label {
        font-size: 13px;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* KPI Cards */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-top: 4px solid var(--synlab-cerulean);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 119, 173, 0.12);
    }

    .kpi-card:nth-child(1) { border-top-color: var(--synlab-midnight); }
    .kpi-card:nth-child(2) { border-top-color: var(--synlab-cerulean); }
    .kpi-card:nth-child(3) { border-top-color: #2C8FC7; }
    .kpi-card:nth-child(4) { border-top-color: var(--synlab-halfbaked); }

    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--synlab-midnight);
    }

    .kpi-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }

    .kpi-trend {
        font-size: 12px;
        margin-top: 6px;
        color: #0077AD;
        font-weight: 500;
    }

    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-attention { background: #E8F4F8; color: #003765; border: 1px solid #7CB8D3; }

    /* Insights Section */
    .insights-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }

    .insight-card {
        background: var(--synlab-bg-light);
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 4px solid var(--synlab-cerulean);
    }

    .insight-number {
        font-size: 20px;
        font-weight: 700;
        color: var(--synlab-cerulean);
    }

    .insight-title {
        font-weight: 600;
        color: var(--synlab-midnight);
        margin: 6px 0 4px;
        font-size: 16px;
    }

    .insight-desc {
        font-size: 13px;
        color: #475569;
        line-height: 1.5;
        margin: 0;
    }

    .insight-tag {
        display: inline-block;
        background: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        color: var(--synlab-cerulean);
        font-weight: 600;
        margin-top: 10px;
    }

    /* Footer */
    .cover-footer {
        background: var(--synlab-navy);
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        color: white;
        font-size: 13px;
        margin-top: 32px;
    }

    .cover-footer strong {
        color: var(--synlab-halfbaked);
    }

    .cover-footer .separator {
        margin: 0 10px;
        opacity: 0.3;
    }

    @media (max-width: 900px) {
        .kpi-row { grid-template-columns: repeat(2, 1fr); }
        .insights-row { grid-template-columns: 1fr; }
        .hero-title { font-size: 32px; }
        .hero-meta { gap: 20px; }
    }
</style>
""",
    unsafe_allow_html=True,
)


# ===== DATA LOADING =====
@st.cache_data
def load_data():
    possible_paths = [
        "data/synlab_clean.csv",
        "synlab_clean.csv",
        "../data/synlab_clean.csv",
        "../synlab_clean.csv",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    return pd.DataFrame()


data = load_data()

if data.empty:
    st.error(
        "⚠️ Data file not found. Please ensure 'synlab_clean.csv' is in the data folder."
    )
    st.stop()

# ===== CALCULATE VERIFIED METRICS =====
total = len(data)
awareness = (data["aware_synlab"].sum() / total) * 100 if total > 0 else 0
usage = (data["used_synlab"].sum() / total) * 100 if total > 0 else 0
awareness_gap = awareness - usage

# NPS Calculation (Valid Responses)
nps_valid = data[data["nps_score"].notna()]
nps_valid_count = len(nps_valid)

promoters = (nps_valid["nps_segment"] == "Promoter").sum()
passives = (nps_valid["nps_segment"] == "Passive").sum()
detractors = (nps_valid["nps_segment"] == "Detractor").sum()

promoter_pct = (promoters / nps_valid_count * 100) if nps_valid_count > 0 else 0
detractor_pct = (
    (detractors / nps_valid_count * 100) if nps_valid_count > 0 else 0
)
nps = promoter_pct - detractor_pct

# ===== COVER CONTENT DISPLAY =====
st.markdown('<div class="cover-container">', unsafe_allow_html=True)

# Hero Section
logo_html = render_hero_logo(height=75, style="margin-bottom: 16px;")

st.markdown(
    f"""
<div class="hero-section">
    {logo_html}
    <h1 class="hero-title">SYNLAB <span class="highlight">Nigeria</span></h1>
    <p class="hero-subtitle">Market Research & Brand Health Dashboard</p>
    <div class="hero-divider"></div>
    <div class="hero-meta">
        <div class="hero-meta-item">
            <span class="hero-meta-value">Abuja</span>
            <span class="hero-meta-label">Market</span>
        </div>
        <div class="hero-meta-item">
            <span class="hero-meta-value">2026</span>
            <span class="hero-meta-label">Year</span>
        </div>
        <div class="hero-meta-item">
            <span class="hero-meta-value">5</span>
            <span class="hero-meta-label">Locations</span>
        </div>
        <div class="hero-meta-item">
            <span class="hero-meta-value">{total}</span>
            <span class="hero-meta-label">Respondents</span>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# High-Level KPI Row
st.markdown(
    f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-value">{total}</div>
        <div class="kpi-label">Total Surveyed</div>
        <div class="kpi-trend">📍 5 Core Locations</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{awareness:.1f}%</div>
        <div class="kpi-label">Brand Awareness</div>
        <div class="kpi-trend">↑ {data['aware_synlab'].sum()} Aware</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{usage:.1f}%</div>
        <div class="kpi-label">Usage Rate</div>
        <div class="kpi-trend">↑ {data['used_synlab'].sum()} Active Users</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value" style="color: #003765;">{nps:.1f}</div>
        <div class="kpi-label">Net Promoter Score</div>
        <div class="kpi-trend"><span class="status-badge status-attention">Needs Attention</span></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Strategic Callouts
st.markdown(
    f"""
<div class="insights-row">
    <div class="insight-card">
        <div class="insight-number">01</div>
        <div class="insight-title">Awareness-Usage Gap</div>
        <div class="insight-desc">
            A <strong>{awareness_gap:.1f}%</strong> conversion gap exists between aware respondents ({data['aware_synlab'].sum()}) and active users ({data['used_synlab'].sum()}).
        </div>
        <span class="insight-tag">🎯 Conversion Opportunity</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">02</div>
        <div class="insight-title">Detractor Mitigation</div>
        <div class="insight-desc">
            NPS stands at <strong>{nps:.1f}</strong> with <strong>{detractor_pct:.1f}%</strong> detractors ({detractors}). Converting <strong>{passives}</strong> passive respondents is key to growth.
        </div>
        <span class="insight-tag">📈 Retention Focus</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">03</div>
        <div class="insight-title">Geographic Expansion</div>
        <div class="insight-desc">
            <strong>Wuse</strong> leads market usage, while <strong>Gwagwalada</strong> (33.3% awareness) presents a high-potential market for targeted campaigns.
        </div>
        <span class="insight-tag">📍 Geographic Strategy</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Navigation Section
st.markdown(
    '<p style="font-size: 16px; font-weight: 700; color: #003765; margin: 8px 0 16px 0;">📑 Dashboard Navigation</p>',
    unsafe_allow_html=True,
)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button(
        "📈 Overview", use_container_width=True, key="cover_nav_overview"
    ):
        st.switch_page("pages/1_Executive_Overview.py")

with nav_col2:
    if st.button(
        "🏷️ Brand Health", use_container_width=True, key="cover_nav_brand"
    ):
        st.switch_page("pages/2_Brand_Health.py")

with nav_col3:
    if st.button(
        "👥 Customer Insights",
        use_container_width=True,
        key="cover_nav_insights",
    ):
        st.switch_page("pages/3_Customer_Insights.py")

with nav_col4:
    if st.button(
        "⚔️ Competitive Intel", use_container_width=True, key="cover_nav_comp"
    ):
        st.switch_page("pages/4_Competitive_Intelligence.py")

with nav_col5:
    if st.button(
        "💡 Strategic Analytics",
        use_container_width=True,
        key="cover_nav_strat",
    ):
        st.switch_page("pages/5_Strategic_Analytics.py")

# Footer
st.markdown(
    f"""
<div class="cover-footer">
    <strong>SYNLAB Nigeria</strong> · Strategic Market Intelligence Report
    <span class="separator">|</span>
    {total} Respondents · 5 Locations · Abuja Focus
    <br>
    <span style="font-size: 11px; opacity: 0.75;">Research and Analysis carried out by Kinetiq Growth Lab for SYNLAB Nigeria</span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
