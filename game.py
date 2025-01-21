import pygame
from menu import MainMenu, Options, Instruction

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.width = 1280
        self.height = 720
        self.display = pygame.display.set_mode((self.width, self.height))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font_name = 'Fonts/8-bit Arcade In.ttf'
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_action()
            self.display.fill((0,0,0))
            self.draw_menu_background()
            self.window.blit(self.display, (0,0))
            pygame.display.update()

    def check_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        return text_rect

    def draw_menu_background(self):
        background_surface = pygame.Surface((720,720))
        background_surface.fill((255,0,255))
        background_surface.set_alpha(200)

        self.display.blit(background_surface, (280, 0))
