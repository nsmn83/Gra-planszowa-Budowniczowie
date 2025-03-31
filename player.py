import pygame
from piece import Piece
from ability import Ability

class Player():
    def __init__(self, img: pygame.surface, id: int):

        #id gracza bedące jednoczesnie jego indeksem w tabeli gracze zwiekosznym o 1
        self.id = id
        self.img = img
        self.pieces = [Piece(self, img), Piece(self, img)]
        self.pieces_set = False
        self.ability = Ability()

    def assign_power(self, ability: Ability):
        self.ability = ability


