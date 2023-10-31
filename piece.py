'''
ZHU HAI WEI YAN
Piece
'''
import turtle
from const import *


class Piece:
    '''
    Class -- Piece
        Represents pieces.
    Attributes:
        pen -- A Turtle.
        row -- The row of a piece, an integer.
        col -- The col of a piece, an integer.
        color -- The color of a piece, a string.
        king -- A boolean which represents whether a piece is a king piece.
    Methods:
        draw_piece -- Helper method. Creates a standard card deck.
        make_king -- Make a piece become a king piece.
        move -- Change the row and col of a piece.
    '''

    def __init__(self, row, col, color):
        '''
            Constructor -- creates a new instance of PIece
            Parameters:
                self -- the current DeckOfCards object
        '''
        self.pen = turtle.Turtle()
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def draw_piece(self):
        '''
            Function -- draw_piece
                Draw a piece in the given position.
            Returns:
                Nothing. Draws a piece in the graphics windo.
        '''
        pen = self.pen
        pen.setposition((-NUM_SQUARES / 2 + self.col + 1 / 2) * SQUARE,
                        (-NUM_SQUARES / 2 + self.row + RATIO) * SQUARE)
        pen.color(self.color)
        pen.pendown()
        pen.begin_fill()
        pen.circle(RADIUS)
        pen.fillcolor(self.color)
        pen.end_fill()
        # If the piece is a king piece, it has some difference.
        self.draw_king_status()
        pen.penup()

    def draw_king_status(self):
        if self.king:
            self.pen.begin_fill()
            self.pen.circle(RADIUS / 2)
            self.pen.fillcolor(ORANGE)
            self.pen.end_fill()

    def make_king(self):
        '''
            Function -- make_king
                Make a piece become a king piece.
            Returns:
                Nothing.
        '''
        self.king = True

    def move(self, row, col):
        '''
            Function -- move
                Change the row and col of a piece.
            Returns:
                Nothing.
        '''
        self.row = row
        self.col = col