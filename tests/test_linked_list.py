import pytest
from core.linked_list import LinkedList

def test_linked_list_initialization():
    """Test the initialization of the LinkedList class."""
    linked_list = LinkedList()
    assert linked_list.head is None, "New linked list head should be None"
    assert linked_list.current is None, "New linked list current should be None"

def test_add_question_grows_list():
    "Test that adding a question grows the list."
    linked_list = LinkedList()

    # initally, the list should be empyt
    assert linked_list.head is None, "List should be empty initially"

    # add first question
    linked_list.add_question("q1", "a1", True)
    assert linked_list.head is not None, "List should not be empty after adding a question"
    assert linked_list.head.question == "q1", "First question should be q1"

    # add second question
    linked_list.add_question("q2", "a2", False)
    assert linked_list.head.next is not None, "List should not be empty after adding a question"
    assert linked_list.head.next.question == "q2", "second question should be q2"

def test_delete_current_node():
    """test that deleting the current node removes it"""
    linked_list = LinkedList()

    # adding questions
    linked_list.add_question("q1", "a1", True)
    linked_list.add_question("q2", "a2", False)
    linked_list.add_question("q3", "a3", True)

    linked_list.current = linked_list.head

    # delete q1
    assert linked_list.head.question == "q1", "first question before deleting is q1"
    linked_list.delete_current_node()
    assert linked_list.head.question == "q2", "first question after deleting once is q2"
    assert linked_list.current == linked_list.head, "current should be at head after deleting the first node"

    # delete q2
    linked_list.delete_current_node()
    assert linked_list.head.question == "q3", "first question after deleting twice is q3"

    # delete q3
    linked_list.delete_current_node()
    assert linked_list.head is None, "there are no more questions left in the list"
    assert linked_list.current is None, "there are no more questions left in the list"

def test_move_right():
    """test that moving right updates the current node"""
    linked_list = LinkedList()

    # adding questions
    linked_list.add_question("q1", "a1", True)
    linked_list.add_question("q2", "a2", False)
    linked_list.add_question("q3", "a3", True)
    linked_list.add_question("q4", "a4", True)
    linked_list.add_question("q5", "a5", False)
    linked_list.add_question("q6", "a6", False)

    linked_list.current = linked_list.head

    assert linked_list.head.question == "q1", "first question is q1"
    linked_list.move_right()
    assert linked_list.current.question == "q2", "current question is q2 after moving right"
    linked_list.move_right()
    assert linked_list.current.question == "q3", "current question is q3 after moving right"
    linked_list.move_right()
    assert linked_list.current.question == "q4", "current question is q4 after moving right"
    linked_list.move_right()
    assert linked_list.current.question == "q5", "current question is q5 after moving right"
    linked_list.move_right()
    assert linked_list.current.question == "q6", "current question is q6 after moving right"
    linked_list.move_right()
    assert linked_list.current is None, "current should be None after moving right from last node"

def test_is_empty():
    """test that is_empty returns correctly if the linked list is empty or not"""
    linked_list = LinkedList()
    assert linked_list.is_empty() is True, "is_empty should be True"
    linked_list.add_question("q1", "a1", True)
    assert linked_list.is_empty() is False, "is_empty should be False"