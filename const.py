"""
ZHU HAI WEI YAN
Constants
"""

# Board configuration
NUM_SQUARES = 8  # The number of squares on each row of the checkerboard.
SQUARE = 50  # The size (in pixels) of each square on the checkerboard.
RADIUS = 22.5  # The radius (in pixels) of the pieces.
RATIO = 0.05  # Ratio for piece contraction.
NUM_EDGE = 4  # Number of edges in the game.
EMPTY = 0  # Constant representing an empty state.
RIGHT_ANGLE = 90  # Constant for a right angle (90 degrees).
DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # The directions of moved pieces

# Window configuration
BOARD_SIZE = NUM_SQUARES * SQUARE
WINDOW_SIZE = BOARD_SIZE + SQUARE

# COLORS
BACKGROUND_COLOR = "white"
SQUARE_COLORS = ("gray", "white")  # Colors of the checkerboard squares.
CHESS_COLORS = ("black", "red")  # Colors of the chess pieces.
RED = "RED"
BLACK = "BLACK"
PEN_COLOR = "black"
KING_COLOR = "orange"
HIGHLIGHT_COLOR = "lime"

# Script FONT
FONT = "Arial"
FONT_COLOR = "deep sky blue"
FONT_SIZE = 30
FONT_STYLE = "bold"
WINNER_MESSAGES = ("YOU WIN!", "YOU LOSE!")
MESSAGE_POSITION = "center"
