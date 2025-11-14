import tkinter as tk
from tkinter import font as tkFont
import random
import os

# Global variables to keep track of jokes and current state
jokes_list = []
current_punchline = ""

def load_jokes():
    """Load jokes from the text file"""
    global jokes_list
    jokes_list = []
    file_path = "Exercise2/randomJokes.txt"

    if not os.path.exists(file_path):
        setup_label.config(text="Oops! Can't find the jokes file at 'Exercise2/randomJokes.txt'")
        return

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if '?' in line:
                    parts = line.split('?', 1)
                    if len(parts) == 2:
                        setup = parts[0].strip() + "?"
                        punchline = parts[1].strip()
                        jokes_list.append((setup, punchline))

        if not jokes_list:
            setup_label.config(text="Hmm, the file is empty. Add some jokes!")

    except Exception as e:
        setup_label.config(text=f"Something went wrong: {e}")


def get_new_joke():
    """Pick a random joke and show it"""
    global current_punchline

    if not jokes_list:
        setup_label.config(text="No jokes available right now!")
        return

    setup, punchline = random.choice(jokes_list)
    current_punchline = punchline

    setup_label.config(text=setup)
    punchline_label.config(text="")

    # Hide the main button, show the other ones
    joke_button.pack_forget()
    punchline_button.pack(pady=5)
    next_joke_button.pack(pady=5)


def show_punchline():
    """Display the punchline"""
    punchline_label.config(text=current_punchline)
    punchline_button.pack_forget()


def go_home():
    """Reset to the home screen"""
    setup_label.config(text="Press the button below to hear a joke!")
    punchline_label.config(text="")
    
    # Hide all buttons except the main joke button
    punchline_button.pack_forget()
    next_joke_button.pack_forget()
    
    # Show the main button
    joke_button.pack(pady=5)


# Create the main window
root = tk.Tk()
root.title("Alexa Joke Bot 🎤")
root.geometry("700x500")
root.configure(bg="#eba4cd")

# Custom fonts
title_font = tkFont.Font(family="Comic Sans MS", size=18, weight="bold")
joke_font = tkFont.Font(family="Arial", size=13)
punchline_font = tkFont.Font(family="Arial", size=13, slant="italic")
button_font = tkFont.Font(family="Helvetica", size=11)

# Title at the top
title_label = tk.Label(root, text="🎭 Alexa's Joke Bot 🎭", 
                       font=title_font, 
                       bg="#eba4cd", 
                       fg="#1a5490")
title_label.pack(pady=(20, 15))

# Joke setup display
setup_label = tk.Label(root, 
                       text="Press the button below to hear a joke!", 
                       font=joke_font, 
                       bg="#eba4cd", 
                       fg="#2c3e50",
                       wraplength=450, 
                       height=4,
                       justify="center")
setup_label.pack(pady=10, padx=15)

# Punchline display
punchline_label = tk.Label(root, 
                           text="", 
                           font=punchline_font,
                           bg="#eba4cd", 
                           fg="#c0392b",
                           wraplength=450, 
                           height=3,
                           justify="center")
punchline_label.pack(pady=5, padx=15)

# Frame for buttons
button_frame = tk.Frame(root, bg="#eba4cd")
button_frame.pack(pady=15)

# Main button to get a joke
joke_button = tk.Button(button_frame, 
                        text="Alexa tell me a Joke",
                        command=get_new_joke, 
                        font=button_font,
                        bg="#3498db", 
                        fg="white",
                        activebackground="#2980b9",
                        cursor="hand2",
                        padx=20,
                        pady=8)
joke_button.pack(pady=5)

# Button to reveal punchline
punchline_button = tk.Button(button_frame, 
                             text="Show Punchline",
                             command=show_punchline, 
                             font=button_font,
                             bg="#9b59b6",
                             fg="white",
                             activebackground="#8e44ad",
                             cursor="hand2",
                             padx=20,
                             pady=6)

# Button to get another joke
next_joke_button = tk.Button(button_frame, 
                             text="Next Joke",
                             command=get_new_joke, 
                             font=button_font,
                             bg="#27ae60",
                             fg="white",
                             activebackground="#229954",
                             cursor="hand2",
                             padx=20,
                             pady=6)

# Bottom buttons frame
bottom_button_frame = tk.Frame(root, bg="#eba4cd")
bottom_button_frame.pack(side=tk.BOTTOM, pady=20)

# Home button
home_button = tk.Button(bottom_button_frame, 
                        text="Return to Home", 
                        command=go_home,
                        font=button_font, 
                        bg="#f39c12", 
                        fg="white",
                        activebackground="#e67e22",
                        cursor="hand2",
                        padx=20,
                        pady=6)
home_button.pack(side=tk.LEFT, padx=10)

# Quit button at the bottom
quit_button = tk.Button(bottom_button_frame, 
                        text="Quit Alexa", 
                        command=root.destroy,
                        font=button_font, 
                        bg="#e74c3c", 
                        fg="white",
                        activebackground="#c0392b",
                        cursor="hand2",
                        padx=20,
                        pady=6)
quit_button.pack(side=tk.LEFT, padx=10)

# Load the jokes when the app starts
load_jokes()
root.mainloop()