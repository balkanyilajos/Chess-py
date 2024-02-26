from enums import Players
from pygame import Surface
from enums import Players
from .piece import Piece
import pygame
import os

class Pawn(Piece):
    def __init__(self, table, x: int, y: int, player: Players, image: Surface):
        super().__init__(table, x, y, player, image)

    def move(self, indexX: int, indexY: int):
        pass

class BlackPawn(Pawn):
    def __init__(self, table, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_pawn.svg")), (size, size))
        super().__init__(table, x, y, Players.BLACK, image)

class WhitePawn(Pawn):
    def __init__(self, table, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_pawn.svg")), (size, size))
        super().__init__(table, x, y, Players.WHITE, image)
