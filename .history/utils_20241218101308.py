# utils.py
import random

def randomize_options(options):
    """Randomize the options to prevent order bias in quizzes."""
    random.shuffle(options)
    return options

def get_user_answer(options):
    """Get valid input from user."""
    user_choice = None
    while user_choice is None:
        try:
            user_choice = int(input("Enter the number of your answer: "))
            if user_choice < 1 or user_choice > len(options):
                print(f"Please select a valid number (1-{len(options)})")
                user_choice = None
        except ValueError:
            print("Invalid input. Please enter a number.")
    return user_choice
