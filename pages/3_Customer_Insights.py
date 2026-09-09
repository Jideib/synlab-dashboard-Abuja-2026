# pages/3_Customer_Insights.py
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
        page_title="Customer Insights | SYNLAB Nigeria",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    st.set_page_config(
        page_title="Customer Insights | SYNLAB Nigeria",
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
        padding: 18px;
        border: 1px solid var(--synlab-border);
        border-left: 4px solid var(--synlab-cerulean);
        height: 100%;
    }
    .insight-number {
        font-size: 16px;
        font-weight: 700;
        color: var(--synlab-cerulean);
    }
    .insight-title {
        font-weight: 700;
        color: var(--synlab-midnight);
        margin: 4px 0;
        font-size: 13.5px;
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

wtp_col = find_col(data, ["wtp_package", "price tier", "wtp"])

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

st.markdown(
    """
<div class="page-header">
    <h1>Customer Insights & Segmentation</h1>
    <p>Demographic profile, package pricing preferences across age and occupation, and strategic customer segment takeaways</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== 1. INTERACTIVE SEGMENT FILTERS =====
st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
st.markdown(
    """<div style="font-weight: 700; color: #003765; font-size: 13px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Interactive Segment Filters</div>""",
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
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Age Group Distribution</h4>""", unsafe_allow_html=True)

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
        fig_age.update_traces(
            textposition="outside",
            textfont=dict(color="#003765", size=12, family="Arial"),
            cliponaxis=False,
        )
        fig_age.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            yaxis=dict(
                tickfont=dict(size=12, color="#003765", family="Arial"),
                showticklabels=True,
            ),
            showlegend=False,
            height=300,
            margin=dict(l=90, r=60, t=10, b=10),
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
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Gender Ratio</h4>""", unsafe_allow_html=True)

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
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color="#003765", size=12),
            ),
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_gender.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No gender records match the active filter criteria.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. OCCUPATION & LOCATION DISTRIBUTION (RETAINED) =====
col_o1, col_o2 = st.columns(2)

with col_o1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Top Occupations</h4>""", unsafe_allow_html=True)

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
        fig_occ.update_traces(
            textposition="outside",
            textfont=dict(color="#003765", size=12, family="Arial"),
            cliponaxis=False,
        )
        fig_occ.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(size=12, color="#003765", family="Arial"),
                showticklabels=True,
            ),
            showlegend=False,
            height=320,
            margin=dict(l=175, r=60, t=10, b=10),
        )
        st.plotly_chart(fig_occ, use_container_width=True)
    else:
        st.info("No occupation records available.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_o2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Location Distribution</h4>""", unsafe_allow_html=True)

    loc_counts = filtered_data["location"].value_counts()

    if not loc_counts.empty:
        fig_loc = px.bar(
            x=loc_counts.index,
            y=loc_counts.values,
            color=loc_counts.values,
            color_continuous_scale=["#5BA3D0", "#003765"],
            text=loc_counts.values,
        )
        fig_loc.update_traces(
            textposition="outside",
            textfont=dict(color="#003765", size=12, family="Arial"),
            cliponaxis=False,
        )
        fig_loc.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            xaxis=dict(
                tickfont=dict(size=11, color="#003765", family="Arial"),
                showticklabels=True,
            ),
            yaxis_title="Respondents",
            yaxis=dict(
                tickfont=dict(size=11, color="#003765", family="Arial"),
            ),
            showlegend=False,
            height=320,
            margin=dict(l=40, r=20, t=10, b=10),
        )
        st.plotly_chart(fig_loc, use_container_width=True)
    else:
        st.info("No location records available.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 4. AGE & OCCUPATION VS. PACKAGE PRICING (HIGH-VISIBILITY MATRIX STYLE) =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Package Pricing Preferences by Age and Occupation</h4>""", unsafe_allow_html=True)

col_p1, col_p2 = st.columns(2)

tier_order = ["Below ₦20,000", "₦20,000-50,000", "₦50,000-100,000", "₦100,000-200,000", "Above ₦200,000"]

with col_p1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 4px 0;">Age Distribution vs. Package Pricing Preference</h4>""", unsafe_allow_html=True)
    st.caption("Distribution matrix showing respondent density across age cohorts and package price tiers")

    if wtp_col and wtp_col in filtered_data.columns and "age" in filtered_data.columns:
        wtp_valid = filtered_data[filtered_data[wtp_col].notna() & (filtered_data[wtp_col] != "I would not purchase this type of package")]
        age_cohorts = ["18-24", "25-34", "35-44", "45-54", "55 and above"]
        
        cross_age = pd.crosstab(wtp_valid["age"], wtp_valid[wtp_col])
        cross_age = cross_age.reindex(index=[a for a in age_cohorts if a in cross_age.index], columns=[t for t in tier_order if t in cross_age.columns]).fillna(0)

        z_vals = cross_age.values
        x_labels = list(cross_age.columns)
        y_labels = list(cross_age.index)
        text_matrix = [[f"<b>{int(val)}</b>" if val > 0 else "-" for val in row] for row in z_vals]

        fig_heat_age = go.Figure(
            data=go.Heatmap(
                z=z_vals,
                x=x_labels,
                y=y_labels,
                text=text_matrix,
                texttemplate="%{text}",
                textfont=dict(size=12, color="#003765", family="Arial"),
                colorscale=[[0, "#F1F5F9"], [0.2, "#D0E6F2"], [0.5, "#7CB8D3"], [1.0, "#0077AD"]],
                showscale=False,
            )
        )
        fig_heat_age.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis=dict(
                tickfont=dict(size=11, color="#003765", family="Arial"),
                side="bottom",
            ),
            yaxis=dict(
                tickfont=dict(size=12, color="#003765", family="Arial"),
                autorange="reversed",
            ),
            height=320,
            margin=dict(l=80, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_heat_age, use_container_width=True)
    else:
        st.info("Pricing data not available for active segment.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_p2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 4px 0;">Occupation vs. Package Pricing Preference</h4>""", unsafe_allow_html=True)
    st.caption("Distribution matrix showing respondent density across professional occupations and package price tiers")

    if wtp_col and wtp_col in filtered_data.columns and "occupation" in filtered_data.columns:
        wtp_valid = filtered_data[filtered_data[wtp_col].notna() & (filtered_data[wtp_col] != "I would not purchase this type of package")]
        top_occs = wtp_valid["occupation"].value_counts().head(5).index.tolist()
        
        cross_occ = pd.crosstab(wtp_valid["occupation"], wtp_valid[wtp_col])
        cross_occ = cross_occ.reindex(index=top_occs, columns=[t for t in tier_order if t in cross_occ.columns]).fillna(0)

        z_vals_occ = cross_occ.values
        x_labels_occ = list(cross_occ.columns)
        y_labels_occ = list(cross_occ.index)
        text_matrix_occ = [[f"<b>{int(val)}</b>" if val > 0 else "-" for val in row] for row in z_vals_occ]

        fig_heat_occ = go.Figure(
            data=go.Heatmap(
                z=z_vals_occ,
                x=x_labels_occ,
                y=y_labels_occ,
                text=text_matrix_occ,
                texttemplate="%{text}",
                textfont=dict(size=12, color="#003765", family="Arial"),
                colorscale=[[0, "#F1F5F9"], [0.2, "#D0E6F2"], [0.5, "#7CB8D3"], [1.0, "#0077AD"]],
                showscale=False,
            )
        )
        fig_heat_occ.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis=dict(
                tickfont=dict(size=11, color="#003765", family="Arial"),
                side="bottom",
            ),
            yaxis=dict(
                tickfont=dict(size=12, color="#003765", family="Arial"),
                autorange="reversed",
            ),
            height=320,
            margin=dict(l=175, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_heat_occ, use_container_width=True)
    else:
        st.info("Pricing data not available for active segment.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 5. BEHAVIORAL PERSONAS WITH CSAT METRICS =====
st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Customer Behavioral Personas</h4>""", unsafe_allow_html=True)

persona_counts = filtered_data["persona"].value_counts()
persona_pcts = (persona_counts / len(filtered_data) * 100).round(1) if len(filtered_data) > 0 else {}

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

# ===== 6. INSURANCE COVERAGE ANALYSIS =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Insurance Coverage Analysis</h4>""", unsafe_allow_html=True)

col_i1, col_i2 = st.columns(2)

with col_i1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Insurance Status Distribution</h4>""", unsafe_allow_html=True)

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
        fig_ins.update_traces(
            textposition="outside",
            textfont=dict(color="#003765", size=12, family="Arial"),
            cliponaxis=False,
        )
        fig_ins.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Respondents",
            yaxis_title="",
            yaxis=dict(
                tickfont=dict(size=12, color="#003765", family="Arial"),
                showticklabels=True,
            ),
            showlegend=False,
            height=300,
            margin=dict(l=165, r=60, t=10, b=10),
        )
        st.plotly_chart(fig_ins, use_container_width=True)
    else:
        st.info("No insurance records available.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_i2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Awareness and Usage by Insurance Type</h4>""", unsafe_allow_html=True)

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
        fig_ins_comp.update_traces(
            textposition="outside",
            textfont=dict(color="#003765", size=11, family="Arial"),
            cliponaxis=False,
        )
        fig_ins_comp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            xaxis=dict(
                tickfont=dict(size=11, color="#003765", family="Arial"),
            ),
            yaxis_title="Percentage (%)",
            yaxis=dict(
                range=[0, 85],
                tickfont=dict(size=11, color="#003765", family="Arial"),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color="#003765", size=12),
            ),
            height=300,
            margin=dict(l=20, r=20, t=10, b=10),
        )
        st.plotly_chart(fig_ins_comp, use_container_width=True)
    else:
        st.info("No insurance cross-analysis records available.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 7. REGIONAL PERFORMANCE CARDS =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("""<h4 style="color: #003765; margin: 0 0 12px 0;">Location Performance Summary (CSAT Focus)</h4>""", unsafe_allow_html=True)

major_loc_order = ["Asokoro", "Gwagwalada", "Gwarimpa", "Wuse", "Kubwa"]
loc_card_data = []

for loc in major_loc_order:
    loc_sub = data[data["location"] == loc]
    t_cnt = len(loc_sub)
    a_cnt = int(loc_sub["aware_synlab"].sum()) if "aware_synlab" in loc_sub.columns else 0
    u_cnt = int(loc_sub["used_synlab"].sum()) if "used_synlab" in loc_sub.columns else 0

    a_pct = round((a_cnt / t_cnt * 100), 1) if t_cnt > 0 else 0.0
    u_pct = round((u_cnt / t_cnt * 100), 1) if t_cnt > 0 else 0.0

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

# ===== 8. EXPANDED STRATEGIC CUSTOMER SEGMENT TAKEAWAYS (8 CARDS) =====
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown(
    """<p style="font-size: 14px; font-weight: 700; color: #003765; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px 0;">Customer Segment Strategic Takeaways (8 Dimensions)</p>""",
    unsafe_allow_html=True,
)

t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">01</div>
        <div class="insight-title">Core Working Cohort (35–44)</div>
        <div class="insight-desc">
            Represents <strong>57%</strong> of active respondents. The majority select packages between ₦20K–₦50K, making them the primary commercial target for routine executive wellness packages.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t_col2:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">02</div>
        <div class="insight-title">Doctor/HMO Loyal Persona</div>
        <div class="insight-desc">
            Commands <strong>53.6%</strong> of respondents with <strong>79.0%</strong> CSAT. Physician referrals and HMO network inclusion are the single largest operational conversion funnel.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t_col3:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">03</div>
        <div class="insight-title">Urban Center Dynamics</div>
        <div class="insight-desc">
            <strong>Wuse (88.9%)</strong> and <strong>Gwagwalada (86.6%)</strong> lead customer satisfaction, validating service standards across high-density commercial corridors.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t_col4:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">04</div>
        <div class="insight-title">Gender Engagement Balance</div>
        <div class="insight-desc">
            Respondents comprise <strong>54.0% Male</strong> and <strong>44.4% Female</strong>. Women index higher on wellness screenings; men index higher on pre-employment and HMO checkups.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

t_col5, t_col6, t_col7, t_col8 = st.columns(4)

with t_col5:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">05</div>
        <div class="insight-title">Quality-First Elasticity</div>
        <div class="insight-desc">
            <strong>60.2%</strong> of all respondents affirm that <em>"quality comes first, though price matters"</em>, indicating that clinical accreditation insulates SYNLAB against discount rivals.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t_col6:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">06</div>
        <div class="insight-title">Corporate vs. Retail Pricing</div>
        <div class="insight-desc">
            Corporate professionals tolerate price tiers up to ₦100K under employer plans, whereas self-employed and civil servants concentrate heavily in the &le; ₦50K sweet spot.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t_col7:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">07</div>
        <div class="insight-title">Digital Result Delivery Gap</div>
        <div class="insight-desc">
            <strong>58.6%</strong> of respondents prefer digital report access (Email, WhatsApp, App). Deploying automated WhatsApp delivery directly resolves turnaround friction.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t_col8:
    st.markdown(
        """
    <div class="insight-card">
        <div class="insight-number">08</div>
        <div class="insight-title">Physician Churn Defense</div>
        <div class="insight-desc">
            <strong>22.2%</strong> of historical laboratory switching is caused by doctor/HMO reassignment. Establishing formal clinical retainers across private clinics secures long-term volume.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ===== 9. NAVIGATION =====
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