# 🎓 EduMetrics - Student Performance Dashboard

**EduMetrics** is a comprehensive Python-based data analysis tool designed for educational institutions. Originally built for general student grading, it has been upgraded to support **B.Tech (Computer Science)** curriculums, multi-class management, and interactive visualizations.

It automates the processing of exam scores, calculates grades, generates PDF report cards, and allows for interactive data exploration via a web GUI.

## 🚀 Features

### Core Features
* **⚡ Automated Grading:** Instantly calculates Total, Percentage, and Grades (A+, A, B, C, F) using NumPy vectorization.
* **📄 PDF Report Cards:** Generates professional, printable PDF result sheets for every student.
* **📊 Advanced Visualizations:**
    * **Bar Chart:** Subject-wise class averages.
    * **Pie Chart:** Overall class grade distribution.
* **🏆 Leaderboard:** Automatically identifies top performers in the batch.

### 🆕 New Features (v2.0)
* **🖥️ Interactive GUI:** A user-friendly web dashboard built with **Streamlit** to filter data and view charts dynamically.
* **📧 Email Automation:** Automatically sends PDF report cards to parents/students via SMTP (Gmail).
* **🏫 Multi-Class Support:** Groups data by Section/Class (e.g., "CS-A", "CS-B") and generates separate reports for each.
* **🎓 B.Tech CS Curriculum:** Pre-configured for subjects like Data Structures, DBMS, OS, and Algorithms.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Matplotlib, Streamlit (GUI)
* **Report Generation:** FPDF
* **Automation:** smtplib (Email), OS

## 📂 Project Structure

```text
EduMetrics/
│
├── dashboard.py               # Legacy CLI application source code
├── app.py                     # NEW: Streamlit GUI application
├── student_marks.csv          # Input data file (B.Tech CS format)
├── summary_report_CS-A.csv    # Output: Processed data for Class A
├── summary_report_CS-B.csv    # Output: Processed data for Class B
│
├── student_reports/           # Generated PDF Report Cards stored here
│   ├── Aryan Khanna_Sem3_Report.pdf
│   └── ...
│
├── subject_performance_bar.png # Generated Bar Chart
├── grade_distribution_pie.png  # Generated Pie Chart
└── README.md                  # Project Documentation
````

## ⚙️ Installation

1.  Clone this repository.
2.  Install the required Python libraries:

<!-- end list -->

```bash
pip install pandas numpy matplotlib fpdf openpyxl streamlit
```

## 🏃‍♂️ How to Run

### Option 1: Interactive GUI (Recommended)

Launch the web dashboard to visualize data and filter by grades.

```bash
streamlit run app.py
```

### Option 2: Command Line (Automation)

Run the script to process data, generate PDFs, and send emails in the background.

```bash
python dashboard.py
```

*Note: Ensure you have configured your Email credentials in `dashboard.py` before running the email function.*

## 📝 Input Data Format (`student_marks.csv`)

The input CSV must now include a **`Class`** column and the relevant B.Tech subjects.

**Structure:**

```csv
Student_ID,Name,Class,Semester,DataStructures,DBMS,OperatingSystems,ComputerNetworks,Algorithms
201,Aryan Khanna,CS-A,3,85,88,82,78,90
202,Ishita Verma,CS-A,3,92,95,90,88,94
...
```

## 🔧 Configuration

### 1\. Changing Subjects

To adapt this tool for other streams (e.g., Mechanical, Commerce), update the `SUBJECTS` list in both `dashboard.py` and `app.py`:

```python
SUBJECTS = ['Math', 'Physics', 'Chemistry'] # Example
```

### 2\. Email Setup

To enable email features, update the `send_email_reports` function in `dashboard.py`:

  * **SENDER\_EMAIL:** Your Gmail address.
  * **SENDER\_PASSWORD:** Your Gmail **App Password** (not your login password).

-----

*Created by [Dharm Patel](https://github.com/Dharm3112)*
