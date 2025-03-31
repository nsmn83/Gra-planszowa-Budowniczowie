import pygame

class Piece():
    def __init__(self, gracz, img: pygame.surface):
        self.x = None
        self.prev_x = None
        self.y = None
        self.prev_y = None
        self.img = img
        self.owner = gracz
        self.moved = False
        self.build = False
    def draw_piece(self, screen: pygame.surface):
        self.img = pygame.transform.scale(self.img, (150, 150))
        screen.blit(self.img, (self.x * 150, self.y * 150))

    def draw_piece_special(self, screen: pygame.surface, x: int, y: int) -> None:
        self.img = pygame.transform.scale(self.img, (500, 500))
        screen.blit(self.img, (x, y))

    def return_piece_position(self):
        if self.x is None or self.y is None:
            return None
        return self.x, self.y

    def change_piece_position(self, x: int, y: int) -> None:
        self.prev_x = self.x
        self.x = x
        self.prev_y = self.y
        self.y = y