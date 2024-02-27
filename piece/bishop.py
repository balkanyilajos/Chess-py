from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Chess

class Bishop(Piece):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(chess, x, y, player, image)

    def isMoveable(self, indexX: int, indexY: int) -> bool:
        if not super().isMoveable(indexX, indexY):
            return False
        
        diffY = abs(indexY - self._y)
        diffX = abs(indexX - self._x)

        return True

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        return []

class BlackBishop(Bishop):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_bishop.svg")), (size, size)) )

class WhiteBishop(Bishop):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_bishop.svg")), (size, size)) )
