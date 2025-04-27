from core.linked_list import *
from ui.cli import *

linked_list = LinkedList()
linked_list.add_question("What is the capital of France?", "Paris", True)
linked_list.add_question("what is the fastest land animal?", "cheetah", True)
linked_list.add_question("what is the largest ocean?", "pacific", True)
linked_list.add_question("what is my name", "dog", False)


linked_list.current = linked_list.head
trivia_game = TriviaGame()
trivia_game.score = 0
trivia_game.linked_list = linked_list

trivia_game.display_current_question()
trivia_game.handle_user_choice()
trivia_game.display_current_question()
trivia_game.handle_user_choice()
trivia_game.display_current_question()
trivia_game.handle_user_choice()
trivia_game.display_current_question()
trivia_game.handle_user_choice()
trivia_game.display_current_question()
trivia_game.handle_user_choice()
trivia_game.display_score()
