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

    def _getAdjacentCoords(self) -> set[tuple[int,int]]:
        return {(1+self._x, 0+self._y), (-1+self._x, 0+self._y), (0+self._x, 1+self._y), (0+self._x, -1+self._y),
                (1+self._x, 1+self._y), (-1+self._x, -1+self._y), (1+self._x, -1+self._y), (-1+self._x, 1+self._y)}

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = self._getAdjacentCoords()
        for cell in self._chess.getBoardGenerator():
            if isinstance(cell, King) and not self._chess.isPieceOfPlayer(cell.player):
                    coords -= cell._getAdjacentCoords()
            elif isinstance(cell, Piece):
                if self._chess.isPieceOfPlayer(cell.player):
                    coords.discard((cell.x, cell.y))
                else:
                    for coord in cell.getMoveablePositions():
                        coords.discard(coord) 

        return list(coords)

class BlackKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (size, size)) )

class WhiteKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (size, size)) )
