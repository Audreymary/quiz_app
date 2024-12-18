# cli.py
import random
from models import session, Question, Option, Answer
from utils import randomize_options, get_user_answer

def load_questions():
    """Load questions from the database."""
    return session.query(Question).all()

def ask_question(question_data):
    """Ask a single question and return True if the answer is correct."""
    print(question_data.text)
    options = randomize_options(question_data.options)  # Shuffle options
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option.text}")
    
    user_choice = get_user_answer(options)

    # Check if the selected option is the correct answer
    correct_option = session.query(Answer).filter_by(option_id=options[user_choice - 1].id).first().option
    if options[user_choice - 1] == correct_option:
        return True
    return False

def quiz():
    """Run the quiz."""
    questions = load_questions()
    random.shuffle(questions)  # Shuffle the questions
    score = 0

    for question in questions:
        if ask_question(question):
            score += 1

    print(f"\nYour final score is {score}/{len(questions)}")
    print("Thanks for playing!")

def add_question():
    """Add a new question to the quiz database."""
    question_text = input("Enter the new question: ")
    new_question = Question(text=question_text)
    session.add(new_question)
    session.commit()

    for i in range(4):
        option_text = input(f"Enter option {i+1}: ")
        new_option = Option(text=option_text, question_id=new_question.id)
        session.add(new_option)

    correct_option_idx = int(input("Enter the number of the correct option: "))
    correct_option = session.query(Option).filter_by(id=correct_option_idx).first()
    new_answer = Answer(option_id=correct_option.id)
    session.add(new_answer)
    session.commit()

    print("New question added successfully!")

def main():
    """Main CLI menu to interact with the quiz app."""
    while True:
        print("\n1. Start the quiz")
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
