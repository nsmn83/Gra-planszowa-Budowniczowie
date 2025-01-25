import pygame
from button import Button



class Menu():
    def __init__(self,game):
        self.game = game
        self.background = pygame.image.load('Pictures/background.jpg')
        self.start_button = Button('START', self.game.width / 2, 270, self.game.display)
        self.two_player_button = Button('2 GRACZY', self.game.width / 2, 470, self.game.display)
        self.three_player_button = Button('3 GRACZY', self.game.width / 2, 670, self.game.display)

    def check_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if self.start_button.rect.collidepoint(x, y):
                    print("Wciśnięto START")
                    #stworzenie graczy w zaleznosci od ich liczby
                    self.game.gameLogic.addPlayers()
                    self.game.menu = None
                    self.run_display = False
                    self.game.playing = True
                if self.two_player_button.rect.collidepoint(x, y):
                    print("Zmieniono liczbę graczy na 2")
                    self.game.gameLogic.setNumOfPlayers(2)
                if self.three_player_button.rect.collidepoint(x, y):
                    print("Zmieniono liczbę graczy na 3")
                    self.game.gameLogic.setNumOfPlayers(3)
        pygame.display.flip()

    def draw_menu_background(self):
        background_surface = pygame.Surface((750, 750))
        background_surface.fill((0, 0, 0))
        background_surface.set_alpha(200)
        self.game.display.blit(background_surface, (280, 0))
        self.start_button.draw()
        self.two_player_button.draw()
        self.three_player_button.draw()
        self.game.draw_text('SANTORINI', 150, self.game.width / 2, 70)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_choice()
            self.game.display.fill((0,0,0))
            self.game.display.blit(self.background, (0, 0))
            self.draw_menu_background()