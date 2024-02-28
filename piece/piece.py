from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
import pygame

from enums import Players

if TYPE_CHECKING:
     from chess import Chess

class Piece(ABC):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface) -> None:
        self._chess = chess
        self._x = x
        self._y = y
        self._player = player
        self._image = image
        self._isInTheOriginalField = True

    @property
    def player(self) -> Players:
        return self._player
    
    @property
    def image(self) -> pygame.Surface:
        return self._image
    
    @property
    def x(self) -> int:
        return self._x
    
    @property 
    def y(self) -> int:
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @y.setter
    def y(self, value):
        self._y = value

    def _getCoords(self, directionX: int, directionY: int, maxMove: int):
        coords = []
        x = self._x + directionX
        y = self._y + directionY
        i = 0
        while i < maxMove and self._chess.isValidCoordinate(x, y):
            if self._chess.isTableCellEmpty(x, y):
                coords.append((x, y))
            else:
                if not self._chess.isPieceOfPlayer(self._chess.getBoardPiece(x, y).player):
                    coords.append((x, y))
                break
            y += directionY
            x += directionX
            i += 1

        return coords

    def isMoveable(self, indexX: int, indexY: int) -> bool:
        return (indexX, indexY) in self.getMoveablePositions()

    def hasSamePosition(self, indexX: int, indexY: int) -> bool:
        return self._x == indexX and self._y == indexY

    @abstractmethod
    def getMoveablePositions(self) -> list[tuple[int, int]]:
        pass
