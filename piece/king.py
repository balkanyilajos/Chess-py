from enums import Players
from pygame import Surface
from enums import Players
from .piece import Piece
import pygame
import os

class King(Piece):
    def __init__(self, table, x: int, y: int, player: Players, image: Surface):
        super().__init__(table, x, y, player, image)

    def move(self, indexX: int, indexY: int):
        pass

class BlackKing(King):
    def __init__(self, table, x: int, y: int, size: int):
        super().__init__(table, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (size, size)) )

class WhiteKing(King):
    def __init__(self, table, x: int, y: int, size: int):
        super().__init__(table, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (size, size)) )
