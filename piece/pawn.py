from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Chess

class Pawn(Piece):
    def __init__(self, chess: Chess, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(chess, x, y, player, image)
        self.upCoords = []
        self.sideCoords = []

    @property
    def x(self) -> int:
        return self._x
    
    @property 
    def y(self) -> int:
        return self._y
    
    @x.setter
    def x(self, value):
        if self._isInTheOriginalField and self._x != value:
             self._isInTheOriginalField = False
             self.upCoords.pop()
        self._x = value
    
    @y.setter
    def y(self, value):
        if self._isInTheOriginalField and self._y != value:
             self._isInTheOriginalField = False
             self.upCoords.pop()
        self._y = value

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = []
        for x, y in self.upCoords:
            x += self._x
            y += self._y
            if self._chess.isValidCoordinate(x,y):
                if self._chess.isTableCellEmpty(x,y):
                   coords.append((x,y))
                else:
                    break
            
        for x, y in self.sideCoords:
            x += self._x
            y += self._y

            if self._chess.isValidCoordinate(x,y) and not self._chess.isTableCellEmpty(x,y) \
               and not self._chess.isPieceOfPlayer(self._chess.getBoardPiece(x,y).player):
                coords.append((x,y))
        
        return coords

class BlackPawn(Pawn):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_pawn.svg")), (size, size))
        super().__init__(chess, x, y, Players.BLACK, image)
        self.upCoords = [(0, 1), (0, 2)]
        self.sideCoords = [(1, 1), (-1, 1)]

class WhitePawn(Pawn):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_pawn.svg")), (size, size))
        super().__init__(chess, x, y, Players.WHITE, image)
        self.upCoords = [(0, -1), (0, -2)]
        self.sideCoords = [(1, -1), (-1, -1)]
