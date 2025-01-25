from piece import Piece
class Tile():
    def __init__(self):
        self.x = None
        self.y = None
        self.piece = None
        self.height = 0

    def isBlocked(self):
        if(self.piece):
            return True
        return False

    def deletePiece(self):
        self.piece = None
