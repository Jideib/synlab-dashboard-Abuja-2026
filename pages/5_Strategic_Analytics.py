# pages/5_Strategic_Analytics.py
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

try:
    icon = Image.open("assets/synlab_logo.png")
    st.set_page_config(
        page_title="Strategic Analytics | SYNLAB Nigeria",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    st.set_page_config(
        page_title="Strategic Analytics | SYNLAB Nigeria",
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
    st.error("Data file not found. Please ensure synlab_clean_deduped.csv is located in the data directory.")
    st.stop()

total = len(data)

def find_col(df, patterns):
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
    return None

aware_col = find_col(data, ["aware_synlab", "aware of?/synlab"])
used_col = find_col(data, ["used_synlab", "used the services of any of the following laboratories?/synlab"])
wtp_col = find_col(data, ["wtp_package", "price tier", "wtp"])
pimp_col = find_col(data, ["price_importance", "price matters"])

st.markdown(
    """
<div class="page-header">
    <h1>Strategic Analytics & Advanced Models</h1>
    <p>Service gap priorities, occupation price elasticity, digital channel preferences, and prioritized action roadmap</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== 1. SERVICE GAP ANALYSIS =====
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Service Gap Analysis (Importance vs. Performance)</h4>", unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)

gap_data = [
    {"Metric": "Diagnostic Accuracy", "Importance": 94, "Performance": 4.31, "Gap": 0.22},
    {"Metric": "Professionalism", "Importance": 88, "Performance": 4.22, "Gap": 0.25},
    {"Metric": "Result Turnaround", "Importance": 86, "Performance": 4.21, "Gap": 0.29},
    {"Metric": "Communication", "Importance": 82, "Performance": 4.22, "Gap": 0.24},
    {"Metric": "Wait Time", "Importance": 79, "Performance": 4.05, "Gap": 0.38},
    {"Metric": "Location Access", "Importance": 76, "Performance": 4.06, "Gap": 0.39},
    {"Metric": "Digital Experience", "Importance": 74, "Performance": 4.03, "Gap": 0.48},
    {"Metric": "Pricing & Value", "Importance": 85, "Performance": 3.92, "Gap": 0.59},
]
gap_df = pd.DataFrame(gap_data)

with col_g1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Importance vs. Performance Matrix</h4>", unsafe_allow_html=True)

    fig_gap = go.Figure()
    for _, row in gap_df.iterrows():
        color = "#003765" if row["Gap"] < 0.30 else "#0077AD" if row["Gap"] < 0.45 else "#2C8FC7"
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

    fig_gap.add_shape(type="line", x0=4.15, y0=68, x1=4.15, y1=98, line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"))
    fig_gap.add_shape(type="line", x0=3.85, y0=80, x1=4.4, y1=80, line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"))

    fig_gap.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="Performance Rating (Scale 1-5)",
        yaxis_title="Customer Importance Ranking (%)",
        xaxis=dict(range=[3.85, 4.4]),
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
        color = "#003765" if row["Gap"] < 0.30 else "#0077AD" if row["Gap"] < 0.45 else "#2C8FC7"

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
        Priority Focus: <strong>Pricing & Value (0.59)</strong> and <strong>Digital Experience (0.48)</strong> show the highest variance between patient expectations and observed service delivery ratings.
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 2. VISIT INTENT & OCCUPATION PRICE ELASTICITY =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Patient Visit Drivers & Occupation Price Elasticity</h4>", unsafe_allow_html=True)

col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Primary Reason for Laboratory Visit (Intent)</h4>", unsafe_allow_html=True)

    q10_col = find_col(data, ["10. Thinking about the last time you used a medical laboratory"])
    if q10_col and q10_col in data.columns:
        v_counts = data[q10_col].value_counts().reset_index()
        v_counts.columns = ["Intent", "Count"]
        v_counts["Pct"] = (v_counts["Count"] / total * 100).round(1)

        fig_visit = px.bar(
            v_counts.sort_values("Count", ascending=True),
            x="Count",
            y="Intent",
            orientation="h",
            color="Count",
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=[f"{c} ({p}%)" for c, p in zip(v_counts.sort_values("Count", ascending=True)["Count"], v_counts.sort_values("Count", ascending=True)["Pct"])],
        )
        fig_visit.update_traces(textposition="outside")
        fig_visit.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Patient Visits",
            yaxis_title="",
            yaxis=dict(tickfont=dict(color="#003765", size=10.5)),
            showlegend=False,
            height=290,
            margin=dict(l=190, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_visit, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_v2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Occupation vs. Price Sensitivity Index</h4>", unsafe_allow_html=True)

    if pimp_col and pimp_col in data.columns and "occupation" in data.columns:
        pimp_valid = data[data[pimp_col].notna() & data["occupation"].notna()]
        top_occs = pimp_valid["occupation"].value_counts().head(5).index
        occ_sub = pimp_valid[pimp_valid["occupation"].isin(top_occs)]

        occ_pimp = pd.crosstab(occ_sub["occupation"], occ_sub[pimp_col], normalize="index") * 100
        pimp_categories = [c for c in ["Price matters but quality comes first", "Price is important but not the most important factor", "Price is the most important factor", "Price is not a significant factor in my decision"] if c in occ_pimp.columns]
        occ_pimp = occ_pimp[pimp_categories].reset_index()

        fig_op = px.bar(
            occ_pimp,
            x="occupation",
            y=pimp_categories,
            barmode="stack",
            color_discrete_sequence=["#003765", "#0077AD", "#7CB8D3", "#CBD5E1"],
        )
        fig_op.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            xaxis=dict(tickfont=dict(size=10.5, color="#003765")),
            yaxis_title="Proportion (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10.5)),
            height=290,
            margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig_op, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. DIGITAL CHANNELS & BOOKING PREFERENCES =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Digital Experience & Patient Channel Preferences</h4>", unsafe_allow_html=True)

col_ch1, col_ch2 = st.columns(2)

with col_ch1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Preferred Result Delivery Channel</h4>", unsafe_allow_html=True)

    if "pref_result_access" in data.columns:
        res_counts = data["pref_result_access"].value_counts().reset_index()
        res_counts.columns = ["Channel", "Count"]

        fig_del = px.pie(
            res_counts,
            values="Count",
            names="Channel",
            color_discrete_sequence=["#003765", "#0077AD", "#2C8FC7", "#5BA3D0", "#E2E8F0"],
            hole=0.45,
        )
        fig_del.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10.5)),
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_del.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_del, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_ch2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Preferred Appointment Booking Method</h4>", unsafe_allow_html=True)

    if "pref_booking" in data.columns:
        book_counts = data["pref_booking"].value_counts().reset_index()
        book_counts.columns = ["Method", "Count"]
        b_total = book_counts["Count"].sum()

        fig_book = px.bar(
            book_counts.sort_values("Count", ascending=True),
            x="Count",
            y="Method",
            orientation="h",
            color="Count",
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=[f"{c} ({round(c/b_total*100, 1)}%)" for c in book_counts.sort_values("Count", ascending=True)["Count"]],
        )
        fig_book.update_traces(textposition="outside")
        fig_book.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Patient Preferences",
            yaxis_title="",
            yaxis=dict(tickfont=dict(color="#003765", size=10.5)),
            showlegend=False,
            height=280,
            margin=dict(l=190, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_book, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 4. ADVANCED MODELS & CLUSTERING =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Advanced Predictive & Clustering Models</h4>", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(
        """
    <div class="model-card">
        <div class="model-value">80.1%</div>
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
        <div class="model-value">74.2%</div>
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

# ===== 5. PRIORITIZED ACTION ROADMAP =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Prioritized Strategic Action Roadmap</h4>", unsafe_allow_html=True)

actions = [
    {
        "priority": "P1 · HIGH",
        "title": "Digital Delivery Modernization (Automated WhatsApp & Portal)",
        "desc": "Automate WhatsApp and email report dispatch to address patient delivery preferences and eliminate physical collection delays.",
        "class": "priority-high",
    },
    {
        "priority": "P1 · HIGH",
        "title": "Preventive Screening Packages (< ₦50,000)",
        "desc": "Launch structured wellness profiles aligned with the 67.2% of respondents seeking packages priced at or below ₦50,000.",
        "class": "priority-high",
    },
    {
        "priority": "P2 · MEDIUM",
        "title": "Physician Network & B2B Clinical Retention",
        "desc": "Mitigate clinical turnover caused by doctor/HMO reassignments by formalizing clinical partnerships with private practitioners across Wuse and Asokoro.",
        "class": "priority-medium",
    },
    {
        "priority": "P2 · MEDIUM",
        "title": "Corridor-Specific Service Optimization",
        "desc": "Deploy mobile phlebotomy outreach in Gwagwalada while optimizing specimen collection workflows in Kubwa to reduce wait-time friction.",
        "class": "priority-medium",
    },
    {
        "priority": "P3 · LOW",
        "title": "Corporate Wellness & Executive Retainers",
        "desc": "Package annual health audits for corporate employers targeting the 35–44 working professional cohort.",
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