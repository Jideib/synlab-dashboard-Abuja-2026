# pages/3_Customer_Insights.py
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Customer Insights & Segmentation· SYNLAB Nigeria",
    page_icon="assets/synlab_logo.png",
    layout="wide",  # <--- THIS KEEPS THE PAGE WIDE ON RELOAD
    initial_sidebar_state="collapsed",
)

def show():
    """Render the Customer Insights & Segmentation page"""

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

        .filter-bar {
            background: white;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 24px;
        }

        .persona-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            text-align: center;
            height: 100%;
            border-top: 4px solid #0077AD;
        }
        .persona-card .persona-icon { font-size: 32px; }
        .persona-card .persona-name { font-weight: 700; color: #003765; font-size: 15px; margin: 8px 0 4px; }
        .persona-card .persona-pct { font-size: 26px; font-weight: 700; color: #0077AD; }
        .persona-card .persona-nps { font-size: 13px; color: #64748b; margin-top: 2px; }
        .persona-card .persona-desc { font-size: 12px; color: #94a3b8; margin-top: 2px; }

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

        .location-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            text-align: center;
            border-top: 4px solid #0077AD;
            height: 100%;
        }
        .location-card .loc-name { font-weight: 700; color: #003765; font-size: 15px; }
        .location-card .loc-value { font-size: 22px; font-weight: 700; color: #0077AD; }
        .location-card .loc-label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }

        @media (max-width: 768px) {
            .main > div { padding: 0 16px !important; }
            .page-header { padding: 16px 20px; }
            .page-header h1 { font-size: 22px; }
            .filter-bar { padding: 12px 16px; }
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

    # Consolidate Jabi into Wuse
    if "location" in data.columns:
        data["location"] = data["location"].replace("Jabi", "Wuse")

    total = len(data)

    # ===== PAGE HEADER =====
    st.markdown(
        """
    <div class="page-header">
        <h1>👥 Customer Insights & Segmentation</h1>
        <p>Demographic deep-dive, occupation cross-analysis, and behavioral personas</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== INTERACTIVE FILTERS =====
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-weight: 700; color: #003765; font-size: 14px; margin-bottom: 8px;">🎛️ Interactive Segment Filters</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    age_options = sorted([str(x) for x in data["age"].dropna().unique()])
    gender_options = sorted([str(x) for x in data["gender"].dropna().unique()])
    location_options = sorted(
        [str(x) for x in data["location"].dropna().unique()]
    )
    occupation_options = sorted(
        [str(x) for x in data["occupation"].dropna().unique()]
    )

    with col1:
        age_filter = st.multiselect(
            "Age Group",
            options=age_options,
            default=age_options,
            key="insights_age_filter",
        )

    with col2:
        gender_filter = st.multiselect(
            "Gender",
            options=gender_options,
            default=gender_options,
            key="insights_gender_filter",
        )

    with col3:
        location_filter = st.multiselect(
            "Location",
            options=location_options,
            default=location_options,
            key="insights_location_filter",
        )

    with col4:
        occupation_filter = st.multiselect(
            "Occupation",
            options=occupation_options,
            default=occupation_options,
            key="insights_occupation_filter",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Filter Application
    filtered_data = data[
        (data["age"].astype(str).isin(age_filter))
        & (data["gender"].astype(str).isin(gender_filter))
        & (data["location"].astype(str).isin(location_filter))
        & (data["occupation"].astype(str).isin(occupation_filter))
    ]

    filtered_total = len(filtered_data)

    if filtered_total < total:
        st.caption(
            f"Showing **{filtered_total}** of **{total}** respondents based on active filters."
        )

    # ===== DEMOGRAPHICS SECTION =====
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Age Group Distribution")

        age_counts = filtered_data["age"].value_counts()
        age_order = [
            "Under 18",
            "18-24",
            "25-34",
            "35-44",
            "45-54",
            "55 and above",
        ]
        age_counts = age_counts.reindex(
            [a for a in age_order if a in age_counts.index]
        )

        if not age_counts.empty:
            fig = px.bar(
                x=age_counts.values,
                y=age_counts.index,
                orientation="h",
                title="Age Group Counts",
                color=age_counts.values,
                color_continuous_scale=["#5BA3D0", "#003765"],
                text=age_counts.values,
            )
            fig.update_traces(texttemplate="%{text}", textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                xaxis_title="Respondents",
                yaxis_title="",
                showlegend=False,
                height=300,
                margin=dict(l=10, r=40, t=40, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            top_age = age_counts.index[0] if len(age_counts) > 0 else "35-44"
            top_age_cnt = age_counts.iloc[0] if len(age_counts) > 0 else 0
            top_age_pct = (
                round(top_age_cnt / filtered_total * 100, 1)
                if filtered_total > 0
                else 0
            )

            st.markdown(
                f"""
            <div style="margin-top: 8px; padding: 8px 12px; background: #E8F4F8; border-radius: 8px;">
                <span style="font-size: 13px; color: #003765;">
                     <strong>{top_age}</strong> is the primary age group representing <strong>{top_age_cnt}</strong> respondents ({top_age_pct}%).
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No age data available for selected filters.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🚻 Gender Ratio")

        gender_counts = filtered_data["gender"].value_counts()

        if not gender_counts.empty:
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Gender Distribution",
                color_discrete_sequence=["#003765", "#0077AD", "#7CB8D3"],
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
                height=340,
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No gender data available for selected filters.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== OCCUPATION & LOCATION =====
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💼 Top Occupations")

        occ_counts = filtered_data["occupation"].value_counts().head(6)

        if not occ_counts.empty:
            fig = px.bar(
                x=occ_counts.values,
                y=occ_counts.index,
                orientation="h",
                title="Respondents by Occupation",
                color=occ_counts.values,
                color_continuous_scale=["#5BA3D0", "#003765"],
                text=occ_counts.values,
            )
            fig.update_traces(texttemplate="%{text}", textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                xaxis_title="Count",
                yaxis_title="",
                showlegend=False,
                height=300,
                margin=dict(l=10, r=40, t=40, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No occupation data available.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📍 Location Distribution")

        loc_counts = filtered_data["location"].value_counts()

        if not loc_counts.empty:
            fig = px.bar(
                x=loc_counts.index,
                y=loc_counts.values,
                title="Respondents by Location",
                color=loc_counts.values,
                color_continuous_scale=["#5BA3D0", "#003765"],
                text=loc_counts.values,
            )
            fig.update_traces(texttemplate="%{text}", textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                xaxis_title="",
                yaxis_title="Count",
                showlegend=False,
                height=300,
                margin=dict(l=10, r=40, t=40, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No location data available.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== BEHAVIORAL PERSONAS =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">🎭 Customer Behavioral Personas</h4>',
        unsafe_allow_html=True,
    )

    def assign_persona(row):
        if row.get("decision_price", 0) == 1:
            return "Price Sensitive"
        elif (
            row.get("decision_doctor", 0) == 1 or row.get("decision_hmo", 0) == 1
        ):
            return "Doctor/HMO Loyal"
        elif row.get("decision_proximity", 0) == 1:
            return "Convenience Seeker"
        elif (
            row.get("decision_reputation", 0) == 1
            or row.get("decision_experience", 0) == 1
        ):
            return "Quality Driven"
        elif row.get("decision_family", 0) == 1:
            return "Socially Influenced"
        else:
            return "Undifferentiated"

    filtered_data["persona"] = filtered_data.apply(assign_persona, axis=1)
    persona_counts = filtered_data["persona"].value_counts()
    persona_pcts = (
        (persona_counts / len(filtered_data) * 100).round(1)
        if len(filtered_data) > 0
        else {}
    )

    # Calculate NPS per persona
    persona_nps = {}
    for persona in persona_counts.index:
        p_df = filtered_data[filtered_data["persona"] == persona]
        nps_valid = p_df[p_df["nps_score"].notna()]
        if len(nps_valid) > 0:
            p = (nps_valid["nps_segment"] == "Promoter").sum()
            d = (nps_valid["nps_segment"] == "Detractor").sum()
            persona_nps[persona] = round(((p - d) / len(nps_valid) * 100), 1)
        else:
            persona_nps[persona] = None

    persona_icons = {
        "Doctor/HMO Loyal": "🏥",
        "Convenience Seeker": "📍",
        "Quality Driven": "⭐",
        "Socially Influenced": "👥",
        "Price Sensitive": "💰",
        "Undifferentiated": "❓",
    }

    persona_colors = [
        "#003765",
        "#0077AD",
        "#2C8FC7",
        "#5BA3D0",
        "#7CB8D3",
        "#94a3b8",
    ]

    if not persona_counts.empty:
        top_personas = persona_counts.head(4)
        cols = st.columns(min(4, len(top_personas)))

        for i, (persona, count) in enumerate(top_personas.items()):
            if i < len(cols):
                with cols[i]:
                    pct = persona_pcts.get(persona, 0)
                    nps_val = persona_nps.get(persona)
                    nps_display = (
                        f"{nps_val:.1f}" if nps_val is not None else "N/A"
                    )
                    color = (
                        persona_colors[i]
                        if i < len(persona_colors)
                        else "#94a3b8"
                    )

                    st.markdown(
                        f"""
                    <div class="persona-card" style="border-top-color: {color};">
                        <div class="persona-icon">{persona_icons.get(persona, '❓')}</div>
                        <div class="persona-name">{persona}</div>
                        <div class="persona-pct">{pct}%</div>
                        <div class="persona-nps">NPS: <strong>{nps_display}</strong></div>
                        <div class="persona-desc">{count} respondents</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        if len(persona_counts) > 0:
            top_p = persona_counts.index[0]
            top_p_pct = persona_pcts.get(top_p, 0)
            st.markdown(
                f"""
            <div style="margin-top: 12px; padding: 12px 16px; background: #E8F4F8; border-radius: 8px;">
                <span style="font-size: 13px; color: #003765;">
                     <strong>{top_p}</strong> is the primary persona segment at <strong>{top_p_pct}%</strong> of filtered respondents.
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No persona data available for current filters.")

    # ===== INSURANCE ANALYSIS =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">💳 Insurance Coverage Analysis</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Insurance Status Distribution")

        ins_counts = filtered_data["insurance"].value_counts()

        if not ins_counts.empty:
            fig = px.bar(
                x=ins_counts.values,
                y=ins_counts.index,
                orientation="h",
                title="Insurance Type",
                color=ins_counts.values,
                color_continuous_scale=["#5BA3D0", "#003765"],
                text=ins_counts.values,
            )
            fig.update_traces(texttemplate="%{text}", textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                xaxis_title="Count",
                yaxis_title="",
                showlegend=False,
                height=300,
                margin=dict(l=10, r=40, t=40, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No insurance data available.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Awareness & Usage by Insurance")

        ins_behavior = (
            filtered_data.groupby("insurance")
            .agg({
                "aware_synlab": lambda x: (x.sum() / len(x)) * 100,
                "used_synlab": lambda x: (x.sum() / len(x)) * 100,
            })
            .round(1)
            .reset_index()
        )
        ins_behavior.columns = ["Insurance", "Awareness %", "Usage %"]

        if not ins_behavior.empty:
            ins_melted = ins_behavior.melt(
                id_vars=["Insurance"],
                var_name="Metric",
                value_name="Percentage",
            )

            fig = px.bar(
                ins_melted,
                x="Insurance",
                y="Percentage",
                color="Metric",
                title="Awareness vs Usage (%)",
                barmode="group",
                color_discrete_sequence=["#003765", "#0077AD"],
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                xaxis_title="",
                yaxis_title="Percentage (%)",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                ),
                height=300,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No insurance behavior data available.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== LOCATION PERFORMANCE CARDS =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">📍 Location Performance Summary</h4>',
        unsafe_allow_html=True,
    )

    loc_summary = (
        data.groupby("location")
        .agg(
            total=("id", "count"),
            aware=("aware_synlab", "sum"),
            used=("used_synlab", "sum"),
        )
        .reset_index()
    )

    loc_summary["Awareness"] = (
        loc_summary["aware"] / loc_summary["total"] * 100
    ).round(1)
    loc_summary["Usage"] = (
        loc_summary["used"] / loc_summary["total"] * 100
    ).round(1)

    # Compute location NPS
    loc_nps_list = []
    for loc in loc_summary["location"]:
        loc_valid = data[
            (data["location"] == loc) & (data["nps_score"].notna())
        ]
        if len(loc_valid) > 0:
            p = (loc_valid["nps_segment"] == "Promoter").sum()
            d = (loc_valid["nps_segment"] == "Detractor").sum()
            loc_nps_list.append(round(((p - d) / len(loc_valid) * 100), 1))
        else:
            loc_nps_list.append(0.0)

    loc_summary["NPS"] = loc_nps_list
    loc_summary = loc_summary.sort_values("total", ascending=False).head(5)

    cols = st.columns(len(loc_summary))

    for i, (_, row) in enumerate(loc_summary.iterrows()):
        with cols[i]:
            nps_col = "#003765" if row["NPS"] >= 0 else "#2C8FC7"
            st.markdown(
                f"""
            <div class="location-card" style="border-top-color: {nps_col};">
                <div class="loc-name">{row['location']}</div>
                <div class="loc-value">{row['Awareness']}%</div>
                <div class="loc-label">Awareness</div>
                <div style="margin: 4px 0;"></div>
                <div class="loc-value" style="font-size: 18px; color: {nps_col};">{row['Usage']}%</div>
                <div class="loc-label">Usage</div>
                <div style="margin: 4px 0;"></div>
                <div class="loc-value" style="font-size: 15px; color: {nps_col};">NPS: {row['NPS']:.1f}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ===== INSIGHTS SECTION =====
    st.markdown("---")
    st.markdown(
        '<p style="font-size: 16px; font-weight: 600; color: #003765; margin: 0 0 16px 0;">💡 Customer Segment Insights</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="insight-card">
            <div class="insight-number">01</div>
            <div class="insight-title">Primary Age Group</div>
            <div class="insight-desc">
                <strong>35–44 years</strong> represents <strong>57.6%</strong> (287) of total respondents — focus corporate checkup packages on this age group.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="insight-card">
            <div class="insight-number">02</div>
            <div class="insight-title">Dominant Persona</div>
            <div class="insight-desc">
                <strong>Doctor/HMO Loyal</strong> makes up <strong>53.8%</strong> (268) of respondents — physician referrals remain the key conversion channel.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="insight-card">
            <div class="insight-number">03</div>
            <div class="insight-title">Largest Location</div>
            <div class="insight-desc">
                <strong>Asokoro</strong> represents 121 respondents (24.3%), but shows lower usage (24.8%) compared to awareness (48.8%).
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
        <div class="insight-card">
            <div class="insight-number">04</div>
            <div class="insight-title">Gender Balance</div>
            <div class="insight-desc">
                Respondents comprise <strong>54.0% Male</strong> (269) and <strong>44.8% Female</strong> (223) — tailored messaging across gender segments is recommended.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== NAVIGATION =====
    st.markdown("---")

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

    with nav_col1:
        if st.button("🏠 Cover", use_container_width=True, key="ins_to_cover"):
            st.switch_page("app.py")

    with nav_col2:
        if st.button(
            "📈 Overview", use_container_width=True, key="ins_to_overview"
        ):
            st.switch_page("pages/1_Executive_Overview.py")

    with nav_col3:
        if st.button("🏷️ Brand Health", use_container_width=True, key="ins_to_brand"):
            st.switch_page("pages/2_Brand_Health.py")

    with nav_col4:
        st.button(
            "👥 Insights",
            use_container_width=True,
            key="ins_active",
            disabled=True,
        )

    with nav_col5:
        if st.button(
            "⚔️ Competitive", use_container_width=True, key="ins_to_comp"
        ):
            st.switch_page("pages/4_Competitive_Intelligence.py")

    with nav_col6:
        if st.button(
            "💡 Strategic", use_container_width=True, key="ins_to_strategic"
        ):
            st.switch_page("pages/5_Strategic_Analytics.py")


if __name__ == "__main__":
    show()
