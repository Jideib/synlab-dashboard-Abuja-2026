import os
import pandas as pd
import streamlit as st
from PIL import Image
from utils import render_hero_logo

# Configuration
try:
    icon = Image.open("assets/synlab_logo.png")
    st.set_page_config(
        page_title="SYNLAB Nigeria | Market Intelligence",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    st.set_page_config(
        page_title="SYNLAB Nigeria | Market Intelligence",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

# Clean, Professional Styling (Emoji-Free)
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .st-emotion-cache-1y4p8pa {display: none;}

    .stApp {
        background-color: #F8FAFC;
    }

    .main > div {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
    }

    :root {
        --synlab-cerulean: #0077AD;
        --synlab-midnight: #003765;
        --synlab-halfbaked: #7CB8D3;
        --synlab-navy: #0A2647;
        --synlab-slate: #64748B;
        --synlab-bg-light: #F1F5F9;
        --synlab-border: #E2E8F0;
    }

    .cover-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 16px 0 32px 0;
    }

    .hero-section {
        background: linear-gradient(135deg, var(--synlab-midnight) 0%, var(--synlab-cerulean) 100%);
        border-radius: 12px;
        padding: 44px 48px;
        text-align: center;
        color: #FFFFFF;
        margin-bottom: 28px;
        box-shadow: 0 4px 16px rgba(0, 55, 101, 0.08);
    }

    .hero-title {
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .hero-title .highlight {
        color: var(--synlab-halfbaked);
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin: 8px 0 0;
        font-weight: 400;
    }

    .hero-divider {
        width: 48px;
        height: 3px;
        background: var(--synlab-halfbaked);
        margin: 18px auto 0;
        border-radius: 2px;
    }

    .hero-meta {
        display: flex;
        justify-content: center;
        gap: 48px;
        margin-top: 24px;
        flex-wrap: wrap;
    }

    .hero-meta-item {
        text-align: center;
    }

    .hero-meta-value {
        font-size: 24px;
        font-weight: 700;
        display: block;
    }

    .hero-meta-label {
        font-size: 12px;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }

    .kpi-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--synlab-border);
        border-top: 4px solid var(--synlab-cerulean);
    }

    .kpi-card:nth-child(1) { border-top-color: var(--synlab-midnight); }
    .kpi-card:nth-child(2) { border-top-color: var(--synlab-cerulean); }
    .kpi-card:nth-child(3) { border-top-color: #205295; }
    .kpi-card:nth-child(4) { border-top-color: #7CB8D3; }

    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        color: var(--synlab-midnight);
        line-height: 1.2;
    }

    .kpi-label {
        font-size: 12px;
        color: var(--synlab-slate);
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 6px;
        letter-spacing: 0.5px;
    }

    .kpi-subtext {
        font-size: 12px;
        margin-top: 6px;
        color: #475569;
        font-weight: 500;
    }

    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        background: #FEE2E2;
        color: #991B1B;
    }

    .status-badge.neutral {
        background: #E8F4F8;
        color: #003765;
    }

    .insights-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }

    .insight-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid var(--synlab-border);
        border-left: 4px solid var(--synlab-cerulean);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .insight-header {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-bottom: 8px;
    }

    .insight-number {
        font-size: 16px;
        font-weight: 700;
        color: var(--synlab-cerulean);
    }

    .insight-title {
        font-weight: 700;
        color: var(--synlab-midnight);
        font-size: 15px;
    }

    .insight-desc {
        font-size: 13px;
        color: #475569;
        line-height: 1.55;
        margin: 0 0 12px 0;
    }

    .insight-tag {
        display: inline-block;
        align-self: flex-start;
        background: var(--synlab-bg-light);
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        color: var(--synlab-midnight);
        font-weight: 600;
        border: 1px solid var(--synlab-border);
    }

    .nav-header {
        font-size: 14px;
        font-weight: 700;
        color: var(--synlab-midnight);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 12px 0 14px 0;
    }

    .cover-footer {
        background: #FFFFFF;
        border: 1px solid var(--synlab-border);
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        color: var(--synlab-slate);
        font-size: 12px;
        margin-top: 28px;
    }

    .cover-footer strong {
        color: var(--synlab-midnight);
    }

    .cover-footer .separator {
        margin: 0 8px;
        color: #CBD5E1;
    }

    @media (max-width: 900px) {
        .kpi-row { grid-template-columns: repeat(2, 1fr); }
        .insights-row { grid-template-columns: 1fr; }
        .hero-title { font-size: 30px; }
        .hero-meta { gap: 24px; }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Data Loading
@st.cache_data
def load_data():
    paths = [
        "data/synlab_clean.csv",
        "synlab_clean.csv",
        "data/synlab_clean_standardized.csv",
        "synlab_clean_standardized.csv",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except Exception:
                pass
    return pd.DataFrame()

data = load_data()

if data.empty:
    st.error("Dataset not found. Please ensure synlab_clean.csv is present in the data folder.")
    st.stop()

# Helper for column matching
def find_column(df, patterns):
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
    return None

aware_col = find_column(data, ["aware_synlab"])
used_col = find_column(data, ["used_synlab"])
nps_col = find_column(data, ["nps_score"])
loc_col = find_column(data, ["location"])

if not aware_col or not used_col:
    st.error("Core awareness and usage columns could not be identified.")
    st.stop()

# Exact Metrics Computation
total = len(data)
data[aware_col] = pd.to_numeric(data[aware_col], errors="coerce").fillna(0)
data[used_col] = pd.to_numeric(data[used_col], errors="coerce").fillna(0)

aware_count = int(data[aware_col].sum())
used_count = int(data[used_col].sum())
awareness_pct = (aware_count / total * 100) if total > 0 else 0
usage_pct = (used_count / total * 100) if total > 0 else 0
conversion_gap = awareness_pct - usage_pct
conversion_rate = (used_count / aware_count * 100) if aware_count > 0 else 0

# NPS Computation
nps = 0.0
promoters = 0
passives = 0
detractors = 0
detractor_pct = 0.0
nps_valid_count = 0

if nps_col and nps_col in data.columns:
    data[nps_col] = pd.to_numeric(data[nps_col], errors="coerce")
    nps_valid = data[data[nps_col].notna()]
    nps_valid_count = len(nps_valid)
    if nps_valid_count > 0:
        promoters = int((nps_valid[nps_col] >= 9).sum())
        passives = int(((nps_valid[nps_col] >= 7) & (nps_valid[nps_col] <= 8)).sum())
        detractors = int((nps_valid[nps_col] <= 6).sum())
        promoter_pct = promoters / nps_valid_count * 100
        detractor_pct = detractors / nps_valid_count * 100
        nps = promoter_pct - detractor_pct

# Location Count
location_count = data[loc_col].nunique() if loc_col and loc_col in data.columns else 5

# Layout Presentation
st.markdown('<div class="cover-container">', unsafe_allow_html=True)

# Hero Block
try:
    logo_html = render_hero_logo(height=65, style="margin-bottom: 14px;")
except Exception:
    logo_html = ""

st.markdown(
    f"""
<div class="hero-section">
    {logo_html}
    <h1 class="hero-title">SYNLAB <span class="highlight">Nigeria</span></h1>
    <p class="hero-subtitle">Market Research and Brand Health Intelligence</p>
    <div class="hero-divider"></div>
    <div class="hero-meta">
        <div class="hero-meta-item">
            <span class="hero-meta-value">Abuja</span>
            <span class="hero-meta-label">Primary Market</span>
        </div>
        <div class="hero-meta-item">
            <span class="hero-meta-value">{location_count}</span>
            <span class="hero-meta-label">Survey Locations</span>
        </div>
        <div class="hero-meta-item">
            <span class="hero-meta-value">{total}</span>
            <span class="hero-meta-label">Validated Respondents</span>
        </div>
        <div class="hero-meta-item">
            <span class="hero-meta-value">{conversion_rate:.1f}%</span>
            <span class="hero-meta-label">Aware-to-Used Conversion</span>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# KPI Cards
nps_badge_html = (
    '<span class="status-badge">Needs Attention</span>'
    if nps < 0
    else '<span class="status-badge neutral">Positive</span>'
)

st.markdown(
    f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-value">{total}</div>
        <div class="kpi-label">Total Respondents</div>
        <div class="kpi-subtext">Abuja Metro Coverage</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{awareness_pct:.1f}%</div>
        <div class="kpi-label">Brand Awareness</div>
        <div class="kpi-subtext">{aware_count} of {total} aware</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{usage_pct:.1f}%</div>
        <div class="kpi-label">Market Usage Rate</div>
        <div class="kpi-subtext">{used_count} active users</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{nps:.1f}</div>
        <div class="kpi-label">Net Promoter Score</div>
        <div class="kpi-subtext">{nps_badge_html}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Executive Insights
st.markdown(
    f"""
<div class="insights-row">
    <div class="insight-card">
        <div>
            <div class="insight-header">
                <span class="insight-number">01</span>
                <span class="insight-title">Conversion Opportunity</span>
            </div>
            <p class="insight-desc">
                SYNLAB commands a <strong>{awareness_pct:.1f}%</strong> awareness rate with <strong>{usage_pct:.1f}%</strong> usage. 
                A <strong>{conversion_gap:.1f}%</strong> gap represents <strong>{aware_count - used_count}</strong> aware prospects yet to convert.
            </p>
        </div>
        <span class="insight-tag">Commercial Funnel</span>
    </div>
    <div class="insight-card">
        <div>
            <div class="insight-header">
                <span class="insight-number">02</span>
                <span class="insight-title">Detractor and Passive Profile</span>
            </div>
            <p class="insight-desc">
                NPS is currently <strong>{nps:.1f}</strong> with <strong>{detractors}</strong> detractors ({detractor_pct:.1f}%) and <strong>{passives}</strong> passives. 
                Addressing turnaround times and pricing transparency can shift passives into promoters.
            </p>
        </div>
        <span class="insight-tag">Customer Experience</span>
    </div>
    <div class="insight-card">
        <div>
            <div class="insight-header">
                <span class="insight-number">03</span>
                <span class="insight-title">Geographic Prioritization</span>
            </div>
            <p class="insight-desc">
                <strong>Gwarimpa</strong> and <strong>Wuse</strong> exhibit high usage efficiency, while <strong>Asokoro</strong> and <strong>Gwagwalada</strong> 
                present untapped upside through physician referral alignment.
            </p>
        </div>
        <span class="insight-tag">Territory Strategy</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Navigation
st.markdown('<div class="nav-header">Dashboard Modules</div>', unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("Executive Overview", use_container_width=True, key="cover_nav_overview"):
        st.switch_page("pages/1_Executive_Overview.py")

with nav_col2:
    if st.button("Brand Health", use_container_width=True, key="cover_nav_brand"):
        st.switch_page("pages/2_Brand_Health.py")

with nav_col3:
    if st.button("Customer Insights", use_container_width=True, key="cover_nav_insights"):
        st.switch_page("pages/3_Customer_Insights.py")

with nav_col4:
    if st.button("Competitive Intelligence", use_container_width=True, key="cover_nav_comp"):
        st.switch_page("pages/4_Competitive_Intelligence.py")

with nav_col5:
    if st.button("Strategic Analytics", use_container_width=True, key="cover_nav_strat"):
        st.switch_page("pages/5_Strategic_Analytics.py")

# Footer
st.markdown(
    f"""
<div class="cover-footer">
    <strong>SYNLAB Nigeria</strong> · Market Intelligence Platform
    <span class="separator">|</span>
    {total} Surveyed Records · Comprehensive Abuja Metropolitan Analysis
</div>
</div>
""",
    unsafe_allow_html=True,
)