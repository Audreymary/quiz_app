# cli.py
import json
import random
from models import session, Question, Option, Answer

def load_questions():
    """Load questions from the database."""
    return session.query(Question).all()

def ask_question(question_data):
    """Ask a single question and return True if the answer is correct."""
    print(question_data.text)
    options = question_data.options
    random.shuffle(options)  # Shuffle options to make quiz more dynamic
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option.text}")
    
    try:
        user_choice = int(input("Enter the number of your answer: "))
        if user_choice < 1 or user_choice > len(options):
            print("Invalid choice. Please choose a valid option.")
            return False
        
        # Check if the selected option is the correct answer
        if options[user_choice - 1] == session.query(Answer).filter_by(option_id=options[user_choice - 1].id).first().option:
            return True
        else:
            return False
    except ValueError:
        print("Please enter a valid number.")
        return False

def quiz():
    """The main function to run the quiz."""
    questions = load_questions()
    random.shuffle(questions)  # Shuffle the questions to make it more interesting
    score = 0

    for question in questions:
        if ask_question(question):
            score += 1

    print(f"\nYour final score is {score}/{len(questions)}.")
    print("Thanks for playing!")

def add_question():
    """Allow the user to add a new question."""
    question_text = input("Enter the new question: ")
    new_question = Question(text=question_text)
    session.add(new_question)
    session.commit()

    for i in range(4):
        option_text = input(f"Enter option {i+1}: ")
        new_option = Option(text=option_text, question_id=new_question.id)
        session.add(new_option)
    
    answer_option = input("Enter the correct option number: ")
    correct_option = session.query(Option).filter_by(id=answer_option).first()
    new_answer = Answer(option_id=correct_option.id)
    session.add(new_answer)
    session.commit()

    print("New question added successfully!")

def main():
    """Main menu to select options for playing or adding questions."""
    while True:
        print("\nWelcome to the Quiz App!")
        print("1. Start the quiz")
        print("2. Add a new question")
        print("3. Exit")
        choice = input("Please enter your choice (1/2/3): ")

        if choice == '1':
            quiz()
        elif choice == '2':
            add_question()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
