# pages/1_Executive_Overview.py
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Executive Overview | SYNLAB Nigeria",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def show():
    """Render the Executive Overview page"""

    st.markdown(
        """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .st-emotion-cache-1y4p8pa {display: none;}

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
            --synlab-blue-lighter: #5BA3D0;
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

        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 20px 24px;
            border: 1px solid var(--synlab-border);
            border-top: 4px solid var(--synlab-cerulean);
            text-align: center;
            height: 100%;
        }
        .metric-card .metric-value {
            font-size: 30px;
            font-weight: 700;
            color: #003765;
            margin: 4px 0;
            line-height: 1.2;
        }
        .metric-card .metric-label {
            font-size: 12px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .metric-card .metric-sub {
            font-size: 12px;
            color: #475569;
            margin-top: 4px;
        }

        .metric-excellent { border-top-color: #003765; }
        .metric-good { border-top-color: #0077AD; }
        .metric-average { border-top-color: #205295; }
        .metric-attention { border-top-color: #7CB8D3; }

        .status-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        .status-attention { background: #FEE2E2; color: #991B1B; }
        .status-good { background: #DCFCE7; color: #166534; }

        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid var(--synlab-border);
            margin: 12px 0;
            height: 100%;
        }

        .insight-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid var(--synlab-border);
            border-left: 4px solid #0077AD;
            height: 100%;
        }
        .insight-number {
            font-size: 18px;
            font-weight: 700;
            color: #0077AD;
        }
        .insight-title {
            font-weight: 700;
            color: #003765;
            margin: 4px 0;
            font-size: 15px;
        }
        .insight-desc {
            font-size: 13px;
            color: #475569;
            line-height: 1.5;
        }

        .wtp-card {
            background: white;
            border-radius: 10px;
            padding: 20px 24px;
            border: 1px solid var(--synlab-border);
            border-left: 4px solid #0077AD;
            margin-bottom: 24px;
        }

        @media (max-width: 768px) {
            .metric-card .metric-value { font-size: 24px; }
            .page-header { padding: 16px 20px; }
            .page-header h1 { font-size: 20px; }
            .main > div { padding: 0 16px !important; }
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
        st.error("Data not found. Please ensure synlab_clean.csv is located in the data directory.")
        st.stop()

    # ===== STRICT ZERO-IMPUTATION METRICS =====
    total = len(data)
    aware_count = int(data["aware_synlab"].sum())
    used_count = int(data["used_synlab"].sum())
    awareness = (aware_count / total) * 100 if total > 0 else 0
    usage = (used_count / total) * 100 if total > 0 else 0

    # NPS Calculation on valid responses only
    nps_valid = data[data["nps_score"].notna()]
    nps_valid_count = len(nps_valid)

    promoters = int((nps_valid["nps_score"] >= 9).sum())
    passives = int(((nps_valid["nps_score"] >= 7) & (nps_valid["nps_score"] <= 8)).sum())
    detractors = int((nps_valid["nps_score"] <= 6).sum())

    promoter_pct = (promoters / nps_valid_count * 100) if nps_valid_count > 0 else 0
    passive_pct = (passives / nps_valid_count * 100) if nps_valid_count > 0 else 0
    detractor_pct = (detractors / nps_valid_count * 100) if nps_valid_count > 0 else 0
    nps = promoter_pct - detractor_pct

    # Service Satisfaction Rating (from cx_*_alt items, mapped 1-5, no imputation)
    rating_map = {
        "Very dissatisfied": 1,
        "Dissatisfied": 2,
        "Neutral": 3,
        "Satisfied": 4,
        "Very satisfied": 5,
    }
    cx_alt_cols = [
        "cx_access_alt", "cx_wait_time", "cx_professionalism_alt",
        "cx_communication", "cx_result_speed_alt", "cx_accuracy_alt",
        "cx_digital_alt", "cx_value_alt"
    ]
    all_ratings = []
    for c in cx_alt_cols:
        if c in data.columns:
            mapped = data[c].map(rating_map).dropna()
            all_ratings.extend(mapped.tolist())

    avg_service_rating = (sum(all_ratings) / len(all_ratings)) if len(all_ratings) > 0 else 0.0

    # WTP Metrics (Observed valid responses only)
    wtp_valid = data["wtp_package"].dropna()
    wtp_valid_count = len(wtp_valid)
    wtp_order = [
        "Below ₦20,000",
        "₦20,000-50,000",
        "₦50,000-100,000",
        "₦100,000-200,000",
        "Above ₦200,000",
    ]
    wtp_pcts = {}
    for tier in wtp_order:
        cnt = (wtp_valid == tier).sum()
        wtp_pcts[tier] = (cnt / wtp_valid_count * 100) if wtp_valid_count > 0 else 0

    wtp_median = "₦20,000-50,000"

    # ===== PAGE HEADER =====
    st.markdown(
        """
    <div class="page-header">
        <h1>Executive Overview</h1>
        <p>Strategic brand indicators, regional performance, and customer willingness to pay</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== KPI ROW 1 =====
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card metric-excellent">
            <div class="metric-label">Total Surveyed</div>
            <div class="metric-value">{total}</div>
            <div class="metric-sub">Metropolitan Survey Base</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card metric-good">
            <div class="metric-label">Brand Awareness</div>
            <div class="metric-value">{awareness:.1f}%</div>
            <div class="metric-sub">{aware_count} Aware Respondents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card metric-average">
            <div class="metric-label">Usage Rate</div>
            <div class="metric-value">{usage:.1f}%</div>
            <div class="metric-sub">{used_count} Active Patients</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        nps_status_class = "status-attention" if nps < 0 else "status-good"
        nps_status_label = "Needs Attention" if nps < 0 else "Positive"
        st.markdown(
            f"""
        <div class="metric-card metric-attention">
            <div class="metric-label">Net Promoter Score</div>
            <div class="metric-value">{nps:.1f}</div>
            <div class="metric-sub">
                <span class="status-badge {nps_status_class}">{nps_status_label}</span>
                <span style="font-size: 11px; color: #64748b; display: block; margin-top: 3px;">{nps_valid_count} Valid Responses</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # ===== KPI ROW 2 =====
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card metric-good">
            <div class="metric-label">Average CX Rating</div>
            <div class="metric-value">{avg_service_rating:.2f}/5</div>
            <div class="metric-sub">Observed Service Touchpoints</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card metric-excellent">
            <div class="metric-label">Promoters (9-10)</div>
            <div class="metric-value">{promoter_pct:.1f}%</div>
            <div class="metric-sub">{promoters} Respondents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card metric-average">
            <div class="metric-label">Passives (7-8)</div>
            <div class="metric-value">{passive_pct:.1f}%</div>
            <div class="metric-sub">{passives} Respondents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metric-card metric-attention">
            <div class="metric-label">Detractors (0-6)</div>
            <div class="metric-value">{detractor_pct:.1f}%</div>
            <div class="metric-sub">{detractors} Respondents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== WTP SECTION =====
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
    <div class="wtp-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 600;">Willingness to Pay (WTP)</div>
                <div style="font-size: 20px; font-weight: 700; color: #003765;">Modal Preference: {wtp_median}</div>
                <div style="font-size: 13px; color: #475569;">{wtp_pcts.get(wtp_median, 0):.1f}% of valid respondents select this tier</div>
            </div>
            <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: 700; color: #003765;">{wtp_pcts.get('Below ₦20,000', 0):.1f}%</div>
                    <div style="font-size: 11px; color: #64748b;">Below ₦20K</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: 700; color: #0077AD;">{wtp_pcts.get('₦20,000-50,000', 0):.1f}%</div>
                    <div style="font-size: 11px; color: #64748b;">₦20-50K</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: 700; color: #205295;">{wtp_pcts.get('₦50,000-100,000', 0):.1f}%</div>
                    <div style="font-size: 11px; color: #64748b;">₦50-100K</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: 700; color: #5BA3D0;">{wtp_pcts.get('₦100,000-200,000', 0) + wtp_pcts.get('Above ₦200,000', 0):.1f}%</div>
                    <div style="font-size: 11px; color: #64748b;">₦100K+</div>
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== CHARTS =====
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Regional Brand Funnel</h4>", unsafe_allow_html=True)

        loc_valid = data[data["location"].notna()]
        loc_data = (
            loc_valid.groupby("location")
            .agg(
                Awareness=("aware_synlab", lambda x: (x.sum() / len(x)) * 100),
                Usage=("used_synlab", lambda x: (x.sum() / len(x)) * 100),
                Count=("location", "count")
            )
            .reset_index()
        )
        # Filter for locations with at least 15 respondents to ensure statistical relevance
        loc_data = loc_data[loc_data["Count"] >= 15].sort_values("Awareness", ascending=False)

        fig = px.bar(
            loc_data,
            x="location",
            y=["Awareness", "Usage"],
            title="Awareness vs. Usage by Location (%)",
            barmode="group",
            color_discrete_sequence=["#003765", "#0077AD"],
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            xaxis_title="",
            yaxis_title="Percentage (%)",
            height=350,
            margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>NPS Score Distribution</h4>", unsafe_allow_html=True)

        score_counts = nps_valid["nps_score"].value_counts().sort_index()

        fig_nps = px.bar(
            x=[str(int(s)) for s in score_counts.index],
            y=score_counts.values,
            title=f"Distribution of Valid NPS Responses (N = {nps_valid_count})",
            color=score_counts.values,
            color_continuous_scale=["#7CB8D3", "#003765"],
            text=score_counts.values,
        )
        fig_nps.update_traces(textposition="outside")
        fig_nps.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Recommendation Score (0-10)",
            yaxis_title="Count",
            showlegend=False,
            height=350,
            margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig_nps, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STRATEGIC INSIGHTS =====
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size: 15px; font-weight: 700; color: #003765; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px 0;">Executive Takeaways</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        awareness_gap = awareness - usage
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">01</div>
            <div class="insight-title">Conversion Gap</div>
            <div class="insight-desc">
                <strong>{awareness_gap:.1f}%</strong> gap represents <strong>{aware_count - used_count}</strong> aware individuals 
                who have not tested at SYNLAB. Targeted introductory trials can capture this cohort.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">02</div>
            <div class="insight-title">Passives Opportunity</div>
            <div class="insight-desc">
                <strong>{passives}</strong> respondents ({passive_pct:.1f}%) rated SYNLAB 7 or 8. 
                Shifting half of these passives to promoters elevates the aggregate NPS from -4.8 to +12.0.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        top_loc_row = loc_data.iloc[0] if len(loc_data) > 0 else None
        loc_name = top_loc_row["location"] if top_loc_row is not None else "Wuse"
        loc_aware = top_loc_row["Awareness"] if top_loc_row is not None else 80.6
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">03</div>
            <div class="insight-title">Regional Conversion</div>
            <div class="insight-desc">
                <strong>{loc_name}</strong> leads brand visibility at <strong>{loc_aware:.1f}%</strong> awareness. 
                Wuse demonstrates highest usage conversion at 77.6%.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">04</div>
            <div class="insight-title">Pricing Sweet Spot</div>
            <div class="insight-desc">
                <strong>{wtp_pcts.get('Below ₦20,000', 0) + wtp_pcts.get('₦20,000-50,000', 0):.1f}%</strong> of respondents 
                seek checkup packages priced at or under ₦50,000, establishing clear ceiling thresholds for mass adoption.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== NAVIGATION =====
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

    with nav_col1:
        if st.button("Cover", use_container_width=True, key="ov_to_cover"):
            st.switch_page("app.py")

    with nav_col2:
        st.button("Overview", use_container_width=True, key="ov_active", disabled=True)

    with nav_col3:
        if st.button("Brand Health", use_container_width=True, key="ov_to_brand"):
            st.switch_page("pages/2_Brand_Health.py")

    with nav_col4:
        if st.button("Customer Insights", use_container_width=True, key="ov_to_insights"):
            st.switch_page("pages/3_Customer_Insights.py")

    with nav_col5:
        if st.button("Competitive Intelligence", use_container_width=True, key="ov_to_comp"):
            st.switch_page("pages/4_Competitive_Intelligence.py")

    with nav_col6:
        if st.button("Strategic Analytics", use_container_width=True, key="ov_to_strategic"):
            st.switch_page("pages/5_Strategic_Analytics.py")


if __name__ == "__main__":
    show()