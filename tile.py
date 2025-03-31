from piece import Piece
class Tile():
    def __init__(self):
        self.x = None
        self.y = None
        self.piece = None
        self.height = 0

    def is_blocked(self):
        if self.piece:
            return True
        return False

    def delete_piece(self):
        self.piece = None

    def return_piece(self):
        return self.piece
