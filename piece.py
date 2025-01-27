import pygame

class Piece():
    def __init__(self, gracz, img):
        self.x = None
        self.prevX = None
        self.y = None
        self.prevY = None
        self.img = img
        self.owner = gracz
        self.moved = False
        self.build = False
    def drawPiece(self, screen):
        self.img = pygame.transform.scale(self.img, (150, 150))
        screen.blit(self.img, (self.x * 150, self.y * 150))

    def drawPieceSpecial(self, screen, x, y):
        self.img = pygame.transform.scale(self.img, (500, 500))
        screen.blit(self.img, (x, y))

    def returnPiecePosition(self):
        if self.x is None or self.y is None:
            return None
        return self.x, self.y

    def changePiecePosition(self, x, y):
        self.prevX = self.x
        self.x = x
        self.prevY = self.y
        self.y = y