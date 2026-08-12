# pages/1_Executive_Overview.py
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Executive Overview · SYNLAB Nigeria",
    page_icon="assets/synlab_logo.png",
    layout="wide",  # <--- THIS KEEPS THE PAGE WIDE ON RELOAD
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
            --synlab-bg-light: #E8F4F8;
        }

        .page-header {
            background: linear-gradient(135deg, var(--synlab-midnight) 0%, var(--synlab-cerulean) 100%);
            color: white;
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        .page-header h1 { margin: 0; font-size: 28px; font-weight: 700; }
        .page-header p { margin: 4px 0 0; opacity: 0.85; }

        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-top: 4px solid #0077AD;
            text-align: center;
            height: 100%;
        }
        .metric-card .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #003765;
            margin: 4px 0;
        }
        .metric-card .metric-label {
            font-size: 13px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .metric-card .metric-sub {
            font-size: 13px;
            color: #94a3b8;
        }

        .metric-excellent { border-top-color: #003765; }
        .metric-good { border-top-color: #0077AD; }
        .metric-average { border-top-color: #2C8FC7; }
        .metric-attention { border-top-color: #5BA3D0; }

        .status-badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-excellent { background: #003765; color: white; }
        .status-good { background: #0077AD; color: white; }
        .status-average { background: #2C8FC7; color: white; }
        .status-attention { background: #E8F4F8; color: #003765; border: 1px solid #7CB8D3; }

        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin: 12px 0;
            height: 100%;
        }

        .insight-card {
            background: #E8F4F8;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #0077AD;
            height: 100%;
        }
        .insight-number {
            font-size: 24px;
            font-weight: 700;
            color: #0077AD;
        }
        .insight-title {
            font-weight: 600;
            color: #003765;
            margin: 4px 0;
        }
        .insight-desc {
            font-size: 14px;
            color: #475569;
            line-height: 1.6;
        }

        .wtp-card {
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 4px solid #0077AD;
            margin-bottom: 24px;
        }

        @media (max-width: 768px) {
            .metric-card .metric-value { font-size: 24px; }
            .page-header { padding: 16px 20px; }
            .page-header h1 { font-size: 22px; }
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
        st.error(
            "⚠️ Data not found. Please ensure synlab_clean.csv is in the data folder."
        )
        st.stop()

    # ===== CALCULATE VERIFIED METRICS =====
    total = len(data)
    awareness = (data["aware_synlab"].sum() / total) * 100 if total > 0 else 0
    usage = (data["used_synlab"].sum() / total) * 100 if total > 0 else 0

    # NPS Calculation
    nps_valid = data[data["nps_score"].notna()]
    nps_valid_count = len(nps_valid)

    promoters = (nps_valid["nps_segment"] == "Promoter").sum()
    passives = (nps_valid["nps_segment"] == "Passive").sum()
    detractors = (nps_valid["nps_segment"] == "Detractor").sum()

    promoter_pct = (
        (promoters / nps_valid_count * 100) if nps_valid_count > 0 else 0
    )
    passive_pct = (
        (passives / nps_valid_count * 100) if nps_valid_count > 0 else 0
    )
    detractor_pct = (
        (detractors / nps_valid_count * 100) if nps_valid_count > 0 else 0
    )
    nps = promoter_pct - detractor_pct

    # Avg Impression Rating
    avg_rating = (
        data["overall_impression_score"].mean() if total > 0 else 0
    )

    # Status Labels
    nps_status = "Needs Attention" if nps < 0 else "Good"
    rating_status = "Good" if avg_rating >= 3.5 else "Average"

    # WTP Metrics
    wtp_counts = data["wtp_package"].value_counts()
    wtp_median = "₦20,000-50,000"
    wtp_pcts = {}
    for tier in [
        "Below ₦20,000",
        "₦20,000-50,000",
        "₦50,000-100,000",
        "₦100,000-200,000",
        "Above ₦200,000",
    ]:
        count = (data["wtp_package"] == tier).sum()
        wtp_pcts[tier] = round(count / total * 100, 1) if total > 0 else 0

    # ===== PAGE HEADER =====
    st.markdown(
        """
    <div class="page-header">
        <h1>📈 Executive Overview</h1>
        <p>High-level performance metrics and key strategic insights</p>
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
            <div class="metric-sub">📍 5 Core Locations</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card metric-good">
            <div class="metric-label">Awareness</div>
            <div class="metric-value">{awareness:.1f}%</div>
            <div class="metric-sub">↑ {data['aware_synlab'].sum()} aware</div>
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
            <div class="metric-sub">↑ {data['used_synlab'].sum()} have used</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metric-card metric-attention">
            <div class="metric-label">Net Promoter Score</div>
            <div class="metric-value" style="color: #003765;">{nps:.1f}</div>
            <div class="metric-sub">
                <span class="status-badge status-attention">{nps_status}</span>
                <span style="font-size: 11px; color: #94a3b8; display: block; margin-top: 2px;">{nps_valid_count} valid responses</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== KPI ROW 2 =====
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card metric-good">
            <div class="metric-label">Average Rating</div>
            <div class="metric-value" style="color: #0077AD;">{avg_rating:.2f}/5</div>
            <div class="metric-sub">Overall Impression</div>
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
            <div class="metric-sub">{promoters} respondents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card metric-average">
            <div class="metric-label">Passive (7-8)</div>
            <div class="metric-value">{passive_pct:.1f}%</div>
            <div class="metric-sub">{passives} respondents</div>
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
            <div class="metric-sub">{detractors} respondents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== WTP SECTION =====
    st.markdown("---")

    st.markdown(
        f"""
    <div class="wtp-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="font-size: 13px; color: #64748b; text-transform: uppercase; font-weight: 600;">💰 Willingness to Pay</div>
                <div style="font-size: 20px; font-weight: 700; color: #003765;">Most Common: {wtp_median}</div>
                <div style="font-size: 14px; color: #475569;">{wtp_pcts.get(wtp_median, 0):.1f}% prefer {wtp_median} packages</div>
            </div>
            <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 700; color: #003765;">{wtp_pcts.get('Below ₦20,000', 0):.1f}%</div>
                    <div style="font-size: 12px; color: #64748b;">Below ₦20K</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 700; color: #0077AD;">{wtp_pcts.get('₦20,000-50,000', 0):.1f}%</div>
                    <div style="font-size: 12px; color: #64748b;">₦20-50K</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 700; color: #2C8FC7;">{wtp_pcts.get('₦50,000-100,000', 0):.1f}%</div>
                    <div style="font-size: 12px; color: #64748b;">₦50-100K</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 700; color: #5BA3D0;">{wtp_pcts.get('₦100,000-200,000', 0) + wtp_pcts.get('Above ₦200,000', 0):.1f}%</div>
                    <div style="font-size: 12px; color: #64748b;">₦100K+</div>
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
        st.subheader("📍 Location Performance")

        loc_data = (
            data.groupby("location")
            .agg({
                "aware_synlab": lambda x: (x.sum() / len(x)) * 100,
                "used_synlab": lambda x: (x.sum() / len(x)) * 100,
            })
            .reset_index()
        )
        loc_data.columns = ["Location", "Awareness", "Usage"]
        loc_data = loc_data.sort_values("Awareness", ascending=False)

        fig = px.bar(
            loc_data,
            x="Location",
            y=["Awareness", "Usage"],
            title="Awareness vs Usage by Location (%)",
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
            xaxis_title="Location",
            yaxis_title="Percentage (%)",
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("⭐ Rating Distribution")

        rating_counts = (
            data["overall_impression_score"].value_counts().sort_index()
        )

        fig = px.bar(
            x=rating_counts.index.astype(str),
            y=rating_counts.values,
            title="SYNLAB Rating Distribution (1-5 Stars)",
            color=rating_counts.values,
            color_continuous_scale=[
                "#7CB8D3",
                "#5BA3D0",
                "#2C8FC7",
                "#0077AD",
                "#003765",
            ],
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Rating Scale",
            yaxis_title="Respondents",
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STRATEGIC INSIGHTS =====
    st.markdown("---")
    st.markdown(
        '<p style="font-size: 16px; font-weight: 600; color: #003765; margin: 0 0 16px 0;">💡 Executive Insights</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        awareness_gap = awareness - usage
        aware_not_using = int((awareness_gap / 100) * total)
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">01</div>
            <div class="insight-title">Awareness Gap</div>
            <div class="insight-desc">
                <strong>{awareness_gap:.1f}%</strong> gap — <strong>{aware_not_using}</strong> respondents
                are aware but have not utilized SYNLAB. Focus on trial incentives.
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
            <div class="insight-title">NPS Strategy</div>
            <div class="insight-desc">
                Current NPS is <strong>{nps:.1f}</strong> with <strong>{detractor_pct:.1f}%</strong> detractors.
                Converting <strong>{passives}</strong> passives to promoters is critical to driving positive NPS.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        best_loc = (
            loc_data.iloc[0]["Location"] if len(loc_data) > 0 else "Wuse"
        )
        best_aware = (
            loc_data.iloc[0]["Awareness"] if len(loc_data) > 0 else 87.5
        )
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">03</div>
            <div class="insight-title">Top Location</div>
            <div class="insight-desc">
                <strong>{best_loc}</strong> leads with <strong>{best_aware:.1f}%</strong> awareness —
                leverage its referral and marketing model across Abuja.
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
            <div class="insight-title">Impression Score</div>
            <div class="insight-desc">
                Average impression score is <strong>{avg_rating:.2f}/5</strong> —
                high service perception provides a base for customer growth.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== NAVIGATION =====
    st.markdown("---")

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

    with nav_col1:
        if st.button("🏠 Cover", use_container_width=True, key="ov_to_cover"):
            st.switch_page("app.py")

    with nav_col2:
        st.button(
            "📈 Overview",
            use_container_width=True,
            key="ov_active",
            disabled=True,
        )

    with nav_col3:
        if st.button("🏷️ Brand Health", use_container_width=True, key="ov_to_brand"):
            st.switch_page("pages/2_Brand_Health.py")

    with nav_col4:
        if st.button("👥 Insights", use_container_width=True, key="ov_to_insights"):
            st.switch_page("pages/3_Customer_Insights.py")

    with nav_col5:
        if st.button("⚔️ Competitive", use_container_width=True, key="ov_to_comp"):
            st.switch_page("pages/4_Competitive_Intelligence.py")

    with nav_col6:
        if st.button("💡 Strategic", use_container_width=True, key="ov_to_strategic"):
            st.switch_page("pages/5_Strategic_Analytics.py")


if __name__ == "__main__":
    show()
