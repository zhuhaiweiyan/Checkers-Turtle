'''
AN GE
CS5001 22FALL
FINAL PROJECT
Test.py
So many functions have no returns and a few returns of some functions cannot be represented on the test functions.
'''

from piece import Piece


def test_constructor():
    red_piece = Piece(5, 6, "red")
    black_piece = Piece(4, 3, "black")
    assert (red_piece.row == 5)
    assert (red_piece.col == 6)
    assert (red_piece.color == "red")
    assert (black_piece.row == 4)
    assert (black_piece.col == 3)
    assert (black_piece.color == "black")
