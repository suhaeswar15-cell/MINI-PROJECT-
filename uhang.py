import tkinter as tk
from tkinter import messagebox
import random
import json
import os

SCORE_FILE = "hangman_score.json"

def load_scoreboard():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as file:
                return json.load(file)
        except:
            return {"wins": 0, "losses": 0, "games_played": 0}
    else:
        return {"wins": 0, "losses": 0, "games_played": 0}


def save_scoreboard(data):
    with open(SCORE_FILE, "w") as file:
        json.dump(data, file)

scoreboard = load_scoreboard()

categories = {
    "Animals": ["tiger", "elephant", "lion", "zebra", "panda", "giraffe"],
    "Fruits": ["apple", "banana", "mango", "orange", "papaya"],
    "Countries": ["india", "brazil", "canada", "japan", "france"],
    "Technology": ["python", "computer", "software", "keyboard", "program"]
}


root = tk.Tk()
root.title("Hangman Game")
root.geometry("600x600")
root.resizable(False, False)


hangman_stages = [
    """
       -----
       |   |
           |
           |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ---------
    """
]

secret_word = ""
display_word = []
incorrect_guesses = 0
max_incorrect = 6
chosen_category = ""


label_category = tk.Label(root, text="Select a Category", font=("Arial", 16))
label_category.pack()

category_var = tk.StringVar(root)
category_var.set("Animals")

dropdown = tk.OptionMenu(root, category_var, *categories.keys())
dropdown.pack()

hangman_label = tk.Label(root, text=hangman_stages[0], font=("Courier", 14))
hangman_label.pack()

word_label = tk.Label(root, text="", font=("Arial", 24))
word_label.pack(pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack()

def start_game():
    global secret_word, display_word, incorrect_guesses, chosen_category

    chosen_category = category_var.get()
    secret_word = random.choice(categories[chosen_category])
    display_word = ["_"] * len(secret_word)
    incorrect_guesses = 0

    hangman_label.config(text=hangman_stages[0])
    word_label.config(text=" ".join(display_word))

    enable_all_buttons()

def guess_letter(letter, button):
    global incorrect_guesses

    button.config(state="disabled")

    if letter in secret_word:
        for i, ch in enumerate(secret_word):
            if ch == letter:
                display_word[i] = letter

        word_label.config(text=" ".join(display_word))

        if "_" not in display_word:
            scoreboard["wins"] += 1
            scoreboard["games_played"] += 1
            save_scoreboard(scoreboard)

            messagebox.showinfo("You Win!", f"Correct word: {secret_word}")
            start_game()

    else:
        incorrect_guesses += 1
        hangman_label.config(text=hangman_stages[incorrect_guesses])

        if incorrect_guesses == max_incorrect:
            scoreboard["losses"] += 1
            scoreboard["games_played"] += 1
            save_scoreboard(scoreboard)

            messagebox.showerror("You Lost!", f"Word was: {secret_word}")
            start_game()

def enable_all_buttons():
    for btn in letter_buttons:
        btn.config(state="normal")


letter_buttons = []
alphabet = "abcdefghijklmnopqrstuvwxyz"

for i, letter in enumerate(alphabet):

    def create_cmd(ltr, btn_ref):
        return lambda: guess_letter(ltr, btn_ref)

    btn = tk.Button(frame_buttons, text=letter.upper(),
                    width=4, height=2, font=("Arial", 12))

    btn.config(command=create_cmd(letter, btn))

    btn.grid(row=i//9, column=i%9, padx=2, pady=2)

    letter_buttons.append(btn)


start_button = tk.Button(root, text="Start Game", font=("Arial", 16),
                         command=start_game)
start_button.pack(pady=20)


root.mainloop()
