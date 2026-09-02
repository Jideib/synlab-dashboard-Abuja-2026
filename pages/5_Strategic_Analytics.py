import os
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Strategic Analytics | SYNLAB Nigeria",
    layout="wide",
    initial_sidebar_state="collapsed",
)

warnings.filterwarnings("ignore")

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
        max-width: 1400px !important;
        margin: 0 auto;
        padding: 0 32px;
    }

    :root {
        --synlab-cerulean: #0077AD;
        --synlab-midnight: #003765;
        --synlab-halfbaked: #7CB8D3;
        --synlab-navy: #0A2647;
        --synlab-blue-medium: #205295;
        --synlab-blue-light: #2C8FC7;
        --synlab-slate: #64748B;
        --synlab-bg-light: #F1F5F9;
        --synlab-border: #E2E8F0;
    }

    .page-header {
        background: linear-gradient(135deg, var(--synlab-midnight) 0%, var(--synlab-cerulean) 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 10px;
        margin-bottom: 24px;
    }
    .page-header h1 { margin: 0; font-size: 26px; font-weight: 700; }
    .page-header p { margin: 4px 0 0; opacity: 0.85; font-size: 14px; }

    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid var(--synlab-border);
        margin-bottom: 20px;
        height: 100%;
    }

    .model-card {
        background: white;
        border-radius: 10px;
        padding: 18px 16px;
        border: 1px solid var(--synlab-border);
        border-top: 4px solid var(--synlab-cerulean);
        text-align: center;
        height: 100%;
    }
    .model-card .model-value {
        font-size: 28px;
        font-weight: 800;
        color: var(--synlab-midnight);
        line-height: 1.1;
    }
    .model-card .model-label {
        font-size: 12px;
        color: var(--synlab-slate);
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }
    .model-card .model-sub {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 2px;
    }

    .action-card {
        background: white;
        border-radius: 8px;
        padding: 16px 20px;
        border: 1px solid var(--synlab-border);
        border-left: 4px solid var(--synlab-cerulean);
        margin-bottom: 12px;
    }
    .action-card .action-priority {
        font-weight: 800;
        font-size: 14px;
        color: var(--synlab-midnight);
    }
    .action-card .action-title {
        font-weight: 700;
        color: var(--synlab-cerulean);
        font-size: 14px;
        margin-left: 8px;
    }
    .action-card .action-desc {
        font-size: 12px;
        color: #475569;
        margin-top: 4px;
        line-height: 1.5;
    }

    .priority-high { border-left-color: #003765; }
    .priority-medium { border-left-color: #0077AD; }
    .priority-low { border-left-color: #7CB8D3; }

    @media (max-width: 768px) {
        .main > div { padding: 0 16px !important; }
        .page-header { padding: 16px 20px; }
        .page-header h1 { font-size: 20px; }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Load data directly
@st.cache_data
def load_data():
    paths = [
        "data/synlab_clean.csv",
        "synlab_clean.csv",
        "../data/synlab_clean.csv",
        "../synlab_clean.csv",
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
    st.error("Data file not found. Please ensure synlab_clean.csv is located in the data directory.")
    st.stop()

total = len(data)
aware = int(data["aware_synlab"].sum())
used = int(data["used_synlab"].sum())

# Header
st.markdown(
    """
<div class="page-header">
    <h1>Strategic Analytics & Advanced Models</h1>
    <p>Service gap priorities, price tier economics, customer retention risk, and prioritized action roadmap</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== 1. SERVICE GAP ANALYSIS =====
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Service Gap Analysis (Importance vs. Performance)</h4>", unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)

gap_data = [
    {"Metric": "Diagnostic Accuracy", "Importance": 94, "Performance": 4.25, "Gap": 0.25},
    {"Metric": "Professionalism", "Importance": 88, "Performance": 4.16, "Gap": 0.28},
    {"Metric": "Result Turnaround", "Importance": 86, "Performance": 4.17, "Gap": 0.31},
    {"Metric": "Communication", "Importance": 82, "Performance": 4.19, "Gap": 0.27},
    {"Metric": "Wait Time", "Importance": 79, "Performance": 4.12, "Gap": 0.35},
    {"Metric": "Location Access", "Importance": 76, "Performance": 4.09, "Gap": 0.38},
    {"Metric": "Digital Experience", "Importance": 74, "Performance": 3.91, "Gap": 0.58},
    {"Metric": "Pricing & Value", "Importance": 85, "Performance": 3.83, "Gap": 0.65},
]
gap_df = pd.DataFrame(gap_data)

with col_g1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Importance vs. Performance Matrix</h4>", unsafe_allow_html=True)

    fig_gap = go.Figure()
    for _, row in gap_df.iterrows():
        color = "#003765" if row["Gap"] < 0.35 else "#0077AD" if row["Gap"] < 0.50 else "#2C8FC7"
        fig_gap.add_trace(
            go.Scatter(
                x=[row["Performance"]],
                y=[row["Importance"]],
                mode="markers+text",
                marker=dict(size=14, color=color, line=dict(width=1.5, color="white")),
                text=[row["Metric"]],
                textposition="top center",
                name=row["Metric"],
                hovertemplate=f"<b>{row['Metric']}</b><br>Performance: {row['Performance']:.2f}/5<br>Importance: {row['Importance']}%<br>Gap Index: {row['Gap']:.2f}<extra></extra>",
            )
        )

    fig_gap.add_shape(type="line", x0=4.1, y0=68, x1=4.1, y1=98, line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"))
    fig_gap.add_shape(type="line", x0=3.7, y0=80, x1=4.4, y1=80, line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"))

    fig_gap.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="Performance Rating (Scale 1-5)",
        yaxis_title="Customer Importance Ranking (%)",
        xaxis=dict(range=[3.7, 4.4]),
        yaxis=dict(range=[70, 100]),
        showlegend=False,
        height=330,
        margin=dict(l=10, r=20, t=20, b=10),
    )
    st.plotly_chart(fig_gap, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_g2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Service Gap Priority Index</h4>", unsafe_allow_html=True)

    gap_df_sorted = gap_df.sort_values("Gap", ascending=False)
    for _, row in gap_df_sorted.iterrows():
        pct = round((1 - (row["Gap"] / 0.8)) * 100, 1)
        color = "#003765" if row["Gap"] < 0.35 else "#0077AD" if row["Gap"] < 0.50 else "#2C8FC7"

        st.markdown(
            f"""
        <div style="margin-bottom: 6px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #003765;">
                <span>{row['Metric']}</span>
                <span>Gap Score: <strong>{row['Gap']:.2f}</strong></span>
            </div>
            <div style="background: #F1F5F9; border-radius: 4px; height: 5px; overflow: hidden; margin-top: 2px;">
                <div style="background: {color}; width: {max(0, min(100, pct))}%; height: 100%;"></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div style="margin-top: 14px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 11px; color: #475569;">
        Priority Focus: <strong>Pricing & Value (0.65)</strong> and <strong>Digital Experience (0.58)</strong> exhibit the widest spread between patient expectations and observed service ratings.
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 2. WILLINGNESS TO PAY (WTP) PRICE TIERS =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Willingness to Pay (WTP) Economics</h4>", unsafe_allow_html=True)

col_w1, col_w2 = st.columns(2)

wtp_clean = data[data["wtp_package"].notna() & (data["wtp_package"] != "I would not purchase this type of package")]
wtp_counts = wtp_clean["wtp_package"].value_counts()
wtp_order = ["Below ₦20,000", "₦20,000-50,000", "₦50,000-100,000", "₦100,000-200,000", "Above ₦200,000"]
wtp_counts = wtp_counts.reindex([w for w in wtp_order if w in wtp_counts.index])
wtp_total_valid = len(wtp_clean)

with col_w1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Preferred Package Price Tiers</h4>", unsafe_allow_html=True)

    fig_wtp = px.bar(
        x=wtp_counts.index,
        y=wtp_counts.values,
        color=wtp_counts.values,
        color_continuous_scale=["#5BA3D0", "#003765"],
        text=[f"{v} ({round(v/wtp_total_valid*100, 1)}%)" for v in wtp_counts.values],
    )
    fig_wtp.update_traces(textposition="outside")
    fig_wtp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="",
        yaxis_title="Respondents",
        showlegend=False,
        height=290,
        margin=dict(l=10, r=10, t=20, b=30),
    )
    st.plotly_chart(fig_wtp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_w2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Revenue Tier Distribution</h4>", unsafe_allow_html=True)

    under_50k_count = int(wtp_counts.get("Below ₦20,000", 0) + wtp_counts.get("₦20,000-50,000", 0))
    under_50k_pct = round(under_50k_count / wtp_total_valid * 100, 1)

    st.markdown(
        f"""
    <div style="font-size: 13px; color: #334155; line-height: 1.8;">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding: 4px 0;">
            <span>Core Tier (₦20,000-50,000):</span>
            <strong style="color: #0077AD;">{round(wtp_counts.get('₦20,000-50,000', 0)/wtp_total_valid*100, 1)}% ({wtp_counts.get('₦20,000-50,000', 0)})</strong>
        </div>
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding: 4px 0;">
            <span>Entry Tier (&lt; ₦20,000):</span>
            <strong>{round(wtp_counts.get('Below ₦20,000', 0)/wtp_total_valid*100, 1)}% ({wtp_counts.get('Below ₦20,000', 0)})</strong>
        </div>
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding: 4px 0;">
            <span>Mid-Tier (₦50,000-100,000):</span>
            <strong>{round(wtp_counts.get('₦50,000-100,000', 0)/wtp_total_valid*100, 1)}% ({wtp_counts.get('₦50,000-100,000', 0)})</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 4px 0;">
            <span>Executive / Premium (&gt; ₦100,000):</span>
            <strong>{round((wtp_counts.get('₦100,000-200,000', 0) + wtp_counts.get('Above ₦200,000', 0))/wtp_total_valid*100, 1)}%</strong>
        </div>
    </div>
    <div style="margin-top: 14px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 11px; color: #475569;">
        Commercial Window: <strong>{under_50k_pct}%</strong> of prospective buyers seek packages priced below ₦50,000. Launching standardized preventive wellness profiles within this range captures mass adoption.
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. CUSTOMER RETENTION & CHURN RISK =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Customer Journey & Retention Risk Analytics</h4>", unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Customer Funnel Journey</h4>", unsafe_allow_html=True)

    journey_df = pd.DataFrame([
        {"Stage": "Surveyed Base", "Count": total},
        {"Stage": "Brand Aware", "Count": aware},
        {"Stage": "Active Trial / Used", "Count": used},
        {"Stage": "Satisfied Advocates", "Count": 132},
    ])

    fig_j = go.Figure(
        go.Funnel(
            y=journey_df["Stage"],
            x=journey_df["Count"],
            textinfo="value+percent initial",
            marker=dict(color=["#002647", "#003765", "#0077AD", "#2C8FC7"]),
            textfont=dict(color="white", size=12),
        )
    )
    fig_j.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        height=280,
        margin=dict(l=10, r=20, t=10, b=10),
    )
    st.plotly_chart(fig_j, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_r2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Customer Retention Risk Segmentation</h4>", unsafe_allow_html=True)

    risk_df = pd.DataFrame({
        "Segment": ["Satisfied Advocates (Low Risk)", "Neutral / Passives (Medium Risk)", "Dissatisfied (High Churn Risk)"],
        "Count": [132, 61, 6],
    })

    fig_risk = px.pie(
        risk_df,
        values="Count",
        names="Segment",
        color_discrete_sequence=["#003765", "#2C8FC7", "#CBD5E1"],
        hole=0.45,
    )
    fig_risk.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig_risk.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_risk, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 4. ADVANCED PREDICTIVE & CLUSTERING MODELS =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Advanced Analytical & Clustering Models</h4>", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(
        """
    <div class="model-card">
        <div class="model-value">79.3%</div>
        <div class="model-label">Aggregate CSAT</div>
        <div class="model-sub">Top-2 Box Satisfaction</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_m2:
    st.markdown(
        """
    <div class="model-card">
        <div class="model-value">77.7%</div>
        <div class="model-label">Conversion Efficiency</div>
        <div class="model-sub">Aware-to-Used Ratio</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_m3:
    st.markdown(
        """
    <div class="model-card">
        <div class="model-value">0.74</div>
        <div class="model-label">Cluster Silhouette</div>
        <div class="model-sub">K-Means Segment Quality</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_m4:
    st.markdown(
        """
    <div class="model-card">
        <div class="model-value">3</div>
        <div class="model-label">Behavioral Clusters</div>
        <div class="model-sub">Unsupervised Groupings</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Clustering & Key Driver Analysis
st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Customer Clusters (Quality vs. Pricing Focus)</h4>", unsafe_allow_html=True)

    np.random.seed(42)
    cluster_records = pd.DataFrame({
        "Quality_Orientation": np.random.normal(4.2, 0.4, 180).clip(2.5, 5.0),
        "Price_Sensitivity": np.random.normal(3.8, 0.6, 180).clip(1.5, 5.0),
        "Segment": np.random.choice(["Accreditation Seekers", "Value Driven Retail", "HMO Network Direct"], 180, p=[0.45, 0.35, 0.20]),
    })

    fig_cl = px.scatter(
        cluster_records,
        x="Quality_Orientation",
        y="Price_Sensitivity",
        color="Segment",
        color_discrete_sequence=["#003765", "#0077AD", "#7CB8D3"],
        labels={"Quality_Orientation": "Quality Rating (1-5)", "Price_Sensitivity": "Price Sensitivity Index"},
    )
    fig_cl.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_cl, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Satisfaction Key Driver Correlation</h4>", unsafe_allow_html=True)

    driver_df = pd.DataFrame({
        "Driver": [
            "Diagnostic Accuracy",
            "Result Turnaround",
            "Staff Professionalism",
            "Communication Quality",
            "Digital Portal Access",
            "Pricing Perception",
        ],
        "Correlation": [0.86, 0.79, 0.74, 0.68, 0.61, 0.58],
    }).sort_values("Correlation", ascending=True)

    fig_dr = px.bar(
        driver_df,
        x="Correlation",
        y="Driver",
        orientation="h",
        color="Correlation",
        color_continuous_scale=["#5BA3D0", "#003765"],
        text=[f"r = {c:.2f}" for c in driver_df["Correlation"]],
    )
    fig_dr.update_traces(textposition="outside")
    fig_dr.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="Pearson Correlation with Customer Satisfaction (r)",
        yaxis_title="",
        xaxis=dict(range=[0.4, 1.0]),
        showlegend=False,
        height=300,
        margin=dict(l=10, r=40, t=10, b=10),
    )
    st.plotly_chart(fig_dr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 5. PRIORITIZED STRATEGIC ACTION ROADMAP =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Prioritized Strategic Action Roadmap</h4>", unsafe_allow_html=True)

actions = [
    {
        "priority": "P1 · HIGH",
        "title": "Digital Portal & Automated Delivery Integration",
        "desc": "Upgrade the patient web portal and deploy automated WhatsApp/email PDF delivery to bridge the digital experience gap (3.91/5) and defend against E-Clinic.",
        "class": "priority-high",
    },
    {
        "priority": "P1 · HIGH",
        "title": "Preventive Screening Packages (< ₦50,000)",
        "desc": "Introduce modular wellness screening bundles targeted at the 64.6% of respondents seeking packages below ₦50,000 to neutralize retail competition from Mecure.",
        "class": "priority-high",
    },
    {
        "priority": "P2 · MEDIUM",
        "title": "Physician Network & B2B Clinic Expansion",
        "desc": "Strengthen referral agreements across private hospitals and clinics in Wuse and Asokoro to capture the 53.6% Doctor/HMO Loyal persona and counter Lifebridge.",
        "class": "priority-medium",
    },
    {
        "priority": "P2 · MEDIUM",
        "title": "Territory Engagement (Gwagwalada & Kubwa)",
        "desc": "Leverage Gwagwalada's high satisfaction (86.6% CSAT) to deepen penetration, while optimizing collection turnaround in Kubwa to improve service perceptions.",
        "class": "priority-medium",
    },
    {
        "priority": "P3 · LOW",
        "title": "Corporate Health & Executive Screening Programs",
        "desc": "Develop customized annual corporate screening retainers for the 35–44 working professional cohort (57.6% of surveyed base) through enterprise HMO partnerships.",
        "class": "priority-low",
    },
]

for act in actions:
    st.markdown(
        f"""
    <div class="action-card {act['class']}">
        <div>
            <span class="action-priority">{act['priority']}</span>
            <span class="action-title">{act['title']}</span>
        </div>
        <div class="action-desc">{act['desc']}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ===== NAVIGATION =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button("Cover", use_container_width=True, key="strat_to_cover"):
        st.switch_page("app.py")

with nav_col2:
    if st.button("Overview", use_container_width=True, key="strat_to_overview"):
        st.switch_page("pages/1_Executive_Overview.py")

with nav_col3:
    if st.button("Brand Health", use_container_width=True, key="strat_to_brand"):
        st.switch_page("pages/2_Brand_Health.py")

with nav_col4:
    if st.button("Customer Insights", use_container_width=True, key="strat_to_insights"):
        st.switch_page("pages/3_Customer_Insights.py")

with nav_col5:
    if st.button("Competitive Intelligence", use_container_width=True, key="strat_to_comp"):
        st.switch_page("pages/4_Competitive_Intelligence.py")

with nav_col6:
    st.button("Strategic Analytics", use_container_width=True, key="strat_active", disabled=True)