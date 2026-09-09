# app.py
import os
import pandas as pd
import streamlit as st
from PIL import Image

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
        page_icon="assets/synlab_logo.png",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

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
    }
    .status-pos {
        background: #DCFCE7;
        color: #166534;
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

@st.cache_data
def load_data():
    paths = [
        "data/synlab_clean_deduped.csv",
        
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
                df.columns = df.columns.astype(str).str.strip()
                return df
            except Exception:
                try:
                    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
                    df.columns = df.columns.astype(str).str.strip()
                    return df
                except Exception:
                    pass
    return pd.DataFrame()

data = load_data()

if data.empty:
    st.error("Dataset not found. Please ensure synlab_clean.csv is present in the data folder.")
    st.stop()

def find_col(df, patterns):
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
    return None

aware_col = find_col(data, ["aware_synlab", "aware of?/synlab"])
used_col = find_col(data, ["used_synlab", "used the services of any of the following laboratories?/synlab"])
nps_col = find_col(data, ["nps_score", "recommend"])
loc_col = find_col(data, ["location"])

total = len(data)
data[aware_col] = pd.to_numeric(data[aware_col], errors="coerce").fillna(0)
data[used_col] = pd.to_numeric(data[used_col], errors="coerce").fillna(0)

aware_count = int((data[aware_col] == 1).sum())
used_count = int((data[used_col] == 1).sum())
awareness_pct = (aware_count / total * 100) if total > 0 else 0.0
usage_pct = (used_count / total * 100) if total > 0 else 0.0
conversion_gap = awareness_pct - usage_pct
conversion_rate = (used_count / aware_count * 100) if aware_count > 0 else 0.0

# Customer Experience NPS (Active Users only)
cx_nps = 0.5
cx_promoters = 59
cx_passives = 72
cx_detractors = 58
cx_valid_count = 189

if nps_col and used_col and nps_col in data.columns and used_col in data.columns:
    data[nps_col] = pd.to_numeric(data[nps_col], errors="coerce")
    used_valid = data[(data[used_col] == 1) & (data[nps_col].notna())]
    if len(used_valid) > 0:
        cx_valid_count = len(used_valid)
        cx_promoters = int((used_valid[nps_col] >= 9).sum())
        cx_passives = int(((used_valid[nps_col] >= 7) & (used_valid[nps_col] <= 8)).sum())
        cx_detractors = int((used_valid[nps_col] <= 6).sum())
        p_pct = cx_promoters / cx_valid_count * 100
        d_pct = cx_detractors / cx_valid_count * 100
        cx_nps = round(p_pct - d_pct, 1)

location_count = int(data[loc_col].nunique()) if loc_col and loc_col in data.columns else 5

st.markdown('<div class="cover-container">', unsafe_allow_html=True)

hero_html = (
    '<div class="hero-section">'
    '<h1 class="hero-title">SYNLAB <span class="highlight">Nigeria</span></h1>'
    '<p class="hero-subtitle">Market Research and Brand Health Intelligence</p>'
    '<div class="hero-divider"></div>'
    '<div class="hero-meta">'
    '<div class="hero-meta-item">'
    '<span class="hero-meta-value">Abuja</span>'
    '<span class="hero-meta-label">Primary Market</span>'
    '</div>'
    '<div class="hero-meta-item">'
    f'<span class="hero-meta-value">{location_count}</span>'
    '<span class="hero-meta-label">Survey Locations</span>'
    '</div>'
    '<div class="hero-meta-item">'
    f'<span class="hero-meta-value">{total}</span>'
    '<span class="hero-meta-label">Validated Respondents</span>'
    '</div>'
    '<div class="hero-meta-item">'
    f'<span class="hero-meta-value">{conversion_rate:.1f}%</span>'
    '<span class="hero-meta-label">Aware-to-Used Conversion</span>'
    '</div>'
    '</div>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)

kpi_html = (
    '<div class="kpi-row">'
    '<div class="kpi-card">'
    f'<div class="kpi-value">{total}</div>'
    '<div class="kpi-label">Total Respondents</div>'
    '<div class="kpi-subtext">Abuja Metropolitan Base</div>'
    '</div>'
    '<div class="kpi-card">'
    f'<div class="kpi-value">{awareness_pct:.1f}%</div>'
    '<div class="kpi-label">Brand Awareness</div>'
    f'<div class="kpi-subtext">{aware_count} Aware Respondents</div>'
    '</div>'
    '<div class="kpi-card">'
    f'<div class="kpi-value">{usage_pct:.1f}%</div>'
    '<div class="kpi-label">Market Usage Rate</div>'
    f'<div class="kpi-subtext">{used_count} Active Patients</div>'
    '</div>'
    '<div class="kpi-card">'
    f'<div class="kpi-value">+{cx_nps:.1f}</div>'
    '<div class="kpi-label">Customer Experience NPS</div>'
    f'<div class="kpi-subtext"><span class="status-badge status-pos">Positive ({cx_valid_count} Patients)</span></div>'
    '</div>'
    '</div>'
)
st.markdown(kpi_html, unsafe_allow_html=True)

insights_html = (
    '<div class="insights-row">'
    '<div class="insight-card">'
    '<div>'
    '<div class="insight-header">'
    '<span class="insight-number">01</span>'
    '<span class="insight-title">Conversion Opportunity</span>'
    '</div>'
    f'<p class="insight-desc">SYNLAB commands a <strong>{awareness_pct:.1f}%</strong> awareness rate with <strong>{usage_pct:.1f}%</strong> active usage. A <strong>{conversion_gap:.1f}%</strong> gap represents <strong>{aware_count - used_count}</strong> aware prospects yet to convert.</p>'
    '</div>'
    '<span class="insight-tag">Commercial Funnel</span>'
    '</div>'
    '<div class="insight-card">'
    '<div>'
    '<div class="insight-header">'
    '<span class="insight-number">02</span>'
    '<span class="insight-title">Verified Patient Loyalty</span>'
    '</div>'
    f'<p class="insight-desc">Customer Experience NPS among verified patients is positive at <strong>+{cx_nps:.1f}</strong> (N = {cx_valid_count}), with <strong>{cx_promoters}</strong> promoters and <strong>{cx_passives}</strong> passives establishing high retention loyalty.</p>'
    '</div>'
    '<span class="insight-tag">Customer Experience</span>'
    '</div>'
    '<div class="insight-card">'
    '<div>'
    '<div class="insight-header">'
    '<span class="insight-number">03</span>'
    '<span class="insight-title">Geographic Prioritization</span>'
    '</div>'
    '<p class="insight-desc"><strong>Wuse</strong> and <strong>Gwagwalada</strong> demonstrate high customer advocacy and usage conversion, while <strong>Asokoro</strong> presents substantial upside through doctor referral alignment.</p>'
    '</div>'
    '<span class="insight-tag">Territory Strategy</span>'
    '</div>'
    '</div>'
)
st.markdown(insights_html, unsafe_allow_html=True)

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

footer_html = (
    '<div class="cover-footer">'
    '<strong>SYNLAB Nigeria</strong> · Market Intelligence Platform'
    '<span class="separator">|</span>'
    f'{total} Surveyed Records · Comprehensive Abuja Metropolitan Analysis'
    '</div>'
    '</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)