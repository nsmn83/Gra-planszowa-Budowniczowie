import pygame
from menu import MainMenu, Options, Instruction
from Gracz import Gracz

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.width = 1280
        self.height = 750
        self.display = pygame.display.set_mode((self.width, self.height))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font_name = 'Fonts/8-bit Arcade In.ttf'
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu
        self.stan_pola = [[(0, None) for _ in range(5)] for _ in range(5)]
        self.floor1 = pygame.image.load("Pictures/floor1.png")
        self.floor2 = pygame.image.load("Pictures/floor2.png")
        self.floor3 = pygame.image.load("Pictures/floor3.png")
        self.floor4 = pygame.image.load("Pictures/floor4.png")
        self.img = pygame.image.load("Pictures/background.jpg")
        self.pionek1 = pygame.image.load("Pictures/pionek1.png")
        self.pionek2 = pygame.image.load("Pictures/pionek2.png")
        self.stan = "postawPionka"
        self.gracze = [Gracz(), Gracz()]
        self.aktywnyPionek = None
        self.aktywnyGracz = None
        self.poleGry = None

    def ktore_pole(self, pos):
        x,y = pos
        x -= 280
        return int(x/150), int(y/150)

    def game_loop(self):
        while self.playing:
            self.check_action()
            self.display.fill((0,0,0))
            self.draw_menu_background()
            self.window.blit(self.display, (0,0))
            pygame.display.update()

    def obliczRuchy(self, pionek):
        kierunki = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, 1)]
        mozliwe_ruchy = []
        obecna_wartosc = self.stan_pola[pionek.x][pionek.y][0]

        for dx, dy in kierunki:
            nowy_x, nowy_y = pionek.x + dx, pionek.y + dy
            if 0 <= nowy_x < len(self.stan_pola) and 0 <= nowy_y < len(self.stan_pola[0]):
                if self.stan_pola[nowy_x][nowy_y][0] <= obecna_wartosc + 1:
                    mozliwe_ruchy.append((nowy_x, nowy_y))

        return mozliwe_ruchy
        for mozliwy in mozliwe_ruchy:
            pygame.draw.rect(self.poleGry, (0, 0, 0), pygame.Rect(mozliwy[0] * 150, mozliwy[1] * 150, 150, 150), 1)


    def blit_screen(self):
        self.draw_menu_background()
        self.window.blit(self.game.display, (0,0))
        pygame.display.update()

    def check_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = self.ktore_pole(event.pos)
                if(self.aktywnyPionek is None):
                    if self.stan_pola[x][y][1] in self.gracze[0].Pionki:
                        self.aktywnyPionek = self.stan_pola[x][y][1]
                        print("Wybrano pionka joł 1")
                        self.obliczRuchy(self.aktywnyPionek)
                        self.stan = "Ruch"
                        break
                    elif self.stan_pola[x][y][1] in self.gracze[1].Pionki:
                        self.aktywnyPionek = self.stan_pola[x][y][1]
                        self.obliczRuchy(self.aktywnyPionek)
                        print("Wybrano pionka joł 2")
                        self.stan = "Ruch"
                        break
                if(self.stan == "postawPionka"):
                    print("Stawianie pionka")
                    if(self.gracze[0].Pionki[0].x is None):
                        self.stan_pola[x][y] = (self.stan_pola[x][y][0], self.gracze[0].Pionki[0])
                        self.gracze[0].Pionki[0].x = x
                        self.gracze[0].Pionki[0].y = y
                    elif (self.gracze[0].Pionki[0].x is None):
                        self.stan_pola[x][y] = (self.stan_pola[x][y][0], self.gracze[0].Pionki[1])
                        self.gracze[0].Pionki[1].x = x
                        self.gracze[0].Pionki[1].y = y
                    elif(self.gracze[1].Pionki[0].x is None):
                        self.stan_pola[x][y] = (self.stan_pola[x][y][0], self.gracze[1].Pionki[0])
                        self.gracze[1].Pionki[0].x = x
                        self.gracze[1].Pionki[0].y = y
                    elif (self.gracze[1].Pionki[0].x is None):
                        self.stan_pola[x][y] = (self.stan_pola[x][y][0], self.gracze[1].Pionki[1])
                        self.gracze[1].Pionki[1].x = x
                        self.gracze[1].Pionki[1].y = y
                    break
                if(self.stan == "Buduj"):
                    self.stan_pola[x][y] = (self.stan_pola[x][y][0]+1, self.stan_pola[x][y][1])
                    self.stan = "None"
                    break
                if(self.stan == "Ruch"):
                    print("Ruszanie pionka przed wywolanie funkcji")
                    self.ruszPionka(x,y)
                    break
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        return text_rect

    def ruszPionka(self, x, y):
        print("Ruszanie pionka joł")
        if((x,y) in self.obliczRuchy(self.aktywnyPionek)):
            self.stan_pola[self.aktywnyPionek.x][self.aktywnyPionek.y] = (self.stan_pola[self.aktywnyPionek.x][self.aktywnyPionek.y][0], None)
            self.aktywnyPionek.x = x
            self.aktywnyPionek.y = y
            self.stan_pola[x][y] = (self.stan_pola[x][y][0], self.aktywnyPionek)
            self.aktywnyPionek = None
            self.stan = "Buduj"

    def draw_menu_background(self):
        self.display.blit(self.img, (0, 0))
        background_surface = pygame.Surface((750,750))
        background_surface.fill((255,252,240))
        self.poleGry = background_surface
        self.rysuj_plansze(background_surface)
        self.display.blit(background_surface, (280, 0))

    def rysuj_plansze(self, surface):
        for row in range(0, 5):
            for col in range(0, 5):
                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(row * 150, col * 150, 150, 150), 1)
                if(self.stan_pola[row][col][0] == 1):
                    self.floor1 = pygame.transform.scale(self.floor1, (150, 150))
                    surface.blit(self.floor1, (row * 150, col * 150))
                if(self.stan_pola[row][col][0] == 2):
                    self.floor2 = pygame.transform.scale(self.floor2, (150, 150))
                    surface.blit(self.floor2, (row * 150, col * 150))
                if(self.stan_pola[row][col][0] == 3):
                    self.floor3 = pygame.transform.scale(self.floor3, (150, 150))
                    surface.blit(self.floor3, (row * 150, col * 150))
                if(self.stan_pola[row][col][0] == 4):
                    self.floor4 = pygame.transform.scale(self.floor4, (150, 150))
                    surface.blit(self.floor4, (row * 150, col * 150))
                if(self.stan_pola[row][col][1] in self.gracze[0].Pionki):
                    self.pionek1 = pygame.transform.scale(self.pionek1, (150, 150))
                    surface.blit(self.pionek1, (row * 150, col * 150))
                if(self.stan_pola[row][col][1] in self.gracze[1].Pionki):
                    self.pionek2 = pygame.transform.scale(self.pionek2, (150, 150))
                    surface.blit(self.pionek2, (row * 150, col * 150))




