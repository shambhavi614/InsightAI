
import pandas as pd
import numpy as np


def inspect_data_quality(df):
    if df.empty:
        raise ValueError("Dataset is empty.")

    rows, columns = df.shape
    total_cells = rows * columns

    missing_count = int(df.isna().sum().sum())
    duplicate_count = int(df.duplicated().sum())

    completeness = (
        100 * (1 - missing_count / total_cells)
        if total_cells else 0
    )

    missing_by_column = (
        df.isna().sum()
        .reset_index()
    )
    missing_by_column.columns = [
        "Column", "Missing Values"
    ]
    missing_by_column["Missing %"] = (
        missing_by_column["Missing Values"]
        / rows * 100
    ).round(2)

    # IQR-based outlier detection
    outlier_rows = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outlier_count = int(
            ((values < lower) | (values > upper)).sum()
        )

        if outlier_count:
            outlier_rows.append({
                "Column": column,
                "Outliers": outlier_count,
                "Lower Bound": round(float(lower), 3),
                "Upper Bound": round(float(upper), 3),
            })

    outliers = pd.DataFrame(
        outlier_rows,
        columns=[
            "Column",
            "Outliers",
            "Lower Bound",
            "Upper Bound",
        ],
    )

    # Detect whitespace inconsistencies
    text_issues = []

    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:
        values = df[column].dropna().astype(str)

        whitespace_count = int(
            (values != values.str.strip()).sum()
        )

        if whitespace_count:
            text_issues.append({
                "Column": column,
                "Issue": "Leading/trailing whitespace",
                "Count": whitespace_count,
            })

    text_issues = pd.DataFrame(
        text_issues,
        columns=["Column", "Issue", "Count"],
    )

    findings = []

    if missing_count:
        findings.append(
            f"{missing_count} missing values detected."
        )

    if duplicate_count:
        findings.append(
            f"{duplicate_count} duplicate rows detected."
        )

    if not outliers.empty:
        findings.append(
            f"Potential outliers detected in "
            f"{len(outliers)} numeric columns."
        )

    if not text_issues.empty:
        findings.append(
            "Some text fields contain extra whitespace."
        )

    if not findings:
        findings.append(
            "No issues detected by the current checks."
        )

    return {
        "rows": rows,
        "columns": columns,
        "missing_count": missing_count,
        "duplicate_count": duplicate_count,
        "completeness": round(completeness, 2),
        "missing_by_column": missing_by_column,
        "outliers": outliers,
        "text_issues": text_issues,
        "findings": findings,
    }
