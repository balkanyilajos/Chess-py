from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Chess

class Knight(Piece):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(chess, x, y, player, image)

    def isMoveable(self, indexX: int, indexY: int) -> bool:
        if not super().isMoveable(indexX, indexY):
            return False
        
        diffX = abs(indexX - self._x)
        diffY = abs(indexY - self._y)
        return (diffX == 2 and diffY == 1) or (diffX == 1 and diffY == 2)

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        return []

class BlackKnight(Knight):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_knight.svg")), (size, size)) )

class WhiteKnight(Knight):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_knight.svg")), (size, size)) )
