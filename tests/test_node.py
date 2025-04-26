import pytest
from core.node import Node

def test_node_creation():
    question = "what is my name?"
    answer = "prajith ravisankar"
    is_correct = True
    trivia_question_1 = Node(question, answer, is_correct)

    assert trivia_question_1.question == question, "question not set correctly"
    assert trivia_question_1.answer == answer, "answer not set correctly"
    assert trivia_question_1.is_correct == is_correct, "is_correct not set correctly"
    assert trivia_question_1.next is None, "next should be none initially"