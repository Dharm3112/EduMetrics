
---

# 8) Optional: Streamlit app (`src/streamlit_app.py`)

If you want an interactive web UI, create `src/streamlit_app.py`:

```python
# src/streamlit_app.py
import streamlit as st
import pandas as pd
import os
from helpers import infer_subject_columns, calculate_grade
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("Student Performance Dashboard (Pandas + NumPy + Matplotlib)")

uploaded = st.file_uploader("Upload marks CSV or Excel", type=["csv", "xlsx"])
if uploaded is not None:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.write("Preview data", df.head())

    subjects = infer_subject_columns(df)
    df[subjects] = df[subjects].apply(pd.to_numeric, errors="coerce")
    df["semester"] = df["semester"].astype(str)

    # compute totals
    num_subjects = len(subjects)
    max_marks = 100
    df["total_marks"] = df[subjects].fillna(0).sum(axis=1)
    df["percentage"] = (df["total_marks"] / (num_subjects * max_marks))*100
    df["grade"] = calculate_grade(df["percentage"].fillna(-1))

    st.subheader("Subject Stats")
    st.dataframe(df[subjects].agg(["mean","median","max","min","std"]).transpose())

    st.subheader("Top Students")
    st.dataframe(df.sort_values("percentage", ascending=False)[["student_id","name","percentage","grade"]].head(10))

    st.subheader("Plot - Average Marks per Subject")
    fig, ax = plt.subplots()
    df[subjects].mean().plot(kind="bar", ax=ax)
    st.pyplot(fig)
