import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dashboard import calculate_performance, SUBJECTS  # Import logic from your existing script

st.set_page_config(page_title="EduMetrics Dashboard", page_icon="🎓")

st.title("🎓 EduMetrics - Student Performance Dashboard")

# 1. File Upload
uploaded_file = st.file_uploader("Upload student_marks.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Process Data
    df = calculate_performance(df)

    # 2. Key Metrics
    st.subheader("📊 Class Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df))
    col1.metric("Class Average", f"{df['Percentage'].mean():.2f}%")

    top_student = df.loc[df['Percentage'].idxmax()]
    col2.metric("Top Performer", top_student['Name'], f"{top_student['Percentage']:.2f}%")

    # 3. Visualizations
    st.subheader("📈 Performance Analysis")

    tab1, tab2 = st.tabs(["Subject Averages (Bar)", "Grade Distribution (Pie)"])

    with tab1:
        avg_marks = df[SUBJECTS].mean()
        fig_bar, ax_bar = plt.subplots()
        ax_bar.bar(SUBJECTS, avg_marks, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336'])
        ax_bar.set_title("Average Marks per Subject")
        st.pyplot(fig_bar)

    with tab2:
        grade_counts = df['Grade'].value_counts()
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%',
                   colors=['gold', 'lightblue', 'lightgreen', 'orange', 'red'])
        ax_pie.set_title("Grade Distribution")
        st.pyplot(fig_pie)

    # 4. Detailed Data Table
    st.subheader("📝 Student Details")
    st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'))

    # 5. Filter by Grade
    grade_filter = st.multiselect("Filter by Grade", options=df['Grade'].unique(), default=df['Grade'].unique())
    filtered_df = df[df['Grade'].isin(grade_filter)]
    st.write(f"Showing {len(filtered_df)} students")
    st.dataframe(filtered_df)

else:
    st.info("Please upload a CSV file to begin.")
