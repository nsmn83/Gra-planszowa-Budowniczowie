import pygame
from menu import Menu
from gameLogic import gameLogic
from turn import Turn
from menuState import MenuState

#Klasa wyswietlajaca rozgrywke lub ustawione menu
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
        self.inProgress = True

        #Utworzenie menu głównego wyswietlanego na poczatku gry
        self.menu = Menu(self)

        #Elementy - dzwieki, obrazki, czcionki uzywane w oknie gry
        self.font_name = 'Fonts/8-bit Arcade In.ttf'
        self.sound = pygame.mixer.Sound('Assets/move.wav')
        self.background = pygame.transform.scale(pygame.image.load("Assets/background.jpg"), (1280, 750))
        self.board_background = pygame.transform.scale(pygame.image.load("Assets/background5.png"), (1280, 750))
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
            self.draw()


    #Funkcja oblsugujaca klikniecia na ekranie gry
    def handleClick(self):
        if not self.inProgress:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.gameLogic.turn == Turn.ENDOFGAME:
                    self.comeBackToMenu()
                elif self.board_display.get_rect(topleft=(280, 0)).collidepoint(event.pos):
                    self.sound.play()
                    # Wywołanie funkcji klasy gameLogic obsługującej logikę gry
                    x, y = self.convertToCords(event.pos)
                    if 0 <= x <= 4 and 0 <= y <= 4:
                        self.gameLogic.handleActions(x, y)
        pygame.display.flip()


    #Funkcja rysujaca tekst na ekranie
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        return text_rect

    #Wypisanie zwycięzcy na ekran
    def showWinner(self):
        winner_text = f"Gracz {self.gameLogic.activePlayer.id + 1} wygrał grę"
        player_head_image = pygame.image.load(f'Assets/player{self.gameLogic.activePlayer.id + 1}_head.png')
        player_head_image = pygame.transform.scale(player_head_image, (500, 500))
        self.display.fill((0, 0, 0))
        self.display.blit(player_head_image, (self.width // 2 - player_head_image.get_width() // 2, 0))
        self.draw_text(winner_text, 100, self.width // 2, self.height // 2 + 150)
        pygame.display.flip()

    #Rysowanie kwadratu z informacją odnośnie aktywnego Gracza
    def drawPlayerInfo(self):
        square_x = 20
        square_y = 20
        square_width = 250
        square_height = 550
        pygame.draw.rect(self.display, (0, 0, 0), (square_x, square_y, square_width, square_height))
        player_head_image = pygame.image.load(f'Assets/player{self.gameLogic.activePlayer.id + 1}_head.png')
        player_head_image = pygame.transform.scale(player_head_image, (250, 250))
        self.display.blit(player_head_image, (square_x, square_y))

        player_info_text = f"Gracz {self.gameLogic.activePlayer.id + 1}"
        self.draw_text(player_info_text, 50, square_x + 125, square_y + 250)
        player_power_text = f"Moc {self.gameLogic.activePlayer.ability.name}"
        self.draw_text(player_power_text, 30, square_x + 125, square_y + 300)
        player_instruction = self.gameLogic.activePlayer.ability.rule
        self.display.blit(player_instruction, (50, 350))

    #Rysowanie tego co sie dzieje na planszy
    def draw(self):
        if self.gameLogic.turn == Turn.ENDOFGAME:
            self.showWinner()
            return
        self.display.blit(self.background, (0, 0))
        self.board_display.blit(self.board_background, (0, 0))
        self.gameLogic.drawGameState(self.board_display)
        self.display.blit(self.board_display, (280, 0))
        self.drawPlayerInfo()

    #Reset stanu gry i przejscie do menu głównego
    def comeBackToMenu(self):
        self.playing = False
        self.menu.state = MenuState.PLAYERMENU
        self.gameLogic = gameLogic()
        self.menu.display_menu()