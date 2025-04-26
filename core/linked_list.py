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