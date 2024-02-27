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

    def isMoveable(self, indexX: int, indexY: int) -> bool:
        if not super().isMoveable(indexX, indexY):
            return False
        print(self.getMoveablePositions())
        diffY = abs(indexY - self._y)
        diffX = abs(indexX - self._x)
        returnValue = False

        if self._chess.isMovingForward(self, indexY):
            if indexX == self._x:
                if self._isInTheOriginalField and diffY == 2:
                    returnValue = self._chess.isTableCellEmpty(indexX, indexY-1) and self._chess.isTableCellEmpty(indexX, indexY)
                else:
                    returnValue = diffY == 1 and self._chess.isTableCellEmpty(indexX, indexY)
            elif diffY == 1 and diffX == 1:
                returnValue = not self._chess.isTableCellEmpty(indexX, indexY)
        
        if returnValue:
            self._isInTheOriginalField = False

        return returnValue

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        points = [(self.x-1, self.y), (self.x+1, self.y), (self.x, self.y-1), (self.x, self.y+1),
                  (self.x-2, self.y), (self.x+2, self.y), (self.x, self.y-2), (self.x, self.y+2),
                  (self.x-1, self.y-1), (self.x+1, self.y+1), (self.x+1, self.y-1), (self.x-1, self.y+1)]
        for i in range(len(points)-1, -1, -1):
            if not self._chess.isValidCoordinate(*points[i]) \
               or not self._chess.isMovingForward(self, points[i][1]):
                del points[i]
        return points

class BlackPawn(Pawn):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_pawn.svg")), (size, size))
        super().__init__(chess, x, y, Players.BLACK, image)


class WhitePawn(Pawn):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        image = pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_pawn.svg")), (size, size))
        super().__init__(chess, x, y, Players.WHITE, image)
