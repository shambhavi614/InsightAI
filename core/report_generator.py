
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)


EMERALD = colors.HexColor("#0F766E")
DARK = colors.HexColor("#142B2C")
MINT = colors.HexColor("#D1FAE5")
LIGHT = colors.HexColor("#F1F5F9")
MUTED = colors.HexColor("#64748B")
RED = colors.HexColor("#B91C1C")
GREEN = colors.HexColor("#047857")


def safe_text(value):
    return escape(str(value))


def money(value):
    return f"{float(value):,.2f}"


def signed_number(value):
    return f"{float(value):+,.2f}"


def format_percent(value):
    if value is None or pd.isna(value):
        return "N/A (zero baseline)"
    return f"{float(value):+.2f}%"


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)

    canvas.drawString(
        42,
        28,
        "InsightAI | Local Data Investigation",
    )

    canvas.drawRightString(
        A4[0] - 42,
        28,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def build_report(
    investigation,
    dataset_name,
    date_column,
    metric_column,
    category_column,
    period_a_start,
    period_a_end,
    period_b_start,
    period_b_end,
    quality=None,
):
    """
    Generate an investigation PDF in memory.

    Returns:
        bytes: Complete PDF document.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=45,
        bottomMargin=50,
        title="InsightAI Investigation Report",
        author="InsightAI",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="BrandTitle",
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=27,
            textColor=EMERALD,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            fontSize=10,
            leading=15,
            textColor=MUTED,
            spaceAfter=16,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeadingCustom",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=17,
            textColor=DARK,
            spaceBefore=16,
            spaceAfter=9,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            fontSize=9,
            leading=14,
            textColor=DARK,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallCustom",
            fontSize=8,
            leading=12,
            textColor=MUTED,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CellCustom",
            fontSize=8,
            leading=11,
            textColor=DARK,
        )
    )

    story = []

    def paragraph(text, style="BodyCustom"):
        return Paragraph(
            safe_text(text),
            styles[style],
        )

    def heading(text):
        story.append(
            paragraph(text, "SectionHeadingCustom")
        )

    def make_table(rows, widths=None):
        table = Table(
            rows,
            colWidths=widths,
            repeatRows=1,
            hAlign="LEFT",
        )

        table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    EMERALD,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, LIGHT],
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ])
        )

        return table

    # =====================================================
    # HEADER
    # =====================================================

    story.append(
        paragraph("InsightAI", "BrandTitle")
    )

    story.append(
        paragraph(
            "DATA INVESTIGATION REPORT",
            "ReportSubtitle",
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=EMERALD,
        )
    )

    story.append(Spacer(1, 14))

    story.append(
        paragraph(
            f"Dataset: {dataset_name}"
        )
    )

    story.append(
        paragraph(
            "Generated: "
            + datetime.now().strftime(
                "%d %B %Y, %I:%M %p"
            )
        )
    )

    # =====================================================
    # INVESTIGATION SETTINGS
    # =====================================================

    heading("1. Investigation Scope")

    scope_rows = [
        ["Setting", "Selected Value"],
        ["Date column", str(date_column)],
        ["Metric", str(metric_column)],
        ["Category", str(category_column)],
        [
            "Period A",
            f"{period_a_start} to {period_a_end}",
        ],
        [
            "Period B",
            f"{period_b_start} to {period_b_end}",
        ],
    ]

    story.append(
        make_table(scope_rows, [140, 370])
    )

    # =====================================================
    # PERFORMANCE SUMMARY
    # =====================================================

    heading("2. Performance Summary")

    total_a = float(investigation["total_a"])
    total_b = float(investigation["total_b"])
    change = float(investigation["change"])
    change_pct = investigation["change_pct"]

    summary_rows = [
        ["Metric", "Value"],
        ["Baseline total", money(total_a)],
        ["Comparison total", money(total_b)],
        ["Absolute change", signed_number(change)],
        ["Percentage change", format_percent(change_pct)],
    ]

    story.append(
        make_table(summary_rows, [255, 255])
    )

    story.append(Spacer(1, 10))

    if change > 0:
        direction = "increased"
    elif change < 0:
        direction = "decreased"
    else:
        direction = "remained unchanged"

    story.append(
        paragraph(
            f"The total {metric_column} {direction} "
            f"from {money(total_a)} in Period A "
            f"to {money(total_b)} in Period B. "
            f"The absolute change was "
            f"{signed_number(change)} "
            f"({format_percent(change_pct)})."
        )
    )

    # =====================================================
    # CATEGORY CONTRIBUTORS
    # =====================================================

    heading("3. Category Contribution Analysis")

    breakdown = investigation["breakdown"].copy()

    if not breakdown.empty:
        positive = breakdown[
            breakdown["Change"] > 0
        ]

        negative = breakdown[
            breakdown["Change"] < 0
        ]

        if not positive.empty:
            best = positive.loc[
                positive["Change"].idxmax()
            ]

            story.append(
                paragraph(
                    "Largest positive contributor: "
                    f"{best[category_column]} "
                    f"({signed_number(best['Change'])})."
                )
            )

        if not negative.empty:
            worst = negative.loc[
                negative["Change"].idxmin()
            ]

            story.append(
                paragraph(
                    "Largest negative contributor: "
                    f"{worst[category_column]} "
                    f"({signed_number(worst['Change'])})."
                )
            )

        story.append(Spacer(1, 8))

        # Build a simple horizontal contribution chart.
        chart_width = 330
        max_abs = max(
            float(breakdown["Change"].abs().max()),
            1.0,
        )

        chart_rows = []

        for _, row in breakdown.iterrows():
            category = str(row[category_column])
            value = float(row["Change"])

            fraction = abs(value) / max_abs
            bar_width = max(
                1,
                fraction * chart_width,
            )

            bar_color = (
                GREEN if value >= 0 else RED
            )

            bar = Table(
                [[""]],
                colWidths=[bar_width],
                rowHeights=[11],
            )

            bar.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        bar_color,
                    ),
                ])
            )

            chart_rows.append([
                paragraph(category, "CellCustom"),
                bar,
                paragraph(
                    signed_number(value),
                    "CellCustom",
                ),
            ])

        contribution_chart = Table(
            chart_rows,
            colWidths=[110, 330, 70],
            hAlign="LEFT",
        )

        contribution_chart.setStyle(
            TableStyle([
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ])
        )

        story.append(contribution_chart)

        story.append(Spacer(1, 12))

        heading("4. Detailed Contribution Table")

        detail_rows = [
            [
                "Category",
                "Period A",
                "Period B",
                "Change",
            ]
        ]

        for _, row in breakdown.iterrows():
            detail_rows.append([
                paragraph(
                    str(row[category_column]),
                    "CellCustom",
                ),
                money(row["Period A"]),
                money(row["Period B"]),
                signed_number(row["Change"]),
            ])

        story.append(
            make_table(
                detail_rows,
                [155, 115, 115, 125],
            )
        )

    else:
        story.append(
            paragraph(
                "No category contribution records "
                "were available."
            )
        )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    heading("5. Data Quality Assessment")

    if quality:
        quality_rows = [
            ["Check", "Result"],
            [
                "Completeness",
                f"{quality['completeness']:.2f}%",
            ],
            [
                "Missing values",
                str(quality["missing_count"]),
            ],
            [
                "Duplicate rows",
                str(quality["duplicate_count"]),
            ],
        ]

        story.append(
            make_table(
                quality_rows,
                [255, 255],
            )
        )

        story.append(Spacer(1, 10))

        for finding in quality.get("findings", []):
            story.append(
                paragraph(f"- {finding}")
            )

    else:
        story.append(
            paragraph(
                "Data-quality results were "
                "not supplied for this report."
            )
        )

    # =====================================================
    # METHODOLOGY
    # =====================================================

    heading("6. Methodology and Limitations")

    methodology = [
        (
            "Period totals are calculated by summing "
            "the selected numeric metric across records "
            "within each inclusive date range."
        ),
        (
            "Category contribution is calculated as "
            "Period B category total minus Period A "
            "category total."
        ),
        (
            "Percentage change is calculated as "
            "(Period B - Period A) / Period A x 100 "
            "when the baseline is nonzero."
        ),
        (
            "Category contributions describe numerical "
            "changes. They do not establish causation."
        ),
        (
            "Results depend on the completeness and "
            "accuracy of the uploaded dataset."
        ),
    ]

    for item in methodology:
        story.append(
            paragraph(f"- {item}")
        )

    story.append(Spacer(1, 16))

    story.append(
        paragraph(
            "Generated locally by InsightAI. "
            "Review source data and business context "
            "before making decisions.",
            "SmallCustom",
        )
    )

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
