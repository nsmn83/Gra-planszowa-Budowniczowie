import pygame

class Pionek():
    def __init__(self, img):
        self.x = None
        self.y = None
        self.img = pygame.image.load(img)

    #sprawdzenie mozliwych ruchow dla danego pionka
    # Updated sprawdzRuchy method to dynamically determine valid moves
    def sprawdzRuchy(self, stanGry):
        from stanGry import stanGry, Tura
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
        self.sprawdzRuchy(stanGry)
        if (x,y) in stanGry.mozliweRuchy:
            self.x = x
            self.y = y
            self.sprawdzTerenBudowy(stanGry)

    def sprawdzTerenBudowy(self, stanGry):
        from stanGry import stanGry, Tura
        stanGry.mozliweBudowanie = (2,2)
        self.stanTury = Tura.BUDUJ

    def zbudujPietro(self, x, y, stanGry):
        from stanGry import stanGry, Tura
        if (x,y) in stanGry.mozliweBudowanie:
            if stanGry.pola[x][y] < 4:
                stanGry.pola[x][y] += 1
                stanGry.zerujMozliweAkcje()
                self.stanTury == "Koniec"

    def rysujPionka(self, screen):
        screen.blit(self.img, self.x * 150, self.y * 150)