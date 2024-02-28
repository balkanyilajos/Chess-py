from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Chess

class King(Piece):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(chess, x, y, player, image)

    def isMoveable(self, indexX: int, indexY: int) -> bool:
        if not super().isMoveable(indexX, indexY):
            return False
        
        diffX = abs(indexX - self._x)
        diffY = abs(indexY - self._y)
        return diffX in (1, 0) and diffY in (1, 0)

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = self._getCoords(1, 0, 1)
        coords += self._getCoords(-1, 0, 1)
        coords += self._getCoords(0, 1, 1)
        coords += self._getCoords(0, -1, 1)
        coords += self._getCoords(1, 1, 1)
        coords += self._getCoords(-1, -1, 1)
        coords += self._getCoords(1, -1, 1)
        coords += self._getCoords(-1, 1, 1)
        return coords

class BlackKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (size, size)) )

class WhiteKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (size, size)) )
