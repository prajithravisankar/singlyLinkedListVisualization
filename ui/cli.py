from core.linked_list import LinkedList
import json

class TriviaGame:
    """
    TriviaGame class manages the trivia game logic and user interaction.
    """
    def __init__(self):
        self.linked_list = LinkedList()
        self.score = 0

    def display_current_question(self) -> None:
        """Displays the current trivia questions and answers to the user.

        Args:
            - linked_list (LinkedList): The Linked List containing trivia questions.
        Example:
            - question: what is 2 + 2?
            - answer: 4
        """
        print("\n---Current Trivia Question---")
        if self.linked_list.current is None:
            print("No trivia questions available.")
            return
        else:
            question = self.linked_list.current.question
            answer = self.linked_list.current.answer
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print("-------------------------------")

    def handle_user_choice(self) -> None:
        """Handles user input to manage trivia game actions

        Args:
            - linked_list (LinkedList): The Linked List containing trivia questions.
        """
        print("\n---Trivia Game Menu---")
        print("1. Delete Question (if wrong)")
        print("2. Next Question")
        print("3. Confirm correct answer")

        while True:
            choice = input("Enter your choice (1 - 3): ")
            if choice in ('1', '2', '3'):
                break
            else:
                print("Invalid choice.")

        if choice == '1':
            if self.linked_list.current is None:
                print("No trivia questions available to delete.")
                return
            elif self.linked_list.current.is_correct:
                print("the question and answer pair was correct, should not have deleted, no points")
            elif self.linked_list.current.is_correct is not True:
                print("✅ Correct (+1 point), deleted wrong question answer pair!")
                self.score += 1
            self.linked_list.delete_current_node()
        elif choice == '2':
            print("⏭️  Moving to next question... no points added")
            self.linked_list.move_right()
            if self.linked_list.current is None:
                print("You've reached the end!")
        elif choice == '3':
            if self.linked_list.current is None:
                print("You've reached the end!")
            elif self.linked_list.current.is_correct:
                print("✅ Correct (+1 point), kept correct question and answer pair!")
                self.score += 1
                self.linked_list.move_right()
            else:
                print("❌ Incorrect! ", self.linked_list.current.answer, " no points")
                self.linked_list.move_right()

    def display_score(self) -> None:
        """Displays the current game score."""
        print(f"\n⭐ Your Score: {self.score} points")

    def load_questions(self):
        """Loads a mix of true and false trivia questions"""
        with open("data/questions.json") as file:
            dictionary = json.load(file)
        for trivia in dictionary:
            self.linked_list.add_question(trivia['question'], trivia['answer'], trivia['isCorrect'])
        self.linked_list.current = self.linked_list.head  # Set starting point

    def cli_game_loop(self):
        """Main game loop for the CLI trivia game."""
        print("\n=== Trivia Trek Challenge ===")
        print("Rules:")
        print("- Delete (1) wrong answers (+1 point)")
        print("- Skip (2) to next question")
        print("- Confirm (3) correct answers (+1 point)\n")

        self.load_questions()

        while self.linked_list.current:
            self.display_current_question()
            self.handle_user_choice()

            if self.linked_list.current is None:
                break

        # Game over summary
        print("\n=== Game Results ===")
        print(f"Final Score: {self.score}")


