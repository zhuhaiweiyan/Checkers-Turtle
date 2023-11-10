import turtle
from const import *

class Piece:
    """
    A class to represent a piece in a checkerboard game.

    Attributes:
        pen (Turtle): A Turtle object for drawing the piece.
        row (int): The row of the piece on the board.
        col (int): The column of the piece on the board.
        color (str): The color of the piece.
        king (bool): Indicates if the piece is a king.
    """

    def __init__(self, row, col, color):
        """
        Constructor to create a new piece.

        Parameters:
            row (int): The row of the piece.
            col (int): The column of the piece.
            color (str): The color of the piece.
        """
        self.pen = turtle.Turtle()
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def draw_piece(self):
        """
        Draws the piece on the board.
        """
        pen = self.pen
        pen.setposition((-NUM_SQUARES / 2 + self.col + 0.5) * SQUARE,
                        (-NUM_SQUARES / 2 + self.row + RATIO) * SQUARE)
        pen.color(self.color)
        pen.pendown()
        pen.begin_fill()
        pen.circle(RADIUS)
        pen.fillcolor(self.color)
        pen.end_fill()
        self.draw_king_status()
        pen.penup()

    def draw_king_status(self):
        """
        Draws an additional circle if the piece is a king.
        """
        if self.king:
            self.pen.begin_fill()
            self.pen.circle(RADIUS / 2)
            self.pen.fillcolor(ORANGE)
            self.pen.end_fill()

    def make_king(self):
        """
        Turns the piece into a king piece.
        """
        self.king = True

    def move(self, row, col):
        """
        Moves the piece to a new position.

        Parameters:
            row (int): The new row for the piece.
            col (int): The new column for the piece.
        """
        self.row = row
        self.col = col
