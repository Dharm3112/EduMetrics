import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
INPUT_FILE = 'student_marks.csv'
OUTPUT_FILE = 'summary_report.csv'
SUBJECTS = ['Math', 'Science', 'English', 'History', 'Computer']

def load_data(filepath):
    """
    Step 1: Read marks from CSV.
    """
    if not os.path.exists(filepath):
        print(f"Error: The file '{filepath}' was not found.")
        return None
    
    print("Loading data...")
    df = pd.read_csv(filepath)
    return df

def calculate_performance(df):
    """
    Step 2: Calculate Total, Percentage, and Grade using NumPy.
    """
    print("Calculating performance metrics...")
    
    # Calculate Total Marks (Summing the subject columns)
    df['Total_Marks'] = df[SUBJECTS].sum(axis=1)
    
    # Calculate Percentage (Assuming each subject is out of 100)
    total_possible_marks = len(SUBJECTS) * 100
    df['Percentage'] = (df['Total_Marks'] / total_possible_marks) * 100
    
    # Calculate Grade using NumPy's select
    conditions = [
        (df['Percentage'] >= 90),
        (df['Percentage'] >= 80),
        (df['Percentage'] >= 70),
        (df['Percentage'] >= 60),
        (df['Percentage'] < 60)
    ]
    
    grades = ['A+', 'A', 'B', 'C', 'F']
    
    # --- THE FIX IS HERE ---
    # We added "default='F'" so it doesn't try to use the number 0
    df['Grade'] = np.select(conditions, grades, default='F')
    
    return df

def perform_subject_analysis(df):
    """
    Step 3: Subject-wise analysis (avg, max, min).
    """
    print("\n--- Subject-Wise Analysis ---")
    
    # We create a dictionary to store stats to easily convert to DataFrame later if needed
    analysis = {}
    
    for subject in SUBJECTS:
        avg_mark = df[subject].mean()
        max_mark = df[subject].max()
        min_mark = df[subject].min()
        
        analysis[subject] = {'Average': avg_mark, 'Max': max_mark, 'Min': min_mark}
        
        print(f"{subject}: Avg={avg_mark:.2f}, Max={max_mark}, Min={min_mark}")
        
    return analysis

def plot_graphs(df):
    """
    Step 4: Generate Graphs (Bar Chart and Line Chart).
    """
    print("\nGenerating graphs...")
    
    # --- GRAPH 1: Average Subject-Wise Marks (Bar Chart) ---
    avg_marks = df[SUBJECTS].mean()
    
    plt.figure(figsize=(10, 6))
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336'] # Custom colors
    plt.bar(SUBJECTS, avg_marks, color=colors)
    
    plt.title('Class Average Marks per Subject')
    plt.xlabel('Subjects')
    plt.ylabel('Average Marks')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the plot
    plt.savefig('subject_performance_bar.png')
    print("Graph saved: subject_performance_bar.png")
    plt.show() # Show the plot window

    # --- GRAPH 2: Student Performance Over Semesters (Line Chart) ---
    # We will pick one student to visualize (e.g., John Doe - ID 101)
    student_id = 101
    student_data = df[df['Student_ID'] == student_id]
    
    if not student_data.empty:
        student_name = student_data.iloc[0]['Name']
        
        plt.figure(figsize=(10, 6))
        plt.plot(student_data['Semester'], student_data['Percentage'], marker='o', linestyle='-', color='b', linewidth=2)
        
        plt.title(f'Performance Trend: {student_name} (Over Semesters)')
        plt.xlabel('Semester')
        plt.ylabel('Percentage')
        plt.xticks(student_data['Semester']) # Ensure only integer semesters are shown
        plt.ylim(0, 100)
        plt.grid(True)
        
        # Save the plot
        plt.savefig(f'student_{student_id}_trend_line.png')
        print(f"Graph saved: student_{student_id}_trend_line.png")
        plt.show()
    else:
        print(f"Student ID {student_id} not found for Line Chart.")

def export_summary(df):
    """
    Step 5: Export summary to CSV.
    """
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSuccess! Summary report exported to '{OUTPUT_FILE}'")
    except Exception as e:
        print(f"Error exporting file: {e}")

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # 1. Load
    data = load_data(INPUT_FILE)
    
    if data is not None:
        # 2. Process
        processed_data = calculate_performance(data)
        
        # Show top 5 rows in console
        print("\n--- Processed Data Preview ---")
        print(processed_data[['Name', 'Semester', 'Total_Marks', 'Percentage', 'Grade']].head())

        # 3. Analyze
        perform_subject_analysis(processed_data)
        
        # 4. Visualize
        plot_graphs(processed_data)
        
        # 5. Export
        export_summary(processed_data)