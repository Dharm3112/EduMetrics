import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_reports(df):
    print("\n--- 📧 Sending Email Reports ---")

    # EMAIL CONFIGURATION (Replace with your details)
    SENDER_EMAIL = "your_email@gmail.com"
    SENDER_PASSWORD = "your_app_password"  # Use App Password, not login password
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    try:
        # Connect to Server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for index, row in df.iterrows():
            if 'Parent_Email' not in row or pd.isna(row['Parent_Email']):
                print(f"Skipping {row['Name']}: No email found.")
                continue

            # Email Content
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = row['Parent_Email']
            msg['Subject'] = f"Exam Results: {row['Name']}"

            body = f"Dear Parent,\n\nPlease find attached the report card for {row['Name']}.\n\nResults:\nPercentage: {row['Percentage']:.2f}%\nGrade: {row['Grade']}\n\nBest Regards,\nSchool Admin"
            msg.attach(MIMEText(body, 'plain'))

            # Attach PDF
            pdf_filename = f"student_reports/{row['Name']}_Sem{row['Semester']}_Report.pdf"
            if os.path.exists(pdf_filename):
                with open(pdf_filename, "rb") as f:
                    attach = MIMEApplication(f.read(), _subtype="pdf")
                    attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_filename))
                    msg.attach(attach)

                # Send
                server.send_message(msg)
                print(f"✅ Sent email to {row['Name']} ({row['Parent_Email']})")
            else:
                print(f"❌ PDF not found for {row['Name']}")

        server.quit()
        print("All emails processed.")

    except Exception as e:
        print(f"Error sending email: {e}")


# --- CONFIGURATION ---
INPUT_FILE = 'student_marks.csv'
OUTPUT_FILE = 'summary_report.csv'
REPORT_DIR = 'student_reports'  # Folder to save PDFs
SUBJECTS = ['DataStructures', 'DBMS', 'OperatingSystems', 'ComputerNetworks', 'Algorithms']


def load_data(filepath):
    if not os.path.exists(filepath):
        print(f"Error: The file '{filepath}' was not found.")
        return None
    print("Loading data...")
    return pd.read_csv(filepath)


def calculate_performance(df):
    print("Calculating performance metrics...")
    df['Total_Marks'] = df[SUBJECTS].sum(axis=1)
    total_possible_marks = len(SUBJECTS) * 100
    df['Percentage'] = (df['Total_Marks'] / total_possible_marks) * 100

    conditions = [
        (df['Percentage'] >= 90),
        (df['Percentage'] >= 80),
        (df['Percentage'] >= 70),
        (df['Percentage'] >= 60),
        (df['Percentage'] < 60)
    ]
    grades = ['A+', 'A', 'B', 'C', 'F']

    # FIXED: Added default='F' to prevent the error you saw earlier
    df['Grade'] = np.select(conditions, grades, default='F')
    return df


def analyze_top_performers(df):
    """
    UPGRADE: Identify and print the top 3 students.
    """
    print("\n--- 🏆 Top 3 Performers ---")
    # Sort by Percentage in Descending order (Highest first)
    top_students = df.sort_values(by='Percentage', ascending=False).head(3)

    rank = 1
    for index, row in top_students.iterrows():
        print(f"#{rank}: {row['Name']} - {row['Percentage']:.2f}% (Grade: {row['Grade']})")
        rank += 1


def plot_advanced_graphs(df):
    """
    UPGRADE: Added a Pie Chart for Grade Distribution.
    """
    print("\nGenerating advanced graphs...")

    # 1. Bar Chart (Existing)
    avg_marks = df[SUBJECTS].mean()
    plt.figure(figsize=(10, 6))
    plt.bar(SUBJECTS, avg_marks, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336'])
    plt.title('Class Average Marks per Subject')
    plt.savefig('subject_performance_bar.png')
    plt.close()  # Close to prevent too many windows popping up

    # 2. Grade Distribution Pie Chart (NEW)
    grade_counts = df['Grade'].value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=140,
            colors=['gold', 'lightblue', 'lightgreen', 'orange', 'red'])
    plt.title('Grade Distribution (Class Performance)')
    plt.savefig('grade_distribution_pie.png')
    print("Graphs saved: 'subject_performance_bar.png' and 'grade_distribution_pie.png'")
    # We show the Pie chart to the user
    plt.show()


def generate_pdf_reports(df):
    """
    UPGRADE: Generate a PDF Report Card for EACH student.
    """
    print("\nGenerating PDF Report Cards...")

    # Create directory if it doesn't exist
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    for index, row in df.iterrows():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"Student Report Card", ln=True, align='C')
        pdf.ln(10)  # Line break

        # Student Details
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Name: {row['Name']}", ln=True)
        pdf.cell(200, 10, txt=f"Student ID: {row['Student_ID']}", ln=True)
        pdf.cell(200, 10, txt=f"Semester: {row['Semester']}", ln=True)
        pdf.ln(10)

        # Marks Table Header
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(100, 10, txt="Subject", border=1)
        pdf.cell(50, 10, txt="Marks Obtained", border=1)
        pdf.ln()

        # Marks Rows
        pdf.set_font("Arial", size=12)
        for subject in SUBJECTS:
            pdf.cell(100, 10, txt=subject, border=1)
            pdf.cell(50, 10, txt=str(row[subject]), border=1)
            pdf.ln()

        pdf.ln(10)

        # Final Summary
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Total Marks: {row['Total_Marks']} / {len(SUBJECTS) * 100}", ln=True)
        pdf.cell(200, 10, txt=f"Percentage: {row['Percentage']:.2f}%", ln=True)
        pdf.set_text_color(255, 0, 0) if row['Grade'] == 'F' else pdf.set_text_color(0, 128, 0)
        pdf.cell(200, 10, txt=f"Final Grade: {row['Grade']}", ln=True)

        # Save PDF
        filename = f"{REPORT_DIR}/{row['Name']}_Sem{row['Semester']}_Report.pdf"
        pdf.output(filename)

    print(f"Success! All report cards saved in the '{REPORT_DIR}' folder.")


def process_multiple_classes(filepath):
    df = load_data(filepath)
    if df is None: return

    # Check if 'Class' column exists
    if 'Class' not in df.columns:
        print("Warning: 'Class' column not found. Processing as single class.")
        # ... Run original logic ...
        return

    # Group by Class
    grouped = df.groupby('Class')

    for class_name, class_df in grouped:
        print(f"\n==========================================")
        print(f"🏫 Processing Class: {class_name}")
        print(f"==========================================")

        # 1. Calculate Performance for this class
        processed_df = calculate_performance(class_df.copy())

        # 2. Analyze Top Performers for this class
        analyze_top_performers(processed_df)

        # 3. Generate Visualizations (Save with unique names)
        # Note: You'll need to update plot_advanced_graphs to accept a prefix/filename
        # e.g., savefig(f"reports/{class_name}_bar_chart.png")

        # 4. Generate Reports
        generate_pdf_reports(processed_df)  # PDF filename already includes Student Name, so it's safe

        # 5. Save Class Specific CSV
        processed_df.to_csv(f"summary_report_{class_name}.csv", index=False)


if __name__ == "__main__":
    process_multiple_classes(INPUT_FILE)


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    data = load_data(INPUT_FILE)

    if data is not None:
        # 1. Process
        processed_data = calculate_performance(data)

        # 2. Analyze Top Performers (NEW)
        analyze_top_performers(processed_data)

        # 3. Visualizations (UPDATED)
        plot_advanced_graphs(processed_data)

        # 4. Generate PDFs (NEW)
        generate_pdf_reports(processed_data)

        # 5. Export Summary
        processed_data.to_csv(OUTPUT_FILE, index=False)

