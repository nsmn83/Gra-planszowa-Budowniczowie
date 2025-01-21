import pygame
from game import Game
from menu import MainMenu

game = Game()


while game.running:
    game.curr_menu.display_menu()
    game.game_loop()