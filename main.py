from game_screen import Game

game = Game()

while game.running:
    game.menu.display_menu()
    game.game_loop()
