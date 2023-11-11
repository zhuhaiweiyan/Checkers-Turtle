class Piece:
    """
    A class to represent a piece in a checkerboard game, without visualization responsibilities.
    
    Attributes:
        row (int): The row of the piece on the board.
        col (int): The column of the piece on the board.
        color (str): The color of the piece.
        king (bool): Indicates if the piece is a king.
    """

    def __init__(self, row, col, color):
        """
        Constructor to create a new piece.

        Parameters:
            row (int): The row of the piece.
            col (int): The column of the piece.
            color (str): The color of the piece.
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        """
        Turns the piece into a king piece.
        """
        self.king = True

    def move(self, row, col):
        """
        Moves the piece to a new position.

        Parameters:
            row (int): The new row for the piece.
            col (int): The new column for the piece.
        """
        self.row = row
        self.col = col