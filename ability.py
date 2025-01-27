from turn import Turn

class Ability:
    def __init__(self):
        self.name = "BRAK"

    #Jesli dana moc nie zmienia ruchu, budowania itp, to zwroci False
    def checkMoves(self, gameLogic, piece, pos):
        return False

    def checkBuild(self, gameLogic, piece, x, y):
        return False

    def performMove(self, gameLogic, piece, x, y):
        return False

    def performBuild(self, gameLogic, piece, x, y):
        return False

class Artemis(Ability):
    def __init__(self):
        super().__init__()
        self.name = "ARTEMIS"
    def performMove(self, gameLogic, piece, x, y):

        if (x, y) in gameLogic.possibleMoves:
            xs, ys = gameLogic.chosenPiece.returnPiecePosition()
            gameLogic.board[xs][ys].piece = None
            gameLogic.chosenPiece.changePiecePosition(x, y)
            gameLogic.board[x][y].piece = gameLogic.chosenPiece
            gameLogic.checkWinConditions()
            gameLogic.possibleMoves = []
            if(gameLogic.chosenPiece.moved == False):
                 gameLogic.chosenPiece.moved = True
                 gameLogic.turn = Turn.CHECKMOVE
            else:
                gameLogic.checkWinConditions()
                if gameLogic.turn != Turn.ENDOFGAME:
                    gameLogic.turn = Turn.CHECKBUILD
        elif gameLogic.chosenPiece.moved == True:
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
        print(gameLogic.possibleMoves)

        #Jesli gracz sprawdza czy moze wykonac drugi ruch, lecz nie ma na niego miejsca to przechodzi do budowania
        if gameLogic.possibleMoves == [] and piece.moved:
            gameLogic.turn = Turn.CHECKBUILD
            return True
        gameLogic.turn = Turn.MOVE
        return True

class Apollo(Ability):
    def __init__(self):
        super().__init__()
        self.name = "APOLLO"

    def checkMoves(self, gameLogic, piece, pos):
        x, y = pos
        valid_moves = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        gameLogic.board[pos[0]][pos[1]].height < gameLogic.board[x][y].height + 2,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        gameLogic.possibleMoves.extend(valid_moves)
        print(gameLogic.possibleMoves)
        for element in gameLogic.possibleMoves:
            x, y = element
            if gameLogic.board[x][y].piece:
                if gameLogic.board[x][y].piece.owner == gameLogic.activePlayer:
                    gameLogic.possibleMoves.remove(element)
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

    def performBuild(self, gameLogic, piece, x, y):
        if (x, y) in gameLogic.possibleBuildingSites and piece.build is False:
            gameLogic.board[x][y].height +=1
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
