"""
ZHU HAI WEI YAN
Visualizer
"""

import turtle
from const import *
from piece import Piece


class Visualizer:
    """
    A class to handle the visualization of the checkerboard game using turtle graphics.
    """

    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.pen.hideturtle()
        turtle.tracer(0, 0)  # Turn off animation for faster drawing

    def initialize_game_window(self):
        turtle.setup(WINDOW_SIZE, WINDOW_SIZE)
        turtle.screensize(BOARD_SIZE, BOARD_SIZE)
        turtle.bgcolor(BACKGROUND_COLOR)

    def draw_square(self, size):
        """
        Draws a square of a given size.

        Parameters:
            size (int): The size of each square's side.
        """
        self.pen.pendown()
        self.pen.begin_fill()
        for _ in range(NUM_EDGE):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.end_fill()
        self.pen.penup()

    def draw_checkerboard(self, num_squares, square_size):
        """
        Draws the checkerboard.
        
        Parameters:
            num_squares (int): The number of squares on one side of the board.
            square_size (int): The size of each square.
        """
        self.pen.hideturtle()
        corner = -num_squares / 2 * square_size
        self.pen.setposition(corner, corner)
        self.pen.color(PEN_COLOR, SQUARE_COLORS[1])
        self.pen.begin_fill()
        self.draw_square(num_squares * square_size)
        self.pen.end_fill()
        self.pen.color(PEN_COLOR, SQUARE_COLORS[0])
        for col in range(num_squares):
            for row in range(num_squares):
                if col % 2 != row % 2:
                    self.pen.setposition(corner + square_size * col, corner + square_size * row)
                    self.pen.begin_fill()
                    self.draw_square(square_size)
                    self.pen.end_fill()

    def draw_piece(self, piece, num_squares, square_size, radius):
        """
        Draws the piece on the board.

        Parameters:
            piece (Piece): The piece to draw.
            num_squares (int): The number of squares on one side of the board.
            square_size (int): The size of each square.
            radius (int): The radius of the piece.
        """
        self.pen.setposition((-num_squares / 2 + piece.col + 0.5) * square_size,
                             (-num_squares / 2 + piece.row + RATIO) * square_size)
        self.pen.color(piece.color)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.circle(radius)
        self.pen.fillcolor(piece.color)
        self.pen.end_fill()
        self.pen.penup()
        if piece.king:
            self.draw_king_status(piece, radius)

    def draw_king_status(self, piece, radius):
        """
        Draws an additional circle if the piece is a king.

        Parameters:
            piece (Piece): The piece to check for king status.
            radius (int): The radius of the king status circle.
        """
        self.pen.setposition((-NUM_SQUARES / 2 + piece.col + 0.5) * SQUARE,
                             (-NUM_SQUARES / 2 + piece.row + RATIO) * SQUARE)
        if piece.king:
            self.pen.begin_fill()
            self.pen.circle(radius / 2)
            self.pen.fillcolor(KING_COLOR)
            self.pen.end_fill()

    def draw_valid_moves(self, moves):
        """
        Draw the current valid moves.
        Parameters:
            moves (list of tuples): The current valid moves.
        """
        for move in moves:
            row, col = move
            self.pen.setposition((-NUM_SQUARES / 2 + col) * SQUARE,
                                 (-NUM_SQUARES / 2 + row) * SQUARE)
            self.pen.color(RED)
            self.pen.pendown()
            for _ in range(NUM_EDGE):
                self.pen.forward(SQUARE)
                self.pen.left(RIGHT_ANGLE)
            self.pen.penup()

    def highlight_pieces(self, pieces):
        """
        Highlight pieces that can move or capture.
        Parameters:
            pieces (list of Piece): The pieces to highlight.
        """
        for piece in pieces:
            row, col = piece.row, piece.col
            self.pen.setposition((-NUM_SQUARES / 2 + col) * SQUARE,
                                 (-NUM_SQUARES / 2 + row) * SQUARE)
            self.pen.color(HIGHLIGHT_COLOR)
            self.pen.pendown()
            for _ in range(NUM_EDGE):
                self.pen.forward(SQUARE)
                self.pen.left(RIGHT_ANGLE)
            self.pen.penup()

    def display_winner(self, winner):
        """
        Display a message for the winner.
        Parameters:
            winner (str): The winner of the game.
        """
        message = WINNER_MESSAGES[0] if winner == BLACK else WINNER_MESSAGES[1]
        self.pen.pencolor(FONT_COLOR)
        self.pen.setposition(0, 0)
        self.pen.pendown()
        self.pen.write(message, False, MESSAGE_POSITION, (FONT, FONT_SIZE, FONT_STYLE))
        self.pen.penup()
