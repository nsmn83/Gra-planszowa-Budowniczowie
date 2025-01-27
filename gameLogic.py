import pygame
from player import Player
from turn import Turn
from tile import Tile

class gameLogic:
    def __init__(self):
        pygame.init()
        self.turn = Turn.SETUP
        self.activePlayer = None
        self.chosenPiece = None
        self.numberOfPlayers = 2
        self.players = []
        self.possibleMoves = []
        self.possibleBuildingSites = []
        self.board = [[Tile() for _ in range(5)] for _ in range(5)]

    # Dodanie graczy
    def addPlayers(self):
        for element in range(self.numberOfPlayers):
            img = f"Pictures/player{element+1}.png"
            img = pygame.image.load(img)
            player = Player(img, element)
            self.players.append(player)
        self.activePlayer = self.players[0]

    # Zmiana liczby graczy biorących udzaił w rozgrywce
    def setNumOfPlayers(self, numOfPlayers):
        self.numberOfPlayers = numOfPlayers

    #Funkcja do zmiany aktualnego gracza na nastepnego
    def switchPlayer(self):
        if self.chosenPiece:
            self.chosenPiece.moved = False
        self.activePlayer = self.players[(self.players.index(self.activePlayer) + 1) % len(self.players)]
        print("Obecny gracz: ", self.activePlayer.id)
        if self.checkIfBlocked():
            print("Obecny gracz: ", self.activePlayer.id)
        return self.activePlayer

    #Pętla oblsugujaca tury graczy
    def handleActions(self, x, y):
        # Pierwsza faza gry - rozstawiamy pionki dopoki kazdy nie bedzie mial ich na planszy
        if self.turn == Turn.SETUP:
            self.setup(x, y)
            return

        # Jesli pionek nie jest wybrany, aktywny gracz wybiera swojego pionka
        if self.chosenPiece is None:
            self.chosenPiece = self.returnPiece(x, y)
            print(f"Gracz wybrał pionka ({x}, {y})")

        elif self.chosenPiece is not None and self.chosenPiece.moved == False:
            if self.board[x][y].piece and self.board[x][y].piece.owner == self.activePlayer:
                self.chosenPiece = self.board[x][y].piece
                self.possibleMoves = []
                self.turn = Turn.CHECKMOVE

        if self.chosenPiece:
            if (self.turn == Turn.BUILD):
                self.performBuild(x, y)
                print(f"Gracz {self.activePlayer.id} zbudowal pietro")

            elif (self.turn == Turn.MOVE):
                self.performMove(x, y)
                print(f"Gracz {self.activePlayer.id} wykonal ruch")

            if (self.turn == Turn.CHECKBUILD):
                self.checkBuild()
                print(f"Gracz {self.activePlayer.id} - sprawdzenie pol pod budowanie")

            if self.chosenPiece and self.turn == Turn.CHECKMOVE:
                self.checkMoves(self.chosenPiece)
                print(f"Gracz {self.activePlayer.id} - sprawdzenie pol pod ruch")

            if self.turn == Turn.ENDOFTURN:
                print(f"Gracz {self.activePlayer.id} konczy swoja ture")
                self.chosenPiece = None
                self.activePlayer = self.switchPlayer()
                print(f"GRACZ {self.activePlayer.id} ZACZYNA TURE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.turn = Turn.CHECKMOVE

            self.checkWinConditions()

    # Funkcja służąca ustawieniu pionktów na początku rozgrywki
    def setup(self, x, y):
        if self.board[x][y].isBlocked():
            print("Wybrano pole, które jest już zajęte!")
            return
        for piece in self.activePlayer.pieces:
            if not piece.returnPiecePosition():
                self.changePosition(x, y, piece)
                print(f"Gracz {self.activePlayer.id} ustawił swojego pionka na polu ({x}, {y})")
                if(self.activePlayer.pieces[1] == piece):
                    self.activePlayer.piecesSet = True
                    self.switchPlayer()
                    if self.activePlayer.piecesSet:
                        print("Gracze rozstawili swoje pionki")
                        self.turn = Turn.CHECKMOVE
                return


    #Sprawdzenie mozliwych pol dow wykonania ruchu
    def checkMoves(self, piece):
        pos = piece.returnPiecePosition()
        if pos is None:
            print("Pionek nie jest jeszcze ustawiony")
            return
        x, y = pos
        if self.activePlayer.moc.checkMoves(self, piece, pos):
            return
        valid_moves = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        self.board[pos[0]][pos[1]].height < self.board[x][y].height + 2 and
                        self.board[pos[0]][pos[1]].piece is None,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        self.possibleMoves.extend(valid_moves)
        self.turn = Turn.MOVE

    #Sprawdzenie mozliwych pol do wykonania budowy
    def checkBuild(self):
        x, y = self.chosenPiece.returnPiecePosition()
        valid_sites = filter(
            lambda pos: 0 <= pos[0] < 5 and 0 <= pos[1] < 5 and
                        self.board[pos[0]][pos[1]].height < 4 and
                        self.board[pos[0]][pos[1]].piece is None,
            [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        )
        self.possibleBuildingSites.extend(valid_sites)

        if self.possibleBuildingSites == []:
            print("Gracz nie moze budowac w swojej turze")
            loser = self.activePlayer
            for piece in loser.pieces:
                x, y = piece.returnPiecePosition()
                self.board[x][y].deletePiece()
            self.activePlayer = self.players[(self.players.index(self.activePlayer) + 1) % len(self.players)]
            self.players.remove(loser)
            self.chosenPiece = None
            self.turn = Turn.CHECKMOVE
            return

        self.turn = Turn.BUILD


    def changePosition(self, x, y, piece):
        if piece.returnPiecePosition():
            self.board[piece.x][piece.y].deletePiece()
        piece.changePiecePosition(x, y)
        self.board[x][y].piece = piece

    #Wykoananie ruchu
    def performMove(self, x, y):
        if self.activePlayer.moc.performMove(self, self.chosenPiece, x, y):
            return
        if (x, y) in self.possibleMoves:
            xs, ys = self.chosenPiece.returnPiecePosition()
            self.board[xs][ys].piece = None
            self.chosenPiece.changePiecePosition(x, y)
            self.chosenPiece.moved = True
            self.board[x][y].piece = self.chosenPiece
            self.possibleMoves = []
            self.checkWinConditions()
            if self.turn != Turn.ENDOFGAME:
                self.turn = Turn.CHECKBUILD

    def performBuild(self, x, y):
        if self.activePlayer.moc.performBuild(self, self.chosenPiece, x, y):
            return
        if (x, y) in self.possibleBuildingSites:
            self.board[x][y].height += 1
            self.possibleBuildingSites = []
            self.turn = Turn.ENDOFTURN
            self.chosenPiece.moved = False

    def checkWinConditions(self):
        if (self.chosenPiece and self.board[self.chosenPiece.x][self.chosenPiece.y].height == 3
        or len(self.players) == 1):
            print("Gracz ", self.activePlayer.id, " wygrał grę")
            self.turn = Turn.ENDOFGAME
            return

    # Na początku tury gracz sprawdza, czy moze wykonac ruch, jesli nie, to jest usuwany z gry
    def checkIfBlocked(self):

        if not self.activePlayer.piecesSet:
            return False
        for piece in self.activePlayer.pieces:
            self.checkMoves(piece)
        if self.possibleMoves:
            self.possibleMoves = []
            return False

        print("Gracz ma zablokowane wszystkie ruchy")
        loser = self.activePlayer
        for piece in loser.pieces:
            x, y = piece.returnPiecePosition()
            self.board[x][y].deletePiece()
        self.activePlayer = self.players[(self.players.index(self.activePlayer) + 1) % len(self.players)]
        self.players.remove(loser)
        return True

    def returnPiece(self, x, y):
        if self.activePlayer is None:
            print("Brak aktualnego gracza!")
            return None
        for piece in self.activePlayer.pieces:
            if (piece.x, piece.y) == (x, y):
                return piece
        return None

    def drawGameState(self, surface):
        self.drawBoard(surface)
        self.drawPieces(surface)
        self.drawMoves(surface)

    def drawBoard(self, surface):
        for row in range(0, 5):
            for col in range(0, 5):
                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(row * 150, col * 150, 150, 150), 1)
                height = self.board[row][col].height
                if 1 <= height <=4:
                    floor_img = pygame.image.load(f"Pictures/ptr{height}.png")
                    floor_img = pygame.transform.scale(floor_img, (150, 150))
                    surface.blit(floor_img, (row * 150, col * 150))

    def drawMoves(self, surface):
        for (x, y) in self.possibleMoves:
            pygame.draw.circle(surface, (0, 255, 0, 255), (x*150+75, y*150+75), radius=74, width=5)

        for (x, y) in self.possibleBuildingSites:
            color = (255, 255, 0, 255)
            if(self.chosenPiece.build == True):
                color = (0,0,255,255)
            pygame.draw.circle(surface, color, (x*150+75, y*150+75), radius=74, width=5)

    def drawPieces(self, surface):
        for player in self.players:
            for piece in player.pieces:
                if piece.returnPiecePosition():
                    x = piece.x * 150
                    y = piece.y * 150
                    piece.drawPiece(surface)
                    if player == self.activePlayer and self.chosenPiece is None and self.turn != Turn.SETUP:
                        pygame.draw.circle(surface, (255, 255, 255), (x + 75, y + 75), 74, width=5)
