
from typing import Literal, Optional

import pandas as pd
from pydantic import BaseModel, Field


class FilterCondition(BaseModel):
    column: str
    operator: Literal["eq", "ne", "gt", "gte", "lt", "lte"]
    value: str | int | float | bool


class AnalysisPlan(BaseModel):
    operation: Literal["sum", "mean", "count", "max", "min"]
    group_by: Optional[str] = None
    target_column: Optional[str] = None
    sort: Literal["asc", "desc"] = "desc"
    limit: int = Field(default=10, ge=1, le=100)
    filters: list[FilterCondition] = Field(default_factory=list)


def _apply_filters(df, filters):
    filtered = df.copy()

    for condition in filters:
        column = condition.column

        if column not in filtered.columns:
            raise ValueError(f"Unknown filter column: {column}")

        series = filtered[column]
        value = condition.value

        if pd.api.types.is_numeric_dtype(series):
            try:
                value = pd.to_numeric(value)
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid numeric filter value: {value}"
                )

        elif pd.api.types.is_datetime64_any_dtype(series):
            value = pd.to_datetime(value, errors="raise")

        else:
            if condition.operator not in ("eq", "ne"):
                raise ValueError(
                    f"Only equality filters are supported for {column}"
                )
            value = str(value)
            series = series.astype("string")

        operators = {
            "eq": lambda a, b: a == b,
            "ne": lambda a, b: a != b,
            "gt": lambda a, b: a > b,
            "gte": lambda a, b: a >= b,
            "lt": lambda a, b: a < b,
            "lte": lambda a, b: a <= b,
        }

        mask = operators[condition.operator](series, value)
        filtered = filtered.loc[mask.fillna(False)]

    return filtered


def execute_analysis(df: pd.DataFrame, plan: AnalysisPlan):
    if df.empty:
        raise ValueError("The dataset is empty.")

    if plan.group_by and plan.group_by not in df.columns:
        raise ValueError(
            f"Unknown grouping column: {plan.group_by}"
        )

    if plan.operation != "count":
        if not plan.target_column:
            raise ValueError("A target column is required.")

        if plan.target_column not in df.columns:
            raise ValueError(
                f"Unknown target column: {plan.target_column}"
            )

        if not pd.api.types.is_numeric_dtype(
            df[plan.target_column]
        ):
            raise ValueError(
                f"{plan.target_column} must be numeric."
            )

    working_df = _apply_filters(df, plan.filters)

    if working_df.empty:
        raise ValueError(
            "No rows match the selected filters."
        )

    if plan.group_by:
        grouped = working_df.groupby(
            plan.group_by,
            dropna=False
        )

        if plan.operation == "count":
            result = grouped.size().reset_index(
                name="Result"
            )
        else:
            result = (
                grouped[plan.target_column]
                .agg(plan.operation)
                .reset_index(name="Result")
            )

        result = result.sort_values(
            "Result",
            ascending=(plan.sort == "asc"),
            kind="stable",
        )

        return result.head(plan.limit).reset_index(drop=True)

    if plan.operation == "count":
        value = len(working_df)
    else:
        value = working_df[plan.target_column].agg(
            plan.operation
        )

    return pd.DataFrame({
        "Metric": [plan.operation],
        "Result": [value],
    })


def generate_summary(result, plan):
    if result.empty:
        return "No results were found."

    if plan.group_by:
        row = result.iloc[0]
        direction = (
            "highest" if plan.sort == "desc"
            else "lowest"
        )

        metric = plan.target_column or "record count"

        return (
            f"**{row[plan.group_by]}** has the "
            f"{direction} {plan.operation} of "
            f"**{metric}**: **{row['Result']:,.2f}**."
        )

    metric = plan.target_column or "records"
    value = result.iloc[0]["Result"]

    return (
        f"The {plan.operation} of **{metric}** "
        f"is **{value:,.2f}**."
    )
