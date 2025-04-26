import pytest
from core.linked_list import LinkedList

def test_linked_list_initialization():
    """Test the initialization of the LinkedList class."""
    linked_list = LinkedList()
    assert linked_list.head is None, "New linked list head should be None"
    assert linked_list.current is None, "New linked list current should be None"