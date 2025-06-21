import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Number Guessing Game")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Init pygame for sound
        pygame.mixer.init()

        # Game state
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 0
        self.player_name = ""
        self.theme = "light"
        self.scoreboard = self.load_scoreboard()

        # Start
        self.create_menu()
        self.create_welcome_screen()

    # ---------- SOUND ----------
    def play_sound(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
        except:
            print(f"Couldn't play sound: {filename}")

    # ---------- THEMES ----------
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        theme_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Light Theme", command=lambda: self.set_theme("light"))
        theme_menu.add_command(label="Dark Theme", command=lambda: self.set_theme("dark"))
        menu_bar.add_cascade(label="Theme", menu=theme_menu)
        self.root.config(menu=menu_bar)

    def set_theme(self, theme):
        self.theme = theme
        bg = "#f0f0f0" if theme == "light" else "#2c2f33"
        fg = "black" if theme == "light" else "white"
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass

    # ---------- SCOREBOARD ----------
    def load_scoreboard(self):
        if os.path.exists("gui_scoreboard.txt"):
            with open("gui_scoreboard.txt", "r") as file:
                lines = file.readlines()
                return {line.split(":")[0].strip(): int(line.split(":")[1]) for line in lines}
        return {}

    def save_scoreboard(self):
        with open("gui_scoreboard.txt", "w") as file:
            for name, score in self.scoreboard.items():
                file.write(f"{name}: {score}\n")

    # ---------- GUI SCREENS ----------
    def create_welcome_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to Number Guessing Game!", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Enter your name:").pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.name_entry.bind("<Return>", self.start_game_event)  # ENTER for Start

        tk.Label(self.root, text="Choose Difficulty:").pack(pady=5)
        self.difficulty_var = tk.StringVar(value="1")
        tk.Radiobutton(self.root, text="Easy (10 tries)", variable=self.difficulty_var, value="1").pack()
        tk.Radiobutton(self.root, text="Medium (7 tries)", variable=self.difficulty_var, value="2").pack()
        tk.Radiobutton(self.root, text="Hard (5 tries)", variable=self.difficulty_var, value="3").pack()

        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=10)

        self.set_theme(self.theme)

    def start_game_event(self, event):
        self.start_game()

    def create_game_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Good luck, {self.player_name}!", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text="Guess a number between 1 and 100").pack()

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", self.check_guess_event)  # ENTER for Guess

        self.feedback_label = tk.Label(self.root, text="", fg="blue")
        self.feedback_label.pack(pady=5)

        self.attempts_label = tk.Label(self.root, text=f"Attempts: {self.attempts}/{self.max_attempts}")
        self.attempts_label.pack()

        tk.Button(self.root, text="Submit Guess", command=self.check_guess).pack(pady=10)

        self.set_theme(self.theme)

    def check_guess_event(self, event):
        self.check_guess()

    def start_game(self):
        self.player_name = self.name_entry.get().strip().capitalize()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return

        level = self.difficulty_var.get()
        self.max_attempts = {"1": 10, "2": 7, "3": 5}[level]
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        self.create_game_screen()

    def check_guess(self):
        guess_text = self.guess_entry.get()
        if not guess_text.isdigit():
            self.feedback_label.config(text="Enter a valid number!", fg="red")
            return

        guess = int(guess_text)
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")

        if guess == self.secret_number:
            self.play_sound("success.mp3")
            msg = f"You guessed it in {self.attempts} attempts!"
            prev_best = self.scoreboard.get(self.player_name)
            if prev_best is None or self.attempts < prev_best:
                self.scoreboard[self.player_name] = self.attempts
                self.save_scoreboard()
                msg += f"\n🏆 New best score!"
            messagebox.showinfo("🎉 Correct!", msg)
            self.ask_play_again()
        elif self.attempts >= self.max_attempts:
            self.play_sound("fail.mp3")
            messagebox.showerror("💀 Game Over", f"You ran out of attempts!\nThe number was {self.secret_number}.")
            self.ask_play_again()
        else:
            if abs(guess - self.secret_number) <= 3:
                self.feedback_label.config(text="💡 You're very close!", fg="orange")
            elif guess < self.secret_number:
                self.feedback_label.config(text="Too low!", fg="blue")
            else:
                self.feedback_label.config(text="Too high!", fg="blue")

    def ask_play_again(self):
        again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if again:
            self.create_welcome_screen()
        else:
            self.show_scoreboard()

    def show_scoreboard(self):
        self.clear_screen()
        tk.Label(self.root, text="📊 Scoreboard (Best Scores)", font=("Arial", 14)).pack(pady=10)
        sorted_scores = sorted(self.scoreboard.items(), key=lambda x: x[1])
        for name, score in sorted_scores:
            tk.Label(self.root, text=f"{name}: {score} attempt(s)", font=("Arial", 11)).pack()
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)
        self.set_theme(self.theme)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
    