'''
ZHU HAI WEI YAN
GameState
'''

import random
from board import Board
from const import *
from visualizer import Visualizer


class GameState:
    """
    A class to represent the state of a checkerboard game.

    Attributes:
        pen (Turtle): A Turtle object for drawing.
        clicked_piece (Piece): The piece that was clicked.
        current_piece (Piece): The currently active piece.
        board (Board): The game board.
        turn (str): The current turn, either BLACK or RED.
        valid_moves (dict): A dictionary of valid moves for the current piece.
    """

    def __init__(self):
        """
        Constructor to create a new game state.
        """
        self.clicked_piece = None
        self.current_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.visualizer = Visualizer()

    def update(self):
        """
        Updates the state of the checkerboard and draws the valid moves.
        """
        self.visualizer.draw_checkerboard(NUM_SQUARES, SQUARE)
        self.board.draw_pieces()
        self.draw_valid_moves(self.valid_moves)

    def screen(self, screen):
        self.screen = screen

    def reset_game_state(self):
        ''' Reset the game state for the next turn '''
        self.current_piece = None
        self.board.aten_pieces = []
        self.board.jumpable = []
        self.board.movable = []
        self.valid_moves.clear()

    def complete_turn(self):
        ''' Complete the turn and update the game state '''
        self.reset_game_state()
        self.exchange_turn()
        self.board.judge_movable(self.turn)
        self.board.judge_jumpable(self.turn)
        self.update()

        if not self.winner():
            if self.turn == BLACK:
                pass  # Set the game to wait for the player
            else:
                self.screen.ontimer(self.computer, 1000)
        else:
            self.exchange_turn()
            print(f"{self.turn} WIN!")
            self.visualizer.display_winner(self.turn)

    def human_click_piece(self, row, col):
        """
        Handles human player's piece selection and movement.

        Parameters:
            row (int): The row of the clicked position.
            col (int): The column of the clicked position.
        """
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
                # self.board.delete_piece(self.board.aten_pieces)
                if self.board.jumpable and self.board.get_captured_moves(
                        self.board.board[row][col]):
                    self.current_piece = self.board.board[row][col]
                    self.board.jumpable = [self.board.board[row][col]]
                    self.valid_moves = self.board.get_captured_moves(
                        self.board.board[row][col])
                else:
                    self.complete_turn()

    def computer(self):
        '''
            Computer move automatically .
        '''
        if self.board.jumpable:
            jump = random.choice(self.board.jumpable)
            valid_moves = self.board.get_valid_moves(jump)
            while valid_moves:
                aim = random.choice(list(valid_moves.keys()))
                self.board.move_piece(jump, aim[0], aim[1])
                # self.board.delete_piece(self.board.aten_pieces)
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

        self.complete_turn()

    def draw_valid_moves(self, moves):
        self.visualizer.draw_valid_moves(moves)
        if self.board.jumpable:
            self.visualizer.highlight_pieces(self.board.jumpable)
        elif self.board.movable:
            self.visualizer.highlight_pieces(self.board.movable)

    def exchange_turn(self):
        ''' Toggle the player's turn '''
        self.turn = RED if self.turn == BLACK else BLACK

    def winner(self):
        if self.board.movable or self.board.jumpable:
            return False
        return True
