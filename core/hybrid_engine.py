
import re
import time

import pandas as pd

from core.analysis_engine import (
    AnalysisPlan,
    execute_analysis,
    generate_summary,
)
from core.query_planner import create_analysis_plan


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def column_aliases(column):
    name = normalize(str(column))
    aliases = {name}

    if name.endswith("s") and len(name) > 1:
        aliases.add(name[:-1])
    else:
        aliases.add(name + "s")

    if name in {"sales", "sale"}:
        aliases.update({
            "sales", "sale", "revenue"
        })

    if name == "quantity":
        aliases.update({
            "quantity", "quantities", "units"
        })

    if name == "product":
        aliases.update({
            "product", "products"
        })

    if name == "region":
        aliases.update({
            "region", "regions"
        })

    return aliases


def mentions_column(question, column):
    text = f" {normalize(question)} "

    for alias in column_aliases(column):
        if f" {alias} " in text:
            return True

    return False


def fast_plan(question, df):
    text = normalize(question)

    unsupported_phrases = [
        "where", "between", "after", "before",
        "compare", "versus", "trend", "monthly",
        "weekly", "yearly", "correlation",
        "percentage", "growth", "forecast",
        "predict", "median", "standard deviation",
        "excluding", "except", "filter",
        "greater than", "less than",
    ]

    if any(
        re.search(
            r"\b" + re.escape(term) + r"\b",
            text
        )
        for term in unsupported_phrases
    ):
        return None

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = [
        column for column in df.columns
        if column not in numeric_columns
    ]

    targets = [
        column for column in numeric_columns
        if mentions_column(text, column)
    ]

    groups = [
        column for column in categorical_columns
        if mentions_column(text, column)
    ]

    if len(targets) != 1:
        return None

    target = targets[0]

    highest = bool(re.search(
        r"\b(highest|most|largest|top|best|maximum)\b",
        text
    ))

    lowest = bool(re.search(
        r"\b(lowest|least|smallest|worst|minimum)\b",
        text
    ))

    if highest and lowest:
        return None

    if re.search(r"\b(average|mean)\b", text):
        operation = "mean"

    elif re.search(r"\b(count|number of|how many)\b", text):
        operation = "count"

    elif re.search(r"\b(total|sum|revenue|sale|sales)\b", text):
        operation = "sum"

    else:
        return None

    # Only allow unambiguous grouping.
    if len(groups) > 1:
        return None

    group_by = groups[0] if groups else None

    # Ranking a category requires grouping.
    if (highest or lowest) and not group_by:
        return None

    return AnalysisPlan(
        operation=operation,
        group_by=group_by,
        target_column=target,
        sort="asc" if lowest else "desc",
        limit=10,
        filters=[],
    )


def validate_ai_plan(question, df, plan):
    text = normalize(question)

    ranking = bool(re.search(
        r"\b(highest|lowest|most|least|top|best|largest|smallest)\b",
        text
    ))

    categorical_mentions = [
        column
        for column in df.columns
        if not pd.api.types.is_numeric_dtype(df[column])
        and mentions_column(text, column)
    ]

    if ranking and categorical_mentions:
        if plan.group_by not in categorical_mentions:
            raise ValueError(
                "AI did not select the required grouping "
                "column. Please rephrase the question."
            )

    if plan.group_by and plan.group_by not in df.columns:
        raise ValueError(
            "AI selected an invalid grouping column."
        )

    return plan


def analyze_question(question, df):
    start = time.perf_counter()

    plan = fast_plan(question, df)
    engine = "Fast Pandas Engine"

    if plan is None:
        engine = "Ollama AI + Pandas"

        plan, error = create_analysis_plan(
            question, df
        )

        if error or plan is None:
            raise ValueError(
                error or "Could not understand the question."
            )

        plan = validate_ai_plan(
            question, df, plan
        )

    result = execute_analysis(df, plan)
    summary = generate_summary(result, plan)

    return {
        "question": question,
        "summary": summary,
        "result": result,
        "plan": plan.model_dump(),
        "engine": engine,
        "time": time.perf_counter() - start,
    }
