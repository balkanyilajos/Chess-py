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

    def _getAdjacentCoords(self) -> list[tuple[int,int]]:
        return [(1+self._x, 0+self._y), (-1+self._x, 0+self._y), (0+self._x, 1+self._y), (0+self._x, -1+self._y),
                (1+self._x, 1+self._y), (-1+self._x, -1+self._y), (1+self._x, -1+self._y), (-1+self._x, 1+self._y)]

    def getMoveablePositions(self) -> list[tuple[int, int]]:
        coords = self._getAdjacentCoords()
        counter = 0
        for i in range(len(coords)-1, -1, -1):
            coord = coords[i]
            x, y = coord
            isKingAddedToBoard = False
            # adds kings to empty cells
            if self._chess.isValidCoordinate(x, y):
                if self._chess.isTableCellEmpty(x, y):
                    self._chess.addPieceToTable(King(self._chess, x, y, self._player, self._image), x, y, modifyCoordsInPiece=False)
                    isKingAddedToBoard = True
            else:
                del coords[i]
                continue
            
            #checks if it can be stepped
            for piece in self._chess.getBoardGenerator():
                if isinstance(piece, King):
                    if not self.isOwnedBySamePlayer(piece) and \
                    abs(piece.x-x) <= 1 and abs(piece.y-y) <= 1:
                        del coords[i]
                        break
                else:
                    if self.isOwnedBySamePlayer(piece):
                        if abs(piece.x-x) == 0 and abs(piece.y-y) == 0:
                            del coords[i]
                            break
                    elif piece.isMoveable(x, y):
                        del coords[i]
                        break
                        
            # removes kings from empty cells
            if isKingAddedToBoard:
                self._chess.deletePieceFromTable(x, y)
                counter += 1

        return coords

class BlackKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.BLACK, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "black_king.svg")), (size, size)) )

class WhiteKing(King):
    def __init__(self, chess: Chess, x: int, y: int, size: int):
        super().__init__(chess, x, y, Players.WHITE, pygame.transform.smoothscale(pygame.image.load(os.path.join("data", "white_king.svg")), (size, size)) )
