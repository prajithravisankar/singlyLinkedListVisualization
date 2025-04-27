from core.linked_list import LinkedList

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
                print("❌ Incorrect! The right answer was:", self.linked_list.current.answer, "no points")
                self.linked_list.move_right()

    def display_score(self) -> None:
        """Displays the current game score."""
        print(f"\n⭐ Your Score: {self.score} points")