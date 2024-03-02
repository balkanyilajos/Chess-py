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

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = []
        directions = [(2,1), (-2,1), (2,-1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for x,y in directions:
            x += self._x
            y += self._y
            if self._chess.isValidCoordinate(x,y) and (self._chess.isTableCellEmpty(x,y) \
               or not self._chess.isRoundOfCurrentPlayer(self._chess.getBoardPiece(x,y).player)):
                coords.append((x,y))

        return coords

class BlackKnight(Knight):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_knight.svg")), (size, size)) )

class WhiteKnight(Knight):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_knight.svg")), (size, size)) )
