# pages/2_Brand_Health.py
import os
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

try:
    icon = Image.open("assets/synlab_logo.png")
    st.set_page_config(
        page_title="Brand Health | SYNLAB Nigeria",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    st.set_page_config(
        page_title="Brand Health | SYNLAB Nigeria",
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

    .funnel-container {
        background: white;
        border-radius: 10px;
        padding: 24px;
        border: 1px solid var(--synlab-border);
        margin-bottom: 24px;
    }

    .funnel-row-horizontal {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        gap: 12px;
        padding: 8px 0;
    }

    .funnel-step-box {
        flex: 1;
        text-align: center;
        padding: 18px 14px;
        border-radius: 8px;
        color: white;
    }

    .funnel-step-box .count {
        font-size: 28px;
        font-weight: 800;
        line-height: 1.1;
    }
    .funnel-step-box .pct {
        font-size: 14px;
        font-weight: 700;
        margin-top: 4px;
        opacity: 0.95;
    }
    .funnel-step-box .label {
        font-size: 12px;
        opacity: 0.85;
        margin-top: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }

    .step-1 { background: #002647; }
    .step-2 { background: #003765; }
    .step-3 { background: #0077AD; }
    .step-4 { background: #2C8FC7; }

    .funnel-connector-arrow {
        font-size: 18px;
        color: #94A3B8;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        user-select: none;
    }

    .sentiment-quote {
        background: #F8FAFC;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 6px 0;
        border-left: 3px solid var(--synlab-cerulean);
        color: #334155;
        font-size: 13px;
        line-height: 1.5;
    }

    .tom-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #F1F5F9;
    }
    .tom-item .lab-name { font-size: 13px; }
    .tom-item .lab-pct { font-size: 12px; color: #64748B; font-weight: 600; }
    .tom-bar { height: 4px; border-radius: 2px; margin-top: 2px; margin-bottom: 4px; }

    .insight-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid var(--synlab-border);
        border-left: 4px solid var(--synlab-cerulean);
        height: 100%;
    }
    .insight-number {
        font-size: 18px;
        font-weight: 700;
        color: var(--synlab-cerulean);
    }
    .insight-title {
        font-weight: 700;
        color: var(--synlab-midnight);
        margin: 4px 0;
        font-size: 14px;
    }
    .insight-desc {
        font-size: 12px;
        color: #475569;
        line-height: 1.55;
    }

    .loc-segment-card {
        background: white;
        border-radius: 10px;
        padding: 16px 14px;
        border: 1px solid var(--synlab-border);
        border-top: 4px solid var(--synlab-cerulean);
        text-align: center;
        height: 100%;
    }

    .loc-stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        border-bottom: 1px solid #F1F5F9;
        font-size: 12px;
    }

    @media (max-width: 850px) {
        .funnel-row-horizontal { flex-direction: column; }
        .funnel-connector-arrow { display: none; }
        .funnel-step-box { width: 100%; }
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

def find_col(df, patterns):
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
    return None

aware_col = find_col(data, ["aware_synlab", "aware of?/synlab"])
used_col = find_col(data, ["used_synlab", "used the services of any of the following laboratories?/synlab"])
nps_col = find_col(data, ["nps_score", "recommend"])
tom_col = find_col(data, ["top_of_mind_lab", "first mind"])
q8_col = find_col(data, ["8. How did you first hear", "first hear about synlab"])

total = len(data)
data[aware_col] = pd.to_numeric(data[aware_col], errors="coerce").fillna(0)
data[used_col] = pd.to_numeric(data[used_col], errors="coerce").fillna(0)
aware = int(data[aware_col].sum())
used = int(data[used_col].sum())

# Overall CX NPS
cx_promoters = 59
cx_passives = 72
cx_detractors = 58
cx_valid_count = 189
cx_nps = 0.5

# Overall Brand Aware NPS
brand_promoters = 77
brand_passives = 84
brand_detractors = 89
brand_valid_count = 250
brand_nps = -4.8

if nps_col and nps_col in data.columns:
    data[nps_col] = pd.to_numeric(data[nps_col], errors="coerce")
    nps_sub = data[data[nps_col].notna()]
    if len(nps_sub) > 0:
        brand_valid_count = len(nps_sub)
        brand_promoters = int((nps_sub[nps_col] >= 9).sum())
        brand_passives = int(((nps_sub[nps_col] >= 7) & (nps_sub[nps_col] <= 8)).sum())
        brand_detractors = int((nps_sub[nps_col] <= 6).sum())
        brand_nps = round((brand_promoters - brand_detractors) / brand_valid_count * 100, 1)

    if used_col and used_col in data.columns:
        used_valid = data[(data[used_col] == 1) & (data[nps_col].notna())]
        if len(used_valid) > 0:
            cx_valid_count = len(used_valid)
            cx_promoters = int((used_valid[nps_col] >= 9).sum())
            cx_passives = int(((used_valid[nps_col] >= 7) & (used_valid[nps_col] <= 8)).sum())
            cx_detractors = int((used_valid[nps_col] <= 6).sum())
            cx_nps = round((cx_promoters - cx_detractors) / cx_valid_count * 100, 1)

def clean_tom(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    s_lower = s.lower()
    if "synlab" in s_lower:
        return "SYNLAB Nigeria"
    elif any(k in s_lower for k in ["echo", "eco"]):
        return "Echo Lab"
    elif "mecure" in s_lower or "me cure" in s_lower:
        return "Mecure Healthcare"
    elif "clina" in s_lower or "lancet" in s_lower:
        return "Clina Lancet"
    elif "afriglobal" in s_lower:
        return "Afriglobal Medicare"
    elif "eclinic" in s_lower or "e-clinic" in s_lower or "e clinic" in s_lower:
        return "E-Clinic Diagnostics"
    elif "amce" in s_lower:
        return "AMCE"
    elif "lifebridge" in s_lower:
        return "Lifebridge Medical"
    elif "firmcare" in s_lower:
        return "Firmcare Diagnostics"
    elif "apin" in s_lower:
        return "APIN Medical Lab"
    elif "lab360" in s_lower:
        return "LAB360"
    elif "health" in s_lower and "scan" in s_lower:
        return "Healthscan"
    elif "gaskiya" in s_lower:
        return "Gaskiya Medical Lab"
    elif "haske" in s_lower:
        return "Haske Lab"
    elif "clinix" in s_lower:
        return "Clinix Diagnostics"
    return s[:25]

st.markdown(
    """
<div class="page-header">
    <h1>Brand Health and Awareness</h1>
    <p>Conversion funnel, customer acquisition channels, regional sentiment segments, and touchpoint perception</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== 1. FUNNEL & CONVERSION DROPOFF =====
st.markdown('<div class="funnel-container">', unsafe_allow_html=True)
st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Brand Conversion Funnel</h4>""", unsafe_allow_html=True)

funnel_steps = [
    {"label": "Total Surveyed", "count": total, "pct": "100.0%", "step": "step-1"},
    {"label": "Brand Aware", "count": aware, "pct": f"{round(aware/total*100, 1)}%", "step": "step-2"},
    {"label": "Active Usage", "count": used, "pct": f"{round(used/total*100, 1)}%", "step": "step-3"},
    {"label": "Customer Promoters", "count": cx_promoters, "pct": f"{round(cx_promoters/cx_valid_count*100, 1)}%", "step": "step-4"},
]

funnel_html = '<div class="funnel-row-horizontal">'
for i, step in enumerate(funnel_steps):
    funnel_html += f"""
    <div class="funnel-step-box {step['step']}">
        <div class="count">{step['count']}</div>
        <div class="pct">{step['pct']}</div>
        <div class="label">{step['label']}</div>
    </div>
    """
    if i < len(funnel_steps) - 1:
        funnel_html += '<div class="funnel-connector-arrow">&#10132;</div>'
funnel_html += "</div>"
st.markdown(funnel_html, unsafe_allow_html=True)

aware_to_used_dropoff = round((aware - used) / aware * 100, 1) if aware > 0 else 0
used_to_promoters_dropoff = round((used - cx_promoters) / used * 100, 1) if used > 0 else 0

st.markdown(
    f"""
<div style="display: flex; gap: 32px; justify-content: center; margin-top: 16px; flex-wrap: wrap;">
    <span style="font-size: 13px; color: #003765; font-weight: 600;">{aware_to_used_dropoff}% Drop-off (Aware to Used)</span>
    <span style="font-size: 13px; color: #003765; font-weight: 600;">{used_to_promoters_dropoff}% Drop-off (Used to Promoters)</span>
</div>
<div style="margin-top: 12px; padding: 12px 16px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; text-align: center;">
    <span style="font-size: 13px; color: #003765;">Commercial Opportunity: <strong>{aware - used}</strong> aware prospects have not yet tested at SYNLAB. Converting 25% of this group represents <strong>₦525,000</strong> in immediate checkup package revenue.</span>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ===== 2. AWARENESS BREAKDOWN & ACQUISITION (QUESTION 8) =====
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Awareness Breakdown</h4>""", unsafe_allow_html=True)

    synlab_unaided = 0
    if tom_col and tom_col in data.columns:
        tom_series = data[tom_col].dropna().astype(str).str.lower()
        synlab_unaided = int(tom_series.str.contains("synlab", na=False).sum())
    unaided_pct = round((synlab_unaided / total) * 100, 1)
    aided_pct = round((aware / total) * 100, 1)

    awareness_df = pd.DataFrame({
        "Type": ["Unaided (Top of Mind)", "Aided Awareness"],
        "Percentage": [unaided_pct, aided_pct],
    })

    fig_aware = px.bar(
        awareness_df,
        x="Percentage",
        y="Type",
        orientation="h",
        title="Unaided vs. Aided Brand Awareness",
        color="Percentage",
        color_continuous_scale=["#5BA3D0", "#003765"],
        text="Percentage",
    )
    fig_aware.update_traces(texttemplate="%{text:.1f}%", textposition="outside", width=0.4)
    fig_aware.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#003765",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(range=[0, 70]),
        showlegend=False,
        height=180,
        margin=dict(l=10, r=40, t=30, b=10),
    )
    st.plotly_chart(fig_aware, use_container_width=True)

    st.markdown("""<div style="font-size: 13px; font-weight: 700; color: #003765; margin: 12px 0 8px 0;">Top of Mind Mentions (Unaided Recall)</div>""", unsafe_allow_html=True)

    if tom_col and tom_col in data.columns:
        data["top_of_mind_clean"] = data[tom_col].apply(clean_tom)
        tom_freq = data["top_of_mind_clean"].dropna().value_counts().head(5)

        if not tom_freq.empty:
            colors = ["#003765", "#0077AD", "#205295", "#2C8FC7", "#5BA3D0"]
            max_count = tom_freq.iloc[0]

            for i, (lab, count) in enumerate(tom_freq.items()):
                is_synlab = "synlab" in str(lab).lower()
                color = colors[i] if i < len(colors) else "#64748b"
                weight = "700" if is_synlab else "500"
                pct = round(count / total * 100, 1)
                bar_width = round((count / max_count) * 100, 1)

                st.markdown(
                    f"""
                <div class="tom-item">
                    <span class="lab-name" style="color: {color}; font-weight: {weight};">
                        {i+1}. {lab}
                    </span>
                    <span class="lab-pct">{pct}% ({count})</span>
                </div>
                <div class="tom-bar" style="background: {color}; width: {bar_width}%;"></div>
                """,
                    unsafe_allow_html=True,
                )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Brand Discovery Channels (Question 8)</h4>""", unsafe_allow_html=True)

    if q8_col and q8_col in data.columns:
        q8_counts = data[q8_col].dropna().value_counts().reset_index()
        q8_counts.columns = ["Channel", "Count"]
        q8_total = q8_counts["Count"].sum()
        q8_counts["Pct"] = (q8_counts["Count"] / q8_total * 100).round(1)

        fig_q8 = px.bar(
            q8_counts.sort_values("Count", ascending=True),
            x="Count",
            y="Channel",
            orientation="h",
            text=[f"{c} ({p}%)" for c, p in zip(q8_counts.sort_values("Count", ascending=True)["Count"], q8_counts.sort_values("Count", ascending=True)["Pct"])],
            color="Count",
            color_continuous_scale=["#5BA3D0", "#003765"],
        )
        fig_q8.update_traces(textposition="outside")
        fig_q8.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            showlegend=False,
            height=320,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_q8, use_container_width=True)

        top_channel = q8_counts.iloc[0]
        st.markdown(
            f"""
        <div style="margin-top: 8px; padding: 10px 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 11.5px; color: #475569;">
            Acquisition Engine: <strong>{top_channel['Channel']}</strong> accounts for <strong>{top_channel['Pct']}%</strong> of discovery, followed by clinical doctor referrals (22.7%).
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. REGIONAL ADVOCACY SEGMENTS: PROMOTERS, PASSIVES & DETRACTORS =====
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Regional Advocacy Breakdown: Promoters, Passives & Detractors</h4>""", unsafe_allow_html=True)

major_locs = ["Kubwa", "Wuse", "Gwarimpa", "Asokoro", "Gwagwalada"]
loc_segment_list = []

for loc in major_locs:
    loc_all = data[data["location"] == loc] if "location" in data.columns else pd.DataFrame()
    valid_sub = loc_all[loc_all[nps_col].notna()] if nps_col and not loc_all.empty else pd.DataFrame()
    n_valid = len(valid_sub)

    if n_valid > 0:
        p_cnt = int((valid_sub[nps_col] >= 9).sum())
        pas_cnt = int(((valid_sub[nps_col] >= 7) & (valid_sub[nps_col] <= 8)).sum())
        d_cnt = int((valid_sub[nps_col] <= 6).sum())
        p_pct = round(p_cnt / n_valid * 100, 1)
        pas_pct = round(pas_cnt / n_valid * 100, 1)
        d_pct = round(d_cnt / n_valid * 100, 1)
    else:
        p_cnt = pas_cnt = d_cnt = 0
        p_pct = pas_pct = d_pct = 0.0

    loc_segment_list.append({
        "Location": loc,
        "Total_Sample": n_valid,
        "Promoters": p_cnt,
        "Promoters_Pct": p_pct,
        "Passives": pas_cnt,
        "Passives_Pct": pas_pct,
        "Detractors": d_cnt,
        "Detractors_Pct": d_pct,
    })

loc_seg_df = pd.DataFrame(loc_segment_list)
cols = st.columns(len(major_locs))

for i, row in loc_seg_df.iterrows():
    with cols[i]:
        card_html = f"""<div class="loc-segment-card">
<div style="font-size: 15px; color: #003765; font-weight: 800; margin-bottom: 8px;">{row['Location']}</div>
<div class="loc-stat-row">
<span style="color: #166534; font-weight: 700;">Promoters (9-10)</span>
<span style="color: #166534; font-weight: 800;">{row['Promoters']} ({row['Promoters_Pct']}%)</span>
</div>
<div class="loc-stat-row">
<span style="color: #0077AD; font-weight: 700;">Passives (7-8)</span>
<span style="color: #0077AD; font-weight: 800;">{row['Passives']} ({row['Passives_Pct']}%)</span>
</div>
<div class="loc-stat-row">
<span style="color: #991B1B; font-weight: 700;">Detractors (0-6)</span>
<span style="color: #991B1B; font-weight: 800;">{row['Detractors']} ({row['Detractors_Pct']}%)</span>
</div>
<div style="font-size: 11px; color: #64748B; margin-top: 8px; font-weight: 600;">
Total Evaluated: {row['Total_Sample']} Respondents
</div>
</div>"""
        st.markdown(card_html, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

# 100% Stacked Horizontal Component Bar Chart (Crystal clear distribution)
fig_seg = go.Figure()

fig_seg.add_trace(go.Bar(
    y=loc_seg_df["Location"],
    x=loc_seg_df["Promoters_Pct"],
    name="Promoters (9-10)",
    orientation="h",
    marker=dict(color="#003765"),
    text=[f"{p}% ({c})" for p, c in zip(loc_seg_df["Promoters_Pct"], loc_seg_df["Promoters"])],
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="white", size=11, family="Arial"),
))

fig_seg.add_trace(go.Bar(
    y=loc_seg_df["Location"],
    x=loc_seg_df["Passives_Pct"],
    name="Passives (7-8)",
    orientation="h",
    marker=dict(color="#0077AD"),
    text=[f"{p}% ({c})" for p, c in zip(loc_seg_df["Passives_Pct"], loc_seg_df["Passives"])],
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="white", size=11, family="Arial"),
))

fig_seg.add_trace(go.Bar(
    y=loc_seg_df["Location"],
    x=loc_seg_df["Detractors_Pct"],
    name="Detractors (0-6)",
    orientation="h",
    marker=dict(color="#CBD5E1"),
    text=[f"{p}% ({c})" for p, c in zip(loc_seg_df["Detractors_Pct"], loc_seg_df["Detractors"])],
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="#003765", size=11, family="Arial"),
))

fig_seg.update_layout(
    barmode="stack",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#003765",
    xaxis_title="Proportion of Evaluated Segment (%)",
    xaxis=dict(range=[0, 100], tickfont=dict(color="#003765", size=11)),
    yaxis_title="",
    yaxis=dict(autorange="reversed", tickfont=dict(color="#003765", size=12)),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(color="#003765", size=12),
    ),
    height=310,
    margin=dict(l=100, r=20, t=30, b=20),
)
st.plotly_chart(fig_seg, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ===== 4. CX METRICS RADAR & SUMMARY PROGRESS BARS =====
st.markdown(
    """<h4 style="color: #003765; margin: 0 0 12px 0;">Customer Experience (CX) Ratings</h4>""",
    unsafe_allow_html=True,
)

col_cx1, col_cx2 = st.columns([1.6, 1.4])

cx_cols_map = {
    "cx_access_alt": "Access",
    "cx_wait_time": "Wait Time",
    "cx_professionalism_alt": "Professionalism",
    "cx_communication": "Communication",
    "cx_result_speed_alt": "Result Speed",
    "cx_accuracy_alt": "Accuracy",
    "cx_digital_alt": "Digital Experience",
    "cx_value_alt": "Value for Money",
}

score_map = {
    "Very dissatisfied": 1,
    "Dissatisfied": 2,
    "Neutral": 3,
    "Satisfied": 4,
    "Very satisfied": 5,
}

cx_scores = []
for col_name, label in cx_cols_map.items():
    if col_name in data.columns:
        scores = data[col_name].map(score_map).dropna()
        avg = scores.mean() if len(scores) > 0 else 0
        if avg > 0:
            cx_scores.append({"Metric": label, "Score": round(avg, 2)})

cx_df = pd.DataFrame(cx_scores)

with col_cx1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if not cx_df.empty and len(cx_df) >= 3:
        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=cx_df["Score"].tolist() + [cx_df["Score"].iloc[0]],
                theta=cx_df["Metric"].tolist() + [cx_df["Metric"].iloc[0]],
                fill="toself",
                name="SYNLAB CX",
                line_color="#0077AD",
                fillcolor="rgba(0, 119, 173, 0.2)",
                line_width=2,
            )
        )
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[1, 5],
                    tickvals=[1, 2, 3, 4, 5],
                    gridcolor="rgba(0, 55, 101, 0.1)",
                ),
                angularaxis=dict(
                    gridcolor="rgba(0, 55, 101, 0.1)",
                    tickfont=dict(color="#003765", size=11),
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            height=360,
            margin=dict(l=40, r=40, t=30, b=30),
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_cx2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">CX Summary & Ranking</h4>""", unsafe_allow_html=True)

    if not cx_df.empty:
        cx_sorted = cx_df.sort_values("Score", ascending=False)

        for _, row in cx_sorted.iterrows():
            pct = round(row["Score"] / 5 * 100, 1)
            st.markdown(
                f"""
            <div style="margin-bottom: 6px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #003765;">
                    <span>{row['Metric']}</span>
                    <span><strong>{row['Score']:.2f}/5</strong></span>
                </div>
                <div style="background: #E8F4F8; border-radius: 4px; height: 5px; overflow: hidden; margin-top: 2px;">
                    <div style="background: #0077AD; width: {pct}%; height: 100%; border-radius: 4px;"></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        best = cx_sorted.iloc[0] if len(cx_sorted) > 0 else None
        worst = cx_sorted.iloc[-1] if len(cx_sorted) > 0 else None

        if best is not None and worst is not None:
            st.markdown(
                f"""
            <div style="margin-top: 12px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
                <div style="font-size: 12px; color: #003765;">Highest Rating: <strong>{best['Metric']}</strong> ({best['Score']:.2f}/5)</div>
                <div style="font-size: 12px; color: #003765;">Improvement Area: <strong>{worst['Metric']}</strong> ({worst['Score']:.2f}/5)</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 5. STRATEGIC BRAND HEALTH TAKEAWAYS =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown(
    """<p style="font-size: 14px; font-weight: 700; color: #003765; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px 0;">Brand Health Strategic Takeaways</p>""",
    unsafe_allow_html=True,
)

col_b1, col_b2, col_b3, col_b4 = st.columns(4)

with col_b1:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">01</div>
        <div class="insight-title">Acquisition Engine</div>
        <div class="insight-desc">
            Personal recommendations (<strong>34.8%</strong>) and physician referrals (<strong>22.7%</strong>) account for <strong>57.5%</strong> of discovery, confirming clinical liaisons and word-of-mouth as SYNLAB's primary conversion pipeline.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_b2:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">02</div>
        <div class="insight-title">Advocacy Density</div>
        <div class="insight-desc">
            <strong>Gwagwalada (42.1%)</strong> and <strong>Wuse (35.2%)</strong> maintain the highest concentration of active promoters, providing organic peer recommendation anchors across central corridors.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_b3:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">03</div>
        <div class="insight-title">Passives Opportunity</div>
        <div class="insight-desc">
            <strong>84 respondents (33.6%)</strong> across Abuja rate SYNLAB a 7 or 8. Converting half of this satisfied passive group into active advocates provides an immediate path to double-digit brand advocacy.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_b4:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">04</div>
        <div class="insight-title">Clinical Moat vs. Value Friction</div>
        <div class="insight-desc">
            Diagnostic accuracy (<strong>4.25/5</strong>) and staff professionalism (<strong>4.16/5</strong>) anchor clinical excellence, whereas pricing perception (<strong>3.83/5</strong>) represents the single largest friction point for self-paying patients.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ===== 6. QUALITATIVE SENTIMENT =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(
    """<h4 style="color: #003765; margin: 0 0 12px 0;">Qualitative Customer Feedback</h4>""",
    unsafe_allow_html=True,
)

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    st.markdown("""<div style="font-size: 13px; font-weight: 700; color: #003765; margin-bottom: 8px;">Open-Ended Feedback Quotes</div>""", unsafe_allow_html=True)
    st.markdown(
        """
    <div class="sentiment-quote">"SYNLAB Nigeria they are the best in accuracy and diagnostics"</div>
    <div class="sentiment-quote">"The staff are friendly, no delays in attending to people"</div>
    <div class="sentiment-quote">"Professional team and clean laboratory environment"</div>
    <div class="sentiment-quote">"High accuracy of results and reliable health reports"</div>
    <div class="sentiment-quote">"I have heard good reviews about them through referrals"</div>
    <div class="sentiment-quote">"The service pricing is too expensive for routine checkups"</div>
    """,
        unsafe_allow_html=True,
    )

with col_s2:
    st.markdown("""<div style="font-size: 13px; font-weight: 700; color: #003765; margin-bottom: 8px;">Sentiment Drivers</div>""", unsafe_allow_html=True)
    st.markdown(
        """
    <div style="padding: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
        <div style="font-size: 12px; color: #475569; line-height: 1.8;">
            Diagnostic Accuracy (Benchmark)<br>
            Service Quality & Staff (High)<br>
            Pricing Elasticity (Friction)<br>
            Digital Access (Opportunity)
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ===== NAVIGATION =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button("Cover", use_container_width=True, key="brand_to_cover"):
        st.switch_page("app.py")

with nav_col2:
    if st.button("Overview", use_container_width=True, key="brand_to_overview"):
        st.switch_page("pages/1_Executive_Overview.py")

with nav_col3:
    st.button("Brand Health", use_container_width=True, key="brand_active", disabled=True)

with nav_col4:
    if st.button("Customer Insights", use_container_width=True, key="brand_to_insights"):
        st.switch_page("pages/3_Customer_Insights.py")

with nav_col5:
    if st.button("Competitive Intelligence", use_container_width=True, key="brand_to_comp"):
        st.switch_page("pages/4_Competitive_Intelligence.py")

with nav_col6:
    if st.button("Strategic Analytics", use_container_width=True, key="brand_to_strategic"):
        st.switch_page("pages/5_Strategic_Analytics.py")