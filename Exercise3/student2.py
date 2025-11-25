import tkinter as tk
from tkinter import ttk, messagebox,scrolledtext
import os

FILE_PATH = "Exercise3/studentMarks.txt"

def load_students(file_path):
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
            
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 6:
                    student = {
                        "id": int(parts[0]),
                        "name": parts[1],
                        "marks": [int(parts[2]), int(parts[3]), int(parts[4])],
                        "exam": int(parts[5])
                    }
                    students.append(student)
    except:
        pass
    return students

def save_students(file_path, students):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as file:
            file.write(f"{len(students)}\n")
            for s in students:
                line = f"{s['id']},{s['name']},{s['marks'][0]},{s['marks'][1]},{s['marks'][2]},{s['exam']}\n"
                file.write(line)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")

def calculate_stats(student):
    coursework = sum(student["marks"])
    total = coursework + student["exam"]
    percentage = (total / 160) * 100
    
    if percentage >= 70:
        grade = 'A'
    elif percentage >= 60:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    elif percentage >= 40:
        grade = 'D'
    else:
        grade = 'F'
    
    return coursework, total, percentage, grade

def view_all_students():
    for item in tree.get_children():
        tree.delete(item)

    if not students:
        messagebox.showinfo("Info", "No students yet!")
        return

    total_percent = 0
    for student in students:
        coursework, total, percent, grade = calculate_stats(student)
        total_percent += percent
        tree.insert("", "end", values=(
            student["id"], 
            student["name"], 
            coursework, 
            student["exam"], 
            f"{percent:.1f}%", 
            grade
        ))
    
    avg = total_percent / len(students)
    summary_label.config(text=f"Total Students: {len(students)} | Average: {avg:.1f}%")

def view_individual():
    window = tk.Toplevel(root)
    window.title("Find Student")
    window.geometry("400x300")
    window.configure(bg="pink")
    
    tk.Label(window, text="Enter Student ID:", bg="pink", font=("Arial", 11)).pack(pady=20)
    entry = tk.Entry(window, font=("Arial", 12), width=20)
    entry.pack(pady=10)
    
    result = tk.Label(window, text="", bg="pink", font=("Arial", 10), justify="left")
    result.pack(pady=20)
    
    def search():
        try:
            student_id = int(entry.get())
            found = None
            for s in students:
                if s["id"] == student_id:
                    found = s
                    break
            
            if found:
                coursework, total, percent, grade = calculate_stats(found)
                info = f"""
Student ID: {found['id']}
Name: {found['name']}
Coursework: {coursework}/60
Exam: {found['exam']}/100
Total: {total}/160
Percentage: {percent:.1f}%
Grade: {grade}
                """
                result.config(text=info)
            else:
                messagebox.showwarning("Not Found", "Student not found!")
        except:
            messagebox.showerror("Error", "Please enter a valid ID")
    
    tk.Button(window, text="Search", command=search, bg="#2196F3", fg="white", 
              font=("Arial", 10), width=15).pack(pady=10)

def show_highest():
    if not students:
        messagebox.showinfo("Info", "No students yet!")
        return
    
    best = max(students, key=lambda s: sum(s["marks"]) + s["exam"])
    coursework, total, percent, grade = calculate_stats(best)
    
    msg = f"""
Top Student!

Name: {best['name']}
ID: {best['id']}
Total Score: {total}/160
Percentage: {percent:.1f}%
Grade: {grade}
    """
    messagebox.showinfo("Highest Score", msg)

def show_lowest():
    if not students:
        messagebox.showinfo("Info", "No students yet!")
        return
    
    lowest = min(students, key=lambda s: sum(s["marks"]) + s["exam"])
    coursework, total, percent, grade = calculate_stats(lowest)
    
    msg = f"""
Lowest Score

Name: {lowest['name']}
ID: {lowest['id']}
Total Score: {total}/160
Percentage: {percent:.1f}%
Grade: {grade}
    """
    messagebox.showinfo("Lowest Score", msg)

def sort_students():
    window = tk.Toplevel(root)
    window.title("Sort Students")
    window.geometry("300x150")
    window.configure(bg="pink")
    
    tk.Label(window, text="Sort by total marks:", bg="pink", font=("Arial", 11)).pack(pady=20)
    
    def sort_low_high():
        students.sort(key=lambda s: sum(s["marks"]) + s["exam"])
        save_students(FILE_PATH, students)
        view_all_students()
        window.destroy()
        messagebox.showinfo("Done", "Sorted from lowest to highest!")
    
    def sort_high_low():
        students.sort(key=lambda s: sum(s["marks"]) + s["exam"], reverse=True)
        save_students(FILE_PATH, students)
        view_all_students()
        window.destroy()
        messagebox.showinfo("Done", "Sorted from highest to lowest!")
    
    tk.Button(window, text="Low to High", command=sort_low_high, bg="#4CAF50", 
              fg="white", width=20).pack(pady=5)
    tk.Button(window, text="High to Low", command=sort_high_low, bg="#2196F3", 
              fg="white", width=20).pack(pady=5)

def add_student():
    try:
        student_id = int(id_entry.get())
        name = name_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return
        
        if not (1000 <= student_id <= 9999):
            messagebox.showerror("Error", "ID must be between 1000-9999")
            return
        
        if any(s["id"] == student_id for s in students):
            messagebox.showerror("Error", "This ID already exists!")
            return
        
        marks = list(map(int, marks_entry.get().split(',')))
        exam = int(exam_entry.get())

        if len(marks) != 3:
            messagebox.showerror("Error", "Need exactly 3 coursework marks")
            return
        
        if any(m < 0 or m > 20 for m in marks):
            messagebox.showerror("Error", "Coursework marks must be 0-20")
            return
        
        if exam < 0 or exam > 100:
            messagebox.showerror("Error", "Exam mark must be 0-100")
            return

        students.append({"id": student_id, "name": name, "marks": marks, "exam": exam})
        save_students(FILE_PATH, students)
        view_all_students()
        clear_fields()
        messagebox.showinfo("Success", "Student added!")
    except ValueError:
        messagebox.showerror("Error", "Please check your input")

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student first")
        return

    if messagebox.askyesno("Confirm", "Delete this student?"):
        student_id = int(tree.item(selected[0], "values")[0])
        global students
        students = [s for s in students if s["id"] != student_id]
        save_students(FILE_PATH, students)
        view_all_students()
        messagebox.showinfo("Done", "Student deleted!")

def update_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student first")
        return
    
    student_id = int(tree.item(selected[0], "values")[0])
    student = None
    for s in students:
        if s["id"] == student_id:
            student = s
            break
    
    if not student:
        return
    
    window = tk.Toplevel(root)
    window.title("Update Student")
    window.geometry("350x250")
    window.configure(bg="pink")
    
    tk.Label(window, text=f"Editing: {student['name']}", bg="pink", 
             font=("Arial", 12, "bold")).pack(pady=15)
    
    tk.Label(window, text="Name:", bg="pink").pack()
    name_upd = tk.Entry(window, width=30)
    name_upd.insert(0, student['name'])
    name_upd.pack(pady=5)
    
    tk.Label(window, text="Marks (e.g., 15,16,14):", bg="pink").pack()
    marks_upd = tk.Entry(window, width=30)
    marks_upd.insert(0, ','.join(map(str, student['marks'])))
    marks_upd.pack(pady=5)
    
    tk.Label(window, text="Exam:", bg="pink").pack()
    exam_upd = tk.Entry(window, width=30)
    exam_upd.insert(0, student['exam'])
    exam_upd.pack(pady=5)
    
    def save_changes():
        try:
            student['name'] = name_upd.get().strip()
            student['marks'] = list(map(int, marks_upd.get().split(',')))
            student['exam'] = int(exam_upd.get())
            
            if len(student['marks']) != 3:
                messagebox.showerror("Error", "Need 3 marks")
                return
            
            save_students(FILE_PATH, students)
            view_all_students()
            window.destroy()
            messagebox.showinfo("Success", "Updated!")
        except:
            messagebox.showerror("Error", "Please check your input")
    
    tk.Button(window, text="Save", command=save_changes, bg="#4CAF50", 
              fg="white", width=15).pack(pady=15)

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    exam_entry.delete(0, tk.END)

# Load students
students = load_students(FILE_PATH)

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x600")
root.configure(bg="pink")

# Header
header = tk.Frame(root, bg="#34495e", height=60)
header.pack(side=tk.TOP, fill=tk.X)
header.pack_propagate(False)

tk.Label(header, text="STUDENT MANAGEMENT", bg="#d1256d", fg="white", 
         font=("Arial", 20, "bold")).pack(expand=True)

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

view_menu = tk.Menu(menu, tearoff=0, font=("Arial", 11))
menu.add_cascade(label="View", menu=view_menu, font=("Arial", 13))
view_menu.add_command(label="1. All Students", command=view_all_students)
view_menu.add_command(label="2. Find Student", command=view_individual)
view_menu.add_command(label="3. Highest Score", command=show_highest)
view_menu.add_command(label="4. Lowest Score", command=show_lowest)

# Input section
input_frame = tk.Frame(root, bg="pink", pady=10)
input_frame.pack(fill=tk.X, padx=10)

tk.Label(input_frame, text="ID:", bg="pink").grid(row=0, column=0, padx=5)
id_entry = tk.Entry(input_frame, width=12)
id_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Name:", bg="pink").grid(row=0, column=2, padx=5)
name_entry = tk.Entry(input_frame, width=20)
name_entry.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="Marks:", bg="pink").grid(row=0, column=4, padx=5)
marks_entry = tk.Entry(input_frame, width=15)
marks_entry.grid(row=0, column=5, padx=5)

tk.Label(input_frame, text="Exam:", bg="pink").grid(row=0, column=6, padx=5)
exam_entry = tk.Entry(input_frame, width=10)
exam_entry.grid(row=0, column=7, padx=5)

# Buttons
btn_frame = tk.Frame(root, bg="pink")
btn_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Button(btn_frame, text="Add", command=add_student, bg="#4CAF50", fg="white", 
          width=12, height=2).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_student, bg="#f44336", fg="white", 
          width=12, height=2).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Update", command=update_student, bg="#FF9800", fg="white", 
          width=12, height=2).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_fields, bg="#9E9E9E", fg="white", 
          width=12, height=2).pack(side=tk.LEFT, padx=5)

# Table
table_frame = tk.Frame(root, bg="pink")
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Add horizontal scrollbar
h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

columns = ("ID", "Name", "Coursework", "Exam", "Percentage", "Grade")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15, 
                    xscrollcommand=h_scrollbar.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

h_scrollbar.config(command=tree.xview)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Coursework", text="Coursework")
tree.heading("Exam", text="Exam")
tree.heading("Percentage", text="Percentage")
tree.heading("Grade", text="Grade")

tree.column("ID", width=80, anchor="center")
tree.column("Name", width=150, anchor="w")
tree.column("Coursework", width=100, anchor="center")
tree.column("Exam", width=100, anchor="center")
tree.column("Percentage", width=100, anchor="center")
tree.column("Grade", width=80, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Summary
summary_frame = tk.Frame(root, bg="lightpink", pady=10)
summary_frame.pack(fill=tk.X, padx=10, pady=5)

summary_label = tk.Label(summary_frame, text="", bg="lightpink", font=("Arial", 11))
summary_label.pack()

# Show all students on start
view_all_students()

root.mainloop()