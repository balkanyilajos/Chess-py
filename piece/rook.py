from enums import Players
from pygame import Surface
from enums import Players
from .piece import Piece
import pygame
import os

class Rook(Piece):
    def __init__(self, table, x: int, y: int, player: Players, image: Surface):
        super().__init__(table, x, y, player, image)

    def move(self, indexX: int, indexY: int):
        pass

class BlackRook(Rook):
    def __init__(self, table, x: int, y: int, size: int):
        super().__init__(table, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_rook.svg")), (size, size)) )

class WhiteRook(Rook):
    def __init__(self, table, x: int, y: int, size: int):
        super().__init__(table, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_rook.svg")), (size, size)) )
