'''
AN GE
CS5001 22FALL
FINAL PROJECT
Test.py
So many functions have no returns and a few returns of some functions cannot be represented on the test functions.
'''

from gamestate import GameState
from board import Board

def test_constructor():
    game = GameState()
    game.board.movable = []
    game.board.jumpable = []
    assert (game.winner() is True)
    game.board.movable = [(2,0),(3,1)]
    assert (game.winner() is False)
    game.board.jumpable = [(3,1)]
    game.board.movable = []
    assert (game.winner() is False)