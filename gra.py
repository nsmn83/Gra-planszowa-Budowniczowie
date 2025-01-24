import pygame
from menu import MainMenu
from stanGry import stanGry, Tura


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
        self.img = pygame.image.load("Pictures/background.jpg")
        self.stanGry = stanGry()

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


    def blit_screen(self):
        self.draw_menu_background()
        self.window.blit(self.display, (0,0))
        pygame.display.update()


    #funkcja obsluguje ogolny przebieg tury, naprzemian ofiaruje graczom wybor pionka a nastepnie wywoluje ture pionka
    def check_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = self.ktore_pole(event.pos)
                #jesli pionek nie jest wybrany nastepuje wybor pionka przez aktualnego gracza
                if self.stanGry.aktualnyPionek is None:
                    #obliczenie pola planszy na podstawie wcisnietego kwadratu
                    self.stanGry.aktualnyPionek = self.sprawdzPoprawnoscWyboru(x,y)
                    if self.stanGry.aktualnyPionek:
                        print("Sprawdzenie ruchow wybranego pionka")
                        self.stanGry.aktualnyPionek.sprawdzRuchy(self.stanGry)  # Check for valid moves
                        self.draw_menu_background()
                        self.window.blit(self.display, (0, 0))
                        pygame.display.update()
                        self.blit_screen()
                        if(self.stanGry.tura == Tura.RUCH):
                            print("Tura Ruch 1")
                elif self.stanGry.tura == Tura.RUCH:
                    print("Tura ruch")
                    self.stanGry.aktualnyPionek.wykonajRuch(x,y,self.stanGry)
                elif self.stanGry.tura == Tura.BUDUJ:
                    self.stanGry.aktualnyPionek.zbudujPietro(x,y,self.stanGry)
                elif self.stanGry.tura == Tura.KONIEC:
                    self.stanGry.aktualnyPionek = None
                    self.stanGry.aktualnyGracz = self.stanGry.zmienGracza()
                    self.stanGry.tura = Tura.RUCH
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        return text_rect

    def sprawdzPoprawnoscWyboru(self, x, y):
        pionek = self.stanGry.zwrocPionka(x, y)
        if pionek:
            print(f"Gracz wybrał pionka o x = {x} i y = {y}")
            return pionek
        return None

    def draw_menu_background(self):
        self.display.blit(self.img, (0, 0))
        background_surface = pygame.Surface((750,750))
        background_surface.fill((255,252,240))
        self.poleGry = background_surface
        self.stanGry.rysujStanGry(background_surface)
        self.stanGry.rysujRuchy(background_surface)
        self.display.blit(background_surface, (280, 0))





