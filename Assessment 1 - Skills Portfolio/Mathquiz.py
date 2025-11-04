from tkinter import *  # Import Tkinter
import tkinter as tk
import time 
import random
from PIL import Image, ImageTk
class MathQuizApp:
    def _init_(self, root):
        # Initialize the app with the main window
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("700x500")
        bg = Image.open("mathquiz bg.png")
bg= bg.resize((700, 500))  # same size as window
bg_image = ImageTk.PhotoImage(bg)
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

 # Initialize quiz-related variables
def _init_(self, root):
        self.score = 0  # User's current score
        self.question_num = 0  # Track the current question number
        self.total_questions = 10  # Total number of questions in the quiz
        self.num1 = 0  # First number in the question
        self.num2 = 0  # Second number in the question
        self.operation = ""  # The operation to be used (addition or subtraction)
        self.correct_answer = 0  # The correct answer for the current question
        self.start_time = time.time()  # Start time for the quiz to calculate elapsed time
         # Difficulty variable to track selected difficulty level
        self.difficulty = StringVar(value="1")

        # Create the UI widgets (Labels, Buttons, etc.)
        Label(root, text="Math Quiz", font=("Arial", 20)).pack(pady=10)  # Title Label
        Label(root, text="Select Difficulty Level:", font=("Arial", 12)).pack()  # Difficulty prompt

        # Difficulty selection buttons
        Button(root, text="Easy (1-digit)", command=lambda: self.start_quiz(1)).pack(pady=5)
        Button(root, text="Moderate (2-digit)", command=lambda: self.start_quiz(2)).pack(pady=5)
        Button(root, text="Advanced (4-digit)", command=lambda: self.start_quiz(3)).pack(pady=5)

        # Label to display the question
        self.question_label = Label(root, text="", font=("Arial", 14))
        self.question_label.pack(pady=10)
          # Text entry for the user to input their answer
        self.answer_var = StringVar()
        self.answer_entry = Entry(root, textvariable=self.answer_var, font=("Arial", 12))
        self.answer_entry.pack()

        # Submit button to check the user's answer
        self.submit_button = Button(root, text="Submit Answer", command=self.check_answer, state="disabled")
        self.submit_button.pack(pady=10)

        # Label for providing feedback after submitting an answer
        self.feedback_label = Label(root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=5)

        # Progress label to show which question the user is on
        self.progress_label = Label(root, text="", font=("Arial", 10))
        self.progress_label.pack(pady=5)

def random_int(self, difficulty):
        """Generates a random integer based on the selected difficulty."""
        if difficulty == 1:  # Easy: 1-digit numbers
            return random.randint(1, 9)
        elif difficulty == 2:  # Moderate: 2-digit numbers
            return random.randint(10, 99)
        elif difficulty == 3:  # Advanced: 4-digit numbers
            return random.randint(1000, 9999)
def decide_operation(self):
        """Randomly selects either addition or subtraction for the current question."""
        return random.choice(['+', '-'])