
import hashlib
from datetime import timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from core.data_loader import (
    load_csv,
    get_dataset_info,
    get_column_info,
    get_summary_statistics,
)
from core.ai_engine import check_ollama
from core.hybrid_engine import analyze_question
from core.data_quality import inspect_data_quality
from core.investigation_engine import investigate_change
from utils.charts import create_chart
from styles.theme import apply_theme
from core.report_generator import build_report
from core.insight_narrator import generate_investigation_narrative
from deployment import DEMO_MODE, ai_available
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="InsightAI | AI Data Investigator",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

if DEMO_MODE:
    st.info(
        "🌐 Public Demo Mode: Data exploration, charts, "
        "investigations, and PDF reports are available. "
        "Local Ollama AI features are disabled."
    )

# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "analysis_history": [],
    "dataset_id": None,
    "pending_question": None,
    "investigation": None,
    "investigation_config": None,
    "manual_chart": None,
    "ai_narrative": None,
    "ai_narrative_config": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# HELPERS
# =========================================================

def style_chart(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#D9F7EF",
        height=height,
        margin=dict(l=25, r=25, t=65, b=35),
        colorway=[
            "#14B8A6",
            "#34D399",
            "#2DD4BF",
            "#FBBF24",
            "#38BDF8",
        ],
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.13)",
        zeroline=False,
    )
    return fig



def reset_dataset_state():
    st.session_state.analysis_history = []
    st.session_state.pending_question = None
    st.session_state.investigation = None
    st.session_state.investigation_config = None
    st.session_state.manual_chart = None
    st.session_state.ai_narrative = None
    st.session_state.ai_narrative_config = None
    if DEMO_MODE:
        st.warning(
            "AI Assistant is available in the local edition. "
            "Use Investigation Lab or Chart Studio in this demo."
        )
        return

def process_question(question, df):
    if not question or not question.strip():
        return

    with st.spinner("InsightAI is analyzing your data..."):
        try:
            analysis = analyze_question(question, df)
            st.session_state.analysis_history.append(
                analysis
            )
        except Exception as error:
            st.session_state.analysis_history.append({
                "question": question,
                "error": str(error),
            })


def render_analysis(item, index):
    if "error" in item:
        st.error(item["error"])
        return

    st.markdown(item["summary"])

    left, right = st.columns(2)

    left.caption(f"⚡ {item['engine']}")
    right.caption(
        f"⏱ Response time: {item['time']:.3f}s"
    )

    result = item["result"]
    plan = item["plan"]

    group = plan.get("group_by")

    if (
        group
        and group in result.columns
        and "Result" in result.columns
        and not result.empty
    ):
        fig = px.bar(
            result,
            x=group,
            y="Result",
            color=group,
            text="Result",
            title=f"Analysis by {group}",
        )

        fig.update_traces(
            textposition="outside"
        )
        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            style_chart(fig, 360),
            use_container_width=True,
            key=f"ai_chart_{index}",
        )

    with st.expander("View calculated results"):
        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("View analysis plan"):
        st.json(plan)


def format_number(value):
    return f"{value:,.2f}"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## ◈ InsightAI")
    st.caption("LOCAL-FIRST DATA INTELLIGENCE")

    st.divider()

    st.markdown("### 📁 Data Workspace")

    uploaded_file = st.file_uploader(
        "Upload your CSV dataset",
        type=["csv"],
        help="Upload a CSV file to explore and investigate.",
    )

    st.divider()

    st.markdown("### ⚡ AI Engine")

    if st.button(
        "Check Ollama Connection",
        use_container_width=True,
    ):
        if check_ollama():
            st.success("Local Ollama is ready.")
        else:
            st.warning(
                "Ollama unavailable. Fast Pandas "
                "queries can still work."
            )

    st.caption("Pandas + Ollama Hybrid Engine")

    st.divider()

    st.markdown("### 🧭 Workspace Modules")

    st.caption("📊 Dataset Overview")
    st.caption("🔎 Data Quality Detective")
    st.caption("📉 Investigation Lab")
    st.caption("📁 Dataset Explorer")
    st.caption("📈 Chart Studio")
    st.caption("🤖 AI Assistant")

    st.divider()

    st.caption("InsightAI • Investigator Edition")



# =========================================================
# HERO — EMERALD + CHARCOAL
# =========================================================

st.markdown("# ◈ InsightAI")

hero_html = """
<div class="insight-hero">
  <div style="color:#5EEAD4; font-size:12px; font-weight:700; letter-spacing:2px; margin-bottom:12px;">
    ✦ INTELLIGENT DATA INVESTIGATION
  </div>
  <h2>Find the story behind your data.</h2>
  <p>Detect hidden data issues, investigate performance changes, and uncover evidence-backed insights.</p>
  <div style="display:flex; flex-wrap:wrap; gap:10px; margin-top:20px;">
    <span style="padding:7px 13px; border-radius:20px; background:#173C37; color:#A7F3D0; font-size:12px;">✦ Local AI</span>
    <span style="padding:7px 13px; border-radius:20px; background:#173C37; color:#A7F3D0; font-size:12px;">✓ Verified Calculations</span>
    <span style="padding:7px 13px; border-radius:20px; background:#173C37; color:#A7F3D0; font-size:12px;">◈ Data Investigation</span>
  </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

# =========================================================
# EMPTY STATE
# =========================================================

if uploaded_file is None:
    st.info(
        "Upload a CSV file from the sidebar "
        "to activate your analytics workspace."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🔎 Detect")
        st.write(
            "Find missing values, duplicates, "
            "outliers, and text inconsistencies."
        )

    with c2:
        st.markdown("### 📉 Investigate")
        st.write(
            "Compare periods and identify "
            "the biggest contributors to changes."
        )

    with c3:
        st.markdown("### 🤖 Ask")
        st.write(
            "Ask questions about your dataset "
            "using the hybrid AI engine."
        )

    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

df, error = load_csv(uploaded_file)

if error:
    st.error(error)
    st.stop()

dataset_hash = hashlib.sha256(
    uploaded_file.getvalue()
).hexdigest()

if st.session_state.dataset_id != dataset_hash:
    st.session_state.dataset_id = dataset_hash
    reset_dataset_state()


# =========================================================
# DASHBOARD METRICS
# =========================================================

info = get_dataset_info(df)

st.markdown("### Workspace Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Records",
    f"{info['rows']:,}",
)

c2.metric(
    "Data Fields",
    info["columns"],
)

c3.metric(
    "Missing Values",
    info["missing_values"],
)

c4.metric(
    "AI Queries",
    len(st.session_state.analysis_history),
)

st.divider()


# =========================================================
# MAIN NAVIGATION
# =========================================================

tabs = st.tabs([
    "📊 Overview",
    "🔎 Data Detective",
    "📉 Investigation Lab",
    "📁 Dataset",
    "📈 Charts",
    "🤖 AI Assistant",
])


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with tabs[0]:
    st.subheader("Dataset Intelligence Overview")

    total_cells = df.shape[0] * df.shape[1]
    missing_cells = int(df.isna().sum().sum())

    completeness = (
        (1 - missing_cells / total_cells) * 100
        if total_cells
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Data Completeness",
        f"{completeness:.1f}%",
    )

    c2.metric(
        "Duplicate Rows",
        int(df.duplicated().sum()),
    )

    c3.metric(
        "Numeric Columns",
        len(
            df.select_dtypes(
                include="number"
            ).columns
        ),
    )

    st.markdown("### Data Preview")

    st.dataframe(
        df.head(15),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Dataset Structure")

    left, right = st.columns([1, 1])

    with left:
        st.dataframe(
            get_column_info(df),
            use_container_width=True,
            hide_index=True,
        )

    with right:
        dtype_counts = (
            df.dtypes.astype(str)
            .value_counts()
            .reset_index()
        )

        dtype_counts.columns = [
            "Data Type",
            "Count",
        ]

        fig = px.pie(
            dtype_counts,
            names="Data Type",
            values="Count",
            hole=0.62,
            title="Column Type Distribution",
            color_discrete_sequence=[
                "#14B8A6",
                "#34D399",
                "#FBBF24",
                "#38BDF8",
            ],
        )

        st.plotly_chart(
            style_chart(fig, 340),
            use_container_width=True,
            key="overview_types",
        )


# =========================================================
# TAB 2 — DATA QUALITY DETECTIVE
# =========================================================

with tabs[1]:
    st.subheader("🔎 Data Quality Detective")

    st.caption(
        "Inspect your dataset for potential "
        "quality issues before making decisions."
    )

    quality = inspect_data_quality(df)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Completeness",
        f"{quality['completeness']:.2f}%",
    )

    c2.metric(
        "Duplicate Rows",
        quality["duplicate_count"],
    )

    c3.metric(
        "Missing Values",
        quality["missing_count"],
    )

    st.markdown("### Investigation Findings")

    for finding in quality["findings"]:
        st.info(finding)

    st.markdown("### Missing Value Analysis")

    missing_df = quality["missing_by_column"]

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True,
    )

    if missing_df["Missing Values"].sum() > 0:
        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing Values",
            color="Missing Values",
            title="Missing Values by Column",
            color_continuous_scale=[
                "#134E4A",
                "#14B8A6",
                "#5EEAD4",
            ],
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
            key="missing_chart",
        )

    st.markdown("### Potential Numeric Outliers")

    if quality["outliers"].empty:
        st.success(
            "No potential outliers were detected "
            "by the current IQR checks."
        )
    else:
        st.warning(
            "Potential outliers found. "
            "Review before removing any records."
        )

        st.dataframe(
            quality["outliers"],
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### Text Consistency")

    if quality["text_issues"].empty:
        st.success(
            "No leading or trailing whitespace "
            "issues detected."
        )
    else:
        st.dataframe(
            quality["text_issues"],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Quality checks are diagnostic. "
        "A clean result does not guarantee "
        "that every value is correct."
    )


# =========================================================
# TAB 3 — INVESTIGATION LAB
# =========================================================

with tabs[2]:
    st.subheader("📉 Investigation Lab")

    st.caption(
        "Compare two non-overlapping periods "
        "and identify which categories contributed "
        "most to the change."
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    date_candidates = []

    for column in df.columns:
        name = str(column).lower()

        if (
            "date" in name
            or "time" in name
        ):
            date_candidates.append(column)

    if not date_candidates:
        date_candidates = df.select_dtypes(
            include=["object", "string", "datetime"]
        ).columns.tolist()

    category_columns = [
        column
        for column in df.columns
        if column not in numeric_columns
    ]

    if (
        not numeric_columns
        or not date_candidates
        or not category_columns
    ):
        st.warning(
            "A numeric metric, date column, "
            "and category column are required."
        )

    else:
        c1, c2, c3 = st.columns(3)

        with c1:
            date_col = st.selectbox(
                "Date Column",
                date_candidates,
                key="invest_date_column",
            )

        with c2:
            metric_col = st.selectbox(
                "Metric",
                numeric_columns,
                key="invest_metric_column",
            )

        with c3:
            categories = [
                column
                for column in category_columns
                if column != date_col
            ]

            if not categories:
                st.warning(
                    "Select a dataset with a "
                    "separate category column."
                )
                st.stop()

            category_col = st.selectbox(
                "Category",
                categories,
                key="invest_category_column",
            )

        parsed_dates = pd.to_datetime(
            df[date_col],
            errors="coerce",
        )

        valid_dates = parsed_dates.dropna()

        if valid_dates.empty:
            st.warning(
                "No valid dates found in "
                "the selected date column."
            )

        else:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            total_days = (
                max_date - min_date
            ).days

            if total_days < 1:
                st.warning(
                    "At least two different dates "
                    "are required for comparison."
                )

            else:
                midpoint = min_date + timedelta(
                    days=total_days // 2
                )

                next_day = midpoint + timedelta(
                    days=1
                )

                st.markdown("### Comparison Periods")

                c1, c2 = st.columns(2)

                with c1:
                    st.markdown(
                        "**Period A — Baseline**"
                    )

                    a_start = st.date_input(
                        "Baseline Start",
                        value=min_date,
                        min_value=min_date,
                        max_value=max_date,
                        key="baseline_start_v2",
                    )

                    a_end = st.date_input(
                        "Baseline End",
                        value=midpoint,
                        min_value=min_date,
                        max_value=max_date,
                        key="baseline_end_v2",
                    )

                with c2:
                    st.markdown(
                        "**Period B — Comparison**"
                    )

                    b_start = st.date_input(
                        "Comparison Start",
                        value=next_day,
                        min_value=min_date,
                        max_value=max_date,
                        key="comparison_start_v2",
                    )

                    b_end = st.date_input(
                        "Comparison End",
                        value=max_date,
                        min_value=min_date,
                        max_value=max_date,
                        key="comparison_end_v2",
                    )

                config = (
                    date_col,
                    metric_col,
                    category_col,
                    str(a_start),
                    str(a_end),
                    str(b_start),
                    str(b_end),
                )

                valid_ranges = (
                    a_start <= a_end
                    and b_start <= b_end
                    and a_end < b_start
                )

                if not valid_ranges:
                    st.warning(
                        "Choose valid, non-overlapping "
                        "periods with Period A before "
                        "Period B."
                    )

                if st.button(
                    "🔎 Investigate Change",
                    type="primary",
                    disabled=not valid_ranges,
                    use_container_width=True,
                ):
                    try:
                        investigation = (
                            investigate_change(
                                df,
                                date_col,
                                metric_col,
                                category_col,
                                a_start,
                                a_end,
                                b_start,
                                b_end,
                            )
                        )

                        st.session_state.investigation = (
                            investigation
                        )

                        st.session_state.investigation_config = (
                            config
                        )

                    except Exception as error:
                        st.session_state.investigation = None
                        st.session_state.investigation_config = None
                        st.error(str(error))

                investigation = (
                    st.session_state.investigation
                )

                if (
                    investigation is not None
                    and st.session_state.investigation_config
                    != config
                ):
                    st.info(
                        "Comparison settings changed. "
                        "Click Investigate Change "
                        "to calculate updated results."
                    )
                    investigation = None

                if investigation is not None:
                    st.divider()

                    st.markdown(
                        "### Investigation Results"
                    )

                    st.markdown(
                        investigation["summary"]
                    )

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Baseline Total",
                        format_number(
                            investigation["total_a"]
                        ),
                    )

                    c2.metric(
                        "Comparison Total",
                        format_number(
                            investigation["total_b"]
                        ),
                    )

                    change_pct = (
                        investigation["change_pct"]
                    )

                    change_label = (
                        f"{change_pct:+.2f}%"
                        if change_pct is not None
                        else "N/A"
                    )

                    c3.metric(
                        "Total Change",
                        format_number(
                            investigation["change"]
                        ),
                        delta=change_label,
                    )

                    breakdown = (
                        investigation["breakdown"]
                    )

                    st.markdown(
                        "### Category Contribution Analysis"
                    )

                    st.dataframe(
                        breakdown,
                        use_container_width=True,
                        hide_index=True,
                    )

                    if not breakdown.empty:
                        # Negative values indicate decreases;
                        # positive values indicate increases.
                        negative = breakdown[
                            breakdown["Change"] < 0
                        ]

                        positive = breakdown[
                            breakdown["Change"] > 0
                        ]

                        left, right = st.columns(2)

                        with left:
                            st.markdown(
                                "#### 📉 Largest Decline"
                            )

                            if negative.empty:
                                st.success(
                                    "No category declines "
                                    "detected."
                                )
                            else:
                                worst = negative.loc[
                                    negative["Change"].idxmin()
                                ]

                                st.error(
                                    f"{worst[category_col]}: "
                                    f"{worst['Change']:+,.2f}"
                                )

                        with right:
                            st.markdown(
                                "#### 📈 Largest Increase"
                            )

                            if positive.empty:
                                st.info(
                                    "No category increases "
                                    "detected."
                                )
                            else:
                                best = positive.loc[
                                    positive["Change"].idxmax()
                                ]

                                st.success(
                                    f"{best[category_col]}: "
                                    f"{best['Change']:+,.2f}"
                                )

                        fig = px.bar(
                            breakdown,
                            x=category_col,
                            y="Change",
                            color="Change",
                            color_continuous_scale=[
                                "#F87171",
                                "#FBBF24",
                                "#34D399",
                            ],
                            title=(
                                "Category Contribution "
                                "to Total Change"
                            ),
                        )

                        fig.add_hline(
                            y=0,
                            line_color="#94A3B8",
                            line_width=1,
                        )

                        st.plotly_chart(
                            style_chart(fig, 450),
                            use_container_width=True,
                            key="investigation_breakdown",
                        )

                    st.caption(
                        "These results identify numerical "
                        "contributors, not proven causal "
                        "reasons for the change."
                    )

                    if investigation["invalid_date_rows"]:
                        st.warning(
                            f"{investigation['invalid_date_rows']} "
                            "rows contained invalid dates "
                            "and were excluded."
                        )

# =====================================================
# PHASE 6 — PDF INVESTIGATION REPORT
# =====================================================

st.divider()

st.markdown("### 📄 Investigation Report")

st.caption(
    "Download a professional PDF containing "
    "the comparison, category contributions, "
    "data-quality findings, and methodology."
)

try:
    report_bytes = build_report(
        investigation=investigation,
        dataset_name=uploaded_file.name,
        date_column=date_col,
        metric_column=metric_col,
        category_column=category_col,
        period_a_start=a_start,
        period_a_end=a_end,
        period_b_start=b_start,
        period_b_end=b_end,
        quality=quality,
    )

    st.download_button(
        label="⬇ Download Investigation PDF",
        data=report_bytes,
        file_name="InsightAI_Investigation_Report.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True,
        key="download_investigation_pdf",
    )

    st.success(
        "Investigation report is ready."
    )

except Exception as error:
    st.error(
        f"Could not generate PDF report: {error}"
    )


# =====================================================
# PHASE 7 — AI INVESTIGATION NARRATOR
# =====================================================

st.divider()

st.markdown("### 🧠 AI Investigation Brief")

st.caption(
    "Generate a local AI explanation based on "
    "verified Pandas calculations."
)

if st.button(
    "✨ Generate AI Investigation Brief",
    use_container_width=True,
    key="generate_ai_investigation",
    disabled=not ai_available(),
):
    with st.spinner(
        "Ollama is interpreting the investigation..."
    ):
        try:
            narrative_result = (
                generate_investigation_narrative(
                    investigation=investigation,
                    category_column=category_col,
                    metric_column=metric_col,
                    period_a_start=a_start,
                    period_a_end=a_end,
                    period_b_start=b_start,
                    period_b_end=b_end,
                )
            )

            st.session_state.ai_narrative = (
                narrative_result
            )

            st.session_state.ai_narrative_config = (
                config
            )

        except Exception as error:
            st.session_state.ai_narrative = None
            st.session_state.ai_narrative_config = None
            st.error(str(error))

saved_narrative = st.session_state.ai_narrative

if (
    saved_narrative is not None
    and st.session_state.ai_narrative_config == config
):
    st.markdown(
        saved_narrative["narrative"]
    )

    st.caption(
        "Generated by local Ollama in "
        f"{saved_narrative['response_time']:.1f}s"
    )

    with st.expander(
        "🔍 View Verified Evidence"
    ):
        st.json(
            saved_narrative["evidence"]
        )

    st.download_button(
        "⬇ Download AI Brief (Markdown)",
        data=saved_narrative["narrative"],
        file_name="InsightAI_AI_Investigation_Brief.md",
        mime="text/markdown",
        use_container_width=True,
        key="download_ai_brief",
    )

elif saved_narrative is not None:
    st.info(
        "Investigation settings changed. "
        "Generate a new AI brief for the "
        "current comparison."
    )

st.caption(
    "AI explanations are hypotheses and may "
    "contain mistakes. Verify conclusions "
    "against the evidence table."
)


# =========================================================
# TAB 4 — DATASET EXPLORER
# =========================================================

with tabs[3]:
    st.subheader("📁 Dataset Explorer")

    st.caption(
        f"Showing up to 200 of {len(df):,} records."
    )

    st.dataframe(
        df.head(200),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Column Information")

    st.dataframe(
        get_column_info(df),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Statistical Summary")

    st.dataframe(
        get_summary_statistics(df),
        use_container_width=True,
    )

    st.download_button(
        "⬇ Download Dataset",
        data=df.to_csv(index=False),
        file_name="insightai_dataset_export.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# TAB 5 — CHART STUDIO
# =========================================================

with tabs[4]:
    st.subheader("📈 Chart Studio")

    st.caption(
        "Create interactive charts to explore "
        "patterns and relationships."
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if not numeric_columns:
        st.warning(
            "No numeric columns available."
        )

    else:
        c1, c2, c3 = st.columns(3)

        with c1:
            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar Chart",
                    "Line Chart",
                    "Scatter Plot",
                    "Pie Chart",
                ],
            )

        with c2:
            x_column = st.selectbox(
                "X Axis",
                df.columns.tolist(),
            )

        with c3:
            y_column = st.selectbox(
                "Y Axis",
                numeric_columns,
            )

        chart_config = (
            chart_type,
            x_column,
            y_column,
        )

        if st.button(
            "Generate Visualization",
            type="primary",
        ):
            try:
                fig = create_chart(
                    df,
                    x_column,
                    y_column,
                    chart_type,
                )

                if fig is not None:
                    st.session_state.manual_chart = (
                        fig,
                        chart_config,
                    )

            except Exception as error:
                st.error(str(error))

        saved_chart = (
            st.session_state.manual_chart
        )

        if saved_chart is not None:
            fig, saved_config = saved_chart

            if saved_config == chart_config:
                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                    key="manual_visualization",
                )
            else:
                st.info(
                    "Chart settings changed. "
                    "Generate the chart again."
                )


# =========================================================
# TAB 6 — AI ASSISTANT
# =========================================================

with tabs[5]:
    st.subheader("🤖 InsightAI Assistant")

    st.caption(
        "Ask questions about your uploaded data. "
        "Results are calculated using Pandas."
    )

    if not st.session_state.analysis_history:
        st.markdown("### Suggested Questions")

        suggestions = [
            "What is the total Sales?",
            "What is the average Quantity?",
            "Which Product has the highest total Sales?",
            "What is the total Sales by Region?",
        ]

        columns = st.columns(2)

        for index, suggestion in enumerate(
            suggestions
        ):
            with columns[index % 2]:
                if st.button(
                    suggestion,
                    key=f"suggestion_{index}",
                    use_container_width=True,
                ):
                    st.session_state.pending_question = (
                        suggestion
                    )

    for index, item in enumerate(
        st.session_state.analysis_history
    ):
        with st.chat_message("user"):
            st.write(item["question"])

        with st.chat_message("assistant"):
            render_analysis(item, index)

    question = st.chat_input(
        "Ask a question about your data..."
    )

    if st.session_state.pending_question:
        question = (
            st.session_state.pending_question
        )
        st.session_state.pending_question = None

    if question:
        process_question(question, df)
        st.rerun()

    if st.session_state.analysis_history:
        if st.button("🗑 Clear Conversation"):
            st.session_state.analysis_history = []
            st.rerun()