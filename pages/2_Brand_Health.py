# pages/2_Brand_Health.py
import os
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Brand Health · SYNLAB Nigeria",
    page_icon="assets/synlab_logo.png",
    layout="wide", 
    initial_sidebar_state="collapsed",
)

def normalize_lab_name(name):
    """Clean and standardize laboratory names"""
    if pd.isna(name):
        return None

    name_lower = str(name).lower().strip()
    name_lower = re.sub(
        r"(medical|diagnostics|laboratory|lab|centre|center|healthcare|services|limited|ltd|diagnostic|nigeria|nigerian)",
        "",
        name_lower,
    )
    name_lower = re.sub(r"[^a-z0-9\s]", "", name_lower).strip()

    lab_mapping = {
        "synlab": "SYNLAB Nigeria",
        "clinix": "Clinix",
        "eco scan": "Eco/Echo Lab",
        "ecolab": "Eco/Echo Lab",
        "echo lab": "Eco/Echo Lab",
        "eco lab": "Eco/Echo Lab",
        "echolab": "Eco/Echo Lab",
        "eco": "Eco/Echo Lab",
        "echo": "Eco/Echo Lab",
        "mecure": "Mecure Healthcare",
        "me cure": "Mecure Healthcare",
        "clina lancet": "Clina Lancet",
        "clina": "Clina Lancet",
        "lancet": "Clina Lancet",
        "afriglobal": "Afriglobal Medicare",
        "eclinic": "E-Clinic & Diagnostics",
        "amce": "AMCE",
        "lifebridge": "Lifebridge Medical Diagnostics",
        "firmcare": "Firmcare Diagnostics",
        "apin": "APIN Medical Laboratory",
        "lab360": "LAB360",
        "pseven": "Pseven Medical Diagnostics",
    }

    for key, value in lab_mapping.items():
        if key in name_lower:
            return value

    return str(name).strip()


def show():
    """Render the Brand Health page"""

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

        /* SIDE-BY-SIDE HORIZONTAL FUNNEL CONTAINER */
        .funnel-container {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 24px;
        }

        .funnel-row-horizontal {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            gap: 12px;
            padding: 12px 0;
        }

        .funnel-step-box {
            flex: 1;
            text-align: center;
            padding: 20px 16px;
            border-radius: 12px;
            color: white;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: transform 0.2s ease;
        }

        .funnel-step-box:hover {
            transform: translateY(-2px);
        }

        .funnel-step-box .count {
            font-size: 32px;
            font-weight: 800;
            line-height: 1.1;
        }
        .funnel-step-box .pct {
            font-size: 15px;
            font-weight: 700;
            margin-top: 4px;
            opacity: 0.95;
        }
        .funnel-step-box .label {
            font-size: 13px;
            opacity: 0.85;
            margin-top: 2px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        /* Step Color Gradients */
        .step-1 { background: linear-gradient(135deg, #002647 0%, #003765 100%); }
        .step-2 { background: linear-gradient(135deg, #005680 0%, #0077AD 100%); }
        .step-3 { background: linear-gradient(135deg, #1E6B9E 0%, #2C8FC7 100%); }
        .step-4 { background: linear-gradient(135deg, #4295C2 0%, #5BA3D0 100%); color: #002647 !important; }

        .funnel-connector-arrow {
            font-size: 24px;
            color: #0077AD;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            padding: 0 4px;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-attention { background: #E8F4F8; color: #003765; border: 1px solid #7CB8D3; }

        .sentiment-quote {
            background: #E8F4F8;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 6px 0;
            border-left: 3px solid #0077AD;
            font-style: italic;
            color: #475569;
            font-size: 13px;
        }

        .tom-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0;
            border-bottom: 1px solid #f1f5f9;
        }
        .tom-item .lab-name { font-size: 14px; }
        .tom-item .lab-pct { font-size: 13px; color: #64748b; }
        .tom-bar { height: 4px; border-radius: 2px; margin-top: 2px; }

        @media (max-width: 850px) {
            .funnel-row-horizontal {
                flex-direction: column;
            }
            .funnel-connector-arrow {
                transform: rotate(90deg);
                margin: 4px 0;
            }
            .funnel-step-box {
                width: 100%;
            }
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

    # ===== PAGE HEADER =====
    st.markdown(
        """
    <div class="page-header">
        <h1>🏷️ Brand Health & Awareness</h1>
        <p>SYNLAB brand funnel, perception, NPS distribution, and CX performance</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== SIDE-BY-SIDE BRAND FUNNEL =====
    st.markdown('<div class="funnel-container">', unsafe_allow_html=True)
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 16px 0;">📊 Brand Funnel Conversion (Side-by-Side)</h4>',
        unsafe_allow_html=True,
    )

    funnel_steps = [
        {
            "label": "Total Surveyed",
            "count": total,
            "pct": "100%",
            "step": "step-1",
        },
        {
            "label": "Brand Aware",
            "count": aware,
            "pct": f"{round(aware/total*100, 1)}%",
            "step": "step-2",
        },
        {
            "label": "Active Usage",
            "count": used,
            "pct": f"{round(used/total*100, 1)}%",
            "step": "step-3",
        },
        {
            "label": "Promoters",
            "count": promoters,
            "pct": f"{round(promoters/total*100, 1)}%",
            "step": "step-4",
        },
    ]

    # Render Side-by-Side Horizontal Layout
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
            funnel_html += (
                '<div class="funnel-connector-arrow">&#10142;</div>'
            )
    funnel_html += "</div>"

    st.markdown(funnel_html, unsafe_allow_html=True)

    aware_to_used_dropoff = (
        round((aware - used) / aware * 100, 1) if aware > 0 else 0
    )
    used_to_promoters_dropoff = (
        round((used - promoters) / used * 100, 1) if used > 0 else 0
    )

    st.markdown(
        f"""
    <div style="display: flex; gap: 32px; justify-content: center; margin-top: 16px; flex-wrap: wrap;">
        <span style="font-size: 13px; color: #003765; font-weight: 600;">⚠️ <strong>{aware_to_used_dropoff}% Drop-off</strong> (Aware → Used)</span>
        <span style="font-size: 13px; color: #003765; font-weight: 600;">⚠️ <strong>{used_to_promoters_dropoff}% Drop-off</strong> (Used → Promoters)</span>
    </div>
    <div style="margin-top: 12px; padding: 12px 16px; background: #E8F4F8; border-radius: 8px; text-align: center;">
        <span style="font-size: 13px; color: #003765;">💡 <strong>Conversion Opportunity:</strong> 60 aware respondents have not utilized SYNLAB (12.0% total awareness-to-usage gap).</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== AWARENESS & NPS SECTION =====
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🔍 Awareness Breakdown")

        if "top_of_mind_lab" in data.columns:
            tom_mentions = data["top_of_mind_lab"].dropna().str.lower()
            synlab_mentions = tom_mentions[
                tom_mentions.str.contains("synlab", na=False)
            ].count()
            unaided_pct = round(synlab_mentions / total * 100, 1)
        else:
            unaided_pct = 0.0

        aided_pct = round(aware / total * 100, 1)

        awareness_df = pd.DataFrame({
            "Type": ["Unaided (Top of Mind)", "Aided Awareness"],
            "Percentage": [unaided_pct, aided_pct],
        })

        fig = px.bar(
            awareness_df,
            x="Percentage",
            y="Type",
            orientation="h",
            title="Unaided vs. Aided Brand Awareness",
            color="Percentage",
            color_continuous_scale=["#5BA3D0", "#003765"],
            text="Percentage",
        )
        fig.update_traces(
            texttemplate="%{text:.1f}%", textposition="outside", width=0.4
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(range=[0, 70]),
            showlegend=False,
            height=180,
            margin=dict(l=10, r=40, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**🏆 Top of Mind Mentions (Unaided)**")

        if "top_of_mind_lab" in data.columns:
            data["top_of_mind_clean"] = data["top_of_mind_lab"].apply(
                normalize_lab_name
            )
            tom_freq = (
                data["top_of_mind_clean"].dropna().value_counts().head(4)
            )

            if not tom_freq.empty:
                colors = ["#003765", "#0077AD", "#2C8FC7", "#5BA3D0"]
                max_count = tom_freq.iloc[0]

                for i, (lab, count) in enumerate(tom_freq.items()):
                    is_synlab = "synlab" in str(lab).lower()
                    color = colors[i] if i < len(colors) else "#64748b"
                    weight = "bold" if is_synlab else "normal"
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
        st.subheader("⭐ Net Promoter Score (NPS)")

        st.markdown(
            f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px;">
            <div style="background: #003765; border-radius: 8px; padding: 12px; text-align: center; color: white;">
                <div style="font-size: 20px; font-weight: 700;">{promoter_pct:.1f}%</div>
                <div style="font-size: 11px; opacity: 0.85;">Promoters ({promoters})</div>
            </div>
            <div style="background: #2C8FC7; border-radius: 8px; padding: 12px; text-align: center; color: white;">
                <div style="font-size: 20px; font-weight: 700;">{passive_pct:.1f}%</div>
                <div style="font-size: 11px; opacity: 0.85;">Passives ({passives})</div>
            </div>
            <div style="background: #7CB8D3; border-radius: 8px; padding: 12px; text-align: center; color: #003765;">
                <div style="font-size: 20px; font-weight: 700;">{detractor_pct:.1f}%</div>
                <div style="font-size: 11px; opacity: 0.85;">Detractors ({detractors})</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background: #E8F4F8; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;">
            <div>
                <div style="font-size: 12px; color: #64748b; font-weight: 600;">NET PROMOTER SCORE</div>
                <div style="font-size: 28px; font-weight: 700; color: #003765;">{nps:.1f}</div>
            </div>
            <div>
                <span class="status-badge status-attention">Needs Attention</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div style="padding: 10px 16px; background: #E8F4F8; border-radius: 8px;">
            <span style="font-size: 13px; color: #003765;">💡 <strong>Key Opportunity:</strong> Converting <strong>{passives} Passives</strong> (33.5%) into Promoters will elevate the overall NPS score above zero.</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== NPS PER LOCATION =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">📍 NPS Performance by Location</h4>',
        unsafe_allow_html=True,
    )

    locations = ["Wuse", "Gwarimpa", "Gwagwalada", "Lugbe", "Asokoro", "Kubwa"]
    location_nps = []

    for loc in locations:
        loc_data = data[data["location"] == loc]
        loc_nps_valid = loc_data[loc_data["nps_score"].notna()]
        loc_total = len(loc_nps_valid)

        if loc_total > 0:
            loc_p = (loc_nps_valid["nps_segment"] == "Promoter").sum()
            loc_d = (loc_nps_valid["nps_segment"] == "Detractor").sum()
            loc_nps_score = round(((loc_p - loc_d) / loc_total * 100), 1)
        else:
            loc_nps_score = 0.0

        loc_aware = (
            round((loc_data["aware_synlab"].sum() / len(loc_data) * 100), 1)
            if len(loc_data) > 0
            else 0.0
        )

        location_nps.append({
            "Location": loc,
            "NPS": loc_nps_score,
            "Respondents": loc_total,
            "Awareness": loc_aware,
        })

    loc_nps_df = pd.DataFrame(location_nps)
    cols = st.columns(len(locations))

    for i, row in loc_nps_df.iterrows():
        with cols[i]:
            color = "#003765" if row["NPS"] >= 0 else "#2C8FC7"
            st.markdown(
                f"""
            <div style="background: white; border-radius: 12px; padding: 14px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-top: 4px solid {color};">
                <div style="font-size: 13px; color: #64748b; font-weight: 600;">{row['Location']}</div>
                <div style="font-size: 24px; font-weight: 700; color: {color};">{row['NPS']:.1f}</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">
                    {row['Respondents']} valid · {row['Awareness']}% aware
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ===== CX METRICS RADAR =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">📈 Customer Experience (CX) Ratings</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    cx_cols = {
        "cx_access": "Access",
        "cx_wait_time": "Wait Time",
        "cx_professionalism": "Professionalism",
        "cx_communication": "Communication",
        "cx_result_speed": "Result Speed",
        "cx_accuracy": "Accuracy",
        "cx_digital": "Digital Experience",
        "cx_value": "Value for Money",
    }

    score_map = {
        "Very dissatisfied": 1,
        "Dissatisfied": 2,
        "Neutral": 3,
        "Satisfied": 4,
        "Very satisfied": 5,
    }

    cx_scores = []
    for col, label in cx_cols.items():
        if col in data.columns:
            scores = data[col].map(score_map).dropna()
            avg = scores.mean() if len(scores) > 0 else 0
            cx_scores.append({"Metric": label, "Score": round(avg, 2)})

    cx_df = pd.DataFrame(cx_scores)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if not cx_df.empty:
            fig = go.Figure()
            fig.add_trace(
                go.Scatterpolar(
                    r=cx_df["Score"].tolist(),
                    theta=cx_df["Metric"].tolist(),
                    fill="toself",
                    name="SYNLAB CX",
                    line_color="#0077AD",
                    fillcolor="rgba(0, 119, 173, 0.2)",
                    line_width=2,
                )
            )

            fig.update_layout(
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
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 CX Summary")

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
                    <div style="background: #E8F4F8; border-radius: 4px; height: 4px; overflow: hidden;">
                        <div style="background: #0077AD; width: {pct}%; height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            best = cx_sorted.iloc[0]
            worst = cx_sorted.iloc[-1]
            st.markdown(
                f"""
            <div style="margin-top: 12px; padding: 10px; background: #E8F4F8; border-radius: 8px;">
                <div style="font-size: 12px; color: #003765;">💪 <strong>Highest Rating:</strong> {best['Metric']} ({best['Score']:.2f}/5)</div>
                <div style="font-size: 12px; color: #003765;">⚠️ <strong>Improvement Area:</strong> {worst['Metric']} ({worst['Score']:.2f}/5)</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== SENTIMENT ANALYSIS =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;">💬 Qualitative Customer Feedback</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📝 Open-Ended Feedback Quotes")

        st.markdown(
            """
        <div class="sentiment-quote positive">💚 "SYNLAB Nigeria they are the best in accuracy and diagnostics"</div>
        <div class="sentiment-quote positive">💚 "The staff are friendly, no delays in attending to people"</div>
        <div class="sentiment-quote positive">💚 "Professional team and clean laboratory environment"</div>
        <div class="sentiment-quote positive">💚 "High accuracy of results and reliable health reports"</div>
        <div class="sentiment-quote neutral">🟡 "I have heard good reviews about them through referrals"</div>
        <div class="sentiment-quote negative">🔴 "The service pricing is too expensive for routine checkups"</div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Sentiment Drivers")

        st.markdown(
            """
        <div style="padding: 12px; background: #E8F4F8; border-radius: 8px;">
            <div style="font-size: 13px; color: #003765; font-weight: 600; margin-bottom: 6px;">💡 Primary Mentions</div>
            <div style="font-size: 13px; color: #475569; line-height: 1.8;">
                • Diagnostic Accuracy ⭐ (High)<br>
                • Service Quality 💬 (High)<br>
                • Pricing Concerns 💰 (Moderate)<br>
                • Digital Access 📱 (Opportunity)
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== NAVIGATION =====
    st.markdown("---")

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

    with nav_col1:
        if st.button("🏠 Cover", use_container_width=True, key="brand_to_cover"):
            st.switch_page("app.py")

    with nav_col2:
        if st.button(
            "📈 Overview", use_container_width=True, key="brand_to_overview"
        ):
            st.switch_page("pages/1_Executive_Overview.py")

    with nav_col3:
        st.button(
            "🏷️ Brand Health",
            use_container_width=True,
            key="brand_active",
            disabled=True,
        )

    with nav_col4:
        if st.button(
            "👥 Insights", use_container_width=True, key="brand_to_insights"
        ):
            st.switch_page("pages/3_Customer_Insights.py")

    with nav_col5:
        if st.button(
            "⚔️ Competitive", use_container_width=True, key="brand_to_comp"
        ):
            st.switch_page("pages/4_Competitive_Intelligence.py")

    with nav_col6:
        if st.button(
            "💡 Strategic", use_container_width=True, key="brand_to_strategic"
        ):
            st.switch_page("pages/5_Strategic_Analytics.py")


if __name__ == "__main__":
    show()
