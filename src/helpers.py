# src/helpers.py
import numpy as np
import pandas as pd

def infer_subject_columns(df, meta_cols=None):
    """
    Return list of subject columns by excluding meta columns and keeping numeric-like columns.
    """
    if meta_cols is None:
        meta_cols = ["student_id", "name", "semester"]
    candidates = [c for c in df.columns if c not in meta_cols]
    numeric_cols = []
    for c in candidates:
        # try converting to numeric; treat non-numeric as NaN but keep column
        df[c] = pd.to_numeric(df[c], errors="coerce")
        numeric_cols.append(c)
    return numeric_cols

def calculate_grade(percent_series):
    """
    Vectorized grade calculation using NumPy.
    """
    conds = [
        percent_series >= 90,
        (percent_series >= 80) & (percent_series < 90),
        (percent_series >= 70) & (percent_series < 80),
        (percent_series >= 60) & (percent_series < 70),
        (percent_series >= 45) & (percent_series < 60),
        percent_series < 45
    ]
    choices = ["A+", "A", "B", "C", "D", "F"]
    # Use np.select on numpy array (handles NaN -> default)
    return np.select(conds, choices, default="NA")
