import pygame

class Piece():
    def __init__(self, gracz, img):
        self.x = None
        self.y = None
        self.img = img
        self.owner = gracz
        self.moved = False
        self.build = False
    def drawPiece(self, screen):
        self.img = pygame.transform.scale(self.img, (150, 150))
        screen.blit(self.img, (self.x * 150, self.y * 150))

    def returnPiecePosition(self):
        if self.x is None or self.y is None:
            return None
        return self.x, self.y

    def changePiecePosition(self, x, y):
        self.x = x
        self.y = y