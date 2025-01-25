import pygame
pygame.font.init()

font = pygame.font.Font('Fonts/8-bit Arcade In.ttf', 80)

class Button():
    def __init__(self, text, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.width = 400
        self.height = 100
        self.button_text = font.render(text, True, 'white')
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)

    # Rysowanie przycisku
    def draw(self):
        color = 'light gray' if self.clicked() else 'black'
        pygame.draw.rect(self.screen, color, self.rect, 0, 5)
        pygame.draw.rect(self.screen, 'black', self.rect, 2, 5)

        # Ustawienie tekstu na srodku przycisku
        text_rect = self.button_text.get_rect(center=(self.x, self.y))
        self.screen.blit(self.button_text, text_rect)

    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        return left_click and self.rect.collidepoint(mouse_pos)



