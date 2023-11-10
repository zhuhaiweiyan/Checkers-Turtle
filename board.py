"""
ZHU HAI WEI YAN
Board
"""
import turtle
from const import *
from piece import Piece


class Board:
    """
    A class to represent the checkerboard in a checkerboard game.

    Attributes:
        pen (Turtle): A Turtle object for drawing the board.
        board (list): A nested list representing the board's state.
        aten_pieces (list): The pieces that can be captured this turn.
        jumpable (list): Pieces that can capture an opponent's piece this turn.
        movable (list): Pieces that can move this turn.
    """

    def __init__(self):
        """
        Constructor to create a new board.
        """
        self.pen = turtle.Turtle()
        self.board = []
        self.aten_pieces = []
        self.jumpable = []
        self.movable = []
        self.create_board()

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

    def draw_checkerboard(self):
        """
        Draws the checkerboard.
        """
        pen = self.pen
        pen.penup()
        pen.hideturtle()
        corner = -NUM_SQUARES / 2 * SQUARE
        pen.setposition(corner, corner)
        pen.color("black", "white")
        pen.begin_fill()
        self.draw_square(NUM_SQUARES * SQUARE)
        pen.end_fill()
        pen.color("black", "gray")
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    pen.setposition(corner + SQUARE * col, corner + SQUARE * row)
                    pen.begin_fill()
                    self.draw_square(SQUARE)
                    pen.end_fill()

    def create_board(self):
        """
        Creates the initial state of the board.
        """
        for row in range(NUM_SQUARES):
            self.board.append([])
            for col in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(EMPTY)
                else:
                    self.board[row].append(EMPTY)
        self.movable = [
            self.board[2][1], self.board[2][3], self.board[2][5],
            self.board[2][7]
        ]

    def draw_pieces(self):
        """
            Draw all pieces on the checkerboard.
        """
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                piece = self.board[row][col]
                if piece != EMPTY:
                    piece.draw_piece()

    def get_piece(self, row, col):
        """
            Get the piece through the row and col.
        """
        return self.board[row][col]

    def move_piece(self, piece, row, col):
        """
        Moves a piece to a new position and potentially promotes it to a king.

        Parameters:
            piece (Piece): The piece to be moved.
            row (int): The new row position for the piece.
            col (int): The new column position for the piece.
        """
        # Swap the positions in the board representation
        self.board[piece.row][piece.col], self.board[row][col] = EMPTY, piece
        # Update the piece's position and check for king status
        piece.move(row, col)
        if (piece.color == BLACK and row == NUM_SQUARES - 1) or (piece.color == RED and row == 0):
            piece.make_king()

    def judge_movable(self, turn):
        """
            Judge whether there are some pieces that can move in the current turn.
        """
        for row in self.board:
            for piece in row:
                if piece != EMPTY:
                    if piece.color == turn:
                        if self.get_uncaptured_moves(piece):
                            self.movable.append(piece)

    def judge_jumpable(self, turn):
        """
            Judge whether there are some pieces that can eat pieces in the current turn.
        """
        for row in self.board:
            for piece in row:
                if piece != EMPTY:
                    if piece.color == turn:
                        if self.get_captured_moves(piece):
                            self.jumpable.append(piece)

    def get_valid_moves(self, piece):
        """
            Get all the positions that the current piece can move to.
        """
        valid_moves = {}
        if self.jumpable:
            if piece in self.jumpable:
                valid_moves.update(self.get_captured_moves(piece))
        else:
            valid_moves.update(self.get_uncaptured_moves(piece))
        return valid_moves

    def get_uncaptured_moves(self, piece):
        """
        Function -- get_uncaptured_moves
            Determines the valid moves for a piece that do not involve capturing an opponent's piece.
            It considers the direction of the movement based on the piece's color and whether
            it is a king. Non-king BLACK pieces can only move downwards, non-king RED pieces can
            only move upwards, and kings can move in any direction.

        Parameters:
            piece -- The current piece for which to determine valid non-capturing moves.

        Returns:
            uncaptured_moves -- A dictionary mapping potential move coordinates to the value
                                of the board at that location, typically EMPTY.
        """

        def add_move(row, col):
            if self.board[row][col] == EMPTY:
                uncaptured_moves[(row, col)] = self.board[row][col]

        uncaptured_moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 方向向量

        for d_row, d_col in directions:
            next_row, next_col = piece.row + d_row, piece.col + d_col
            if 0 <= next_row < NUM_SQUARES and 0 <= next_col < NUM_SQUARES:
                if (piece.color == BLACK and d_row > 0) or \
                        (piece.color == RED and d_row < 0) or piece.king:
                    add_move(next_row, next_col)
        return uncaptured_moves

    def get_captured_moves(self, piece):
        """
        Function -- get_captured_moves
            Identifies all the possible moves where the current piece can capture an opponent's piece.
            It checks for opponent pieces adjacent to the current piece and if the space beyond them
            is empty, allowing for a capturing move. It handles moves differently based on the piece's
            color and king status, with the same directional movement restrictions as in
            `get_uncaptured_moves`.

        Parameters:
            piece -- The current piece for which to determine valid capturing moves.

        Returns:
            capture_moves -- A dictionary containing all possible capturing moves for the piece,
                             where keys are the coordinates after the capture and values are EMPTY,
                             representing the space to which the piece would move.
        """

        def add_capture_move(row, col, enemy_row, enemy_col):
            if self.board[row][col] == EMPTY and \
                    isinstance(self.board[enemy_row][enemy_col], Piece) and \
                    self.board[enemy_row][enemy_col].color != piece.color:
                capture_moves[(row, col)] = self.board[row][col]
                self.aten_pieces.append(self.board[enemy_row][enemy_col])

        capture_moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 方向向量

        for d_row, d_col in directions:
            enemy_row, enemy_col = piece.row + d_row, piece.col + d_col
            capture_row, capture_col = enemy_row + d_row, enemy_col + d_col
            if 0 <= enemy_row < NUM_SQUARES and 0 <= enemy_col < NUM_SQUARES and \
                    0 <= capture_row < NUM_SQUARES and 0 <= capture_col < NUM_SQUARES:
                if self.board[enemy_row][enemy_col] != EMPTY and \
                        (piece.color == BLACK and d_row > 0) or \
                        (piece.color == RED and d_row < 0) or piece.king:
                    add_capture_move(capture_row, capture_col, enemy_row, enemy_col)

        return capture_moves

    def delete_piece(self, pieces):
        """
        Function -- delete_piece
            Delete the pieces in the board.
        Parameters:
            pieces -- The deleted pieces.
        Returns:
            Nothing.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = EMPTY
