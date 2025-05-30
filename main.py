from core.linked_list import *
from ui.cli import *

def main():
    game = TriviaGame()

    game.linked_list.current = game.linked_list.head  # Start at first question

    # Start game
    game.cli_game_loop()

if __name__ == "__main__":
    main()
