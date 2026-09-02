import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Customer Insights | SYNLAB Nigeria",
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

    .filter-bar {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid var(--synlab-border);
        margin-bottom: 24px;
    }

    .persona-card {
        background: white;
        border-radius: 10px;
        padding: 20px 16px;
        border: 1px solid var(--synlab-border);
        border-top: 4px solid var(--synlab-cerulean);
        text-align: center;
        height: 100%;
    }
    .persona-card .persona-name {
        font-weight: 700;
        color: var(--synlab-midnight);
        font-size: 15px;
        margin-bottom: 4px;
    }
    .persona-card .persona-pct {
        font-size: 26px;
        font-weight: 800;
        color: var(--synlab-cerulean);
        line-height: 1.1;
    }
    .persona-card .persona-csat {
        font-size: 13px;
        color: #003765;
        font-weight: 700;
        margin-top: 6px;
    }
    .persona-card .persona-desc {
        font-size: 11px;
        color: var(--synlab-slate);
        margin-top: 2px;
    }

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
        line-height: 1.5;
    }

    .location-card {
        background: white;
        border-radius: 10px;
        padding: 18px 14px;
        border: 1px solid var(--synlab-border);
        border-top: 3px solid var(--synlab-cerulean);
        text-align: center;
        height: 100%;
    }
    .location-card .loc-name { font-weight: 700; color: #003765; font-size: 15px; }
    .location-card .loc-value { font-size: 20px; font-weight: 800; color: #0077AD; margin-top: 2px; }
    .location-card .loc-label { font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }

    @media (max-width: 768px) {
        .main > div { padding: 0 16px !important; }
        .page-header { padding: 16px 20px; }
        .page-header h1 { font-size: 20px; }
        .filter-bar { padding: 12px 16px; }
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

# CX columns & rating mapping
cx_alt_cols = [
    "cx_access_alt", "cx_wait_time", "cx_professionalism_alt",
    "cx_communication", "cx_result_speed_alt", "cx_accuracy_alt",
    "cx_digital_alt", "cx_value_alt"
]
rating_map = {
    "Very dissatisfied": 1,
    "Dissatisfied": 2,
    "Neutral": 3,
    "Satisfied": 4,
    "Very satisfied": 5,
}

# Assign Behavioral Personas
def assign_persona(row):
    if row.get("decision_price", 0) == 1:
        return "Price Sensitive"
    elif row.get("decision_doctor", 0) == 1 or row.get("decision_hmo", 0) == 1:
        return "Doctor/HMO Loyal"
    elif row.get("decision_proximity", 0) == 1:
        return "Convenience Seeker"
    elif row.get("decision_reputation", 0) == 1 or row.get("decision_experience", 0) == 1:
        return "Quality Driven"
    elif row.get("decision_family", 0) == 1:
        return "Socially Influenced"
    else:
        return "Undifferentiated"

data["persona"] = data.apply(assign_persona, axis=1)

# Header
st.markdown(
    """
<div class="page-header">
    <h1>Customer Insights & Segmentation</h1>
    <p>Demographic profile, customer satisfaction (CSAT) across corridors, and behavioral archetype dynamics</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== 1. INTERACTIVE SEGMENT FILTERS =====
st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
st.markdown(
    '<div style="font-weight: 700; color: #003765; font-size: 13px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Interactive Segment Filters</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

age_options = sorted([str(x) for x in data["age"].dropna().unique()])
gender_options = sorted([str(x) for x in data["gender"].dropna().unique()])
location_options = sorted([str(x) for x in data["location"].dropna().unique()])
occupation_options = sorted([str(x) for x in data["occupation"].dropna().unique()])

with col1:
    age_filter = st.multiselect("Age Group", options=age_options, default=age_options, key="ins_age")
with col2:
    gender_filter = st.multiselect("Gender", options=gender_options, default=gender_options, key="ins_gender")
with col3:
    location_filter = st.multiselect("Location", options=location_options, default=location_options, key="ins_loc")
with col4:
    occupation_filter = st.multiselect("Occupation", options=occupation_options, default=occupation_options, key="ins_occ")

st.markdown("</div>", unsafe_allow_html=True)

# Apply Filters
filtered_data = data[
    (data["age"].astype(str).isin(age_filter))
    & (data["gender"].astype(str).isin(gender_filter))
    & (data["location"].astype(str).isin(location_filter))
    & (data["occupation"].astype(str).isin(occupation_filter))
]

filtered_total = len(filtered_data)
if filtered_total < total:
    st.caption(f"Displaying **{filtered_total}** of **{total}** verified respondents based on active filters.")

# ===== 2. DEMOGRAPHICS & GENDER =====
col_d1, col_d2 = st.columns(2)

with col_d1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Age Group Distribution</h4>", unsafe_allow_html=True)

    age_counts = filtered_data["age"].value_counts()
    age_order = ["18-24", "25-34", "35-44", "45-54", "55 and above"]
    age_counts = age_counts.reindex([a for a in age_order if a in age_counts.index])

    if not age_counts.empty:
        fig_age = px.bar(
            x=age_counts.values,
            y=age_counts.index,
            orientation="h",
            color=age_counts.values,
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=[f"{v} ({round(v/filtered_total*100, 1)}%)" for v in age_counts.values],
        )
        fig_age.update_traces(textposition="outside")
        fig_age.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            showlegend=False,
            height=300,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_age, use_container_width=True)

        top_age = age_counts.index[0] if len(age_counts) > 0 else "35-44"
        top_age_cnt = age_counts.iloc[0] if len(age_counts) > 0 else 0
        top_age_pct = round(top_age_cnt / filtered_total * 100, 1) if filtered_total > 0 else 0

        st.markdown(
            f"""
        <div style="margin-top: 8px; padding: 10px 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px;">
            <span style="font-size: 12px; color: #003765;">
                <strong>{top_age}</strong> is the primary age group representing <strong>{top_age_cnt}</strong> respondents ({top_age_pct}%).
            </span>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No age records match the active filter criteria.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_d2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Gender Ratio</h4>", unsafe_allow_html=True)

    gender_counts = filtered_data["gender"].value_counts()

    if not gender_counts.empty:
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            color_discrete_sequence=["#003765", "#0077AD", "#7CB8D3"],
            hole=0.45,
        )
        fig_gender.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_gender.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No gender records match the active filter criteria.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. OCCUPATION & LOCATION =====
col_o1, col_o2 = st.columns(2)

with col_o1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Top Occupations</h4>", unsafe_allow_html=True)

    occ_counts = filtered_data["occupation"].value_counts().head(6)

    if not occ_counts.empty:
        fig_occ = px.bar(
            x=occ_counts.values,
            y=occ_counts.index,
            orientation="h",
            color=occ_counts.values,
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=[f"{v} ({round(v/filtered_total*100, 1)}%)" for v in occ_counts.values],
        )
        fig_occ.update_traces(textposition="outside")
        fig_occ.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            showlegend=False,
            height=300,
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_occ, use_container_width=True)
    else:
        st.info("No occupation records available.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_o2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Location Distribution</h4>", unsafe_allow_html=True)

    loc_counts = filtered_data["location"].value_counts()

    if not loc_counts.empty:
        fig_loc = px.bar(
            x=loc_counts.index,
            y=loc_counts.values,
            color=loc_counts.values,
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=loc_counts.values,
        )
        fig_loc.update_traces(textposition="outside")
        fig_loc.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            yaxis_title="Respondents",
            showlegend=False,
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_loc, use_container_width=True)
    else:
        st.info("No location records available.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 4. BEHAVIORAL PERSONAS WITH CSAT METRICS =====
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Customer Behavioral Personas</h4>", unsafe_allow_html=True)

persona_counts = filtered_data["persona"].value_counts()
persona_pcts = (persona_counts / len(filtered_data) * 100).round(1) if len(filtered_data) > 0 else {}

# Calculate CSAT per persona (Top-2 Box: Satisfied or Very Satisfied)
persona_csat_dict = {}
for p_name in persona_counts.index:
    p_df = filtered_data[filtered_data["persona"] == p_name]
    p_ratings = []
    for c in cx_alt_cols:
        if c in p_df.columns:
            p_ratings.extend(p_df[c].map(rating_map).dropna().tolist())
    if len(p_ratings) > 0:
        csat_pct_val = round(sum(1 for r in p_ratings if r >= 4) / len(p_ratings) * 100, 1)
        mean_val = round(sum(p_ratings) / len(p_ratings), 2)
        persona_csat_dict[p_name] = f"{csat_pct_val}% ({mean_val}/5)"
    else:
        persona_csat_dict[p_name] = "N/A"

persona_colors = ["#002647", "#003765", "#0077AD", "#2C8FC7"]

if not persona_counts.empty:
    top_personas = persona_counts.head(4)
    cols = st.columns(len(top_personas))

    for i, (p_name, count) in enumerate(top_personas.items()):
        with cols[i]:
            pct = persona_pcts.get(p_name, 0)
            csat_display = persona_csat_dict.get(p_name, "N/A")
            card_border = persona_colors[i] if i < len(persona_colors) else "#64748B"

            st.markdown(
                f"""
            <div class="persona-card" style="border-top-color: {card_border};">
                <div class="persona-name">{p_name}</div>
                <div class="persona-pct" style="color: {card_border};">{pct}%</div>
                <div class="persona-csat">CSAT: {csat_display}</div>
                <div class="persona-desc">{count} Respondents</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    top_persona_name = persona_counts.index[0]
    st.markdown(
        f"""
    <div style="margin-top: 12px; padding: 12px 16px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
        <span style="font-size: 13px; color: #003765;">
            Dominant Segment: <strong>{top_persona_name}</strong> represents <strong>{persona_pcts.get(top_persona_name, 0)}%</strong> of respondents, maintaining strong service satisfaction ({persona_csat_dict.get(top_persona_name, '')}) driven by physician referrals and HMO panels.
        </span>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ===== 5. INSURANCE COVERAGE ANALYSIS =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Insurance Coverage Analysis</h4>", unsafe_allow_html=True)

col_i1, col_i2 = st.columns(2)

with col_i1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Insurance Status Distribution</h4>", unsafe_allow_html=True)

    ins_counts = filtered_data["insurance"].value_counts()

    if not ins_counts.empty:
        fig_ins = px.bar(
            x=ins_counts.values,
            y=ins_counts.index,
            orientation="h",
            color=ins_counts.values,
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=[f"{v} ({round(v/filtered_total*100, 1)}%)" for v in ins_counts.values],
        )
        fig_ins.update_traces(textposition="outside")
        fig_ins.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            showlegend=False,
            height=300,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_ins, use_container_width=True)
    else:
        st.info("No insurance records available.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_i2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Awareness and Usage by Insurance Type</h4>", unsafe_allow_html=True)

    ins_behavior = (
        filtered_data.groupby("insurance")
        .agg(
            Awareness=("aware_synlab", lambda x: (x.sum() / len(x)) * 100),
            Usage=("used_synlab", lambda x: (x.sum() / len(x)) * 100),
        )
        .round(1)
        .reset_index()
    )

    if not ins_behavior.empty:
        ins_melted = ins_behavior.melt(
            id_vars=["insurance"],
            value_vars=["Awareness", "Usage"],
            var_name="Metric",
            value_name="Percentage",
        )

        fig_ins_comp = px.bar(
            ins_melted,
            x="insurance",
            y="Percentage",
            color="Metric",
            barmode="group",
            text=[f"{p:.1f}%" for p in ins_melted["Percentage"]],
            color_discrete_sequence=["#003765", "#0077AD"],
        )
        fig_ins_comp.update_traces(textposition="outside")
        fig_ins_comp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            yaxis_title="Percentage (%)",
            yaxis=dict(range=[0, 80]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_ins_comp, use_container_width=True)
    else:
        st.info("No insurance cross-analysis records available.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 6. LOCATION PERFORMANCE CARDS WITH CSAT =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #003765; margin: 0 0 12px 0;'>Location Performance Summary (CSAT Focus)</h4>", unsafe_allow_html=True)

major_loc_order = ["Asokoro", "Gwagwalada", "Gwarimpa", "Wuse", "Kubwa"]
loc_card_data = []

for loc in major_loc_order:
    loc_sub = data[data["location"] == loc]
    t_cnt = len(loc_sub)
    a_cnt = int(loc_sub["aware_synlab"].sum())
    u_cnt = int(loc_sub["used_synlab"].sum())

    a_pct = round((a_cnt / t_cnt * 100), 1) if t_cnt > 0 else 0.0
    u_pct = round((u_cnt / t_cnt * 100), 1) if t_cnt > 0 else 0.0

    # Collect touchpoint ratings for this location
    r_list = []
    for c in cx_alt_cols:
        if c in loc_sub.columns:
            r_list.extend(loc_sub[c].map(rating_map).dropna().tolist())

    if len(r_list) > 0:
        csat_score = round(sum(1 for r in r_list if r >= 4) / len(r_list) * 100, 1)
        mean_rating = round(sum(r_list) / len(r_list), 2)
    else:
        csat_score = 0.0
        mean_rating = 0.0

    loc_card_data.append({
        "Location": loc,
        "Total": t_cnt,
        "Awareness": a_pct,
        "Usage": u_pct,
        "CSAT": csat_score,
        "Mean_Rating": mean_rating,
        "Ratings_Count": len(r_list)
    })

loc_card_df = pd.DataFrame(loc_card_data)
loc_cols = st.columns(len(loc_card_df))

for i, row in loc_card_df.iterrows():
    with loc_cols[i]:
        card_border = "#003765" if row["CSAT"] >= 80 else "#0077AD" if row["CSAT"] >= 70 else "#2C8FC7"
        st.markdown(
            f"""
        <div class="location-card" style="border-top-color: {card_border};">
            <div class="loc-name">{row['Location']}</div>
            <div class="loc-value">{row['Awareness']}%</div>
            <div class="loc-label">Awareness</div>
            <div style="margin: 4px 0;"></div>
            <div class="loc-value" style="font-size: 18px; color: {card_border};">{row['Usage']}%</div>
            <div class="loc-label">Usage</div>
            <div style="margin: 4px 0;"></div>
            <div class="loc-value" style="font-size: 18px; color: #003765;">{row['CSAT']}%</div>
            <div class="loc-label">CSAT ({row['Mean_Rating']}/5)</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ===== 7. STRATEGIC CUSTOMER SEGMENT INSIGHTS =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown(
    '<p style="font-size: 14px; font-weight: 700; color: #003765; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px 0;">Customer Segment Insights</p>',
    unsafe_allow_html=True,
)

col_in1, col_in2, col_in3, col_in4 = st.columns(4)

with col_in1:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">01</div>
        <div class="insight-title">Primary Age Group</div>
        <div class="insight-desc">
            <strong>35–44 years</strong> represents <strong>57.6%</strong> (287) of total respondents — focus corporate checkup packages on this core working cohort.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_in2:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">02</div>
        <div class="insight-title">Dominant Persona</div>
        <div class="insight-desc">
            <strong>Doctor/HMO Loyal</strong> makes up <strong>53.6%</strong> (267) of respondents with <strong>79.0%</strong> CSAT — physician referrals remain the key conversion channel.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_in3:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">03</div>
        <div class="insight-title">High-Satisfaction Corridors</div>
        <div class="insight-desc">
            <strong>Wuse (88.9%)</strong>, <strong>Gwagwalada (86.6%)</strong>, and <strong>Gwarimpa (84.1%)</strong> lead customer satisfaction, validating service standards across urban centers.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_in4:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">04</div>
        <div class="insight-title">Gender Balance</div>
        <div class="insight-desc">
            Respondents comprise <strong>54.0% Male</strong> (269) and <strong>44.4% Female</strong> (221) — tailored messaging across gender segments is recommended.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ===== NAVIGATION =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button("Cover", use_container_width=True, key="ins_to_cover"):
        st.switch_page("app.py")

with nav_col2:
    if st.button("Overview", use_container_width=True, key="ins_to_overview"):
        st.switch_page("pages/1_Executive_Overview.py")

with nav_col3:
    if st.button("Brand Health", use_container_width=True, key="ins_to_brand"):
        st.switch_page("pages/2_Brand_Health.py")

with nav_col4:
    st.button("Customer Insights", use_container_width=True, key="ins_active", disabled=True)

with nav_col5:
    if st.button("Competitive Intelligence", use_container_width=True, key="ins_to_comp"):
        st.switch_page("pages/4_Competitive_Intelligence.py")

with nav_col6:
    if st.button("Strategic Analytics", use_container_width=True, key="ins_to_strategic"):
        st.switch_page("pages/5_Strategic_Analytics.py")