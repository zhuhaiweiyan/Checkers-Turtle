"""
ZHU HAI WEI YAN
GameState
"""

import random
from board import Board
from const import *
from visualizer import Visualizer


class GameState:
    """
    A class to represent the state of a checkerboard game.

    Attributes:
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
        self.screen = None
        self.clicked_piece = None
        self.current_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.visualizer = Visualizer()
        self.game_over = False

    def update(self):
        """
        Updates the state of the checkerboard and draws the valid moves.
        """
        self.visualizer.draw_checkerboard(NUM_SQUARES, SQUARE)
        self.board.draw_pieces()
        self.visualize_moves(self.valid_moves)

    def screen(self, screen):
        self.screen = screen

    def reset_game_state(self):
        """ Reset the game state for the next turn """
        self.current_piece = None
        self.board.aten_pieces = []
        self.board.jumpable = []
        self.board.movable = []
        self.valid_moves.clear()

    def complete_turn(self):
        """ Complete the turn and update the game state """
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
            self.game_over = True

    def handle_click(self, x, y):
        """
        Handles the click event within the game window.
        """
        row = int(y // SQUARE + NUM_SQUARES / 2)
        col = int(x // SQUARE + NUM_SQUARES / 2)
        if -NUM_SQUARES / 2 * SQUARE <= x <= NUM_SQUARES / 2 * SQUARE and \
           -NUM_SQUARES / 2 * SQUARE <= y <= NUM_SQUARES / 2 * SQUARE:
            print(f"Clicked at ({row}, {col})")
            self.human_click_piece(row, col)
        else:
            print("The click was not in bounds.")

    def human_click_piece(self, row, col):
        """
        Handles human player's piece selection and movement.

        Parameters:
            row (int): The row of the clicked position.
            col (int): The column of the clicked position.
        """
        if self.game_over:
            return
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
                if self.board.jumpable and self.board.get_captured_moves(
                        self.board.board[row][col]):
                    self.current_piece = self.board.board[row][col]
                    self.board.jumpable = [self.board.board[row][col]]
                    self.valid_moves = self.board.get_captured_moves(
                        self.board.board[row][col])
                else:
                    self.complete_turn()

    def computer(self):
        """
            Computer move automatically .
        """
        if self.game_over:
            return
        if self.board.jumpable:
            jump = random.choice(self.board.jumpable)
            valid_moves = self.board.get_valid_moves(jump)
            while valid_moves:
                aim = random.choice(list(valid_moves.keys()))
                self.board.move_piece(jump, aim[0], aim[1])
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

    def visualize_moves(self, moves):
        """
        Draws the valid moves and highlights the pieces that can move or capture.
        """
        self.visualizer.draw_valid_moves(moves)
        active_pieces = self.board.jumpable if self.board.jumpable else self.board.movable
        self.visualizer.highlight_pieces(active_pieces)

    def exchange_turn(self):
        """
        Toggles the player's turn to the opposite color.
        """
        self.turn = RED if self.turn == BLACK else BLACK

    def winner(self):
        """
        Determines if the game has a winner.
        
        Returns:
            True if the current player has no valid moves left, indicating a win for the other player.
        """
        return not (self.board.movable or self.board.jumpable)
