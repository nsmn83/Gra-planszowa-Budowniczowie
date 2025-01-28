import pygame
from button import Button
from ability import Ability, Artemis, Apollo, Atlas, Demeter, Hefajstos, Minotaur, Hermes, Faun
from menuState import MenuState



class Menu():
    def __init__(self,game):

        #Przyciski dotyczace menu wyboru liczby graczy
        self.game = game
        self.background = pygame.transform.scale(pygame.image.load("Assets/background.jpg"), (1280, 750))
        self.start_button = Button('START', self.game.width / 2, 270, self.game.display)
        self.two_player_button = Button('2 GRACZY', self.game.width / 2, 400, self.game.display)
        self.three_player_button = Button('3 GRACZY', self.game.width / 2, 530, self.game.display)
        self.state = MenuState.PLAYERMENU
        self.sound = pygame.mixer.Sound("Assets/move.wav")

        #Przyciski dotyczace ekranu wyboru mocu
        self.AbilityArray = [Ability(), Artemis(), Apollo(), Atlas(), Demeter(), Hefajstos(), Minotaur(), Hermes(), Faun()]
        self.start_game_button = Button('START', self.game.width / 2, 270, self.game.display)
        self.power_buttons = []
        self.power_indexes = []

    #Obsluga tego co dzieje sie w menu
    def check_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sound.play()
                x,y = event.pos
                if self.state == MenuState.PLAYERMENU:
                    self.PlayerMenuHandler(x, y)
                elif self.state == MenuState.POWERMENU:
                    self.powerMenuHandler(x, y)
        pygame.display.flip()

    #Oblsuga menu startowego - zmiana liczby graczy
    def PlayerMenuHandler(self, x, y):
        if self.start_button.rect.collidepoint(x, y):

            #Utworzenie graczy bioracych udzial w rozgrywce
            self.game.gameLogic.addPlayers()

            #Tablica przechowuje indeksy mocy
            self.power_indexes = [0 for _ in range(self.game.gameLogic.numberOfPlayers)]

            #Utworzenie przyciskow do wybrania mocy przez graczy, przejscie do menu wyboru mocy
            self.createPowerButtons()
            self.state = MenuState.POWERMENU

        #Zmiana liczby graczy
        if self.two_player_button.rect.collidepoint(x, y):
            self.game.gameLogic.setNumOfPlayers(2)

        #Zmiana liczby graczy
        if self.three_player_button.rect.collidepoint(x, y):
            self.game.gameLogic.setNumOfPlayers(3)

    #Obsluga klikniec w menu wyboru mocy
    def powerMenuHandler(self, x, y):

        #Rozpoczecie gry
        if self.start_game_button.rect.collidepoint(x, y):
            for index, player in enumerate(self.game.gameLogic.players):
                power = self.AbilityArray[self.power_indexes[index]]
                player.assingPower(power)
            self.startGame()
            self.power_buttons = []
            self.power_indexes = []

        #Zmiana mocy przez gracza
        for index, button in enumerate(self.power_buttons):
            if button.rect.collidepoint(x, y):
                self.power_indexes[index] = (self.power_indexes[index] + 1) % len(self.AbilityArray)
                power = self.AbilityArray[self.power_indexes[index]]
                button.text = f"GRACZ {index + 1} MOC {power.name}"


    #Utworzenie przyciskow do wyboru mocy
    def createPowerButtons(self):
        offset = 130
        for player in range(self.game.gameLogic.numberOfPlayers):
            button_text = f"GRACZ {player + 1} BRAK MOCY"
            button = Button(button_text, self.game.width / 2, 270 + (player+1) * offset, self.game.display, 50)
            self.power_buttons.append(button)

    #Rozpoczecie gry - wylaczenie menu, wyswietlania menu, wlaczenie petli gry
    def startGame(self):
        self.run_display = False
        self.game.playing = True

    #Rysowanie menu
    def draw_menu_background(self):
        background_surface = pygame.Surface((750, 750))
        background_surface.fill((0, 0, 0))
        background_surface.set_alpha(200)
        self.game.display.blit(background_surface, (280, 0))
        if self.state == MenuState.PLAYERMENU:
            self.start_button.draw()
            self.two_player_button.draw()
            self.three_player_button.draw()
            self.game.draw_text('SANTORINI', 150, self.game.width / 2, 70)
        elif self.state == MenuState.POWERMENU:
            self.start_game_button.draw()
            for button in self.power_buttons:
                button.draw()


    #Odswiezanie menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_choice()
            self.game.display.fill((0,0,0))
            self.game.display.blit(self.background, (0, 0))
            self.draw_menu_background()