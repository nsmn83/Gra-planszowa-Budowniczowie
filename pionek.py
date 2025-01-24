import pygame
from tura import Tura

class Pionek():
    def __init__(self, img):
        self.x = None
        self.y = None
        self.img = pygame.image.load(img)

    #sprawdzenie mozliwych ruchow dla danego pionka
    # Updated sprawdzRuchy method to dynamically determine valid moves
    def sprawdzRuchy(self, stanGry):
        valid_moves = []
        x, y = self.x, self.y

        # Example: Check the 8 surrounding squares
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:  # Skip the piece's own square
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 5 and 0 <= ny < 5:  # Ensure within board bounds
                        valid_moves.append((nx, ny))

        stanGry.mozliweRuchy = valid_moves
        print(stanGry.mozliweRuchy)
        stanGry.tura = Tura.RUCH

    #wykonanie ruchu przez pionek
    def wykonajRuch(self, x, y, stanGry):
        if (x, y) in stanGry.mozliweRuchy:
            self.x = x
            self.y = y
            stanGry.mozliweRuchy = []
            self.sprawdzWarunkiWygranej(stanGry)
            stanGry.tura = Tura.SPRAWDZBUDOWE

    def sprawdzBudowe(self, stanGry):
        valid_moves = []
        x, y = self.x, self.y

        # Example: Check the 8 surrounding squares
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:  # Skip the piece's own square
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 5 and 0 <= ny < 5:  # Ensure within board bounds
                        valid_moves.append((nx, ny))
        stanGry.mozliweBudowanie = valid_moves
        stanGry.tura = Tura.BUDUJ

    def wykonajBudowe(self, x, y, stanGry):
        stanGry.pola[x][y] += 1
        stanGry.mozliweBudowanie = []
        stanGry.tura = Tura.KONIEC

    def rysujPionka(self, screen):
        screen.blit(self.img, self.x * 150, self.y * 150)

    def sprawdzWarunkiWygranej(self, stanGry):
        if stanGry.pola[self.x][self.y] == 3:
            print("Gracz ", stanGry.aktualnyGracz.id, " wygrał gre")