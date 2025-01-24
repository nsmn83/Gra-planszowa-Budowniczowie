import pygame
from pionek import Pionek

class Gracz():
    def __init__(self, img):
        self.nazwa = None
        self.img = img
        self.pionki = [Pionek(img), Pionek(img)]
