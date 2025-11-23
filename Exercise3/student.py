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
        messagebox.showinfo("Info", "No students in the system.")
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
    search_window.title("View Individual Student")
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

def add_student():
    """Add a new student."""
    try:
        id_ = int(id_entry.get())
        name = name_entry.get().strip()
        
        if not name:
            raise ValueError("Name cannot be empty.")
        
        if not (1000 <= id_ <= 9999):
            raise ValueError("Student ID must be between 1000 and 9999.")
        
        if any(student["id"] == id_ for student in students):
            raise ValueError(f"Student ID {id_} already exists.")
        
        marks = list(map(int, marks_entry.get().split(',')))
        exam = int(exam_entry.get())

        if len(marks) != 3:
            raise ValueError("Coursework marks must have exactly 3 values.")
        
        if any(mark < 0 or mark > 20 for mark in marks):
            raise ValueError("Coursework marks must be between 0 and 20.")
        
        if exam < 0 or exam > 100:
            raise ValueError("Exam mark must be between 0 and 100.")

        students.append({"id": id_, "name": name, "marks": marks, "exam": exam})
        save_students(FILE_PATH, students)
        view_all_students()
        clear_entries()
        messagebox.showinfo("Success", "Student added successfully.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def delete_student():
    """Delete a selected student."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No student selected.")
        return

    response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if not response:
        return

    selected_student_id = int(tree.item(selected_item[0], "values")[0])
    global students
    students = [student for student in students if student["id"] != selected_student_id]

    save_students(FILE_PATH, students)
    view_all_students()
    messagebox.showinfo("Success", "Student deleted successfully.")

def clear_entries():
    """Clear input fields."""
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    exam_entry.delete(0, tk.END)

# Load initial student data from file
students = load_students(FILE_PATH)

# Create main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x600")
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
input_frame = tk.Frame(root, padx=10, pady=10, bg="pink")
input_frame.pack(side=tk.TOP, fill=tk.X)

table_frame = tk.Frame(root, padx=10, pady=10, bg="pink")
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

summary_frame = tk.Frame(root, padx=10, pady=5, bg="pink")
summary_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Input fields for adding students
tk.Label(input_frame, text="ID (1000-9999):", bg="pink").grid(row=0, column=0, padx=5, pady=5)
id_entry = tk.Entry(input_frame, width=12)
id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Name:", bg="pink").grid(row=0, column=2, padx=5, pady=5)
name_entry = tk.Entry(input_frame, width=15)
name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Marks (3 values, 0-20):", bg="pink").grid(row=0, column=4, padx=5, pady=5)
marks_entry = tk.Entry(input_frame, width=12)
marks_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(input_frame, text="Exam (0-100):", bg="pink").grid(row=0, column=6, padx=5, pady=5)
exam_entry = tk.Entry(input_frame, width=10)
exam_entry.grid(row=0, column=7, padx=5, pady=5)

# Buttons for actions
add_button = tk.Button(input_frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white")
add_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

delete_button = tk.Button(input_frame, text="Delete Student", command=delete_student, bg="#f44336", fg="white")
delete_button.grid(row=1, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

view_button = tk.Button(input_frame, text="Refresh View", command=view_all_students, bg="#2196F3", fg="white")
view_button.grid(row=1, column=4, columnspan=2, padx=5, pady=10, sticky="ew")

clear_button = tk.Button(input_frame, text="Clear Fields", command=clear_entries, bg="#FF9800", fg="white")
clear_button.grid(row=1, column=6, columnspan=2, padx=5, pady=10, sticky="ew")

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