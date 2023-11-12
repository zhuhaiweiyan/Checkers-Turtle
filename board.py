"""
ZHU HAI WEI YAN
Board
"""

from const import *
from piece import Piece
from visualizer import Visualizer


class Board:
    """
    A class to represent the checkerboard in a checkerboard game.

    Attributes:
        board (list): A nested list representing the board's state.
        aten_pieces (list): The pieces that can be captured this turn.
        jumpable (list): Pieces that can capture an opponent's piece this turn.
        movable (list): Pieces that can move this turn.
        visualizer (Visualizer): An instance of the Visualizer class for drawing.
    """

    def __init__(self):
        """
        Constructor to create a new board.
        """
        self.board = []
        self.aten_pieces = []
        self.jumpable = []
        self.movable = []
        self.visualizer = Visualizer()
        self.create_board()
        self.visualizer.draw_checkerboard(NUM_SQUARES, SQUARE)
        self.draw_pieces()

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
        # initialize self.movable
        self.judge_movable(BLACK)

    def draw_pieces(self):
        """
        Draw all pieces on the checkerboard using the visualizer.
        """
        for row in self.board:
            for piece in row:
                if piece != EMPTY:
                    self.visualizer.draw_piece(piece, NUM_SQUARES, SQUARE, RADIUS)

    def get_piece(self, row, col):
        """
            Get the piece through the row and col.
        """
        return self.board[row][col]

    def move_piece(self, piece, new_row, new_col):
        """
        Moves a piece to a new position and potentially promotes it to a king.
        """
        self.aten_pieces = []
        captured_moves = self.get_captured_moves(piece)
        if (new_row, new_col) in captured_moves:
            enemy_position = captured_moves[(new_row, new_col)]
            self.aten_pieces.append(self.board[enemy_position[0]][enemy_position[1]])
 
        self.board[piece.row][piece.col] = EMPTY
        self.board[new_row][new_col] = piece
        piece.move(new_row, new_col)
        
        if (piece.color == BLACK and new_row == NUM_SQUARES - 1) or \
           (piece.color == RED and new_row == 0):
            piece.make_king()
        
        if self.aten_pieces:
            self.delete_piece(self.aten_pieces)

    def judge_jumpable(self, turn):
        """
        Judge whether there are some pieces that can capture an opponent's piece this turn.
        """
        self.jumpable.clear()
        for row in self.board:
            for piece in row:
                if piece != EMPTY and piece.color == turn:
                    if self.get_captured_moves(piece):
                        self.jumpable.append(piece)

    def judge_movable(self, turn):
        """
        Judge whether there are some pieces that can move in the current turn.
        """
        if not self.jumpable:  # Only fill movable if no pieces can jump
            self.movable.clear()
            for row in self.board:
                for piece in row:
                    if piece != EMPTY and piece.color == turn:
                        if self.get_uncaptured_moves(piece):
                            self.movable.append(piece)

    def get_valid_moves(self, piece):
        """
        Get all the positions that the current piece can move to.
        """
        valid_moves = {}
        if piece in self.jumpable:
            valid_moves.update(self.get_captured_moves(piece))
        elif not self.jumpable:
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

        uncaptured_moves = {}
        for d_row, d_col in DIRECTIONS:
            next_row, next_col = piece.row + d_row, piece.col + d_col
            if 0 <= next_row < NUM_SQUARES and 0 <= next_col < NUM_SQUARES:
                if (piece.color == BLACK and d_row > 0) or \
                        (piece.color == RED and d_row < 0) or piece.king:
                    if self.board[next_row][next_col] == EMPTY:
                        uncaptured_moves[(next_row, next_col)] = self.board[next_row][next_col]
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
        capture_moves = {}
        for d_row, d_col in DIRECTIONS:
            enemy_row, enemy_col = piece.row + d_row, piece.col + d_col
            capture_row, capture_col = enemy_row + d_row, enemy_col + d_col
            if 0 <= enemy_row < NUM_SQUARES and 0 <= enemy_col < NUM_SQUARES and \
                    0 <= capture_row < NUM_SQUARES and 0 <= capture_col < NUM_SQUARES:
                if self.board[enemy_row][enemy_col] != EMPTY and \
                        (piece.color == BLACK and d_row > 0) or \
                        (piece.color == RED and d_row < 0) or piece.king:
                    if isinstance(self.board[enemy_row][enemy_col], Piece) and \
                            self.board[enemy_row][enemy_col].color != piece.color and \
                            self.board[capture_row][capture_col] == EMPTY:
                        capture_moves[(capture_row, capture_col)] = (enemy_row, enemy_col)
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
