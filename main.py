"""
ZHU HAI WEI YAN
Main function
"""

import turtle
from gamestate import GameState


def main():
    """
    Main function to set up and start the checkerboard game.
    """

    game = GameState()
    game.visualizer.initialize_game_window()

    # Set up click handling
    screen = turtle.Screen()
    game.screen(screen)
    screen.onclick(lambda x, y: game.handle_click(x, y))

    # Start the game loop
    turtle.done()


if __name__ == "__main__":
    main()
