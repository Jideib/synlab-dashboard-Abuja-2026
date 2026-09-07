# pages/4_Competitive_Intelligence.py
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

try:
    icon = Image.open("assets/synlab_logo.png")
    st.set_page_config(
        page_title="Competitive Intelligence | SYNLAB Nigeria",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    st.set_page_config(
        page_title="Competitive Intelligence | SYNLAB Nigeria",
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

    .threat-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid var(--synlab-border);
        border-top: 4px solid var(--synlab-midnight);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .threat-card .comp-tag { font-size: 11px; color: var(--synlab-cerulean); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .threat-card .comp-name { font-weight: 700; color: var(--synlab-midnight); font-size: 17px; margin-top: 2px; }
    .threat-card .comp-score { font-weight: 800; font-size: 24px; color: var(--synlab-cerulean); margin: 4px 0; }
    .threat-card .comp-stats { font-size: 12px; color: var(--synlab-slate); margin-bottom: 8px; font-weight: 600; }
    .threat-card .comp-desc { font-size: 12px; color: #475569; line-height: 1.55; }

    .threat-item-mini {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        border-bottom: 1px solid #F1F5F9;
    }
    .threat-item-mini .threat-name { font-weight: 600; color: var(--synlab-midnight); font-size: 13px; }
    .threat-item-mini .threat-score { font-weight: 700; font-size: 12px; }

    .swot-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 12px;
    }
    .swot-card {
        border-radius: 10px;
        padding: 20px 24px;
        min-height: 200px;
        display: flex;
        flex-direction: column;
    }
    .swot-card h4 {
        margin: 0 0 12px 0;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .swot-card ul {
        margin: 0;
        padding-left: 18px;
        font-size: 13px;
        line-height: 1.6;
    }
    .swot-card li { margin-bottom: 6px; }

    .swot-strengths { background: #003765; color: white; }
    .swot-weaknesses { background: #E8F4F8; color: #003765; border: 1px solid #7CB8D3; }
    .swot-opportunities { background: #0077AD; color: white; }
    .swot-threats { background: #F1F5F9; color: #002647; border: 1px solid #CBD5E1; }

    @media (max-width: 768px) {
        .main > div { padding: 0 16px !important; }
        .page-header { padding: 16px 20px; }
        .page-header h1 { font-size: 20px; }
        .swot-grid { grid-template-columns: 1fr; }
    }
</style>
""",
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    paths = [
        "data/synlab_clean.csv",
        "synlab_clean.csv",
        "data/SYNLAB_Surveys_Cleaned_498.csv",
        "SYNLAB_Surveys_Cleaned_498.csv",
        "data/synlab_clean_standardized.csv",
        "synlab_clean_standardized.csv",
        "../data/synlab_clean.csv",
        "../synlab_clean.csv",
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
    st.error("Data file not found. Please ensure synlab_clean.csv is located in the data directory.")
    st.stop()

total = len(data)

def find_col(df, patterns):
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
    return None

q14_col = find_col(data, ["14. Which medical laboratory would you say you prefer", "prefer most"])

competitors = [
    {"id": "synlab", "name": "SYNLAB Nigeria", "aware_col": "aware_synlab", "used_col": "used_synlab"},
    {"id": "lifebridge", "name": "Lifebridge Medical", "aware_col": "aware_lifebridge", "used_col": "used_lifebridge"},
    {"id": "eclinic", "name": "E-Clinic Diagnostics", "aware_col": "aware_eclinic", "used_col": "used_eclinic"},
    {"id": "firmcare", "name": "Firmcare Diagnostics", "aware_col": "aware_firmcare", "used_col": "used_firmcare"},
    {"id": "mecure", "name": "Mecure Healthcare", "aware_col": "aware_mecure", "used_col": "used_mecure"},
    {"id": "echolab", "name": "Echo Lab", "aware_col": "aware_echolab", "used_col": "used_echolab"},
    {"id": "lab360", "name": "LAB360", "aware_col": "aware_lab360", "used_col": "used_lab360"},
    {"id": "clinix", "name": "Clinix Diagnostics", "aware_col": "aware_clinix", "used_col": "used_clinix"},
    {"id": "afriglobal", "name": "Afriglobal Medicare", "aware_col": "aware_afriglobal", "used_col": "used_afriglobal"},
    {"id": "apin", "name": "APIN Medical Lab", "aware_col": "aware_apin", "used_col": "used_apin"},
    {"id": "clina", "name": "Clina Lancet", "aware_col": "aware_clina_lancet", "used_col": "used_clina_lancet"},
    {"id": "amce", "name": "AMCE", "aware_col": "aware_amce", "used_col": "used_amce"},
]

comp_data = []
for comp in competitors:
    a_col = comp["aware_col"]
    u_col = comp["used_col"]

    aware_count = int(data[a_col].sum()) if a_col in data.columns else 0
    used_count = int(data[u_col].sum()) if u_col in data.columns else 0

    aware_pct = round(aware_count / total * 100, 1) if total > 0 else 0.0
    used_pct = round(used_count / total * 100, 1) if total > 0 else 0.0
    conversion = round(used_count / aware_count * 100, 1) if aware_count > 0 else 0.0
    threat = round((aware_pct * 0.4) + (used_pct * 0.6), 1)

    comp_data.append({
        "id": comp["id"],
        "name": comp["name"],
        "awareness": aware_pct,
        "aware_count": aware_count,
        "usage": used_pct,
        "used_count": used_count,
        "conversion": conversion,
        "threat": threat,
        "is_synlab": comp["id"] == "synlab",
    })

comp_df = pd.DataFrame(comp_data)
comp_df_sorted = comp_df.sort_values("usage", ascending=False)

st.markdown(
    """
<div class="page-header">
    <h1>Competitive Intelligence</h1>
    <p>Market usage share, brand preference share, positioning matrix, competitor switching inflow, and SWOT strategy</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== 1. MARKET USAGE SHARE =====
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Market Usage Share (%)</h4>", unsafe_allow_html=True)

col_m1, col_m2 = st.columns([2, 1])

with col_m1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    fig_usage = px.bar(
        comp_df_sorted,
        x="name",
        y="usage",
        title="Laboratory Usage Rates in Abuja Metropolitan Market (%)",
        color="usage",
        color_continuous_scale=["#5BA3D0", "#003765"],
        text=[f"{u:.1f}% ({c})" for u, c in zip(comp_df_sorted["usage"], comp_df_sorted["used_count"])],
    )
    fig_usage.update_traces(textposition="outside")
    fig_usage.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="",
        yaxis_title="Usage Rate (%)",
        yaxis=dict(range=[0, 50]),
        showlegend=False,
        height=360,
        margin=dict(l=10, r=20, t=40, b=50),
    )
    st.plotly_chart(fig_usage, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_m2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Market Leadership Position</h4>", unsafe_allow_html=True)

    leader = comp_df_sorted.iloc[0]
    runner_up = comp_df_sorted.iloc[1]
    lead_margin = round(leader["usage"] - runner_up["usage"], 1)

    st.markdown(
        f"""
    <div style="text-align: center; padding: 16px 0;">
        <div style="font-size: 18px; font-weight: 700; color: #003765;">{leader['name']}</div>
        <div style="font-size: 38px; font-weight: 800; color: #0077AD; margin: 4px 0;">{leader['usage']}%</div>
        <div style="font-size: 12px; color: #64748B; text-transform: uppercase; font-weight: 600;">Metropolitan Market Share</div>
        <div style="margin-top: 18px; padding: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; text-align: left;">
            <div style="font-size: 13px; color: #003765; font-weight: 700;">Leadership Advantage: +{lead_margin}%</div>
            <div style="font-size: 12px; color: #475569; margin-top: 4px; line-height: 1.5;">
                SYNLAB commands more than 3x the market usage of its nearest competitor, <strong>{runner_up['name']}</strong> ({runner_up['usage']}%).
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 2. BRAND PREFERENCE SHARE (QUESTION 14) =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Brand Preference Share (First-Choice Laboratory)</h4>", unsafe_allow_html=True)

col_pr1, col_pr2 = st.columns([1.6, 1.0])

def parse_preferred_lab(text):
    if pd.isna(text):
        return None
    s = str(text).lower()
    if "synlab" in s:
        return "SYNLAB Nigeria"
    elif "echo" in s or "eco" in s:
        return "Echo Lab"
    elif "lifebridge" in s or "life bridge" in s:
        return "Lifebridge Medical"
    elif "hospital" in s or "general" in s:
        return "Hospital-based Lab"
    elif "apin" in s:
        return "APIN Medical Lab"
    elif "mecure" in s:
        return "Mecure Healthcare"
    elif "eclinic" in s or "e-clinic" in s:
        return "E-Clinic Diagnostics"
    elif "clinix" in s:
        return "Clinix Diagnostics"
    else:
        return "Other / Alternative"

with col_pr1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if q14_col and q14_col in data.columns:
        pref_series = data[q14_col].apply(parse_preferred_lab).dropna()
        pref_counts = pref_series.value_counts().reset_index()
        pref_counts.columns = ["Laboratory", "Count"]
        pref_total_n = pref_counts["Count"].sum()
        pref_counts["Pct"] = (pref_counts["Count"] / pref_total_n * 100).round(1)

        fig_pref = px.bar(
            pref_counts.sort_values("Count", ascending=True),
            x="Count",
            y="Laboratory",
            orientation="h",
            text=[f"{c} ({p}%)" for c, p in zip(pref_counts.sort_values("Count", ascending=True)["Count"], pref_counts.sort_values("Count", ascending=True)["Pct"])],
            color="Count",
            color_continuous_scale=["#5BA3D0", "#003765"],
        )
        fig_pref.update_traces(textposition="outside")
        fig_pref.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="First-Choice Mentions",
            yaxis_title="",
            showlegend=False,
            height=300,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_pref, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pr2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Choice Rationale</h4>", unsafe_allow_html=True)
    st.markdown(
        """
    <div style="font-size: 12px; color: #334155; line-height: 1.7; padding: 6px 0;">
        <strong>SYNLAB Allegiance (45.6%):</strong> Cited repeatedly for <em>"highest diagnostic accuracy"</em>, <em>"reliable health reports"</em>, and <em>"professional environment"</em>.<br><br>
        <strong>Hospital Laboratories (11.8%):</strong> Retained by patients whose physicians process samples in-house during clinical consultations.<br><br>
        <strong>Echo Lab (7.4%):</strong> Driven by ultrasound and imaging combination convenience.
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. POSITIONING MATRIX & CONVERSION =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Competitive Positioning Matrix</h4>", unsafe_allow_html=True)

col_p1, col_p2 = st.columns([1.3, 1.0])

with col_p1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Awareness vs. Usage Matrix</h4>", unsafe_allow_html=True)

    fig_matrix = go.Figure()

    label_offsets = {
        "SYNLAB Nigeria": {"ax": 0, "ay": -35},
        "Lifebridge Medical": {"ax": 0, "ay": -45},
        "E-Clinic Diagnostics": {"ax": 65, "ay": -15},
        "Firmcare Diagnostics": {"ax": -70, "ay": -25},
        "Mecure Healthcare": {"ax": 65, "ay": -25},
        "Echo Lab": {"ax": -65, "ay": -10},
        "Clinix Diagnostics": {"ax": 65, "ay": 20},
        "LAB360": {"ax": -60, "ay": 20},
        "Afriglobal Medicare": {"ax": -65, "ay": -25},
        "APIN Medical Lab": {"ax": -55, "ay": 35},
        "Clina Lancet": {"ax": 55, "ay": 35},
        "AMCE": {"ax": 0, "ay": 40},
    }

    for _, row in comp_df.iterrows():
        color = "#003765" if row["is_synlab"] else "#0077AD"
        size = 18 if row["is_synlab"] else 11

        fig_matrix.add_trace(
            go.Scatter(
                x=[row["awareness"]],
                y=[row["usage"]],
                mode="markers",
                marker=dict(size=size, color=color, line=dict(width=1.5, color="white")),
                name=row["name"],
                hovertemplate=f"<b>{row['name']}</b><br>Awareness: {row['awareness']}%<br>Usage: {row['usage']}%<extra></extra>",
            )
        )

        offset = label_offsets.get(row["name"], {"ax": 20, "ay": -20})
        fig_matrix.add_annotation(
            x=row["awareness"],
            y=row["usage"],
            text=f"<b>{row['name']}</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=0.8,
            arrowwidth=1.0,
            arrowcolor="#64748B",
            ax=offset["ax"],
            ay=offset["ay"],
            font=dict(size=10, color="#003765" if row["is_synlab"] else "#334155"),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(0, 55, 101, 0.2)",
            borderwidth=1,
            borderpad=2,
        )

    avg_aware = comp_df["awareness"].mean()
    avg_usage = comp_df["usage"].mean()

    fig_matrix.add_shape(type="line", x0=avg_aware, y0=0, x1=avg_aware, y1=50, line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"))
    fig_matrix.add_shape(type="line", x0=0, y0=avg_usage, x1=60, y1=avg_usage, line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"))

    fig_matrix.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="Brand Awareness (%)",
        yaxis_title="Market Usage (%)",
        xaxis=dict(range=[-2, 60]),
        yaxis=dict(range=[-2, 48]),
        showlegend=False,
        height=380,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_matrix, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_p2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 8px 0;'>Awareness-to-Usage Conversion (%)</h4>", unsafe_allow_html=True)

    fig_conv = px.bar(
        comp_df_sorted,
        x="name",
        y="conversion",
        color="conversion",
        color_continuous_scale=["#5BA3D0", "#003765"],
        text=[f"{c:.1f}%" for c in comp_df_sorted["conversion"]],
    )
    fig_conv.update_traces(textposition="outside")
    fig_conv.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="",
        yaxis_title="Conversion Rate (%)",
        yaxis=dict(range=[0, 120]),
        showlegend=False,
        height=180,
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig_conv, use_container_width=True)

    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #003765; margin: 12px 0 6px 0;'>Competitor Threat Score Ranking</div>", unsafe_allow_html=True)
    threat_df = comp_df_sorted[comp_df_sorted["is_synlab"] == False].sort_values("threat", ascending=False).head(6)

    for i, (_, r) in enumerate(threat_df.iterrows()):
        st.markdown(
            f"""
        <div class="threat-item-mini">
            <span class="threat-name">{i+1}. {r['name']}</span>
            <span class="threat-score" style="color: #0077AD;">Score: {r['threat']:.1f} ({r['usage']}% usage)</span>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 4. COMPETITIVE ADVANTAGE =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Competitive Advantage vs. Alternative Laboratories</h4>", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)

label_map = {
    "cx_professionalism": "Staff Professionalism",
    "cx_result_speed": "Result Turnaround Speed",
    "cx_accuracy": "Diagnostic Accuracy & Precision",
    "cx_access": "Location Access & Convenience",
    "cx_range": "Test Menu Comprehensive Range",
    "cx_digital": "Digital Portal & Online Experience",
    "cx_value": "Pricing & Value for Money",
}

comp_adv_list = []
for col_key, title in label_map.items():
    if col_key in data.columns:
        valid_comp = data[col_key].dropna()
        n_valid = len(valid_comp)
        better_cnt = ((valid_comp == "Better") | (valid_comp == "Much better")).sum()
        pct = round(better_cnt / n_valid * 100, 1)
        comp_adv_list.append({"Parameter": title, "Superiority_Pct": pct, "Valid_N": n_valid})

comp_adv_df = pd.DataFrame(comp_adv_list).sort_values("Superiority_Pct", ascending=True)

col_a1, col_a2 = st.columns([1.6, 1.0])

with col_a1:
    fig_adv = px.bar(
        comp_adv_df,
        x="Superiority_Pct",
        y="Parameter",
        orientation="h",
        text=[f"{p:.1f}% Better" for p in comp_adv_df["Superiority_Pct"]],
        color="Superiority_Pct",
        color_continuous_scale=["#5BA3D0", "#003765"],
    )
    fig_adv.update_traces(textposition="outside")
    fig_adv.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="Percentage Rated Better or Much Better than Alternative Labs (%)",
        yaxis_title="",
        xaxis=dict(range=[40, 95]),
        showlegend=False,
        height=320,
        margin=dict(l=10, r=40, t=10, b=10),
    )
    st.plotly_chart(fig_adv, use_container_width=True)

with col_a2:
    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #003765; margin-bottom: 8px;'>Competitive Moat Analysis</div>", unsafe_allow_html=True)
    st.markdown(
        """
    <div style="padding: 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; font-size: 12px; color: #334155; line-height: 1.7;">
        <strong>Clinical Benchmark:</strong> Staff professionalism (81.4%) and turnaround speed (79.4%) represent SYNLAB's strongest competitive moats.<br><br>
        <strong>Diagnostic Precision:</strong> 73.8% of patients consider SYNLAB superior in accuracy.<br><br>
        <strong>Defensive Focus:</strong> Pricing & Value (59.8%) is the only parameter below 65%, highlighting out-of-pocket sensitivity against local clinics.
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ===== 5. COMPETITOR SWITCHING INFLOW / WIN-RATE MATRIX =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown(
    """<h4 style="color: #003765; margin: 0 0 12px 0;">Laboratory Switching Dynamics & Competitor Inflow</h4>""",
    unsafe_allow_html=True,
)

col_sw1, col_sw2 = st.columns([1.5, 1.0])

with col_sw1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(
        """<h4 style="color: #003765; margin: 0 0 6px 0;">Where Patients are Leaving Other Labs</h4>""",
        unsafe_allow_html=True,
    )

    inflow_df = pd.DataFrame({
        "Driver": [
            "Doctor / HMO Reassignment",
            "Pricing / High Cost at Previous Lab",
            "Inconvenient Location / Distance",
            "Inaccurate Results / Quality Deficit",
            "Poor Customer Service / Long Wait",
        ],
        "Switch_Volume": [102, 78, 65, 54, 43],
        "Opportunity_Rate": [22.2, 17.0, 14.1, 11.7, 9.3],
    }).sort_values("Switch_Volume", ascending=True)

    fig_inflow = px.bar(
        inflow_df,
        x="Switch_Volume",
        y="Driver",
        orientation="h",
        color="Switch_Volume",
        color_continuous_scale=["#5BA3D0", "#003765"],
        text=[f"{v} ({p}%)" for v, p in zip(inflow_df["Switch_Volume"], inflow_df["Opportunity_Rate"])],
    )
    fig_inflow.update_traces(
        textposition="outside",
        textfont=dict(color="#003765", size=11),
        cliponaxis=False,
    )
    fig_inflow.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="Patients Citing Factor",
        yaxis_title="",
        yaxis=dict(tickfont=dict(color="#003765", size=11)),
        showlegend=False,
        height=280,
        margin=dict(l=190, r=50, t=10, b=10),
    )
    st.plotly_chart(fig_inflow, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_sw2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(
        """<h4 style="color: #003765; margin: 0 0 6px 0;">Patient Acquisition Win-Rate</h4>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div style="padding: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; font-size: 12px; color: #334155; line-height: 1.7;">
        <strong>Clinical Reassignment (22.2%):</strong> Primary driver of market movement. Doctors migrating away from standalone clinics direct patients to SYNLAB when hospital panels fail.<br><br>
        <strong>Quality Friction (11.7%):</strong> 54 patients left rivals due to inaccurate results, creating an acquisition wedge for SYNLAB's international accreditation.
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 6. PRIMARY THREATS & COUNTER-STRATEGIES =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Primary Competitive Threats & Counter-Strategies</h4>", unsafe_allow_html=True)

col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    st.markdown(
        """
    <div class="threat-card">
        <div>
            <div class="comp-tag">Threat #1 · Doctor Referrals</div>
            <div class="comp-name">Lifebridge Medical</div>
            <div class="comp-score">Threat Score: 11.6</div>
            <div class="comp-stats">12.0% Usage · 11.0% Awareness · 109.1% Conversion</div>
            <div class="comp-desc">
                Commands the second highest usage share in Abuja (12.0%). Demonstrates high conversion efficiency driven by established doctor referral loops across private hospitals.
            </div>
        </div>
        <div style="margin-top: 14px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 11px; color: #003765;">
            <strong>Counter-Strategy:</strong> Deepen physician relations, corporate HMO retention, and B2B clinical partnerships in central Abuja corridors.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_t2:
    st.markdown(
        """
    <div class="threat-card">
        <div>
            <div class="comp-tag">Threat #2 · Digital Convenience</div>
            <div class="comp-name">E-Clinic Diagnostics</div>
            <div class="comp-score">Threat Score: 11.5</div>
            <div class="comp-stats">9.4% Usage · 14.7% Awareness · 64.4% Conversion</div>
            <div class="comp-desc">
                Commands the highest brand awareness among all non-SYNLAB competitors (14.7%). Streamlined online booking and rapid portal results appeal to tech-enabled patients.
            </div>
        </div>
        <div style="margin-top: 14px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 11px; color: #003765;">
            <strong>Counter-Strategy:</strong> Upgrade SYNLAB's digital patient portal, enable automated WhatsApp delivery, and promote mobile scheduling.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_t3:
    st.markdown(
        """
    <div class="threat-card">
        <div>
            <div class="comp-tag">Threat #3 · Screening Packages</div>
            <div class="comp-name">Mecure Healthcare</div>
            <div class="comp-score">Threat Score: 7.8</div>
            <div class="comp-stats">6.0% Usage · 10.6% Awareness · 56.6% Conversion</div>
            <div class="comp-desc">
                Competes directly on bundled wellness packages and routine checkups, drawing away price-sensitive out-of-pocket individuals.
            </div>
        </div>
        <div style="margin-top: 14px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 11px; color: #003765;">
            <strong>Counter-Strategy:</strong> Introduce modular wellness packages within the ₦20,000–₦50,000 sweet spot while emphasizing test accuracy.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ===== 7. STRATEGIC SWOT MATRIX =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Strategic SWOT Matrix</h4>", unsafe_allow_html=True)

st.markdown(
    """
<div class="swot-grid">
    <div class="swot-card swot-strengths">
        <h4>Strengths</h4>
        <ul>
            <li>Dominant metropolitan usage leader at 42.0% (209 active patients)</li>
            <li>Highest market awareness across Abuja (54.0%)</li>
            <li>Strong awareness-to-usage conversion rate (77.7%)</li>
            <li>Benchmark clinical reputation: 81.4% rate staff professionalism superior</li>
        </ul>
    </div>
    <div class="swot-card swot-weaknesses">
        <h4>Weaknesses</h4>
        <ul>
            <li>Price sensitivity among self-paying patients (59.8% rate value superior)</li>
            <li>Digital portal adoption lags pure-play tech diagnostic centers</li>
            <li>Sample collection wait times during peak morning hours</li>
            <li>Lower spontaneous recall in peripheral suburban corridors</li>
        </ul>
    </div>
    <div class="swot-card swot-opportunities">
        <h4>Opportunities</h4>
        <ul>
            <li>60 conversion-ready aware prospects (12.0% awareness-usage gap)</li>
            <li>Modular wellness screening packages priced under ₦50,000</li>
            <li>Automated WhatsApp and mobile results delivery integration</li>
            <li>Targeted physician referral programs in Wuse, Gwarimpa, and Gwagwalada</li>
        </ul>
    </div>
    <div class="swot-card swot-threats">
        <h4>Threats</h4>
        <ul>
            <li>Lifebridge Medical leveraging deep doctor referral integration</li>
            <li>E-Clinic Diagnostics expanding market share through digital channels</li>
            <li>Mecure Healthcare offering aggressive pricing on routine tests</li>
            <li>HMO fee-schedule pressures impacting diagnostic reimbursement</li>
        </ul>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ===== NAVIGATION =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button("Cover", use_container_width=True, key="comp_to_cover"):
        st.switch_page("app.py")

with nav_col2:
    if st.button("Overview", use_container_width=True, key="comp_to_overview"):
        st.switch_page("pages/1_Executive_Overview.py")

with nav_col3:
    if st.button("Brand Health", use_container_width=True, key="comp_to_brand"):
        st.switch_page("pages/2_Brand_Health.py")

with nav_col4:
    if st.button("Customer Insights", use_container_width=True, key="comp_to_insights"):
        st.switch_page("pages/3_Customer_Insights.py")

with nav_col5:
    st.button("Competitive Intelligence", use_container_width=True, key="comp_active", disabled=True)

with nav_col6:
    if st.button("Strategic Analytics", use_container_width=True, key="comp_to_strategic"):
        st.switch_page("pages/5_Strategic_Analytics.py")