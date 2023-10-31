'''
ZHU HAI WEI YAN
GameState
'''
import turtle
import random
from board import Board
from const import *


class GameState:
    '''
    Class -- Board
        Represents a board.
    Attributes:
        pen -- A Turtle.
        clicked_piece -- The clicked piece.
        current_piece -- The current piece.
        board -- Create a Board object.
        turn -- The current turn.
        valid_moves -- Valid move sof the current piece.
    Methods:
        update -- Update the checkerboard.
        click_piece -- Determine the correctness of the clicked piece and execute the corresponding actions.
        draw_valid_moves -- Draw the current valid moves.
        exchange_turn -- Exchange the turn.
        winner -- Judge whether the game has a winner or not.
        screen -- Add the screen.
    '''

    def __init__(self):
        '''
        Constructor -- creates a new instance of PIece
        Parameters:
            self -- the game
        '''
        self.pen = turtle.Turtle()
        self.clicked_piece = None
        self.current_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def update(self):
        '''
        Function -- update
            Update the checkerboard.
        Returns:
            Nothing.
        '''
        self.board.draw_checkerboard()
        self.board.draw_pieces()
        self.draw_valid_moves(self.valid_moves)

    def screen(self, screen):
        '''
        Function -- screen
            Add the screen.
        Returns:
            Nothing.
        '''
        self.screen = screen

    def human_click_piece(self, row, col):
        '''
        Function -- click_piece
            Determine the correctness of the clicked piece and execute the corresponding actions.
        Parameters:
            row -- the row of the piece.
            col -- the col of the piece.
        Returns:
            Nothing.
        '''
        if 0 <= row < NUM_SQUARES and 0 <= col < NUM_SQUARES:
            self.clicked_piece = self.board.get_piece(row, col)
        if self.clicked_piece:
            if self.clicked_piece.color == self.turn:
                self.valid_moves.clear()
                self.valid_moves = self.board.get_valid_moves(
                    self.clicked_piece)
                self.current_piece = self.clicked_piece
                self.update()
        else:
            if self.current_piece and (row, col) in self.valid_moves:
                self.board.move_piece(self.current_piece, row, col)
                self.board.delete_piece(self.board.aten_pieces)
                if self.board.jumpable and self.board.get_captured_moves(
                        self.board.board[row][col]):
                    self.current_piece = self.board.board[row][col]
                    self.board.jumpable = [self.board.board[row][col]]
                    self.valid_moves = self.board.get_captured_moves(
                        self.board.board[row][col])
                else:
                    self.current_piece = None
                    self.board.aten_pieces = []
                    self.board.jumpable = []
                    self.board.movable = []
                    self.valid_moves.clear()
                    self.exchange_turn()
                    self.board.judge_movable(self.turn)
                    self.board.judge_jumpable(self.turn)
                    self.update()
                    if not self.winner():
                        self.update()
                        self.screen.ontimer(self.computer, 1000)
                    else:
                        self.update()
                        self.exchange_turn()
                        print(self.turn, "WIN!")
                        self.pen.pencolor("deep sky blue")
                        self.pen.setposition(0, 0)
                        self.pen.pendown()
                        self.pen.write("YOU WIN!", False, 'center',
                                       ("Arial", 30, "bold"))
                        self.pen.penup()

    def computer(self):
        '''
        Function -- computer
            Computer move automatically .
        Returns:
            Nothing.
        '''
        if self.board.jumpable:
            jump = random.choice(self.board.jumpable)
            valid_moves = self.board.get_valid_moves(jump)
            while valid_moves:
                aim = random.choice(list(valid_moves.keys()))
                self.board.move_piece(jump, aim[0], aim[1])
                self.board.delete_piece(self.board.aten_pieces)
                piece = self.board.board[aim[0]][aim[1]]
                valid_moves = self.board.get_captured_moves(piece)
        else:
            if self.board.movable:
                move = random.choice(self.board.movable)
                valid_moves = self.board.get_valid_moves(move)
                if valid_moves:
                    aim = random.choice(list(valid_moves.keys()))
                    self.board.move_piece(move, aim[0], aim[1])
                    self.board.judge_movable(self.turn)

        self.board.aten_pieces = []
        self.board.jumpable = []
        self.board.movable = []
        self.valid_moves.clear()
        self.update()
        self.exchange_turn()
        self.board.judge_movable(self.turn)
        self.board.judge_jumpable(self.turn)
        if self.winner():
            print("Computer WIN!")
            self.pen.pencolor("deep sky blue")
            self.pen.setposition(0, 0)
            self.pen.pendown()
            self.pen.write("YOU LOSE!", False, 'center', ("Arial", 30, "bold"))
            self.pen.penup()

    def draw_valid_moves(self, moves):
        '''
        Function -- draw_valid_moves
            Draw the current valid moves.
        Parameters:
            moves -- The current valid moves.
        Returns:
            Nothing.
        '''
        pen = self.pen
        for move in moves:
            row = move[0]
            col = move[1]
            pen.setposition((-NUM_SQUARES / 2 + col) * SQUARE,
                            (-NUM_SQUARES / 2 + row) * SQUARE)
            pen.color("red")
            pen.pendown()
            for i in range(NUM_EDGE):
                pen.forward(SQUARE)
                pen.left(RIGHT_ANGLE)
            pen.penup()
        if self.board.jumpable:
            for piece in self.board.jumpable:
                row = piece.row
                col = piece.col
                print(row, col)
                pen.setposition((-NUM_SQUARES / 2 + col) * SQUARE,
                                (-NUM_SQUARES / 2 + row) * SQUARE)
                pen.color("lime")
                pen.pendown()
                for i in range(NUM_EDGE):
                    pen.forward(SQUARE)
                    pen.left(RIGHT_ANGLE)
                pen.penup()
        elif self.board.movable:
            for piece in self.board.movable:
                row = piece.row
                col = piece.col
                pen.setposition((-NUM_SQUARES / 2 + col) * SQUARE,
                                (-NUM_SQUARES / 2 + row) * SQUARE)
                pen.color("lime")
                pen.pendown()
                for i in range(NUM_EDGE):
                    pen.forward(SQUARE)
                    pen.left(RIGHT_ANGLE)
                pen.penup()

    def exchange_turn(self):
        '''
        Function -- exchange_turn
            Exchange the turn.
        Returns:
            Nothing.
        '''
        if self.turn == BLACK:
            self.turn = RED
        else:
            self.turn = BLACK

    def winner(self):
        '''
        Function -- winner
            Judge whether the game has a winner or not.
        Returns:
            Return False if pieces of the current turn have valid moves. Otherwise return True.
        '''
        if self.board.movable or self.board.jumpable:
            return False
        return True
