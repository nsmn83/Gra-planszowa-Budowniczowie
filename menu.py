import pygame

import game


class Menu():
    def __init__(self, game):
        self.instrukcja_rect = None
        self.opcje_rect = None
        self.start_rect = None
        self.game = game
        self.run_display = True
        self.img = pygame.image.load("Pictures/background.jpg")

    def blit_screen(self):
        self.game.display.blit(self.img, (0,0))
        self.draw_menu_background()
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()

    def draw_menu_background(self):
        background_surface = pygame.Surface((720,720))
        background_surface.fill((0,0,0))
        background_surface.set_alpha(200)
        self.game.display.blit(background_surface, (280, 0))
        self.game.draw_text('SANTORINI', 150, self.game.width / 2, 170)
        self.start_rect = self.game.draw_text('START', 100, self.game.width / 2, 270)
        self.opcje_rect = self.game.draw_text('OPCJE', 100, self.game.width / 2, 370)
        self.instrukcja_rect = self.game.draw_text('INSTRUKCJA', 100, self.game.width / 2, 470)




class MainMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_choice()
            self.game.display.fill((0,0,0))
            self.blit_screen()

    def check_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if self.opcje_rect.collidepoint(x,y):
                    self.game.curr_menu = Options(self.game)
                    self.run_display = False
                elif self.instrukcja_rect.collidepoint(x,y):
                    self.game.curr_menu = Instruction(self.game)
                    self.run_display = False
                elif self.start_rect.collidepoint(x,y):
                    self.game.playing = True
                    self.run_display = False
                    self.game.curr_menu = None
        pygame.display.flip()

class Instruction(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        self.powrot_rect = None


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_choice()
            self.game.display.fill((0,0,0))
            self.blit_screen()

    def blit_screen(self):
        self.game.display.blit(self.img, (0,0))
        self.draw_menu_background()
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()

    def check_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.powrot_rect.collidepoint(x, y):
                    self.game.curr_menu = MainMenu(self.game)
                    self.run_display = False

    def draw_menu_background(self):
        background_surface = pygame.Surface((720,720))
        background_surface.fill((0,0,0))
        background_surface.set_alpha(200)

        self.game.display.blit(background_surface, (280, 0))

        text = "ZASADY GRY"
        self.game.draw_text(text, 100, self.game.width / 2, 170)
        self.powrot_rect = self.game.draw_text('POWRÓT', 100, self.game.width / 2, 470)


class Options(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_choice()
            self.game.display.fill((0,0,0))
            self.blit_screen()

    def blit_screen(self):
        self.game.display.blit(self.img, (0,0))
        self.draw_menu_background()
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()

    def check_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.powrot_rect.collidepoint(x, y):
                    self.game.curr_menu = MainMenu(self.game)
                    self.run_display = False

    def draw_menu_background(self):
        background_surface = pygame.Surface((720,720))
        background_surface.fill((0,0,0))
        background_surface.set_alpha(200)

        self.game.display.blit(background_surface, (280, 0))

        text = "OPCJE"
        self.game.draw_text(text, 100, self.game.width / 2, 170)
        self.powrot_rect = self.game.draw_text('POWRÓT', 100, self.game.width / 2, 470)
