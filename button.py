import pygame
pygame.font.init()

class Button():
    def __init__(self, text: str, x: int, y: int, screen, font_size: int = 80):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.width = 600
        self.height = 100
        self.button_offset = 100
        self.font_size = font_size
        self.font = pygame.font.Font('Fonts/8-bit Arcade In.ttf', font_size)
        self.button_text = self.font.render(self.text, True, 'white')
        self.rect = pygame.Rect(self.x, self.y, self.width + self.button_offset, self.height)
        self.rect.center = (self.x, self.y)

    # Rysowanie przycisku
    def draw(self):
        self.button_text = self.font.render(self.text, True, 'white')
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



