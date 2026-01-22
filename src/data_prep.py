from __future__ import annotations
import pandas as pd

def load_parallel_csv(local_csv_path: str, source_col: str, target_col: str) -> pd.DataFrame:
    df = pd.read_csv(local_csv_path)

    if df.empty:
        raise ValueError("CSV is empty.")

    missing_cols = [c for c in [source_col, target_col] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}. Found columns: {list(df.columns)}")

    df = df.dropna(subset=[source_col, target_col]).copy()
    df[source_col] = df[source_col].astype(str).str.strip()
    df[target_col] = df[target_col].astype(str).str.strip()

    # Optional: remove blank lines after strip
    df = df[(df[source_col] != "") & (df[target_col] != "")]
    return df


