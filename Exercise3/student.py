import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

FILE_PATH = "Exercise3/studentMarks.txt"  # Path to the file containing student data

def load_students(file_path):
    """Load student data from the file."""
    students = []
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("0\n")
            return students
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) == 0:
                return students
            
            # Skip first line (number of students)
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                student_data = line.split(',')
                if len(student_data) == 6:
                    student = {
                        "id": int(student_data[0]),
                        "name": student_data[1],
                        "marks": list(map(int, student_data[2:5])),
                        "exam": int(student_data[5])
                    }
                    students.append(student)
    except:
        pass
    return students

def save_students(file_path, students):
    """Save student data to the file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as file:
            file.write(f"{len(students)}\n")
            for student in students:
                record = f"{student['id']},{student['name']},{','.join(map(str, student['marks']))},{student['exam']}\n"
                file.write(record)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

def calculate_total(student):
    """Calculate total marks and percentage for a student."""
    total_coursework = sum(student["marks"])
    total_marks = total_coursework + student["exam"]
    percentage = (total_marks / 160) * 100
    grade = get_grade(percentage)
    return total_coursework, student["exam"], total_marks, percentage, grade

def get_grade(percentage):
    """Determine the grade based on the percentage."""
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def view_all_students():
    """View all students in a table."""
    for i in tree.get_children():
        tree.delete(i)

    if not students:
        messagebox.showinfo("OPPSSS", "No students in the system.")
        return

    total_percentage = 0
    for student in students:
        total_coursework, exam, total, percentage, grade = calculate_total(student)
        total_percentage += percentage
        tree.insert("", "end", values=(student["id"], student["name"], total_coursework, exam, total, f"{percentage:.2f}%", grade))
    
    # Show summary
    avg_percentage = total_percentage / len(students)
    summary_text.config(state='normal')
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, f"Total Students: {len(students)}\n")
    summary_text.insert(tk.END, f"Average Percentage: {avg_percentage:.2f}%")
    summary_text.config(state='disabled')

def view_individual_student():
    """View individual student record."""
    search_window = tk.Toplevel(root)
    search_window.title("Individual Student")
    search_window.geometry("400x300")
    search_window.configure(bg="pink")
    

    tk.Label(search_window, text="Enter Student ID:", bg="pink", font=("Arial", 12)).pack(pady=20)
    search_entry = tk.Entry(search_window, font=("Arial", 12))
    search_entry.pack(pady=10)
    
    result_text = scrolledtext.ScrolledText(search_window, height=8, width=45, font=("Arial", 10))
    result_text.pack(pady=10)
    
    def search():
        try:
            student_id = int(search_entry.get())
            found = None
            for student in students:
                if student["id"] == student_id:
                    found = student
                    break
            
            if found:
                total_coursework, exam, total, percentage, grade = calculate_total(found)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Student ID: {found['id']}\n")
                result_text.insert(tk.END, f"Name: {found['name']}\n")
                result_text.insert(tk.END, f"Coursework Marks: {', '.join(map(str, found['marks']))}\n")
                result_text.insert(tk.END, f"Total Coursework: {total_coursework}\n")
                result_text.insert(tk.END, f"Exam Mark: {exam}\n")
                result_text.insert(tk.END, f"Total Marks: {total}\n")
                result_text.insert(tk.END, f"Percentage: {percentage:.2f}%\n")
                result_text.insert(tk.END, f"Grade: {grade}\n")
            else:
                messagebox.showwarning("Not Found", f"Student with ID {student_id} not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student ID.")
    
    tk.Button(search_window, text="Search", command=search, bg="#2196F3", fg="white", font=("Arial", 10)).pack(pady=10)

def show_highest_score():
    """Show student with highest total score."""
    if not students:
        messagebox.showinfo("Info", "No students in the system.")
        return
    
    highest_student = max(students, key=lambda s: sum(s["marks"]) + s["exam"])
    total_coursework, exam, total, percentage, grade = calculate_total(highest_student)
    
    result_window = tk.Toplevel(root)
    result_window.title("Highest Score")
    result_window.geometry("400x300")
    result_window.configure(bg="pink")
    
    tk.Label(result_window, text="Student with Highest Total Score", bg="pink", font=("Arial", 14, "bold")).pack(pady=20)
    
    result_text = scrolledtext.ScrolledText(result_window, height=8, width=45, font=("Arial", 10))
    result_text.pack(pady=10)
    
    result_text.insert(tk.END, f"Student ID: {highest_student['id']}\n")
    result_text.insert(tk.END, f"Name: {highest_student['name']}\n")
    result_text.insert(tk.END, f"Total Coursework: {total_coursework}\n")
    result_text.insert(tk.END, f"Exam Mark: {exam}\n")
    result_text.insert(tk.END, f"Total Marks: {total}\n")
    result_text.insert(tk.END, f"Percentage: {percentage:.2f}%\n")
    result_text.insert(tk.END, f"Grade: {grade}\n")
    result_text.config(state='disabled')

def show_lowest_score():
    """Show student with lowest total score."""
    if not students:
        messagebox.showinfo("Info", "No students in the system.")
        return
    
    lowest_student = min(students, key=lambda s: sum(s["marks"]) + s["exam"])
    total_coursework, exam, total, percentage, grade = calculate_total(lowest_student)
    
    result_window = tk.Toplevel(root)
    result_window.title("Lowest Score")
    result_window.geometry("400x300")
    result_window.configure(bg="pink")
    
    tk.Label(result_window, text="Student with Lowest Total Score", bg="pink", font=("Arial", 14, "bold")).pack(pady=20)
    
    result_text = scrolledtext.ScrolledText(result_window, height=8, width=45, font=("Arial", 10))
    result_text.pack(pady=10)
    
    result_text.insert(tk.END, f"Student ID: {lowest_student['id']}\n")
    result_text.insert(tk.END, f"Name: {lowest_student['name']}\n")
    result_text.insert(tk.END, f"Total Coursework: {total_coursework}\n")
    result_text.insert(tk.END, f"Exam Mark: {exam}\n")
    result_text.insert(tk.END, f"Total Marks: {total}\n")
    result_text.insert(tk.END, f"Percentage: {percentage:.2f}%\n")
    result_text.insert(tk.END, f"Grade: {grade}\n")
    result_text.config(state='disabled')

# Load initial student data from file
students = load_students(FILE_PATH)

# Create main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x500")
root.configure(bg="pink")

# Menu Bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# View Menu
view_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="View All Students", command=view_all_students)
view_menu.add_command(label="View Individual Student", command=view_individual_student)
view_menu.add_separator()
view_menu.add_command(label="Highest Score", command=show_highest_score)
view_menu.add_command(label="Lowest Score", command=show_lowest_score)

# Frames for layout
table_frame = tk.Frame(root, padx=10, pady=10, bg="pink")
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

summary_frame = tk.Frame(root, padx=10, pady=5, bg="pink")
summary_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Table for displaying student data
columns = ("ID", "Name", "Coursework", "Exam", "Total", "Percentage", "Grade")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Define table headers and column properties
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

# Add vertical scrollbar to the table
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Summary text box
tk.Label(summary_frame, text="Summary:", bg="pink", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
summary_text = tk.Text(summary_frame, height=2, width=50, bg="lightyellow", state='disabled')
summary_text.pack(side=tk.LEFT, padx=5)

# Initialize the table view with all students
view_all_students()

# Start the Tkinter application
root.mainloop()