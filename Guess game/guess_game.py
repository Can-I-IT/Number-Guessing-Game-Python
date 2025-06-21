import random
import pygame
from colorama import Fore, Style, init
import os

# Initialize colorama and pygame
init(autoreset=True)
pygame.mixer.init()

# Sound-playing functions
def play_success_sound():
    pygame.mixer.music.load("success.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def play_fail_sound():
    pygame.mixer.music.load("fail.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Load scoreboard from file
def load_scoreboard():
    if os.path.exists("scoreboard.txt"):
        with open("scoreboard.txt", "r") as file:
            lines = file.readlines()
            return {line.split(":")[0].strip(): int(line.split(":")[1]) for line in lines}
    return {}

# Save scoreboard to file
def save_scoreboard(scoreboard):
    with open("scoreboard.txt", "w") as file:
        for name, score in scoreboard.items():
            file.write(f"{name}: {score}\n")

# Main game function
def play_game():
    print(Fore.CYAN + "🎮 Welcome to the Number Guessing Game!")

    scoreboard = load_scoreboard()

    player_name = input(Fore.LIGHTWHITE_EX + "Enter your name: ").strip().capitalize()
    print(Fore.GREEN + f"Hello {player_name}, let's begin!\n")

    while True:
        # Select difficulty
        print(Fore.YELLOW + "\nChoose your difficulty level:")
        print("1 - Easy (10 attempts)")
        print("2 - Medium (7 attempts)")
        print("3 - Hard (5 attempts)")

        while True:
            level = input(Fore.BLUE + "Enter 1, 2, or 3: ")
            if level == '1':
                max_attempts = 10
                break
            elif level == '2':
                max_attempts = 7
                break
            elif level == '3':
                max_attempts = 5
                break
            else:
                print(Fore.RED + "❌ Invalid input. Please enter 1, 2, or 3.")

        secret_number = random.randint(1, 100)
        attempts = 0

        print(Fore.MAGENTA + "\nI'm thinking of a number between 1 and 100...")
        print(f"You have {max_attempts} attempts. Good luck, {player_name}!\n")

        while attempts < max_attempts:
            try:
                guess = int(input(Fore.WHITE + f"Attempt {attempts + 1}: Enter your guess: "))
                attempts += 1

                if guess == secret_number:
                    print(Fore.GREEN + f"🎉 Correct, {player_name}! You guessed it in {attempts} tries.")
                    play_success_sound()

                    # Scoreboard logic
                    previous_best = scoreboard.get(player_name)
                    if previous_best is None or attempts < previous_best:
                        scoreboard[player_name] = attempts
                        print(Fore.LIGHTCYAN_EX + f"🏆 New best score recorded for {player_name}!")

                    break
                elif guess < secret_number:
                    print(Fore.YELLOW + "Too low.")
                else:
                    print(Fore.YELLOW + "Too high.")

                if abs(guess - secret_number) <= 3 and guess != secret_number:
                    print(Fore.CYAN + "💡 You're very close!")

            except ValueError:
                print(Fore.RED + "❗ Please enter a valid number.")

        if guess != secret_number:
            print(Fore.RED + f"\n💀 Game Over, {player_name}! The number was {secret_number}.")
            play_fail_sound()

        # Save updated scoreboard
        save_scoreboard(scoreboard)

        again = input(Fore.CYAN + "\n🔁 Do you want to play again? (yes/no): ").lower()
        if again != "yes":
            print(Fore.GREEN + f"👋 Thanks for playing, {player_name}!")
            print(Fore.MAGENTA + "\n📊 Final Scoreboard:")
            for name, score in sorted(scoreboard.items(), key=lambda x: x[1]):
                print(Fore.LIGHTWHITE_EX + f"{name}: {score} attempt(s)")
            break

# Run the game
play_game()
