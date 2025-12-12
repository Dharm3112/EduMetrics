# src/dashboard.py
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from helpers import infer_subject_columns, calculate_grade

# ---------- Config ----------
DEFAULT_DATA = "../data/marks_sample.csv"
OUTPUT_DIR = "../outputs/reports"
META_COLS = ["student_id", "name", "semester"]
MAX_MARKS_PER_SUBJECT = 100  # adjust if needed

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Functions ----------
def load_data(path):
    if path.endswith((".xls", ".xlsx")):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    return df

def clean_and_infer(df):
    subjects = infer_subject_columns(df, meta_cols=META_COLS)
    # ensure numeric
    df[subjects] = df[subjects].apply(pd.to_numeric, errors="coerce")
    # normalize semester as string for pivoting (keeps ordering later if needed)
    df["semester"] = df["semester"].astype(str)
    return df, subjects

def compute_totals(df, subjects, treat_missing_as_zero=False):
    if treat_missing_as_zero:
        totals = df[subjects].fillna(0).sum(axis=1)
    else:
        # if any subject missing, total will be NaN to flag incomplete records
        totals = df[subjects].sum(axis=1, skipna=False)
    df["total_marks"] = totals
    num_subjects = len(subjects)
    df["percentage"] = (df["total_marks"] / (MAX_MARKS_PER_SUBJECT * num_subjects)) * 100
    df["grade"] = calculate_grade(df["percentage"].fillna(-1))  # NA -> 'NA'
    return df

def subject_stats(df, subjects):
    stats = df[subjects].agg(["mean", "median", "max", "min", "std"]).transpose().rename(
        columns={"mean": "avg", "median": "median", "max": "max", "min": "min", "std": "std"}
    )
    stats.index.name = "subject"
    return stats

def save_summary(df, subjects, outdir):
    summary_cols = META_COLS + subjects + ["total_marks", "percentage", "grade"]
    summary = df[summary_cols].copy()
    summary.to_csv(os.path.join(outdir, "summary.csv"), index=False)
    return summary

def save_subject_stats(stats, outdir):
    stats.to_csv(os.path.join(outdir, "subject_stats.csv"))

def pivot_semesters(df, outdir):
    pivot = df.pivot_table(index=["student_id", "name"], columns="semester", values="percentage")
    pivot.to_csv(os.path.join(outdir, "student_semester_percentages.csv"))
    return pivot

def plot_avg_marks(stats, outdir):
    plt.figure(figsize=(8,5))
    plt.bar(stats.index, stats["avg"])
    plt.title("Average Marks per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    p = os.path.join(outdir, "avg_marks_per_subject.png")
    plt.savefig(p)
    plt.close()
    return p

def plot_student_trends(df, outdir, top_n=None):
    # For each student, plot trend of percentage vs semester
    saved = []
    grouped = df.groupby(["student_id", "name"])
    for (sid, sname), group in grouped:
        sem_perf = group.sort_values("semester")[["semester", "percentage"]].dropna()
        if sem_perf.empty:
            continue
        plt.figure(figsize=(7,4))
        plt.plot(sem_perf["semester"], sem_perf["percentage"], marker="o")
        plt.title(f"{sname} ({sid}) - Semester Trend")
        plt.xlabel("Semester")
        plt.ylabel("Percentage")
        plt.ylim(0, 100)
        plt.grid(axis='y', linestyle='--', linewidth=0.5)
        fname = os.path.join(outdir, f"{sid}_{sname}_semester_trend.png")
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        saved.append(fname)
    return saved

# ---------- CLI ----------
def main(args):
    df = load_data(args.data)
    print(f"Loaded data: {df.shape} rows x columns")
    df, subjects = clean_and_infer(df)
    print("Detected subject columns:", subjects)

    df = compute_totals(df, subjects, treat_missing_as_zero=args.treat_missing_as_zero)

    stats = subject_stats(df, subjects)
    save_subject_stats(stats, OUTPUT_DIR)
    print("Subject stats saved.")

    summary = save_summary(df, subjects, OUTPUT_DIR)
    print("Summary saved.")

    pivot = pivot_semesters(df, OUTPUT_DIR)
    print("Student-semester pivot saved.")

    avg_plot = plot_avg_marks(stats, OUTPUT_DIR)
    print("Avg marks plot saved:", avg_plot)

    student_plots = plot_student_trends(df, OUTPUT_DIR)
    print(f"Saved {len(student_plots)} student trend plots.")

    # Quick console prints
    print("\nTop students by percentage:")
    print(summary.sort_values("percentage", ascending=False)[["student_id","name","percentage","grade"]].head(10).to_string(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Student Performance Dashboard (Pandas + NumPy + Matplotlib)")
    parser.add_argument("--data", type=str, default=DEFAULT_DATA, help="Path to marks CSV/XLSX")
    parser.add_argument("--treat-missing-as-zero", action="store_true", help="Fill missing subject marks as zero before summing")
    args = parser.parse_args()
    main(args)
