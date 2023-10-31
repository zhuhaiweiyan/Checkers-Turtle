'''
ZHU HAI WEI YAN
Board
'''
import turtle
from const import *
from piece import Piece


class Board():
    '''
    Class -- Board
        Represents a board.
    Attributes:
        pen -- A Turtle.
        board -- All pieces existed on the checkerboard, a nested double list.
        aten_pieces -- The aten pieces in the current turn, a list.
        jumpable -- All pieces which can eat the oppponent's piece in the current turn, a string.
        movable -- All pieces which can move in the current turn, a string.
    Methods:
        draw_square -- Draw a square.
        draw_checkerboard -- Draw a checkerboard.
        create_board -- Create a nested list storing status of all squares.
        draw_pieces -- Draw all pieces on the checkerboard.
        get_piece -- Find the piece through the row and col.
        move_piece -- Move the piece to the position (row,col).
        judge_movable -- Judge whether there are some pieces that can move in the current turn.
        judge_jaumpable -- Judge whether there are some pieces that can eat pieces in the current turn.
        get_valid_moves -- Get all the positions that the current piece can move to.
        get_uncaptured_moves -- Get all the uncaptured positions that the current piece can move to.
        get_captured_moves -- Get all the captured positions that the current piece can move to.
        delete_piece -- Delete the pieces in the board.
    '''

    def __init__(self):
        '''
            Constructor -- creates a new instance of PIece
            Parameters:
                self -- the board
        '''
        self.pen = turtle.Turtle()
        self.board = []
        self.aten_pieces = []
        self.jumpable = []
        self.movable = []
        self.create_board()

    def draw_square(self, size):
        '''
        Function -- draw_square
            Draw a square.
        Parameters:
            size -- The length of each side of the square.
        Returns:
            Nothing. Draws a square in the graphics window.
        '''
        self.pen.pendown()
        self.pen.begin_fill()
        for i in range(NUM_EDGE):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.end_fill()
        self.pen.penup()

    def draw_checkerboard(self):
        '''
        Function -- draw_checkerboard
            Draw a checkerboard.
        Returns:
            Nothing. Draws a checkerboard in the graphics window.
        '''
        pen = self.pen
        pen.penup()
        pen.hideturtle()
        pen.color("black", "white")
        corner = -NUM_SQUARES / 2 * SQUARE
        pen.setposition(corner, corner)
        self.draw_square(NUM_SQUARES * SQUARE)
        pen.color("black", "gray")
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    pen.setposition(corner + SQUARE * col,
                                    corner + SQUARE * row)
                    self.draw_square(SQUARE)

    def create_board(self):
        '''
        Function -- create_board
            Create a nested list storing status of all squares.
        Returns:
            Nothing.
        '''
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
        '''
        Function -- draw_pieces
            Draw all pieces on the checkerboard.
        Returns:
            Nothing.
        '''
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                piece = self.board[row][col]
                if piece != EMPTY:
                    piece.draw_piece()

    def get_piece(self, row, col):
        '''
        Function -- get_piece
            Find the piece through the row and col.
        Parameters:
            row -- the row
            col -- the col
        Returns:
            Nothing.
        '''
        return self.board[row][col]

    def move_piece(self, piece, row, col):
        '''
        Function -- move_piece
            Move the piece to the position (row,col).
        Parameters:
            row -- the row
            col -- the col
        Returns:
            Nothing.
        '''
        self.board[piece.row][piece.col], self.board[row][col] = self.board[
            row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == NUM_SQUARES - 1 or row == 0:
            piece.make_king()

    def judge_movable(self, turn):
        '''
        Function -- judge_movable
            Judge whether there are some pieces that can move in the current turn.
        Parameters:
            turn -- The current turn.
        Returns:
            Nothing.
        '''
        for row in self.board:
            for piece in row:
                if piece != EMPTY:
                    if piece.color == turn:
                        if self.get_uncaptured_moves(piece):
                            self.movable.append(piece)

    def judge_jumpable(self, turn):
        '''
        Function -- judge_jumpable
            Judge whether there are some pieces that can eat pieces in the current turn.
        Parameters:
            turn -- The current turn.
        Returns:
            Nothing.
        '''
        for row in self.board:
            for piece in row:
                if piece != EMPTY:
                    if piece.color == turn:
                        if self.get_captured_moves(piece):
                            self.jumpable.append(piece)

    def get_valid_moves(self, piece):
        '''
        Function -- get_valid_moves
            Get all the positions that the current piece can move to.
        Parameters:
            piece -- The current piece.
        Returns:
            valid_moves -- Return valid moves of the current piece.
        '''
        valid_moves = {}
        if self.jumpable:
            if piece in self.jumpable:
                valid_moves.update(self.get_captured_moves(piece))
        else:
            valid_moves.update(self.get_uncaptured_moves(piece))
        return valid_moves

    def get_uncaptured_moves(self, piece):
        uncaptured_moves = {}

        def try_move(row, col, color):
            if self.board[row][col] == EMPTY:
                uncaptured_moves[(row, col)] = self.board[row][col]

        row, col = piece.row, piece.col
        if piece.color == BLACK or piece.king:
            if row + 1 < NUM_SQUARES:
                if col - 1 >= 0:
                    try_move(row + 1, col - 1, piece.color)
                if col + 1 < NUM_SQUARES:
                    try_move(row + 1, col + 1, piece.color)
        if piece.color == RED or piece.king:
            if row - 1 >= 0:
                if col - 1 >= 0:
                    try_move(row - 1, col - 1, piece.color)
                if col + 1 < NUM_SQUARES:
                    try_move(row - 1, col + 1, piece.color)
        return uncaptured_moves

    def get_captured_moves(self, piece):
        capture_moves = {}

        def try_capture(row, col, next_row, next_col, color):
            if self.board[row][col] != EMPTY and self.board[row][col].color != color:
                if self.board[next_row][next_col] == EMPTY:
                    capture_moves[(next_row, next_col)] = self.board[next_row][next_col]
                    self.aten_pieces = [self.board[row][col]]

        row, col = piece.row, piece.col
        if piece.color == BLACK or piece.king:
            if row + 1 < NUM_SQUARES and row + 2 < NUM_SQUARES:
                if col - 1 >= 0 and col - 2 >= 0:
                    try_capture(row + 1, col - 1, row + 2, col - 2, piece.color)
                if col + 1 < NUM_SQUARES and col + 2 < NUM_SQUARES:
                    try_capture(row + 1, col + 1, row + 2, col + 2, piece.color)
        if piece.color == RED or piece.king:
            if row - 1 >= 0 and row - 2 >= 0:
                if col - 1 >= 0 and col - 2 >= 0:
                    try_capture(row - 1, col - 1, row - 2, col - 2, piece.color)
                if col + 1 < NUM_SQUARES and col + 2 < NUM_SQUARES:
                    try_capture(row - 1, col + 1, row - 2, col + 2, piece.color)
        return capture_moves

    # def get_uncaptured_moves(self, piece):
    #     '''
    #     Function -- get_uncaptured_moves
    #         Get all the uncaptured positions that the current piece can move to.
    #     Parameters:
    #         piece -- The current piece.
    #     Returns:
    #         uncaptured_moves -- Return uncaptured moves of the current piece.
    #     '''
    #     uncaptured_moves = {}
    #     row = piece.row
    #     col = piece.col
    #     if piece.color == BLACK or piece.king:
    #         if row + 1 < NUM_SQUARES and col - 1 >= 0:
    #             if self.board[row + 1][col - 1] == EMPTY:
    #                 uncaptured_moves[(row + 1,
    #                                   col - 1)] = self.board[row + 1][col - 1]
    #         if row + 1 < NUM_SQUARES and col + 1 < NUM_SQUARES:
    #             if self.board[row + 1][col + 1] == EMPTY:
    #                 uncaptured_moves[(row + 1,
    #                                   col + 1)] = self.board[row + 1][col + 1]
    #     if piece.color == RED or piece.king:
    #         if row - 1 >= 0 and col - 1 >= 0:
    #             if self.board[row - 1][col - 1] == EMPTY:
    #                 uncaptured_moves[(row - 1,
    #                                   col - 1)] = self.board[row - 1][col - 1]
    #         if row - 1 >= 0 and col + 1 < NUM_SQUARES:
    #             if self.board[row - 1][col + 1] == EMPTY:
    #                 uncaptured_moves[(row - 1,
    #                                   col + 1)] = self.board[row - 1][col + 1]
    #     return uncaptured_moves
    #
    # def get_captured_moves(self, piece):
    #     '''
    #     Function -- get_captured_moves
    #         Get all the captured positions that the current piece can move to.
    #     Parameters:
    #         piece -- The current piece.
    #     Returns:
    #         uncaptured_moves -- Return captured moves of the current piece.
    #     '''
    #     capture_moves = {}
    #     row = piece.row
    #     col = piece.col
    #     if piece.color == BLACK or piece.king:
    #         if row + 1 < NUM_SQUARES and col - 1 >= 0:
    #             if self.board[row + 1][col - 1] != EMPTY:
    #                 if self.board[row + 1][col - 1].color != piece.color:
    #                     if row + 2 < NUM_SQUARES and col - 2 >= 0:
    #                         if self.board[row + 2][col - 2] == EMPTY:
    #                             capture_moves[(row + 2, col -
    #                                            2)] = self.board[row + 2][col -
    #                                                                      2]
    #                             self.aten_pieces = [
    #                                 self.board[row + 1][col - 1]
    #                             ]
    #         if row + 1 < NUM_SQUARES and col + 1 < NUM_SQUARES:
    #             if self.board[row + 1][col + 1] != EMPTY:
    #                 if self.board[row + 1][col + 1].color != piece.color:
    #                     if row + 2 < NUM_SQUARES and col + 2 < NUM_SQUARES:
    #                         if self.board[row + 2][col + 2] == EMPTY:
    #                             capture_moves[(row + 2, col +
    #                                            2)] = self.board[row + 2][col +
    #                                                                      2]
    #                             self.aten_pieces = [
    #                                 self.board[row + 1][col + 1]
    #                             ]
    #     if piece.color == RED or piece.king:
    #         if row - 1 >= 0 and col - 1 >= 0:
    #             if self.board[row - 1][col - 1] != EMPTY:
    #                 if self.board[row - 1][col - 1].color != piece.color:
    #                     if row - 2 >= 0 and col - 2 >= 0:
    #                         if self.board[row - 2][col - 2] == EMPTY:
    #                             capture_moves[(row - 2, col -
    #                                            2)] = self.board[row - 2][col -
    #                                                                      2]
    #                             self.aten_pieces = [
    #                                 self.board[row - 1][col - 1]
    #                             ]
    #         if row - 1 >= 0 and col + 1 < NUM_SQUARES:
    #             if self.board[row - 1][col + 1] != EMPTY:
    #                 if self.board[row - 1][col + 1].color != piece.color:
    #                     if row - 2 >= 0 and col + 2 < NUM_SQUARES:
    #                         if self.board[row - 2][col + 2] == EMPTY:
    #                             capture_moves[(row - 2, col +
    #                                            2)] = self.board[row - 2][col +
    #                                                                      2]
    #                             self.aten_pieces = [
    #                                 self.board[row - 1][col + 1]
    #                             ]
    #     return capture_moves

    def delete_piece(self, pieces):
        '''
        Function -- delete_piece
            Delete the pieces in the board.
        Parameters:
            pieces -- The deleted pieces.
        Returns:
            Nothing.
        '''
        for piece in pieces:
            self.board[piece.row][piece.col] = EMPTY
