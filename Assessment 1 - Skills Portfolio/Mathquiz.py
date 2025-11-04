from tkinter import *  # Import Tkinter
import tkinter as tk
import time 
import random

class MathQuiz:
    def __init__(self, root):
        # Initialize the app with the main window
        self.root = root
        self.root.title("Fun Math Challenge")
        self.root.geometry("750x550")
        self.root.configure(bg='#f0f8ff')  # Light blue background
        
        # Set a nice font scheme
        self.title_font = ("Comic Sans MS", 24, "bold")
        self.header_font = ("Arial", 16, "bold")
        self.normal_font = ("Arial", 14)
        self.button_font = ("Arial", 12, "bold")
        
        self.score = 0
        self.question_num = 0
        self.total_questions = 10
        self.num1 = 0
        self.num2 = 0
        self.operation = ""
        self.correct_answer = 0
        self.start_time = 0
        self.current_frame = None
        self.difficulty = StringVar(value="easy")
        
        # Add some encouraging messages
        self.encouragements = [
            "You're doing great!",
            "Keep going!",
            "Math superstar!",
            "You've got this!",
            "Amazing work!",
            "Brain power!",
            "So smart!",
            "Fantastic!"
        ]
        
        self.display_welcome_screen()

    def display_welcome_screen(self):
        """Display a friendly welcome screen."""
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = Frame(self.root, bg='#f0f8ff')
        self.current_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Welcome title with emoji
        Label(self.current_frame, text="🎉 Welcome to Math Fun! 🎉", 
              font=self.title_font, fg="#2E86AB", bg='#f0f8ff').pack(pady=30)
        
        # Friendly description
        desc_text = "Get ready for a fun math adventure!\nPractice your skills and become a math whiz!"
        Label(self.current_frame, text=desc_text, font=self.normal_font, 
              bg='#f0f8ff', fg="#333333", justify=CENTER).pack(pady=20)
        
        # Difficulty selection with better labels
        Label(self.current_frame, text="Choose Your Challenge Level:", 
              font=self.header_font, fg="#A23B72", bg='#f0f8ff').pack(pady=25)
        
        # Create a frame for buttons
        button_frame = Frame(self.current_frame, bg='#f0f8ff')
        button_frame.pack(pady=10)
        
        # Color-coded difficulty buttons
        Button(button_frame, text="🌟 Easy Starter\nNumbers 1-9", 
               font=self.button_font, bg="#90EE90", fg="black",
               width=20, height=3, 
               command=lambda: self.startQuiz("easy")).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="💪 Moderate Challenge\nNumbers 10-99", 
               font=self.button_font, bg="#FFD700", fg="black",
               width=20, height=3,
               command=lambda: self.startQuiz("moderate")).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="🚀 Advanced Master\nNumbers 100-999", 
               font=self.button_font, bg="#FF6B6B", fg="white",
               width=20, height=3,
               command=lambda: self.startQuiz("advanced")).pack(side=LEFT, padx=10)
        
        # Fun footer
        Label(self.current_frame, text="Remember: Every math expert started with practice!", 
              font=("Arial", 10, "italic"), bg='#f0f8ff', fg="#666666").pack(side=BOTTOM, pady=20)

    def startQuiz(self, level):
        """Start the quiz with friendly encouragement."""
        self.difficulty.set(level)
        self.score = 0
        self.question_num = 0
        self.start_time = time.time()
        
        # Show a quick start message
        level_names = {"easy": "Easy Starter", "moderate": "Moderate Challenge", "advanced": "Advanced Master"}
        start_label = Label(self.root, text=f"Starting {level_names[level]}... Get ready!", 
                           font=self.header_font, bg="#e8f4f8", fg="#2E86AB")
        start_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.root.update()
        time.sleep(1.2)  # Brief pause
        start_label.destroy()
        
        self.show_quiz_screen()

    def get_difficulty_rules(self, level):
        if level == "easy":
            num_range = (1, 9)
        elif level == "moderate":
            num_range = (10, 99)
        else:  # advanced
            num_range = (100, 999)
        return num_range

    def decideOperation(self):
        """Randomly decide between + or -."""
        return random.choice(["+", "-"])

    def generate_question(self):
        """Generate a new math question based on difficulty."""
        level = self.difficulty.get()
        num_range = self.get_difficulty_rules(level)
        
        self.num1 = random.randint(num_range[0], num_range[1])
        self.num2 = random.randint(num_range[0], num_range[1])
        self.operation = self.decideOperation()
        
        if self.operation == "+":
            self.correct_answer = self.num1 + self.num2
        else:  # subtraction
            # Ensure we don't get negative answers
            if self.num1 < self.num2:
                self.num1, self.num2 = self.num2, self.num1
            self.correct_answer = self.num1 - self.num2

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        try:
            if int(user_answer) == self.correct_answer:
                self.score += 1
                return True
            return False
        except ValueError:
            return False

    def show_quiz_screen(self):
        """Display the quiz interface with a friendly design."""
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = Frame(self.root, bg='#f0f8ff')
        self.current_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header with progress and score
        header_frame = Frame(self.current_frame, bg='#f0f8ff')
        header_frame.pack(fill=X, padx=10, pady=10)
        
        # Progress information
        progress_text = f"Question {self.question_num + 1} of {self.total_questions}"
        Label(header_frame, text=progress_text, font=self.normal_font, 
              bg='#f0f8ff', fg="#555555").pack(side=LEFT)
        
        # Score display with emoji
        score_emoji = "⭐" if self.score > 0 else "🔢"
        score_text = f"Score: {self.score} {score_emoji}"
        Label(header_frame, text=score_text, font=self.normal_font, 
              bg='#f0f8ff', fg="#2E86AB").pack(side=RIGHT)
        
        # Random encouragement
        if random.random() > 0.6:  # 40% chance to show encouragement
            encouragement = random.choice(self.encouragements)
            Label(self.current_frame, text=encouragement, font=("Arial", 12, "italic"), 
                  bg='#f0f8ff', fg="#A23B72").pack(pady=5)
        
        # Main question area
        question_frame = Frame(self.current_frame, bg='#f0f8ff')
        question_frame.pack(expand=True, pady=30)
        
        # Generate and display question
        self.generate_question()
        question_text = f"What is {self.num1} {self.operation} {self.num2} ?"
        Label(question_frame, text=question_text, 
              font=("Arial", 22, "bold"), bg='#f0f8ff', fg="#2E86AB").pack(pady=30)
        
        # Answer entry with placeholder text
        answer_frame = Frame(question_frame, bg='#f0f8ff')
        answer_frame.pack(pady=20)
        
        Label(answer_frame, text="Your answer:", font=self.normal_font, 
              bg='#f0f8ff').pack(pady=5)
        
        self.answer_var = StringVar()
        answer_entry = Entry(answer_frame, textvariable=self.answer_var, 
                           font=("Arial", 18), width=8, justify=CENTER,
                           bg='white', relief=SOLID, bd=2)
        answer_entry.pack(pady=10)
        answer_entry.focus()  # Focus on the entry field
        
        # Bind Enter key to submit
        answer_entry.bind('<Return>', lambda event: self.submit_answer())
        
        # Submit button
        Button(question_frame, text="✓ Check Answer", font=self.button_font,
               bg="#4CAF50", fg="white", padx=20, pady=10,
               command=self.submit_answer).pack(pady=15)
        
        # Navigation buttons
        nav_frame = Frame(self.current_frame, bg='#f0f8ff')
        nav_frame.pack(side=BOTTOM, pady=10)
        
        Button(nav_frame, text="🏠 Back to Menu", font=("Arial", 10),
               bg="#666666", fg="white",
               command=self.display_welcome_screen).pack(pady=5)

    def submit_answer(self):
        """Handle answer submission with friendly feedback."""
        user_answer = self.answer_var.get().strip()
        
        if not user_answer:
            # Show message if no answer entered
            no_answer_label = Label(self.current_frame, 
                                   text="Please enter an answer first!",
                                   font=("Arial", 12), fg="orange", bg='#f0f8ff')
            no_answer_label.pack(pady=5)
            self.root.after(1500, no_answer_label.destroy)
            return
            
        is_correct = self.check_answer(user_answer)
        
        # Provide friendly feedback
        if is_correct:
            feedback = f"🎉 Correct! {random.choice(['Well done!', 'Awesome!', 'Perfect!', 'You got it!'])}"
            color = "#2E7D32"  # Dark green
            bg_color = "#C8E6C9"  # Light green
        else:
            feedback = f"💡 The answer is {self.correct_answer}. {random.choice(['Nice try!', 'Almost!', 'Next time!', 'Keep practicing!'])}"
            color = "#C62828"  # Dark red
            bg_color = "#FFCDD2"  # Light red
            
        # Show feedback in a more noticeable way
        feedback_frame = Frame(self.current_frame, bg=bg_color, relief=RAISED, bd=2)
        feedback_frame.pack(pady=10, padx=50, fill=X)
        
        feedback_label = Label(feedback_frame, text=feedback, 
                             font=("Arial", 14, "bold"), fg=color, bg=bg_color)
        feedback_label.pack(pady=10)
        
        # Update the display after a short delay
        self.root.after(2000, self.next_question_or_finish)

    def next_question_or_finish(self):
        """Move to next question or finish quiz."""
        if self.question_num < self.total_questions:
            self.show_quiz_screen()
        else:
            self.show_results()

    def show_results(self):
        """Display final results in a celebratory way."""
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = Frame(self.root, bg='#f0f8ff')
        self.current_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        percentage = (self.score / self.total_questions) * 100
        
        # Celebration emoji based on score
        if percentage >= 90:
            celebration = "🏆 CHAMPION! 🏆"
            message = "Outstanding! You're a math superstar!"
            color = "#FFD700"  # Gold
        elif percentage >= 75:
            celebration = "🎉 Excellent! 🎉"
            message = "Great job! Your math skills are impressive!"
            color = "#C0C0C0"  # Silver
        elif percentage >= 60:
            celebration = "👍 Good Work! 👍"
            message = "Well done! You're getting better every day!"
            color = "#CD7F32"  # Bronze
        else:
            celebration = "💪 Keep Going! 💪"
            message = "Practice makes perfect! You'll get it next time!"
            color = "#2E86AB"  # Blue
        
        # Results display
        Label(self.current_frame, text="Quiz Complete!", 
              font=self.title_font, fg="#2E86AB", bg='#f0f8ff').pack(pady=20)
        
        Label(self.current_frame, text=celebration, 
              font=("Arial", 20, "bold"), fg=color, bg='#f0f8ff').pack(pady=10)
        
        # Score in a nice frame
        score_frame = Frame(self.current_frame, bg='#e8f4f8', relief=RAISED, bd=2)
        score_frame.pack(pady=15, padx=50, fill=X)
        
        Label(score_frame, text=f"Final Score: {self.score} out of {self.total_questions}", 
              font=self.header_font, bg='#e8f4f8').pack(pady=10)
        
        Label(score_frame, text=f"That's {percentage:.0f}% correct!", 
              font=self.normal_font, bg='#e8f4f8').pack(pady=5)
        
        # Time information
        time_text = f"⏱️  Your time: {minutes} minutes and {seconds} seconds"
        Label(self.current_frame, text=time_text, 
              font=self.normal_font, bg='#f0f8ff', fg="#555555").pack(pady=10)
        
        # Encouraging message
        Label(self.current_frame, text=message, 
              font=("Arial", 12), bg='#f0f8ff', fg="#333333", wraplength=400).pack(pady=15)
        
        # Action buttons
        button_frame = Frame(self.current_frame, bg='#f0f8ff')
        button_frame.pack(pady=20)
        
        Button(button_frame, text="🔄 Try Again", font=self.button_font,
               bg="#2196F3", fg="white", padx=15, pady=8,
               command=lambda: self.startQuiz(self.difficulty.get())).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="🏠 Main Menu", font=self.button_font,
               bg="#666666", fg="white", padx=15, pady=8,
               command=self.display_welcome_screen).pack(side=LEFT, padx=10)


# Main program
if __name__ == "__main__":
    root = Tk()
    app = MathQuiz(root)
    root.mainloop()