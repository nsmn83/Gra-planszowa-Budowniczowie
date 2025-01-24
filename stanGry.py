import pygame
from gracz import  Gracz
from tura import Tura
class stanGry():
    def __init__(self):
        pygame.init()
        self.tura = Tura.SPRAWDZRUCH
        self.aktualnyPionek = None
        self.gracze = [Gracz("Pictures/pionek1.png", 0), Gracz("Pictures/pionek2.png", 1)]
        self.aktualnyGracz = self.gracze[0]
        self.mozliweRuchy = []
        self.mozliweBudowanie = []
        # Ustawienie pozycji pionków gracza
        self.gracze[0].pionki[0].x, self.gracze[0].pionki[0].y = 2, 3
        self.gracze[0].pionki[1].x, self.gracze[0].pionki[1].y = 1, 1
        self.gracze[1].pionki[0].x, self.gracze[1].pionki[0].y = 3, 3
        self.gracze[1].pionki[1].x, self.gracze[1].pionki[1].y = 4, 4
        self.pola = [[0 for _ in range(5)] for _ in range(5)]
        self.floor1 = pygame.image.load("Pictures/floor1.png")
        self.floor2 = pygame.image.load("Pictures/floor2.png")
        self.floor3 = pygame.image.load("Pictures/floor3.png")
        self.floor4 = pygame.image.load("Pictures/floor4.png")

    def wypiszTure(self):
        print(f"Obecna tura: {self.tura.name}")

    def zmienGracza(self):
        indeksGracza = self.gracze.index(self.aktualnyGracz)
        indeksNastepnegoGracza = (indeksGracza + 1) % len(self.gracze)
        self.aktualnyGracz = self.gracze[indeksNastepnegoGracza]
        print("Obecny gracz: ", self.aktualnyGracz.id)
        return self.aktualnyGracz

    def zerujMozliweAkcje(self):
        self.mozliweRuchy = []
        self.mozliweBudowanie = []

    def zwrocPionka(self, x, y):
        if self.aktualnyGracz is None:
            print("Brak aktualnego gracza!")
            return None
        for pionek in self.aktualnyGracz.pionki:
            if (pionek.x, pionek.y) == (x, y):
                return pionek
        return None

    def rysuj_plansze(self, surface):
        for row in range(0, 5):
            for col in range(0, 5):
                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(row * 150, col * 150, 150, 150), 1)
                if(self.pola[row][col] == 1):
                    self.floor1 = pygame.transform.scale(self.floor1, (150, 150))
                    surface.blit(self.floor1, (row * 150, col * 150))
                if(self.pola[row][col] == 2):
                    self.floor2 = pygame.transform.scale(self.floor2, (150, 150))
                    surface.blit(self.floor2, (row * 150, col * 150))
                if(self.pola[row][col] == 3):
                    self.floor3 = pygame.transform.scale(self.floor3, (150, 150))
                    surface.blit(self.floor3, (row * 150, col * 150))
                if(self.pola[row][col] == 4):
                    self.floor4 = pygame.transform.scale(self.floor4, (150, 150))
                    surface.blit(self.floor4, (row * 150, col * 150))


    def rysujRuchy(self, surface):
        for (x, y) in self.mozliweRuchy:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(x * 150, y * 150, 150, 150), 5)

        for (x, y) in self.mozliweBudowanie:
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(x * 150, y * 150, 150, 150), 5)


    def rysujPionki(self, surface):
        for gracz in self.gracze:
            for pionek in gracz.pionki:
                if pionek.x is not None and pionek.y is not None:
                    x = pionek.x * 150
                    y = pionek.y * 150
                    obrazek = pionek.img
                    obrazek = pygame.transform.scale(obrazek, (150, 150))
                    surface.blit(obrazek, (x, y))



    def rysujStanGry(self, surface):
        self.rysuj_plansze(surface)
        self.rysujPionki(surface)