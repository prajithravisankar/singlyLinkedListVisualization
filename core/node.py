class Node:
    """
    Representa a single node in Trivia Linked List

    Each Node Stores:
    - a trivia question
    - answer to the trivia question
    - whether the answer is correct or not
    - a pointer to the next node in the linked list of trivia questions
    """
    def __init__(self, question: str, answer: str, is_correct: bool) -> None:
        self.question = question
        self.answer = answer
        self.is_correct = is_correct
        self.next = None

