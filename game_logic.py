import pygame
from player import Player
from piece import Piece
from turn import Turn
from tile import Tile


class gameLogic:
    def __init__(self):
        pygame.init()
        self.turn = Turn.SETUP
        self.active_player = None
        self.chosen_piece = None
        self.num_of_players = 2
        self.players = []
        self.possible_moves = []
        self.possible_building_sites = []
        self.board = [[Tile() for _ in range(5)] for _ in range(5)]

        #Budowle
        self.images = [
            pygame.transform.scale(pygame.image.load("Assets/floor1.png"), (150, 150)),
            pygame.transform.scale(pygame.image.load("Assets/floor2.png"), (150, 150)),
            pygame.transform.scale(pygame.image.load("Assets/floor3.png"), (150, 150)),
            pygame.transform.scale(pygame.image.load("Assets/floor4.png"), (150, 150))
        ]

    # Dodanie graczy
    def add_players(self):
        for element in range(self.num_of_players):
            img = f"Assets/player{element + 1}.png"
            img = pygame.image.load(img)
            player = Player(img, element)
            self.players.append(player)
        self.active_player = self.players[0]

    # Zmiana liczby graczy biorących udzaił w rozgrywce
    def set_num_of_players(self, num: int) -> None:
        self.num_of_players = num

    # Funkcja do zmiany aktualnego gracza na nastepnego
    def switch_player(self):
        if self.chosen_piece:
            self.chosen_piece.moved = False
        self.active_player = self.players[(self.players.index(self.active_player) + 1) % len(self.players)]
        self.check_if_blocked()
        return self.active_player

    # Pętla oblsugujaca tury graczy
    def handle_actions(self, x: int, y: int):
        # Pierwsza faza gry - rozstawiamy pionki dopoki kazdy nie bedzie mial ich na planszy
        if self.turn == Turn.SETUP:
            self.setup(x, y)
            return

        # Jesli pionek nie jest wybrany, aktywny gracz wybiera swojego pionka
        if self.chosen_piece is None:
            self.chosen_piece = self.return_piece(x, y)

        elif self.chosen_piece is not None and not self.chosen_piece.moved:
            if self.board[x][y].return_piece() and self.board[x][y].piece.owner == self.active_player:
                self.chosen_piece = self.board[x][y].return_piece()
                self.possible_moves = []
                self.turn = Turn.CHECKMOVE

        if self.chosen_piece:
            if self.turn == Turn.BUILD:
                self.perform_build(x, y)

            elif self.turn == Turn.MOVE:
                self.perform_move(x, y)

            if self.chosen_piece and self.turn == Turn.CHECKMOVE:
                self.check_moves(self.chosen_piece)

            if self.turn == Turn.CHECKBUILD:
                self.check_build()

            if self.turn == Turn.ENDOFTURN:
                self.chosen_piece.moved = False
                self.chosen_piece = None
                self.active_player = self.switch_player()
                self.turn = Turn.CHECKMOVE

            self.check_win_conditions()

    # Funkcja służąca ustawieniu pionktów na początku rozgrywki
    def setup(self, x: int, y: int):
        if self.board[x][y].is_blocked():
            return
        for piece in self.active_player.pieces:
            if not piece.return_piece_position():
                self.change_position(x, y, piece)
                if self.active_player.pieces[1] == piece:
                    self.active_player.pieces_set = True
                    self.switch_player()
                    if self.active_player.pieces_set:
                        self.turn = Turn.CHECKMOVE
                return

    # Sprawdzenie mozliwych pol do wykonania ruchu
    def check_moves(self, piece: Piece):
        pos = piece.return_piece_position()
        if pos is None:
            return
        if self.active_player.ability.check_moves(self, piece, pos):
            return
        x, y = pos
        valid = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        self.board[pos[0]][pos[1]].height < self.board[x][y].height + 2 and
                        self.board[pos[0]][pos[1]].piece is None,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        self.possible_moves.extend(valid)
        self.turn = Turn.MOVE

    # Sprawdzenie mozliwych pol do wykonania budowy
    def check_build(self):
        x, y = self.chosen_piece.return_piece_position()
        valid = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        self.board[pos[0]][pos[1]].height < 4 and
                        self.board[pos[0]][pos[1]].piece is None,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        self.possible_building_sites.extend(valid)

        # Jesli nie mozesz wykonac budowy w swojej turze odpadasz z gry
        if not self.possible_building_sites:
            self.delete_loser()
            self.chosen_piece = None
            self.turn = Turn.CHECKMOVE
            return

        self.turn = Turn.BUILD

    # Zmiana pozycji poprzec zmiane koordynatow pionka i przypisaniu go odpowiedniemu polu planszy
    def change_position(self, x: int, y: int, piece: Piece):
        if piece.return_piece_position():
            self.board[piece.x][piece.y].delete_piece()
        piece.change_piece_position(x, y)
        self.board[x][y].piece = piece

    # Wykonanie ruchu
    def perform_move(self, x: int, y: int):
        if self.active_player.ability.perform_move(self, self.chosen_piece, x, y):
            return
        if (x, y) in self.possible_moves:
            xs, ys = self.chosen_piece.return_piece_position()
            self.board[xs][ys].piece = None
            self.chosen_piece.change_piece_position(x, y)
            self.chosen_piece.moved = True
            self.board[x][y].piece = self.chosen_piece
            self.possible_moves = []
            self.check_win_conditions()
            if self.turn != Turn.ENDOFGAME:
                self.turn = Turn.CHECKBUILD

    # Budowanie
    def perform_build(self, x: int, y: int):
        if self.active_player.ability.perform_build(self, self.chosen_piece, x, y):
            return
        elif (x, y) in self.possible_building_sites:
            self.board[x][y].height += 1
            self.possible_building_sites = []
            self.turn = Turn.ENDOFTURN
            self.chosen_piece.moved = False

    # Sprawdzenie czy czy gracz w swoim ruchu wszedl na 3 pietro lub czy pozostali odpadli
    def check_win_conditions(self):
        if self.active_player.ability.check_win_condition(self) or self.chosen_piece and self.chosen_piece.moved and \
                self.board[self.chosen_piece.x][
                    self.chosen_piece.y].height == 3 or len(self.players) == 1:
            self.turn = Turn.ENDOFGAME

    # Na początku tury gracz sprawdza, czy moze wykonac ruch, jesli nie, to jest usuwany z gry
    def check_if_blocked(self):

        if not self.active_player.pieces_set:
            return False
        for piece in self.active_player.pieces:
            self.check_moves(piece)
        if self.possible_moves:
            self.possible_moves = []
            return False
        self.delete_loser()

    # Funkcja zwracajaca pionka jesli
    def return_piece(self, x: int, y: int):
        if self.active_player is None:
            return None
        if self.board[x][y].piece and self.board[x][y].piece.owner == self.active_player:
            return self.board[x][y].piece
        return None

    # Usuniecie gracza z rozgrywki
    def delete_loser(self):
        loser = self.active_player
        for piece in loser.pieces:
            x, y = piece.return_piece_position()
            self.board[x][y].delete_piece()
        self.active_player = self.players[(self.players.index(self.active_player) + 1) % len(self.players)]
        self.players.remove(loser)
        return True

    # Funkcja rysujaca plansze, pionki i mozliwe ruchy
    def draw_game_state(self, surface: pygame.surface):
        self.draw_board(surface)
        self.draw_pieces(surface)
        self.draw_moves(surface)

    def draw_board(self, surface: pygame.surface):
        for row in range(0, 5):
            for col in range(0, 5):
                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(row * 150, col * 150, 150, 150), 1)
                height = self.board[row][col].height
                if 1 <= height <= 4:
                    surface.blit(self.images[height - 1], (row * 150, col * 150))

    def draw_moves(self, surface: pygame.surface):
        for (x, y) in self.possible_moves:
            pygame.draw.circle(surface, (0, 255, 0, 255), (x * 150 + 75, y * 150 + 75), radius=74, width=5)

        for (x, y) in self.possible_building_sites:
            color = (255, 255, 0, 255)
            if self.chosen_piece.build:
                color = (0, 0, 255, 255)
            pygame.draw.circle(surface, color, (x * 150 + 75, y * 150 + 75), radius=74, width=5)

    def draw_pieces(self, surface: pygame.surface):
        for player in self.players:
            for piece in player.pieces:
                if piece.return_piece_position():
                    x = piece.x * 150
                    y = piece.y * 150
                    piece.draw_piece(surface)
                    if player == self.active_player and self.chosen_piece is None and self.turn != Turn.SETUP:
                        pygame.draw.circle(surface, (255, 255, 255), (x + 75, y + 75), 74, width=5)
