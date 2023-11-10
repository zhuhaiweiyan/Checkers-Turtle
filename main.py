"""
ZHU HAI WEI YAN
Main function
"""

import turtle
from const import *
from gamestate import GameState


def click_handler(x, y, game):
    """
    Called when a click occurs within the game window.

    Parameters:
        x (float): X coordinate of the click.
        y (float): Y coordinate of the click.
        game (GameState): The current game state object.
    """
    row = int(y // SQUARE + NUM_SQUARES / 2)
    col = int(x // SQUARE + NUM_SQUARES / 2)
    if -NUM_SQUARES / 2 * SQUARE <= x <= NUM_SQUARES / 2 * SQUARE and \
       -NUM_SQUARES / 2 * SQUARE <= y <= NUM_SQUARES / 2 * SQUARE:
        print(f"Clicked at ({row}, {col})")
        game.human_click_piece(row, col)
    else:
        print("The click was not in bounds.")


def main():
    """
    Main function to set up and start the checkerboard game.
    """
    # Set up the game window
    board_size = NUM_SQUARES * SQUARE
    window_size = board_size + SQUARE
    turtle.setup(window_size, window_size)
    turtle.screensize(board_size, board_size)
    turtle.bgcolor("white")
    turtle.tracer(0, 0)  # Immediate drawing without animation

    # Initialize the game state
    game = GameState()
    game.board.draw_checkerboard()
    game.board.draw_pieces()

    # Set up click handling
    screen = turtle.Screen()
    game.screen(screen)
    screen.onclick(lambda x, y: click_handler(x, y, game))

    # Start the game loop
    turtle.done()


if __name__ == "__main__":
    main()
