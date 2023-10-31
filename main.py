"""
ZHU HAI WEI YAN
Main program
"""

import turtle
from const import *
from gamestate import GameState


def click_handler(x, y):
    """
        Function -- click_handler
            Called when a click occurs.
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Returns:
            Does not and should not return. Click handlers are a special type
            of function automatically called by Turtle. You will not have
            access to anything returned by this function.
    """
    row = int(y // SQUARE + NUM_SQUARES / 2)
    col = int(x // SQUARE + NUM_SQUARES / 2)
    if -NUM_SQUARES / 2 * SQUARE <= x <= NUM_SQUARES / 2 * SQUARE and -NUM_SQUARES / 2 * SQUARE <= y <= NUM_SQUARES / 2 * SQUARE:
        print("Clicked at (", row, ",", col, ")")
        game.human_click_piece(row, col)
    else:
        print("The click was not in bounds.")


def main():
    board_size = NUM_SQUARES * SQUARE
    window_size = board_size + SQUARE
    turtle.setup(window_size, window_size)
    turtle.screensize(board_size, board_size)
    turtle.bgcolor("white")
    turtle.tracer(0, 0)
    # makes the drawing appear immediately
    #
    #
    #

    global game
    game = GameState()
    game.board.draw_checkerboard()
    game.board.draw_pieces()

    #
    #
    #
    # Click handling
    screen = turtle.Screen()
    GameState.screen(game, screen)
    # This will call the click_handler function when a click occurs
    screen.onclick(click_handler)
    # Stops the window from closing.
    turtle.done()


if __name__ == "__main__":
    main()
