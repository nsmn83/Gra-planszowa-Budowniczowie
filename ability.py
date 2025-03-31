from turn import Turn
import pygame


# Klasa Ability, bazowo kazda funkcja zwraca fałsz, klasy poszczegolnych bóstw zmieniaja dane funkcje, jesli
# moc tego wymaga (np. Artemis po pierwszym ruchu ma mozliwosc wykonania drugiego przed koncem tury)
class Ability:
    def __init__(self):
        self.name = "BRAK"
        self.rule = pygame.image.load("Assets/basic_opis.jpg")

    # Jesli dana moc nie zmienia ruchu, budowania itp, to zwroci False
    def check_moves(self, game_logic, piece, pos: tuple):
        return False

    def perform_move(self, game_logic, piece, x: int, y: int):
        return False

    def check_win_condition(self, game_logic):
        return False

    def perform_build(self, game_logic, piece, x: int, y: int):
        return False


class Artemis(Ability):
    def __init__(self):
        super().__init__()
        self.name = "ARTEMIS"
        self.rule = pygame.image.load("Assets/artemis_opis.jpg")

    #Wykonanie ruchu ze sprawdzeniem czy jest to pierwszy czy drugi ruch
    def perform_move(self, game_logic, piece, x: int, y: int):

        if (x, y) in game_logic.possible_moves:
            xs, ys = game_logic.chosen_piece.return_piece_position()
            game_logic.board[xs][ys].delete_piece()
            game_logic.chosen_piece.change_piece_position(x, y)
            game_logic.board[x][y].piece = game_logic.chosen_piece
            game_logic.check_win_conditions()
            game_logic.possible_moves = []
            if not game_logic.chosen_piece.moved:
                game_logic.chosen_piece.moved = True
                game_logic.turn = Turn.CHECKMOVE
            else:
                game_logic.check_win_conditions()
                if game_logic.turn != Turn.ENDOFGAME:
                    game_logic.turn = Turn.CHECKBUILD
        elif game_logic.chosen_piece.moved:
            game_logic.check_win_conditions()
            if game_logic.turn != Turn.ENDOFGAME:
                game_logic.turn = Turn.CHECKBUILD

    def check_moves(self, game_logic, piece, pos: tuple):
        x, y = pos
        valid = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        game_logic.board[pos[0]][pos[1]].height < game_logic.board[x][y].height + 2 and
                        game_logic.board[pos[0]][pos[1]].piece is None,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        game_logic.possible_moves.extend(valid)
        prev_position = (piece.prev_x, piece.prev_y)
        if prev_position in game_logic.possible_moves and piece.moved:
            game_logic.possible_moves.remove(prev_position)

        # Jesli gracz sprawdza czy moze wykonac drugi ruch, lecz nie ma na niego miejsca to przechodzi do budowania
        if not game_logic.possible_moves and piece.moved:
            game_logic.turn = Turn.CHECKBUILD
            return True
        game_logic.turn = Turn.MOVE
        return True


class Apollo(Ability):
    def __init__(self):
        super().__init__()
        self.name = "APOLLO"
        self.rule = pygame.image.load("Assets/apollo_opis.jpg")

    def check_moves(self, game_logic, piece, pos: tuple):
        x, y = pos
        valid = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        game_logic.board[pos[0]][pos[1]].height < game_logic.board[x][y].height + 2 and
                        (game_logic.board[pos[0]][pos[1]].piece is None or game_logic.board[pos[0]][
                            pos[1]].piece.owner != game_logic.active_player),
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        game_logic.possible_moves.extend(valid)
        game_logic.turn = Turn.MOVE
        return True

    def perform_move(self, game_logic, piece, x: int, y: int):
        if (x, y) in game_logic.possible_moves:
            enemy_piece = None
            xs, ys = game_logic.chosen_piece.return_piece_position()
            if game_logic.board[x][y].piece and game_logic.board[x][y].piece != game_logic.active_player:
                enemy_piece = game_logic.board[x][y].piece
                enemy_piece.change_piece_position(xs, ys)
            game_logic.board[xs][ys].piece = enemy_piece
            game_logic.chosen_piece.change_piece_position(x, y)
            game_logic.board[x][y].piece = game_logic.chosen_piece
            game_logic.chosen_piece.moved = True
            game_logic.check_win_conditions()
            game_logic.possible_moves = []
            if game_logic.turn != Turn.ENDOFGAME:
                game_logic.possible_moves = []
                game_logic.turn = Turn.CHECKBUILD


class Atlas(Ability):
    def __init__(self):
        super().__init__()
        self.name = "ATLAS"
        self.rule = pygame.image.load("Assets/atlas_opis.jpg")

    def perform_build(self, game_logic, piece, x: int, y: int):
        if (x, y) in game_logic.possible_building_sites and piece.build is False:
            game_logic.board[x][y].height += 1
            game_logic.possible_building_sites = []
            game_logic.turn = Turn.ENDOFTURN
            piece.build = False
            piece.moved = False
        elif piece.build:
            if (x, y) in game_logic.possible_building_sites:
                game_logic.board[x][y].height = 4
                game_logic.possible_building_sites = []
                game_logic.turn = Turn.ENDOFTURN
                piece.build = False
                piece.moved = False
        else:
            piece.build = True


class Demeter(Ability):
    def __init__(self):
        super().__init__()
        self.name = "DEMETER"
        self.rule = pygame.image.load("Assets/demeter_opis.jpg")

    def perform_build(self, game_logic, piece, x: int, y: int):
        if (x, y) in game_logic.possible_building_sites and not piece.build:
            game_logic.board[x][y].height += 1
            piece.build = True
            game_logic.possible_building_sites.remove((x, y))
        elif piece.build:
            if (x, y) in game_logic.possible_building_sites:
                game_logic.board[x][y].height += 1
            game_logic.possible_building_sites = []
            piece.build = False
            game_logic.turn = Turn.ENDOFTURN
            game_logic.chosen_piece.moved = False


class Hefajstos(Ability):
    def __init__(self):
        super().__init__()
        self.name = "HEFAJSTOS"
        self.rule = pygame.image.load("Assets/hefajstos_opis.jpg")

    def perform_build(self, game_logic, piece, x: int, y: int):
        if (x, y) in game_logic.possible_building_sites and not piece.build:
            game_logic.board[x][y].height += 1
            piece.build = True
            game_logic.possible_building_sites = [(x, y)]
            if game_logic.board[x][y].height >= 3:
                piece.build = False
                game_logic.turn = Turn.ENDOFTURN
                game_logic.chosen_piece.moved = False
                game_logic.possible_building_sites = []
        elif piece.build:
            if (x, y) in game_logic.possible_building_sites:
                game_logic.board[x][y].height += 1
            game_logic.possible_building_sites = []
            piece.build = False
            game_logic.turn = Turn.ENDOFTURN
            game_logic.chosen_piece.moved = False
        return True


class Minotaur(Ability):
    def __init__(self):
        super().__init__()
        self.name = "MINOTAUR"
        self.rule = pygame.image.load("Assets/minotaur_opis.jpg")

    def check_moves(self, game_logic, piece, pos: tuple):
        x, y = pos
        valid = []
        change = [-1, 0, 1]
        for dx in change:
            for dy in change:
                if dx == 0 and dy == 0:
                    continue
                temp_x, temp_y = x + dx, y + dy

                if 0 <= temp_x <= 4 and 0 <= temp_y <= 4:
                    tile = game_logic.board[temp_x][temp_y]
                    if game_logic.board[temp_x][temp_y].height <= game_logic.board[x][y].height + 1:
                        if not tile.piece:
                            valid.append((temp_x, temp_y))
                        elif tile.piece.owner != game_logic.active_player:
                            behindX, behindY = temp_x + dx, temp_y + dy
                            if 0 <= behindY <= 4 and 0 <= behindX <= 4:
                                secondTile = game_logic.board[behindX][behindY]
                                if secondTile.piece is None and secondTile.height < 4:
                                    valid.append((temp_x, temp_y))

        game_logic.possible_moves.extend(valid)
        game_logic.turn = Turn.MOVE
        return True

    def perform_move(self, game_logic, piece, x: int, y: int):
        if (x, y) in game_logic.possible_moves:
            enemy_piece = None
            xs, ys = game_logic.chosen_piece.return_piece_position()
            game_logic.board[xs][ys].delete_piece()
            dx, dy = x - xs, y - ys
            if game_logic.board[x][y].piece:
                enemy_piece = game_logic.board[x][y].piece
                enemy_piece.change_piece_position(x + dx, y + dy)
                game_logic.board[x + dx][y + dy].piece = enemy_piece
            game_logic.chosen_piece.change_piece_position(x, y)
            game_logic.board[x][y].piece = game_logic.chosen_piece
            game_logic.chosen_piece.moved = True
            game_logic.check_win_conditions()
            game_logic.possible_moves = []
            if game_logic.turn != Turn.ENDOFGAME:
                game_logic.possible_moves = []
                game_logic.turn = Turn.CHECKBUILD

class Hermes(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Hermes"
        self.rule = pygame.image.load("Assets/hermes_opis.jpg")

    def check_moves(self, game_logic, piece, pos: tuple):
        x, y = pos
        valid = []
        change = [1, 0, -1]
        height = game_logic.board[x][y].height
        for dx in change:
            for dy in change:
                temp_x, temp_y = x + dx, y + dy
                if dx == 0 and dy == 0:
                    continue
                while 0 <= temp_x <= 4 and 0 <= temp_y <= 4:
                    if game_logic.board[temp_x][temp_y].height != height or game_logic.board[temp_x][temp_y].piece:
                        break
                    valid.append((temp_x, temp_y))
                    temp_x += dx
                    temp_y += dy

        game_logic.possible_moves.extend(valid)
        game_logic.turn = Turn.MOVE
        return False

class Faun(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Faun"
        self.rule = pygame.image.load("Assets/faun_opis.jpg")

    def check_win_condition(self, game_logic):
        if game_logic.chosen_piece and game_logic.chosen_piece.moved:
            piece = game_logic.chosen_piece
            if game_logic.board[piece.prev_x][piece.prev_y].height - game_logic.board[piece.x][piece.y].height >= 2:
                return True
        return False