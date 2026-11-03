
import pandas as pd


def investigate_change(
    df,
    date_column,
    metric_column,
    category_column,
    period_a_start,
    period_a_end,
    period_b_start,
    period_b_end,
):
    required = [
        date_column,
        metric_column,
        category_column,
    ]

    for column in required:
        if column not in df.columns:
            raise ValueError(
                f"Unknown column: {column}"
            )

    working = df.copy()

    working["_insight_date"] = pd.to_datetime(
        working[date_column],
        errors="coerce",
    )

    if working["_insight_date"].isna().all():
        raise ValueError(
            "The selected date column has no valid dates."
        )

    working["_insight_metric"] = pd.to_numeric(
        working[metric_column],
        errors="coerce",
    )

    if working["_insight_metric"].notna().sum() == 0:
        raise ValueError(
            "The selected metric has no numeric values."
        )

    a_start = pd.Timestamp(period_a_start)
    a_end = pd.Timestamp(period_a_end)
    b_start = pd.Timestamp(period_b_start)
    b_end = pd.Timestamp(period_b_end)

    if a_start > a_end or b_start > b_end:
        raise ValueError(
            "Start date must be before end date."
        )

    if a_end >= b_start:
        raise ValueError(
            "Choose two non-overlapping periods, "
            "with Period A before Period B."
        )

    period_a = working[
        working["_insight_date"].dt.normalize().between(
            a_start, a_end
        )
    ]

    period_b = working[
        working["_insight_date"].dt.normalize().between(
            b_start, b_end
        )
    ]

    if period_a.empty or period_b.empty:
        raise ValueError(
            "Both periods must contain records."
        )

    total_a = float(
        period_a["_insight_metric"].sum()
    )
    total_b = float(
        period_b["_insight_metric"].sum()
    )

    change = total_b - total_a

    change_pct = (
        change / abs(total_a) * 100
        if total_a != 0 else None
    )

    group_a = period_a.groupby(
        category_column,
        dropna=False
    )["_insight_metric"].sum()

    group_b = period_b.groupby(
        category_column,
        dropna=False
    )["_insight_metric"].sum()

    breakdown = pd.concat(
        [group_a, group_b],
        axis=1,
        keys=["Period A", "Period B"],
    ).fillna(0)

    breakdown["Change"] = (
        breakdown["Period B"]
        - breakdown["Period A"]
    )

    breakdown = (
        breakdown.reset_index()
        .sort_values("Change")
        .reset_index(drop=True)
    )

    direction = (
        "increased" if change > 0
        else "decreased" if change < 0
        else "remained unchanged"
    )

    if change_pct is None:
        pct_text = (
            "A percentage change is undefined "
            "because Period A totals zero."
        )
    else:
        pct_text = (
            f"The change is {change_pct:+.2f}%."
        )

    summary = (
        f"**{metric_column} {direction}** "
        f"from **{total_a:,.2f}** to "
        f"**{total_b:,.2f}**. "
        f"{pct_text}"
    )

    return {
        "total_a": total_a,
        "total_b": total_b,
        "change": change,
        "change_pct": change_pct,
        "summary": summary,
        "breakdown": breakdown,
        "period_a_rows": len(period_a),
        "period_b_rows": len(period_b),
        "invalid_date_rows": int(
            working["_insight_date"].isna().sum()
        ),
    }
