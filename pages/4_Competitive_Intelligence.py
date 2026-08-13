# pages/4_Competitive_Intelligence.py
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Competitive Intelligence · SYNLAB Nigeria",
    page_icon="assets/synlab_logo.png",
    layout="wide",  # <--- THIS KEEPS THE PAGE WIDE ON RELOAD
    initial_sidebar_state="collapsed",
)

def show():
    """Render the Competitive Intelligence page"""

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

        .threat-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-top: 4px solid #003765;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .threat-card .comp-name { font-weight: 700; color: #003765; font-size: 16px; }
        .threat-card .comp-score { font-weight: 800; font-size: 22px; color: #0077AD; margin: 4px 0; }
        .threat-card .comp-desc { font-size: 13px; color: #475569; line-height: 1.5; margin-top: 8px; }

        /* STANDARDIZED SWOT CARDS */
        .swot-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 12px;
        }
        .swot-card {
            border-radius: 12px;
            padding: 20px 24px;
            min-height: 220px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        .swot-card h4 {
            margin: 0 0 12px 0;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .swot-card ul {
            margin: 0;
            padding-left: 20px;
            font-size: 13px;
            line-height: 1.6;
            flex-grow: 1;
        }
        .swot-card li {
            margin-bottom: 8px;
        }

        .swot-strengths { background: #003765; color: white; }
        .swot-weaknesses { background: #5BA3D0; color: #003765; }
        .swot-opportunities { background: #0077AD; color: white; }
        .swot-threats { background: #7CB8D3; color: #003765; }

        .threat-item-mini {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            border-bottom: 1px solid #f1f5f9;
        }
        .threat-item-mini .threat-name { font-weight: 600; color: #003765; font-size: 13px; }
        .threat-item-mini .threat-score { font-weight: 700; font-size: 13px; }

        @media (max-width: 768px) {
            .main > div { padding: 0 16px !important; }
            .page-header { padding: 16px 20px; }
            .page-header h1 { font-size: 22px; }
            .swot-grid { grid-template-columns: 1fr; }
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

    total = len(data)

    competitors = [
        {
            "id": "synlab",
            "name": "SYNLAB Nigeria",
            "aware_col": "aware_synlab",
            "used_col": "used_synlab",
        },
        {
            "id": "lifebridge",
            "name": "Lifebridge Medical",
            "aware_col": "aware_lifebridge",
            "used_col": "used_lifebridge",
        },
        {
            "id": "eclinic",
            "name": "E-Clinic & Diagnostics",
            "aware_col": "aware_eclinic",
            "used_col": "used_eclinic",
        },
        {
            "id": "firmcare",
            "name": "Firmcare Diagnostics",
            "aware_col": "aware_firmcare",
            "used_col": "used_firmcare",
        },
        {
            "id": "mecure",
            "name": "Mecure Healthcare",
            "aware_col": "aware_mecure",
            "used_col": "used_mecure",
        },
        {
            "id": "clinix",
            "name": "Clinix Diagnostics",
            "aware_col": "aware_clinix",
            "used_col": "used_clinix",
        },
        {
            "id": "lab360",
            "name": "LAB360",
            "aware_col": "aware_lab360",
            "used_col": "used_lab360",
        },
        {
            "id": "apin",
            "name": "APIN Medical Lab",
            "aware_col": "aware_apin",
            "used_col": "used_apin",
        },
        {
            "id": "afriglobal",
            "name": "Afriglobal Medicare",
            "aware_col": "aware_afriglobal",
            "used_col": "used_afriglobal",
        },
        {
            "id": "clina",
            "name": "Clina Lancet",
            "aware_col": "aware_clina_lancet",
            "used_col": "used_clina_lancet",
        },
        {
            "id": "amce",
            "name": "AMCE",
            "aware_col": "aware_amce",
            "used_col": "used_amce",
        },
    ]

    comp_data = []
    for comp in competitors:
        aware_count = (
            data[comp["aware_col"]].sum()
            if comp["aware_col"] in data.columns
            else 0
        )
        used_count = (
            data[comp["used_col"]].sum()
            if comp["used_col"] in data.columns
            else 0
        )

        aware_pct = round(aware_count / total * 100, 1) if total > 0 else 0
        used_pct = round(used_count / total * 100, 1) if total > 0 else 0
        conversion = (
            round(used_count / aware_count * 100, 1) if aware_count > 0 else 0
        )

        threat = round((aware_pct * 0.4) + (used_pct * 0.6), 1)

        comp_data.append({
            "id": comp["id"],
            "name": comp["name"],
            "awareness": aware_pct,
            "usage": used_pct,
            "conversion": conversion,
            "threat": threat,
            "is_synlab": comp["id"] == "synlab",
        })

    comp_df = pd.DataFrame(comp_data)
    comp_df_sorted = comp_df.sort_values("usage", ascending=False)

    # ===== PAGE HEADER =====
    st.markdown(
        """
    <div class="page-header">
        <h1> Competitive Intelligence</h1>
        <p>Market share, perceived quality vs. pricing positioning, and strategic threat analysis</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== MARKET SHARE (USAGE) =====
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;"> Market Usage Share (%)</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        fig = px.bar(
            comp_df_sorted,
            x="name",
            y="usage",
            title="Laboratory Usage Rates in Abuja Market (%)",
            color="usage",
            color_continuous_scale=["#5BA3D0", "#003765"],
            text="usage",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            yaxis_title="Usage Rate (%)",
            showlegend=False,
            height=380,
            margin=dict(l=10, r=40, t=40, b=60),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader(" Market Leader")

        top = comp_df_sorted.iloc[0]
        second = comp_df_sorted.iloc[1]
        gap = top["usage"] - second["usage"]

        st.markdown(
            f"""
        <div style="text-align: center; padding: 12px 0;">
            <div style="font-size: 40px; margin-bottom: 4px;"></div>
            <div style="font-size: 18px; font-weight: 700; color: #003765;">{top['name']}</div>
            <div style="font-size: 32px; font-weight: 800; color: #0077AD; margin: 4px 0;">{top['usage']}%</div>
            <div style="font-size: 12px; color: #64748b;">Market Usage Rate</div>
            <div style="margin-top: 12px; padding: 10px; background: #E8F4F8; border-radius: 8px;">
                <span style="font-size: 12px; color: #003765;">
                    <strong>Leadership Margin:</strong> SYNLAB leads by <strong>+{gap:.1f}%</strong> over {second['name']} ({second['usage']}%).
                </span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== AWARENESS VS USAGE MATRIX WITH ARROWS =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;"> Competitive Positioning Matrix</h4>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Awareness vs. Usage Scatter Matrix (Clustered Callouts)")

        fig = go.Figure()

        label_offsets = {
            "SYNLAB Nigeria": {"ax": 0, "ay": -40},
            "Lifebridge Medical": {"ax": 45, "ay": -25},
            "E-Clinic & Diagnostics": {"ax": 50, "ay": 25},
            "Mecure Healthcare": {"ax": -50, "ay": -25},
            "Firmcare Diagnostics": {"ax": -45, "ay": 25},
            "Clinix Diagnostics": {"ax": 45, "ay": -15},
            "LAB360": {"ax": -35, "ay": -30},
            "APIN Medical Lab": {"ax": -45, "ay": 20},
            "Afriglobal Medicare": {"ax": -40, "ay": 35},
            "Clina Lancet": {"ax": 35, "ay": 35},
            "AMCE": {"ax": 40, "ay": 40},
        }

        for _, row in comp_df.iterrows():
            color = "#003765" if row["is_synlab"] else "#0077AD"
            size = 20 if row["is_synlab"] else 12
            symbol = "star" if row["is_synlab"] else "circle"

            fig.add_trace(
                go.Scatter(
                    x=[row["awareness"]],
                    y=[row["usage"]],
                    mode="markers",
                    marker=dict(
                        size=size,
                        color=color,
                        symbol=symbol,
                        line=dict(width=1, color="white"),
                    ),
                    name=row["name"],
                    hovertemplate=f"<b>{row['name']}</b><br>Awareness: {row['awareness']}%<br>Usage: {row['usage']}%<extra></extra>",
                )
            )

            offset = label_offsets.get(
                row["name"], {"ax": 20, "ay": -20}
            )

            fig.add_annotation(
                x=row["awareness"],
                y=row["usage"],
                text=f"<b>{row['name']}</b>",
                showarrow=True,
                arrowhead=2,
                arrowsize=0.8,
                arrowwidth=1.2,
                arrowcolor="#003765" if row["is_synlab"] else "#64748b",
                ax=offset["ax"],
                ay=offset["ay"],
                font=dict(
                    size=10,
                    color="#003765" if row["is_synlab"] else "#334155",
                ),
                bgcolor="rgba(255, 255, 255, 0.85)",
                bordercolor="rgba(0, 119, 173, 0.3)"
                if row["is_synlab"]
                else "rgba(0,0,0,0.1)",
                borderwidth=1,
                borderpad=3,
            )

        avg_aware = comp_df["awareness"].mean()
        avg_usage = comp_df["usage"].mean()

        fig.add_shape(
            type="line",
            x0=avg_aware,
            y0=0,
            x1=avg_aware,
            y1=50,
            line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"),
        )
        fig.add_shape(
            type="line",
            x0=0,
            y0=avg_usage,
            x1=60,
            y1=avg_usage,
            line=dict(color="rgba(0,0,0,0.15)", width=1, dash="dash"),
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="Brand Awareness (%)",
            yaxis_title="Market Usage (%)",
            xaxis=dict(range=[-2, 60]),
            yaxis=dict(range=[-2, 48]),
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader(" Conversion Efficiency (%)")

        fig = px.bar(
            comp_df_sorted,
            x="name",
            y="conversion",
            title="Awareness → Usage Conversion Efficiency (%)",
            color="conversion",
            color_continuous_scale=["#5BA3D0", "#003765"],
            text="conversion",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#003765",
            xaxis_title="",
            yaxis_title="Conversion Rate (%)",
            showlegend=False,
            height=200,
            margin=dict(l=10, r=40, t=40, b=60),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(" Threat Score Ranking")
        threat_df = (
            comp_df_sorted[comp_df_sorted["is_synlab"] == False]
            .sort_values("threat", ascending=False)
            .head(4)
        )

        for i, (_, row) in enumerate(threat_df.iterrows()):
            color = "#003765" if i == 0 else "#0077AD" if i == 1 else "#2C8FC7"

            st.markdown(
                f"""
            <div class="threat-item-mini">
                <span class="threat-name">{i+1}. {row['name']}</span>
                <span class="threat-score" style="color: {color};">Threat Score: {row['threat']:.1f} (Usage: {row['usage']}%)</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # =====  PERCEIVED QUALITY VS. PRICING =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;"> Perceived Quality vs. Pricing Positioning</h4>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Perceived Quality vs. Pricing Matrix")

    perf_map = {
        "Much worse": 1,
        "Worse": 2,
        "About the same": 3,
        "Better": 4,
        "Much better": 5,
    }

    if "perf_quality" in data.columns and "perf_pricing" in data.columns:
        data["q_score"] = data["perf_quality"].map(perf_map)
        data["p_score"] = data["perf_pricing"].map(perf_map)

        pos_data = []
        for comp in competitors:
            if comp["used_col"] in data.columns:
                sub = data[data[comp["used_col"]] == 1]
                valid_sub = sub[
                    sub["q_score"].notna() & sub["p_score"].notna()
                ]
                n_count = len(valid_sub)

                if n_count >= 5:
                    avg_q = valid_sub["q_score"].mean()
                    avg_p = valid_sub["p_score"].mean()
                    pos_data.append({
                        "id": comp["id"],
                        "name": comp["name"],
                        "price": round(avg_p, 2),
                        "quality": round(avg_q, 2),
                        "n": n_count,
                        "is_synlab": comp["id"] == "synlab",
                    })

        pos_df = pd.DataFrame(pos_data)

        if len(pos_df) > 0:
            fig = px.scatter(
                pos_df,
                x="price",
                y="quality",
                text="name",
                size="n",
                color="is_synlab",
                color_discrete_map={True: "#003765", False: "#5BA3D0"},
                size_max=36,
            )
            fig.update_traces(textposition="top center")
            fig.add_hline(y=3.0, line_dash="dot", line_color="#94a3b8")
            fig.add_vline(x=3.0, line_dash="dot", line_color="#94a3b8")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#003765",
                xaxis_title="Perceived pricing vs. other labs (1=much worse, 5=much better)",
                yaxis_title="Perceived quality vs. other labs (1=much worse, 5=much better)",
                xaxis=dict(range=[2.5, 5.0]),
                yaxis=dict(range=[2.5, 5.2]),
                showlegend=False,
                height=420,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption(
                "Based on each brand's own users comparing it to the other lab. SYNLAB Nigeria is perceived to have good quality with matching pricing having both pricing nd qulaity on ≥ 4."
            )
        else:
            st.info(
                "Not enough paired quality/pricing responses per competitor to plot this reliably."
            )
    else:
        st.info("Quality and pricing comparative fields are not available.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== TOP THREE THREATS CLEARLY IDENTIFIED & EXPLAINED =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;"> Top Three Competitive Threats & Deep-Dive Analysis</h4>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="threat-card" style="border-top-color: #003765;">
            <div>
                <div style="font-size: 11px; color: #0077AD; font-weight: 700; text-transform: uppercase;">THREAT #1 · HIGH CONVERSION NICHE</div>
                <div class="comp-name">Lifebridge Medical</div>
                <div class="comp-score">Threat Score: 11.6</div>
                <div style="font-size: 12px; color: #64748b;">12.0% Usage · 11.0% Awareness · 109.1% Conversion</div>
                <div class="comp-desc">
                    <strong>Why it's a big threat:</strong> Lifebridge shows an extraordinary conversion efficiency (>100%), indicating powerful doctor/HMO referral networks in Abuja. They capture high repeat clinical usage despite low brand marketing visibility[cite: 4].
                </div>
            </div>
            <div style="margin-top: 12px; padding: 8px; background: #E8F4F8; border-radius: 6px; font-size: 11px; color: #003765;">
                <strong>Strategic Counter:</strong> Leveraging more on physician engagement, HMO  and more business partnership retention in Abuja core locations.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="threat-card" style="border-top-color: #0077AD;">
            <div>
                <div style="font-size: 11px; color: #0077AD; font-weight: 700; text-transform: uppercase;">THREAT #2 · DIGITAL EXPANSION</div>
                <div class="comp-name">E-Clinic & Diagnostics</div>
                <div class="comp-score">Threat Score: 11.5</div>
                <div style="font-size: 12px; color: #64748b;">9.4% Usage · 14.7% Awareness · 64.4% Conversion</div>
                <div class="comp-desc">
                    <strong>Why it's a big threat:</strong> E-Clinic holds the 2nd highest brand awareness in Abuja (14.7%). Their digital-first patient portal and mobile booking capture younger, tech-savvy demographics and price-conscious retail users.
                </div>
            </div>
            <div style="margin-top: 12px; padding: 8px; background: #E8F4F8; border-radius: 6px; font-size: 11px; color: #003765;">
                <strong>Strategic Counter:</strong> Improving SYNLAB's patient mobile and digital report delivery experience.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="threat-card" style="border-top-color: #2C8FC7;">
            <div>
                <div style="font-size: 11px; color: #0077AD; font-weight: 700; text-transform: uppercase;">THREAT #3 · RETAIL VALUE</div>
                <div class="comp-name">Mecure Healthcare</div>
                <div class="comp-score">Threat Score: 7.8</div>
                <div style="font-size: 12px; color: #64748b;">6.0% Usage · 10.6% Awareness · 56.6% Conversion</div>
                <div class="comp-desc">
                    <strong>Why it's a big threat:</strong> Mecure leverages aggressive pricing and established brand equity across diagnostics. They compete directly on routine health check packages, drawing away price-sensitive walk-in patients.
                </div>
            </div>
            <div style="margin-top: 12px; padding: 8px; background: #E8F4F8; border-radius: 6px; font-size: 11px; color: #003765;">
                 <strong>Strategic Counter:</strong> Introducing more structured wellness packages priced within the ₦50,000 band.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== STANDARDIZED SWOT BOXES =====
    st.markdown("---")
    st.markdown(
        '<h4 style="color: #003765; margin: 0 0 12px 0;"> Standardized Strategic SWOT Matrix</h4>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="swot-grid">
        <div class="swot-card swot-strengths">
            <h4> STRENGTHS</h4>
            <ul>
                <li>Highest market brand awareness in Abuja (54.2%)</li>
                <li>Dominant market usage leader at 42.2%</li>
                <li>Best conversion efficiency (77.8% awareness to active usage)</li>
                <li>High impression rating (3.90/5) with clinical accuracy perception</li>
            </ul>
        </div>
        <div class="swot-card swot-weaknesses">
            <h4> WEAKNESSES</h4>
            <ul>
                <li>Net Promoter Score (-5.2) driven by 35.9% detractors</li>
                <li>Digital experience score (3.90/5) lags physical laboratory rating</li>
                <li>Wait times and turnaround speed noted in feedback</li>
                <li>Perception of premium pricing creates barrier for walk-ins</li>
            </ul>
        </div>
        <div class="swot-card swot-opportunities">
            <h4> OPPORTUNITIES</h4>
            <ul>
                <li>12.0% awareness-to-usage gap (60 conversion-ready prospects</li>
                <li>Corporate wellness checkup packages for 35–44 age bracket (57.6%)</li>
                <li>Digital portal expansion for online booking and instant results</li>
                <li>Expanded physician referral programs in Wuse and Asokoro</li>
            </ul>
        </div>
        <div class="swot-card swot-threats">
            <h4> THREATS</h4>
            <ul>
                <li>Lifebridge Medical's referral conversion network (12.0% usage)</li>
                <li>E-Clinic gaining traction in digital diagnostics (14.7% awareness)</li>
                <li>Mecure offering aggressive pricing on routine health packages</li>
                <li>Increasing price sensitivity among out-of-pocket patients</li>
            </ul>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ===== NAVIGATION =====
    st.markdown("---")

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

    with nav_col1:
        if st.button("🏠 Cover", use_container_width=True, key="comp_to_cover"):
            st.switch_page("app.py")

    with nav_col2:
        if st.button(
            "📈 Overview", use_container_width=True, key="comp_to_overview"
        ):
            st.switch_page("pages/1_Executive_Overview.py")

    with nav_col3:
        if st.button("🏷️ Brand Health", use_container_width=True, key="comp_to_brand"):
            st.switch_page("pages/2_Brand_Health.py")

    with nav_col4:
        if st.button(
            "👥 Insights", use_container_width=True, key="comp_to_insights"
        ):
            st.switch_page("pages/3_Customer_Insights.py")

    with nav_col5:
        st.button(
            "⚔️ Competitive",
            use_container_width=True,
            key="comp_active",
            disabled=True,
        )

    with nav_col6:
        if st.button(
            "💡 Strategic", use_container_width=True, key="comp_to_strategic"
        ):
            st.switch_page("pages/5_Strategic_Analytics.py")


if __name__ == "__main__":
    show()