from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
import pygame

from enums import Players

if TYPE_CHECKING:
     from chess import Board

class Piece(ABC):
    def __init__(self, board: Board, x: int, y: int, player: Players, image: pygame.Surface) -> None:
        self._board = board
        self._x = x
        self._y = y
        self._player = player
        self._image = image
        self._moveablePositions = []

    @property
    def player(self) -> Players:
        return self._player
    
    @property
    def image(self) -> pygame.Surface:
        return self._image
    
    @property
    def moveablePositions(self) -> list[tuple[int, int]]:
        return self._moveablePositions

    @property
    def x(self) -> int:
        return self._x
    
    @property 
    def y(self) -> int:
        return self._y

    @moveablePositions.setter
    def moveablePositions(self, value):
        self._moveablePositions = value

    @x.setter
    def x(self, value):
        self._x = value
    
    @y.setter
    def y(self, value):
        self._y = value

    def _getCoords(self, directionX: int, directionY: int, maxMove: int = None) -> list[tuple[int, int]]:
        if maxMove is None:
            maxMove = self._board.WIDTH if self._board.WIDTH > self._board.HEIGHT else self._board.HEIGHT
            
        coords = []
        x = self._x + directionX
        y = self._y + directionY
        i = 0
        while i < maxMove and self._board.isValidCoordinate(x, y):
            if self._board.isTableCellEmpty(x, y):
                coords.append((x, y))
            else:
                if not self.isOwnedBySamePlayer(self._board.getBoardPiece(x, y)):
                    coords.append((x, y))
                break
            y += directionY
            x += directionX
            i += 1

        return coords

    def isMoveable(self, indexX: int, indexY: int, recalculate: bool = False) -> bool:        
        return (indexX, indexY) in self.getMoveablePositions(recalculate=recalculate)
    
    def isOwnedBySamePlayer(self, other: Piece):
        return self._player == other._player 

    def hasSamePosition(self, indexX: int, indexY: int) -> bool:
        return self._x == indexX and self._y == indexY

    @abstractmethod
    def getMoveablePositions(self, recalculate: bool = False) -> list[tuple[int, int]]:
        pass