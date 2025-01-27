import pygame
from piece import Piece
from ability import Ability, Artemis, Apollo, Atlas

class Player():
    def __init__(self, img, id):

        #id gracza bedące jednoczesnie jego indeksem w tabeli gracze zwiekosznym o 1
        self.id = id
        self.img = img
        self.pieces = [Piece(self, img), Piece(self, img)]
        self.piecesSet = False
        self.moce = None
        if self.id == 0:
            self.moc = Atlas("Atlas")
        if self.id == 1:
            self.moc = Artemis("Artemis")
        if self.id == 2:
            self.moc = Apollo("Apollo")