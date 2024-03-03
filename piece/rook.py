from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Board

class Rook(Piece):
    def __init__(self, board: Board, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(board, x, y, player, image)

    def getMoveablePositions(self, recalculate:bool = False) -> list[tuple[int, int]]:
        if not recalculate:
            return self._moveablePositions
        
        self._moveablePositions = coords = self._getCoords(1, 0)
        coords += self._getCoords(-1, 0)
        coords += self._getCoords(0, 1)
        coords += self._getCoords(0, -1)
        return coords

class BlackRook(Rook):
    def __init__(self, board: Board, x: int, y: int, size: int):
        super().__init__(board, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_rook.svg")), (size, size)) )

class WhiteRook(Rook):
    def __init__(self, board: Board, x: int, y: int, size: int):
        super().__init__(board, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_rook.svg")), (size, size)) )
