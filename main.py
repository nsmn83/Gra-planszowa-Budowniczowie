import pygame
from gameScreen import Game

game = Game()

while game.running:
    game.menu.display_menu()
    game.game_loop()
