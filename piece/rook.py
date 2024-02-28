from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Chess

class Rook(Piece):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(chess, x, y, player, image)

    def isMoveable(self, indexX: int, indexY: int) -> bool:
        if not super().isMoveable(indexX, indexY):
            return False
        return True

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = self._getCoords(1, 0, self._chess.BOARD_SIZE)
        coords += self._getCoords(-1, 0, self._chess.BOARD_SIZE)
        coords += self._getCoords(0, 1, self._chess.BOARD_SIZE)
        coords += self._getCoords(0, -1, self._chess.BOARD_SIZE)
        return coords

class BlackRook(Rook):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_rook.svg")), (size, size)) )

class WhiteRook(Rook):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_rook.svg")), (size, size)) )
