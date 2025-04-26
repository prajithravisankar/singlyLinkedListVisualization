from core.node import Node


class LinkedList:
    """Manages a singly linked list of nodes of trivia questions.

    Responsibilities:
    - Maintains reference to the first node (head)
    - tracks current node during traversal
    - supports operations like add/delete/move etc.
    """
    def __init__(self) -> None:
        self.head = None
        self.current = None

    def add_question(self, question: str, answer: str, is_correct: bool) -> None:
        """Adds new trivia question to the end of the linked list.

        Args:
            - question (str): The trivia question.
            - answer (str): The answer to the trivia question.
            - is_correct (bool): Whether the answer is correct.
        """
        new_node = Node(question, answer, is_correct)

        if self.head is None:
            self.head = new_node
            self.current = self.head
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def delete_current_node(self) -> None:
        """Deletes the current node in the linked list."""
        if self.head is None:
            return

        # case 1: delete head node
        if self.current == self.head:
            self.head = self.head.next
            self.current = self.head
            return

        # case 2: delete middle or last node
        prev = self.head
        while prev.next != self.current:
            prev = prev.next
            if prev is None:
                return
        prev.next = self.current.next
        if prev.next is not None:
            self.current = prev.next
        else:
            self.current = prev