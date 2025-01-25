import pygame
from piece import Piece

class Player():
    def __init__(self, img, id):

        #id gracza bedące jednoczesnie jego indeksem w tabeli gracze zwiekosznym o 1
        self.id = id
        self.img = img
        self.pieces = [Piece(self, img), Piece(self, img)]
        self.piecesSet = False
