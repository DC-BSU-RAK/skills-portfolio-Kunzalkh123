import tkinter as tk
from tkinter import ttk, messagebox
import os

FILE_PATH = "Exercise3/studentMarks.txt"  # Path to the file containing student data

def load_students(file_path):
    """
    Load student data from the file.
    Returns a list of dictionaries containing student data.
    """
    students = []  # List to store all student data
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass  # Create empty file
            return students
        
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Read all lines from the file
            for line in lines:  # Read every line, including the first one
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                student_data = line.split(',')  # Split each line by comma
                if len(student_data) == 6:  # Ensure the data is complete
                    student = {
                        "id": int(student_data[0]),  # Convert ID to integer
                        "name": student_data[1],  # Student name
                        "marks": list(map(int, student_data[2:5])),  # Convert marks to integers
                        "exam": int(student_data[5])  # Exam mark as integer
                    }
                    students.append(student)  # Add student to the list
    except:
        pass
    return students

def save_students(file_path, students):
    """
    Save student data to the file.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as file:
            for student in students:
                # Write each student's data to the file
                record = f"{student['id']},{student['name']},{','.join(map(str, student['marks']))},{student['exam']}\n"
                file.write(record)
    except Exception as e:
        # If there is an error saving, show an error message
        messagebox.showerror("Error", f"Error saving data: {e}")

def calculate_total(student):
    """
    Calculate total marks and percentage for a student.
    """
    total_coursework = sum(student["marks"])  # Sum of the coursework marks
    total_marks = total_coursework + student["exam"]  # Total marks (coursework + exam)
    percentage = (total_marks / 160) * 100  # Calculate percentage based on total possible marks (160)
    grade = get_grade(percentage)  # Get the grade based on percentage
    return total_coursework, student["exam"], total_marks, percentage, grade  # Return all calculated values

def get_grade(percentage):
    """
    Determine the grade based on the percentage.
    """
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
    """
    View all students in a table.
    """
    # Remove all existing rows from the treeview
    for i in tree.get_children():
        tree.delete(i)

    # Insert all students into the treeview with calculated data
    for student in students:
        total_coursework, exam, total, percentage, grade = calculate_total(student)
        tree.insert("", "end", values=(student["id"], student["name"], total_coursework, exam, total, f"{percentage:.2f}%", grade))

def add_student():
    """
    Add a new student.
    """
    try:
        # Get input values from the entry fields
        id_ = int(id_entry.get())  # Student ID
        name = name_entry.get().strip()  # Student name
        
        # Validate name is not empty
        if not name:
            raise ValueError("Name cannot be empty.")
        
        # Check for duplicate ID
        if any(student["id"] == id_ for student in students):
            raise ValueError(f"Student ID {id_} already exists.")
        
        marks = list(map(int, marks_entry.get().split(',')))  # Convert marks from string to list of integers
        exam = int(exam_entry.get())  # Exam marks

        if len(marks) != 3:
            raise ValueError("Coursework marks must have exactly 3 values.")  # Validate marks input
        
        # Validate marks are non-negative
        if any(mark < 0 for mark in marks) or exam < 0:
            raise ValueError("Marks cannot be negative.")

        # Append the new student to the list
        students.append({"id": id_, "name": name, "marks": marks, "exam": exam})
        save_students(FILE_PATH, students)  # Save updated student data to file
        view_all_students()  # Refresh the student table
        clear_entries()  # Clear input fields
        messagebox.showinfo("Success", "Student added successfully.")  # Show success message
    except ValueError as e:
        # Show error message if input is invalid
        messagebox.showerror("Error", f"Invalid input: {e}")

def delete_student():
    """
    Delete a selected student.
    """
    selected_item = tree.selection()  # Get the selected item in the treeview
    if not selected_item:
        messagebox.showwarning("Warning", "No student selected.")  # Show warning if no student is selected
        return

    # Confirm deletion
    response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if not response:
        return

    selected_student_id = int(tree.item(selected_item[0], "values")[0])  # Get student ID from selected row
    global students
    # Remove the student with the selected ID from the list
    students = [student for student in students if student["id"] != selected_student_id]

    save_students(FILE_PATH, students)  # Save updated student data to file
    view_all_students()  # Refresh the student table
    messagebox.showinfo("Success", "Student deleted successfully.")  # Show success message

def clear_entries():
    """
    Clear input fields.
    """
    # Clear the content of each entry field
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    exam_entry.delete(0, tk.END)

# Load initial student data from file
students = load_students(FILE_PATH)

# Create main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("900x500")
root.configure(bg="pink")

# Frames for layout
input_frame = tk.Frame(root, padx=10, pady=10, bg="pink")
input_frame.pack(side=tk.TOP, fill=tk.X)

table_frame = tk.Frame(root, padx=10, pady=10, bg="pink")
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Input fields for adding students
tk.Label(input_frame, text="ID:", bg="pink").grid(row=0, column=0, padx=5, pady=5)
id_entry = tk.Entry(input_frame, width=10)
id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Name:", bg="pink").grid(row=0, column=2, padx=5, pady=5)
name_entry = tk.Entry(input_frame, width=15)
name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Marks (3 values, comma-separated):", bg="pink").grid(row=0, column=4, padx=5, pady=5)
marks_entry = tk.Entry(input_frame, width=15)
marks_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(input_frame, text="Exam:", bg="pink").grid(row=0, column=6, padx=5, pady=5)
exam_entry = tk.Entry(input_frame, width=10)
exam_entry.grid(row=0, column=7, padx=5, pady=5)

# Buttons for actions
add_button = tk.Button(input_frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white")
add_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

delete_button = tk.Button(input_frame, text="Delete Student", command=delete_student, bg="#f44336", fg="white")
delete_button.grid(row=1, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

view_button = tk.Button(input_frame, text="View All Students", command=view_all_students, bg="#2196F3", fg="white")
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
    tree.column(col, anchor="center", width=100)

# Add vertical scrollbar to the table
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Initialize the table view with all students
view_all_students()

# Start the Tkinter application
root.mainloop()