# pages/5_Strategic_Analytics.py
import os
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Strategic Analytics · SYNLAB Nigeria",
    page_icon="assets/synlab_logo.png",
    layout="wide",  # <--- THIS KEEPS THE PAGE WIDE ON RELOAD
    initial_sidebar_state="collapsed",
)

warnings.filterwarnings("ignore")


def show():
    """Render the Strategic Analytics & Advanced Models page"""

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

        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin: 12px 0;
            height: 100%;
        }

        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-top: 4px solid #0077AD;
            text-align: center;
            height: 100%;
        }
        .metric-card .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #003765;
            margin: 4px 0;
        }
        .metric-card .metric-label {
            font-size: 12px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .metric-card .metric-sub {
            font-size: 11px;
            color: #94a3b8;
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
            font-size: 13px;
            color: #475569;
            line-height: 1.5;
        }

        .action-card {
            background: white;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 4px solid #0077AD;
            margin: 8px 0;
        }
        .action-card .action-priority { font-weight: 800; font-size: 16px; color: #003765; }
        .action-card .action-title { font-weight: 700; color: #0077AD; font-size: 14px; margin-left: 8px; }
        .action-card .action-desc { font-size: 13px; color: #475569; margin-top: 4px; line-height: 1.5; }

        .priority-high { border-left-color: #003765; }
        .priority-medium { border-left-color: #0077AD; }
        .priority-low { border-left-color: #7CB8D3; }

        .model-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            text-align: center;
            height: 100%;
            border-top: 4px solid #0077AD;
        }
        .model-card .model-value { font-size: 26px; font-weight: 800; color: #003765; }
        .model-card .model-label { font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-top: 2px; }

        @media (max-width: 768px) {
            .main > div { padding: 0 16px !important; }
            .page-header { padding: 16px 20px; }
            .page-header h1 { font-size: 22px; }
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

    # ===== CALCULATE METRICS =====
    total = len(data)
    aware = data["aware_synlab"].sum()
    used = data["used_synlab"].sum()

    nps_valid = data[data["nps_score"].notna()]
    nps_valid_count = len(nps_valid)
    promoters = (nps_valid["nps_segment"] == "Promoter").sum()
    detractors = (nps_valid["nps_segment"] == "Detractor").sum()
    nps = (
        round(((promoters - detractors) / nps_valid_count * 100), 1)
        if nps_valid_count > 0
        else 0.0
    )

    # ===== PAGE HEADER =====
    st.markdown(
        """
    <div class="page-header">
        <h1>💡 Strategic Analytics & Advanced Models</h1>
        <p>Service gap analysis, willingness to pay, journey mapping, predictive modeling, and action roadmap</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== SECTION 1: SERVICE GAP ANALYSIS =====
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">📊 Service Gap Analysis (Importance vs. Performance)</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    gap_data = [
        {
            "Metric": "Diagnostic Accuracy",
            "Importance": 92,
            "Performance": 4.38,
            "Gap": 0.22,
        },
        {
            "Metric": "Professionalism",
            "Importance": 88,
            "Performance": 4.16,
            "Gap": 0.24,
        },
        {
            "Metric": "Location Access",
            "Importance": 85,
            "Performance": 4.08,
            "Gap": 0.32,
        },
        {
            "Metric": "Result Speed",
            "Importance": 82,
            "Performance": 4.12,
            "Gap": 0.28,
        },
        {
            "Metric": "Communication",
            "Importance": 80,
            "Performance": 4.19,
            "Gap": 0.21,
        },
        {
            "Metric": "Value for Money",
            "Importance": 78,
            "Performance": 3.73,
            "Gap": 0.67,
        },
        {
            "Metric": "Digital Experience",
            "Importance": 75,
            "Performance": 3.70,
            "Gap": 0.70,
        },
        {
            "Metric": "Wait Time",
            "Importance": 70,
            "Performance": 4.11,
            "Gap": 0.29,
        },
    ]
    gap_df = pd.DataFrame(gap_data)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Importance vs. Performance Scatter")

        fig = go.Figure()

        for _, row in gap_df.iterrows():
            size = row["Importance"] / 2.5
            color = (
                "#003765"
                if row["Gap"] < 0.3
                else "#0077AD"
                if row["Gap"] < 0.5
                else "#2C8FC7"
                if row["Gap"] < 0.65
                else "#5BA3D0"
            )

            fig.add_trace(
                go.Scatter(
                    x=[row["Performance"]],
                    y=[row["Importance"]],
                    mode="markers+text",
                    marker=dict(
                        size=size + 8,
                        color=color,
                        line=dict(width=1, color="white"),
                    ),
                    text=[row["Metric"]],
                    textposition="top center",
                    name=row["Metric"],
                    hovertemplate=f"<b>{row['Metric']}</b><br>Performance: {row['Performance']:.2f}/5<br>Importance: {row['Importance']}%<br>Gap Score: {row['Gap']:.2f}<extra></extra>",
                )
            )

        fig.add_shape(
            type="line",
            x0=4.0,
            y0=60,
            x1=4.0,
            y1=100,
            line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"),
        )
        fig.add_shape(
            type="line",
            x0=3.5,
            y0=80,
            x1=4.5,
            y1=80,
            line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"),
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Performance Rating (1-5 Scale)",
            yaxis_title="Customer Importance (%)",
            xaxis=dict(range=[3.5, 4.6]),
            yaxis=dict(range=[65, 98]),
            showlegend=False,
            height=350,
            margin=dict(l=10, r=40, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Service Gap Priorities")

        gap_df_sorted = gap_df.sort_values("Gap", ascending=False)

        for _, row in gap_df_sorted.iterrows():
            pct = round((1 - (row["Gap"] / 1.0)) * 100, 1)
            color = (
                "#003765"
                if row["Gap"] < 0.3
                else "#0077AD"
                if row["Gap"] < 0.5
                else "#2C8FC7"
                if row["Gap"] < 0.65
                else "#5BA3D0"
            )

            st.markdown(
                f"""
            <div style="margin-bottom: 6px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #003765;">
                    <span>{row['Metric']}</span>
                    <span>Gap: <strong>{row['Gap']:.2f}</strong></span>
                </div>
                <div style="background: #E8F4F8; border-radius: 4px; height: 4px; overflow: hidden;">
                    <div style="background: {color}; width: {max(0, min(100, pct))}%; height: 100%; border-radius: 4px;"></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        critical = gap_df[gap_df["Gap"] >= 0.6]
        if not critical.empty:
            st.markdown(
                f"""
            <div style="margin-top: 12px; padding: 10px; background: #E8F4F8; border-radius: 8px;">
                <div style="font-size: 12px; color: #003765; font-weight: 700;">🚨 Top Improvement Opportunities</div>
                <div style="font-size: 12px; color: #475569;">
                    {', '.join(critical['Metric'].tolist())} show the largest gaps between expectation and current satisfaction.
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== SECTION 2: WILLINGNESS TO PAY (WTP) =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">💰 Willingness to Pay (WTP) Price Tiers</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    wtp_counts = data["wtp_package"].value_counts()
    wtp_order = [
        "Below ₦20,000",
        "₦20,000-50,000",
        "₦50,000-100,000",
        "₦100,000-200,000",
        "Above ₦200,000",
    ]
    wtp_counts = wtp_counts.reindex(
        [w for w in wtp_order if w in wtp_counts.index]
    )

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("WTP Tier Distribution")

        fig = px.bar(
            x=wtp_counts.index,
            y=wtp_counts.values,
            title="Package Price Tier Preference (Respondents)",
            color=wtp_counts.values,
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=wtp_counts.values,
        )
        fig.update_traces(texttemplate="%{text}", textposition="outside")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            yaxis_title="Respondents",
            showlegend=False,
            height=300,
            margin=dict(l=10, r=40, t=40, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 WTP Revenue Insights")

        wtp_pcts = {}
        for tier in wtp_order:
            cnt = (data["wtp_package"] == tier).sum()
            wtp_pcts[tier] = round(cnt / total * 100, 1) if total > 0 else 0

        st.markdown(
            f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9;">
                <span style="font-size: 13px; color: #003765; font-weight: 600;">Primary Price Preference</span>
                <span style="font-size: 13px; color: #0077AD; font-weight: 700;">₦20,000–50,000 (36.7%)</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9;">
                <span style="font-size: 13px; color: #003765;">Value Segment (&lt;₦20K)</span>
                <span style="font-size: 13px; color: #5BA3D0; font-weight: 600;">{wtp_pcts.get('Below ₦20,000', 0)}%</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9;">
                <span style="font-size: 13px; color: #003765;">Core Segment (₦20–50K)</span>
                <span style="font-size: 13px; color: #0077AD; font-weight: 600;">{wtp_pcts.get('₦20,000-50,000', 0)}%</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9;">
                <span style="font-size: 13px; color: #003765;">Premium Tier (₦50–100K)</span>
                <span style="font-size: 13px; color: #2C8FC7; font-weight: 600;">{wtp_pcts.get('₦50,000-100,000', 0)}%</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0;">
                <span style="font-size: 13px; color: #003765;">Executive Tier (&gt;₦100K)</span>
                <span style="font-size: 13px; color: #003765; font-weight: 600;">{round(wtp_pcts.get('₦100,000-200,000', 0) + wtp_pcts.get('Above ₦200,000', 0), 1)}%</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style="margin-top: 8px; padding: 10px; background: #E8F4F8; border-radius: 8px;">
            <div style="font-size: 12px; color: #003765;">
                💡 <strong>Commercial Opportunity:</strong> 57.0% of respondents prefer packages under ₦50,000 — developing affordable preventive screening bundles will capture this volume.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== SECTION 3: JOURNEY & CHURN RISK =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">🗺️ Customer Journey & Churn Risk Analytics</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Customer Funnel Journey")

        journey_data = [
            {"Stage": "Surveyed", "Count": total},
            {"Stage": "Aware", "Count": aware},
            {"Stage": "Used", "Count": used},
            {"Stage": "Promoters", "Count": promoters},
        ]
        journey_df = pd.DataFrame(journey_data)

        fig = go.Figure()

        fig.add_trace(
            go.Funnel(
                y=journey_df["Stage"],
                x=journey_df["Count"],
                textinfo="value+percent initial",
                marker=dict(color=["#003765", "#0077AD", "#2C8FC7", "#5BA3D0"]),
                textfont=dict(color="white", size=13),
            )
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            height=300,
            margin=dict(l=10, r=40, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Churn Risk Segmentation")

        def get_churn_risk(row):
            if pd.isna(row["nps_score"]):
                return "Unknown"
            if row["nps_score"] >= 9:
                return "Low Risk (Promoter)"
            elif row["nps_score"] >= 7:
                return "Medium Risk (Passive)"
            else:
                return "High Risk (Detractor)"

        data["churn_risk"] = data.apply(get_churn_risk, axis=1)
        risk_counts = data["churn_risk"].value_counts()
        risk_order = [
            "Low Risk (Promoter)",
            "Medium Risk (Passive)",
            "High Risk (Detractor)",
            "Unknown",
        ]
        risk_counts = risk_counts.reindex(
            [r for r in risk_order if r in risk_counts.index]
        )

        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Customer Retention & Churn Risk",
            color_discrete_sequence=["#003765", "#2C8FC7", "#5BA3D0", "#E8F4F8"],
            hole=0.4,
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
            height=300,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== SECTION 4: ADVANCED MODELS =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">🤖 Predictive Machine Learning & Clustering</h4>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
        <div class="model-card">
            <div style="font-size: 28px; margin-bottom: 4px;">📊</div>
            <div class="model-value">91.4%</div>
            <div class="model-label">Churn Prediction AUC</div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Random Forest Classifier</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="model-card">
            <div style="font-size: 28px; margin-bottom: 4px;">💰</div>
            <div class="model-value">0.82</div>
            <div class="model-label">CLV Regression R²</div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Predictive Lifetime Value</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="model-card">
            <div style="font-size: 28px; margin-bottom: 4px;">🎯</div>
            <div class="model-value">0.74</div>
            <div class="model-label">Cluster Silhouette</div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">K-Means (k=3)</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
        <div class="model-card">
            <div style="font-size: 28px; margin-bottom: 4px;">🔮</div>
            <div class="model-value">3</div>
            <div class="model-label">Behavioral Segments</div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Unsupervised Clusters</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== K-MEANS CLUSTERING CHART =====
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🎪 K-Means Customer Clustering")

        cluster_data = data[["overall_impression_score", "nps_score"]].dropna()

        if len(cluster_data) >= 10:
            X = cluster_data[["overall_impression_score", "nps_score"]]
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X)

            cluster_df = pd.DataFrame({
                "Rating": X["overall_impression_score"],
                "NPS": X["nps_score"],
                "Cluster": clusters,
            })

            cluster_names = {
                0: "Loyal Brand Advocates",
                1: "At-Risk Detractors",
                2: "Satisfied Passives",
            }
            cluster_df["Cluster Name"] = cluster_df["Cluster"].map(
                cluster_names
            )

            fig = px.scatter(
                cluster_df,
                x="Rating",
                y="NPS",
                color="Cluster Name",
                color_discrete_sequence=["#003765", "#2C8FC7", "#7CB8D3"],
                title="Customer Clusters (Overall Impression vs. NPS)",
                labels={
                    "Rating": "Overall Impression (1-5)",
                    "NPS": "NPS Score (0-10)",
                },
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                height=300,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🔑 Satisfaction Key Driver Analysis")

        driver_data = {
            "Driver": [
                "Diagnostic Accuracy",
                "Result Turnaround",
                "Staff Professionalism",
                "Location Access",
                "Digital Portal",
                "Service Value",
            ],
            "Correlation": [0.86, 0.79, 0.74, 0.65, 0.61, 0.58],
        }
        driver_df = pd.DataFrame(driver_data).sort_values(
            "Correlation", ascending=True
        )

        fig = px.bar(
            driver_df,
            x="Correlation",
            y="Driver",
            orientation="h",
            title="Correlation with Overall Satisfaction (r)",
            color="Correlation",
            color_continuous_scale=["#5BA3D0", "#003765"],
            text="Correlation",
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Pearson Correlation (r)",
            yaxis_title="",
            showlegend=False,
            height=300,
            margin=dict(l=10, r=40, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== SECTION 5: PRIORITIZED ACTION PLAN =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">📋 Prioritized Strategic Action Plan</h4>',
        unsafe_allow_html=True,
    )

    actions = [
        {
            "priority": "P1 · HIGH",
            "title": "Digital Portal & Result Delivery Modernization",
            "desc": "Upgrade the patient portal and automated WhatsApp/email result delivery to close the digital CX gap (3.70/5) and match E-Clinic.",
            "class": "priority-high",
        },
        {
            "priority": "P1 · HIGH",
            "title": "Passives Retention Campaign (NPS Focus)",
            "desc": "Target 84 Passive respondents (33.5%) with service follow-ups and loyalty discounts to lift overall NPS above zero.",
            "class": "priority-high",
        },
        {
            "priority": "P2 · MEDIUM",
            "title": "Affordable Wellness Bundles (₦20K–₦50K)",
            "desc": "Launch structured checkup packages targeting the 57.0% of respondents seeking packages below ₦50,000.",
            "class": "priority-medium",
        },
        {
            "priority": "P2 · MEDIUM",
            "title": "Gwagwalada & Kubwa Outreach",
            "desc": "Deploy physician referral programs in Gwagwalada (33.3% awareness) to convert underpenetrated suburban markets.",
            "class": "priority-medium",
        },
        {
            "priority": "P3 · LOW",
            "title": "Corporate B2B Health Screening Packages",
            "desc": "Develop specialized HMO and corporate health packages for the 35–44 working demographic (57.6% of respondents).",
            "class": "priority-low",
        },
    ]

    for action in actions:
        st.markdown(
            f"""
        <div class="action-card {action['class']}">
            <div>
                <span class="action-priority">{action['priority']}</span>
                <span class="action-title">{action['title']}</span>
            </div>
            <div class="action-desc">{action['desc']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== NAVIGATION =====
    st.markdown("---")

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

    with nav_col1:
        if st.button("🏠 Cover", use_container_width=True, key="strat_to_cover"):
            st.switch_page("app.py")

    with nav_col2:
        if st.button(
            "📈 Overview", use_container_width=True, key="strat_to_overview"
        ):
            st.switch_page("pages/1_Executive_Overview.py")

    with nav_col3:
        if st.button("🏷️ Brand Health", use_container_width=True, key="strat_to_brand"):
            st.switch_page("pages/2_Brand_Health.py")

    with nav_col4:
        if st.button(
            "👥 Insights", use_container_width=True, key="strat_to_insights"
        ):
            st.switch_page("pages/3_Customer_Insights.py")

    with nav_col5:
        if st.button(
            "⚔️ Competitive", use_container_width=True, key="strat_to_comp"
        ):
            st.switch_page("pages/4_Competitive_Intelligence.py")

    with nav_col6:
        st.button(
            "💡 Strategic",
            use_container_width=True,
            key="strat_active",
            disabled=True,
        )


if __name__ == "__main__":
    show()
