
import pandas as pd
import plotly.express as px


def create_chart(df, x_column, y_column, chart_type):
    if df.empty:
        return None

    if chart_type == "Bar Chart":
        return px.bar(
            df,
            x=x_column,
            y=y_column,
            color=x_column,
            title=f"{y_column} by {x_column}"
        )

    elif chart_type == "Line Chart":
        return px.line(
            df,
            x=x_column,
            y=y_column,
            markers=True,
            title=f"{y_column} Trend"
        )

    elif chart_type == "Scatter Plot":
        return px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{x_column} vs {y_column}"
        )

    elif chart_type == "Pie Chart":
        grouped = (
            df.groupby(x_column, dropna=False)[y_column]
            .sum()
            .reset_index()
        )

        return px.pie(
            grouped,
            names=x_column,
            values=y_column,
            title=f"{y_column} Distribution"
        )

    return None
