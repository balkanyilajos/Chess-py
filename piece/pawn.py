from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

from enums import Players
from piece.piece import Piece

if TYPE_CHECKING:
     from chess import Board

class Pawn(Piece):
    def __init__(self, board: Board, x: int, y: int, player: Players, image: pygame.Surface):
        super().__init__(board, x, y, player, image)
        self._isInTheOriginalField = True
        self._enPassant = False
        self._enPassantCoords = []

        self._upCoord = (0, 0)
        self._leftCoord = (0, 0)
        self._rightCoord = (0, 0)
        self._downCoord = (0, 0)

    @property
    def x(self) -> int:
        return self._x
    
    @property 
    def y(self) -> int:
        return self._y
    
    @x.setter
    def x(self, value):
        self._enPassant = False
        if self._isInTheOriginalField and self._x != value:
             self._enPassant = True
             self._isInTheOriginalField = False
        self._x = value
        if (self._x, self._y) in self._enPassantCoords:
            self._board.deletePieceFromTable(self._x-self._downCoord[0], self._y-self._downCoord[1])
    
    @y.setter
    def y(self, value):
        self._enPassant = False
        if self._isInTheOriginalField and self._y != value:
             self._enPassant = True
             self._isInTheOriginalField = False
        self._y = value
        if (self._x, self._y) in self._enPassantCoords:
            self._board.deletePieceFromTable(self._x-self._downCoord[0], self._y-self._downCoord[1])

    def getMoveablePositions(self, recalculate:bool = False) -> list[tuple[int, int]]:
        if not recalculate:
            return self._moveablePositions
        
        self._moveablePositions = coords = []
        self._enPassantCoords = []
        #calculate the up coords
        x = self._x
        y = self._y
        rangeTo = 3 if self._isInTheOriginalField else 2
        for _ in range(1, rangeTo):
            x += self._upCoord[0]
            y += self._upCoord[1]
            if self._board.isValidCoordinate(x,y) and self._board.isTableCellEmpty(x,y):
                coords.append((x, y))
            else:
                break

        #calculate the side up coords
        x = self._x + self._upCoord[0]
        y = self._y + self._upCoord[1]
        sideUpCoords = [(x + self._leftCoord[0], y + self._leftCoord[1]), (x + self._rightCoord[0], y + self._rightCoord[1])]
        for x, y in sideUpCoords:
            if self._board.isValidCoordinate(x,y) and not self._board.isTableCellEmpty(x,y) \
               and not self.isOwnedBySamePlayer(self._board.getBoardPiece(x,y)):
                coords.append((x,y))

        #calculate en passant
        sideCoords = [(self._x + self._leftCoord[0], self._y + self._leftCoord[1]), (self._x + self._rightCoord[0], self._y + self._rightCoord[1])]
        for x, y in sideCoords:
            if self._board.isValidCoordinate(x,y):
               sidePiece = self._board.getBoardPiece(x,y)
               if isinstance(sidePiece, Pawn) and not self.isOwnedBySamePlayer(sidePiece) \
                  and sidePiece._enPassant:
                   sidePiece._enPassant = False
                   newCoord = (x+self._upCoord[0], y+self._upCoord[1])
                   self._enPassantCoords.append(newCoord)
                   if newCoord not in coords:
                       coords.append(newCoord)

        return coords

class BlackPawn(Pawn):
    def __init__(self, board: Board, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_pawn.svg")), (size, size))
        super().__init__(board, x, y, Players.BLACK, image)
        self._upCoord = (0, 1)
        self._downCoord = (0, -1)
        self._leftCoord = (1, 0)
        self._rightCoord = (-1, 0)

class WhitePawn(Pawn):
    def __init__(self, board: Board, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_pawn.svg")), (size, size))
        super().__init__(board, x, y, Players.WHITE, image)
        self._upCoord = (0, -1)
        self._downCoord = (0, -1)
        self._leftCoord = (1, 0)
        self._rightCoord = (-1, 0)