from tkinter import *
import tkinter as tk
import time 
import random
from tkinter import messagebox
from PIL import Image, ImageTk

# Create main window
root = tk.Tk()
root.title("WELCOME TO THE MATH QUIZZ!!!!!!")
root.geometry("700x500")

# Global variables for quiz state
score = 0
question_num = 0
total_questions = 10
num1 = 0
num2 = 0
operation = ""
correct_answer = 0
start_time = 0
difficulty = 1

def clearscreen():
    """Clear all widgets from the root window"""
    for widget in root.winfo_children():
        widget.destroy()

def set_background():
    """Set background image for the window"""
    global bg_image_ref
    img = Image.open("mathquiz bg.PNG")
    img = img.resize((700, 500), Image.Resampling.LANCZOS)
    bg_image_ref = ImageTk.PhotoImage(img)
    bg_label = Label(root, image=bg_image_ref)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def introscreen():
    """Display the introduction screen"""
    clearscreen()
    set_background()
    title_frame = Frame(root, bg="#f3ca7e", relief=RIDGE, bd=3)
    title_frame.place(relx=0.5, rely=0.3, anchor=CENTER)
    title_label = Label(title_frame, text="WELCOME TO THE MATH QUIZ!", 
                       font=("Arial", 32, "bold"), 
                       bg="#f3ca7e", 
                       fg="#1976D2",
                       padx=30,
                       pady=15)
    title_label.pack()

    startbutton = Button(root, text="START", font=("Arial", 16, "bold"), 
                         command=levelscreen, bg="#ec407a", fg="white", width=20, height=2)
    startbutton.place(relx=0.5, rely=0.75, anchor=CENTER)

def levelscreen():
    """Display the level selection screen"""
    clearscreen()
    set_background()
    
    # Call the level selection function
    show_level_selection()

def show_level_selection():
    """Show difficulty level selection screen"""

    frame = Frame(root, bg="#f3ca7e", relief=RIDGE, bd=3)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    Label(frame, text="WLCOME TO THE Math Quiz", font=("Arial", 35, "bold"), bg="#f3ca7e", fg='#1976D2').pack(pady=25, padx=50)
    Label(frame, text="Select Difficulty Level:", font=("Arial", 14), bg="#f3ca7e", fg='#424242').pack(pady=15)
    
    # Difficulty selection buttons
    Button(frame, text="Easy (1-digit)", font=("Arial", 13), bg="#4CAF50", fg="white",
           command=lambda: start_quiz(1), width=22, height=2).pack(pady=8)
    Button(frame, text="Moderate (2-digit)", font=("Arial", 13), bg="#FF9800", fg="white",
           command=lambda: start_quiz(2), width=22, height=2).pack(pady=8)
    Button(frame, text="Advanced (4-digit)", font=("Arial", 13), bg="#f44336", fg="white",
           command=lambda: start_quiz(3), width=22, height=2).pack(padx=50, pady=(8, 25))

def random_int(difficulty_level):
    """Generates a random integer based on the selected difficulty."""
    if difficulty_level == 1:  # Easy: 1-digit numbers
        return random.randint(1, 9)
    elif difficulty_level == 2:  # Moderate: 2-digit numbers
        return random.randint(10, 99)
    elif difficulty_level == 3:  # Advanced: 4-digit numbers
        return random.randint(1000, 9999)

def decide_operation():
    """Randomly selects either addition or subtraction for the current question."""
    return random.choice(['+', '-'])

def start_quiz(difficulty_level):
    """Starts the quiz based on the selected difficulty level."""
    global score, question_num, start_time, difficulty
    global question_label, answer_var, answer_entry, submit_button, feedback_label, progress_label
    
    difficulty = difficulty_level
    score = 0
    question_num = 0
    start_time = time.time()
    
    # Clear the window
    clearscreen()
    set_background()
    
    # Home button
    home_btn = Button(root, text="Main Home", font=("Arial", 10), 
                      command=introscreen, bg="#CF4F8F", fg="white", width=10)
    home_btn.place(x=10, y=10)
    
   
    Label(root, text="Math Quiz", font=("Arial", 20, "bold"), bg='white', fg='#1976D2').pack(pady=15)
    
    question_label = Label(root, text="", font=("Arial", 18), bg='white', fg='#212121')
    question_label.pack(pady=20)
    
    answer_var = StringVar()
    answer_entry = Entry(root, textvariable=answer_var, font=("Arial", 16), width=20)
    answer_entry.pack(pady=10)
    answer_entry.bind('<Return>', lambda event: check_answer())
    
    submit_button = Button(root, text="Submit Answer", font=("Arial", 14),
                          command=check_answer, bg="#4CAF50", fg="white", width=15)
    submit_button.pack(pady=10)

    feedback_label = Label(root, text="", font=("Arial", 14), bg='white')
    feedback_label.pack(pady=10)

    progress_label = Label(root, text="", font=("Arial", 12), bg='white', fg='#424242')
    progress_label.pack(pady=10)
    
    # Start with first question
    next_question()

def next_question():
    """Displays the next question in the quiz."""
    global num1, num2, operation, correct_answer, question_num
    
    if question_num < total_questions:
        num1 = random_int(difficulty)
        num2 = random_int(difficulty)
        operation = decide_operation()

        # Adjust for subtraction to avoid negative answers
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1

        # Calculate the correct answer
        if operation == '+':
            correct_answer = num1 + num2
        else:
            correct_answer = num1 - num2

        # Update the question
        question_label.config(text=f"What is {num1} {operation} {num2}?")
        answer_var.set("")
        feedback_label.config(text="")
        progress_label.config(text=f"Question {question_num + 1}/{total_questions} | Score: {score}")
        answer_entry.focus()
    else:
        end_quiz()

def show_answer_feedback(user_answer):
    """Shows whether the user's answer was correct or wrong."""
    if user_answer == correct_answer:
        feedback_label.config(text="Omg you are correct! ✓", fg="green")
    else:
        feedback_label.config(text=f"Oppss wrong answer ✗ Correct answer: {correct_answer}", fg="red")

def check_answer():
    """Checks the user's answer and provides feedback."""
    global score, question_num
    
    user_input = answer_var.get()
    if not user_input or not user_input.lstrip('-').isdigit():
        feedback_label.config(text="Please enter a valid number.", fg="red")
        return

    user_answer = int(user_input)
    show_answer_feedback(user_answer)

    if user_answer == correct_answer:
        score += 10

    question_num += 1
    root.after(1500, next_question)

def end_quiz():
    """Ends the quiz and shows the user's results."""
    elapsed_time = time.time() - start_time
    
    messagebox.showinfo("Quiz Completed",
                       f"Your final score: {score}/100\nTime taken: {elapsed_time:.2f} seconds")
    display_results()

def display_results():
    """Displays the results based on the user's score."""
    clearscreen()
    set_background()
    
    # Home button
    home_btn = Button(root, text="Return back to Home", font=("Arial", 10), 
                      command=introscreen, bg="#E495D0", fg="white", width=20)
    home_btn.place(x=10, y=10)
    
    # Determine grade
    if score >= 90:
        grade = "A+"
        message = "Excellent!!"
        color = "#2E7D32"
    elif score >= 80:
        grade = "A"
        message = "Great job!"
        color = "#388E3C"
    elif score >= 70:
        grade = "B"
        message = "Nice work! Keep practicing!"
        color = "#1976D2"
    elif score >= 60:
        grade = "C"
        message = "Good effort!"
        color = "#F57C00"
    else:
        grade = "D"
        message = "Don't worry, keep trying!"
        color = "#D32F2F"

    # Display results
    Label(root, text="Quiz Results", font=("Arial", 24, "bold"), bg='white', fg='#1976D2').pack(pady=20)
    Label(root, text=f"Final Score: {score}/100", font=("Arial", 18), bg='white', fg='#212121').pack(pady=10)
    Label(root, text=f"Grade: {grade}", font=("Arial", 18), bg='white', fg=color).pack(pady=10)
    Label(root, text=message, font=("Arial", 16), bg='white', fg=color).pack(pady=10)
    
    Button(root, text="Play Again", font=("Arial", 14), 
           command=reset_quiz, bg="#2196F3", fg="white", width=15).pack(pady=15)
    Button(root, text="Exit", font=("Arial", 14), 
           command=root.quit, bg="#f44336", fg="white", width=15).pack(pady=10)

def reset_quiz():
    """Resets the quiz and returns to level selection."""
    levelscreen()

# Start the application
if __name__ == "__main__":
    introscreen()
    root.mainloop()