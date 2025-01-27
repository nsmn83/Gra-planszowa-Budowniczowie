import pygame
from menu import Menu
from gameLogic import gameLogic
from turn import Turn

#klasa wyswietlajaca rozgrywke lub ustawione menu
class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        #Parametry gry
        self.running = True
        self.playing = False
        self.width = 1280
        self.height = 750
        self.board_width = 750
        self.board_height = 750
        self.display = pygame.display.set_mode((self.width, self.height))
        self.board_display = pygame.Surface((self.board_width, self.board_height))

        #Utworzenie menu głównego wyswietlanego na poczatku gry
        self.menu = Menu(self)

        #Elementy - dzwieki, obrazki, czcionki uzywane w oknie gry
        self.font_name = 'Fonts/8-bit Arcade In.ttf'
        self.sound = pygame.mixer.Sound('Pictures/move.wav')
        self.background = pygame.transform.scale(pygame.image.load("Pictures/background.jpg"), (1280, 750))
        self.board_background = pygame.transform.scale(pygame.image.load("Pictures/background5.png"), (1280, 750))
        self.gameLogic = gameLogic()

    #Zmiana pozycji z pikesli na indeks pola
    def convertToCords(self, pos):
        x, y = pos
        x -= 280 # Przesunięcie pola gry względem okna
        return int(x/150), int(y/150)

    #Petla gry
    def game_loop(self):
        while self.playing:
            self.handleClick()
            self.display.fill((0,0,0))
            if self.gameLogic.turn == Turn.ENDOFGAME:
                self.showWinner()
            else:
                self.draw()

    #Rysowanie tego co sie dzieje na planszy
    def draw(self):
        self.display.blit(self.background, (0, 0))
        self.board_display.blit(self.board_background, (0, 0))
        self.gameLogic.drawGameState(self.board_display)
        self.display.blit(self.board_display, (280, 0))

        #


    #funkcja oblsugujaca klikniecia na ekranie gry
    def handleClick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.board_display.get_rect(topleft=(280, 0)).collidepoint(event.pos):
                    self.sound.play()
                    # Wywołanie funkcji klasy gameLogic obsługującej logikę gry
                    x, y = self.convertToCords(event.pos)
                    if 0 <= x <= 4 and 0 <= y <= 4:
                        self.gameLogic.handleActions(x, y)

        pygame.display.flip()


    #funkcja rysujaca tekst na ekranie
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        return text_rect

    def showWinner(self):
        winner_text = f"Gracz {self.gameLogic.activePlayer.id} wygrał grę"
        self.gameLogic.activePlayer.pieces[0].drawPieceSpecial(self.display, 0, 200)
        self.draw_text(winner_text, 50, self.width // 2, self.height // 2)
        self.running = False
        pygame.display.flip()



