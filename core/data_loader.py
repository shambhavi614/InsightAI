
import pandas as pd


def load_csv(file):
    try:
        df = pd.read_csv(file)

        if df.empty:
            return None, "The CSV file is empty."

        return df, None

    except Exception as e:
        return None, str(e)


def get_dataset_info(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
    }


def get_column_info(df):
    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing": df.isnull().sum().values,
        "Unique Values": df.nunique().values,
    })


def get_summary_statistics(df):
    return df.describe(include="all").transpose()
