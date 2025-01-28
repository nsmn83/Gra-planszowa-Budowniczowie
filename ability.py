from turn import Turn
import pygame


# Klasa Ability, bazowo kazda funkcja zwraca fałsz, klasy poszczegolnych bóstw zmieniaja dane funkcje, jesli
# moc tego wymaga (np. Artemis po pierwszym ruchu ma mozliwosc wykonania drugiego przed koncem tury)
class Ability:
    def __init__(self):
        self.name = "BRAK"
        self.rule = pygame.image.load("Assets/basic_opis.jpg")

    # Jesli dana moc nie zmienia ruchu, budowania itp, to zwroci False
    def checkMoves(self, gameLogic, piece, pos):
        return False

    def performMove(self, gameLogic, piece, x, y):
        return False

    def checkWinCondition(self, gameLogic):
        return False

    def performBuild(self, gameLogic, piece, x, y):
        return False


class Artemis(Ability):
    def __init__(self):
        super().__init__()
        self.name = "ARTEMIS"
        self.rule = pygame.image.load("Assets/artemis_opis.jpg")

    #Wykonanie ruchu ze sprawdzeniem czy jest to pierwszy czy drugi ruch
    def performMove(self, gameLogic, piece, x, y):

        if (x, y) in gameLogic.possibleMoves:
            xs, ys = gameLogic.chosenPiece.returnPiecePosition()
            gameLogic.board[xs][ys].deletePiece()
            gameLogic.chosenPiece.changePiecePosition(x, y)
            gameLogic.board[x][y].piece = gameLogic.chosenPiece
            gameLogic.checkWinConditions()
            gameLogic.possibleMoves = []
            if not gameLogic.chosenPiece.moved:
                gameLogic.chosenPiece.moved = True
                gameLogic.turn = Turn.CHECKMOVE
            else:
                gameLogic.checkWinConditions()
                if gameLogic.turn != Turn.ENDOFGAME:
                    gameLogic.turn = Turn.CHECKBUILD
        elif gameLogic.chosenPiece.moved:
            gameLogic.checkWinConditions()
            if gameLogic.turn != Turn.ENDOFGAME:
                gameLogic.turn = Turn.CHECKBUILD

    def checkMoves(self, gameLogic, piece, pos):
        x, y = pos
        valid_moves = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        gameLogic.board[pos[0]][pos[1]].height < gameLogic.board[x][y].height + 2 and
                        gameLogic.board[pos[0]][pos[1]].piece is None,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        gameLogic.possibleMoves.extend(valid_moves)
        prev_position = (piece.prevX, piece.prevY)
        if prev_position in gameLogic.possibleMoves and piece.moved:
            gameLogic.possibleMoves.remove(prev_position)

        # Jesli gracz sprawdza czy moze wykonac drugi ruch, lecz nie ma na niego miejsca to przechodzi do budowania
        if not gameLogic.possibleMoves and piece.moved:
            gameLogic.turn = Turn.CHECKBUILD
            return True
        gameLogic.turn = Turn.MOVE
        return True


class Apollo(Ability):
    def __init__(self):
        super().__init__()
        self.name = "APOLLO"
        self.rule = pygame.image.load("Assets/apollo_opis.jpg")

    def checkMoves(self, gameLogic, piece, pos):
        x, y = pos
        valid_moves = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        gameLogic.board[pos[0]][pos[1]].height < gameLogic.board[x][y].height + 2 and
                        (gameLogic.board[pos[0]][pos[1]].piece is None or gameLogic.board[pos[0]][
                            pos[1]].piece.owner != gameLogic.activePlayer),
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        gameLogic.possibleMoves.extend(valid_moves)
        gameLogic.turn = Turn.MOVE
        return True

    def performMove(self, gameLogic, piece, x, y):
        if (x, y) in gameLogic.possibleMoves:
            enemyPiece = None
            xs, ys = gameLogic.chosenPiece.returnPiecePosition()
            if gameLogic.board[x][y].piece and gameLogic.board[x][y].piece != gameLogic.activePlayer:
                enemyPiece = gameLogic.board[x][y].piece
                enemyPiece.changePiecePosition(xs, ys)
            gameLogic.board[xs][ys].piece = enemyPiece
            gameLogic.chosenPiece.changePiecePosition(x, y)
            gameLogic.board[x][y].piece = gameLogic.chosenPiece
            gameLogic.chosenPiece.moved = True
            gameLogic.checkWinConditions()
            gameLogic.possibleMoves = []
            if gameLogic.turn != Turn.ENDOFGAME:
                gameLogic.possibleMoves = []
                gameLogic.turn = Turn.CHECKBUILD


class Atlas(Ability):
    def __init__(self):
        super().__init__()
        self.name = "ATLAS"
        self.rule = pygame.image.load("Assets/atlas_opis.jpg")

    def performBuild(self, gameLogic, piece, x, y):
        if (x, y) in gameLogic.possibleBuildingSites and piece.build is False:
            gameLogic.board[x][y].height += 1
            gameLogic.possibleBuildingSites = []
            gameLogic.turn = Turn.ENDOFTURN
            piece.build = False
            piece.moved = False
        elif piece.build:
            if (x, y) in gameLogic.possibleBuildingSites:
                gameLogic.board[x][y].height = 4
                gameLogic.possibleBuildingSites = []
                gameLogic.turn = Turn.ENDOFTURN
                piece.build = False
                piece.moved = False
        else:
            piece.build = True


class Demeter(Ability):
    def __init__(self):
        super().__init__()
        self.name = "DEMETER"
        self.rule = pygame.image.load("Assets/demeter_opis.jpg")

    def performBuild(self, gameLogic, piece, x, y):
        if (x, y) in gameLogic.possibleBuildingSites and not piece.build:
            gameLogic.board[x][y].height += 1
            piece.build = True
            gameLogic.possibleBuildingSites.remove((x, y))
        elif piece.build:
            if (x, y) in gameLogic.possibleBuildingSites:
                gameLogic.board[x][y].height += 1
            gameLogic.possibleBuildingSites = []
            piece.build = False
            gameLogic.turn = Turn.ENDOFTURN
            gameLogic.chosenPiece.moved = False


class Hefajstos(Ability):
    def __init__(self):
        super().__init__()
        self.name = "HEFAJSTOS"
        self.rule = pygame.image.load("Assets/hefajstos_opis.jpg")

    def performBuild(self, gameLogic, piece, x, y):
        if (x, y) in gameLogic.possibleBuildingSites and not piece.build:
            gameLogic.board[x][y].height += 1
            piece.build = True
            gameLogic.possibleBuildingSites = [(x, y)]
            if gameLogic.board[x][y].height >= 3:
                piece.build = False
                gameLogic.turn = Turn.ENDOFTURN
                gameLogic.chosenPiece.moved = False
                gameLogic.possibleBuildingSites = []
        elif piece.build:
            if (x, y) in gameLogic.possibleBuildingSites:
                gameLogic.board[x][y].height += 1
            gameLogic.possibleBuildingSites = []
            piece.build = False
            gameLogic.turn = Turn.ENDOFTURN
            gameLogic.chosenPiece.moved = False
        return True


class Minotaur(Ability):
    def __init__(self):
        super().__init__()
        self.name = "MINOTAUR"
        self.rule = pygame.image.load("Assets/minotaur_opis.jpg")

    def checkMoves(self, gameLogic, piece, pos):
        x, y = pos
        valid_moves = []
        change = [-1, 0, 1]
        for dx in change:
            for dy in change:
                if dx == 0 and dy == 0:
                    continue
                tempX, tempY = x + dx, y + dy

                if 0 <= tempX <= 4 and 0 <= tempY <= 4:
                    tile = gameLogic.board[tempX][tempY]
                    if gameLogic.board[tempX][tempY].height <= gameLogic.board[x][y].height + 1:
                        if not tile.piece:
                            valid_moves.append((tempX, tempY))
                        elif tile.piece.owner != gameLogic.activePlayer:
                            behindX, behindY = tempX + dx, tempY + dy
                            if 0 <= behindY <= 4 and 0 <= behindX <= 4:
                                secondTile = gameLogic.board[behindX][behindY]
                                if secondTile.piece is None and secondTile.height < 4:
                                    valid_moves.append((tempX, tempY))

        gameLogic.possibleMoves.extend(valid_moves)
        gameLogic.turn = Turn.MOVE
        return True

    def performMove(self, gameLogic, piece, x, y):
        if (x, y) in gameLogic.possibleMoves:
            enemyPiece = None
            xs, ys = gameLogic.chosenPiece.returnPiecePosition()
            gameLogic.board[xs][ys].deletePiece()
            dx, dy = x - xs, y - ys
            if gameLogic.board[x][y].piece:
                enemyPiece = gameLogic.board[x][y].piece
                enemyPiece.changePiecePosition(x + dx, y + dy)
                gameLogic.board[x + dx][y + dy].piece = enemyPiece
            gameLogic.chosenPiece.changePiecePosition(x, y)
            gameLogic.board[x][y].piece = gameLogic.chosenPiece
            gameLogic.chosenPiece.moved = True
            gameLogic.checkWinConditions()
            gameLogic.possibleMoves = []
            if gameLogic.turn != Turn.ENDOFGAME:
                gameLogic.possibleMoves = []
                gameLogic.turn = Turn.CHECKBUILD

class Hermes(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Hermes"
        self.rule = pygame.image.load("Assets/hermes_opis.jpg")

    def checkMoves(self, gameLogic, piece, pos):
        x, y = pos
        valid_moves = []
        change = [1, 0, -1]
        height = gameLogic.board[x][y].height
        for dx in change:
            for dy in change:
                tempX, tempY = x + dx, y + dy
                if dx == 0 and dy == 0:
                    continue
                while 0 <= tempX <= 4 and 0 <= tempY <= 4:
                    if gameLogic.board[tempX][tempY].height != height or gameLogic.board[tempX][tempY].piece:
                        break
                    valid_moves.append((tempX, tempY))
                    tempX += dx
                    tempY += dy

        gameLogic.possibleMoves.extend(valid_moves)
        gameLogic.turn = Turn.MOVE
        return False

class Faun(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Faun"
        self.rule = pygame.image.load("Assets/faun_opis.jpg")

    def checkWinCondition(self, gameLogic):
        if gameLogic.chosenPiece and gameLogic.chosenPiece.moved:
            piece = gameLogic.chosenPiece
            if gameLogic.board[piece.prevX][piece.prevY].height - gameLogic.board[piece.x][piece.y].height >= 2:
                return True
        return False